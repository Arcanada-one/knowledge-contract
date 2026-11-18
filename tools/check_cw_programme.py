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

# Provisional authored claim classes. Changing one requires an explicit reviewed
# release-boundary revision; a graph-only edit must not silently promote a
# domain-model or literature-review paper into an empirical field-effect claim.
# This pins the *class*, not the truth or independent acceptance of the prose.
PAPER_CLAIM_CLASSES = {
    "CW-P01": "review", "CW-P02": "domain_model", "CW-P03": "domain_model",
    "CW-P04": "resource_semantics", "CW-P05": "capability_model",
    "CW-P06": "simulation_comparison", "CW-P07": "simulation_comparison",
    "CW-P08": "simulation_comparison", "CW-P09": "organizational_effect",
    "CW-P10": "forecast_backtest", "CW-P11": "decision_profile",
    "CW-P12": "conditional_admissibility", "CW-P13": "organizational_effect",
    "CW-P14": "conditional_control", "CW-P15": "organizational_transfer",
    "CW-P16": "evidence_lifecycle",
}

# Provisional, author-declared release claim prose pinned to an exact source
# revision. Equality detects an unreviewed edit; it does NOT establish truth,
# evidence acceptance, rights, translated fidelity, or publishability.
# Deliberate scope changes require a separately reviewed release revision.
PAPER_CLAIM_SCOPES = {
    "CW-P01": "Reviewed research map with appraised primary sources and explicit unresolved gaps.",
    "CW-P02": "Representation of organizational needs and obligations; no measured organizational benefit is claimed.",
    "CW-P03": "Typed work dependencies and concurrent resource semantics under stated assumptions.",
    "CW-P04": "Resource types, units and conditional admissibility; no unrestricted universal resource law.",
    "CW-P05": "Task-specific capability, competency evidence and team conditions; occupation titles do not establish individual ability.",
    "CW-P06": "System performance and local-metric counterexamples in declared validated comparisons, not field effects.",
    "CW-P07": "Flow and release-policy comparisons within the validated manufacturing model and declared operating region.",
    "CW-P08": "Qualification-aware staffing and scheduling comparisons in the declared service model.",
    "CW-P09": "Measured organizational effects of hiring, training or automation under the evaluated bounded intervention.",
    "CW-P10": "Time-respecting forecast and uncertainty backtests; prediction quality is separate from intervention effects.",
    "CW-P11": "Organizational knowledge prerequisites and bounded context; effectiveness requires separately scoped comparative evidence.",
    "CW-P12": "Conditional admissibility and verifiable decision records under explicit assumptions, not unconditional future safety.",
    "CW-P13": "Causal effects under an identified bounded field design with observed interventions and stated interference limits.",
    "CW-P14": "Conditional stability results and finite operational criteria within declared models; no universal field guarantee.",
    "CW-P15": "Held-out cross-organization transfer of observed intervention outcomes with independent reproduction and explicit transport limits.",
    "CW-P16": "Versioned knowledge revision, contradiction handling and evidence invalidation; no automatic runtime authority.",
}


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


