#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate a bounded reading map; do not infer truth, task readiness or grants."""
from __future__ import annotations
import argparse
import collections
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

GROUPS = ('documents', 'terms', 'claims', 'foundation_units', 'roadmap_nodes')
SHAPES = {
    'uses-term': ('document', 'term'),
    'states-bounded-claim': ('document', 'claim'),
    'has-candidate': ('manuscript-unit', 'document'),
    'extends-existing-path': ('manuscript-unit', 'document'),
    'addresses-planned-scope': ('manuscript-unit', 'research-work-definition'),
    'informs-not-blocks': ('research-work-definition', 'research-work-definition'),
    'reading-interface': ('document', 'document'),
}
# Proposed /2 adds descriptive traceability from a claim revision to external sources.
SHAPES_V2 = {**SHAPES,
    'claim-has-ground': ('claim', 'evidence-assessment'),
    'ground-uses-source': ('evidence-assessment', 'source-record'),
}
ROOT_V1 = ('record_type', 'status', 'scope', 'not_authority_for', 'snapshot_policy', 'sources', *GROUPS,
           'preparation_order', 'preparation_order_semantics', 'baseline_pilot_boundary', 'relation_kinds',
           'relations', 'retained_source_map', 'required_output_semantics', 'provenance')
GROUPS_V2 = {'source_records': 'source-record', 'evidence_assessments': 'evidence-assessment'}
DEPTHS = {'historic_v2_label', 'official_abstract_only', 'full_primary_text'}
FINDINGS = {'historical-unchecked', 'supports-bounded-comparison', 'not-applicable', 'contradictory', 'indeterminate'}
INDEPENDENCE = {'author_self_check', 'internal_independent', 'external_peer_review'}

def is_utc(value) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z', value):
        return False
    try:
        datetime.fromisoformat(value[:-1] + '+00:00'); return True
    except ValueError:
        return False

