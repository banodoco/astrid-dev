from pathlib import Path
import json,shutil,subprocess,hashlib
base=Path('/home/user/cells/evidence/h3real');p=base/'package'; rows=[]
for n in ['T2-video-only','T3-corrected','T4','T5a-video-only','T5b-video-only']:
 f=p/'dryrun'/f'{n}.output.json'
 d=json.loads(f.read_text()); code=int((p/'dryrun'/f'{n}.exit').read_text())
 assert code==0 and d['status']=='ready' and not d['fixes'] and not d['issues']
 assert d['entry']['bindings']['seed']==42
 job=Path(d['entry']['job_dir']).name;src=base/'plan-snapshots'/job
 assert src.exists(), f'missing graph snapshot for {n}: {job}'
 if src.exists():
  for k in ['compilation.json','workflow.vibe.json']:
   shutil.copy2(src/k,p/'dryrun'/f'{n}.{k}')
  assert hashlib.sha256((src/'workflow.vibe.json').read_bytes()).hexdigest() == d['entry']['build_plan']['workflow_members']['workflow.vibe.json']
 rows.append({'test':n,'exit':code,'status':d['status'],'target_state':d['target']['state'],'seed':d['entry']['bindings']['seed'],'steps':d['entry']['bindings']['steps'],'captured_job':job})
(p/'dryrun/summary.json').write_text(json.dumps(rows,indent=2)+'\n')
with (p/'plan-checks.log').open('w') as out:
 for n,steps,turbo in [('T5a-video-only','8','on'),('T5b-video-only','20','off')]:
  cmd=['python3','check_plan.py',f'dryrun/{n}.output.json',f'dryrun/{n}.workflow.vibe.json',steps,turbo]
  out.write('COMMAND: '+' '.join(cmd)+'\n');out.flush()
  subprocess.run(cmd,cwd=p,stdout=out,stderr=subprocess.STDOUT,check=True)
assert (p/'requests/T4.yaml').read_bytes()==Path('/home/user/cells/evidence/h3live/package/requests/T4.yaml').read_bytes()
assert (p/'selftest.log').read_text().endswith('ALL SELF-TEST EXPECTATIONS PASSED\n')
print(json.dumps(rows,indent=2))
