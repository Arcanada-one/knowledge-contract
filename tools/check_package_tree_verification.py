#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Check a PackageTreeVerification/v1 document (CANDIDATE, KCLIVE-03).

Structural only: a PASS says the document is well formed. It does not prove the scan was
done, that bytes were delivered to a consumer, or that any receipt matched.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PACKAGE_ID = re.compile(r"^d_[0-9a-f]{64}/[A-Za-z0-9][A-Za-z0-9._@+-]{0,119}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REFUSAL_CODES = (
    "not_found", "unauthorized", "corrupt", "collected", "unavailable", "missing", "invalid_id",
    "path_injection_refused",
)
REQUIRED = frozenset({
    "schema", "package_id", "digest_algorithm", "digest_domain", "tree_sha256", "member_count",
    "size_bytes", "resolution", "outcome", "runtime_authorized", "knowledge_admitted", "kc2_admission",
})
ALLOWED = REQUIRED | {"refusal_code"}
RESOLUTION_KEYS = frozenset({"method", "holder_host", "volume", "role", "registry_ref", "path_disclosed"})


def _fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def _nonempty(v: object) -> bool:
    return isinstance(v, str) and v != ""


def check_doc(doc: object) -> None:
    if not isinstance(doc, dict):
        _fail("document must be a JSON object")
    missing = sorted(REQUIRED - set(doc))
    if missing:
        _fail(f"missing field(s): {missing}")
    unknown = sorted(set(doc) - ALLOWED)
    if unknown:
        _fail(f"unknown field(s): {unknown}")
    if doc["schema"] != "PackageTreeVerification/v1":
        _fail("schema must be PackageTreeVerification/v1")
    if not (isinstance(doc["package_id"], str) and PACKAGE_ID.fullmatch(doc["package_id"])):
        _fail("package_id must be a package id d_<sha256>/<pipeline_version>")
    if doc["digest_algorithm"] != "sha256":
        _fail("digest_algorithm must be sha256")
    if doc["digest_domain"] != "sha256-tree-manifest-v1":
        _fail("digest_domain must be sha256-tree-manifest-v1 (never sha256-exact-bytes)")
    if not (isinstance(doc["tree_sha256"], str) and SHA256.fullmatch(doc["tree_sha256"])):
        _fail("tree_sha256 must be 64 lowercase hex")
    count = doc["member_count"]
    if type(count) is not int or count < 1:
        _fail("member_count must be a JSON integer > 0")
    size = doc["size_bytes"]
    if type(size) is not int or size < 0:
        _fail("size_bytes must be a non-negative JSON integer")
    res = doc["resolution"]
    if not isinstance(res, dict) or set(res) != RESOLUTION_KEYS:
        _fail(f"resolution must be an object with exactly {sorted(RESOLUTION_KEYS)}")
    if res["method"] != "location_registry":
        _fail("resolution.method must be location_registry")
    if not (_nonempty(res["holder_host"]) and _nonempty(res["volume"]) and _nonempty(res["registry_ref"])):
        _fail("resolution holder_host, volume and registry_ref must be non-empty strings")
    if not (res["role"] is None or isinstance(res["role"], str)):
        _fail("resolution.role must be a string or null")
    if res["path_disclosed"] is not False:
        _fail("resolution.path_disclosed must be false")
    if doc["outcome"] not in ("verified", "refused"):
        _fail("outcome must be verified or refused")
    if doc["outcome"] == "verified" and "refusal_code" in doc:
        _fail("verified observation must not carry refusal_code")
    if doc["outcome"] == "refused" and doc.get("refusal_code") not in REFUSAL_CODES:
        _fail(f"refused observation requires refusal_code from {list(REFUSAL_CODES)}")
    if doc["runtime_authorized"] is not False:
        _fail("runtime_authorized must be false")
    if doc["knowledge_admitted"] is not False:
        _fail("knowledge_admitted must be false")
    if doc["kc2_admission"] != "not_measured":
        _fail("kc2_admission must be not_measured")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    check_doc(json.loads(args.path.read_text(encoding="utf-8")))
    print(json.dumps({"verdict": "PASS", "kind": "package-tree-verification", "path": str(args.path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
