#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Prepare Muneral request templates and check supplied readbacks; never call an API.

The input is a Coordinated Work proposal graph, not an execution ledger.
Native task UUIDs are accepted only from a separate private binding file.
This tool uses no credentials, network library, subprocess, or environment lookup.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid

try:
    from tools import check_cw_programme as programme_checker
except ModuleNotFoundError:
    import check_cw_programme as programme_checker

PROJECT_UUID = "5d427422-4a5e-45a7-bc3b-f0aa11579a5b"
BINDINGS_SCHEMA = "kc-cw-muneral-bindings/1"
READBACK_SCHEMA = "kc-cw-muneral-readback/1"
PUBLIC_SCHEMA = "kc-cw-registration-public-receipt/1"
LIMITATION = "Offline consistency only; no Muneral request or source authentication was performed."

FULL_PROGRAMME_ID = "KC-CW-20261118"
FULL_PROGRAMME_SCHEMA = "CoordinatedWorkExecutionProposal/v1"
FULL_PROGRAMME_TASK_IDS = {f"CW-N{number:02d}" for number in range(1, 33)}


def requires_full_programme_profile(graph):
    """Recognize the known scientific programme independently of removable mode keys.

    Generic fixtures remain supported, but deleting schema/papers must not
    downgrade the 104-package Coordinated Work proposal to the generic lane.
    """
    tasks = graph.get("tasks")
    task_ids = {row.get("id") for row in tasks if isinstance(row, dict)} if isinstance(tasks, list) else set()
    return (graph.get("programme_id") == FULL_PROGRAMME_ID
            or graph.get("schema") == FULL_PROGRAMME_SCHEMA
            or any(key in graph for key in ("papers", "hypotheses", "paper_release_contracts",
                                            "paper_release_metrics"))
            or bool(task_ids & FULL_PROGRAMME_TASK_IDS))


def require_full_programme_profile(graph):
    require(graph.get("programme_id") == FULL_PROGRAMME_ID
            and graph.get("schema") == FULL_PROGRAMME_SCHEMA
            and isinstance(graph.get("papers"), list) and len(graph["papers"]) == 16
            and isinstance(graph.get("hypotheses"), list) and len(graph["hypotheses"]) == 12
            and isinstance(graph.get("source"), dict),
            "full-programme profile incomplete or downgraded")


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def nonblank(value, label):
    require(isinstance(value, str) and value.strip() == value and bool(value),
            f"{label}: expected a nonblank trimmed string")
    require(not any(0xD800 <= ord(c) <= 0xDFFF for c in value),
            f"{label}: isolated Unicode surrogate")
    return value


def native_uuid(value, label, nullable=False):
    if nullable and value is None:
        return None
    nonblank(value, label)
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise Invalid(f"{label}: not a UUID") from exc
    require(str(parsed) == value and parsed.int != 0,
            f"{label}: use a canonical nonzero native UUID")
    return value


def timestamp(value, label):
    nonblank(value, label)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Invalid(f"{label}: invalid ISO 8601 timestamp") from exc
    require(parsed.tzinfo is not None, f"{label}: timezone required")
    return value


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    data = Path(path).read_bytes()
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=strict_object,
                           parse_constant=lambda v: (_ for _ in ()).throw(Invalid(f"nonfinite JSON number: {v}")))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise Invalid(f"{path}: not strict UTF-8 JSON: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level object required")
    return value, hashlib.sha256(data).hexdigest()


def topological(ids, parents):
    remaining = {key: set(parents.get(key, [])) for key in ids}
    order, waves = [], []
    while remaining:
        wave = sorted(key for key, needs in remaining.items() if not needs)
        require(bool(wave), "dependency cycle detected")
        waves.append(wave)
        order.extend(wave)
        for key in wave:
            del remaining[key]
        for needs in remaining.values():
            needs.difference_update(wave)
    return order, waves


