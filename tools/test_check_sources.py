import tempfile
import unittest
from pathlib import Path

from tools import check_sources

HEADER = "| Source | Author | URI | License | What was used | Where |\n| --- | --- | --- | --- | --- | --- |\n"


def make(files: dict[str, str], register: str = "") -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "SOURCES.md").write_text("# Sources\n\n" + HEADER + register, encoding="utf-8")
    for name, body in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return root


class CheckSourcesTests(unittest.TestCase):
    def test_empty_scaffold_passes(self):
        self.assertEqual(check_sources.check(make({"papers/.gitkeep": "", "spec/.gitkeep": ""})), [])

    def test_uncovered_paper_fails(self):
        problems = check_sources.check(make({"papers/p.md": "# P\n"}))
        self.assertEqual(len(problems), 1)
        self.assertIn("papers/p.md", problems[0])

    def test_uncovered_spec_json_fails(self):
        self.assertEqual(len(check_sources.check(make({"spec/s.json": "{}"}))), 1)

    def test_sources_none_passes(self):
        self.assertEqual(check_sources.check(make({"papers/p.md": "---\nsources: none\n---\n# P\n"})), [])

    def test_inline_and_list_sources_pass(self):
        files = {
            "papers/a.md": "---\nsources: [Doe 2020]\n---\n# A\n",
            "spec/b.md": "---\nsources:\n  - Doe 2020\n---\n# B\n",
        }
        self.assertEqual(check_sources.check(make(files)), [])

    def test_empty_sources_key_fails(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": "---\nsources:\ntitle: x\n---\n# P\n"}))), 1)

    def test_register_row_covers_any_type(self):
        row = "| Doe | Jane Doe | https://example.org/d | CC-BY-4.0 | definition | `spec/s.json` |\n"
        self.assertEqual(check_sources.check(make({"spec/s.json": "{}"}, row)), [])

    def test_register_row_for_other_path_does_not_cover(self):
        row = "| Doe | Jane Doe | https://example.org/d | CC-BY-4.0 | definition | `spec/other.md` |\n"
        self.assertEqual(len(check_sources.check(make({"spec/s.md": "# S\n"}, row))), 1)

    def test_front_matter_outside_header_is_ignored(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": "# P\n---\nsources: none\n---\n"}))), 1)

    def test_missing_register_fails(self):
        root = Path(tempfile.mkdtemp())
        self.assertEqual(check_sources.check(root), ["SOURCES.md is missing"])


if __name__ == "__main__":
    unittest.main()
