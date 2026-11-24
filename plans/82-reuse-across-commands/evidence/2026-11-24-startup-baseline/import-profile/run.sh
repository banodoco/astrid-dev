#!/usr/bin/env bash
# Real `astrid generate image ... --no-wait` from the dev checkout (plan-82-base) against the stand-in ComfyUI on loopback,
# under python -X importtime. Isolated HOME + isolated Runtime data root; runs from $O (not the checkout) so no
# .astrid-data is created in the repo. Runs the command twice: cold (starts pack host) then warm. Usage: run.sh [PORT]
set -u
E=/home/user/astrid-agent.env; CO=/home/user/astrid-agent
O=/home/user/baseline/importprofile; H=$O/home; PORT=${1:-18391}
SD=/home/user/astrid-dev/plans/81-once-per-command/evidence/installed-container-baseline/standin
mkdir -p $H/.local/share $H/.local/state $H/.config $H/.cache $O/tmp $O/data
export HOME=$H XDG_DATA_HOME=$H/.local/share XDG_STATE_HOME=$H/.local/state XDG_CONFIG_HOME=$H/.config XDG_CACHE_HOME=$H/.cache TMPDIR=$O/tmp
unset ASTRID_RUNTIME_ENDPOINT ASTRID_RUNTIME_CREDENTIAL ASTRID_PREPARED_CONNECTION
export PYTHONPATH=$E/vibecomfy:$CO ASTRID_RUNTIME_CHECKOUT=$E/runtime ASTRID_VIBECOMFY_CHECKOUT=$E/vibecomfy
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8
export ASTRID_RUNTIME_LAUNCHER=$E/venv/bin/astrid-runtime ASTRID_RUNTIME_DATA_ROOT=$O/data ASTRID_RUNTIME_DOOR_PORT=${DOOR:-17483}
export PATH=$E/venv/bin:/usr/local/bin:/usr/bin:/bin
PY=$E/venv/bin/python
cd $O
cat > $O/source-profile.json <<JSON
{"profile": "astrid", "source_checkout": "$CO", "runtime_checkout": "$E/runtime", "runtime_environment": "$E/venv"}
JSON
$PY $SD/standin_comfy.py --port $PORT > $O/standin.log 2>&1 &
SP=$!; trap 'kill $SP 2>/dev/null; $E/venv/bin/astrid-runtime down --data-root $O/data >/dev/null 2>&1' EXIT
for i in $(seq 1 60); do grep -q "stand-in ComfyUI" $O/standin.log 2>/dev/null && break; sleep 1; done
cat $O/standin.log
$E/venv/bin/astrid-runtime workspace create --profile astrid --data-root $O/data --realm-root $O/data/runtime/realms/realm-floor --realm-id realm-floor --source-manifest $O/source-profile.json --json > $O/workspace-create.json 2> $O/workspace-create.err
echo "workspace create rc=$?"
$E/venv/bin/astrid-runtime up --profile astrid --source-manifest $O/source-profile.json --data-root $O/data --door-port $ASTRID_RUNTIME_DOOR_PORT --hosted-origin off --json > $O/runtime-up.json 2> $O/runtime-up.err
echo "runtime up rc=$?"
$PY -X utf8 -m astrid.omp_agent projects create floor --name floor --select --json > $O/project-create.json 2> $O/project-create.err; echo "project create rc=$?"
: > $O/result.txt
for run in cold warm; do
  t0=$(date +%s.%N)
  timeout 280 $PY -X utf8 -X importtime -m astrid.omp_agent generate image "a red square on a plain background" --mode t2i \
    --placement http://127.0.0.1:$PORT --project floor --no-wait --json --timings > $O/generate-$run.stdout 2> $O/importtime-$run.stderr
  rc=$?; t1=$(date +%s.%N)
  echo "$run exit=$rc wall=$(echo "$t1 - $t0" | bc)" | tee -a $O/result.txt
  sleep 15
done
# third run: attribute who triggers the four named imports (stack of the first import of each)
$PY -X utf8 /home/user/baseline/importprofile/trace_importer.py generate image "a red square on a plain background" --mode t2i \
  --placement http://127.0.0.1:$PORT --project floor --no-wait --json > $O/generate-trace.stdout 2> $O/trace.stderr; echo "trace exit=$?" | tee -a $O/result.txt
