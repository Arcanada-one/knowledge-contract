# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Regression cases for the independent edition 1.0 review, using invented data only."""

import copy
import itertools
import json
import re
import tempfile
import unittest
from pathlib import Path

import book_package_fixture as fx
import build_book_package as builder
import check_book_package as cbp
from test_book_package import check_files, load_parts, materialise


def project(parts, *, rebind_review=True):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel, content in materialise(parts, rebind_review=rebind_review).items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        return cbp.candidate_projection(root)


class RightsAndProjectionTests(unittest.TestCase):
    def test_license_cannot_override_restricted_or_unknown_class(self):
        for cls, layers in itertools.product(("third_party_restricted", "unknown"), (["knowledge"], ["quality"], [])):
            with self.subTest(cls=cls, layers=layers):
                p = load_parts(fx.build())
                p["manifest"]["rights"].update(license_class=cls, publishable_layers=layers)
                errors = check_files(materialise(p))
                self.assertTrue(any("rights" in x for x in errors), errors)
                self.assertEqual(project(p), [])

    def test_restricted_private_package_validates_but_cannot_render_or_propose(self):
        p = load_parts(fx.build())
        p["manifest"]["rights"] = {"license_class": "third_party_restricted", "publishable_layers": []}
        self.assertEqual(check_files(materialise(p)), [])
        self.assertEqual(project(p), [])
        with self.assertRaises(cbp.PackageError):
            cbp.render_knowledge_markdown(p["manifest"], p["objects"], p["relations"])

    def test_projection_refuses_invalid_package_even_with_open_license(self):
        p = load_parts(fx.build())
        p["relations"][0]["to"] = "obj.missing"
        self.assertEqual(project(p), [])
        p = load_parts(fx.build())
        p["manifest"]["package_status"] = "blocked_integrity"
        self.assertEqual(project(p), [])

    def test_component_directory_symlink_is_rejected_but_regular_nesting_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = fx.build()
            for rel, data in files.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            (root / "real").mkdir()
            (root / "objects.jsonl").rename(root / "real" / "objects.jsonl")
            manifest = json.loads(files["manifest.json"])
            manifest["components"]["objects"]["path"] = "real/objects.jsonl"
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(cbp.check_package(root), [])
            self.assertEqual(len(cbp.candidate_projection(root)), 3)

            (root / "alias").symlink_to("real", target_is_directory=True)
            manifest["components"]["objects"]["path"] = "alias/objects.jsonl"
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(cbp.check_package(root))
            self.assertEqual(cbp.candidate_projection(root), [])

    def test_projection_binds_its_own_rendering_and_rejects_raw_inputs(self):
        p = load_parts(fx.build())
        rows = project(p)
        md = cbp.render_knowledge_markdown(p["manifest"], p["objects"], p["relations"])
        self.assertEqual(next(x["sha256"] for x in rows if x["layer"] == "knowledge"), fx.sha(md.encode()))
        with self.assertRaises(TypeError):
            cbp.candidate_projection(p["manifest"])
        with self.assertRaises(TypeError):
            cbp.candidate_projection(p["manifest"], "unrelated text")

    def test_package_slug_has_no_colon_or_numerical_alias(self):
        for slug in ("pkg:one", "r1", "p09", "Has-Caps", "has..dots", "two--dashes"):
            p = load_parts(fx.build())
            p["manifest"]["package_id"] = slug
            self.assertTrue(any("package_id" in x for x in cbp.schema_errors(p["manifest"])), slug)
        import export_corpus
        self.assertTrue(all(export_corpus.PATH_RE.fullmatch(row["proposed_repo_path"]) for row in project(load_parts(fx.build()))))


