"""Mutation pass: every `# check: NAME` guard in the exporter must be load-bearing.

Each guard is disabled in turn (its condition replaced by False) in a scratch copy of the
tree and the exporter tests are run against that copy; a guard whose removal leaves the tests
green is a gap. This is an author-side tool: run it locally before pushing a change to the
exporter (python3 -B -m unittest tools.test_export_check_mutations, about five minutes); it is
deliberately not part of the pull request CI. Set EXPORT_MUTATION_TABLE=1 to print the table.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
GUARD = re.compile(r"^(\s*)(if|elif) (.*):  # check: (\w+)$")


NOT_AN_ASSERTION = (b"ImportError", b"ModuleNotFoundError", b"FileNotFoundError", b"SyntaxError", b"NameError")


def scratch_run(source_text: str) -> subprocess.CompletedProcess:
    """Run the exporter tests in a scratch copy of the whole tree whose export_corpus.py is `source_text`."""
    with tempfile.TemporaryDirectory() as temp:
        scratch = Path(temp)
        shutil.copytree(ROOT / "tools", scratch / "tools", ignore=shutil.ignore_patterns("__pycache__", "test_export_check_mutations.py"))
        shutil.copytree(ROOT / "corpus", scratch / "corpus")
        shutil.copytree(ROOT / "papers", scratch / "papers")
        for edition_dir in ("engineering", "reference", "appendices"):  # DEC-AUP-0175: the 29-document scope reads these
            shutil.copytree(ROOT / edition_dir, scratch / edition_dir)
        shutil.copy(ROOT / "publication-catalog.json", scratch / "publication-catalog.json")
        for declared in ("REUSE.toml", "NOTICE", "LICENSE"):
            shutil.copy(ROOT / declared, scratch / declared)
        (scratch / "tools/export_corpus.py").write_text(source_text)
        return subprocess.run([sys.executable, "-B", "-m", "unittest", "-f", "tools.test_export_corpus"], cwd=scratch,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def is_assertion_kill(result: subprocess.CompletedProcess) -> bool:
    """A mutant is killed only by a failed assertion; a crash of the scratch copy (import, missing file, syntax) is not a kill."""
    return (result.returncode != 0 and b"FAIL: " in result.stderr
            and not any(marker in result.stderr for marker in NOT_AN_ASSERTION))


class GuardMutationTests(unittest.TestCase):
    def test_a_no_op_mutant_is_reported_as_survived(self) -> None:
        """Self-test of the harness: an unchanged exporter must run green and must not count as killed."""
        source = (ROOT / "tools/export_corpus.py").read_text()
        result = scratch_run(source)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace")[-400:])
        self.assertFalse(is_assertion_kill(result))
        broken = subprocess.CompletedProcess([], 1, b"", b"FAIL: test_x\nFileNotFoundError: publication-catalog.json\n")
        self.assertFalse(is_assertion_kill(broken), "a crashed scratch copy must not count as a kill")
        self.assertTrue(is_assertion_kill(subprocess.CompletedProcess([], 1, b"", b"FAIL: test_x\nAssertionError: boom\n")))

    def test_every_guard_is_killed_by_the_exporter_tests(self) -> None:
        source_text = (ROOT / "tools/export_corpus.py").read_text()
        source = source_text.splitlines()
        guards = [(i, m.group(4)) for i, line in enumerate(source) if (m := GUARD.match(line))]
        self.assertGreaterEqual(len(guards), 20)
        # Baseline control: the unmutated scratch copy must exit 0, otherwise every mutant would "die" of a broken copy.
        baseline = scratch_run(source_text)
        self.assertEqual(baseline.returncode, 0, "baseline (unmutated scratch copy) must exit 0: " + baseline.stderr.decode(errors="replace")[-400:])
        survivors, table = [], [("baseline_unmutated", "exit 0")]
        for index, name in guards:
            lines = list(source)
            match = GUARD.match(lines[index])
            lines[index] = f"{match.group(1)}{match.group(2)} False:  # check: {name}"
            result = scratch_run("\n".join(lines) + "\n")
            killed = is_assertion_kill(result)
            table.append((name, "killed (assertion failure)" if killed else f"SURVIVED or broken (exit {result.returncode})"))
            if not killed:
                survivors.append(name)
        print("\n" + "\n".join(f"{name:28} {state}" for name, state in table), flush=True)
        self.assertEqual(survivors, [], "guards whose removal no test notices")


class ScopeListMutationTests(unittest.TestCase):
    """DEC-AUP-0172: each edit of the explicit SCOPE_PATHS list that widens, narrows or turns it into a prefix must be noticed by a test."""

    P00 = '    "papers/P00_introduction.md",\n'
    MUTANTS = {
        "drop_P07": lambda s: s.replace('    "papers/P07_reasoning_and_evidence.md",\n', ""),
        "misspell_P13": lambda s: s.replace('economics.md",\n    # DEC-AUP-0175', 'economic.md",\n    # DEC-AUP-0175'),
        "add_russian_text": lambda s: s.replace(ScopeListMutationTests.P00, ScopeListMutationTests.P00 + '    "papers/ru/P00_introduction.md",\n'),
        "add_papers_readme": lambda s: s.replace(ScopeListMutationTests.P00, ScopeListMutationTests.P00 + '    "papers/README.md",\n'),
        "add_fifteenth_page": lambda s: s.replace(ScopeListMutationTests.P00, ScopeListMutationTests.P00 + '    "papers/P14_future_paper.md",\n'),
        "add_spec_page": lambda s: s.replace(ScopeListMutationTests.P00, ScopeListMutationTests.P00 + '    "spec/STATUS_MODEL.md",\n'),
        "drop_edition_paper": lambda s: s.replace('    "papers/semantic-objects-and-context/PAPER.md",\n', ""),
        "add_unlisted_engineering_page": lambda s: s.replace(ScopeListMutationTests.P00, ScopeListMutationTests.P00 + '    "engineering/specifications/book-package/README.md",\n'),
        "add_review_page": lambda s: s.replace(ScopeListMutationTests.P00, ScopeListMutationTests.P00 + '    "reviews/publication-integrity/REVIEW.md",\n'),
        "prefix_rule_engineering": lambda s: s.replace("if path not in SCOPE_PATHS:  # check: scope_paths",
                                                      "if not (path in SCOPE_PATHS or path.startswith('engineering/')):  # check: scope_paths"),
        "prefix_rule": lambda s: s.replace("if path not in SCOPE_PATHS:  # check: scope_paths",
                                           "if not (path in SCOPE_PATHS or path.startswith('papers/')):  # check: scope_paths"),
    }

    @staticmethod
    def _scratch_run(source_text: str) -> subprocess.CompletedProcess:
        return scratch_run(source_text)

    def test_every_scope_list_mutant_is_killed(self) -> None:
        source = (ROOT / "tools/export_corpus.py").read_text()
        # Baseline control: the unmutated scratch copy must pass, otherwise every mutant would "die" of a broken copy.
        baseline = self._scratch_run(source)
        self.assertEqual(baseline.returncode, 0, "baseline (unmutated scratch copy) must exit 0: " + baseline.stderr.decode(errors="replace")[-400:])
        table, survivors = [("baseline_unmutated", "exit 0")], []
        for name, mutate in self.MUTANTS.items():
            mutated = mutate(source)
            self.assertNotEqual(mutated, source, f"mutant {name} no longer applies; update the mutant")
            result = self._scratch_run(mutated)
            # Killed only if the baseline passed and the mutant fails with an assertion, not an import or file error.
            assertion_failure = is_assertion_kill(result)
            table.append((name, "killed (assertion failure)" if assertion_failure else f"SURVIVED or broken (exit {result.returncode})"))
            if not assertion_failure:
                survivors.append(name)
        print("\n" + "\n".join(f"{n:22} {state}" for n, state in table))
        self.assertEqual(survivors, [], "scope-list mutants no test notices")


if __name__ == "__main__":
    unittest.main()
