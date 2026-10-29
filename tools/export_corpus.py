#!/usr/bin/env python3
"""Dry-run export of explicitly allowlisted, merged public corpus bytes.

This produces a candidate bundle for a downstream indexer. It never writes to
Scrutator, advances a serving generation, or claims KC2 admission.

Trust root (DEC-AUP-0171): an allowlist row is exported only if a matching
publication decision line sits in an append-only decision file under
``corpus/publication-decisions/`` on the pinned main, introduced by a merge-commit
pull request before the row, with a receipt that binds two or more unanimous blind
agent reviews to the reviewed head and diff digest. The reviews run under the same
account and model family as the writer; the manifest says so
(``reviewer_identity_class``) and nothing here proves independence, identity or
copyright.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib

REPO = Path(__file__).resolve().parents[1]
SOURCE = "Arcanada-one/knowledge-contract"
HEADER = "| Source commit | Path | Content SHA-256 | Author/rights holder | License | Publication decision | Status | Supersedes | Status decision |"
SCHEMA = "KnowledgeContractCandidateExport/v2"
PATH_RE = re.compile(r"^(papers|spec|articles|schemas)/[A-Za-z0-9][A-Za-z0-9_./-]*\.md$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
DEC_DIR = "corpus/publication-decisions/"
RECEIPT_DIR = DEC_DIR + "receipts/"
DECISION_REF_RE = re.compile(r"^(corpus/publication-decisions/[A-Za-z0-9][A-Za-z0-9_-]*\.jsonl)@([0-9a-f]{40})#([0-9a-f]{64})$")
RECEIPT_RE = re.compile(r"^corpus/publication-decisions/receipts/([A-Za-z0-9][A-Za-z0-9_-]*)\.json$")
DECISION_SCHEMA = "KnowledgeContractPublicationDecision/v2"
DECISION_KEYS = frozenset(("schema", "path", "sha256", "rights_holder", "license", "status", "upstream",
                           "rights_basis", "third_party", "attribution", "limits", "receipt"))
DECISION_TEXT_KEYS = ("rights_holder", "upstream", "rights_basis", "third_party", "attribution", "limits")
RECEIPT_KEYS = frozenset(("reviewed_head", "base", "diff_sha256", "decision_lines_sha256", "reviewers"))
# The only files the decision tree may hold. Batch names use [A-Za-z0-9_-] only: no dots, no case tricks, no subdirectories.
BATCH = r"[A-Za-z0-9][A-Za-z0-9_-]*"
TREE_LAYOUT = (
    re.compile(rf"corpus/publication-decisions/{BATCH}\.jsonl"),
    re.compile(rf"corpus/publication-decisions/receipts/{BATCH}\.json"),
    re.compile(rf"corpus/publication-decisions/receipts/{BATCH}/reviewer-[1-9][0-9]*\.(?:md|input\.txt)"),
)
UPSTREAM_RE = re.compile(r"^([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)@([0-9a-f]{40}):([A-Za-z0-9][A-Za-z0-9_./-]*)$")
PERSON_RE = re.compile(r"^[A-Z][A-Za-z.'-]+(?: [A-Z][A-Za-z.'-]+)+$")
REVIEWER_KEYS = frozenset(("session_id", "model", "input_digest", "transcript_sha256", "verdict"))
# Scope fixed by DEC-AUP-0171 item 7: only these six already-public documents may be listed until a later DEC changes it.
SCOPE_PATHS = frozenset((
    "articles/project-overview.md", "articles/openness-and-attribution-policy.md", "articles/attribution-policy.md",
    "articles/contribution-guide.md", "articles/sources-register.md", "articles/site-summary-llms.md",
))
DECLARATION_FILES = ("REUSE.toml", "NOTICE", "LICENSE")
MIN_REVIEWERS = 2
# The checklist every blind reviewer receives, pinned by digest so it cannot be weakened silently (DEC-AUP-0171 item 3).
CHECKLIST_TEXT = (
    "Fixed checklist for a blind publication review (DEC-AUP-0171):\n"
    "1. The sha256 of each listed blob equals the digest in its decision line.\n"
    "2. The upstream pointer and the license declarations (LICENSE, NOTICE, REUSE.toml, front matter) agree.\n"
    "3. The rights holder is a named person and rights_basis quotes the REUSE.toml holder string.\n"
    "4. No third-party text, marks, secrets, host paths, host names or addresses.\n"
    "5. The credit line is present.\n"
    "6. limits states what this review does not establish.\n"
    "Verdict: APPROVE only if every item holds.\n"
)
CHECKLIST_SHA256 = "c853f2c581ff831c5a2a4c141154e9c4f76594b55d0181403e068d992c01f3fe"
IDENTITY_CLASS = "same_account_blind_agent"
READBACK = "decision_file_matched"
ALLOWED_LICENSES = {"CC-BY-4.0", "Apache-2.0"}
# Transcripts, inputs and receipts are public: no host paths, private or carrier-grade addresses, or internal host names.
# Public domains and public addresses are not denied.
DENY_SHAPE = re.compile(
    rb"/home/|/Users/|/run/user/"
    rb"|\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    rb"|\b172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b"
    rb"|\b192\.168\.\d{1,3}\.\d{1,3}\b"
    rb"|\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b"
    rb"|\barcana-[A-Za-z0-9-]+|\b[A-Za-z0-9-]+\.ts\.net\b")
SECRET_SHAPE = re.compile(rb"(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|mun_sk_[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9]{20,}|vault_[A-Za-z0-9_-]{20,})")
MAX_BYTES = 1024 * 1024
NONE_CELLS = {"", "\u2014", "none"}


class ExportError(Exception):
    pass


def command(*args: str, data: bytes | None = None, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(args, cwd=REPO, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check and result.returncode:
        raise ExportError(f"{args[0]} operation failed with exit {result.returncode}")
    return result


def parse_allowlist(markdown: str) -> list[dict[str, str]]:
    lines = markdown.splitlines()
    try:
        start = lines.index(HEADER)
    except ValueError as error:
        raise ExportError("canonical allowlist header missing or changed") from error
    if start + 1 >= len(lines) or not re.fullmatch(r"\|(?:\s*-+\s*\|){9}", lines[start + 1]):
        raise ExportError("allowlist separator missing or malformed")
    entries: list[dict[str, str]] = []
    names = ("source_commit", "path", "sha256", "rights_holder", "license", "decision", "status", "supersedes", "status_decision")
    cursor = start + 2
    while cursor < len(lines):
        line = lines[cursor]
        if not line.strip():
            break
        if not line.startswith("|"):
            raise ExportError("allowlist table has an unmarked or malformed row")
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 9:
            raise ExportError("allowlist row must have nine cells")
        entries.append(dict(zip(names, cells, strict=True)))
        cursor += 1
    for line in lines[cursor + 1 :]:
        if line.lstrip().startswith("|") or line.count("|") >= 8:
            raise ExportError("row-like content appears after the allowlist table")
    return entries


def live_main() -> str:
    remote = command("git", "ls-remote", "origin", "refs/heads/main").stdout.decode().strip().split()
    if len(remote) != 2 or not SHA_RE.fullmatch(remote[0]) or remote[1] != "refs/heads/main":
        raise ExportError("live origin/main could not be pinned")
    command("git", "fetch", "--quiet", "origin", "main")
    fetched = command("git", "rev-parse", "FETCH_HEAD").stdout.decode().strip()
    if fetched != remote[0]:
        raise ExportError("main moved during source pinning; retry from a new snapshot")
    return fetched


def git_blob(commit: str, path: str, main_sha: str) -> bytes:
    if command("git", "merge-base", "--is-ancestor", commit, main_sha, check=False).returncode:
        raise ExportError("source commit is not merged into pinned main")
    tree = command("git", "ls-tree", commit, "--", path).stdout.decode().strip().split()
    if len(tree) != 4 or tree[0] not in {"100644", "100755"} or tree[1] != "blob" or tree[3] != path:
        raise ExportError("source path is missing, symlinked or not a regular blob")
    content = command("git", "show", f"{commit}:{path}").stdout
    if not content or len(content) > MAX_BYTES:
        raise ExportError("source blob is empty or exceeds the one MiB bound")
    return content


def secret_scan(content: bytes) -> None:
    if SECRET_SHAPE.search(content):
        raise ExportError("secret-shaped content quarantined")
    try:
        result = command("gitleaks", "stdin", "--no-banner", "--redact", data=content, check=False)
    except FileNotFoundError as error:
        raise ExportError("gitleaks unavailable; content quarantined") from error
    if result.returncode:
        raise ExportError("gitleaks could not clear content; content quarantined")


# --- GitHub API reads (injectable; tests replace these) -----------------------------------------

def gh_json(path: str):
    try:
        return json.loads(command("gh", "api", "--paginate", "repos/" + SOURCE + "/" + path).stdout)
    except (FileNotFoundError, ValueError) as error:
        raise ExportError("GitHub API read failed") from error


def pulls_for_commit(sha: str) -> list[dict]:
    value = gh_json("commits/" + sha + "/pulls")
    return value if isinstance(value, list) else []


def pull_info(number: int) -> dict:
    value = gh_json("pulls/" + str(number))
    return value if isinstance(value, dict) else {}


# --- row and decision validation ----------------------------------------------------------------

def validate_row(row: dict[str, str]) -> None:
    if not SHA_RE.fullmatch(row["source_commit"]):
        raise ExportError("source commit must be a full lowercase SHA")
    path = row["path"]
    if not PATH_RE.fullmatch(path) or ".." in Path(path).parts or "//" in path:
        raise ExportError("source path is outside the public corpus allowlist")
    if path not in SCOPE_PATHS:  # check: scope_paths
        raise ExportError("source path is outside the scope fixed by DEC-AUP-0171")
    if not DIGEST_RE.fullmatch(row["sha256"]):
        raise ExportError("content SHA-256 is missing or malformed")
    if not row["rights_holder"] or row["rights_holder"] in {"?", "unknown", "TBD"}:
        raise ExportError("rights holder is not established")
    if row["license"] not in ALLOWED_LICENSES:  # check: license_allowed
        raise ExportError("license is absent or outside reviewed project licenses")
    if not DECISION_REF_RE.fullmatch(row["decision"]):
        raise ExportError("publication decision must reference a decision file line digest")
    if row["status"] not in {"current", "superseded", "withdrawn"}:
        raise ExportError("publication status is unknown")
    if row["supersedes"] not in NONE_CELLS and not DIGEST_RE.fullmatch(row["supersedes"]):
        raise ExportError("superseded digest must be absent or a SHA-256")
    if row["status"] == "current" and row["status_decision"] not in NONE_CELLS:
        raise ExportError("current row must not have a later status decision")
    if row["status"] != "current" and not DECISION_REF_RE.fullmatch(row["status_decision"]):
        raise ExportError("non-current row needs a precise later status decision")


def canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def show(rev: str, path: str) -> str | None:
    result = command("git", "show", f"{rev}:{path}", check=False)
    return result.stdout.decode("utf-8", "replace") if result.returncode == 0 else None


def glob_match(pattern: str, path: str) -> bool:
    regex = ""
    i = 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            regex += ".*"
            i += 2
        elif pattern[i] == "*":
            regex += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            regex += "[^/]"
            i += 1
        else:
            regex += re.escape(pattern[i])
            i += 1
    return re.fullmatch(regex, path) is not None


def reuse_terms(commit: str, path: str) -> tuple[str, list[str]]:
    """The license REUSE.toml at `commit` assigns to `path` (override beats aggregate; ambiguity refuses)."""
    text = show(commit, "REUSE.toml")
    if text is None:
        raise ExportError("REUSE.toml is missing at the source commit")
    try:
        annotations = tomllib.loads(text).get("annotations")
    except tomllib.TOMLDecodeError as error:
        raise ExportError("REUSE.toml is not valid TOML") from error
    if not isinstance(annotations, list):
        raise ExportError("REUSE.toml has no annotations")
    hits: list[tuple[str, str, list[str]]] = []
    for annotation in annotations:
        patterns = annotation.get("path") if isinstance(annotation, dict) else None
        patterns = [patterns] if isinstance(patterns, str) else patterns
        if not isinstance(patterns, list) or not any(isinstance(p, str) and glob_match(p, path) for p in patterns):
            continue
        license_id = annotation.get("SPDX-License-Identifier")
        if not isinstance(license_id, str):
            raise ExportError("REUSE.toml annotation does not carry a single license identifier")
        holder = annotation.get("SPDX-FileCopyrightText", [])
        holders = [holder] if isinstance(holder, str) else [h for h in holder if isinstance(h, str)] if isinstance(holder, list) else []
        hits.append((str(annotation.get("precedence", "closest")), license_id, holders))
    overrides = [(license_id, holders) for precedence, license_id, holders in hits if precedence == "override"]
    if len(overrides) > 1:  # check: single_override
        raise ExportError("more than one REUSE.toml override matches the path")
    if overrides:
        return overrides[0]
    licenses = {license_id for _, license_id, _ in hits}
    if len(licenses) != 1:
        raise ExportError("REUSE.toml does not assign exactly one license to the path")
    return licenses.pop(), sorted({h for _, _, holders in hits for h in holders})


DECISION_FILE_RE = re.compile(r"corpus/publication-decisions/[A-Za-z0-9][A-Za-z0-9_-]*\.jsonl")


def check_write_once(main_sha: str) -> None:
    """The decision tree is write-once per file: a file is created in one commit and never modified, renamed or deleted."""
    revs = command("git", "log", "--first-parent", "--reverse", "--format=%H", main_sha, "--", DEC_DIR).stdout.decode().split()
    for rev in revs:
        if command("git", "rev-parse", "--verify", "--quiet", rev + "^1", check=False).returncode:
            continue
        status = command("git", "diff", "--no-renames", "--name-status", rev + "^1", rev, "--", DEC_DIR).stdout.decode().splitlines()
        if any(entry.partition("\t")[0] != "A" for entry in status):  # check: tree_write_once
            raise ExportError("decision tree is write-once: an existing file was modified, deleted or renamed")


def unique_merge_base(head: str, other: str) -> str:
    bases = command("git", "merge-base", "--all", head, other).stdout.decode().split()
    if len(bases) != 1:  # check: unique_merge_base
        raise ExportError("receipt base is ambiguous: more than one merge base")
    return bases[0]


def load_decisions(main_sha: str) -> list[dict]:
    """Every decision line of every decision file on the pinned main, validated strictly."""
    if command("git", "rev-parse", "--is-shallow-repository").stdout.decode().strip() != "false":  # check: full_history
        raise ExportError("history incomplete: shallow clone")
    check_write_once(main_sha)
    listing = command("git", "ls-tree", "-r", main_sha, "--", DEC_DIR).stdout.decode().splitlines()
    decisions: list[dict] = []
    seen_lines: set[str] = set()
    for entry in listing:
        meta, _, name = entry.partition("\t")
        mode, kind = meta.split()[:2]
        if not any(layout.fullmatch(name) for layout in TREE_LAYOUT):  # check: tree_layout
            raise ExportError("decision tree holds a file outside the allowed layout")
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ExportError("decision file is not a regular blob")
        if not DECISION_FILE_RE.fullmatch(name):
            continue
        for number, line in enumerate((show(main_sha, name) or "").splitlines()):
            try:
                obj = json.loads(line)
            except ValueError as error:
                raise ExportError("decision line malformed") from error
            if not isinstance(obj, dict) or set(obj) != DECISION_KEYS or canonical(obj) != line:  # check: strict_line
                raise ExportError("decision line malformed")
            if obj["schema"] != DECISION_SCHEMA or any(not isinstance(obj[k], str) or not obj[k].strip() for k in DECISION_TEXT_KEYS):  # check: mandatory_fields
                raise ExportError("decision line malformed: mandatory fields missing")
            if not PATH_RE.fullmatch(obj["path"]) or not DIGEST_RE.fullmatch(obj["sha256"]) or not RECEIPT_RE.fullmatch(obj["receipt"]):
                raise ExportError("decision line malformed")
            if obj["status"] not in {"current", "superseded", "withdrawn"} or obj["license"] not in ALLOWED_LICENSES:
                raise ExportError("decision line malformed")
            if obj["receipt"] != f"{RECEIPT_DIR}{Path(name).stem}.json":  # check: receipt_own_batch
                raise ExportError("decision line malformed: receipt names another batch")
            if command("git", "cat-file", "-e", f"{main_sha}:{obj['receipt']}", check=False).returncode:  # check: receipt_file_exists
                raise ExportError("decision line malformed: its receipt file is missing")
            if not PERSON_RE.fullmatch(obj["rights_holder"]) or "contributors" in obj["rights_holder"].lower():  # check: rights_holder_person
                raise ExportError("decision line malformed: rights holder is not a named person")
            parsed = UPSTREAM_RE.fullmatch(obj["upstream"])
            if obj["upstream"] != "original" and (parsed is None or parsed.group(1).lower().endswith(".git")):  # check: upstream_format
                raise ExportError("decision line malformed: upstream is neither original nor repo@commit:path")
            if line in seen_lines:  # check: repeat_line
                raise ExportError("decision line malformed: repeated line")
            seen_lines.add(line)
            decisions.append({"file": name, "no": number, "line": line,
                              "line_sha256": hashlib.sha256(line.encode()).hexdigest(), "obj": obj})
    return decisions


def tuple_of(obj: dict) -> tuple:
    return tuple(obj[k] for k in ("path", "sha256", "rights_holder", "license", "status"))


def first_parent_order(main_sha: str) -> dict[str, int]:
    revs = command("git", "rev-list", "--first-parent", "--reverse", main_sha).stdout.decode().split()
    return {rev: index for index, rev in enumerate(revs)}


def introducing_commit(main_sha: str, file: str, present) -> str:
    """First first-parent commit of main whose version of `file` satisfies `present` while its parent does not."""
    revs = command("git", "log", "--first-parent", "--reverse", "--format=%H", main_sha, "--", file).stdout.decode().split()
    for rev in revs:
        parent = command("git", "rev-parse", "--verify", "--quiet", rev + "^1", check=False)
        before = show(rev + "^1", file) if parent.returncode == 0 else None
        if present(show(rev, file) or "") and not present(before or ""):
            return rev
    raise ExportError("introducing commit not found on pinned main")


def latest_introducing_commit(main_sha: str, file: str, present) -> str:
    """The first-parent commit of main that most recently added the text (a removed and re-added row counts from the re-addition)."""
    revs = command("git", "log", "--first-parent", "--reverse", "--format=%H", main_sha, "--", file).stdout.decode().split()
    found = None
    for rev in revs:
        parent = command("git", "rev-parse", "--verify", "--quiet", rev + "^1", check=False)
        before = show(rev + "^1", file) if parent.returncode == 0 else None
        if present(show(rev, file) or "") and not present(before or ""):  # check: latest_row_addition
            found = rev
    if found is None:
        raise ExportError("introducing commit not found on pinned main")
    return found


def merged_pull(rev: str) -> int:
    prs = [pr for pr in pulls_for_commit(rev) if pr.get("merged_at") and pr.get("merge_commit_sha") == rev]
    if len(prs) != 1 or not isinstance(prs[0].get("number"), int):  # check: merged_pull_commit
        raise ExportError("commit is not a merged pull request commit")
    return prs[0]["number"]


def changed_paths(older: str, newer: str) -> list[str]:
    return command("git", "diff", "--no-renames", "--name-only", older, newer).stdout.decode().splitlines()


def is_ancestor(older: str, newer: str) -> bool:
    return command("git", "merge-base", "--is-ancestor", older, newer, check=False).returncode == 0


def rank(order: dict[str, int], d: dict) -> tuple:
    return (order[d["intro"]], d["file"].encode(), d["no"])


def find_decision(decisions: list[dict], order: dict[str, int], cell: str, row: dict[str, str], status: str) -> dict:
    """Among lines with the row's exact tuple the last counts; the cell must point at that line."""
    match = DECISION_REF_RE.fullmatch(cell)
    if match is None:
        raise ExportError("publication decision must reference a decision file, commit and line digest")
    want = tuple(({**row, "status": status})[k] for k in ("path", "sha256", "rights_holder", "license", "status"))
    found = sorted((d for d in decisions if tuple_of(d["obj"]) == want), key=lambda d: rank(order, d))
    if not found:  # check: tuple_match
        raise ExportError("no merged decision matches row")
    last = found[-1]
    if (last["file"], last["intro"], last["line_sha256"]) != match.groups():  # check: pointer_is_last
        raise ExportError("no merged decision matches row: the cell does not point at the last matching line")
    return last