def validate(data: dict) -> dict:
    errors: list[str] = []
    nodes: dict[str, dict] = {}
    def require(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)
    v2 = data.get('record_type') == 'knowledge-corpus-map/2'
    require(v2 or data.get('record_type') == 'knowledge-corpus-map/1', 'unsupported record type')
    shapes = SHAPES_V2 if v2 else SHAPES
    if v2:
        for key in sorted(set(data) - set(ROOT_V1) - set(GROUPS_V2)):
            errors.append(f'unknown top-level key {key}')
    require(data.get('status') == 'proposed-reference-view', 'scope must remain proposed-reference-view')
    sources = data.get('sources', {})
    require(isinstance(sources, dict) and bool(sources), 'sources required')
    if not isinstance(sources, dict):
        sources = {}
    for key, source in sources.items():
        require(isinstance(source, dict), f'invalid source {key}')
        if not isinstance(source, dict):
            continue
        require(source.get('repository') == 'Arcanada-one/knowledge-contract', f'foreign repository {key}')
        require(bool(re.fullmatch(r'[0-9a-f]{40}', str(source.get('commit', '')))), f'unpinned source {key}')
        if v2:
            require(set(source) <= {'repository', 'commit'}, f'external identifier in sources {key}')
    for group in GROUPS:
        rows = data.get(group, [])
        require(isinstance(rows, list), f'invalid group {group}')
        if not isinstance(rows, list):
            continue
        for node in rows:
            if not isinstance(node, dict):
                errors.append(f'invalid node in {group}'); continue
            identity = node.get('id')
            require(isinstance(identity, str) and bool(identity), f'missing ID in {group}')
            if not isinstance(identity, str):
                continue
            require(identity not in nodes, f'duplicate ID {identity}')
            nodes[identity] = node
            # Source-backed nodes need an immutable source and a safe locator.
            # Claims inherit the source through their explicit document link.
            source_key = node.get('source')
            if group != 'claims' or 'source' in node:
                require(isinstance(source_key, str) and source_key in sources,
                        f'missing or unknown source for {identity}')
            locator_key = 'source_path' if group == 'roadmap_nodes' else 'path'
            if group != 'claims' or locator_key in node:
                p = node.get(locator_key)
                require(isinstance(p, str) and bool(p) and not PurePosixPath(p).is_absolute()
                        and '..' not in PurePosixPath(p).parts and '\\' not in p
                        and '\x00' not in p and str(PurePosixPath(p)) == p,
                        f'missing or unsafe {locator_key} for {identity}')
    for group, kind in GROUPS_V2.items() if v2 else ():
        rows = data.get(group, [])
        require(isinstance(rows, list), f'invalid group {group}')
        for node in rows if isinstance(rows, list) else []:
            identity = node.get('id') if isinstance(node, dict) else None
            require(isinstance(identity, str) and bool(identity), f'missing ID in {group}')
            if not isinstance(identity, str) or not identity:
                continue
            require(identity not in nodes, f'duplicate ID {identity}')
            require(node.get('kind') == kind, f'invalid kind for {identity}')
            nodes[identity] = node
    for record in data.get('source_records', []) if v2 else []:
        if not isinstance(record, dict):
            continue
        rid = record.get('id')
        require(record.get('identifier_type') in {'doi', 'url', 'isbn'}, f'invalid identifier type {rid}')
        require(isinstance(record.get('identifier'), str) and bool(record['identifier'].strip()), f'missing identifier {rid}')
        require(isinstance(record.get('title'), str) and bool(record['title'].strip()), f'missing title {rid}')
        retrieved = record.get('retrieved_at')
        require(is_utc(retrieved) or (retrieved is None and bool(record.get('historical_v2_label'))),
                f'invalid retrieved_at {rid}')
        for field in ('historical_v2_id', 'historical_v2_label'):
            require(field not in record or (isinstance(record[field], str) and bool(record[field])), f'invalid {field} {rid}')
        require('commit' not in record and 'repository' not in record, f'source record carries a Git pin {rid}')
    for a in data.get('evidence_assessments', []) if v2 else []:
        if not isinstance(a, dict):
            continue
        aid, depth = a.get('id'), a.get('inspection_depth')
        for field in ('method', 'scope', 'limitations', 'assessor_identity', 'assessor_role'):
            require(isinstance(a.get(field), str) and bool(a[field].strip()), f'missing {field} {aid}')
        require(depth in DEPTHS, f'invalid inspection_depth {aid}')
        require(a.get('finding') in FINDINGS, f'invalid finding {aid}')
        require(a.get('reviewer_independence') in INDEPENDENCE, f'invalid reviewer_independence {aid}')
        require(is_utc(a.get('observed_at')) or (a.get('observed_at') is None and depth == 'historic_v2_label'),
                f'invalid observed_at {aid}')
        if depth == 'historic_v2_label':
            require(a.get('finding') == 'historical-unchecked', f'historic label claims a finding {aid}')
            require(not any('verified' in str(a.get(f, '')).lower() for f in ('method', 'scope', 'finding', 'limitations')),
                    f'historic label claims verification {aid}')
            require(a.get('reviewer_independence') == 'author_self_check', f'historic label claims independent review {aid}')
        # ClaimRevision = (claim_id, document_source_commit), resolved claim -> document -> source -> commit.
        claim = nodes.get(a.get('claim_id'), {})
        require(claim.get('kind') == 'claim', f'assessment has no claim {aid}')
        doc = nodes.get(claim.get('document'), {})
        current = sources.get(doc.get('source'), {}).get('commit') if isinstance(sources.get(doc.get('source')), dict) else None
        pinned = a.get('document_source_commit')
        require(bool(re.fullmatch(r'[0-9a-f]{40}', str(pinned))), f'unpinned assessment {aid}')
        require(pinned == current, f'STALE assessment {aid}: claim revision moved')
    for node in data.get('documents', []):
        require(node.get('status') in {'accepted-source','editorial-proposal','research-draft'}, f'invalid document status {node.get("id")}')
        require(str(node.get('path','')).endswith('/PAPER.md'), f'not a manuscript {node.get("id")}')
    for claim in data.get('claims', []):
        d = nodes.get(claim.get('document'), {})
        require(d.get('kind') == 'document', f'claim has no document {claim.get("id")}')
        require(isinstance(claim.get('premises'), list) and bool(claim['premises']), f'claim has no premises {claim.get("id")}')
        require(bool(claim.get('limits')) and bool(claim.get('source_location')), f'claim lacks limits/location {claim.get("id")}')
        require(claim.get('assessment') == 'producer-summary-not-independent-review', f'unsupported review claim {claim.get("id")}')
    for unit in data.get('foundation_units', []):
        status, target = unit.get('status'), unit.get('document')
        require(status in {'complete-candidate','planned-target','planned-extension'}, f'invalid unit status {unit.get("id")}')
        if status == 'planned-target':
            require(target is None, f'planned target impersonates document {unit.get("id")}')
        else:
            require(nodes.get(target, {}).get('kind') == 'document', f'existing target missing {unit.get("id")}')
        for r in unit.get('covers', []):
            require(nodes.get(r, {}).get('kind') == 'research-work-definition', f'unknown RM coverage {unit.get("id")}')
    required: list[tuple[str,str]] = []
    for node in data.get('roadmap_nodes', []):
        require(node.get('execution_state') == 'not-established-by-this-map', f'unsupported task state {node.get("id")}')
        deps = node.get('requires', [])
        require(isinstance(deps, list), f'invalid required list {node.get("id")}')
        if not isinstance(deps, list):
            continue
        require(len(deps) == len(set(deps)), f'duplicate required edge {node.get("id")}')
        for dep in deps:
            require(nodes.get(dep, {}).get('kind') == 'research-work-definition', f'unknown prerequisite {dep}')
            required.append((node['id'], dep))
    # Cycle check applies only to required-output edges, never to reading interfaces.
    children: dict[str,list[str]] = collections.defaultdict(list)
    indegree = {n['id']:0 for n in data.get('roadmap_nodes', [])}
    for dependent, prerequisite in required:
        if prerequisite in indegree and dependent in indegree:
            children[prerequisite].append(dependent); indegree[dependent] += 1
    queue = collections.deque(k for k,v in indegree.items() if v == 0)
    visited = 0
    while queue:
        x = queue.popleft(); visited += 1
        for y in children[x]:
            indegree[y] -= 1
            if indegree[y] == 0:
                queue.append(y)
    require(visited == len(indegree), 'required-output cycle')
    seen = set()
    relations = data.get('relations', [])
    for edge in relations:
        a,b,k = edge.get('from'),edge.get('to'),edge.get('kind')
        require(k in shapes, f'unknown relation kind {k}')
        require((a,k,b) not in seen, f'duplicate relation {a}/{k}/{b}')
        seen.add((a,k,b))
        require(a in nodes and b in nodes, f'dangling relation {a}/{b}')
        if k in shapes and a in nodes and b in nodes:
            require((nodes[a].get('kind'),nodes[b].get('kind')) == shapes[k], f'relation type mismatch {a}/{k}/{b}')
        require(bool(edge.get('basis')), f'missing relation basis {a}/{b}')
        if k == 'claim-has-ground' and b in nodes:
            require(nodes[b].get('claim_id') == a, f'ground claim mismatch {a}/{b}')
    for a in data.get('evidence_assessments', []) if v2 else []:
        aid = a.get('id') if isinstance(a, dict) else None
        grounds = sum(1 for e in relations if e.get('kind') == 'claim-has-ground' and e.get('to') == aid)
        uses = sum(1 for e in relations if e.get('kind') == 'ground-uses-source' and e.get('from') == aid)
        require(grounds == 1, f'assessment needs exactly one claim-has-ground edge {aid}')
        require(uses >= 1, f'assessment uses no source {aid}')
        # An inspection of the source itself needs a source that was actually opened.
        if isinstance(a, dict) and a.get('inspection_depth') in ('official_abstract_only', 'full_primary_text'):
            used = [nodes.get(e.get('to'), {}) for e in relations if e.get('kind') == 'ground-uses-source' and e.get('from') == aid]
            require(all(r.get('retrieved_at') for r in used), f'inspection without a retrieved source {aid}')
    for unit in data.get('foundation_units', []):
        actual = {e['to'] for e in relations if e.get('from') == unit['id'] and e.get('kind') == 'addresses-planned-scope'}
        require(actual == set(unit.get('covers', [])), f'coverage mismatch {unit["id"]}')
    order = data.get('preparation_order', [])
    require(len(order) == len(set(order)) and set(order) == {x['id'] for x in data.get('foundation_units', [])}, 'invalid preparation order')
    require(set(data.get('relation_kinds', {})) == set(shapes), 'relation semantics mismatch')
    if v2:
        for k in ('claim-has-ground', 'ground-uses-source'):
            meaning = data.get('relation_kinds', {}).get(k)
            require(isinstance(meaning, str) and 'traceability' in meaning.lower()
                    and 'verified' not in meaning.lower(), f'relation {k} must state descriptive traceability only')
    require(bool(data.get('required_output_semantics')) and bool(data.get('baseline_pilot_boundary')), 'missing graph boundary')
    imported = data.get('retained_source_map', {})
    require(imported.get('source') in sources and imported.get('relation_count') == 18, 'invalid retained F01 map reference')
    require(bool(re.fullmatch(r'[0-9a-f]{40}', str(imported.get('blob','')))), 'missing retained map identity')
    counted = GROUPS + (tuple(GROUPS_V2) if v2 else ())
    return {'structural_valid':not errors,'errors':errors,'counts':{**{g:len(data.get(g,[])) for g in counted},'nodes':len(nodes),'explicit_relations':len(relations),'required_output_edges':len(required)},'semantic_review':'not_established_by_this_check','runtime_readiness':'not_established_by_this_check','site_delivery':'not_established_by_this_check'}

