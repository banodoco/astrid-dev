#!/usr/bin/env python3
"""Run a product render on the fixed stack. usage: render.py NAME [START END]"""
import json, subprocess, sys, time, re
S="~"
name=sys.argv[1]; rng=sys.argv[2:4]
profile={"width":1920,"height":1080,"fps_rational":[30,1],"time_base":[1,90000],"container":"mp4","video_codec":"h264","video_profile":None,"video_level":None,"pixel_format":"yuv420p","audio_codec":"aac","audio_sample_rate":48000,"audio_channel_layout":"stereo","duration_tolerance":1}
argv=["bash",S+"/fixed/astrid.sh","timelines","render","77f906f3242c48179ab86ca7c3e62eb4","--project","801a01b3a87941a1ab25958c488afdbf","--backend","rendering.remotion","--profile",json.dumps(profile),"--output-name",name+".mp4","--wait","--timeout-seconds","14400","--json","--expected-version","38"]
if rng: argv+=["--range",*rng]
t=time.time()
log=open(f"{S}/take/{name}.log","w")
p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd="/tmp")
last=""
for line in p.stdout:
    log.write(f"{time.strftime('%H:%M:%S')} {line}"); log.flush()
    last=line
    s=line.strip()
    if s.startswith("{"):
        try:
            d=json.loads(s); err=d.get("error") or {}
            print("OK" if d.get("ok") else "FAILED", round(time.time()-t,1),"s")
            if err: print(err.get("message","")[:1500]); print("task",err.get("details",{}).get("kernel_task_id"))
            else: print(json.dumps(d)[:2500])
        except Exception as e: print("unparsed:",s[:800])
    elif re.search(r"\d+%|failed|running|queued",s): print(time.strftime('%H:%M:%S'),s[:160])
print("exit",p.wait(),"elapsed",round(time.time()-t,1))