def scan_public_text(content: bytes) -> None:
    if DENY_SHAPE.search(content):  # check: deny_scan
        raise ExportError("receipt or transcript carries a host path, host name or address")
    secret_scan(content)


def added_decision_lines(intro: str) -> list[str]:
    """The decision-file lines that `intro^1..intro` adds."""
    added: list[str] = []
    for name in changed_paths(intro + "^1", intro):
        if DECISION_FILE_RE.fullmatch(name):
            before = set((show(intro + "^1", name) or "").splitlines())
            added += [line for line in (show(intro, name) or "").splitlines() if line not in before]
    return added


def change_info(intro: str) -> dict:
    """Checks every decision-introducing commit; returns its pull request number, first parent and final head."""
    pr_number = merged_pull(intro)
    if any(not name.startswith(DEC_DIR) for name in changed_paths(intro + "^1", intro)):  # check: decision_commit_scope
        raise ExportError("decision commit edits more than decisions")
    parents = command("git", "rev-list", "--parents", "-n", "1", intro).stdout.decode().split()
    if len(parents) != 3:  # check: merge_commit_rule
        raise ExportError("head not recoverable: a decision pull request must be merged with a merge commit")
    if pull_info(pr_number).get("head", {}).get("sha") != parents[2]:  # check: head_matches_api
        raise ExportError("head not recoverable: merge commit does not carry the pull request head")
    for name in changed_paths(parents[1], intro):
        if not name.startswith(DEC_DIR):
            continue
        ours = command("git", "rev-parse", "--verify", "--quiet", f"{intro}:{name}", check=False).stdout.decode().strip()
        theirs = command("git", "rev-parse", "--verify", "--quiet", f"{parents[2]}:{name}", check=False).stdout.decode().strip()
        if ours != theirs:  # check: merge_no_evil
            raise ExportError("decision tree in the merge commit differs from the pull request head")
    return {"pr": pr_number, "first_parent": parents[1], "final_head": parents[2]}


