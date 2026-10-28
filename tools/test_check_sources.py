import tempfile
import unittest
from pathlib import Path

from tools import check_sources

HEADER = "| Source | Author | URI | License | What was used | Where |\n| --- | --- | --- | --- | --- | --- |\n"
DOE = "| Doe 2020 | Jane Doe | https://example.org/d | CC-BY-4.0 | definition | `papers/z.md` |\n"


def make(files: dict[str, str], register: str = "") -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "SOURCES.md").write_text("# Sources\n\n" + HEADER + register, encoding="utf-8")
    for name, body in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return root


def front(value: str) -> str:
    return f"---\n{value}\n---\n# P\n"


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
        self.assertEqual(check_sources.check(make({"papers/p.md": front("sources: none")})), [])

    def test_registered_flow_and_block_lists_pass(self):
        files = {"papers/a.md": front("sources: [Doe 2020]"), "spec/b.md": front("sources:\n  - Doe 2020\n  - 'doe 2020'")}
        self.assertEqual(check_sources.check(make(files, DOE)), [])

    def test_unregistered_list_entry_fails(self):
        problems = check_sources.check(make({"papers/p.md": front("sources: [Doe 2020, Roe 2021]")}, DOE))
        self.assertEqual(len(problems), 1)
        self.assertIn("Roe 2021", problems[0])

    def test_empty_flow_list_fails(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": front("sources: []")}, DOE))), 1)

    def test_list_of_blank_entries_fails(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": front("sources: [ , '' ]")}, DOE))), 1)

    def test_empty_string_fails(self):
        for value in ('sources: ""', "sources: ''"):
            with self.subTest(value=value):
                self.assertEqual(len(check_sources.check(make({"papers/p.md": front(value)}, DOE))), 1)

    def test_bare_scalar_fails(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": front("sources: Doe 2020")}, DOE))), 1)

    def test_empty_key_fails(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": front("sources:\ntitle: x")}, DOE))), 1)

    def test_register_row_covers_any_type(self):
        row = "| Doe | Jane Doe | https://example.org/d | CC-BY-4.0 | definition | `spec/s.json` |\n"
        self.assertEqual(check_sources.check(make({"spec/s.json": "{}"}, row)), [])

    def test_register_row_for_other_path_does_not_cover(self):
        row = "| Doe | Jane Doe | https://example.org/d | CC-BY-4.0 | definition | `spec/other.md` |\n"
        self.assertEqual(len(check_sources.check(make({"spec/s.md": "# S\n"}, row))), 1)

    def test_front_matter_outside_header_is_ignored(self):
        self.assertEqual(len(check_sources.check(make({"papers/p.md": "# P\n---\nsources: none\n---\n"}))), 1)

    def test_missing_register_fails(self):
        self.assertEqual(check_sources.check(Path(tempfile.mkdtemp())), ["SOURCES.md is missing"])


if __name__ == "__main__":
    unittest.main()
