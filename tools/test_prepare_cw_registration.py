#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Synthetic controls for the offline CW registrar; no real task UUIDs or API calls."""
import copy
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).with_name("prepare_cw_registration.py")
SPEC = importlib.util.spec_from_file_location("cw_registration", TOOL)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

DIGEST = "a" * 64
SOURCE = "b" * 40


def fixture():
    ac = [{"number": 1, "text": "Record the scoped output and its negative control."}]
    tasks = []
    for key in ("CW-A01", "CW-A02"):
        tasks.append({
            "id": key, "epic_id": "CW-E00", "title": "Synthetic task " + key,
            "status": "proposed", "external_task_id": None, "execution_assigned": False,
            "proposed_owner_role": "KC-Brain", "proposed_executor_role": "KC-SWE",
            "outputs": [{"id": key + ".O1", "description": "Synthetic output", "kind": "test"}],
            "acceptance_criteria": copy.deepcopy(ac), "dependencies": [],
            "negative_controls": ["Synthetic negative case"], "evidence_required": ["Synthetic receipt"],
        })
    tasks[1]["dependencies"] = [{"task_id": "CW-A01", "consumes": ["CW-A01.O1"], "reason": "Consumes the first output."}]
    graph = {
        "programme_id": "KC-CW-SYNTHETIC", "title": "Synthetic programme",
        "description": "Synthetic authored programme scope.",
        "proposed_owner_role": "KC-Brain", "proposed_executor_role": "KC-SWE",
        "acceptance_criteria": copy.deepcopy(ac),
        "epics": [{"id": "CW-E00", "title": "Synthetic epic", "description": "Synthetic only.",
                   "proposed_owner_role": "KC-Brain", "proposed_executor_role": "KC-SWE",
                   "task_ids": ["CW-A01", "CW-A02"], "acceptance_criteria": copy.deepcopy(ac)}],
        "tasks": tasks,
    }
    return graph


def recorded_fixture(graph):
    plan = M.prepare(graph, DIGEST, SOURCE)
    bindings = plan["bindings_template"]
    bindings["inventories"] = [{"project_uuid": M.PROJECT_UUID, "coverage": "complete_project_index",
                               "observed_at": "2026-11-18T00:00:00Z", "evidence_ref": "urn:synthetic:inventory"}]
    for role, data in bindings["roles"].items():
        data.update(native_id="synthetic-native-" + role, evidence_ref="urn:synthetic:role:" + role)
    by_key = {}
    for number, row in enumerate(bindings["items"], 1):
        # Explicitly synthetic fixture identifiers; never used in request handoffs.
        row.update(task_uuid=f"10000000-0000-4000-8000-{number:012d}", decision="create",
                   reconciliation_evidence_ref="urn:synthetic:reconcile:" + row["proposal_id"])
        by_key[row["proposal_id"]] = row
    programme, nodes, _, edges, _ = M.normalize_graph(graph)
    snapshot = {"schema": M.READBACK_SCHEMA, "programme_id": programme, "graph_sha256": DIGEST,
                "source_commit": SOURCE, "observed_at": "2026-11-18T00:01:00Z", "tasks": [], "dependencies": []}
    for key, node in nodes.items():
        row = by_key[key]
        snapshot["tasks"].append({
            "proposal_id": key, "task_uuid": row["task_uuid"], "project_uuid": row["project_uuid"],
            "parent_uuid": by_key[node["parent"]]["task_uuid"] if node["parent"] else None,
            "owner_role": node["proposed_owner_role"], "executor_role": node["proposed_executor_role"],
            "owner_native_id": bindings["roles"][node["proposed_owner_role"]]["native_id"],
            "executor_native_id": bindings["roles"][node["proposed_executor_role"]]["native_id"],
            "task_evidence_ref": "urn:synthetic:task", "owner_evidence_ref": "urn:synthetic:owner",
            "assignees_evidence_ref": "urn:synthetic:assignees", "readiness_evidence_ref": "urn:synthetic:readiness",
            "scope_record_type": "description", "scope_evidence_ref": "urn:synthetic:scope",
            "scope_record_sha256": hashlib.sha256(M.description(node, DIGEST, SOURCE).encode("utf-8")).hexdigest(),
        })
    for edge in edges:
        snapshot["dependencies"].append({"from_uuid": by_key[edge["from_proposal_id"]]["task_uuid"],
                                        "to_uuid": by_key[edge["to_proposal_id"]]["task_uuid"],
                                        "type": "depends_on", "evidence_ref": "urn:synthetic:edge"})
    return bindings, snapshot


