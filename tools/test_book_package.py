import copy
import json
import tempfile
import unittest
from pathlib import Path

import book_package_fixture as fx
import check_book_package as cbp

VALID = fx.FIXTURE_ROOT / "valid" / "synthetic-rle-primer"


def load_parts(files: dict[str, bytes]) -> dict:
    jl = lambda name: [json.loads(x) for x in files[name].decode().splitlines()]  # noqa: E731
    return {"manifest": json.loads(files["manifest.json"]), "objects": jl("objects.jsonl"), "relations": jl("relations.jsonl"),
            "edits": jl("edits.jsonl"), "quality": json.loads(files["quality.json"]), "files": dict(files)}


def materialise(parts: dict, rehash: bool = True) -> dict[str, bytes]:
    """Re-serialise parsed parts; with rehash the manifest digests and counts follow, so only the intended rule can fail."""
    jl = lambda rows: ("\n".join(json.dumps(r, sort_keys=True, separators=(",", ":")) for r in rows) + "\n").encode()  # noqa: E731
    files = dict(parts["files"])
    files["objects.jsonl"], files["relations.jsonl"], files["edits.jsonl"] = jl(parts["objects"]), jl(parts["relations"]), jl(parts["edits"])
    files["quality.json"] = json.dumps(parts["quality"], indent=1, sort_keys=True).encode() + b"\n"
    m = parts["manifest"]
    if rehash:
        c = m["components"]
        for key, name, rows in (("objects", "objects.jsonl", parts["objects"]), ("relations", "relations.jsonl", parts["relations"]), ("edits", "edits.jsonl", parts["edits"])):
            c[key]["sha256"], c[key]["count"] = fx.sha(files[name]), len(rows)
        c["quality"]["sha256"] = fx.sha(files["quality.json"])
        if "document_md" in c:
            c["document_md"]["sha256"] = fx.sha(files[c["document_md"]["path"]])
        c["readable_md"]["sha256"] = fx.sha(files[c["readable_md"]["path"]])
    files["manifest.json"] = json.dumps(m, indent=1, sort_keys=True).encode() + b"\n"
    return files


def check_files(files: dict[str, bytes]) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel, data in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(data)
        try:
            return cbp.check_package(root)
        except cbp.PackageError as exc:
            return [str(exc)]


def stale_edit(p):
    p["edits"][0]["status"] = "stale"
    p["edits"][0]["depends_on_objects"] = ["obj.rle.meaning"]


def anchor_other_source(p):
    p["objects"][0]["evidence"][0]["source_sha256"] = "0" * 64


def page_anchor(bad_bbox):
    def run(p):
        p["objects"][0]["evidence"][0] = {"kind": "page_bbox", "page": 1, "bbox": [5, 5, 4, 9] if bad_bbox else [5, 5, 40, 9], "bbox_origin": "top_left", "bbox_unit": "pt",
                                          "representation_id": fx.REP, "source_sha256": fx.SRC_SHA}
    return run


def spine_anchor(p):
    p["objects"][0]["evidence"][0] = {"kind": "spine_offset", "spine_item": "a.xhtml", "start": 9, "end": 3, "representation_id": fx.REP, "source_sha256": fx.SRC_SHA}


# name -> (mutation on parsed parts, expected fragment of a reported problem)
def edit_field(name, value):
    return lambda p: p["edits"][0].__setitem__(name, value)


def unrelated_readable(p):
    p["files"]["readable.md"] = b"# Unrelated text\n"


