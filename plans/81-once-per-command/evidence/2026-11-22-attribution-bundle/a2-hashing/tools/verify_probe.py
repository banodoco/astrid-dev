import json, os, subprocess, sys, tempfile
from pathlib import Path
with tempfile.TemporaryDirectory(prefix='a4-launcher-probe-') as d:
 root=Path(d); p=root/'known.py'; p.write_bytes(b'private-fixture-contents-42'); y=root/'known.yaml'; y.write_text('answer: 42\n'); output=root/'events.json'
 code='''import hashlib,json,sys,yaml
from pathlib import Path
from hash_probe import install
p,y=map(Path,sys.argv[1:]); expected=hashlib.sha256(b'private-fixture-contents-42').hexdigest(); install()
for _ in range(2):
 data=p.read_bytes(); assert hashlib.sha256(data).hexdigest()==expected
with p.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()==expected
assert yaml.safe_load(y.read_text())=={'answer':42}
try: hashlib.sha256('bad')
except TypeError: pass
else: raise AssertionError('hash exception changed')
try: yaml.safe_load('[unterminated')
except yaml.YAMLError: pass
else: raise AssertionError('yaml exception changed')
import hash_probe
class Broken:
 def append(self,*a): raise RuntimeError('observer fault')
hash_probe._events=Broken()
assert hashlib.sha256(b'x').hexdigest()==hashlib.new('sha256',b'x').hexdigest()
assert yaml.safe_load('a: 1')=={'a':1}
'''
 env={k:os.environ[k] for k in ('PATH','LANG') if k in os.environ}; env.update(PYTHONPATH='/root/codex/plan-81m/run/a2-hash',A4_HASH_LOG=str(output))
 # Preserve event list before injected failure in a second process for assertions.
 clean=code.split('import hash_probe\nclass Broken:')[0]
 run=subprocess.run([sys.executable,'-c',clean,str(p),str(y)],env=env,capture_output=True,text=True); assert run.returncode==0,run.stderr
 x=json.loads(output.read_text()); events=x['events']; hashes=[e for e in events if e['kind']=='sha256' and e['path'] and e['path'].endswith('known.py')]; files=[e for e in events if e['kind']=='sha256.file_digest']; loads=[e for e in events if e['kind']=='yaml.safe_load' and e['path'] and e['path'].endswith('known.yaml')]
 assert len(hashes)==2 and all(e['bytes']==len(b'private-fixture-contents-42') and e['metadata_before']==e['metadata_after'] for e in hashes),hashes
 assert len(files)==1 and files[0]['bytes']==len(b'private-fixture-contents-42') and files[0]['metadata_before']==files[0]['metadata_after'],files
 assert len(loads)==1,loads
 assert 'private-fixture-contents-42' not in output.read_text()
 env.pop('A4_HASH_LOG'); run=subprocess.run([sys.executable,'-c',code,str(p),str(y)],env=env,capture_output=True,text=True); assert run.returncode==0,run.stderr
 print('PASS repeated read linkage, byte counts, digest parity, YAML nesting, exception transparency, observer append failure, no content logged')