def verify_source_objects(data: dict, repo: Path) -> dict:
    """Optional local Git object checks; never fetch or mutate a checkout."""
    checks = {}
    for group in ('documents','terms','foundation_units','roadmap_nodes'):
        for n in data[group]:
            source = data['sources'][n['source']]
            path = n.get('path',n.get('source_path'))
            spec = source['commit'] + ':' + path
            if spec in checks:
                continue
            run = subprocess.run(['git','-C',str(repo),'cat-file','-e',spec],capture_output=True,text=True)
            checks[spec] = run.returncode == 0
    ref = data['retained_source_map']
    spec = data['sources'][ref['source']]['commit'] + ':' + ref['path']
    run = subprocess.run(['git','-C',str(repo),'rev-parse',spec],capture_output=True,text=True)
    exact = run.returncode == 0 and run.stdout.strip() == ref['blob']
    return {'objects':checks,'retained_map_blob_matches':exact,'pass':all(checks.values()) and exact,'limit':'Object existence and one blob identity only; not full-text semantic or anchor validation.'}

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--map',type=Path,default=Path(__file__).resolve().parents[1]/'reference/foundations/corpus-map.json')
    p.add_argument('--repo',type=Path,help='Optional local repository with all pinned Git objects; no network.')
    p.add_argument('--expected-sha256')
    args=p.parse_args()
    try:
        raw=args.map.read_bytes()
        data=json.loads(raw.decode('utf-8'))
        if not isinstance(data,dict):
            raise ValueError('map root must be an object')
        result=validate(data)
        result['sha256']=hashlib.sha256(raw).hexdigest()
        result['bytes']=len(raw)
        if args.expected_sha256 and result['sha256'] != args.expected_sha256:
            result['errors'].append('map integrity mismatch');result['structural_valid']=False
        if args.repo:
            result['source_objects']=verify_source_objects(data,args.repo)
        else:
            result['source_objects']={'status':'not_run','reason':'No local repository supplied; connector source reads are separate evidence.'}
        print(json.dumps(result,indent=2,sort_keys=True))
        return 0 if result['structural_valid'] and result['source_objects'].get('pass',True) else 1
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(f'INPUT_ERROR: {exc}',file=sys.stderr);return 2
if __name__=='__main__':
    raise SystemExit(main())
