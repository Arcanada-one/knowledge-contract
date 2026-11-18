# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Meaningful adverse controls for source coverage and proposal graph semantics."""
from copy import deepcopy
import unittest

from tools import check_cw_programme as checker


class ProgrammeControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arguments = checker.inputs()

    def setUp(self):
        self.graph = deepcopy(self.arguments[0])

    def task(self, key):
        return next(t for t in self.graph["tasks"] if t["id"] == key)

    def refresh_metrics(self):
        edges = {t["id"]: [d["task_id"] for d in t["dependencies"]] for t in self.graph["tasks"]}
        _, depth, _ = checker.topology(set(edges), edges)
        self.graph["proposed_graph_metrics"] = {"tasks": len(edges), "edges": sum(map(len, edges.values())),
                                                "longestDependencyChainNodes": max(depth.values())}

    def reject(self, reason):
        with self.assertRaisesRegex(checker.InvalidProgramme, reason):
            checker.validate(self.graph, *self.arguments[1:])

    def add_dependency(self, child, parent):
        self.task(child)["dependencies"].append({"task_id": parent, "consumes": [parent + ".O1"], "reason": "negative control"})

    def test_full_proposal_preserves_baseline_and_covers_papers_hypotheses(self):
        result = checker.validate(*self.arguments)
        self.assertEqual((result["work_packages"], result["source_steps_preserved"], result["paper_boundaries_covered"],
                          result["hypotheses_covered"]), (104, 72, 16, 12))
        self.assertEqual(result["native_registration"], "NOT_VERIFIED")

    def test_actual_epic_and_source_task_identifier_collision(self):
        self.graph["epics"][1]["id"] = "CW-E01"
        self.reject("identifier collision")

    def test_missing_source_step(self):
        self.graph["tasks"] = [t for t in self.graph["tasks"] if t["id"] != "CW-A04"]
        self.reject("scope counts")

    def test_rewritten_original_acceptance(self):
        self.task("CW-A04")["source_acceptance"] = "Treat all same-title pairs as duplicates."
        self.reject("source provenance rewritten")

    def test_lost_original_dependency_history(self):
        self.task("CW-H03")["source_dependencies"] = []
        self.reject("source provenance rewritten")

    def test_deleted_removed_edge_history_is_refused(self):
        self.task("CW-A03")["dependency_revisions"]["removed"] = []
        self.reject("revision removed differs from frozen-to-proposed")

    def test_repeated_added_edge_history_is_refused(self):
        entries = self.task("CW-A03")["dependency_revisions"]["added"]
        entries.append(deepcopy(entries[0]))
        self.reject("duplicate revision added edge")

    def test_blank_revision_edge_reason_is_refused(self):
        self.task("CW-A03")["dependency_revisions"]["removed"][0]["reason"] = "   "
        self.reject("revision removed edge lacks identity or reason")

    def test_forged_removed_edge_identity_is_refused(self):
        self.task("CW-A03")["dependency_revisions"]["removed"][0]["task_id"] = "CW-A01"
        self.reject("revision removed differs from frozen-to-proposed")

    def test_missing_general_dependency_revision_reason_is_refused(self):
        self.task("CW-A03")["dependency_revision_reason"] = ""
        self.reject("blank dependency revision rationale")

    def test_incomplete_epic_membership(self):
        self.graph["epics"][0]["task_ids"].pop()
        self.reject("epic membership")

    def test_consumed_output_belongs_to_a_different_predecessor(self):
        self.task("CW-A01")["dependencies"][0]["consumes"] = ["CW-A02.O1"]
        self.reject("wrong output")

    def test_dependency_cycle(self):
        self.add_dependency("CW-N01", "CW-N02")
        self.reject("dependency cycle")

    def test_duplicate_dependency(self):
        t = self.task("CW-A01")
        t["dependencies"].append(deepcopy(t["dependencies"][0]))
        self.reject("duplicate edge")

    def test_actual_old_domain_serialization_reintroduced(self):
        self.add_dependency("CW-H03", "CW-H02")
        self.refresh_metrics()
        self.reject("domain stands serialized")

    def test_announcement_registry_barrier_reintroduced(self):
        self.add_dependency("CW-N07", "CW-N06")
        self.refresh_metrics()
        self.reject("announcement unnecessarily blocked")

    def test_universal_empirical_gate_reintroduced(self):
        self.add_dependency("CW-N30", "CW-H01")
        self.refresh_metrics()
        self.reject("all publication classes blocked")

    def test_field_gate_removed(self):
        self.task("CW-H08")["dependencies"] = [d for d in self.task("CW-H08")["dependencies"] if d["task_id"] != "CW-N29"]
        self.refresh_metrics()
        self.reject("required evidence gate removed")

    def test_model_validity_cannot_precede_any_actual_domain_stand(self):
        for domain in ("CW-H02", "CW-H03", "CW-H04"):
            with self.subTest(domain=domain):
                self.graph = deepcopy(self.arguments[0])
                validity = self.task("CW-N18")
                validity["dependencies"] = [d for d in validity["dependencies"] if d["task_id"] != domain]
                self.refresh_metrics()
                self.reject("required evidence gate removed: CW-N18")

    def test_forged_native_status(self):
        self.task("CW-N06")["status"] = "completed"
        self.reject("promoted to execution state")

    def test_forged_assignment(self):
        self.task("CW-N06")["execution_assigned"] = True
        self.reject("native binding asserted")

    def test_root_programme_cannot_claim_completed(self):
        self.graph["status"] = "completed"
        self.reject("promoted to execution state")

    def test_root_programme_requires_its_own_acceptance_contract(self):
        self.graph["acceptance_criteria"] = []
        self.reject("acceptance criteria not consecutively numbered")

    def test_root_programme_requires_a_known_proposed_role(self):
        self.graph["proposed_owner_role"] = "unverified actor"
        self.reject("unknown proposed role")

    def test_boolean_is_not_an_acceptance_criterion_number(self):
        self.graph["acceptance_criteria"][0]["number"] = True
        self.reject("acceptance criteria not consecutively numbered")

    def test_future_output_claimed_as_created(self):
        self.task("CW-H08")["outputs"][0]["created"] = True
        self.reject("future output claimed")

    def test_paper_identity_swapped_without_changing_membership(self):
        a, b = self.graph["papers"][:2]
        a["source_index"], b["source_index"] = b["source_index"], a["source_index"]
        self.reject("source paper boundary altered")

    def test_hypothesis_refutation_erased(self):
        self.graph["hypotheses"][0]["source_refutation"] = "Always succeeds"
        self.reject("source hypothesis/refutation altered")

    def test_existing_but_wrong_task_cannot_replace_the_declared_boundary_map(self):
        for family in ("papers", "hypotheses"):
            with self.subTest(family=family):
                self.graph = deepcopy(self.arguments[0])
                self.graph[family][0]["mapped_task_ids"] = ["CW-N01"]
                self.reject("boundary mapping disagrees")

    def test_bibliographic_records_promoted_to_full_appraisals(self):
        self.graph["evidence_baseline"]["full_text_critical_appraisals"] = 1176
        self.reject("source evidence boundary changed")

    def test_same_count_foreign_source_rows(self):
        foreign = deepcopy(self.arguments[1])
        foreign[0]["id"] = "OTHER"
        with self.assertRaisesRegex(checker.InvalidProgramme, "source72 identity"):
            checker.validate(self.graph, foreign, *self.arguments[2:])

    def test_ambiguous_json_is_refused(self):
        for text in ('{"status":"proposed","status":"done"}', '{"cost":NaN}'):
            with self.subTest(text=text), self.assertRaises(checker.InvalidProgramme):
                checker.strict_json(text)

    def test_escaped_lone_surrogates_and_numeric_overflow_are_refused(self):
        for text in ('"\\ud800"', '{"nested":["\\udfff"]}', '{"\\ud800":1}',
                     '{"cost":1e309}', '{"nested":[-1e309]}'):
            with self.subTest(text=text), self.assertRaises(checker.InvalidProgramme):
                checker.strict_json(text)

    def test_valid_non_ascii_and_surrogate_pair_are_preserved(self):
        decoded = checker.strict_json('{"ru":"проверка","zh":"检查","pair":"\\ud83d\\ude00","cost":1.5}')
        self.assertEqual(decoded, {"ru": "проверка", "zh": "检查", "pair": "😀", "cost": 1.5})

    def release_instances(self):
        return checker.instantiate_release_instances(self.graph)

    def test_release_contracts_have_separate_counts_and_no_native_claim(self):
        result = checker.validate_release_instances(self.graph, self.release_instances())
        self.assertEqual((result["contracts"], result["required_evidence_edges"],
                          result["validated_release_stage_nodes"]), (16, 138, 96))
        self.assertEqual(result["native_release_instances_created"], 0)
        self.assertEqual(result["evidence_acceptance"], "NOT_VERIFIED")

    def test_p13_release_without_h08_is_refused(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P13")
        manuscript = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I03")
        manuscript["dependencies"] = [d for d in manuscript["dependencies"] if d["node_id"] != "CW-H08"]
        with self.assertRaisesRegex(checker.InvalidProgramme, "not upstream: CW-P13/CW-H08"):
            checker.validate_release_instances(self.graph, instances)

    def test_p09_and_p15_release_without_h08_are_refused(self):
        for paper_id in ("CW-P09", "CW-P15"):
            with self.subTest(paper_id=paper_id):
                instances = self.release_instances()
                release = next(r for r in instances if r["paper_id"] == paper_id)
                manuscript = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I03")
                manuscript["dependencies"] = [d for d in manuscript["dependencies"] if d["node_id"] != "CW-H08"]
                with self.assertRaisesRegex(checker.InvalidProgramme, "not upstream: " + paper_id + "/CW-H08"):
                    checker.validate_release_instances(self.graph, instances)

    def test_coverage_link_cannot_replace_required_paper_gate(self):
        contract = next(c for c in self.graph["paper_release_contracts"] if c["paper_id"] == "CW-P13")
        contract["required_gates"] = [g for g in contract["required_gates"] if g["task_id"] != "CW-H08"]
        self.graph["paper_release_metrics"]["required_evidence_edges"] -= 1
        self.reject("required paper evidence gates differ: CW-P13")

    def test_advisory_link_cannot_satisfy_release_evidence(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P13")
        gate = next(d for d in release["nodes"][0]["dependencies"] if d["node_id"] == "CW-H08")
        gate["type"] = "related_to"
        with self.assertRaisesRegex(checker.InvalidProgramme, "advisory release edge"):
            checker.validate_release_instances(self.graph, instances)

    def test_foreign_paper_reproducibility_package_does_not_satisfy_release(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P13")
        freeze = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I04")
        freeze["dependencies"][0].update(node_id="CW-P09.I03", consumes=["CW-P09.I03.O1"])
        with self.assertRaisesRegex(checker.InvalidProgramme, "foreign artifact"):
            checker.validate_release_instances(self.graph, instances)

    def test_generic_template_does_not_replace_specific_artifact_output(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P13")
        freeze = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I04")
        freeze["dependencies"][0].update(node_id="CW-I03", consumes=["CW-I03.O1"])
        with self.assertRaisesRegex(checker.InvalidProgramme, "artifact-specific release chain"):
            checker.validate_release_instances(self.graph, instances)

    def test_release_scope_cannot_be_silently_weakened(self):
        instances = self.release_instances()
        next(r for r in instances if r["paper_id"] == "CW-P13")["claim_scope"] = "Protocol only."
        with self.assertRaisesRegex(checker.InvalidProgramme, "claim_scope does not match"):
            checker.validate_release_instances(self.graph, instances)

    def test_review_release_remains_independent_of_field_intervention(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P01")
        edges = {t["id"]: [d["task_id"] for d in t["dependencies"]] for t in self.graph["tasks"]}
        edges.update({n["id"]: [d["node_id"] for d in n["dependencies"]] for n in release["nodes"]})
        _, _, ancestors = checker.topology(set(edges), edges)
        self.assertNotIn("CW-H08", ancestors["CW-P01.I08"])

    def test_reproduction_cannot_wait_for_target_publication_package(self):
        task = self.task("CW-N28")
        task["dependencies"][-1].update(task_id="CW-I04", consumes=["CW-I04.O1"])
        self.refresh_metrics()
        self.reject("reproduction must use a frozen evaluation package")

    def test_release_template_cannot_claim_native_assignment(self):
        instances = self.release_instances()
        instances[0]["nodes"][0]["execution_assigned"] = True
        with self.assertRaisesRegex(checker.InvalidProgramme, "claims native execution"):
            checker.validate_release_instances(self.graph, instances)

    def test_duplicate_paper_release_contract_is_refused(self):
        self.graph["paper_release_contracts"][-1] = deepcopy(self.graph["paper_release_contracts"][0])
        self.reject("duplicate or unknown paper release contract")


if __name__ == "__main__":
    unittest.main()
