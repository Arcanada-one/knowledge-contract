#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact arithmetic and finite counterexamples for the analytical reuse report.

All inputs are newly authored synthetic examples. No timings, model costs,
authorization service, or historical package execution are simulated as observed.
"""
from fractions import Fraction
import json


def costs(n, h, g, r, v, fixed):
    cold = n * g
    reused = fixed + n * v + n * h * r + n * (1 - h) * g
    margin = h * (g - r) - v
    return cold, reused, cold - reused, margin


def main():
    scenarios = []
    for name, args in [
        ('high_hit_rate_loses', (100, Fraction(9, 10), 10, 1, 9, 0)),
        ('positive_margin_with_fixed_cost', (100, Fraction(9, 10), 10, 1, 1, 100)),
        ('zero_margin_never_repays_fixed_cost', (100, Fraction(1, 2), 10, 2, 4, 100)),
    ]:
        cold, reused, saving, margin = costs(*args)
        n, _, _, _, _, fixed = args
        scenarios.append({'name': name, 'cold_cost': str(cold),
                          'reuse_cost': str(reused), 'saving': str(saving),
                          'per_request_margin': str(margin),
                          'identity_holds': saving == n * margin - fixed})

    # A declared dependency set can remain equal while an omitted premise changes.
    before = {'value': 3, 'legend_sign': 1}
    after = {'value': 3, 'legend_sign': -1}
    declared_dependencies_equal = before['value'] == after['value']
    omitted_dependency_changes_result = (before['value'] * before['legend_sign']
                                         != after['value'] * after['legend_sign'])

    # An empty positive read-set cannot describe an exhaustive negative answer.
    old_domain = []
    new_domain = ['matching-item']
    old_positive_readset = set(old_domain)
    old_members_unchanged = all(x in new_domain for x in old_positive_readset)
    negative_answer_changed = (len(old_domain) == 0) != (len(new_domain) == 0)

    # Local logical gates are inputs, not authenticated authorization decisions.
    def admit(gates):
        return bool(gates) and all(value == 'pass' for value in gates.values())

    gate_inputs = {'integrity': 'pass', 'current_authority': 'pass', 'scope': 'pass'}
    mutations_rejected = []
    for gate in gate_inputs:
        for state in ['fail', 'unknown']:
            trial = dict(gate_inputs)
            trial[gate] = state
            mutations_rejected.append(not admit(trial))

    # Strict threshold for expected h; this does not assert an integer hit count.
    _, _, _, margin = costs(100, Fraction(9, 10), 10, 1, 1, 100)
    first_profitable_expected_n = (Fraction(100) // margin) + 1
    before_threshold = costs(first_profitable_expected_n - 1, Fraction(9, 10), 10, 1, 1, 100)[2]
    at_threshold = costs(first_profitable_expected_n, Fraction(9, 10), 10, 1, 1, 100)[2]
    checks = {
        'all_cost_identities_hold': all(row['identity_holds'] for row in scenarios),
        'ninety_percent_hits_can_lose': Fraction(scenarios[0]['saving']) == -90,
        'positive_synthetic_margin_saves_610': Fraction(scenarios[1]['saving']) == 610,
        'zero_margin_leaves_fixed_loss': Fraction(scenarios[2]['saving']) == -100,
        'expected_break_even_is_strict': before_threshold <= 0 < at_threshold,
        'equal_incomplete_dependencies_do_not_preserve_result': declared_dependencies_equal and omitted_dependency_changes_result,
        'unchanged_positive_readset_does_not_preserve_absence': old_members_unchanged and negative_answer_changed,
        'all_required_gates_pass_positive_control': admit(gate_inputs),
        'all_six_fail_unknown_mutations_rejected': all(mutations_rejected),
        'independent_cache_savings_double_count': (10 - 6) + (10 - 1) > (10 - 1),
    }
    result = {'schema': 'knowledge-contract.synthetic-reuse-analysis/1',
              'scenarios': scenarios, 'first_profitable_expected_n': first_profitable_expected_n,
              'checks': checks, 'passed': all(checks.values()),
              'scope': 'New deterministic illustrations of logical and algebraic counterexamples. All costs are unitless synthetic inputs; no measured savings, runtime performance, real authorization, or semantic truth is claimed.'}
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
