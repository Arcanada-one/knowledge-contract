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
        self.assertEqual(len(invalid), 25)
        self.assertEqual(len([n for n in fx.EXPECTED if n.startswith("valid/")]), 12)
        spec = (cpr.REPO / "engineering/specifications/pipeline/SPECIFICATION.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"`(PIPE-[A-Z-]+)`", spec))
        self.assertEqual(listed - {"PIPE-EMPTY"}, {c for c in set(fx.EXPECTED.values()) if c})
        self.assertIn("PIPE-EMPTY", listed)  # refused by test_an_empty_or_missing_directory_is_refused: a directory cannot be committed empty

    def test_fixtures_are_deterministic(self):
        self.assertEqual(fx.variants(), fx.variants())


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