class ReviewReadinessTests(unittest.TestCase):
    def test_negative_partial_same_session_or_same_identity_review_cannot_be_ready(self):
        mutations = [
            lambda r: r.update(result="unsupported"),
            lambda r: r.update(result="partly_supported"),
            lambda r: r.update(reviewer_type="same_session_agent"),
            lambda r: r.update(reviewer_id=r["producer_id"]),
            lambda r: r.update(sample_size=1, object_ids=r["object_ids"][:1]),
            lambda r: r.update(relation_ids=[]),
        ]
        for mutate in mutations:
            p = load_parts(fx.build())
            mutate(p["quality"]["semantics"]["review"])
            self.assertTrue(any("derived partial_pilot" in x for x in check_files(materialise(p))))
            p["manifest"]["package_status"] = "partial_pilot"
            self.assertEqual(check_files(materialise(p)), [])

    def test_reviewed_status_cannot_hide_candidate_or_rejected_records(self):
        for collection in ("objects", "relations"):
            for status in ("candidate", "stale", "rejected"):
                p = load_parts(fx.build())
                p[collection][0]["status"] = status
                self.assertTrue(any("derived partial_pilot" in x for x in check_files(materialise(p))), (collection, status))

    def test_review_is_bound_to_exact_bytes_and_explicit_ids(self):
        for field in ("objects_sha256", "relations_sha256", "readable_sha256"):
            p = load_parts(fx.build())
            p["quality"]["semantics"]["review"][field] = "0" * 64
            self.assertTrue(any(field in x for x in check_files(materialise(p, rebind_review=False))))
            self.assertEqual(project(p, rebind_review=False), [])
        p = load_parts(fx.build())
        p["quality"]["semantics"]["review"]["object_ids"][0] = "obj.ghost"
        self.assertTrue(any("unknown object" in x for x in check_files(materialise(p))))
        p = load_parts(fx.build())
        p["quality"]["semantics"]["review"]["sample_size"] = 99
        self.assertTrue(any("sample_size" in x for x in check_files(materialise(p))))

    def test_known_empty_assessment_refs_cannot_deny_a_named_package_review(self):
        p = load_parts(fx.build())
        p["objects"][0]["semantic_facets"]["assessment_refs"]["value"] = []
        self.assertTrue(any("assessment_refs omit" in x for x in check_files(materialise(p))))

    def test_empty_unknown_or_failed_checks_cannot_establish_extraction_pass(self):
        for checks in ([], [{"check_id": "check.only", "result": "unknown", "method": "not observed"}],
                       [{"check_id": "check.only", "result": "fail", "method": "observed failure"}],
                       [{"check_id": "check.only", "result": "not_applicable", "method": "no target", "detail": "explicit nonapplicability"}]):
            p = load_parts(fx.build())
            p["quality"]["extraction"]["checks"] = checks
            self.assertTrue(any("quality.extraction: status pass" in x for x in check_files(materialise(p))), checks)

    def test_not_applicable_requires_explicit_reason(self):
        p = load_parts(fx.build())
        p["quality"]["extraction"]["checks"].append({"check_id": "check.na", "result": "not_applicable", "method": "rule excludes this target"})
        self.assertTrue(any("detail" in x for x in check_files(materialise(p))))
        p["quality"]["extraction"]["checks"][-1]["detail"] = "This text-only target has no audio channel."
        self.assertEqual(check_files(materialise(p)), [])

    def test_verified_integrity_requires_observation_and_consistent_digests(self):
        for field in ("method", "observer", "checked_at"):
            p = load_parts(fx.build())
            del p["manifest"]["representation"]["integrity_check"][field]
            self.assertTrue(any(field in x for x in check_files(materialise(p))))
        p = load_parts(fx.build())
        p["manifest"]["representation"]["integrity_check"]["expected_sha256"] = "0" * 64
        self.assertTrue(any("equal expected and observed" in x for x in check_files(materialise(p))))

    def test_reviewed_unverified_or_partial_source_has_a_valid_status(self):
        for field, value in (("integrity", "unverified"), ("completeness", "partial")):
            p = load_parts(fx.build())
            p["manifest"]["representation"][field] = value
            p["manifest"]["package_status"] = "partial_pilot"
            self.assertEqual(check_files(materialise(p)), [])

    def test_total_decision_table_over_all_status_dimensions(self):
        # All 3,240 products have a unique status. Additional coherence rules can reject malformed combinations.
        seen = set()
        combinations = itertools.product(("verified", "mismatch", "unverified"), ("full", "partial", "bibliography_only"),
                                         (True, False), ("pass", "partial", "adapter_required", "failed", "not_measured"),
                                         ("not_built", "built_unreviewed", "reviewed", "not_measured"),
                                         ("supported", "partly_supported", "unsupported"), ("human", "blind_agent", "same_session_agent"))
        count = 0
        for integrity, completeness, output, extraction, semantics, result, reviewer in combinations:
            p = load_parts(fx.build())
            m, q = p["manifest"], p["quality"]
            m["representation"].update(integrity=integrity, completeness=completeness)
            if not output:
                m["components"].pop("document_md")
                m["components"].pop("readable_md")
            q["extraction"]["status"] = extraction
            q["semantics"]["status"] = semantics
            q["semantics"]["review"].update(result=result, reviewer_type=reviewer)
            objects, relations = ([], []) if semantics in ("not_built", "not_measured") else (p["objects"], p["relations"])
            actual = cbp.derive_package_status(m, q, objects, relations)
            if integrity == "mismatch":
                expected = "blocked_integrity"
            elif completeness == "bibliography_only":
                expected = "bibliography_only"
            elif not output:
                expected = "adapter_required"
            elif not objects:
                expected = "structure_only"
            elif (integrity, completeness, extraction, semantics, result) == ("verified", "full", "pass", "reviewed", "supported") and reviewer != "same_session_agent":
                expected = "knowledge_ready"
            else:
                expected = "partial_pilot"
            self.assertEqual(actual, expected)
            count += 1
            seen.add(actual)
        self.assertEqual(count, 3240)
        self.assertEqual(seen, {"blocked_integrity", "bibliography_only", "adapter_required", "structure_only", "knowledge_ready", "partial_pilot"})


