#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Read-only, exact-ref inventory of translation files; not a fidelity verdict.

Count the union, not the sum, of base and draft paths. Source-catalogue scope
is explicit. Git blob equality identifies unchanged overlaps, not semantic
accuracy, rendition admission, source currency, deployment or index admission.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any

LOCALES = ("ru", "zh-Hans")
KINDS = {"paper", "specification", "study", "glossary", "bibliography", "appendix"}


def catalogue_paths(catalogue: dict[str, Any]) -> dict[str, str]:
    """Validate unique canonical paths and return path -> document kind."""
    docs = catalogue.get("documents")
    if not isinstance(docs, list) or not docs:
        raise ValueError("catalogue.documents must be a nonempty list")
    result: dict[str, str] = {}
    for doc in docs:
        if not isinstance(doc, dict):
            raise ValueError("catalogue document must be an object")
        path, kind = doc.get("path"), doc.get("type")
        if not isinstance(path, str) or not path or "\\" in path:
            raise ValueError("canonical path must be a nonempty POSIX path")
        p = PurePosixPath(path)
        if p.is_absolute() or ".." in p.parts or str(p) != path or not path.endswith(".md"):
            raise ValueError(f"unsafe or noncanonical path: {path!r}")
        if not isinstance(kind, str) or kind not in KINDS:
            raise ValueError(f"unsupported document kind: {kind!r}")
        if path in result:
            raise ValueError(f"duplicate catalogue path: {path}")
        result[path] = kind
    return result


def coverage(paths: dict[str, str], base: dict[str, str], draft: dict[str, str],
             locale: str) -> dict[str, Any]:
    if locale not in LOCALES:
        raise ValueError("unsupported locale")
    expected = {f"translations/{locale}/{p}": kind for p, kind in paths.items()}
    a, b = set(expected) & base.keys(), set(expected) & draft.keys()
    overlap = a & b
    identical = {p for p in overlap if base[p] == draft[p]}
    groups = {
        "base_present": a,
        "draft_present": b,
        "overlap": overlap,
        "identical_overlap": identical,
        "different_overlap": overlap - identical,
        "draft_only": b - a,
        "base_only": a - b,
        "union_present": a | b,
        "missing_from_both": set(expected) - (a | b),
    }
    by_kind = {}
    for kind in sorted(set(paths.values())):
        relevant = {p for p, k in expected.items() if k == kind}
        by_kind[kind] = {"source_documents": len(relevant)}
        by_kind[kind].update({name: len(members & relevant) for name, members in groups.items()})
    prefix = f"translations/{locale}/"
    return {
        "source_documents": len(paths),
        "counts": {name: len(value) for name, value in groups.items()},
        "paths": {name: sorted(value) for name, value in groups.items()},
        "by_kind": by_kind,
        "uncounted_translation_paths": sorted(
            p for p in base.keys() | draft.keys() if p.startswith(prefix) and p not in expected),
    }


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if result.returncode:
        raise ValueError("git read failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def exact_ref(repo: Path, ref: str) -> str:
    if not re.fullmatch(r"[0-9a-fA-F]{40}", ref):
        raise ValueError("refs must be full 40-hex commit IDs; fetch them before running")
    found = git(repo, "rev-parse", "--verify", ref + "^{commit}").decode().strip()
    if found != ref.lower():
        raise ValueError("commit identity mismatch")
    return found


def tree_blobs(repo: Path, ref: str) -> dict[str, str]:
    result = {}
    for item in git(repo, "ls-tree", "-rz", ref, "--", "translations").split(b"\0"):
        if not item:
            continue
        metadata, raw_path = item.split(b"\t", 1)
        mode, kind, blob = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8", "strict")
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"translation entry is not a regular file: {path}")
        result[path] = blob
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--source-ref", required=True, help="commit defining the catalogue denominator")
    parser.add_argument("--base-ref", required=True, help="pinned accepted branch snapshot")
    parser.add_argument("--draft-ref", required=True, help="pinned candidate branch snapshot")
    args = parser.parse_args()
    try:
        source, base, draft = (exact_ref(args.repo, x) for x in
                               (args.source_ref, args.base_ref, args.draft_ref))
        catalogue = json.loads(git(args.repo, "show", source + ":publication-catalog.json"))
        paths = catalogue_paths(catalogue)
        a, b = tree_blobs(args.repo, base), tree_blobs(args.repo, draft)
        report = {
            "kind": "translation-file-coverage/1",
            "scope": "Git file presence and blob identity only",
            "source_ref": source, "base_ref": base, "draft_ref": draft,
            "source_documents": len(paths),
            "source_by_kind": dict(sorted(Counter(paths.values()).items())),
            "locales": {loc: coverage(paths, a, b, loc) for loc in LOCALES},
            "not_established": ["body completeness", "translation fidelity", "source currency",
                                "rendition admission", "served website", "index admission"],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, UnicodeError, TypeError, AttributeError) as exc:
        print(json.dumps({"error": str(exc), "inventory_completed": False}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