PACKAGE_MUTATIONS = {
    "duplicate_edit_id": (lambda p: p["edits"].append(copy.deepcopy(p["edits"][0])), "duplicate edit_id"),
    "duplicate_asset_id": (lambda p: p["manifest"]["components"]["assets"].append(copy.deepcopy(p["manifest"]["components"]["assets"][0])), "duplicate asset_id"),
    "edit_input_digest_wrong": (edit_field("input_sha256", "0" * 64), "input_sha256 is not the digest"),
    "edit_output_digest_wrong": (edit_field("output_sha256", "0" * 64), "output_sha256 is not the digest"),
    "edit_original_not_in_text": (edit_field("original_text", "text that is not there"), "does not occur"),
    "readable_is_not_the_replay": (unrelated_readable, "not the replay"),
    "anchor_kind_does_not_fit_format": (lambda p: p["objects"][0].__setitem__("evidence", [{"kind": "page_bbox", "page": 1, "bbox": [1, 1, 5, 5], "bbox_origin": "top_left", "bbox_unit": "pt", "representation_id": fx.REP, "source_sha256": fx.SRC_SHA}]), "does not fit source format"),
    "relation_endpoint_unknown": (lambda p: p["relations"][0].__setitem__("to", "obj.nowhere"), "is not an object of this package"),
    "relation_self_loop": (lambda p: p["relations"][0].__setitem__("to", p["relations"][0]["from"]), "to itself"),
    "duplicate_object_id": (lambda p: p["objects"].append(copy.deepcopy(p["objects"][0])), "duplicate object_id"),
    "duplicate_relation_id": (lambda p: p["relations"].append(copy.deepcopy(p["relations"][0])), "duplicate relation_id"),
    "anchor_other_source_hash": (anchor_other_source, "another representation or source hash"),
    "anchor_bbox_without_area": (page_anchor(True), "bbox has no area"),
    "anchor_spine_end_before_start": (spine_anchor, "end precedes start"),
    "stale_edit_leaves_object_reviewed": (stale_edit, "depends on a stale edit"),
    "object_other_package": (lambda p: p["objects"][0].__setitem__("package_id", "other.r1"), "package_id differs"),
    "object_other_edition": (lambda p: p["objects"][0].__setitem__("edition_id", "ed.other"), "differ from the manifest"),
    "edit_depends_on_unknown_object": (lambda p: p["edits"][0].__setitem__("depends_on_objects", ["obj.ghost"]), "unknown object"),
    "edit_changes_nothing": (lambda p: p["edits"][0].__setitem__("replacement_text", p["edits"][0]["original_text"]), "changes nothing"),
    "quality_counts_differ": (lambda p: p["quality"]["semantics"].__setitem__("objects_count", 99), "counts differ"),
    "quality_pass_with_failed_check": (lambda p: p["quality"]["extraction"]["checks"][0].__setitem__("result", "fail"), "failed check"),
    "quality_pass_units_differ": (lambda p: p["quality"]["extraction"].__setitem__("units_seen", 2), "units_seen"),
    "ready_but_semantics_unreviewed": (lambda p: (p["quality"]["semantics"].__setitem__("status", "built_unreviewed"), p["quality"]["semantics"].pop("review")), "knowledge_ready requires"),
    "structure_only_with_built_semantics": (lambda p: p["manifest"].__setitem__("package_status", "structure_only"), "structure_only requires"),
    "restricted_work_publishes_text": (lambda p: p["manifest"]["rights"].__setitem__("license_class", "third_party_restricted"), "may not publish"),
    "document_input_hash_differs": (lambda p: p["manifest"]["components"]["document_md"].__setitem__("input_sha256", "1" * 64), "input_sha256"),
    "document_and_readable_same_file": (lambda p: p["manifest"]["components"]["readable_md"].update(path="document.md", sha256=fx.sha(p["files"]["document.md"])), "different files"),
}


