#!/usr/bin/env python3
"""Fail when a commit in BASE..HEAD lacks a Signed-off-by trailer (DCO 1.1)."""
from __future__ import annotations

import re
import subprocess
import sys

SIGNOFF_RE = re.compile(r"^Signed-off-by: .+ <[^<>\s]+@[^<>\s]+>\s*$", re.M)


def commits(base: str, head: str, repo: str = ".") -> list[tuple[str, str, int]]:
    out = subprocess.run(
        ["git", "-C", repo, "log", "--format=%H%x1f%P%x1f%B%x1e", f"{base}..{head}"],
        check=True, capture_output=True, text=True,
    ).stdout
    rows = []
    for record in out.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        sha, parents, body = record.split("\x1f", 2)
        rows.append((sha, body, len(parents.split())))
    return rows


def unsigned(base: str, head: str, repo: str = ".") -> list[str]:
    return [
        sha for sha, body, parent_count in commits(base, head, repo)
        if parent_count < 2 and not SIGNOFF_RE.search(body)
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: check_dco.py BASE HEAD", file=sys.stderr)
        return 2
    bad = unsigned(argv[1], argv[2])
    for sha in bad:
        print(f"DCO_CHECK_FAIL {sha} has no Signed-off-by trailer (use git commit -s)")
    if bad:
        return 1
    print("DCO_CHECK_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
