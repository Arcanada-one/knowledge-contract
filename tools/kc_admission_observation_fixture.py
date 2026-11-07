#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Build the synthetic KCAdmissionObservation/v1 (CANDIDATE) fixtures: positive observations and one-defect mutants (every byte invented here, KCLIVE-01).

`python3 tools/kc_admission_observation_fixture.py write` regenerates schemas/fixtures/kc-admission-observation/; the unit tests rebuild the same bytes in memory and
fail if the committed files drift. Every positive names the source system `synthetic-fixture` and a record id starting `synthetic:`: it is a fixture, never a native
observation, and no id, issuer, event or digest here is real. Next to an observation `NAME.json` the files `NAME.source.json` (the exact synthetic native record bytes
that `native_source.sha256` hashes) and `NAME.work-item.json` (the exact synthetic work item record bytes) may sit. A passing fixture is a statement about the checker's
rules only, not about Argana, Muneral or any admission.
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


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(record: dict) -> bytes:
    return (json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def halves(label: str) -> tuple[bytes, bytes, str]:
    body = json.dumps({"synthetic_body": label}, sort_keys=True, separators=(",", ":")).encode()
    manifest = json.dumps({"synthetic_manifest": label}, sort_keys=True, separators=(",", ":")).encode()
    return body, manifest, "sha256:" + sha(body + manifest)


def native_contract(label: str, verdict: str, obligations: list[dict], task_id: str, stored_at: str = "2026-01-01T00:00:00Z") -> tuple[bytes, str]:
    """A synthetic record shaped like ArganaContractRecord/v1 (src/argana/contracts.py build_record); no goal text, no real digest."""
    body, manifest, digest = halves(label)
    record = {
        "schema": cka.ARGANA_RECORD_SCHEMA, "digest": digest,
        "canonical": {"rule": "sha256(canonical_json(body) || canonical_json(closure_manifest))", "body_b64": base64.b64encode(body).decode(),
                      "closure_manifest_b64": base64.b64encode(manifest).decode(), "length": len(body) + len(manifest)},
        "kc2": {"revision": None, "snapshot": "synthetic-snapshot", "verdict": verdict, "reduction": "synthetic"},
        "obligations": obligations, "roles": [], "skills": [], "blueprints": [], "other_pinned": [], "budget_envelope": {},
        "request": {"task_id": task_id, "goal": "synthetic goal"}, "stored_at_utc": stored_at,
    }
    return dump(record), digest


def native_decision(task_id: str, outcome: str, extra: dict) -> bytes:
    return dump({"synthetic": "native-decision", "task_id": task_id, "outcome": outcome, **extra})


def observation(label: str, outcome: str | None, source: bytes | None, **fields) -> dict:
    record = {"schema": cka.SCHEMA_ID, "status": "observed", "claims_scope": cka.CLAIMS_SCOPE, "claims": dict(CLAIMS), "subject": {"task_id": f"synthetic:task-{label}"}}
    if outcome:
        record["resolver_outcome"] = outcome
        record["native_source"] = {"system": cka.SYNTHETIC_SYSTEM, "record_id": f"synthetic:record-{label}", "digest_domain": "sha256-exact-bytes", "sha256": sha(source)}
    record.update(fields)
    return record


def build() -> dict[str, dict]:
    """Case name -> {obs, source, work} for the valid ones; every value is bytes or None."""
    cases: dict[str, dict] = {}
    task = "synthetic:task-c1"
    src, digest = native_contract("c1", "T", [], task)
    obs = observation("c1", "contract", src, resolver_verdict="T", contract_digest=digest, obligations=[])
    obs["native_source"].update({"record_id": "synthetic:" + digest, "source_schema": cka.ARGANA_RECORD_SCHEMA, "recorded_at": "2026-01-01T00:00:00Z"})
    cases["01-observed-contract-with-verified-exact-bytes"] = {"obs": obs, "source": src}

    task = "synthetic:task-c2"
    src, digest = native_contract("c2", "K", [{"kind": "synthetic-obligation"}], task)
    obs = observation("c2", "contract", src, resolver_verdict="K", contract_digest=digest, obligations=[{"kind": "synthetic-obligation"}])
    obs["native_source"].update({"record_id": "synthetic:" + digest, "source_schema": cka.ARGANA_RECORD_SCHEMA})
    cases["02-observed-contract-k-keeps-its-obligation"] = {"obs": obs, "source": src}

    src, digest = native_contract("c3", "T", [], "synthetic:task-c3")
    work = dump({"synthetic": "work-item-record", "id": "synthetic:work-item-c3"})
    obs = observation("c3", "contract", src, contract_digest=digest, obligations=[], work_item_id="synthetic:work-item-c3",
                      work_item_binding={"system": cka.SYNTHETIC_SYSTEM, "record_id": "synthetic:work-item-c3", "digest_domain": "sha256-exact-bytes", "sha256": sha(work)})
    obs["native_source"].update({"record_id": "synthetic:" + digest, "source_schema": cka.ARGANA_RECORD_SCHEMA})
    cases["03-observed-contract-with-evidenced-work-item"] = {"obs": obs, "source": src, "work": work}

    src = native_decision("synthetic:task-c4", "underdetermined", {"verdict": "U"})
    obs = observation("c4", "underdetermined", src, resolver_verdict="U", missing=[{"capability_token": "synthetic-capability"}])
    cases["04-observed-underdetermined-with-missing-and-no-work-item"] = {"obs": obs, "source": src}

    src = native_decision("synthetic:task-c5", "refusal", {"code": "SYNTHETIC_REFUSAL"})
    obs = observation("c5", "refusal", src, resolver_verdict="F", refusal_code="SYNTHETIC_REFUSAL")
    cases["05-observed-refusal-with-typed-code"] = {"obs": obs, "source": src}

    obs = {"schema": cka.SCHEMA_ID, "status": "unavailable", "reason": "outcome_not_persisted", "claims_scope": cka.CLAIMS_SCOPE, "claims": dict(CLAIMS)}
    cases["06-unavailable-with-typed-reason"] = {"obs": obs, "source": None}
    return cases


def variants() -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    valid = build()
    for name, case in valid.items():
        files[f"valid/{name}.json"] = dump(case["obs"])
        if case.get("source") is not None:
            files[f"valid/{name}{SOURCE}"] = case["source"]
        if case.get("work") is not None:
            files[f"valid/{name}{WORK}"] = case["work"]
    contract, contract_k = valid["01-observed-contract-with-verified-exact-bytes"], valid["02-observed-contract-k-keeps-its-obligation"]
    with_work, under, refusal = valid["03-observed-contract-with-evidenced-work-item"], valid["04-observed-underdetermined-with-missing-and-no-work-item"], valid["05-observed-refusal-with-typed-code"]
    unavailable = valid["06-unavailable-with-typed-reason"]

    def mutant(name: str, base: dict, edit, source: bytes | None | str = "keep", work: bytes | None | str = "keep") -> None:
        record = copy.deepcopy(base["obs"])
        edit(record)
        files[f"invalid/{name}.json"] = dump(record)
        src = base.get("source") if source == "keep" else source
        wrk = base.get("work") if work == "keep" else work
        if src is not None:
            files[f"invalid/{name}{SOURCE}"] = src
        if wrk is not None:
            files[f"invalid/{name}{WORK}"] = wrk

    def pop(*keys):
        return lambda r: [r.pop(k) for k in keys]

    mutant("missing_native_record_presented_as_observed", contract, pop("native_source"), source=None)
    mutant("native_bytes_do_not_match_the_digest", contract, lambda r: None, source=contract["source"] + b" ")
    mutant("work_item_bytes_do_not_match_the_digest", with_work, lambda r: None, work=with_work["work"] + b" ")

    def altered_native(label: str, edit, verdict: str = "T") -> dict:
        """A contract observation whose native bytes were edited in one place (after which sha256 is recomputed, so only that edit can be refused)."""
        src, digest = native_contract(label, verdict, [], f"synthetic:task-{label}")
        record = json.loads(src)
        edit(record)
        altered = dump(record)
        obs = observation(label, "contract", altered, contract_digest=digest, obligations=[])
        obs["native_source"].update({"record_id": "synthetic:" + digest, "source_schema": cka.ARGANA_RECORD_SCHEMA})
        return {"obs": obs, "source": altered}

    broken = altered_native("m1", lambda r: r["canonical"].update({"body_b64": base64.b64encode(b'{"synthetic_body":"altered"}').decode()}))
    mutant("contract_digest_is_not_the_digest_of_the_halves", broken, lambda r: None)
    mutant("forged_record_path_as_record_id", under, lambda r: r["native_source"].update({"record_id": "synthetic:../../etc/passwd"}))
    mutant("forged_issuer_unknown_source_system", under, lambda r: r["native_source"].update({"system": "trusted-issuer", "record_id": "record-without-prefix"}))
    mutant("synthetic_system_without_the_synthetic_prefix", under, lambda r: r["native_source"].update({"record_id": "record-without-prefix"}))
    mutant("native_system_with_the_synthetic_prefix", under, lambda r: r["native_source"].update({"system": "argana-contract-store"}))
    forged = json.loads(contract["source"])
    forged["schema"] = "SomethingElse/v1"
    forged_bytes = dump(forged)
    mutant("forged_native_record_of_another_schema", contract, lambda r: r["native_source"].update({"sha256": sha(forged_bytes)}), source=forged_bytes)
    mutant("work_item_id_without_source_proof", with_work, pop("work_item_binding"), work=None)
    mutant("work_item_binding_names_another_record", with_work, lambda r: r["work_item_binding"].update({"record_id": "synthetic:work-item-other"}))
    mutant("work_item_id_on_a_refusal", refusal, lambda r: r.update({"work_item_id": "synthetic:work-item-c5"}))
    mutant("unknown_schema_value", contract, lambda r: r.update({"schema": "KCAdmissionObservation/v2"}))
    mutant("contract_digest_on_a_refusal", refusal, lambda r: r.update({"contract_digest": contract["obs"]["contract_digest"]}))
    mutant("missing_on_a_contract", contract, lambda r: r.update({"missing": [{"capability_token": "synthetic-capability"}]}))
    mutant("refusal_code_on_an_underdetermined", under, lambda r: r.update({"refusal_code": "SYNTHETIC_REFUSAL"}))
    mutant("reason_on_an_observed_record", contract, lambda r: r.update({"reason": "no_native_record"}))
    mutant("outcome_on_an_unavailable_record", unavailable, lambda r: r.update({"resolver_outcome": "contract"}))
    mutant("contract_digest_on_an_unavailable_record", unavailable, lambda r: r.update({"contract_digest": contract["obs"]["contract_digest"]}))
    mutant("conflicting_message_identity", contract, lambda r: r.update({"message_id": "synthetic:another-record"}))
    mutant("admitted_true", contract, lambda r: r.update({"admitted": True}))
    mutant("authorized_true_in_claims", contract, lambda r: r["claims"].update({"runtime_authorization": True}))
    mutant("publishable_true_on_unavailable", unavailable, lambda r: r.update({"publishable": True}))
    mutant("claim_set_to_measured", contract, lambda r: r["claims"].update({"source_admission": "MEASURED"}))
    mutant("claim_set_to_ready", contract, lambda r: r["claims"].update({"issuer_authority": "READY"}))
    mutant("claim_missing", contract, lambda r: r["claims"].pop("publication"))
    mutant("claims_scope_widened", contract, lambda r: r.update({"claims_scope": "admission"}))
    mutant("unknown_extra_field", contract, lambda r: r.update({"issuer": "synthetic-issuer"}))
    mutant("unknown_extra_field_in_native_source", contract, lambda r: r["native_source"].update({"path": "/var/lib/synthetic"}))
    mutant("k_verdict_drops_the_obligations", contract_k, lambda r: r.update({"obligations": []}))
    mutant("obligations_differ_from_the_native_record", contract_k, lambda r: r.update({"obligations": [{"kind": "another-kind"}]}))
    mutant("verdict_differs_from_the_native_record", contract_k, lambda r: r.update({"resolver_verdict": "T"}))
    mutant("task_differs_from_the_native_record", under, lambda r: r.update({"subject": {"task_id": "synthetic:another-task"}}))
    mutant("outcome_differs_from_the_native_record", refusal, lambda r: r.update({"resolver_outcome": "underdetermined", "missing": [{"capability_token": "x"}]}) or r.pop("refusal_code"))
    mutant("recorded_at_differs_from_the_native_record", contract, lambda r: r["native_source"].update({"recorded_at": "2026-02-02T00:00:00Z"}))
    mutant("verdict_outside_the_enum", contract, lambda r: r.update({"resolver_verdict": "OK"}))
    mutant("refusal_code_not_a_typed_code", refusal, lambda r: r.update({"refusal_code": "refused it"}))
    mutant("underdetermined_without_missing", under, pop("missing"))
    mutant("unavailable_reason_outside_the_enum", unavailable, lambda r: r.update({"reason": "because"}))
    mutant("unavailable_without_a_reason", unavailable, pop("reason"))
    mutant("digest_domain_is_not_exact_bytes", contract, lambda r: r["native_source"].update({"digest_domain": "sha256-tree-manifest-v1"}))
    mutant("unknown_work_item_source", with_work, lambda r: r["work_item_binding"].update({"system": "trusted-tracker"}))
    mutant("contract_source_schema_absent", contract, lambda r: r["native_source"].pop("source_schema"))
    mutant("record_id_does_not_name_the_contract", contract, lambda r: r["native_source"].update({"record_id": "synthetic:another-contract"}))
    mutant("native_record_digest_field_differs", altered_native("m2", lambda r: r.update({"digest": "sha256:" + "0" * 64})), lambda r: None)
    mutant("native_record_without_a_task_id", altered_native("m3", lambda r: r["request"].pop("task_id")), lambda r: None)
    mutant("claims_not_an_object", contract, lambda r: r.update({"claims": None}))
    contract_bytes = files["valid/01-observed-contract-with-verified-exact-bytes.json"]
    files["invalid/duplicate_member.json"] = contract_bytes.replace(b'"status": "observed"', b'"status": "observed",\n  "status": "observed"', 1)
    files["invalid/not_json.json"] = b"not json\n"
    return files


def _expected() -> dict[str, str | None]:
    codes = {
        "missing_native_record_presented_as_observed": "KCAO-NATIVE-MISSING", "native_bytes_do_not_match_the_digest": "KCAO-BYTES-DIGEST",
        "work_item_bytes_do_not_match_the_digest": "KCAO-BYTES-DIGEST", "native_system_with_the_synthetic_prefix": "KCAO-FORGED",
        "unknown_work_item_source": "KCAO-FORGED", "contract_source_schema_absent": "KCAO-CONTRACT-DIGEST", "record_id_does_not_name_the_contract": "KCAO-FORGED",
        "native_record_digest_field_differs": "KCAO-FORGED", "native_record_without_a_task_id": "KCAO-NATIVE-MISMATCH", "claims_not_an_object": "KCAO-CLAIMS", "contract_digest_is_not_the_digest_of_the_halves": "KCAO-CONTRACT-DIGEST",
        "forged_record_path_as_record_id": "KCAO-FORGED", "forged_issuer_unknown_source_system": "KCAO-FORGED", "synthetic_system_without_the_synthetic_prefix": "KCAO-FORGED",
        "forged_native_record_of_another_schema": "KCAO-FORGED", "work_item_id_without_source_proof": "KCAO-WORKITEM-NO-PROOF", "work_item_binding_names_another_record": "KCAO-WORKITEM-NO-PROOF",
        "work_item_id_on_a_refusal": "KCAO-BRANCH", "unknown_schema_value": "KCAO-SCHEMA-ID", "contract_digest_on_a_refusal": "KCAO-BRANCH", "missing_on_a_contract": "KCAO-BRANCH",
        "refusal_code_on_an_underdetermined": "KCAO-BRANCH", "reason_on_an_observed_record": "KCAO-BRANCH", "outcome_on_an_unavailable_record": "KCAO-BRANCH",
        "contract_digest_on_an_unavailable_record": "KCAO-BRANCH", "conflicting_message_identity": "KCAO-IDENTITY-CONFLICT", "admitted_true": "KCAO-POSITIVE-FLAG",
        "authorized_true_in_claims": "KCAO-POSITIVE-FLAG", "publishable_true_on_unavailable": "KCAO-POSITIVE-FLAG", "claim_set_to_measured": "KCAO-CLAIMS", "claim_set_to_ready": "KCAO-CLAIMS",
        "claim_missing": "KCAO-CLAIMS", "claims_scope_widened": "KCAO-CLAIMS", "unknown_extra_field": "KCAO-SCHEMA", "unknown_extra_field_in_native_source": "KCAO-SCHEMA",
        "k_verdict_drops_the_obligations": "KCAO-SCHEMA", "obligations_differ_from_the_native_record": "KCAO-NATIVE-MISMATCH", "verdict_differs_from_the_native_record": "KCAO-NATIVE-MISMATCH",
        "task_differs_from_the_native_record": "KCAO-NATIVE-MISMATCH", "outcome_differs_from_the_native_record": "KCAO-NATIVE-MISMATCH", "recorded_at_differs_from_the_native_record": "KCAO-NATIVE-MISMATCH",
        "verdict_outside_the_enum": "KCAO-SCHEMA", "refusal_code_not_a_typed_code": "KCAO-SCHEMA", "underdetermined_without_missing": "KCAO-SCHEMA", "unavailable_reason_outside_the_enum": "KCAO-SCHEMA",
        "unavailable_without_a_reason": "KCAO-SCHEMA", "digest_domain_is_not_exact_bytes": "KCAO-SCHEMA", "duplicate_member": "KCAO-READ", "not_json": "KCAO-READ",
    }
    expected: dict[str, str | None] = {f"valid/{name}": None for name in build()}
    expected.update({f"invalid/{name}": code for name, code in codes.items()})
    return expected


EXPECTED = _expected()


def observations() -> dict[str, bytes]:
    """The observation files only (not the byte sidecars), keyed `valid/NAME` / `invalid/NAME`."""
    return {k[: -len(".json")]: v for k, v in variants().items() if not k.endswith((SOURCE, WORK))}


def sidecar(files: dict[str, bytes], name: str, suffix: str) -> bytes | None:
    return files.get(f"{name}{suffix}")


def write() -> None:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT)
    for name, data in variants().items():
        target = FIXTURE_ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (FIXTURE_ROOT / "README.md").write_text(
        "# Synthetic KCAdmissionObservation/v1 (CANDIDATE) records\n\nEvery file here is invented for this repository and is a fixture, not a native observation: the source system is "
        "`synthetic-fixture` and every record id starts `synthetic:`. `valid/` holds six records (observed `contract` with verified exact-byte provenance, a `K` contract that keeps its "
        "obligation, a contract with an evidenced work item, observed `underdetermined`, observed `refusal`, and `unavailable`); passing them is a statement about the checker's rules only, "
        "not about Argana, Muneral or any admission. `NAME.source.json` holds the exact synthetic native record bytes whose SHA-256 is `native_source.sha256`; `NAME.work-item.json` holds the "
        "exact synthetic work item record bytes. Each file under `invalid/` is a mutant with one defect and one expected refusal code (see `EXPECTED` in "
        "`tools/kc_admission_observation_fixture.py`). Regenerate with\n`python3 tools/kc_admission_observation_fixture.py write`; the unit tests fail if the committed files drift.\n",
        encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    else:
        print("usage: kc_admission_observation_fixture.py write", file=sys.stderr)
        raise SystemExit(2)
