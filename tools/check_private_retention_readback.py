#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Check PrivateRetention* documents against RET-* rules (structural)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SOURCE_ID = re.compile(r"^d_[0-9a-f]{64}$")
PACKAGE_ID = re.compile(r"^d_[0-9a-f]{64}/[A-Za-z0-9][A-Za-z0-9._@+-]{0,119}$")


def _fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def check_honesty(doc: dict) -> None:
    if doc.get("runtime_authorized") is not False:
        _fail("runtime_authorized must be false")
    if doc.get("knowledge_admitted") is not False:
        _fail("knowledge_admitted must be false")
    if doc.get("kc2_admission") != "not_measured":
        _fail("kc2_admission must be not_measured")


def check_object_id(oid: str) -> str:
    if SOURCE_ID.fullmatch(oid):
        return "original"
    if PACKAGE_ID.fullmatch(oid):
        return "package"
    _fail(f"invalid object_id: {oid!r}")
    raise AssertionError("unreachable")


def check_profile(doc: dict) -> None:
    if doc.get("schema") != "PrivateRetentionProfile/v1":
        _fail("schema must be PrivateRetentionProfile/v1")
    check_honesty(doc)
    for key in ("profile_id", "holder_host", "volume", "store_root"):
        if not doc.get(key):
            _fail(f"missing {key}")
    if doc.get("id_grammar") != "d_<sha256>":
        _fail("id_grammar must be d_<sha256>")
    if doc.get("digest_domain") != "sha256-exact-bytes":
        _fail("digest_domain must be sha256-exact-bytes")
    sep = doc.get("corpus_separation") or {}
    for key in ("originals_store", "kc_corpus_derived", "public_publication"):
        if not sep.get(key):
            _fail(f"corpus_separation.{key} required")


def check_readback(doc: dict) -> None:
    if doc.get("schema") != "PrivateExactReadbackReceipt/v1":
        _fail("schema must be PrivateExactReadbackReceipt/v1")
    check_honesty(doc)
    kind = check_object_id(doc["object_id"])
    if doc.get("object_kind") != kind:
        _fail("object_kind does not match object_id")
    if doc.get("content_exact") is not True:
        _fail("content_exact must be true on this receipt schema")
    if doc.get("digest_algorithm") != "sha256":
        _fail("digest_algorithm must be sha256")
    if doc.get("digest_domain") != "sha256-exact-bytes":
        _fail("digest_domain must be sha256-exact-bytes")
    if not re.fullmatch(r"[0-9a-f]{64}", doc.get("sha256") or ""):
        _fail("sha256 must be 64 lowercase hex")
    if int(doc.get("size_bytes", -1)) < 0:
        _fail("size_bytes must be >= 0")
    resolution = doc.get("resolution") or {}
    if resolution.get("method") not in ("location_registry", "source_library_index"):
        _fail("resolution.method invalid")
    if resolution.get("path_disclosed") is not False:
        _fail("resolution.path_disclosed must be false (LOC-R012 / RET-R004)")
    if doc.get("outcome") not in ("matched", "refused"):
        _fail("outcome invalid")
    if doc["outcome"] == "matched":
        if doc.get("refusal_code"):
            _fail("matched receipt must not carry refusal_code")
        if kind == "original" and doc["sha256"] != doc["object_id"][2:]:
            _fail("original sha256 must equal digest embedded in object_id")
    elif not doc.get("refusal_code"):
        _fail("refused receipt requires refusal_code")


def check_tombstone(doc: dict) -> None:
    if doc.get("schema") != "PrivateRetentionTombstone/v1":
        _fail("schema must be PrivateRetentionTombstone/v1")
    check_honesty(doc)
    check_object_id(doc["object_id"])
    if doc.get("state") not in ("collected", "unavailable"):
        _fail("state must be collected or unavailable")
    if not doc.get("recorded_at"):
        _fail("recorded_at required")
    prior = doc.get("prior_sha256")
    if prior is not None and not re.fullmatch(r"[0-9a-f]{64}", prior):
        _fail("prior_sha256 must be null or 64 hex")


def check_doc(doc: dict) -> str:
    schema = doc.get("schema")
    if schema == "PrivateRetentionProfile/v1":
        check_profile(doc)
        return "profile"
    if schema == "PrivateExactReadbackReceipt/v1":
        check_readback(doc)
        return "readback"
    if schema == "PrivateRetentionTombstone/v1":
        check_tombstone(doc)
        return "tombstone"
    _fail(f"unknown schema: {schema!r}")
    raise AssertionError("unreachable")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path, help="JSON document to check")
    args = ap.parse_args()
    doc = json.loads(args.path.read_text(encoding="utf-8"))
    kind = check_doc(doc)
    print(json.dumps({"verdict": "PASS", "kind": kind, "path": str(args.path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
