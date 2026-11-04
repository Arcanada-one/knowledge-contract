#!/usr/bin/env python3
"""Validate a Knowledge Contract book package and project it onto candidate export rows.

A package is a directory with manifest.json and the files the manifest names. This tool applies the JSON Schema in
schemas/book-package.schema.json to every record, then the cross-file rules a schema cannot express (digests, counts,
anchor identity, relation endpoints, stale propagation, status coherence, rights vs layers). It never reads the network,
never writes to an index and never claims KC2 admission.
"""

from __future__ import annotations

import functools
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "book-package.schema.json"
RESTRICTED_LAYERS = frozenset(("document_md", "readable_md", "assets"))
ADMISSIBLE_OFFSET_KINDS = frozenset(("spine_offset",))


class PackageError(Exception):
    pass


DISPATCH = {"KCBookPackageManifest/v1": "Manifest", "KCBookObject/v1": "Object", "KCBookRelation/v1": "Relation",
            "KCBookEdit/v1": "Edit", "KCBookQuality/v1": "Quality"}


@functools.lru_cache(maxsize=None)
def schema_validator(definition: str | None = None) -> jsonschema.Draft202012Validator:
    """Validator for the whole schema, or for one definition so that an error names its real cause instead of a failed oneOf."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    if definition is not None:
        schema = {"$schema": schema["$schema"], "$ref": f"#/$defs/{definition}", "$defs": schema["$defs"]}
    return jsonschema.Draft202012Validator(schema)


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[object]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise PackageError(f"{path.name}:{number}: blank line")
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise PackageError(f"{path.name}:{number}: invalid JSON ({exc.msg})") from exc
    return records


def _anchors_of(obj: dict) -> list[dict]:
    if obj.get("schema") == "KCBookRelation/v1":
        return [item["anchor"] for item in obj.get("evidence", [])]
    if obj.get("schema") == "KCBookEdit/v1":
        return [obj["anchor"]]
    return list(obj.get("evidence", []))


def check_package(root: Path) -> list[str]:
    """Return every problem found; an empty list means the package passed all of this tool's checks (not KC2 admission)."""
    problems: list[str] = []
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"manifest.json: unreadable ({type(exc).__name__})"]
    problems += [f"manifest.json: {m}" for m in schema_errors(manifest)]
    if problems:
        return problems
    comps, rep = manifest["components"], manifest["representation"]

    files = {k: v for k, v in comps.items() if k in ("document_md", "readable_md", "edits", "objects", "relations", "quality")}
    for name, meta in files.items():
        path = root / meta["path"]
        if not path.is_file():
            problems.append(f"{name}: file {meta['path']} is missing")
        elif sha256_file(path) != meta["sha256"]:
            problems.append(f"{name}: sha256 of {meta['path']} differs from the manifest")
    for asset in comps.get("assets", []):
        if asset["state"] == "present":
            path = root / asset["path"]
            if not path.is_file() or sha256_file(path) != asset["sha256"]:
                problems.append(f"asset {asset['asset_id']}: missing or digest differs")
    if problems:
        return problems

    if "document_md" in comps and comps["document_md"]["input_sha256"] != rep["source_sha256"]:
        problems.append("document_md.input_sha256 must equal the source representation sha256")
    if "document_md" in comps and comps["document_md"]["path"] == comps["readable_md"]["path"]:
        problems.append("document_md and readable_md must be different files")

    rights = manifest["rights"]
    if rights["license_class"] != "author_open" and RESTRICTED_LAYERS & set(rights["publishable_layers"]):
        problems.append("a work that is not author_open may not publish document_md, readable_md or assets")

    objects = read_jsonl(root / comps["objects"]["path"])
    relations = read_jsonl(root / comps["relations"]["path"])
    edits = read_jsonl(root / comps["edits"]["path"])
    quality = json.loads((root / comps["quality"]["path"]).read_text(encoding="utf-8"))

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
        if record["schema"] == "KCBookObject/v1" and (record["work_id"], record["edition_id"]) != (manifest["work"]["work_id"], manifest["edition"]["edition_id"]):
            problems.append(f"object {record['object_id']}: work_id/edition_id differ from the manifest")
        for anchor in _anchors_of(record):
            if (anchor["representation_id"], anchor["source_sha256"]) != (rep["representation_id"], rep["source_sha256"]):
                problems.append(f"{record['schema']}: an evidence anchor names another representation or source hash")
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

    # Staleness: a stale edit invalidates every object that depends on it, and every relation that touches such an object.
    stale_edit_objs = {dep for e in edits if e["status"] == "stale" for dep in e["depends_on_objects"]}
    for obj in objects:
        if obj["object_id"] in stale_edit_objs and obj["status"] not in ("stale", "rejected"):
            problems.append(f"object {obj['object_id']}: depends on a stale edit but is {obj['status']}")
    stale_objs = {o["object_id"] for o in objects if o["status"] == "stale"} | stale_edit_objs
    for rel in relations:
        if (rel["from"] in stale_objs or rel["to"] in stale_objs) and rel["status"] not in ("stale", "rejected"):
            problems.append(f"relation {rel['relation_id']}: touches a stale object but is {rel['status']}")

    # Quality: counts agree with the files; extraction and semantic quality stay apart.
    sem = quality["semantics"]
    if (sem["objects_count"], sem["relations_count"]) != (len(objects), len(relations)):
        problems.append("quality.semantics counts differ from the object and relation files")
    if quality["package_id"] != manifest["package_id"]:
        problems.append("quality: package_id differs from the manifest")
    ext = quality["extraction"]
    if "units_expected" in ext and "units_seen" in ext and ext["status"] == "pass" and ext["units_seen"] != ext["units_expected"]:
        problems.append("quality.extraction: status pass with units_seen different from units_expected")
    if any(c["result"] == "fail" for c in ext["checks"]) and ext["status"] == "pass":
        problems.append("quality.extraction: status pass with a failed check")
    status = manifest["package_status"]
    if status == "knowledge_ready" and not (ext["status"] == "pass" and sem["status"] == "reviewed"):
        problems.append("package_status knowledge_ready requires extraction pass and semantics reviewed")
    if status == "structure_only" and sem["status"] != "not_built":
        problems.append("package_status structure_only requires semantics not_built")
    if status != "knowledge_ready" and sem["status"] == "reviewed" and ext["status"] == "pass":
        problems.append("extraction pass and semantics reviewed, but package_status does not say knowledge_ready")
    if sem["status"] in ("not_built", "not_measured") and objects:
        problems.append("semantics not_built/not_measured but the object file is not empty")
    return problems


