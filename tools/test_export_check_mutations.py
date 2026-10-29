"""Mutation pass: every `# check: NAME` guard in the exporter must be load-bearing.

Each guard is disabled in turn (its condition replaced by False) in a scratch copy of the
tree and the exporter tests are run against that copy; a guard whose removal leaves the tests
green is a gap. Set EXPORT_MUTATION_TABLE=1 to print the table.
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


class GuardMutationTests(unittest.TestCase):
    def test_every_guard_is_killed_by_the_exporter_tests(self) -> None:
        source = (ROOT / "tools/export_corpus.py").read_text().splitlines()
        guards = [(i, m.group(4)) for i, line in enumerate(source) if (m := GUARD.match(line))]
        self.assertGreaterEqual(len(guards), 20)
        survivors, table = [], []
        for index, name in guards:
            with tempfile.TemporaryDirectory() as temp:
                scratch = Path(temp)
                shutil.copytree(ROOT / "tools", scratch / "tools", ignore=shutil.ignore_patterns("__pycache__", "test_export_check_mutations.py"))
                shutil.copytree(ROOT / "corpus", scratch / "corpus")
                lines = list(source)
                match = GUARD.match(lines[index])
                lines[index] = f"{match.group(1)}{match.group(2)} False:  # check: {name}"
                (scratch / "tools/export_corpus.py").write_text("\n".join(lines) + "\n")
                result = subprocess.run([sys.executable, "-B", "-m", "unittest", "-f", "tools.test_export_corpus"], cwd=scratch,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            killed = result.returncode != 0
            table.append((name, "killed" if killed else "SURVIVED"))
            if not killed:
                survivors.append(name)
        if os.environ.get("EXPORT_MUTATION_TABLE"):
            print("\n".join(f"{name:28} {state}" for name, state in table))
        self.assertEqual(survivors, [], "guards whose removal no test notices")


if __name__ == "__main__":
    unittest.main()
