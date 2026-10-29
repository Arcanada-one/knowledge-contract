#!/usr/bin/env python3
"""Fail a pull request that changes two of: decision-tree files, the allowlist table, content paths.

DEC-AUP-0171: a decision must land in a pull request of its own, before the allowlist row, and
neither may share a change with the content it approves.
"""

from __future__ import annotations

import re
import subprocess
import sys

AREAS = (
    re.compile(r"^corpus/publication-decisions/"),
    re.compile(r"^corpus/README\.md$"),
    re.compile(r"^(articles|papers|spec|schemas)/"),
)


def violates(paths: list[str]) -> bool:
    """True when a change touches two of: decision-tree files, the allowlist table, content paths."""
    return sum(any(area.match(p) for p in paths) for area in AREAS) >= 2


def changed_paths(base: str, head: str) -> list[str]:
    """Paths changed between the merge base and the head: NUL-separated (names with tabs, newlines or quotes stay whole) and
    without rename detection (a rename shows both its old and its new path, so a move out of a content directory is seen)."""
    result = subprocess.run(["git", "diff", "--no-renames", "-z", "--name-only", f"{base}...{head}"], stdout=subprocess.PIPE, check=True)
    return [name.decode("utf-8", "surrogateescape") for name in result.stdout.split(b"\0") if name]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: check_separation.py BASE_SHA HEAD_SHA", file=sys.stderr)
        return 2
    paths = changed_paths(argv[1], argv[2])
    if violates(paths):
        print("SEPARATION_FAIL: decision or allowlist-table files and content paths changed in one pull request", file=sys.stderr)
        return 1
    print("SEPARATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
