# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""KCAdmissionObservation/v1 (CANDIDATE), repair after the KC-Brain (6711021786) and Agent-Brain (6711043209) reviews (KCLIVE-01).

The positive fixtures pass at the level `fixture-evidence`, every mutant is refused with exactly its code, the committed fixtures equal the regenerated ones, the schema alone
refuses what it can express, the claims stay NOT_MEASURED, structure-only and strict-evidence are different and distinguishable, a native source is compared with every emitted
fact, every JSON shape reaches a typed refusal, every read is bounded, KC-Brain's 16 CLI probes are reproduced, and switching off any guard of the checker turns a scenario red.

The checker under test is the one in this directory unless KCAO_CHECKER_DIR names another tools directory (used once to run these tests against the previous head 8b033d05 and record
which of them were red before the repair)."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import types
import unittest
from collections import namedtuple
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_kc_admission_observation as K  # noqa: E402  (the repository's checker: constants and expectations; CKA below is the checker UNDER TEST)
import kc_admission_observation_fixture as fx  # noqa: E402


def load_checker() -> types.ModuleType:
    where = os.environ.get("KCAO_CHECKER_DIR")
    if not where:
        return K
    path = Path(where) / "check_kc_admission_observation.py"
    spec = importlib.util.spec_from_file_location("kcao_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CKA = load_checker()
SCHEMA = json.loads(CKA.SCHEMA_PATH.read_text(encoding="utf-8"))
SOURCE_TEXT = Path(CKA.__file__).read_text(encoding="utf-8")
FILES = fx.variants()
EXPECT = fx.expected()
FIXTURE_ROOT = fx.FIXTURE_ROOT


class Outcome:
    """What a checker gave, whatever its API: the new Result, or the legacy (problems, flags) of 8b033d05 (level None)."""

    def __init__(self, problems, flags, level=None, unavailable=None, mode=None):
        self.problems, self.flags, self.level, self.unavailable, self.mode = list(problems), list(flags), level, unavailable, mode

    @property
    def codes(self) -> set[str]:
        return {p.split(":", 1)[0] for p in self.problems}


def strict(data, src=None, work=None, *, fixture=True, require=False, module=None) -> Outcome:
    m = module or CKA
    if hasattr(m, "check_strict"):
        r = m.check_strict(data, src, work, fixture=fixture, require_work_item=require)
        return Outcome(r.problems, r.flags, r.level, r.unavailable, r.mode)
    problems, flags = m.inspect(data, src, work)
    return Outcome(problems, flags)


def structure(data, *, fixture=True, require=False, module=None) -> Outcome:
    m = module or CKA
    if hasattr(m, "check_structure"):
        r = m.check_structure(data, fixture=fixture, require_work_item=require)
        return Outcome(r.problems, r.flags, r.level, r.unavailable, r.mode)
    problems, flags = m.inspect(data)
    return Outcome(problems, flags)


def sc(name: str, suffix: str):
    return fx.sidecar(FILES, name, suffix)


def codes_of(out: Outcome) -> set[str]:
    return out.codes


def dumpb(x) -> bytes:
    return fx.dump(x)


def rehash(obs: dict, src: bytes | None = None, work: bytes | None = None) -> dict:
    if src is not None:
        obs["native_source"]["sha256"] = fx.sha(src)
    if work is not None:
        obs["work_item_binding"]["sha256"] = fx.sha(work)
    return obs


def case_of(name: str) -> dict:
    """A deep copy of one valid case as {obs: dict, source: bytes|None, work: bytes|None}."""
    case = copy.deepcopy(next(v for k, v in fx.build().items() if k.startswith(name)))
    return case


def make_real(case: dict) -> dict:
    """The same synthetic bytes under the REAL source label argana-contract-store (non-fixture mode). Used only by tests; the bytes remain synthetic."""
    ns = case["obs"]["native_source"]
    ns["system"] = K.ARGANA_SYSTEM
    ns["record_id"] = ns["record_id"].removeprefix("synthetic:")
    return case


def edit_source(case: dict, edit) -> dict:
    parsed = json.loads(case["source"])
    edit(parsed)
    case["source"] = dumpb(parsed)
    rehash(case["obs"], src=case["source"])
    return case


Scenario = namedtuple("Scenario", "id mode fixture require obs src work codes level reason flags", defaults=(None,))


def run_scenario(module: types.ModuleType, s: Scenario):
    check = module.check_structure(s.obs, fixture=s.fixture, require_work_item=s.require) if s.mode == "structure-only" else \
        module.check_strict(s.obs, s.src, s.work, fixture=s.fixture, require_work_item=s.require)
    return check.codes, check.level, (check.unavailable or {}).get("reason"), frozenset(f.split(":", 1)[0] for f in check.flags)


# ------------------------------------------------------------------ the expected result of every scenario is DECLARED here, never read back from the checker

PRE_EVIDENCE_CODES = {"KCAO-READ", "KCAO-SCHEMA", "KCAO-SCHEMA-ID", "KCAO-POSITIVE-FLAG", "KCAO-CLAIMS", "KCAO-BRANCH", "KCAO-NATIVE-MISSING"}
# mutants refused by a structural/policy rule without any native bytes (besides the PRE_EVIDENCE_CODES ones)
STRUCTURE_REFUSED = {
    "invalid/work_item_id_without_source_proof", "invalid/forged_record_path_as_record_id", "invalid/forged_issuer_unknown_source_system",
    "invalid/synthetic_system_without_the_synthetic_prefix", "invalid/native_system_with_the_synthetic_prefix", "invalid/unknown_work_item_source",
    "invalid/work_item_binding_with_a_muneral_system",
}


def structure_expectation(name: str):
    code = EXPECT[name]
    if code is None:
        return set(), K.LEVEL_UNAVAILABLE_RECORD if "unavailable" in name else K.LEVEL_STRUCTURE
    if code in PRE_EVIDENCE_CODES or name in STRUCTURE_REFUSED:
        return {code}, K.LEVEL_REFUSED
    return set(), K.LEVEL_UNAVAILABLE_RECORD if "unavailable" in name else K.LEVEL_STRUCTURE


def strict_expectation(name: str):
    code = EXPECT[name]
    if code is not None:
        return {code}, K.LEVEL_REFUSED
    return set(), K.LEVEL_UNAVAILABLE_RECORD if "unavailable" in name else K.LEVEL_FIXTURE


def build_scenarios() -> list[Scenario]:
    out: list[Scenario] = []
    obs_files = fx.observations()
    for name, data in obs_files.items():
        out.append(Scenario(f"strict-fixture:{name}", "strict-evidence", True, False, data, sc(name, fx.SOURCE), sc(name, fx.WORK), *strict_expectation(name), None))
    for name, data in obs_files.items():
        codes, level = structure_expectation(name)
        out.append(Scenario(f"structure-fixture:{name}", "structure-only", True, False, data, None, None, codes, level, None))

    def add(i, mode, fixture, require, case, codes, level, reason=None, with_sidecars=True, flags=None):
        out.append(Scenario(i, mode, fixture, require, dumpb(case["obs"]), case.get("source") if with_sidecars else None, case.get("work") if with_sidecars else None, codes, level, reason,
                            None if flags is None else frozenset(flags)))

    # the real source label in the live (non-fixture) mode: synthetic bytes, so this proves the checker's rules and nothing about Argana
    c1 = make_real(case_of("01"))
    add("real:contract-strict", "strict-evidence", False, False, c1, set(), K.LEVEL_NATIVE, flags={"KCAO-FLAG-MUTABLE-LOCATOR"})
    add("real:contract-structure", "structure-only", False, False, c1, set(), K.LEVEL_STRUCTURE, flags={"KCAO-FLAG-STRUCTURE-ONLY"})
    add("flags:fixture-contract-strict", "strict-evidence", True, False, case_of("01"), set(), K.LEVEL_FIXTURE, flags={"KCAO-FLAG-SYNTHETIC-SOURCE", "KCAO-FLAG-MUTABLE-LOCATOR"})
    add("flags:fixture-decision-strict", "strict-evidence", True, False, case_of("04"), set(), K.LEVEL_FIXTURE, flags={"KCAO-FLAG-SYNTHETIC-SOURCE"})
    add("flags:fixture-work-item-strict", "strict-evidence", True, False, case_of("03"), set(), K.LEVEL_FIXTURE,
        flags={"KCAO-FLAG-SYNTHETIC-SOURCE", "KCAO-FLAG-SYNTHETIC-WORK-ITEM", "KCAO-FLAG-MUTABLE-LOCATOR"})
    add("flags:fixture-work-item-structure", "structure-only", True, False, case_of("03"), set(), K.LEVEL_STRUCTURE,
        flags={"KCAO-FLAG-SYNTHETIC-SOURCE", "KCAO-FLAG-SYNTHETIC-WORK-ITEM", "KCAO-FLAG-STRUCTURE-ONLY", "KCAO-FLAG-WORK-ITEM-BYTES-NOT-SUPPLIED"})
    add("flags:fixture-decision-structure", "structure-only", True, False, case_of("04"), set(), K.LEVEL_STRUCTURE, flags={"KCAO-FLAG-SYNTHETIC-SOURCE", "KCAO-FLAG-STRUCTURE-ONLY"})
    add("flags:unavailable-record-has-no-flags", "strict-evidence", True, False, case_of("06"), set(), K.LEVEL_UNAVAILABLE_RECORD, flags=set(), with_sidecars=False)
    add("flags:required-binding-flag", "strict-evidence", True, True, case_of("01"), set(), K.LEVEL_UNAVAILABLE, "native_binding_unverified",
        flags={"KCAO-FLAG-SYNTHETIC-SOURCE", "KCAO-FLAG-MUTABLE-LOCATOR", "KCAO-FLAG-BINDING-REQUIRED"})
    add("real:contract-k-strict", "strict-evidence", False, False, make_real(case_of("02")), set(), K.LEVEL_NATIVE)
    add("real:contract-in-fixture-mode-is-fixture-evidence", "strict-evidence", True, False, c1, set(), K.LEVEL_FIXTURE)
    add("real:strict-without-bytes", "strict-evidence", False, False, c1, {"KCAO-STRICT-NO-NATIVE-BYTES"}, K.LEVEL_REFUSED, with_sidecars=False)
    relabel = make_real(case_of("01"))
    relabel["obs"].update({"resolver_outcome": "refusal", "refusal_code": "SOME_REFUSAL"})
    relabel["obs"].pop("contract_digest"), relabel["obs"].pop("obligations")
    add("real:contract-bytes-relabelled-refusal", "strict-evidence", False, False, relabel, {"KCAO-NATIVE-MISMATCH"}, K.LEVEL_REFUSED)
    relabel = make_real(case_of("01"))
    relabel["obs"].update({"resolver_outcome": "underdetermined", "missing": [{"capability_token": "x"}]})
    relabel["obs"].pop("contract_digest"), relabel["obs"].pop("obligations")
    add("real:contract-bytes-relabelled-underdetermined", "strict-evidence", False, False, relabel, {"KCAO-NATIVE-MISMATCH"}, K.LEVEL_REFUSED)
    add("real:decision-profile-has-no-live-source", "strict-evidence", False, False, make_real(case_of("04")), {"KCAO-NATIVE-PROFILE"}, K.LEVEL_REFUSED)
    for tag, edit, code in (
        ("extra-obligation-field", lambda n: n.update({"obligations": [{"kind": "k", "ref": "r"}]}), "KCAO-NATIVE-UNSUPPORTED-SHAPE"),
        ("request-is-an-array", lambda n: n.update({"request": ["x"]}), "KCAO-NATIVE-INVALID"),
        ("task-differs", lambda n: n["request"].update({"task_id": "synthetic:other"}), "KCAO-NATIVE-MISMATCH"),
    ):
        add(f"real:{tag}", "strict-evidence", False, False, edit_source(make_real(case_of("01")), edit), {code}, K.LEVEL_REFUSED)
    omitted = make_real(case_of("02"))
    omitted["obs"].pop("resolver_verdict")
    add("real:native-verdict-omitted", "strict-evidence", False, False, omitted, {"KCAO-NATIVE-MISMATCH"}, K.LEVEL_REFUSED)
    # the work item binding has no approved native profile: the live path omits it
    w3 = make_real(case_of("03"))
    add("real:synthetic-work-item-binding-strict", "strict-evidence", False, False, w3, {"KCAO-SYNTHETIC-NOT-FIXTURE"}, K.LEVEL_REFUSED)
    add("real:synthetic-work-item-binding-structure", "structure-only", False, False, w3, {"KCAO-SYNTHETIC-NOT-FIXTURE"}, K.LEVEL_REFUSED)
    w3m = make_real(case_of("03"))
    w3m["obs"]["work_item_binding"]["system"] = "muneral"
    add("real:muneral-binding-strict", "strict-evidence", False, False, w3m, {"KCAO-WORKITEM-NO-PROFILE"}, K.LEVEL_REFUSED)
    add("real:muneral-binding-structure", "structure-only", False, False, w3m, {"KCAO-WORKITEM-NO-PROFILE"}, K.LEVEL_REFUSED)
    w3f = make_real(case_of("03"))
    add("real:synthetic-binding-on-a-real-source-in-fixture-mode", "strict-evidence", True, False, w3f, {"KCAO-FORGED"}, K.LEVEL_REFUSED)
    # a consumer that requires the binding
    add("require:live-record-without-binding-strict", "strict-evidence", False, True, c1, set(), K.LEVEL_UNAVAILABLE, "native_binding_unverified")
    add("require:live-record-without-binding-structure", "structure-only", False, True, c1, set(), K.LEVEL_UNAVAILABLE, "native_binding_unverified")
    add("require:fixture-with-verified-binding", "strict-evidence", True, True, case_of("03"), set(), K.LEVEL_FIXTURE)
    add("require:fixture-with-binding-in-structure-mode-is-unverified", "structure-only", True, True, case_of("03"), set(), K.LEVEL_UNAVAILABLE, "native_binding_unverified")
    add("require:fixture-without-binding", "strict-evidence", True, True, case_of("01"), set(), K.LEVEL_UNAVAILABLE, "native_binding_unverified")
    add("require:fixture-with-a-wrong-binding-is-a-refusal", "strict-evidence", True, True, dict(case_of("03"), work=b"not json"), {"KCAO-BYTES-DIGEST"}, K.LEVEL_REFUSED)
    add("require:an-unavailable-record", "strict-evidence", True, True, case_of("06"), set(), K.LEVEL_UNAVAILABLE_RECORD, "outcome_not_persisted", with_sidecars=False)
    # synthetic labels are valid only in fixture mode, in both modes
    for n in ("01", "03", "04", "05", "08"):
        add(f"no-fixture-mode:{n}-strict", "strict-evidence", False, False, case_of(n), {"KCAO-SYNTHETIC-NOT-FIXTURE"}, K.LEVEL_REFUSED)
        add(f"no-fixture-mode:{n}-structure", "structure-only", False, False, case_of(n), {"KCAO-SYNTHETIC-NOT-FIXTURE"}, K.LEVEL_REFUSED)
    # strict-evidence without the native bytes is never a pass
    for n in ("01", "02", "03", "04", "05", "08"):
        add(f"strict-without-bytes:{n}", "strict-evidence", True, False, case_of(n), {"KCAO-STRICT-NO-NATIVE-BYTES"}, K.LEVEL_REFUSED, with_sidecars=False)
    # bounded and non-bytes inputs
    big = b" " * (CKA.MAX_BYTES + 1)
    out.append(Scenario("bounds:observation-too-large", "structure-only", True, False, big, None, None, {"KCAO-READ"}, K.LEVEL_REFUSED, None))
    out.append(Scenario("bounds:observation-is-not-bytes", "structure-only", True, False, "text", None, None, {"KCAO-READ"}, K.LEVEL_REFUSED, None))
    out.append(Scenario("bounds:observation-nests-too-deeply", "structure-only", True, False, b"[" * 200000, None, None, {"KCAO-READ"}, K.LEVEL_REFUSED, None))
    s4 = case_of("04")
    out.append(Scenario("bounds:native-too-large", "strict-evidence", True, False, dumpb(s4["obs"]), big, None, {"KCAO-NATIVE-READ"}, K.LEVEL_REFUSED, None))
    out.append(Scenario("bounds:native-is-not-bytes", "strict-evidence", True, False, dumpb(s4["obs"]), "text", None, {"KCAO-NATIVE-READ"}, K.LEVEL_REFUSED, None))
    deep = b"[" * 200000
    out.append(Scenario("bounds:native-nests-too-deeply", "strict-evidence", True, False, dumpb(rehash(s4["obs"], src=deep)), deep, None, {"KCAO-NATIVE-READ"}, K.LEVEL_REFUSED, None))
    s3 = case_of("03")
    out.append(Scenario("bounds:work-item-too-large", "strict-evidence", True, False, dumpb(s3["obs"]), s3["source"], big, {"KCAO-WORKITEM-INVALID"}, K.LEVEL_REFUSED, None))
    out.append(Scenario("bounds:work-item-nests-too-deeply", "strict-evidence", True, False, dumpb(rehash(s3["obs"], work=deep)), s3["source"], deep, {"KCAO-WORKITEM-INVALID"}, K.LEVEL_REFUSED, None))
    return out


SCENARIOS = build_scenarios()


def same(s: Scenario, result: tuple) -> bool:
    return result[:3] == (s.codes, s.level, s.reason) and (s.flags is None or result[3] == s.flags)


def run_all(module: types.ModuleType, stop_at_first: bool = False) -> dict[str, tuple]:
    """scenario id -> (codes, level, reason); a crash outside the checker's own guard is a distinct CRASH marker, never a pass. With stop_at_first only the first deviation is returned."""
    got: dict[str, tuple] = {}
    for s in SCENARIOS:
        try:
            result = run_scenario(module, s)
        except Exception as exc:  # noqa: BLE001
            result = ({f"CRASH-{exc.__class__.__name__}"}, None, None, frozenset())
        got[s.id] = result
        if stop_at_first and not same(s, result):
            break
    return got


def deviations(module: types.ModuleType, stop_at_first: bool = True) -> dict[str, tuple]:
    by_id = {s.id: s for s in SCENARIOS}
    return {k: v for k, v in run_all(module, stop_at_first).items() if not same(by_id[k], v)}


# ------------------------------------------------------------------ the review findings, by fixture name

FINDINGS = {
    "R-KCAO1": [  # the native branch is validated against a supported profile and EVERY emitted fact is compared
        "same_contract_labelled_as_a_refusal", "same_contract_labelled_as_underdetermined", "empty_native_object_for_an_underdetermined", "native_decision_with_only_its_schema",
        "native_decision_without_an_outcome", "native_decision_without_a_task_id", "native_refusal_without_its_code", "native_underdetermined_without_missing",
        "refusal_code_differs_from_the_native_code", "missing_differs_from_the_native_payload", "missing_drops_a_native_entry", "underdetermined_verdict_differs_from_the_native_verdict",
        "underdetermined_omits_the_native_verdict", "contract_omits_the_native_verdict", "verdict_emitted_but_the_native_record_has_none", "contract_verdict_differs_from_the_native_record",
        "recorded_at_emitted_but_the_native_record_has_none", "decision_recorded_at_differs_from_the_native_time", "recorded_at_differs_from_the_native_record",
        "source_schema_absent_on_a_decision", "source_schema_absent_on_a_contract", "source_schema_is_an_unsupported_version", "decision_profile_cannot_carry_a_contract",
        "outcome_differs_from_the_native_record", "task_differs_from_the_native_record", "record_id_does_not_name_the_contract", "obligations_differ_from_the_native_record",
        "native_has_an_obligation_the_observation_omits"],
    "R-KCAO2": [  # the work item bytes are parsed and joined; the live path omits the binding
        "work_item_bytes_are_not_json", "work_item_bytes_are_an_unrelated_object", "work_item_bytes_are_an_array", "work_item_record_names_another_work_item",
        "work_item_record_names_another_contract", "work_item_record_names_another_work_item_and_contract", "work_item_record_names_another_task", "work_item_record_joins_another_intake",
        "work_item_record_is_not_the_named_evidence", "work_item_binding_names_another_record", "work_item_binding_equal_to_the_work_item_id_is_not_the_evidence",
        "work_item_sidecar_is_missing", "work_item_record_has_another_schema", "work_item_record_has_an_extra_field", "work_item_binding_with_a_muneral_system"],
    "R-KCAO3": [  # every JSON shape reaches a typed refusal
        "resolver_outcome_is_an_array", "resolver_outcome_is_an_object", "resolver_outcome_is_a_string", "resolver_outcome_is_a_number", "resolver_outcome_is_null",
        "native_request_is_an_array", "native_request_is_a_string", "native_request_is_null", "native_request_is_a_number", "native_request_is_missing",
        "native_kc2_is_an_array", "native_kc2_is_a_string", "native_kc2_is_null", "native_kc2_is_a_number",
        "native_obligations_is_null", "native_obligations_is_an_object", "native_obligations_is_a_string", "native_obligation_item_is_null", "native_obligation_item_is_a_number",
        "native_obligation_item_is_a_string", "native_obligation_item_is_an_array", "native_obligation_without_a_kind", "native_obligation_kind_is_not_a_string",
        "native_bytes_are_an_array", "native_bytes_are_null", "native_bytes_are_a_number", "native_bytes_are_a_string", "native_bytes_are_not_json", "native_bytes_are_a_lone_surrogate",
        "observation_is_an_array", "observation_is_null", "observation_is_a_number", "observation_is_a_string", "claims_is_an_array", "subject_is_a_string", "native_source_is_an_array",
        "obligations_is_a_string", "canonical_object_is_missing", "canonical_is_a_string", "canonical_half_is_not_base64", "canonical_half_is_a_number"],
    "contract-halves": [  # strictly parsed, canonical, in agreement with contract_digest
        "canonical_halves_are_not_json", "canonical_body_is_not_in_canonical_form", "canonical_body_is_a_json_array", "canonical_body_holds_a_float", "canonical_body_repeats_a_member",
        "canonical_manifest_is_a_number", "canonical_body_is_not_utf8", "contract_digest_is_not_the_digest_of_the_halves"],
    "B5-unknown-condition-fields": [
        "native_obligation_carries_an_extra_condition_field", "native_missing_item_carries_an_extra_condition_field", "native_decision_carries_an_unprojected_field"],
}

# KC-Brain comment A: the sixteen isolated CLI probes -> (probe id, what it was, fixture name, expected exit code, expected output token)
PROBES = [
    ("P01", "positive control: observed contract with verified exact bytes", "valid/01-observed-contract-with-verified-exact-bytes", 0, "KCAO_PASS_FIXTURE_EVIDENCE"),
    ("P02", "positive control: contract with an evidenced work item", "valid/03-observed-contract-with-evidenced-work-item", 0, "KCAO_PASS_FIXTURE_EVIDENCE"),
    ("P03", "control: wrong native hash", "invalid/native_bytes_do_not_match_the_digest", 1, "KCAO-BYTES-DIGEST"),
    ("P04", "control: positive flag", "invalid/admitted_true", 1, "KCAO-POSITIVE-FLAG"),
    ("P05", "control: mixed branch", "invalid/contract_digest_on_a_refusal", 1, "KCAO-BRANCH"),
    ("P06", "underdetermined backed by exact bytes {} with the hash recomputed", "invalid/empty_native_object_for_an_underdetermined", 1, "KCAO-FORGED"),
    ("P07", "refusal says OTHER_REFUSAL, the native record says another code", "invalid/refusal_code_differs_from_the_native_code", 1, "KCAO-NATIVE-MISMATCH"),
    ("P08", "underdetermined observation changes the missing capability", "invalid/missing_differs_from_the_native_payload", 1, "KCAO-NATIVE-MISMATCH"),
    ("P09", "underdetermined verdict T, native verdict U", "invalid/underdetermined_verdict_differs_from_the_native_verdict", 1, "KCAO-NATIVE-MISMATCH"),
    ("P10", "work_item_binding hash matches bytes `not a JSON record`", "invalid/work_item_bytes_are_not_json", 1, "KCAO-WORKITEM-INVALID"),
    ("P11", "work-item source names another id and another contract, binding hash recomputed", "invalid/work_item_record_names_another_work_item_and_contract", 1, "KCAO-WORKITEM-MISMATCH"),
    ("P12", "canonical body bytes NOT JSON, manifest empty, all digests recomputed", "invalid/canonical_halves_are_not_json", 1, "KCAO-NATIVE-INVALID"),
    ("P13", "native contract verdict K retained, observation omits resolver_verdict", "invalid/contract_omits_the_native_verdict", 1, "KCAO-NATIVE-MISMATCH"),
    ("P14", "resolver_outcome is an array (was an untyped TypeError)", "invalid/resolver_outcome_is_an_array", 1, "KCAO-SCHEMA"),
    ("P15", "native.request is a nonempty array (was an untyped AttributeError)", "invalid/native_request_is_an_array", 1, "KCAO-NATIVE-INVALID"),
]


def run_cli(*argv: str, module=None) -> tuple[int, str]:
    m = module or CKA
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = m.main(["check", *argv])
    return rc, out.getvalue() + err.getvalue()


def cli_probe(name: str, structure_only: bool = False, module=None) -> tuple[int, str]:
    """One isolated CLI probe of a fixture, written to files the way KC-Brain ran them."""
    m = module or CKA
    with tempfile.TemporaryDirectory() as tmp:
        obs = Path(tmp) / "obs.json"
        obs.write_bytes(FILES[f"{name}.json"])
        args = [str(obs)]
        src, work = FILES.get(f"{name}{fx.SOURCE}"), FILES.get(f"{name}{fx.WORK}")
        if hasattr(m, "check_strict"):
            args = ["--mode", "structure-only" if structure_only else "strict-evidence", "--fixture", *args]
        if not structure_only:
            if src is not None:
                (Path(tmp) / "src.json").write_bytes(src)
                args += ["--source", str(Path(tmp) / "src.json")]
            if work is not None:
                (Path(tmp) / "work.json").write_bytes(work)
                args += ["--work-item", str(Path(tmp) / "work.json")]
        return run_cli(*args, module=m)


# ================================================================== tests

class FixtureTests(unittest.TestCase):
    def test_committed_fixtures_equal_the_regenerated_ones(self):
        committed = {str(p.relative_to(FIXTURE_ROOT)): p.read_bytes() for p in sorted(FIXTURE_ROOT.glob("*/*.json"))}
        self.assertEqual(committed, FILES, "run python3 tools/kc_admission_observation_fixture.py write")
        self.assertEqual((FIXTURE_ROOT / "README.md").read_text(encoding="utf-8"), fx.README)

    def test_every_positive_passes_and_every_mutant_is_refused_with_exactly_its_code(self):
        for name, data in fx.observations().items():
            with self.subTest(fixture=name):
                got = strict(data, sc(name, fx.SOURCE), sc(name, fx.WORK))
                want = EXPECT[name]
                self.assertEqual(got.codes, set() if want is None else {want}, (name, got.problems))

    def test_the_expectations_cover_exactly_the_generated_observations(self):
        self.assertEqual(set(EXPECT), set(fx.observations()))

    def test_every_refusal_code_class_is_exercised(self):
        used = {c for c in EXPECT.values() if c}
        self.assertEqual(used, {"KCAO-READ", "KCAO-SCHEMA-ID", "KCAO-POSITIVE-FLAG", "KCAO-CLAIMS", "KCAO-BRANCH", "KCAO-NATIVE-MISSING", "KCAO-SCHEMA", "KCAO-FORGED",
                                "KCAO-WORKITEM-NO-PROOF", "KCAO-WORKITEM-NO-PROFILE", "KCAO-WORKITEM-INVALID", "KCAO-WORKITEM-MISMATCH", "KCAO-BYTES-DIGEST", "KCAO-CONTRACT-DIGEST",
                                "KCAO-NATIVE-MISMATCH", "KCAO-NATIVE-INVALID", "KCAO-NATIVE-UNSUPPORTED-SHAPE", "KCAO-NATIVE-PROFILE", "KCAO-NATIVE-READ"})

    def test_the_identity_conflict_code_is_gone_with_message_id(self):
        self.assertNotIn("KCAO-IDENTITY-CONFLICT", SOURCE_TEXT)
        self.assertNotIn("message_id", SOURCE_TEXT)
        for path, data in FILES.items():
            if "message_id_is_not_a_field" not in path:
                self.assertNotIn(b"message_id", data, path)

    def test_every_positive_is_labelled_synthetic_and_is_fixture_evidence_never_native(self):
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
                out = strict(data, sc(name, fx.SOURCE), sc(name, fx.WORK))
                self.assertEqual(out.level, K.LEVEL_FIXTURE)
                self.assertNotEqual(out.level, K.LEVEL_NATIVE)
                self.assertTrue(any("SYNTHETIC-SOURCE" in f for f in out.flags), out.flags)
                if "work_item_id" in record:
                    self.assertTrue(record["work_item_id"].startswith("synthetic:"))

    def test_the_branches_have_the_documented_shapes(self):
        shapes = {}
        for name, data in fx.observations().items():
            if name.startswith("valid/"):
                r = json.loads(data)
                shapes[name[6:8]] = (r["status"], r.get("resolver_outcome"), r.get("resolver_verdict"), sorted(set(r) & (CKA.ALL_BRANCH_FIELDS | {"reason"} | ({"subject"} if r["status"] == "unavailable" else set()))))
        self.assertEqual(shapes, {
            "01": ("observed", "contract", "T", ["contract_digest", "obligations"]), "02": ("observed", "contract", "K", ["contract_digest", "obligations"]),
            "03": ("observed", "contract", "T", ["contract_digest", "obligations", "work_item_binding", "work_item_id"]),
            "04": ("observed", "underdetermined", "U", ["missing"]), "05": ("observed", "refusal", "F", ["refusal_code"]),
            "06": ("unavailable", None, None, ["reason"]), "07": ("unavailable", None, None, ["reason", "subject"]),
            "08": ("observed", "refusal", None, ["refusal_code"])})

    def test_the_k_contract_keeps_its_obligation_and_a_recorded_verdict_is_projected(self):
        self.assertEqual(json.loads(fx.observations()["valid/02-observed-contract-k-keeps-its-obligation"])["obligations"], [{"kind": "synthetic-obligation"}])
        for name in ("valid/01-observed-contract-with-verified-exact-bytes", "valid/03-observed-contract-with-evidenced-work-item"):
            self.assertEqual(json.loads(fx.observations()[name])["resolver_verdict"], "T")

    def test_the_evidence_record_id_of_the_work_item_is_not_the_task_id(self):
        record = json.loads(fx.observations()["valid/03-observed-contract-with-evidenced-work-item"])
        self.assertNotEqual(record["work_item_binding"]["record_id"], record["subject"]["task_id"])
        self.assertNotEqual(record["work_item_binding"]["record_id"], record["work_item_id"])

    def test_each_mutant_reaches_its_comparison_not_an_earlier_digest_guard(self):
        stale = {"invalid/native_bytes_do_not_match_the_digest", "invalid/work_item_bytes_do_not_match_the_digest", "invalid/sha256_with_a_trailing_newline"}
        for name, data in fx.observations().items():
            if not name.startswith("invalid/") or name in stale:
                continue
            record = json.loads(data) if data[:1] == b"{" else None
            if not record or "native_source" not in record or not isinstance(record.get("native_source"), dict) or sc(name, fx.SOURCE) is None:
                continue
            with self.subTest(fixture=name):
                self.assertEqual(record["native_source"].get("sha256"), fx.sha(sc(name, fx.SOURCE)), "the native hash must be recomputed")
                if sc(name, fx.WORK) is not None and "work_item_binding" in record:
                    self.assertEqual(record["work_item_binding"]["sha256"], fx.sha(sc(name, fx.WORK)), "the work item hash must be recomputed")
                self.assertNotEqual(EXPECT[name], "KCAO-BYTES-DIGEST")


class FindingTests(unittest.TestCase):
    """Each review finding is a list of fixtures; every one must exist and be refused with its declared code (these are the red-before cases)."""

    def check_finding(self, key: str):
        for short in FINDINGS[key]:
            name = f"invalid/{short}"
            with self.subTest(finding=key, case=short):
                self.assertIn(name, EXPECT)
                out = strict(fx.observations()[name], sc(name, fx.SOURCE), sc(name, fx.WORK))
                self.assertEqual(out.codes, {EXPECT[name]}, out.problems)
                self.assertNotIn("KCAO-INTERNAL", out.codes)

    def test_R_KCAO1_native_branch_is_compared_with_every_emitted_fact(self):
        self.check_finding("R-KCAO1")

    def test_R_KCAO2_work_item_bytes_are_parsed_and_joined(self):
        self.check_finding("R-KCAO2")

    def test_R_KCAO3_every_json_shape_reaches_a_typed_refusal(self):
        self.check_finding("R-KCAO3")

    def test_contract_halves_are_strictly_parsed_canonical_and_agree_with_the_digest(self):
        self.check_finding("contract-halves")

    def test_B5_unknown_extra_condition_fields_are_unsupported_never_dropped(self):
        self.check_finding("B5-unknown-condition-fields")

    def test_the_findings_name_only_existing_fixtures(self):
        for key, names in FINDINGS.items():
            for short in names:
                self.assertIn(f"invalid/{short}", EXPECT, (key, short))


class ProbeTests(unittest.TestCase):
    """KC-Brain's sixteen isolated CLI probes (comment A), reproduced as deterministic tests."""

    def test_probes_01_to_15_through_the_command_line(self):
        for pid, what, name, rc_want, token in PROBES:
            with self.subTest(probe=pid, what=what):
                rc, text = cli_probe(name)
                self.assertNotIn("Traceback", text)
                self.assertEqual(rc, rc_want, text)
                self.assertIn(token, text)

    def test_probe_16_structure_only_without_a_source_passes_only_as_structure(self):
        rc, text = cli_probe("valid/01-observed-contract-with-verified-exact-bytes", structure_only=True)
        self.assertEqual(rc, 0, text)
        self.assertIn("KCAO_PASS_STRUCTURE_ONLY", text)
        self.assertIn("KCAO-FLAG-STRUCTURE-ONLY", text)
        self.assertNotIn("FIXTURE_EVIDENCE", text)
        self.assertNotIn("NATIVE_CONTENT_AGREEMENT", text)

    def test_the_sixteen_probes_are_all_accounted_for(self):
        self.assertEqual([p[0] for p in PROBES] + ["P16"], [f"P{i:02d}" for i in range(1, 17)])


class ModeTests(unittest.TestCase):
    """Section C: structure-only and strict-evidence are separate entry points, distinguishable in the output; nothing drops the flags."""

    def test_there_is_no_helper_that_drops_the_mode_or_the_flags(self):
        self.assertFalse(hasattr(CKA, "check_observation"))
        self.assertFalse(hasattr(CKA, "inspect"))
        self.assertTrue(hasattr(CKA, "check_structure") and hasattr(CKA, "check_strict"))

    def test_structure_only_names_its_mode_and_level_and_never_reads_native_bytes(self):
        name = "valid/01-observed-contract-with-verified-exact-bytes"
        r = CKA.check_structure(fx.observations()[name], fixture=True)
        self.assertEqual((r.mode, r.level, r.problems), ("structure-only", "structure-only", ()))
        self.assertTrue(any(f.startswith("KCAO-FLAG-STRUCTURE-ONLY") for f in r.flags))
        self.assertTrue(r.passed)
        self.assertNotIn(r.level, (K.LEVEL_FIXTURE, K.LEVEL_NATIVE))

    def test_structure_only_passes_a_record_whose_evidence_is_wrong_so_its_pass_is_not_provenance(self):
        wrong = "invalid/underdetermined_verdict_differs_from_the_native_verdict"
        self.assertEqual(structure(fx.observations()[wrong]).level, "structure-only")
        self.assertEqual(strict(fx.observations()[wrong], sc(wrong, fx.SOURCE)).codes, {"KCAO-NATIVE-MISMATCH"})

    def test_strict_without_native_bytes_is_a_typed_refusal_never_a_pass(self):
        for name, data in fx.observations().items():
            if name.startswith("valid/") and json.loads(data)["status"] == "observed":
                with self.subTest(fixture=name):
                    out = strict(data, None, None)
                    self.assertEqual(out.codes, {"KCAO-STRICT-NO-NATIVE-BYTES"})
                    self.assertEqual(out.level, K.LEVEL_REFUSED)

    def test_a_synthetic_result_is_never_promoted_to_a_native_pass(self):
        name = "valid/01-observed-contract-with-verified-exact-bytes"
        self.assertEqual(strict(fx.observations()[name], sc(name, fx.SOURCE)).level, K.LEVEL_FIXTURE)
        self.assertEqual(strict(fx.observations()[name], sc(name, fx.SOURCE), fixture=False).codes, {"KCAO-SYNTHETIC-NOT-FIXTURE"})
        self.assertEqual(structure(fx.observations()[name], fixture=False).codes, {"KCAO-SYNTHETIC-NOT-FIXTURE"})

    def test_the_native_level_needs_a_non_fixture_supported_profile_and_still_flags_the_mutable_locator(self):
        case = make_real(case_of("01"))
        out = strict(dumpb(case["obs"]), case["source"], fixture=False)
        self.assertEqual((out.codes, out.level), (set(), K.LEVEL_NATIVE))
        self.assertTrue(any(f.startswith("KCAO-FLAG-MUTABLE-LOCATOR") for f in out.flags), out.flags)
        self.assertFalse(any("SYNTHETIC" in f for f in out.flags))

    def test_the_command_line_prints_the_level_and_requires_a_mode(self):
        base = FIXTURE_ROOT / "valid" / "01-observed-contract-with-verified-exact-bytes"
        rc, text = run_cli("--mode", "strict-evidence", "--fixture", str(base) + ".json", "--source", str(base) + ".source.json")
        self.assertEqual(rc, 0, text)
        self.assertIn("KCAO_MODE strict-evidence LEVEL fixture-evidence", text)
        self.assertIn("KCAO_FLAG KCAO-FLAG-SYNTHETIC-SOURCE", text)
        rc, text = run_cli("--mode", "structure-only", "--fixture", str(base) + ".json")
        self.assertIn("KCAO_MODE structure-only LEVEL structure-only", text)
        self.assertEqual(run_cli(str(base) + ".json")[0], 2)  # no mode
        self.assertEqual(run_cli("--mode", "bogus", str(base) + ".json")[0], 2)
        self.assertEqual(run_cli("--mode", "structure-only", "--fixture", str(base) + ".json", "--source", str(base) + ".source.json")[0], 2)  # bytes belong to strict
        self.assertEqual(run_cli("--mode", "strict-evidence", "--mode", "structure-only", str(base) + ".json")[0], 2)
        self.assertEqual(run_cli()[0], 2)
        self.assertEqual(run_cli("--mode", "strict-evidence", "--bogus", "a")[0], 2)
        rc, text = run_cli("--mode", "strict-evidence", "--fixture", str(base) + ".json")
        self.assertEqual(rc, 1)
        self.assertIn("KCAO-STRICT-NO-NATIVE-BYTES", text)
        rc, text = run_cli("--mode", "strict-evidence", str(base) + ".json", "--source", str(base) + ".source.json")
        self.assertEqual(rc, 1)
        self.assertIn("KCAO-SYNTHETIC-NOT-FIXTURE", text)

    def test_the_unavailable_record_is_its_own_level(self):
        name = "valid/06-unavailable-with-typed-reason"
        for out in (structure(fx.observations()[name]), strict(fx.observations()[name])):
            self.assertEqual((out.codes, out.level), (set(), K.LEVEL_UNAVAILABLE_RECORD))


class BindingAndUnavailableTests(unittest.TestCase):
    def test_a_consumer_requiring_the_binding_gets_unavailable_native_binding_unverified(self):
        case = make_real(case_of("01"))
        r = CKA.check_strict(dumpb(case["obs"]), case["source"], None, fixture=False, require_work_item=True)
        self.assertEqual((r.problems, r.level, r.passed, r.unavailable["reason"]), ((), K.LEVEL_UNAVAILABLE, False, "native_binding_unverified"))
        self.assertEqual(r.unavailable["subject"], {"task_id": case["obs"]["subject"]["task_id"]})
        self.assertEqual(list(cka_validator().iter_errors(r.unavailable)), [])

    def test_the_command_line_exits_3_for_unavailable_and_prints_the_typed_record(self):
        case = make_real(case_of("01"))
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "o.json").write_bytes(dumpb(case["obs"]))
            (Path(tmp) / "s.json").write_bytes(case["source"])
            rc, text = run_cli("--mode", "strict-evidence", "--require-work-item", str(Path(tmp) / "o.json"), "--source", str(Path(tmp) / "s.json"))
        self.assertEqual(rc, 3, text)
        self.assertIn("KCAO_UNAVAILABLE native_binding_unverified", text)
        self.assertNotIn("KCAO_PASS", text)

    def test_the_live_non_fixture_record_omits_the_work_item_and_a_record_with_one_is_refused(self):
        case = make_real(case_of("03"))
        case["obs"]["work_item_binding"]["system"] = "muneral"
        for mode in ("structure-only", "strict-evidence"):
            r = CKA.check_structure(dumpb(case["obs"])) if mode == "structure-only" else CKA.check_strict(dumpb(case["obs"]), case["source"], case["work"])
            self.assertEqual(r.codes, {"KCAO-WORKITEM-NO-PROFILE"}, (mode, r.problems))

    def test_every_unavailable_reason_builds_a_schema_valid_record_whose_subject_is_only_the_request(self):
        enum = SCHEMA["$defs"]["unavailable"]["properties"]["reason"]["enum"]
        self.assertEqual(list(K.REASONS), enum)
        for reason in ("native_record_invalid", "native_binding_unverified", "unsupported_source_shape"):
            self.assertIn(reason, enum)
        for reason in K.REASONS:
            for subject in (None, "synthetic:task-requested"):
                record = K.unavailable_record(reason, subject)
                self.assertEqual(list(cka_validator().iter_errors(record)), [], record)
                self.assertEqual(record.get("subject"), None if subject is None else {"task_id": subject})
                self.assertEqual(set(record), {"schema", "status", "reason", "claims_scope", "claims"} | ({"subject"} if subject else set()))
        with self.assertRaises(ValueError):
            K.unavailable_record("because")

    def test_refusal_codes_that_a_producer_maps_to_a_reason_use_the_ratified_vocabulary(self):
        self.assertTrue(set(K.CODE_TO_REASON.values()) <= set(K.REASONS))
        self.assertEqual(set(K.CODE_TO_REASON.values()), {"native_record_invalid", "unsupported_source_shape"})


