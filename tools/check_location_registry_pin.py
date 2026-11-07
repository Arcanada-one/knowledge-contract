#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Check a LocationRegistryPin/v1 envelope (CANDIDATE, KCLIVE-03).

Structural only. A PASS says the envelope is well formed; it does not say the digest came from a
trusted source, that it matches any registry bytes, or that an issuer witnessed the revision.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED = frozenset({"schema", "registry_revision", "digest_domain", "registry_sha256"})
ALLOWED = REQUIRED | {"issuer_witness"}


def _fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def check_doc(doc: object) -> None:
    if not isinstance(doc, dict):
        _fail("document must be a JSON object")
    missing = sorted(REQUIRED - set(doc))
    if missing:
        _fail(f"missing field(s): {missing}")
    unknown = sorted(set(doc) - ALLOWED)
    if unknown:
        _fail(f"unknown field(s): {unknown}")
    if doc["schema"] != "LocationRegistryPin/v1":
        _fail("schema must be LocationRegistryPin/v1")
    if not (isinstance(doc["registry_revision"], str) and doc["registry_revision"] != ""):
        _fail("registry_revision must be a non-empty label (a label is not a pin)")
    if doc["digest_domain"] != "sha256-exact-bytes":
        _fail("digest_domain must be sha256-exact-bytes")
    if not (isinstance(doc["registry_sha256"], str) and SHA256.fullmatch(doc["registry_sha256"])):
        _fail("registry_sha256 must be 64 lowercase hex")
    if doc.get("issuer_witness") is not None:
        _fail("issuer_witness must be absent or null: no issuer exists, source admission is NOT_MEASURED")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    check_doc(json.loads(args.path.read_text(encoding="utf-8")))
    print(json.dumps({"verdict": "PASS", "kind": "location-registry-pin", "path": str(args.path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