def validate_release_contracts(graph):
    """Check declared evidence gates, separately from the 104-package DAG."""
    tasks = {row["id"]: row for row in graph["tasks"]}
    papers = {row["id"]: row for row in graph["papers"]}
    contracts = graph.get("paper_release_contracts")
    require(isinstance(contracts, list) and len(contracts) == len(papers),
            "per-paper required-gate map is missing or incomplete")
    seen = set()
    for contract in contracts:
        key = contract.get("paper_id")
        require(key in papers and key not in seen, "duplicate or unknown paper release contract")
        seen.add(key)
        require(contract.get("claim_class") == PAPER_CLAIM_CLASSES[key],
                f"paper release claim class changed without reviewed revision: {key}")
        require(contract.get("status") == "proposed" and contract.get("external_artifact_id") is None,
                "paper release contract promoted to accepted artifact")
        require(isinstance(contract.get("claim_scope"), str) and contract["claim_scope"].strip(),
                "paper release claim scope missing")
        require(contract.get("claim_scope") == PAPER_CLAIM_SCOPES[key],
                f"paper release claim scope changed without reviewed revision: {key}")
        require(contract.get("narrower_scope_policy") == "separate_reviewed_contract_no_effect_claim",
                "narrower claims require a separate reviewed release contract")
        required = set(papers[key]["mapped_task_ids"])
        if key in {"CW-P09", "CW-P13", "CW-P15"}:
            required.update({"CW-E06", "CW-F06", "CW-N29", "CW-H08"})
            expected_class = "organizational_transfer" if key == "CW-P15" else "organizational_effect"
            require(contract.get("claim_class") == expected_class, f"field claim scope silently changed: {key}")
        if key in {"CW-P06", "CW-P07", "CW-P08"}:
            required.update({"CW-H01", "CW-N17", "CW-N18", "CW-H05", "CW-H06", "CW-N20"})
            require(contract.get("claim_class") == "simulation_comparison", f"comparison scope changed: {key}")
        gates = contract.get("required_gates")
        require(isinstance(gates, list) and gates, f"required paper gates missing: {key}")
        actual = []
        for gate in gates:
            task_id = gate.get("task_id")
            require(task_id in tasks and task_id not in actual, f"invalid or duplicate paper gate: {key}")
            actual.append(task_id)
            require(gate.get("type") == "requires_evidence" and isinstance(gate.get("reason"), str)
                    and gate["reason"].strip(), f"untyped paper evidence gate: {key}")
            wanted_outputs = [output["id"] for output in tasks[task_id]["outputs"]]
            require(gate.get("consumes") == wanted_outputs, f"paper gate consumes the wrong output: {key}/{task_id}")
        require(set(actual) == required, f"required paper evidence gates differ: {key}")
        require(contract.get("release_template_task_ids") == [f"CW-I{n:02}" for n in range(3, 9)],
                f"paper release-stage templates differ: {key}")
    metrics = {"contracts": len(contracts),
               "required_evidence_edges": sum(len(c["required_gates"]) for c in contracts),
               "release_instance_templates": len(contracts), "release_stage_nodes": 6 * len(contracts),
               "native_release_instances_created": 0}
    require(graph.get("paper_release_metrics") == metrics, "paper release metrics do not match contracts")
    return metrics


def instantiate_release_instances(graph):
    """Produce scope-bound release DAG templates; no native tasks or receipts."""
    validate_release_contracts(graph)
    tasks = {row["id"]: row for row in graph["tasks"]}
    result = []
    for contract in graph["paper_release_contracts"]:
        paper_id = contract["paper_id"]
        template_ids = contract["release_template_task_ids"]
        aliases = {key: paper_id + "." + key.removeprefix("CW-") for key in template_ids}
        nodes = []
        for template_id in template_ids:
            node_id = aliases[template_id]
            dependencies = []
            for edge in tasks[template_id]["dependencies"]:
                source = edge["task_id"]
                target = aliases.get(source, source)
                consumes = [value.replace(source + ".", target + ".", 1) for value in edge["consumes"]]
                dependencies.append({"node_id": target, "type": "depends_on", "consumes": consumes,
                                     "reason": "Consumes this artifact's own stage output or required shared input."})
            if template_id == "CW-I03":
                existing = {edge["node_id"] for edge in dependencies}
                for gate in contract["required_gates"]:
                    if gate["task_id"] not in existing:
                        dependencies.append({"node_id": gate["task_id"], "type": "requires_evidence",
                                             "consumes": list(gate["consumes"]), "reason": gate["reason"]})
            nodes.append({"id": node_id, "template_task_id": template_id, "status": "proposed",
                          "external_task_id": None, "execution_assigned": False,
                          "outputs": [{"id": node_id + ".O1", "created": False}],
                          "dependencies": dependencies})
        result.append({"paper_id": paper_id, "claim_class": contract["claim_class"],
                       "claim_scope": contract["claim_scope"], "status": "proposed",
                       "external_artifact_id": None, "release_target_id": aliases["CW-I08"],
                       "nodes": nodes})
    return result


