#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate a bounded reading map; do not infer truth, task readiness or grants."""
from __future__ import annotations
import argparse
import collections
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

def validate(data: dict) -> dict:
    errors: list[str] = []
    nodes: dict[str, dict] = {}
    def require(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)
    require(data.get('record_type') == 'knowledge-corpus-map/1', 'unsupported record type')
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
        require(k in SHAPES, f'unknown relation kind {k}')
        require((a,k,b) not in seen, f'duplicate relation {a}/{k}/{b}')
        seen.add((a,k,b))
        require(a in nodes and b in nodes, f'dangling relation {a}/{b}')
        if k in SHAPES and a in nodes and b in nodes:
            require((nodes[a].get('kind'),nodes[b].get('kind')) == SHAPES[k], f'relation type mismatch {a}/{k}/{b}')
        require(bool(edge.get('basis')), f'missing relation basis {a}/{b}')
    for unit in data.get('foundation_units', []):
        actual = {e['to'] for e in relations if e.get('from') == unit['id'] and e.get('kind') == 'addresses-planned-scope'}
        require(actual == set(unit.get('covers', [])), f'coverage mismatch {unit["id"]}')
    order = data.get('preparation_order', [])
    require(len(order) == len(set(order)) and set(order) == {x['id'] for x in data.get('foundation_units', [])}, 'invalid preparation order')
    require(set(data.get('relation_kinds', {})) == set(SHAPES), 'relation semantics mismatch')
    require(bool(data.get('required_output_semantics')) and bool(data.get('baseline_pilot_boundary')), 'missing graph boundary')
    imported = data.get('retained_source_map', {})
    require(imported.get('source') in sources and imported.get('relation_count') == 18, 'invalid retained F01 map reference')
    require(bool(re.fullmatch(r'[0-9a-f]{40}', str(imported.get('blob','')))), 'missing retained map identity')
    return {'structural_valid':not errors,'errors':errors,'counts':{**{g:len(data.get(g,[])) for g in GROUPS},'nodes':len(nodes),'explicit_relations':len(relations),'required_output_edges':len(required)},'semantic_review':'not_established_by_this_check','runtime_readiness':'not_established_by_this_check','site_delivery':'not_established_by_this_check'}

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
