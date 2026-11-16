"""Repeat the retained pre-fix case without rewriting its historical evidence.

Run this file from any directory. The unchanged observer/model are read from
--adapter-root; the session module is loaded from the archived sibling source.
All fixture effects remain inside a temporary local Git directory. JSON goes to
stdout, so each caller chooses a new output file for a successor execution.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--adapter-root',type=Path,default=Path('/workspace/scratch/5cd1d6f67b86/agent-state-resume'))
args=parser.parse_args()
root=args.adapter_root.resolve()
expected={'tools/repository_observer.py':'0de30dfec05fab77730d905aa04e58efa6a23f50a5fb12e669b3326b3f230cba',
 'engineering/studies/agent-situation-controls/situation.py':'4c15d461e4d67de5984f40a94a7b92f70745c5fc9f2f39aa2681c287c31ed1c1'}
for relative,sha in expected.items():
    if hashlib.sha256((root/relative).read_bytes()).hexdigest()!=sha:
        raise SystemExit('dependency bytes changed: '+relative)
archive=Path(__file__).with_name('repository_session_before_preflight_review.py')
raw=archive.read_bytes()
if hashlib.sha256(raw).hexdigest()!='340e69e85d89aa6da363f0a5cf26a3fb7161176e6c9a3aa9cc1506330de5a63f':
    raise SystemExit('archived session bytes changed')
sys.path.insert(0,str(root))
spec=importlib.util.spec_from_file_location('retained_repository_session',archive)
session=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=session
spec.loader.exec_module(session)
with tempfile.TemporaryDirectory(prefix='retained-session-preflight-') as tmp:
    repo=Path(tmp)/'repo'; repo.mkdir()
    def git(*arguments):
        return subprocess.run(['git','-C',str(repo),*arguments],check=True,
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode().strip()
    git('init','--initial-branch=main')
    git('config','user.name','Retained session review')
    git('config','user.email','review@example.invalid')
    (repo/'source.txt').write_text('First required content.\n')
    git('add','--','source.txt');git('commit','-m','First content')
    profile=session.make_profile(repo,'preflight-case','retained-review',['source.txt'])
    first=session.start(repo,profile)
    (repo/'source.txt').write_text('Second required content.\n')
    git('add','--','source.txt');git('commit','-m','Changed required content')
    second=session.preflight(repo,profile,first)
    third=session.preflight(repo,profile,second)
    reproduced=(first['result']=='READY' and second['result']=='INVALID'
                and third['result']=='VALID'
                and first['context_id']!=second['context_id']==third['context_id'])
    result={'record_kind':'new-execution-of-retained-pre-fix-probe',
      'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
      'session_sha256':hashlib.sha256(raw).hexdigest(),'observer_and_model_sha256':expected,
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'resume_called':False,'finding_reproduced':reproduced,
      'steps':[{'operation':r['operation'],'result':r['result'],'context_id':r['context_id'],
                'prior_validation':r['prior_validation']} for r in (first,second,third)],
      'limits':'Local real Git; same-controller internal review; no external effect or permission.'}
    print(json.dumps(result,sort_keys=True,indent=2))
    if not reproduced:raise SystemExit('retained finding no longer reproduced')
