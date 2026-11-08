#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Controls for tools/verify_retrieval_context.py, including title-only projection.

These assert exit codes. Fixtures are built in temporary directories from the
accepted paper bytes; modified manuscript copies are not committed.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "verify_retrieval_context.py"
PAPER = ROOT / "papers" / "retrieval-and-context-composition" / "PAPER.md"
ACCEPTED_BLOB = "9311c0d157d5a926e3c08f6a087a53866064f4e0"
PAPER_SHA256 = "e457fadcb17424e15083504a2babb2646aedc8aec7370048cd77854a8c7af64f"


def accepted_bytes() -> bytes:
    data = PAPER.read_bytes()
    if hashlib.sha256(data).hexdigest() != PAPER_SHA256:
        raise AssertionError("accepted paper bytes drifted from PAPER_SHA256")
    return data


def run_checker(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(CHECKER), *args],
        cwd=str(cwd or ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def write_paper(directory: Path, data: bytes) -> Path:
    path = directory / "PAPER.md"
    path.write_bytes(data)
    return path


class AcceptedPaperControls(unittest.TestCase):
    def test_accepted_paper_exits_zero(self) -> None:
        result = run_checker(["--paper", str(PAPER)])
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["pass"])
        self.assertEqual(report["document"]["passed"], report["document"]["total"])


class TitleOnlyPositiveControls(unittest.TestCase):
    def test_title_only_against_accepted_blob_exits_zero(self) -> None:
        result = run_checker(
            ["--paper", str(PAPER), "--title-only-against", ACCEPTED_BLOB]
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertTrue(report["pass"])
        self.assertEqual(report["record_type"], "retrieval-context-title-only-projection/1")

    def test_synthetic_title_only_change_exits_zero(self) -> None:
        data = accepted_bytes().decode("utf-8")
        data = data.replace(
            'title: "Retrieval, Coverage, and Context Composition under Resource Limits"',
            'title: "Synthetic Title Only Projection"',
            1,
        )
        data = data.replace(
            "# Retrieval, Coverage, and Context Composition under Resource Limits\n",
            "# Synthetic Title Only Projection\n",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), data.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertTrue(report["pass"])
        self.assertEqual(sorted(report["title_fields_changed"]), ["h1", "title"])


class TitleOnlyNegativeControls(unittest.TestCase):
    def _mutate_body(self, old: str, new: str) -> bytes:
        text = accepted_bytes().decode("utf-8")
        if old not in text:
            raise AssertionError(f"fixture needle missing: {old!r}")
        return text.replace(old, new, 1).encode("utf-8")

    def test_changed_negation_exits_nonzero(self) -> None:
        mutated = self._mutate_body(
            "a complete dependency graph is not evidence that its conditions survived delivery",
            "a complete dependency graph is evidence that its conditions survived delivery",
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), mutated)
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertFalse(report["pass"])
        self.assertEqual(report["refusal_reason"], "incomplete_mapping")

    def test_changed_number_exits_nonzero(self) -> None:
        mutated = self._mutate_body("Four judgments are needed.", "Five judgments are needed.")
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), mutated)
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["refusal_reason"], "incomplete_mapping")

    def test_changed_premise_exits_nonzero(self) -> None:
        mutated = self._mutate_body(
            "the ground set is finite",
            "the ground set is infinite",
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), mutated)
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["refusal_reason"], "incomplete_mapping")

    def test_unknown_source_exits_nonzero(self) -> None:
        result = run_checker(
            [
                "--paper",
                str(PAPER),
                "--title-only-against",
                "0000000000000000000000000000000000000000",
            ]
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["refusal_reason"], "unknown_source")

    def test_incomplete_mapping_extra_front_matter_key_exits_nonzero(self) -> None:
        text = accepted_bytes().decode("utf-8")
        text = text.replace(
            'title: "Retrieval, Coverage, and Context Composition under Resource Limits"\n',
            'title: "Synthetic Title Only Projection"\nshort_title: "Synthetic"\n',
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["refusal_reason"], "incomplete_mapping")

    def test_unsupported_version_exits_nonzero(self) -> None:
        result = run_checker(
            [
                "--paper",
                str(PAPER),
                "--title-only-against",
                ACCEPTED_BLOB,
                "--title-only-version",
                "99",
            ]
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["refusal_reason"], "unsupported_version")

    def test_truncated_copy_exits_nonzero(self) -> None:
        truncated = accepted_bytes()[:200]
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), truncated)
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertIn(report["refusal_reason"], {"incomplete_mapping", "corrupted_candidate"})

    def test_byte_flip_exits_nonzero(self) -> None:
        data = bytearray(accepted_bytes())
        # Flip a body byte well after the title block.
        index = 4000
        data[index] = data[index] ^ 0x01
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), bytes(data))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertIn(report["refusal_reason"], {"incomplete_mapping", "corrupted_candidate"})


class DefaultModeCorruptionControls(unittest.TestCase):
    def test_default_mode_rejects_byte_flip(self) -> None:
        data = bytearray(accepted_bytes())
        data[4000] ^= 0x01
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), bytes(data))
            result = run_checker(["--paper", str(paper)])
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertFalse(report["pass"])


if __name__ == "__main__":
    unittest.main()
