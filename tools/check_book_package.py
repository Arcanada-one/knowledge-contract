#!/usr/bin/env python3
"""Validate a Knowledge Contract book package and project it onto candidate export rows.

A package is a directory with manifest.json and the files the manifest names. This tool applies the JSON Schema in
schemas/book-package.schema.json to every record, then the cross-file rules a schema cannot express (digests, counts,
anchor identity, relation endpoints, stale propagation, status coherence, rights vs layers). It never reads the network,
never writes to an index and never claims runtime admission.
"""

from __future__ import annotations

import functools
import hashlib
import json
import math
import os
import re
import stat
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import jsonschema

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "book-package.schema.json"
RESTRICTED_LAYERS = frozenset(("document_md", "readable_md", "assets", "knowledge", "quality"))
ADMISSIBLE_OFFSET_KINDS = frozenset(("spine_offset",))
FORMAT_ANCHORS = {"pdf": {"page_bbox"}, "djvu": {"page_bbox"}, "ps": {"page_bbox"}, "epub": {"spine_offset"}, "html": {"section_block"},
                  "md": {"section_block"}, "txt": {"section_block"}, "tex": {"section_block"}, "xlsx": {"sheet_range"}, "json": {"json_pointer"},
                  "ppt": {"slide_block"}, "pptx": {"slide_block"}, "zip": set(), "tar_gz": set(), "sevenz": set()}


class PackageError(Exception):
    pass


DISPATCH = {"KCBookPackageManifest/v2": "Manifest", "KCBookObject/v2": "Object", "KCBookRelation/v2": "Relation",
            "KCBookEdit/v2": "Edit", "KCBookQuality/v2": "Quality"}
FORMAT_CHECKER = jsonschema.FormatChecker()


@FORMAT_CHECKER.checks("date-time", raises=(ValueError, TypeError))
def utc_seconds(value):
    datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return True


@functools.lru_cache(maxsize=None)
def schema_validator(definition: str | None = None) -> jsonschema.Draft202012Validator:
    """Validator for the whole schema, or for one definition so that an error names its real cause instead of a failed oneOf."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    if definition is not None:
        schema = {"$schema": schema["$schema"], "$ref": f"#/$defs/{definition}", "$defs": schema["$defs"]}
    return jsonschema.Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def schema_errors(record: object) -> list[str]:
    """Errors of one record. The record's `schema` field selects its definition; an unknown value is itself an error."""
    tag = record.get("schema") if isinstance(record, dict) else None
    if tag not in DISPATCH:
        return [f"<root>: unknown or missing schema field {tag!r}"]
    errors = sorted(schema_validator(DISPATCH[tag]).iter_errors(record), key=lambda e: list(e.absolute_path))
    out = []
    for e in errors:
        where = "/".join(str(p) for p in e.absolute_path) or "<root>"
        message = e.message if len(e.message) < 160 else e.message[:80] + " ... " + e.message[-70:]
        out.append(f"{where}: {message}")
    return out


def safe_file(root: Path, rel: str) -> Path | None:
    """A regular file below `root`, with no traversal or symlink in any component of `rel`."""
    relative = Path(rel)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        return None
    path = root
    try:
        for index, part in enumerate(relative.parts):
            path = path / part
            mode = os.lstat(path).st_mode
            required_type = stat.S_ISREG if index == len(relative.parts) - 1 else stat.S_ISDIR
            if not required_type(mode):
                return None
        inside = path.resolve().is_relative_to(root.resolve())
    except (OSError, RuntimeError, ValueError):
        return None
    return path if inside else None


def count_overlapping(text: str, part: str) -> int:
    """Occurrences of `part` in `text`, overlapping ones included ("aa" occurs twice in "xaaay")."""
    count, start = 0, text.find(part)
    while start != -1:
        count += 1
        start = text.find(part, start + 1)
    return count


