#!/usr/bin/env bash
# Installed-Astrid A/B/C run: three isolated installs, one shared stand-in ComfyUI, arms alternated per round, load-gated.
#   before = published Release 14 tuple (omp from npm)
#   after  = final local candidate: Agent 705298cd (scratch repo), Runtime 72b129e5, VibeComfy 950023c8
#   vc48   = final comparison candidate: Agent b5c30e61, Runtime 72b129e5, VibeComfy 48b5fa9e
#   ./run-ab-installed.sh            prepare + validate only (install if absent, versions, --timings check, one UNTIMED command per arm)
#   ./run-ab-installed.sh --run      prepare, then the gated timed run (fails, does not run ungated, if load < 1.0 is not reached in 10 min)
# Env: BEFORE_MANIFEST, CANDIDATE_MANIFEST, VC48_MANIFEST (defaults: manifest-omp-npm.json, manifest-candidate.json, manifest-candidate-vc48.json),
#      ARMS (default "before after vc48"; "before after" gives the two-arm run), EVIDENCE_DIR, LOAD_MAX (1.0), LOAD_WAIT_SECONDS (600),
#      SAMPLES (5), STANDIN_PORT (18188), KEEP_RUNTIME=1, IB (live install root; default /root/codex/installed-baseline).
# Setting, every time: installed builds, CPU container, stand-in ComfyUI; not covered: a real ComfyUI's node-info answer, GPU work.
# Only candidate arms (after, vc48) run `generate` with --timings; the before build cannot. This difference affects comparisons.
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ASTRID_AB_ATTEST=${ASTRID_AB_ATTEST-on}
case "$ASTRID_AB_ATTEST" in on|off) ;; *) echo "FAIL: ASTRID_AB_ATTEST must be on or off" >&2; exit 1;; esac
export ASTRID_AB_ATTEST
if [ "$ASTRID_AB_ATTEST" = on ]; then
  : "${ASTRID_RUNTIME_SOURCE_REPO:?set ASTRID_RUNTIME_SOURCE_REPO to a local Runtime Git repository containing each manifest commit}"
  git -C "$ASTRID_RUNTIME_SOURCE_REPO" rev-parse --git-dir >/dev/null || { echo "FAIL: ASTRID_RUNTIME_SOURCE_REPO is not a Git repository" >&2; exit 1; }
