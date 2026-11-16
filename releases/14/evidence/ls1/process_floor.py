#!/usr/bin/env python3
"""Measure fresh interpreter and prebuilt native no-op process wall time."""
import argparse,json,statistics,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--native',required=True); p.add_argument('--output',required=True); p.add_argument('--samples',type=int,default=20); a=p.parse_args()
rows=[]
for name,cmd in [('python',[sys.executable,'-c','pass']),('native',[a.native])]:
    for i in range(a.samples):
        t=time.perf_counter_ns(); subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); rows.append({'kind':name,'sample':i,'wall_ms':(time.perf_counter_ns()-t)/1e6})
summary={name:{'median':statistics.median(r['wall_ms'] for r in rows if r['kind']==name),'max':max(r['wall_ms'] for r in rows if r['kind']==name)} for name in ('python','native')}
Path(a.output).write_text(json.dumps({'summary_ms':summary,'records':rows},indent=2)+'\n'); print(json.dumps(summary,indent=2))
