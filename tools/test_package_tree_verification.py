#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Tests for the CANDIDATE PackageTreeVerification/v1 schema and checker (KCLIVE-03)."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_package_tree_verification.py"
FIXTURES = ROOT / "schemas" / "fixtures" / "package-tree-verification"
SCHEMA = ROOT / "schemas" / "package-tree-verification.schema.json"
VALID = ("verified-valid.json", "refused-valid.json")


def run_check(doc: object) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(doc, handle)
    return subprocess.run([sys.executable, str(CHECKER), handle.name], capture_output=True, text=True, check=False)


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


class TestPackageTreeVerification(unittest.TestCase):
    def test_valid_fixtures_pass(self) -> None:
        for name in VALID:
            result = run_check(load(name))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_every_invalid_fixture_fails(self) -> None:
        names = sorted(p.name for p in FIXTURES.glob("invalid-*.json"))
        self.assertGreaterEqual(len(names), 11)
        for name in names:
            self.assertNotEqual(run_check(load(name)).returncode, 0, name)

    def test_each_required_field_missing(self) -> None:
        doc = load("verified-valid.json")
        for key in list(doc):
            bad = copy.deepcopy(doc)
            del bad[key]
            self.assertNotEqual(run_check(bad).returncode, 0, key)
        for key in doc["resolution"]:
            bad = copy.deepcopy(doc)
            del bad["resolution"][key]
            self.assertNotEqual(run_check(bad).returncode, 0, key)

    def test_coerced_numbers_are_refused(self) -> None:
        for key, value in (("member_count", True), ("member_count", 2.0), ("size_bytes", "9"), ("size_bytes", False)):
            bad = load("verified-valid.json")
            bad[key] = value
            self.assertNotEqual(run_check(bad).returncode, 0, (key, value))

    def test_not_an_object(self) -> None:
        self.assertNotEqual(run_check([]).returncode, 0)

    def test_exact_bytes_label_is_refused_with_a_clear_message(self) -> None:
        result = run_check(load("invalid-wrong-digest-domain.json"))
        self.assertIn("sha256-tree-manifest-v1", result.stderr + result.stdout)

    def test_schema_and_checker_agree_on_every_fixture(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema not installed")
        validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
        for path in sorted(FIXTURES.glob("*.json")):
            doc = json.loads(path.read_text())
            by_schema = validator.is_valid(doc)
            by_checker = run_check(doc).returncode == 0
            self.assertEqual(by_schema, by_checker, path.name)
            self.assertEqual(by_checker, path.name in VALID, path.name)

    def test_schema_is_marked_candidate_and_never_exact_bytes(self) -> None:
        schema = json.loads(SCHEMA.read_text())
        self.assertIn("CANDIDATE", schema["title"])
        self.assertEqual(schema["properties"]["digest_domain"], {"const": "sha256-tree-manifest-v1"})


if __name__ == "__main__":
    unittest.main()
