#!/usr/bin/env python3
"""Dry-run export of explicitly allowlisted, merged public corpus bytes.

This produces a candidate bundle for a downstream indexer. It never writes to
Scrutator, advances a serving generation, or claims KC2 admission.
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


REPO = Path(__file__).resolve().parents[1]
SOURCE = "Arcanada-one/knowledge-contract"
HEADER = "| Source commit | Path | Content SHA-256 | Author/rights holder | License | Publication decision | Status | Supersedes | Status decision |"
ALLOWED_LICENSES = {"CC-BY-4.0", "Apache-2.0"}
PATH_RE = re.compile(r"^(papers|spec|articles|schemas)/[A-Za-z0-9][A-Za-z0-9_./-]*\.(md|json|ya?ml)$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
DECISION_RE = re.compile(r"^https://github\.com/Arcanada-one/knowledge-contract/pull/([1-9][0-9]*)#pullrequestreview-([1-9][0-9]*)$")
SECRET_SHAPE = re.compile(rb"(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|mun_sk_[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9]{20,}|vault_[A-Za-z0-9_-]{20,})")
MAX_BYTES = 1024 * 1024


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


def validate_row(row: dict[str, str]) -> None:
    if not SHA_RE.fullmatch(row["source_commit"]):
        raise ExportError("source commit must be a full lowercase SHA")
    path = row["path"]
    if not PATH_RE.fullmatch(path) or ".." in Path(path).parts or "//" in path:
        raise ExportError("source path is outside the public corpus allowlist")
    if not DIGEST_RE.fullmatch(row["sha256"]):
        raise ExportError("content SHA-256 is missing or malformed")
    if not row["rights_holder"] or row["rights_holder"] in {"?", "unknown", "TBD"}:
        raise ExportError("rights holder is not established")
    if row["license"] not in ALLOWED_LICENSES:
        raise ExportError("license is absent or outside reviewed project licenses")
    if not DECISION_RE.fullmatch(row["decision"]):
        raise ExportError("publication decision needs a precise Knowledge Contract PR review URL")
    if row["status"] not in {"current", "superseded", "withdrawn"}:
        raise ExportError("publication status is unknown")
    if row["supersedes"] not in {"", "—", "none"} and not DIGEST_RE.fullmatch(row["supersedes"]):
        raise ExportError("superseded digest must be absent or a SHA-256")
    if row["status"] == "current" and row["status_decision"] not in {"", "—", "none"}:
        raise ExportError("current row must not have a later status decision")
    if row["status"] != "current" and not DECISION_RE.fullmatch(row["status_decision"]):
        raise ExportError("non-current row needs a precise later status decision")


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


def publication_review(row: dict[str, str]) -> None:
    """Read back an exact-head APPROVED review for the merged source revision."""
    match = DECISION_RE.fullmatch(row["decision"])
    if match is None:
        raise ExportError("publication decision URL is malformed")
    pr_number, review_id = match.groups()
    prefix = "repos/Arcanada-one/knowledge-contract/pulls/" + pr_number
    try:
        pr = json.loads(command("gh", "api", prefix).stdout)
        review = json.loads(command("gh", "api", prefix + "/reviews/" + review_id).stdout)
    except (FileNotFoundError, ValueError) as error:
        raise ExportError("publication review could not be read back") from error
    author = pr.get("user", {}).get("login") if isinstance(pr.get("user"), dict) else None
    reviewer = review.get("user", {}).get("login") if isinstance(review.get("user"), dict) else None
    if (not pr.get("merged_at") or pr.get("merge_commit_sha") != row["source_commit"] or
            not SHA_RE.fullmatch(pr.get("head", {}).get("sha", "")) or
            review.get("id") != int(review_id) or review.get("state") != "APPROVED" or
            review.get("commit_id") != pr["head"]["sha"] or not review.get("submitted_at") or
            not author or not reviewer or reviewer == author):
        raise ExportError("publication review is absent, stale or bound to another merge")
    decisions = []
    for line in (review.get("body") or "").splitlines():
        if line.startswith("KnowledgeContractPublicationDecision/v1 "):
            try:
                decisions.append(json.loads(line.split(" ", 1)[1]))
            except ValueError as error:
                raise ExportError("publication decision body is malformed") from error
    expected = {key: row[key] for key in ("path", "sha256", "rights_holder", "license")}
    expected["status"] = "current"
    expected["reviewed_head"] = pr["head"]["sha"]
    if len(decisions) != 1 or decisions[0] != expected:
        raise ExportError("publication review does not bind exact path, digest and rights")


def status_review(row: dict[str, str], main_sha: str) -> None:
    match = DECISION_RE.fullmatch(row["status_decision"])
    if match is None:
        raise ExportError("later status decision URL is malformed")
    pr_number, review_id = match.groups()
    prefix = "repos/Arcanada-one/knowledge-contract/pulls/" + pr_number
    try:
        pr = json.loads(command("gh", "api", prefix).stdout)
        review = json.loads(command("gh", "api", prefix + "/reviews/" + review_id).stdout)
    except (FileNotFoundError, ValueError) as error:
        raise ExportError("later status review could not be read back") from error
    author = pr.get("user", {}).get("login") if isinstance(pr.get("user"), dict) else None
    reviewer = review.get("user", {}).get("login") if isinstance(review.get("user"), dict) else None
    head = pr.get("head", {}).get("sha", "")
    merge = pr.get("merge_commit_sha", "")
    if (not pr.get("merged_at") or not SHA_RE.fullmatch(merge) or
            command("git", "merge-base", "--is-ancestor", merge, main_sha, check=False).returncode or
            not SHA_RE.fullmatch(head) or review.get("id") != int(review_id) or
            review.get("state") != "APPROVED" or review.get("commit_id") != head or
            not review.get("submitted_at") or not author or not reviewer or reviewer == author):
        raise ExportError("later status review is absent, stale or unmerged")
    decisions = []
    for line in (review.get("body") or "").splitlines():
        if line.startswith("KnowledgeContractStatusDecision/v1 "):
            try:
                decisions.append(json.loads(line.split(" ", 1)[1]))
            except ValueError as error:
                raise ExportError("later status decision body is malformed") from error
    expected = {key: row[key] for key in ("source_commit", "path", "sha256", "status")}
    expected["reviewed_head"] = head
    if len(decisions) != 1 or decisions[0] != expected:
        raise ExportError("later status review does not bind exact source revision")


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
    for row in rows:
        publication_review(row)
        if row["status"] != "current":
            status_review(row, main_sha)
        content = git_blob(row["source_commit"], row["path"], main_sha)
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ExportError("source blob digest differs from allowlist")
        secret_scan(content)
        candidate = dict(row)
        candidate["publication_review_readback"] = "verified"
        candidate["status_review_readback"] = "verified" if row["status"] != "current" else "not_applicable"
        candidate["public_export"] = "eligible" if row["status"] == "current" else "withheld"
        candidate["kc2_admission"] = "not_measured"
        candidates.append(candidate)
        if row["status"] == "current":
            files[row["path"]] = content
    manifest: dict[str, object] = {
        "schema": "KnowledgeContractCandidateExport/v1",
        "source_repository": SOURCE,
        "allowlist_commit": main_sha,
        "row_count": len(rows),
        "export_count": len(files),
        "status": "empty_allowlist" if not rows else "candidate_only",
        "publication_review_readback": "verified" if rows else "not_applicable",
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