def retained_record(main_sha: str, intro: str, head: str, final_head: str, path: str) -> bytes:
    """A receipt, input or transcript: introduced after the reviewed head by the decision change, never altered since."""
    if path not in changed_paths(head, final_head):  # check: retained_in_range
        raise ExportError("retained record was not introduced in the receipt commit range")
    if command("git", "cat-file", "-e", f"{head}:{path}", check=False).returncode == 0:  # check: retained_after_head
        raise ExportError("retained record already existed at the reviewed head")
    at_intro = command("git", "show", f"{intro}:{path}", check=False)
    at_main = command("git", "show", f"{main_sha}:{path}", check=False)
    if at_intro.returncode or at_main.returncode or at_intro.stdout != at_main.stdout:  # check: retained_unchanged
        raise ExportError("retained record changed after its decision change or is missing")
    return at_main.stdout


def upstream_commit(upstream: str, source: str) -> str | None:
    """Commit whose declarations the reviewers saw: the source commit for original text, the upstream commit for this repository, None for another repository."""
    if upstream == "original":
        return source
    repo, commit_, _ = UPSTREAM_RE.fullmatch(upstream).groups()
    return commit_ if repo.lower() == SOURCE.lower() else None


def declarations(commit_: str) -> bytes:
    if command("git", "cat-file", "-e", f"{commit_}^{{commit}}", check=False).returncode:  # check: upstream_commit_exists
        raise ExportError("upstream commit does not exist in this repository")
    out = b""
    for name in DECLARATION_FILES:
        blob = command("git", "show", f"{commit_}:{name}", check=False)
        if blob.returncode:  # check: declaration_present
            raise ExportError("license declaration is missing at the declared commit")
        out += f"DECL {name} {len(blob.stdout)}\n".encode() + blob.stdout + b"\n"
    return out


