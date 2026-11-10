# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Controls for the isolated RM-04 reconcile harness (synthetic fixtures only)."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.reconcile_workgraph import (
    EDGE_DEPENDS,
    EDGE_RELATED,
    REASON_CONFLICTING_STATUS,
    REASON_DUPLICATE_RM_BINDING,
    REASON_EXCESS_EDGE,
    REASON_EXTERNAL_DEPENDS_ON,
    REASON_MISSING_EDGE,
    REASON_OK,
    REASON_REVERSED_EDGE,
    REASON_UNKNOWN_RM_LABEL,
    REASON_UNBOUND_RM,
    SCHEMA_ID,
    build_synthetic_snapshot_from_definition,
    dumps_deterministic,
    main,
    reconcile,
)

REPO = Path(__file__).resolve().parents[1]
DEFINITION_PATH = REPO / "roadmap" / "dependencies.json"
TOOL = REPO / "tools" / "reconcile_workgraph.py"


def _mini_definition() -> dict:
    """Small synthetic definition: 3 RMs, 2 requires, 1 advisory informs."""
    return {
        "kind": "roadmap-dependencies",
        "revision": "synthetic-test-1",
        "nodes": [
            {"id": "RM-A", "requires": []},
            {"id": "RM-B", "requires": ["RM-A"]},
            {"id": "RM-C", "requires": ["RM-B"], "informs_not_blocks": []},
        ],
        "advisory_links": [
            {"from": "RM-A", "to": "RM-C", "kind": "informs_not_blocks"},
        ],
    }


def _agreeing_mini_snapshot(definition: dict) -> dict:
    return build_synthetic_snapshot_from_definition(definition)


