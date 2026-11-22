#!/usr/bin/env bash
# A/B installed-Astrid run: BEFORE = published Release 14 tuple, AFTER = candidate manifest; two isolated installs,
# one shared stand-in ComfyUI, arms alternated, load-gated.
#   ./run-ab-installed.sh            prepare + validate only (install if absent, versions, --timings check, one UNTIMED command per arm)
#   ./run-ab-installed.sh --run      prepare, then the gated, timed A/B (fails, does not run ungated, if load < 1.0 is not reached)
# Env: CANDIDATE_MANIFEST (default manifest-candidate.json), BEFORE_MANIFEST (default manifest-omp-npm.json),
#      EVIDENCE_DIR, LOAD_MAX (1.0), LOAD_WAIT_SECONDS (600), SAMPLES (5), STANDIN_PORT (18188), KEEP_RUNTIME=1.
# Setting, every time: installed builds, CPU container, stand-in ComfyUI; not covered: a real ComfyUI's node-info answer, GPU work.
set -euo pipefail
IB=/root/codex/installed-baseline; cd "$IB"
MODE=prepare; [ "${1:-}" = "--run" ] && MODE=run
STAMP=$(date -u +%Y%m%d-%H%M%S)
EVIDENCE_DIR=${EVIDENCE_DIR:-$IB/evidence/ab-$MODE-$STAMP}; mkdir -p "$EVIDENCE_DIR"
BEFORE_MANIFEST=${BEFORE_MANIFEST:-$IB/manifest-omp-npm.json}
CANDIDATE_MANIFEST=${CANDIDATE_MANIFEST:-$IB/manifest-candidate.json}
PORT=${STANDIN_PORT:-18188}
echo "SETTING: installed builds, CPU container, stand-in ComfyUI; not covered: a real ComfyUI's node-info answer, GPU work."

arm_env() {  # $1 = before|after ; sets HOME/XDG/TMPDIR/PROGRAM/DATA/DOOR for that arm
  if [ "$1" = before ]; then H=$IB/home; PROGRAM=$IB/program; DATA=$IB/data; TMPD=$IB/scratch/tmp; DOOR=17340
  else H=$IB/home-after; PROGRAM=$IB/program-after; DATA=$IB/data-after; TMPD=$IB/scratch/tmp-after; DOOR=17341; fi
  mkdir -p "$H/.local/share" "$H/.local/state" "$H/.config" "$H/.cache" "$TMPD"
  export HOME=$H XDG_DATA_HOME=$H/.local/share XDG_STATE_HOME=$H/.local/state XDG_CONFIG_HOME=$H/.config XDG_CACHE_HOME=$H/.cache TMPDIR=$TMPD
  export ASTRID_RUNTIME_DOOR_PORT=$DOOR
}
curl -fsS -o "$EVIDENCE_DIR/install.sh" https://astrid.haus/install
for arm in before after; do
  ( arm_env $arm
    M=$BEFORE_MANIFEST; [ $arm = after ] && M=$CANDIDATE_MANIFEST
    cp "$M" "$EVIDENCE_DIR/manifest-$arm.json"
    if ! "$PROGRAM/run-astrid" --version >/dev/null 2>&1; then
      echo "installing $arm arm ($(basename "$M"))"
      sh "$EVIDENCE_DIR/install.sh" --manifest "$M" --root "$PROGRAM" --data-root "$DATA" --yes --autostart off --command on --skills off --skill-copies off </dev/null \
        > "$EVIDENCE_DIR/install-$arm.out" 2>&1 || { echo "INSTALL FAILED ($arm): $(grep -m1 -v '^\(Getting\|Using\|Downloading\|Your choice\)' "$EVIDENCE_DIR/install-$arm.out" | head -c 300); see $EVIDENCE_DIR/install-$arm.out" >&2; exit 1; }
    fi
    cp "$PROGRAM"/versions/*/manifest.json "$EVIDENCE_DIR/installed-manifest-$arm.json"
    # the installed tuple must equal the requested manifest's pins
    python3 - "$M" "$EVIDENCE_DIR/installed-manifest-$arm.json" $arm <<'PY'
import json, sys
want, got = (json.load(open(p)) for p in sys.argv[1:3])
for k in ("agent", "runtime", "vibecomfy", "lifecycle"):
    if want[k]["sha"] != got[k]["sha"]: sys.exit(f"{sys.argv[3]} arm: installed {k} {got[k]['sha'][:8]} != requested {want[k]['sha'][:8]}; remove program/data/home for that arm and re-run")
PY
    "$PROGRAM/run-astrid" --version > "$EVIDENCE_DIR/astrid-version-$arm.txt" 2>&1
  ) || exit 1
done
sha256sum "$EVIDENCE_DIR"/install.sh "$EVIDENCE_DIR"/manifest-before.json "$EVIDENCE_DIR"/manifest-after.json "$EVIDENCE_DIR"/installed-manifest-*.json > "$EVIDENCE_DIR/hashes.txt"
python3 - "$EVIDENCE_DIR" <<'PY'
import json, sys
d = sys.argv[1]
for arm in ("before", "after"):
    m = json.load(open(f"{d}/installed-manifest-{arm}.json"))
    print(f"  {arm}: agent {m['agent']['sha'][:8]} runtime {m['runtime']['sha'][:8]} vibecomfy {m['vibecomfy']['sha'][:8]} lifecycle {m['lifecycle']['sha'][:8]} omp {m['tools']['omp']['source']}")
PY

# shared stand-in ComfyUI, run with the BEFORE arm's venv python (validated to serve both arms)
BPY=$(echo "$IB"/program/versions/*/py/bin/python | cut -d' ' -f1)
"$BPY" -I "$IB/standin/standin_comfy.py" --port "$PORT" >"$EVIDENCE_DIR/standin.log" 2>&1 &
STANDIN_PID=$!; SAMPLER=
cleanup() {
  [ -n "$SAMPLER" ] && kill "$SAMPLER" 2>/dev/null || true
  kill "$STANDIN_PID" 2>/dev/null || true
  [ "${KEEP_RUNTIME:-0}" = 1 ] || { pkill -f "$IB/program/versions" 2>/dev/null; pkill -f "$IB/program-after/versions" 2>/dev/null; } || true
}
trap cleanup EXIT
for i in $(seq 20); do curl -s -m2 "http://127.0.0.1:$PORT/system_stats" >/dev/null && break; sleep 1; done
( while :; do echo "$(date -u +%FT%TZ) $(cut -d' ' -f1-3 /proc/loadavg)" >> "$EVIDENCE_DIR/load-samples.txt"; sleep 30; done ) &
SAMPLER=$!
for arm in before after; do   # start both Runtimes (separate door ports), tolerate the first-call restart failure
  ( arm_env $arm; for i in 1 2 3 4; do "$PROGRAM/run-astrid" projects list --json >/dev/null 2>&1 && break; sleep 4; done )
