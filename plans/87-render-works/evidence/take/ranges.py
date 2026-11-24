#!/usr/bin/env python3
"""Render the film in product-rendered ranges, one after another, retrying a failed range."""
import json, subprocess, sys, time, glob, os, shutil
S="~"
R=os.path.expanduser("~/astrid-release/release-14-r6-fixes")
RANGES=[("0","50"),("50","100"),("100","150"),("150","196.566666")]
profile={"width":1920,"height":1080,"fps_rational":[30,1],"time_base":[1,90000],"container":"mp4","video_codec":"h264","video_profile":None,"video_level":None,"pixel_format":"yuv420p","audio_codec":"aac","audio_sample_rate":48000,"audio_channel_layout":"stereo","duration_tolerance":1}
status=open(S+"/take/ranges-status.log","a")
def say(m):
    status.write(time.strftime("%H:%M:%S ")+m+"\n"); status.flush()
def clean():
    for d in glob.glob(R+"/data/attempts/*/astrid-attempt-*"): shutil.rmtree(d, ignore_errors=True)
def run(i,a,b,attempt):
    name=f"r6-part{i}-try{attempt}"
    argv=["bash",S+"/fixed/astrid.sh","timelines","render","77f906f3242c48179ab86ca7c3e62eb4","--project","801a01b3a87941a1ab25958c488afdbf","--backend","rendering.remotion","--profile",json.dumps(profile),"--output-name",name+".mp4","--wait","--timeout-seconds","14400","--json","--expected-version","38","--range",a,b]
    t=time.time(); out=""
    p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd="/tmp")
    with open(f"{S}/take/{name}.log","w") as log:
        for line in p.stdout:
            log.write(time.strftime("%H:%M:%S ")+line); log.flush()
            if line.strip().startswith("{"): out=line.strip()
    p.wait()
    try: d=json.loads(out)
    except Exception: d={}
    if d.get("ok"):
        art=[x for x in d["data"]["outputs"]["artifacts"] if x.get("is_primary")][0]
        dg=art["digest"].split(":")[1]
        src=glob.glob(f"{R}/data/runtime/realms/*/cas/sha256/{dg[:2]}/{dg[2:]}")[0]
        dst=f"{S}/take/part{i}.mp4"; shutil.copy(src,dst)
        say(f"part {i} [{a}-{b}] OK in {time.time()-t:.0f}s size {art['size']} -> {dst}")
        return True
    msg=(d.get("error") or {}).get("message","no json")[:300].replace("\n"," | ")
    say(f"part {i} [{a}-{b}] FAILED try {attempt} after {time.time()-t:.0f}s: {msg}")
    tid=((d.get("error") or {}).get("details") or {}).get("kernel_task_id")
    if tid: subprocess.run(["bash",S+"/fixed/astrid.sh","tasks","cancel",tid,"--project","801a01b3a87941a1ab25958c488afdbf","--json"],capture_output=True,cwd="/tmp")
    return False
say("START ranges "+str(RANGES))
for i,(a,b) in enumerate(RANGES):
    if os.path.exists(f"{S}/take/part{i}.mp4"): say(f"part {i} already done"); continue
    for attempt in (1,2,3):
        clean()
        if run(i,a,b,attempt): break
    else:
        say(f"GIVING UP on part {i}"); sys.exit(1)
say("ALL PARTS DONE")
