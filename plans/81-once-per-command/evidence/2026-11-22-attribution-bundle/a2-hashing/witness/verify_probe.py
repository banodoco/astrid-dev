import json,os,subprocess,sys,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory(prefix='a4-launcher-witness-') as d:
 p=Path(d)/'known.json'; p.write_text('{"fixture": 42}')
 log=Path(d)/'events.json'
 code='''from pathlib import Path
import sys
import vibecomfy.porting.object_info.generation as g
import vibecomfy.porting.object_info.consume as c
from witness_probe import install
p=Path(sys.argv[1]); expected=g.cache_file_witness(p); install()
def outer():
 def inner():return g.cache_file_witness(p)
 return inner()
assert outer()==expected
assert c.cache_file_witness(p)==expected
assert g.cache_file_witness(p.parent/'missing.json') is None
'''
 env={k:os.environ[k] for k in ('PATH','LANG') if k in os.environ};env.update(PYTHONPATH='/root/codex/plan-81m/run/a2-witness:/root/codex/plan-81m/VibeComfy',A4_WITNESS_LOG=str(log))
 result=subprocess.run([sys.executable,'-c',code,str(p)],env=env,capture_output=True,text=True);assert result.returncode==0,result.stderr
 x=json.loads(log.read_text());assert len(x['events'])==3
 names=[frame[2] for frame in x['events'][0]['stack']]; assert names[:2]==['inner','outer'],names
 assert all(e['metadata_before']==e['metadata_after'] for e in x['events'])
 assert 'fixture": 42' not in log.read_text()
 print('PASS witness parity, preloaded alias, missing-file behavior, complete caller stack and no content logging')