class ReconcileWorkgraphControls(unittest.TestCase):
    def test_positive_real_definition_25_bound_45_requires_4_informs(self):
        definition = json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))
        snapshot = build_synthetic_snapshot_from_definition(definition)
        report = reconcile(definition, snapshot)
        self.assertTrue(report["agreement"])
        self.assertEqual(report["reason_codes"], [REASON_OK])
        self.assertEqual(len(report["bindings"]), 25)
        self.assertEqual(report["definition"]["requires_count"], 45)
        self.assertEqual(report["definition"]["informs_not_blocks_count"], 4)
        self.assertEqual(len(report["edges"]["requires_matched"]), 45)
        self.assertEqual(len(report["edges"]["informs_matched"]), 4)
        self.assertEqual(len(report["edges"]["external"]), 3)
        for edge in report["edges"]["external"]:
            self.assertEqual(edge["type"], EDGE_RELATED)
        self.assertFalse(report["network_calls"])
        self.assertFalse(report["effects_authorized"])

    def test_cli_positive_real_definition_exit_0(self):
        definition = json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))
        snapshot = build_synthetic_snapshot_from_definition(definition)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            snap_path = tmp_path / "snapshot.json"
            out_path = tmp_path / "report.json"
            snap_path.write_text(dumps_deterministic(snapshot), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "--definition",
                        str(DEFINITION_PATH),
                        "--snapshot",
                        str(snap_path),
                        "--output",
                        str(out_path),
                    ]
                )
            self.assertEqual(code, 0)
            report = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertTrue(report["agreement"])
            self.assertEqual(report["reason_codes"], [REASON_OK])

    def test_duplicate_registration_refuses_both(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        # Second task also claims RM-A.
        snapshot["tasks"].append(
            {
                "id": "syn-dup-0001",
                "title": "Duplicate claim",
                "status": "open",
                "rm_label": "RM-A",
            }
        )
        report = reconcile(definition, snapshot)
        self.assertFalse(report["agreement"])
        self.assertIn(REASON_DUPLICATE_RM_BINDING, report["reason_codes"])
        self.assertNotIn("RM-A", report["bindings"])
        detail = next(
            d for d in report["disagreements"] if d["reason_code"] == REASON_DUPLICATE_RM_BINDING
        )
        self.assertEqual(sorted(detail["details"]["task_ids"]), ["syn-0001", "syn-dup-0001"])

    def test_conflicting_status_no_merge(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        snapshot["status_records"] = [
            {"rm_label": "RM-B", "status": "open"},
            {"rm_label": "RM-B", "status": "done"},
        ]
        report = reconcile(definition, snapshot)
        self.assertFalse(report["agreement"])
        self.assertIn(REASON_CONFLICTING_STATUS, report["reason_codes"])
        # Single binding for RM-B remains; statuses are not merged into one value.
        self.assertEqual(report["bindings"].get("RM-B"), "syn-0002")
        detail = next(
            d for d in report["disagreements"] if d["reason_code"] == REASON_CONFLICTING_STATUS
        )
        self.assertEqual(detail["details"]["statuses"], ["done", "open"])
        self.assertIn("not merged", detail["details"]["execution_authority"])

    def test_conflicting_status_via_duplicate_claimants(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        snapshot["tasks"].append(
            {
                "id": "syn-dup-status",
                "title": "Other status claim",
                "status": "blocked",
                "rm_label": "RM-B",
            }
        )
        # Flip original RM-B status so the two claimants disagree.
        for task in snapshot["tasks"]:
            if task["id"] == "syn-0002":
                task["status"] = "open"
        report = reconcile(definition, snapshot)
        self.assertIn(REASON_DUPLICATE_RM_BINDING, report["reason_codes"])
        self.assertIn(REASON_CONFLICTING_STATUS, report["reason_codes"])
        self.assertNotIn("RM-B", report["bindings"])

    def test_reversed_edge_not_matched(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        # Reverse RM-B -> RM-A depends_on into RM-A -> RM-B.
        for edge in snapshot["edges"]:
            if edge["type"] == EDGE_DEPENDS and edge["from"] == "syn-0002" and edge["to"] == "syn-0001":
                edge["from"], edge["to"] = edge["to"], edge["from"]
                break
        report = reconcile(definition, snapshot)
        self.assertFalse(report["agreement"])
        self.assertIn(REASON_REVERSED_EDGE, report["reason_codes"])
        self.assertIn(REASON_MISSING_EDGE, report["reason_codes"])
        self.assertEqual(report["edges"]["requires_matched"], [["RM-C", "RM-B"]])

    def test_missing_and_excess_edges(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        # Drop RM-C -> RM-B depends_on; add excess depends_on RM-C -> RM-A.
        snapshot["edges"] = [
            e
            for e in snapshot["edges"]
            if not (e["type"] == EDGE_DEPENDS and e["from"] == "syn-0003" and e["to"] == "syn-0002")
        ]
        snapshot["edges"].append({"from": "syn-0003", "to": "syn-0001", "type": EDGE_DEPENDS})
        report = reconcile(definition, snapshot)
        self.assertIn(REASON_MISSING_EDGE, report["reason_codes"])
        self.assertIn(REASON_EXCESS_EDGE, report["reason_codes"])
        missing = report["edges"]["missing"]
        self.assertTrue(
            any(
                m.get("dependent_rm") == "RM-C" and m.get("prerequisite_rm") == "RM-B"
                for m in missing
            )
        )
        excess = report["edges"]["excess"]
        self.assertTrue(
            any(
                e.get("dependent_rm") == "RM-C" and e.get("prerequisite_rm") == "RM-A"
                for e in excess
            )
        )

    def test_external_depends_on_not_counted_as_requires(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        # Replace a valid related external with depends_on; also remove internal requires
        # match attempt via external (external must never satisfy requires).
        snapshot["edges"].append(
            {"from": "syn-0002", "to": "syn-ext-0001", "type": EDGE_DEPENDS}
        )
        report = reconcile(definition, snapshot)
        self.assertIn(REASON_EXTERNAL_DEPENDS_ON, report["reason_codes"])
        # Requires matches stay exact for the internal edges that remain.
        self.assertEqual(len(report["edges"]["requires_matched"]), 2)
        self.assertTrue(
            any(e["type"] == EDGE_DEPENDS for e in report["edges"]["external"])
        )

    def test_unknown_rm_label_typed_error(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        snapshot["tasks"].append(
            {
                "id": "syn-unknown",
                "title": "Unknown label",
                "status": "open",
                "rm_label": "RM-ZZ",
            }
        )
        report = reconcile(definition, snapshot)
        self.assertFalse(report["agreement"])
        self.assertIn(REASON_UNKNOWN_RM_LABEL, report["reason_codes"])
        self.assertEqual(report["unknown_rm_labels"][0]["rm_label"], "RM-ZZ")

    def test_unbound_rm_reported(self):
        definition = _mini_definition()
        snapshot = _agreeing_mini_snapshot(definition)
        snapshot["tasks"] = [t for t in snapshot["tasks"] if t.get("rm_label") != "RM-C"]
        # Also drop edges that referenced syn-0003 to avoid malformed endpoints.
        snapshot["edges"] = [
            e for e in snapshot["edges"] if e["from"] != "syn-0003" and e["to"] != "syn-0003"
        ]
        report = reconcile(definition, snapshot)
        self.assertIn(REASON_UNBOUND_RM, report["reason_codes"])
        self.assertIn("RM-C", report["unbound_rms"])
        self.assertNotIn("RM-C", report["bindings"])

    def test_determinism(self):
        definition = json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))
        snapshot = build_synthetic_snapshot_from_definition(definition)
        a = dumps_deterministic(reconcile(definition, snapshot))
        b = dumps_deterministic(reconcile(copy.deepcopy(definition), copy.deepcopy(snapshot)))
        self.assertEqual(a, b)

    def test_subprocess_cli_network_free_stdlib_only(self):
        """Run CLI in a subprocess; tool source must not import network clients."""
        source = TOOL.read_text(encoding="utf-8")
        for banned in (
            "urllib",
            "requests",
            "http.client",
            "httpx",
            "aiohttp",
            "socket",
        ):
            self.assertNotIn(f"import {banned}", source)
            self.assertNotIn(f"from {banned}", source)
        definition = json.loads(DEFINITION_PATH.read_text(encoding="utf-8"))
        snapshot = build_synthetic_snapshot_from_definition(definition)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            snap_path = tmp_path / "snap.json"
            snap_path.write_text(dumps_deterministic(snapshot), encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(TOOL),
                    "--definition",
                    str(DEFINITION_PATH),
                    "--snapshot",
                    str(snap_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            self.assertTrue(report["agreement"])
            self.assertFalse(report["network_calls"])

    def test_schema_constant(self):
        self.assertEqual(SCHEMA_ID, "rm04-tracker-snapshot/1")


if __name__ == "__main__":
    unittest.main()
