"""Boundary tests for the public corpus candidate exporter (DEC-AUP-0171 decision-file route).

The decision-file tests build real git repositories in temporary directories so ordering,
ancestry and diff rules run against real history; only the GitHub API reads are replaced.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from contextlib import ExitStack
from pathlib import Path
import unittest
from unittest.mock import patch

from tools import export_corpus as export

DEC = "corpus/publication-decisions/"
RECEIPT = DEC + "receipts/"
HOLDER = "Pavel Valentov"
DOCS = ("articles/project-overview.md", "articles/openness-and-attribution-policy.md", "articles/attribution-policy.md",
        "articles/contribution-guide.md", "articles/sources-register.md", "articles/site-summary-llms.md")
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid", "GIT_CONFIG_GLOBAL": os.devnull,
       "GIT_AUTHOR_DATE": "2026-10-29T12:00:00+00:00", "GIT_COMMITTER_DATE": "2026-10-29T12:00:00+00:00"}
REUSE_DEFAULT = """version = 1

[[annotations]]
path = "**"
precedence = "aggregate"
SPDX-FileCopyrightText = "2026 Example Holder and contributors"
SPDX-License-Identifier = "CC-BY-4.0"

[[annotations]]
path = ["tools/**", "schemas/**"]
precedence = "override"
SPDX-FileCopyrightText = "2026 Example Holder and contributors"
SPDX-License-Identifier = "Apache-2.0"
"""
REUSE_HOLDER = "2026 Example Holder and contributors"
REUSE_TWO_OVERRIDES = REUSE_DEFAULT + """
[[annotations]]
path = "articles/**"
precedence = "override"
SPDX-License-Identifier = "CC-BY-4.0"