# name -> fragment that the first schema error must contain (the reason the fixture is rejected, not merely that it is)
EXPECTED_REASON = {
    "edit_irreversible": "reversible: True was expected", "edit_blank_reason": "reason:", "edit_unknown_basis": "basis: 'felt like it' is not one of", "edit_without_reason": "reason: '' is too short",
    "manifest_absolute_path": "components/objects/path", "manifest_admitted_by_itself": "kc2_admission: 'not_measured' was expected",
    "manifest_bibliography_only_with_document": "components:", "manifest_document_md_marks_generated_text": "contains_generated_text: False was expected",
    "manifest_mismatch_but_ready": "package_status: 'blocked_integrity' was expected", "manifest_missing_asset_with_path": "components/assets/1",
    "manifest_non_https_locator": "representation/locator", "manifest_path_traversal": "components/readable_md/path",
    "manifest_ready_but_partial": "representation/completeness: 'full' was expected", "object_admitted_by_itself": "kc2_admission: 'not_measured' was expected",
    "object_author_with_generation": "should not be valid under", "object_benchmark_without_context": "'benchmark_context' is a required property",
    "object_empty_text": "text: '' should be non-empty", "object_extra_field": "'confidence' was unexpected",
    "object_generated_presented_as_author": "presented_as_author: False was expected", "object_generated_without_generation": "'generation' is a required property",
    "object_known_with_empty_kinds": "semantic_facets/content_kinds", "object_missing_facet": "'governance_refs' is a required property",
    "object_no_evidence": "evidence: [] should be non-empty", "object_unknown_content_kind": "semantic_facets/content_kinds",
    "object_unknown_without_reason": "semantic_facets/discourse_functions", "quality_cer_null_but_measured": "extraction/cer",
    "quality_cer_zero_without_reference": "extraction/cer", "quality_not_built_with_objects": "semantics:", "quality_overall_score": "'overall_score' was unexpected",
    "quality_reviewed_without_review": "'review' is a required property", "relation_contradicts_one_sided": "evidence:",
    "relation_generated_without_generation": "'generation' is a required property", "relation_no_evidence": "evidence: [] should be non-empty",
    "relation_unknown_type": "relation_type: 'is_like' is not one of",
}
# anchor fixtures: the field of the anchor that must be the cause, checked against the branch of the anchor's own kind
ANCHOR_CAUSE = {"object_anchor_bad_sheet_range": "range", "object_anchor_bbox_three_numbers": "bbox", "object_anchor_page_zero": "page",
                "object_anchor_pointer_without_slash": "pointer", "object_anchor_wrong_hash": "source_sha256", "object_anchor_unknown_kind": "kind"}


def anchor_branch_errors(anchor: dict) -> list[str]:
    schema = json.loads(cbp.SCHEMA_PATH.read_text())
    branches = schema["$defs"]["Anchor"]["oneOf"]
    chosen = [b for b in branches if b["properties"]["kind"]["const"] == anchor.get("kind")]
    if not chosen:
        return ["kind"]
    import jsonschema
    validator = jsonschema.Draft202012Validator({"$schema": schema["$schema"], **chosen[0], "$defs": schema["$defs"]})
    return ["/".join(str(x) for x in e.absolute_path) for e in validator.iter_errors(anchor)]


class FixtureTests(unittest.TestCase):
    def test_valid_package_passes(self):
        self.assertEqual(cbp.check_package(VALID), [])

    def test_committed_fixtures_equal_regenerated_bytes(self):
        for rel, data in fx.build().items():
            self.assertEqual((VALID / rel).read_bytes(), data, rel)
        for name, rec in fx.anchor_examples().items():
            text = json.dumps(rec, indent=1, sort_keys=True) + "\n"
            self.assertEqual((fx.FIXTURE_ROOT / "valid" / "anchors" / f"{name}.json").read_text(), text, name)

    def test_every_anchor_kind_has_a_valid_example(self):
        kinds = {json.loads(p.read_text())["evidence"][0]["kind"] for p in (fx.FIXTURE_ROOT / "valid" / "anchors").glob("*.json")}
        self.assertEqual(kinds, {"page_bbox", "spine_offset", "section_block", "sheet_range", "json_pointer", "slide_block"})
        for path in (fx.FIXTURE_ROOT / "valid" / "anchors").glob("*.json"):
            self.assertEqual(cbp.schema_errors(json.loads(path.read_text())), [], path.name)

    def test_invalid_fixture_set_equals_mutation_registry(self):
        on_disk = {p.stem for p in (fx.FIXTURE_ROOT / "invalid").glob("*.json")}
        self.assertEqual(on_disk, set(fx.RECORD_MUTATIONS))

    def test_every_negative_fixture_is_rejected_and_matches_regenerated_bytes(self):
        bases = fx.record_bases(fx.build())
        for name, (base, mutate) in fx.RECORD_MUTATIONS.items():
            path = fx.FIXTURE_ROOT / "invalid" / f"{name}.json"
            rec = json.loads(path.read_text())
            self.assertTrue(cbp.schema_errors(rec), f"{name} was accepted")
            fresh = copy.deepcopy(bases[base])
            mutate(fresh)
            self.assertEqual(rec, fresh, f"{name} drifted from the generator")

    def test_every_negative_fixture_is_rejected_for_its_own_reason(self):
        self.assertEqual(set(EXPECTED_REASON) | set(ANCHOR_CAUSE), set(fx.RECORD_MUTATIONS))
        for name, fragment in EXPECTED_REASON.items():
            rec = json.loads((fx.FIXTURE_ROOT / "invalid" / f"{name}.json").read_text())
            self.assertIn(fragment, cbp.schema_errors(rec)[0], name)
        for name, field in ANCHOR_CAUSE.items():
            rec = json.loads((fx.FIXTURE_ROOT / "invalid" / f"{name}.json").read_text())
            self.assertIn(field, anchor_branch_errors(rec["evidence"][0]), name)

    def test_each_mutation_is_a_single_change_that_the_unmutated_base_survives(self):
        for name, base in fx.record_bases(fx.build()).items():
            if name == "relation_contra":
                continue
            self.assertEqual(cbp.schema_errors(base), [], f"base {name} is not valid on its own")

    def test_contradicts_with_both_sides_is_accepted(self):
        base = fx.record_bases(fx.build())["relation_contra"]
        self.assertEqual(cbp.schema_errors(base), [])


