#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate publication structure, Markdown navigation and evidence references.

Usage: python3 tools/check_publication.py [repository-root]
Requires Pandoc 3.1.3; uses its Markdown AST and GitHub-compatible heading IDs.
No network requests and no assertions about the truth of scientific claims.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

EXPECTED_COUNTS = {"paper": 11, "specification": 11, "study": 7, "glossary": 1, "bibliography": 1, "appendix": 2}
KINDS = {
    "paper": ("papers", "PAPER.md", "scientific-paper"),
    "specification": ("engineering/specifications", "SPECIFICATION.md", "engineering-specification"),
    "study": ("engineering/studies", "STUDY.md", "engineering-study"),
    "glossary": ("reference", "GLOSSARY.md", "glossary"),
    "bibliography": ("reference", "BIBLIOGRAPHY.md", "bibliography"),
    "appendix": ("appendices", "APPENDIX.md", "appendix"),
}
REQUIRED_META = ("name", "title", "artifact", "edition", "author", "language", "license", "description")
FORMAT = "markdown+gfm_auto_identifiers+pipe_tables+tex_math_dollars+tex_math_single_backslash+autolink_bare_uris"
EVIDENCE_INDEX = "engineering/studies/evidence-index.json"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
OPAQUE_NUMBERED_NAME = re.compile(r"(?:[a-z][0-9]+|[0-9]+)\Z", re.I)
EDITION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*))?\Z")


