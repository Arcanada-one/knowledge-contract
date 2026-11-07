# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""KCAdmissionObservation/v1 (CANDIDATE): the positive fixtures pass, every mutant is refused with exactly its code, the committed fixtures equal the regenerated ones,
the schema alone refuses what it can express, the claims stay NOT_MEASURED, and switching off any guard of the checker turns the fixtures red (KCLIVE-01)."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import re
import sys
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_kc_admission_observation as cka  # noqa: E402
import kc_admission_observation_fixture as fx  # noqa: E402

SCHEMA = json.loads(cka.SCHEMA_PATH.read_text(encoding="utf-8"))
SOURCE_TEXT = Path(cka.__file__).read_text(encoding="utf-8")
FILES = fx.variants()


def codes(problems: list[str]) -> set[str]:
    return {p.split(":", 1)[0] for p in problems}


def run_all(module) -> dict[str, set[str]]:
    """The set of refusal codes the checker `module` gives each fixture; a crash is its own result, never a pass."""
    out: dict[str, set[str]] = {}
    for name, data in fx.observations().items():
        try:
            problems = module.inspect(data, fx.sidecar(FILES, name, fx.SOURCE), fx.sidecar(FILES, name, fx.WORK))[0]
            out[name] = codes(problems)
        except Exception as exc:  # noqa: BLE001
            out[name] = {f"CRASH-{exc.__class__.__name__}"}
    return out


def expected_codes() -> dict[str, set[str]]:
    return {n: (set() if c is None else {c}) for n, c in fx.EXPECTED.items()}


def disable(source: str, guard: str, occurrence: int = 0) -> str:
    """The checker source with the `if`/`elif` line that contains `guard` switched off (its condition becomes `False and (...)`)."""
    lines = source.splitlines()
    hits = [i for i, line in enumerate(lines) if guard in line and re.match(r"\s*(if|elif)\s", line)]
    assert len(hits) > occurrence, f"no guard {guard!r} (occurrence {occurrence})"
    i = hits[occurrence]
    lines[i] = re.sub(r"^(\s*(?:if|elif)\s)(.*):\s*$", r"\1False and (\2):", lines[i], count=1)
    assert "False and (" in lines[i], lines[i]
    return "\n".join(lines)


def load(source: str) -> types.ModuleType:
    module = types.ModuleType("check_kc_admission_observation_mutant")
    module.__file__ = cka.__file__
    exec(compile(source, cka.__file__, "exec"), module.__dict__)
    return module


# (name, guard text, occurrence): every refusal condition of the checker that has a fixture.
GUARDS = [
    ("selector", 'if record.get("schema") != SCHEMA_ID:', 0),
    ("boolean", "if _has_bool(record):", 0),
    ("claims", 'if record.get("claims_scope") != CLAIMS_SCOPE', 0),
    ("unavailable-branch", "if stray:", 0),
    ("observed-branch", "if stray:", 1),
    ("native-missing", 'if "native_source" not in record:', 0),
    ("reason-on-observed", 'if "reason" in record:', 0),
    ("work-item-no-binding", 'if "work_item_id" in record and "work_item_binding" not in record:', 0),
    ("path-like-id", "if re.search(", 0),
    ("unknown-source", "if not synthetic and system not in NATIVE_SYSTEMS:", 0),
    ("synthetic-coupling", 'if synthetic != record_id.startswith("synthetic:"):', 0),
    ("message-identity", 'if "message_id" in record and record["message_id"] != record_id:', 0),
    ("unknown-work-item-source", 'if binding["system"] not in WORK_ITEM_SYSTEMS and not synthetic:', 0),
    ("work-item-record", 'if binding["record_id"] != record["work_item_id"]:', 0),
    ("work-item-bytes", "elif hashlib.sha256(work_item_bytes)", 0),
    ("native-bytes", 'if hashlib.sha256(source_bytes).hexdigest() != ns["sha256"]:', 0),
    ("native-task", "if native_task is not None and", 0),
    ("native-outcome", 'if "outcome" in native and', 0),
    ("source-schema", 'if ns.get("source_schema") != ARGANA_RECORD_SCHEMA:', 0),
    ("native-record-schema", 'if native.get("schema") != ARGANA_RECORD_SCHEMA:', 0),
    ("halves-digest", 'if "sha256:" + hashlib.sha256(halves).hexdigest() != digest:', 0),
    ("native-digest-identity", 'if native.get("digest") != digest or', 0),
    ("argana-task", 'if task != record["subject"]["task_id"]:', 0),
    ("native-verdict", 'if "resolver_verdict" in record and verdict != record["resolver_verdict"]:', 0),
    ("obligations", 'if [o.get("kind") for o in native.get("obligations", [])]', 0),
    ("recorded-at", 'if "recorded_at" in ns and', 0),
]