def validate_release_instances(graph, instances):
    """Require actual typed upstream gates in each supplied release DAG template.

    This is structural validation, not evidence acceptance or native admission.
    """
    metrics = validate_release_contracts(graph)
    require(isinstance(instances, list) and len(instances) == metrics["contracts"],
            "release instance coverage differs from paper contracts")
    tasks = {row["id"]: row for row in graph["tasks"]}
    contracts = {row["paper_id"]: row for row in graph["paper_release_contracts"]}
    dependencies = {key: [edge["task_id"] for edge in row["dependencies"]] for key, row in tasks.items()}
    outputs = {output["id"]: key for key, row in tasks.items() for output in row["outputs"]}
    seen, nodes = set(), {}
    for instance in instances:
        paper_id = instance.get("paper_id")
        require(paper_id in contracts and paper_id not in seen, "duplicate or unknown release instance")
        seen.add(paper_id)
        contract = contracts[paper_id]
        for key in ("claim_class", "claim_scope"):
            require(instance.get(key) == contract[key], f"release instance {key} does not match contract: {paper_id}")
        require(instance.get("status") == "proposed" and instance.get("external_artifact_id") is None,
                "release instance claims completed publication")
        expected_ids = {paper_id + f".I{n:02}" for n in range(3, 9)}
        stage_rows = instance.get("nodes")
        require(isinstance(stage_rows, list) and len(stage_rows) == 6
                and {row.get("id") for row in stage_rows} == expected_ids,
                f"release stage identity mismatch: {paper_id}")
        require(instance.get("release_target_id") == paper_id + ".I08", "wrong release target")
        for row in stage_rows:
            key = row["id"]
            require(key not in dependencies and key not in nodes, "release node identifier collision")
            require(row.get("template_task_id") == "CW-" + key.split(".")[-1], "release stage template mismatch")
            require(row.get("status") == "proposed" and row.get("external_task_id") is None
                    and row.get("execution_assigned") is False, "release node claims native execution")
            require(row.get("outputs") == [{"id": key + ".O1", "created": False}], "release stage output mismatch")
            outputs[key + ".O1"] = key
            edges = row.get("dependencies")
            require(isinstance(edges, list) and edges, "release stage requires typed dependencies")
            dependencies[key] = [edge.get("node_id") for edge in edges]
            nodes[key] = row
    for key, node in nodes.items():
        paper_id = key.split(".")[0]
        allowed = set(tasks) | {paper_id + f".I{n:02}" for n in range(3, 9)}
        for edge in node["dependencies"]:
            parent = edge.get("node_id")
            require(parent in allowed, f"foreign artifact cannot satisfy release stage: {key}")
            require(edge.get("type") in {"depends_on", "requires_evidence"}, "advisory release edge is not a gate")
            consumes = edge.get("consumes")
            require(isinstance(consumes, list) and consumes and len(consumes) == len(set(consumes))
                    and all(outputs.get(value) == parent for value in consumes), "release edge consumes wrong output")
        template = tasks[node["template_task_id"]]
        expected_inputs = {paper_id + "." + edge["task_id"].removeprefix("CW-")
                           if edge["task_id"] in {f"CW-I{n:02}" for n in range(3, 9)} else edge["task_id"]
                           for edge in template["dependencies"]}
        require(expected_inputs <= set(dependencies[key]), f"artifact-specific release chain missing: {key}")
    _, _, ancestors = topology(set(dependencies), dependencies)
    for instance in instances:
        paper_id = instance["paper_id"]
        for gate in contracts[paper_id]["required_gates"]:
            require(gate["task_id"] in ancestors[paper_id + ".I03"],
                    f"required paper gate is not upstream: {paper_id}/{gate['task_id']}")
            require(gate["task_id"] in ancestors[instance["release_target_id"]],
                    f"required paper gate does not reach publication: {paper_id}/{gate['task_id']}")
    # Upstream reachability alone cannot prove that this paper instantiated
    # its own typed evidence edge. A generic path through another work package
    # can remain after a required direct gate is removed. Preserve the one
    # existing template dependency (P16/I02) as an explicitly checked overlap.
    for instance in instances:
        paper_id = instance["paper_id"]
        template_inputs = {edge["task_id"] for edge in tasks["CW-I03"]["dependencies"]}
        manuscript_edges = nodes[paper_id + ".I03"]["dependencies"]
        for gate in contracts[paper_id]["required_gates"]:
            required_type = "depends_on" if gate["task_id"] in template_inputs else "requires_evidence"
            matches = [edge for edge in manuscript_edges
                       if edge.get("node_id") == gate["task_id"]
                       and edge.get("type") == required_type
                       and edge.get("consumes") == gate["consumes"]]
            require(len(matches) == 1,
                    f"required direct release evidence edge missing or mistyped: {paper_id}/{gate['task_id']}")
    # A release instance is a deterministic source-bound proposal, not a
    # place to insert additional empirical blockers or rewrite rationales
    # without a reviewed source change. Subset/reachability checks alone
    # accept unrelated extra gates while all required gates remain present.
    canonical = {node["id"]: node["dependencies"]
                 for release in instantiate_release_instances(graph) for node in release["nodes"]}
    for key, node in nodes.items():
        actual = sorted(json.dumps(edge, sort_keys=True, ensure_ascii=False)
                        for edge in node["dependencies"])
        expected = sorted(json.dumps(edge, sort_keys=True, ensure_ascii=False)
                          for edge in canonical[key])
        require(actual == expected, f"release edge provenance differs from source template: {key}")
    return {**metrics, "validated_release_stage_nodes": len(nodes),
            "evidence_acceptance": "NOT_VERIFIED", "native_registration": "NOT_VERIFIED"}


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
        require(task.get("origin") in {"imported", "addition"}, f"unknown task origin: {key}")
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
            original_edges = {"CW-" + edge for edge in original["dependencies"]}
            imported[source_id] = key
        else:
            require(task.get("source_step_id") is None and task.get("source_dependencies") == [],
                    f"addition claims a frozen source baseline: {key}")
            original_edges = set()
        # Every ledger describes the frozen-to-proposed delta. Additions have
        # no frozen source edges, so removed is empty and added is the complete
        # current prerequisite set. Historical proposal corrections live in
        # the source-pinned decision record, not inside this active ledger.
        proposed_edges = set(dependencies[key])
        revision = task.get("dependency_revisions")
        require(isinstance(revision, dict) and set(revision) == {"removed", "added"},
                f"dependency revision ledger missing or malformed: {key}")
        for direction, expected_edges in (("removed", original_edges - proposed_edges),
                                           ("added", proposed_edges - original_edges)):
            entries = revision[direction]
            require(isinstance(entries, list), f"revision {direction} must be an array: {key}")
            ids = []
            for entry in entries:
                require(isinstance(entry, dict)
                        and isinstance(entry.get("task_id"), str) and entry["task_id"].strip()
                        and isinstance(entry.get("reason"), str) and entry["reason"].strip(),
                        f"revision {direction} edge lacks identity or reason: {key}")
                ids.append(entry["task_id"])
            require(len(ids) == len(set(ids)), f"duplicate revision {direction} edge: {key}")
            require(set(ids) == expected_edges,
                    f"revision {direction} differs from frozen-to-proposed edge delta: {key}")
        require(isinstance(task.get("dependency_revision_reason"), str)
                and task["dependency_revision_reason"].strip(),
                f"blank dependency revision rationale: {key}")
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
        # Source-table position and stable paper identity are a single frozen
        # mapping. Swapping both the source index and prose must not allow
        # a different paper to borrow an internally consistent source row.
        require(type(paper.get("source_index")) is int
                and 1 <= paper["source_index"] <= len(original_papers)
                and paper["id"] == f"CW-P{paper['source_index']:02d}",
                f"paper frozen source identity mismatch: {paper['id']}")
        require(paper["mapped_task_ids"] and set(paper["mapped_task_ids"]) <= set(by_id), "paper task coverage incomplete")
        require([paper[k] for k in ("source_title", "source_main_question", "source_engineering_companion")]
                == original_papers[paper["source_index"] - 1], "source paper boundary altered")
        require(paper["outcome"] == "not_evaluated" and paper["external_artifact_id"] is None, "paper promoted to result")
        require(set(paper["release_template_task_ids"]) == {f"CW-I{n:02}" for n in range(3, 9)}, "paper release gates incomplete")
    require({p["source_index"] for p in papers} == set(range(1, 17)), "source16 paper coverage mismatch")
    for hypothesis in hypotheses:
        require(type(hypothesis.get("source_number")) is int
                and 1 <= hypothesis["source_number"] <= len(original_hypotheses)
                and hypothesis["id"] == f"CW-HYP{hypothesis['source_number']:02d}",
                f"hypothesis frozen source identity mismatch: {hypothesis['id']}")
        require(hypothesis["mapped_task_ids"] and set(hypothesis["mapped_task_ids"]) <= set(by_id), "hypothesis task coverage incomplete")
        require([hypothesis[k] for k in ("source_statement", "source_comparison", "source_refutation")]
                == original_hypotheses[hypothesis["source_number"] - 1],
                "source hypothesis/refutation altered")
        require(hypothesis["outcome"] == "unknown", "hypothesis promoted to finding")
        require(hypothesis["registration_task_id"] == "CW-H01" and hypothesis["analysis_task_id"] == "CW-N20",
                "hypothesis preregistration/analysis link lost")
    require({h["source_number"] for h in hypotheses} == set(range(1, 13)), "source12 hypothesis coverage mismatch")

    release_result = validate_release_instances(graph, instantiate_release_instances(graph))
    require(set(dependencies["CW-N28"]) == {"CW-H06", "CW-N16"},
            "reproduction must use a frozen evaluation package, not its own publication release")

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
            "paper_release_contracts": release_result["contracts"],
            "paper_required_evidence_edges": release_result["required_evidence_edges"],
            "release_stage_templates": release_result["validated_release_stage_nodes"],
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
