#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Tests for check_private_registration.py and committed fixtures."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "schemas" / "fixtures" / "private-artifact-registry"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_private_registration as cpr  # noqa: E402


class CheckPrivateRegistrationTests(unittest.TestCase):
    def test_valid_fixtures(self):
        valid = FIX / "valid"
        self.assertTrue(valid.is_dir())
        for path in sorted(valid.glob("*.json")):
            problems = cpr.validate(json.loads(path.read_text()))
            self.assertEqual(problems, [], msg=f"{path.name}: {problems}")

    def test_invalid_fixtures_each_have_problems(self):
        invalid = FIX / "invalid"
        self.assertTrue(invalid.is_dir())
        for path in sorted(invalid.glob("*.json")):
            problems = cpr.validate(json.loads(path.read_text()))
            self.assertTrue(problems, msg=f"{path.name} expected problems")

    def test_assessor_must_differ(self):
        doc = json.loads((FIX / "valid" / "handoff-accepted.json").read_text())
        doc["acceptance"]["assessor_id"] = doc["acceptance"]["producer_id"]
        problems = cpr.validate(doc)
        self.assertTrue(any("assessor_id must be distinct" in p for p in problems))

    def test_outcomes_require_owner_when_unresolved(self):
        doc = {
            "schema": "PrivatePerBookOutcomes/v1",
            "cohort": "drive-books-18",
            "books": [{"book_id": "RU10", "status": "unresolved"}],
            "runtime_authorized": False,
            "knowledge_admitted": False,
            "kc2_admission": "not_measured",
        }
        problems = cpr.validate(doc)
        self.assertTrue(any("owner and blocking_reason" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
