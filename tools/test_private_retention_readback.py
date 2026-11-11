#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Unit tests for check_private_retention_readback."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_private_retention_readback.py"
FIXTURES = ROOT / "schemas" / "fixtures" / "private-retention-readback"


def run_check(doc: dict) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(doc, handle)
        path = handle.name
    return subprocess.run(
        [sys.executable, str(CHECKER), path],
        capture_output=True,
        text=True,
        check=False,
    )


class TestPrivateRetentionReadbackChecker(unittest.TestCase):
    def test_valid_fixtures(self) -> None:
        for name in (
            "profile-valid.json",
            "readback-matched.json",
            "tombstone-collected.json",
        ):
            path = FIXTURES / name
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_refuse_path_disclosed(self) -> None:
        doc = json.loads((FIXTURES / "readback-matched.json").read_text())
        doc["resolution"]["path_disclosed"] = True
        result = run_check(doc)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("path_disclosed", result.stderr + result.stdout)

    def test_refuse_digest_mismatch_vs_id(self) -> None:
        doc = json.loads((FIXTURES / "readback-matched.json").read_text())
        doc["sha256"] = "0" * 64
        result = run_check(doc)
        self.assertNotEqual(result.returncode, 0)

    def test_refuse_knowledge_admitted(self) -> None:
        doc = json.loads((FIXTURES / "profile-valid.json").read_text())
        doc["knowledge_admitted"] = True
        result = run_check(doc)
        self.assertNotEqual(result.returncode, 0)

    def _receipt(self) -> dict:
        return json.loads((FIXTURES / "readback-matched.json").read_text())

    def _refused(self, doc: dict, needle: str) -> None:
        result = run_check(doc)
        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertIn(needle, result.stderr + result.stdout)

    def test_refuse_size_bytes_that_is_not_a_nonnegative_integer(self) -> None:
        for value in ("12", True, 12.5, -0.5, -1, None):
            with self.subTest(size_bytes=value):
                doc = self._receipt()
                doc["size_bytes"] = value
                self._refused(doc, "size_bytes")
        doc = self._receipt()
        del doc["size_bytes"]
        self._refused(doc, "size_bytes")

    def test_refusal_code_must_be_in_the_closed_set(self) -> None:
        doc = self._receipt()
        doc["outcome"] = "refused"
        doc["refusal_code"] = "invented-code"
        self._refused(doc, "refusal_code")
        doc["refusal_code"] = "corrupt"
        self.assertEqual(run_check(doc).returncode, 0)
        del doc["refusal_code"]
        self._refused(doc, "refusal_code")
        matched = self._receipt()
        matched["refusal_code"] = None
        self._refused(matched, "refusal_code")

    def test_refuse_published_corpus_admission_outside_closed_set(self) -> None:
        for value in ("accepted", "", None):
            with self.subTest(published_corpus_admission=value):
                doc = self._receipt()
                doc["published_corpus_admission"] = value
                self._refused(doc, "published_corpus_admission")
        doc = self._receipt()
        del doc["published_corpus_admission"]
        self._refused(doc, "published_corpus_admission")
        doc["published_corpus_admission"] = "not_applicable"
        self.assertEqual(run_check(doc).returncode, 0)

    def test_refuse_unknown_receipt_or_resolution_field(self) -> None:
        doc = self._receipt()
        doc["resolution"]["path"] = "/synthetic/private/source"
        self._refused(doc, "unknown resolution field")
        doc = self._receipt()
        doc["path"] = "/synthetic/private/source"
        self._refused(doc, "unknown receipt field")
        doc = self._receipt()
        doc["resolution"]["role"] = "original"
        self.assertEqual(run_check(doc).returncode, 0)

    def test_schema_and_checker_agree_on_every_case(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(json.loads((ROOT / "schemas" / "private-retention-readback.schema.json").read_text()))

        def mutate(**changes):
            doc = self._receipt()
            for key, value in changes.items():
                if key == "resolution_extra":
                    doc["resolution"].update(value)
                elif value is KeyError:
                    del doc[key]
                else:
                    doc[key] = value
            return doc

        accepted = [json.loads((FIXTURES / name).read_text()) for name in ("profile-valid.json", "readback-matched.json", "tombstone-collected.json")]
        accepted.append(mutate(outcome="refused", refusal_code="not_found"))
        accepted.append(mutate(published_corpus_admission="not_applicable"))
        rejected = [
            mutate(size_bytes="12"), mutate(size_bytes=True), mutate(size_bytes=12.5), mutate(size_bytes=-0.5),
            mutate(size_bytes=-1), mutate(size_bytes=KeyError),
            mutate(outcome="refused", refusal_code="invented-code"), mutate(outcome="refused"),
            mutate(refusal_code="not_found"),
            mutate(published_corpus_admission=KeyError), mutate(published_corpus_admission="accepted"),
            mutate(resolution_extra={"path": "/synthetic/private/source"}), mutate(path="/synthetic/private/source"),
            mutate(resolution_extra={"path_disclosed": True}), mutate(knowledge_admitted=True),
        ]
        for doc in accepted:
            with self.subTest(accepted=doc):
                self.assertEqual(list(validator.iter_errors(doc)), [])
                self.assertEqual(run_check(doc).returncode, 0)
        for doc in rejected:
            with self.subTest(rejected=doc):
                self.assertNotEqual(list(validator.iter_errors(doc)), [])
                self.assertEqual(run_check(doc).returncode, 1)
        # Rules the schema cannot state: the checker alone enforces them.
        checker_only = [
            mutate(sha256="0" * 64),  # digest must equal the one embedded in object_id
            mutate(object_kind="package"),  # kind must follow the object_id grammar
            mutate(size_bytes=12.0),  # JSON Schema counts 12.0 as an integer; the checker wants a JSON integer
        ]
        for doc in checker_only:
            with self.subTest(checker_only=doc):
                self.assertEqual(list(validator.iter_errors(doc)), [])
                self.assertEqual(run_check(doc).returncode, 1)


if __name__ == "__main__":
    unittest.main()