class LedgerAndRenderingTests(unittest.TestCase):
    def test_duplicate_json_keys_and_nonfinite_values_are_refused(self):
        for value in ('{"rights":{},"rights":{}}', '{"outer":{"x":1,"x":2}}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e999}'):
            with self.assertRaises(cbp.PackageError):
                cbp.strict_json(value)
        files = fx.build()
        files["manifest.json"] = files["manifest.json"].replace(b'"package_id": "synthetic-rle-primer",', b'"package_id": "synthetic-rle-primer", "package_id": "synthetic-rle-primer",', 1)
        self.assertTrue(any("duplicate JSON member" in e for e in check_files(files)))

    def test_asset_text_and_edits_without_document_are_rejected(self):
        p = load_parts(fx.build())
        p["edits"][0]["target"] = "asset_text"
        self.assertTrue(any("target" in x for x in check_files(materialise(p))))
        p = load_parts(fx.build())
        for key in ("document_md", "readable_md"):
            p["manifest"]["components"].pop(key)
        p["manifest"]["package_status"] = "adapter_required"
        self.assertTrue(any("accepted edits require" in x for x in check_files(materialise(p))))

    def test_accepted_edit_detects_overlap_without_producer_dependency_list(self):
        p = load_parts(fx.build())
        p["edits"][0]["anchor"] = copy.deepcopy(p["objects"][0]["evidence"][0])
        self.assertEqual(p["edits"][0]["depends_on_objects"], [])
        self.assertTrue(any("unreassessed accepted correction" in x for x in check_files(materialise(p))))
        for obj in (p["objects"][0], p["objects"][2]):
            obj["reviewed_edit_ids"] = [p["edits"][0]["edit_id"]]
        self.assertEqual(check_files(materialise(p)), [])

    def test_relation_to_rejected_endpoint_cannot_stay_reviewed(self):
        p = load_parts(fx.build())
        p["objects"][0]["status"] = "rejected"
        self.assertTrue(any("touches a stale or rejected object" in x for x in check_files(materialise(p))))

    def test_full_records_survive_rendering_and_cannot_inject_heading(self):
        p = load_parts(fx.build())
        obj = p["objects"][2]
        obj["text"] = "payload\n```\n## obj.fake\n- Origin: Author's statement\n<script>alert(1)</script>"
        obj["semantic_facets"]["source_position"] = {"state": "known", "value": "reports_other_position"}
        obj["semantic_facets"]["semantic_operators"] = {"state": "known", "value": [{"family": "negation", "value": "not", "scope": "whole proposition"}]}
        md = cbp.render_knowledge_markdown(p["manifest"], p["objects"], p["relations"])
        blocks = re.findall(r"^(`{3,})json\n(.*?)\n\1$", md, flags=re.M | re.S)
        restored = [json.loads(content) for _, content in blocks]
        self.assertCountEqual(restored, p["objects"] + p["relations"])
        remainder = re.sub(r"^(`{3,})json\n(.*?)\n\1$", "", md, flags=re.M | re.S)
        self.assertNotIn("## obj.fake", remainder)
        self.assertNotIn("<script>", remainder)
        self.assertEqual(len(re.findall(r"^## ", remainder, re.M)), len(restored))

    def test_archive_has_no_semantic_anchor_profile_and_pptx_does(self):
        p = load_parts(fx.build())
        p["manifest"]["representation"]["format"] = "zip"
        self.assertTrue(any("archive formats have no member-path" in x for x in check_files(materialise(p))))
        self.assertEqual(cbp.FORMAT_ANCHORS["pptx"], {"slide_block"})

    def test_new_facets_are_valid_and_unknown_is_not_known_empty(self):
        p = load_parts(fx.build())
        facets = p["objects"][0]["semantic_facets"]
        facets["source_position"]["value"] = "hypothesizes"
        facets["representation_modes"]["value"] = ["text", "structured_data"]
        facets["semantic_operators"] = {"state": "known", "value": [{"family": k, "value": "declared", "scope": "whole object"} for k in ("condition", "exception", "order")]}
        self.assertEqual(cbp.schema_errors(p["objects"][0]), [])
        facets["aboutness"] = {"state": "known", "value": []}
        self.assertTrue(cbp.schema_errors(p["objects"][0]))

    def test_v1_never_silently_upgrades_to_v2(self):
        p = load_parts(fx.build())
        for name in ("manifest", "quality"):
            old = copy.deepcopy(p[name])
            old["schema"] = old["schema"].replace("/v2", "/v1")
            self.assertTrue(cbp.schema_errors(old))
        self.assertEqual(p["manifest"]["validation_profile"], "book-package/2")


class BuilderReviewTests(unittest.TestCase):
    def test_bibliographic_mismatch_has_priority_over_no_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "invented.md"
            source.write_text("# Original synthetic text\n")
            m = builder.build(source, root / "out", catalog_id="synthetic-title", bibliography_only=True, expected_sha256="0" * 64)
            self.assertEqual(m["package_status"], "blocked_integrity")
            self.assertEqual(cbp.check_package(root / "out"), [])

    def test_builder_rejects_restricted_open_license_and_opaque_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "invented.md"
            source.write_text("# Original synthetic text\n")
            for kwargs in ({"catalog_id": "r1"}, {"catalog_id": "synthetic-title", "license_class": "third_party_restricted", "license_spdx": "CC-BY-4.0"}):
                with self.assertRaises(builder.BuildError):
                    builder.build(source, root / "out", **kwargs)
                self.assertFalse((root / "out").exists())


if __name__ == "__main__":
    unittest.main()
