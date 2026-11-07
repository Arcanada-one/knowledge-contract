#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Build or check the inventory-first candidate knowledge-corpus-map/2 (Muneral KC-MAP2-1).

Inputs are pinned: the accepted /1 map and KC-Brain's historical v2 reference inventory, vendored
byte for byte from PR #67 at commit 5e1837a0. One source_record is emitted per inventory row that
states a DOI or an explicit URL in its own text; every other row is excluded and counted, never
completed with a derived identifier. No evidence assessment or claim edge is emitted: KC-Brain
approved zero claim/source pairs. The candidate is not a published map, an index admission or a
statement that any source was read.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'reference/foundations/corpus-map.json'
DIR = ROOT / 'reviews/corpus-map-v2'
TSV = DIR / 'V2_REFERENCES.tsv'
OUT = DIR / 'corpus-map-v2.inventory-candidate.json'
MANIFEST = DIR / 'MANIFEST.json'
TSV_SOURCE = {'repository': 'Arcanada-one/knowledge-contract', 'commit': '5e1837a0fc676f89103b3b9f06a38bfb39ab7a66',
              'path': 'reviews/bibliography-v2/V2_REFERENCES.tsv', 'blob': '578bf2395846b6b262bd1d0a4b95811704ade749'}
BASE_BLOB = 'a7b2fb8cde305b8fe4145df1ee7d7179478fdd60'
ROWS = 74
V2_RELATION_KINDS = {
    'claim-has-ground': 'Descriptive traceability from a claim revision to an assessment; not a truth verdict.',
    'ground-uses-source': 'Descriptive traceability from an assessment to an external source record; not endorsement.',
}
DOI_RE = re.compile(r'\bdoi:\s*(10\.\d{4,9}/\S+?)(?=\.?(?:\s|$))', re.I)
URL_RE = re.compile(r'(https?://[^\s,;]+?)(?=[.,;)]?(?:\s|$))')


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def identifier(text: str) -> tuple[str, str] | None:
    """Return (type, identifier) only for a DOI or URL written in the row text itself."""
    doi = DOI_RE.search(text)
    if doi:
        return 'doi', doi.group(1)
    url = URL_RE.search(text)
    if url:
        return 'url', url.group(1)
    return None