def external_sections(middle: bytes) -> list[str]:
    """Parse recorded-only declaration sections of other repositories; returns their upstream strings."""
    seen, pos = [], 0
    try:
        while pos < len(middle):
            end = middle.index(b"\n", pos)
            header = middle[pos:end].decode()
            if not header.startswith("UPSTREAM "):
                raise ValueError
            pos, records = end + 1, 0
            while middle.startswith(b"DECL ", pos):
                end = middle.index(b"\n", pos)
                parts = middle[pos:end].decode().split(" ")
                length = int(parts[2]) if len(parts) == 3 and parts[2].isdigit() else 0
                if length == 0 or middle[end + 1 + length:end + 2 + length] != b"\n":
                    raise ValueError
                pos, records = end + 2 + length, records + 1
            if records == 0:
                raise ValueError
            seen.append(header[len("UPSTREAM "):])
    except (ValueError, UnicodeDecodeError) as error:
        raise ExportError("retained reviewer input has malformed external license declarations") from error
    return seen


def receipt_check(main_sha: str, decision: dict, intro: str, info: dict, source: str) -> str:
    """Validate the receipt behind one decision line; returns the verified base."""
    receipt_path = decision["obj"]["receipt"]
    first_parent, final_head = info["first_parent"], info["final_head"]
    if hashlib.sha256(CHECKLIST_TEXT.encode()).hexdigest() != CHECKLIST_SHA256:  # check: checklist_pin
        raise ExportError("checklist differs from the pinned digest")
    stem = RECEIPT_RE.fullmatch(receipt_path).group(1)
    at_intro = command("git", "show", f"{intro}:{receipt_path}", check=False)
    if at_intro.returncode:  # check: receipt_present
        raise ExportError("receipt does not bind tuple: receipt missing")
    scan_public_text(at_intro.stdout)
    try:
        receipt = json.loads(at_intro.stdout.decode())
    except ValueError as error:
        raise ExportError("receipt does not bind tuple: malformed") from error
    if not isinstance(receipt, dict) or set(receipt) != RECEIPT_KEYS:
        raise ExportError("receipt does not bind tuple: malformed")
    head, base = receipt["reviewed_head"], receipt["base"]
    if not SHA_RE.fullmatch(str(head)) or not SHA_RE.fullmatch(str(base)) or not DIGEST_RE.fullmatch(str(receipt["diff_sha256"])):
        raise ExportError("receipt does not bind tuple: malformed")
    if not is_ancestor(head, final_head):  # check: head_ancestor
        raise ExportError("receipt reviewed head is not an ancestor of the pull request head")
    retained_record(main_sha, intro, head, final_head, receipt_path)
    if any(not name.startswith(RECEIPT_DIR) for name in changed_paths(head, final_head)):  # check: receipt_only_after_head
        raise ExportError("decision pull request changed more than receipts after the reviewed head")
    if base != unique_merge_base(head, first_parent):  # check: receipt_base
        raise ExportError("receipt base differs from the pull request merge base")
    names = changed_paths(base, head)
    if any(not name.startswith(DEC_DIR) or name.startswith(RECEIPT_DIR) for name in names):  # check: reviewed_diff_scope
        raise ExportError("reviewed diff is not limited to decision files")
    diff = command("git", "-c", "diff.algorithm=myers", "-c", "core.autocrlf=false", "diff", "--no-renames", "--no-ext-diff",
                   "--binary", "--full-index", "-U3", base, head).stdout
    digest = hashlib.sha256(diff + b"--files--\n" + b"".join(name.encode() + b"\n" for name in sorted(names))).hexdigest()
    if digest != receipt["diff_sha256"]:  # check: diff_digest
        raise ExportError("receipt diff digest does not match git")
    added = added_decision_lines(intro)
    listed = receipt["decision_lines_sha256"]
    if not isinstance(listed, list) or len(set(listed)) != len(listed) or set(listed) != {hashlib.sha256(x.encode()).hexdigest() for x in added}:  # check: lines_set
        raise ExportError("receipt does not bind tuple: decision lines differ from the lines the change adds")
    blobs = b""
    for o in sorted((json.loads(x) for x in added), key=lambda o: (o["path"], o["sha256"], o["upstream"])):
        blob = command("git", "show", f"{base}:{o['path']}", check=False)
        if blob.returncode or hashlib.sha256(blob.stdout).hexdigest() != o["sha256"]:  # check: blob_at_base
            raise ExportError("embedded source blob at the base differs from the decision digest")
        blobs += f"BLOB {o['path']} {o['sha256']} {o['upstream']} {len(blob.stdout)}\n".encode() + blob.stdout + b"\n"
    upstreams = sorted({json.loads(x)["upstream"] for x in added})
    own = [u for u in upstreams if upstream_commit(u, source) is not None]
    external = [u for u in upstreams if upstream_commit(u, source) is None]
    declared = b"".join(f"UPSTREAM {u}\n".encode() + declarations(upstream_commit(u, source)) for u in own)
    head_part = diff + b"--sources--\n" + blobs + b"--declarations--\n" + declared
    tail_part = b"--checklist--\n" + CHECKLIST_TEXT.encode()
    reviewers = receipt["reviewers"]
    if not isinstance(reviewers, list) or len(reviewers) < MIN_REVIEWERS:  # check: min_reviewers
        raise ExportError("receipt needs at least two blind reviewers")
    sessions, transcripts = set(), set()
    for number, reviewer in enumerate(reviewers, 1):
        if not isinstance(reviewer, dict) or set(reviewer) != REVIEWER_KEYS:
            raise ExportError("receipt reviewer entry is malformed")
        if reviewer["verdict"] != "APPROVE":  # check: unanimous_approve
            raise ExportError("receipt reviewer verdict is not APPROVE")
        if not all(isinstance(reviewer[k], str) and reviewer[k].strip() for k in ("session_id", "model")) or \
                not DIGEST_RE.fullmatch(str(reviewer["input_digest"])) or not DIGEST_RE.fullmatch(str(reviewer["transcript_sha256"])):
            raise ExportError("receipt reviewer entry is malformed")
        sessions.add(reviewer["session_id"])
        transcripts.add(reviewer["transcript_sha256"])
        transcript = retained_record(main_sha, intro, head, final_head, f"{RECEIPT_DIR}{stem}/reviewer-{number}.md")
        if hashlib.sha256(transcript).hexdigest() != reviewer["transcript_sha256"]:  # check: transcript_digest
            raise ExportError("receipt transcript digest does not match the retained transcript")
        scan_public_text(transcript)
        text = transcript.decode("utf-8", "replace")
        lines_ = [line for line in text.splitlines() if line.strip()]
        if lines_ and lines_[0].startswith("SCRUBBED:") and not re.fullmatch(r"SCRUBBED: \d+ replacements", lines_[0]):  # check: scrub_header
            raise ExportError("receipt transcript scrub header is malformed")
        if reviewer["session_id"] not in text or reviewer["input_digest"] not in text:  # check: transcript_embeds
            raise ExportError("receipt transcript does not embed its session id and input digest")
        if not lines_ or lines_[-1] != f"VERDICT: APPROVE {receipt['diff_sha256']}":  # check: transcript_verdict
            raise ExportError("receipt transcript does not end with the verdict line bound to the diff digest")
        retained = retained_record(main_sha, intro, head, final_head, f"{RECEIPT_DIR}{stem}/reviewer-{number}.input.txt")
        if hashlib.sha256(retained).hexdigest() != reviewer["input_digest"]:  # check: input_digest
            raise ExportError("receipt input digest does not match the retained reviewer input")
        if not retained.startswith(head_part) or not retained.endswith(tail_part) or len(retained) < len(head_part) + len(tail_part):  # check: input_content
            raise ExportError("retained reviewer input is not the reviewed diff, the embedded source blobs, the license declarations and the pinned checklist")
        if external_sections(retained[len(head_part):len(retained) - len(tail_part)]) != external:  # check: declarations_external
            raise ExportError("retained reviewer input lacks the recorded license declarations of the other upstream repositories")
        scan_public_text(retained)
    if len(sessions) != len(reviewers):  # check: distinct_sessions
        raise ExportError("receipt reviewer sessions are not distinct")
    if len(transcripts) != len(reviewers):  # check: distinct_transcripts
        raise ExportError("receipt reviewer transcripts are not distinct")
    return base


