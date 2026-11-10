#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Isolated RM-04 workgraph reconciliation harness (synthetic / dry-run only).

Compares a roadmap definition in ``roadmap/dependencies.json`` shape against an
in-memory tracker snapshot. Never contacts Muneral or any tracker API. Never
writes bindings, statuses or edges. Exit non-zero when disagreements exist.

Tracker snapshot schema ``rm04-tracker-snapshot/1``:

- ``tasks``: opaque ``id``, ``title``, ``status``, optional ``rm_label`` binding
  claim (or ``binding`` alias).
- ``edges``: ``from`` = dependent task id, ``to`` = prerequisite task id,
  ``type`` in ``depends_on`` | ``related_to``.

Definition edges:

- node ``requires`` → expected ``depends_on`` (dependent = node, prereq = member).
- node ``informs_not_blocks`` → expected ``related_to`` (same orientation).
- top-level ``advisory_links`` with ``kind: informs_not_blocks`` keep the ordered
  source pair (``from``, ``to``): ``from`` informs ``to`` but does not block
  ``to``. Expected ``related_to`` compares that same ordered pair.

Snapshot option ``related_to_orientation`` (also CLI
``--related-to-orientation``):

- ``ordered``: compare exact from→to; a reverse advisory observation is
  ``reversed_edge``.
- ``unverified`` (default): tracker ``related_to`` orientation is not assumed
  order-preserving. A reverse advisory observation is neither a match nor an
  accepted reversal; it is reported as ``advisory_direction_unverified`` and
  keeps exit non-zero / hold. ``depends_on`` comparisons stay ordered always.
  External ``related_to`` edges stay classified separately.

External edges (an endpoint outside the bound RM task set) are classified
separately and never satisfy a ``requires`` edge. A ``depends_on`` external edge
is a disagreement.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SCHEMA_ID = "rm04-tracker-snapshot/1"
RECORD_TYPE = "rm04-reconcile-report/1"
EDGE_DEPENDS = "depends_on"
EDGE_RELATED = "related_to"
ADVISORY_KIND = "informs_not_blocks"
ORIENTATION_ORDERED = "ordered"
ORIENTATION_UNVERIFIED = "unverified"
RELATED_TO_ORIENTATIONS = frozenset({ORIENTATION_ORDERED, ORIENTATION_UNVERIFIED})

REASON_OK = "agreement"
REASON_DUPLICATE_RM_BINDING = "duplicate_rm_binding"
REASON_CONFLICTING_STATUS = "conflicting_status"
REASON_REVERSED_EDGE = "reversed_edge"
REASON_ADVISORY_DIRECTION_UNVERIFIED = "advisory_direction_unverified"
REASON_MISSING_EDGE = "missing_edge"
REASON_EXCESS_EDGE = "excess_edge"
REASON_EXTERNAL_DEPENDS_ON = "external_depends_on"
REASON_UNKNOWN_RM_LABEL = "unknown_rm_label"
REASON_UNBOUND_RM = "unbound_rm"
REASON_MALFORMED_INPUT = "malformed_input"
REASON_INPUT_ERROR = "input_error"

DISAGREEMENT_REASONS = frozenset(
    {
        REASON_DUPLICATE_RM_BINDING,
        REASON_CONFLICTING_STATUS,
        REASON_REVERSED_EDGE,
        REASON_ADVISORY_DIRECTION_UNVERIFIED,
        REASON_MISSING_EDGE,
        REASON_EXCESS_EDGE,
        REASON_EXTERNAL_DEPENDS_ON,
        REASON_UNKNOWN_RM_LABEL,
        REASON_UNBOUND_RM,
    }
)