def criteria(value, label):
    require(isinstance(value, list) and bool(value), f"{label}: numbered AC list required")
    for number, item in enumerate(value, 1):
        require(isinstance(item, dict) and type(item.get("number")) is int
                and item["number"] == number, f"{label}: AC numbers must be contiguous from 1")
        nonblank(item.get("text"), f"{label} AC {number}")
    return value


def normalize_graph(graph):
    programme_id = nonblank(graph.get("programme_id"), "programme_id")
    require(bool(re.fullmatch(r"KC-CW-[A-Za-z0-9][A-Za-z0-9-]*", programme_id)), "invalid public programme identifier")
    if requires_full_programme_profile(graph):
        require_full_programme_profile(graph)
    epics, tasks = graph.get("epics"), graph.get("tasks")
    require(isinstance(epics, list) and bool(epics), "epics: nonempty array required")
    require(isinstance(tasks, list) and bool(tasks), "tasks: nonempty array required")
    nodes = {}
    nodes[programme_id] = {
        "id": programme_id, "kind": "programme", "parent": None,
        "title": graph.get("title"),
        "description": nonblank(graph.get("description"), "programme description"),
        "proposed_owner_role": graph.get("proposed_owner_role"),
        "proposed_executor_role": graph.get("proposed_executor_role"),
        "acceptance_criteria": criteria(graph.get("acceptance_criteria"), programme_id),
    }
    for epic in epics:
        require(isinstance(epic, dict), "epic: object required")
        key = nonblank(epic.get("id"), "epic id")
        require(bool(re.fullmatch(r"CW-[A-Z]+[0-9]{2,}", key)), "invalid public epic identifier")
        require(key not in nodes, f"duplicate proposal id: {key}")
        # A missing epic AC is an input defect; do not invent completion conditions.
        criteria(epic.get("acceptance_criteria"), key)
        nodes[key] = dict(epic, kind="epic", parent=programme_id)
    epic_ids = {epic["id"] for epic in epics}
    task_ids = set()
    for task in tasks:
        require(isinstance(task, dict), "task: object required")
        key = nonblank(task.get("id"), "task id")
        require(bool(re.fullmatch(r"CW-[A-Z]+[0-9]{2,}", key)), "invalid public task identifier")
        require(key not in nodes, f"duplicate proposal id: {key}")
        require(task.get("epic_id") in epic_ids, f"{key}: unknown epic")
        require(task.get("status") == "proposed" and task.get("external_task_id") is None
                and task.get("execution_assigned") is False,
                f"{key}: graph must keep proposed state separate from native execution")
        criteria(task.get("acceptance_criteria"), key)
        outputs = task.get("outputs")
        require(isinstance(outputs, list) and bool(outputs), f"{key}: outputs required")
        require(all(isinstance(output, dict) for output in outputs),
                f"{key}: output record must be an object")
        output_ids = [nonblank(o.get("id"), f"{key} output id") for o in outputs]
        require(len(output_ids) == len(set(output_ids)), f"{key}: duplicate output ids")
        for output in outputs:
            nonblank(output.get("description"), f"{key} output description")
        nodes[key] = dict(task, kind="task", parent=task["epic_id"])
        task_ids.add(key)
    for key, node in nodes.items():
        for field in ("title", "proposed_owner_role", "proposed_executor_role"):
            nonblank(node.get(field), f"{key} {field}")
    for epic in epics:
        wanted = {task["id"] for task in tasks if task["epic_id"] == epic["id"]}
        actual = epic.get("task_ids")
        require(isinstance(actual, list) and len(actual) == len(set(actual))
                and set(actual) == wanted, f"{epic['id']}: child membership differs from task epic_id")
    edges, parents = [], {}
    for key in sorted(task_ids):
        deps = nodes[key].get("dependencies")
        require(isinstance(deps, list), f"{key}: dependencies array required")
        parents[key] = set()
        for dependency in deps:
            require(isinstance(dependency, dict), f"{key}: dependency object required")
            target = dependency.get("task_id")
            require(target in task_ids and target != key, f"{key}: unknown or self dependency {target}")
            require(target not in parents[key], f"{key}: duplicate dependency {target}")
            consumes = dependency.get("consumes")
            available = {o["id"] for o in nodes[target]["outputs"]}
            require(isinstance(consumes, list) and bool(consumes)
                    and len(consumes) == len(set(consumes)) and set(consumes) <= available,
                    f"{key}: consumed outputs do not belong to {target}")
            nonblank(dependency.get("reason"), f"{key}->{target} reason")
            parents[key].add(target)
            edges.append({"from_proposal_id": key, "to_proposal_id": target,
                          "type": "depends_on", "consumes": consumes, "reason": dependency["reason"]})
    task_order, waves = topological(task_ids, parents)
    if requires_full_programme_profile(graph):
        try:
            # Share the full-programme output gate before any scope text is
            # generated; the generic imported/synthetic mode remains supported.
            programme_checker.validate_output_contracts(tasks)
            programme_checker.validate_release_contracts(graph)
        except programme_checker.InvalidProgramme as exc:
            raise Invalid(str(exc)) from exc
        for template_id in ["CW-N30"] + [f"CW-I{n:02}" for n in range(3, 9)]:
            nodes[template_id]["paper_release_contracts"] = graph["paper_release_contracts"]
    create_order = [programme_id] + sorted(epic_ids) + task_order
    return programme_id, nodes, create_order, edges, waves


