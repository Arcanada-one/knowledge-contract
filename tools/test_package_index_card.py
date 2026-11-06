"""Finite checks for PackageIndexCard/v1 validator."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_package_index_card.py"


def run_checker(doc: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(doc, fh)
        path = fh.name
    return subprocess.run(
        ["python3", str(CHECKER), path],
        capture_output=True,
        text=True,
        check=False,
    )


class PackageIndexCardTests(unittest.TestCase):
    def test_valid_card_passes(self) -> None:
        card = {
            "schema": "PackageIndexCard/v1",
            "source_id": "d_" + "a" * 64,
            "package_id": "d_" + "a" * 64 + "/book-package-2@r1",
            "package_slug": "pilot-s4-index-book",
            "exporter_path_slug": "pkg-" + "a" * 12 + "-" + "b" * 8,
            "span": {"kind": "full_document"},
            "licence": "public_domain;own_layers=CC-BY-4.0",
            "publication_state": "public_domain",
            "layer": "readable",
            "source_path": "articles/book-packages/pkg-" + "a" * 12 + "-" + "b" * 8 + "/readable.md",
            "content_sha256": "c" * 64,
            "damage_places": 0,
            "damage_status": "clean",
            "knowledge_ready": False,
            "kc2_admission": "not_measured",
        }
        result = run_checker(card)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_damaged_as_clean_refused(self) -> None:
        card = {
            "schema": "PackageIndexCard/v1",
            "source_id": "d_" + "a" * 64,
            "package_id": "d_" + "a" * 64 + "/book-package-2@r1",
            "package_slug": "pilot-s4-index-book",
            "exporter_path_slug": "pkg-" + "a" * 12 + "-" + "b" * 8,
            "span": {"kind": "full_document"},
            "licence": "public_domain",
            "publication_state": "public_domain",
            "layer": "readable",
            "source_path": "articles/book-packages/pkg-" + "a" * 12 + "-" + "b" * 8 + "/readable.md",
            "content_sha256": "c" * 64,
            "damage_places": 5,
            "damage_status": "clean",
            "knowledge_ready": False,
            "kc2_admission": "not_measured",
        }
        result = run_checker(card)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("damaged_presented_as_clean", result.stderr)


if __name__ == "__main__":
    unittest.main()