class PackageMutationTests(unittest.TestCase):
    def test_every_cross_file_mutation_is_reported_with_the_expected_message(self):
        for name, (mutate, fragment) in PACKAGE_MUTATIONS.items():
            parts = load_parts(fx.build())
            mutate(parts)
            problems = check_files(materialise(parts))
            self.assertTrue(any(fragment in p for p in problems), f"{name}: {fragment!r} not in {problems}")

    def test_byte_flip_in_a_component_breaks_its_digest(self):
        for rel in ("document.md", "readable.md", "assets/fig1.svg", "objects.jsonl", "relations.jsonl", "edits.jsonl", "quality.json"):
            files = fx.build()
            files[rel] = files[rel] + b" "
            self.assertTrue(any("differs" in p or "missing" in p for p in check_files(files)), rel)

    def test_missing_component_is_reported(self):
        for rel in ("document.md", "objects.jsonl", "assets/fig1.svg"):
            files = fx.build()
            del files[rel]
            self.assertTrue(check_files(files), rel)

    def test_blank_line_in_jsonl_is_refused(self):
        files = materialise(load_parts(fx.build()))
        files["objects.jsonl"] += b"\n"
        manifest = json.loads(files["manifest.json"])
        manifest["components"]["objects"]["sha256"] = fx.sha(files["objects.jsonl"])
        files["manifest.json"] = json.dumps(manifest, indent=1, sort_keys=True).encode() + b"\n"
        self.assertTrue(any("blank line" in p for p in check_files(files)))

    def test_manifest_count_mismatch_is_reported(self):
        parts = load_parts(fx.build())
        parts["manifest"]["components"]["objects"]["count"] = 9
        files = materialise(parts, rehash=False)
        self.assertTrue(any("manifest count" in p for p in check_files(files)))

    def test_mutation_registries_are_not_empty(self):
        self.assertGreaterEqual(len(PACKAGE_MUTATIONS), 18)
        self.assertGreaterEqual(len(fx.RECORD_MUTATIONS), 35)


def ledger_package(document: str, readable: str, edits: list[tuple[str, str]]) -> dict[str, bytes]:
    """The valid fixture with document.md replaced and an accepted-edit ledger built over it, digests chained and rehashed."""
    parts = load_parts(fx.build())
    base = parts["edits"][0]
    parts["files"]["document.md"] = document.encode()
    parts["files"]["readable.md"] = readable.encode()
    rows, current = [], document
    for number, (before, after) in enumerate(edits, 1):
        text_before = current
        current = current.replace(before, after, 1) if before else after + current
        rows.append({**base, "edit_id": f"edit.{number}", "original_text": before, "replacement_text": after,
                     "input_sha256": fx.sha(text_before.encode()), "output_sha256": fx.sha(current.encode())})
    parts["edits"] = rows
    parts["manifest"]["components"]["document_md"]["input_sha256"] = parts["manifest"]["representation"]["source_sha256"]
    return materialise(parts)


