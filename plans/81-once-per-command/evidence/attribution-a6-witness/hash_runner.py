#!/usr/bin/env python3
"""Source launcher experiment. Run under flock; never import credentials into evidence."""
import argparse
import contextlib
import json
import hashlib
import importlib.metadata
import http.server
import threading
import platform
import re
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path('/root/codex/plan-81m')
locator = argparse.ArgumentParser(add_help=False)
locator.add_argument('--agent', type=Path, required=True)
locator.add_argument('--agent-sha', required=True)
source_identity, _ = locator.parse_known_args()
AGENT, RUNTIME, VIBE = source_identity.agent.resolve(), ROOT/'a4-runtime', ROOT/'VibeComfy'
sys.path[:0] = list(map(str, (AGENT, RUNTIME, VIBE)))
from tests.integrations.test_runpod_slot_path_cpu import SlotPod, _slot_classes
from tests.integrations._pinned_source import attached_comfy
from tests.integrations.runpod_slot_pod import PodComfy, receipt_files
from astrid.core.generation import entries
from astrid.sdk import AstridClient

HOOK = '''\
import json, os, sys, time
from pathlib import Path
if os.environ.get("A4_HOOK_LOG") and sys.argv[0] == "-m" and "start" in sys.argv and "--runtime-checkout" in sys.argv:
 from runtime_protocol.server import RuntimeHandler
 original = RuntimeHandler._send
 Path(os.environ["A4_HOOK_LOG"] + ".loaded").write_text(str(os.getpid()))
 def observed(self, status, payload=None, **kwargs):
  deferred = getattr(self, "_defer_response", False)
  result = original(self, status, payload, **kwargs)
  if not deferred and getattr(self, "command", None) == "POST" and self.path.split("?", 1)[0] == "/v1/tasks" and status == 201:
   with open(os.environ["A4_HOOK_LOG"], "a") as out:
    out.write(json.dumps({"time_ns": time.monotonic_ns(), "task_id": payload["data"]["task_id"]}) + "\\n")
  return result
 RuntimeHandler._send = observed
'''

