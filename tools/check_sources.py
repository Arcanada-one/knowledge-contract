#!/usr/bin/env python3
"""Fail when a file under papers/ or spec/ has no source declaration.

A file is covered when either:
- SOURCES.md has a table row whose last cell (Where) contains the file path in
  backticks, or
- (Markdown only) its front matter has `sources: none`, or `sources:` with a
  non-empty list (flow `[a, b]` or block `- a`) in which every entry equals the
  Source cell of a SOURCES.md row (case-insensitive).
`sources: []`, `sources: ""` and an empty `sources:` do not count.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOTS = ("papers", "spec")
FRONT_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
SOURCES_KEY_RE = re.compile(r"^sources:[ \t]*(.*)$", re.M)


def register(sources_md: str) -> tuple[set[str], set[str]]:
    """Return (paths covered by a row's Where cell, folded Source names)."""
    paths: set[str] = set()
    names: set[str] = set()
    for line in sources_md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or set(cells[0]) <= {"-", " ", ":"} or cells[0].lower() == "source":
            continue
        paths.update(re.findall(r"`([^`]+)`", cells[-1]))
        names.add(cells[0].casefold())
    return paths, names


def declared_entries(text: str) -> list[str] | None:
    """Front-matter `sources:` as a list of entries; ['none'] for none; None if absent or empty."""
    match = FRONT_RE.match(text)
    if not match:
        return None
    block = match.group(1)
    key = SOURCES_KEY_RE.search(block)
    if not key:
        return None
    inline = key.group(1).strip()
    if inline == "none":
        return ["none"]
    if inline.startswith("[") and inline.endswith("]"):
        items = [i.strip().strip("'\"").strip() for i in inline[1:-1].split(",")]
    elif inline:
        return None
    else:
        items = []
        for line in block[key.end():].splitlines():
            if not line.strip():
                continue
            item = re.match(r"\s+-\s+(.*\S)\s*$", line)
            if not item:
                break
            items.append(item.group(1).strip().strip("'\"").strip())
    items = [i for i in items if i]
    return items or None


def check(root: Path) -> list[str]:
    sources_md = root / "SOURCES.md"
    if not sources_md.is_file():
        return ["SOURCES.md is missing"]
    covered, names = register(sources_md.read_text(encoding="utf-8"))
    problems: list[str] = []
    for top in ROOTS:
        base = root / top
        if not base.is_dir():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file() and p.name != ".gitkeep"):
            rel = path.relative_to(root).as_posix()
            if rel in covered:
                continue
            entries = declared_entries(path.read_text(encoding="utf-8")) if path.suffix == ".md" else None
            if entries == ["none"]:
                continue
            if entries:
                unknown = [e for e in entries if e.casefold() not in names]
                if not unknown:
                    continue
                problems.append(f"{rel}: front-matter sources not in the SOURCES.md register: {', '.join(unknown)}")
                continue
            problems.append(f"{rel}: no SOURCES.md row and no valid front-matter `sources:` (a non-empty list of registered sources, or `sources: none`)")
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