done
cp "$IB/standin/media.png" "$EVIDENCE_DIR/media.png"

if [ "$MODE" = prepare ]; then
  echo "validation (UNTIMED):"
  "$IB/program-after/run-astrid" generate image --help | grep -q -- '--timings' && echo "  candidate 'generate image --help' lists --timings: yes" || { echo "  candidate lacks --timings" >&2; exit 1; }
  "$IB/program/run-astrid" generate image --help | grep -q -- '--timings' && echo "  before arm lists --timings: yes (unexpected)" || echo "  before arm lists --timings: no (expected)"
  for arm in before after; do
    ( arm_env $arm; X=""; [ $arm = after ] && X="--timings"; P=prep-$arm-$STAMP
      "$PROGRAM/run-astrid" projects create $P --name $P --select --json >/dev/null
      "$PROGRAM/run-astrid" generate image "a red square" --mode t2i --placement "http://127.0.0.1:$PORT" --project $P --no-wait --json $X > "$EVIDENCE_DIR/prep-$arm.json"
      python3 -c "import json;d=json.load(open('$EVIDENCE_DIR/prep-$arm.json'));assert d['ok'] and d['kernel_task_id'];print('  $arm untimed generate: ok, task', d['kernel_task_id'][:8], 'timings' if d.get('timings') else 'no timings')" )
  done
  echo "prepare OK. Timed run: $0 --run"; exit 0
fi

export IB EVIDENCE_DIR COMFY_URL="http://127.0.0.1:$PORT" MEDIA_PNG="$EVIDENCE_DIR/media.png"
export ARMS_JSON=$(python3 - <<PY
import json
IB="$IB"
print(json.dumps({"before": {"launcher": f"{IB}/program/run-astrid", "home": f"{IB}/home", "tmp": f"{IB}/scratch/tmp"},
                  "after": {"launcher": f"{IB}/program-after/run-astrid", "home": f"{IB}/home-after", "tmp": f"{IB}/scratch/tmp-after", "generate_extra": ["--timings"]}}))
PY
)
python3 "$IB/ab_run.py"