def new_bindings(programme_id, nodes, digest, source_commit):
    roles = sorted({n[f] for n in nodes.values() for f in ("proposed_owner_role", "proposed_executor_role")})
    return {
        "schema": BINDINGS_SCHEMA, "programme_id": programme_id,
        "graph_sha256": digest, "source_commit": source_commit,
        "inventories": [{"project_uuid": PROJECT_UUID, "coverage": "NOT_READ",
                         "observed_at": None, "evidence_ref": None}],
        "single_writer_role": "KC-SWE",
        "roles": {role: {"native_id": None, "evidence_ref": None} for role in roles},
        "items": [{"proposal_id": key, "decision": "unresolved", "task_uuid": None,
                   "project_uuid": PROJECT_UUID, "parent_mode": "native",
                   "scope_record_type": "description",
                   "preserved_parent_uuid": None, "logical_parent_evidence_ref": None,
                   "reconciliation_evidence_ref": None} for key in nodes],
    }


def check_bindings(bindings, programme_id, nodes, digest, source_commit):
    require(bindings.get("schema") == BINDINGS_SCHEMA, "unsupported bindings schema")
    for field, expected in (("programme_id", programme_id), ("graph_sha256", digest), ("source_commit", source_commit)):
        require(bindings.get(field) == expected, f"bindings {field} does not match this exact graph/source")
    nonblank(bindings.get("single_writer_role"), "single_writer_role")
    rows = bindings.get("items")
    require(isinstance(rows, list), "bindings items must be an array")
    result, used = {}, set()
    for row in rows:
        require(isinstance(row, dict), "binding item must be an object")
        key = row.get("proposal_id")
        require(key in nodes and key not in result, f"unknown or duplicate binding: {key}")
        require(row.get("decision") in {"unresolved", "create", "reuse", "unknown_outcome"},
                f"{key}: unsupported reconciliation decision")
        native_uuid(row.get("project_uuid"), f"{key} project_uuid")
        task_uuid = native_uuid(row.get("task_uuid"), f"{key} task_uuid", nullable=True)
        require(task_uuid is None or task_uuid not in used, f"{key}: one native task bound to multiple proposal scopes")
        if task_uuid:
            require(row["decision"] in {"reuse", "create"}, f"{key}: UUID cannot resolve an unresolved/unknown outcome")
            nonblank(row.get("reconciliation_evidence_ref"), f"{key} reconciliation evidence")
            used.add(task_uuid)
        if row["decision"] == "reuse":
            require(task_uuid is not None, f"{key}: reuse needs actual native UUID")
        if row["decision"] == "create":
            nonblank(row.get("reconciliation_evidence_ref"), f"{key} create reconciliation evidence")
        require(row.get("parent_mode") in {"native", "reference_only"}, f"{key}: invalid parent mode")
        require(row.get("scope_record_type") in {"description", "content"}, f"{key}: invalid native scope record type")
        if row["parent_mode"] == "reference_only":
            require(row["decision"] == "reuse" and nodes[key]["parent"] is not None,
                    f"{key}: reference-only parent is for reused children only")
            native_uuid(row.get("preserved_parent_uuid"), f"{key} preserved parent", nullable=True)
            nonblank(row.get("logical_parent_evidence_ref"), f"{key} logical parent evidence")
        result[key] = row
    require(set(result) == set(nodes), "bindings must contain every proposal exactly once")
    return result


