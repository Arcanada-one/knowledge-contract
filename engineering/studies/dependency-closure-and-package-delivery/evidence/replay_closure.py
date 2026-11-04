#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the published finite dependency graph, without source books or a model.
The DFS follows the original package algorithm; the reference is a least fixed point.
This verifies graph laws only. It does not replay the complete package's 46 checks.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def closure(roots, deps):
    done = set()
    active = set()

    def visit(key):
        if key not in deps:
            raise ValueError('Unknown artifact ' + key)
        if key in active:
            raise ValueError('Dependency cycle ' + key)
        if key in done:
            return
        active.add(key)
        for child in deps[key]:
            visit(child)
        active.remove(key)
        done.add(key)

    for key in roots:
        visit(key)
    return done


def reference_closure(roots, deps):
    result = set(roots)
    while True:
        enlarged = result | {child for node in result for child in deps[node]}
        if enlarged == result:
            return result
        result = enlarged


def main():
    raw = (HERE / 'dependency-graph.json').read_bytes()
    data = json.loads(raw)
    deps = data['dependencies']
    skills = data['skill_roots']
    closures = {}
    failures = {'reference': [], 'idempotence': [], 'union': [], 'monotonicity': []}
    singles = {root: reference_closure([root], deps) for root in skills}
    for mask in range(1 << len(skills)):
        roots = [root for bit, root in enumerate(skills) if mask >> bit & 1]
        actual = closure(roots, deps)
        closures[mask] = actual
        if actual != reference_closure(roots, deps):
            failures['reference'].append(mask)
        if closure(actual, deps) != actual:
            failures['idempotence'].append(mask)
        if actual != set().union(*(singles[root] for root in roots)):
            failures['union'].append(mask)
    pairs = 0
    for mask, actual in closures.items():
        for bit in range(len(skills)):
            if not (mask >> bit & 1):
                pairs += 1
                if not actual <= closures[mask | (1 << bit)]:
                    failures['monotonicity'].append([mask, bit])
    controls = {}
    for name, roots, graph in [('unknown_root', ['absent'], deps),
                               ('cycle', ['one'], {'one': ['two'], 'two': ['one']})]:
        try:
            closure(roots, graph)
        except ValueError:
            controls[name] = True
        else:
            controls[name] = False
    passed = not any(failures.values()) and all(controls.values())
    result = {'schema': 'knowledge-contract.public-closure-replay/1',
              'graph_sha256': hashlib.sha256(raw).hexdigest(),
              'vertex_count': len(deps), 'skill_subsets': len(closures),
              'inclusion_pairs': pairs, 'failures': failures,
              'negative_controls_rejected': controls, 'passed': passed,
              'scope': 'New replay of the extracted historical required-dependency graph; not the complete historical package selftest, semantic validation, source-quality verification, or a model trial.'}
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
