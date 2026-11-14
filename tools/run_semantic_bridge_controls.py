#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Run the finite semantic-mask oracle and retain its exact program identities."""
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


def _identity(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    files = ("tools/semantic_bridge.py", "tools/test_semantic_bridge.py",
             "tools/run_semantic_bridge_controls.py")
    before = {name: _identity(root / name) for name in files}
    sys.path.insert(0, str(root))
    oracle = importlib.import_module("tools.test_semantic_bridge")
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    result = oracle.run_finite_audit()
    elapsed = time.perf_counter() - started
    completed_at = datetime.now(timezone.utc).isoformat()
    after = {name: _identity(root / name) for name in files}
    if before != after:
        raise RuntimeError("program inputs changed during the recorded run")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    report = {
        "schema": "knowledge-contract.semantic-bridge-controls/1",
        "checkout_head": head,
        "source_identity_note": "The checkout head is not the identity of uncommitted candidate files; program hashes below bind this run.",
        "programs": before,
        "runtime": platform.python_version(),
        "started_at": started_at,
        "completed_at": completed_at,
        "elapsed_seconds": round(elapsed, 6),
        "audit": result,
        "effects_authorized": False,
        "limits": "Complete declared finite formal families, original fixture bytes and public API checks. Unit-boundary/CLI tests have their own execution log. No natural-language fidelity, translation review, real-world truth, grant authentication, external independence or LLM performance is established.",
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({
        "result": "pass", "output": str(args.output),
        "boolean_space": result["boolean_space"]["observed_counts"],
        "alternative_space": result["alternative_space"]["observed_counts"],
        "original_examples": len(result["original_examples"]["examples"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
