"""Narrow fresh-process verification of the retained preflight defect and history binding."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root=Path('/workspace/scratch/5cd1d6f67b86/agent-state-resume')
cli=root/'tools/repository_session.py'
expected='ca4afc21b0256a0c7a7f4d22fea3c483e8ae223a618ef5b87132cd3195c7546a'
assert hashlib.sha256(cli.read_bytes()).hexdigest()==expected
commands=[]
receipts=[]
with tempfile.TemporaryDirectory(prefix='fixed-session-review-') as tmp:
    directory=Path(tmp); repo=directory/'repo'; repo.mkdir()
    def git(*args):
        return subprocess.run(['git','-C',str(repo),*args],check=True,
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode().strip()
    git('init','--initial-branch=main')
    git('config','user.name','Fixed session review')
    git('config','user.email','review@example.invalid')
    (repo/'source.txt').write_text('Initial required source.\n')
    git('add','--','source.txt');git('commit','-m','Initial source')
    def invoke(*args):
        argv=[sys.executable,'-B',str(cli),*map(str,args)]
        result=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        commands.append({'argv':argv,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
        return result
    profile=directory/'profile.json'
    result=invoke('profile','--repo',repo,'--task-id','fixed-preflight-review',
                  '--scope','bounded-fixed-review','--path','source.txt','--output',profile)
    assert result.returncode==0,result.stderr
    def step(operation,previous=None):
        output=directory/f'receipt-{len(receipts)+1}.json'
        args=[operation,'--repo',repo,'--profile',profile,'--output',output]
        if previous is not None:args.extend(['--previous',previous])
        result=invoke(*args)
        receipt=json.loads(output.read_text())
        assert receipt['implementation']['session']==expected
        receipts.append(receipt)
        return output,receipt,result
    a,first,r=step('start');assert r.returncode==0 and first['result']=='READY'
    (repo/'source.txt').write_text('Changed required source.\n')
    git('add','--','source.txt');git('commit','-m','Relevant required change')
    b,failed,r=step('preflight',a);assert r.returncode==1 and failed['result']=='INVALID'
    c,locked,r=step('preflight',b);assert r.returncode==1 and locked['result']=='RESUME_REQUIRED'
    assert failed['adopted_context_id']==locked['adopted_context_id']==first['context_id']
    assert failed['context_id']==locked['context_id']!=first['context_id']
    assert failed['resume_required'] is True and locked['resume_required'] is True
    d,resumed,r=step('resume',c);assert r.returncode==0 and resumed['result']=='READY'
    e,valid,r=step('preflight',d);assert r.returncode==0 and valid['result']=='VALID'
    assert resumed['adopted_context_id']==valid['adopted_context_id']==locked['context_id']
    assert resumed['resume_required'] is False and valid['resume_required'] is False
    assert valid['operations']==['START','PREFLIGHT','PREFLIGHT','RESUME','PREFLIGHT']
    # Change an earlier operation that is followed by a later explicit resume.
    # The final candidate/adopted state is unchanged; the retained predecessor's
    # operation-prefix digest must still detect this changed history.
    altered=deepcopy(valid)
    altered['operations'][1]='RESUME'
    payload={k:v for k,v in altered.items() if k!='receipt_id'}
    altered['receipt_id']=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,
                            separators=(',',':'),allow_nan=False).encode()).hexdigest()
    bad=directory/'altered-history.json';bad.write_text(json.dumps(altered))
    rejected=invoke('inspect','--input',bad)
    assert rejected.returncode==2
    assert 'predecessor disagrees with retained ledger prefix' in rejected.stderr,rejected.stderr
    record={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
      'source_sha256':{'tools/repository_session.py':expected,
          'tools/test_repository_session.py':hashlib.sha256((root/'tools/test_repository_session.py').read_bytes()).hexdigest()},
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'fresh_process_lifecycle':[{k:r[k] for k in ['operation','sequence','result','context_id','adopted_context_id','resume_required']} for r in receipts],
      'history_tamper':{'changed_operation_index':1,'outer_digest_recomputed':True,
                         'final_state_would_be_unchanged_due_to_later_resume':True,
                         'exit_code':rejected.returncode,'error':rejected.stderr.strip()},
      'commands':commands,'result':'PASS',
      'limits':'Two narrow behavioral obligations using real Git and new CLI processes; same controller/model family/host; no external independent acceptance or permission claim.'}
    target=Path(__file__).with_name('fixed-session-result.json')
    with target.open('x') as f:json.dump(record,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
    with Path(__file__).with_name('fixed-session-receipts.json').open('x') as f:
        json.dump(receipts,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
    assert hashlib.sha256(cli.read_bytes()).hexdigest()==expected
    print('successor lifecycle:',[r['result'] for r in receipts])
    print('history tamper:',rejected.returncode,rejected.stderr.strip())
    print('source SHA256:',expected)