def text_of(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(text_of(x) for x in value)
    if not isinstance(value, dict):
        return ""
    kind = value.get("t")
    if kind in {"Space", "SoftBreak", "LineBreak"}:
        return " "
    if kind in {"Code", "Math"}:
        return value["c"][-1]
    if kind in {"Link", "Image"}:
        return text_of(value["c"][1])
    return text_of(value.get("c", ""))


def walk(value: object):
    if isinstance(value, list):
        for item in value:
            yield from walk(item)
    elif isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk(item)


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.append(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


class PublicationCheck:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.errors: list[str] = []
        self.cache: dict[Path, dict | None] = {}
        self.catalog_by_path: dict[str, dict] = {}

    def fail(self, origin: str, message: str) -> None:
        self.errors.append(f"{origin}: {message}")

    def relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def local_target(self, origin: Path, raw: str, *, allow_remote: bool = False) -> tuple[Path, str] | None:
        label = self.relative(origin)
        if not isinstance(raw, str) or not raw:
            self.fail(label, "empty or non-string reference")
            return None
        parts = urlsplit(raw)
        if parts.scheme or raw.startswith("//"):
            if allow_remote and parts.scheme in {"http", "https", "mailto"}:
                return None
            self.fail(label, f"reference must be a repository-relative path: {raw}")
            return None
        decoded = unquote(parts.path)
        if decoded.startswith("/") or "\\" in decoded:
            self.fail(label, f"absolute or non-portable path: {raw}")
            return None
        target = (origin.parent / decoded).resolve() if decoded else origin.resolve()
        if not target.is_relative_to(self.root):
            self.fail(label, f"path escape: {raw}")
            return None
        if not target.exists():
            self.fail(label, f"broken link: {raw}")
            return None
        return target, unquote(parts.fragment)

    def markdown(self, path: Path) -> dict | None:
        path = path.resolve()
        if path in self.cache:
            return self.cache[path]
        command = ["pandoc", "--from=" + FORMAT, "--to=json", str(path)]
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode:
            self.fail(self.relative(path), "Markdown parse failed: " + result.stderr.strip())
            self.cache[path] = None
            return None
        ast = json.loads(result.stdout)
        refs = HTMLReferences()
        headings, links = [], []
        for node in walk(ast["blocks"]):
            kind = node.get("t")
            if kind == "Header":
                headings.append((node["c"][0], node["c"][1][0], text_of(node["c"][2])))
            elif kind in {"Link", "Image"}:
                links.append(node["c"][2][0])
            elif kind in {"RawBlock", "RawInline"} and node["c"][0] in {"html", "html5"}:
                refs.feed(node["c"][1])
        ids = [h[1] for h in headings] + refs.ids
        duplicates = [x for x, n in Counter(ids).items() if x and n > 1]
        if duplicates:
            self.fail(self.relative(path), "duplicate anchors: " + ", ".join(duplicates))
        parsed = {"meta": ast.get("meta", {}), "headings": headings, "ids": set(ids), "links": links + refs.links}
        self.cache[path] = parsed
        return parsed

    def check_links(self, path: Path) -> None:
        doc = self.markdown(path)
        if not doc:
            return
        for raw in doc["links"]:
            resolved = self.local_target(path, raw, allow_remote=True)
            if not resolved:
                continue
            target, fragment = resolved
            if not fragment:
                continue
            if target.suffix.lower() == ".md":
                parsed = self.markdown(target)
                if parsed and fragment not in parsed["ids"]:
                    self.fail(self.relative(path), f"broken anchor: {raw}")
            elif target.suffix.lower() == ".json" and fragment.startswith("/"):
                self.json_pointer(target, fragment, self.relative(path))
            elif re.fullmatch(r"L[1-9][0-9]*(?:-L[1-9][0-9]*)?", fragment) and target.is_file():
                lines = [int(x) for x in re.findall(r"[0-9]+", fragment)]
                if max(lines) > len(target.read_text(encoding="utf-8").splitlines()) or lines[-1] < lines[0]:
                    self.fail(self.relative(path), f"broken line anchor: {raw}")
            else:
                self.fail(self.relative(path), f"unverifiable anchor target: {raw}")

    def load_json(self, path: Path) -> dict | list | None:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            self.fail(self.relative(path), f"invalid or missing JSON: {exc}")
            return None

    def json_pointer(self, target: Path, pointer: str, origin: str) -> None:
        data = self.load_json(target)
        if data is None:
            return
        if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")) or re.search(r"~(?![01])", pointer):
            self.fail(origin, f"invalid JSON pointer: {pointer!r}")
            return
        try:
            for token in pointer.split("/")[1:] if pointer else []:
                token = token.replace("~1", "/").replace("~0", "~")
                if isinstance(data, list):
                    if not re.fullmatch(r"0|[1-9][0-9]*", token):
                        raise KeyError(token)
                    data = data[int(token)]
                elif isinstance(data, dict):
                    data = data[token]
                else:
                    raise KeyError(token)
        except (KeyError, IndexError, TypeError, ValueError):
            self.fail(origin, f"broken JSON pointer: {self.relative(target)}#{pointer}")

    def check_catalog(self) -> dict | None:
        catalog_path = self.root / "publication-catalog.json"
        catalog = self.load_json(catalog_path)
        if (not isinstance(catalog, dict) or catalog.get("schema_version") != 1
                or not isinstance(catalog.get("edition"), str)
                or not EDITION.fullmatch(catalog["edition"])):
            self.fail("publication-catalog.json", "expected schema_version 1 and a numeric publication edition (major.minor[.patch])")
            return None
        docs = catalog.get("documents")
        if not isinstance(docs, list):
            self.fail("publication-catalog.json", "documents must be an array")
            return None
        counts = Counter(d.get("type") for d in docs if isinstance(d, dict))
        if counts != Counter(EXPECTED_COUNTS):
            self.fail("publication-catalog.json", f"document counts differ: expected {EXPECTED_COUNTS}; found {dict(counts)}")
        seen_slugs, seen_titles = set(), set()
        for doc in docs:
            if not isinstance(doc, dict):
                self.fail("publication-catalog.json", "document must be an object")
                continue
            kind, slug, path, title = (doc.get(k) for k in ("type", "slug", "path", "title"))
            if kind not in KINDS or not isinstance(slug, str) or not SLUG.fullmatch(slug):
                self.fail("publication-catalog.json", f"unknown type or invalid readable slug: {doc}")
                continue
            if OPAQUE_NUMBERED_NAME.fullmatch(slug):
                self.fail("publication-catalog.json", f"opaque numbered canonical slug is prohibited: {slug}")
                continue
            if doc.get("edition") != catalog["edition"]:
                self.fail("publication-catalog.json", f"document edition differs from catalogue: {slug}")
            directory, filename, artifact = KINDS[kind]
            expected_path = f"{directory}/{slug}/{filename}"
            if path != expected_path:
                self.fail(str(path), f"wrong file type/path: expected {expected_path}")
            if not isinstance(path, str):
                continue
            if path in self.catalog_by_path or slug in seen_slugs:
                self.fail(path, "duplicate catalog path or slug")
            if not isinstance(title, str) or not title.strip():
                self.fail(path, "missing catalog title")
            elif OPAQUE_NUMBERED_NAME.fullmatch(title.strip()):
                self.fail(path, "opaque numbered canonical title is prohibited")
            elif title.casefold() in seen_titles:
                self.fail(path, "duplicate catalog title")
            else:
                seen_titles.add(title.casefold())
            seen_slugs.add(slug)
            self.catalog_by_path[path] = doc
            resolved = self.local_target(catalog_path, path)
            if not resolved or not resolved[0].is_file():
                continue
            file_path = resolved[0]
            parsed = self.markdown(file_path)
            if not parsed:
                continue
            meta = {key: text_of(value).strip() for key, value in parsed["meta"].items()}
            for key in REQUIRED_META:
                if not meta.get(key):
                    self.fail(path, f"missing frontmatter metadata: {key}")
            for key, value in {"name": slug, "title": title, "artifact": artifact, "edition": catalog["edition"], "language": "en", "license": "CC-BY-4.0"}.items():
                if meta.get(key) != value:
                    self.fail(path, f"frontmatter {key} differs: expected {value!r}, found {meta.get(key)!r}")
            h1 = [h for h in parsed["headings"] if h[0] == 1]
            if len(h1) != 1:
                self.fail(path, f"expected one H1; found {len(h1)}")
            elif h1[0][2] != title:
                self.fail(path, "H1 differs from catalog title")
            if kind == "paper":
                body = file_path.read_text(encoding="utf-8")
                forbidden = [r"\bMM_A[A-Za-z0-9_.-]*", r"not in this release", r"\b[0-9]+\.[0-9]+\.[0-9]+-draft(?:\.[0-9]+)?\b", r"\bmm-envelope/0\.1\b", r"sandbox:/"]
                for pattern in forbidden:
                    if re.search(pattern, body, re.I):
                        self.fail(path, "internal or unfinished-publication marker in scientific text: " + pattern)
            self.check_links(file_path)
        return catalog

    def check_evidence(self, edition: str) -> None:
        origin = self.root / EVIDENCE_INDEX
        index = self.load_json(origin)
        if not isinstance(index, dict) or index.get("schema") != "knowledge-contract.claim-evidence-index/1" or index.get("edition") != edition:
            self.fail(EVIDENCE_INDEX, "unsupported evidence-index schema or edition")
            return
        studies, claims = index.get("studies"), index.get("claims")
        if not isinstance(studies, list) or not isinstance(claims, list):
            self.fail(EVIDENCE_INDEX, "studies and claims must be arrays")
            return
        if index.get("claim_count") != len(claims) or not claims:
            self.fail(EVIDENCE_INDEX, "claim_count must equal the nonempty claims array length")
        expected_studies = {path for path, doc in self.catalog_by_path.items() if doc["type"] == "study"}
        indexed_studies, study_names = set(), set()
        for study in studies:
            if not isinstance(study, dict) or not all(isinstance(study.get(k), str) and study[k] for k in ("name", "report", "origin")):
                self.fail(EVIDENCE_INDEX, "study entry needs name, report and origin")
                continue
            if study["name"] in study_names:
                self.fail(EVIDENCE_INDEX, "duplicate study name: " + study["name"])
            study_names.add(study["name"])
            report = self.local_target(origin, study["report"])
            evidence_origin = self.local_target(origin, study["origin"])
            if report:
                relative = self.relative(report[0])
                indexed_studies.add(relative)
                if relative not in expected_studies or self.catalog_by_path.get(relative, {}).get("slug") != study["name"]:
                    self.fail(EVIDENCE_INDEX, "study report/name does not match catalog: " + study["report"])
            if evidence_origin:
                self.check_evidence_origin(evidence_origin[0], study["name"])
        if indexed_studies != expected_studies:
            self.fail(EVIDENCE_INDEX, "evidence index must cover exactly the catalog studies")
        claim_ids = set()
        required = ("claim_id", "study", "statement", "claim_kind", "model", "test_or_argument", "evidence", "counterexample_or_rival", "result", "limits", "scientific_context", "public_reproduction")
        for claim in claims:
            if not isinstance(claim, dict):
                self.fail(EVIDENCE_INDEX, "claim must be an object")
                continue
            label = EVIDENCE_INDEX + ":" + str(claim.get("claim_id", "unknown"))
            for key in required:
                if key not in claim or claim[key] is None or claim[key] == "":
                    self.fail(label, "missing claim field: " + key)
            identity = claim.get("claim_id")
            if not isinstance(identity, str) or not SLUG.fullmatch(identity):
                self.fail(label, "claim_id must be a readable kebab-case identifier")
            elif identity in claim_ids:
                self.fail(label, "duplicate claim_id")
            else:
                claim_ids.add(identity)
            report = self.local_target(origin, claim.get("study"))
            if report and self.relative(report[0]) not in indexed_studies:
                self.fail(label, "claim refers to a study outside the index")
            for key in ("evidence", "limits", "scientific_context"):
                if not isinstance(claim.get(key), list) or not claim[key]:
                    self.fail(label, key + " must be a nonempty array")
            for item in claim.get("evidence", []) if isinstance(claim.get("evidence"), list) else []:
                if not isinstance(item, dict):
                    self.fail(label, "evidence reference must be an object")
                    continue
                target = self.local_target(origin, item.get("path"))
                if target and "json_pointer" in item:
                    self.json_pointer(target[0], item["json_pointer"], label)
            for path in claim.get("scientific_context", []) if isinstance(claim.get("scientific_context"), list) else []:
                target = self.local_target(origin, path)
                if target and self.catalog_by_path.get(self.relative(target[0]), {}).get("type") != "paper":
                    self.fail(label, "scientific_context must refer to a catalog scientific paper")
        for directory in (self.root / "engineering/studies").glob("*/evidence"):
            for path in directory.rglob("*.md"):
                self.check_links(path)

    def check_evidence_origin(self, path: Path, study_name: str) -> None:
        record = self.load_json(path)
        if not isinstance(record, dict) or record.get("schema") != "knowledge-contract.study-evidence-origin/1" or record.get("study") != study_name:
            self.fail(self.relative(path), "evidence origin schema/study mismatch")
            return
        files = record.get("files")
        if not isinstance(files, list):
            self.fail(self.relative(path), "origin files must be an array")
            return
        seen = set()
        for item in files:
            if not isinstance(item, dict) or not isinstance(item.get("file"), str) or not item.get("representation"):
                self.fail(self.relative(path), "origin entry needs file and representation")
                continue
            if item["file"] in seen:
                self.fail(self.relative(path), "duplicate origin file: " + item["file"])
            seen.add(item["file"])
            target = self.local_target(path, item["file"])
            if not target or not target[0].is_file():
                continue
            raw = target[0].read_bytes()
            digest = item.get("published_sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                self.fail(self.relative(path), "origin entry needs an exact published_sha256: " + item["file"])
            elif sha256(raw).hexdigest() != digest:
                self.fail(self.relative(path), "evidence hash mismatch: " + item["file"])
            if type(item.get("size_bytes")) is not int or item["size_bytes"] != len(raw):
                self.fail(self.relative(path), "evidence size mismatch: " + item["file"])
            if item.get("byte_identity_verified") is True and item.get("original_source_sha256") != digest:
                self.fail(self.relative(path), "claimed exact source bytes have a different digest: " + item["file"])
        actual = {p.relative_to(path.parent).as_posix() for p in path.parent.rglob("*")
                  if p.is_file() and p != path and "__pycache__" not in p.parts}
        if seen != actual:
            self.fail(self.relative(path), "origin must cover every evidence file exactly once")


def check(root: Path) -> list[str]:
    try:
        version = subprocess.check_output(["pandoc", "--version"], text=True).splitlines()[0].split()[1]
    except (OSError, subprocess.CalledProcessError, IndexError) as exc:
        return [f"Pandoc 3.1.3 is required: {exc}"]
    if version != "3.1.3":
        return [f"Pandoc 3.1.3 is required; found {version}"]
    checker = PublicationCheck(root)
    catalog = checker.check_catalog()
    if catalog:
        checker.check_evidence(catalog["edition"])
    return checker.errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = check(root)
    for error in errors:
        print("PUBLICATION_CHECK_FAIL " + error)
    if errors:
        return 1
    print("PUBLICATION_CHECK_PASS: catalog, document metadata, Markdown links, evidence references and hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