def complete_inventories(bindings):
    records = bindings.get("inventories")
    require(isinstance(records, list), "inventories must be an array")
    complete, seen = set(), set()
    for record in records:
        require(isinstance(record, dict), "inventory must be an object")
        project = native_uuid(record.get("project_uuid"), "inventory project_uuid")
        require(project not in seen, "duplicate project inventory")
        seen.add(project)
        coverage = record.get("coverage")
        require(coverage in {"NOT_READ", "own_tasks_only", "complete_project_index", "authoritative_owner_inventory"},
                "unsupported inventory coverage")
        if coverage in {"complete_project_index", "authoritative_owner_inventory"}:
            timestamp(record.get("observed_at"), "inventory observed_at")
            nonblank(record.get("evidence_ref"), "complete inventory evidence")
            complete.add(project)
    return complete


def description(node, digest, source_commit):
    lines = [f"Proposal: {node['id']}", f"Graph SHA-256: {digest}",
             f"Source commit: {source_commit or 'NOT_BOUND_TO_COMMITTED_SOURCE'}",
             f"Proposed accountable role: {node['proposed_owner_role']}",
             f"Proposed execution role: {node['proposed_executor_role']}",
             "These role proposals do not assign native principals or start work.", "",
             node.get("description", node["title"]), "", "Acceptance criteria:"]
    if node.get("needs_child_instantiation"):
        lines[6:6] = ["This is a broad work package requiring bounded child-task instantiation before implementation dispatch."]
    lines.extend(f"AC{ac['number']}. {ac['text']}" for ac in node["acceptance_criteria"])
    for field, heading in (("outputs", "Outputs"), ("evidence_required", "Required evidence"),
                            ("negative_controls", "Negative controls"), ("dependencies", "Required prerequisite outputs"),
                            ("paper_release_contracts", "Required per-paper release contracts; instantiate and validate before dispatch")):
        if node.get(field):
            lines += ["", heading + ":"]
            for value in node[field]:
                lines.append("- " + (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)))
    return "\n".join(lines)


