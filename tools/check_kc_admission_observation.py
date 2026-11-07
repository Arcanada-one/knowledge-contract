#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate a KCAdmissionObservation/v1 (CANDIDATE) record: the cross-field rules a JSON Schema cannot express (KCLIVE-01; KC-Brain 6710410432 and its review 6711021786).

    check_kc_admission_observation.py --mode structure-only|strict-evidence|diagnostic-agreement [--fixture] [--require-work-item] OBSERVATION.json [--source NATIVE_BYTES] [--work-item WORK_ITEM_BYTES]

Three entry points, never one that can drop another's flags (`check_structure`, `check_strict`, `check_diagnostic`; each returns a `Result` that names its mode and its level):

* structure-only: the record is well formed, honest about what it did not measure, and policy-clean. It reports ONLY structural validity (level `structure-only`); it never
  looks at native bytes and says so in a flag. It cannot be read as provenance.
* strict-evidence: the exact native bytes MUST be supplied. Their SHA-256 is compared with native_source.sha256, the same bytes are parsed once, the (system, source_schema)
  pair must be a SUPPORTED native source profile, and EVERY fact the observation emits (task, outcome, verdict, time, schema, contract halves and digest, obligations, missing,
  refusal code) is compared with that source. A fact the source lacks, or states differently, is a refusal; a genuinely recorded verdict must appear in the projection.
  Without native bytes strict mode is a typed refusal, never a pass. KC-Brain 6711755408 (choice b): a digest-named mutable `ArganaContractRecord/v1` is NOT an admissible strict-evidence
  source; a hash of bytes sampled now is content agreement only. Strict mode therefore never returns a pass for it: explicit mutable bytes are refused with `KCAO-SOURCE-MUTABLE`,
  and no retained event source at all is the typed unavailable `exact_bytes_unrecoverable`. No immutable source profile is registered (an `ArganaIntakeSnapshot/v1` candidate is not one:
  `KCAO-NATIVE-PROFILE`, `unsupported_source_shape`), so the only strict pass is the synthetic `fixture-evidence`.
* diagnostic-agreement: the same comparison of every emitted fact with the mutable bytes, kept for diagnosis only. Its level is `diagnostic-content-agreement`, it carries
  `KCAO-FLAG-NON-ADMISSIVE`, it is never `passed`, and its exit code is 5, not 0. It is not strict evidence and cannot be read as provenance or as a source observation.

