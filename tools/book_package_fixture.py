#!/usr/bin/env python3
"""Build the synthetic book package fixture and its negative variants (all text invented for this repository).

Run `python3 tools/book_package_fixture.py write` to regenerate schemas/fixtures/book-package/; the unit tests rebuild the
same bytes in memory and fail if the committed files drift. Nothing here is third-party text.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_book_package as cbp  # noqa: E402

FIXTURE_ROOT = cbp.REPO / "schemas" / "fixtures" / "book-package"
PKG = "synthetic-rle-primer"
REP, WORK, EDN = "rep.synthetic-rle-primer.md", "work.synthetic-rle-primer", "ed.synthetic-rle-primer.en"
SRC_BYTES = b"# Synthetic primer on run-length encoding\n\n## Definition\n\nRun-length encoding replaces a run of equal symbols by the symbol and the run length.\n\n## Limits\n\nThe method can enlarge data that has no runs.\n\n## Figure 1\n\n![Figure 1](assets/fig1.svg)\n"
SRC_SHA = hashlib.sha256(SRC_BYTES).hexdigest()
GEN = {"tool": "fixture-generator", "tool_version": "0.0.0", "run_id": "run.fixture.1", "input_sha256": SRC_SHA, "generated_at": "2026-11-04T00:00:00Z"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def anchor(section: str, block: str) -> dict:
    return {"kind": "section_block", "representation_id": REP, "source_sha256": SRC_SHA, "section_id": section, "block_id": block}


def facets(kind: str, position: str = "asserts") -> dict:
    unk = lambda: {"state": "unknown", "reason": "not annotated in this fixture"}  # noqa: E731
    return {"representation_modes": {"state": "known", "value": ["text"]}, "content_kinds": {"state": "known", "value": [kind]},
            "discourse_functions": unk(), "aboutness": {"state": "known", "value": ["run-length encoding"]},
            "source_position": {"state": "known", "value": position}, "semantic_operators": {"state": "not_applicable", "reason": "no operators in this statement"},
            "assessment_refs": {"state": "known", "value": ["review.fixture.semantic"]}, "governance_refs": {"state": "known", "value": []}}


def obj(oid: str, kind: str, text: str, origin: str, section: str, block: str, content_kind: str, **extra) -> dict:
    rec = {"schema": "KCBookObject/v2", "object_id": oid, "package_id": PKG, "work_id": WORK, "edition_id": EDN, "object_kind": kind, "text": text,
           "text_language": "en", "origin": origin, "presented_as_author": False, "evidence": [anchor(section, block)],
           "semantic_facets": facets(content_kind), "status": "reviewed", "kc2_admission": "not_measured"}
    if origin != "author_statement":
        rec["generation"] = copy.deepcopy(GEN)
    rec.update(extra)
    return rec


def build() -> dict[str, bytes]:
    """Return {relative path inside the package: bytes} for the valid package."""
    document = SRC_BYTES
    readable = SRC_BYTES.replace(b"Synthetic primer", b"Synthetic primer (readable edition)")
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10"/></svg>\n'
    objects = [
        obj("obj.rle.definition", "concept", "Run-length encoding replaces a run of equal symbols by the symbol and the run length.", "author_statement", "sec.definition", "blk.1", "definition"),
        obj("obj.rle.limit", "claim", "The method can enlarge data that has no runs.", "author_statement", "sec.limits", "blk.1", "constraint_norm",
            claim_class="general", qualifiers={"conditions": ["input without runs"]}),
        obj("obj.rle.meaning", "concept", "In plain words: store how many times a symbol repeats instead of repeating it.", "generated_meaning", "sec.definition", "blk.1", "explanatory_model"),
        obj("obj.fig1.description", "figure", "Black square of ten by ten units.", "generated_description", "sec.figure1", "blk.1", "state_description"),
    ]
    relations = [
        {"schema": "KCBookRelation/v2", "relation_id": "rel.def", "package_id": PKG, "relation_type": "defines", "from": "obj.rle.definition", "to": "obj.rle.meaning",
         "origin": "generated_meaning", "presented_as_author": False, "generation": copy.deepcopy(GEN), "evidence": [{"side": "both", "anchor": anchor("sec.definition", "blk.1")}],
         "status": "reviewed", "kc2_admission": "not_measured"},
        {"schema": "KCBookRelation/v2", "relation_id": "rel.limit", "package_id": PKG, "relation_type": "requires", "from": "obj.rle.limit", "to": "obj.rle.definition",
         "origin": "author_statement", "presented_as_author": True, "conditions": ["only when the input has long runs"],
         "evidence": [{"side": "from", "anchor": anchor("sec.limits", "blk.1")}, {"side": "to", "anchor": anchor("sec.definition", "blk.1")}], "status": "reviewed", "kc2_admission": "not_measured"},
    ]
    edits = [{"schema": "KCBookEdit/v2", "edit_id": "edit.1", "package_id": PKG, "target": "readable_md", "anchor": anchor("sec.title", "blk.1"),
              "original_text": "Synthetic primer", "replacement_text": "Synthetic primer (readable edition)", "basis": "other", "reason": "label the readable edition",
              "actor_type": "tool", "input_sha256": sha(document), "output_sha256": sha(readable), "reversible": True, "status": "accepted", "depends_on_objects": []}]
    jl = lambda rows: ("\n".join(json.dumps(r, sort_keys=True, separators=(",", ":")) for r in rows) + "\n").encode()  # noqa: E731
    quality = {"schema": "KCBookQuality/v2", "package_id": PKG,
               "extraction": {"status": "pass", "units_expected": 3, "units_seen": 3, "checks": [{"check_id": "chk.order", "result": "pass", "method": "section order compared with source headings"}],
                              "cer": {"metric_status": "not_measured", "value": None}},
               "semantics": {"status": "reviewed", "objects_count": len(objects), "relations_count": len(relations),
                             "review": {"review_id": "review.fixture.semantic", "reviewer_type": "blind_agent", "reviewer_id": "fixture.reviewer",
                                        "producer_id": "fixture.generator", "independence_basis": "synthetic identity separation for schema testing; no real review is asserted",
                                        "reviewed_at": "2026-11-04T00:00:00Z", "sample_size": 4, "result": "supported",
                                        "object_ids": [o["object_id"] for o in objects], "relation_ids": [r["relation_id"] for r in relations],
                                        "objects_sha256": sha(jl(objects)), "relations_sha256": sha(jl(relations)), "readable_sha256": sha(readable)}}, "kc2_admission": "not_measured"}
    files = {"document.md": document, "readable.md": readable, "assets/fig1.svg": svg, "edits.jsonl": jl(edits), "objects.jsonl": jl(objects),
             "relations.jsonl": jl(relations), "quality.json": json.dumps(quality, indent=1, sort_keys=True).encode() + b"\n"}
    manifest = {"schema": "KCBookPackageManifest/v2", "validation_profile": "book-package/2", "package_id": PKG, "release_id": "r1", "created_at": "2026-11-04T00:00:00Z",
                "work": {"work_id": WORK, "title": "Synthetic primer on run-length encoding"}, "edition": {"edition_id": EDN, "language": "en", "kind": "original"},
                "representation": {"representation_id": REP, "format": "md", "source_sha256": SRC_SHA, "size_bytes": len(SRC_BYTES), "integrity": "verified", "completeness": "full",
                                   "integrity_check": {"method": "synthetic source-byte digest comparison", "observer": "fixture.generator", "checked_at": "2026-11-04T00:00:00Z", "expected_sha256": SRC_SHA, "observed_sha256": SRC_SHA}},
                "related_works": [], "rights": {"license_class": "author_open", "holder": "Knowledge Contract Arcana contributors", "license": "CC-BY-4.0", "publishable_layers": ["document_md", "readable_md", "assets", "knowledge", "quality"]},
                "components": {"document_md": {"path": "document.md", "sha256": sha(document), "input_sha256": SRC_SHA, "tool": "fixture-generator", "tool_version": "0.0.0", "contains_generated_text": False},
                               "readable_md": {"path": "readable.md", "sha256": sha(readable), "contains_generated_text": False},
                               "assets": [{"asset_id": "asset.fig1", "kind": "image", "state": "present", "path": "assets/fig1.svg", "sha256": sha(svg)},
                                          {"asset_id": "asset.fig2", "kind": "image", "state": "missing_asset"}],
                               "edits": {"path": "edits.jsonl", "sha256": sha(files["edits.jsonl"]), "count": len(edits)},
                               "objects": {"path": "objects.jsonl", "sha256": sha(files["objects.jsonl"]), "count": len(objects)},
                               "relations": {"path": "relations.jsonl", "sha256": sha(files["relations.jsonl"]), "count": len(relations)},
                               "quality": {"path": "quality.json", "sha256": sha(files["quality.json"])}},
                "tooling": [{"tool": "fixture-generator", "tool_version": "0.0.0"}], "package_status": "knowledge_ready", "kc2_admission": "not_measured"}
    files["manifest.json"] = json.dumps(manifest, indent=1, sort_keys=True).encode() + b"\n"
    return files


def anchor_examples() -> dict[str, dict]:
    """One valid object per anchor kind; each is a whole object record so it validates on its own."""
    base = obj("obj.anchor", "concept", "Anchor kind example.", "generated_meaning", "s", "b", "definition")
    common = {"representation_id": REP, "source_sha256": SRC_SHA}
    kinds = {
        "page_bbox": {"kind": "page_bbox", "page": 3, "bbox": [10, 20, 200, 80], "bbox_origin": "top_left", "bbox_unit": "pt", **common},
        "spine_offset": {"kind": "spine_offset", "spine_item": "text/ch01.xhtml", "element_path": "/html/body/p[2]", "start": 0, "end": 42, **common},
        "section_block": anchor("sec.a", "blk.1"),
        "sheet_range": {"kind": "sheet_range", "sheet": "Results", "range": "B2:D9", "layer": "cached_value", **common},
        "json_pointer": {"kind": "json_pointer", "pointer": "/primaryContentSections/0/content/1", **common},
        "slide_block": {"kind": "slide_block", "slide": 4, "block_id": "blk.title", **common},
    }
    out = {}
    for name, a in kinds.items():
        rec = copy.deepcopy(base)
        rec["object_id"] = f"obj.anchor.{name}".replace("_", "-")
        rec["evidence"] = [a]
        out[name] = rec
    return out


PD_EVIDENCE = {
    "basis": "Synthetic determination for schema testing: invented work, invented digitiser; no real rights are asserted.",
    "own_layers_license": "CC-BY-4.0", "jurisdictions": ["worldwide"], "worldwide_reason": "the synthetic work is stated to be out of term in every jurisdiction, for testing only",
    "evidence_urls": ["https://example.org/synthetic-primer/rights"], "determined_at": "2026-11-05T00:00:00Z", "determined_by": "fixture.determiner",
    "work": {"status": "term_expired", "basis": "the synthetic author is stated to have died more than seventy years ago"},
    "digital_copy": {"status": "open", "terms": "CC0-1.0", "basis": "the synthetic digitiser's page states CC0 1.0"}}
PD_DAMAGE = {"status": "declared", "places": 2, "declarations": [
    {"code": "FILED_DEFECT", "count": 1, "items": [{"page_id": "p0002", "what": "D-synthetic-0001", "quote": "a filed ligature defect"}]},
    {"code": "KNOWN_TEXT_DAMAGE", "count": 1, "items": [{"page_id": "p0003", "block_id": "b0001", "what": "unreadable word"}]}]}


def build_public_domain() -> dict[str, bytes]:
    """The valid package re-cast as a public-domain work with declared damage: rights class public_domain with its evidence, the layers
    Arcanada writes under an author licence, a damage declaration (so the status cannot be knowledge_ready)."""
    files = build()
    quality = json.loads(files["quality.json"])
    quality["damage"] = copy.deepcopy(PD_DAMAGE)
    files["quality.json"] = json.dumps(quality, indent=1, sort_keys=True).encode() + b"\n"
    manifest = json.loads(files["manifest.json"])
    manifest["rights"] = {"license_class": "public_domain", "holder": "Knowledge Contract Arcana contributors",
                          "publishable_layers": ["document_md", "readable_md", "knowledge", "quality"], "public_domain": copy.deepcopy(PD_EVIDENCE)}
    manifest["components"]["quality"]["sha256"] = sha(files["quality.json"])
    manifest["package_status"] = "partial_pilot"
    files["manifest.json"] = json.dumps(manifest, indent=1, sort_keys=True).encode() + b"\n"
    return files


def _del(path):
    def run(r):
        node = r
        for key in path[:-1]:
            node = node[key]
        del node[path[-1]]
    return run


def _set(path, value):
    def run(r):
        node = r
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
    return run


def _first_evidence(r):
    return r["evidence"][0]


# name -> (record kind to mutate, mutation). Each must make the schema reject the record.
RECORD_MUTATIONS: dict[str, tuple[str, object]] = {
    "manifest_restricted_open_license": ("manifest", lambda r: r["rights"].update(license_class="third_party_restricted", publishable_layers=[])),
    "manifest_unknown_open_license": ("manifest", lambda r: r["rights"].update(license_class="unknown", publishable_layers=[])),
    "manifest_restricted_knowledge_layer": ("manifest", lambda r: r.__setitem__("rights", {"license_class": "third_party_restricted", "publishable_layers": ["knowledge"]})),
    "manifest_integrity_without_observer": ("manifest", _del(["representation", "integrity_check", "observer"])),
    "manifest_missing_profile": ("manifest", _del(["validation_profile"])),
    "manifest_legacy_profile": ("manifest", _set(["schema"], "KCBookPackageManifest/v1")),
    "manifest_package_id_colon": ("manifest", _set(["package_id"], "pkg:one")),
    "edit_unsupported_asset_text": ("edit", _set(["target"], "asset_text")),
    "quality_review_without_scope": ("quality", _del(["semantics", "review", "object_ids"])),
    "quality_review_without_binding": ("quality", _del(["semantics", "review", "objects_sha256"])),
    "quality_na_without_basis": ("quality", _set(["extraction", "checks"], [{"check_id": "check.na", "result": "not_applicable", "method": "omitted basis"}])),
    "object_generated_without_generation": ("object_gen", _del(["generation"])),
    "object_generated_presented_as_author": ("object_gen", _set(["presented_as_author"], True)),
    "object_author_with_generation": ("object_author", lambda r: r.__setitem__("generation", copy.deepcopy(GEN))),
    "object_no_evidence": ("object_author", _set(["evidence"], [])),
    "object_anchor_wrong_hash": ("object_author", lambda r: r["evidence"][0].__setitem__("source_sha256", "xyz")),
    "object_anchor_unknown_kind": ("object_author", lambda r: r["evidence"][0].__setitem__("kind", "line_number")),
    "object_anchor_page_zero": ("object_page", lambda r: r["evidence"][0].__setitem__("page", 0)),
    "object_anchor_bbox_three_numbers": ("object_page", lambda r: r["evidence"][0].__setitem__("bbox", [1, 2, 3])),
    "object_anchor_pointer_without_slash": ("object_pointer", lambda r: r["evidence"][0].__setitem__("pointer", "primaryContentSections/0")),
    "object_anchor_bad_sheet_range": ("object_sheet", lambda r: r["evidence"][0].__setitem__("range", "2B:9D")),
    "object_missing_facet": ("object_author", lambda r: r["semantic_facets"].pop("governance_refs")),
    "object_unknown_without_reason": ("object_author", lambda r: r["semantic_facets"]["discourse_functions"].pop("reason")),
    "object_known_with_empty_kinds": ("object_author", lambda r: r["semantic_facets"].__setitem__("content_kinds", {"state": "known", "value": []})),
    "object_unknown_content_kind": ("object_author", lambda r: r["semantic_facets"].__setitem__("content_kinds", {"state": "known", "value": ["vibes"]})),
    "object_admitted_by_itself": ("object_author", _set(["kc2_admission"], "admitted")),
    "object_benchmark_without_context": ("object_author", lambda r: r.__setitem__("claim_class", "benchmark")),
    "object_extra_field": ("object_author", _set(["confidence"], 0.99)),
    "object_empty_text": ("object_author", _set(["text"], "")),
    "relation_unknown_type": ("relation_gen", _set(["relation_type"], "is_like")),
    "relation_no_evidence": ("relation_gen", _set(["evidence"], [])),
    "relation_generated_without_generation": ("relation_gen", _del(["generation"])),
    "relation_contradicts_one_sided": ("relation_contra", lambda r: r.__setitem__("evidence", r["evidence"][:1])),
    "edit_irreversible": ("edit", _set(["reversible"], False)),
    "edit_without_reason": ("edit", _set(["reason"], "")),
    "edit_blank_reason": ("edit", _set(["reason"], "     ")),
    "edit_unknown_basis": ("edit", _set(["basis"], "felt like it")),
    "quality_overall_score": ("quality", _set(["overall_score"], 0.97)),
    "quality_cer_null_but_measured": ("quality", _set(["extraction", "cer"], {"metric_status": "measured", "value": None})),
    "quality_cer_zero_without_reference": ("quality", _set(["extraction", "cer"], {"metric_status": "measured", "value": 0})),
    "quality_not_built_with_objects": ("quality", lambda r: r["semantics"].update(status="not_built", objects_count=3)),
    "quality_reviewed_without_review": ("quality", lambda r: r["semantics"].pop("review")),
    "manifest_document_md_marks_generated_text": ("manifest", _set(["components", "document_md", "contains_generated_text"], True)),
    "manifest_bibliography_only_with_document": ("manifest", _set(["representation", "completeness"], "bibliography_only")),
    "manifest_mismatch_but_ready": ("manifest", _set(["representation", "integrity"], "mismatch")),
    "manifest_ready_but_partial": ("manifest", _set(["representation", "completeness"], "partial")),
    "manifest_missing_asset_with_path": ("manifest", lambda r: r["components"]["assets"][1].update(path="assets/fig2.png")),
    "manifest_path_traversal": ("manifest", _set(["components", "readable_md", "path"], "../readable.md")),
    "manifest_absolute_path": ("manifest", _set(["components", "objects", "path"], "/etc/objects.jsonl")),
    "manifest_admitted_by_itself": ("manifest", _set(["kc2_admission"], "admitted")),
    "manifest_non_https_locator": ("manifest", _set(["representation", "locator"], "file:///book.pdf")),
    "manifest_public_domain_without_evidence": ("manifest_pd", _del(["rights", "public_domain"])),
    "manifest_public_domain_work_not_expired": ("manifest_pd", _set(["rights", "public_domain", "work", "status"], "in_copyright")),
    "manifest_public_domain_digital_copy_restricted": ("manifest_pd", _set(["rights", "public_domain", "digital_copy", "status"], "restricted")),
    "manifest_public_domain_without_digital_copy_fact": ("manifest_pd", _del(["rights", "public_domain", "digital_copy"])),
    "manifest_public_domain_without_work_fact": ("manifest_pd", _del(["rights", "public_domain", "work"])),
    "manifest_public_domain_no_evidence_url": ("manifest_pd", _set(["rights", "public_domain", "evidence_urls"], [])),
    "manifest_public_domain_plain_http_evidence": ("manifest_pd", _set(["rights", "public_domain", "evidence_urls"], ["http://example.org/rights"])),
    "manifest_public_domain_worldwide_without_reason": ("manifest_pd", _del(["rights", "public_domain", "worldwide_reason"])),
    "manifest_public_domain_unknown_terms": ("manifest_pd", _set(["rights", "public_domain", "digital_copy", "terms"], "all rights reserved")),
    "manifest_author_open_with_public_domain_block": ("manifest", lambda r: r["rights"].__setitem__("public_domain", copy.deepcopy(PD_EVIDENCE))),
    "manifest_restricted_with_public_domain_block": ("manifest", lambda r: r.__setitem__("rights", {"license_class": "third_party_restricted", "publishable_layers": [],
                                                                                                      "public_domain": copy.deepcopy(PD_EVIDENCE)})),
    "manifest_public_domain_with_top_level_license": ("manifest_pd", _set(["rights", "license"], "CC-BY-4.0")),
    "quality_damage_declared_without_declarations": ("quality_pd", _set(["damage", "declarations"], [])),
    "quality_damage_none_with_places": ("quality_pd", _set(["damage", "status"], "none")),
    "quality_damage_declared_zero_places": ("quality_pd", _set(["damage", "places"], 0)),
    "quality_damage_lowercase_code": ("quality_pd", _set(["damage", "declarations", 0, "code"], "filed_defect")),
    "quality_damage_item_without_what": ("quality_pd", _del(["damage", "declarations", 0, "items", 0, "what"])),
}


def record_bases(files: dict[str, bytes]) -> dict[str, dict]:
    objects = [json.loads(line) for line in files["objects.jsonl"].decode().split("\n")[:-1]]
    relations = [json.loads(line) for line in files["relations.jsonl"].decode().split("\n")[:-1]]
    anchors = anchor_examples()
    contra = copy.deepcopy(relations[1])
    contra["relation_type"] = "contradicts"
    contra["origin"] = "author_statement"
    contra["presented_as_author"] = True
    return {"object_author": objects[0], "object_gen": objects[2], "object_page": anchors["page_bbox"], "object_pointer": anchors["json_pointer"],
            "object_sheet": anchors["sheet_range"], "relation_gen": relations[0], "relation_contra": contra,
            "edit": json.loads(files["edits.jsonl"].decode().split("\n")[:-1][0]), "quality": json.loads(files["quality.json"]),
            "manifest": json.loads(files["manifest.json"]),
            "manifest_pd": json.loads(build_public_domain()["manifest.json"]), "quality_pd": json.loads(build_public_domain()["quality.json"])}


def write() -> None:
    files = build()
    pkg = FIXTURE_ROOT / "valid" / "synthetic-rle-primer"
    pkg.mkdir(parents=True, exist_ok=True)
    for rel, data in files.items():
        target = pkg / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    pd = FIXTURE_ROOT / "valid" / "synthetic-public-domain-primer"
    pd.mkdir(parents=True, exist_ok=True)
    for rel, data in build_public_domain().items():
        target = pd / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    anchors_dir = FIXTURE_ROOT / "valid" / "anchors"
    anchors_dir.mkdir(parents=True, exist_ok=True)
    for name, rec in anchor_examples().items():
        (anchors_dir / f"{name}.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    bad_dir = FIXTURE_ROOT / "invalid"
    bad_dir.mkdir(parents=True, exist_ok=True)
    bases = record_bases(files)
    for name, (base, mutate) in RECORD_MUTATIONS.items():
        rec = copy.deepcopy(bases[base])
        mutate(rec)
        (bad_dir / f"{name}.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
        print("fixtures written")
    else:
        print("usage: book_package_fixture.py write", file=sys.stderr)
        raise SystemExit(2)
