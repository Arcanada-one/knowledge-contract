#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Source-bound reader references and adversarial cross-locale controls.

No claim of scientific admission, linguistic review, site serving or KC2 use.
"""
import json
import hashlib
import re
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIN = "6a6f202f7f70be2ad3aea3369e45409761708596"
OLD = f"https://github.com/Arcanada-one/knowledge-contract/blob/{PIN}"
READERS = {
    "READING.md": ("DOCUMENTS.md", f"{OLD}/DOCUMENTS.md", "contains {n} entries"),
    "guides/READING.ru.md": ("../DOCUMENTS.md", f"{OLD}/DOCUMENTS.md", "содержит {n} записи"),
    "guides/READING.zh-Hans.md": ("../DOCUMENTS.md", f"{OLD}/DOCUMENTS.md", "包含{n}项"),
    "README.md": ("publication-catalog.json", f"{OLD}/publication-catalog.json", "contains {n} reading entries"),
}

def check_reader(source, live_path, historic_url, count, current_phrase):
    lines = source.splitlines()
    old = [l for l in lines if "31" in l and f"]({historic_url})" in l]
    now = [l for l in lines if current_phrase.format(n=count) in l and f"]({live_path})" in l]
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
        for path, (live, old, phrase) in READERS.items():
            with self.subTest(path=path):
                self.assertEqual(check_reader(self.reader_text[path], live, old, self.n, phrase), [])

    def test_mutable_historical_link_mutant(self):
        for path, (live, old, phrase) in READERS.items():
            with self.subTest(path=path):
                src = self.reader_text[path]
                changed = src.replace(f"]({old})", f"]({live})", 1)
                self.assertNotEqual(changed, src)
                self.assertIn("historic_31_points_to_mutable_source",
                    check_reader(changed, live, old, self.n, phrase))

    def test_stale_current_count_mutant(self):
        for path, (live, old, phrase) in READERS.items():
            with self.subTest(path=path):
                lines = self.reader_text[path].splitlines()
                positions = [i for i, line in enumerate(lines)
                    if phrase.format(n=self.n) in line and f"]({live})" in line]
                self.assertEqual(len(positions), 1)
                i = positions[0]
                lines[i] = lines[i].replace(phrase.format(n=self.n), phrase.format(n=31), 1)
                self.assertIn("current_count_must_resolve_live_source",
                    check_reader("\n".join(lines), live, old, self.n, phrase))


# An immutable mechanical receipt is not a validation of a successor index.
REPORT_SOURCE_COMMIT = "d5e684e201f6d41498c4fbd8c2a3497eed2bb30e"
REPORT_BLOB = "c02b44d69a0cd7b704b10323389a56c563b1b62d"

REPORT_NAME = "validation-report.json"
STUDIES_DIR = ROOT / "engineering/studies"
# Inline Markdown link: [text](destination). Destination has no space or ')'.
LINK = re.compile(r"\[[^\]]*\]\(([^()\s]*)\)")

def report_pointer_problems(study_reader, report_bytes, index, studies_dir=STUDIES_DIR):
    errors = []
    passages = [p for p in study_reader.split("\n\n")
                if "Historical validation scope." in p]
    if len(passages) != 1:
        return ["missing_or_duplicated_scope_pointer"]
    passage = passages[0]
    required = (
        "preserved mechanical", "validation-report.json", REPORT_BLOB,
        REPORT_SOURCE_COMMIT, "reports **24 claims**",
        "**not regenerated**", "**26-claim** candidate index",
        "describes the pinned source snapshot",
        "**present at source", "The precise source revision and execution procedure",
    )
    if any(item not in passage for item in required):
        errors.append("unbound_or_misrepresented_historical_report")
    # The report must be a real link, not just the filename as text: a parsed
    # destination exactly equal to REPORT_NAME, resolving to a file beside the README.
    if REPORT_NAME not in LINK.findall(passage):
        errors.append("report_link_destination_not_exact")
    elif not (Path(studies_dir) / REPORT_NAME).is_file():
        errors.append("report_link_target_missing")
    actual_blob = hashlib.sha1(b"blob " + str(len(report_bytes)).encode("ascii") +
                               b"\0" + report_bytes).hexdigest()
    if actual_blob != REPORT_BLOB:
        errors.append("report_blob_changed")
    try:
        report = json.loads(report_bytes)
        if type(report.get("claim_count")) is not int or report["claim_count"] != 24:
            errors.append("report_claim_count_changed")
        if type(index.get("claim_count")) is not int or index["claim_count"] != 26:
            errors.append("successor_claim_count_changed")
    except (ValueError, TypeError, AttributeError):
        errors.append("invalid_report_or_index")
    return errors

class HistoricalReportPointerControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study = (ROOT / "engineering/studies/README.md").read_text(encoding="utf-8")
        cls.report = (ROOT / "engineering/studies/validation-report.json").read_bytes()
        cls.index = json.loads((ROOT / "engineering/studies/evidence-index.json")
                               .read_text(encoding="utf-8"))

    def test_preserved_24_claim_report_is_not_26_claim_candidate(self):
        self.assertEqual(report_pointer_problems(self.study, self.report, self.index), [])

    def test_pointer_mutants_are_detected(self):
        changes = (
            ("reports **24 claims**", "reports **26 claims**"),
            (REPORT_SOURCE_COMMIT, "0000000000000000000000000000000000000000"),
            ("**not regenerated**", "**regenerated**"),
            ("**present at source", "**produced at source"),
            (REPORT_BLOB, "1111111111111111111111111111111111111111"),
        )
        for original, mutant in changes:
            with self.subTest(mutant=original):
                changed = self.study.replace(original, mutant, 1)
                self.assertNotEqual(changed, self.study)
                self.assertIn("unbound_or_misrepresented_historical_report",
                              report_pointer_problems(changed, self.report, self.index))
        changed_index = dict(self.index, claim_count=24)
        self.assertIn("successor_claim_count_changed",
                      report_pointer_problems(self.study, self.report, changed_index))
    def link_mutant(self, replacement):
        original = "](validation-report.json)"
        self.assertEqual(self.study.count(original), 1)
        return self.study.replace(original, replacement, 1)

    def test_link_destination_nonexistent_target_is_detected(self):
        """Only the destination changes; the link text stays identical."""
        changed = self.link_mutant("](nonexistent-report.json)")
        self.assertIn("report_link_destination_not_exact",
                      report_pointer_problems(changed, self.report, self.index))

    def test_link_destination_non_exact_form_is_refused(self):
        """Rule: the destination must equal `validation-report.json` byte for
        byte. Prefixes (`./`), fragments (`#x`), queries and other spellings of
        an existing file are refused, even though they would resolve."""
        for dest in ("./validation-report.json#x", "./validation-report.json",
                     "validation-report.json#x", "validation-report.json?x"):
            with self.subTest(dest=dest):
                changed = self.link_mutant(f"]({dest})")
                self.assertIn("report_link_destination_not_exact",
                              report_pointer_problems(changed, self.report, self.index))

    def test_bare_filename_without_link_is_refused(self):
        """Only the link is removed; the bare filename text stays in the paragraph."""
        label = "[preserved mechanical `validation-report.json`]"
        changed = self.link_mutant("").replace(label, label[1:-1], 1)
        self.assertNotIn("](validation-report.json)", changed)
        self.assertIn("`validation-report.json`", changed)
        self.assertIn("report_link_destination_not_exact",
                      report_pointer_problems(changed, self.report, self.index))

    def test_exact_link_to_missing_file_is_refused(self):
        """The README is unchanged; the studies directory lacks the report file."""
        with tempfile.TemporaryDirectory() as empty:
            self.assertIn("report_link_target_missing",
                          report_pointer_problems(self.study, self.report, self.index, empty))

if __name__ == "__main__":
    unittest.main()
