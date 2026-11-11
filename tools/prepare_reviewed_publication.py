#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prepare exact title/source deltas for already reviewed translations.

Read-only Git access, no network, credentials, publication decision, index write,
merge or deployment. Output files are proposals outside the source checkout.
A previous fidelity review is never relabelled as review of these new bytes.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
TITLE_KEYS = {"title", "short_title", "subtitle", "previous_title"}
LANGUAGES = {"ru": (2, 3, ": "), "zh-Hans": (4, 5, "：")}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def text_bytes(data: bytes) -> str:
    text = data.decode("utf-8", errors="strict")
    if not text.endswith("\n") or any(c in text for c in ("\r", "\x00", "\u0085", "\u2028", "\u2029", "\ufeff")):
        raise ValueError("expected UTF-8, LF-only, final-newline text")
    return text


def document(text: str) -> tuple[list[str], dict[str, str], str, str, str]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing front matter")
    header, body = text[4:].split("\n---\n", 1)
    lines = header.split("\n")
    fields: dict[str, str] = {}
    for line in lines:
        m = re.fullmatch(r"([a-z_]+):\s*(.*)", line)
        if not m or m[1] in fields:
            raise ValueError("unsupported or duplicate front-matter field")
        value = m[2]
        if value.startswith('"'):
            value = json.loads(value)
        if not isinstance(value, str):
            raise ValueError("non-string front-matter value")
        fields[m[1]] = value
    m = re.search(r"(?m)^# ([^\n]+)\n", body)
    if not m:
        raise ValueError("missing H1")
    return lines, fields, body[:m.start()], m[1], body[m.end():]


def old_anchor(title: str) -> str:
    # Used only to recognize the exact existing compatibility-anchor shape.
    # Actual section maps are obtained from the required Pandoc parser below.
    slug = re.sub(r"[^\w\-\s]", "", title.lower(), flags=re.UNICODE)
    slug = re.sub(r"\s+", "-", slug)
    return re.sub(r"^[^a-zA-Z]*", "", slug)


def unchanged_source_body(old: bytes, current: bytes) -> dict[str, Any]:
    old_text, current_text = text_bytes(old), text_bytes(current)
    a_lines, a, a_prefix, a_h1, a_rest = document(old_text)
    b_lines, b, b_prefix, b_h1, b_rest = document(current_text)
    if a_h1 != a.get("title") or b_h1 != b.get("title"):
        raise ValueError("source title/H1 disagreement")
    if a_prefix.strip():
        raise ValueError("unexpected old source prefix")
    permitted_prefix = ('<!-- markdownlint-disable-next-line MD033 -->\n'
                        f'<a id="{old_anchor(a["title"])}"></a>')
    if b_prefix.strip() not in ("", permitted_prefix):
        raise ValueError("unexpected current source prefix")
    if b.get("title") != a.get("title"):
        if b.get("previous_title") != a["title"]:
            raise ValueError("missing exact previous-title mapping")
        if b.get("title") != b.get("short_title", "") + ": " + b.get("subtitle", ""):
            raise ValueError("invalid current short-name mapping")
    def retained(lines: list[str]) -> list[str]:
        return [line for line in lines if line.split(":", 1)[0] not in TITLE_KEYS]
    if retained(a_lines) != retained(b_lines) or a_rest != b_rest:
        raise ValueError("source changed outside the explicit title/compatibility-anchor scope")
    return {"kind": "exact-byte-comparison-after-explicit-title-map",
            "old_title": a["title"], "current_title": b["title"],
            "retained_body_sha256": hashlib.sha256(a_rest.encode()).hexdigest(),
            "scientific_body_unchanged": True}


def adapt_target(data: bytes, name: list[str], language: str,
                 old_commit: str, old_source_blob: str,
                 source_commit: str, source_blob: str) -> bytes:
    lines, fields, prefix, heading, rest = document(text_bytes(data))
    if fields.get("language") != language:
        raise ValueError("target language mismatch")
    if fields.get("source_commit") != old_commit or fields.get("source_git_blob") != old_source_blob:
        raise ValueError("target does not declare the reviewed source")
    if fields.get("translation_status") != "author-draft":
        raise ValueError("unexpected target status; do not silently replace a decision")
    # Every existing target in this batch declares a stable source-heading anchor.
    match = re.fullmatch(r"(.*?) \{#([A-Za-z0-9_-]+)\}", heading)
    if not match or match[1] != fields.get("title") or prefix.strip():
        raise ValueError("unsupported target H1/anchor structure")
    short_index, subtitle_index, separator = LANGUAGES[language]
    short, subtitle = name[short_index], name[subtitle_index]
    title = short + separator + subtitle
    replacements = {
        "title": title, "short_title": short, "subtitle": subtitle,
        "source_commit": source_commit, "source_git_blob": source_blob,
        "source_review_state": "title-map-proposal; exact-delta review pending",
        "original_source_commit": old_commit,
        "original_source_git_blob": old_source_blob,
        "original_rendition_git_blob": git_blob(data),
    }
    out, seen = [], set()
    for line in lines:
        key = line.split(":", 1)[0]
        out.append(key + ": " + json.dumps(replacements[key], ensure_ascii=False)
                   if key in replacements else line)
        seen.add(key)
    out.extend(key + ": " + json.dumps(value, ensure_ascii=False)
               for key, value in replacements.items() if key not in seen)
    result = ("---\n" + "\n".join(out) + "\n---\n" + prefix +
              "# " + title + " {#" + match[2] + "}\n" + rest).encode()
    # No body, link, equation, table, identifier or old target anchor is edited.
    _, _, new_prefix, new_heading, new_rest = document(text_bytes(result))
    if new_prefix != prefix or new_rest != rest or not new_heading.endswith(" {#" + match[2] + "}"):
        raise ValueError("unexpected target body or anchor mutation")
    return result


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=30).stdout