def strip_rows(text: str) -> list[str]:
    lines = text.splitlines()
    if HEADER not in lines:
        return lines
    start = lines.index(HEADER) + 2
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    return lines[:start] + lines[end:]


def verify_row(main_sha: str, decisions: list[dict], row: dict[str, str], order: dict[str, int], infos: dict[str, dict]) -> dict[str, str]:
    """Check one row against the decision file; return the manifest decision references."""
    key = (row["path"], row["sha256"])
    ranked = sorted((d for d in decisions if (d["obj"]["path"], d["obj"]["sha256"]) == key), key=lambda d: rank(order, d))
    chain = [find_decision(decisions, order, row["decision"], row, "current")]
    if row["status"] != "current":
        chain.append(find_decision(decisions, order, row["status_decision"], row, row["status"]))
    if ranked[-1] is not chain[-1]:  # check: effective_status
        raise ExportError("a later decision changes the effective status of this row")
    if len(chain) == 2 and (chain[0]["intro"] == chain[1]["intro"] or not is_ancestor(chain[0]["intro"], chain[1]["intro"])):  # check: status_after_decision
        raise ExportError("status decision must come after the publication decision")
    refs = {"decision": row["decision"], "status_decision": row["status_decision"] if row["status"] != "current" else "none"}
    source = row["source_commit"]
    if source not in order:  # check: source_first_parent
        raise ExportError("source commit must be a first-parent commit of main")
    bases = [receipt_check(main_sha, decision, decision["intro"], infos[decision["intro"]], source) for decision in chain]
    last_intro = chain[-1]["intro"]
    for rev in command("git", "log", "--first-parent", "--reverse", "--format=%H", main_sha, "--", "corpus/README.md").stdout.decode().split():
        if rev != last_intro and is_ancestor(last_intro, rev) and not _parses(show(rev, "corpus/README.md") or ""):  # check: table_always_parses
            raise ExportError("an allowlist table version after the decision does not parse")
    row_commit = latest_introducing_commit(main_sha, "corpus/README.md", lambda text: _has_row(text, row))
    merged_pull(row_commit)
    if row_commit == last_intro or not is_ancestor(last_intro, row_commit):  # check: decision_precedes_row
        raise ExportError("decision must precede allowlist row")
    if changed_paths(row_commit + "^1", row_commit) != ["corpus/README.md"]:  # check: row_commit_scope
        raise ExportError("allowlist row commit changes more than corpus/README.md")
    if strip_rows(show(row_commit + "^1", "corpus/README.md") or "") != strip_rows(show(row_commit, "corpus/README.md") or ""):  # check: row_commit_table_only
        raise ExportError("allowlist row commit changes more than table rows")
    if source in (row_commit, chain[0]["intro"]) or not is_ancestor(source, bases[0]):  # check: source_relation
        raise ExportError("source commit must be an ancestor of the receipt base and differ from the row commit")
    reuse_license, reuse_holders = reuse_terms(source, row["path"])
    if reuse_license != row["license"]:  # check: reuse_license
        raise ExportError("license differs from the one REUSE.toml assigns at the source commit")
    if not reuse_holders or any(holder not in chain[0]["obj"]["rights_basis"] for holder in reuse_holders):  # check: rights_basis_quotes_holder
        raise ExportError("rights_basis does not quote the holder string REUSE.toml assigns at the source commit")
    return refs


