#!/usr/bin/env python3
"""Fail when a file under papers/ or spec/ has no source declaration.

A file is covered when SOURCES.md has a table row whose last cell contains the
file path in backticks, or (Markdown only) its front matter has a `sources:`
key that is a non-empty list or the literal `none`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOTS = ("papers", "spec")
FRONT_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
SOURCES_KEY_RE = re.compile(r"^sources:[ \t]*(.*)$", re.M)


def register_paths(sources_md: str) -> set[str]:
    covered: set[str] = set()
    for line in sources_md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        covered.update(re.findall(r"`([^`]+)`", cells[-1]))
    return covered


def front_matter_declares(text: str) -> bool:
    match = FRONT_RE.match(text)
    if not match:
        return False
    block = match.group(1)
    key = SOURCES_KEY_RE.search(block)
    if not key:
        return False
    inline = key.group(1).strip()
    if inline.lower() == "none":
        return True
    if inline and not inline.startswith("#"):
        return True
    after = block[key.end():].splitlines()
    return any(re.match(r"\s+-\s+\S", item) for item in after[:50] if item.strip()) and bool(
        after and re.match(r"\s+-\s+\S", next((i for i in after if i.strip()), ""))
    )


def check(root: Path) -> list[str]:
    sources_md = root / "SOURCES.md"
    if not sources_md.is_file():
        return ["SOURCES.md is missing"]
    covered = register_paths(sources_md.read_text(encoding="utf-8"))
    problems: list[str] = []
    for top in ROOTS:
        base = root / top
        if not base.is_dir():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file() and p.name != ".gitkeep"):
            rel = path.relative_to(root).as_posix()
            if rel in covered:
                continue
            if path.suffix == ".md" and front_matter_declares(path.read_text(encoding="utf-8")):
                continue
            problems.append(f"{rel}: no SOURCES.md row and no front-matter `sources:` (use `sources: none` if there are none)")
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    problems = check(root)
    for problem in problems:
        print(f"SOURCES_CHECK_FAIL {problem}")
    if problems:
        return 1
    print("SOURCES_CHECK_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
