# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Document classification (kc-doc-class/1): the twelve valid cases pass, every mutant is refused with its code, the committed fixtures equal the regenerated
ones, the canon digest recomputes, the specification matches the canon and the fixtures, and mutating the schema or the checker turns the fixtures red."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import re
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_document_classification as cdc  # noqa: E402
import check_pipeline_receipts as cpr  # noqa: E402
import document_classification_fixture as fx  # noqa: E402
import pipeline_fixture as pf  # noqa: E402

SPEC = (cdc.REPO / "engineering" / "specifications" / "pipeline" / "SPECIFICATION.md").read_text(encoding="utf-8")
CHECKER_SOURCE = Path(cdc.__file__).read_text(encoding="utf-8")
CLASSES = ["book", "paper", "export", "dataset", "other"]


def codes(problems: list[str]) -> set[str]:
    return {p.split(":", 1)[0] for p in problems}


def mutated_checker(code: str) -> types.ModuleType:
    """The checker with the condition that guards `code` switched off."""
    lines = CHECKER_SOURCE.splitlines()
    hits = [i for i, line in enumerate(lines) if f'"{code}:' in line or f"f\"{code}:" in line]
    assert hits, f"{code} is not appended anywhere"
    for hit in hits:
        i = hit
        while not re.match(r"\s*(if|elif)\s", lines[i]):
            i -= 1
        lines[i] = re.sub(r"^(\s*(?:if|elif)\s)(.*):\s*$", r"\1False and (\2):", lines[i], count=1)
        assert "False and (" in lines[i], lines[i]
    module = types.ModuleType("check_document_classification_mutant")
    module.__file__ = cdc.__file__
    exec(compile("\n".join(lines), cdc.__file__, "exec"), module.__dict__)
    return module


class FixtureTests(unittest.TestCase):
    def test_committed_fixtures_equal_the_regenerated_ones(self):
        committed = {f"{p.parent.name}/{p.name}": p.read_bytes() for p in sorted(fx.FIXTURE_ROOT.glob("*/*.json"))}
        self.assertEqual(committed, {f"{k}.json": v for k, v in fx.variants().items()}, "run python3 tools/document_classification_fixture.py write")

    def test_every_valid_case_passes_and_every_mutant_is_refused_with_exactly_its_code(self):
        for name, data in fx.variants().items():
            with self.subTest(fixture=name):
                found = codes(cdc.check_classification(data))
                expected = fx.EXPECTED[name]
                self.assertEqual(found, set() if expected is None else {expected}, name)

    def test_the_expectations_cover_exactly_the_generated_files(self):
        self.assertEqual(set(fx.EXPECTED), set(fx.variants()))

    def test_the_twelve_boundary_cases_have_the_outcomes_of_the_canon(self):
        got = {}
        for name, record in fx.CASES:
            got[name[:2]] = (record["status"], record["class"], tuple(record["candidates"]), record["coverage"])
        self.assertEqual(got, {
            "01": ("classified", "book", ("book",), "complete"), "02": ("classified", "book", ("book",), "complete"), "03": ("classified", "book", ("book",), "partial"),
            "04": ("classified", "paper", ("paper",), "complete"), "05": ("classified", "other", ("other",), "complete"), "06": ("classified", "export", ("export",), "complete"),
            "07": ("classified", "dataset", ("dataset",), "complete"), "08": ("classified", "dataset", ("dataset",), "complete"), "09": ("classified", "paper", ("paper",), "complete"),
            "10": ("classified", "other", ("other",), "complete"), "11": ("unknown", None, (), "not_measured"), "12": ("ambiguous", None, ("book", "paper"), "not_measured")})

    def test_no_valid_case_invents_a_confidence_number(self):
        for name, record in fx.CASES:
            self.assertEqual(record["confidence"]["status"], "not_measured", name)
            self.assertNotIn("score", record["confidence"], name)


