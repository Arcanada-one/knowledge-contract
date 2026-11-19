#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Author-side tests of byte bindings, not scientific or reviewer acceptance.

The programme graph and criterion are real repository inputs. Every document,
result, person, protocol context and supplied observation below is explicitly
synthetic. A mechanical pass must never promote any of them to qualified review.
"""
from __future__ import annotations

import copy
from dataclasses import replace
import hashlib
import unittest
from unittest.mock import patch

try:
    from tools import prepare_cw_review as review
except ModuleNotFoundError:
    import prepare_cw_review as review


SOURCE_COMMIT = "9cbcd22fc215e8089363912dc531e42ef6845e29"
PREVIOUS_SOURCE_COMMIT = "b9b06226b1d67e82ff78ec2ca922af04a428469f"
GRAPH_SHA256 = "8c7b7e6fb1f95df9f9c1c85ce083fa7ba3250ed6637ae7ce1a41d6cc1c49e3a6"
JSON_DOMAIN = "sha256/raw-utf8-json-v1"


def synthetic_artifact(name, data, *, json_value=False, revision="synthetic-v1"):
    if json_value:
        return review.Artifact("synthetic:" + name, revision, review.encode(data), JSON_DOMAIN)
    return review.Artifact("synthetic:" + name, revision, data)


class ReviewBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The real pinned programme graph is a fixture, not fabricated output.
        # Read the tracked file so this also works in a shallow CI checkout.
        raw = (review.ROOT / review.GRAPH_PATH).read_bytes()
        if hashlib.sha256(raw).hexdigest() != GRAPH_SHA256:
            raise AssertionError("real CW graph fixture changed; review the fixture pin")
        cls.graph = review.Artifact("kc:cw-execution-graph", SOURCE_COMMIT, raw, JSON_DOMAIN)
        cls.criterion = review.criterion_artifact()
        cls.source = review.decode(raw)

    def fixtures(self, paper_id="CW-P02", *, announcement=False):
        documents = {
            "en": synthetic_artifact("complete-document:en", b"SYNTHETIC complete English document.\n\nSynthetic claim body.\n\nSynthetic final limitation.\n"),
            "ru": synthetic_artifact("complete-document:ru", "СИНТЕТИЧЕСКИЙ полный русский документ.\n\nСинтетическое утверждение.\n\nСинтетическое последнее ограничение.\n".encode("utf-8")),
            "zh-Hans": synthetic_artifact("complete-document:zh-Hans", "合成测试完整中文文档。\n\n合成测试主张。\n\n合成测试最终限制。\n".encode("utf-8")),
        }
        options = {
            "graph": self.graph,
            "expected_source_ref": self.graph.ref,
            "criterion": self.criterion,
            "purpose": "programme_announcement" if announcement else "paper_result",
            "documents": documents,
            "review_policy": synthetic_artifact("review-policy", b"SYNTHETIC review policy; no authority or publication grant.\n"),
        }
        if not announcement:
            contract = next(c for c in self.source["paper_release_contracts"] if c["paper_id"] == paper_id)
            outputs = sorted({out for gate in contract["required_gates"] for out in gate["consumes"]})
            options.update({
                "paper_id": paper_id,
                "applicability": synthetic_artifact("applicability", {
                    "population_or_model": "SYNTHETIC two-agent toy model, not a real organization",
                    "conditions": "SYNTHETIC deterministic fixture conditions",
                    "time_horizon": "SYNTHETIC one-step observation window",
                    "comparison": "SYNTHETIC inert comparator",
                    "quantifiers": "SYNTHETIC this finite fixture only",
                    "assumptions": "SYNTHETIC no authentic reviewer or external result",
                    "excluded_conclusions": "SYNTHETIC no scientific support, rights or competence established",
                }, json_value=True),
                "evidence": {out: review.Evidence(
                    synthetic_artifact("output:" + out, ("SYNTHETIC actual fixture bytes for " + out + "; not a research result.\n").encode("utf-8")),
                    "SYNTHETIC complete fixture record for " + out,
                    "new_synthetic_example",
                ) for out in outputs},
            })
        return options

    def observation(self, subject, prop, *, result="pass", suffix="one", context_changes=None, rule=None):
        scope = review.observation_scope(subject, prop)
        method = {"id": "synthetic:binding-fixture-method", "version": "synthetic-v1"}
        observer = "synthetic:unverified-reviewer"
        context = {
            "schema": "kc-cw-review-context/1",
            "subject": subject.artifact.ref,
            "criterion": subject.criterion.ref,
            "property": prop,
            "scope": scope,
            "reviewer": observer,
            "method": method,
            "review_kind": "internal_technical",
            "reviewer_access": "SYNTHETIC fixture bytes only; actual access not authenticated",
            "shared_dependencies": "SYNTHETIC same author-controlled test fixture",
            "independence_boundary": "SYNTHETIC no independent scientific review",
            "competence_basis": "SYNTHETIC self-report only; no competence verified",
        }
        if context_changes:
            context.update(context_changes)
        material = synthetic_artifact("context:" + prop + ":" + suffix, context, json_value=True)
        refs = []
        for item in (*subject.inputs, material):
            if item.ref not in refs:
                refs.append(item.ref)
        record = {
            "schema": "KCObservation/v1",
            "observation_id": "synthetic:observation:" + prop + ":" + suffix,
            "subject": subject.artifact.ref,
            "property": prop,
            "criterion": subject.criterion.ref,
            "method": method,
            "observer": observer,
            "observed_at": "2026-01-01T00:00:00Z",
            "result": result,
            "scope": scope,
            "evidence_refs": refs,
            "trust_assumptions": ["SYNTHETIC untrusted fixture; no authenticity assumption is established"],
            "limitations": ["SYNTHETIC mechanical binding test; not a review receipt or scientific evidence"],
        }
        if rule is not None:
            record["inapplicability_rule"] = rule.ref
        return review.encode(record), material

    def observations(self, subject):
        pairs = [self.observation(subject, prop) for prop in subject.required_properties]
        return tuple(raw for raw, _ in pairs), tuple(material for _, material in pairs)

    def assert_unknown_authority(self, report):
        for key in ("claim_support", "qualified_review", "reviewer_authenticity", "result", "eligibility"):
            self.assertEqual(report[key], "unknown", key)
        self.assertEqual(report["impact"], "requires_review")
        self.assertEqual(report["decision"], "revalidate")
        self.assertIs(report["effects_authorized"], False)
        self.assertIn("REVIEW_REQUIRED", report["reason_codes"])
        self.assertIn("reviewer_authenticity_not_established", report["reason_codes"])
        self.assertIn("competence_not_established", report["reason_codes"])
        for row in report["supplied_observations"]:
            self.assertEqual(row["authenticity"], "unknown")
            self.assertEqual(row["competence"], "unknown")

    def assert_successor_requires_review(self, original, successor, expected_changed_field):
        observations, materials = self.observations(original)
        self.assertNotEqual(original.artifact.ref, successor.artifact.ref)
        report = review.inspect_subject(successor, observations=observations, review_materials=materials,
                                        previous_descriptor=original.artifact.data)
        self.assertEqual(report["preparation_result"], "pass")
        self.assertEqual(report["binding_result"], "fail")
        self.assertIn(expected_changed_field, report["changed_material_fields"])
        self.assertIn("successor_assessment_required", report["reason_codes"])
        for row in report["supplied_observations"]:
            self.assertIn("subject_mismatch", row["problems"])
        self.assert_unknown_authority(report)
        return report

    def assert_missing_material(self, subject, prop, missing_ref):
        raw, material = self.observation(subject, prop)
        record = review.decode(raw)
        self.assertIn(missing_ref, record["evidence_refs"])
        record["evidence_refs"].remove(missing_ref)
        report = review.inspect_subject(subject, observations=[review.encode(record)], review_materials=[material])
        problems = report["supplied_observations"][0]["problems"]
        self.assertIn("required_material_not_referenced", problems)
        self.assertNotIn("evidence_bytes_missing_or_changed", problems)
        self.assertNotIn("review_context_missing_or_mismatched", problems)
        self.assert_unknown_authority(report)

    def test_unhashable_enum_inputs_are_typed_preparation_refusals(self):
        # Structural input errors are not scientific negative assessments.
        # These containers were TypeError before the bounded type guards.
        valid = synthetic_artifact("valid-enum", b"SYNTHETIC control bytes.")
        self.assertEqual(valid.hash_domain, "sha256/raw-bytes-v1")
        self.assertEqual(review.Evidence(valid, "SYNTHETIC locator", "original_result").origin,
                         "original_result")
        self.assertEqual(review.bind_subject(**self.fixtures()).missing, ())
        for malformed in ([], {}):
            with self.subTest(field="hash_domain", kind=type(malformed).__name__):
                with self.assertRaisesRegex(review.Invalid, "unsupported hash domain"):
                    review.Artifact("synthetic:invalid-domain", "synthetic-v1",
                                    b"SYNTHETIC bytes", malformed)
            with self.subTest(field="evidence_origin", kind=type(malformed).__name__):
                with self.assertRaisesRegex(review.Invalid, "unsupported evidence origin"):
                    review.Evidence(valid, "SYNTHETIC locator", malformed)
            with self.subTest(field="purpose", kind=type(malformed).__name__):
                options = self.fixtures()
                options["purpose"] = malformed
                with self.assertRaisesRegex(review.Invalid, "unsupported review purpose"):
                    review.bind_subject(**options)

    def test_complete_paper_packets_bind_but_never_establish_review(self):
        for paper_id in ("CW-P01", "CW-P02", "CW-P13"):
            with self.subTest(paper=paper_id):
                subject = review.bind_subject(**self.fixtures(paper_id))
                observations, materials = self.observations(subject)
                report = review.inspect_subject(subject, observations=observations, review_materials=materials)
                self.assertEqual(subject.missing, ())
                self.assertEqual(len(subject.required_properties), 7)
                self.assertEqual(report["preparation_result"], "pass")
                self.assertEqual(report["binding_result"], "pass")
                self.assertEqual(report["missing_properties"], [])
                self.assertEqual({row["extent"] for row in report["descriptor"]["documents"]}, {"complete_file"})
                self.assertTrue(all(row["origin"] == "new_synthetic_example" for row in report["descriptor"]["evidence"]))
                self.assert_unknown_authority(report)

    def test_no_supplied_observations_leave_binding_unknown(self):
        subject = review.bind_subject(**self.fixtures())
        report = review.inspect_subject(subject)
        self.assertEqual(report["preparation_result"], "pass")
        self.assertEqual(report["binding_result"], "unknown")
        self.assertEqual(set(report["missing_properties"]), set(subject.required_properties))
        self.assert_unknown_authority(report)

    def test_full_document_tail_changes_in_every_language_invalidate_old_observations(self):
        for language in ("en", "ru", "zh-Hans"):
            with self.subTest(language=language):
                options = self.fixtures()
                original = review.bind_subject(**options)
                artifact = options["documents"][language]
                options["documents"][language] = replace(artifact, data=artifact.data + b"\nSYNTHETIC changed final paragraph outside the opening claim.\n")
                self.assert_successor_requires_review(original, review.bind_subject(**options), "documents")

    def test_changed_applicability_domain_invalidate_old_observations(self):
        options = self.fixtures()
        original = review.bind_subject(**options)
        domain = review.decode(options["applicability"].data)
        domain["population_or_model"] = "SYNTHETIC three-agent model; changed applicability"
        options["applicability"] = replace(options["applicability"], data=review.encode(domain))
        self.assert_successor_requires_review(original, review.bind_subject(**options), "applicability")

    def test_criterion_raw_bytes_are_bound_even_when_json_meaning_is_identical(self):
        options = self.fixtures()
        original = review.bind_subject(**options)
        options["criterion"] = replace(options["criterion"], data=options["criterion"].data + b"\n")
        successor = review.bind_subject(**options)
        self.assertEqual(review.decode(original.criterion.data), review.decode(successor.criterion.data))
        report = self.assert_successor_requires_review(original, successor, "criterion")
        self.assertTrue(all("criterion_mismatch" in row["problems"] for row in report["supplied_observations"]))

    def test_changed_review_policy_invalidate_old_observations(self):
        options = self.fixtures()
        original = review.bind_subject(**options)
        options["review_policy"] = replace(options["review_policy"], data=b"SYNTHETIC changed policy requiring a different review procedure.\n")
        self.assert_successor_requires_review(original, review.bind_subject(**options), "review_policy")

    def test_changed_actual_evidence_bytes_invalidate_old_observations(self):
        options = self.fixtures()
        original = review.bind_subject(**options)
        output = sorted(options["evidence"])[0]
        item = options["evidence"][output]
        options["evidence"][output] = replace(item, artifact=replace(item.artifact, data=b"SYNTHETIC changed result bytes.\n"))
        self.assert_successor_requires_review(original, review.bind_subject(**options), "evidence")

    def test_evidence_locator_and_origin_are_material_changes(self):
        for field, value in (("locator", "SYNTHETIC different location in a complete artifact"),
                             ("origin", "reconstructed_view")):
            with self.subTest(field=field):
                options = self.fixtures()
                original = review.bind_subject(**options)
                output = sorted(options["evidence"])[0]
                options["evidence"][output] = replace(options["evidence"][output], **{field: value})
                self.assert_successor_requires_review(original, review.bind_subject(**options), "evidence")

    def test_selected_source_revision_change_requires_successor_review_even_with_same_graph(self):
        options = self.fixtures()
        original = review.bind_subject(**options)
        # Both commits are real; the graph blob is identical at these revisions.
        options["graph"] = replace(self.graph, revision=PREVIOUS_SOURCE_COMMIT)
        options["expected_source_ref"] = options["graph"].ref
        report = self.assert_successor_requires_review(original, review.bind_subject(**options), "source")
        self.assertEqual(report["descriptor"]["source"]["revision_provenance"],
                         "caller_selected_expected_reference_not_authenticated")

    def test_hash_domain_change_is_not_equivalent_to_original_reference(self):
        options = self.fixtures()
        original = review.bind_subject(**options)
        options["applicability"] = replace(options["applicability"], hash_domain="sha256/raw-bytes-v1")
        self.assert_successor_requires_review(original, review.bind_subject(**options), "applicability")

    def test_weakened_criterion_is_rejected(self):
        options = self.fixtures()
        criterion = review.decode(options["criterion"].data)
        criterion["properties"]["paper_result"].remove("claim_support")
        options["criterion"] = synthetic_artifact("weakened-criterion", criterion, json_value=True)
        with self.assertRaisesRegex(review.Invalid, "mandatory properties cannot be weakened"):
            review.bind_subject(**options)

    def test_p01_p02_claim_changes_cannot_inherit_review_when_pin_maps_are_updated(self):
        for paper_id in ("CW-P01", "CW-P02"):
            for field, map_name in (("claim_scope", "PAPER_CLAIM_SCOPES"), ("claim_class", "PAPER_CLAIM_CLASSES")):
                with self.subTest(paper=paper_id, field=field):
                    options = self.fixtures(paper_id)
                    original = review.bind_subject(**options)
                    source = copy.deepcopy(self.source)
                    contract = next(c for c in source["paper_release_contracts"] if c["paper_id"] == paper_id)
                    replacement = "SYNTHETIC altered claim text after the original observation" if field == "claim_scope" else "synthetic_altered_claim_class"
                    contract[field] = replacement
                    mutated = review.Artifact("synthetic:mutated-source-graph", "c" * 40, review.encode(source), JSON_DOMAIN)
                    options.update(graph=mutated, expected_source_ref=mutated.ref)
                    with patch.dict(getattr(review.programme, map_name), {paper_id: replacement}):
                        # The patched map deliberately admits the new statement.
                        # The adapter must still give it a different subject.
                        successor = review.bind_subject(**options)
                        self.assert_successor_requires_review(original, successor, "claim")

    def test_mutated_gate_map_at_same_revision_fails_independently_selected_source_ref(self):
        for field in ("required_gates", "mapped_task_ids"):
            with self.subTest(field=field):
                source = copy.deepcopy(self.source)
                if field == "required_gates":
                    source["paper_release_contracts"][0][field].pop()
                else:
                    source["papers"][0][field].pop()
                options = self.fixtures()
                options["graph"] = replace(self.graph, data=review.encode(source))
                with self.assertRaisesRegex(review.Invalid, "independently selected expected reference"):
                    review.bind_subject(**options)

    def test_selected_reference_covers_every_ref_component(self):
        for changes in ({"artifact_id": "synthetic:unexpected-source"},
                        {"revision": "a" * 40}, {"hash_domain": "sha256/raw-bytes-v1"}):
            with self.subTest(changes=changes):
                options = self.fixtures()
                options["graph"] = replace(self.graph, **changes)
                with self.assertRaisesRegex(review.Invalid, "independently selected expected reference"):
                    review.bind_subject(**options)

    def test_missing_paper_outputs_are_reported_as_missing_inputs(self):
        options = self.fixtures("CW-P13")
        required = sorted(options["evidence"])
        options["evidence"] = {}
        subject = review.bind_subject(**options)
        observations, materials = self.observations(subject)
        report = review.inspect_subject(subject, observations=observations, review_materials=materials)
        self.assertEqual(subject.missing, tuple("output:" + output for output in required))
        self.assertEqual(report["preparation_result"], "unknown")
        self.assertIn("required_inputs_missing", report["reason_codes"])
        self.assertTrue(all(row["artifact"] is None and row["origin"] == "missing"
                            for row in report["descriptor"]["evidence"]))
        self.assert_unknown_authority(report)

    def test_task_identifier_or_future_path_cannot_substitute_for_actual_output_bytes(self):
        for value in ("CW-B01", "future/results/CW-B01.json", {"task_id": "CW-B01", "status": "planned"}):
            with self.subTest(value=value):
                options = self.fixtures()
                output = sorted(options["evidence"])[0]
                options["evidence"][output] = value
                with self.assertRaisesRegex(review.Invalid, "not observed evidence"):
                    review.bind_subject(**options)

    def test_evidence_rejects_nonbytes_empty_and_planned_origins(self):
        with self.assertRaisesRegex(review.Invalid, "actual artifact bytes"):
            review.Evidence("synthetic:future-file", "SYNTHETIC future locator", "new_synthetic_example")
        with self.assertRaisesRegex(review.Invalid, "artifact is empty"):
            review.Evidence(synthetic_artifact("empty", b""), "SYNTHETIC locator", "new_synthetic_example")
        with self.assertRaisesRegex(review.Invalid, "a plan is not an output"):
            review.Evidence(synthetic_artifact("plan", b"SYNTHETIC planned record"), "SYNTHETIC locator", "planned")

    def test_missing_english_applicability_and_policy_remain_explicit(self):
        options = self.fixtures()
        del options["documents"]["en"]
        options.pop("applicability")
        options.pop("review_policy")
        subject = review.bind_subject(**options)
        self.assertEqual(set(subject.missing), {"complete_document:en", "applicability", "review_policy"})
        report = review.inspect_subject(subject)
        self.assertEqual(report["preparation_result"], "unknown")
        self.assert_unknown_authority(report)

    def test_incomplete_applicability_descriptor_cannot_silently_drop_exclusions(self):
        options = self.fixtures()
        domain = review.decode(options["applicability"].data)
        del domain["excluded_conclusions"]
        options["applicability"] = synthetic_artifact("incomplete-domain", domain, json_value=True)
        with self.assertRaisesRegex(review.Invalid, "incomplete or unsupported applicability"):
            review.bind_subject(**options)

    def test_claim_support_requires_each_actual_result_reference(self):
        options = self.fixtures("CW-P13")
        subject = review.bind_subject(**options)
        for output, item in options["evidence"].items():
            with self.subTest(output=output):
                self.assert_missing_material(subject, "claim_support", item.artifact.ref)

    def test_coverage_and_rights_require_all_bound_language_documents(self):
        options = self.fixtures()
        subject = review.bind_subject(**options)
        for prop in ("claim_coverage", "publication_rights"):
            for language, document in options["documents"].items():
                with self.subTest(property=prop, language=language):
                    self.assert_missing_material(subject, prop, document.ref)

    def test_translation_requires_both_source_and_target_complete_documents(self):
        options = self.fixtures()
        subject = review.bind_subject(**options)
        for language in ("ru", "zh-Hans"):
            for required in ("en", language):
                with self.subTest(target=language, required=required):
                    self.assert_missing_material(subject, "translation_fidelity:" + language,
                                                 options["documents"][required].ref)

    def test_applicability_and_protocol_require_their_own_material(self):
        options = self.fixtures()
        subject = review.bind_subject(**options)
        self.assert_missing_material(subject, "applicability", options["applicability"].ref)
        self.assert_missing_material(subject, "review_protocol", options["review_policy"].ref)

    def test_announcement_needs_no_scientific_results_or_applicability(self):
        subject = review.bind_subject(**self.fixtures(announcement=True))
        observations, materials = self.observations(subject)
        report = review.inspect_subject(subject, observations=observations, review_materials=materials)
        self.assertEqual(subject.missing, ())
        self.assertEqual(report["preparation_result"], "pass")
        self.assertEqual(report["binding_result"], "pass")
        self.assertEqual(report["descriptor"]["evidence"], [])
        self.assertIsNone(report["descriptor"]["applicability"])
        self.assertEqual(report["descriptor"]["claim"]["status"], "proposed")
        self.assertEqual(report["descriptor"]["claim"]["work_packages"], 104)
        self.assertNotIn("claim_support", subject.required_properties)
        self.assert_unknown_authority(report)

    def test_announcement_accuracy_requires_graph_and_all_documents(self):
        options = self.fixtures(announcement=True)
        subject = review.bind_subject(**options)
        for material in (self.graph, *options["documents"].values()):
            with self.subTest(material=material.artifact_id):
                self.assert_missing_material(subject, "announcement_accuracy", material.ref)
        self.assert_missing_material(subject, "review_protocol", options["review_policy"].ref)

    def test_announcement_cannot_inherit_a_paper_identity_or_scientific_output_set(self):
        for extra in ({"paper_id": "CW-P02"}, {"evidence": self.fixtures()["evidence"]}):
            with self.subTest(extra=tuple(extra)):
                options = self.fixtures(announcement=True)
                options.update(extra)
                with self.assertRaises(review.Invalid):
                    review.bind_subject(**options)

    def test_forged_context_fields_fail_even_with_fresh_context_hashes(self):
        subject = review.bind_subject(**self.fixtures())
        mismatches = {
            "reviewer": "synthetic:different-reviewer",
            "subject": self.graph.ref,
            "criterion": self.graph.ref,
            "method": {"id": "synthetic:different-method", "version": "synthetic-v1"},
            "property": "publication_rights",
            "scope": "SYNTHETIC narrower scope that does not cover this subject",
            "review_kind": "synthetic_unsupported_kind",
            "competence_basis": True,
            "reviewer_access": " ",
            "shared_dependencies": [],
            "independence_boundary": None,
        }
        for field, value in mismatches.items():
            with self.subTest(field=field):
                # Hash and ref are recomputed after the mutation. This isolates
                # contextual binding from a trivial stale artifact digest.
                raw, material = self.observation(subject, "claim_support", context_changes={field: value})
                report = review.inspect_subject(subject, observations=[raw], review_materials=[material])
                problems = report["supplied_observations"][0]["problems"]
                self.assertIn("review_context_missing_or_mismatched", problems)
                self.assertNotIn("evidence_bytes_missing_or_changed", problems)
                self.assert_unknown_authority(report)

    def test_review_kind_malformed_json_values_are_reported_as_context_mismatches(self):
        subject = review.bind_subject(**self.fixtures())
        for valid_kind in ("editorial", "internal_technical", "independent_agent", "external_peer"):
            with self.subTest(review_kind=valid_kind):
                raw, material = self.observation(subject, "claim_support",
                                                 context_changes={"review_kind": valid_kind})
                report = review.inspect_subject(subject, observations=[raw], review_materials=[material])
                row = report["supplied_observations"][0]
                self.assertEqual(row["binding_result"], "pass")
                self.assertEqual(row["problems"], [])
        for invalid_kind in ("synthetic_unsupported_kind", [], {}):
            with self.subTest(review_kind=invalid_kind):
                raw, material = self.observation(subject, "claim_support",
                                                 context_changes={"review_kind": invalid_kind})
                report = review.inspect_subject(subject, observations=[raw], review_materials=[material])
                row = report["supplied_observations"][0]
                self.assertEqual(row["binding_result"], "fail")
                self.assertEqual(row["claimed_result"], "pass")
                self.assertIn("review_context_missing_or_mismatched", row["problems"])
                self.assertIs(report["effects_authorized"], False)

    def test_self_declared_external_review_and_competence_never_authenticate(self):
        subject = review.bind_subject(**self.fixtures())
        pairs = [self.observation(subject, prop, context_changes={
            "review_kind": "external_peer",
            "competence_basis": "SYNTHETIC unverified claim of expertise and external approval",
            "independence_boundary": "SYNTHETIC self-declared independence, not established",
        }) for prop in subject.required_properties]
        report = review.inspect_subject(subject, observations=[p[0] for p in pairs], review_materials=[p[1] for p in pairs])
        self.assertEqual(report["binding_result"], "pass")
        self.assert_unknown_authority(report)

    def test_internally_matching_wrong_scope_still_fails_deterministic_scope(self):
        subject = review.bind_subject(**self.fixtures())
        wrong_scope = "SYNTHETIC opening paragraph only"
        raw, material = self.observation(subject, "claim_support", context_changes={"scope": wrong_scope})
        record = review.decode(raw)
        record["scope"] = wrong_scope
        report = review.inspect_subject(subject, observations=[review.encode(record)], review_materials=[material])
        self.assertEqual(report["supplied_observations"][0]["problems"], ["scope_mismatch"])
        self.assert_unknown_authority(report)

    def test_context_for_another_property_cannot_be_reused(self):
        subject = review.bind_subject(**self.fixtures())
        raw, material = self.observation(subject, "claim_coverage")
        record = review.decode(raw)
        record["property"] = "publication_rights"
        record["scope"] = review.observation_scope(subject, "publication_rights")
        report = review.inspect_subject(subject, observations=[review.encode(record)], review_materials=[material])
        self.assertIn("review_context_missing_or_mismatched", report["supplied_observations"][0]["problems"])
        self.assertNotIn("scope_mismatch", report["supplied_observations"][0]["problems"])
        self.assert_unknown_authority(report)

    def test_additional_authority_flag_is_not_a_supported_context_extension(self):
        subject = review.bind_subject(**self.fixtures())
        raw, material = self.observation(subject, "claim_support", context_changes={"authenticated": True})
        report = review.inspect_subject(subject, observations=[raw], review_materials=[material])
        self.assertIn("review_context_missing_or_mismatched", report["supplied_observations"][0]["problems"])
        self.assert_unknown_authority(report)

    def test_missing_or_ambiguous_context_cannot_satisfy_binding(self):
        subject = review.bind_subject(**self.fixtures())
        raw, material = self.observation(subject, "claim_support")
        report = review.inspect_subject(subject, observations=[raw])
        self.assertIn("evidence_bytes_missing_or_changed", report["supplied_observations"][0]["problems"])
        self.assertIn("review_context_missing_or_mismatched", report["supplied_observations"][0]["problems"])
        second = replace(material, artifact_id="synthetic:second-protocol-context")
        record = review.decode(raw)
        record["evidence_refs"].append(second.ref)
        ambiguous = review.inspect_subject(subject, observations=[review.encode(record)], review_materials=[material, second])
        self.assertIn("review_context_missing_or_mismatched", ambiguous["supplied_observations"][0]["problems"])
        self.assert_unknown_authority(ambiguous)

    def test_conflicting_bytes_for_one_identity_are_rejected_without_last_writer_wins(self):
        subject = review.bind_subject(**self.fixtures())
        raw, material = self.observation(subject, "claim_support")
        context = review.decode(material.data)
        context["competence_basis"] = "SYNTHETIC conflicting claimed competence"
        conflicting = replace(material, data=review.encode(context))
        for materials in ((material, conflicting), (conflicting, material)):
            with self.subTest(order=[m.ref["sha256"] for m in materials]):
                with self.assertRaisesRegex(review.Invalid, "conflicting bytes for the same artifact identity"):
                    review.inspect_subject(subject, observations=[raw], review_materials=materials)

    def test_duplicate_observation_identifiers_are_rejected_even_when_bytes_match(self):
        subject = review.bind_subject(**self.fixtures())
        raw, material = self.observation(subject, "claim_support")
        changed = review.decode(raw)
        changed["result"] = "fail"
        for second in (raw, review.encode(changed)):
            with self.subTest(same_bytes=second == raw):
                with self.assertRaisesRegex(review.Invalid, "duplicate observation ID"):
                    review.inspect_subject(subject, observations=[raw, second], review_materials=[material])

    def test_negative_unknown_and_exemption_observations_are_retained_in_both_orders(self):
        subject = review.bind_subject(**self.fixtures())
        pairs = [self.observation(subject, prop) for prop in subject.required_properties if prop != "claim_support"]
        rule = synthetic_artifact("inapplicability-rule", b"SYNTHETIC proposed exemption; validity is not established.\n")
        pairs.extend(self.observation(subject, "claim_support", result=result, suffix=result,
                                      rule=rule if result == "not_applicable" else None)
                     for result in ("pass", "fail", "unknown", "not_applicable"))
        for order in (pairs, list(reversed(pairs))):
            with self.subTest(order=[review.decode(p[0])["result"] for p in order]):
                report = review.inspect_subject(subject, observations=[p[0] for p in order],
                                                review_materials=[p[1] for p in order] + [rule])
                self.assertEqual(report["binding_result"], "pass")
                support = [row for row in report["supplied_observations"] if row["property"] == "claim_support"]
                self.assertEqual(len(support), 4)
                self.assertEqual({row["claimed_result"] for row in support}, {"pass", "fail", "unknown", "not_applicable"})
                self.assertIn("supplied_negative_assessment_retained", report["reason_codes"])
                self.assertIn("supplied_unknown_assessment_retained", report["reason_codes"])
                self.assertIn("supplied_exemption_not_established", report["reason_codes"])
                for raw, _ in order:
                    record = review.decode(raw)
                    row = next(r for r in report["supplied_observations"] if r["observation_id"] == record["observation_id"])
                    self.assertEqual(row["sha256"], hashlib.sha256(raw).hexdigest())
                self.assert_unknown_authority(report)

    def test_not_applicable_needs_actual_rule_bytes_and_cannot_hide_missing_rule(self):
        subject = review.bind_subject(**self.fixtures())
        rule = synthetic_artifact("unavailable-rule", b"SYNTHETIC rule bytes intentionally withheld from inspection.\n")
        raw, material = self.observation(subject, "claim_support", result="not_applicable", rule=rule)
        report = review.inspect_subject(subject, observations=[raw], review_materials=[material])
        self.assertIn("inapplicability_rule_unresolved", report["supplied_observations"][0]["problems"])
        self.assert_unknown_authority(report)
        record = review.decode(raw)
        del record["inapplicability_rule"]
        with self.assertRaisesRegex(review.Invalid, "malformed observation"):
            review.inspect_subject(subject, observations=[review.encode(record)], review_materials=[material])

    def test_forged_bound_subject_cannot_delete_missing_inputs(self):
        options = self.fixtures()
        options["evidence"] = {}
        incomplete = review.bind_subject(**options)
        with self.assertRaisesRegex(review.Invalid, "reconstructed mandatory inputs"):
            review.inspect_subject(replace(incomplete, missing=()))

    def test_forged_bound_subject_cannot_delete_required_review_properties(self):
        complete = review.bind_subject(**self.fixtures())
        with self.assertRaisesRegex(review.Invalid, "reconstructed mandatory inputs"):
            review.inspect_subject(replace(complete, required_properties=()))

    def test_descriptor_rewrite_with_recomputed_hash_cannot_remove_an_output_obligation(self):
        options = self.fixtures()
        options["evidence"] = {}
        incomplete = review.bind_subject(**options)
        descriptor = review.decode(incomplete.artifact.data)
        descriptor["evidence"] = []
        descriptor["missing_inputs"] = []
        raw = review.encode(descriptor)
        artifact = replace(incomplete.artifact, data=raw, revision="content-" + hashlib.sha256(raw).hexdigest())
        with self.assertRaisesRegex(review.Invalid, "reconstructed mandatory inputs"):
            review.inspect_subject(replace(incomplete, artifact=artifact, missing=()))


if __name__ == "__main__":
    unittest.main()
