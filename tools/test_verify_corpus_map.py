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
def v2_map():
    """A small valid /2 fixture derived from the accepted /1 map; not a real assessment."""
    d=copy.deepcopy(BASE);d['record_type']='knowledge-corpus-map/2'
    d['relation_kinds']['claim-has-ground']='Descriptive traceability from a claim revision to an assessment; not a truth verdict.'
    d['relation_kinds']['ground-uses-source']='Descriptive traceability from an assessment to an external source record; not endorsement.'
    commit=d['sources'][next(x for x in d['documents'] if x['id']=='D01')['source']]['commit']
    d['source_records']=[
        {'id':'SR01','kind':'source-record','identifier_type':'doi','identifier':'10.0000/example','title':'Example source','retrieved_at':'2026-11-01T12:00:00Z'},
        {'id':'SR02','kind':'source-record','identifier_type':'isbn','identifier':'978-0-00-000000-0','title':'Catalogue-only label','retrieved_at':None,'historical_v2_id':'v2-17','historical_v2_label':'Historic label'}]
    base={'kind':'evidence-assessment','claim_id':'C01','document_source_commit':commit,'method':'Read the official abstract','scope':'Premise 1 only','limitations':'Abstract only','assessor_identity':'fixture','assessor_role':'fixture-author','reviewer_independence':'author_self_check'}
    d['evidence_assessments']=[
        {**base,'id':'EA01','inspection_depth':'official_abstract_only','finding':'supports-bounded-comparison','observed_at':'2026-11-02T08:30:00Z'},
        {**base,'id':'EA02','inspection_depth':'historic_v2_label','finding':'historical-unchecked','observed_at':None,'method':'Carried historic label','scope':'Label only'}]
    d['relations']+=[
        {'from':'C01','kind':'claim-has-ground','to':'EA01','basis':'fixture'},
        {'from':'EA01','kind':'ground-uses-source','to':'SR01','basis':'fixture'},
        {'from':'C01','kind':'claim-has-ground','to':'EA02','basis':'fixture'},
        {'from':'EA02','kind':'ground-uses-source','to':'SR02','basis':'fixture'}]
    return d
V2=v2_map()
def drop(d,kind,to=None,frm=None):
    d['relations']=[e for e in d['relations'] if not (e['kind']==kind and (to is None or e['to']==to) and (frm is None or e['from']==frm))]
