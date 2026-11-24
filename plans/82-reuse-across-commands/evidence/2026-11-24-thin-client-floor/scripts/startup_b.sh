#!/usr/bin/env bash
# B: interpreter start and import cost on the installed build. Run after env.sh; OUT dir as $1.
set -euo pipefail
OUT=$1; mkdir -p "$OUT"
. /root/plan82-floor/scripts/venv-env.sh
t() { python3 - "$@" <<'PY'
import subprocess, sys, time, statistics, json
n = int(sys.argv[1]); cmd = sys.argv[2:]
subprocess.run(cmd, capture_output=True)  # warm-up
w = []
for _ in range(n):
    t0 = time.perf_counter(); subprocess.run(cmd, capture_output=True); w.append(time.perf_counter() - t0)
print(json.dumps({"cmd": " ".join(cmd)[-90:], "median": round(statistics.median(w), 4), "samples": [round(x, 4) for x in w]}))
PY
}
{
t 7 "$VPY" -I -S -c pass
t 7 "$VPY" -I -c pass
t 7 "$VPY" -X utf8 -I -c pass
t 7 sh -c :
t 5 "$PROGRAM/run-astrid" --version
t 5 "$VPY" -X utf8 -I -m astrid.omp_agent --version
t 7 "$VPY" -I -S /root/plan82-floor/scripts/thin_client.py validation x 1
} > "$OUT/startup.jsonl"
cat "$OUT/startup.jsonl"
# import graph of the real generate command (the second process run_astrid.py execs into)
for i in 1 2 3; do
  "$VPY" -X utf8 -X importtime -I -m astrid.omp_agent generate image "a red square on a plain background" --mode t2i \
    --placement http://127.0.0.1:18388 --project floor --no-wait --json > "$OUT/importtime-$i.stdout" 2> "$OUT/importtime-$i.stderr"
  python3 /root/plan82-floor/scripts/hostreq.py "{\"mode\":\"wait\",\"task_id\":\"$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["kernel_task_id"])' "$OUT/importtime-$i.stdout")\"}" 60 >/dev/null
  sleep 20
done
"$VPY" -I -S -X importtime /root/plan82-floor/scripts/thin_client.py validation x 1 > /dev/null 2> "$OUT/importtime-thin-client.stderr" || true