class CanonTests(unittest.TestCase):
    def test_the_canon_agrees_with_the_schema(self):
        self.assertEqual(cdc.check_canon(), [])

    def test_the_canon_has_the_five_classes_and_the_migration_statement(self):
        canon = json.loads(cdc.CANON_PATH.read_text())
        self.assertEqual([c["id"] for c in canon["classes"]], CLASSES)
        self.assertEqual(canon["taxonomy_id"], "kc-doc-class/1")
        self.assertIn("No classification result, receipt or other data was ever written", canon["migration"]["history"])

    def test_every_fixture_carries_the_digest_of_the_current_canon(self):
        digest = hashlib.sha256(cdc.CANON_PATH.read_bytes()).hexdigest()
        self.assertEqual(digest, cdc.canon_digest())
        for name, record in fx.CASES:
            self.assertEqual(record["canon_sha256"], digest, name)

    def test_a_changed_canon_makes_every_result_stale_instead_of_being_read_as_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            changed = Path(tmp) / "document-classes.json"
            changed.write_bytes(cdc.CANON_PATH.read_bytes().replace(b"book or an independently", b"book or any independently", 1))
            data = fx.variants()["valid/01-complete-book-with-evidenced-identity"]
            self.assertEqual(codes(cdc.check_classification(data, changed)), {"DCL-CANON"})

    def test_a_canon_that_disagrees_with_the_schema_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            for old, new in ((b'"id": "dataset"', b'"id": "table"'), (b'"kc-doc-class/1"', b'"kc-doc-class/2"'), (b'"id": "unknown"', b'"id": "unsure"')):
                with self.subTest(old=old):
                    changed = Path(tmp) / "c.json"
                    changed.write_bytes(cdc.CANON_PATH.read_bytes().replace(old, new, 1))
                    self.assertEqual(codes(cdc.check_canon(changed)), {"DCL-CANON-FILE"})


class SpecificationTests(unittest.TestCase):
    def test_the_specification_table_is_the_canon(self):
        canon = json.loads(cdc.CANON_PATH.read_text())
        section = SPEC[SPEC.index("## 10. Document classes"):]
        rows = {m[1]: (m[2], m[3]) for m in re.finditer(r"^\| `(\w+)` \| (.*?) \| (.*?) \|$", section, re.M)}
        for c in canon["classes"]:
            self.assertIn(c["id"], rows)
            self.assertEqual(rows[c["id"]][0].replace("`", ""), c["definition"])
            self.assertEqual(rows[c["id"]][1].replace("`", ""), c["boundary"])

    def test_the_numbers_in_the_specification_are_the_numbers_of_the_fixtures(self):
        valid = [k for k in fx.variants() if k.startswith("valid/")]
        invalid = [k for k in fx.variants() if k.startswith("invalid/")]
        self.assertEqual(len(valid), 12)
        self.assertIn("The twelve boundary cases are committed", SPEC)
        words = {28: "Twenty-eight"}
        self.assertIn(words.get(len(invalid), "?"), SPEC, f"the specification names {len(invalid)} mutants as another number")

    def test_the_requirements_are_numbered_and_cite_a_test_or_say_that_they_need_other_evidence(self):
        register = json.loads((cdc.REPO / "engineering" / "specifications" / "requirements.json").read_text())["requirements"]
        ids = {r["id"] for r in register if r["document"].endswith("pipeline/SPECIFICATION.md")}
        for n in range(14, 23):
            self.assertIn(f"PIP-R{n:03d}", ids)

    def test_the_migration_wording_claims_no_history(self):
        self.assertIn("existed only as a proposal", SPEC)
        self.assertIn("No classification result, receipt or other data was ever written with it", SPEC)

    def test_section_six_no_longer_says_that_only_author_open_publishes(self):
        six = SPEC[SPEC.index("## 6. Rights and publication boundary"):SPEC.index("## 7.")]
        self.assertNotIn("a work that is not `author_open` stays out", six)
        self.assertIn("neither `author_open` nor `public_domain`", six)