def render_knowledge_markdown(manifest: dict, objects: list[dict], relations: list[dict]) -> str:
    """Deterministic Markdown rendering of the knowledge layer: the only form the candidate exporter can carry.

    Generated content is labelled in every block so no reader mistakes it for the author's statement.
    """
    lines = ["---", f"package_id: {manifest['package_id']}", f"work_id: {manifest['work']['work_id']}",
             f"edition_id: {manifest['edition']['edition_id']}", "kc2_admission: not_measured", "sources: none", "---", "",
             f"# Knowledge layer of {manifest['package_id']}", ""]
    def origin_label(origin: str) -> str:
        if origin == "author_statement":
            return "Author's statement (quoted or closely paraphrased)"
        if origin == "editor_correction":
            return "Editorial correction"
        return "GENERATED, not the author's statement (" + origin + ")"

    for obj in sorted(objects, key=lambda o: o["object_id"]):
        lines += [f"## {obj['object_id']}", "",
                  f"- Kind: {obj['object_kind']}; status: {obj['status']}",
                  f"- Origin: {origin_label(obj['origin'])}",
                  f"- Evidence anchors: {len(obj['evidence'])}", "", obj["text"], ""]
    for rel in sorted(relations, key=lambda r: r["relation_id"]):
        lines += [f"## {rel['relation_id']}", "",
                  f"- {rel['from']} **{rel['relation_type']}** {rel['to']}; status: {rel['status']}",
                  f"- Origin: {origin_label(rel['origin'])}", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


LAYER_FILE = {"document_md": "document_md", "readable_md": "readable_md"}


def candidate_projection(manifest: dict, knowledge_md: str | None) -> list[dict]:
    """Rows a publication step may propose for the candidate export. Only Markdown layers can be carried; an absent row means deny.

    The exporter (tools/export_corpus.py) still decides: it accepts only paths under papers/, spec/, articles/ or schemas/ that
    are in its explicit scope list, with a merged source commit and a reviewed publication decision. This function proposes; it
    does not widen that scope.
    """
    rights, rows = manifest["rights"], []
    for layer in rights["publishable_layers"]:
        if layer in LAYER_FILE:
            meta = manifest["components"].get(layer)
            if meta:
                rows.append({"layer": layer, "path_in_package": meta["path"], "sha256": meta["sha256"]})
        elif layer == "knowledge" and knowledge_md is not None:
            rows.append({"layer": layer, "path_in_package": "knowledge.md", "sha256": hashlib.sha256(knowledge_md.encode("utf-8")).hexdigest()})
    for row in rows:
        row.update(license_class=rights["license_class"], rights_holder=rights.get("holder", "unknown"), status="current",
                   kc2_admission="not_measured", package_id=manifest["package_id"])
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
    print("BOOK_PACKAGE_PASS (structure only; no extraction truth, no KC2 admission)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
