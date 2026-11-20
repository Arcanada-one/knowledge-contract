#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reconcile bibliographic records conservatively; never upgrade reading status."""
from pathlib import Path
import json, re, unicodedata, hashlib
from difflib import SequenceMatcher
from collections import Counter, defaultdict

BASE = Path(__file__).parent

def norm(value):
    s = unicodedata.normalize('NFKD', str(value or '')).casefold()
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '', s)

def doi_norm(value):
    return re.sub(r'^https?://(?:dx\.)?doi\.org/', '', str(value or '').strip(), flags=re.I).casefold()

def records(path):
    obj = json.loads(path.read_text())
    return obj if isinstance(obj,list) else obj.get('records',obj.get('sources',[]))

def main():
    core = []
    merges = []
    by_doi, by_url = {}, {}
    inputs = ['operations_sources.json','workforce_sources.json','agent_sources.json','root_sources.json']
    for filename in inputs:
        for x in records(BASE/filename):
            authors = x.get('authors', '')
            if isinstance(authors,list): authors = '; '.join(authors)
            r = {
                'id':'', 'aliases':[x['id']], 'title':x['title'], 'authors':authors,
                'year':x.get('year'), 'doi':doi_norm(x.get('doi')) or None,
                'url':x.get('canonical_url',x.get('url')), 'family':x.get('primary_family',x.get('family','unclassified')),
                'source_type':x.get('source_type','source'), 'evidence_level':x.get('evidence_level','metadata'),
                'relevance':x.get('relevance',x.get('relevance_ru','')),
                'notes':x.get('notes') or x.get('publication_note') or '',
                'web_refs':[x.get('verification_ref',x.get('web_ref'))],
                'status':'primary_record_checked', 'full_text_critical_appraisal_complete':False,
                'checked_on':x.get('verified_on','2026-11-18'),
                'provenance_files':[filename],
            }
            idx = by_doi.get(r['doi']) if r['doi'] else None
            if idx is None and r['url']:
                candidate = by_url.get(r['url'].rstrip('/'))
                if candidate is not None and norm(core[candidate]['title']) == norm(r['title']): idx=candidate
            if idx is not None:
                old=core[idx]
                old['aliases'] += r['aliases']; old['provenance_files'] += r['provenance_files']
                old['web_refs'] += [z for z in r['web_refs'] if z and z not in old['web_refs']]
                merges.append({'kind':'core','kept':old['aliases'][0],'merged':r['aliases'][0],'basis':'identical DOI or identical URL and normalized title'})
                continue
            r['id']=f'CW-S{len(core)+1:04d}'
            idx=len(core); core.append(r)
            if r['doi']: by_doi[r['doi']]=idx
            if r['url']: by_url[r['url'].rstrip('/')]=idx
    candidate_inputs=['workforce_cited_candidates.json','workforce_2013_cited_candidates.json']
    candidates=[]; exact={}; core_matches=[]
    for filename in candidate_inputs:
        for x in records(BASE/filename):
            r=dict(x);r['aliases']=[r.pop('id')];r['provenance_files']=[filename]
            key=norm(r['bibliographic_text'])
            if key in exact:
                old=candidates[exact[key]]
                old['aliases'] += r['aliases']; old['provenance'] += r['provenance']
                old['additional_parent_sources'] = old.get('additional_parent_sources',[])+[{'id':r.get('parent_source_id'),'url':r.get('parent_url')}]
                merges.append({'kind':'candidate','kept':old['aliases'][0],'merged':r['aliases'][0],'basis':'identical normalized complete bibliography text'})
                continue
            r['id']=f'CW-C{len(candidates)+1:04d}'
            r['family']='personnel_scheduling_citation_candidate'
            r['evidence_level']='citation_only';r['status']='not_individually_verified'
            r['authors']=r.get('authors_as_cited','')
            exact[key]=len(candidates);candidates.append(r)
    # Same-title/year records remain distinct until author, venue and edition agree.
    groups=defaultdict(list)
    for r in core+candidates: groups[(norm(r['title']),r['year'])].append(r['id'])
    possible=[{'normalized_title':k[0],'year':k[1],'records':v,'status':'manual_identity_review_required'} for k,v in groups.items() if len(v)>1]
    near=[]
    for i,a in enumerate(candidates):
        if len(norm(a['title']))<12:continue
        for b in candidates[i+1:]:
            if a['year']!=b['year']:continue
            na,nb=norm(a['title']),norm(b['title'])
            if na==nb:continue
            if abs(len(na)-len(nb))>max(len(na),len(nb))*.12:continue
            score=SequenceMatcher(None,na,nb).ratio()
            if score>=.94:
                near.append({'records':[a['id'],b['id']],'title_similarity':round(score,4),'status':'possible_duplicate_not_merged'})
    def save(name,obj): (BASE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    save('consolidated_sources.json',core);save('consolidated_candidates.json',candidates)
    source_counts={name:len(records(BASE/name)) for name in inputs+candidate_inputs}
    manifest={
      'created_on':'2026-11-18','scope':'Initial scoping corpus, not a completed systematic review',
      'input_counts':source_counts,'raw_rows':sum(source_counts.values()),
      'checked_core_records':len(core),'citation_candidate_records':len(candidates),
      'retained_bibliographic_records':len(core)+len(candidates),'automatic_merges':len(merges),
      'same_title_year_groups_for_review':len(possible),'near_title_pairs_for_review':len(near),
      'unique_scholarly_works_count':None,
      'counting_note':'Retained records are not claimed to be unique works. Title/year matches and versions are retained for manual identity resolution; verified core and citation-only candidates can still refer to the same work.',
      'full_text_critical_appraisals_completed':0,
      'coverage_note':'The bulk candidate list is dominated by personnel scheduling sources through 2012; this is retrieval history, not the intended weight of the final theory. Modern and other-field expansion remains required.',
      'core_families':dict(Counter(r['family'] for r in core)),
      'core_reading_levels':dict(Counter(r['evidence_level'] for r in core)),
      'input_sha256':{name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in inputs+candidate_inputs},
    }
    save('corpus_manifest.json',manifest)
    save('identity_review.json',{'automatic_merges':merges,'same_title_year':possible,'near_title':near})
    assert len({r['id'] for r in core+candidates})==len(core)+len(candidates)
    assert all(r['title'] and r['url'] for r in core)
    assert all(r['parent_url'] and r['provenance'] for r in candidates)
    assert all(not r['full_text_critical_appraisal_complete'] for r in core)
    print(json.dumps({k:manifest[k] for k in ['raw_rows','checked_core_records','citation_candidate_records','retained_bibliographic_records','automatic_merges','same_title_year_groups_for_review','near_title_pairs_for_review']},ensure_ascii=False))

if __name__=='__main__': main()
