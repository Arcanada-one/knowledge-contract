# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
import copy
import json
import unittest

from tools import build_corpus_map_v2_inventory as b
from tools.verify_corpus_map import validate

BASE, TSV = b.BASE.read_bytes(), b.TSV.read_bytes()
OUT, MANIFEST = b.OUT.read_bytes(), b.MANIFEST.read_bytes()
CAND = json.loads(OUT)


def dump(o):
    return (json.dumps(o, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


class InventoryCandidate(unittest.TestCase):
    """Inventory-first /2 candidate: pinned inputs, verbatim identifiers, zero claim or evidence links."""

    def errors(self, cand=None, tsv=TSV, base=BASE):
        return b.check(base, tsv, OUT if cand is None else dump(cand), MANIFEST)

    def test_committed_candidate_is_the_build_of_the_pinned_inputs(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(b.build(BASE, TSV), (OUT, MANIFEST))

    def test_candidate_is_a_valid_v2_map(self):
        result = validate(copy.deepcopy(CAND))
        self.assertTrue(result['structural_valid'], result['errors'])

    def test_counts_account_for_every_inventory_row(self):
        counts = json.loads(MANIFEST)['counts']
        self.assertEqual(counts['inventory_rows'], 74)
        self.assertEqual(counts['source_records'] + counts['excluded'], 74)
        self.assertEqual(counts['source_records'], len(CAND['source_records']))
        self.assertEqual(counts['evidence_assessments'], 0)

    def test_every_stated_doi_or_url_is_included(self):
        import csv, io, re
        rows = csv.DictReader(io.StringIO(TSV.decode('utf-8')), delimiter='\t')
        stated = {r['v2_ref_id'] for r in rows if re.search(r'doi:\s*10\.|https?://', r['legacy_bibliography_text'], re.I)}
        self.assertEqual(stated, {r['historical_v2_id'] for r in CAND['source_records']})

    def test_fabricated_identifier_is_rejected(self):
        d = copy.deepcopy(CAND)
        d['source_records'][0]['identifier'] = '10.0000/invented'
        self.assertTrue(any('identifier not stated' in e for e in self.errors(d)))

    def test_derived_arxiv_url_is_rejected(self):
        excluded = [x for x in json.loads(MANIFEST)['excluded'] if x['arxiv_id_in_text']]
        self.assertTrue(excluded)
        d = copy.deepcopy(CAND)
        rid = excluded[0]['historical_v2_id']
        d['source_records'].append({'id': f'SR-{rid}', 'kind': 'source-record', 'identifier_type': 'url',
                                    'identifier': 'https://arxiv.org/abs/0000.00000', 'title': 'x', 'retrieved_at': None,
                                    'historical_v2_id': rid, 'historical_v2_label': 'x'})
        self.assertTrue(any('not traceable' in e for e in self.errors(d)))

    def test_stale_inventory_pin_is_rejected(self):
        self.assertTrue(any('pinned blob' in e for e in self.errors(tsv=TSV + b'V2-075\tx\n')))

    def test_stale_base_source_pin_is_rejected(self):
        d = copy.deepcopy(CAND)
        first = next(iter(d['sources']))
        d['sources'][first]['commit'] = '0' * 40
        self.assertTrue(any('/1 base changed: sources' in e for e in self.errors(d)))

    def _with_assessment(self, **overrides):
        d = copy.deepcopy(CAND)
        claim = d['claims'][0]
        doc = next(x for x in d['documents'] if x['id'] == claim['document'])
        a = {'id': 'EA-X', 'kind': 'evidence-assessment', 'claim_id': claim['id'],
             'document_source_commit': d['sources'][doc['source']]['commit'], 'inspection_depth': 'historic_v2_label',
             'finding': 'historical-unchecked', 'method': 'Carried label', 'observed_at': None, 'scope': 'Label only',
             'limitations': 'No primary text read', 'assessor_identity': 'KC-Brain', 'assessor_role': 'author-screening',
             'reviewer_independence': 'author_self_check', **overrides}
        sr = d['source_records'][0]['id']
        d['evidence_assessments'] = [a]
        d['relations'] = d['relations'] + [{'from': claim['id'], 'kind': 'claim-has-ground', 'to': 'EA-X', 'basis': 'test'},
                                           {'from': 'EA-X', 'kind': 'ground-uses-source', 'to': sr, 'basis': 'test'}]
        return d

    def test_unapproved_link_is_rejected_even_when_structurally_valid(self):
        d = self._with_assessment()
        self.assertTrue(validate(copy.deepcopy(d))['structural_valid'])
        errors = self.errors(d)
        self.assertTrue(any('evidence assessment present' in e for e in errors))
        self.assertTrue(any('edge present' in e for e in errors))

    def test_wrong_inspection_depth_is_rejected(self):
        for depth in ('official_abstract_only', 'full_primary_text'):
            errs = validate(self._with_assessment(inspection_depth=depth, finding='supports-bounded-comparison',
                                                  observed_at='2026-11-07T00:00:00Z'))['errors']
            self.assertTrue(any('inspection without a retrieved source' in e for e in errs), depth)

    def test_invented_independent_review_is_rejected(self):
        for level in ('internal_independent', 'external_peer_review'):
            errs = validate(self._with_assessment(reviewer_independence=level))['errors']
            self.assertTrue(any('historic label claims independent review' in e for e in errs), level)

    def test_claimed_retrieval_is_rejected(self):
        d = copy.deepcopy(CAND)
        d['source_records'][0]['retrieved_at'] = '2026-11-07T00:00:00Z'
        self.assertTrue(any('retrieval claimed' in e for e in self.errors(d)))


if __name__ == '__main__':
    unittest.main()
