#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate the finite CW proposal and its provenance, never native task state.

This is a structural/coverage gate. It does not establish scientific correctness,
independent acceptance, native registration, readiness, deployment or authority.
"""
from __future__ import annotations

from collections import Counter, deque
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = Path("roadmap/coordinated-work/plan")
ROLES = {"KC-Brain", "KC-SWE", "Agent-Brain", "Agent-SWE", "DEUS-Arcana", "Research-Arcana"}


class InvalidProgramme(ValueError):
    """The proposal cannot support the claimed structural result."""


def require(condition, message):
    if not condition:
        raise InvalidProgramme(message)


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def constant(value):
        raise InvalidProgramme(f"non-finite JSON constant: {value}")

    def decoded_values(value):
        # Escaped surrogates and exponent overflow are visible only after JSON
        # decoding; validating the input string alone does not reject them.
        if isinstance(value, str):
            value.encode("utf-8", errors="strict")
        elif isinstance(value, float):
            require(math.isfinite(value), "non-finite decoded JSON number")
        elif isinstance(value, dict):
            for key, child in value.items():
                decoded_values(key)
                decoded_values(child)
        elif isinstance(value, list):
            for child in value:
                decoded_values(child)

    try:
        text.encode("utf-8", errors="strict")
        result = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
        decoded_values(result)
    except UnicodeError as error:
        raise InvalidProgramme("non-scalar Unicode in JSON") from error
    return result


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def source_table(text, heading):
    section = text.split(heading, 1)[1].split("\n## ", 1)[0]
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in section.splitlines() if line.startswith("| ")]
    return rows[2:]


def topology(nodes, dependencies):
    """Kahn traversal; depth is a node count, not duration or speedup."""
    indegree = {key: len(dependencies[key]) for key in nodes}
    successors = {key: [] for key in nodes}
    for key in nodes:
        require(len(dependencies[key]) == len(set(dependencies[key])), f"duplicate edge: {key}")
        for predecessor in dependencies[key]:
            require(predecessor in nodes, f"unknown dependency: {key} <- {predecessor}")
            successors[predecessor].append(key)
    queue = deque(sorted(key for key in nodes if indegree[key] == 0))
    order, depth, ancestors = [], {}, {}
    while queue:
        key = queue.popleft()
        order.append(key)
        depth[key] = 1 + max((depth[p] for p in dependencies[key]), default=0)
        ancestors[key] = set(dependencies[key])
        for predecessor in dependencies[key]:
            ancestors[key].update(ancestors[predecessor])
        for child in sorted(successors[key]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    require(len(order) == len(nodes), "dependency cycle")
    return order, depth, ancestors


def validate(graph, baseline, baseline_bytes, source_readme, source_experiments):
    require(graph.get("schema") == "CoordinatedWorkExecutionProposal/v1", "unknown proposal schema")
    require(graph.get("authority") == "Muneral", "wrong execution authority")
    require(graph.get("proposal_ids_are_muneral_ids") is False, "proposal IDs are not native IDs")
    require(graph.get("current_task_statuses_included") is False, "native status must remain separate")
    require(graph.get("external_task_id") is None and graph.get("execution_assigned") is False,
            "programme claims a native binding")
    require(graph["source"]["step_blob"] == git_blob(baseline_bytes), "source72 blob mismatch")
    source = {row["id"]: row for row in baseline}
    require(len(source) == len(baseline) == 72, "baseline must retain 72 unique source rows")
    expected_source = {f"{family}{number:02}" for family in "ABCDEFGHI" for number in range(1, 9)}
    require(set(source) == expected_source, "source72 identity coverage mismatch")

    tasks, epics, papers, hypotheses = graph["tasks"], graph["epics"], graph["papers"], graph["hypotheses"]
    all_ids = [graph["programme_id"]] + [row["id"] for rows in (tasks, epics, papers, hypotheses) for row in rows]
    require(len(set(all_ids)) == len(all_ids), "proposal identifier collision")
    require((len(tasks), len(epics), len(papers), len(hypotheses)) == (104, 23, 16, 12), "declared scope counts changed")
    require(epics[0]["id"] == "CW-EP00" and graph["priority_order"][0] == "CW-EP00", "launch epic is not first")
    by_id = {row["id"]: row for row in tasks}
    epic_by_id = {row["id"]: row for row in epics}
    require(set(by_id) == {"CW-" + key for key in expected_source} | {f"CW-N{n:02}" for n in range(1, 33)},
            "work-package identity set changed")
    assigned = Counter(key for row in epics for key in row["task_ids"])
    require(set(assigned) == set(by_id) and set(assigned.values()) == {1}, "epic membership is incomplete or duplicated")

    outputs = {}
    imported = {}
    dependencies = {}
    for row in [graph] + epics + tasks:
        row_id = row.get("id", row.get("programme_id"))
        require(row["status"] == "proposed", f"proposal promoted to execution state: {row_id}")
        require(row["external_task_id"] is None and row["execution_assigned"] is False,
                f"native binding asserted in proposal: {row_id}")
        for role in ("proposed_owner_role", "proposed_executor_role", "proposed_reviewer_role"):
            require(row[role] in ROLES, f"unknown proposed role: {row_id}/{role}")
        criteria = row["acceptance_criteria"]
        require(all(type(a["number"]) is int for a in criteria)
                and [a["number"] for a in criteria] == list(range(1, len(criteria) + 1)) and len(criteria) >= 3,
                f"acceptance criteria not consecutively numbered: {row_id}")
        require(all(isinstance(a["text"], str) and a["text"].strip() for a in criteria), "empty acceptance criterion")

    for task in tasks:
        key = task["id"]
        require(task["epic_id"] in epic_by_id and key in epic_by_id[task["epic_id"]]["task_ids"], "epic relation mismatch")
        require(task["evidence_required"] and task["negative_controls"], f"unfalsifiable output contract: {key}")
        require(task["outputs"], f"missing output: {key}")
        for output in task["outputs"]:
            require(output["id"] not in outputs, "duplicate output identity")
            require(output["created"] is False, "future output claimed as created")
            path = Path(output["proposed_path"])
            require(not path.is_absolute() and ".." not in path.parts, "unsafe proposed output path")
            outputs[output["id"]] = key
        dependencies[key] = [d["task_id"] for d in task["dependencies"]]
        if task["origin"] == "imported":
            source_id = task["source_step_id"]
            require(source_id in source and source_id not in imported, "source row missing or duplicated")
            original = source[source_id]
            for target_key, original_key in (("source_acceptance", "acceptance"), ("source_deliverable", "deliverable"),
                                             ("source_status", "status"), ("source_dependencies", "dependencies"),
                                             ("title", "title"), ("title_ru", "title_ru")):
                require(task[target_key] == original[original_key], f"source provenance rewritten: {key}/{target_key}")
            require(task["source_acceptance"] == task["acceptance_criteria"][0]["text"], "source acceptance lost")
            require(task["source_blob"] == graph["source"]["step_blob"], "task source blob changed")
            imported[source_id] = key
    require(set(imported) == expected_source, "imported source72 coverage incomplete")
    require(graph["coverage"]["source_step_to_task"] == imported, "source crosswalk differs from task contracts")
    for task in tasks:
        for edge in task["dependencies"]:
            require(edge["reason"].strip() and edge["consumes"], "dependency lacks consumed output or reason")
            for consumed in edge["consumes"]:
                require(outputs.get(consumed) == edge["task_id"], f"edge consumes the wrong output: {task['id']}/{consumed}")

    order, depth, ancestors = topology(set(by_id), dependencies)
    source_order, source_depth, _ = topology(set(source), {key: row["dependencies"] for key, row in source.items()})
    metrics = {"tasks": len(tasks), "edges": sum(map(len, dependencies.values())), "longestDependencyChainNodes": max(depth.values())}
    require(metrics == graph["proposed_graph_metrics"], "proposed graph metrics do not match graph")
    require(len(source_order) == 72 and sum(len(row["dependencies"]) for row in source.values()) == 78
            and max(source_depth.values()) == 64, "retained source topology changed")

    original_papers = source_table(source_readme, "## Potential scientific series")
    original_hypotheses = source_table(source_experiments, "## Twelve testable hypotheses")
    require(len(original_papers) == 16 and len(original_hypotheses) == 12, "source boundary tables changed")
    for boundary in papers + hypotheses:
        mapped = boundary["mapped_task_ids"]
        declared = ["CW-" + key for key in boundary["baseline_steps"] + boundary["additional_steps"]]
        require(len(mapped) == len(set(mapped)) and mapped == declared,
                f"boundary mapping disagrees with declared steps: {boundary['id']}")
        require(boundary["baseline_steps"] and set(boundary["baseline_steps"]) <= expected_source,
                f"boundary baseline steps invalid: {boundary['id']}")
        require(set(boundary["additional_steps"]) <= {f"N{n:02}" for n in range(1, 33)},
                f"boundary additional steps invalid: {boundary['id']}")
    for paper in papers:
        require(paper["mapped_task_ids"] and set(paper["mapped_task_ids"]) <= set(by_id), "paper task coverage incomplete")
        require([paper[k] for k in ("source_title", "source_main_question", "source_engineering_companion")]
                == original_papers[paper["source_index"] - 1], "source paper boundary altered")
        require(paper["outcome"] == "not_evaluated" and paper["external_artifact_id"] is None, "paper promoted to result")
        require(set(paper["release_template_task_ids"]) == {f"CW-I{n:02}" for n in range(3, 9)}, "paper release gates incomplete")
    require({p["source_index"] for p in papers} == set(range(1, 17)), "source16 paper coverage mismatch")
    for hypothesis in hypotheses:
        require(hypothesis["mapped_task_ids"] and set(hypothesis["mapped_task_ids"]) <= set(by_id), "hypothesis task coverage incomplete")
        require([hypothesis[k] for k in ("source_statement", "source_comparison", "source_refutation")]
                == original_hypotheses[hypothesis["source_number"] - 1],
                "source hypothesis/refutation altered")
        require(hypothesis["outcome"] == "unknown", "hypothesis promoted to finding")
        require(hypothesis["registration_task_id"] == "CW-H01" and hypothesis["analysis_task_id"] == "CW-N20",
                "hypothesis preregistration/analysis link lost")
    require({h["source_number"] for h in hypotheses} == set(range(1, 13)), "source12 hypothesis coverage mismatch")

    # Real counterexamples to indiscriminate serialization, not a speed claim.
    for domain in ("CW-H02", "CW-H03", "CW-H04"):
        require(not (ancestors[domain] & ({"CW-H02", "CW-H03", "CW-H04"} - {domain})), "independent domain stands serialized")
        require("CW-H01" in ancestors[domain], "stand protocol binding removed")
    require("CW-H08" not in ancestors["CW-I01"], "novelty review delayed until field trial")
    require("CW-N06" not in ancestors["CW-N07"], "announcement unnecessarily blocked by registry")
    require("CW-H01" not in ancestors["CW-N30"], "all publication classes blocked by empirical preregistration")
    for child, parents in {"CW-N18": {"CW-H02", "CW-H03", "CW-H04"},
                           "CW-H05": {"CW-N18", "CW-N20"}, "CW-H07": {"CW-H06", "CW-N26"},
                           "CW-H08": {"CW-H07", "CW-N29"}, "CW-N08": {"CW-N06", "CW-N07"}}.items():
        require(parents <= ancestors[child], f"required evidence gate removed: {child}")
    expected = {"initial_checked_bibliographic_records": 157, "additional_citation_candidates": 1019,
                "retained_records": 1176, "unique_work_count": "not_established", "full_text_critical_appraisals": 0,
                "candidate_papers": 16, "hypotheses": 12, "source_steps": 72, "reported_probe_revision": 2,
                "reported_probe_scenarios": 10, "reported_probe_periods": 100, "reported_probe_checks": 190,
                "reported_probe_violations": 0}
    require(all(type(graph["evidence_baseline"].get(k)) is type(v) and graph["evidence_baseline"].get(k) == v for k, v in expected.items()),
            "source evidence boundary changed")
    return {"schema": graph["schema"], "epics": len(epics), "work_packages": len(tasks), "source_steps_preserved": len(imported),
            "paper_boundaries_covered": len(papers), "hypotheses_covered": len(hypotheses),
            "blocking_edges": metrics["edges"], "longest_dependency_chain_nodes": max(depth.values()),
            "source_longest_dependency_chain_nodes": max(source_depth.values()),
            "ready_roots_in_proposal": [key for key in order if not dependencies[key]],
            "native_registration": "NOT_VERIFIED", "scope": "proposal structure and source coverage only"}


def inputs(root=ROOT):
    raw = (root / PLAN / "roadmap_steps.json").read_bytes()
    graph = strict_json((root / PLAN / "execution-graph.json").read_text(encoding="utf-8"))
    return (graph, strict_json(raw.decode("utf-8")), raw,
            (root / "roadmap/coordinated-work/README.md").read_text(encoding="utf-8"),
            (root / "roadmap/coordinated-work/EXPERIMENTS.md").read_text(encoding="utf-8"))


def main():
    try:
        print(json.dumps(validate(*inputs()), ensure_ascii=False, indent=2))
    except (InvalidProgramme, ValueError, TypeError, KeyError, UnicodeError, OSError) as error:
        print(f"CW_PROGRAMME_REFUSE: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
