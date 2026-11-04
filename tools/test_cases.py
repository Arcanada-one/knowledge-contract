import re
import unittest
from pathlib import Path

import check_cases as cc

WRITTEN = (cc.CASES / "paper-publication-pipeline.md").read_text(encoding="utf-8")
PLANNED = (cc.CASES / "public-read-api.md").read_text(encoding="utf-8")


def problems(text):
    return cc.check_case_text(text, "t")


# name -> (function text -> text, fragment expected among the problems)
MUTATIONS = {
    "untagged_number": (lambda t: t.replace("holds 6 [R4] decision lines", "holds 7 decision lines"), "has no receipt tag"),
    "wrong_number_right_tag": (lambda t: t.replace("holds 6 [R4]", "holds 7 [R4]"), "differs from R4"),
    "wrong_value_in_table": (lambda t: t.replace("| count | /decision_lines_sha256 | 6 |", "| count | /decision_lines_sha256 | 7 |"), "states 7 but the receipt gives 6"),
    "tag_without_row": (lambda t: t.replace("holds 6 [R4]", "holds 6 [R40]"), "has no row"),
    "unused_receipt": (lambda t: t.replace("14 [R5]", "many"), "never used"),
    "number_word": (lambda t: t.replace("A pair of blind reviewers", "Two blind reviewers"), "number word"),
    "missing_file": (lambda t: t.replace("receipts/meaning-management/link-rewrites.json", "receipts/none.json"), "cannot be resolved"),
    "path_traversal": (lambda t: t.replace("receipts/meaning-management/link-rewrites.json", "../etc/passwd"), "cannot be resolved"),
    "bad_pointer": (lambda t: t.replace("| /files | 24 |", "| /nofiles | 24 |"), "cannot be resolved"),
    "unknown_kind": (lambda t: t.replace("| count | /files |", "| guess | /files |"), "unknown kind"),
    "missing_section": (lambda t: t.replace("## What failed on the way", "## Notes"), "section 'What failed on the way'"),
    "empty_section": (lambda t: re.sub(r"## Limits\n.*?## What failed", "## Limits\n\nn/a\n\n## What failed", t, flags=re.S), "section 'Limits'"),
    "host_path": (lambda t: t.replace("## Goal\n", "## Goal\n\nSee /home/user/x.\n"), "host detail"),
    "private_address": (lambda t: t.replace("## Goal\n", "## Goal\n\nHost 10.1.2.3 was used.\n"), "host detail"),
    "secret_shape": (lambda t: t.replace("## Goal\n", "## Goal\n\nkey ghp_" + "a" * 24 + "\n"), "secret shape"),
    "email": (lambda t: t.replace("## Goal\n", "## Goal\n\nWrite to someone@example.org\n"), "personal identifier"),
    "handle": (lambda t: t.replace("## Goal\n", "## Goal\n\nAsk @someone about it\n"), "personal identifier"),
    "hyphen_range": (lambda t: t.replace("holds 6 [R4] decision lines", "holds 6-7 decision lines"), "has no receipt tag"),
    "glued_unit": (lambda t: t.replace("## Goal\n", "## Goal\n\nIt took 300ms and 12x more.\n"), "has no receipt tag"),
    "ordinal_word": (lambda t: t.replace("## Goal\n", "## Goal\n\nThe nineteenth item came third.\n"), "number word"),
    "number_in_table_outside_receipts": (lambda t: t.replace("## Limits\n", "## Limits\n\n| a | b |\n| - | - |\n| 77 | x |\n"), "has no receipt tag"),
    "number_in_html_comment": (lambda t: t.replace("## Goal\n", "## Goal\n\n<!-- 99 files -->\n"), "has no receipt tag"),
    "number_in_link_text": (lambda t: t.replace("## Goal\n", "## Goal\n\nSee [the 42 items](https://example.org/a).\n"), "has no receipt tag"),
    "wrong_license": (lambda t: t.replace("license: CC-BY-4.0", "license: MIT"), "CC-BY-4.0"),
    "wrong_status": (lambda t: t.replace("status: written", "status: done"), "status must be"),
    "no_front_matter_key": (lambda t: t.replace("case_id: paper-publication-pipeline\n", ""), "lacks case_id"),
}


class CaseTests(unittest.TestCase):
    def test_committed_cases_pass(self):
        self.assertEqual(cc.check_all(), [])

    def test_every_mutation_is_reported(self):
        for name, (fn, fragment) in MUTATIONS.items():
            out = problems(fn(WRITTEN))
            self.assertNotEqual(fn(WRITTEN), WRITTEN, f"{name} did not change the text")
            self.assertTrue(any(fragment in p for p in out), f"{name}: {fragment!r} not in {out}")

    def test_planned_case_rules(self):
        self.assertEqual(problems(PLANNED), [])
        self.assertTrue(any("may not carry numbers" in p for p in problems(PLANNED.replace("Pending. Not measured", "Pending. 5 checks. Not measured", 1))))
        self.assertTrue(any("lists no receipts" in p for p in problems(PLANNED.replace("None yet.", "\n| R1 | a | count | /x | 1 |\n"))))
        self.assertTrue(any("lists no receipts" in p for p in problems(re.sub(r"awaiting: .*\n", "", PLANNED))))

    def test_index_must_list_every_case_and_nothing_else(self):
        index = (cc.CASES / "README.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"\| `([a-z0-9-]+)` \|", index))
        on_disk = {p.stem for p in cc.CASES.glob("*.md") if p.name != "README.md" and not p.name.startswith("_")}
        self.assertEqual(listed, on_disk)

    def test_aal2_required_cases_exist(self):
        required = {"paper-publication-pipeline", "ru10-stand-and-repin", "ocr-stand-doclab", "conversion-adapter-and-deploy", "book-to-knowledge-pipeline",
                    "theory-checks", "practical-closure", "public-read-api"}
        self.assertTrue(required <= {p.stem for p in cc.CASES.glob("*.md")})

    def test_a_changed_receipt_breaks_the_case(self):
        import json
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for sub in ("cases", "corpus", "receipts"):
                shutil.copytree(cc.REPO / sub, root / sub)
            old_repo, old_cases = cc.REPO, cc.CASES
            cc.REPO, cc.CASES = root, root / "cases"
            try:
                self.assertEqual(cc.check_all(), [])
                path = root / "corpus" / "publication-decisions" / "receipts" / "b1.json"
                data = json.loads(path.read_text())
                data["decision_lines_sha256"].append("0" * 64)
                path.write_text(json.dumps(data))
                self.assertTrue(any("states 6 but the receipt gives 7" in p for p in cc.check_all(root / "cases")))
            finally:
                cc.REPO, cc.CASES = old_repo, old_cases


if __name__ == "__main__":
    unittest.main()
