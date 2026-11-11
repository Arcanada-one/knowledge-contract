#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Finite regressions for location-registry checker (not a conformance certificate)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
import check_location_registry as clr  # noqa: E402

DIGEST = "a" * 64
SOURCE = f"d_{DIGEST}"
PACKAGE = f"{SOURCE}/book-package-2"


def sample_row(**overrides):
    row = {
        "schema": "LocationRegistryRow/v1",
        "object_kind": "original",
        "object_id": SOURCE,
        "holder_host": "arcana-dbs",
        "volume": "/srv",
        "path": f"/srv/source-library/originals/{DIGEST[:2]}/{DIGEST}",
        "role": "primary",
        "size_bytes": 12,
        "verified_at": None,
        "verified_sha256": None,
    }
    row.update(overrides)
    return row


def sample_registry(entries=None):
    return {
        "schema": "LocationRegistry/v1",
        "contour": "arcana-dbs:/srv/source-library",
        "entries": entries if entries is not None else [sample_row()],
    }


class LocationRegistryTests(unittest.TestCase):
    def test_valid_registry_and_receipt(self):
        self.assertEqual(clr.validate_document(sample_registry()), [])
        receipt = {
            "schema": "LocationVerifyReceipt/v1",
            "run_id": "run-1",
            "tool": {"name": "verify_locations.py", "version": "0.1.0"},
            "started_at": "2026-11-06T17:00:00Z",
            "finished_at": "2026-11-06T17:00:01Z",
            "registry_sha256": DIGEST,
            "counts": {"ok": 1, "missing": 0, "corrupt": 0, "not_measured": 0},
            "non_ok": [],
            "kc2_admission": "not_measured",
        }
        self.assertEqual(clr.validate_document(receipt), [])

    def test_path_is_not_an_identity(self):
        bad = sample_row(object_id="/srv/source-library/foo.pdf")
        problems = clr.validate_document(sample_registry([bad]))
        self.assertTrue(any("object_id" in p for p in problems))

    def test_verified_sha_must_match_source_id(self):
        bad = sample_row(verified_sha256="b" * 64, verified_at="2026-11-06T17:00:00Z")
        problems = clr.validate_document(sample_registry([bad]))
        self.assertTrue(any("verified_sha256" in p for p in problems))

    def test_duplicate_primary_refused(self):
        problems = clr.validate_document(
            sample_registry([sample_row(), sample_row(path="/other")])
        )
        self.assertTrue(any("duplicate primary" in p for p in problems))

    def test_package_id_shape(self):
        row = sample_row(object_kind="package", object_id=PACKAGE, path="/srv/packages/x")
        self.assertEqual(clr.validate_document(sample_registry([row])), [])
        bad = sample_row(object_kind="package", object_id=SOURCE)
        problems = clr.validate_document(sample_registry([bad]))
        self.assertTrue(any("package object_id" in p for p in problems))

    def test_kc2_admission_locked(self):
        receipt = {
            "schema": "LocationVerifyReceipt/v1",
            "run_id": "run-1",
            "tool": {"name": "verify_locations.py", "version": "0.1.0"},
            "started_at": "2026-11-06T17:00:00Z",
            "finished_at": "2026-11-06T17:00:01Z",
            "registry_sha256": DIGEST,
            "counts": {"ok": 0, "missing": 0, "corrupt": 0, "not_measured": 0},
            "non_ok": [],
            "kc2_admission": "admitted",
        }
        problems = clr.validate_document(receipt)
        self.assertTrue(any("kc2_admission" in p for p in problems))

    def test_cli_pass_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.json"
            bad = root / "bad.json"
            good.write_text(json.dumps(sample_registry()) + "\n", encoding="utf-8")
            bad.write_text(
                json.dumps(sample_registry([sample_row(object_id="not-an-id")])) + "\n",
                encoding="utf-8",
            )
            import subprocess
            import sys

            ok = subprocess.run(
                [sys.executable, str(Path(clr.__file__)), str(good)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            fail = subprocess.run(
                [sys.executable, str(Path(clr.__file__)), str(bad)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(fail.returncode, 1, fail.stdout + fail.stderr)


if __name__ == "__main__":
    unittest.main()
