#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded producer probes of the existing checker on copies of actual pages.

No production repair or independent semantic/a11y acceptance is implied.
The static observations below do not compute CSS layout or browser visibility.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass, field
from hashlib import sha256
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

SITE: Path
OUT: Path
LOCALES = ('en', 'ru', 'zh-Hans')
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

@dataclass(eq=False)
class Node:
    tag: str
    attrs: dict
    start: int
    open_end: int
    end: int = 0
    parent: Node | None = None
    children: list = field(default_factory=list)
    def chain(self):
        n = self
        while n:
            yield n
            n = n.parent
    def classes(self):
        return (self.attrs.get('class') or '').split()
    def text(self):
        return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
    def language(self):
        return next((n.attrs['lang'] for n in self.chain() if 'lang' in n.attrs), None)

class Tree(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.html = text
        self.offsets = [0]
        for m in re.finditer('\n', text):
            self.offsets.append(m.end())
        self.root = Node('#document',{},0,0,len(text))
        self.stack = [self.root]
        self.nodes = []
        self.feed(text)
        self.close()
    def absolute_pos(self):
        line,col = self.getpos()
        return self.offsets[line-1]+col
    def handle_starttag(self,tag,attrs):
        start=self.absolute_pos(); end=start+len(self.get_starttag_text())
        node=Node(tag,dict(attrs),start,end,end,self.stack[-1])
        self.stack[-1].children.append(node);self.nodes.append(node)
        if tag not in VOID:self.stack.append(node)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.stack.pop()
    def handle_endtag(self,tag):
        end=self.html.find('>',self.absolute_pos())+1
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:
                for n in self.stack[i:]:n.end=end
                del self.stack[i:]
                break
    def handle_data(self,data):
        self.stack[-1].children.append(data)

def require(value, message):
    if not value:raise ValueError(message)

def modify(html, edits):
    for start,end,value in sorted(edits,reverse=True):
        html=html[:start]+value+html[end:]
    return html

def attribute(html,node,name,value):
    opening=html[node.start:node.open_end]
    opening=re.sub(r'\s+'+re.escape(name)+r'(?:="[^"]*"|=\x27[^\x27]*\x27|=[^\s>]+)?','',opening,flags=re.I)
    if value is not False:
        opening=opening[:-1]+(' '+name if value is None else ' '+name+'="'+value+'"')+'>'
    return modify(html,[(node.start,node.open_end,opening)])

def badges(tree,work=None):
    return [n for n in tree.nodes if 'data-work-status' in n.attrs and (work is None or n.attrs['data-work-status']==work)]

def snippets(tree,work):
    return [{'path':[n.tag+('.'+'.'.join(n.classes()) if n.classes() else '') for n in list(b.chain())[:7]],
             'effective_language':b.language(),'html':tree.html[b.start:b.end]} for b in badges(tree,work)]

def checker():
    p=SITE/'scripts/publication_checks.py'
    s=importlib.util.spec_from_file_location('old_publication_checks_probe',p)
    m=importlib.util.module_from_spec(s)
    sys.modules[s.name]=m
    s.loader.exec_module(m)
    return m,p

def old_check(module,records,html,relative,name):
    root=OUT/'cases'/name
    target=root/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html,encoding='utf-8')
    try:
        result=module.check_status_labels(root,records)
        return {'accepted':True,'labelled_pages':result,'error':None,
                'input_sha256':sha256(html.encode()).hexdigest(),'path':str(target.relative_to(OUT))}
    except ValueError as e:
        return {'accepted':False,'labelled_pages':None,'error':str(e),
                'input_sha256':sha256(html.encode()).hexdigest(),'path':str(target.relative_to(OUT))}

