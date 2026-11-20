#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Deterministic three-stage fluid illustration. Standard library only."""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


def quantity(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a quantity')
    return Fraction(str(value))


def out_number(value):
    return value.numerator if value.denominator == 1 else str(value)


def simulate(case):
    horizon = case['horizon_periods']
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError('horizon_periods must be a positive integer')
    if len(case['stages']) != 3:
        raise ValueError('Exactly three stages are required')
    supply = quantity(case['supply_per_period'])
    demand = quantity(case['demand_per_period'])
    release = quantity(case['release_limit_per_period'])
    if min(supply, demand, release) < 0:
        raise ValueError('Supply, demand and release must be nonnegative')
    effective = []
    for stage in case['stages']:
        nominal = quantity(stage['nominal_capacity_per_period'])
        available = quantity(stage['availability_fraction'])
        work = quantity(stage['work_units_per_good_unit'])
        if nominal < 0 or not 0 <= available <= 1 or work <= 0:
            raise ValueError('Invalid stage capacity, availability, or work content')
        effective.append(nominal * available / work)
    b12 = b23 = finished = Fraction(0)
    totals = {key: Fraction(0) for key in ('admitted', 'stage_2_processed', 'stage_3_processed', 'shipped', 'unused_supply', 'unserved_demand')}
    series = []
    for period in range(1, horizon + 1):
        # Zero transit lag: output may be processed by the next stage this period.
        admitted = min(supply, release, effective[0])
        stage2 = min(b12 + admitted, effective[1])
        b12 += admitted - stage2
        stage3 = min(b23 + stage2, effective[2])
        b23 += stage2 - stage3
        finished += stage3
        shipped = min(finished, demand)
        finished -= shipped
        # Potential demand is period-specific; unmet units are tracked, not queued.
        flows = dict(admitted=admitted, stage_2_processed=stage2, stage_3_processed=stage3, shipped=shipped, unused_supply=supply-admitted, unserved_demand=demand-shipped)
        for key, value in flows.items():
            totals[key] += value
        series.append(dict(period=period, **{key: out_number(value) for key, value in flows.items()}, buffer_12_end=out_number(b12), buffer_23_end=out_number(b23), finished_goods_end=out_number(finished), cumulative_shipped=out_number(totals['shipped']), cumulative_unserved_demand=out_number(totals['unserved_demand'])))
    return dict(case_id=case['id'], horizon_periods=horizon,
                effective_good_unit_capacity_per_period=[out_number(c) for c in effective],
                totals={key: out_number(value) for key, value in totals.items()},
                ending_inventory=dict(buffer_12=out_number(b12), buffer_23=out_number(b23), finished_goods=out_number(finished)),
                series=series)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).with_name('cases.json'))
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('raw_results.json'))
    args = parser.parse_args()
    raw_input = args.inputs.read_bytes()
    spec = json.loads(raw_input)
    results = [simulate(case) for case in spec['cases']]
    payload = dict(probe='three_stage_fluid_v2', revision=2, origin=spec['origin'], classification='mathematical illustration; finite regression; not agent evaluation or empirical validation; unserved potential demand tracked without customer-backlog dynamics', input_sha256=hashlib.sha256(raw_input).hexdigest(), units=spec['units'], results=results)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(output=str(args.out.resolve()), cases=len(results))))


if __name__ == '__main__':
    main()
