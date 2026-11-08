#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Controls for tools/verify_retrieval_context.py, including title-only projection.

These assert exit codes. Fixtures are built in temporary directories from the
accepted paper blob bytes; modified manuscript copies are not committed.
"""
from __future__ import annotations

import hashlib
import json
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
MAIN_CLEAR_NAMES_SHA256 = "a27a209c419480f2eb3c80e826c0da507fece1c1c66045d5c34d647656c3c2a9"
ACCEPTED_TITLE = "Retrieval, Coverage, and Context Composition under Resource Limits"
ACCEPTED_SLUG = "retrieval-coverage-and-context-composition-under-resource-limits"


def accepted_bytes() -> bytes:
    """Pinned accepted edition bytes from git, not whatever HEAD currently names PAPER.md."""
    data = subprocess.check_output(["git", "cat-file", "-p", ACCEPTED_BLOB], cwd=str(ROOT))
    if hashlib.sha256(data).hexdigest() != PAPER_SHA256:
        raise AssertionError("accepted paper blob drifted from PAPER_SHA256")
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


def clear_names_text() -> str:
    """Exact main@4d0a0ed Clear Names bytes for this paper, built from the accepted blob."""
    # Prefer the live tree when it already matches the measured Clear Names digest.
    if PAPER.is_file() and hashlib.sha256(PAPER.read_bytes()).hexdigest() == MAIN_CLEAR_NAMES_SHA256:
        return PAPER.read_text(encoding="utf-8")
    text = accepted_bytes().decode("utf-8")
    text = text.replace(
        f'title: "{ACCEPTED_TITLE}"\n',
        (
            f'title: "Context Assembly: {ACCEPTED_TITLE}"\n'
            f'short_title: "Context Assembly"\n'
            f'subtitle: "{ACCEPTED_TITLE}"\n'
            f'previous_title: "{ACCEPTED_TITLE}"\n'
        ),
        1,
    )
    text = text.replace(
        f"# {ACCEPTED_TITLE}\n",
        (
            "<!-- markdownlint-disable-next-line MD033 -->\n"
            f'<a id="{ACCEPTED_SLUG}"></a>\n'
            "\n"
            f"# Context Assembly: {ACCEPTED_TITLE}\n"
        ),
        1,
    )
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if digest != MAIN_CLEAR_NAMES_SHA256:
        raise AssertionError(f"synthetic Clear Names bytes drifted: {digest}")
    return text


class AcceptedPaperControls(unittest.TestCase):
    def test_accepted_blob_materialization_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), accepted_bytes())
            result = run_checker(["--paper", str(paper)])
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["pass"])


class TitleOnlyPositiveControls(unittest.TestCase):
    def test_title_only_against_accepted_blob_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), accepted_bytes())
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertTrue(report["pass"])

    def test_synthetic_title_only_change_exits_zero(self) -> None:
        data = accepted_bytes().decode("utf-8")
        data = data.replace(
            f'title: "{ACCEPTED_TITLE}"',
            'title: "Synthetic Title Only Projection"',
            1,
        )
        data = data.replace(
            f"# {ACCEPTED_TITLE}\n",
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

    def test_main_clear_names_bytes_pass_title_only(self) -> None:
        text = clear_names_text()
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertTrue(report["pass"])


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
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_changed_number_exits_nonzero(self) -> None:
        mutated = self._mutate_body("Four judgments are needed.", "Five judgments are needed.")
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), mutated)
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_changed_premise_exits_nonzero(self) -> None:
        mutated = self._mutate_body("the ground set is finite", "the ground set is infinite")
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), mutated)
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_unknown_source_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), accepted_bytes())
            result = run_checker(
                [
                    "--paper",
                    str(paper),
                    "--title-only-against",
                    "0000000000000000000000000000000000000000",
                ]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "unknown_source")

    def test_incomplete_mapping_unknown_front_matter_key_exits_nonzero(self) -> None:
        text = clear_names_text().replace(
            'previous_title: "Retrieval, Coverage, and Context Composition under Resource Limits"\n',
            (
                'previous_title: "Retrieval, Coverage, and Context Composition under Resource Limits"\n'
                'editorial_note: "not allowlisted"\n'
            ),
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_previous_title_must_equal_accepted_title(self) -> None:
        text = clear_names_text().replace(
            f'previous_title: "{ACCEPTED_TITLE}"',
            'previous_title: "Wrong Previous Title"',
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_anchor_id_must_be_accepted_slug(self) -> None:
        text = clear_names_text().replace(
            f'<a id="{ACCEPTED_SLUG}"></a>',
            '<a id="wrong-slug"></a>',
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_extra_line_before_h1_exits_nonzero(self) -> None:
        text = clear_names_text().replace(
            "<!-- markdownlint-disable-next-line MD033 -->\n",
            "<!-- markdownlint-disable-next-line MD033 -->\n<!-- extra -->\n",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_h1_must_equal_new_title(self) -> None:
        text = clear_names_text().replace(
            f"# Context Assembly: {ACCEPTED_TITLE}\n",
            "# Mismatched Heading\n",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), text.encode("utf-8"))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "incomplete_mapping")

    def test_body_byte_flip_after_valid_title_change_exits_nonzero(self) -> None:
        data = bytearray(clear_names_text().encode("utf-8"))
        data[4000] ^= 0x01
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), bytes(data))
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            json.loads(result.stdout)["refusal_reason"],
            {"incomplete_mapping", "corrupted_candidate"},
        )

    def test_unsupported_version_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), accepted_bytes())
            result = run_checker(
                [
                    "--paper",
                    str(paper),
                    "--title-only-against",
                    ACCEPTED_BLOB,
                    "--title-only-version",
                    "99",
                ]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["refusal_reason"], "unsupported_version")

    def test_truncated_copy_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), accepted_bytes()[:200])
            result = run_checker(
                ["--paper", str(paper), "--title-only-against", ACCEPTED_BLOB]
            )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            json.loads(result.stdout)["refusal_reason"],
            {"incomplete_mapping", "corrupted_candidate"},
        )


class DefaultModeCorruptionControls(unittest.TestCase):
    def test_default_mode_rejects_byte_flip_on_accepted_bytes(self) -> None:
        data = bytearray(accepted_bytes())
        data[4000] ^= 0x01
        with tempfile.TemporaryDirectory() as tmp:
            paper = write_paper(Path(tmp), bytes(data))
            result = run_checker(["--paper", str(paper)])
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse(json.loads(result.stdout)["pass"])


if __name__ == "__main__":
    unittest.main()
