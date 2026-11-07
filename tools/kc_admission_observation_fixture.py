#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Build the synthetic KCAdmissionObservation/v1 (CANDIDATE) fixtures: positive observations and one-defect mutants (every byte invented here, KCLIVE-01).

`python3 tools/kc_admission_observation_fixture.py write` regenerates schemas/fixtures/kc-admission-observation/; the unit tests rebuild the same bytes in memory and
fail if the committed files drift. Every positive names the source system `synthetic-fixture` and a record id starting `synthetic:`: it is a fixture, never a native
observation, valid only in explicit fixture mode (`--fixture`), and no id, issuer, event or digest here is real. Next to an observation `NAME.json` the files `NAME.source.json`
(the exact synthetic native record bytes that `native_source.sha256` hashes) and `NAME.work-item.json` (the exact synthetic work item record bytes) may sit. In every
mutant whose defect lives in a sidecar the hash is RECOMPUTED, so the case reaches its intended comparison and not the earlier digest guard; only the two `*_do_not_match_the_digest`
mutants keep a stale hash on purpose. A passing fixture is a statement about the checker's rules only, not about Argana, Muneral or any admission.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_kc_admission_observation as cka  # noqa: E402

FIXTURE_ROOT = cka.REPO / "schemas" / "fixtures" / "kc-admission-observation"
CLAIMS = {k: "NOT_MEASURED" for k in cka.CLAIM_KEYS}
SOURCE, WORK = ".source.json", ".work-item.json"
SD, WI = cka.SYNTHETIC_DECISION_SCHEMA, cka.SYNTHETIC_WORK_ITEM_SCHEMA
TIME = "2026-01-01T00:00:00Z"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(record) -> bytes:
    return (json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def halves(label: str) -> tuple[bytes, bytes]:
    return canonical({"synthetic_body": label}), canonical({"synthetic_manifest": label})


def native_contract(label: str, verdict: str, obligations: list, task_id: str, stored_at: str = TIME, parts: tuple[bytes, bytes] | None = None) -> tuple[bytes, str]:
    """A synthetic record shaped like ArganaContractRecord/v1 (src/argana/contracts.py build_record); no goal text, no real digest. `parts` overrides the two canonical halves."""
    body, manifest = parts or halves(label)
    digest = "sha256:" + sha(body + manifest)
    record = {
        "schema": cka.ARGANA_RECORD_SCHEMA, "digest": digest,
        "canonical": {"rule": "sha256(canonical_json(body) || canonical_json(closure_manifest))", "body_b64": base64.b64encode(body).decode(),
                      "closure_manifest_b64": base64.b64encode(manifest).decode(), "length": len(body) + len(manifest)},
        "kc2": {"revision": None, "snapshot": "synthetic-snapshot", "verdict": verdict, "reduction": "synthetic"},
        "obligations": obligations, "roles": [], "skills": [], "blueprints": [], "other_pinned": [], "budget_envelope": {},
        "request": {"task_id": task_id, "goal": "synthetic goal"}, "stored_at_utc": stored_at,
    }
    return dump(record), digest


def native_decision(task_id: str, outcome: str, **fields) -> bytes:
    """A synthetic non-contract native record (profile SyntheticNativeDecision/v1): it carries every fact the observation asserts."""
    return dump({"schema": SD, "task_id": task_id, "outcome": outcome, **fields})


def work_record(label: str, **over) -> bytes:
    record = {"schema": WI, "record_id": f"synthetic:evidence-{label}", "work_item_id": f"synthetic:work-item-{label}", "contract_digest": over.pop("contract_digest"),
              "task_id": f"synthetic:task-{label}", "intake_record_id": over.pop("intake_record_id")}
    record.update(over)
    return dump(record)


def observation(label: str, outcome: str, source: bytes, source_schema: str, **fields) -> dict:
    record = {"schema": cka.SCHEMA_ID, "status": "observed", "claims_scope": cka.CLAIMS_SCOPE, "claims": dict(CLAIMS), "subject": {"task_id": f"synthetic:task-{label}"},
              "resolver_outcome": outcome,
              "native_source": {"system": cka.SYNTHETIC_SYSTEM, "record_id": f"synthetic:record-{label}", "digest_domain": "sha256-exact-bytes", "sha256": sha(source),
                                "source_schema": source_schema}}
    record.update(fields)
    return record


def contract_case(label: str, verdict: str, obligations: list, parts: tuple[bytes, bytes] | None = None, **fields) -> dict:
    src, digest = native_contract(label, verdict, obligations, f"synthetic:task-{label}", parts=parts)
    obs = observation(label, "contract", src, cka.ARGANA_RECORD_SCHEMA, contract_digest=digest, obligations=copy.deepcopy(obligations), **fields)
    obs["native_source"]["record_id"] = "synthetic:" + digest
    return {"obs": obs, "source": src}


def build() -> dict[str, dict]:
    """Case name -> {obs, source, work} for the valid ones; every value is bytes or None."""
    cases: dict[str, dict] = {}
    case = contract_case("c1", "T", [], resolver_verdict="T")
    case["obs"]["native_source"]["recorded_at"] = TIME
    cases["01-observed-contract-with-verified-exact-bytes"] = case
    cases["02-observed-contract-k-keeps-its-obligation"] = contract_case("c2", "K", [{"kind": "synthetic-obligation"}], resolver_verdict="K")

    case = contract_case("c3", "T", [], resolver_verdict="T")
    work = work_record("c3", contract_digest=case["obs"]["contract_digest"], intake_record_id=case["obs"]["native_source"]["record_id"])
    case["obs"].update({"work_item_id": "synthetic:work-item-c3", "work_item_binding": {"system": cka.SYNTHETIC_SYSTEM, "record_id": "synthetic:evidence-c3",
                                                                                          "digest_domain": "sha256-exact-bytes", "sha256": sha(work)}})
    case["work"] = work
    cases["03-observed-contract-with-evidenced-work-item"] = case

    src = native_decision("synthetic:task-c4", "underdetermined", verdict="U", missing=[{"capability_token": "synthetic-capability"}], stored_at_utc=TIME)
    obs = observation("c4", "underdetermined", src, SD, resolver_verdict="U", missing=[{"capability_token": "synthetic-capability"}])
    obs["native_source"]["recorded_at"] = TIME
    cases["04-observed-underdetermined-with-missing-and-no-work-item"] = {"obs": obs, "source": src}

    src = native_decision("synthetic:task-c5", "refusal", verdict="F", refusal_code="SYNTHETIC_REFUSAL")
    cases["05-observed-refusal-with-typed-code"] = {"obs": observation("c5", "refusal", src, SD, resolver_verdict="F", refusal_code="SYNTHETIC_REFUSAL"), "source": src}

    cases["06-unavailable-with-typed-reason"] = {"obs": cka.unavailable_record("outcome_not_persisted"), "source": None}
    cases["07-unavailable-native-binding-unverified-with-the-requested-subject"] = {"obs": cka.unavailable_record("native_binding_unverified", "synthetic:task-requested"), "source": None}

    src = native_decision("synthetic:task-c8", "refusal", refusal_code="SYNTHETIC_PRE_RESOLVER_REFUSAL")
    cases["08-observed-refusal-without-a-recorded-verdict"] = {"obs": observation("c8", "refusal", src, SD, refusal_code="SYNTHETIC_PRE_RESOLVER_REFUSAL"), "source": src}
    return cases


EXPECT: dict[str, str | None] = {}


def variants() -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    valid = build()
    EXPECT.clear()
    for name, case in valid.items():
        files[f"valid/{name}.json"] = dump(case["obs"])
        EXPECT[f"valid/{name}"] = None
        if case.get("source") is not None:
            files[f"valid/{name}{SOURCE}"] = case["source"]
        if case.get("work") is not None:
            files[f"valid/{name}{WORK}"] = case["work"]
    contract, contract_k = valid["01-observed-contract-with-verified-exact-bytes"], valid["02-observed-contract-k-keeps-its-obligation"]
    with_work, under = valid["03-observed-contract-with-evidenced-work-item"], valid["04-observed-underdetermined-with-missing-and-no-work-item"]
    refusal, unavailable = valid["05-observed-refusal-with-typed-code"], valid["06-unavailable-with-typed-reason"]
    no_verdict = valid["08-observed-refusal-without-a-recorded-verdict"]

    def put(name: str, obs_bytes: bytes, code: str, src: bytes | None, wrk: bytes | None) -> None:
        EXPECT[f"invalid/{name}"] = code
        files[f"invalid/{name}.json"] = obs_bytes
        if src is not None:
            files[f"invalid/{name}{SOURCE}"] = src
        if wrk is not None:
            files[f"invalid/{name}{WORK}"] = wrk

    def mutant(name: str, base: dict, code: str, edit=None, *, source="keep", work="keep", src_edit=None, work_edit=None, rehash: bool = True) -> None:
        """One defect, one expected code. A sidecar that is replaced or edited is re-hashed into the observation (rehash=True), so only the edit can be refused."""
        record = copy.deepcopy(base["obs"])
        if edit:
            edit(record)
        src = base.get("source") if source == "keep" else source
        wrk = base.get("work") if work == "keep" else work
        if src_edit is not None:
            parsed = json.loads(src)
            src_edit(parsed)  # in place; the return value is ignored (pop/update lambdas return things)
            src = dump(parsed)
        if work_edit is not None:
            parsed = json.loads(wrk)
            work_edit(parsed)
            wrk = dump(parsed)
        if rehash:
            if src is not None and "native_source" in record and (src_edit is not None or source != "keep"):
                record["native_source"]["sha256"] = sha(src)
            if wrk is not None and "work_item_binding" in record and (work_edit is not None or work != "keep"):
                record["work_item_binding"]["sha256"] = sha(wrk)
        put(name, dump(record), code, src, wrk)

    def pop(*keys):
        return lambda r: [r.pop(k) for k in keys]

    def to_underdetermined(r):
        for k in ("contract_digest", "obligations"):
            r.pop(k)
        r.update({"resolver_outcome": "underdetermined", "missing": [{"capability_token": "synthetic-capability"}]})

    def to_refusal(r):
        for k in ("contract_digest", "obligations"):
            r.pop(k)
        r.update({"resolver_outcome": "refusal", "refusal_code": "SYNTHETIC_REFUSAL"})

    # ---- identity, branch and claim rules (unchanged in meaning)
    mutant("missing_native_record_presented_as_observed", contract, "KCAO-NATIVE-MISSING", pop("native_source"), source=None)
    mutant("native_bytes_do_not_match_the_digest", contract, "KCAO-BYTES-DIGEST", source=contract["source"] + b" ", rehash=False)
    mutant("work_item_bytes_do_not_match_the_digest", with_work, "KCAO-BYTES-DIGEST", work=with_work["work"] + b" ", rehash=False)
    mutant("forged_record_path_as_record_id", under, "KCAO-FORGED", lambda r: r["native_source"].update({"record_id": "synthetic:../../etc/passwd"}))
    mutant("forged_issuer_unknown_source_system", under, "KCAO-FORGED", lambda r: r["native_source"].update({"system": "trusted-issuer", "record_id": "record-without-prefix"}))
    mutant("synthetic_system_without_the_synthetic_prefix", under, "KCAO-FORGED", lambda r: r["native_source"].update({"record_id": "record-without-prefix"}))
    mutant("native_system_with_the_synthetic_prefix", under, "KCAO-FORGED", lambda r: r["native_source"].update({"system": "argana-contract-store"}))
    mutant("forged_native_record_of_another_schema", contract, "KCAO-FORGED", src_edit=lambda n: n.update({"schema": "SomethingElse/v1"}))
    mutant("work_item_id_without_source_proof", with_work, "KCAO-WORKITEM-NO-PROOF", pop("work_item_binding"), work=None)
    mutant("work_item_id_on_a_refusal", refusal, "KCAO-BRANCH", lambda r: r.update({"work_item_id": "synthetic:work-item-c5"}))
    mutant("unknown_schema_value", contract, "KCAO-SCHEMA-ID", lambda r: r.update({"schema": "KCAdmissionObservation/v2"}))
    mutant("contract_digest_on_a_refusal", refusal, "KCAO-BRANCH", lambda r: r.update({"contract_digest": contract["obs"]["contract_digest"]}))
    mutant("missing_on_a_contract", contract, "KCAO-BRANCH", lambda r: r.update({"missing": [{"capability_token": "synthetic-capability"}]}))
    mutant("refusal_code_on_an_underdetermined", under, "KCAO-BRANCH", lambda r: r.update({"refusal_code": "SYNTHETIC_REFUSAL"}))
    mutant("reason_on_an_observed_record", contract, "KCAO-BRANCH", lambda r: r.update({"reason": "no_native_record"}))
    mutant("outcome_on_an_unavailable_record", unavailable, "KCAO-BRANCH", lambda r: r.update({"resolver_outcome": "contract"}))
    mutant("contract_digest_on_an_unavailable_record", unavailable, "KCAO-BRANCH", lambda r: r.update({"contract_digest": contract["obs"]["contract_digest"]}))
    mutant("native_source_on_an_unavailable_record", unavailable, "KCAO-BRANCH", lambda r: r.update({"native_source": contract["obs"]["native_source"]}))
    mutant("message_id_is_not_a_field", contract, "KCAO-SCHEMA", lambda r: r.update({"message_id": contract["obs"]["native_source"]["record_id"]}))
    mutant("admitted_true", contract, "KCAO-POSITIVE-FLAG", lambda r: r.update({"admitted": True}))
    mutant("authorized_true_in_claims", contract, "KCAO-POSITIVE-FLAG", lambda r: r["claims"].update({"runtime_authorization": True}))
    mutant("publishable_true_on_unavailable", unavailable, "KCAO-POSITIVE-FLAG", lambda r: r.update({"publishable": True}))
    mutant("claim_set_to_measured", contract, "KCAO-CLAIMS", lambda r: r["claims"].update({"source_admission": "MEASURED"}))
    mutant("claim_set_to_ready", contract, "KCAO-CLAIMS", lambda r: r["claims"].update({"issuer_authority": "READY"}))
    mutant("claim_missing", contract, "KCAO-CLAIMS", lambda r: r["claims"].pop("publication"))
    mutant("claims_scope_widened", contract, "KCAO-CLAIMS", lambda r: r.update({"claims_scope": "admission"}))
    mutant("claims_not_an_object", contract, "KCAO-CLAIMS", lambda r: r.update({"claims": None}))
    mutant("claims_is_an_array", contract, "KCAO-CLAIMS", lambda r: r.update({"claims": []}))
    mutant("unknown_extra_field", contract, "KCAO-SCHEMA", lambda r: r.update({"issuer": "synthetic-issuer"}))
    mutant("unknown_extra_field_in_native_source", contract, "KCAO-SCHEMA", lambda r: r["native_source"].update({"path": "/var/lib/synthetic"}))
    mutant("k_verdict_drops_the_obligations", contract_k, "KCAO-SCHEMA", lambda r: r.update({"obligations": []}))
    mutant("verdict_outside_the_enum", contract, "KCAO-SCHEMA", lambda r: r.update({"resolver_verdict": "OK"}))
    mutant("refusal_code_not_a_typed_code", refusal, "KCAO-SCHEMA", lambda r: r.update({"refusal_code": "refused it"}))
    mutant("refusal_code_with_a_trailing_newline", refusal, "KCAO-SCHEMA", lambda r: r.update({"refusal_code": "SYNTHETIC_REFUSAL\n"}))
    mutant("sha256_with_a_trailing_newline", contract, "KCAO-SCHEMA", lambda r: r["native_source"].update({"sha256": sha(contract["source"]) + "\n"}), rehash=False)
    mutant("underdetermined_without_missing", under, "KCAO-SCHEMA", pop("missing"))
    mutant("unavailable_reason_outside_the_enum", unavailable, "KCAO-SCHEMA", lambda r: r.update({"reason": "because"}))
    mutant("unavailable_without_a_reason", unavailable, "KCAO-SCHEMA", pop("reason"))
    mutant("unavailable_subject_is_not_an_object", unavailable, "KCAO-SCHEMA", lambda r: r.update({"subject": "synthetic:task-x"}))
    mutant("digest_domain_is_not_exact_bytes", contract, "KCAO-SCHEMA", lambda r: r["native_source"].update({"digest_domain": "sha256-tree-manifest-v1"}))
    mutant("unknown_work_item_source", with_work, "KCAO-FORGED", lambda r: r["work_item_binding"].update({"system": "trusted-tracker"}))
    mutant("work_item_binding_with_a_muneral_system", with_work, "KCAO-WORKITEM-NO-PROFILE", lambda r: r["work_item_binding"].update({"system": "muneral"}))

    # ---- R-KCAO3 shapes on the observation itself: every valid JSON shape reaches a typed refusal
    for tag, shape in (("an_array", []), ("an_object", {"a": 1}), ("a_string", "nonsense"), ("a_number", 7), ("null", None)):
        mutant(f"resolver_outcome_is_{tag}", contract, "KCAO-SCHEMA", lambda r, shape=shape: r.update({"resolver_outcome": shape}))
    mutant("subject_is_a_string", contract, "KCAO-SCHEMA", lambda r: r.update({"subject": "synthetic:task-c1"}))
    mutant("native_source_is_an_array", contract, "KCAO-SCHEMA", lambda r: r.update({"native_source": []}))
    mutant("obligations_is_a_string", contract, "KCAO-SCHEMA", lambda r: r.update({"obligations": "none"}))
    for tag, raw in (("an_array", b"[]\n"), ("null", b"null\n"), ("a_number", b"7\n"), ("a_string", b'"contract"\n')):
        put(f"observation_is_{tag}", raw, "KCAO-SCHEMA", None, None)
    put("duplicate_member", dump(contract["obs"]).replace(b'"status": "observed"', b'"status": "observed",\n  "status": "observed"', 1), "KCAO-READ", None, None)
    put("not_json", b"not json\n", "KCAO-READ", None, None)

    # ---- R-KCAO1: the native source is compared with EVERY emitted fact (hashes recomputed, so each case reaches its comparison)
    mutant("same_contract_labelled_as_a_refusal", contract, "KCAO-NATIVE-MISMATCH", to_refusal)
    mutant("same_contract_labelled_as_underdetermined", contract, "KCAO-NATIVE-MISMATCH", to_underdetermined)
    mutant("empty_native_object_for_an_underdetermined", under, "KCAO-FORGED", source=b"{}")
    mutant("native_decision_with_only_its_schema", under, "KCAO-NATIVE-INVALID", source=dump({"schema": SD}))
    mutant("native_decision_without_an_outcome", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.pop("outcome"))
    mutant("native_decision_without_a_task_id", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.pop("task_id"))
    mutant("native_decision_outcome_is_an_array", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"outcome": ["underdetermined"]}))
    mutant("native_decision_task_is_not_a_string", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"task_id": ["synthetic:task-c4"]}))
    mutant("native_refusal_without_its_code", refusal, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.pop("refusal_code"))
    mutant("native_refusal_code_is_not_a_string", refusal, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"refusal_code": 7}))
    mutant("refusal_code_differs_from_the_native_code", refusal, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"refusal_code": "OTHER_REFUSAL"}))
    mutant("native_underdetermined_without_missing", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.pop("missing"))
    mutant("missing_differs_from_the_native_payload", under, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"missing": [{"capability_token": "other-capability"}]}))
    mutant("missing_drops_a_native_entry", under, "KCAO-NATIVE-MISMATCH", src_edit=lambda n: n["missing"].append({"capability_token": "second-capability"}))
    mutant("underdetermined_verdict_differs_from_the_native_verdict", under, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"resolver_verdict": "T"}))
    mutant("underdetermined_omits_the_native_verdict", under, "KCAO-NATIVE-MISMATCH", pop("resolver_verdict"))
    mutant("contract_omits_the_native_verdict", contract_k, "KCAO-NATIVE-MISMATCH", pop("resolver_verdict"))
    mutant("verdict_emitted_but_the_native_record_has_none", no_verdict, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"resolver_verdict": "F"}))
    mutant("contract_verdict_differs_from_the_native_record", contract_k, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"resolver_verdict": "T"}))
    mutant("native_verdict_outside_the_enum", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"verdict": "X"}))
    mutant("native_verdict_is_an_array", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"verdict": ["U"]}))
    mutant("recorded_at_emitted_but_the_native_record_has_none", refusal, "KCAO-NATIVE-MISMATCH", lambda r: r["native_source"].update({"recorded_at": TIME}))
    mutant("decision_recorded_at_differs_from_the_native_time", under, "KCAO-NATIVE-MISMATCH", lambda r: r["native_source"].update({"recorded_at": "2026-02-02T00:00:00Z"}))
    mutant("native_stored_time_is_not_a_string", under, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"stored_at_utc": 20260101}))
    mutant("recorded_at_differs_from_the_native_record", contract, "KCAO-NATIVE-MISMATCH", lambda r: r["native_source"].update({"recorded_at": "2026-02-02T00:00:00Z"}))
    mutant("task_differs_from_the_native_record", under, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"subject": {"task_id": "synthetic:another-task"}}))
    mutant("outcome_differs_from_the_native_record", refusal, "KCAO-NATIVE-MISMATCH", lambda r: (r.update({"resolver_outcome": "underdetermined", "missing": [{"capability_token": "x"}]}), r.pop("refusal_code")))
    mutant("source_schema_absent_on_a_contract", contract, "KCAO-NATIVE-PROFILE", lambda r: r["native_source"].pop("source_schema"))
    mutant("source_schema_absent_on_a_decision", under, "KCAO-NATIVE-PROFILE", lambda r: r["native_source"].pop("source_schema"))
    mutant("source_schema_is_an_unsupported_version", contract, "KCAO-NATIVE-PROFILE", lambda r: r["native_source"].update({"source_schema": "ArganaContractRecord/v2"}))
    mutant("source_schema_names_another_profile_than_the_bytes", contract, "KCAO-FORGED", lambda r: r["native_source"].update({"source_schema": SD}))
    mutant("decision_profile_cannot_carry_a_contract", contract, "KCAO-NATIVE-MISMATCH", lambda r: r["native_source"].update({"source_schema": SD}),
           source=native_decision("synthetic:task-c1", "contract"))
    mutant("record_id_does_not_name_the_contract", contract, "KCAO-FORGED", lambda r: r["native_source"].update({"record_id": "synthetic:another-contract"}))
    mutant("native_record_digest_field_differs", contract, "KCAO-FORGED", src_edit=lambda n: n.update({"digest": "sha256:" + "0" * 64}))
    mutant("native_record_without_a_task_id", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n["request"].pop("task_id"))
    mutant("native_record_task_is_a_number", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n["request"].update({"task_id": 7}))
    for tag, shape in (("an_array", ["wrong-type"]), ("a_string", "wrong-type"), ("null", None), ("a_number", 7)):
        mutant(f"native_request_is_{tag}", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n, shape=shape: n.update({"request": shape}))
    mutant("native_request_is_missing", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.pop("request"))
    for tag, shape in (("an_array", ["T"]), ("a_string", "T"), ("null", None), ("a_number", 7)):
        mutant(f"native_kc2_is_{tag}", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n, shape=shape: n.update({"kc2": shape}))
    for tag, shape in (("null", None), ("an_object", {"kind": "x"}), ("a_string", "kind")):
        mutant(f"native_obligations_is_{tag}", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n, shape=shape: n.update({"obligations": shape}))
    for tag, item in (("null", None), ("a_number", 7), ("a_string", "kind"), ("an_array", ["kind"])):
        mutant(f"native_obligation_item_is_{tag}", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n, item=item: n.update({"obligations": [item]}))
    mutant("native_obligation_without_a_kind", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"obligations": [{}]}))
    mutant("native_obligation_kind_is_not_a_string", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"obligations": [{"kind": 7}]}))
    mutant("native_obligation_carries_an_extra_condition_field", contract_k, "KCAO-NATIVE-UNSUPPORTED-SHAPE",
           src_edit=lambda n: n.update({"obligations": [{"kind": "synthetic-obligation", "ref": "synthetic-ref"}]}))
    mutant("native_missing_item_carries_an_extra_condition_field", under, "KCAO-NATIVE-UNSUPPORTED-SHAPE",
           src_edit=lambda n: n.update({"missing": [{"capability_token": "synthetic-capability", "reason": "synthetic"}]}))
    mutant("native_decision_carries_an_unprojected_field", under, "KCAO-NATIVE-UNSUPPORTED-SHAPE", src_edit=lambda n: n.update({"detail": "synthetic detail"}))
    mutant("obligations_differ_from_the_native_record", contract_k, "KCAO-NATIVE-MISMATCH", lambda r: r.update({"obligations": [{"kind": "another-kind"}]}))
    mutant("native_has_an_obligation_the_observation_omits", contract, "KCAO-NATIVE-MISMATCH", src_edit=lambda n: n.update({"obligations": [{"kind": "synthetic-obligation"}]}))
    for tag, raw in (("an_array", b"[]\n"), ("null", b"null\n"), ("a_number", b"7\n"), ("a_string", b'"native"\n'), ("not_json", b"not a JSON record"), ("a_lone_surrogate", b'{"a": "\\ud800"}\n')):
        mutant(f"native_bytes_are_{tag}", under, "KCAO-NATIVE-READ", source=raw)

    # ---- contract halves: parsed strictly, canonical, and in agreement with contract_digest (the digest is recomputed over the new halves)
    def halves_case(name: str, code: str, body: bytes, manifest: bytes) -> None:
        case = contract_case("m1", "T", [], parts=(body, manifest), resolver_verdict="T")
        put(name, dump(case["obs"]), code, case["source"], None)

    halves_case("canonical_halves_are_not_json", "KCAO-NATIVE-INVALID", b"NOT JSON", b"")
    halves_case("canonical_body_is_not_in_canonical_form", "KCAO-NATIVE-INVALID", b'{"a": 1}', b"{}")
    halves_case("canonical_body_is_a_json_array", "KCAO-NATIVE-INVALID", b"[1]", b"{}")
    halves_case("canonical_body_holds_a_float", "KCAO-NATIVE-INVALID", b'{"a":1.5}', b"{}")
    halves_case("canonical_body_repeats_a_member", "KCAO-NATIVE-INVALID", b'{"a":1,"a":2}', b"{}")
    halves_case("canonical_manifest_is_a_number", "KCAO-NATIVE-INVALID", b"{}", b"7")
    halves_case("canonical_body_is_not_utf8", "KCAO-NATIVE-INVALID", b"\xff\xfe", b"{}")
    mutant("contract_digest_is_not_the_digest_of_the_halves", contract, "KCAO-CONTRACT-DIGEST",
           src_edit=lambda n: (n["canonical"].update({"body_b64": base64.b64encode(canonical({"synthetic_body": "altered"})).decode()}), n.update({"digest": contract["obs"]["contract_digest"]})))
    mutant("canonical_object_is_missing", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.pop("canonical"))
    mutant("canonical_is_a_string", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n.update({"canonical": "halves"}))
    mutant("canonical_half_is_not_base64", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n["canonical"].update({"body_b64": "!!!not-base64!!!"}))
    mutant("canonical_half_is_a_number", contract, "KCAO-NATIVE-INVALID", src_edit=lambda n: n["canonical"].update({"closure_manifest_b64": 7}))

    # ---- R-KCAO2: the work item bytes are parsed and joined to the work item, the contract, the task and this intake (the evidence record id is NOT the task id)
    def with_work_edit(name: str, code: str, edit) -> None:
        mutant(name, with_work, code, work_edit=edit)

    mutant("work_item_bytes_are_not_json", with_work, "KCAO-WORKITEM-INVALID", work=b"not a JSON record")
    mutant("work_item_bytes_are_an_unrelated_object", with_work, "KCAO-WORKITEM-INVALID", work=dump({"hello": "world"}))
    mutant("work_item_bytes_are_an_array", with_work, "KCAO-WORKITEM-INVALID", work=b"[]\n")
    mutant("work_item_bytes_are_null", with_work, "KCAO-WORKITEM-INVALID", work=b"null\n")
    with_work_edit("work_item_record_has_another_schema", "KCAO-WORKITEM-INVALID", lambda w: w.update({"schema": "SomethingElse/v1"}))
    with_work_edit("work_item_record_has_an_extra_field", "KCAO-WORKITEM-INVALID", lambda w: w.update({"title": "synthetic"}))
    with_work_edit("work_item_record_field_is_not_a_string", "KCAO-WORKITEM-INVALID", lambda w: w.update({"task_id": 7}))
    with_work_edit("work_item_record_lacks_a_field", "KCAO-WORKITEM-INVALID", lambda w: w.pop("intake_record_id"))
    with_work_edit("work_item_record_names_another_work_item", "KCAO-WORKITEM-MISMATCH", lambda w: w.update({"work_item_id": "synthetic:work-item-other"}))
    with_work_edit("work_item_record_names_another_contract", "KCAO-WORKITEM-MISMATCH", lambda w: w.update({"contract_digest": "sha256:" + "1" * 64}))
    with_work_edit("work_item_record_names_another_work_item_and_contract", "KCAO-WORKITEM-MISMATCH",
                   lambda w: w.update({"work_item_id": "synthetic:work-item-other", "contract_digest": "sha256:" + "1" * 64}))
    with_work_edit("work_item_record_names_another_task", "KCAO-WORKITEM-MISMATCH", lambda w: w.update({"task_id": "synthetic:task-other"}))
    with_work_edit("work_item_record_joins_another_intake", "KCAO-WORKITEM-MISMATCH", lambda w: w.update({"intake_record_id": "synthetic:record-other-intake"}))
    with_work_edit("work_item_record_is_not_the_named_evidence", "KCAO-WORKITEM-MISMATCH", lambda w: w.update({"record_id": "synthetic:evidence-other"}))
    mutant("work_item_binding_names_another_record", with_work, "KCAO-WORKITEM-MISMATCH", lambda r: r["work_item_binding"].update({"record_id": "synthetic:evidence-other"}))
    mutant("work_item_binding_equal_to_the_work_item_id_is_not_the_evidence", with_work, "KCAO-WORKITEM-MISMATCH", lambda r: r["work_item_binding"].update({"record_id": "synthetic:work-item-c3"}))
    mutant("work_item_sidecar_is_missing", with_work, "KCAO-WORKITEM-NO-PROOF", work=None)
    return files


