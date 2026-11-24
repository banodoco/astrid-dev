#!/usr/bin/env python3
"""Source launcher experiment. Run under flock; never import credentials into evidence."""
import argparse
import ast
import contextlib
import json
import hashlib
import importlib.metadata
import http.server
import threading
import platform
import re
import site as site_module
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
sys.dont_write_bytecode = True

ROOT = Path('/root/codex/plan-81m')
locator = argparse.ArgumentParser(add_help=False)
locator.add_argument('--agent', type=Path, required=True)
locator.add_argument('--agent-sha', required=True)
locator.add_argument('--vibe', type=Path, default=ROOT/'witness-vibe-base')
locator.add_argument('--vibe-sha', default='48b5fa9e45630e1bc502651975ec0ef3a5e74c4c')
source_identity, _ = locator.parse_known_args()
AGENT, RUNTIME, VIBE = source_identity.agent.resolve(), ROOT/'a4-runtime', source_identity.vibe.resolve()
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
 p.add_argument('--observer-log', action='store_true', help='enable CLI hash observer for measured processes')
 p.add_argument('--attest', choices=['before', 'after'], help='run an untimed host import attestation for this arm')
 p.add_argument('--target-url', required=True); p.add_argument('--target-receipts', type=Path, required=True)
 p.add_argument('--routes', nargs='+', choices=['W'], default=['W']); p.add_argument('--modes', nargs='+', choices=['plain','timings'], default=['plain','timings'])
 args = p.parse_args()
 if args.trials < 1: p.error('--trials must be positive')
 out=args.output.resolve(); out.mkdir(parents=True, exist_ok=False)
 if len(source_identity.agent_sha)!=40 or any(c not in '0123456789abcdef' for c in source_identity.agent_sha): p.error('--agent-sha must be a full lowercase 40-character SHA')
 if source_identity.agent_sha != '72bc29d88e0c1a605842a9f9407e5ca4dbfcb17a': raise RuntimeError('A-6 profile source SHA mismatch')
 manifest={'source':'source', 'python':sys.version, 'executable':sys.executable, 'trials':[], 'seed':12345, 'sampler':'not collected', 'revisions':{}, 'cpu_count':os.cpu_count(), 'cpu':next((line.partition(':')[2].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')), 'unknown'), 'platform':platform.platform(), 'load':os.getloadavg(), 'packages':sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions() if d.metadata.get('Name'))}
 for key,path,expected in [('agent',AGENT,source_identity.agent_sha),('runtime',RUNTIME,'182311f9d363712c0339254bd27e091d0e18318d'),('vibecomfy',VIBE,source_identity.vibe_sha)]:
  sha=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
  if sha!=expected or subprocess.check_output(['git','-C',str(path),'status','--porcelain'],text=True).strip(): raise RuntimeError(f'{key} pin or clean state mismatch')
  manifest['revisions'][key]=sha
 with tempfile.TemporaryDirectory(prefix='a4-launcher-') as td:
  work=Path(td)
  for name in ('home','tmp','hook'): (work/name).mkdir()
  (work/'hook/sitecustomize.py').write_text(HOOK)
  (work/'hook/hash_probe.py').write_bytes(Path(__file__).with_name('hash_probe.py').read_bytes())
  with (work/'hook/sitecustomize.py').open('a') as site:
   site.write('\nif os.environ.get("A4_HASH_LOG"):\n import hash_probe\n hash_probe.install()\n')
  source=work/'source.json'; source.write_text(json.dumps({'profile':'astrid','source_checkout':str(AGENT),'runtime_checkout':str(RUNTIME),'runtime_environment':sys.prefix}))
  env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','SSL_CERT_FILE') if k in os.environ}
  env.update(HOME=str(work/'home'),TMPDIR=str(work/'tmp'),PYTHONDONTWRITEBYTECODE='1',ASTRID_RUNTIME_DATA_ROOT=str(work/'data'),ASTRID_RUNTIME_SOURCE_MANIFEST=str(source),ASTRID_RUNTIME_CHECKOUT=str(RUNTIME),ASTRID_PACK_HOST_PYTHON=sys.executable,ASTRID_RUNTIME_DOOR_PORT='0',PYTHONPATH=os.pathsep.join(map(str,(work/'hook',AGENT,RUNTIME,VIBE))),A4_HOOK_LOG=str(work/'admissions.jsonl'))
  cli_env=dict(env); cli_env.pop('A4_HOOK_LOG'); cli_env['PYTHONPATH']=os.pathsep.join(map(str,(AGENT,RUNTIME,VIBE)))
  os.environ.clear(); os.environ.update(env)
  launcher=[sys.executable,'-m','astrid_runtime']; console=Path(__file__).with_name('astrid')
  shebang=console.open().readline().strip()[2:]
  if Path(shebang).resolve()!=Path(sys.executable).resolve(): raise RuntimeError('current interpreter binary does not match the pinned console shebang')
  module_path=Path(__import__('astrid.console', fromlist=['']).__file__).resolve()
  manifest['console']=str(console); manifest['console_sha256']=hashlib.sha256(console.read_bytes()).hexdigest()
  manifest['interpreter']=sys.executable; manifest['interpreter_sha256']=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()
  manifest['console_module']=str(module_path); manifest['console_module_sha256']=hashlib.sha256(module_path.read_bytes()).hexdigest()
  manifest['vibe_template_sha256']=hashlib.sha256((VIBE/'ready_templates/image/qwen_image_2_1_turbo.py').read_bytes()).hexdigest()
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
    vibe_identity=subprocess.check_output([sys.executable,'-c','import vibecomfy; print(vibecomfy.__file__)'],env=cli_env,text=True).strip()
    if not Path(vibe_identity).resolve().is_relative_to(VIBE): raise RuntimeError('VibeComfy module does not import pinned checkout')
    manifest['vibe_module']=vibe_identity
    manifest['vibe_module_sha256']=hashlib.sha256(Path(vibe_identity).read_bytes()).hexdigest()
    manifest['agent_module']=identity
    manifest['agent_module_sha256']=hashlib.sha256(Path(identity).read_bytes()).hexdigest()
    if not (work/'admissions.jsonl.loaded').is_file(): raise RuntimeError('Runtime response hook did not load')
    registration=json.loads((work/'data/runtime/generic-host.json').read_text())
    if Path(registration['source_checkout']).resolve()!=AGENT: raise RuntimeError('host source checkout mismatch')
    manifest['host_source_checkout']=registration['source_checkout']
    manifest['host_pid']=registration['pid']
    manifest['host_process_birth_id']=registration.get('process_birth_id')
    created=client.projects.create(name='Attribution',slug='attribution',idempotency_key='project')
    if not created.ok: raise RuntimeError(str(created.error))
    project=created.data['project_id']
    provider=SlotPod(work/'claim.json',work/'attempts',_slot_classes(('image','t2i')))
    files=[path for engine in dict.fromkeys(('comfyui',*entries.runpod_engines())) for path in receipt_files(provider._receipt_for(engine))]
    provider.comfy.installed_files=lambda:files
    (out/'target-inventory.json').write_text(json.dumps(provider.comfy.object_info(),sort_keys=True,indent=2)+'\n')
    manifest['target_inventory']='target-inventory.json'
    manifest['response_clock']='monotonic_ns; Runtime and target server response emission after write; hook overhead included'
    manifest['cli_hook']='hash observer is CLI-only and enabled only for measured processes when --observer-log is set'
    with contextlib.nullcontext(args.target_url) as url:
     seen=set(); seen_prompts=set()
     for route in args.routes:
      for mode in args.modes:
       for n in range(-1,args.trials):
        label=f'{route}-{mode}-'+('warmup' if n<0 else str(n+1)); prompt=f'A red cube on a white tabletop. {label}'
        base=['generate','workflow',str(VIBE/'ready_templates/image/qwen_image_2_1_turbo.py'),'--prompt',prompt]
        base+=['--placement',url,'--project',project,'--seed','12345','--no-wait','--json']
        if mode == 'timings': base+=['--timings']
        launch=[sys.executable,str(console),*base]
        trial_env=dict(cli_env)
        observer_path=None
        if args.observer_log and n >= 0:
         observer_path=out/f'{label}.hash.json'
         trial_env['A4_HASH_LOG']=str(observer_path)
         trial_env['A6_VIBE_ROOT']=str(VIBE)
         trial_env['PYTHONPATH']=os.pathsep.join(map(str,(work/'hook',AGENT,RUNTIME,VIBE)))
        load_at_start=os.getloadavg()
        if n >= 0 and not args.attest and load_at_start[0] >= 1.0:
         raise RuntimeError(f'busy at CLI sample start: {load_at_start}; sample invalid')
        before=args.target_receipts.stat().st_size; start=time.monotonic_ns(); proc=subprocess.run(launch,env=trial_env,capture_output=True,timeout=240); end=time.monotonic_ns()
        (out/f'{label}.stdout').write_bytes(redact(proc.stdout))
        (out/f'{label}.stderr').write_bytes(redact(proc.stderr))
        row={'route':route,'mode':mode,'warmup':n<0,'trial':n+1,'returncode':proc.returncode,'spawn_ns':start,'exit_ns':end,'wall_seconds':(end-start)/1e9,'stdout':f'{label}.stdout','stderr':f'{label}.stderr','observer_log':observer_path.name if observer_path else None,'load_at_start':load_at_start,'load':os.getloadavg(),'prompt':prompt,'argv':[x.replace(url,'<target>').replace(str(work),'<scratch>') for x in launch]}
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
         with args.target_receipts.open('rb') as receipts:
          receipts.seek(before)
          acks=[json.loads(line) for line in receipts if line.strip()]
         if matches and acks or time.monotonic()>=receipt_deadline: break
         time.sleep(.01)
        if len(matches)!=1 or len(acks)!=1 or prompt not in json.dumps(acks[0]['body']) or acks[0]['prompt_id'] in seen_prompts: raise RuntimeError(f'{label}: admission or target mismatch or repeated target receipt')
        seen_prompts.add(acks[0]['prompt_id'])
        row.update(task_id=task,admission_ns=matches[0]['time_ns'],target_ack_ns=acks[0]['time_ns'],target_prompt_id=acks[0]['prompt_id'],task_state='succeeded')
        (out/f'{label}.target.json').write_text(json.dumps(acks[0]['body'],indent=2)+'\n'); (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(label,'ok',flush=True)
    if args.attest:
     path=VIBE/'vibecomfy/porting/object_info/consume.py'
     tree=ast.parse(path.read_text())
     functions=[node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == '_resolve_class_type']
     if len(functions)!=1: raise RuntimeError('attestation canary function not found uniquely')
     marker=any(isinstance(node, ast.Name) and node.id == '_CLASS_ENTRY_SNAPSHOT' for node in ast.walk(functions[0]))
     if marker != (args.attest == 'after'): raise RuntimeError('attestation canary does not match arm')
     log=out/'host-attestation.jsonl'
     records=[json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
     expected_hash=hashlib.sha256(path.read_bytes()).hexdigest()
     matching=[r for r in records if r['file']==str(path) and r['sha256']==expected_hash
               and Path(r['prefix']).resolve()==Path(sys.prefix).resolve()
               and r['interpreter_sha256']==hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()
               and any(item['pid']==registration['pid'] for item in r['lineage'])]
     if not matching: raise RuntimeError('no actual host or descendant consume.py execution attested')
     pths=[Path(root)/'attribution-source.pth' for root in site_module.getsitepackages() if (Path(root)/'attribution-source.pth').is_file()]
     if len(pths)!=1: raise RuntimeError('arm source .pth is not unique')
     manifest['attestation']={'marker_in_resolve_class_type':marker, 'resolve_class_type_source':ast.get_source_segment(path.read_text(), functions[0]), 'consume_sha256':expected_hash, 'pth':str(pths[0]), 'pth_sha256':hashlib.sha256(pths[0].read_bytes()).hexdigest(), 'records':matching}
     (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  finally:
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
