#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Synthetic admission counterexamples and cost examples for the corrected study.

This does not authenticate a permission or replay a historical production run.
The edition-1.0 program and its output remain unchanged in ../evidence/.
"""
from fractions import Fraction
import json


REQUIRED_GATES = (
    "integrity", "result_class", "task_requirements", "dependency_equivalence",
    "current_access", "temporal_policy", "permitted_transformations",
    "modality_delivery", "budget",
)


def admit(gates):
    """All nine named gates are applicable in this deliberately finite profile."""
    return (type(gates) is dict and set(gates) == set(REQUIRED_GATES)
            and all(type(gates[name]) is str and gates[name] == "pass"
                    for name in REQUIRED_GATES))


def costs(n, hit_fraction, cold_cost, reuse_cost, validation_cost, overhead):
    cold = n * cold_cost
    reused = (overhead + n * validation_cost + n * hit_fraction * reuse_cost
              + n * (1 - hit_fraction) * cold_cost)
    margin = hit_fraction * (cold_cost - reuse_cost) - validation_cost
    return cold, reused, cold - reused, margin


def main():
    all_pass = dict.fromkeys(REQUIRED_GATES, "pass")
    cases = []
    for gate in REQUIRED_GATES:
        for mutation in ("missing", "fail", "unknown"):
            trial = all_pass.copy()
            if mutation == "missing":
                del trial[gate]
            else:
                trial[gate] = mutation
            cases.append({"gate": gate, "mutation": mutation,
                          "rejected": not admit(trial)})
    malformed = {
        "empty": {}, "one_gate_only": {"integrity": "pass"},
        "unknown_extra_gate": dict(all_pass, extra="pass"),
        "unjustified_not_applicable": dict(all_pass, budget="not_applicable"),
        "boolean_is_not_pass": dict(all_pass, integrity=True),
        "not_an_object": [],
    }
    worked_examples = []
    for name, args in [
        ("high_hit_rate_loses", (100, Fraction(9, 10), 10, 1, 9, 0)),
        ("positive_margin_with_fixed_cost", (100, Fraction(9, 10), 10, 1, 1, 100)),
        ("zero_margin_leaves_fixed_loss", (100, Fraction(1, 2), 10, 2, 4, 100)),
        ("storage_grows_per_request", (100, Fraction(9, 10), 10, 1, 1, 100 + 8 * 100)),
    ]:
        cold, reused, saving, margin = costs(*args)
        worked_examples.append({
            "name": name, "cold_cost": str(cold), "reuse_cost": str(reused),
            "saving": str(saving), "margin_before_overhead": str(margin),
            "identity_holds": saving == args[0] * margin - args[-1],
        })
    margin = Fraction(71, 10)
    first_profitable_n = (Fraction(100) // margin) + 1
    # These two explicit dependency models illustrate premises, not real evidence.
    before = {"value": 3, "legend_sign": 1}
    after = {"value": 3, "legend_sign": -1}
    old_domain, new_domain = [], ["matching-item"]
    checks = {
        "positive_control_admitted": admit(all_pass),
        "all_27_required_gate_mutations_rejected": all(c["rejected"] for c in cases),
        "all_malformed_inputs_rejected": all(not admit(v) for v in malformed.values()),
        "arithmetic_examples_agree_with_identity": all(x["identity_holds"] for x in worked_examples),
        "strict_fixed_overhead_threshold": (first_profitable_n - 1) * margin <= 100 < first_profitable_n * margin,
        "growing_storage_reverses_savings": Fraction(worked_examples[-1]["saving"]) == -190,
        "omitted_dependency_changes_meaning": before["value"] == after["value"] and before["value"] * before["legend_sign"] != after["value"] * after["legend_sign"],
        "new_domain_member_changes_absence": all(x in new_domain for x in old_domain) and (not old_domain) != (not new_domain),
        "adding_two_savings_against_one_baseline_double_counts": (10 - 6) + (10 - 1) > 10 - 1,
    }
    report = {
        "schema": "knowledge-contract.synthetic-reuse-analysis/2",
        "required_gates": list(REQUIRED_GATES), "mutation_count": len(cases),
        "gate_mutations": cases, "malformed_cases": list(malformed),
        "worked_cost_examples": worked_examples,
        "first_profitable_expected_n_fixed_overhead": first_profitable_n,
        "checks": checks, "passed": all(checks.values()),
        "scope": "New finite synthetic gate checks and exact arithmetic examples. All nine named gates are required and applicable here; not_applicable has no witness in this profile and is rejected. No authenticated authority, real cost measurement, general semantic proof or historical rerun is claimed.",
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