def prepare(graph, digest, source_commit=None, bindings=None, release_instances=None):
    require(isinstance(digest, str) and bool(re.fullmatch(r"[0-9a-f]{64}", digest)), "graph digest must be exact SHA-256")
    if source_commit is not None:
        require(bool(re.fullmatch(r"[0-9a-f]{40}", source_commit)), "source_commit must be a full lowercase Git SHA")
    programme_id, nodes, order, edges, waves = normalize_graph(graph)
    generated_releases = []
    if requires_full_programme_profile(graph):
        try:
            generated_releases = (programme_checker.instantiate_release_instances(graph)
                                  if release_instances is None else release_instances)
            programme_checker.validate_release_instances(graph, generated_releases)
        except programme_checker.InvalidProgramme as exc:
            raise Invalid(str(exc)) from exc
    else:
        require(release_instances is None, "release instances require a declared paper programme")
    bindings = new_bindings(programme_id, nodes, digest, source_commit) if bindings is None else bindings
    bound = check_bindings(bindings, programme_id, nodes, digest, source_commit)
    inventoried_projects = complete_inventories(bindings)
    actions = []
    for number, key in enumerate(order, 1):
        node, row = nodes[key], bound[key]
        if row["task_uuid"] is not None:
            continue
        parent = node["parent"]
        actual_parent = bound[parent]["task_uuid"] if parent else None
        body = {"projectId": row["project_uuid"], "title": f"KCP {key}: {node['title']}",
                "description": description(node, digest, source_commit), "status": "todo"}
        if parent:
            body["parentId"] = actual_parent or "${MUNERAL_UUID:" + parent + "}"
        holds = []
        if not source_commit:
            holds.append("source_commit_not_bound")
        if row["project_uuid"] not in inventoried_projects:
            holds.append("complete_project_inventory_not_recorded")
        if row["decision"] != "create":
            holds.append("creation_not_reconciled" if row["decision"] != "unknown_outcome" else "unknown_outcome_do_not_repost")
        if parent and not actual_parent:
            holds.append("parent_uuid_not_bound")
        actions.append({"order": number, "proposal_id": key, "kind": node["kind"],
                        "method": "POST", "path": "/tasks", "body_template": body,
                        "template_complete": not (parent and not actual_parent),
                        "recorded_prerequisites_complete": not holds, "holds": holds,
                        "requires_current_principal_scope_check": True,
                        "proposed_owner_role": node["proposed_owner_role"],
                        "proposed_executor_role": node["proposed_executor_role"]})
    edge_actions = []
    for number, edge in enumerate(edges, 1):
        source = bound[edge["from_proposal_id"]]["task_uuid"]
        target = bound[edge["to_proposal_id"]]["task_uuid"]
        edge_actions.append(dict(edge, order=number, method="POST",
            path="/tasks/" + (source or "${MUNERAL_UUID:" + edge["from_proposal_id"] + "}") + "/dependencies",
            body_template={"toTaskId": target or "${MUNERAL_UUID:" + edge["to_proposal_id"] + "}", "type": "depends_on"},
            template_complete=bool(source and target),
            requires_existing_edge_reconciliation=True,
            requires_creator_or_executor_scope_on_both_endpoints=True))
    return {
        "schema": "kc-cw-muneral-registration-plan/1", "programme_id": programme_id,
        "graph_sha256": digest, "source_commit": source_commit, "mode": "offline_templates_only",
        "limitation": LIMITATION, "node_count": len(nodes), "task_count": len(graph["tasks"]),
        "epic_count": len(graph["epics"]), "dependency_count": len(edges),
        "actual_uuid_bindings_supplied": sum(bool(row["task_uuid"]) for row in bound.values()),
        "create_requests": actions, "dependency_requests": edge_actions,
        "paper_release_instance_templates": generated_releases,
        "paper_release_template_count": len(generated_releases),
        "paper_release_stage_count": sum(len(r["nodes"]) for r in generated_releases),
        "native_release_instances_created": 0,
        "paper_release_limitation": "Separate proposed release DAGs; not native requests, accepted evidence or publication authorization.",
        "required_native_scope_records": [
            {"proposal_id": key, "task_uuid": bound[key]["task_uuid"],
             "record_type": bound[key]["scope_record_type"],
             "sha256": hashlib.sha256(description(nodes[key], digest, source_commit).encode("utf-8")).hexdigest(),
             "text": description(nodes[key], digest, source_commit)} for key in order
        ],
        "execution_topological_waves": waves,
        "wave_limitation": "Ordering is a proposal only. Native readiness, accepted prerequisite outputs, owner scope and capacity must be read before execution.",
        "bindings_template": bindings,
    }