class ReconcileError(Exception):
    def __init__(self, reason_code: str, message: str, details: dict | None = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.message = message
        self.details = details or {}


def dumps_deterministic(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReconcileError(REASON_MALFORMED_INPUT, f"{label} must be an object")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ReconcileError(REASON_MALFORMED_INPUT, f"{label} must be an array")
    return value


def _require_str(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ReconcileError(REASON_MALFORMED_INPUT, f"{label} must be a non-empty string")
    return value


def load_definition(data: Any) -> dict[str, Any]:
    doc = _require_mapping(data, "definition")
    nodes = _require_list(doc.get("nodes"), "definition.nodes")
    rm_ids: list[str] = []
    requires: set[tuple[str, str]] = set()
    related: set[tuple[str, str]] = set()
    seen: set[str] = set()
    for i, node in enumerate(nodes):
        n = _require_mapping(node, f"definition.nodes[{i}]")
        rm_id = _require_str(n.get("id"), f"definition.nodes[{i}].id")
        if rm_id in seen:
            raise ReconcileError(
                REASON_MALFORMED_INPUT,
                f"duplicate definition node id {rm_id}",
                {"rm_id": rm_id},
            )
        seen.add(rm_id)
        rm_ids.append(rm_id)
        for prereq in _require_list(n.get("requires", []), f"definition.nodes[{i}].requires"):
            requires.add((rm_id, _require_str(prereq, f"requires entry on {rm_id}")))
        for soft in _require_list(
            n.get("informs_not_blocks", []), f"definition.nodes[{i}].informs_not_blocks"
        ):
            # Same orientation as requires: this node is dependent, listed id is soft prereq.
            related.add((rm_id, _require_str(soft, f"informs_not_blocks entry on {rm_id}")))
    for i, link in enumerate(_require_list(doc.get("advisory_links", []), "advisory_links")):
        item = _require_mapping(link, f"advisory_links[{i}]")
        kind = _require_str(item.get("kind"), f"advisory_links[{i}].kind")
        if kind != ADVISORY_KIND:
            raise ReconcileError(
                REASON_MALFORMED_INPUT,
                f"unsupported advisory kind {kind}",
                {"kind": kind},
            )
        src = _require_str(item.get("from"), f"advisory_links[{i}].from")
        dst = _require_str(item.get("to"), f"advisory_links[{i}].to")
        # from informs to but does not block to — keep ordered source pair (from, to).
        related.add((src, dst))
    rm_set = set(rm_ids)
    for dependent, prereq in requires | related:
        if dependent not in rm_set or prereq not in rm_set:
            raise ReconcileError(
                REASON_MALFORMED_INPUT,
                "definition edge endpoint outside node set",
                {"dependent": dependent, "prerequisite": prereq},
            )
    return {
        "rm_ids": rm_ids,
        "rm_set": rm_set,
        "requires": requires,
        "related": related,
        "revision": doc.get("revision"),
        "raw": doc,
    }


def _task_rm_label(task: dict[str, Any]) -> str | None:
    if "rm_label" in task and task["rm_label"] is not None:
        return _require_str(task["rm_label"], "task.rm_label")
    if "binding" in task and task["binding"] is not None:
        return _require_str(task["binding"], "task.binding")
    return None


def load_snapshot(data: Any) -> dict[str, Any]:
    doc = _require_mapping(data, "snapshot")
    schema = doc.get("schema")
    if schema is not None and schema != SCHEMA_ID:
        raise ReconcileError(
            REASON_MALFORMED_INPUT,
            f"unsupported snapshot schema {schema}",
            {"schema": schema},
        )
    tasks_out: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for i, task in enumerate(_require_list(doc.get("tasks"), "snapshot.tasks")):
        t = _require_mapping(task, f"snapshot.tasks[{i}]")
        tid = _require_str(t.get("id"), f"snapshot.tasks[{i}].id")
        if tid in seen_ids:
            raise ReconcileError(
                REASON_MALFORMED_INPUT,
                f"duplicate task id {tid}",
                {"task_id": tid},
            )
        seen_ids.add(tid)
        title = _require_str(t.get("title"), f"snapshot.tasks[{i}].title")
        status = _require_str(t.get("status"), f"snapshot.tasks[{i}].status")
        tasks_out.append(
            {
                "id": tid,
                "title": title,
                "status": status,
                "rm_label": _task_rm_label(t),
            }
        )
    edges_out: list[dict[str, str]] = []
    for i, edge in enumerate(_require_list(doc.get("edges", []), "snapshot.edges")):
        e = _require_mapping(edge, f"snapshot.edges[{i}]")
        etype = _require_str(e.get("type"), f"snapshot.edges[{i}].type")
        if etype not in {EDGE_DEPENDS, EDGE_RELATED}:
            raise ReconcileError(
                REASON_MALFORMED_INPUT,
                f"unsupported edge type {etype}",
                {"type": etype},
            )
        edges_out.append(
            {
                "from": _require_str(e.get("from"), f"snapshot.edges[{i}].from"),
                "to": _require_str(e.get("to"), f"snapshot.edges[{i}].to"),
                "type": etype,
            }
        )
    orientation_raw = doc.get("related_to_orientation", ORIENTATION_UNVERIFIED)
    orientation = _require_str(orientation_raw, "snapshot.related_to_orientation")
    if orientation not in RELATED_TO_ORIENTATIONS:
        raise ReconcileError(
            REASON_MALFORMED_INPUT,
            f"unsupported related_to_orientation {orientation}",
            {"related_to_orientation": orientation},
        )
    return {
        "tasks": tasks_out,
        "edges": edges_out,
        "related_to_orientation": orientation,
        "raw": doc,
    }


def _sorted_pairs(pairs: set[tuple[str, str]]) -> list[list[str]]:
    return [[a, b] for a, b in sorted(pairs)]


def reconcile(
    definition_data: Any,
    snapshot_data: Any,
    *,
    related_to_orientation: str | None = None,
) -> dict[str, Any]:
    """Pure reconcile. Returns a deterministic report; never mutates inputs."""
    definition = load_definition(definition_data)
    snapshot = load_snapshot(snapshot_data)

    orientation = related_to_orientation or snapshot["related_to_orientation"]
    if orientation not in RELATED_TO_ORIENTATIONS:
        raise ReconcileError(
            REASON_MALFORMED_INPUT,
            f"unsupported related_to_orientation {orientation}",
            {"related_to_orientation": orientation},
        )

    reason_codes: list[str] = []
    disagreements: list[dict[str, Any]] = []

    def add_disagreement(code: str, message: str, **details: Any) -> None:
        if code not in reason_codes:
            reason_codes.append(code)
        disagreements.append({"reason_code": code, "message": message, "details": details})

    claims_by_rm: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unknown_labels: list[dict[str, str]] = []
    statuses_by_rm: dict[str, set[str]] = defaultdict(set)
    for task in snapshot["tasks"]:
        label = task["rm_label"]
        if label is None:
            continue
        if label not in definition["rm_set"]:
            unknown_labels.append({"task_id": task["id"], "rm_label": label})
            add_disagreement(
                REASON_UNKNOWN_RM_LABEL,
                f"snapshot task {task['id']} claims unknown RM label {label}",
                task_id=task["id"],
                rm_label=label,
            )
            continue
        claims_by_rm[label].append(task)
        statuses_by_rm[label].add(task["status"])

    bindings: dict[str, str] = {}
    unbound: list[str] = []
    for rm_id in definition["rm_ids"]:
        claimants = claims_by_rm.get(rm_id, [])
        if not claimants:
            unbound.append(rm_id)
            add_disagreement(
                REASON_UNBOUND_RM,
                f"RM {rm_id} has no binding claim",
                rm_id=rm_id,
            )
            continue
        if len(claimants) > 1:
            ids = [c["id"] for c in claimants]
            add_disagreement(
                REASON_DUPLICATE_RM_BINDING,
                f"RM {rm_id} claimed by multiple tasks; neither binding selected",
                rm_id=rm_id,
                task_ids=ids,
            )
            continue
        bindings[rm_id] = claimants[0]["id"]

    # Union of per-RM task statuses and optional status_records.
    status_records = snapshot["raw"].get("status_records")
    if status_records is not None:
        for i, rec in enumerate(_require_list(status_records, "snapshot.status_records")):
            item = _require_mapping(rec, f"status_records[{i}]")
            rm_id = _require_str(item.get("rm_label"), f"status_records[{i}].rm_label")
            status = _require_str(item.get("status"), f"status_records[{i}].status")
            if rm_id not in definition["rm_set"]:
                add_disagreement(
                    REASON_UNKNOWN_RM_LABEL,
                    f"status record claims unknown RM label {rm_id}",
                    rm_label=rm_id,
                )
                continue
            statuses_by_rm[rm_id].add(status)

    for rm_id, statuses in sorted(statuses_by_rm.items()):
        if len(statuses) > 1:
            add_disagreement(
                REASON_CONFLICTING_STATUS,
                f"RM {rm_id} has conflicting statuses; no status selected",
                rm_id=rm_id,
                statuses=sorted(statuses),
                disagreement_detected=True,
                effects="none",
            )

    bound_task_ids = set(bindings.values())
    task_to_rm = {tid: rm for rm, tid in bindings.items()}

    expected_depends = set(definition["requires"])
    expected_related = set(definition["related"])

    observed_depends: set[tuple[str, str]] = set()
    observed_related: set[tuple[str, str]] = set()
    direction_unverified_pairs: set[tuple[str, str]] = set()
    external_edges: list[dict[str, Any]] = []
    unknown_endpoint_edges: list[dict[str, Any]] = []

    task_ids = {t["id"] for t in snapshot["tasks"]}
    for edge in snapshot["edges"]:
        frm = edge["from"]
        to = edge["to"]
        etype = edge["type"]
        if frm not in task_ids or to not in task_ids:
            unknown_endpoint_edges.append(edge)
            add_disagreement(
                REASON_MALFORMED_INPUT,
                "edge endpoint is not a known task id",
                edge=edge,
            )
            continue
        frm_bound = frm in bound_task_ids
        to_bound = to in bound_task_ids
        if not frm_bound or not to_bound:
            classification = {
                "from": frm,
                "to": to,
                "type": etype,
                "from_bound": frm_bound,
                "to_bound": to_bound,
            }
            external_edges.append(classification)
            if etype == EDGE_DEPENDS:
                add_disagreement(
                    REASON_EXTERNAL_DEPENDS_ON,
                    "external edge typed depends_on; never counted as a requires match",
                    edge=classification,
                )
            continue
        dep_rm = task_to_rm[frm]
        pre_rm = task_to_rm[to]
        pair = (dep_rm, pre_rm)
        rev = (pre_rm, dep_rm)
        if etype == EDGE_DEPENDS:
            # depends_on comparisons are always ordered.
            if pair in expected_depends:
                observed_depends.add(pair)
            elif rev in expected_depends:
                add_disagreement(
                    REASON_REVERSED_EDGE,
                    "depends_on edge is reversed relative to requires",
                    expected_dependent=pre_rm,
                    expected_prerequisite=dep_rm,
                    observed_from=frm,
                    observed_to=to,
                    edge_type=etype,
                )
            else:
                add_disagreement(
                    REASON_EXCESS_EDGE,
                    "depends_on edge has no matching requires",
                    dependent_rm=dep_rm,
                    prerequisite_rm=pre_rm,
                    edge_type=etype,
                )
        else:  # related_to (advisory / informs_not_blocks)
            if pair in expected_related:
                observed_related.add(pair)
            elif rev in expected_related:
                if orientation == ORIENTATION_ORDERED:
                    add_disagreement(
                        REASON_REVERSED_EDGE,
                        "related_to edge is reversed relative to informs_not_blocks",
                        expected_from=pre_rm,
                        expected_to=dep_rm,
                        observed_from=frm,
                        observed_to=to,
                        edge_type=etype,
                        related_to_orientation=orientation,
                    )
                else:
                    # Unverified: neither match nor accepted reversal.
                    direction_unverified_pairs.add(rev)
                    add_disagreement(
                        REASON_ADVISORY_DIRECTION_UNVERIFIED,
                        (
                            "related_to orientation unverified; reversed advisory "
                            "pair is neither matched nor an accepted reversal"
                        ),
                        expected_from=pre_rm,
                        expected_to=dep_rm,
                        observed_from=frm,
                        observed_to=to,
                        edge_type=etype,
                        related_to_orientation=orientation,
                    )
            else:
                add_disagreement(
                    REASON_EXCESS_EDGE,
                    "related_to edge has no matching informs_not_blocks",
                    dependent_rm=dep_rm,
                    prerequisite_rm=pre_rm,
                    edge_type=etype,
                )

    for pair in sorted(expected_depends - observed_depends):
        add_disagreement(
            REASON_MISSING_EDGE,
            "requires edge missing from snapshot depends_on edges",
            dependent_rm=pair[0],
            prerequisite_rm=pair[1],
            edge_type=EDGE_DEPENDS,
        )
    for pair in sorted(expected_related - observed_related):
        if pair in direction_unverified_pairs:
            # Covered by advisory_direction_unverified; do not also count as missing.
            continue
        add_disagreement(
            REASON_MISSING_EDGE,
            "informs_not_blocks edge missing from snapshot related_to edges",
            dependent_rm=pair[0],
            prerequisite_rm=pair[1],
            edge_type=EDGE_RELATED,
        )

    # Stable order for reason codes: disagreement set order of first appearance,
    # already preserved; if none, agreement.
    if not reason_codes:
        reason_codes = [REASON_OK]

    agreement = reason_codes == [REASON_OK]
    disagreement_detected = not agreement
    report = {
        "record_type": RECORD_TYPE,
        "schema": SCHEMA_ID,
        "agreement": agreement,
        "disagreement_detected": disagreement_detected,
        "effects": "none",
        "reason_codes": reason_codes,
        "related_to_orientation": orientation,
        "definition": {
            "revision": definition["revision"],
            "rm_count": len(definition["rm_ids"]),
            "requires_count": len(definition["requires"]),
            "informs_not_blocks_count": len(definition["related"]),
        },
        "bindings": {rm: bindings[rm] for rm in definition["rm_ids"] if rm in bindings},
        "unbound_rms": unbound,
        "unknown_rm_labels": unknown_labels,
        "edges": {
            "requires_matched": _sorted_pairs(observed_depends),
            "informs_matched": _sorted_pairs(observed_related),
            "missing": [
                d["details"]
                for d in disagreements
                if d["reason_code"] == REASON_MISSING_EDGE
            ],
            "excess": [
                d["details"]
                for d in disagreements
                if d["reason_code"] == REASON_EXCESS_EDGE
            ],
            "reversed": [
                d["details"]
                for d in disagreements
                if d["reason_code"] == REASON_REVERSED_EDGE
            ],
            "advisory_direction_unverified": [
                d["details"]
                for d in disagreements
                if d["reason_code"] == REASON_ADVISORY_DIRECTION_UNVERIFIED
            ],
            "external": external_edges,
        },
        "disagreements": disagreements,
        "effects_authorized": False,
        "network_calls": False,
        "notes": (
            "Dry-run / replay only. No tracker write, no Muneral call, "
            "no status merge, no binding repair. effects=none (never a permission). "
            f"related_to_orientation={orientation}."
        ),
    }
    return report


def build_synthetic_snapshot_from_definition(definition_data: Any) -> dict[str, Any]:
    """Build an agreeing synthetic snapshot from a definition (in-memory only)."""
    definition = load_definition(definition_data)
    tasks = []
    rm_to_task: dict[str, str] = {}
    for i, rm_id in enumerate(definition["rm_ids"], start=1):
        tid = f"syn-{i:04d}"
        rm_to_task[rm_id] = tid
        tasks.append(
            {
                "id": tid,
                "title": f"Synthetic binding for {rm_id}",
                "status": "open",
                "rm_label": rm_id,
            }
        )
    # A few unbound external tasks for related_to external edges.
    external_ids = ["syn-ext-0001", "syn-ext-0002", "syn-ext-0003"]
    for eid in external_ids:
        tasks.append(
            {
                "id": eid,
                "title": f"External synthetic task {eid}",
                "status": "open",
            }
        )
    edges: list[dict[str, str]] = []
    for dependent, prereq in sorted(definition["requires"]):
        edges.append(
            {
                "from": rm_to_task[dependent],
                "to": rm_to_task[prereq],
                "type": EDGE_DEPENDS,
            }
        )
    for dependent, prereq in sorted(definition["related"]):
        edges.append(
            {
                "from": rm_to_task[dependent],
                "to": rm_to_task[prereq],
                "type": EDGE_RELATED,
            }
        )
    # External related_to edges from first three bound tasks; never depends_on.
    for tid, eid in zip(
        [rm_to_task[rm] for rm in definition["rm_ids"][:3]], external_ids, strict=True
    ):
        edges.append({"from": tid, "to": eid, "type": EDGE_RELATED})
    return {
        "kind": "tracker-snapshot",
        "schema": SCHEMA_ID,
        "tasks": tasks,
        "edges": edges,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile roadmap/dependencies.json against a synthetic tracker "
            "snapshot. Network-free dry-run; never writes tracker state."
        )
    )
    parser.add_argument(
        "--definition",
        required=True,
        help="Path to roadmap definition JSON (dependencies.json shape)",
    )
    parser.add_argument(
        "--snapshot",
        required=True,
        help="Path to tracker snapshot JSON (rm04-tracker-snapshot/1)",
    )
    parser.add_argument(
        "--related-to-orientation",
        choices=sorted(RELATED_TO_ORIENTATIONS),
        default=None,
        help=(
            "Override snapshot related_to_orientation. "
            f"Default when unset on snapshot: {ORIENTATION_UNVERIFIED}. "
            f"{ORIENTATION_ORDERED}=exact from→to (reversed_edge on reverse); "
            f"{ORIENTATION_UNVERIFIED}=reversed advisory → "
            f"{REASON_ADVISORY_DIRECTION_UNVERIFIED} (exit non-zero / hold)."
        ),
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the JSON report (stdout always used too)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        definition = json.loads(Path(args.definition).read_text(encoding="utf-8"))
        snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
        report = reconcile(
            definition,
            snapshot,
            related_to_orientation=args.related_to_orientation,
        )
    except ReconcileError as exc:
        report = {
            "record_type": RECORD_TYPE,
            "agreement": False,
            "disagreement_detected": True,
            "effects": "none",
            "reason_codes": [exc.reason_code],
            "disagreements": [
                {
                    "reason_code": exc.reason_code,
                    "message": exc.message,
                    "details": exc.details,
                }
            ],
            "effects_authorized": False,
            "network_calls": False,
        }
        sys.stdout.write(dumps_deterministic(report))
        if args.output:
            Path(args.output).write_text(dumps_deterministic(report), encoding="utf-8")
        return 1 if exc.reason_code != REASON_INPUT_ERROR else 2
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "record_type": RECORD_TYPE,
            "agreement": False,
            "disagreement_detected": True,
            "effects": "none",
            "reason_codes": [REASON_INPUT_ERROR],
            "disagreements": [
                {
                    "reason_code": REASON_INPUT_ERROR,
                    "message": str(exc),
                    "details": {},
                }
            ],
            "effects_authorized": False,
            "network_calls": False,
        }
        sys.stdout.write(dumps_deterministic(report))
        return 2

    text = dumps_deterministic(report)
    sys.stdout.write(text)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    return 0 if report["agreement"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