ROW_KEYS = ("source_commit", "path", "sha256", "rights_holder", "license", "decision", "status", "supersedes", "status_decision")


def _has_row(text: str, row: dict[str, str]) -> bool:
    """True when a line of `text` carries the row's cells, whether or not the table around it parses."""
    cells = [row[k] for k in ROW_KEYS]
    return any(line.startswith("|") and [c.strip() for c in line.strip().strip("|").split("|")] == cells for line in text.splitlines())


def _parses(text: str) -> bool:
    try:
        parse_allowlist(text)
        return True
    except ExportError:
        return False


def build(main_sha: str, rows: list[dict[str, str]]) -> tuple[dict[str, object], dict[str, bytes]]:
    if len({(row["source_commit"], row["path"]) for row in rows}) != len(rows):
        raise ExportError("duplicate source commit/path row")
    candidates: list[dict[str, str]] = []
    files: dict[str, bytes] = {}
    current_paths: set[str] = set()
    for row in rows:
        validate_row(row)
        if row["status"] == "current":
            if row["path"] in current_paths:
                raise ExportError("multiple current revisions for one source path")
            current_paths.add(row["path"])
    for row in rows:
        if row["status"] == "superseded" and not any(
                newer["path"] == row["path"] and newer["supersedes"] == row["sha256"]
                for newer in rows):
            raise ExportError("superseded revision has no linked replacement")
    decisions = load_decisions(main_sha) if rows else []
    order = first_parent_order(main_sha) if rows else {}
    infos: dict[str, dict] = {}
    for d in decisions:  # every decision line must come from a clean merged change, rows or not
        d["intro"] = introducing_commit(main_sha, d["file"], lambda text, line=d["line"]: line in text.splitlines())
        if d["intro"] not in infos:
            infos[d["intro"]] = change_info(d["intro"])
    for row in rows:
        refs = verify_row(main_sha, decisions, row, order, infos)
        content = git_blob(row["source_commit"], row["path"], main_sha)
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ExportError("source blob digest differs from allowlist")
        secret_scan(content)
        candidate = dict(row)
        candidate["decision"] = refs["decision"]
        candidate["status_decision"] = refs["status_decision"]
        candidate["publication_review_readback"] = READBACK
        candidate["status_review_readback"] = READBACK if row["status"] != "current" else "not_applicable"
        candidate["reviewer_identity_class"] = IDENTITY_CLASS
        candidate["public_export"] = "eligible" if row["status"] == "current" else "withheld"
        candidate["kc2_admission"] = "not_measured"
        candidates.append(candidate)
        if row["status"] == "current":
            files[row["path"]] = content
    manifest: dict[str, object] = {
        "schema": SCHEMA,
        "source_repository": SOURCE,
        "allowlist_commit": main_sha,
        "row_count": len(rows),
        "export_count": len(files),
        "status": "empty_allowlist" if not rows else "candidate_only",
        "publication_review_readback": READBACK if rows else "not_applicable",
        "kc2_runtime_admission": "not_measured",
        "scrutator_projection": "not_applied",
        "entries": candidates,
    }
    return manifest, files