class LedgerReversibilityTests(unittest.TestCase):
    def test_unique_edit_replays_forward_and_backward(self):
        files = ledger_package("alpha beta gamma\n", "alpha BETA gamma\n", [("beta", "BETA")])
        self.assertEqual(check_files(files), [])

    def test_edit_of_a_second_occurrence_is_refused(self):
        problems = check_files(ledger_package("beta beta\n", "beta BETA\n", [("beta", "BETA")]))
        self.assertTrue(any("occurs 2 times" in p for p in problems), problems)

    def test_empty_original_text_is_refused(self):
        problems = check_files(ledger_package("alpha\n", "xalpha\n", [("", "x")]))
        self.assertTrue(any("must not be empty" in p for p in problems), problems)

    def test_empty_replacement_is_refused(self):
        problems = check_files(ledger_package("alpha beta\n", "alpha \n", [("beta", "")]))
        self.assertTrue(any("must not be empty" in p for p in problems), problems)

    def test_replacement_that_duplicates_existing_text_is_refused(self):
        problems = check_files(ledger_package("alpha beta\n", "alpha alpha\n", [("beta", "alpha")]))
        self.assertTrue(any("cannot be reversed" in p for p in problems), problems)

    def test_overlapping_edit_chain_is_refused(self):
        problems = check_files(ledger_package("abcd\n", "xd\n", [("abc", "xyz"), ("yz", "")]))
        self.assertTrue(problems)


def without_edits(document: str, readable: str) -> dict[str, bytes]:
    """The valid fixture with the given document and readable texts and an empty ledger (zero bytes, count 0)."""
    files = ledger_package(document, readable, [])
    manifest = json.loads(files["manifest.json"])
    files["edits.jsonl"] = b""
    manifest["components"]["edits"].update({"sha256": fx.sha(b""), "count": 0})
    files["manifest.json"] = json.dumps(manifest, indent=1, sort_keys=True).encode() + b"\n"
    return files


class NewlineAndOverlapTests(unittest.TestCase):
    def test_crlf_document_with_lf_readable_is_refused(self):
        # zero edits: readable.md must be byte-equal to document.md, not equal after newline translation
        files = without_edits("line one\r\nline two\r\n", "line one\nline two\n")
        self.assertTrue(any("not the replay" in p for p in check_files(files)), check_files(files))
        self.assertEqual(check_files(without_edits("line one\r\nline two\r\n", "line one\r\nline two\r\n")), [])

    def test_lone_cr_is_not_a_newline_for_comparison(self):
        files = without_edits("a\rb\n", "a\nb\n")
        self.assertTrue(any("not the replay" in p for p in check_files(files)))

    def test_crlf_document_with_honest_edit_passes_with_byte_digests(self):
        files = ledger_package("line one\r\nline two\r\n", "line one\r\nline 2\r\n", [("two", "2")])
        self.assertEqual(check_files(files), [])

    def test_original_text_containing_crlf_can_be_edited(self):
        files = ledger_package("a\r\nb\r\nc\n", "a\r\nB\nc\n", [("b\r\n", "B\n")])
        self.assertEqual(check_files(files), [])

    def test_overlapping_original_occurrences_count_as_repeats(self):
        problems = check_files(ledger_package("xaaay\n", "xBy\n", [("aa", "B")]))
        self.assertTrue(any("overlapping counted" in p and "2 times" in p for p in problems), problems)

    def test_overlapping_replacement_occurrences_count_as_repeats(self):
        problems = check_files(ledger_package("xaBy\n", "xaaay\n", [("B", "aa")]))
        self.assertTrue(any("cannot be reversed" in p for p in problems), problems)

    def test_count_overlapping(self):
        self.assertEqual((cbp.count_overlapping("xaaay", "aa"), cbp.count_overlapping("abc", "d"), cbp.count_overlapping("aaa", "aaa")), (2, 0, 1))


