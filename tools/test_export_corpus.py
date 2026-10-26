"""Boundary tests for the public corpus candidate exporter."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from tools import export_corpus as export


class ExportBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.content = b"# Public example\nA bounded statement.\n"
        self.row = {
            "source_commit": "a" * 40,
            "path": "papers/example.md",
            "sha256": hashlib.sha256(self.content).hexdigest(),
            "rights_holder": "Example contributor",
            "license": "CC-BY-4.0",
            "decision": "https://github.com/Arcanada-one/knowledge-contract/pull/5#pullrequestreview-123",
            "status": "current",
            "supersedes": "none",
            "status_decision": "none",
        }

    def test_current_empty_allowlist_exports_no_files(self) -> None:
        rows = export.parse_allowlist((export.REPO / "corpus/README.md").read_text())
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

    def test_pinned_regular_blob_produces_candidate_only(self) -> None:
        with patch.object(export, "publication_review"), patch.object(export, "git_blob", return_value=self.content), patch.object(export, "secret_scan"):
            manifest, files = export.build("b" * 40, [self.row])
        self.assertEqual(files, {"papers/example.md": self.content})
        self.assertEqual(manifest["kc2_runtime_admission"], "not_measured")
        self.assertEqual(manifest["scrutator_projection"], "not_applied")

    def test_draft_path_and_license_uncertainty_refuse(self) -> None:
        for update in ({"path": "../private/draft.md"}, {"license": "unknown"}):
            with self.subTest(update=update):
                with self.assertRaises(export.ExportError):
                    export.validate_row({**self.row, **update})

    def test_changed_bytes_refuse_before_export(self) -> None:
        with patch.object(export, "publication_review"), patch.object(export, "git_blob", return_value=b"different"):
            with self.assertRaisesRegex(export.ExportError, "digest differs"):
                export.build("b" * 40, [self.row])

    def test_secret_shaped_candidate_is_quarantined(self) -> None:
        with self.assertRaisesRegex(export.ExportError, "secret-shaped"):
            export.secret_scan(b"-----BEGIN PRIVATE KEY-----\nsynthetic\n")

    def test_withdrawn_revision_is_recorded_but_not_exported(self) -> None:
        row = {**self.row, "status": "withdrawn",
               "status_decision": "https://github.com/Arcanada-one/knowledge-contract/pull/6#pullrequestreview-456"}
        with patch.object(export, "publication_review"), patch.object(export, "status_review"), \
                patch.object(export, "git_blob", return_value=self.content), patch.object(export, "secret_scan"):
            manifest, files = export.build("b" * 40, [row])
        self.assertEqual(files, {})
        self.assertEqual(manifest["entries"][0]["public_export"], "withheld")

    def test_unmerged_source_commit_refuses(self) -> None:
        class Result:
            returncode = 1

        with patch.object(export, "command", return_value=Result()):
            with self.assertRaisesRegex(export.ExportError, "not merged"):
                export.git_blob("a" * 40, "papers/example.md", "b" * 40)

    def test_publication_review_must_match_exact_merged_head(self) -> None:
        pr = {"merged_at": "2026-10-26T00:00:00Z", "merge_commit_sha": "a" * 40,
              "head": {"sha": "c" * 40}, "user": {"login": "author"}}
        decision = {key: self.row[key] for key in ("path", "sha256", "rights_holder", "license", "status")}
        decision["reviewed_head"] = "c" * 40
        review = {"id": 123, "state": "APPROVED", "commit_id": "c" * 40,
                  "submitted_at": "2026-10-26T00:00:00Z", "user": {"login": "reviewer"},
                  "body": "KnowledgeContractPublicationDecision/v1 " + json.dumps(decision)}
        def api(*args, **kwargs):
            value = review if "/reviews/" in args[-1] else pr
            return type("Result", (), {"stdout": json.dumps(value).encode()})()
        with patch.object(export, "command", side_effect=api):
            export.publication_review(self.row)
            review["commit_id"] = "d" * 40
            with self.assertRaisesRegex(export.ExportError, "stale"):
                export.publication_review(self.row)
            review["commit_id"] = "c" * 40
            decision["sha256"] = "d" * 64
            review["body"] = "KnowledgeContractPublicationDecision/v1 " + json.dumps(decision)
            with self.assertRaisesRegex(export.ExportError, "bind exact"):
                export.publication_review(self.row)
            review["body"] = "KnowledgeContractPublicationDecision/v1 " + json.dumps({**decision, "sha256": self.row["sha256"]})
            review["user"] = {}
            with self.assertRaisesRegex(export.ExportError, "absent"):
                export.publication_review(self.row)

    def test_later_status_decision_binds_old_revision(self) -> None:
        row = {**self.row, "status": "withdrawn",
               "status_decision": "https://github.com/Arcanada-one/knowledge-contract/pull/6#pullrequestreview-456"}
        pr = {"merged_at": "2026-10-26T00:00:00Z", "merge_commit_sha": "e" * 40,
              "head": {"sha": "f" * 40}, "user": {"login": "author"}}
        decision = {key: row[key] for key in ("source_commit", "path", "sha256", "status")}
        decision["reviewed_head"] = "f" * 40
        review = {"id": 456, "state": "APPROVED", "commit_id": "f" * 40,
                  "submitted_at": "2026-10-26T00:00:00Z", "user": {"login": "reviewer"},
                  "body": "KnowledgeContractStatusDecision/v1 " + json.dumps(decision)}
        def api(*args, **kwargs):
            if args[:3] == ("git", "merge-base", "--is-ancestor"):
                return type("Result", (), {"returncode": 0})()
            return type("Result", (), {"stdout": json.dumps(review if "/reviews/" in args[-1] else pr).encode()})()
        with patch.object(export, "command", side_effect=api):
            export.status_review(row, "b" * 40)
            review["body"] = review["body"].replace('"withdrawn"', '"current"')
            with self.assertRaisesRegex(export.ExportError, "bind exact"):
                export.status_review(row, "b" * 40)

    def test_superseded_revision_requires_linked_new_row(self) -> None:
        old = {**self.row, "status": "superseded",
               "status_decision": "https://github.com/Arcanada-one/knowledge-contract/pull/6#pullrequestreview-456"}
        with self.assertRaisesRegex(export.ExportError, "no linked replacement"):
            export.build("b" * 40, [old])
        new = {**self.row, "source_commit": "b" * 40, "sha256": "c" * 64,
               "supersedes": old["sha256"]}
        with patch.object(export, "publication_review"), patch.object(export, "status_review"), \
                patch.object(export, "git_blob", return_value=self.content), patch.object(export, "secret_scan"):
            with self.assertRaisesRegex(export.ExportError, "digest differs"):
                export.build("b" * 40, [old, new])

    def test_reviewed_correction_exports_only_new_revision(self) -> None:
        old = {**self.row, "status": "superseded",
               "status_decision": "https://github.com/Arcanada-one/knowledge-contract/pull/6#pullrequestreview-456"}
        replacement = b"# Corrected public example\n"
        new = {**self.row, "source_commit": "b" * 40,
               "sha256": hashlib.sha256(replacement).hexdigest(),
               "supersedes": old["sha256"]}
        def blob(commit, path, main):
            return self.content if commit == old["source_commit"] else replacement
        with patch.object(export, "publication_review"), patch.object(export, "status_review"), \
                patch.object(export, "git_blob", side_effect=blob), patch.object(export, "secret_scan"):
            manifest, files = export.build("b" * 40, [old, new])
        self.assertEqual(files, {"papers/example.md": replacement})
        self.assertEqual(manifest["entries"][0]["public_export"], "withheld")
        self.assertEqual(manifest["entries"][1]["public_export"], "eligible")

    def test_two_current_revisions_of_same_path_refuse(self) -> None:
        second = {**self.row, "source_commit": "b" * 40}
        with patch.object(export, "publication_review"):
            with self.assertRaisesRegex(export.ExportError, "multiple current"):
                export.build("b" * 40, [self.row, second])

    def test_bundle_is_not_published_before_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "bundle"
            with patch.object(export.Path, "write_bytes", side_effect=OSError("synthetic write failure")):
                with self.assertRaises(OSError):
                    export.write_bundle(output, {"schema": "fixture"}, {"papers/example.md": self.content})
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
