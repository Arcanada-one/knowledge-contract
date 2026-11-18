#!/usr/bin/env python3
"""Verify saved raw observations against independent fixtures and physical bounds."""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from analytical_bound import cut_bounds, shipment_upper_bound


def n(value):
    return Q(str(value))


def main():
    base = Path(__file__).parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=base/'cases.json')
    parser.add_argument('--actual', type=Path, default=base/'raw_results.json')
    parser.add_argument('--expected', type=Path, default=base/'expected_results.json')
    parser.add_argument('--report', type=Path, default=base/'verification_report.json')
    args = parser.parse_args()
    raw_input = args.inputs.read_bytes()
    cases = {c['id']: c for c in json.loads(raw_input)['cases']}
    actual_doc = json.loads(args.actual.read_text())
    actual = {r['case_id']: r for r in actual_doc['results']}
    expected = {r['case_id']: r for r in json.loads(args.expected.read_text())['expected']}
    checks = []
    def check(name, condition, details=None):
        checks.append(dict(check=name, passed=bool(condition), details=details))
    check('input_digest', actual_doc['input_sha256'] == hashlib.sha256(raw_input).hexdigest())
    check('case_ids', set(cases) == set(actual) == set(expected))
    for case_id, case in cases.items():
        result = actual[case_id]
        exp = expected[case_id]
        series = result['series']
        check(case_id+':horizon', len(series) == case['horizon_periods'])
        for key, value in exp['totals'].items():
            check(case_id+':fixture:totals:'+key, n(result['totals'][key]) == n(value))
        for key, value in exp['ending_inventory'].items():
            check(case_id+':fixture:inventory:'+key, n(result['ending_inventory'][key]) == n(value))
        check(case_id+':fixture:each_period_shipped', all(n(s['shipped']) == n(exp['shipped_each_period']) for s in series))
        bound = shipment_upper_bound(case)
        check(case_id+':independent_bound', n(result['totals']['shipped']) <= bound, {'upper_bound':str(bound), 'cuts':{key:str(value) for key,value in cut_bounds(case).items()}})
        prev12 = prev23 = prevfg = Q(0)
        accumulated = {key:Q(0) for key in ('admitted','stage_2_processed','stage_3_processed','shipped','unused_supply')}
        valid = True
        for s in series:
            a,b,c,d = (n(s[key]) for key in ('admitted','stage_2_processed','stage_3_processed','shipped'))
            q12,q23,fg = (n(s[key]) for key in ('buffer_12_end','buffer_23_end','finished_goods_end'))
            valid &= min(a,b,c,d,q12,q23,fg) >= 0
            valid &= q12 == prev12+a-b and q23 == prev23+b-c and fg == prevfg+c-d
            valid &= a <= n(case['supply_per_period']) and a <= n(case['release_limit_per_period']) and d <= n(case['demand_per_period'])
            for processed, stage in zip((a,b,c),case['stages']):
                valid &= processed*n(stage['work_units_per_good_unit']) <= n(stage['nominal_capacity_per_period'])*n(stage['availability_fraction'])
            valid &= n(s['unused_supply']) == n(case['supply_per_period'])-a
            prev12,prev23,prevfg = q12,q23,fg
            for key in accumulated: accumulated[key] += n(s[key])
            valid &= n(s['cumulative_shipped']) == accumulated['shipped']
        check(case_id+':period_balances_and_resource_limits',valid)
        check(case_id+':reported_totals',all(accumulated[key]==n(result['totals'][key]) for key in accumulated))
        check(case_id+':system_conservation',n(result['totals']['admitted'])==n(result['totals']['shipped'])+sum(n(value) for value in result['ending_inventory'].values()))
    def shipped(cid):return n(actual[cid]['totals']['shipped'])
    check('paired:admission_limit_same_output',shipped('base_local')==shipped('base_gated'))
    check('paired:admission_limit_less_wip',n(actual['base_gated']['ending_inventory']['buffer_12'])<n(actual['base_local']['ending_inventory']['buffer_12']))
    check('paired:non_bottleneck_boost_same_output',shipped('base_local')==shipped('non_bottleneck_boost'))
    check('paired:bottleneck_boost_more_output',shipped('bottleneck_boost')>shipped('base_gated'))
    check('counterexample:setup_below_nominal_min',shipped('setup_loss')<10*min(n(s['nominal_capacity_per_period']) for s in cases['setup_loss']['stages']))
    check('counterexample:rework_below_nominal_min',shipped('rework_overhead')<10*min(n(s['nominal_capacity_per_period']) for s in cases['rework_overhead']['stages']))
    failures=[c['check'] for c in checks if not c['passed']]
    report=dict(status='PASS' if not failures else 'FAIL', classification='finite numerical and conservation checks only; no empirical or agent validation; no universal stability claim', cases=len(cases),checks_count=len(checks), failures=failures, checks=checks)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','cases','checks_count','failures')},ensure_ascii=False))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
