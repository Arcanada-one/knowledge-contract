# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import copy
import json
import unittest
from tools.verify_corpus_map import validate

BASE=json.loads((Path(__file__).resolve().parents[1]/'reference/foundations/corpus-map.json').read_text())
class CorpusMapControls(unittest.TestCase):
    def mutated(self,change):
        d=copy.deepcopy(BASE);change(d);return validate(d)
    def test_valid_snapshot(self):self.assertTrue(validate(BASE)['structural_valid'])
    def test_unpinned_source(self):self.assertFalse(self.mutated(lambda d:d['sources']['f01'].update(commit='main'))['structural_valid'])
    def test_unknown_source(self):self.assertFalse(self.mutated(lambda d:d['documents'][0].update(source='absent'))['structural_valid'])
    def test_missing_document_source(self):self.assertFalse(self.mutated(lambda d:d['documents'][0].pop('source'))['structural_valid'])
    def test_missing_term_source(self):self.assertFalse(self.mutated(lambda d:d['terms'][0].pop('source'))['structural_valid'])
    def test_missing_foundation_source(self):self.assertFalse(self.mutated(lambda d:d['foundation_units'][0].pop('source'))['structural_valid'])
    def test_missing_roadmap_source(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].pop('source'))['structural_valid'])
    def test_missing_roadmap_source_path(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].pop('source_path'))['structural_valid'])
    def test_unsafe_roadmap_source_path(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].update(source_path='../outside.json'))['structural_valid'])
    def test_absolute_roadmap_source_path(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].update(source_path='/tmp/dependencies.json'))['structural_valid'])
    def test_unsafe_roadmap_backslash(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].update(source_path='roadmap\\outside.json'))['structural_valid'])
    def test_duplicate_identity(self):self.assertFalse(self.mutated(lambda d:d['terms'].append(d['terms'][0]))['structural_valid'])
    def test_dangling_edge(self):self.assertFalse(self.mutated(lambda d:d['relations'][0].update(to='absent'))['structural_valid'])
    def test_wrong_edge_type(self):self.assertFalse(self.mutated(lambda d:d['relations'][0].update(to='C01'))['structural_valid'])
    def test_claim_premises_required(self):self.assertFalse(self.mutated(lambda d:d['claims'][0].update(premises=[]))['structural_valid'])
    def test_planned_target_not_completed(self):self.assertFalse(self.mutated(lambda d:d['foundation_units'][1].update(status='complete-candidate'))['structural_valid'])
    def test_task_completion_not_inferred(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].update(execution_state='completed'))['structural_valid'])
    def test_required_cycle_rejected(self):self.assertFalse(self.mutated(lambda d:d['roadmap_nodes'][0].update(requires=['RM-05']))['structural_valid'])
    def test_reading_cycle_allowed(self):
        # The authentic snapshot already has reciprocal D01/D03 reading links.
        self.assertTrue(validate(BASE)['structural_valid'])
        self.assertTrue(any(e['from']=='D01' and e['to']=='D03' for e in BASE['relations']))
        self.assertTrue(any(e['from']=='D03' and e['to']=='D01' for e in BASE['relations']))
    def test_plan_coverage_drift(self):self.assertFalse(self.mutated(lambda d:d['foundation_units'][0]['covers'].append('RM-25'))['structural_valid'])
    def test_private_absolute_path_rejected(self):self.assertFalse(self.mutated(lambda d:d['documents'][0].update(path='/tmp/PAPER.md'))['structural_valid'])
    def test_fake_independent_review_rejected(self):self.assertFalse(self.mutated(lambda d:d['claims'][0].update(assessment='independently-proven'))['structural_valid'])
if __name__=='__main__':unittest.main()
