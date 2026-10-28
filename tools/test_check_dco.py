import subprocess
import tempfile
import unittest
from pathlib import Path

from tools import check_dco


def run(repo: Path, *args: str, env_extra: dict | None = None) -> str:
    import os
    env = dict(os.environ)
    env.update({"GIT_AUTHOR_NAME": "Alice", "GIT_AUTHOR_EMAIL": "alice@example.org",
                "GIT_COMMITTER_NAME": "Alice", "GIT_COMMITTER_EMAIL": "alice@example.org"})
    env.update(env_extra or {})
    return subprocess.run(["git", "-c", "commit.gpgsign=false", "-C", str(repo), *args],
                          check=True, capture_output=True, text=True, env=env).stdout.strip()


class CheckDcoTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp())
        run(self.repo, "init", "-q", "-b", "main")
        (self.repo / "a").write_text("1")
        run(self.repo, "add", "a")
        run(self.repo, "commit", "-q", "-m", "base")
        self.base = run(self.repo, "rev-parse", "HEAD")

    def commit(self, name: str, message: str | None = None, *flags: str, env_extra: dict | None = None) -> None:
        (self.repo / name).write_text(name)
        run(self.repo, "add", name)
        run(self.repo, "commit", "-q", *flags, "-m", message or f"add {name}", env_extra=env_extra)

    def bad(self) -> list[str]:
        return check_dco.unsigned(self.base, "HEAD", str(self.repo))

    def test_unsigned_commit_is_rejected(self):
        self.commit("u")
        self.assertEqual(len(self.bad()), 1)

    def test_signed_commit_passes(self):
        self.commit("s", None, "-s")
        self.assertEqual(self.bad(), [])

    def test_one_unsigned_among_signed_is_rejected(self):
        self.commit("s", None, "-s")
        self.commit("u")
        self.assertEqual(len(self.bad()), 1)

    def test_fake_trailer_without_address_is_rejected(self):
        self.commit("f", "x\n\nSigned-off-by: nobody")
        self.assertEqual(len(self.bad()), 1)

    def test_signoff_in_body_but_not_in_trailer_block_is_rejected(self):
        self.commit("b", "subject\n\nSigned-off-by: Alice <alice@example.org>\n\nlater paragraph")
        self.assertEqual(len(self.bad()), 1)

    def test_signoff_as_subject_only_is_rejected(self):
        self.commit("s1", "Signed-off-by: Alice <alice@example.org>", "--cleanup=verbatim")
        self.assertEqual(len(self.bad()), 1)

    def test_signoff_among_other_trailers_passes(self):
        self.commit("t", "subject\n\nbody\n\nCo-Authored-By: Bob <bob@example.org>\nSigned-off-by: Alice <alice@example.org>")
        self.assertEqual(self.bad(), [])

    def test_signoff_for_someone_else_is_rejected(self):
        self.commit("o", "subject\n\nSigned-off-by: Mallory <mallory@example.org>")
        self.assertEqual(len(self.bad()), 1)

    def test_signoff_matching_committer_only_passes(self):
        self.commit("c", "subject\n\nSigned-off-by: Carol <carol@example.org>",
                    env_extra={"GIT_COMMITTER_NAME": "Carol", "GIT_COMMITTER_EMAIL": "carol@example.org"})
        self.assertEqual(self.bad(), [])

    def test_signoff_name_match_is_case_insensitive(self):
        self.commit("i", "subject\n\nSigned-off-by: ALICE <ALICE@example.org>")
        self.assertEqual(self.bad(), [])

    def test_allow_listed_bot_without_signoff_passes(self):
        self.commit("d", "bump", env_extra={
            "GIT_AUTHOR_NAME": "dependabot[bot]",
            "GIT_AUTHOR_EMAIL": "49699333+dependabot[bot]@users.noreply.github.com"})
        self.assertEqual(self.bad(), [])

    def test_bot_lookalike_is_rejected(self):
        self.commit("d2", "bump", env_extra={
            "GIT_AUTHOR_NAME": "dependabot[bot]", "GIT_AUTHOR_EMAIL": "evil@example.org"})
        self.assertEqual(len(self.bad()), 1)

    def test_merge_commit_itself_is_not_checked_but_its_commits_are(self):
        run(self.repo, "checkout", "-q", "-b", "side")
        self.commit("side-signed", None, "-s")
        run(self.repo, "checkout", "-q", "main")
        self.commit("main-signed", None, "-s")
        run(self.repo, "merge", "-q", "--no-ff", "-m", "Merge side", "side")
        self.assertEqual(self.bad(), [])

    def test_unsigned_commit_brought_in_by_merge_is_rejected(self):
        run(self.repo, "checkout", "-q", "-b", "side")
        self.commit("side-unsigned")
        run(self.repo, "checkout", "-q", "main")
        self.commit("main-signed", None, "-s")
        run(self.repo, "merge", "-q", "--no-ff", "-m", "Merge side", "side")
        self.assertEqual(len(self.bad()), 1)

    def test_empty_range_passes(self):
        self.assertEqual(self.bad(), [])


if __name__ == "__main__":
    unittest.main()
