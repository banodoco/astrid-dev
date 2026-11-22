#!/usr/bin/env bash
set -u
cd /root/codex/plan-81
log=run/us2-post69/clean-wait.jsonl
start=$(date -u +%s)
while :; do
 python3 - "$log" <<'PY'
import datetime,json,os,sys
with open(sys.argv[1],'a') as f:f.write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'load1':os.getloadavg()[0]})+'\n')
PY
 if python3 -c 'import os,sys;sys.exit(0 if os.getloadavg()[0] < 1.0 else 1)'; then
  flock -n /tmp/astrid-timing.lock bash -c '
   python3 -c "import os,sys;sys.exit(0 if os.getloadavg()[0] < 1.0 else 75)" || exit 75
   python3 -u -c '\''import datetime,json,os,time
p="run/us2-post69/gate-clean-load.jsonl"
while True:
 with open(p,"a") as f:f.write(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"load1":os.getloadavg()[0]})+"\n")
 time.sleep(30)'\'' & sampler=$!
   trap '\''kill "$sampler" 2>/dev/null || :; wait "$sampler" 2>/dev/null || :'\'' EXIT
   bash run/us2-post69/run.sh post69-gate-clean-545238
  '
  rc=$?
  if [ "$rc" -ne 75 ] && [ "$rc" -ne 1 ]; then exit "$rc"; fi
  if [ -d run/us2-normalized/post69-gate-clean-545238 ]; then exit "$rc"; fi
 fi
 now=$(date -u +%s)
 if [ $((now-start)) -ge 600 ]; then echo 'no qualifying low-load slot within 10 minutes'; exit 75; fi
 sleep 30
done
