#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate a KCAdmissionObservation/v1 (CANDIDATE) record: the cross-field rules a JSON Schema cannot express (KCLIVE-01, KC-Brain comment 6710410432).

    check_kc_admission_observation.py OBSERVATION.json [--source NATIVE_RECORD_BYTES] [--work-item MURAL_RECORD_BYTES]

The checker works from the files given and the schema in this repository alone: no network, no Argana, no Muneral. Order of work, fail-closed, first refusal wins:
the bytes are read strictly (one JSON object, no duplicate members, bounded), the schema selector must be exactly KCAdmissionObservation/v1, no boolean appears anywhere
(there is no authorized/admitted/publishable or generic success flag), the claims scope and the five claims are exactly the fixed NOT_MEASURED set, the fields of
each branch are exclusive, an observed record carries a native source, and only then does schema validation run. After the schema, identity and provenance are
checked: a path-like or unknown source, a conflicting message identity, a work item without source proof, the sha256-exact-bytes of the supplied native bytes, and
(for ArganaContractRecord/v1 bytes) that the canonical halves recompute to contract_digest and agree with the observation.

What a pass means: the record is well formed, honest about what it did not measure, and (when native bytes are supplied) agrees with those bytes. It never means
admission, authority, runtime authorization, delivery or publication. Without native bytes the pass is STRUCTURE ONLY and says so. A source named
synthetic-fixture is reported with a flag and is never a native observation. Every refusal carries a stable KCAO-... code.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_book_package as cbp  # noqa: E402  (strict JSON reader shared with the other validators)

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "kc-admission-observation.schema.json"
SCHEMA_ID = "KCAdmissionObservation/v1"
CLAIMS_SCOPE = "resolver-outcome-observation-only"
CLAIM_KEYS = ("issuer_authority", "source_admission", "runtime_authorization", "consumer_delivery", "publication")
MAX_BYTES = 1 << 20
SYNTHETIC_SYSTEM = "synthetic-fixture"
NATIVE_SYSTEMS = ("argana-contract-store",)
WORK_ITEM_SYSTEMS = ("muneral",)
ARGANA_RECORD_SCHEMA = "ArganaContractRecord/v1"
COMMON = {"schema", "status", "claims_scope", "claims"}
OBSERVED_COMMON = COMMON | {"subject", "native_source", "message_id", "resolver_outcome", "resolver_verdict"}
BRANCH_FIELDS = {"contract": {"contract_digest", "obligations", "work_item_id", "work_item_binding"}, "underdetermined": {"missing"}, "refusal": {"refusal_code"}}
ALL_BRANCH_FIELDS = set().union(*BRANCH_FIELDS.values())
UNAVAILABLE_FIELDS = COMMON | {"reason", "subject"}
FORBIDDEN_ON_UNAVAILABLE = {"native_source", "message_id", "resolver_outcome", "resolver_verdict"} | ALL_BRANCH_FIELDS


