# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Pipeline receipt chains: the valid fixture passes, every mutant is refused with its code, the committed fixtures equal the regenerated ones,
and mutating the validator itself turns the fixtures red."""

from __future__ import annotations

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
import check_pipeline_receipts as cpr  # noqa: E402
import pipeline_fixture as fx  # noqa: E402

VALIDATOR_SOURCE = (Path(cpr.__file__)).read_text(encoding="utf-8")


def codes(problems: list[str]) -> set[str]:
    return {p.split(":", 1)[0] for p in problems}


def materialise(files: dict[str, bytes]) -> Path:
    directory = Path(tempfile.mkdtemp(prefix="pipeline-chain-"))
    for name, data in files.items():
        (directory / name).write_bytes(data)
    return directory


def mutated_validator(code: str) -> types.ModuleType:
    """The validator with the condition that guards `code` switched off."""
    lines = VALIDATOR_SOURCE.splitlines()
    hits = [i for i, line in enumerate(lines) if f'f"{code}:' in line]
    assert hits, f"{code} is not appended anywhere"
    for hit in hits:
        i = hit
        while not re.match(r"\s*(if|elif)\s", lines[i]):
            i -= 1
        lines[i] = re.sub(r"^(\s*(?:if|elif)\s)(.*):\s*$", r"\1False and (\2):", lines[i], count=1)
        assert "False and (" in lines[i], lines[i]
    module = types.ModuleType("check_pipeline_receipts_mutant")
    module.__file__ = cpr.__file__
    exec(compile("\n".join(lines), cpr.__file__, "exec"), module.__dict__)
    return module


class FixtureTests(unittest.TestCase):
    def test_committed_fixtures_equal_the_regenerated_ones(self):
        committed = {}
        for path in sorted(fx.FIXTURE_ROOT.glob("*/*")):
            committed[f"{path.parent.name}/{path.name}"] = {p.name: p.read_bytes() for p in sorted(path.iterdir())}
        self.assertEqual(committed, fx.variants(), "run python3 tools/pipeline_fixture.py write")

    def test_the_valid_chain_passes(self):
        self.assertEqual(cpr.check_chain(materialise(fx.variants()["valid/synthetic-chain"])), [])

    def test_every_mutant_is_refused_with_its_code(self):
        for name, files in fx.variants().items():
            expected = fx.EXPECTED[name]
            with self.subTest(name):
                problems = cpr.check_chain(materialise(files))
                if expected is None:
                    self.assertEqual(problems, [])
                else:
                    self.assertIn(expected, codes(problems), problems)

    def test_every_code_of_the_specification_has_a_mutant(self):
        invalid = [n for n in fx.EXPECTED if n.startswith("invalid/")]
        self.assertEqual(len(invalid), 41)
        self.assertEqual(len([n for n in fx.EXPECTED if n.startswith("valid/")]), 13)
        spec = (cpr.REPO / "engineering/specifications/pipeline/SPECIFICATION.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"`(PIPE-[A-Z-]+)`", spec))
        self.assertEqual(listed - {"PIPE-EMPTY"}, {c for c in set(fx.EXPECTED.values()) if c})
        self.assertIn("PIPE-EMPTY", listed)  # refused by test_an_empty_or_missing_directory_is_refused: a directory cannot be committed empty

    def test_the_counts_the_specification_states_are_the_counts_of_the_fixtures(self):
        spec = (cpr.REPO / "engineering/specifications/pipeline/SPECIFICATION.md").read_text(encoding="utf-8")
        words = {13: "Thirteen", 41: "forty-one"}
        valid = len([n for n in fx.EXPECTED if n.startswith("valid/")])
        invalid = len([n for n in fx.EXPECTED if n.startswith("invalid/")])
        self.assertIn(f"{words[valid]} valid", spec)
        self.assertIn(f"{words[invalid]} one-defect mutants", spec)
        self.assertIn(f"{words[invalid]} mutants of the first", spec)
        readme = (fx.FIXTURE_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"`valid/` holds {words[valid].lower()} chains", readme)

    def test_fixtures_are_deterministic(self):
        self.assertEqual(fx.variants(), fx.variants())


class ImportAdapterTests(unittest.TestCase):
    def chain(self, name: str) -> list[dict]:
        return [json.loads(data) for _, data in sorted(fx.variants()[name].items())]

    def test_the_imported_chain_is_a_new_chain_from_intake_with_the_import_named_and_nothing_executed(self):
        chain = self.chain("valid/imported-recognition-chain")
        self.assertEqual([r["stage"] for r in chain][:4], ["intake", "classify", "convert", "recognise"])
        self.assertEqual(chain[1]["outcome"], "skipped")
        recognise = chain[3]
        self.assertTrue(recognise["tool"]["name"].endswith(cpr.IMPORT_SUFFIX))
        measured = {m["name"]: m for m in recognise["measurements"]}
        self.assertEqual((measured["recognition_executed"]["status"], measured["recognition_executed"]["value"]), ("measured", False))
        self.assertEqual(measured["original_finished_at"]["status"], "not_measured")
        self.assertTrue(measured["recorded_damage_places"]["name"].startswith("recorded_"))
        self.assertEqual(cpr.check_chain(materialise(fx.variants()["valid/imported-recognition-chain"])), [])

    def test_the_import_rules_object_in_their_own_code_and_the_digest_mismatch_in_the_input_rule(self):
        imports = [n for n in fx.EXPECTED if n.startswith("invalid/") and ("import" in n or "recognition_not_executed" in n)]
        self.assertEqual(len(imports), 14)
        for name in imports:
            with self.subTest(name):
                found = codes(cpr.check_chain(materialise(fx.variants()[name])))
                self.assertEqual(found, {"PIPE-INPUT"} if name.endswith("output_not_consumed") else {"PIPE-IMPORT"}, name)
        elsewhere = cpr.check_chain(materialise(fx.variants()["invalid/import_named_on_another_stage"]))
        self.assertTrue(any("recognise only" in p for p in elsewhere), elsewhere)  # the stage rule itself, not the measurement rule that would also object

    def test_other_spellings_of_false_are_not_false_and_the_match_of_the_import_name_is_exact(self):
        def check(edit) -> set:
            chain = self.chain("valid/imported-recognition-chain")
            chain[4]["measurements"] = []  # the verify-only bundle record is tested on its own; here only the recognise receipt is varied
            edit(chain)
            return codes(cpr.check_chain(materialise(fx.link(chain))))
        for value in ("false", 0, None):
            with self.subTest(import_value=value):
                found = check(lambda c, value=value: c[3]["measurements"][0].update(value=value))
                self.assertTrue(found & {"PIPE-IMPORT", "PIPE-SCHEMA"}, found)
            with self.subTest(ordinary_tool_value=value):
                found = check(lambda c, value=value: (c[3].update(tool={"name": "doclab-ocr", "version": "0"}), c[3]["measurements"][0].update(value=value)))
                self.assertNotIn("PIPE-IMPORT", found)  # "false" and 0 are not the boolean the rule is about; null is refused by the schema
        # an ordinary tool with 0 does not claim the boolean false; with the real false it is refused
        self.assertEqual(check(lambda c: (c[3].update(tool={"name": "doclab-ocr", "version": "0"}), c[3]["measurements"][0].update(value=0))), set())
        self.assertIn("PIPE-IMPORT", check(lambda c: c[3].update(tool={"name": "doclab-Import", "version": "0"})))  # not an exact -import name, and false is claimed
        self.assertEqual(check(lambda c: c[3].update(tool={"name": "doclab-import", "version": "0"})), set())
        for lookalike in ("reimport", "x_import", "import", "doclab-import-2"):  # only a name that ends with "-import" names an import; the others are ordinary tools
            self.assertIn("PIPE-IMPORT", check(lambda c, lookalike=lookalike: c[3].update(tool={"name": lookalike, "version": "0"})), lookalike)

    def test_a_repeated_original_run_id_or_finish_time_is_refused_too(self):
        for name in ("original_run_id", "original_finished_at"):
            with self.subTest(name):
                chain = self.chain("valid/imported-recognition-chain")
                chain[3]["measurements"].append({"name": name, "status": "not_measured", "reason": "listed twice"})
                self.assertEqual(codes(cpr.check_chain(materialise(fx.link(chain)))), {"PIPE-IMPORT"})

    def test_an_ordinary_recognition_that_did_not_run_nothing_special_stays_valid_and_a_failed_import_needs_no_measurements(self):
        chain = self.chain("valid/synthetic-chain")
        self.assertEqual(cpr.check_chain(materialise(fx.link(chain))), [])
        imported = self.chain("valid/imported-recognition-chain")
        imported[3].update(outcome="refused", reason="the earlier outputs do not match the source", outputs=[], measurements=[])
        self.assertEqual(cpr.check_chain(materialise(fx.link(imported[:4]))), [])

    def test_the_receipts_carry_the_rights_state_known_and_a_determination_lives_only_in_the_package(self):
        spec = (cpr.REPO / "engineering/specifications/pipeline/SPECIFICATION.md").read_text(encoding="utf-8")
        self.assertIn("the rights state known at that stage", spec)
        self.assertIn("only in the package's rights record, never in a receipt", spec)
        self.assertIn("a chain that starts at `unknown` does not end at `public_domain`", spec)
        self.assertIn("A receipt never claims work that was not done", spec)
        self.assertIn("the imported `recognise` is the one case of a stage that verified and did not run", spec)
        chain = self.chain("valid/imported-recognition-chain")
        self.assertEqual({r["rights_class"] for r in chain}, {"unknown"})  # the imported chain determines nothing
        widened = self.chain("valid/imported-recognition-chain")
        widened[-1]["rights_class"] = "public_domain"  # a determination made in a receipt is a widening
        self.assertIn("PIPE-RIGHTS", codes(cpr.check_chain(materialise(fx.link(widened)))))

    def test_the_bundle_of_an_import_chain_records_that_it_verified_and_did_not_assemble(self):
        chain = self.chain("valid/imported-recognition-chain")
        measured = {m["name"]: (m["status"], m["value"]) for m in chain[4]["measurements"]}
        self.assertEqual(measured, {"bundle_assembled": ("measured", False), "bundle_verified": ("measured", True)})
        self.assertFalse(chain[4]["tool"]["name"].endswith(cpr.IMPORT_SUFFIX))  # the import name belongs to recognise only
        self.assertEqual(cpr.check_chain(materialise(fx.link(chain))), [])
        ordinary = self.chain("valid/synthetic-chain")
        self.assertEqual(cpr.check_chain(materialise(fx.link(ordinary))), [])  # an ordinary bundle carries neither measurement
        ordinary[4]["measurements"] = [{"name": "bundle_assembled", "status": "measured", "value": True}, {"name": "bundle_verified", "status": "measured", "value": True}]
        self.assertEqual(cpr.check_chain(materialise(fx.link(ordinary))), [])  # assembled and then verified is allowed anywhere
        with_import_only = self.chain("valid/imported-recognition-chain")
        with_import_only[4]["measurements"] = []
        self.assertEqual(cpr.check_chain(materialise(fx.link(with_import_only))), [])  # the verify-only record is allowed, not required
        spec = (cpr.REPO / "engineering/specifications/pipeline/SPECIFICATION.md").read_text(encoding="utf-8")
        self.assertIn("MAY verify an existing bundle instead of assembling it", spec)
        self.assertIn("it does not check that the output is the hash of the verified manifest", spec)
        self.assertIn("The checker refuses only a widening of the class along a chain", spec)
        self.assertIn("a chain whose receipts all carry `public_domain` is not refused by it", spec)
        every = self.chain("valid/synthetic-chain")
        for record in every:
            record["rights_class"] = "public_domain"
        self.assertEqual(cpr.check_chain(materialise(fx.link(every))), [])  # the limit stated in the text: only widening is refused

    def test_a_non_boolean_bundle_measurement_and_a_repeated_one_are_refused(self):
        for label, edit in {"string": lambda m: m.update(value="false"), "number": lambda m: m.update(value=0)}.items():
            with self.subTest(label):
                chain = self.chain("valid/imported-recognition-chain")
                edit(chain[4]["measurements"][0])
                self.assertEqual(codes(cpr.check_chain(materialise(fx.link(chain)))), {"PIPE-IMPORT"})
        for name in ("bundle_assembled", "bundle_verified"):  # the first value is the checker's reading only if there is no other
            chain = self.chain("valid/imported-recognition-chain")
            chain[4]["measurements"].append({"name": name, "status": "measured", "value": name == "bundle_verified"})  # agrees with the first
            self.assertEqual(codes(cpr.check_chain(materialise(fx.link(chain)))), {"PIPE-IMPORT"}, name)
        chain = self.chain("valid/imported-recognition-chain")
        chain[4]["measurements"] = [chain[4]["measurements"][0], chain[4]["measurements"][1], {"name": "bundle_assembled", "status": "measured", "value": True}]
        self.assertEqual(codes(cpr.check_chain(materialise(fx.link(chain)))), {"PIPE-IMPORT"})  # last-wins would read assembled true here
        for stage_index in (3, 5):  # the bundle measurements on recognise and on kc-package
            chain = self.chain("valid/imported-recognition-chain")
            chain[stage_index]["measurements"] = chain[stage_index].get("measurements", []) + [{"name": "bundle_verified", "status": "measured", "value": True},
                                                                                             {"name": "bundle_assembled", "status": "measured", "value": False}]
            self.assertIn("PIPE-IMPORT", codes(cpr.check_chain(materialise(fx.link(chain)))), stage_index)
        for repeated in (False, True):  # a second value is refused even when it agrees with the first: one reading only
            chain = self.chain("valid/imported-recognition-chain")
            chain[4]["measurements"].append({"name": "bundle_verified", "status": "measured", "value": repeated})
            self.assertEqual(codes(cpr.check_chain(materialise(fx.link(chain)))), {"PIPE-IMPORT"})

    def test_the_receipt_schema_gained_no_field_for_imports(self):
        schema = json.loads((cpr.REPO / "schemas" / "pipeline-receipt.schema.json").read_text())
        self.assertNotIn("import", json.dumps(schema).lower())
        self.assertEqual(set(schema["properties"]), {"schema", "document_id", "stage", "run_id", "previous_receipt_sha256", "tool", "started_at", "finished_at", "outcome",
                                                       "reason", "rights_class", "inputs", "outputs", "measurements", "kc2_admission"})


class ValidatorBehaviourTests(unittest.TestCase):
    def test_a_skipped_convert_is_a_valid_chain_and_recognise_reads_the_source(self):
        files = fx.variants()["valid/native-format-chain"]
        self.assertEqual(cpr.check_chain(materialise(files)), [])
        skipped = json.loads(files["03-convert.json"])
        self.assertEqual((skipped["outcome"], skipped["outputs"]), ("skipped", []))

    def test_a_receipt_may_not_be_a_symbolic_link_or_oversized(self):
        valid = fx.variants()["valid/synthetic-chain"]
        directory = materialise(valid)
        target = Path(tempfile.mkdtemp()) / "elsewhere.json"
        target.write_bytes(valid["01-intake.json"])
        (directory / "01-intake.json").unlink()
        (directory / "01-intake.json").symlink_to(target)
        self.assertIn("PIPE-READ", codes(cpr.check_chain(directory)))
        big = materialise(valid)
        (big / "99-big.json").write_bytes(b" " * (cpr.MAX_RECEIPT_BYTES + 1))
        self.assertIn("PIPE-READ", codes(cpr.check_chain(big)))

    def test_an_empty_or_missing_directory_is_refused(self):
        self.assertEqual(codes(cpr.check_chain(Path(tempfile.mkdtemp()))), {"PIPE-EMPTY"})
        self.assertEqual(codes(cpr.check_chain(Path("/nonexistent-chain-directory"))), {"PIPE-EMPTY"})

    def test_a_chain_may_stop_after_any_stage(self):
        valid = fx.variants()["valid/synthetic-chain"]
        for keep in range(1, 9):
            with self.subTest(keep=keep):
                files = {k: v for k, v in sorted(valid.items())[:keep]}
                self.assertEqual(cpr.check_chain(materialise(files)), [])

    def test_a_chain_that_ends_with_a_refusal_is_valid_and_offers_no_output(self):
        receipts = fx.valid_receipts()[:4]
        receipts[3].update(outcome="refused", reason="the file is not a book", outputs=[])
        self.assertEqual(cpr.check_chain(materialise(fx.link(receipts))), [])

    def test_public_domain_is_a_rights_class_of_a_chain_and_is_as_open_as_author_open(self):
        receipts = fx.valid_receipts()
        for r in receipts:
            r["rights_class"] = "public_domain"
        self.assertEqual(cpr.check_chain(materialise(fx.link(receipts))), [])
        receipts[5]["rights_class"] = "author_open"  # between the two open classes nothing widens
        self.assertEqual(cpr.check_chain(materialise(fx.link(receipts))), [])
        widened = fx.valid_receipts()
        for r in widened:
            r["rights_class"] = "unknown"
        widened[6]["rights_class"] = "public_domain"
        self.assertIn("PIPE-RIGHTS", codes(cpr.check_chain(materialise(fx.link(widened)))))

    def test_order_comes_from_the_links_not_from_file_names(self):
        valid = fx.variants()["valid/synthetic-chain"]
        renamed = {f"z{9 - n}.json": data for n, (name, data) in enumerate(sorted(valid.items()))}
        self.assertEqual(cpr.check_chain(materialise(renamed)), [])

    def test_a_non_json_file_extension_is_not_a_receipt(self):
        files = dict(fx.variants()["valid/synthetic-chain"])
        files["notes.txt"] = b"not a receipt"
        self.assertEqual(cpr.check_chain(materialise(files)), [])

    def test_command_line_exit_codes(self):
        valid = materialise(fx.variants()["valid/synthetic-chain"])
        bad = materialise(fx.variants()["invalid/id_changed"])
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(cpr.main(["x", str(valid)]), 0)
            self.assertEqual(cpr.main(["x", str(bad)]), 1)
            self.assertEqual(cpr.main(["x"]), 2)
        self.assertIn("PIPELINE_CHAIN_PASS", out.getvalue())
        self.assertIn("PIPELINE_CHAIN_FAIL PIPE-ID", out.getvalue())

    def test_a_pass_says_what_it_does_not_claim(self):
        out = io.StringIO()
        with redirect_stdout(out):
            cpr.main(["x", str(materialise(fx.variants()["valid/synthetic-chain"]))])
        self.assertIn("no stage quality, no KC2 admission", out.getvalue())


class ValidatorMutationTests(unittest.TestCase):
    """Switch off one rule of the validator; the mutant fixture that the rule exists for must stop being refused with that code."""

    CASES = {
        "PIPE-LINK": "invalid/link_broken_by_an_edit", "PIPE-FORK": "invalid/fork", "PIPE-ID": "invalid/id_changed",
        "PIPE-IDENTITY": "invalid/source_is_not_the_id", "PIPE-AFTER-STOP": "invalid/consumed_after_refusal",
        "PIPE-INPUT": "invalid/input_not_from_predecessor", "PIPE-TIME": "invalid/time_runs_backwards",
        "PIPE-RIGHTS": "invalid/rights_widened", "PIPE-STAGE-ORDER": "invalid/out_of_order", "PIPE-HEAD": "invalid/orphan_file",
        "PIPE-SKIP": "invalid/essential_stage_skipped", "PIPE-SOURCE": "invalid/source_as_input_of_a_later_stage",
    }

    def test_each_rule_is_load_bearing(self):
        variants = fx.variants()
        for code, name in self.CASES.items():
            with self.subTest(code):
                original = cpr.check_chain(materialise(variants[name]))
                self.assertIn(code, codes(original))
                mutant = mutated_validator(code)
                try:
                    survivors = codes(mutant.check_chain(materialise(variants[name])))
                except (KeyError, IndexError, TypeError):
                    continue  # with the guard off the validator cannot even continue: the guard is load-bearing
                self.assertNotIn(code, survivors, f"{code} is not guarded by its own condition")

    def test_the_valid_chain_still_passes_every_mutant(self):
        valid = fx.variants()["valid/synthetic-chain"]
        for code in self.CASES:
            with self.subTest(code):
                self.assertEqual(mutated_validator(code).check_chain(materialise(valid)), [])


class SchemaTests(unittest.TestCase):
    def test_the_schema_is_a_valid_draft_2020_12_document(self):
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(json.loads(cpr.SCHEMA_PATH.read_text(encoding="utf-8")))

    def test_the_stage_list_of_the_schema_equals_the_validator_order(self):
        schema = json.loads(cpr.SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(tuple(schema["properties"]["stage"]["enum"]), cpr.STAGES)
        self.assertEqual(len(cpr.STAGES), 9)


if __name__ == "__main__":
    unittest.main()