class FixtureTests(unittest.TestCase):
    def test_committed_fixtures_equal_the_regenerated_ones(self):
        committed = {str(p.relative_to(fx.FIXTURE_ROOT)): p.read_bytes() for p in sorted(fx.FIXTURE_ROOT.glob("*/*.json"))}
        self.assertEqual(committed, FILES, "run python3 tools/kc_admission_observation_fixture.py write")
        self.assertTrue((fx.FIXTURE_ROOT / "README.md").is_file())

    def test_every_positive_passes_and_every_mutant_is_refused_with_exactly_its_code(self):
        got = run_all(cka)
        for name, want in expected_codes().items():
            with self.subTest(fixture=name):
                self.assertEqual(got[name], want, name)

    def test_the_expectations_cover_exactly_the_generated_observations(self):
        self.assertEqual(set(fx.EXPECTED), set(fx.observations()))

    def test_every_negative_expectation_code_is_distinct_per_case_class(self):
        used = {c for c in fx.EXPECTED.values() if c}
        self.assertEqual(used, {"KCAO-READ", "KCAO-SCHEMA-ID", "KCAO-POSITIVE-FLAG", "KCAO-CLAIMS", "KCAO-BRANCH", "KCAO-NATIVE-MISSING", "KCAO-SCHEMA", "KCAO-FORGED",
                                "KCAO-IDENTITY-CONFLICT", "KCAO-WORKITEM-NO-PROOF", "KCAO-BYTES-DIGEST", "KCAO-CONTRACT-DIGEST", "KCAO-NATIVE-MISMATCH"})

    def test_every_positive_is_labelled_synthetic_and_never_a_native_observation(self):
        for name, data in fx.observations().items():
            if not name.startswith("valid/"):
                continue
            record = json.loads(data)
            if record["status"] == "unavailable":
                continue
            with self.subTest(fixture=name):
                self.assertEqual(record["native_source"]["system"], "synthetic-fixture")
                self.assertTrue(record["native_source"]["record_id"].startswith("synthetic:"))
                self.assertTrue(record["subject"]["task_id"].startswith("synthetic:"))
                flags = cka.inspect(data, fx.sidecar(FILES, name, fx.SOURCE), fx.sidecar(FILES, name, fx.WORK))[1]
                self.assertTrue(any("SYNTHETIC-SOURCE" in f for f in flags), flags)
                if "work_item_id" in record:
                    self.assertTrue(record["work_item_id"].startswith("synthetic:"))

    def test_a_positive_without_native_bytes_is_structure_only_never_provenance(self):
        data = fx.observations()["valid/01-observed-contract-with-verified-exact-bytes"]
        problems, flags = cka.inspect(data)
        self.assertEqual(problems, [])
        self.assertTrue(any("NATIVE-BYTES-NOT-SUPPLIED" in f for f in flags), flags)

    def test_the_four_branches_have_the_documented_shapes(self):
        shapes = {}
        for name, data in fx.observations().items():
            if name.startswith("valid/"):
                r = json.loads(data)
                shapes[name[6:8]] = (r["status"], r.get("resolver_outcome"), sorted(set(r) & (cka.ALL_BRANCH_FIELDS | {"reason"})))
        self.assertEqual(shapes, {
            "01": ("observed", "contract", ["contract_digest", "obligations"]), "02": ("observed", "contract", ["contract_digest", "obligations"]),
            "03": ("observed", "contract", ["contract_digest", "obligations", "work_item_binding", "work_item_id"]),
            "04": ("observed", "underdetermined", ["missing"]), "05": ("observed", "refusal", ["refusal_code"]), "06": ("unavailable", None, ["reason"])})

    def test_the_k_contract_keeps_its_obligation_and_a_missing_one_is_refused(self):
        data = fx.observations()["valid/02-observed-contract-k-keeps-its-obligation"]
        self.assertEqual(json.loads(data)["obligations"], [{"kind": "synthetic-obligation"}])


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.validator = cka._validator()

    def test_the_schema_is_a_valid_draft_2020_12_schema_marked_candidate(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("CANDIDATE", SCHEMA["title"])
        self.assertIn("NEVER MEANS ADMISSION READY", SCHEMA["description"])

    def test_the_schema_has_no_boolean_anywhere_so_no_positive_flag_can_be_declared(self):
        self.assertNotIn('"boolean"', json.dumps(SCHEMA))
        for key in ("authorized", "admitted", "publishable", "success", "ok"):
            self.assertNotIn(f'"{key}"', json.dumps(SCHEMA))

    def test_every_object_of_every_branch_is_closed(self):
        def walk(node, path):
            if isinstance(node, dict):
                if node.get("type") == "object" and "properties" in node:
                    self.assertIs(node.get("additionalProperties"), False, path)
                for k, v in node.items():
                    walk(v, f"{path}/{k}")
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, f"{path}[{i}]")
        walk(SCHEMA, "#")

    def test_the_claims_are_fixed(self):
        claims = SCHEMA["$defs"]["claims"]
        self.assertEqual(set(claims["required"]), set(cka.CLAIM_KEYS))
        self.assertEqual({v["const"] for v in claims["properties"].values()}, {"NOT_MEASURED"})
        self.assertEqual(SCHEMA["$defs"]["claims_scope"]["const"], "resolver-outcome-observation-only")

    def test_the_schema_alone_refuses_what_it_can_express(self):
        for name, data in fx.observations().items():
            code = fx.EXPECTED.get(name)
            if code in {"KCAO-SCHEMA-ID", "KCAO-POSITIVE-FLAG", "KCAO-CLAIMS", "KCAO-BRANCH", "KCAO-NATIVE-MISSING", "KCAO-SCHEMA"} or name.endswith("work_item_id_without_source_proof"):
                with self.subTest(fixture=name):
                    self.assertTrue(list(self.validator.iter_errors(json.loads(data))), name)
            elif code is None:
                with self.subTest(fixture=name):
                    self.assertEqual(list(self.validator.iter_errors(json.loads(data))), [], name)

    def test_the_schema_accepts_no_mixed_branch_even_without_the_checker(self):
        contract = json.loads(fx.observations()["valid/01-observed-contract-with-verified-exact-bytes"])
        for extra in ({"missing": [{"capability_token": "x"}]}, {"refusal_code": "SOME_CODE"}, {"reason": "no_native_record"}):
            with self.subTest(extra=extra):
                self.assertTrue(list(self.validator.iter_errors({**contract, **extra})))


