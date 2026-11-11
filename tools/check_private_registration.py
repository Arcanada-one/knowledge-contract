#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate private-artifact-registry records (PAR-R001..R010)."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "private-artifact-registry.schema.json"
SOURCE_ID = re.compile(r"^d_[0-9a-f]{64}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
AUTHORITY_KEYS = (
    "source_rights",
    "library_acceptance",
    "private_registry_adoption",
    "published_corpus_admission",
    "index_readback",
    "native_task_run_authority",
)
TRI = {"pass", "fail", "not_applicable", "not_measured"}


def load_json(path: Path):
    text = path.read_bytes()
    if text.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM refused")
    return json.loads(text.decode("utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_honesty(doc: dict, problems: list[str], prefix: str) -> None:
    if doc.get("runtime_authorized") is not False:
        problems.append(f"{prefix}: runtime_authorized must be false")
    if doc.get("knowledge_admitted") is not False:
        problems.append(f"{prefix}: knowledge_admitted must be false")
    if doc.get("kc2_admission") != "not_measured":
        problems.append(f"{prefix}: kc2_admission must be not_measured")


def check_authority(doc: dict, problems: list[str], prefix: str) -> None:
    auth = doc.get("authority_boundaries")
    if not isinstance(auth, dict):
        problems.append(f"{prefix}: authority_boundaries required")
        return
    for key in AUTHORITY_KEYS:
        if key not in auth:
            problems.append(f"{prefix}: authority_boundaries missing {key}")
        elif auth[key] not in TRI:
            problems.append(f"{prefix}: authority_boundaries.{key} invalid")
    for key in auth:
        if key not in AUTHORITY_KEYS:
            problems.append(f"{prefix}: unknown authority key {key}")


def check_acceptance(acc: dict, artifact_sha256: str, problems: list[str], prefix: str) -> None:
    if not isinstance(acc, dict) or acc.get("schema") != "SemanticAcceptanceRecord/v1":
        problems.append(f"{prefix}: acceptance must be SemanticAcceptanceRecord/v1")
        return
    if acc.get("result") != "supported":
        problems.append(f"{prefix}: acceptance.result must be supported for registration")
    if acc.get("artifact_sha256") != artifact_sha256:
        problems.append(f"{prefix}: acceptance.artifact_sha256 must equal handoff sha256")
    assessor = acc.get("assessor_id")
    producer = acc.get("producer_id")
    if not isinstance(assessor, str) or not assessor:
        problems.append(f"{prefix}: acceptance.assessor_id required")
    if not isinstance(producer, str) or not producer:
        problems.append(f"{prefix}: acceptance.producer_id required")
    if isinstance(assessor, str) and isinstance(producer, str) and assessor == producer:
        problems.append(f"{prefix}: assessor_id must be distinct from producer_id")
    scope = acc.get("scope")
    if not isinstance(scope, dict) or not scope.get("permitted_purpose"):
        problems.append(f"{prefix}: acceptance.scope.permitted_purpose required")
    if not isinstance(scope, dict) or not isinstance(scope.get("exclusions"), list):
        problems.append(f"{prefix}: acceptance.scope.exclusions must be an array")


def check_handoff(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivateRegistrationHandoff/v1":
        return ["schema must be PrivateRegistrationHandoff/v1"]
    check_honesty(doc, problems, "handoff")
    check_authority(doc, problems, "handoff")
    sha = doc.get("sha256")
    if not isinstance(sha, str) or not SHA256.match(sha):
        problems.append("handoff: sha256 must be 64 lowercase hex")
    else:
        check_acceptance(doc.get("acceptance") or {}, sha, problems, "handoff")
    sid = doc.get("source_document_id")
    status = doc.get("source_document_id_status", "measured" if sid else "not_measured")
    if status == "measured":
        if not isinstance(sid, str) or not SOURCE_ID.match(sid):
            problems.append("handoff: source_document_id must be d_<sha256> when measured")
    elif status == "not_measured":
        if not doc.get("source_document_id_reason"):
            problems.append("handoff: source_document_id_reason required when not_measured")
    else:
        problems.append("handoff: source_document_id_status invalid")
    closure = doc.get("dependency_closure")
    if not isinstance(closure, list):
        problems.append("handoff: dependency_closure must be an array")
    return problems


def check_registry(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivateArtifactRegistry/v1":
        return ["schema must be PrivateArtifactRegistry/v1"]
    entries = doc.get("entries")
    if not isinstance(entries, list):
        return ["entries must be an array"]
    seen = set()
    for i, row in enumerate(entries):
        if not isinstance(row, dict):
            problems.append(f"entries[{i}]: must be an object")
            continue
        key = (row.get("artifact_id"), row.get("revision"))
        if key in seen:
            problems.append(f"entries[{i}]: duplicate artifact_id+revision")
        seen.add(key)
        if not isinstance(row.get("sha256"), str) or not SHA256.match(row["sha256"]):
            problems.append(f"entries[{i}]: sha256 invalid")
        if not isinstance(row.get("acceptance_sha256"), str) or not SHA256.match(row["acceptance_sha256"]):
            problems.append(f"entries[{i}]: acceptance_sha256 invalid")
    return problems


def check_readback(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivateReadbackReceipt/v1":
        return ["schema must be PrivateReadbackReceipt/v1"]
    check_honesty(doc, problems, "readback")
    check_authority(doc, problems, "readback")
    if doc.get("outcome") not in ("matched", "not_found", "digest_mismatch", "refused"):
        problems.append("readback: outcome invalid")
    return problems


def check_retrieval(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivateRetrievalReceipt/v1":
        return ["schema must be PrivateRetrievalReceipt/v1"]
    check_honesty(doc, problems, "retrieval")
    check_authority(doc, problems, "retrieval")
    budget = doc.get("budget")
    if isinstance(budget, dict):
        if budget.get("status") == "measured":
            if not isinstance(budget.get("observed_bytes"), int):
                problems.append("retrieval: measured budget needs observed_bytes")
        elif budget.get("status") == "not_measured":
            if not budget.get("reason"):
                problems.append("retrieval: not_measured budget needs reason")
    return problems


def check_delivery(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivateDeliveryReceipt/v1":
        return ["schema must be PrivateDeliveryReceipt/v1"]
    check_honesty(doc, problems, "delivery")
    check_authority(doc, problems, "delivery")
    return problems


def check_witness(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivateUseWitness/v1":
        return ["schema must be PrivateUseWitness/v1"]
    check_honesty(doc, problems, "witness")
    check_authority(doc, problems, "witness")
    if doc.get("assessment") == "applied" and not doc.get("output_sha256"):
        problems.append("witness: applied assessment requires output_sha256")
    return problems


def check_outcomes(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema") != "PrivatePerBookOutcomes/v1":
        return ["schema must be PrivatePerBookOutcomes/v1"]
    if "runtime_authorized" in doc:
        check_honesty(doc, problems, "outcomes")
    books = doc.get("books")
    if not isinstance(books, list) or not books:
        return ["books must be a nonempty array"]
    for i, row in enumerate(books):
        if not isinstance(row, dict):
            problems.append(f"books[{i}]: must be an object")
            continue
        status = row.get("status")
        if status == "use_witness":
            if not row.get("use_witness_id"):
                problems.append(f"books[{i}]: use_witness requires use_witness_id")
        elif status == "unresolved":
            if not row.get("owner") or not row.get("blocking_reason"):
                problems.append(f"books[{i}]: unresolved requires owner and blocking_reason")
        else:
            problems.append(f"books[{i}]: status must be use_witness or unresolved")
    return problems


DISPATCH = {
    "PrivateRegistrationHandoff/v1": check_handoff,
    "PrivateArtifactRegistry/v1": check_registry,
    "PrivateReadbackReceipt/v1": check_readback,
    "PrivateRetrievalReceipt/v1": check_retrieval,
    "PrivateDeliveryReceipt/v1": check_delivery,
    "PrivateUseWitness/v1": check_witness,
    "PrivatePerBookOutcomes/v1": check_outcomes,
}


def validate(doc: dict) -> list[str]:
    schema = doc.get("schema")
    fn = DISPATCH.get(schema)
    if not fn:
        return [f"unknown schema {schema!r}"]
    return fn(doc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    failed = 0
    for path in args.paths:
        try:
            doc = load_json(path)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {path}: {exc}")
            failed += 1
            continue
        problems = validate(doc)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
