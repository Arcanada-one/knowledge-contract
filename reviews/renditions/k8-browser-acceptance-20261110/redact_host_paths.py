#!/usr/bin/env python3
"""Deterministic host-path redaction for K8 browser-acceptance evidence.

Only substitution rules (applied in order, exact string replace):
  1) /home/dev/aup/claude-work/kcswe-k8-browser/.venv -> <local-venv>
  2) /home/dev/aup/claude-work/kcswe-k8-browser/ -> ./

Reads originals from --src, writes redacted report.json and REPORT.md to --dst.
Prints JSON with per-rule counts and sha256 of inputs/outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RULES: list[tuple[str, str]] = [
    ("/home/dev/aup/claude-work/kcswe-k8-browser/.venv", "<local-venv>"),
    ("/home/dev/aup/claude-work/kcswe-k8-browser/", "./"),
]
FILES = ("report.json", "REPORT.md")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def redact(text: str) -> tuple[str, list[dict]]:
    counts: list[dict] = []
    out = text
    for before, after in RULES:
        n = out.count(before)
        if n:
            out = out.replace(before, after)
        counts.append({"before": before, "after": after, "count": n})
    return out, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--dst", type=Path, required=True)
    args = ap.parse_args()
    args.dst.mkdir(parents=True, exist_ok=True)
    summary = {"rules": [ {"before": b, "after": a} for b, a in RULES ], "files": {}}
    for name in FILES:
        raw = (args.src / name).read_bytes()
        # originals are UTF-8 text
        text = raw.decode("utf-8")
        redacted, counts = redact(text)
        out_bytes = redacted.encode("utf-8")
        (args.dst / name).write_bytes(out_bytes)
        summary["files"][name] = {
            "original_sha256": sha256_bytes(raw),
            "original_bytes": len(raw),
            "redacted_sha256": sha256_bytes(out_bytes),
            "redacted_bytes": len(out_bytes),
            "rule_counts": counts,
        }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
