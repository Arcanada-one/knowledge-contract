import unittest

from tools.check_separation import violates


class SeparationTests(unittest.TestCase):
    def test_mixed_changes_fail(self):
        self.assertTrue(violates(["corpus/publication-decisions/b1.jsonl", "articles/a.md"]))
        self.assertTrue(violates(["corpus/README.md", "papers/p.md"]))
        self.assertTrue(violates(["corpus/publication-decisions/receipts/b1.json", "schemas/s.md"]))

    def test_decision_files_and_the_table_in_one_change_fail(self):
        self.assertTrue(violates(["corpus/publication-decisions/b1.jsonl", "corpus/README.md"]))
        self.assertTrue(violates(["corpus/publication-decisions/receipts/b1.json", "corpus/README.md", "tools/x.py"]))

    def test_non_ascii_paths_are_seen_by_the_command(self):
        import os, subprocess, sys, tempfile
        from pathlib import Path
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@example.invalid", "GIT_CONFIG_GLOBAL": os.devnull}
        script = Path(__file__).resolve().parent / "check_separation.py"
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            def git(*args):
                return subprocess.run(("git", "-c", "commit.gpgsign=false", *args), cwd=repo, env=env, check=True, stdout=subprocess.PIPE).stdout.decode().strip()
            git("init", "-q", "-b", "main")
            (repo / "a.txt").write_text("a")
            git("add", "-A"); git("commit", "-q", "-m", "base")
            base = git("rev-parse", "HEAD")
            (repo / "articles").mkdir(); (repo / "articles" / "caf\u00e9.md").write_text("x")
            (repo / "corpus").mkdir(); (repo / "corpus" / "README.md").write_text("table")
            git("add", "-A"); git("commit", "-q", "-m", "mixed")
            result = subprocess.run([sys.executable, str(script), base, git("rev-parse", "HEAD")], cwd=repo, env=env,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 1, result.stderr)

    def _run(self, setup, change):
        import os, subprocess, sys, tempfile
        from pathlib import Path
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@example.invalid", "GIT_CONFIG_GLOBAL": os.devnull}
        script = Path(__file__).resolve().parent / "check_separation.py"
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)

            def git(*args):
                return subprocess.run(("git", "-c", "commit.gpgsign=false", *args), cwd=repo, env=env, check=True, stdout=subprocess.PIPE).stdout.decode().strip()

            git("init", "-q", "-b", "main")
            setup(repo)
            git("add", "-A"); git("commit", "-q", "--allow-empty", "-m", "base")
            base = git("rev-parse", "HEAD")
            change(repo, git)
            git("add", "-A"); git("commit", "-q", "-m", "change")
            return subprocess.run([sys.executable, str(script), base, git("rev-parse", "HEAD")], cwd=repo, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode

    def test_a_rename_out_of_a_content_directory_is_seen_together_with_a_decision_file(self):
        # with rename detection git lists only the new name (docs/...), so the move out of articles/ would pass unseen
        def setup(repo):
            (repo / "articles").mkdir()
            (repo / "articles" / "project-overview.md").write_text("some content that is long enough to be detected as a rename\n" * 5)

        def change(repo, git):
            (repo / "docs").mkdir()
            git("mv", "articles/project-overview.md", "docs/project-overview.md")
            (repo / "corpus" / "publication-decisions").mkdir(parents=True)
            (repo / "corpus" / "publication-decisions" / "b1.jsonl").write_text("")

        self.assertEqual(self._run(setup, change), 1)

    def test_names_with_tab_newline_and_quote_stay_whole(self):
        for name in ("articles/with\ttab.md", "articles/with\nnewline.md", 'articles/with"quote.md', "articles/with space.md"):
            with self.subTest(name=name):
                def change(repo, git, name=name):
                    (repo / "articles").mkdir(exist_ok=True)
                    (repo / "articles" / name.split("/", 1)[1]).write_text("x")
                    (repo / "corpus" / "publication-decisions").mkdir(parents=True, exist_ok=True)
                    (repo / "corpus" / "publication-decisions" / "b1.jsonl").write_text("")

                self.assertEqual(self._run(lambda repo: (repo / "a.txt").write_text("a"), change), 1)

    def test_a_clean_decision_change_passes_through_the_command(self):
        def change(repo, git):
            (repo / "corpus" / "publication-decisions").mkdir(parents=True)
            (repo / "corpus" / "publication-decisions" / "b1.jsonl").write_text("")

        self.assertEqual(self._run(lambda repo: (repo / "a.txt").write_text("a"), change), 0)

    def test_single_area_changes_pass(self):
        self.assertFalse(violates(["corpus/publication-decisions/b1.jsonl", "corpus/publication-decisions/receipts/b1.json"]))
        self.assertFalse(violates(["corpus/README.md", "OPENNESS.md", "tools/export_corpus.py"]))
        self.assertFalse(violates(["articles/a.md", "papers/p.md"]))
        self.assertFalse(violates([]))


if __name__ == "__main__":
    unittest.main()