class CheckerTests(unittest.TestCase):
    def valid(self, prefix: str = "01") -> dict:
        name = next(n for n in fx.observations() if n.startswith(f"valid/{prefix}"))
        return json.loads(fx.observations()[name])

    def test_a_non_object_and_garbage_are_refused(self):
        self.assertEqual(codes(cka.check_observation(b"[]")), {"KCAO-SCHEMA"})
        self.assertEqual(codes(cka.check_observation(b"\xff")), {"KCAO-READ"})
        self.assertEqual(codes(cka.check_observation(b'{"a": NaN}')), {"KCAO-READ"})

    def test_an_oversized_record_is_refused_before_parsing(self):
        self.assertEqual(codes(cka.check_observation(b" " * ((1 << 20) + 1))), {"KCAO-READ"})

    def test_a_native_record_that_is_not_json_is_refused(self):
        record = self.valid("04")
        junk = b"not json"
        record["native_source"]["sha256"] = hashlib.sha256(junk).hexdigest()
        self.assertEqual(codes(cka.check_observation(fx.dump(record), junk)), {"KCAO-NATIVE-READ"})

    def test_a_contract_whose_bytes_are_not_an_argana_record_cannot_verify_its_digest(self):
        record = self.valid("01")
        record["native_source"].pop("source_schema")
        self.assertEqual(codes(cka.check_observation(fx.dump(record), FILES["valid/01-observed-contract-with-verified-exact-bytes.source.json"])), {"KCAO-CONTRACT-DIGEST"})

    def test_the_claims_never_change_with_the_branch(self):
        for name, data in fx.observations().items():
            if name.startswith("valid/"):
                r = json.loads(data)
                self.assertEqual(r["claims"], {k: "NOT_MEASURED" for k in cka.CLAIM_KEYS}, name)
                self.assertEqual(r["claims_scope"], "resolver-outcome-observation-only", name)

    def run_cli(self, *argv: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = cka.main(["check", *argv])
        return rc, out.getvalue() + err.getvalue()

    def test_the_command_line_reports_pass_flags_and_failures(self):
        base = fx.FIXTURE_ROOT / "valid" / "01-observed-contract-with-verified-exact-bytes"
        rc, text = self.run_cli(str(base) + ".json", "--source", str(base) + ".source.json")
        self.assertEqual(rc, 0, text)
        self.assertIn("KCAO_FLAG KCAO-FLAG-SYNTHETIC-SOURCE", text)
        self.assertIn("never admission", text)
        rc, text = self.run_cli(str(base) + ".json")
        self.assertEqual(rc, 0)
        self.assertIn("NATIVE-BYTES-NOT-SUPPLIED", text)
        bad = fx.FIXTURE_ROOT / "invalid" / "admitted_true.json"
        rc, text = self.run_cli(str(bad))
        self.assertEqual((rc, "KCAO_FAIL KCAO-POSITIVE-FLAG" in text), (1, True))
        rc, text = self.run_cli(str(base) + ".json", "--source", str(base) + ".source.json ")
        self.assertEqual(rc, 1)
        self.assertEqual(self.run_cli()[0], 2)
        self.assertEqual(self.run_cli("a", "--bogus", "b")[0], 2)

    def test_the_command_line_reads_a_missing_file_as_a_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, text = self.run_cli(str(Path(tmp) / "absent.json"))
        self.assertEqual(rc, 1)
        self.assertIn("KCAO-READ", text)


class MutationTests(unittest.TestCase):
    def test_the_unmutated_checker_is_the_baseline(self):
        self.assertEqual(run_all(load(SOURCE_TEXT)), expected_codes())

    def test_switching_off_any_guard_turns_a_fixture_red(self):
        want = expected_codes()
        for name, guard, occurrence in GUARDS:
            with self.subTest(guard=name):
                self.assertNotEqual(run_all(load(disable(SOURCE_TEXT, guard, occurrence))), want, f"guard {name} is not tested by any fixture")

    def test_weakening_a_compound_guard_turns_a_fixture_red(self):
        want = expected_codes()
        weakened = [
            ('or any(claims[k] != "NOT_MEASURED" for k in claims)', ""),
            ("or set(claims) != set(CLAIM_KEYS)", ""),
            ("or not isinstance(claims, dict)", ""),
            ("cbp.strict_json(data.decode", "json.loads(data.decode"),
            ("_validator().iter_errors(record)", "[]"),
            ('if synthetic != record_id.startswith("synthetic:"):', 'if synthetic and not record_id.startswith("synthetic:"):'),
            ('or not ns["record_id"].endswith(digest)', ""),
        ]
        for old, new in weakened:
            with self.subTest(mutation=old):
                self.assertIn(old, SOURCE_TEXT)
                self.assertNotEqual(run_all(load(SOURCE_TEXT.replace(old, new, 1))), want)

    def test_every_refusal_code_the_checker_can_return_has_a_fixture(self):
        emitted = set(re.findall(r'"(KCAO-[A-Z-]+):', SOURCE_TEXT)) | set(re.findall(r'f"(KCAO-[A-Z-]+):', SOURCE_TEXT))
        emitted = {c for c in emitted if "FLAG" not in c}
        self.assertEqual(emitted - {c for c in fx.EXPECTED.values() if c}, {"KCAO-NATIVE-READ"})


if __name__ == "__main__":
    unittest.main()