Source time (KC-Brain 6711021786 choice 1, fail-closed reading; provisional, see the PR body): a supported source that carries `stored_at_utc` requires the observation to carry the same
string as `native_source.recorded_at`, exactly as stored (producer time, never the observer's receipt time); omitting a known source time is `KCAO-NATIVE-MISMATCH`. A source without a time
leaves `recorded_at` absent, and that is accepted.

Supported profiles. `argana-contract-store` + `ArganaContractRecord/v1` supports ONLY the `contract` branch and is MUTABLE (the digest-named record is mutable metadata, not an immutable intake
event): diagnostic only, never strict. Non-contract branches have no durable native source yet, so only the synthetic profile `SyntheticNativeDecision/v1` can carry
them, and only in `--fixture` mode. The synthetic labels (system `synthetic-fixture`, id prefix `synthetic:`) and the work-item binding (`SyntheticWorkItemRecord/v1`; no native
binding profile is approved) are valid ONLY with `--fixture`; their pass level is `fixture-evidence`, never a native observation. Without `--fixture` a record that carries
work_item_id/work_item_binding is refused, and a consumer that requires the binding (`--require-work-item`) gets a typed `unavailable` / `native_binding_unverified`.

Exit codes: 0 pass, 1 refusal (every refusal carries a stable KCAO-... code), 2 usage, 3 unavailable (no retained source, or the consumer's requirement is unmet), 4 operational error (IO),
5 diagnostic agreement (non-admissive; never a pass), each distinct from a refusal. Reads of the observation and of each sidecar are bounded. A pass never means admission, authority, runtime authorization, delivery or publication.
"""

from __future__ import annotations

import base64
import errno
import hashlib
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
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
ARGANA_SYSTEM = "argana-contract-store"
NATIVE_SYSTEMS = (ARGANA_SYSTEM,)
MUNERAL_SYSTEM = "muneral"
ARGANA_RECORD_SCHEMA = "ArganaContractRecord/v1"
SYNTHETIC_DECISION_SCHEMA = "SyntheticNativeDecision/v1"
SYNTHETIC_WORK_ITEM_SCHEMA = "SyntheticWorkItemRecord/v1"
VERDICTS = ("T", "K", "U", "F")
MODES = ("structure-only", "strict-evidence", "diagnostic-agreement")
REASONS = ("no_native_record", "outcome_not_persisted", "record_unreadable", "read_path_not_opted_in", "exact_bytes_unrecoverable",
           "native_record_invalid", "native_binding_unverified", "unsupported_source_shape")
COMMON = {"schema", "status", "claims_scope", "claims"}
OBSERVED_COMMON = COMMON | {"subject", "native_source", "resolver_outcome", "resolver_verdict"}
BRANCH_FIELDS = {"contract": {"contract_digest", "obligations", "work_item_id", "work_item_binding"}, "underdetermined": {"missing"}, "refusal": {"refusal_code"}}
ALL_BRANCH_FIELDS = set().union(*BRANCH_FIELDS.values())
UNAVAILABLE_FIELDS = COMMON | {"reason", "subject"}
FORBIDDEN_ON_UNAVAILABLE = {"native_source", "resolver_outcome", "resolver_verdict"} | ALL_BRANCH_FIELDS
READ_ERRORS = (cbp.PackageError, ValueError, UnicodeDecodeError, RecursionError, TypeError)

# Levels a Result can have. Only the last two follow a comparison with native bytes; `fixture-evidence` is synthetic and `diagnostic-content-agreement` is explicitly non-admissive.
# There is deliberately no level for a strict native pass: no immutable source profile is registered (KC-Brain 6711755408).
LEVEL_REFUSED = "refused"
LEVEL_STRUCTURE = "structure-only"
LEVEL_UNAVAILABLE_RECORD = "unavailable-record"
LEVEL_UNAVAILABLE = "unavailable"
LEVEL_FIXTURE = "fixture-evidence"
LEVEL_DIAGNOSTIC = "diagnostic-content-agreement"

# Refusal codes that correspond to a typed `unavailable.reason` a producer would use after the same attempt (the checker itself only rejects).
CODE_TO_REASON = {"KCAO-NATIVE-READ": "native_record_invalid", "KCAO-NATIVE-INVALID": "native_record_invalid", "KCAO-NATIVE-UNSUPPORTED-SHAPE": "unsupported_source_shape",
                  "KCAO-NATIVE-PROFILE": "unsupported_source_shape"}


@dataclass(frozen=True)
class Result:
    """The one outcome type. `problems` are `CODE: text` refusals; `flags` say what was not measured; `level` says what a pass is worth; `unavailable` is a typed unavailable record."""

    problems: tuple[str, ...]
    flags: tuple[str, ...]
    mode: str
    level: str
    unavailable: dict | None = None

    @property
    def refused(self) -> bool:
        return bool(self.problems)

    @property
    def passed(self) -> bool:
        """A pass is neither a refusal, nor unavailable, nor a diagnostic agreement (which is non-admissive by definition)."""
        return not self.problems and self.unavailable is None and self.level != LEVEL_DIAGNOSTIC

    @property
    def codes(self) -> set[str]:
        return {p.split(":", 1)[0] for p in self.problems}


def _refuse(mode: str, *problems: str) -> Result:
    return Result(tuple(problems), (), mode, LEVEL_REFUSED)


def unavailable_record(reason: str, requested_task_id: str | None = None) -> dict:
    """A typed unavailable observation. `subject`, when given, is the REQUESTED target only; it is never an observed identity."""
    if reason not in REASONS:
        raise ValueError(f"unknown unavailable reason {reason!r}")
    record = {"schema": SCHEMA_ID, "status": "unavailable", "reason": reason, "claims_scope": CLAIMS_SCOPE, "claims": {k: "NOT_MEASURED" for k in CLAIM_KEYS}}
    if requested_task_id is not None:
        record["subject"] = {"task_id": requested_task_id}
    return record


_VALIDATOR = None


def _validator() -> jsonschema.Draft202012Validator:
    global _VALIDATOR
    if _VALIDATOR is None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        _VALIDATOR = jsonschema.Draft202012Validator(schema)
    return _VALIDATOR


def _has_bool(value) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, dict):
        return any(_has_bool(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_bool(v) for v in value)
    return False


def _has_float(value) -> bool:
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(_has_float(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_float(v) for v in value)
    return False


def _read(data: bytes, name: str):
    """Bounded: the size is checked before any decode, parse or hash."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes")
    if len(data) > MAX_BYTES:
        raise ValueError(f"{name} is at most {MAX_BYTES} bytes")
    return cbp.strict_json(bytes(data).decode("utf-8"), name)


def _bounded(data, name: str) -> None:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes")
    if len(data) > MAX_BYTES:
        raise ValueError(f"{name} is at most {MAX_BYTES} bytes")


def _pre_schema(record: dict) -> list[str]:
    """Refusals that must name their own cause before a generic schema error could hide it. Every access is type-guarded: a valid JSON of any shape reaches a typed refusal."""
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
        if isinstance(outcome, str) and outcome in BRANCH_FIELDS:
            stray = sorted((set(record) & ALL_BRANCH_FIELDS) - BRANCH_FIELDS[outcome])
            if stray:
                return [f"KCAO-BRANCH: an observed {outcome} record carries {', '.join(stray)} of another branch"]
            if "reason" in record:
                return ["KCAO-BRANCH: an observed record carries reason, which belongs to unavailable"]
            if "work_item_id" in record and "work_item_binding" not in record:
                return ["KCAO-WORKITEM-NO-PROOF: work_item_id has no work_item_binding; a resolver contract alone is not a work item"]
    return []


# ---------------------------------------------------------------- entry points

def check_structure(data: bytes, *, fixture: bool = False, require_work_item: bool = False) -> Result:
    """STRUCTURE ONLY. Reports structural validity and nothing about native bytes; the Result says `structure-only` and carries the NOT_MEASURED flag."""
    return _guarded(data, None, None, "structure-only", fixture, require_work_item)


def check_strict(data: bytes, source_bytes: bytes | None, work_item_bytes: bytes | None = None, *, fixture: bool = False, require_work_item: bool = False) -> Result:
    """STRICT EVIDENCE. Without the exact native bytes this is a typed refusal. With them every emitted fact is compared with the source profile, but a MUTABLE source
    (the digest-named ArganaContractRecord/v1) is never admissible: explicit bytes are refused (KCAO-SOURCE-MUTABLE), no retained source is the typed unavailable."""
    return _guarded(data, source_bytes, work_item_bytes, "strict-evidence", fixture, require_work_item)


def check_diagnostic(data: bytes, source_bytes: bytes | None, work_item_bytes: bytes | None = None, *, fixture: bool = False, require_work_item: bool = False) -> Result:
    """DIAGNOSTIC CONTENT AGREEMENT. The same comparison as strict evidence, also for a mutable source, but the result is explicitly NON-ADMISSIVE: its own level and flag,
    never `passed`. It is separate from strict evidence and never a substitute for it."""
    return _guarded(data, source_bytes, work_item_bytes, "diagnostic-agreement", fixture, require_work_item)


def _guarded(data, source_bytes, work_item_bytes, mode: str, fixture: bool, require_work_item: bool) -> Result:
    try:
        return _run(data, source_bytes, work_item_bytes, mode, bool(fixture), bool(require_work_item))
    except RecursionError:
        return _refuse(mode, "KCAO-READ: the JSON nests too deeply to read")
    except Exception as exc:  # noqa: BLE001 — a last resort so no input shape ever escapes as a traceback; a specific guard must fire first
        return _refuse(mode, f"KCAO-INTERNAL: an unexpected {exc.__class__.__name__} reached the outer guard")


def _run(data, source_bytes, work_item_bytes, mode: str, fixture: bool, require_work_item: bool) -> Result:
    try:
        record = _read(data, "observation.json")
    except READ_ERRORS as exc:
        return _refuse(mode, f"KCAO-READ: {exc}")
    if not isinstance(record, dict):
        return _refuse(mode, "KCAO-SCHEMA: not a JSON object")
    problems = _pre_schema(record)
    if problems:
        return _refuse(mode, *problems)
    for error in sorted(_validator().iter_errors(record), key=lambda e: list(map(str, e.path))):
        problems.append(f"KCAO-SCHEMA: {'/'.join(str(p) for p in error.path) or '<root>'}: {error.message[:160]}")
    if problems:
        return _refuse(mode, *problems)
    if record["status"] == "unavailable":
        unavailable = record if require_work_item else None
        return Result((), (), mode, LEVEL_UNAVAILABLE_RECORD, unavailable)
    flags: list[str] = []
    problems = _policy(record, fixture, flags)
    if problems:
        return _refuse(mode, *problems)
    if mode == "structure-only":
        flags.append("KCAO-FLAG-STRUCTURE-ONLY: only the structure was checked; the native bytes were not read, so provenance and every comparison with the source are NOT_MEASURED")
        if "work_item_id" in record:
            flags.append("KCAO-FLAG-WORK-ITEM-BYTES-NOT-SUPPLIED: the work item bytes were not read, so the binding is NOT_MEASURED")
        return _finish(record, flags, mode, LEVEL_STRUCTURE, require_work_item, verified_binding=False)
    if mode == "strict-evidence" and not fixture and _mutable(record):
        return _mutable_source(record, source_bytes, flags)
    problems = _evidence(record, source_bytes, work_item_bytes, fixture, flags)
    if problems:
        return _refuse(mode, *problems)
    if mode == "diagnostic-agreement":
        flags.append("KCAO-FLAG-NON-ADMISSIVE: diagnostic content agreement only; it is not strict evidence, not a source observation, and never admission, authority, authorization, delivery or publication")
        return _finish(record, flags, mode, LEVEL_DIAGNOSTIC, require_work_item, verified_binding="work_item_id" in record)
    return _finish(record, flags, mode, LEVEL_FIXTURE, require_work_item, verified_binding="work_item_id" in record)


def _mutable(record: dict) -> bool:
    ns = record["native_source"]
    profile = PROFILES.get((ns["system"], ns.get("source_schema")))
    return bool(profile and profile["mutable"])


def _mutable_source(record: dict, source_bytes, flags: list[str]) -> Result:
    """KC-Brain 6711755408 (b): a digest-named mutable record is not an admissible strict-evidence source. No retained event source = typed unavailable; explicit bytes = refusal."""
    flags.append("KCAO-FLAG-MUTABLE-LOCATOR: a digest-named ArganaContractRecord is mutable metadata, not an immutable intake event; a matching hash is content agreement only")
    if source_bytes is None:
        unavailable = unavailable_record("exact_bytes_unrecoverable", record["subject"]["task_id"])
        flags.append("KCAO-FLAG-NO-RETAINED-SOURCE: no retained event source was supplied for a record that names a mutable locator")
        return Result((), tuple(flags), "strict-evidence", LEVEL_UNAVAILABLE, unavailable)
    return _refuse("strict-evidence", "KCAO-SOURCE-MUTABLE: a digest-named mutable ArganaContractRecord/v1 is not an admissible strict-evidence source; "
                   "matching bytes are content agreement only (use diagnostic-agreement, which is non-admissive)")


def _finish(record: dict, flags: list[str], mode: str, level: str, require_work_item: bool, verified_binding: bool) -> Result:
    if require_work_item and not verified_binding:
        unavailable = unavailable_record("native_binding_unverified", record["subject"]["task_id"])
        flags.append("KCAO-FLAG-BINDING-REQUIRED: the consumer requires a verified work item binding; none is verified")
        return Result((), tuple(flags), mode, LEVEL_UNAVAILABLE, unavailable)
    return Result((), tuple(flags), mode, level)


# ---------------------------------------------------------------- policy: identity, synthetic labels, work-item gate (no bytes needed)

def _policy(record: dict, fixture: bool, flags: list[str]) -> list[str]:
    ns = record["native_source"]
    system, record_id = ns["system"], ns["record_id"]
    synthetic = system == SYNTHETIC_SYSTEM
    if re.search(r"[\\/]|\.\.", record_id):
        return [f"KCAO-FORGED: record_id {record_id[:80]!r} is a path, not an immutable record id"]
    if not synthetic and system not in NATIVE_SYSTEMS:
        return [f"KCAO-FORGED: source system {system!r} is not one this checker knows; a source label alone is not an issuer"]
    if synthetic != record_id.startswith("synthetic:"):
        return ["KCAO-FORGED: the synthetic-fixture system and the synthetic: record id prefix must appear together"]
    if synthetic and not fixture:
        return ["KCAO-SYNTHETIC-NOT-FIXTURE: a synthetic label is valid only in explicit fixture mode and is never promoted to a real observation"]
    if synthetic:
        flags.append("KCAO-FLAG-SYNTHETIC-SOURCE: the source is a synthetic fixture, not a native observation")
    if "work_item_id" in record:
        binding = record["work_item_binding"]
        bsystem = binding["system"]
        if bsystem != SYNTHETIC_SYSTEM and bsystem != MUNERAL_SYSTEM:
            return [f"KCAO-FORGED: work item source {bsystem!r} is not one this checker knows"]
        if bsystem == SYNTHETIC_SYSTEM and not fixture:
            return ["KCAO-SYNTHETIC-NOT-FIXTURE: a synthetic work item binding is valid only in explicit fixture mode"]
        if bsystem == MUNERAL_SYSTEM:
            return ["KCAO-WORKITEM-NO-PROFILE: no native work item binding profile is approved; the live, non-fixture record must omit work_item_id and work_item_binding"]
        if not synthetic:
            return ["KCAO-FORGED: a synthetic work item binding cannot hang on a non-synthetic native source"]
        flags.append("KCAO-FLAG-SYNTHETIC-WORK-ITEM: the work item binding is a synthetic fixture")
    return []


# ---------------------------------------------------------------- strict evidence

def _evidence(record: dict, source_bytes, work_item_bytes, fixture: bool, flags: list[str]) -> list[str]:
    ns = record["native_source"]
    if source_bytes is None:
        return ["KCAO-STRICT-NO-NATIVE-BYTES: strict-evidence needs the exact native bytes; without them there is nothing to verify, and that is never a pass"]
    try:
        _bounded(source_bytes, "native record")
    except (ValueError, TypeError) as exc:
        return [f"KCAO-NATIVE-READ: {exc}"]
    if hashlib.sha256(source_bytes).hexdigest() != ns["sha256"]:
        return ["KCAO-BYTES-DIGEST: native_source.sha256 is not the SHA-256 of the exact native bytes supplied"]
    try:
        native = _read(source_bytes, "native record")
    except READ_ERRORS as exc:
        return [f"KCAO-NATIVE-READ: the native bytes are not strict JSON: {exc}"]
    if not isinstance(native, dict):
        return ["KCAO-NATIVE-READ: the native record is not a JSON object"]
    profile = PROFILES.get((ns["system"], ns.get("source_schema")))
    if profile is None:
        return [f"KCAO-NATIVE-PROFILE: ({ns['system']}, {str(ns.get('source_schema'))[:80]}) is not a supported native source profile; an unsupported or absent source schema is never guessed"]
    if native.get("schema") != ns["source_schema"]:
        return [f"KCAO-FORGED: the native bytes are not a {ns['source_schema']} record"]
    if record["resolver_outcome"] not in profile["outcomes"]:
        return [f"KCAO-NATIVE-MISMATCH: a {ns['source_schema']} record can support only the {'/'.join(sorted(profile['outcomes']))} branch, not {record['resolver_outcome']}"]
    if ns["source_schema"] == ARGANA_RECORD_SCHEMA:
        flags.append("KCAO-FLAG-MUTABLE-LOCATOR: a digest-named ArganaContractRecord is mutable metadata, not an immutable intake event; the immutable snapshot, "
                     "source authentication and every claim stay NOT_MEASURED")
    problems = profile["verify"](record, native)
    if problems:
        return problems
    return _work_item(record, work_item_bytes) if "work_item_id" in record else []


def _verdict(record: dict, native_verdict) -> list[str]:
    """A verdict the source genuinely recorded must appear in the projection and be equal; an emitted verdict the source lacks is refused."""
    if native_verdict is None:
        if "resolver_verdict" in record:
            return ["KCAO-NATIVE-MISMATCH: resolver_verdict is emitted but the native record records no verdict"]
        return []
    if native_verdict not in VERDICTS:
        return ["KCAO-NATIVE-INVALID: the native verdict is not one of T, K, U, F"]
    if "resolver_verdict" not in record:
        return ["KCAO-NATIVE-MISMATCH: the native record records a verdict that the observation omits; a recorded verdict is never dropped"]
    if record["resolver_verdict"] != native_verdict:
        return ["KCAO-NATIVE-MISMATCH: resolver_verdict differs from the verdict in the native record"]
    return []


def _time(record: dict, native_time) -> list[str]:
    ns = record["native_source"]
    if native_time is not None and not isinstance(native_time, str):
        return ["KCAO-NATIVE-INVALID: the native stored time is not a string"]
    if native_time is not None and "recorded_at" not in ns:
        return ["KCAO-NATIVE-MISMATCH: the native record stores a time (stored_at_utc) that the observation omits; a known source time is copied, never dropped"]
    if "recorded_at" in ns and native_time != ns["recorded_at"]:
        return ["KCAO-NATIVE-MISMATCH: recorded_at differs from, or is absent in, the time stored in the native record"]
    return []


def _conditions(items, allowed: str, what: str) -> tuple[list[dict] | None, list[str]]:
    """Native condition items (obligations, missing) as `[{allowed: str}]`. A non-list or non-object item is invalid; an extra field is an unsupported shape, never dropped."""
    if not isinstance(items, list):
        return None, [f"KCAO-NATIVE-INVALID: native {what} is not a list"]
    out = []
    for item in items:
        if not isinstance(item, dict):
            return None, [f"KCAO-NATIVE-INVALID: a native {what} item is not an object"]
        extra = sorted(set(item) - {allowed})
        if extra:
            return None, [f"KCAO-NATIVE-UNSUPPORTED-SHAPE: a native {what} item carries {', '.join(extra)[:80]}; the projection keeps only {allowed}, and nothing is silently dropped"]
        if not isinstance(item.get(allowed), str):
            return None, [f"KCAO-NATIVE-INVALID: a native {what} item has no string {allowed}"]
        out.append({allowed: item[allowed]})
    return out, []


def _canonical_half(value, name: str) -> bytes:
    if not isinstance(value, str):
        raise TypeError(f"{name} is not a string")
    raw = base64.b64decode(value, validate=True)
    parsed = cbp.strict_json(raw.decode("utf-8"), name)
    if not isinstance(parsed, dict):
        raise ValueError(f"{name} is not a JSON object")
    if _has_float(parsed):
        raise ValueError(f"{name} holds a float; canonical JSON forbids floats")
    if json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii") != raw:
        raise ValueError(f"{name} is not in canonical JSON form")
    return raw


def _verify_argana(record: dict, native: dict) -> list[str]:
    digest, ns = record["contract_digest"], record["native_source"]
    canonical = native.get("canonical")
    if not isinstance(canonical, dict):
        return ["KCAO-NATIVE-INVALID: the native record has no canonical object"]
    try:
        halves = _canonical_half(canonical.get("body_b64"), "canonical body") + _canonical_half(canonical.get("closure_manifest_b64"), "canonical closure manifest")
    except READ_ERRORS as exc:
        return [f"KCAO-NATIVE-INVALID: the canonical halves are not strict canonical JSON objects: {exc.__class__.__name__}: {str(exc)[:80]}"]
    if "sha256:" + hashlib.sha256(halves).hexdigest() != digest:
        return ["KCAO-CONTRACT-DIGEST: contract_digest is not the SHA-256 of the canonical halves in the native record"]
    if native.get("digest") != digest or not ns["record_id"].endswith(digest):
        return ["KCAO-FORGED: the native record digest and the record id do not name the observed contract"]
    request, kc2 = native.get("request"), native.get("kc2")
    if not isinstance(request, dict) or not isinstance(kc2, dict):
        return ["KCAO-NATIVE-INVALID: the native request and kc2 members must be objects"]
    task = request.get("task_id")
    if not isinstance(task, str):
        return ["KCAO-NATIVE-INVALID: the native record carries no string request.task_id"]
    if task != record["subject"]["task_id"]:
        return ["KCAO-NATIVE-MISMATCH: the native record names another task than subject.task_id"]
    problems = _verdict(record, kc2.get("verdict"))
    if problems:
        return problems
    wanted, problems = _conditions(native.get("obligations"), "kind", "obligations")
    if problems:
        return problems
    if wanted != record["obligations"]:
        return ["KCAO-NATIVE-MISMATCH: the obligations differ from the native record; existing obligations are never dropped"]
    return _time(record, native.get("stored_at_utc"))


def _verify_decision(record: dict, native: dict) -> list[str]:
    """The synthetic non-contract profile: every fact an observation asserts must be carried by the source."""
    outcome = record["resolver_outcome"]
    absent = sorted({"schema", "task_id", "outcome"} - set(native))
    if absent:
        return [f"KCAO-NATIVE-INVALID: the native decision lacks the mandatory field(s) {', '.join(absent)}"]
    if not isinstance(native["task_id"], str) or not isinstance(native["outcome"], str):
        return ["KCAO-NATIVE-INVALID: the native task_id and outcome must be strings"]
    if native["task_id"] != record["subject"]["task_id"]:
        return ["KCAO-NATIVE-MISMATCH: the native record names another task than subject.task_id"]
    if native["outcome"] != outcome:
        return ["KCAO-NATIVE-MISMATCH: the native record names another outcome than resolver_outcome"]
    branch_key = "missing" if outcome == "underdetermined" else "refusal_code"
    extra = sorted(set(native) - {"schema", "task_id", "outcome", "verdict", "stored_at_utc", branch_key})
    if extra:
        return [f"KCAO-NATIVE-UNSUPPORTED-SHAPE: the synthetic native decision carries {', '.join(extra)[:80]}, which this profile does not project"]
    if branch_key not in native:
        return [f"KCAO-NATIVE-INVALID: the native {outcome} decision lacks {branch_key}"]
    problems = _verdict(record, native.get("verdict"))
    if problems:
        return problems
    if outcome == "underdetermined":
        wanted, problems = _conditions(native["missing"], "capability_token", "missing")
        if problems:
            return problems
        if wanted != record["missing"]:
            return ["KCAO-NATIVE-MISMATCH: the missing capabilities differ from the complete native payload"]
    else:
        if not isinstance(native["refusal_code"], str):
            return ["KCAO-NATIVE-INVALID: the native refusal_code is not a string"]
        if native["refusal_code"] != record["refusal_code"]:
            return ["KCAO-NATIVE-MISMATCH: refusal_code differs from the native refusal code; uppercase syntax alone is not evidence"]
    return _time(record, native.get("stored_at_utc"))


PROFILES = {
    (ARGANA_SYSTEM, ARGANA_RECORD_SCHEMA): {"fixture_only": False, "mutable": True, "outcomes": frozenset({"contract"}), "verify": _verify_argana},
    (SYNTHETIC_SYSTEM, ARGANA_RECORD_SCHEMA): {"fixture_only": True, "mutable": False, "outcomes": frozenset({"contract"}), "verify": _verify_argana},
    (SYNTHETIC_SYSTEM, SYNTHETIC_DECISION_SCHEMA): {"fixture_only": True, "mutable": False, "outcomes": frozenset({"underdetermined", "refusal"}), "verify": _verify_decision},
}


def _work_item(record: dict, work_item_bytes) -> list[str]:
    """Fixture mode only. The bytes that are hashed are the bytes that are parsed; the record must name the work item, the contract, the task and THIS intake."""
    binding = record["work_item_binding"]
    if work_item_bytes is None:
        return ["KCAO-WORKITEM-NO-PROOF: the work item record bytes were not supplied, so the binding is unproven"]
    try:
        _bounded(work_item_bytes, "work item record")
    except (ValueError, TypeError) as exc:
        return [f"KCAO-WORKITEM-INVALID: {exc}"]
    if hashlib.sha256(work_item_bytes).hexdigest() != binding["sha256"]:
        return ["KCAO-BYTES-DIGEST: work_item_binding.sha256 is not the SHA-256 of the exact work item bytes supplied"]
    try:
        work = _read(work_item_bytes, "work item record")
    except READ_ERRORS as exc:
        return [f"KCAO-WORKITEM-INVALID: the work item bytes are not strict JSON: {exc}"]
    keys = {"schema", "record_id", "work_item_id", "contract_digest", "task_id", "intake_record_id"}
    if not isinstance(work, dict) or work.get("schema") != SYNTHETIC_WORK_ITEM_SCHEMA or set(work) != keys or any(not isinstance(work[k], str) for k in keys):
        return [f"KCAO-WORKITEM-INVALID: the work item bytes are not a {SYNTHETIC_WORK_ITEM_SCHEMA} record with exactly its string fields"]
    if work["record_id"] != binding["record_id"]:
        return ["KCAO-WORKITEM-MISMATCH: the work item record is not the evidence record that work_item_binding names"]
    if work["work_item_id"] != record["work_item_id"]:
        return ["KCAO-WORKITEM-MISMATCH: the work item record names another work item than work_item_id"]
    if work["contract_digest"] != record["contract_digest"]:
        return ["KCAO-WORKITEM-MISMATCH: the work item record names another contract than contract_digest"]
    if work["task_id"] != record["subject"]["task_id"]:
        return ["KCAO-WORKITEM-MISMATCH: the work item record names another task than subject.task_id"]
    if work["intake_record_id"] != record["native_source"]["record_id"]:
        return ["KCAO-WORKITEM-MISMATCH: the work item record joins another intake than native_source.record_id"]
    return []


# ---------------------------------------------------------------- command line

USAGE = ("usage: check_kc_admission_observation.py --mode structure-only|strict-evidence|diagnostic-agreement [--fixture] [--require-work-item] OBSERVATION.json "
         "[--source NATIVE_BYTES] [--work-item WORK_ITEM_BYTES]  (the byte options belong to strict-evidence and diagnostic-agreement)")


def _read_file(path: str) -> bytes:
    """At most MAX_BYTES + 1 bytes of a regular file; the caller's size check then refuses the excess. A non-regular file is an operational error."""
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError(errno.EINVAL, "not a regular file", path)
        chunks, left = [], MAX_BYTES + 1
        while left > 0:
            chunk = os.read(fd, min(left, 1 << 16))
            if not chunk:
                break
            chunks.append(chunk)
            left -= len(chunk)
        return b"".join(chunks)
    finally:
        os.close(fd)


def _parse_args(args: list[str]) -> tuple[str, dict[str, str], set[str]]:
    paths: dict[str, str] = {}
    flags: set[str] = set()
    obs = None
    while args:
        token = args.pop(0)
        if token in ("--fixture", "--require-work-item"):
            if token in flags:
                raise IndexError
            flags.add(token)
        elif token in ("--mode", "--source", "--work-item"):
            if token in paths:
                raise IndexError
            paths[token] = args.pop(0)
        elif token.startswith("--") or obs is not None:
            raise IndexError
        else:
            obs = token
    if obs is None or paths.get("--mode") not in MODES:
        raise IndexError
    if paths["--mode"] == "structure-only" and ("--source" in paths or "--work-item" in paths):
        raise IndexError
    return obs, paths, flags


PASS_TEXT = {
    LEVEL_STRUCTURE: "KCAO_PASS_STRUCTURE_ONLY (structural validity ONLY: no native bytes were read, nothing is verified, provenance NOT_MEASURED)",
    LEVEL_UNAVAILABLE_RECORD: "KCAO_PASS_UNAVAILABLE_RECORD (a well-formed unavailable record: it asserts no observation and no evidence)",
    LEVEL_FIXTURE: "KCAO_PASS_FIXTURE_EVIDENCE (a synthetic fixture agrees with its synthetic bytes; this is NOT a native observation)",
    LEVEL_DIAGNOSTIC: "KCAO_DIAGNOSTIC_NON_ADMISSIVE (the record agrees with the supplied mutable bytes; this is NOT a pass, NOT strict evidence, and never admission, authority, authorization, delivery or publication)",
}


def main(argv: list[str]) -> int:
    try:
        obs, paths, options = _parse_args(argv[1:])
    except IndexError:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        data = _read_file(obs)
        source = _read_file(paths["--source"]) if "--source" in paths else None
        work = _read_file(paths["--work-item"]) if "--work-item" in paths else None
    except OSError as exc:
        print(f"KCAO_IOERROR operational error, not a refusal: {exc.__class__.__name__}: {exc.strerror or exc}")
        return 4
    fixture, require = "--fixture" in options, "--require-work-item" in options
    if paths["--mode"] == "structure-only":
        result = check_structure(data, fixture=fixture, require_work_item=require)
    elif paths["--mode"] == "diagnostic-agreement":
        result = check_diagnostic(data, source, work, fixture=fixture, require_work_item=require)
    else:
        result = check_strict(data, source, work, fixture=fixture, require_work_item=require)
    for p in result.problems:
        print(f"KCAO_FAIL {p}")
    if result.problems:
        return 1
    for f in result.flags:
        print(f"KCAO_FLAG {f}")
    print(f"KCAO_MODE {result.mode} LEVEL {result.level}")
    if result.unavailable is not None:
        print(f"KCAO_UNAVAILABLE {result.unavailable['reason']} {json.dumps(result.unavailable, sort_keys=True)}")
        return 3
    print(PASS_TEXT[result.level])
    return 5 if result.level == LEVEL_DIAGNOSTIC else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
