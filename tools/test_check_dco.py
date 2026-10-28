import subprocess
import tempfile
import unittest
from pathlib import Path

from tools import check_dco

GIT = ["git", "-c", "user.name=T", "-c", "user.email=t@example.org", "-c", "commit.gpgsign=false"]


def run(repo: Path, *args: str) -> str:
    return subprocess.run([*GIT, "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


class CheckDcoTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp())
        run(self.repo, "init", "-q", "-b", "main")
        (self.repo / "a").write_text("1")
        run(self.repo, "add", "a")
        run(self.repo, "commit", "-q", "-m", "base")
        self.base = run(self.repo, "rev-parse", "HEAD")

    def commit(self, name: str, *flags: str) -> None:
        (self.repo / name).write_text(name)
        run(self.repo, "add", name)
        run(self.repo, "commit", "-q", *flags, "-m", f"add {name}")

    def test_unsigned_commit_is_rejected(self):
        self.commit("u")
        self.assertEqual(len(check_dco.unsigned(self.base, "HEAD", str(self.repo))), 1)

    def test_signed_commit_passes(self):
        self.commit("s", "-s")
        self.assertEqual(check_dco.unsigned(self.base, "HEAD", str(self.repo)), [])

    def test_one_unsigned_among_signed_is_rejected(self):
        self.commit("s", "-s")
        self.commit("u")
        self.assertEqual(len(check_dco.unsigned(self.base, "HEAD", str(self.repo))), 1)

    def test_fake_trailer_without_address_is_rejected(self):
        (self.repo / "f").write_text("f")
        run(self.repo, "add", "f")
        run(self.repo, "commit", "-q", "-m", "x\n\nSigned-off-by: nobody")
        self.assertEqual(len(check_dco.unsigned(self.base, "HEAD", str(self.repo))), 1)

    def test_empty_range_passes(self):
        self.assertEqual(check_dco.unsigned(self.base, "HEAD", str(self.repo)), [])


if __name__ == "__main__":
    unittest.main()