def build(base_bytes: bytes, tsv_bytes: bytes) -> tuple[bytes, bytes]:
    base = json.loads(base_bytes.decode('utf-8'))
    rows = list(csv.DictReader(io.StringIO(tsv_bytes.decode('utf-8')), delimiter='\t'))
    records, excluded = [], []
    for row in rows:
        rid, text = row['v2_ref_id'], row['legacy_bibliography_text']
        found = identifier(text)
        if found is None:
            excluded.append({'historical_v2_id': rid, 'reason': 'no DOI or URL stated in the inventory text',
                             'arxiv_id_in_text': bool(re.search(r'arXiv:\s*\d', text))})
            continue
        records.append({'id': f'SR-{rid}', 'kind': 'source-record', 'identifier_type': found[0], 'identifier': found[1],
                        'title': text, 'retrieved_at': None, 'historical_v2_id': rid,
                        'historical_v2_label': row['legacy_verification_label']})
    out = dict(base)
    out['record_type'] = 'knowledge-corpus-map/2'
    out['relation_kinds'] = {**base['relation_kinds'], **V2_RELATION_KINDS}
    out['source_records'] = records
    out['evidence_assessments'] = []
    manifest = {
        'record_type': 'knowledge-corpus-map-v2-inventory-candidate-manifest/1',
        'muneral_task': 'ba97d5d1-3a0c-4949-8dde-1c5522be167c',
        'status': 'candidate-only; not published, not indexed, no source inspected by this build',
        'base_map': {'path': 'reference/foundations/corpus-map.json', 'blob': git_blob(base_bytes),
                     'sha256': hashlib.sha256(base_bytes).hexdigest()},
        'inventory': {**TSV_SOURCE, 'vendored_path': 'reviews/corpus-map-v2/V2_REFERENCES.tsv',
                      'sha256': hashlib.sha256(tsv_bytes).hexdigest(), 'rows': len(rows)},
        'counts': {'inventory_rows': len(rows), 'source_records': len(records), 'excluded': len(excluded),
                   'by_identifier_type': {t: sum(r['identifier_type'] == t for r in records) for t in ('doi', 'url', 'isbn')},
                   'evidence_assessments': 0, 'claim_has_ground_edges': 0, 'ground_uses_source_edges': 0},
        'rules': ['identifier is copied from the row text; no DOI, URL or ISBN is derived (an arXiv number is not turned into a URL)',
                  'title is the verbatim historical bibliography text, not a parsed title',
                  'retrieved_at is null: this build opened no source',
                  'historical_v2_label is the legacy verification label, a historical label only',
                  'zero approved claim/source pairs: no evidence assessment and no claim-has-ground or ground-uses-source edge'],
        'excluded': excluded,
    }
    dump = lambda o: (json.dumps(o, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    return dump(out), dump(manifest)


def check(base_bytes: bytes, tsv_bytes: bytes, out_bytes: bytes, manifest_bytes: bytes) -> list[str]:
    errors = []
    if git_blob(tsv_bytes) != TSV_SOURCE['blob']:
        errors.append('vendored inventory differs from the pinned blob')
    if git_blob(base_bytes) != BASE_BLOB:
        errors.append('base /1 map differs from the pinned blob')
    want_out, want_manifest = build(base_bytes, tsv_bytes)
    if out_bytes != want_out:
        errors.append('candidate map is not the deterministic build of the pinned inputs')
    if manifest_bytes != want_manifest:
        errors.append('manifest is not the deterministic build of the pinned inputs')
    base, cand = json.loads(base_bytes), json.loads(out_bytes)
    for key in base:
        if key not in ('record_type', 'relation_kinds') and cand.get(key) != base[key]:
            errors.append(f'/1 base changed: {key}')
    if any(cand.get('relation_kinds', {}).get(k) != v for k, v in base['relation_kinds'].items()):
        errors.append('/1 base changed: relation_kinds')
    if cand.get('evidence_assessments') != []:
        errors.append('evidence assessment present without an approved claim/source pair')
    if any(e.get('kind') in V2_RELATION_KINDS for e in cand.get('relations', [])):
        errors.append('claim or source edge present without an approved claim/source pair')
    rows = {r['v2_ref_id']: r for r in csv.DictReader(io.StringIO(tsv_bytes.decode('utf-8')), delimiter='\t')}
    for rec in cand.get('source_records', []):
        row = rows.get(rec.get('historical_v2_id'))
        if row is None or rec.get('title') != row['legacy_bibliography_text']:
            errors.append(f'source record not traceable to an inventory row {rec.get("id")}')
        elif str(rec.get('identifier')) not in row['legacy_bibliography_text']:
            errors.append(f'identifier not stated in the inventory text {rec.get("id")}')
        if rec.get('retrieved_at') is not None:
            errors.append(f'retrieval claimed by an inventory build {rec.get("id")}')
    if len(rows) != ROWS:
        errors.append(f'inventory has {len(rows)} rows, expected {ROWS}')
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true', help='verify the committed candidate instead of writing it')
    args = p.parse_args()
    base_bytes, tsv_bytes = BASE.read_bytes(), TSV.read_bytes()
    if args.check:
        errors = check(base_bytes, tsv_bytes, OUT.read_bytes(), MANIFEST.read_bytes())
        for e in errors:
            print(f'MAP2_INVENTORY_FAIL {e}')
        if not errors:
            print('MAP2_INVENTORY_PASS')
        return 1 if errors else 0
    out, manifest = build(base_bytes, tsv_bytes)
    OUT.write_bytes(out)
    MANIFEST.write_bytes(manifest)
    print(json.loads(manifest)['counts'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
