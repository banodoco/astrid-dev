#!/usr/bin/env bash
set -u
cd /root/codex/plan-81
python3 -u -c 'import datetime,json,os,time
p="run/us2-post69/trial-d-load.jsonl"
while True:
 with open(p,"a") as f:f.write(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"load1":os.getloadavg()[0]})+"\n")
 time.sleep(30)' & sampler=$!
trap 'kill "$sampler" 2>/dev/null || :; wait "$sampler" 2>/dev/null || :' EXIT
bash run/us2-post69/run.sh post69-gate-d-545238