def cka_validator():
    return CKA._validator()


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.validator = cka_validator()

    def test_the_schema_is_a_valid_draft_2020_12_schema_marked_candidate_and_resolved(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("CANDIDATE", SCHEMA["title"])
        self.assertIn("NEVER MEANS ADMISSION READY", SCHEMA["description"])
        self.assertIn("6711021786", SCHEMA["description"])
        self.assertNotIn("PROVISIONAL", json.dumps(SCHEMA))
        self.assertIn("mutable metadata", SCHEMA["description"])

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
        self.assertEqual(set(claims["required"]), set(CKA.CLAIM_KEYS))
        self.assertEqual({v["const"] for v in claims["properties"].values()}, {"NOT_MEASURED"})
        self.assertEqual(SCHEMA["$defs"]["claims_scope"]["const"], "resolver-outcome-observation-only")

    def test_message_id_is_not_a_field_of_any_branch(self):
        def keys(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    yield k
                    yield from keys(v)
            elif isinstance(node, list):
                for v in node:
                    yield from keys(v)
        self.assertNotIn("message_id", set(keys(SCHEMA)))
        for branch in ("observed_contract", "observed_underdetermined", "observed_refusal", "unavailable"):
            self.assertNotIn("message_id", SCHEMA["$defs"][branch]["properties"])

    def test_the_unavailable_subject_is_documented_as_the_requested_target_only(self):
        self.assertIn("REQUESTED target only", SCHEMA["$defs"]["unavailable"]["properties"]["subject"]["description"])

    def test_every_pattern_is_a_whole_string_pattern(self):
        patterns = []

        def collect(node):
            if isinstance(node, dict):
                if isinstance(node.get("pattern"), str):
                    patterns.append(node["pattern"])
                for v in node.values():
                    collect(v)
            elif isinstance(node, list):
                for v in node:
                    collect(v)
        collect(SCHEMA)
        self.assertGreaterEqual(len(patterns), 6)
        for pattern in patterns:
            self.assertTrue(pattern.endswith("(?![\\s\\S])"), pattern)
            self.assertNotIn("$", pattern)

    def test_the_schema_alone_refuses_what_it_can_express(self):
        for name, data in fx.observations().items():
            code = EXPECT.get(name)
            if code in {"KCAO-SCHEMA-ID", "KCAO-POSITIVE-FLAG", "KCAO-CLAIMS", "KCAO-BRANCH", "KCAO-NATIVE-MISSING", "KCAO-SCHEMA"} or name.endswith("work_item_id_without_source_proof"):
                with self.subTest(fixture=name):
                    self.assertTrue(list(self.validator.iter_errors(json.loads(data))), name)
            elif code is None:
                with self.subTest(fixture=name):
                    self.assertEqual(list(self.validator.iter_errors(json.loads(data))), [], name)

    def test_the_schema_accepts_no_mixed_branch_even_without_the_checker(self):
        contract = json.loads(fx.observations()["valid/01-observed-contract-with-verified-exact-bytes"])
        for extra in ({"missing": [{"capability_token": "x"}]}, {"refusal_code": "SOME_CODE"}, {"reason": "no_native_record"}, {"message_id": "x"}):
            with self.subTest(extra=extra):
                self.assertTrue(list(self.validator.iter_errors({**contract, **extra})))


class BoundsAndIoTests(unittest.TestCase):
    """Operational errors (IO) are distinct from refusals, and every read is bounded before it is parsed or hashed."""

    def test_a_missing_file_is_an_operational_error_not_a_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, text = run_cli("--mode", "structure-only", "--fixture", str(Path(tmp) / "absent.json"))
        self.assertEqual(rc, 4, text)
        self.assertIn("KCAO_IOERROR", text)
        self.assertNotIn("KCAO_FAIL", text)

    def test_a_missing_sidecar_and_a_directory_and_a_device_are_operational_errors(self):
        base = FIXTURE_ROOT / "valid" / "01-observed-contract-with-verified-exact-bytes"
        rc, text = run_cli("--mode", "strict-evidence", "--fixture", str(base) + ".json", "--source", str(base) + ".source.json ")
        self.assertEqual(rc, 4)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run_cli("--mode", "structure-only", tmp)[0], 4)
        self.assertEqual(run_cli("--mode", "structure-only", "/dev/zero")[0], 4)  # not read to its end: a device is not a regular file

    def test_an_oversized_file_is_read_to_the_bound_only_and_refused_as_a_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            big = Path(tmp) / "big.json"
            big.write_bytes(b" " * (CKA.MAX_BYTES * 3))
            self.assertEqual(len(CKA._read_file(str(big))), CKA.MAX_BYTES + 1)
            rc, text = run_cli("--mode", "structure-only", "--fixture", str(big))
        self.assertEqual(rc, 1)
        self.assertIn("KCAO-READ", text)

    def test_each_sidecar_is_bounded_before_it_is_hashed(self):
        s4 = case_of("04")
        calls = []
        real = hashlib.sha256

        class Spy:
            @staticmethod
            def sha256(data=b""):
                calls.append(len(data))
                return real(data)
        original = CKA.hashlib
        CKA.hashlib = Spy
        try:
            r = CKA.check_strict(dumpb(s4["obs"]), b" " * (CKA.MAX_BYTES + 1), None, fixture=True)
        finally:
            CKA.hashlib = original
        self.assertEqual(r.codes, {"KCAO-NATIVE-READ"})
        self.assertEqual([n for n in calls if n > CKA.MAX_BYTES], [])

    def test_the_outer_guard_turns_an_unexpected_exception_into_a_typed_refusal(self):
        original = CKA._policy
        CKA._policy = lambda *a, **k: 1 / 0
        try:
            r = CKA.check_structure(fx.observations()["valid/01-observed-contract-with-verified-exact-bytes"], fixture=True)
        finally:
            CKA._policy = original
        self.assertEqual(r.codes, {"KCAO-INTERNAL"})

    def test_no_fixture_shape_reaches_the_outer_guard(self):
        for name, data in fx.observations().items():
            out = strict(data, sc(name, fx.SOURCE), sc(name, fx.WORK))
            self.assertNotIn("KCAO-INTERNAL", out.codes, name)
            self.assertNotIn("KCAO-INTERNAL", structure(data).codes, name)

    def test_nan_and_non_utf8_and_duplicates_are_refused(self):
        self.assertEqual(structure(b'{"a": NaN}').codes, {"KCAO-READ"})
        self.assertEqual(structure(b"\xff").codes, {"KCAO-READ"})
        self.assertEqual(structure(b"[]").codes, {"KCAO-SCHEMA"})


class ScenarioTests(unittest.TestCase):
    def test_every_scenario_has_its_declared_result(self):
        got = run_all(CKA)
        for s in SCENARIOS:
            with self.subTest(scenario=s.id):
                self.assertEqual(got[s.id][:3], (s.codes, s.level, s.reason))
                if s.flags is not None:
                    self.assertEqual(got[s.id][3], s.flags)

    def test_the_scenarios_cover_both_modes_the_live_labels_and_the_requirement(self):
        ids = {s.id.split(":")[0] for s in SCENARIOS}
        self.assertTrue({"strict-fixture", "structure-fixture", "real", "require", "no-fixture-mode", "strict-without-bytes", "bounds"} <= ids)


# ------------------------------------------------------------------ mutation of the checker's own guards

def disable_text(line: str) -> str:
    return re.sub(r"^(\s*(?:if|elif)\s)(.*):\s*$", r"\1False and (\2):", line, count=1)


def split_top(cond: str, op: str) -> list[str]:
    """Split a condition at ` op ` outside brackets and string literals."""
    parts, depth, cur, i, quote = [], 0, "", 0, None
    while i < len(cond):
        ch = cond[i]
        if quote:
            cur += ch
            if ch == "\\":
                cur += cond[i + 1]
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            cur += ch
        elif ch in "([{":
            depth += 1
            cur += ch
        elif ch in ")]}":
            depth -= 1
            cur += ch
        elif depth == 0 and cond.startswith(f" {op} ", i):
            parts.append(cur)
            cur = ""
            i += len(op) + 1
        else:
            cur += ch
        i += 1
    parts.append(cur)
    return parts


def guard_lines(source: str) -> list[int]:
    """Indices of every `if`/`elif` line whose block holds a KCAO- refusal (the checker's refusal guards)."""
    lines = source.splitlines()
    found = []
    for i, line in enumerate(lines):
        m = re.match(r"(\s*)(if|elif)\s.*:\s*$", line)
        if not m:
            continue
        indent = len(m.group(1))
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > indent):
            if "KCAO-" in lines[j]:
                found.append(i)
                break
            j += 1
    return found