class SchemaTests(unittest.TestCase):
    def schema(self) -> dict:
        return json.loads(cdc.SCHEMA_PATH.read_text())

    def refused_by(self, schema: dict, record: dict) -> bool:
        import jsonschema
        return bool(list(jsonschema.Draft202012Validator(schema).iter_errors(record)))

    def per_class_mismatches(self) -> list[dict]:
        base = copy.deepcopy(fx.CASES[0][1])
        out = []
        for cls in CLASSES:
            other = next(c for c in CLASSES if c != cls)
            r = copy.deepcopy(base)
            r.update({"class": cls, "candidates": [other]})
            out.append(r)
        return out

    def test_every_class_must_be_its_own_only_candidate(self):
        for record in self.per_class_mismatches():
            self.assertTrue(self.refused_by(self.schema(), record), record["class"])

    def test_removing_any_invariant_from_the_schema_lets_a_bad_record_through(self):
        schema = self.schema()
        bad = [json.loads(v) for k, v in fx.variants().items() if k.startswith("invalid/") and fx.EXPECTED[k] == "DCL-SCHEMA" and k != "invalid/not_json"] + self.per_class_mismatches()
        for i in range(len(schema["allOf"])):
            mutated = copy.deepcopy(schema)
            del mutated["allOf"][i]
            with self.subTest(rule=i):
                self.assertTrue(any(not self.refused_by(mutated, r) for r in bad), f"allOf[{i}] guards nothing")

    def test_the_schema_properties_that_carry_the_other_rules_are_each_needed(self):
        schema = self.schema()
        bad = [json.loads(v) for k, v in fx.variants().items() if k.startswith("invalid/") and fx.EXPECTED[k] == "DCL-SCHEMA" and k != "invalid/not_json"]
        edits = {
            "coverage required": lambda s: s["required"].remove("coverage"),
            "evidence minItems": lambda s: s["properties"]["evidence"].pop("minItems"),
            "additionalProperties": lambda s: s.update(additionalProperties=True),
            "confidence oneOf": lambda s: s["properties"].update(confidence={}),
            "document id pattern": lambda s: s["properties"]["document_id"].pop("pattern"),
            "evidence digest pattern": lambda s: s["properties"]["evidence"]["items"]["properties"]["representation_sha256"].pop("pattern"),
            "evidence basis required": lambda s: s["properties"]["evidence"]["items"]["required"].remove("basis"),
            "candidates unique": lambda s: s["properties"]["candidates"].pop("uniqueItems"),
        }
        for name, edit in edits.items():
            mutated = self.schema()
            edit(mutated)
            with self.subTest(edit=name):
                self.assertTrue(any(not self.refused_by(mutated, r) for r in bad), name)

    def test_the_result_has_no_rights_damage_readiness_or_admission_field(self):
        props = set(self.schema()["properties"])
        for forbidden in ("rights_class", "license", "damage", "knowledge_ready", "package_status", "kc2_admission", "publishable"):
            self.assertNotIn(forbidden, props)


class CheckerTests(unittest.TestCase):
    def test_each_refusal_code_of_the_checker_is_needed(self):
        for code, fixture in (("DCL-TAXONOMY", "invalid/taxonomy_is_the_proposal_label"), ("DCL-CANON", "invalid/taxonomy_digest_wrong")):
            module = mutated_checker(code)
            with self.subTest(code=code):
                self.assertEqual(module.check_classification(fx.variants()[fixture]), [], f"{code} is not needed to refuse {fixture}")

    def test_the_independent_invariant_check_agrees_with_the_schema(self):
        valid = [r for _, r in fx.CASES]
        for record in valid:
            self.assertEqual(cdc._invariants(record), [])
        for key, data in fx.variants().items():
            if key.startswith("invalid/") and fx.EXPECTED[key] == "DCL-SCHEMA" and key != "invalid/not_json":
                record = json.loads(data)
                if "status" in record and ("class" in record or "candidates" in record):
                    structural = any(s in key for s in ("class", "candidate", "ambiguous", "unknown", "other", "measured"))
                    if structural and "evidence" not in key and "coverage" not in key and "digest" not in key and "document_id" not in key and "unknown_field" not in key and "confidence_without" not in key:
                        self.assertTrue(cdc._invariants(record), key)

    def test_the_command_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            good, bad = Path(tmp) / "g.json", Path(tmp) / "b.json"
            good.write_bytes(fx.variants()["valid/12-unresolved-book-versus-report-evidence"])
            bad.write_bytes(fx.variants()["invalid/taxonomy_digest_wrong"])
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(cdc.main(["x", str(good)]), 0)
                self.assertEqual(cdc.main(["x", str(bad)]), 1)
                self.assertEqual(cdc.main(["x", str(Path(tmp) / "missing.json")]), 1)
                self.assertEqual(cdc.main(["x"]), 2)
            self.assertIn("DOCCLASS_PASS", out.getvalue())
            self.assertIn("DCL-CANON", out.getvalue())

    def test_an_oversized_or_deeply_nested_file_is_a_refusal_not_a_traceback(self):
        self.assertEqual(codes(cdc.check_classification(b" " * ((1 << 20) + 1))), {"DCL-READ"})
        self.assertEqual(codes(cdc.check_classification(b"[" * 100000)), {"DCL-READ"})
        self.assertEqual(codes(cdc.check_classification(b"\xff")), {"DCL-READ"})
        self.assertEqual(codes(cdc.check_classification(b"[]")), {"DCL-SCHEMA"})


