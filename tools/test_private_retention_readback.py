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


if __name__ == "__main__":
    unittest.main()