def mutants(source: str) -> list[tuple[str, str]]:
    """(label, mutated source): every guard switched off, and for each `or`/`and` guard every operand neutralised."""
    lines = source.splitlines()
    out = []
    for i in guard_lines(source):
        line = lines[i]
        m = re.match(r"(\s*(?:if|elif)\s)(.*):\s*$", line)
        head, cond = m.group(1), m.group(2)
        mutated = lines.copy()
        mutated[i] = disable_text(line)
        out.append((f"L{i + 1} off: {cond[:70]}", "\n".join(mutated)))
        for op, neutral in (("or", "False"), ("and", "True")):
            parts = split_top(cond, op)
            if len(parts) > 1:
                for k, part in enumerate(parts):
                    variant = parts.copy()
                    variant[k] = neutral
                    mutated = lines.copy()
                    mutated[i] = f"{head}{f' {op} '.join(variant)}:"
                    out.append((f"L{i + 1} {op}-operand {k} -> {neutral}: {part[:60]}", "\n".join(mutated)))
    return out


def load_source(source: str) -> types.ModuleType:
    name = "check_kc_admission_observation_mutant"
    module = types.ModuleType(name)
    module.__file__ = CKA.__file__
    sys.modules[name] = module  # a dataclass looks its module up by name
    try:
        exec(compile(source, CKA.__file__, "exec"), module.__dict__)
    finally:
        del sys.modules[name]
    return module


