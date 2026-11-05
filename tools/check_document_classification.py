#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate a DocumentClassification/v1 result against the kc-doc-class/1 canon (engineering/specifications/pipeline).

    check_document_classification.py CLASSIFICATION.json

The checker works from the file and the canon in this repository alone: no network, no registry. It applies schemas/document-classification.schema.json, then
the rules a reader must not take on trust: the taxonomy identifier is the one this canon defines (an older or newer label is refused, never read as the
latest canon), the canon digest is the SHA-256 of the exact bytes of document-classes.json, and the status, class and candidate invariants hold (rechecked
here independently of the schema). `check_canon` checks the canon file against the schema; `check_binding` checks the link from a classify receipt. Every
refusal carries a stable DCL-... code. It never claims that a class is right, only that the record is well formed, honest about what was not measured, and
bound to one canon and one document.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_book_package as cbp  # noqa: E402  (strict JSON reader shared with the other validators)

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "document-classification.schema.json"
CANON_PATH = REPO / "engineering" / "specifications" / "pipeline" / "document-classes.json"
TAXONOMY_ID = "kc-doc-class/1"
CLASSES = ("book", "paper", "export", "dataset", "other")
MAX_BYTES = 1 << 20


def canon_digest(canon_path: Path = CANON_PATH) -> str:
    return hashlib.sha256(Path(canon_path).read_bytes()).hexdigest()


def _validator() -> jsonschema.Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def check_canon(canon_path: Path = CANON_PATH) -> list[str]:
    """The canon file agrees with the schema: same class ids, same statuses, the taxonomy identifier this tool knows."""
    problems: list[str] = []
    try:
        canon = cbp.strict_json(cbp.read_text_strict(Path(canon_path)), Path(canon_path).name)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (cbp.PackageError, json.JSONDecodeError, OSError) as exc:
        return [f"DCL-CANON-FILE: {exc}"]
    if not isinstance(canon, dict) or canon.get("taxonomy_id") != TAXONOMY_ID:
        problems.append(f"DCL-CANON-FILE: the canon does not define {TAXONOMY_ID}")
        return problems
    ids = [c.get("id") for c in canon.get("classes", []) if isinstance(c, dict)]
    if ids != schema["properties"]["class"]["enum"][:-1]:
        problems.append("DCL-CANON-FILE: the class ids of the canon differ from the class enumeration of the schema")
    statuses = [s.get("id") for s in canon.get("statuses", []) if isinstance(s, dict)]
    if statuses != schema["properties"]["status"]["enum"]:
        problems.append("DCL-CANON-FILE: the statuses of the canon differ from the status enumeration of the schema")
    for c in canon.get("classes", []):
        if not (isinstance(c, dict) and isinstance(c.get("definition"), str) and c["definition"].strip() and isinstance(c.get("boundary"), str) and c["boundary"].strip()):
            problems.append("DCL-CANON-FILE: a class has no definition or no boundary")
    return problems


def _invariants(record: dict) -> list[str]:
    status, cls, cands, reason = record.get("status"), record.get("class"), record.get("candidates"), record.get("reason")
    ok_reason = isinstance(reason, str) and reason.strip() != ""
    if status == "classified":
        good = cls in CLASSES and cands == [cls]
    elif status == "ambiguous":
        good = cls is None and isinstance(cands, list) and len(set(cands)) >= 2 and len(set(cands)) == len(cands) and set(cands) <= set(CLASSES[:4]) and ok_reason
    elif status == "unknown":
        good = cls is None and cands == [] and ok_reason
    else:
        good = False
    conf = record.get("confidence") or {}
    if conf.get("status") == "not_measured" and ("score" in conf or "method" in conf):
        good = False
    return [] if good else [f"DCL-INVARIANT: status {status!r} with class {cls!r} and candidates {cands!r} breaks the status/class/candidate rules"]


def check_classification(data: bytes, canon_path: Path = CANON_PATH) -> list[str]:
    """Problems of one classification result, each as `CODE: text`; an empty list is a well-formed result."""
    problems: list[str] = []
    if len(data) > MAX_BYTES:
        return [f"DCL-READ: a classification is at most {MAX_BYTES} bytes"]
    try:
        record = cbp.strict_json(data.decode("utf-8"), "classification.json")
    except (cbp.PackageError, json.JSONDecodeError, UnicodeDecodeError, RecursionError) as exc:
        return [f"DCL-READ: {exc}"]
    if not isinstance(record, dict):
        return ["DCL-SCHEMA: not a JSON object"]
    for error in sorted(_validator().iter_errors(record), key=lambda e: list(map(str, e.path))):
        where = "/".join(str(p) for p in error.path) or "<root>"
        problems.append(f"DCL-SCHEMA: {where}: {error.message[:160]}")
    if problems:
        return problems
    if record["taxonomy_id"] != TAXONOMY_ID:
        problems.append(f"DCL-TAXONOMY: {record['taxonomy_id']!r} is not the taxonomy this canon defines ({TAXONOMY_ID}); a result is never read against the latest canon")
    if record["canon_sha256"] != canon_digest(canon_path):
        problems.append("DCL-CANON: canon_sha256 is not the SHA-256 of the exact bytes of document-classes.json")
    problems += _invariants(record)
    return problems


def check_binding(receipt: dict, classification: bytes) -> list[str]:
    """The classify receipt names these exact bytes as its output with role `classification`, for the same document."""
    problems: list[str] = []
    if receipt.get("stage") != "classify" or receipt.get("outcome") != "done":
        return ["DCL-BINDING: only a classify receipt that finished carries a classification"]
    outputs = [o for o in receipt.get("outputs", []) if isinstance(o, dict) and o.get("role") == "classification"]
    if len(outputs) != 1:
        problems.append(f"DCL-BINDING: the receipt lists {len(outputs)} outputs with role classification, not exactly one")
    elif outputs[0].get("sha256") != hashlib.sha256(classification).hexdigest():
        problems.append("DCL-BINDING: the output digest of the receipt is not the SHA-256 of the classification bytes")
    try:
        if json.loads(classification).get("document_id") != receipt.get("document_id"):
            problems.append("DCL-BINDING: the classification names another document than the receipt")
    except (ValueError, AttributeError):
        problems.append("DCL-BINDING: the classification is not a JSON object")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_document_classification.py CLASSIFICATION.json", file=sys.stderr)
        return 2
    try:
        data = Path(argv[1]).read_bytes()
    except OSError as exc:
        print(f"DOCCLASS_FAIL DCL-READ: {exc}")
        return 1
    problems = check_canon() + check_classification(data)
    if problems:
        for p in problems:
            print(f"DOCCLASS_FAIL {p}")
        return 1
    print("DOCCLASS_PASS (form, canon digest and status/class/candidate rules only; no judgement that the class is right)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