class FileHandlingTests(unittest.TestCase):
    def write(self, root: Path, files: dict[str, bytes]) -> None:
        for rel, data in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(data)

    def test_symlinked_component_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, outside = Path(tmp) / "pkg", Path(tmp) / "outside.md"
            files = fx.build()
            self.write(root, files)
            outside.write_bytes(files["document.md"])  # same bytes and digest, but outside the package
            (root / "document.md").unlink()
            (root / "document.md").symlink_to(outside)
            self.assertTrue(any("symlink" in p for p in cbp.check_package(root)))

    def test_symlinked_manifest_and_directory_component_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "pkg"
            files = fx.build()
            self.write(root, files)
            (root / "manifest.json").rename(Path(tmp) / "m.json")
            (root / "manifest.json").symlink_to(Path(tmp) / "m.json")
            self.assertTrue(any("manifest.json" in p and "symlink" in p for p in cbp.check_package(root)))

    def test_non_utf8_files_fail_cleanly_with_the_file_name(self):
        for rel in ("document.md", "objects.jsonl", "quality.json", "readable.md", "manifest.json"):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "pkg"
                files = fx.build()
                files[rel] = b"\xff\xfe\xfa" + files[rel]
                if rel != "manifest.json":  # keep the digest right so the decode error is what is reached
                    manifest = json.loads(files["manifest.json"])
                    for comp in manifest["components"].values():
                        if isinstance(comp, dict) and comp.get("path") == rel:
                            comp["sha256"] = fx.sha(files[rel])
                    files["manifest.json"] = json.dumps(manifest, indent=1, sort_keys=True).encode() + b"\n"
                self.write(root, files)
                try:
                    problems = cbp.check_package(root)
                except cbp.PackageError as exc:
                    problems = [str(exc)]
                self.assertTrue(problems and any(rel in p or "UTF-8" in p or "unreadable" in p for p in problems), (rel, problems))
                self.assertEqual(cbp.main(["x", str(root)]), 1)


class MappingTests(unittest.TestCase):
    def test_knowledge_rendering_labels_generated_content(self):
        parts = load_parts(fx.build())
        md = cbp.render_knowledge_markdown(parts["manifest"], parts["objects"], parts["relations"])
        self.assertIn("Author's statement", md)
        self.assertIn("GENERATED, not the author's statement (generated_meaning)", md)
        self.assertIn("kc2_admission: not_measured", md)
        self.assertEqual(md.count("GENERATED"), sum(1 for o in parts["objects"] + parts["relations"] if o["origin"] != "author_statement"))

    def test_projection_only_proposes_publishable_markdown_layers(self):
        parts = load_parts(fx.build())
        md = cbp.render_knowledge_markdown(parts["manifest"], parts["objects"], parts["relations"])
        rows = cbp.candidate_projection(parts["manifest"], md)
        self.assertEqual({r["layer"] for r in rows}, {"document_md", "readable_md", "knowledge"})  # assets and quality are not Markdown
        self.assertTrue(all(r["kc2_admission"] == "not_measured" and r["status"] == "proposed" and r["limits"] for r in rows))
        self.assertTrue(all(r["proposed_repo_path"].startswith("articles/book-packages/") for r in rows))
        import export_corpus as ec
        self.assertTrue(all(ec.PATH_RE.fullmatch(r["proposed_repo_path"]) for r in rows))
        no_licence = copy.deepcopy(parts["manifest"])
        no_licence["rights"].pop("license")
        self.assertEqual(cbp.candidate_projection(no_licence, md), [])
        parts["manifest"]["rights"]["publishable_layers"] = []
        self.assertEqual(cbp.candidate_projection(parts["manifest"], md), [])

    def test_projection_does_not_widen_the_exporter_scope(self):
        import export_corpus as ec
        parts = load_parts(fx.build())
        md = cbp.render_knowledge_markdown(parts["manifest"], parts["objects"], parts["relations"])
        for row in cbp.candidate_projection(parts["manifest"], md):
            self.assertNotIn(f"schemas/fixtures/{row['path_in_package']}", ec.SCOPE_PATHS)
        self.assertNotIn("spec/BOOK_PACKAGE.md", ec.SCOPE_PATHS)  # until a decision widens it, the spec is not an indexing input


if __name__ == "__main__":
    unittest.main()