class CorpusMapV2Controls(unittest.TestCase):
    def check(self,change,fragment):
        d=copy.deepcopy(V2);change(d);r=validate(d)
        self.assertFalse(r['structural_valid']);self.assertTrue(any(fragment in e for e in r['errors']),r['errors'])
    def test_valid_v2_fixture(self):
        r=validate(V2);self.assertTrue(r['structural_valid'],r['errors'])
        self.assertEqual((r['counts']['source_records'],r['counts']['evidence_assessments']),(2,2))
    def test_v1_map_unchanged(self):
        r=validate(BASE);self.assertTrue(r['structural_valid'])
        self.assertEqual(r['counts'],{'documents':9,'terms':16,'claims':9,'foundation_units':6,'roadmap_nodes':25,'nodes':65,'explicit_relations':99,'required_output_edges':45})
    def test_v1_rejects_v2_relation_kind(self):
        d=copy.deepcopy(BASE);d['relations'].append({'from':'C01','kind':'claim-has-ground','to':'D01','basis':'x'})
        self.assertFalse(validate(d)['structural_valid'])
    def test_unknown_top_level_key(self):self.check(lambda d:d.update(notes='x'),'unknown top-level key notes')
    def test_unknown_group(self):self.check(lambda d:d.update(datasets=[{'id':'X01','kind':'dataset'}]),'unknown top-level key datasets')
    def test_unknown_relation_kind(self):self.check(lambda d:d['relations'].append({'from':'C01','kind':'claim-proves','to':'EA01','basis':'x'}),'unknown relation kind claim-proves')
    def test_duplicate_id_across_groups(self):self.check(lambda d:d['source_records'][0].update(id='D01'),'duplicate ID D01')
    def test_duplicate_id_new_groups(self):self.check(lambda d:d['evidence_assessments'][1].update(id='SR01'),'duplicate ID SR01')
    def test_external_record_in_sources(self):self.check(lambda d:d['sources'].update(doi={'identifier_type':'doi','identifier':'10.0000/example'}),'foreign repository doi')
    def test_external_identifier_on_pinned_source(self):self.check(lambda d:d['sources']['corpus'].update(url='https://example.org'),'external identifier in sources corpus')
    def test_source_record_git_pin(self):self.check(lambda d:d['source_records'][0].update(commit='a'*40),'carries a Git pin SR01')
    def test_source_record_repository(self):self.check(lambda d:d['source_records'][0].update(repository='Arcanada-one/knowledge-contract'),'carries a Git pin SR01')
    def test_source_record_bad_retrieved_at(self):self.check(lambda d:d['source_records'][0].update(retrieved_at='2026-11-01'),'invalid retrieved_at SR01')
    def test_stale_document_source_commit(self):self.check(lambda d:d['evidence_assessments'][0].update(document_source_commit='0'*40),'STALE assessment EA01')
    def test_no_claim_has_ground(self):self.check(lambda d:drop(d,'claim-has-ground',to='EA01'),'exactly one claim-has-ground edge EA01')
    def test_two_claim_has_ground(self):self.check(lambda d:d['relations'].append({'from':'C01','kind':'claim-has-ground','to':'EA01','basis':'again'}),'duplicate relation C01/claim-has-ground/EA01')
    def test_no_ground_uses_source(self):self.check(lambda d:drop(d,'ground-uses-source',frm='EA01'),'assessment uses no source EA01')
    def test_unreferenced_assessment(self):
        def change(d):drop(d,'claim-has-ground',to='EA02');drop(d,'ground-uses-source',frm='EA02')
        self.check(change,'exactly one claim-has-ground edge EA02')
    def test_wrong_endpoint_type(self):self.check(lambda d:d['relations'].append({'from':'EA01','kind':'ground-uses-source','to':'D01','basis':'x'}),'relation type mismatch EA01/ground-uses-source/D01')
    def test_dangling_ground_source(self):self.check(lambda d:d['relations'].append({'from':'EA01','kind':'ground-uses-source','to':'SR99','basis':'x'}),'dangling relation EA01/SR99')
    def test_ground_from_other_claim(self):
        def change(d):drop(d,'claim-has-ground',to='EA01');d['relations'].append({'from':'C02','kind':'claim-has-ground','to':'EA01','basis':'x'})
        self.check(change,'ground claim mismatch C02/EA01')
    def test_ground_edge_without_basis(self):self.check(lambda d:d['relations'][-1].update(basis=''),'missing relation basis EA02/SR02')
    def test_historic_label_with_finding(self):self.check(lambda d:d['evidence_assessments'][1].update(finding='supports-bounded-comparison'),'historic label claims a finding EA02')
    def test_historic_label_says_verified(self):self.check(lambda d:d['evidence_assessments'][1].update(scope='Label VERIFIED by v2'),'historic label claims verification EA02')
    def test_null_observed_at_needs_historic_depth(self):self.check(lambda d:d['evidence_assessments'][0].update(observed_at=None),'invalid observed_at EA01')
    def test_invalid_inspection_depth(self):self.check(lambda d:d['evidence_assessments'][0].update(inspection_depth='skimmed'),'invalid inspection_depth EA01')
    def test_invalid_finding(self):self.check(lambda d:d['evidence_assessments'][0].update(finding='proven'),'invalid finding EA01')
    def test_invalid_reviewer_independence(self):self.check(lambda d:d['evidence_assessments'][0].update(reviewer_independence='self'),'invalid reviewer_independence EA01')
    def test_required_text_field(self):self.check(lambda d:d['evidence_assessments'][0].update(assessor_role=' '),'missing assessor_role EA01')
    def test_assessment_cannot_upgrade_claim(self):self.check(lambda d:d['claims'][0].update(assessment='supports-bounded-comparison'),'unsupported review claim C01')
    def test_new_relation_semantics_required(self):self.check(lambda d:d['relation_kinds'].pop('ground-uses-source'),'relation semantics mismatch')
    def test_new_relation_semantics_descriptive(self):self.check(lambda d:d['relation_kinds'].update({'claim-has-ground':'The claim is verified by this ground.'}),'must state descriptive traceability only')
if __name__=='__main__':unittest.main()