def _validator() -> jsonschema.Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def _has_bool(value) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, dict):
        return any(_has_bool(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_bool(v) for v in value)
    return False


def _read(data: bytes, name: str):
    if len(data) > MAX_BYTES:
        raise ValueError(f"{name} is at most {MAX_BYTES} bytes")
    return cbp.strict_json(data.decode("utf-8"), name)


def _pre_schema(record: dict) -> list[str]:
    """Refusals that must name their own cause before a generic schema error could hide it."""
    if record.get("schema") != SCHEMA_ID:
        return [f"KCAO-SCHEMA-ID: the selector {str(record.get('schema'))[:80]!r} is not {SCHEMA_ID}; a record is never read as the nearest known schema"]
    if _has_bool(record):
        return ["KCAO-POSITIVE-FLAG: a boolean appears in the record; v1 has no authorized/admitted/publishable or generic success flag"]
    claims = record.get("claims")
    if record.get("claims_scope") != CLAIMS_SCOPE or not isinstance(claims, dict) or set(claims) != set(CLAIM_KEYS) or any(claims[k] != "NOT_MEASURED" for k in claims):
        return [f"KCAO-CLAIMS: claims_scope must be {CLAIMS_SCOPE} and the five claims exactly {', '.join(CLAIM_KEYS)} = NOT_MEASURED"]
    status = record.get("status")
    if status == "unavailable":
        stray = sorted(set(record) & FORBIDDEN_ON_UNAVAILABLE)
        if stray:
            return [f"KCAO-BRANCH: an unavailable record carries {', '.join(stray)}; it forbids an outcome, a digest, a work item and any positive field"]
    elif status == "observed":
        if "native_source" not in record:
            return ["KCAO-NATIVE-MISSING: a record presented as observed has no native_source; with no durable native record the status is unavailable"]
        outcome = record.get("resolver_outcome")
        if outcome in BRANCH_FIELDS:
            stray = sorted((set(record) & ALL_BRANCH_FIELDS) - BRANCH_FIELDS[outcome])
            if stray:
                return [f"KCAO-BRANCH: an observed {outcome} record carries {', '.join(stray)} of another branch"]
            if "reason" in record:
                return ["KCAO-BRANCH: an observed record carries reason, which belongs to unavailable"]
            if "work_item_id" in record and "work_item_binding" not in record:
                return ["KCAO-WORKITEM-NO-PROOF: work_item_id has no work_item_binding; a resolver contract alone is not a work item"]
    return []


def inspect(data: bytes, source_bytes: bytes | None = None, work_item_bytes: bytes | None = None) -> tuple[list[str], list[str]]:
    """(problems, flags). Problems are `CODE: text` refusals; an empty list is a well-formed record. Flags are not refusals: they say what was not measured."""
    try:
        record = _read(data, "observation.json")
    except (cbp.PackageError, ValueError, UnicodeDecodeError, RecursionError) as exc:
        return [f"KCAO-READ: {exc}"], []
    if not isinstance(record, dict):
        return ["KCAO-SCHEMA: not a JSON object"], []
    problems = _pre_schema(record)
    if problems:
        return problems, []
    for error in sorted(_validator().iter_errors(record), key=lambda e: list(map(str, e.path))):
        problems.append(f"KCAO-SCHEMA: {'/'.join(str(p) for p in error.path) or '<root>'}: {error.message[:160]}")
    if problems:
        return problems, []
    flags: list[str] = []
    if record["status"] == "unavailable":
        return [], flags
    return _provenance(record, source_bytes, work_item_bytes, flags), flags


def _provenance(record: dict, source_bytes: bytes | None, work_item_bytes: bytes | None, flags: list[str]) -> list[str]:
    ns = record["native_source"]
    system, record_id = ns["system"], ns["record_id"]
    synthetic = system == SYNTHETIC_SYSTEM
    if re.search(r"[\\/]|\.\.", record_id):
        return [f"KCAO-FORGED: record_id {record_id[:80]!r} is a path, not an immutable record id"]
    if not synthetic and system not in NATIVE_SYSTEMS:
        return [f"KCAO-FORGED: source system {system!r} is not one this checker knows; a source label alone is not an issuer"]
    if synthetic != record_id.startswith("synthetic:"):
        return ["KCAO-FORGED: the synthetic-fixture system and the synthetic: record id prefix must appear together"]
    if "message_id" in record and record["message_id"] != record_id:
        return ["KCAO-IDENTITY-CONFLICT: message_id differs from native_source.record_id; one record must have one identity"]
    if synthetic:
        flags.append("KCAO-FLAG-SYNTHETIC-SOURCE: the source is a synthetic fixture, not a native observation")
    problems = _work_item(record, work_item_bytes, flags)
    if problems:
        return problems
    if source_bytes is None:
        flags.append("KCAO-FLAG-NATIVE-BYTES-NOT-SUPPLIED: the exact native bytes were not supplied, so provenance is NOT_MEASURED (structure only)")
        return []
    if hashlib.sha256(source_bytes).hexdigest() != ns["sha256"]:
        return ["KCAO-BYTES-DIGEST: native_source.sha256 is not the SHA-256 of the exact native bytes supplied"]
    try:
        native = _read(source_bytes, "native record")
    except (cbp.PackageError, ValueError, UnicodeDecodeError, RecursionError) as exc:
        return [f"KCAO-NATIVE-READ: the native bytes are not strict JSON: {exc}"]
    if not isinstance(native, dict):
        return ["KCAO-NATIVE-READ: the native record is not a JSON object"]
    return _against_native(record, native)


def _work_item(record: dict, work_item_bytes: bytes | None, flags: list[str]) -> list[str]:
    if "work_item_id" not in record:
        return []
    binding = record["work_item_binding"]
    synthetic = binding["system"] == SYNTHETIC_SYSTEM
    if binding["system"] not in WORK_ITEM_SYSTEMS and not synthetic:
        return [f"KCAO-FORGED: work item source {binding['system']!r} is not one this checker knows"]
    if binding["record_id"] != record["work_item_id"]:
        return ["KCAO-WORKITEM-NO-PROOF: work_item_binding names another record than work_item_id"]
    if synthetic:
        flags.append("KCAO-FLAG-SYNTHETIC-WORK-ITEM: the work item binding is a synthetic fixture")
    if work_item_bytes is None:
        flags.append("KCAO-FLAG-WORK-ITEM-BYTES-NOT-SUPPLIED: the exact work item record bytes were not supplied, so the binding is NOT_MEASURED")
    elif hashlib.sha256(work_item_bytes).hexdigest() != binding["sha256"]:
        return ["KCAO-BYTES-DIGEST: work_item_binding.sha256 is not the SHA-256 of the exact work item bytes supplied"]
    return []


def _against_native(record: dict, native: dict) -> list[str]:
    ns, outcome = record["native_source"], record["resolver_outcome"]
    request = native.get("request")
    native_task = native.get("task_id", request.get("task_id") if isinstance(request, dict) else None)
    if native_task is not None and native_task != record["subject"]["task_id"]:
        return ["KCAO-NATIVE-MISMATCH: the native record names another task than subject.task_id"]
    if "outcome" in native and native["outcome"] != outcome:
        return ["KCAO-NATIVE-MISMATCH: the native record names another outcome than resolver_outcome"]
    if outcome == "contract":
        if ns.get("source_schema") != ARGANA_RECORD_SCHEMA:
            return [f"KCAO-CONTRACT-DIGEST: contract_digest cannot be verified from bytes whose source_schema is not {ARGANA_RECORD_SCHEMA}"]
        return _argana_contract(record, native)
    return []


def _argana_contract(record: dict, native: dict) -> list[str]:
    digest, ns = record["contract_digest"], record["native_source"]
    if native.get("schema") != ARGANA_RECORD_SCHEMA:
        return [f"KCAO-FORGED: the native bytes are not a {ARGANA_RECORD_SCHEMA} record"]
    try:
        canonical = native["canonical"]
        halves = base64.b64decode(canonical["body_b64"], validate=True) + base64.b64decode(canonical["closure_manifest_b64"], validate=True)
    except Exception as exc:  # noqa: BLE001 — every shape failure is one typed refusal
        return [f"KCAO-NATIVE-READ: the canonical halves are unreadable: {exc.__class__.__name__}"]
    if "sha256:" + hashlib.sha256(halves).hexdigest() != digest:
        return ["KCAO-CONTRACT-DIGEST: contract_digest is not the SHA-256 of the canonical halves in the native record"]
    if native.get("digest") != digest or not ns["record_id"].endswith(digest):
        return ["KCAO-FORGED: the native record digest and the record id do not name the observed contract"]
    task = (native.get("request") or {}).get("task_id")
    if task != record["subject"]["task_id"]:
        return ["KCAO-NATIVE-MISMATCH: the native record names another task than subject.task_id"]
    verdict = (native.get("kc2") or {}).get("verdict")
    if "resolver_verdict" in record and verdict != record["resolver_verdict"]:
        return ["KCAO-NATIVE-MISMATCH: resolver_verdict differs from the verdict in the native record"]
    if [o.get("kind") for o in native.get("obligations", [])] != [o["kind"] for o in record["obligations"]]:
        return ["KCAO-NATIVE-MISMATCH: the obligations differ from the native record; existing obligations are never dropped"]
    if "recorded_at" in ns and native.get("stored_at_utc") != ns["recorded_at"]:
        return ["KCAO-NATIVE-MISMATCH: recorded_at differs from the time stored in the native record"]
    return []


def check_observation(data: bytes, source_bytes: bytes | None = None, work_item_bytes: bytes | None = None) -> list[str]:
    return inspect(data, source_bytes, work_item_bytes)[0]


def main(argv: list[str]) -> int:
    args = argv[1:]
    paths: dict[str, str] = {}
    try:
        obs = args.pop(0)
        while args:
            key = args.pop(0)
            if key not in ("--source", "--work-item") or key in paths:
                raise IndexError
            paths[key] = args.pop(0)
    except IndexError:
        print("usage: check_kc_admission_observation.py OBSERVATION.json [--source NATIVE_BYTES] [--work-item WORK_ITEM_BYTES]", file=sys.stderr)
        return 2
    try:
        data = Path(obs).read_bytes()
        source = Path(paths["--source"]).read_bytes() if "--source" in paths else None
        work = Path(paths["--work-item"]).read_bytes() if "--work-item" in paths else None
    except OSError as exc:
        print(f"KCAO_FAIL KCAO-READ: {exc}")
        return 1
    problems, flags = inspect(data, source, work)
    if problems:
        for p in problems:
            print(f"KCAO_FAIL {p}")
        return 1
    for f in flags:
        print(f"KCAO_FLAG {f}")
    print("KCAO_PASS (form and, where bytes were supplied, agreement with those bytes; never admission, authority, authorization, delivery or publication)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