def read_text_strict(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")  # strict and byte-exact: no universal-newline translation
    except UnicodeDecodeError as exc:
        raise PackageError(f"{path.name}: not valid UTF-8 (byte {exc.start})") from exc
    except OSError as exc:
        raise PackageError(f"{path.name}: unreadable ({type(exc).__name__})") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_lines(text: str, name: str = "input") -> list[str]:
    """Lines separated by "\\n" only, as a "\\n"-reader (the consumer) sees them. One empty trailing element is allowed
    (the final newline); a line ending in "\\r" is refused. U+2028, U+0085, \\x0b, \\x0c, \\x1c-\\x1e and a lone "\\r" are ordinary
    characters here, never separators, so the validator and a "\\n"-splitting reader see the same records."""
    parts = text.split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    for number, line in enumerate(parts, 1):
        if line.endswith("\r"):
            raise PackageError(f"{name}:{number}: line ends with a carriage return")
    return parts


def read_jsonl(path: Path) -> list[object]:
    records = []
    for number, line in enumerate(split_lines(read_text_strict(path), path.name), 1):
        if not line.strip():
            raise PackageError(f"{path.name}:{number}: blank line")
        try:
            records.append(strict_json(line, f"{path.name}:{number}"))
        except json.JSONDecodeError as exc:
            raise PackageError(f"{path.name}:{number}: invalid JSON ({exc.msg})") from exc
    return records


def strict_json(text: str, name: str = "JSON") -> object:
    """One interpretation at every reader: duplicate object members and non-JSON number constants are refused."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise PackageError(f"{name}: duplicate JSON member {key!r}")
            result[key] = value
        return result

    def nonfinite(value):
        raise PackageError(f"{name}: non-finite JSON number {value}")

    value = json.loads(text, object_pairs_hook=pairs, parse_constant=nonfinite)
    def scalar_strings(item):
        if isinstance(item, str):
            if any(0xD800 <= ord(c) <= 0xDFFF for c in item):
                raise PackageError(f"{name}: isolated surrogate in JSON string")
        elif isinstance(item, dict):
            for k, v in item.items():
                scalar_strings(k)
                scalar_strings(v)
        elif isinstance(item, list):
            for v in item:
                scalar_strings(v)
        elif isinstance(item, float) and not math.isfinite(item):
            raise PackageError(f"{name}: numeric value overflows the finite parser range")
    scalar_strings(value)
    return value


def _anchors_of(obj: dict) -> list[dict]:
    if obj.get("schema") == "KCBookRelation/v2":
        return [item["anchor"] for item in obj.get("evidence", [])]
    if obj.get("schema") == "KCBookEdit/v2":
        return [obj["anchor"]]
    return list(obj.get("evidence", []))


def anchors_overlap(a: dict, b: dict) -> bool:
    """Conservative source-region overlap; an undecidable intersection stays potentially affected."""
    if (a["representation_id"], a["source_sha256"]) != (b["representation_id"], b["source_sha256"]):
        return False
    if a["kind"] != b["kind"]:
        return True
    kind = a["kind"]
    if kind == "section_block":
        return (a["section_id"], a["block_id"]) == (b["section_id"], b["block_id"])
    if kind == "slide_block":
        return (a["slide"], a["block_id"]) == (b["slide"], b["block_id"])
    if kind == "spine_offset":
        return a["spine_item"] == b["spine_item"] and max(a["start"], b["start"]) <= min(a["end"], b["end"])
    if kind == "page_bbox":
        if a["page"] != b["page"]:
            return False
        if (a["bbox_origin"], a["bbox_unit"]) != (b["bbox_origin"], b["bbox_unit"]):
            return True
        x0, y0, x1, y1 = a["bbox"]
        u0, v0, u1, v1 = b["bbox"]
        return max(x0, u0) < min(x1, u1) and max(y0, v0) < min(y1, v1)
    if kind == "sheet_range":
        return a["sheet"] == b["sheet"]  # whole-sheet over-invalidation is deliberate
    if kind == "json_pointer":
        x, y = a["pointer"], b["pointer"]
        return x == y or x.startswith(y + "/") or y.startswith(x + "/")
    return True


def review_is_independent(review: dict) -> bool:
    """Check the declared separation; authenticating these identities belongs to the consumer's trust boundary."""
    return (review.get("reviewer_type") in ("human", "blind_agent")
            and review.get("reviewer_id") != review.get("producer_id")
            and bool(review.get("independence_basis", "").strip()))


def complete_supported_review(quality: dict, objects: list[dict], relations: list[dict]) -> bool:
    sem = quality["semantics"]
    review = sem.get("review", {})
    return (sem["status"] == "reviewed" and bool(objects) and review.get("result") == "supported"
            and review_is_independent(review)
            and set(review.get("object_ids", [])) == {o["object_id"] for o in objects}
            and set(review.get("relation_ids", [])) == {r["relation_id"] for r in relations}
            and review.get("sample_size") == len(objects)
            and all(o["status"] == "reviewed" for o in objects)
            and all(r["status"] == "reviewed" for r in relations))


def derive_package_status(manifest: dict, quality: dict, objects: list[dict], relations: list[dict]) -> str:
    """Total first-match status decision; structural/observation coherence is checked separately."""
    rep, sem, ext = manifest["representation"], quality["semantics"], quality["extraction"]
    if rep["integrity"] == "mismatch":
        return "blocked_integrity"
    if rep["completeness"] == "bibliography_only":
        return "bibliography_only"
    if "document_md" not in manifest["components"]:
        return "adapter_required"
    if sem["status"] in ("not_built", "not_measured") and not objects and not relations:
        return "structure_only"
    if (rep["integrity"] == "verified" and rep["completeness"] == "full" and ext["status"] == "pass"
            and quality.get("damage", {"status": "none"})["status"] == "none"
            and ext["checks"] and all(c["result"] in ("pass", "not_applicable") for c in ext["checks"])
            and any(c["result"] == "pass" for c in ext["checks"])
            and complete_supported_review(quality, objects, relations)):
        return "knowledge_ready"
    return "partial_pilot"


def check_package(root: Path) -> list[str]:
    """Return every problem found; an empty list means the package passed all of this tool's checks (not runtime admission)."""
    problems: list[str] = []
    if safe_file(root, "manifest.json") is None:
        return ["manifest.json: missing, not a regular file, or a symlink"]
    try:
        manifest = strict_json(read_text_strict(root / "manifest.json"), "manifest.json")
    except (PackageError, json.JSONDecodeError) as exc:
        return [f"manifest.json: unreadable ({type(exc).__name__}: {exc})" if isinstance(exc, PackageError) else f"manifest.json: unreadable ({type(exc).__name__})"]
    problems += [f"manifest.json: {m}" for m in schema_errors(manifest)]
    if problems:
        return problems
    comps, rep = manifest["components"], manifest["representation"]

    files = {k: v for k, v in comps.items() if k in ("document_md", "readable_md", "edits", "objects", "relations", "quality")}
    for name, meta in files.items():
        path = safe_file(root, meta["path"])
        if path is None:
            problems.append(f"{name}: file {meta['path']} is missing, not a regular file, or a symlink")
        elif sha256_file(path) != meta["sha256"]:
            problems.append(f"{name}: sha256 of {meta['path']} differs from the manifest")
    for asset in comps.get("assets", []):
        if asset["state"] == "present":
            path = safe_file(root, asset["path"])
            if path is None or sha256_file(path) != asset["sha256"]:
                problems.append(f"asset {asset['asset_id']}: missing or digest differs")
    if problems:
        return problems

    if "document_md" in comps and comps["document_md"]["input_sha256"] != rep["source_sha256"]:
        problems.append("document_md.input_sha256 must equal the source representation sha256")
    if "document_md" in comps and comps["document_md"]["path"] == comps["readable_md"]["path"]:
        problems.append("document_md and readable_md must be different files")

    rights = manifest["rights"]
    open_class = rights["license_class"] in ("author_open", "public_domain")
    if not open_class and RESTRICTED_LAYERS & set(rights["publishable_layers"]):
        problems.append("a work that is neither author_open nor public_domain may not publish any package layer")
    if not open_class and "license" in rights:
        problems.append("a work that is neither author_open nor public_domain may not declare a publication license")
    # A public_domain work carries its evidence and NO top-level `license` (schema): the public-domain text is covered by the evidence record alone. The layers
    # Arcanada writes (knowledge, quality) are published only under `public_domain.own_layers_license`, which covers exactly those two layers.
    if rights["license_class"] == "public_domain" and {"knowledge", "quality"} & set(rights["publishable_layers"]) and "own_layers_license" not in rights["public_domain"]:
        problems.append("a public_domain package publishes the knowledge or quality layer only under public_domain.own_layers_license")
    integrity_check = rep.get("integrity_check")
    if integrity_check:
        if integrity_check["observed_sha256"] != rep["source_sha256"]:
            problems.append("integrity_check.observed_sha256 differs from the source representation digest")
        equal = integrity_check["expected_sha256"] == integrity_check["observed_sha256"]
        if rep["integrity"] == "verified" and not equal:
            problems.append("verified integrity requires equal expected and observed source digests")
        if rep["integrity"] == "mismatch" and equal:
            problems.append("mismatch integrity requires different expected and observed source digests")

    objects = read_jsonl(root / comps["objects"]["path"])
    relations = read_jsonl(root / comps["relations"]["path"])
    edits = read_jsonl(root / comps["edits"]["path"])
    try:
        quality = strict_json(read_text_strict(root / comps["quality"]["path"]), "quality.json")
    except json.JSONDecodeError as exc:
        return [f"quality: invalid JSON ({exc.msg})"]

    for label, records, expected in (("objects", objects, comps["objects"]["count"]),
                                     ("relations", relations, comps["relations"]["count"]),
                                     ("edits", edits, comps["edits"]["count"])):
        if len(records) != expected:
            problems.append(f"{label}: manifest count {expected} differs from {len(records)} records")
        for index, record in enumerate(records, 1):
            problems += [f"{label}:{index}: {m}" for m in schema_errors(record)]
    problems += [f"quality: {m}" for m in schema_errors(quality)]
    if problems:
        return problems

    ids = [o["object_id"] for o in objects]
    if len(set(ids)) != len(ids):
        problems.append("objects: duplicate object_id")
    rel_ids = [r["relation_id"] for r in relations]
    if len(set(rel_ids)) != len(rel_ids):
        problems.append("relations: duplicate relation_id")
    if len({e["edit_id"] for e in edits}) != len(edits):
        problems.append("edits: duplicate edit_id")
    asset_ids = [a["asset_id"] for a in comps.get("assets", [])]
    if len(set(asset_ids)) != len(asset_ids):
        problems.append("assets: duplicate asset_id")
    known = set(ids)
    for rel in relations:
        for end in ("from", "to"):
            if rel[end] not in known:
                problems.append(f"relation {rel['relation_id']}: {end} endpoint {rel[end]} is not an object of this package")
        if rel["from"] == rel["to"]:
            problems.append(f"relation {rel['relation_id']}: a relation may not connect an object to itself")

    for record in [*objects, *relations, *edits]:
        if record["package_id"] != manifest["package_id"]:
            problems.append(f"{record['schema']}: package_id differs from the manifest")
        if record["schema"] == "KCBookObject/v2" and (record["work_id"], record["edition_id"]) != (manifest["work"]["work_id"], manifest["edition"]["edition_id"]):
            problems.append(f"object {record['object_id']}: work_id/edition_id differ from the manifest")
        for anchor in _anchors_of(record):
            if (anchor["representation_id"], anchor["source_sha256"]) != (rep["representation_id"], rep["source_sha256"]):
                problems.append(f"{record['schema']}: an evidence anchor names another representation or source hash")
            if anchor["kind"] not in FORMAT_ANCHORS[rep["format"]]:
                problems.append(f"{record['schema']}: anchor kind {anchor['kind']} does not fit source format {rep['format']}")
            if anchor["kind"] in ADMISSIBLE_OFFSET_KINDS and anchor["end"] < anchor["start"]:
                problems.append(f"{record['schema']}: anchor end precedes start")
            if anchor["kind"] == "page_bbox":
                x0, y0, x1, y1 = anchor["bbox"]
                if x1 <= x0 or y1 <= y0:
                    problems.append(f"{record['schema']}: bbox has no area")
    for edit in edits:
        if edit["status"] == "accepted" and edit["original_text"] == edit["replacement_text"]:
            problems.append(f"edit {edit['edit_id']}: accepted edit changes nothing")
        for dep in edit["depends_on_objects"]:
            if dep not in known:
                problems.append(f"edit {edit['edit_id']}: depends on unknown object {dep}")

    if "document_md" not in comps:
        if any(e["status"] == "accepted" for e in edits):
            problems.append("accepted edits require document_md and readable_md")
        if objects or relations:
            problems.append("a package without converter output cannot contain a built semantic layer")
    if not FORMAT_ANCHORS[rep["format"]] and ("document_md" in comps or objects or relations or edits):
        problems.append("archive formats have no member-path anchor profile; converter and semantic layers are unsupported")

    # Ledger: the readable edition is exactly the replay of the accepted edits over document.md, and digests chain.
    if "document_md" in comps:
        original = current = read_text_strict(root / comps["document_md"]["path"])
        applied: list[dict] = []
        chain = comps["document_md"]["sha256"]
        for edit in [e for e in edits if e["status"] == "accepted" and e["target"] == "readable_md"]:
            if edit["input_sha256"] != chain:
                problems.append(f"edit {edit['edit_id']}: input_sha256 is not the digest of the text it was applied to")
            before, after = edit["original_text"], edit["replacement_text"]
            if not before or not after:
                problems.append(f"edit {edit['edit_id']}: original_text and replacement_text must not be empty (an insertion or deletion has no search-reversible form)")
                continue
            if before not in current:
                problems.append(f"edit {edit['edit_id']}: original_text does not occur in the text it edits")
                continue
            if count_overlapping(current, before) != 1:
                problems.append(f"edit {edit['edit_id']}: original_text occurs {count_overlapping(current, before)} times (overlapping counted) in the text it edits; it must be unique so the edit is positional")
                continue
            current = current.replace(before, after, 1)
            if count_overlapping(current, after) != 1:
                problems.append(f"edit {edit['edit_id']}: replacement_text must occur exactly once in the text it produced, or the edit cannot be reversed")
                continue
            applied.append(edit)
            chain = hashlib.sha256(current.encode("utf-8")).hexdigest()
            if edit["output_sha256"] != chain:
                problems.append(f"edit {edit['edit_id']}: output_sha256 is not the digest of the text it produced")
        # Reversibility is checked, not assumed: undoing the applied edits in reverse order must give document.md exactly.
        undone = current
        for edit in reversed(applied):
            undone = undone.replace(edit["replacement_text"], edit["original_text"], 1)
        if undone != original:
            problems.append("the accepted edits do not reverse to document_md exactly")
        readable = read_text_strict(root / comps["readable_md"]["path"])
        if readable != current:
            problems.append("readable_md is not the replay of the accepted edits over document_md")

    # Staleness: accepted corrections affect overlapping anchors even if a producer omits depends_on_objects.
    # Explicit re-review is bound to the current object, relation and readable bytes below; it cannot be inferred from a timestamp.
    review = quality["semantics"].get("review", {})
    edits_by_id = {e["edit_id"]: e for e in edits}
    stale_edit_objs = set()
    for obj in objects:
        reviewed_edits = set(obj.get("reviewed_edit_ids", []))
        if any(eid not in edits_by_id or edits_by_id[eid]["status"] != "accepted" for eid in reviewed_edits):
            problems.append(f"object {obj['object_id']}: reviewed_edit_ids must name accepted edits of this package")
        for edit in edits:
            if edit["status"] not in ("accepted", "stale"):
                continue
            affected = (obj["object_id"] in edit["depends_on_objects"]
                        or any(anchors_overlap(a, edit["anchor"]) for a in obj["evidence"]))
            reconsidered = (edit["status"] == "accepted" and edit["edit_id"] in reviewed_edits
                            and obj["object_id"] in review.get("object_ids", [])
                            and review.get("result") == "supported" and review_is_independent(review)
                            and obj["status"] == "reviewed")
            if affected and not reconsidered:
                stale_edit_objs.add(obj["object_id"])
                if obj["status"] not in ("stale", "rejected"):
                    problems.append(f"object {obj['object_id']}: depends on a stale edit or an unreassessed accepted correction but is {obj['status']}")
    stale_objs = {o["object_id"] for o in objects if o["status"] in ("stale", "rejected")} | stale_edit_objs
    for rel in relations:
        if (rel["from"] in stale_objs or rel["to"] in stale_objs) and rel["status"] not in ("stale", "rejected"):
            problems.append(f"relation {rel['relation_id']}: touches a stale or rejected object but is {rel['status']}")

    # Quality: counts agree with the files; extraction and semantic quality stay apart.
    sem = quality["semantics"]
    damage = quality.get("damage")
    if damage is not None and damage["places"] != sum(d["count"] for d in damage["declarations"]):
        problems.append("quality.damage.places differs from the sum of the declaration counts; a declared place is counted once")
    if (sem["objects_count"], sem["relations_count"]) != (len(objects), len(relations)):
        problems.append("quality.semantics counts differ from the object and relation files")
    if quality["package_id"] != manifest["package_id"]:
        problems.append("quality: package_id differs from the manifest")
    ext = quality["extraction"]
    if "units_expected" in ext and "units_seen" in ext and ext["status"] == "pass" and ext["units_seen"] != ext["units_expected"]:
        problems.append("quality.extraction: status pass with units_seen different from units_expected")
    if ext["status"] == "pass":
        if not ext["checks"] or not any(c["result"] == "pass" for c in ext["checks"]):
            problems.append("quality.extraction: status pass requires at least one applicable passing check")
        if any(c["result"] == "fail" for c in ext["checks"]):
            problems.append("quality.extraction: status pass with a failed check")
        if any(c["result"] == "unknown" for c in ext["checks"]):
            problems.append("quality.extraction: status pass with an unknown check")
    if len({c["check_id"] for c in ext["checks"]}) != len(ext["checks"]):
        problems.append("quality.extraction: duplicate check_id")
    if "document_md" in comps and ext["status"] == "adapter_required":
        problems.append("quality.extraction adapter_required contradicts available converter output")
    if "document_md" not in comps and ext["status"] in ("pass", "partial"):
        problems.append("quality.extraction pass/partial requires converter output")
    if review:
        if review["sample_size"] != len(review["object_ids"]):
            problems.append("semantic review sample_size differs from its distinct object_ids")
        if not set(review["object_ids"]).issubset(known) or not set(review["relation_ids"]).issubset(set(rel_ids)):
            problems.append("semantic review names an unknown object or relation")
        for key in ("objects", "relations", "readable_md"):
            field = "readable_sha256" if key == "readable_md" else f"{key}_sha256"
            if key not in comps or review[field] != comps[key]["sha256"]:
                problems.append(f"semantic review {field} is not bound to the current package bytes")
        for obj in objects:
            if obj["object_id"] in review["object_ids"]:
                refs = obj["semantic_facets"]["assessment_refs"]
                if refs["state"] != "known" or review["review_id"] not in refs["value"]:
                    problems.append(f"object {obj['object_id']}: assessment_refs omit the package review that names it")
    status = manifest["package_status"]
    expected = derive_package_status(manifest, quality, objects, relations)
    if status != expected:
        problems.append(f"package_status {status} differs from derived {expected}; knowledge_ready requires a complete independent supported review, full verified source and extraction pass; structure_only requires an unbuilt semantic layer")
    if sem["status"] in ("not_built", "not_measured") and (objects or relations):
        problems.append("semantics not_built/not_measured but the semantic files are not empty")
    return problems


def render_knowledge_markdown(manifest: dict, objects: list[dict], relations: list[dict]) -> str:
    """Deterministic lossless record rendering; payload cannot escape its literal fenced container.

    This public rendering is unavailable for restricted/unknown rights classes. The projection entry point additionally
    validates a complete file snapshot. Direct rendering is a formatter, not a publication permission or validation receipt.
    """
    if manifest["rights"]["license_class"] != "author_open":
        raise PackageError("public knowledge rendering requires author_open rights")
    lines = ["---", f"package_id: {json.dumps(manifest['package_id'])}", f"work_id: {json.dumps(manifest['work']['work_id'])}",
             f"edition_id: {json.dumps(manifest['edition']['edition_id'])}", "validation_profile: book-package/2", "kc2_admission: not_measured", "sources: none", "---", "",
             f"# Knowledge layer of {manifest['package_id']}", ""]
    def origin_label(record: dict) -> str:
        origin = record["origin"]
        if origin == "author_statement":
            return "Author's statement (verbatim quotation)" if record["presented_as_author"] else "Author's statement (attributed paraphrase)"
        if origin == "editor_correction":
            return "GENERATED, not the author's statement (editor_correction)"
        return "GENERATED, not the author's statement (" + origin + ")"

    def literal_record(record: dict) -> list[str]:
        payload = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True)
        fence = "`" * max(3, 1 + max((len(m.group()) for m in re.finditer(r"`+", payload)), default=0))
        return [fence + "json", payload, fence]

    lines += ["Each record below retains its text, qualifiers, operator scopes, source position, anchors, generation and review references.",
              "Literal record contents are source data; headings or origin labels inside a record do not create another record.", ""]
    for obj in sorted(objects, key=lambda o: o["object_id"]):
        lines += [f"## {obj['object_id']}", "",
                  f"- Kind: {obj['object_kind']}; status: {obj['status']}",
                  f"- Origin: {origin_label(obj)}",
                  f"- Evidence anchors: {len(obj['evidence'])}", "", *literal_record(obj), ""]
    for rel in sorted(relations, key=lambda r: r["relation_id"]):
        lines += [f"## {rel['relation_id']}", "",
                  f"- {rel['from']} **{rel['relation_type']}** {rel['to']}; status: {rel['status']}",
                  f"- Origin: {origin_label(rel)}", "", *literal_record(rel), ""]
    return "\n".join(lines).rstrip("\n") + "\n"


