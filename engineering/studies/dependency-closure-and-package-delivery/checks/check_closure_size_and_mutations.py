#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Measure the published graph and test a small, declared implementation fault model."""
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
LEGACY = HERE.parent / "evidence" / "replay_closure.py"
spec = importlib.util.spec_from_file_location("edition_one_closure", LEGACY)
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


def missing_cycle_guard(roots, deps):
    """Fault: mark a node done on entry and omit the active-cycle rejection."""
    seen = set()
    def visit(key):
        if key in seen:
            return
        if key not in deps:
            raise ValueError("Unknown artifact")
        seen.add(key)
        for child in deps[key]:
            visit(child)
    for root in roots:
        visit(root)
    return seen


def missing_child(roots, deps):
    """Fault: skip the final edge at every expanded vertex."""
    return replay.closure(roots, {k: v[:-1] for k, v in deps.items()})


def unknown_as_leaf(roots, deps):
    """Fault: preserve unknown roots instead of rejecting them."""
    graph = dict(deps)
    for root in roots:
        graph.setdefault(root, [])
    return replay.closure(roots, graph)


def fails_oracle(function, roots, deps, expected=None, must_reject=False):
    try:
        result = function(roots, deps)
    except ValueError:
        return not must_reject
    return must_reject or result != expected


def main():
    raw = (HERE.parent / "evidence" / "dependency-graph.json").read_bytes()
    graph = json.loads(raw)
    deps = graph["dependencies"]
    layout = json.loads((HERE.parent / "evidence" / "layout-preservation-report.json").read_bytes())
    names = {row["artifact_id"].split(":")[-1]: Path(row["path"]).stem for row in layout["items"]}
    roots = graph["skill_roots"] + ["R01", "R02", "B01", "B02", "A01"]
    sizes = [{"root": root, "readable_name": names[root],
              "records": len(replay.closure([root], deps))} for root in roots]
    cycle = {"one": ["two"], "two": ["one"]}
    chain = {"root": ["child"], "child": ["leaf"], "leaf": []}
    cases = [
        ("cycle_must_reject", ["one"], cycle, None, True),
        ("all_children_required", ["root"], chain, {"root", "child", "leaf"}, False),
        ("unknown_root_must_reject", ["absent"], deps, None, True),
    ]
    controls = {name: not fails_oracle(replay.closure, roots_, deps_, expected, reject)
                for name, roots_, deps_, expected, reject in cases}
    mutation_rows = []
    for name, function in [("omit_cycle_guard", missing_cycle_guard),
                           ("skip_required_child", missing_child),
                           ("unknown_root_as_leaf", unknown_as_leaf)]:
        detected_by = [case for case, roots_, deps_, expected, reject in cases
                       if fails_oracle(function, roots_, deps_, expected, reject)]
        mutation_rows.append({"mutation": name, "detected_by": detected_by,
                              "detected": bool(detected_by)})
    checks = {
        "unchanged_implementation_matches_three_oracles": all(controls.values()),
        "all_three_declared_mutants_detected": all(row["detected"] for row in mutation_rows),
        "pilot_roots_deliver_108": len(replay.closure(["B01", "R01", "R02"], deps)) == 108,
    }
    report = {
        "schema": "knowledge-contract.closure-size-and-mutation-check/1",
        "graph_sha256": hashlib.sha256(raw).hexdigest(),
        "vertices": len(deps), "required_edges": sum(len(v) for v in deps.values()),
        "single_root_closures": sizes,
        "all_skill_roots_records": len(replay.closure(graph["skill_roots"], deps)),
        "pilot_roots": ["B01", "R01", "R02"],
        "pilot_root_closure_records": len(replay.closure(["B01", "R01", "R02"], deps)),
        "positive_and_negative_oracles": controls, "mutations": mutation_rows,
        "checks": checks, "passed": all(checks.values()),
        "scope": "New post-review metadata measurement and three hand-selected implementation mutants. Counts are records, not bytes or tokens. No semantic dependency completeness, historical rerun of the full package, or general mutation adequacy is claimed.",
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