def safe_path(value: str) -> str:
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "\\" in value or ":" in value or not p.parts:
        raise ValueError("unsafe repository path")
    return value


def checked_commit(value: str) -> str:
    if not HEX40.fullmatch(value):
        raise ValueError("an immutable full commit is required")
    return value


def load_json(data: bytes) -> Any:
    def unique(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--manifest", type=Path,
                        default=Path("translations/release/first-reviewed-batch.json"))
    parser.add_argument("--output", type=Path,
                        help="New directory outside the source checkout for proposed files and exact diffs")
    args = parser.parse_args()
    repo = args.repository.resolve()
    source_commit = checked_commit(args.source_commit)
    manifest_path = args.manifest if args.manifest.is_absolute() else repo / args.manifest
    manifest = load_json(manifest_path.read_bytes())
    if manifest.get("schema") != "knowledge-contract.reviewed-batch-input/1":
        raise ValueError("unsupported reviewed-batch input")
    old_commit = checked_commit(manifest["reviewed_source_commit"])
    target_commit = checked_commit(manifest["target_snapshot"])
    # The English source must be a descendant of the earlier reviewed source.
    git(repo, "merge-base", "--is-ancestor", old_commit, source_commit)
    names = load_json(git(repo, "show", source_commit + ":reference/document-naming/names.json"))
    name_rows = {row[0]: row for row in names["documents"]}
    catalogue = load_json(git(repo, "show", source_commit + ":publication-catalog.json"))
    works = {entry["slug"]: entry for entry in catalogue["documents"]}
    output = args.output.resolve() if args.output else None
    if output:
        if output == repo or repo in output.parents or output.exists():
            raise ValueError("output must be a new directory outside the repository")
    entries, files, seen = [], {}, set()
    for work in manifest["works"]:
        slug, path = work["work"], safe_path(work["source_path"])
        if slug not in works or works[slug]["path"] != path or slug in seen:
            raise ValueError("unknown, duplicate or wrong-path catalogue work")
        seen.add(slug)
        old = git(repo, "show", old_commit + ":" + path)
        current = git(repo, "show", source_commit + ":" + path)
        if git_blob(old) != work["reviewed_source_blob"]:
            raise ValueError("reviewed source blob mismatch")
        evidence_path = safe_path(work["evidence_path"])
        # Evidence is a retained provenance record, not a newly issued verdict.
        evidence = (repo / evidence_path).read_bytes()
        if str(work["review_comment_id"]).encode() not in evidence:
            raise ValueError("review evidence does not identify the actual primary review")
        alignment = unchanged_source_body(old, current)
        for language, expected_blob in work["target_blobs"].items():
            if language not in LANGUAGES or not HEX40.fullmatch(expected_blob):
                raise ValueError("invalid target binding")
            target_path = "translations/" + language + "/" + path
            target = git(repo, "show", target_commit + ":" + target_path)
            if git_blob(target) != expected_blob:
                raise ValueError("reviewed target blob mismatch")
            prepared = adapt_target(target, name_rows[slug], language, old_commit,
                                    work["reviewed_source_blob"], source_commit, git_blob(current))
            files[target_path] = prepared
            entries.append({
                "work": slug, "language": language, "source_path": path,
                "source_revision": source_commit, "source_blob": git_blob(current),
                "source_sha256": hashlib.sha256(current).hexdigest(),
                "reviewed_source_revision": old_commit,
                "reviewed_source_blob": work["reviewed_source_blob"],
                "old_target_revision": target_commit, "old_target_blob": expected_blob,
                "target_path": target_path, "prepared_target_blob": git_blob(prepared),
                "prepared_target_sha256": hashlib.sha256(prepared).hexdigest(),
                "retained_target_body_sha256": hashlib.sha256(document(text_bytes(target))[4].encode()).hexdigest(),
                "source_alignment": alignment,
                "original_review_comment_id": work["review_comment_id"],
                "original_reviewer": work["reviewer"],
                "translation_author": work["translator"],
                "original_review_evidence_path": evidence_path,
                "original_review_evidence_blob": git_blob(evidence),
                "exact_delta_review_required": True,
                "section_map_and_renderer_checks": "not_performed",
                "admission": "not_issued", "deployment": "not_performed",
            })
    if len(entries) != manifest["expected_target_count"] or len(seen) != manifest["expected_work_count"]:
        raise ValueError("finite scope count mismatch")
    report = {"schema": "knowledge-contract.rendition-preparation/1", "pass": True,
              "scope": "exact-byte identity after declared title metadata and H1 mapping only",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              "target_count": len(entries), "entries": entries,
              "not_established": ["new independent fidelity verdict", "rendition admission",
                                  "renderer link/section parity", "source merge", "site deploy", "index refresh"]}
    if output:
        output.mkdir(parents=True)
        patches = []
        for path, prepared in files.items():
            destination = output / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(prepared)
            old = git(repo, "show", target_commit + ":" + path)
            patches.extend(difflib.unified_diff(text_bytes(old).splitlines(keepends=True),
                                               text_bytes(prepared).splitlines(keepends=True),
                                               fromfile="a/" + path, tofile="b/" + path))
        (output / "title-source-alignment.patch").write_text("".join(patches), encoding="utf-8")
        (output / "preparation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, subprocess.SubprocessError) as error:
        print(json.dumps({"schema": "knowledge-contract.rendition-preparation/1", "pass": False,
                          "reason": str(error), "admission": "not_issued"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
