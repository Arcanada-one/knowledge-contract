import unittest

from tools.check_separation import violates


class SeparationTests(unittest.TestCase):
    def test_mixed_changes_fail(self):
        self.assertTrue(violates(["corpus/publication-decisions/b1.jsonl", "articles/a.md"]))
        self.assertTrue(violates(["corpus/README.md", "papers/p.md"]))
        self.assertTrue(violates(["corpus/publication-decisions/receipts/b1.json", "schemas/s.md"]))

    def test_single_area_changes_pass(self):
        self.assertFalse(violates(["corpus/publication-decisions/b1.jsonl", "corpus/publication-decisions/receipts/b1.json"]))
        self.assertFalse(violates(["corpus/README.md", "OPENNESS.md", "tools/export_corpus.py"]))
        self.assertFalse(violates(["articles/a.md", "papers/p.md"]))
        self.assertFalse(violates([]))


if __name__ == "__main__":
    unittest.main()
