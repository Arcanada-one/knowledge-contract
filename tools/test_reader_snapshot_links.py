#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Source-bound reader references and adversarial cross-locale controls.

No claim of scientific admission, linguistic review, site serving or KC2 use.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIN = "6a6f202f7f70be2ad3aea3369e45409761708596"
OLD = f"https://github.com/Arcanada-one/knowledge-contract/blob/{PIN}"
READERS = {
    "READING.md": ("DOCUMENTS.md", f"{OLD}/DOCUMENTS.md"),
    "guides/READING.ru.md": ("../DOCUMENTS.md", f"{OLD}/DOCUMENTS.md"),
    "guides/READING.zh-Hans.md": ("../DOCUMENTS.md", f"{OLD}/DOCUMENTS.md"),
    "README.md": ("publication-catalog.json", f"{OLD}/publication-catalog.json"),
}

def check_reader(source, live_path, historic_url, count):
    lines = source.splitlines()
    old = [l for l in lines if "31" in l and f"]({historic_url})" in l]
    now = [l for l in lines if str(count) in l and f"]({live_path})" in l]
    result = []
    if len(old) != 1:
        result.append("historic_31_must_resolve_immutable_source")
    if len(now) != 1:
        result.append("current_count_must_resolve_live_source")
    if any("31" in l and f"]({live_path})" in l for l in lines):
        result.append("historic_31_points_to_mutable_source")
    return result

class SnapshotReaderControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = len(json.loads((ROOT / "publication-catalog.json").read_text(encoding="utf-8"))["documents"])
        cls.rows = sum(l.startswith("| [") for l in
            (ROOT / "DOCUMENTS.md").read_text(encoding="utf-8").splitlines())
        cls.reader_text = {p: (ROOT / p).read_text(encoding="utf-8") for p in READERS}

    def test_live_catalogue_and_four_readers(self):
        self.assertEqual(self.n, self.rows)
        self.assertNotEqual(self.n, 31)
        for path, (live, old) in READERS.items():
            with self.subTest(path=path):
                self.assertEqual(check_reader(self.reader_text[path], live, old, self.n), [])

    def test_mutable_historical_link_mutant(self):
        for path, (live, old) in READERS.items():
            with self.subTest(path=path):
                src = self.reader_text[path]
                changed = src.replace(f"]({old})", f"]({live})", 1)
                self.assertNotEqual(changed, src)
                self.assertIn("historic_31_points_to_mutable_source",
                    check_reader(changed, live, old, self.n))

    def test_stale_current_count_mutant(self):
        for path, (live, old) in READERS.items():
            with self.subTest(path=path):
                lines = self.reader_text[path].splitlines()
                positions = [i for i, line in enumerate(lines)
                    if str(self.n) in line and f"]({live})" in line]
                self.assertEqual(len(positions), 1)
                i = positions[0]
                lines[i] = lines[i].replace(str(self.n), "31", 1)
                self.assertIn("current_count_must_resolve_live_source",
                    check_reader("\n".join(lines), live, old, self.n))

if __name__ == "__main__":
    unittest.main()