fi
source "$SCRIPT_DIR/runtime-readiness.sh"
IB=${IB:-/root/codex/installed-baseline}
case "$IB" in /*) ;; *) echo "IB must be an absolute path" >&2; exit 1;; esac
MODE=prepare; [ "${1:-}" = "--run" ] && MODE=run
STAMP=$(date -u +%Y%m%d-%H%M%S)
EVIDENCE_DIR=${EVIDENCE_DIR:-$IB/evidence/ab-$MODE-$STAMP}
mkdir -p "$(dirname -- "$EVIDENCE_DIR")"
mkdir -- "$EVIDENCE_DIR" || { echo "FAIL: evidence directory must be fresh: $EVIDENCE_DIR" >&2; exit 1; }
exec > >(tee "$EVIDENCE_DIR/console.log") 2>&1
ARMS=${ARMS:-"before after vc48"}
PORT=${STANDIN_PORT:-18188}
echo "SETTING: installed builds, CPU container, stand-in ComfyUI; not covered: a real ComfyUI's node-info answer, GPU work."

arm_manifest() { case "$1" in before) echo "${BEFORE_MANIFEST:-$SCRIPT_DIR/manifest-omp-npm.json}";; after) echo "${CANDIDATE_MANIFEST:-$SCRIPT_DIR/manifest-candidate.json}";; vc48) echo "${VC48_MANIFEST:-$SCRIPT_DIR/manifest-candidate-vc48.json}";; esac; }
arm_env() {  # sets HOME/XDG/TMPDIR/PROGRAM/DATA and the Runtime door port for one arm
  case "$1" in
    before) SUF=""; DOOR=17340;; after) SUF="-after"; DOOR=17341;; vc48) SUF="-vc48"; DOOR=17342;;
  esac
  H=$IB/home$SUF; PROGRAM=$IB/program$SUF; DATA=$IB/data$SUF; TMPD=$IB/scratch/tmp$SUF
  [ "$1" = before ] && TMPD=$IB/scratch/tmp
  mkdir -p "$H/.local/share" "$H/.local/state" "$H/.config" "$H/.cache" "$TMPD" || return 1
  export HOME=$H XDG_DATA_HOME=$H/.local/share XDG_STATE_HOME=$H/.local/state XDG_CONFIG_HOME=$H/.config XDG_CACHE_HOME=$H/.cache TMPDIR=$TMPD
  unset ASTRID_RUNTIME_LAUNCHER ASTRID_RUNTIME_ENDPOINT ASTRID_RUNTIME_CREDENTIAL ASTRID_RUNTIME_DATA_ROOT ASTRID_PREPARED_CONNECTION ASTRID_TIMELINE_EVAL_ENDPOINT ASTRID_TIMELINE_EVAL_CREDENTIAL ASTRID_TIMELINE_EVAL_REALM_ID ASTRID_TIMELINE_EVAL_ACTOR_ID
  export ASTRID_RUNTIME_DOOR_PORT=$DOOR
}
curl -fsS -o "$EVIDENCE_DIR/install.sh" https://astrid.haus/install
for arm in $ARMS; do
  ( M=$(arm_manifest "$arm") || exit 1
    cp "$M" "$EVIDENCE_DIR/manifest-$arm.json" || exit 1
    arm_env "$arm" || exit 1
    if ! "$PROGRAM/run-astrid" --version >/dev/null 2>&1; then
      echo "installing $arm arm ($(basename "$M"))"
      sh "$EVIDENCE_DIR/install.sh" --manifest "$M" --root "$PROGRAM" --data-root "$DATA" --yes --autostart off --command on --skills off --skill-copies off </dev/null \
        > "$EVIDENCE_DIR/install-$arm.out" 2>&1 || { echo "INSTALL FAILED ($arm): see $EVIDENCE_DIR/install-$arm.out" >&2; exit 1; }
    fi
    SELECTED=$(python3 "$SCRIPT_DIR/runtime_attestation.py" --selected "$PROGRAM/current") || exit 1
    cp "$SELECTED/manifest.json" "$EVIDENCE_DIR/installed-manifest-$arm.json" || exit 1
    python3 - "$M" "$EVIDENCE_DIR/installed-manifest-$arm.json" $arm <<'PY'   # the installed tuple must equal the requested pins
import json, sys
want, got = (json.load(open(p)) for p in sys.argv[1:3])
for k in ("agent", "runtime", "vibecomfy", "lifecycle"):
    if want[k]["sha"] != got[k]["sha"]: sys.exit(f"{sys.argv[3]} arm: installed {k} {got[k]['sha'][:8]} != requested {want[k]['sha'][:8]}; remove that arm's program/data/home and re-run")
PY
    [ $? -eq 0 ] || exit 1
    "$PROGRAM/run-astrid" --version > "$EVIDENCE_DIR/astrid-version-$arm.txt" 2>&1 || exit 1
    if [ "$ASTRID_AB_ATTEST" = on ]; then
      python3 "$SCRIPT_DIR/runtime_attestation.py" --source "$PROGRAM/current" "$EVIDENCE_DIR/manifest-$arm.json" || exit 1
    fi
  ) || exit 1
done
( cd "$EVIDENCE_DIR"; sha256sum install.sh manifest-*.json installed-manifest-*.json > hashes.txt )
python3 - "$EVIDENCE_DIR" $ARMS <<'PY'
import json, sys
d = sys.argv[1]
for arm in sys.argv[2:]:
    m = json.load(open(f"{d}/installed-manifest-{arm}.json"))
    print(f"  {arm}: agent {m['agent']['sha'][:8]} runtime {m['runtime']['sha'][:8]} vibecomfy {m['vibecomfy']['sha'][:8]} lifecycle {m['lifecycle']['sha'][:8]} omp {m['tools']['omp']['source']}")
PY

# Capture this invocation before launching children; PID alone can be reused.
SCRIPT_START=$(python3 "$SCRIPT_DIR/process_ownership.py" capture "$$")
export ASTRID_ATTEST_START_TICKS=$SCRIPT_START PYTHONDONTWRITEBYTECODE=1
STANDIN_PID=; STANDIN_START=; SAMPLER=; SAMPLER_START=
cleanup() {
  if [ -n "$SAMPLER_START" ]; then python3 "$SCRIPT_DIR/process_ownership.py" signal "$SAMPLER" "$SAMPLER_START" || echo "Cleanup: sampler already exited or could not be safely signaled." >&2; fi
  if [ -n "$STANDIN_START" ]; then python3 "$SCRIPT_DIR/process_ownership.py" signal "$STANDIN_PID" "$STANDIN_START" || echo "Cleanup: stand-in already exited or could not be safely signaled." >&2; fi
  if [ "${KEEP_RUNTIME:-0}" != 1 ]; then
    python3 "$SCRIPT_DIR/process_ownership.py" descendants "$$" "$SCRIPT_START" "$IB/program/versions" "$IB/program-after/versions" "$IB/program-vc48/versions" || echo "Cleanup: descendant scan failed." >&2
    echo "Cleanup: detached or reparented Runtime processes cannot be attributed safely and may still be running." >&2
  fi
}
trap cleanup EXIT
BPY="$(python3 "$SCRIPT_DIR/runtime_attestation.py" --selected "$IB/program/current")/py/bin/python"   # stand-in runs on the before arm's venv (validated to serve every arm)
"$BPY" -I "$SCRIPT_DIR/standin/standin_comfy.py" --port "$PORT" >"$EVIDENCE_DIR/standin.log" 2>&1 &
STANDIN_PID=$!
STANDIN_START=$(python3 "$SCRIPT_DIR/process_ownership.py" capture "$STANDIN_PID" "$$" "$SCRIPT_START") || { echo "FAIL: cannot establish stand-in identity" >&2; exit 1; }
# The stand-in logs only after it has bound the port. A successful HTTP response
# alone could come from an unrelated listener when our child failed to bind.
standin_ready=0
for i in $(seq 20); do
  if ! kill -0 "$STANDIN_PID" 2>/dev/null; then break; fi
  if grep -Fq "stand-in ComfyUI on 127.0.0.1:$PORT " "$EVIDENCE_DIR/standin.log" &&
     curl -fsS -m2 "http://127.0.0.1:$PORT/system_stats" >/dev/null &&
     kill -0 "$STANDIN_PID" 2>/dev/null; then
    standin_ready=1; break
  fi
  sleep 1
done
if [ "$standin_ready" != 1 ]; then
  echo "FAIL: stand-in did not become ready; see $EVIDENCE_DIR/standin.log" >&2
  exit 1
fi
python3 "$SCRIPT_DIR/load_sampler.py" "$EVIDENCE_DIR/load-samples.txt" &
SAMPLER=$!
SAMPLER_START=$(python3 "$SCRIPT_DIR/process_ownership.py" capture "$SAMPLER" "$$" "$SCRIPT_START") || { echo "FAIL: cannot establish sampler identity" >&2; exit 1; }
for arm in $ARMS; do   # start every Runtime (separate door ports); the first call after a teardown may fail once
  ( arm_env "$arm" && runtime_ready "$PROGRAM/run-astrid" "$arm" "$EVIDENCE_DIR/runtime-ready-$arm.log" ) || exit 1
done
if [ "$ASTRID_AB_ATTEST" = on ]; then
  for arm in $ARMS; do
    ( arm_env "$arm" && python3 "$SCRIPT_DIR/runtime_attestation.py" "$DOOR" "$PROGRAM/current" "$EVIDENCE_DIR/manifest-$arm.json" "$EVIDENCE_DIR/runtime-listener-$arm.json" ) || exit 1
  done
fi
cp "$SCRIPT_DIR/standin/media.png" "$EVIDENCE_DIR/media.png"

if [ "$MODE" = prepare ]; then
  echo "validation (UNTIMED):"
  for arm in $ARMS; do
    ( arm_env $arm; X=""
      if "$PROGRAM/run-astrid" generate image --help | grep -q -- '--timings'; then X="--timings"; echo "  $arm: generate image lists --timings: yes"; else echo "  $arm: generate image lists --timings: no"; fi
      P=prep-$arm-$STAMP
      attest_prepare() { if [ "$ASTRID_AB_ATTEST" = on ]; then python3 "$SCRIPT_DIR/runtime_attestation.py" "$DOOR" "$PROGRAM/current" "$EVIDENCE_DIR/manifest-$arm.json" "$EVIDENCE_DIR/prepare-$arm-$1.json"; fi; }
      attest_prepare projects-before || exit 1
      "$PROGRAM/run-astrid" projects create "$P" --name "$P" --select --json >/dev/null || exit 1
      attest_prepare projects-after || exit 1
      if [ "$ASTRID_AB_ATTEST" = on ]; then cmp -s "$EVIDENCE_DIR/prepare-$arm-projects-before.json" "$EVIDENCE_DIR/prepare-$arm-projects-after.json" || exit 1; fi
      attest_prepare generate-before || exit 1
      "$PROGRAM/run-astrid" generate image "a red square" --mode t2i --placement "http://127.0.0.1:$PORT" --project $P --no-wait --json $X > "$EVIDENCE_DIR/prep-$arm.json" 2>/dev/null || exit 1
      attest_prepare generate-after || exit 1
      if [ "$ASTRID_AB_ATTEST" = on ]; then cmp -s "$EVIDENCE_DIR/prepare-$arm-generate-before.json" "$EVIDENCE_DIR/prepare-$arm-generate-after.json" || exit 1; fi
      python3 - "$EVIDENCE_DIR/prep-$arm.json" "$arm" <<'PY'
import json, sys
with open(sys.argv[1]) as f: d = json.load(f)
assert d["ok"] and d["kernel_task_id"]
print(" ", sys.argv[2], "untimed generate: ok, task", d["kernel_task_id"][:8], "with stage table" if d.get("timings") else "no stage table")
PY
    ) || exit 1
  done
  echo "prepare OK. Timed run: $0 --run"; exit 0
fi

export IB EVIDENCE_DIR COMFY_URL="http://127.0.0.1:$PORT" MEDIA_PNG="$EVIDENCE_DIR/media.png"
export ARMS_JSON=$(ARMS="$ARMS" python3 - <<'PY'
import json, os
IB = os.environ["IB"]
suf = {"before": "", "after": "-after", "vc48": "-vc48"}
ports = {"before": 17340, "after": 17341, "vc48": 17342}
out = {}
for a in os.environ["ARMS"].split():
    s = suf[a]
    out[a] = {"launcher": f"{IB}/program{s}/run-astrid", "home": f"{IB}/home{s}",
              "tmp": f"{IB}/scratch/tmp{s}" if a != "before" else f"{IB}/scratch/tmp", "door_port": ports[a],
              "current": f"{IB}/program{s}/current", "manifest": f"{os.environ['EVIDENCE_DIR']}/manifest-{a}.json"}
    if a != "before": out[a]["generate_extra"] = ["--timings"]   # candidate builds only; the published build cannot
print(json.dumps(out))
PY
)
python3 "$SCRIPT_DIR/ab_run.py"
