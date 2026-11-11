# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Synthetic inventory and disposable-Git tests, not translation assessment."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.report_translation_coverage import catalogue_paths, coverage


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.paths = {"papers/a/PAPER.md": "paper", "papers/b/PAPER.md": "paper"}
        self.a = "translations/ru/papers/a/PAPER.md"
        self.b = "translations/ru/papers/b/PAPER.md"

    def test_equal_overlap_not_double_counted(self):
        got = coverage(self.paths, {self.a: "x"}, {self.a: "x", self.b: "y"}, "ru")
        self.assertEqual(got["counts"]["union_present"], 2)
        self.assertEqual(got["counts"]["draft_only"], 1)
        self.assertEqual(got["counts"]["identical_overlap"], 1)

    def test_different_overlap_retained_for_review(self):
        got = coverage(self.paths, {self.a: "old"}, {self.a: "new"}, "ru")
        self.assertEqual(got["counts"]["different_overlap"], 1)
        self.assertEqual(got["counts"]["union_present"], 1)

    def test_base_only_not_lost(self):
        got = coverage(self.paths, {self.a: "x"}, {self.b: "y"}, "ru")
        self.assertEqual(got["counts"]["base_only"], 1)
        self.assertEqual(got["counts"]["missing_from_both"], 0)

    def test_new_catalogue_entry_increases_missing(self):
        extended = dict(self.paths, **{"papers/c/PAPER.md": "paper"})
        got = coverage(extended, {self.a: "x"}, {self.a: "x", self.b: "y"}, "ru")
        self.assertEqual(got["source_documents"], 3)
        self.assertEqual(got["counts"]["missing_from_both"], 1)

    def test_ancillary_and_other_locale_excluded(self):
        got = coverage(self.paths, {}, {self.a: "x", "translations/STATUS.md": "s",
                       "translations/ru/README.md": "r", self.b.replace("/ru/", "/zh-Hans/"): "z"}, "ru")
        self.assertEqual(got["counts"]["union_present"], 1)
        self.assertEqual(got["uncounted_translation_paths"], ["translations/ru/README.md"])

    def test_duplicate_catalogue_path_rejected(self):
        doc = {"path": "papers/a/PAPER.md", "type": "paper"}
        with self.assertRaises(ValueError):
            catalogue_paths({"documents": [doc, doc]})

    def test_unsafe_path_rejected(self):
        for path in ("../PAPER.md", "/PAPER.md", "a/../PAPER.md", "a//PAPER.md", "a\\PAPER.md"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                catalogue_paths({"documents": [{"path": path, "type": "paper"}]})

    def test_invalid_kind_or_shape_rejected(self):
        for docs in ([], [False], [{"path": "a.md", "type": False}]):
            with self.subTest(docs=docs), self.assertRaises(ValueError):
                catalogue_paths({"documents": docs})

    def test_unknown_locale_rejected(self):
        with self.assertRaises(ValueError):
            coverage(self.paths, {}, {}, "en")

    def test_31_25_4_inventory(self):
        paths = {f"papers/p{i}/PAPER.md": "paper" for i in range(31)}
        files = [f"translations/ru/{p}" for p in paths]
        base = {p: str(i) for i, p in enumerate(files[:4])}
        draft = {p: str(i) for i, p in enumerate(files[:25])}
        got = coverage(paths, base, draft, "ru")["counts"]
        self.assertEqual((got["union_present"], got["draft_only"], got["missing_from_both"]), (25, 21, 6))

    def test_cli_disposable_git_and_no_worktree_mutation(self):
        script = Path(__file__).with_name("report_translation_coverage.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def run(*args):
                return subprocess.check_output(["git", "-C", directory, *args]).decode().strip()
            run("init", "-q")
            run("config", "user.name", "Synthetic Test")
            run("config", "user.email", "test@example.invalid")
            (root / "publication-catalog.json").write_text(json.dumps({"documents": [
                {"path": p, "type": k} for p, k in self.paths.items()]}))
            (root / self.a).parent.mkdir(parents=True)
            (root / self.a).write_text("first synthetic body\n")
            run("add", "."); run("commit", "-qm", "base")
            base = run("rev-parse", "HEAD")
            (root / self.b).parent.mkdir(parents=True)
            (root / self.b).write_text("second synthetic body\n")
            run("add", "."); run("commit", "-qm", "draft")
            draft = run("rev-parse", "HEAD")
            command = [sys.executable, "-B", str(script), "--repo", directory,
                       "--source-ref", base, "--base-ref", base, "--draft-ref", draft]
            first = subprocess.run(command, text=True, capture_output=True)
            second = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            report = json.loads(first.stdout)
            self.assertEqual(report["locales"]["ru"]["counts"]["union_present"], 2)
            self.assertEqual(report["locales"]["zh-Hans"]["counts"]["missing_from_both"], 2)
            self.assertIn("translation fidelity", report["not_established"])
            self.assertEqual(run("status", "--porcelain"), "")
            self.assertEqual(run("rev-parse", "HEAD"), draft)

    def test_cli_unknown_ref_is_error_not_empty_inventory(self):
        script = Path(__file__).with_name("report_translation_coverage.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            for ref in ("main", "0" * 40, "--help"):
                run = subprocess.run([sys.executable, "-B", str(script), "--repo", directory,
                    "--source-ref", ref, "--base-ref", "0" * 40, "--draft-ref", "1" * 40],
                    text=True, capture_output=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(run.stdout, "")


if __name__ == "__main__":
    unittest.main()