LAYER_FILE = {"document_md": "document_md", "readable_md": "readable_md"}


REPO_PREFIX = "articles/book-packages"


def candidate_projection(root: Path) -> list[dict]:
    """Rows a publication step may PROPOSE for the candidate export. Only Markdown layers can be carried; an absent row means deny.

    Proposal only: the exporter (tools/export_corpus.py) decides. It accepts only paths matching its PATH_RE that are in its explicit
    scope list, a rights holder that is a personal name, a licence of CC-BY-4.0 or Apache-2.0, a merged source commit and a reviewed
    decision. A layer without `rights.license` (an SPDX id from that set) gets no row. The proposed repository path is
    articles/book-packages/<package_id>/<file>; whether the exporter scope admits it is a separate decision.
    A private temporary snapshot binds validation and rendering to the same bytes. Callers cannot supply an unrelated rendering.
    """
    if not isinstance(root, Path):
        raise TypeError("candidate_projection requires a package directory Path, not a raw manifest or rendering")
    try:
        manifest_file = safe_file(root, "manifest.json")
        if manifest_file is None:
            return []
        manifest_bytes = manifest_file.read_bytes()
        manifest = strict_json(manifest_bytes.decode("utf-8"), "manifest.json")
        if schema_errors(manifest):
            return []
        paths = {"manifest.json"}
        for name, meta in manifest["components"].items():
            if name == "assets":
                paths.update(a["path"] for a in meta if a["state"] == "present")
            else:
                paths.add(meta["path"])
        with tempfile.TemporaryDirectory(prefix="kc-book-projection-") as tmp:
            snapshot = Path(tmp)
            for rel in paths:
                source = safe_file(root, rel)
                if source is None:
                    return []
                target = snapshot / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(manifest_bytes if rel == "manifest.json" else source.read_bytes())
            if check_package(snapshot):
                return []
            comps = manifest["components"]
            objects = read_jsonl(snapshot / comps["objects"]["path"])
            relations = read_jsonl(snapshot / comps["relations"]["path"])
    except (PackageError, OSError, UnicodeDecodeError, json.JSONDecodeError):
        return []
    rights, rows = manifest["rights"], []
    licence = rights.get("license")
    # public_domain gets no rows here: the corpus exporter's scope and rights check (a personal-name holder and an author's licence) do not describe
    # a public-domain work, and a book library is not the corpus. Deny until a decision widens it.
    if rights["license_class"] != "author_open" or licence not in ("CC-BY-4.0", "Apache-2.0"):
        return rows
    pid, q = manifest["package_id"], manifest["package_status"]
    if q in ("blocked_integrity", "bibliography_only", "adapter_required"):
        return rows
    knowledge_md = render_knowledge_markdown(manifest, objects, relations)
    limits = (f"package_status {q}; quality blocks and semantic review are in quality.json of the package; does not establish extraction "
              f"fidelity, semantic correctness or runtime admission")
    for layer in rights["publishable_layers"]:
        if layer in LAYER_FILE and manifest["components"].get(layer):
            meta = manifest["components"][layer]
            name, digest = meta["path"], meta["sha256"]
            if not name.endswith(".md"):
                continue
        elif layer == "knowledge" and knowledge_md is not None:
            name, digest = "knowledge.md", hashlib.sha256(knowledge_md.encode("utf-8")).hexdigest()
        else:
            continue
        rows.append({"layer": layer, "path_in_package": name, "proposed_repo_path": f"{REPO_PREFIX}/{pid}/{name}", "sha256": digest,
                     "rights_holder": rights.get("holder", "unknown"), "license": licence, "status": "proposed", "limits": limits,
                     "kc2_admission": "not_measured", "package_id": pid})
    return rows


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_book_package.py PACKAGE_DIR", file=sys.stderr)
        return 2
    try:
        problems = check_package(Path(argv[1]))
    except PackageError as exc:
        problems = [str(exc)]
    for problem in problems:
        print(f"BOOK_PACKAGE_FAIL {problem}")
    if problems:
        return 1
    print("BOOK_PACKAGE_PASS (structure only; no extraction truth, no runtime admission)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
