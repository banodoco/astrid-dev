import os,sys,time,json,datetime,subprocess,pathlib,socket
P=pathlib.Path('/root/codex/p77box/run3/receipts'); base='/root/codex/p77box'; runtime=base+'/stack/program/versions/1d2700baa660/py/bin/astrid-runtime'
E={'PATH':'/usr/bin:/bin','HOME':base+'/stack/home','XDG_DATA_HOME':base+'/stack/home/.local/share','XDG_STATE_HOME':base+'/stack/home/.local/state','TMPDIR':base+'/stack/tmp','ASTRID_NODE_EXECUTABLE':base+'/node-v20.19.4-linux-x64/bin/node','ASTRID_RUNTIME_DOOR_PORT':'17501'}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
def scan():
 result=[]
 for p in pathlib.Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'); s=(p/'stat').read_text().rsplit(')',1)[1].split()
   if base+'/stack/program/' not in cmd or ('astrid-runtime status' in cmd):continue
   if any(x in cmd for x in ('/bin/bash -c','monitor.py','codex exec')):continue
   result.append({'pid':int(p.name),'state':s[0],'cpu_seconds':(int(s[11])+int(s[12]))/os.sysconf('SC_CLK_TCK'),'start_ticks':int(s[19]),'command':cmd[:500]})
  except (OSError,ValueError,IndexError):pass
 return result
start=datetime.datetime.fromisoformat((P/'02-start.txt').read_text().splitlines()[0].replace('Z','+00:00')).timestamp(); dumped=set(); n=1
with (P/'03-monitor.jsonl').open('a',buffering=1) as f:
 while True:
  now=time.time(); delay=start+n*30-now
  if delay>0:time.sleep(delay)
  ts=utc(); procs=scan(); status={}
  try:
   x=subprocess.run([runtime,'status','--data-root',base+'/stack/data','--json'],env=E,capture_output=True,text=True,timeout=8)
   try: status=json.loads(x.stdout)
   except ValueError: status={'stdout':x.stdout,'stderr':x.stderr}
   status={'exit':x.returncode,'result':status}
  except subprocess.TimeoutExpired:status={'timeout_seconds':8}
  try: free=subprocess.check_output(['free','-m'],text=True)
  except Exception as e:free=str(e)
  support=status.get('result',{}).get('support',{}) if isinstance(status.get('result'),dict) else {}
  discovery=status.get('result',{}).get('discovery') if isinstance(status.get('result'),dict) else None
  health=status.get('result',{}).get('health') if isinstance(status.get('result'),dict) else None
  record={'scheduled_seconds':n*30,'utc':ts,'status':status,'discovery_answered':bool(discovery),'health_answered':bool(health),'processes':procs,'free_m':free}
  f.write(json.dumps(record)+'\n')
  if support.get('healthy') is True and discovery and isinstance(health,dict) and health.get('status')=='ok':
   (P/'03-observation-final.done').write_text(json.dumps({'outcome':'healthy_observed','utc':utc(),'observation_utc':ts})+'\n');break
  elapsed=time.time()-start
  for threshold in (30,120,300):
   if elapsed>=threshold and threshold not in dumped:
    dumped.add(threshold); target=max(procs,key=lambda v:v['cpu_seconds'],default=None)
    with (P/f'03-pyspy-{threshold}.txt').open('w') as d:
     d.write(f'utc={utc()} target={target}\n');d.flush()
     if target:
      try:
       z=subprocess.run(['/tmp/phaseA-pyspy/venv/bin/py-spy','dump','--pid',str(target['pid'])],stdout=d,stderr=subprocess.STDOUT,timeout=20);d.write(f'\nexit={z.returncode}\n')
      except Exception as e:d.write(f'error={e}\n')
     else:d.write('No process found.\n')
  if (P/'02-up.done').exists() and not procs:
   (P/'03-observation-final.done').write_text(json.dumps({'outcome':'up_finished_no_process','utc':utc()})+'\n');break
  if elapsed>=2700:
   (P/'03-observation-final.done').write_text(json.dumps({'outcome':'45_minute_limit','utc':utc()})+'\n');break
  n+=1
