#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Finite synthetic controls for four editorial clarifications; not a runtime test."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


def main() -> int:
    results: list[dict[str, object]] = []

    def record(case: str, expected: object, observed: object, scope: str) -> None:
        results.append({"id": case, "expected": expected, "observed": observed,
                        "pass": expected == observed, "scope": scope})

    states = (0, 1)
    identity_paths = [(x, x, x) for x in states]
    observed = {
        "state_paths": identity_paths,
        "within_step_preservation": all(x == y and 1-y == 1-z
                                        for x, y, z in identity_paths),
        "endpoint_observations_equal": [x == 1-z for x, _, z in identity_paths],
    }
    record("E01-state-versus-observation", {
        "state_paths": [(0, 0, 0), (1, 1, 1)],
        "within_step_preservation": True,
        "endpoint_observations_equal": [False, False],
    }, observed, "Two Boolean states; two identity transitions; mismatched observation interface.")

    identity_relation = ((0, 0), (1, 1))
    branching_relation = ((0, 0), (0, 1))
    record("E02-universal-output", {
        "positive_all_preserve": True, "favorable_sample_preserves": True,
        "all_branching_outputs_preserve": False,
    }, {
        "positive_all_preserve": all(x == y for x, y in identity_relation),
        "favorable_sample_preserves": branching_relation[0][0] == branching_relation[0][1],
        "all_branching_outputs_preserve": all(x == y for x, y in branching_relation),
    }, "Two explicitly enumerated finite relations; a favorable sample is not universal preservation.")

    path_checks = [(x, x == 1, x == 1) for x in states]
    record("E03-precondition-boundary", [(0, False, False), (1, True, True)],
           path_checks, "Identity followed by constant-one; columns are input, second precondition, endpoint equality.")

    incompatible = ({"a"}, {"b"})
    compatible = ({"a", "b"},)
    required = {"a", "b"}
    record("E04-coherent-snapshot", {
        "union_covers": True, "one_incompatible_snapshot_covers": False,
        "one_compatible_snapshot_covers": True,
    }, {
        "union_covers": required <= set().union(*incompatible),
        "one_incompatible_snapshot_covers": any(required <= s for s in incompatible),
        "one_compatible_snapshot_covers": any(required <= s for s in compatible),
    }, "Two requirements; two incompatible fixed snapshots and a positive coherent snapshot.")

    universe = {"a", "b", "c"}
    packages = ({"a", "b"}, {"b", "c"}, {"a"})
    selection_checks = []
    for bits in itertools.product((False, True), repeat=len(packages)):
        chosen = [i for i, bit in enumerate(bits) if bit]
        candidate = set().union(*(packages[i] for i in chosen))
        delivered_records = [(i, frozenset(packages[i])) for i in chosen]
        delivered = set().union(*(payload for _, payload in delivered_records))
        for budget in range(len(packages) + 1):
            cover_feasible = candidate >= universe and len(chosen) <= budget
            delivery_feasible = delivered >= universe and len(delivered_records) <= budget
            selection_checks.append(cover_feasible == delivery_feasible)
    record("E05-intact-unit-cost-cover", {"comparisons": 32, "equal": True},
           {"comparisons": len(selection_checks), "equal": all(selection_checks)},
           "Eight subsets of three packages, budgets 0..3; literal intact payload and one cost unit per package.")

    chosen = (0, 1)
    candidate = packages[0] | packages[1]
    corrupted_delivery = packages[0] | (packages[1] - {"c"})
    record("E06-lossful-delivery-control", {
        "candidate_covers": True, "delivered_covers": False,
        "declared_unit_cost": 2,
    }, {
        "candidate_covers": candidate >= universe,
        "delivered_covers": corrupted_delivery >= universe,
        "declared_unit_cost": len(chosen),
    }, "The same covering selection at budget two, with one required delivered coordinate deliberately removed.")

    report = {
        "scope": "new_finite_synthetic_editorial_examples",
        "effects_authorized": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "case_groups": len(results),
        "passed_groups": sum(bool(row["pass"]) for row in results),
        "cases": results,
        "limits": "Not a proof, historical replay, semantic extraction evaluation, repository-wide test suite, model trial, or production admission.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(row["pass"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