[[annotations]]
path = "articles/*.md"
precedence = "override"
SPDX-License-Identifier = "CC-BY-4.0"
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(("git", "-c", "commit.gpgsign=false", *args), cwd=repo, env=ENV, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()


def write(repo: Path, path: str, text: str | bytes) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(text if isinstance(text, bytes) else text.encode())


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def table(rows: list[dict[str, str]]) -> str:
    lines = [export.HEADER, "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    keys = ("source_commit", "path", "sha256", "rights_holder", "license", "decision", "status", "supersedes", "status_decision")
    lines += ["| " + " | ".join(row[k] for k in keys) + " |" for row in rows]
    return "# Public corpus allowlist\n\n" + "\n".join(lines) + "\n"


def review_digest(repo: Path, base: str, head: str) -> tuple[str, list[str], bytes]:
    names = git(repo, "diff", "--no-renames", "--name-only", base, head).splitlines()
    diff = subprocess.run(("git", "-c", "diff.algorithm=myers", "-c", "core.autocrlf=false", "diff", "--no-renames", "--no-ext-diff",
                           "--binary", "--full-index", "-U3", base, head), cwd=repo, env=ENV, check=True, stdout=subprocess.PIPE).stdout
    return hashlib.sha256(diff + b"--files--\n" + b"".join(n.encode() + b"\n" for n in sorted(names))).hexdigest(), names, diff


def decision_obj(path: str, sha: str, status: str = "current", batch: str = "b1", **over) -> dict:
    obj = {"schema": export.DECISION_SCHEMA, "path": path, "sha256": sha, "rights_holder": HOLDER, "license": "CC-BY-4.0",
           "status": status, "upstream": "original", "rights_basis": f"author declaration in NOTICE; REUSE.toml holder string: {REUSE_HOLDER}; contributor parts rest on DCO sign-offs, declared and not verified",
           "third_party": "none found", "attribution": "credit line present",
           "limits": "does not establish identity or agent-text copyright", "receipt": f"{RECEIPT}{batch}.json"}
    obj.update(over)
    return obj


class World:
    """A repository with content S (and optional gap commit), decision pull requests merged by merge commit, and row changes."""

    def __init__(self, tmp: Path, docs=DOCS[:1], **o) -> None:
        self.o, self.docs = o, docs
        self.repo = tmp / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        write(self.repo, "corpus/README.md", table([]))
        self.init_commit = commit(self.repo, "init")
        self.contents = {d: (f"# {d}\nA bounded statement about {d}." + (" Read /run/user/1000/x." if o.get("deny_in_doc") else "") + "\n").encode() for d in docs}
        for d, c in self.contents.items():
            write(self.repo, d, c)
        write(self.repo, "REUSE.toml", REUSE_TWO_OVERRIDES if o.get("two_overrides") else REUSE_DEFAULT)
        write(self.repo, "NOTICE", o.get("notice", "Notice text of the example project\nAuthor: Pavel Valentov, Independent Researcher\nAuthor: Corrected Holder, Independent Researcher\n"))
        write(self.repo, "LICENSE", "Official license text placeholder\n")
        self.S = commit(self.repo, "content")
        self.E = commit(self.repo, "gap commit on main") if o.get("main_gap") else None
        if o.get("changed_after_source"):
            self.contents = {d: c + b"A later edit.\n" for d, c in self.contents.items()}
            for d, c in self.contents.items():
                write(self.repo, d, c)
            self.E = commit(self.repo, "content edited after the source commit")
        self.X = None
        if o.get("source_side_merged"):
            git(self.repo, "checkout", "-q", "-b", "content-side", self.S)
            self.X = commit(self.repo, "content step on a side branch")
            git(self.repo, "checkout", "-q", "main")
            git(self.repo, "merge", "--no-ff", "-q", "-m", "merge the side branch", "content-side")
            self.M = git(self.repo, "rev-parse", "HEAD")
        self.sha = {d: ("e" * 64 if o.get("bad_blob_digest") else hashlib.sha256(c).hexdigest()) for d, c in self.contents.items()}
        self.merged: dict[str, int] = {}
        self.heads: dict[int, str] = {}
        self.pr_count = 10
        self.batches: dict[str, dict] = {}
        self.R = None
        if not o.get("no_decision_commit"):
            objs = [decision_obj(d, self.sha[d], **o.get("decision_over", {})) for d in docs]
            if o.get("extra_key"):
                objs[0]["extra"] = "x"
            if o.get("duplicate"):
                objs.append({**objs[0], "attribution": "second line, same tuple"})
            ups = o.get("upstreams", {})
            for obj in objs:
                if obj["path"] in ups:
                    obj["upstream"] = ups[obj["path"]]
            self.decision_pr("b1", objs, parent=self.M if o.get("source_side_merged") else (self.E if o.get("changed_after_source") else None))
        if o.get("source_on_side"):
            self.source = self.batches["b1"]["C"]
        elif o.get("source_is_decision"):
            self.source = self.batches["b1"]["I"]
        elif o.get("source_side_merged"):
            self.source = self.X
        elif o.get("source_init"):
            self.source = self.init_commit
        elif o.get("source_gap"):
            self.source = self.E
        else:
            self.source = self.S
        if not o.get("no_rows"):
            self.add_rows([self.row(d, "b1", i) for i, d in enumerate(docs)])
        self.main = git(self.repo, "rev-parse", "HEAD")

    # --- builders ---------------------------------------------------------------------------
    def decision_pr(self, batch: str, objs: list[dict], parent: str | None = None, extra: dict | None = None, **k) -> dict:
        repo, o = self.repo, {**self.o, **k}
        extra = extra or {}
        every = objs + [x for v in extra.values() for x in v]
        number = self.pr_count = self.pr_count + 1
        git(repo, "checkout", "-q", "-b", f"pr-{batch}", parent or self.S)
        lines = [export.canonical(x) for x in objs]
        if o.get("repeat_line"):
            lines.append(lines[0])
        write(repo, f"{DEC}{batch}.jsonl", "\n".join(lines) + "\n" if lines else "")
        for other, other_objs in extra.items():
            write(repo, f"{DEC}{other}.jsonl", "\n".join(export.canonical(x) for x in other_objs) + "\n")
        info = {}
        if o.get("source_on_side"):
            git(repo, "commit", "-q", "--allow-empty", "-m", "side-branch content step")
            info["C"] = git(repo, "rev-parse", "HEAD")
        if o.get("same_commit"):
            write(repo, "corpus/README.md", table([]) + "changed in the decision change\n")
        if o.get("decision_extra_path"):
            write(repo, "notes.txt", "unrelated")
        if o.get("reviewed_receipt_path"):
            write(repo, RECEIPT + "b1/reviewer-9.md", "receipt-area file inside the reviewed diff")
        d1 = commit(repo, "decision lines")
        info["D1"] = d1
        base = git(repo, "merge-base", d1, git(repo, "rev-parse", "main"))
        digest, names, diff = review_digest(repo, base, d1)
        added = [export.canonical(x) for x in every]
        blobs = b""
        for x in sorted(every, key=lambda x: (x["path"], x["sha256"], x["upstream"])):
            blob = subprocess.run(("git", "show", f"{base}:{x['path']}"), cwd=repo, env=ENV, check=True, stdout=subprocess.PIPE).stdout
            blobs += f"BLOB {x['path']} {x['sha256']} {x['upstream']} {len(blob)}\n".encode() + blob + b"\n"
        decl = b""
        ups = sorted({x["upstream"] for x in every})
        parsed = {u: export.UPSTREAM_RE.fullmatch(u) for u in ups}
        for u in ups:
            if u != "original" and parsed[u] is None:
                continue
            if u != "original" and parsed[u].group(1) != export.SOURCE:
                continue
            commit_ = self.S if u == "original" else parsed[u].group(2)
            files_ = []
            for name in export.DECLARATION_FILES:
                got = subprocess.run(("git", "show", f"{commit_}:{name}"), cwd=repo, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if got.returncode == 0:
                    files_.append((name, got.stdout))
            decl += f"UPSTREAM {u}\n".encode() + b"".join(f"DECL {n} {len(b_)}\n".encode() + b_ + b"\n" for n, b_ in files_)
        if o.get("input_without_decl"):
            decl = b""
        for u in [u for u in ups if parsed[u] is not None and parsed[u].group(1) != export.SOURCE]:
            if o.get("external_decl_missing"):
                decl += f"UPSTREAM {u}\n".encode()
            elif o.get("external_decl_empty"):
                decl += f"UPSTREAM {u}\nDECL LICENSE 0\n\n".encode()
            elif not o.get("external_decl_absent"):
                decl += f"UPSTREAM {u}\nDECL REUSE.toml 13\nrecorded-bits\n".encode()
        retained = diff + b"--sources--\n" + blobs + b"--declarations--\n" + decl + b"--checklist--\n" + export.CHECKLIST_TEXT.encode()
        if o.get("input_without_blobs"):
            retained = diff + b"--sources--\n--declarations--\n" + decl + b"--checklist--\n" + export.CHECKLIST_TEXT.encode()
        if o.get("input_without_diff"):
            retained = b"checklist only\n"
        input_digest = hashlib.sha256(retained).hexdigest()
        head = d1
        if o.get("receipt_head_other"):
            git(repo, "checkout", "-q", "-b", f"side-{batch}", self.S)
            write(repo, "side.txt", "never merged")
            head = commit(repo, "side")
            git(repo, "checkout", "-q", f"pr-{batch}")
        lsha = [hashlib.sha256(x.encode()).hexdigest() for x in added]
        for bname in [batch, *extra]:
            sessions = o.get("session_ids", [f"{bname}-s1", f"{bname}-s2", f"{bname}-s3"])
            verdict_digest = o.get("verdict_digest", o.get("receipt_diff", digest))
            reviewers = []
            for n in range(1, o.get("reviewers", 2) + 1):
                if o.get("same_transcript"):
                    text = f"sessions {sessions[0]} {sessions[1]}\ninput {input_digest}\nidentical transcript\nVERDICT: APPROVE {verdict_digest}\n"
                else:
                    body = o.get("transcript_text", f"blind review {n} of {bname}: digests match, license consistent")
                    text = f"session {sessions[n - 1]}\ninput digest {'5' * 64 if o.get('bad_input_digest') else input_digest}\n{body}\n"
                    if o.get("no_embed"):
                        text = f"{body}\n"
                    text += f"VERDICT: APPROVE {verdict_digest}\n"
                    if o.get("scrub_header") == "ok":
                        text = "SCRUBBED: 3 replacements\n" + text
                    if o.get("scrub_header") == "bad":
                        text = "SCRUBBED: many things\n" + text
                write(repo, f"{RECEIPT}{bname}/reviewer-{n}.md", text)
                if not o.get("no_input_file"):
                    write(repo, f"{RECEIPT}{bname}/reviewer-{n}.input.txt", retained)
                reviewers.append({"session_id": sessions[n - 1], "model": "model-/home/x" if o.get("deny_in_receipt") else f"model-{n}",
                                  "input_digest": "5" * 64 if o.get("bad_input_digest") else input_digest,
                                  "transcript_sha256": hashlib.sha256(text.encode()).hexdigest(), "verdict": o.get("verdict", "APPROVE")})
            if o.get("bad_transcript"):
                reviewers[0]["transcript_sha256"] = "1" * 64
            listed = lsha[:-1] if o.get("receipt_lines") == "SUBSET" else (lsha + ["9" * 64] if o.get("receipt_lines") == "SUPERSET" else o.get("receipt_lines", lsha))
            if o.get("reviewer_extra_key"):
                reviewers[0]["note"] = "an extra key"
            receipt = {"reviewed_head": "HEAD" if o.get("receipt_head_text") else head, "base": o.get("receipt_base", base),
                       "diff_sha256": o.get("receipt_diff", digest), "decision_lines_sha256": listed, "reviewers": reviewers}
            if o.get("receipt_extra_key"):
                receipt["files"] = []
            if not o.get("no_receipt") and not o.get("late_receipt"):
                write(repo, f"{RECEIPT}{bname}.json", json.dumps(receipt, sort_keys=True))
        if o.get("receipt_commit_extra"):
            write(repo, DEC + "zz.jsonl", "")
        d2 = commit(repo, "receipt")
        git(repo, "checkout", "-q", "main")
        if o.get("squash_decision"):
            git(repo, "merge", "--squash", f"pr-{batch}")
            i = commit(repo, f"decision change {batch} (#{number})")
        else:
            if o.get("evil_merge"):
                git(repo, "merge", "--no-ff", "--no-commit", f"pr-{batch}")
                write(repo, DEC + "evil.jsonl", "")
                git(repo, "add", "-A")
                git(repo, "commit", "-q", "-m", f"decision change {batch} (#{number})")
            else:
                git(repo, "merge", "--no-ff", "-q", "-m", f"decision change {batch} (#{number})", f"pr-{batch}")
            i = git(repo, "rev-parse", "HEAD")
        if o.get("late_receipt"):
            write(repo, f"{RECEIPT}{batch}.json", json.dumps(receipt, sort_keys=True))
            commit(repo, "late receipt")
        info.update(I=i, D2=d2, lsha=lsha[:len(objs)], lines=added, number=number,
                    extra={other: [hashlib.sha256(export.canonical(x).encode()).hexdigest() for x in v] for other, v in extra.items()})
        if not o.get("unmerged_decision"):
            self.merged[i] = number
        self.heads[number] = o.get("api_head", d2)
        self.batches[batch] = info
        return info

    def cell(self, batch: str, index: int = 0) -> str:
        if batch not in self.batches:
            return f"{DEC}{batch}.jsonl@{'a' * 40}#{'b' * 64}"
        b = self.batches[batch]
        return f"{DEC}{batch}.jsonl@{b['I']}#{b['lsha'][index]}"

    def row(self, doc: str, batch: str, index: int, status: str = "current", status_cell: str = "none", cell: str | None = None) -> dict:
        o = self.o
        return {"source_commit": self.source, "path": doc, "sha256": self.sha[doc], "rights_holder": o.get("row_holder", HOLDER),
                "license": o.get("row_license", "CC-BY-4.0"), "decision": cell or self.cell(batch, index), "status": status,
                "supersedes": "none", "status_decision": status_cell}

    def add_rows(self, rows: list[dict], extra: dict[str, str] | None = None, prose: str = "") -> str:
        write(self.repo, "corpus/README.md", table(rows) + prose)
        for path, text in (extra or {}).items():
            write(self.repo, path, text)
        number = self.pr_count = self.pr_count + 1
        self.R = commit(self.repo, f"allowlist rows (#{number})")
        self.merged[self.R] = number
        self.main = self.R
        return self.R

    # --- running ----------------------------------------------------------------------------
    def patches(self) -> ExitStack:
        stack = ExitStack()
        merged, heads = self.merged, self.heads

        def pulls(sha):
            return [{"number": merged[sha], "merged_at": "2026-10-29T00:00:00Z", "merge_commit_sha": sha,
                     "base": {"ref": self.o.get("pull_base", "main")}}] if sha in merged else []

        stack.enter_context(patch.object(export, "REPO", self.repo))
        stack.enter_context(patch.object(export, "pulls_for_commit", pulls))
        stack.enter_context(patch.object(export, "pull_info", lambda number: {"head": {"sha": heads.get(number, "")}}))
        stack.enter_context(patch.object(export, "secret_scan"))
        return stack

    def run(self, main: str | None = None):
        main = main or self.main
        with self.patches():
            return export.build(main, export.parse_allowlist(export.show(main, "corpus/README.md")))


class DecisionRouteTests(unittest.TestCase):
    def world(self, **o) -> World:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return World(Path(temp.name), **o)

    def refuses(self, pattern: str, **o) -> None:
        with self.assertRaisesRegex(export.ExportError, pattern):
            self.world(**o).run()

    # ---- positive controls ---------------------------------------------------------------
    def test_six_public_documents_export_as_candidates(self) -> None:
        manifest, files = self.world(docs=DOCS).run()
        self.assertEqual((manifest["schema"], manifest["row_count"], manifest["export_count"], manifest["status"]),
                         ("KnowledgeContractCandidateExport/v2", 6, 6, "candidate_only"))
        self.assertEqual(set(files), set(DOCS))
        self.assertEqual(manifest["publication_review_readback"], "decision_file_matched")
        for entry in manifest["entries"]:
            self.assertEqual(entry["publication_review_readback"], "decision_file_matched")
            self.assertEqual(entry["status_review_readback"], "not_applicable")
            self.assertEqual(entry["reviewer_identity_class"], "same_account_blind_agent")
            self.assertEqual(entry["public_export"], "eligible")
            self.assertEqual(entry["status_decision"], "none")
            self.assertRegex(entry["decision"], r"^corpus/publication-decisions/b1\.jsonl@[0-9a-f]{40}#[0-9a-f]{64}$")
        self.assertEqual(manifest["scrutator_projection"], "not_applied")
        self.assertEqual(manifest["kc2_runtime_admission"], "not_measured")
        self.assertNotIn("reviewer_independence", manifest["entries"][0])

    def test_withdrawn_row_is_recorded_not_exported_and_later_line_beats_current_row(self) -> None:
        w = self.world()
        doc = DOCS[0]
        w.decision_pr("b2", [decision_obj(doc, w.sha[doc], "withdrawn", "b2")], parent=w.main)
        row = w.row(doc, "b1", 0, "withdrawn", w.cell("b2", 0))
        r2 = w.add_rows([row])
        manifest, files = w.run(r2)
        self.assertEqual(files, {})
        self.assertEqual(manifest["entries"][0]["public_export"], "withheld")
        self.assertEqual(manifest["entries"][0]["status_review_readback"], "decision_file_matched")
        self.assertRegex(manifest["entries"][0]["status_decision"], r"^corpus/publication-decisions/b2\.jsonl@[0-9a-f]{40}#[0-9a-f]{64}$")
        r3 = w.add_rows([w.row(doc, "b1", 0)])
        with self.assertRaisesRegex(export.ExportError, "later decision changes the effective status"):
            w.run(r3)

    def test_a_key_can_return_to_current_through_a_new_line_with_its_own_receipt(self) -> None:
        w = self.world()
        doc = DOCS[0]
        w.decision_pr("b2", [decision_obj(doc, w.sha[doc], "withdrawn", "b2")], parent=w.main)
        w.decision_pr("b3", [decision_obj(doc, w.sha[doc], "current", "b3", attribution="credit line present again")], parent=w.main)
        good = w.add_rows([w.row(doc, "b3", 0)])
        manifest, files = w.run(good)
        self.assertEqual(set(files), {doc})
        self.assertIn("b3.jsonl@", manifest["entries"][0]["decision"])
        stale = w.add_rows([w.row(doc, "b1", 0)])
        with self.assertRaisesRegex(export.ExportError, "does not point at the last matching line"):
            w.run(stale)

    def test_orphan_decision_exports_nothing_and_is_not_an_error(self) -> None:
        w = self.world(docs=DOCS[:2], no_rows=True)
        r = w.add_rows([w.row(DOCS[0], "b1", 0)])
        manifest, files = w.run(r)
        self.assertEqual(set(files), {DOCS[0]})
        self.assertEqual(manifest["row_count"], 1)

    # ---- negative controls: each asserts the message of the check under test -------------
    def test_self_approving_change_is_refused(self) -> None:
        self.refuses("edits more than decisions", same_commit=True)

    def test_missing_decision_and_digest_mismatch_are_refused(self) -> None:
        self.refuses("no merged decision matches row", no_decision_commit=True)
        w = self.world()
        bad = w.row(DOCS[0], "b1", 0, cell=f"{DEC}b1.jsonl@{w.batches['b1']['I']}#{'0' * 64}")
        r = w.add_rows([bad])
        with self.assertRaisesRegex(export.ExportError, "does not point at the last matching line"):
            w.run(r)

    def test_one_character_license_or_holder_change_is_refused(self) -> None:
        self.refuses("no merged decision matches row", row_holder="Pavel Valentoz")
        self.refuses("no merged decision matches row", row_license="Apache-2.0")

    def test_license_must_equal_what_reuse_toml_assigns(self) -> None:
        self.refuses("differs from the one REUSE.toml assigns", decision_over={"license": "Apache-2.0"}, row_license="Apache-2.0")
        self.refuses("more than one REUSE.toml override", two_overrides=True)

    def test_malformed_decision_lines_are_refused(self) -> None:
        self.refuses("decision line malformed$", extra_key=True)
        self.refuses("mandatory fields missing", decision_over={"rights_basis": " "})
        self.refuses("mandatory fields missing", decision_over={"limits": ""})
        self.refuses("repeated line", repeat_line=True)

    def test_decision_commit_that_edits_more_than_decisions_is_refused(self) -> None:
        self.refuses("edits more than decisions", decision_extra_path=True)

    def test_row_commit_must_only_add_table_rows(self) -> None:
        w = self.world(no_rows=True)
        r = w.add_rows([w.row(DOCS[0], "b1", 0)], extra={"tools/other.py": "x = 1\n"})
        with self.assertRaisesRegex(export.ExportError, "changes more than corpus/README.md"):
            w.run(r)
        w2 = self.world(no_rows=True)
        r2 = w2.add_rows([w2.row(DOCS[0], "b1", 0)], prose="\nA prose sentence added together with the row.\n")
        with self.assertRaisesRegex(export.ExportError, "changes more than table rows"):
            w2.run(r2)
        w3 = self.world(no_rows=True)
        r3 = w3.add_rows([w3.row(DOCS[0], "b1", 0)], extra={DEC + "other.jsonl": ""})
        with self.assertRaisesRegex(export.ExportError, "changes more than corpus/README.md"):
            w3.run(r3)

    def test_decision_must_precede_the_row(self) -> None:
        w = self.world()
        with patch.object(export, "latest_introducing_commit", lambda m, f, p: w.batches["b1"]["I"]):
            with self.assertRaisesRegex(export.ExportError, "decision must precede allowlist row"):
                w.run()

    def test_source_commit_rules(self) -> None:
        self.refuses("first-parent commit of main", source_on_side=True)
        self.refuses("ancestor of the receipt base", source_is_decision=True)
        self.refuses("ancestor of the receipt base", main_gap=True, source_gap=True)

    def test_unmerged_decision_commit_is_refused(self) -> None:
        self.refuses("not a merged pull request commit", unmerged_decision=True)

    def test_unmerged_decision_line_is_refused_even_without_a_row(self) -> None:
        w = self.world(docs=DOCS[:2], no_rows=True)
        w.decision_pr("b9", [decision_obj(DOCS[1], w.sha[DOCS[1]], "withdrawn", "b9")], parent=w.main, unmerged_decision=True)
        r = w.add_rows([w.row(DOCS[0], "b1", 0)])
        with self.assertRaisesRegex(export.ExportError, "not a merged pull request commit"):
            w.run(r)

    def test_decision_read_from_worktree_is_ignored(self) -> None:
        w = self.world(no_decision_commit=True)
        write(w.repo, DEC + "b1.jsonl", export.canonical(decision_obj(DOCS[0], w.sha[DOCS[0]])) + "\n")
        with self.assertRaisesRegex(export.ExportError, "no merged decision matches row"):
            w.run()

    def test_shallow_clone_is_refused(self) -> None:
        w = self.world()
        shallow = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(("rm", "-r", str(shallow))))
        subprocess.run(("git", "clone", "-q", "--depth", "1", "file://" + str(w.repo), str(shallow / "c")), env=ENV, check=True)
        with patch.object(export, "REPO", shallow / "c"):
            with self.assertRaisesRegex(export.ExportError, "history incomplete"):
                export.load_decisions("HEAD")

    def test_decision_tree_is_write_once(self) -> None:
        cases = {
            "line modified": lambda r: (r / DEC / "b1.jsonl").write_text((r / DEC / "b1.jsonl").read_text().replace("credit line present", "edited")),
            "file deleted": lambda r: (r / DEC / "b1.jsonl").unlink(),
            "receipt altered": lambda r: (r / DEC / "receipts" / "b1.json").write_text("{}"),
            "transcript deleted": lambda r: (r / DEC / "receipts" / "b1" / "reviewer-1.md").unlink(),
            "file renamed": lambda r: (r / DEC / "b1.jsonl").rename(r / DEC / "renamed.jsonl"),
        }
        for name, tamper in cases.items():
            with self.subTest(name):
                w = self.world()
                tamper(w.repo)
                w.main = commit(w.repo, f"tamper: {name} (#99)")
                w.merged[w.main] = 99
                with self.assertRaisesRegex(export.ExportError, "write-once"):
                    w.run()

    def test_new_decisions_go_in_new_batch_files_and_a_modified_batch_file_is_refused(self) -> None:
        w = self.world(docs=DOCS[:2])
        with (w.repo / DEC / "b1.jsonl").open("a") as handle:
            handle.write(export.canonical(decision_obj(DOCS[1], w.sha[DOCS[1]], "withdrawn", "b1")) + "\n")
        main = commit(w.repo, "append a line (#98)")
        with patch.object(export, "REPO", w.repo):
            with self.assertRaisesRegex(export.ExportError, "write-once"):
                export.check_write_once(main)

    def test_ambiguous_merge_base_is_refused(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        git(repo, "init", "-q", "-b", "main")
        write(repo, "f", "0")
        base = commit(repo, "base")
        git(repo, "checkout", "-q", "-b", "a")
        write(repo, "a", "1")
        a1 = commit(repo, "a1")
        git(repo, "checkout", "-q", "-b", "b", base)
        write(repo, "b", "1")
        b1 = commit(repo, "b1")
        git(repo, "checkout", "-q", "-b", "ma", a1)
        git(repo, "merge", "--no-ff", "-q", "-m", "merge b into a", b1)
        git(repo, "checkout", "-q", "-b", "mb", b1)
        git(repo, "merge", "--no-ff", "-q", "-m", "merge a into b", a1)
        with patch.object(export, "REPO", repo):
            with self.assertRaisesRegex(export.ExportError, "more than one merge base"):
                export.unique_merge_base("ma", "mb")
            self.assertEqual(export.unique_merge_base("a", "b"), base)

    def test_status_decision_in_the_same_change_is_refused(self) -> None:
        w = self.world(no_rows=True)
        doc = DOCS[0]
        w.decision_pr("b2", [decision_obj(doc, w.sha[doc], "current", "b2", attribution="again"),
                             decision_obj(doc, w.sha[doc], "withdrawn", "b2")], parent=w.main)
        r = w.add_rows([w.row(doc, "b2", 1, "withdrawn", w.cell("b2", 1), cell=w.cell("b2", 0))])
        with self.assertRaisesRegex(export.ExportError, "status decision must come after"):
            w.run(r)

    def test_receipt_failures_are_refused(self) -> None:
        self.refuses("its receipt file is missing", no_receipt=True)
        self.refuses("receipt does not bind tuple: receipt missing", late_receipt=True)
        self.refuses("decision lines differ from the lines the change adds", receipt_lines=["f" * 64])
        self.refuses("decision lines differ from the lines the change adds", docs=DOCS, receipt_lines="SUBSET")
        self.refuses("diff digest does not match git", receipt_diff="2" * 64)
        self.refuses("merge base", receipt_base="3" * 40)
        self.refuses("reviewed diff is not limited to decision files", reviewed_receipt_path=True)
        self.refuses("at least two blind reviewers", reviewers=1)
        self.refuses("verdict is not APPROVE", verdict="REQUEST_CHANGES")
        self.refuses("transcript digest does not match", bad_transcript=True)
        self.refuses("input digest does not match", bad_input_digest=True)
        self.refuses("not introduced in the receipt commit range", no_input_file=True)
        self.refuses("the license declarations and the pinned checklist", input_without_diff=True)
        self.refuses("the license declarations and the pinned checklist", input_without_blobs=True)
        self.refuses("sessions are not distinct", session_ids=["same", "same", "x"])
        self.refuses("transcripts are not distinct", same_transcript=True)
        self.refuses("not an ancestor of the pull request head", receipt_head_other=True)
        self.refuses("more than receipts after the reviewed head", receipt_commit_extra=True)

    def test_transcript_must_embed_ids_and_end_with_the_bound_verdict_line(self) -> None:
        self.refuses("does not embed its session id and input digest", no_embed=True)
        self.refuses("does not end with the verdict line bound to the diff digest", verdict_digest="0" * 64)
        self.refuses("scrub header is malformed", scrub_header="bad")
        manifest, _ = self.world(scrub_header="ok").run()
        self.assertEqual(manifest["row_count"], 1)

    def test_source_blob_at_the_base_must_match_the_decision_digest(self) -> None:
        self.refuses("embedded source blob at the base differs", bad_blob_digest=True)

    def test_merge_commit_must_not_add_decision_files_of_its_own(self) -> None:
        self.refuses("differs from the pull request head", evil_merge=True)

    def test_receipt_superset_and_public_text_scans(self) -> None:
        self.refuses("decision lines differ from the lines the change adds", receipt_lines="SUPERSET")
        self.refuses("host path, host name or address", deny_in_receipt=True)
        self.refuses("host path, host name or address", deny_in_doc=True)

    def test_public_addresses_and_domains_are_not_denied_but_private_ones_are(self) -> None:
        for text in (b"see https://github.com/Arcanada-one and 8.8.8.8", b"contract.place and arcanada.ai", b"2001:db8::1 and fe80ab", b"1.127.0.0.1x"):
            self.assertIsNone(export.DENY_SHAPE.search(text), text)
        for text in (b"10.1.2.3", b"172.20.0.1", b"192.168.1.5", b"100.100.1.1", b"arcana-example", b"x.example.ts.net", b"/run/user/1000/a",
                     b"127.0.0.1", b"127.12.0.9", b"169.254.10.1", b"fd12:3456:789a::1", b"FC00::1", b"fdab::", b"Arcana-Example", b"/HOME/x", b"X.Example.TS.NET", b"/Users/a", b"/RUN/USER/1"):
            self.assertIsNotNone(export.DENY_SHAPE.search(text), text)

    def test_license_outside_the_two_and_unmerged_row_change_are_refused(self) -> None:
        w = self.world(no_rows=True)
        bad = w.row(DOCS[0], "b1", 0)
        bad["license"] = "MIT"
        with self.assertRaisesRegex(export.ExportError, "outside reviewed project licenses"):
            export.validate_row(bad)
        r = w.add_rows([w.row(DOCS[0], "b1", 0)])
        del w.merged[r]
        with self.assertRaisesRegex(export.ExportError, "not a merged pull request commit"):
            w.run(r)

    def test_row_with_the_old_holder_after_a_correction_is_refused(self) -> None:
        w = self.world(no_rows=True)
        doc = DOCS[0]
        w.decision_pr("b2", [decision_obj(doc, w.sha[doc], "current", "b2", rights_holder="Corrected Holder")], parent=w.main)
        r = w.add_rows([w.row(doc, "b1", 0)])
        with self.assertRaisesRegex(export.ExportError, "later decision changes the effective status"):
            w.run(r)
        fixed = w.add_rows([{**w.row(doc, "b2", 0), "rights_holder": "Corrected Holder"}])
        self.assertEqual(w.run(fixed)[0]["entries"][0]["rights_holder"], "Corrected Holder")

    def test_reviewer_input_must_embed_the_license_declarations(self) -> None:
        self.refuses("license declarations and the pinned checklist", input_without_decl=True)

    def test_license_declarations_must_exist_at_the_source_commit(self) -> None:
        self.refuses("license declaration is missing at the declared commit", source_init=True)

    def test_receipt_must_name_its_own_batch(self) -> None:
        self.refuses("receipt names another batch", decision_over={"receipt": RECEIPT + "b9.json"})

    def test_table_pointers_must_name_the_matched_line_commit_and_digest(self) -> None:
        w = self.world(no_rows=True)
        good = w.cell("b1", 0)
        file_, rest = good.split("@")
        commit_, digest = rest.split("#")
        for bad in (f"{file_}@{w.S}#{digest}", f"{file_}@{commit_}#{'0' * 64}", f"{DEC}other.jsonl@{commit_}#{digest}"):
            with self.subTest(bad=bad):
                r = w.add_rows([w.row(DOCS[0], "b1", 0, cell=bad)])
                with self.assertRaisesRegex(export.ExportError, "does not point at the last matching line"):
                    w.run(r)

    def test_status_that_the_decision_file_does_not_hold_is_refused(self) -> None:
        w = self.world(no_rows=True, main_gap=True)
        for status in ("withdrawn", "superseded"):
            with self.subTest(status=status):
                rows = [w.row(DOCS[0], "b1", 0, status, w.cell("b1", 0))]
                if status == "superseded":
                    rows.append({**w.row(DOCS[0], "b1", 0), "source_commit": w.E or w.S, "sha256": "c" * 64, "supersedes": w.sha[DOCS[0]]})
                r = w.add_rows(rows)
                with self.assertRaisesRegex(export.ExportError, "no merged decision matches row"):
                    w.run(r)

    def test_a_path_outside_the_six_documents_is_refused(self) -> None:
        row = {"source_commit": "a" * 40, "path": "articles/another.md", "sha256": "b" * 64, "rights_holder": HOLDER, "license": "CC-BY-4.0",
               "decision": f"{DEC}b1.jsonl@{'c' * 40}#{'d' * 64}", "status": "current", "supersedes": "none", "status_decision": "none"}
        with self.assertRaisesRegex(export.ExportError, "outside the scope fixed by DEC-AUP-0171"):
            export.validate_row(row)
        for path in ("articles/a.txt", "schemas/x.json", "papers/p.yml"):
            with self.assertRaises(export.ExportError):
                export.validate_row({**row, "path": path})

    def test_row_commit_is_the_most_recent_addition_of_the_row(self) -> None:
        w = self.world(no_rows=True)
        row = w.row(DOCS[0], "b1", 0)
        w.add_rows([row], extra={"tools/dirty.py": "x = 1\n"})
        w.add_rows([])
        r3 = w.add_rows([row])
        self.assertEqual(w.run(r3)[0]["row_count"], 1)

    def test_pinned_checklist_digest_constant_is_enforced(self) -> None:
        w = self.world()
        with patch.object(export, "CHECKLIST_SHA256", "0" * 64):
            with self.assertRaisesRegex(export.ExportError, "checklist differs from the pinned digest"):
                w.run()

    def test_transcript_lacking_only_one_of_session_or_digest_is_refused(self) -> None:
        self.refuses("does not embed its session id and input digest", no_embed=True)

    # ---- decision-tree layout, upstream declarations, holder strings, isolation of single guards ----
    def test_any_file_outside_the_allowed_layout_is_refused(self) -> None:
        for name in ("b2.v2.jsonl", "sub/b2.jsonl", "B2.JSONL", "b2.jsonl.txt", "receipts/b2.v1.json", "receipts/b1/notes.txt", ".hidden.jsonl"):
            with self.subTest(name=name):
                w = self.world()
                write(w.repo, DEC + name, export.canonical(decision_obj(DOCS[0], w.sha[DOCS[0]], "withdrawn", "b2")) + "\n")
                w.main = commit(w.repo, f"stray file {name} (#90)")
                w.merged[w.main] = 90
                with self.assertRaisesRegex(export.ExportError, "outside the allowed layout"):
                    w.run()

    def test_upstream_field_is_parsed_and_its_commit_must_exist(self) -> None:
        self.refuses("upstream is neither original nor repo@commit:path", decision_over={"upstream": "somewhere in the world"})
        self.refuses("upstream commit does not exist", decision_over={"upstream": f"Arcanada-one/knowledge-contract@{'a' * 40}:README.md"})

    def test_upstream_in_this_repository_reads_declarations_at_the_upstream_commit(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        probe = World(Path(temp.name))
        upstream = f"Arcanada-one/knowledge-contract@{probe.S}:README.md"
        manifest, files = self.world(upstreams={DOCS[0]: upstream}).run()
        self.assertEqual(set(files), {DOCS[0]})

    def test_upstream_in_another_repository_needs_recorded_declarations(self) -> None:
        ext = f"Arcanada-one/contract-place-site@{'7' * 40}:public/llms.txt"
        manifest, files = self.world(docs=DOCS[:2], upstreams={DOCS[1]: ext}).run()
        self.assertEqual(manifest["row_count"], 2)
        for knob in ("external_decl_absent", "external_decl_missing", "external_decl_empty"):
            with self.subTest(knob=knob):
                with self.assertRaisesRegex(export.ExportError, "external license declarations|other upstream repositories"):
                    self.world(docs=DOCS[:2], upstreams={DOCS[1]: ext}, **{knob: True}).run()

    def test_rights_holder_must_be_a_named_person_and_basis_must_quote_the_reuse_holder(self) -> None:
        for holder in ("Knowledge Contract Arcana contributors", "TBD", "pavel", "Pavel Valentov and contributors"):
            with self.subTest(holder=holder):
                self.refuses("rights holder is not a named person", decision_over={"rights_holder": holder})
        self.refuses("does not quote the holder string", decision_over={"rights_basis": "author declaration only"})

    def test_tree_write_once_fires_alone_when_an_unreferenced_batch_file_is_renamed(self) -> None:
        w = self.world()
        w.decision_pr("b7", [], parent=w.main)
        (w.repo / DEC / "b7.jsonl").rename(w.repo / DEC / "b8.jsonl")
        w.main = commit(w.repo, "rename an empty batch file (#91)")
        w.merged[w.main] = 91
        with self.assertRaisesRegex(export.ExportError, "write-once"):
            w.run()
        with patch.object(export, "check_write_once", lambda m: None):
            self.assertEqual(w.run()[0]["row_count"], 1)

    def test_source_first_parent_fires_alone_for_a_side_branch_commit_that_is_an_ancestor_of_the_base(self) -> None:
        w = self.world(source_side_merged=True)
        with self.assertRaisesRegex(export.ExportError, "first-parent commit of main"):
            w.run()
        with patch.object(export, "first_parent_order", lambda m: {**{r: i for i, r in enumerate(git(w.repo, "rev-list", "--first-parent", "--reverse", m).split())}, w.X: 10 ** 6}):
            self.assertEqual(w.run()[0]["row_count"], 1)

    @unittest.skipUnless(shutil.which("gitleaks"), "gitleaks binary not installed: real secret_scan test skipped")
    def test_real_gitleaks_scan_quarantines_a_secret_shape_that_the_builtin_pattern_misses(self) -> None:
        token = "xoxb-" + "123456789012-1234567890123-" + "AbCdEfGhIjKlMnOpQrStUvWx"
        self.assertIsNone(export.SECRET_SHAPE.search(token.encode()))
        with self.assertRaisesRegex(export.ExportError, "quarantined"):
            export.secret_scan(("token = " + token + "\n").encode())
        export.secret_scan(b"plain public text about a bounded statement\n")

    def test_a_row_cannot_be_swapped_in_through_an_unparsable_table_and_a_later_clean_change(self) -> None:
        w = self.world(no_rows=True)
        row = w.row(DOCS[0], "b1", 0)
        write(w.repo, "corpus/README.md", table([row]) + "| junk |\n")
        dirty = commit(w.repo, "row plus a junk table line (#31)")
        w.merged[dirty] = 31
        clean = w.add_rows([row])
        with self.assertRaisesRegex(export.ExportError, "does not parse"):
            w.run(clean)
        # without that guard the clean change would be taken for the row's change and the export would go through
        with patch.object(export, "_parses", lambda text: True):
            self.assertEqual(w.run(clean)[0]["row_count"], 1)

    def test_a_directly_pushed_row_with_smuggled_files_is_refused_even_when_the_table_is_later_cleaned(self) -> None:
        w = self.world(no_rows=True)
        row = w.row(DOCS[0], "b1", 0)
        write(w.repo, "tools/smuggled.py", "x = 1\n")
        write(w.repo, "corpus/README.md", table([row]) + "| junk |\n")
        commit(w.repo, "direct push: row, smuggled file, junk line")
        clean = w.add_rows([row])
        with self.assertRaisesRegex(export.ExportError, "does not parse"):
            w.run(clean)
        with patch.object(export, "_parses", lambda text: True):
            with self.assertRaisesRegex(export.ExportError, "not a merged pull request commit"):
                w.run(clean)

    def test_upstream_repository_names_are_compared_case_insensitively_and_aliases_are_refused(self) -> None:
        self.refuses("upstream commit does not exist", decision_over={"upstream": f"arcanada-one/Knowledge-Contract@{'a' * 40}:README.md"})
        self.refuses("upstream is neither original nor repo@commit:path", decision_over={"upstream": f"Arcanada-one/knowledge-contract.git@{'a' * 40}:README.md"})
        self.refuses("upstream is neither original nor repo@commit:path", decision_over={"upstream": f"Arcanada-one/knowledge-contract.GIT@{'a' * 40}:README.md"})

    def test_a_lowercase_or_uppercase_contributors_holder_is_refused(self) -> None:
        for holder in ("Pavel Valentov Contributors", "PAVEL VALENTOV CONTRIBUTORS", "Pavel Valentov contributors"):
            with self.subTest(holder=holder):
                self.refuses("rights holder is not a named person", decision_over={"rights_holder": holder})

    def test_file_name_order_within_one_decision_change_is_bytewise(self) -> None:
        # in one change, "B1.jsonl" sorts before "a1.jsonl" bytewise (uppercase first), so a1 holds the last line
        for last_status, expect_ok in (("current", True), ("withdrawn", False)):
            with self.subTest(last=last_status):
                w = self.world(no_rows=True)
                doc = DOCS[0]
                first_status = "withdrawn" if last_status == "current" else "current"
                w.decision_pr("a1", [decision_obj(doc, w.sha[doc], last_status, "a1", attribution="in a1")], parent=w.main,
                              extra={"B1": [decision_obj(doc, w.sha[doc], first_status, "B1", attribution="in B1")]})
                cur = "a1" if last_status == "current" else "B1"
                index_cell = f"{DEC}{cur}.jsonl@{w.batches['a1']['I']}#" + (w.batches["a1"]["lsha"][0] if cur == "a1" else w.batches["a1"]["extra"]["B1"][0])
                # the earlier b1 batch is also current for this key: reference the last current line (a1 or B1) explicitly
                r = w.add_rows([w.row(doc, "b1", 0, cell=index_cell)])
                if expect_ok:
                    self.assertEqual(w.run(r)[0]["row_count"], 1)
                else:
                    with self.assertRaisesRegex(export.ExportError, "later decision changes the effective status|does not point at the last matching line"):
                        w.run(r)

    def test_checklist_is_pinned_by_digest(self) -> None:
        w = self.world()
        with patch.object(export, "CHECKLIST_TEXT", export.CHECKLIST_TEXT + "weaker item\n"):
            with self.assertRaisesRegex(export.ExportError, "checklist differs from the pinned digest"):
                w.run()

    # ---- hardening follow-up (DEC-AUP-0171 amendment 1 item 6): checks that no earlier test isolated ----
    def _add_merged_commit(self, w: World, message: str, number: int) -> str:
        sha = commit(w.repo, f"{message} (#{number})")
        w.merged[sha] = number
        w.main = sha
        return sha

    def _craft_decision_line(self, **changes) -> str:
        w = self.world(no_rows=True)
        obj = decision_obj(DOCS[0], w.sha[DOCS[0]], batch="b9")
        obj.update(changes)
        write(w.repo, f"{DEC}b9.jsonl", export.canonical(obj) + "\n")
        write(w.repo, f"{RECEIPT}b9.json", "{}")
        main = commit(w.repo, "crafted decision line (#77)")
        with patch.object(export, "REPO", w.repo):
            export.load_decisions(main)
        return main

    def test_decision_line_formats_and_vocabularies_are_enforced_on_their_own(self) -> None:
        self.assertTrue(self._craft_decision_line())
        for field, value in (("path", "articles/x.txt"), ("path", "../articles/x.md"), ("sha256", "abc"), ("sha256", "Z" * 64),
                             ("receipt", "corpus/x.json"), ("receipt", RECEIPT + "b9.JSON")):
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(export.ExportError, "decision line malformed$"):
                    self._craft_decision_line(**{field: value})
        for field, value in (("status", "maybe"), ("license", "MIT"), ("license", "cc-by-4.0")):
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(export.ExportError, "decision line malformed$"):
                    self._craft_decision_line(**{field: value})

    def test_a_symlink_in_the_decision_tree_is_refused_as_not_a_regular_blob(self) -> None:
        w = self.world()
        os.symlink("b1.jsonl", w.repo / DEC / "b9.jsonl")
        main = commit(w.repo, "symlinked batch file (#78)")
        with patch.object(export, "REPO", w.repo):
            with self.assertRaisesRegex(export.ExportError, "not a regular blob"):
                export.load_decisions(main)

    def test_receipt_and_reviewer_key_sets_and_value_formats_are_strict(self) -> None:
        self.refuses("receipt does not bind tuple: malformed", receipt_extra_key=True)
        self.refuses("receipt does not bind tuple: malformed", receipt_head_text=True)
        self.refuses("receipt reviewer entry is malformed", reviewer_extra_key=True)

    def test_row_cells_decision_references_are_checked_by_message(self) -> None:
        row = {"source_commit": "a" * 40, "path": DOCS[0], "sha256": "b" * 64, "rights_holder": HOLDER, "license": "CC-BY-4.0",
               "decision": f"{DEC}b1.jsonl@{'c' * 40}#{'d' * 64}", "status": "current", "supersedes": "none", "status_decision": "none"}
        export.validate_row(row)
        with self.assertRaisesRegex(export.ExportError, "must reference a decision file line digest"):
            export.validate_row({**row, "decision": "https://example.invalid/review"})
        with self.assertRaisesRegex(export.ExportError, "must not have a later status decision"):
            export.validate_row({**row, "status_decision": f"{DEC}b2.jsonl@{'c' * 40}#{'e' * 64}"})
        for bad in ("none", "", "https://example.invalid/x", f"{DEC}b2.jsonl@{'c' * 40}#short"):
            with self.subTest(status_decision=bad):
                with self.assertRaisesRegex(export.ExportError, "needs a precise later status decision"):
                    export.validate_row({**row, "status": "withdrawn", "status_decision": bad})

    def test_the_same_source_commit_and_path_twice_is_refused_before_anything_else(self) -> None:
        row = {"source_commit": "a" * 40, "path": DOCS[0], "sha256": "b" * 64, "rights_holder": HOLDER, "license": "CC-BY-4.0",
               "decision": f"{DEC}b1.jsonl@{'c' * 40}#{'d' * 64}", "status": "current", "supersedes": "none", "status_decision": "none"}
        with self.assertRaisesRegex(export.ExportError, "duplicate source commit/path row"):
            export.build("b" * 40, [row, dict(row)])

    def test_content_edited_between_the_source_commit_and_the_base_does_not_export_under_the_old_source(self) -> None:
        # the decision digest is the blob at the receipt base (the edited text); the row points at the older source commit
        self.refuses("source blob digest differs from allowlist", changed_after_source=True)

    def test_a_pull_request_that_does_not_target_main_is_not_a_merged_pull_request_commit(self) -> None:
        self.refuses("does not target main", pull_base="release")

    def test_every_receipts_file_is_scanned_even_when_no_receipt_names_it(self) -> None:
        w = self.world()
        write(w.repo, f"{RECEIPT}b1/reviewer-9.md", "stray note that mentions /home/someone/file\n")
        self._add_merged_commit(w, "unreferenced receipts file", 92)
        with self.assertRaisesRegex(export.ExportError, "host path, host name or address"):
            w.run()

    def test_decision_files_are_scanned_for_host_strings(self) -> None:
        self.refuses("host path, host name or address", decision_over={"third_party": "seen at 10.1.2.3 on the build host"})
        self.refuses("host path, host name or address", decision_over={"limits": "FD12:3456::1 is not a public address"})

    def test_the_loader_scans_decision_files_itself_for_host_strings(self) -> None:
        # load_decisions alone (no receipt check, so the reviewer input cannot catch it first)
        for field, value in (("third_party", "seen at 10.1.2.3 on the build host"), ("limits", "see /home/someone/notes"),
                             ("attribution", "FD12:3456::1 is private")):
            with self.subTest(field=field):
                with self.assertRaisesRegex(export.ExportError, "host path, host name or address"):
                    self._craft_decision_line(**{field: value})

    def test_rights_basis_must_say_that_contributor_parts_rest_on_dco_sign_offs(self) -> None:
        self.refuses("DCO sign-offs", decision_over={"rights_basis": f"author declaration in NOTICE; REUSE.toml holder string: {REUSE_HOLDER}"})

    def test_dco_must_appear_as_a_whole_word(self) -> None:
        base = f"author declaration in NOTICE; REUSE.toml holder string: {REUSE_HOLDER}; "
        for text in ("DCOM sign-offs are declared", "noDCO sign-offs", "dco sign-offs", "the DCOs"):
            with self.subTest(text=text):
                self.refuses("DCO sign-offs", decision_over={"rights_basis": base + text})
        manifest, _ = self.world(decision_over={"rights_basis": base + "contributor parts rest on DCO sign-offs, declared and not verified"}).run()
        self.assertEqual(manifest["row_count"], 1)

    def test_a_decision_file_with_a_host_string_is_named_as_a_decision_file(self) -> None:
        with self.assertRaisesRegex(export.ExportError, "^decision file carries a host path, host name or address"):
            self._craft_decision_line(third_party="seen at 10.1.2.3 on the build host")

    def test_notice_author_line_shapes_are_pinned(self) -> None:
        # accepted: no comma (the whole text after `Author:` is the name); refused: indent, lower case, Co-Author
        manifest, _ = self.world(notice="Notice\nAuthor: Pavel Valentov\n").run()
        self.assertEqual(manifest["entries"][0]["rights_holder"], "Pavel Valentov")
        for notice in ("Notice\n  Author: Pavel Valentov, Independent Researcher\n",
                       "Notice\nauthor: Pavel Valentov, Independent Researcher\n",
                       "Notice\nCo-Author: Pavel Valentov, Independent Researcher\n",
                       "Notice\nContact: Pavel Valentov\n"):
            with self.subTest(notice=notice):
                self.refuses("not the author named in NOTICE", notice=notice)

    def test_rights_holder_must_be_the_author_named_in_notice_at_the_source_commit(self) -> None:
        self.refuses("not the author named in NOTICE", decision_over={"rights_holder": "Another Person"}, row_holder="Another Person")
        manifest, _ = self.world(decision_over={"rights_holder": "Corrected Holder"}, row_holder="Corrected Holder").run()
        self.assertEqual(manifest["entries"][0]["rights_holder"], "Corrected Holder")

    def test_the_notice_author_must_equal_the_rights_holder_not_merely_start_with_it(self) -> None:
        for holder in ("Pavel Va", "Pavel Valento", "Pavel Valentov Junior", "Pavel"):
            with self.subTest(holder=holder):
                if len(holder.split()) < 2:
                    continue  # a single word is refused earlier as not a named person
                self.refuses("not the author named in NOTICE", decision_over={"rights_holder": holder}, row_holder=holder)
        manifest, _ = self.world().run()
        self.assertEqual(manifest["entries"][0]["rights_holder"], "Pavel Valentov")

    def test_squash_merged_decision_pull_request_is_refused(self) -> None:
        self.refuses("head not recoverable: a decision pull request must be merged", squash_decision=True)
        self.refuses("head not recoverable: merge commit does not carry", api_head="4" * 40)

    def test_host_path_or_address_in_a_transcript_is_refused(self) -> None:
        self.refuses("host path, host name or address", transcript_text="read /home/someone/file and 10.1.2.3\n")

    def test_retained_records_must_be_introduced_in_the_receipt_range_and_stay_unchanged(self) -> None:
        w = self.world()
        b = w.batches["b1"]
        path = f"{RECEIPT}b1.json"
        with patch.object(export, "REPO", w.repo):
            self.assertTrue(export.retained_record(w.main, b["I"], b["D1"], b["D2"], path))
            with self.assertRaisesRegex(export.ExportError, "not introduced in the receipt commit range"):
                export.retained_record(w.main, b["I"], b["D1"], b["D2"], DEC + "b1.jsonl")
            with self.assertRaisesRegex(export.ExportError, "already existed at the reviewed head"):
                self._existed(w, b, path)
            (w.repo / path).write_text("{}")
            changed = commit(w.repo, "receipt altered later")
            with self.assertRaisesRegex(export.ExportError, "changed after its decision change"):
                export.retained_record(changed, b["I"], b["D1"], b["D2"], path)

    def _existed(self, w: World, b: dict, path: str) -> None:
        # a head that already carries the path: the merge commit itself serves as such a head, with an empty range after it
        with patch.object(export, "changed_paths", lambda a, c: [path]):
            export.retained_record(w.main, b["I"], b["I"], b["D2"], path)

    def test_v1_review_route_is_gone(self) -> None:
        self.assertFalse(hasattr(export, "publication_review"))
        self.assertFalse(hasattr(export, "status_review"))


class ExportBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.content = b"# Public example\nA bounded statement.\n"
        self.row = {
            "source_commit": "a" * 40,
            "path": "articles/project-overview.md",
            "sha256": hashlib.sha256(self.content).hexdigest(),
            "rights_holder": "Example contributor",
            "license": "CC-BY-4.0",
            "decision": "corpus/publication-decisions/b1.jsonl@" + "c" * 40 + "#" + "d" * 64,
            "status": "current",
            "supersedes": "none",
            "status_decision": "none",
        }

    def test_the_committed_table_parses_and_an_empty_table_exports_no_files(self) -> None:
        text = (export.REPO / "corpus/README.md").read_text()
        committed = export.parse_allowlist(text)  # the committed table must parse, whatever rows it holds
        self.assertTrue(all(row["path"] in export.SCOPE_PATHS for row in committed))
        rows = export.parse_allowlist("\n".join(export.strip_rows(text)))
        self.assertEqual(rows, [])
        manifest, files = export.build("b" * 40, rows)
        self.assertEqual((manifest["row_count"], manifest["export_count"], files), (0, 0, {}))
        self.assertEqual(manifest["status"], "empty_allowlist")

    def test_malformed_or_late_rows_refuse_instead_of_disappearing(self) -> None:
        base = export.HEADER + "\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        row = "| " + " | ".join(self.row.values()) + " |\n"
        for body in (row.removeprefix("| "), "\n" + row, row + "interposed note\n" + row):
            with self.subTest(body=body):
                with self.assertRaises(export.ExportError):
                    export.parse_allowlist(base + body)

    def test_secret_shaped_candidate_is_quarantined(self) -> None:
        with self.assertRaisesRegex(export.ExportError, "secret-shaped"):
            export.secret_scan(b"-----BEGIN PRIVATE KEY-----\nsynthetic\n")

    def test_unmerged_source_commit_refuses(self) -> None:
        class Result:
            returncode = 1

        with patch.object(export, "command", return_value=Result()):
            with self.assertRaisesRegex(export.ExportError, "not merged"):
                export.git_blob("a" * 40, "papers/example.md", "b" * 40)

    def test_bundle_is_not_published_before_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "bundle"
            with patch.object(export.Path, "write_bytes", side_effect=OSError("synthetic write failure")):
                with self.assertRaises(OSError):
                    export.write_bundle(output, {"schema": "fixture"}, {"papers/example.md": self.content})
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_draft_path_and_license_uncertainty_refuse(self) -> None:
        for update in ({"path": "../private/draft.md"}, {"license": "unknown"}, {"decision": "https://example.invalid/review"}, {"path": "schemas/x.json"}, {"path": "articles/a.txt"}):
            with self.subTest(update=update):
                with self.assertRaises(export.ExportError):
                    export.validate_row({**self.row, **update})

    def test_superseded_revision_requires_linked_new_row(self) -> None:
        old = {**self.row, "status": "superseded", "status_decision": "corpus/publication-decisions/b2.jsonl@" + "c" * 40 + "#" + "e" * 64}
        with self.assertRaisesRegex(export.ExportError, "no linked replacement"):
            export.build("b" * 40, [old])

    def test_two_current_revisions_of_same_path_refuse(self) -> None:
        second = {**self.row, "source_commit": "b" * 40}
        with self.assertRaisesRegex(export.ExportError, "multiple current"):
            export.build("b" * 40, [self.row, second])


if __name__ == "__main__":
    unittest.main()
