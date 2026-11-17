#!/usr/bin/env python3
"""Check a dated translation inventory against actual source/target bytes.

This asserts exact identities/counts only. It does not establish linguistic
fidelity, independent review, deployment or native admission.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

BASELINE = 'b00b42fb5ca4f32ca443812c980c13d4d5d53d81'
BEGIN = '<!-- CURRENT-RENDITION-INVENTORY:BEGIN -->'
END = '<!-- CURRENT-RENDITION-INVENTORY:END -->'
KEYS = {'catalogue_works', 'metadata_cards', 'registered_bodies',
        'source_mismatches', 'missing_pairs', 'historical_review_entries'}

def pairs(items):
    out = {}
    for k, v in items:
        if k in out:
            raise ValueError('DUPLICATE_JSON_FIELD: '+k)
        out[k] = v
    return out

def parse(raw):
    def reject(v):
        raise ValueError('NONFINITE_JSON: '+v)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)

def witness(md):
    if md.count(BEGIN) != 1 or md.count(END) != 1:
        raise ValueError('WITNESS_MARKERS')
    section = md.split(BEGIN, 1)[1].split(END, 1)[0].strip()
    fence = chr(96)*3
    m = re.fullmatch(re.escape(fence) + r'json\s*\n(.*?)\n' +
                     re.escape(fence), section, re.S)
    if not m:
        raise ValueError('WITNESS_FORMAT')
    obj = parse(m.group(1))
    if not isinstance(obj, dict) or set(obj) != KEYS:
        raise ValueError('WITNESS_FIELDS')
    return obj

def baseline_renditions(root):
    """Read immutable pre-update review objects from actual Git history."""
    completed = subprocess.run(
        ['git', '-C', str(root), 'show', BASELINE + ':publication-renditions.json'],
        capture_output=True, check=False)
    if completed.returncode:
        raise ValueError('HISTORICAL_BASELINE_UNAVAILABLE')
    return parse(completed.stdout.decode('utf-8'))['renditions']

def verify_bindings_and_reviews(docs, bodies, baseline):
    by_slug = {d['slug']: d['path'] for d in docs}
    if len(by_slug) != len(docs):
        raise ValueError('DUPLICATE_SLUG')
    for entry in bodies:
        key = (entry['work'], entry['language'])
        path = by_slug.get(entry['work'])
        if path is None or entry['source']['path'] != path:
            raise ValueError('SOURCE_PATH_NOT_CATALOG: ' + repr(key))
        target = 'translations/' + entry['language'] + '/' + path
        if entry['rendition']['path'] != target:
            raise ValueError('RENDITION_PATH_NOT_CATALOG: ' + repr(key))
    def reviews(entries):
        return {(e['work'], e['language']): e['review']
                for e in entries if 'review' in e}
    prior, current = reviews(baseline), reviews(bodies)
    if len(prior) != 8 or len(current) != 8 or current != prior:
        raise ValueError('HISTORICAL_REVIEW_OBJECT_CHANGED')

def structural_negatives(root):
    """Execute two in-memory identity mutants, not changed count fields."""
    docs = parse((root/'publication-catalog.json').read_text('utf-8'))['documents']
    entries = parse((root/'publication-renditions.json').read_text('utf-8'))['renditions']
    baseline = baseline_renditions(root)
    verify_bindings_and_reviews(docs, entries, baseline)
    source_mutant = copy.deepcopy(entries)
    source_mutant[0]['source']['path'] = 'papers/semantic-objects-and-context/PAPER.md'
    review_mutant = copy.deepcopy(entries)
    reviewed = next(e for e in review_mutant if 'review' in e)
    reviewed['review']['limitations'] += ' (unauthorised historical revision)'
    caught = 0
    for name, mutated, code in (
        ('source-path-swap', source_mutant, 'SOURCE_PATH_NOT_CATALOG'),
        ('review-object-edit', review_mutant, 'HISTORICAL_REVIEW_OBJECT_CHANGED'),
    ):
        try:
            verify_bindings_and_reviews(docs, mutated, baseline)
        except ValueError as error:
            if not str(error).startswith(code):
                raise
            caught += 1
        else:
            raise RuntimeError('STRUCTURAL_MUTANT_NOT_CAUGHT: ' + name)
    return caught

def inventory(root):
    catalog = parse((root/'publication-catalog.json').read_text('utf-8'))
    meta = parse((root/'publication-localization.json').read_text('utf-8'))
    sidecar = parse((root/'publication-renditions.json').read_text('utf-8'))
    docs, cards, bodies = catalog['documents'], meta['entries'], sidecar['renditions']
    verify_bindings_and_reviews(docs, bodies, baseline_renditions(root))
    slugs = [d['slug'] for d in docs]
    if len(slugs) != len(set(slugs)):
        raise ValueError('DUPLICATE_SLUG')
    required = {(s,lang) for s in slugs for lang in ('ru','zh-Hans')}
    mkeys = [(x['work'], x['language']) for x in cards]
    bkeys = [(x['work'], x['language']) for x in bodies]
    if set(mkeys) != required or len(mkeys) != len(set(mkeys)):
        raise ValueError('CARD_COVERAGE_OR_DUPLICATE')
    if len(bkeys) != len(set(bkeys)) or not set(bkeys) <= required:
        raise ValueError('BODY_IDENTITY_OR_DUPLICATE')
    old_source = 0
    for entry in bodies:
        for kind in ('source','rendition'):
            rec = entry[kind]
            path = Path(rec['path'])
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('PATH_ESCAPE')
            if hashlib.sha256((root/path).read_bytes()).hexdigest() != rec['sha256']:
                if kind == 'source':
                    old_source += 1
                else:
                    raise ValueError('BODY_BYTES_DIFFER: '+rec['path'])
    return {
        'catalogue_works': len(docs), 'metadata_cards': len(cards),
        'registered_bodies': len(bodies), 'source_mismatches': old_source,
        'missing_pairs': [list(k) for k in sorted(required - set(bkeys))],
        'historical_review_entries': sum('review' in x for x in bodies),
    }

def match(observed, actual):
    if observed != actual:
        raise ValueError('WITNESS_MISMATCH: ' +
                         ','.join(sorted(k for k in KEYS if observed.get(k) != actual.get(k))))

def receipt_match(root, actual):
    report = parse((root/'reviews/renditions/source-currency-20261116/review-followup-result.json').read_text('utf-8'))
    if report['result'] != 'PASS':
        raise ValueError('SOURCE_REPORT_NOT_PASS')
    match({
        'catalogue_works': 36,
        'metadata_cards': report['metadata_records'],
        'registered_bodies': report['rendition_entries'],
        'source_mismatches': report['current_source_mismatches'],
        'missing_pairs': report['missing_pairs'],
        'historical_review_entries': report['historical_review_objects_unchanged'],
    }, actual)

def negatives(actual):
    match(actual, actual)
    mutants = [
        ('stale-older-source', {'source_mismatches': 10}),
        ('metadata-instead-of-body', {'registered_bodies': actual['metadata_cards']}),
        ('pretend-reviewed', {'historical_review_entries': actual['registered_bodies']}),
        ('hide-missing', {'missing_pairs': []}),
    ]
    count = 0
    for name, changes in mutants:
        try:
            match(dict(actual, **changes), actual)
        except ValueError as e:
            if not str(e).startswith('WITNESS_MISMATCH:'):
                raise
            count += 1
        else:
            raise RuntimeError('MUTANT_NOT_CAUGHT: '+name)
    return count

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root', type=Path, default=Path('.'))
    p.add_argument('--self-test', action='store_true')
    args=p.parse_args()
    root=args.root.resolve()
    actual=inventory(root)
    match(witness((root/'roadmap/TRANSLATIONS.md').read_text('utf-8')),actual)
    receipt_match(root,actual)
    detected=(negatives(actual) + structural_negatives(root)) if args.self_test else 0
    print(json.dumps({'result':'PASS','inventory':actual,'mutants_caught':detected},sort_keys=True))

if __name__ == '__main__':
    main()