class BindingTests(unittest.TestCase):
    def receipt(self, data: bytes) -> dict:
        record = next(r for r in pf.valid_receipts() if r["stage"] == "classify")
        record = copy.deepcopy(record)
        doc = json.loads(data)["document_id"]
        record["document_id"] = doc
        record["outputs"] = [{"role": "classification", "sha256": hashlib.sha256(data).hexdigest()}]
        return record

    def test_a_receipt_that_lists_the_exact_bytes_is_bound(self):
        data = fx.variants()["valid/01-complete-book-with-evidenced-identity"]
        self.assertEqual(cdc.check_binding(self.receipt(data), data), [])

    def test_the_binding_is_refused_when_it_does_not_hold(self):
        data = fx.variants()["valid/01-complete-book-with-evidenced-identity"]
        other = fx.variants()["valid/04-standalone-preprint-or-long-report"]
        cases = {
            "another file's bytes": (self.receipt(data), other),
            "digest altered": ({**self.receipt(data), "outputs": [{"role": "classification", "sha256": "0" * 64}]}, data),
            "no classification output": ({**self.receipt(data), "outputs": [{"role": "result_bundle", "sha256": hashlib.sha256(data).hexdigest()}]}, data),
            "two classification outputs": ({**self.receipt(data), "outputs": self.receipt(data)["outputs"] * 2}, data),
            "another document": ({**self.receipt(data), "document_id": "d_" + "1" * 64}, data),
            "stage is not classify": ({**self.receipt(data), "stage": "convert"}, data),
            "classify skipped": ({**self.receipt(data), "outcome": "skipped", "outputs": []}, data),
            "not an object": (self.receipt(data), b"[]"),
        }
        for name, (receipt, payload) in cases.items():
            with self.subTest(case=name):
                self.assertEqual(codes(cdc.check_binding(receipt, payload)), {"DCL-BINDING"})

    def test_the_receipt_schema_is_unchanged_and_the_existing_chains_stay_valid(self):
        schema = json.loads(cpr.SCHEMA_PATH.read_text())
        for forbidden in ("class", "taxonomy", "taxonomy_id", "canon_sha256", "classification"):
            self.assertNotIn(forbidden, schema["properties"])
        chain = pf.link(pf.valid_receipts())
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in chain.items():
                (Path(tmp) / name).write_bytes(data)
            self.assertEqual(cpr.check_chain(Path(tmp)), [])
        classify = next(r for r in pf.valid_receipts() if r["stage"] == "classify")
        self.assertEqual([o["role"] for o in classify["outputs"]], ["classification"])

    def test_a_skipped_classify_stage_leaves_no_classification(self):
        skipped = next(r for r in pf.variants()["valid/classify-and-convert-skipped"].items() if "classify" in r[0])
        record = json.loads(skipped[1])
        self.assertEqual((record["outcome"], record["outputs"]), ("skipped", []))


if __name__ == "__main__":
    unittest.main()
