# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Meaningful adverse controls for source coverage and proposal graph semantics."""
from copy import deepcopy
import json
import unicodedata
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
        task = self.task(child)
        task["dependencies"].append({"task_id": parent, "consumes": [parent + ".O1"], "reason": "negative control"})
        # Semantic mutants must have a coherent ledger so they reach the
        # independent rule they are intended to test.
        if task["origin"] == "addition":
            task["dependency_revisions"]["added"].append({"task_id": parent, "reason": "negative control"})

    def test_full_proposal_preserves_baseline_and_covers_papers_hypotheses(self):
        result = checker.validate(*self.arguments)
        self.assertEqual((result["work_packages"], result["source_steps_preserved"], result["paper_boundaries_covered"],
                          result["hypotheses_covered"]), (104, 72, 16, 12))
        self.assertEqual(result["native_registration"], "NOT_VERIFIED")

    def test_frozen_source_reference_refuses_coordinated_relabeling(self):
        # A coherent graph and correct step blob do not authenticate a rewritten
        # repository, commit, branch or path used in reader/source links.
        for field, forged in (("head", "0" * 40),
                              ("repository", "Other/relabelled-research"),
                              ("branch", "forged/other-source"),
                              ("step_path", "roadmap/coordinated-work/plan/other.json"),
                              ("source_status", "published")):
            with self.subTest(source_field=field):
                self.graph = deepcopy(self.arguments[0])
                self.graph["source"][field] = forged
                self.reject("source identity drift from frozen reference")

    def test_source_pin_rejects_boolean_aliases_and_unknown_fields(self):
        # Python numeric equality must not replace the frozen reference types.
        for field, forged in (("pull_request", True), ("source_task_count", True),
                              ("pull_request", 125.0), ("source_task_count", 72.0),
                              ("pull_request", 126), ("source_task_count", 73)):
            with self.subTest(source_field=field, forged=forged):
                self.graph = deepcopy(self.arguments[0])
                self.graph["source"][field] = forged
                self.reject("source identity drift from frozen reference")
        self.graph = deepcopy(self.arguments[0])
        self.graph["source"]["native_registration"] = "complete"
        self.reject("source identity drift from frozen reference")
        self.graph = deepcopy(self.arguments[0])
        del self.graph["source"]["branch"]
        self.reject("source identity drift from frozen reference")

    def test_frozen_source_blob_refuses_coordinated_baseline_rewrite(self):
        # A digest matching mutable local bytes is not the original Git object.
        # Keep source metadata/topology coherent while rewriting one frozen title.
        baseline = deepcopy(self.arguments[1])
        row = next(row for row in baseline if row["id"] == "A01")
        row["title"] += " [synthetic rewritten baseline]"
        self.task("CW-A01")["title"] = row["title"]
        raw = (json.dumps(baseline, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        forged_blob = checker.git_blob(raw)
        self.assertNotEqual(forged_blob, self.arguments[0]["source"]["step_blob"])
        self.graph["source"]["step_blob"] = forged_blob
        imported = [task for task in self.graph["tasks"] if task["origin"] == "imported"]
        self.assertEqual(len(imported), 72)
        for task in imported:
            task["source_blob"] = forged_blob
        with self.assertRaisesRegex(checker.InvalidProgramme, "source identity drift from frozen reference"):
            checker.validate(self.graph, baseline, raw, *self.arguments[3:])

    def test_coordinated_output_relabel_is_refused_even_when_all_consumers_follow(self):
        owner = "CW-A01"
        task = self.task(owner)
        original = task["outputs"][0]["id"]
        forged = "CW-OTHER-PAPER.O999"
        task["outputs"][0]["id"] = forged
        rewritten = 0
        for consumer in self.graph["tasks"]:
            for edge in consumer["dependencies"]:
                for index, consumed in enumerate(edge["consumes"]):
                    if consumed == original:
                        edge["consumes"][index] = forged
                        rewritten += 1
        for paper in self.graph["paper_release_contracts"]:
            for gate in paper["required_gates"]:
                for index, consumed in enumerate(gate["consumes"]):
                    if consumed == original:
                        gate["consumes"][index] = forged
                        rewritten += 1
        self.assertGreater(rewritten, 0, "must mutate an actual consumer")
        self.reject("output owner identity mismatch: CW-A01")

    def test_output_identity_requires_contiguous_task_local_numbering(self):
        self.task("CW-A01")["outputs"][0]["id"] = "CW-A01.O0"
        self.reject("output owner identity mismatch: CW-A01")

    def test_two_output_owners_cannot_share_the_same_proposed_path(self):
        first = self.task("CW-A01")["outputs"][0]["proposed_path"]
        self.task("CW-A02")["outputs"][0]["proposed_path"] = first
        self.reject("duplicate proposed output path: CW-A02/CW-A02.O1")

    def test_lexically_equivalent_output_paths_cannot_alias(self):
        first = self.task("CW-A01")["outputs"][0]["proposed_path"]
        self.task("CW-A02")["outputs"][0]["proposed_path"] = "./" + first
        self.reject("duplicate proposed output path: CW-A02/CW-A02.O1")

    def test_repeated_separators_and_dot_components_cannot_alias_an_output(self):
        first = self.task("CW-A01")["outputs"][0]["proposed_path"]
        for alias in (first.replace("/", "//", 1), first.replace("/", "/./", 1), first + "/"):
            with self.subTest(path=alias):
                self.graph = deepcopy(self.arguments[0])
                self.task("CW-A02")["outputs"][0]["proposed_path"] = alias
                self.reject("duplicate proposed output path: CW-A02/CW-A02.O1")

    def test_output_file_directory_overlap_is_refused_in_either_order(self):
        for paths in (("results/a.md", "results/a.md/child.md"),
                      ("results/a.md/child.md", "results/a.md")):
            with self.subTest(paths=paths):
                self.graph = deepcopy(self.arguments[0])
                for key, path in zip(("CW-A01", "CW-A02"), paths):
                    self.task(key)["outputs"][0]["proposed_path"] = path
                self.reject("overlapping proposed output paths: CW-A02/CW-A02.O1")

    def test_output_destinations_require_safe_relative_file_paths(self):
        for path in (None, 0, "", ".", "   ", "/absolute.md", "../escape.md",
                     "results/../escape.md", "results\\name.md", "C:relative.md",
                     "results/nu\x00l.md", "results/new\nline.md", "results/del\x7f.md"):
            with self.subTest(path=path):
                self.graph = deepcopy(self.arguments[0])
                self.task("CW-A01")["outputs"][0]["proposed_path"] = path
                self.reject("unsafe proposed output path")

    def test_unique_paths_still_require_canonical_spelling(self):
        for path in ("./results/new.md", "results//new.md", "results/./new.md", "results/new.md/"):
            with self.subTest(path=path):
                self.graph = deepcopy(self.arguments[0])
                self.task("CW-A01")["outputs"][0]["proposed_path"] = path
                self.reject("noncanonical proposed output path")

    def test_distinct_output_paths_allow_shared_parents_and_character_prefixes(self):
        for paths in (("results/a.md", "results/a.md-extra"),
                      ("results/one/a.md", "results/two/a.md"),
                      ("different-root/a.md", "results/a.md")):
            with self.subTest(paths=paths):
                self.graph = deepcopy(self.arguments[0])
                for key, path in zip(("CW-A01", "CW-A02"), paths):
                    self.task(key)["outputs"][0]["proposed_path"] = path
                result = checker.validate(self.graph, *self.arguments[1:])
                self.assertEqual(result["work_packages"], 104)

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

    def test_all_addition_removed_ledgers_refuse_phantom_edges(self):
        # Includes the independent reviewer's exact root-package counterexample.
        for number in range(1, 33):
            key = f"CW-N{number:02}"
            with self.subTest(task=key):
                self.graph = deepcopy(self.arguments[0])
                self.task(key)["dependency_revisions"]["removed"] = [
                    {"task_id": "CW-ZZ99", "reason": "independent reviewer counterexample"}]
                self.reject(f"revision removed differs from frozen-to-proposed edge delta: {key}")

    def test_all_addition_added_ledgers_match_actual_dependencies(self):
        for number in range(1, 33):
            key = f"CW-N{number:02}"
            with self.subTest(task=key):
                self.graph = deepcopy(self.arguments[0])
                entries = self.task(key)["dependency_revisions"]["added"]
                if entries:
                    entries.pop()
                else:
                    entries.append({"task_id": "CW-ZZ99", "reason": "phantom prerequisite"})
                self.reject(f"revision added differs from frozen-to-proposed edge delta: {key}")

    def test_addition_forged_added_edge_is_refused(self):
        self.task("CW-N28")["dependency_revisions"]["added"][-1]["task_id"] = "CW-I04"
        self.reject("revision added differs from frozen-to-proposed edge delta: CW-N28")

    def test_addition_duplicate_added_edge_is_refused(self):
        entries = self.task("CW-N02")["dependency_revisions"]["added"]
        entries.append(deepcopy(entries[0]))
        self.reject("duplicate revision added edge: CW-N02")

    def test_addition_blank_edge_reason_is_refused(self):
        self.task("CW-N02")["dependency_revisions"]["added"][0]["reason"] = "   "
        self.reject("revision added edge lacks identity or reason: CW-N02")

    def test_addition_malformed_ledger_is_refused(self):
        for value in (None, {}, {"removed": [], "added": [], "proposal_corrections": {}},
                      {"removed": {}, "added": []}, {"removed": [], "added": {}}):
            with self.subTest(value=value):
                self.graph = deepcopy(self.arguments[0])
                self.task("CW-N01")["dependency_revisions"] = value
                self.reject("ledger missing or malformed|revision (removed|added) must be an array")

    def test_addition_blank_general_revision_reason_is_refused(self):
        self.task("CW-N01")["dependency_revision_reason"] = ""
        self.reject("blank dependency revision rationale: CW-N01")

    def test_unknown_origin_cannot_bypass_revision_validation(self):
        self.task("CW-N01")["origin"] = "unchecked"
        self.reject("unknown task origin: CW-N01")

    def test_addition_cannot_forge_a_frozen_source_baseline(self):
        for field, value in (("source_step_id", "A01"), ("source_dependencies", ["A01"])):
            with self.subTest(field=field):
                self.graph = deepcopy(self.arguments[0])
                self.task("CW-N01")[field] = value
                self.reject("addition claims a frozen source baseline: CW-N01")

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
        # Keep the altered provenance ledger coherent, so this test reaches
        # the independent forbidden-serialization condition.
        revisions = self.task("CW-H03")["dependency_revisions"]
        revisions["removed"] = [e for e in revisions["removed"] if e["task_id"] != "CW-H02"]
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
        # This mutation tests the H08 protected gate, not the separate
        # frozen-source dependency revision ledger.
        revision = self.task("CW-H08")["dependency_revisions"]
        revision["added"] = [e for e in revision["added"] if e["task_id"] != "CW-N29"]
        self.refresh_metrics()
        self.reject("required evidence gate removed")

    def test_model_validity_cannot_precede_any_actual_domain_stand(self):
        for domain in ("CW-H02", "CW-H03", "CW-H04"):
            with self.subTest(domain=domain):
                self.graph = deepcopy(self.arguments[0])
                validity = self.task("CW-N18")
                validity["dependencies"] = [d for d in validity["dependencies"] if d["task_id"] != domain]
                revision = validity["dependency_revisions"]
                revision["added"] = [d for d in revision["added"] if d["task_id"] != domain]
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
        self.reject("paper frozen source identity mismatch")

    def test_paper_source_text_mismatch_still_reaches_source_boundary_check(self):
        # Preserve the old textual-provenance refusal as a separate oracle.
        self.graph["papers"][0]["source_main_question"] = "synthetic unrelated question"
        self.reject("source paper boundary altered")

    def test_full_paper_source_row_swap_cannot_relabel_paper_identity(self):
        a, b = self.graph["papers"][:2]
        for field in ("source_index", "source_title", "source_main_question",
                      "source_engineering_companion"):
            a[field], b[field] = b[field], a[field]
        # Each record still matches some real frozen row, but the paper IDs
        # must not silently point to the other manuscript.
        self.reject("paper frozen source identity mismatch")

    def test_full_hypothesis_source_row_swap_cannot_relabel_hypothesis(self):
        a, b = self.graph["hypotheses"][:2]
        for field in ("source_number", "source_statement", "source_comparison", "source_refutation"):
            a[field], b[field] = b[field], a[field]
        self.reject("hypothesis frozen source identity mismatch")

    def test_out_of_range_paper_source_row_is_typed_refusal(self):
        for number in (0, 17):
            with self.subTest(source_index=number):
                self.graph = deepcopy(self.arguments[0])
                paper = self.graph["papers"][0]
                paper.update(id=f"CW-P{number:02d}", source_index=number)
                self.reject("paper frozen source identity mismatch")

    def test_out_of_range_hypothesis_source_row_is_typed_refusal(self):
        for number in (0, 13):
            with self.subTest(source_number=number):
                self.graph = deepcopy(self.arguments[0])
                hypothesis = self.graph["hypotheses"][0]
                hypothesis.update(id=f"CW-HYP{number:02d}", source_number=number)
                self.reject("hypothesis frozen source identity mismatch")

    def test_paper_index_requires_exact_int_not_a_subclass(self):
        # Mutant control: isinstance(value, int) would accept bool and int subclasses.
        class IntSubclass(int):
            pass
        for value in (True, IntSubclass(1)):
            with self.subTest(source_index_type=type(value).__name__):
                self.graph = deepcopy(self.arguments[0])
                self.graph["papers"][0]["source_index"] = value
                self.reject("paper frozen source identity mismatch")

    def test_hypothesis_number_requires_exact_int_not_a_subclass(self):
        # Same guard must hold independently for the hypothesis source table.
        class IntSubclass(int):
            pass
        for value in (True, IntSubclass(1)):
            with self.subTest(source_number_type=type(value).__name__):
                self.graph = deepcopy(self.arguments[0])
                self.graph["hypotheses"][0]["source_number"] = value
                self.reject("hypothesis frozen source identity mismatch")

    def test_all_16_claim_scopes_refuse_nfkc_compatibility_aliases(self):
        # Kill a future NFKC-before-equality mutant, not a semantic claim.
        for paper_id, pinned in checker.PAPER_CLAIM_SCOPES.items():
            with self.subTest(paper_id=paper_id):
                index = next(i for i, ch in enumerate(pinned) if "A" <= ch <= "Z" or "a" <= ch <= "z")
                alias = pinned[:index] + chr(ord(pinned[index]) + 0xFEE0) + pinned[index + 1:]
                self.assertNotEqual(alias, pinned)
                self.assertEqual(unicodedata.normalize("NFKC", alias), pinned)
                graph = deepcopy(self.graph)
                contract = next(c for c in graph["paper_release_contracts"] if c["paper_id"] == paper_id)
                contract["claim_scope"] = alias
                with self.assertRaisesRegex(checker.InvalidProgramme,
                                            "paper release claim scope changed without reviewed revision: " + paper_id):
                    checker.validate(graph, *self.arguments[1:])

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

    def test_domain_model_cannot_silently_escalate_to_organizational_effect(self):
        contract = next(c for c in self.graph["paper_release_contracts"] if c["paper_id"] == "CW-P02")
        self.assertNotIn("CW-H08", {g["task_id"] for g in contract["required_gates"]})
        contract["claim_class"] = "organizational_effect"
        contract["claim_scope"] = "Measured organizational productivity improvement."
        self.reject("paper release claim class changed without reviewed revision: CW-P02")

    def test_review_paper_cannot_silently_claim_organizational_effect(self):
        contract = next(c for c in self.graph["paper_release_contracts"] if c["paper_id"] == "CW-P01")
        contract["claim_class"] = "organizational_effect"
        contract["claim_scope"] = "Unrestricted universal organizational productivity effect."
        self.reject("paper release claim class changed without reviewed revision: CW-P01")

    def test_p02_scope_escalation_refused_with_unchanged_class(self):
        contract = next(c for c in self.graph["paper_release_contracts"] if c["paper_id"] == "CW-P02")
        self.assertEqual(contract["claim_class"], "domain_model")
        contract["claim_scope"] = "Certified causal productivity increase of 99% in all workplaces."
        self.reject("paper release claim scope changed without reviewed revision: CW-P02")

    def test_p01_scope_escalation_refused_with_unchanged_class(self):
        contract = next(c for c in self.graph["paper_release_contracts"] if c["paper_id"] == "CW-P01")
        self.assertEqual(contract["claim_class"], "review")
        contract["claim_scope"] = "This literature review proves universal real-world profit gains."
        self.reject("paper release claim scope changed without reviewed revision: CW-P01")

    def test_all_16_declared_scope_pins_match_frozen_graph(self):
        actual = {c["paper_id"]: c["claim_scope"] for c in self.graph["paper_release_contracts"]}
        self.assertEqual(actual, checker.PAPER_CLAIM_SCOPES)

    def test_all_16_scope_pins_refuse_case_and_outer_whitespace_aliases(self):
        # Exact source identity must not silently become strip/casefold equality.
        for paper_id, pinned in checker.PAPER_CLAIM_SCOPES.items():
            for mutation, changed in (
                ("case", pinned.swapcase()),
                ("outer_whitespace", " " + pinned + " "),
            ):
                with self.subTest(paper_id=paper_id, mutation=mutation):
                    self.assertNotEqual(changed, pinned)
                    graph = deepcopy(self.graph)
                    contract = next(c for c in graph["paper_release_contracts"]
                                    if c["paper_id"] == paper_id)
                    contract["claim_scope"] = changed
                    with self.assertRaisesRegex(
                        checker.InvalidProgramme,
                        "paper release claim scope changed without reviewed revision: " + paper_id,
                    ):
                        checker.validate(graph, *self.arguments[1:])

    def test_unknown_field_effect_alias_cannot_bypass_claim_class_guard(self):
        contract = next(c for c in self.graph["paper_release_contracts"] if c["paper_id"] == "CW-P02")
        contract["claim_class"] = "proven_benefit"
        self.reject("paper release claim class changed without reviewed revision: CW-P02")

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

    def test_transitive_generic_ancestor_cannot_replace_p01_direct_evidence_gate(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P01")
        manuscript = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I03")
        manuscript["dependencies"] = [edge for edge in manuscript["dependencies"]
                                      if edge["node_id"] != "CW-A01"]
        # A01 is still upstream through I01/A08/A07/A06/A02, but the
        # paper-specific requires_evidence edge was deliberately removed.
        with self.assertRaisesRegex(checker.InvalidProgramme,
                                    "required direct release evidence edge missing or mistyped: CW-P01/CW-A01"):
            checker.validate_release_instances(self.graph, instances)

    def test_retyped_p01_evidence_gate_cannot_pass_as_generic_dependency(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P01")
        manuscript = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I03")
        next(edge for edge in manuscript["dependencies"] if edge["node_id"] == "CW-A01")["type"] = "depends_on"
        with self.assertRaisesRegex(checker.InvalidProgramme,
                                    "required direct release evidence edge missing or mistyped: CW-P01/CW-A01"):
            checker.validate_release_instances(self.graph, instances)

    def test_p16_direct_template_overlap_is_still_a_valid_release_gate(self):
        instances = self.release_instances()
        release = next(r for r in instances if r["paper_id"] == "CW-P16")
        manuscript = next(n for n in release["nodes"] if n["template_task_id"] == "CW-I03")
        edge = next(e for e in manuscript["dependencies"] if e["node_id"] == "CW-I02")
        self.assertEqual((edge["type"], edge["consumes"]), ("depends_on", ["CW-I02.O1"]))
        self.assertEqual(checker.validate_release_instances(self.graph, instances)["contracts"], 16)

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

    def test_review_release_refuses_unreviewed_added_field_gate(self):
        instances = self.release_instances()
        paper = next(r for r in instances if r["paper_id"] == "CW-P01")
        release = next(n for n in paper["nodes"] if n["template_task_id"] == "CW-I08")
        release["dependencies"].append({
            "node_id": "CW-H08", "type": "depends_on", "consumes": ["CW-H08.O1"],
            "reason": "synthetic unrelated field intervention gate",
        })
        with self.assertRaisesRegex(checker.InvalidProgramme, "release edge provenance differs"):
            checker.validate_release_instances(self.graph, instances)

    def test_release_edge_rationale_cannot_change_without_source_revision(self):
        instances = self.release_instances()
        paper = next(r for r in instances if r["paper_id"] == "CW-P01")
        freeze = next(n for n in paper["nodes"] if n["template_task_id"] == "CW-I04")
        freeze["dependencies"][0]["reason"] = "synthetic unreviewed rationale"
        with self.assertRaisesRegex(checker.InvalidProgramme, "release edge provenance differs"):
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
        task["dependency_revisions"]["added"][-1]["task_id"] = "CW-I04"
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