class MutationTests(unittest.TestCase):
    def test_the_unmutated_checker_is_the_clean_baseline(self):
        self.assertEqual(deviations(load_source(SOURCE_TEXT), stop_at_first=False), {})

    def test_there_are_many_guards_and_each_mutant_is_killed_by_a_failing_scenario(self):
        all_mutants = mutants(SOURCE_TEXT)
        self.assertGreaterEqual(len(all_mutants), 90, len(all_mutants))
        survivors, errors = [], []
        for label, text in all_mutants:
            try:
                module = load_source(text)
            except SyntaxError as exc:  # a mutant that does not compile proves nothing
                errors.append((label, str(exc)))
                continue
            if not deviations(module):
                survivors.append(label)
        self.assertEqual(errors, [])
        self.assertEqual(survivors, [], "mutants no scenario can tell from the checker")

    def test_every_refusal_code_the_checker_can_return_has_a_scenario(self):
        emitted = set(re.findall(r'"(KCAO-[A-Z-]+):', SOURCE_TEXT)) | set(re.findall(r'f"(KCAO-[A-Z-]+):', SOURCE_TEXT))
        emitted = {c for c in emitted if "FLAG" not in c}
        covered = {c for c in EXPECT.values() if c} | {c for s in SCENARIOS for c in s.codes} | {"KCAO-INTERNAL"}
        self.assertEqual(emitted - covered, set())


if __name__ == "__main__":
    unittest.main()
