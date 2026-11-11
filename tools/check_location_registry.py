#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate LocationRegistry/v1 and LocationVerifyReceipt/v1 records against the schema and LOC identity rules."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "location-registry.schema.json"
SOURCE_ID = re.compile(r"^d_[0-9a-f]{64}$")
PACKAGE_ID = re.compile(r"^d_[0-9a-f]{64}/[A-Za-z0-9][A-Za-z0-9._@+-]{0,119}$")


def load_json(path: Path):
    text = path.read_bytes()
    if text.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM refused")
    return json.loads(text.decode("utf-8"))


def validate_row(row: dict, problems: list[str], prefix: str) -> None:
    if row.get("schema") != "LocationRegistryRow/v1":
        problems.append(f"{prefix}: schema must be LocationRegistryRow/v1")
        return
    kind = row.get("object_kind")
    oid = row.get("object_id")
    if kind == "original":
        if not isinstance(oid, str) or not SOURCE_ID.match(oid):
            problems.append(f"{prefix}: original object_id must be d_<sha256>")
        elif row.get("verified_sha256") is not None:
            expect = oid[2:]
            if row["verified_sha256"] != expect:
                problems.append(f"{prefix}: verified_sha256 must equal digest in object_id")
    elif kind == "package":
        if not isinstance(oid, str) or not PACKAGE_ID.match(oid):
            problems.append(f"{prefix}: package object_id must be d_<sha256>/<pipeline-version>")
    else:
        problems.append(f"{prefix}: object_kind must be original or package")
    if row.get("role") not in ("primary", "mirror", "backup"):
        problems.append(f"{prefix}: role must be primary|mirror|backup")
    for key in ("holder_host", "volume", "path"):
        if not isinstance(row.get(key), str) or not row.get(key):
            problems.append(f"{prefix}: {key} required")
    if not isinstance(row.get("size_bytes"), int) or row["size_bytes"] < 0:
        problems.append(f"{prefix}: size_bytes must be a non-negative integer")


def validate_registry(doc: dict) -> list[str]:
    problems = []
    if doc.get("schema") != "LocationRegistry/v1":
        return ["schema must be LocationRegistry/v1"]
    entries = doc.get("entries")
    if not isinstance(entries, list):
        return ["entries must be an array"]
    seen_primary = set()
    for i, row in enumerate(entries):
        if not isinstance(row, dict):
            problems.append(f"entries[{i}]: must be an object")
            continue
        validate_row(row, problems, f"entries[{i}]")
        if row.get("role") == "primary":
            key = row.get("object_id")
            if key in seen_primary:
                problems.append(f"entries[{i}]: duplicate primary for {key}")
            seen_primary.add(key)
    return problems


def validate_receipt(doc: dict) -> list[str]:
    problems = []
    if doc.get("schema") != "LocationVerifyReceipt/v1":
        return ["schema must be LocationVerifyReceipt/v1"]
    if doc.get("kc2_admission") != "not_measured":
        problems.append("kc2_admission must be not_measured")
    counts = doc.get("counts") or {}
    for k in ("ok", "missing", "corrupt", "not_measured"):
        if not isinstance(counts.get(k), int) or counts[k] < 0:
            problems.append(f"counts.{k} must be a non-negative integer")
    non_ok = doc.get("non_ok")
    if not isinstance(non_ok, list):
        problems.append("non_ok must be an array")
    return problems


def validate_document(doc: dict) -> list[str]:
    schema = doc.get("schema")
    if schema == "LocationRegistry/v1":
        return validate_registry(doc)
    if schema == "LocationVerifyReceipt/v1":
        return validate_receipt(doc)
    if schema == "LocationRegistryRow/v1":
        problems = []
        validate_row(doc, problems, "row")
        return problems
    return [f"unsupported schema {schema!r}"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument(
        "--jsonschema",
        action="store_true",
        help="Also validate with draft 2020-12 jsonschema if installed",
    )
    args = ap.parse_args()
    schema = None
    if args.jsonschema:
        import jsonschema

        schema = load_json(SCHEMA_PATH)
    exit_code = 0
    for path in args.paths:
        try:
            doc = load_json(path)
        except Exception as exc:  # noqa: BLE001 — surface parse errors as check failures
            print(f"FAIL {path}: {exc}")
            exit_code = 1
            continue
        problems = validate_document(doc)
        if schema is not None and doc.get("schema") in (
            "LocationRegistry/v1",
            "LocationVerifyReceipt/v1",
        ):
            try:
                import jsonschema

                jsonschema.Draft202012Validator(schema).validate(doc)
            except Exception as exc:  # noqa: BLE001
                problems.append(f"jsonschema: {exc}")
        if problems:
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
            exit_code = 1
        else:
            print(f"PASS {path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
