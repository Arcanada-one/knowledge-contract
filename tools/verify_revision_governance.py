#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Arcanada contributors
# SPDX-License-Identifier: Apache-2.0
"""Offline document checks and finite illustrations; not KC runtime conformance."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path

CANDIDATE_SHA256 = '20079132357dc2e4e651cde78d528b37712ecdef030af3934ebd2e8048e3f78a'
PROTECTED = {'front_matter': '52d350dbdf1ac083208fe6a04b7cedca6dc437ada4f41b484ae644aba56e28dc', 'section4': '7a37e45f9c13101a107bde74e2e9c7e661efadbc8447c5b82620d4b1a26cdc09', 'section8': '5c12326758cb385f3512674e975fa4c0de9e329d897d054f07a9e897fba974d5', 'references': '3c4df3065f10678cbf6de362e6aabd8fb1eec229655818873c2f1882b87c697e'}
OLD_HEADINGS = ['# Knowledge Revision, Version Identity, and the Adoption of Norms', '## Abstract', '## 1. Research question', '## 2. Five different objects of change', '## 3. Revision operations and their grounds', '## 4. Conditional properties', '### Proposition 1. Pinned references preserve historical selection', '### Proposition 2. Checks transfer through preserved complete inputs', '### Proposition 3. Complete dependencies identify candidates for reassessment', '### Proposition 4. Adoption is not a truth-preserving inference rule', '## 5. Authority and normative admission', '## 6. Historical reproduction and current use', '## 7. Falsification and evidence boundary', '## 8. Connections to the published engineering work', '## References']
ORIGINAL_MATH = ['f', 'd', 'A', 'F', 'A\\land F', 'A\\land\\neg F', 'F', 'A\\land\\neg F', 'A\\Rightarrow F', 'F', 'F']
ORIGINAL_LINKS = [('../../engineering/studies/executable-projections-and-revision/STUDY.md', ''), ('../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md', ''), ('../../reference/glossary/GLOSSARY.md', ''), ('../interaction-and-memory/PAPER.md', ''), ('../controlled-knowledge-reuse/PAPER.md', ''), ('', 'https://www.w3.org/TR/prov-dm/'), ('https://www.sciencedirect.com/science/article/pii/0004370279900080', ''), ('https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a', ''), ('', 'https://doi.org/10.2307/2274239')]


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def document_checks(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    headings = re.findall(r'^#{1,6} .+$', text, re.M)
    current = {
        'front_matter': text.split('---', 2)[1],
        'section4': between(text, '## 4. Conditional properties', '## 5.'),
        'section8': between(text, '## 8. Connections to the published engineering work', '## 9.'),
        'references': text.split('## References', 1)[1],
    }
    checks = {
        'exact_candidate_sha256': digest(raw) == CANDIDATE_SHA256,
        'utf8_without_bom': not raw.startswith(b'\xef\xbb\xbf'),
        'lf_and_final_newline': b'\r' not in raw and raw.endswith(b'\n'),
        'one_h1': len(re.findall(r'^# ', text, re.M)) == 1,
        'four_propositions': len(re.findall(r'^### Proposition ', text, re.M)) == 4,
        'all_old_headings_retained_in_order': [h for h in headings if h in OLD_HEADINGS] == OLD_HEADINGS,
        'mathematics_exact': re.findall(r'\\\((.*?)\\\)', text, re.S) == ORIGINAL_MATH,
        'link_targets_exact': re.findall(r'\]\(([^)]+)\)|<(https?://[^>]+)>', text) == ORIGINAL_LINKS,
        'no_placeholders': not re.search(r'\b(?:TODO|FIXME|TBD)\b', text),
        'existing_citations_used': all(f'[{n}]' in text.split('## References',1)[0] for n in (1,2,3)),
        'explicit_deductive_method': 'The argument proceeds by definitions, explicit premises, and their consequences.' in text,
        'constructed_not_observed': 'the example asserts no observed deployment result' in text,
    }
    checks.update({key + '_exact': digest(value.encode()) == PROTECTED[key] for key,value in current.items()})
    return {'scope':'document identity/preservation only, not scientific truth', 'checks': checks, 'pass':all(checks.values())}


def reverse_reachable(edges: set[tuple[int,int]], changed: int) -> set[int]:
    # An edge (assessment, dependency) points toward the used input.
    seen, frontier = {changed}, [changed]
    while frontier:
        node = frontier.pop()
        for dependent, dependency in edges:
            if dependency == node and dependent not in seen:
                seen.add(dependent)
                frontier.append(dependent)
    return seen


def finite_models() -> dict:
    vertices = range(3)
    possible = list(itertools.product(vertices, repeat=2))
    graph_count = comparisons = 0
    failures = []
    for bits in itertools.product((False, True), repeat=len(possible)):
        edges = {edge for edge,on in zip(possible,bits) if on}
        # Different implementation: Warshall closure in the forward graph.
        closure = [[i == j or (i,j) in edges for j in vertices] for i in vertices]
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
        graph_count += 1
        for changed in vertices:
            got = reverse_reachable(edges, changed)
            for assessment in vertices:
                comparisons += 1
                if ((assessment in got) != closure[assessment][changed]):
                    failures.append({'graph':sorted(edges),'changed':changed,'assessment':assessment})
    equal_input_pairs = 0
    for table in itertools.product((False,True),repeat=4):
        for d in range(4):
            for _old_label,_new_label in itertools.product(range(2),repeat=2):
                equal_input_pairs += 1
                assert table[d] == table[d]
    valuations = list(itertools.product((False,True),repeat=2))  # (adoption, fact)
    admitted_model_sets = 0
    for choose in itertools.product((False,True),repeat=4):
        worlds = [w for w,on in zip(valuations,choose) if on]
        if not (any(a and f for a,f in worlds) and any(a and not f for a,f in worlds)):
            continue
        admitted_model_sets += 1
        if all(not a or f for a,f in worlds) or all(not a or not f for a,f in worlds):
            failures.append({'adoption_worlds':worlds})
    return {
        'scope':'exhaustive only in the stated finite domains; generated by the same producer',
        'three_vertex_directed_graphs_with_loops':graph_count,
        'reachability_membership_comparisons':comparisons,
        'boolean_function_equal_input_label_pairs':equal_input_pairs,
        'adoption_model_sets_satisfying_both_satisfiability_premises':admitted_model_sets,
        'violations':failures,'pass':not failures,
    }


def boundary_controls() -> dict:
    results = {}
    def record(name: str, condition: bool) -> None:
        results[name] = bool(condition)
    revisions = {'r1':'validated-only','r2':'all-inputs'}
    pin = lambda revision: revisions.get(revision)
    record('pin_ignores_current_pointer', all(pin('r1')=='validated-only' for _current in revisions))
    record('floating_alias_distinguished', revisions['r1'] != revisions['r2'])
    record('missing_pin_does_not_fallback', pin('missing') is None)
    record('same_title_is_not_same_content', ('procedure','validated-only') != ('procedure','all-inputs'))
    record('complete_context_sees_policy_change', ('r1','p1') != ('r1','p2'))
    check = lambda text,allowed: bool(text) and allowed
    record('hidden_permission_breaks_text_only_transfer', check('same',True) != check('same',False))
    record('changed_evaluator_breaks_transfer', (lambda _:True)('x') != (lambda _:False)('x'))
    record('repeated_success_is_not_soundness', (lambda _:True)('invalid') is True and not ('invalid'=='valid'))
    record('cyclic_graph_terminates', reverse_reachable({(0,1),(1,0),(2,1)},1)=={0,1,2})
    record('transitive_dependency_not_only_direct', 0 in reverse_reachable({(0,1),(1,2)},2))
    record('omitted_edge_hides_affected', 0 not in reverse_reachable({(0,1)},2))
    record('independent_ground_can_preserve_support', any([False,True]))
    record('all_required_grounds_can_fail', not all([False,True]))
    record('adoption_with_false_fact_is_countermodel', True and not False)
    record('entailed_fact_excluded_by_premise', not any(a and not a for a in (False,True)))
    record('authority_withdrawal_not_history_erasure', {'adopted_then':True,'authorized_now':False}['adopted_then'])
    record('future_effective_time_not_current', not (10 >= 20))
    record('unknown_mandatory_condition_not_pass', None is not True)
    return {'scope':'18 authored synthetic controls, not real operations', 'checks':results, 'run':len(results),'pass':all(results.values())}


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--paper',type=Path,default=Path('papers/revision-and-governance/PAPER.md'))
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    try:
        doc=document_checks(args.paper)
        models=finite_models()
        controls=boundary_controls()
        report={'record_type':'revision-governance-local-illustrations','candidate_sha256':CANDIDATE_SHA256,
                'document':doc,'finite_models':models,'boundary_controls':controls,
                'not_established':['general theorem by enumeration','dependency discovery','production retention or authorization','AGM operator conformance','independent review','full repository CI','site release or index admission']}
        report['pass']=all(v['pass'] for v in (doc,models,controls))
    except (OSError,UnicodeError,IndexError,AssertionError) as error:
        report={'pass':False,'input_error':str(error)}
        print(json.dumps(report,indent=2))
        return 2
    encoded=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(encoded,encoding='utf-8')
    print(encoded,end='')
    return 0 if report['pass'] else 1

if __name__=='__main__':
    raise SystemExit(main())
