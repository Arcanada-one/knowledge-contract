#!/usr/bin/env python3
"""Deterministic field review of the public redacted K8 report.json.

Scans response_headers_sample keys and counts residual markers that would
indicate unexpected credentials, cookies, host paths, or identifiers.
Writes JSON (and optional Markdown) without embedding private host paths.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

IPV4_RE = re.compile(
    r"(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)"
)
ABS_HOST_PATH_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_])/(?:home|Users|run/user)/[^\s\"']*"
)
COOKIE_RE = re.compile(r"(?i)\b(?:set-)?cookie\b")
CF_RAY_RE = re.compile(r"(?i)\bcf-ray\b")
TOKEN_KEY_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|secret|password|passwd|authorization|bearer|"
    r"access[_-]?token|refresh[_-]?token|session[_-]?id|private[_-]?key)\b"
)
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
USER_AGENT_RE = re.compile(r"(?i)\buser-agent\b")
URL_RE = re.compile(r"https?://[^\s\"'<>]+")


def collect_header_keys(report: dict) -> list[str]:
    keys: set[str] = set()
    for row in report.get("results") or []:
        sample = row.get("response_headers_sample") or {}
        if isinstance(sample, dict):
            for key in sample:
                keys.add(str(key).lower())
    return sorted(keys)


def non_github_hosts(text: str) -> list[str]:
    hosts: set[str] = set()
    for match in URL_RE.finditer(text):
        host = (urlparse(match.group(0)).hostname or "").lower()
        if host and host != "github.com" and not host.endswith(".github.com"):
            hosts.add(host)
    # Also catch hostnames named in free text (e.g. script[src*=host/...]).
    for match in re.finditer(
        r"(?i)(?:src\*=|//)([a-z0-9.-]+\.[a-z]{2,})(?:/|[\"'\]]|$)",
        text,
    ):
        host = match.group(1).lower()
        if host != "github.com" and not host.endswith(".github.com"):
            hosts.add(host)
    return sorted(hosts)


def review(report_path: Path) -> dict:
    raw = report_path.read_bytes()
    text = raw.decode("utf-8")
    report = json.loads(text)
    header_keys = collect_header_keys(report)
    return {
        "report_path": str(report_path.name),
        "report_sha256": __import__("hashlib").sha256(raw).hexdigest(),
        "report_bytes": len(raw),
        "header_keys_kept": header_keys,
        "counts": {
            "ipv4": len(IPV4_RE.findall(text)),
            "absolute_host_paths": len(ABS_HOST_PATH_RE.findall(text)),
            "cookies": len(COOKIE_RE.findall(text)),
            "cf_ray": len(CF_RAY_RE.findall(text)),
            "tokens_keys": len(TOKEN_KEY_RE.findall(text)),
            "emails": len(EMAIL_RE.findall(text)),
            "user_agents": len(USER_AGENT_RE.findall(text)),
        },
        "non_github_hosts": non_github_hosts(text),
    }


def to_markdown(data: dict) -> str:
    counts = data["counts"]
    lines = [
        "---",
        'title: "K8 browser-acceptance public report.json field review"',
        "sources: none",
        'status: "Deterministic residual-field scan of redacted report.json"',
        "updated: 2026-11-10",
        "---",
        "",
        "# K8 browser-acceptance public report.json field review",
        "",
        "Deterministic scan of the committed redacted `report.json`.",
        "This is a bounded residual-field review, not an independent browser",
        "replay and not a claim that every unknown field is safe.",
        "",
        f"- report bytes: `{data['report_bytes']}`",
        f"- report sha256: `{data['report_sha256']}`",
        "",
        "## Header keys kept (`response_headers_sample`)",
        "",
    ]
    if data["header_keys_kept"]:
        for key in data["header_keys_kept"]:
            lines.append(f"- `{key}`")
    else:
        lines.append("- (none)")
    lines.extend(
        [
            "",
            "Expected only: `content-type`, `last-modified`.",
            "",
            "## Residual marker counts",
            "",
            "| Marker | Count |",
            "| --- | ---: |",
            f"| IPv4 | {counts['ipv4']} |",
            f"| Absolute host paths | {counts['absolute_host_paths']} |",
            f"| Cookies | {counts['cookies']} |",
            f"| cf-ray | {counts['cf_ray']} |",
            f"| Tokens/keys | {counts['tokens_keys']} |",
            f"| Emails | {counts['emails']} |",
            f"| User agents | {counts['user_agents']} |",
            "",
            "Expected count for each marker above: `0`.",
            "",
            "## Non-github host strings",
            "",
        ]
    )
    if data["non_github_hosts"]:
        for host in data["non_github_hosts"]:
            lines.append(f"- `{host}`")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).resolve().parent / "report.json",
    )
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--md-out", type=Path)
    args = ap.parse_args()
    data = review(args.report)
    args.json_out.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if args.md_out is not None:
        args.md_out.write_text(to_markdown(data), encoding="utf-8")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