def write_bundle(output: Path, manifest: dict[str, object], files: dict[str, bytes]) -> None:
    if output.exists():
        raise ExportError("output path already exists; refusing overwrite")
    if not output.parent.is_dir():
        raise ExportError("output parent directory must already exist")
    stage = Path(tempfile.mkdtemp(prefix=".kcp-export-", dir=output.parent))
    try:
        for path, content in files.items():
            target = stage / "files" / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        (stage / "manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
        if output.exists():
            raise ExportError("output path appeared while staging")
        os.rename(stage, output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        main_sha = live_main()
        head = command("git", "rev-parse", "HEAD").stdout.decode().strip()
        if head != main_sha:
            raise ExportError("exporter must run from exact current main")
        if command("git", "status", "--porcelain", "--untracked-files=all").stdout.strip():
            raise ExportError("exporter checkout is not clean at pinned main")
        committed = command("git", "show", f"{main_sha}:tools/export_corpus.py").stdout
        if committed != Path(__file__).read_bytes():
            raise ExportError("running exporter bytes differ from pinned main")
        source = command("git", "show", f"{main_sha}:corpus/README.md").stdout.decode()
        rows = parse_allowlist(source)
        manifest, files = build(main_sha, rows)
        write_bundle(args.output, manifest, files)
    except ExportError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 3
    except OSError:
        print("REFUSED: candidate bundle I/O failure", file=sys.stderr)
        return 3
    print(f"{manifest['status']}: {args.output / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