def main():
    global SITE, OUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir',type=Path,required=True,
                        help='Explicit input checkout with the checker and generated public pages')
    parser.add_argument('--output-dir',type=Path,required=True,
                        help='New empty output directory, for example in RUNNER_TEMP or scratch; never overwritten and must not overlap the input site')
    parser.add_argument('--expect-fixed',action='store_true',
                        help='Exit1 when a fixed checker violates the frozen54-case decisions')
    args=parser.parse_args()
    SITE=args.site_dir.resolve();OUT=args.output_dir.resolve()
    require(SITE.is_dir(),'site input directory is absent')
    require(not OUT.is_relative_to(SITE) and not SITE.is_relative_to(OUT),
            'output directory overlaps the input site')
    require(not OUT.exists() or not any(OUT.iterdir()),'refusing to overwrite a prior run')
    OUT.mkdir(parents=True,exist_ok=True)
    sys.dont_write_bytecode=True
    module,script=checker()
    catalog=json.loads((SITE/'src/content/catalog.json').read_bytes())
    records=catalog['records']
    report={'scope':'actual generated-page copies; selected static status checker only; no browser or independent acceptance',
            'inventory':'actual54',
            'probe_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'site_directory':str(SITE),
            'site_head':subprocess.check_output(['git','-C',str(SITE),'rev-parse','HEAD'],text=True).strip(),
            'source_commit':json.loads((SITE/'publication-manifest.json').read_bytes())['commit'],
            'checker_sha256':sha256(script.read_bytes()).hexdigest(),
            'actual_baseline_labelled_pages':module.check_status_labels(SITE/'public',records),
            'inputs':{},'cases':[],'structures':{}}
    work='geometry-of-semantic-representations'
    for locale in LOCALES:
        rel=Path(locale)/'programme/index.html'
        html=(SITE/'public'/rel).read_text();tree=Tree(html)
        owners=badges(tree,work)
        require(len(owners)>=2,locale+': need duplicate actual programme badges')
        report['inputs'][rel.as_posix()]=sha256(html.encode()).hexdigest()
        report['structures'][locale+'/programme']=snippets(tree,work)
        owner=owners[0]
        inner=next(n for n in tree.nodes if n.parent is owner and 'status-badge' in n.classes())
        cases=[('unchanged','valid_baseline',html),
               ('inherited_lang','valid_inherited_language',attribute(html,owner,'lang',False)),
               ('wrong_lang','wrong_explicit_language',attribute(html,owner,'lang','xx')),
               ('empty_lang','unknown_explicit_language',attribute(html,owner,'lang','')),
               ('hidden_badge','explicit_hidden_attribute',attribute(html,inner,'hidden',None)),
               ('aria_hidden_owner','explicit_accessibility_exclusion',attribute(html,owner,'aria-hidden','true')),
               ('inert_owner','explicit_inert_subtree',attribute(html,owner,'inert',None)),
               ('display_none_owner','inline_display_none',attribute(html,owner,'style','display:none')),
               ('visibility_hidden_badge','inline_visibility_hidden',attribute(html,inner,'style','visibility:hidden')),
               ('content_visibility_hidden_owner','inline_content_visibility_hidden',attribute(html,owner,'style','content-visibility:hidden')),
               ('partial_duplicate','missing_one_direct_link_badge',modify(html,[(owner.start,owner.end,'')]))]
        moved=modify(html,[(n.start,n.end,'') for n in owners])
        i=moved.rfind('</footer>');require(i>=0,'footer absent')
        moved=moved[:i]+html[owner.start:owner.end]+moved[i:]
        cases.append(('all_to_footer','all_local_work_badges_misplaced',moved))
        inherited=Tree(cases[1][2]);changed_owner=badges(inherited,work)[0]
        require(changed_owner.language()==locale,'inherited language incorrect')
        for name,condition,text in cases:
            if name!='unchanged':require(text!=html,'mutation unchanged')
            result=old_check(module,records,text,rel,locale+'_'+name)
            report['cases'].append({'locale':locale,'case':name,'condition':condition,**result})
        for section in ('roadmap','engineering/specifications/semantic-verification'):
            rp=Path(locale)/section/'index.html';raw=(SITE/'public'/rp).read_text();t=Tree(raw)
            report['inputs'][rp.as_posix()]=sha256(raw.encode()).hexdigest()
            report['structures'][locale+'/'+section]=snippets(t,work)
            report['cases'].append({'locale':locale,'case':'unchanged_'+section,'condition':'valid_baseline',
                                    **old_check(module,records,raw,rp,locale+'_'+section.replace('/','_'))})
            if section.startswith('engineering/'):
                reader_owners=badges(t,work)
                require(len(reader_owners)==1,'expected one Geometry sidebar status')
                ro=reader_owners[0]
                require(ro.parent and 'rm-linked-status' in ro.parent.classes(),'reader group precondition')
                rb=next(n for n in t.nodes if n.parent is ro and 'status-badge' in n.classes())
                relocated=modify(raw,[(ro.start,ro.end,'')]);fi=relocated.rfind('</footer>')
                require(fi>=0,'reader footer absent')
                relocated=relocated[:fi]+raw[ro.start:ro.end]+relocated[fi:]
                rcases=[('reader_inherited_lang','valid_inherited_language',attribute(raw,ro,'lang',False)),
                        ('reader_wrong_lang','wrong_explicit_language',attribute(raw,ro,'lang','xx')),
                        ('reader_hidden_badge','explicit_hidden_attribute',attribute(raw,rb,'hidden',None)),
                        ('reader_group_to_footer','reader_group_loses_its_status',relocated)]
                for name,condition,text in rcases:
                    require(text!=raw,'reader mutation unchanged')
                    if condition=='valid_inherited_language':
                        require(badges(Tree(text),work)[0].language()==locale,'reader inheritance')
                    report['cases'].append({'locale':locale,'case':name,'condition':condition,
                                            **old_check(module,records,text,rp,locale+'_'+name)})
        rp=Path(locale)/'roadmap/index.html';raw=(SITE/'public'/rp).read_text();t=Tree(raw)
        field_owners=[o for o in badges(t,work) if any(n.tag=='dd' for n in o.chain())]
        report.setdefault('unavailable_controls',[]).append({'locale':locale,
            'case':'roadmap_other_field_does_not_cover','actual_work_badges':len(field_owners),
            'all_work_badges':len(badges(t)),
            'reason':'Not in the frozen actual54 inventory: original generated roadmap had no labelled fields. Test grouped-field design in a separately labelled renderer fixture.'})
    for case in report['cases']:
        case['case_id']=case['locale']+'::'+case['case']
        case['expected_acceptance']=case['condition'].startswith('valid_')
        case['matches_declared_decision']=case['accepted']==case['expected_acceptance']
    require(len(report['cases'])==54 and len({c['case_id'] for c in report['cases']})==54,
            'frozen54 case identity mismatch')
    report['counts']={'cases':len(report['cases']),'checker_accepted':sum(c['accepted'] for c in report['cases']),
                      'matched_decisions':sum(c['matches_declared_decision'] for c in report['cases']),
                      'expected_positive_cases':sum(c['expected_acceptance'] for c in report['cases']),
                      'expected_negative_cases':sum(not c['expected_acceptance'] for c in report['cases']),
                      'conditions':dict(Counter(c['condition'] for c in report['cases']))}
    (OUT/'badge_actual_page_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'structures','cases'}},ensure_ascii=False,indent=2))
    print('case_results',[(c['locale'],c['case'],c['accepted']) for c in report['cases']])
    if args.expect_fixed and report['counts']['matched_decisions']!=len(report['cases']):
        raise SystemExit(1)

if __name__=='__main__':main()