class RegistrationControls(unittest.TestCase):
    def setUp(self):
        self.graph = fixture()
        self.bindings, self.snapshot = recorded_fixture(self.graph)

    def verify(self):
        return M.verify_readback(self.graph, DIGEST, SOURCE, self.bindings, self.snapshot)

    def test_unbound_graph_produces_templates_not_registration_claim(self):
        # Generic imported/synthetic mode does not promise full CW output fields.
        for task in self.graph["tasks"]:
            self.assertNotIn("proposed_path", task["outputs"][0])
            self.assertNotIn("created", task["outputs"][0])
        plan = M.prepare(self.graph, DIGEST)
        self.assertEqual(plan["actual_uuid_bindings_supplied"], 0)
        self.assertEqual(len(plan["create_requests"]), 4)
        self.assertTrue(all(not action["recorded_prerequisites_complete"] for action in plan["create_requests"]))
        self.assertEqual(plan["create_requests"][0]["proposal_id"], "KC-CW-SYNTHETIC")
        self.assertEqual(plan["dependency_requests"][0]["from_proposal_id"], "CW-A02")
        self.assertEqual(plan["dependency_requests"][0]["to_proposal_id"], "CW-A01")
        self.assertNotIn("ownerId", plan["create_requests"][0]["body_template"])

    def test_generic_unhashable_task_id_is_a_typed_refusal(self):
        for invalid_id in ([], {}):
            with self.subTest(task_id=invalid_id):
                graph = copy.deepcopy(self.graph)
                graph["tasks"][0]["id"] = invalid_id
                with self.assertRaisesRegex(M.Invalid, "task id: expected a nonblank trimmed string"):
                    M.prepare(graph, DIGEST, SOURCE)

    def test_consistent_snapshot_has_sanitized_public_receipt(self):
        public = self.verify()
        self.assertEqual(public["registration_snapshot"], "OFFLINE_CONSISTENT")
        self.assertEqual(public["execution_status"], "NOT_INFERRED")
        encoded = json.dumps(public)
        for item in self.bindings["items"]:
            self.assertNotIn(item["task_uuid"], encoded)
        self.assertNotIn("urn:synthetic", encoded)
        self.assertNotIn("synthetic-native-", encoded)
        self.assertEqual(public["matched_blocking_dependencies"], 1)

    def test_reconciled_binding_omits_duplicate_create(self):
        plan = M.prepare(self.graph, DIGEST, SOURCE, self.bindings)
        self.assertEqual(plan["create_requests"], [])

    def test_unknown_outcome_never_becomes_repost_candidate(self):
        plan = M.prepare(self.graph, DIGEST, SOURCE)
        binding = plan["bindings_template"]
        binding["items"][0]["decision"] = "unknown_outcome"
        after = M.prepare(self.graph, DIGEST, SOURCE, binding)
        self.assertIn("unknown_outcome_do_not_repost", after["create_requests"][0]["holds"])

    def test_own_task_listing_cannot_prove_complete_inventory(self):
        self.bindings["inventories"][0]["coverage"] = "own_tasks_only"
        with self.assertRaisesRegex(M.Invalid, "authoritative inventories"):
            self.verify()

    def test_unknown_outcome_with_unconfirmed_uuid_rejected(self):
        self.bindings["items"][0]["decision"] = "unknown_outcome"
        with self.assertRaisesRegex(M.Invalid, "unknown outcome"):
            self.verify()

    def test_unresolved_mapping_cannot_make_public_receipt(self):
        self.bindings["items"][0].update(task_uuid=None, decision="unresolved")
        with self.assertRaisesRegex(M.Invalid, "every actual UUID"):
            self.verify()

    def test_uuid_alias_cannot_collapse_two_proposal_scopes(self):
        self.bindings["items"][1]["task_uuid"] = self.bindings["items"][0]["task_uuid"]
        with self.assertRaisesRegex(M.Invalid, "multiple proposal scopes"):
            self.verify()

    def test_parent_readback_mismatch(self):
        self.snapshot["tasks"][-1]["parent_uuid"] = None
        with self.assertRaisesRegex(M.Invalid, "parent mismatch"):
            self.verify()

    def test_reused_native_parent_can_be_preserved_with_explicit_link(self):
        row = self.bindings["items"][-1]
        row.update(decision="reuse", parent_mode="reference_only", preserved_parent_uuid=None,
                   logical_parent_evidence_ref="urn:synthetic:parent-mapping")
        self.snapshot["tasks"][-1]["parent_uuid"] = None
        public = self.verify()
        self.assertEqual(public["reference_only_parent_bindings"], 1)

    def test_parent_reference_without_evidence_rejected(self):
        row = self.bindings["items"][-1]
        row.update(decision="reuse", parent_mode="reference_only")
        with self.assertRaisesRegex(M.Invalid, "logical parent evidence"):
            self.verify()

    def test_owner_role_mismatch(self):
        self.snapshot["tasks"][-1]["owner_role"] = "Agent-Brain"
        with self.assertRaisesRegex(M.Invalid, "owner role mismatch"):
            self.verify()

    def test_executor_identity_mismatch(self):
        self.snapshot["tasks"][-1]["executor_native_id"] = "synthetic-different-agent"
        with self.assertRaisesRegex(M.Invalid, "executor native identity"):
            self.verify()

    def test_stale_source_commit_rejected(self):
        self.snapshot["source_commit"] = "c" * 40
        with self.assertRaisesRegex(M.Invalid, "source_commit mismatch"):
            self.verify()

    def test_different_native_acceptance_scope_rejected(self):
        self.snapshot["tasks"][-1]["scope_record_sha256"] = "e" * 64
        with self.assertRaisesRegex(M.Invalid, "scope record digest mismatch"):
            self.verify()

    def test_reused_task_can_bind_versioned_native_content(self):
        self.bindings["items"][-1].update(decision="reuse", scope_record_type="content")
        self.snapshot["tasks"][-1]["scope_record_type"] = "content"
        self.verify()

    def test_epic_and_work_package_id_collision_rejected(self):
        self.graph["epics"][0]["id"] = "CW-A01"
        for item in self.graph["tasks"]:
            item["epic_id"] = "CW-A01"
        with self.assertRaisesRegex(M.Invalid, "duplicate proposal id"):
            M.prepare(self.graph, DIGEST)

    def test_changed_graph_bytes_rejected(self):
        self.bindings["graph_sha256"] = "d" * 64
        with self.assertRaisesRegex(M.Invalid, "graph_sha256"):
            self.verify()

    def test_reversed_dependency_not_accepted(self):
        edge = self.snapshot["dependencies"][0]
        edge["from_uuid"], edge["to_uuid"] = edge["to_uuid"], edge["from_uuid"]
        with self.assertRaisesRegex(M.Invalid, "dependency mismatch"):
            self.verify()

    def test_missing_dependency_not_accepted(self):
        self.snapshot["dependencies"] = []
        with self.assertRaisesRegex(M.Invalid, "dependency mismatch"):
            self.verify()

    def test_advisory_link_does_not_satisfy_blocker(self):
        self.snapshot["dependencies"][0]["type"] = "related_to"
        with self.assertRaisesRegex(M.Invalid, "dependency mismatch"):
            self.verify()

    def test_unmodelled_external_blocker_is_not_silently_ignored(self):
        self.snapshot["dependencies"].append({"from_uuid": self.snapshot["tasks"][-1]["task_uuid"],
            "to_uuid": "10000000-0000-4000-8000-999999999999", "type": "depends_on", "evidence_ref": "urn:synthetic:extra"})
        with self.assertRaisesRegex(M.Invalid, "unexpected"):
            self.verify()

    def test_duplicate_blocking_readback_rejected(self):
        self.snapshot["dependencies"].append(copy.deepcopy(self.snapshot["dependencies"][0]))
        with self.assertRaisesRegex(M.Invalid, "duplicate native blocking"):
            self.verify()

    def test_claimed_native_state_in_proposal_rejected(self):
        self.graph["tasks"][0]["execution_assigned"] = True
        with self.assertRaisesRegex(M.Invalid, "proposed state"):
            M.prepare(self.graph, DIGEST)

    def test_missing_consumed_output_rejected(self):
        self.graph["tasks"][1]["dependencies"][0]["consumes"] = ["CW-A01.DOES-NOT-EXIST"]
        with self.assertRaisesRegex(M.Invalid, "consumed outputs"):
            M.prepare(self.graph, DIGEST)

    def test_cycle_rejected(self):
        self.graph["tasks"][0]["dependencies"] = [{"task_id": "CW-A02", "consumes": ["CW-A02.O1"], "reason": "Synthetic cycle."}]
        with self.assertRaisesRegex(M.Invalid, "cycle"):
            M.prepare(self.graph, DIGEST)

    def test_epic_ac_cannot_be_silently_invented(self):
        del self.graph["epics"][0]["acceptance_criteria"]
        with self.assertRaisesRegex(M.Invalid, "numbered AC"):
            M.prepare(self.graph, DIGEST)

    def test_duplicate_json_keys_and_nonfinite_number_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for raw in ('{"tasks": [], "tasks": [1]}', '{"score": NaN}'):
                path.write_text(raw)
                with self.assertRaises(M.Invalid):
                    M.load_json(path)

    def test_unicode_surrogate_is_rejected_before_serialization(self):
        self.graph["tasks"][0]["title"] = "bad\ud800"
        with self.assertRaisesRegex(M.Invalid, "surrogate"):
            M.prepare(self.graph, DIGEST)

    def test_empty_bindings_are_not_replaced_with_default(self):
        with self.assertRaisesRegex(M.Invalid, "bindings schema"):
            M.prepare(self.graph, DIGEST, SOURCE, {})

    def test_cli_does_not_overwrite_prior_output(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "graph.json"
            out = Path(temp) / "existing"
            source.write_text(json.dumps(self.graph))
            out.mkdir()
            sentinel = out / "keep.txt"
            sentinel.write_text("preserve")
            with contextlib.redirect_stderr(io.StringIO()):
                result = M.main(["--graph", str(source), "--output", str(out)])
            self.assertEqual(result, 2)
            self.assertEqual(sentinel.read_text(), "preserve")


class PaperReleasePreparationControls(unittest.TestCase):
    def setUp(self):
        path = TOOL.parent.parent / "roadmap/coordinated-work/plan/execution-graph.json"
        self.graph, self.digest = M.load_json(path)

    def test_full_programme_cannot_downgrade_by_removing_schema_and_papers(self):
        # This is the real 104-task programme, not the small synthetic fixture.
        for removed in (("schema", "papers"),
                        ("schema", "papers", "paper_release_contracts",
                         "hypotheses", "source", "paper_release_metrics")):
            with self.subTest(removed=removed):
                graph = copy.deepcopy(self.graph)
                # A malformed full output must never escape its own checker
                # merely because the input stripped two mode selectors.
                next(task for task in graph["tasks"] if task["id"] == "CW-A01")["outputs"][0]["created"] = True
                for key in removed:
                    graph.pop(key, None)
                with self.assertRaisesRegex(M.Invalid, "full-programme profile"):
                    M.prepare(graph, self.digest, SOURCE)

    def test_full_programme_cannot_downgrade_by_also_changing_public_id(self):
        graph = copy.deepcopy(self.graph)
        graph["programme_id"] = "KC-CW-RENAMED"
        for key in ("schema", "papers", "paper_release_contracts",
                    "hypotheses", "source", "paper_release_metrics"):
            graph.pop(key, None)
        with self.assertRaisesRegex(M.Invalid, "full-programme profile"):
            M.prepare(graph, self.digest, SOURCE)

    def test_full_programme_unhashable_task_id_is_a_typed_refusal(self):
        for invalid_id in ([], {}):
            with self.subTest(task_id=invalid_id):
                graph = copy.deepcopy(self.graph)
                graph["tasks"][0]["id"] = invalid_id
                with self.assertRaisesRegex(M.Invalid, "task id: expected a nonblank trimmed string"):
                    M.prepare(graph, self.digest, SOURCE)

    def test_programme_prepares_release_templates_separately_from_native_records(self):
        plan = M.prepare(self.graph, self.digest, SOURCE)
        self.assertEqual((plan["node_count"], plan["task_count"], plan["dependency_count"]), (128, 104, 247))
        self.assertEqual((plan["paper_release_template_count"], plan["paper_release_stage_count"]), (16, 96))
        self.assertEqual(plan["native_release_instances_created"], 0)
        self.assertEqual(len(plan["create_requests"]), 128)
        scope = next(r["text"] for r in plan["required_native_scope_records"] if r["proposal_id"] == "CW-I03")
        self.assertIn("CW-P13", scope)
        self.assertIn("CW-H08", scope)

    def test_registrar_refuses_coordinated_output_owner_relabel(self):
        first = next(t for t in self.graph["tasks"] if t["id"] == "CW-A01")
        original = first["outputs"][0]["id"]
        forged = "CW-OTHER-PAPER.O999"
        first["outputs"][0]["id"] = forged
        rewritten = 0
        for task in self.graph["tasks"]:
            for edge in task["dependencies"]:
                for index, consumed in enumerate(edge["consumes"]):
                    if consumed == original:
                        edge["consumes"][index] = forged
                        rewritten += 1
        for contract in self.graph["paper_release_contracts"]:
            for gate in contract["required_gates"]:
                for index, consumed in enumerate(gate["consumes"]):
                    if consumed == original:
                        gate["consumes"][index] = forged
                        rewritten += 1
        self.assertGreater(rewritten, 0, "must retain coherent actual consumers")
        with self.assertRaisesRegex(M.Invalid, "output owner identity mismatch: CW-A01"):
            M.prepare(self.graph, self.digest, SOURCE)

    def test_registrar_refuses_duplicate_proposed_output_paths(self):
        baseline = copy.deepcopy(self.graph)
        destination = next(t for t in baseline["tasks"] if t["id"] == "CW-A01")["outputs"][0]["proposed_path"]
        for duplicate in (destination, "./" + destination):
            with self.subTest(proposed_path=duplicate):
                self.graph = copy.deepcopy(baseline)
                second = next(t for t in self.graph["tasks"] if t["id"] == "CW-A02")
                second["outputs"][0]["proposed_path"] = duplicate
                with self.assertRaisesRegex(M.Invalid, "duplicate proposed output path: CW-A02/CW-A02.O1"):
                    M.prepare(self.graph, self.digest, SOURCE)

    def test_registrar_refuses_unsafe_full_programme_output_path(self):
        first = next(t for t in self.graph["tasks"] if t["id"] == "CW-A01")
        for unsafe in ("/tmp/output.md", "../output.md"):
            with self.subTest(proposed_path=unsafe):
                first["outputs"][0]["proposed_path"] = unsafe
                with self.assertRaisesRegex(M.Invalid, "unsafe proposed output path"):
                    M.prepare(self.graph, self.digest, SOURCE)

    def test_registrar_refuses_full_programme_output_claimed_created(self):
        first = next(t for t in self.graph["tasks"] if t["id"] == "CW-A01")
        first["outputs"][0]["created"] = True
        with self.assertRaisesRegex(M.Invalid, "future output claimed as created"):
            M.prepare(self.graph, self.digest, SOURCE)

    def test_registrar_refuses_incomplete_full_programme_output_fields(self):
        baseline = copy.deepcopy(self.graph)
        for field, value, message in (
                ("created", None, "future output claimed as created"),
                ("proposed_path", None, "unsafe proposed output path"),
                ("proposed_path", 7, "unsafe proposed output path"),
                ("record", 7, "CW-A01: output record must be an object")):
            with self.subTest(field=field, value=value):
                self.graph = copy.deepcopy(baseline)
                outputs = next(t for t in self.graph["tasks"] if t["id"] == "CW-A01")["outputs"]
                output = outputs[0]
                if field == "record":
                    outputs[0] = value
                elif value is None:
                    del output[field]
                else:
                    output[field] = value
                with self.assertRaisesRegex(M.Invalid, message):
                    M.prepare(self.graph, self.digest, SOURCE)

    def test_registrar_refuses_p13_instance_without_field_gate(self):
        releases = M.programme_checker.instantiate_release_instances(self.graph)
        p13 = next(r for r in releases if r["paper_id"] == "CW-P13")
        p13["nodes"][0]["dependencies"] = [d for d in p13["nodes"][0]["dependencies"] if d["node_id"] != "CW-H08"]
        with self.assertRaisesRegex(M.Invalid, "not upstream: CW-P13/CW-H08"):
            M.prepare(self.graph, self.digest, SOURCE, release_instances=releases)

    def test_registrar_refuses_missing_per_paper_contracts(self):
        del self.graph["paper_release_contracts"]
        with self.assertRaisesRegex(M.Invalid, "required-gate map"):
            M.prepare(self.graph, self.digest, SOURCE)

    def test_registrar_refuses_release_graph_from_another_source(self):
        with tempfile.TemporaryDirectory() as temp:
            graph_path = Path(temp) / "graph.json"
            graph_path.write_text(json.dumps(self.graph, ensure_ascii=False))
            _, digest = M.load_json(graph_path)
            release_path = Path(temp) / "releases.json"
            release_path.write_text(json.dumps({"schema": "CoordinatedWorkReleaseInstances/v1",
                "graph_sha256": digest, "source_commit": "c" * 40,
                "instances": M.programme_checker.instantiate_release_instances(self.graph)}))
            with contextlib.redirect_stderr(io.StringIO()):
                code = M.main(["--graph", str(graph_path), "--source-commit", SOURCE,
                               "--release-instances", str(release_path), "--output", str(Path(temp) / "new")])
            self.assertEqual(code, 2)
            self.assertFalse((Path(temp) / "new").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
