#!/usr/bin/env bash
# Installed-Astrid baseline: install the PUBLISHED Astrid into an isolated home (if absent), start a
# stand-in ComfyUI, run the owner's us0-published.py against it, tear down, print the summary.
#   ./run-installed-baseline.sh [--timings]
# Env: ASTRID_INSTALL_MANIFEST (path or URL; default is the published manifest),
#      EVIDENCE_DIR (default evidence/run-<UTC stamp>), LOAD_MAX, LOAD_WAIT_SECONDS.
set -euo pipefail
IB=/root/codex/installed-baseline
export HOME=$IB/home XDG_DATA_HOME=$IB/home/.local/share XDG_STATE_HOME=$IB/home/.local/state \
       XDG_CONFIG_HOME=$IB/home/.config XDG_CACHE_HOME=$IB/home/.cache TMPDIR=$IB/scratch/tmp
mkdir -p "$TMPDIR" "$XDG_DATA_HOME" "$XDG_STATE_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
PROGRAM=$IB/program DATA=$IB/data
STAMP=$(date -u +%Y%m%d-%H%M%S)
EVIDENCE_DIR=${EVIDENCE_DIR:-$IB/evidence/run-$STAMP}
WANT_TIMINGS=0; [ "${1:-}" = "--timings" ] && WANT_TIMINGS=1
GEN_EXTRA="--mode t2i"
mkdir -p "$EVIDENCE_DIR"

# 1. install (idempotent): skip if the installed launcher already answers --version.
LAUNCHER=$PROGRAM/run-astrid
if ! "$LAUNCHER" --version >/dev/null 2>&1; then
  MANIFEST=${ASTRID_INSTALL_MANIFEST:-}
  if [ -z "$MANIFEST" ]; then
    curl -fsS -o "$EVIDENCE_DIR/install-manifest.json" https://astrid.haus/install-manifest.json
    MANIFEST=$EVIDENCE_DIR/install-manifest.json
  fi
  case "$MANIFEST" in http*) curl -fsS -o "$EVIDENCE_DIR/install-manifest.json" "$MANIFEST"; MANIFEST=$EVIDENCE_DIR/install-manifest.json;; esac
  curl -fsS -o "$EVIDENCE_DIR/install.sh" https://astrid.haus/install
  sh "$EVIDENCE_DIR/install.sh" --manifest "$MANIFEST" --root "$PROGRAM" --data-root "$DATA" \
     --yes --autostart off --command on --skills off --skill-copies off </dev/null \
     || { echo "INSTALL FAILED; see $XDG_STATE_HOME/astrid-runtime/logs/install.log" >&2; exit 1; }
fi
sha256sum "$EVIDENCE_DIR"/install.sh "$EVIDENCE_DIR"/install-manifest.json 2>/dev/null > "$EVIDENCE_DIR/hashes.txt" || true
"$LAUNCHER" --version > "$EVIDENCE_DIR/astrid-version.txt" 2>&1 || true

# supported-flag check: only add --timings to generate if the installed build lists it.
if [ "$WANT_TIMINGS" = 1 ]; then
  if "$LAUNCHER" generate image --help 2>&1 | grep -q -- '--timings'; then GEN_EXTRA="--mode t2i --timings"
  else echo "NOTE: this build's 'generate image' has no --timings; running the normal batch only." | tee "$EVIDENCE_DIR/timings-unsupported.txt"; fi
fi
"$LAUNCHER" generate image --help > "$EVIDENCE_DIR/generate-image-help.txt" 2>&1 || true

# 2. stand-in ComfyUI: run with the installed venv python (imports installed astrid + vibecomfy).
PY=$(echo "$PROGRAM"/versions/*/py/bin/python | cut -d' ' -f1)
PORT=${STANDIN_PORT:-18188}
"$PY" -I "$IB/standin/standin_comfy.py" --port $PORT >"$EVIDENCE_DIR/standin.log" 2>&1 &
STANDIN_PID=$!
SAMPLER=
cleanup() {
  [ -n "$SAMPLER" ] && kill $SAMPLER 2>/dev/null || true
  kill $STANDIN_PID 2>/dev/null || true
  # Tear down the Runtime/pack host this install started (only processes whose command line is under our program dir).
  [ "${KEEP_RUNTIME:-0}" = 1 ] || pkill -f "$PROGRAM/versions" 2>/dev/null || true
}
trap cleanup EXIT
for i in $(seq 20); do curl -s -m2 http://127.0.0.1:$PORT/system_stats >/dev/null && break; sleep 1; done
( while :; do echo "$(date -u +%FT%TZ) $(cut -d' ' -f1-3 /proc/loadavg)" >> "$EVIDENCE_DIR/load-samples.txt"; sleep 30; done ) &
SAMPLER=$!

# 3. measure: every astrid call goes through the gating wrapper; its jsonl is the authoritative timing.
cp "$IB/standin/media.png" "$EVIDENCE_DIR/media.png"
export REAL_ASTRID=$LAUNCHER TIMING_LOG=$EVIDENCE_DIR/timing.jsonl
export ASTRID_CMD=$IB/timed-astrid.py COMFY_URL=http://127.0.0.1:$PORT MEDIA_PNG=$EVIDENCE_DIR/media.png
export EVIDENCE_DIR GEN_EXTRA
# warm the Runtime once so the first timed command is not a cold start (not counted)
# (after a teardown the first launcher call restarts the Runtime and may fail once; retry up to 4 times.)
for i in 1 2 3 4; do "$LAUNCHER" projects list --json >/dev/null 2>&1 && break; sleep 3; done
python3 "$IB/us0-published.py"
# supplementary floor: interpreter+import cost of a fresh launcher process, and a read-only call.
for i in 1 2 3 4 5; do "$IB/timed-astrid.py" --version >/dev/null; done
for i in 1 2 3; do "$IB/timed-astrid.py" generate defaults --json >/dev/null; done
python3 "$IB/summarize_timings.py" "$EVIDENCE_DIR"
echo "authoritative timings (wait excluded): $EVIDENCE_DIR/timing-summary.json"