def main():
 p = argparse.ArgumentParser(parents=[locator]); p.add_argument('output', type=Path); p.add_argument('--trials', type=int, default=5)
 p.add_argument('--routes', nargs='+', choices=['W','I','E'], default=['W','I','E']); p.add_argument('--modes', nargs='+', choices=['plain','timings','importtime','cprofile'], default=['plain','timings','importtime','cprofile'])
 args = p.parse_args()
 if args.trials < 1: p.error('--trials must be positive')
 out=args.output.resolve(); out.mkdir(parents=True, exist_ok=False)
 if len(source_identity.agent_sha)!=40 or any(c not in '0123456789abcdef' for c in source_identity.agent_sha): p.error('--agent-sha must be a full lowercase 40-character SHA')
 manifest={'source':'source', 'python':sys.version, 'executable':sys.executable, 'trials':[], 'seed':12345, 'sampler':'not collected', 'revisions':{}, 'cpu_count':os.cpu_count(), 'cpu':next((line.partition(':')[2].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')), 'unknown'), 'platform':platform.platform(), 'load':os.getloadavg(), 'packages':sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions() if d.metadata.get('Name'))}
 for key,path,expected in [('agent',AGENT,source_identity.agent_sha),('runtime',RUNTIME,'182311f9d363712c0339254bd27e091d0e18318d'),('vibecomfy',VIBE,'799d90f619a6723d0b376b7e77aef09c244a0821')]:
  sha=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
  if sha!=expected or subprocess.check_output(['git','-C',str(path),'status','--porcelain'],text=True).strip(): raise RuntimeError(f'{key} pin or clean state mismatch')
  manifest['revisions'][key]=sha
 ack=[]; original=PodComfy.submit; original_handle=http.server.BaseHTTPRequestHandler.handle_one_request; pending=threading.local()
 def submit(self, body):
  status, payload=original(self, body)
  if status==200: pending.receipt=(payload['prompt_id'],body)
  return status,payload
 def handle(self):
  pending.receipt=None
  result=original_handle(self)
  if getattr(self,'command',None)=='POST' and getattr(self,'path',None)=='/prompt' and pending.receipt is not None:
   prompt_id,body=pending.receipt; ack.append((time.monotonic_ns(),prompt_id,body))
  return result
 PodComfy.submit=submit; http.server.BaseHTTPRequestHandler.handle_one_request=handle
 with tempfile.TemporaryDirectory(prefix='a4-launcher-') as td:
  work=Path(td)
  for name in ('home','tmp','hook'): (work/name).mkdir()
  (work/'hook/sitecustomize.py').write_text(HOOK)
  source=work/'source.json'; source.write_text(json.dumps({'profile':'astrid','source_checkout':str(AGENT),'runtime_checkout':str(RUNTIME),'runtime_environment':sys.prefix}))
  env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','SSL_CERT_FILE') if k in os.environ}
  env.update(HOME=str(work/'home'),TMPDIR=str(work/'tmp'),PYTHONDONTWRITEBYTECODE='1',ASTRID_RUNTIME_DATA_ROOT=str(work/'data'),ASTRID_RUNTIME_SOURCE_MANIFEST=str(source),ASTRID_RUNTIME_CHECKOUT=str(RUNTIME),ASTRID_PACK_HOST_PYTHON=sys.executable,ASTRID_RUNTIME_DOOR_PORT='0',PYTHONPATH=os.pathsep.join(map(str,(work/'hook',AGENT,RUNTIME,VIBE))),A4_HOOK_LOG=str(work/'admissions.jsonl'))
  cli_env=dict(env); cli_env.pop('A4_HOOK_LOG'); cli_env['PYTHONPATH']=os.pathsep.join(map(str,(AGENT,RUNTIME,VIBE)))
  os.environ.clear(); os.environ.update(env)
  launcher=[sys.executable,'-m','astrid_runtime']; console='/root/codex/plan-81m/run/a2-hash/astrid'
  manifest['console']=console; manifest['console_sha256']=hashlib.sha256(Path(console).read_bytes()).hexdigest()
  def redact(data):
   data=data.replace(str(work).encode(),b'<scratch>')
   return re.sub(rb'http://127\.0\.0\.1:\d+', b'<local-redacted>', data)
  def run(cmd):
   result=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=180)
   if result.returncode: raise RuntimeError(f'{cmd[:4]} failed: {result.stderr[-4000:]} {result.stdout[-4000:]}')
   return result
  target_stack=contextlib.ExitStack()
  try:
   run(launcher+['workspace','create','--realm-root',str(work/'realm'),'--process-control','sandbox','--hosted-origin','off','--json'])
   with AstridClient.open_from_launcher() as client:
    identity=subprocess.check_output([sys.executable,'-c','import astrid; print(astrid.__file__)'],env=cli_env,text=True).strip()
    if not Path(identity).resolve().is_relative_to(AGENT): raise RuntimeError('console does not import pinned source')
    manifest['agent_module']=identity
    if not (work/'admissions.jsonl.loaded').is_file(): raise RuntimeError('Runtime response hook did not load')
    registration=json.loads((work/'data/runtime/generic-host.json').read_text())
    if Path(registration['source_checkout']).resolve()!=AGENT: raise RuntimeError('host source checkout mismatch')
    manifest['host_source_checkout']=registration['source_checkout']
    created=client.projects.create(name='Attribution',slug='attribution',idempotency_key='project')
    if not created.ok: raise RuntimeError(str(created.error))
    project=created.data['project_id']
    provider=SlotPod(work/'claim.json',work/'attempts',_slot_classes(('image','t2i')))
    files=[path for engine in dict.fromkeys(('comfyui',*entries.runpod_engines())) for path in receipt_files(provider._receipt_for(engine))]
    provider.comfy.installed_files=lambda:files
    (out/'target-inventory.json').write_text(json.dumps(provider.comfy.object_info(),sort_keys=True,indent=2)+'\n')
    manifest['target_inventory']='target-inventory.json'
    manifest['response_clock']='monotonic_ns; Runtime and target server response emission after write; hook overhead included'
    manifest['cli_hook']='none; Runtime observer exists only in launcher-managed daemon'
    with contextlib.nullcontext(target_stack.enter_context(attached_comfy(provider.comfy))) as url:
     seen=set()
     for route in args.routes:
      for mode in args.modes:
       for n in range(-1,args.trials):
        label=f'{route}-{mode}-'+('warmup' if n<0 else str(n+1)); prompt=f'A red cube on a white tabletop. {label}'
        base=['generate']+(['workflow',str(VIBE/'ready_templates/image/qwen_image_2_1_turbo.py'),'--prompt',prompt] if route=='W' else ['image',prompt])
        if route=='E': base+=['--entry','qwen-image-2.1-turbo']
        base+=['--placement',url,'--project',project,'--seed','12345','--no-wait','--json']
        if mode in ('plain','timings'): base+=['--timings']
        profile=out/f'{label}.prof'
        launch=[console,*base] if mode in ('plain','timings','importtime') else [sys.executable,'-m','cProfile','-o',str(profile),console,*base]
        trial_env=dict(cli_env)
        trial_env['A4_HASH_LOG']=str(out/f'{label}.hash.json')
        if mode=='importtime': trial_env['PYTHONPROFILEIMPORTTIME']='1'
        before=len(ack); start=time.monotonic_ns(); proc=subprocess.run(launch,env=trial_env,capture_output=True,timeout=240); end=time.monotonic_ns()
        (out/f'{label}.stdout').write_bytes(redact(proc.stdout))
        (out/f'{label}.stderr').write_bytes(redact(proc.stderr))
        row={'route':route,'mode':mode,'warmup':n<0,'trial':n+1,'returncode':proc.returncode,'spawn_ns':start,'exit_ns':end,'wall_seconds':(end-start)/1e9,'stdout':f'{label}.stdout','stderr':f'{label}.stderr','profile':profile.name if mode=='cprofile' else None,'load':os.getloadavg(),'prompt':prompt,'hash_log':f'{label}.hash.json','argv':[x.replace(url,'<target>').replace(str(work),'<scratch>') for x in launch]}
        manifest['trials'].append(row); (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        if proc.returncode: raise RuntimeError(f'{label} failed; see raw output')
        payload=json.loads(proc.stdout); task=payload.get('kernel_task_id') or payload.get('task_id')
        if not task or task in seen: raise RuntimeError(f'{label}: task missing or repeated')
        seen.add(task); deadline=time.monotonic()+120
        while time.monotonic()<deadline:
         result=client.tasks.show(task)
         if result.ok and result.data.get('state') in ('succeeded','failed','cancelled'): break
         time.sleep(.05)
        if not result.ok or result.data.get('state')!='succeeded': raise RuntimeError(f'{label}: task did not succeed')
        hook=work/'admissions.jsonl'; receipt_deadline=time.monotonic()+5
        while True:
         rows=[json.loads(line) for line in hook.read_text().splitlines()] if hook.exists() else []
         matches=[r for r in rows if task == r['task_id']]
         acks=ack[before:]
         if matches and acks or time.monotonic()>=receipt_deadline: break
         time.sleep(.01)
        if len(matches)!=1 or len(acks)!=1 or prompt not in json.dumps(acks[0][2]): raise RuntimeError(f'{label}: admission or target mismatch')
        row.update(task_id=task,admission_ns=matches[0]['time_ns'],target_ack_ns=acks[0][0],target_prompt_id=acks[0][1],task_state='succeeded')
        (out/f'{label}.target.json').write_text(json.dumps(acks[0][2],indent=2)+'\n'); (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(label,'ok',flush=True)
  finally:
   PodComfy.submit=original; http.server.BaseHTTPRequestHandler.handle_one_request=original_handle
   had_error=sys.exc_info()[0] is not None
   try:
    stopped=subprocess.run(launcher+['down','--profile','astrid','--data-root',str(work/'data'),'--source-manifest',str(source),'--hosted-origin','off','--json'],env=env,capture_output=True,timeout=90)
   finally:
    target_stack.close()
   (out/'teardown.stderr').write_bytes(redact(stopped.stderr))
   manifest['teardown_returncode']=stopped.returncode
   (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
   if stopped.returncode and not had_error: raise RuntimeError('Runtime down failed; see teardown stderr')

if __name__=='__main__': main()