def verify_readback(graph, digest, source_commit, bindings, snapshot):
    programme_id, nodes, _, edges, _ = normalize_graph(graph)
    bound = check_bindings(bindings, programme_id, nodes, digest, source_commit)
    require({row["project_uuid"] for row in bound.values()} <= complete_inventories(bindings),
            "complete readback requires authoritative inventories for every mapped project")
    require(source_commit is not None, "readback verification requires exact source_commit")
    require(snapshot.get("schema") == READBACK_SCHEMA, "unsupported readback schema")
    for field, value in (("programme_id", programme_id), ("graph_sha256", digest), ("source_commit", source_commit)):
        require(snapshot.get(field) == value, f"snapshot {field} mismatch")
    observed_at = timestamp(snapshot.get("observed_at"), "snapshot observed_at")
    require(all(row["task_uuid"] for row in bound.values()), "complete readback requires every actual UUID binding")
    roles = bindings.get("roles")
    require(isinstance(roles, dict), "private role bindings required")
    actual = {}
    for item in snapshot.get("tasks", []):
        require(isinstance(item, dict), "snapshot task must be an object")
        key = item.get("proposal_id")
        require(key in nodes and key not in actual, f"unknown or duplicate readback task: {key}")
        expected, node = bound[key], nodes[key]
        require(native_uuid(item.get("task_uuid"), f"{key} observed UUID") == expected["task_uuid"], f"{key}: task UUID mismatch")
        require(native_uuid(item.get("project_uuid"), f"{key} observed project") == expected["project_uuid"], f"{key}: project mismatch")
        parent = node["parent"]
        wanted_parent = (bound[parent]["task_uuid"] if parent else None) if expected["parent_mode"] == "native" else expected.get("preserved_parent_uuid")
        require(native_uuid(item.get("parent_uuid"), f"{key} observed parent", nullable=True) == wanted_parent, f"{key}: native parent mismatch")
        for field in ("owner", "executor"):
            role = node[f"proposed_{field}_role"]
            require(item.get(f"{field}_role") == role, f"{key}: {field} role mismatch")
            principal = roles.get(role, {})
            nonblank(principal.get("native_id"), f"{role} actual native identity")
            nonblank(principal.get("evidence_ref"), f"{role} identity evidence")
            require(item.get(f"{field}_native_id") == principal["native_id"], f"{key}: {field} native identity mismatch")
        for field in ("task_evidence_ref", "owner_evidence_ref", "assignees_evidence_ref", "readiness_evidence_ref"):
            nonblank(item.get(field), f"{key} {field}")
        require(item.get("scope_record_type") == expected["scope_record_type"], f"{key}: native scope record type mismatch")
        required_scope_digest = hashlib.sha256(description(node, digest, source_commit).encode("utf-8")).hexdigest()
        require(item.get("scope_record_sha256") == required_scope_digest, f"{key}: accepted scope record digest mismatch")
        nonblank(item.get("scope_evidence_ref"), f"{key} native scope evidence")
        actual[key] = item
    require(set(actual) == set(nodes), "readback does not cover every proposal")
    expected_edges = {(bound[e["from_proposal_id"]]["task_uuid"], bound[e["to_proposal_id"]]["task_uuid"], "depends_on") for e in edges}
    observed_edges = set()
    advisory_count = 0
    for edge in snapshot.get("dependencies", []):
        source = native_uuid(edge.get("from_uuid"), "edge source")
        target = native_uuid(edge.get("to_uuid"), "edge target")
        kind = edge.get("type")
        require(kind in {"depends_on", "blocks", "related_to", "duplicates"}, "invalid native edge type")
        nonblank(edge.get("evidence_ref"), "edge evidence")
        if kind in {"related_to", "duplicates"}:
            advisory_count += 1
            continue
        triple = (source, target, kind)
        require(triple not in observed_edges, "duplicate native blocking edge record")
        observed_edges.add(triple)
    require(observed_edges == expected_edges,
            f"blocking dependency mismatch: {len(expected_edges-observed_edges)} missing, {len(observed_edges-expected_edges)} unexpected; reversed/extra/external blockers require explicit reconciliation")
    # Whitelist only; never copy native UUIDs, principal identities or private evidence URLs.
    return {
        "schema": PUBLIC_SCHEMA, "programme_id": programme_id, "graph_sha256": digest,
        "source_commit": source_commit, "observed_at": observed_at,
        "registration_snapshot": "OFFLINE_CONSISTENT",
        "native_live_verification": "NOT_PERFORMED_BY_THIS_TOOL", "execution_status": "NOT_INFERRED",
        "bound_proposals": len(nodes), "bound_programmes": 1,
        "bound_epics": len(graph["epics"]), "bound_tasks": len(graph["tasks"]),
        "matched_blocking_dependencies": len(expected_edges),
        "advisory_links_not_used_as_blockers": advisory_count,
        "reference_only_parent_bindings": sum(row["parent_mode"] == "reference_only" for row in bound.values()),
        "proposal_ids": sorted(nodes), "limitation": LIMITATION,
    }


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(path).chmod(0o600)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", required=True)
    parser.add_argument("--source-commit", help="Exact committed source; omit only while preparing an uncommitted candidate")
    parser.add_argument("--bindings", help="Private reconciled native UUID mapping; never publish this file")
    parser.add_argument("--readback", help="Private normalized exact readbacks; requires --bindings")
    parser.add_argument("--release-instances", help="Optional exact-source release DAG templates to validate before preparation")
    parser.add_argument("--output", required=True, help="New output directory; existing files are not overwritten")
    args = parser.parse_args(argv)
    try:
        graph, digest = load_json(args.graph)
        bindings = load_json(args.bindings)[0] if args.bindings else None
        require(not args.readback or bindings is not None, "--readback requires --bindings")
        supplied_releases = None
        if args.release_instances:
            release_file = load_json(args.release_instances)[0]
            require(release_file.get("schema") == "CoordinatedWorkReleaseInstances/v1", "unsupported release instance schema")
            require(release_file.get("graph_sha256") == digest and release_file.get("source_commit") == args.source_commit,
                    "release instances must bind this exact graph and source")
            supplied_releases = release_file.get("instances")
            require(isinstance(supplied_releases, list), "release instances must be an explicit array")
        plan = prepare(graph, digest, args.source_commit, bindings, supplied_releases)
        receipt = verify_readback(graph, digest, args.source_commit, bindings, load_json(args.readback)[0]) if args.readback else None
        out = Path(args.output)
        require(not out.exists(), "output directory already exists; choose a new versioned directory")
        out.mkdir(parents=True, mode=0o700)
        private_bindings = plan.pop("bindings_template")
        if receipt:
            plan["satisfied_dependency_count"] = len(plan["dependency_requests"])
            plan["dependency_requests"] = []
        write_json(out / "registration-plan.private.json", plan)
        write_json(out / "bindings.private.json", private_bindings)
        if plan["paper_release_instance_templates"]:
            write_json(out / "paper-release-instances.private.json", {
                "schema": "CoordinatedWorkReleaseInstances/v1", "graph_sha256": digest,
                "source_commit": args.source_commit, "instances": plan["paper_release_instance_templates"],
                "native_release_instances_created": 0,
                "limitation": plan["paper_release_limitation"],
            })
        scopes = out / "scope-records.private"
        scopes.mkdir(mode=0o700)
        for record in plan["required_native_scope_records"]:
            path = scopes / (record["proposal_id"] + ".txt")
            path.write_text(record["text"], encoding="utf-8")
            path.chmod(0o600)
        if receipt:
            write_json(out / "registration-receipt.public.json", receipt)
        write_json(out / "preparation-summary.json", {
            "mode": plan["mode"], "programme_id": plan["programme_id"],
            "node_count": plan["node_count"], "task_count": plan["task_count"],
            "epic_count": plan["epic_count"], "dependency_count": plan["dependency_count"],
            "paper_release_template_count": plan["paper_release_template_count"],
            "paper_release_stage_count": plan["paper_release_stage_count"],
            "native_release_instances_created": 0,
            "actual_uuid_bindings_supplied": plan["actual_uuid_bindings_supplied"],
            "native_requests_executed": 0, "source_commit": args.source_commit,
            "readback_consistency": "NOT_CHECKED" if receipt is None else "OFFLINE_CONSISTENT",
            "limitation": LIMITATION,
        })
        print(json.dumps({"prepared": str(out), "nodes": plan["node_count"],
                          "dependencies": plan["dependency_count"], "native_requests_executed": 0}))
        return 0
    except (Invalid, OSError, TypeError, KeyError, AttributeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
