#!/usr/bin/env python3
"""Deterministic host-path redaction for K8 browser-acceptance evidence.

Public rule identities (before-strings are private; only digests are published):
  R1 after=<local-venv> before_sha256=8ab426728e31fcf3c152d6da488d1be39f7e62045c279a67be1b50334fcfcf35
  R2 after=./            before_sha256=c02dd7a0cde79ccea59f7bcaa8032e2820cf782b8e1697ddb5159d1599237705

Requires --mapping <private JSON> whose rules supply the exact before-strings.
Refuses unless each rule's UTF-8 before-string hashes to the published digest
and the after-string matches the published after-string.
Reads originals from --src, writes redacted report.json and REPORT.md to --dst.
Prints JSON with per-rule counts and sha256 of inputs/outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PUBLISHED_RULES: list[dict[str, str]] = [
    {
        "id": "R1",
        "after": "<local-venv>",
        "before_sha256": (
            "8ab426728e31fcf3c152d6da488d1be39f7e62045c279a67be1b50334fcfcf35"
        ),
    },
    {
        "id": "R2",
        "after": "./",
        "before_sha256": (
            "c02dd7a0cde79ccea59f7bcaa8032e2820cf782b8e1697ddb5159d1599237705"
        ),
    },
]
FILES = ("report.json", "REPORT.md")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def load_rules(mapping_path: Path) -> list[tuple[str, str, str]]:
    """Return ordered (rule_id, before, after) validated against published digests."""
    raw = json.loads(mapping_path.read_text(encoding="utf-8"))
    by_id: dict[str, dict] = {}
    for item in raw.get("rules", []):
        rid = item.get("id")
        if not isinstance(rid, str):
            raise SystemExit("mapping rule missing string id")
        if rid in by_id:
            raise SystemExit(f"duplicate mapping rule id: {rid}")
        by_id[rid] = item

    ordered: list[tuple[str, str, str]] = []
    for published in PUBLISHED_RULES:
        rid = published["id"]
        if rid not in by_id:
            raise SystemExit(f"mapping missing published rule {rid}")
        item = by_id[rid]
        before = item.get("before")
        after = item.get("after")
        if not isinstance(before, str) or not isinstance(after, str):
            raise SystemExit(f"mapping rule {rid} needs string before/after")
        digest = sha256_text(before)
        if digest != published["before_sha256"]:
            raise SystemExit(
                f"digest mismatch for {rid}: got {digest}, "
                f"expected {published['before_sha256']}"
            )
        if after != published["after"]:
            raise SystemExit(
                f"after mismatch for {rid}: got {after!r}, "
                f"expected {published['after']!r}"
            )
        claimed = item.get("before_sha256")
        if claimed is not None and claimed != digest:
            raise SystemExit(
                f"mapping before_sha256 for {rid} does not match before-string"
            )
        ordered.append((rid, before, after))

    extra = set(by_id) - {p["id"] for p in PUBLISHED_RULES}
    if extra:
        raise SystemExit(f"mapping has unexpected rule ids: {sorted(extra)}")
    return ordered


def redact(text: str, rules: list[tuple[str, str, str]]) -> tuple[str, list[dict]]:
    counts: list[dict] = []
    out = text
    for rid, before, after in rules:
        n = out.count(before)
        if n:
            out = out.replace(before, after)
        counts.append(
            {
                "id": rid,
                "after": after,
                "before_sha256": sha256_text(before),
                "count": n,
            }
        )
    return out, counts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--dst", type=Path, required=True)
    ap.add_argument(
        "--mapping",
        type=Path,
        required=True,
        help="private JSON mapping with before-strings for published rule digests",
    )
    args = ap.parse_args(argv)
    rules = load_rules(args.mapping)
    args.dst.mkdir(parents=True, exist_ok=True)
    summary = {
        "rules": [
            {
                "id": rid,
                "after": after,
                "before_sha256": sha256_text(before),
            }
            for rid, before, after in rules
        ],
        "files": {},
    }
    for name in FILES:
        raw = (args.src / name).read_bytes()
        text = raw.decode("utf-8")
        redacted, counts = redact(text, rules)
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