def observations() -> dict[str, bytes]:
    """The observation files only (not the byte sidecars), keyed `valid/NAME` / `invalid/NAME`."""
    return {k[: -len(".json")]: v for k, v in variants().items() if not k.endswith((SOURCE, WORK))}


def expected() -> dict[str, str | None]:
    variants()
    return dict(EXPECT)


def sidecar(files: dict[str, bytes], name: str, suffix: str) -> bytes | None:
    return files.get(f"{name}{suffix}")


README = (
    "# Synthetic KCAdmissionObservation/v1 (CANDIDATE) records\n\n"
    "Every file here is invented for this repository and is a fixture, not a native observation: the source system is `synthetic-fixture` and every record id starts "
    "`synthetic:`. Synthetic labels and the work item binding are valid ONLY in explicit fixture mode (`--fixture`); without it they are refused, and a fixture pass has the "
    "level `fixture-evidence`, never a native observation. `valid/` holds eight records (observed `contract` with verified exact-byte provenance, a `K` contract that keeps its "
    "obligation, a contract with an evidenced synthetic work item, observed `underdetermined`, observed `refusal`, an observed `refusal` whose source records no verdict, "
    "`unavailable` with a typed reason, and `unavailable` / `native_binding_unverified` whose `subject` is the requested target only); passing them is a statement about the "
    "checker's rules only, not about Argana, Muneral or any admission. `NAME.source.json` holds the exact synthetic native record bytes whose SHA-256 is `native_source.sha256`: "
    "an `ArganaContractRecord/v1`-shaped record for the `contract` branch (the only branch the Argana record can support) or a `SyntheticNativeDecision/v1` record that carries every "
    "fact an `underdetermined` or `refusal` observation asserts; `NAME.work-item.json` holds the exact synthetic `SyntheticWorkItemRecord/v1` bytes. The real digest-named Argana "
    "record is mutable metadata and cannot be an immutable intake event, so until native capture exists the honest live result is `unavailable`. Each file under `invalid/` is a "
    "mutant with one defect and one expected refusal code (see `EXPECT` in `tools/kc_admission_observation_fixture.py`); a sidecar defect is re-hashed so the case reaches the intended "
    "comparison, except the two `*_do_not_match_the_digest` mutants. Regenerate with\n`python3 tools/kc_admission_observation_fixture.py write`; the unit tests fail if the committed "
    "files drift.\n")


def write() -> None:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT)
    for name, data in variants().items():
        target = FIXTURE_ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (FIXTURE_ROOT / "README.md").write_text(README, encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    else:
        print("usage: kc_admission_observation_fixture.py write", file=sys.stderr)
        raise SystemExit(2)
