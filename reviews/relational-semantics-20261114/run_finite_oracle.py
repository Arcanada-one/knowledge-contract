#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Run the separately authored finite oracle and bind its exact local inputs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


def digest(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository = args.repository.resolve()
    files = ("tools/semantic_relations.py", "tools/test_semantic_relations.py")
    before = {name: digest(repository / name) for name in files}
    sys.path.insert(0, str(repository))
    module = importlib.import_module("tools.test_semantic_relations")
    started_at = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    audit = module.run_finite_audit()
    elapsed = time.monotonic() - start
    after = {name: digest(repository / name) for name in files}
    if before != after:
        raise RuntimeError("implementation/oracle changed during the observation")
    base = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repository, text=True).strip()
    report = {
        "schema": "knowledge-contract.finite-relation-oracle/1",
        "base_commit": base,
        "source_identity_note": "The files below may be uncommitted; their hashes bind this run, not base HEAD alone.",
        "programs": before,
        "runner": digest(Path(__file__)),
        "runtime": platform.python_version(),
        "started_at": started_at,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed, 6),
        "audit": audit,
        "effects_authorized": False,
        "limits": "Finite exact reference semantics and API controls; same controller/model family/host. Not an external review, model trial or production admission.",
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "result": "pass",
                      "relations": audit["relations"]["observed_counts"],
                      "geometry": audit["geometry"]["observed_counts"],
                      "mutants_detected": sum(row["detected"] for row in audit["single_defect_controls"]["mutants"])},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
