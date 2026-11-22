#!/usr/bin/env bash
set -u

# Run the unchanged US-2 full latency integration gate in an isolated process
# environment. This harness is evidence tooling; it does not change the repo.

ROOT=/root/codex/plan-81
TASK="$ROOT/run/worktrees/us-2"
TASK_BASE="$ROOT/run/worktrees/us-2-post69.env"
EVIDENCE="$ROOT/run/us2-normalized"
PY="$TASK_BASE/venv/bin/python"

usage() {
  echo "usage: $0 TRIAL_BASENAME [CANONICAL_STAGE] [generate|timelines]" >&2
  echo "examples: $0 baseline-1" >&2
  echo "          $0 runtime-health-delay 'Runtime GET /v1/capabilities' generate" >&2
}

if [[ $# -lt 1 || $# -gt 3 ]]; then usage; exit 64; fi
TRIAL_NAME=$1
STAGE=${2-}
FAMILY=${3-generate}
if [[ ! "$TRIAL_NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$ ]]; then
  echo "trial basename must be a safe filename component" >&2; exit 64
fi
if [[ "$FAMILY" != generate && "$FAMILY" != timelines ]]; then
  echo "target CLI family must be generate or timelines" >&2; exit 64
fi
if [[ -n "$STAGE" && "$FAMILY" == generate && "$STAGE" != "Runtime acquisition lock" && "$STAGE" != "workflow build" && "$STAGE" != "Runtime GET /v1/capabilities" && "$STAGE" != "Runtime GET /v1/objects/{digest}" ]]; then
  echo "unsupported canonical stage for generate" >&2; exit 64
fi
if [[ -n "$STAGE" && "$FAMILY" == timelines && "$STAGE" != "Runtime acquisition lock" && "$STAGE" != "Runtime GET /v1/capabilities" && "$STAGE" != "Runtime GET /v1/objects/{digest}" ]]; then
  echo "unsupported canonical stage for timelines" >&2; exit 64
fi
if [[ ! -x "$PY" ]]; then echo "expected isolated Python executable missing: $PY" >&2; exit 66; fi

TRIAL="$EVIDENCE/$TRIAL_NAME"
if ! mkdir -m 700 "$TRIAL" 2>/dev/null; then
  echo "trial already exists (refusing to overwrite evidence): $TRIAL" >&2; exit 73
fi
mkdir -m 700 "$TRIAL/home" "$TRIAL/hook"
LOG="$TRIAL/pytest.log"
META="$TRIAL/metadata.json"
ROWS="$TRIAL/cli-samples.jsonl"
EVENTS="$TRIAL/delay-events.jsonl"
BASE="$TRIAL/basetemp"
PLUGIN="$EVIDENCE/evidence_plugin.py"
HOOK="$EVIDENCE/delay_hook.py"

export ROOT TASK TASK_BASE TRIAL META ROWS EVENTS BASE PLUGIN HOOK STAGE FAMILY

if [[ -n "$STAGE" ]]; then
  cp "$HOOK" "$TRIAL/hook/sitecustomize.py"
  PYTHONPATH_PREFIX="$TRIAL/hook:$EVIDENCE"
else
  PYTHONPATH_PREFIX="$EVIDENCE"
fi

# Record only repository identities and boolean dirty state. Never record env
# variables, credential files, process arguments, or test payloads.
"$PY" - <<'PY'
import datetime, json, os, pathlib, subprocess

def git_record(path):
    p = pathlib.Path(path)
    if not p.exists():
        return {"path": str(p), "present": False}
    def git(*args):
        return subprocess.check_output(["git", "-C", str(p), *args], text=True, stderr=subprocess.DEVNULL).strip()
    try:
        head = git("rev-parse", "HEAD")
        tree = git("write-tree")
        dirty = bool(git("status", "--porcelain", "--untracked-files=normal"))
        return {"path": str(p), "present": True, "head": head, "tree": tree, "dirty": dirty}
    except Exception as exc:
        return {"path": str(p), "present": True, "error_class": type(exc).__name__}

def loadavg():
    try:
        return [float(x) for x in pathlib.Path("/proc/loadavg").read_text().split()[:3]]
    except Exception:
        return None

data = {
    "trial": os.environ["TRIAL"],
    "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "start_load_1_5_15": loadavg(),
    "stage": os.environ["STAGE"] or None,
    "family": os.environ["FAMILY"],
    "repositories": {
        "source": git_record(os.environ["TASK"]),
        "runtime": git_record(os.path.join(os.environ["TASK_BASE"], "runtime")),
        "lifecycle": git_record(os.path.join(os.environ["TASK_BASE"], "lifecycle")),
        "vibecomfy": git_record(os.path.join(os.environ["TASK_BASE"], "vibecomfy")),
    },
}
pathlib.Path(os.environ["META"]).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

export US2_EVIDENCE_ROWS="$ROWS"
export US2_EVIDENCE_EVENTS="$EVENTS"
export US2_EVIDENCE_STAGE="$STAGE"
export US2_EVIDENCE_FAMILY="$FAMILY"

cd "$TASK"
env -i \
  HOME="$TRIAL/home" XDG_CONFIG_HOME="$TRIAL/home/.config" XDG_CACHE_HOME="$TRIAL/home/.cache" \
  LANG=C.UTF-8 PATH="$TASK_BASE/venv/bin:/usr/local/bin:/usr/bin:/bin" \
  ASTRID_RUNTIME_CHECKOUT="$TASK_BASE/runtime" \
  ASTRID_TEST_LIFECYCLE_CHECKOUT="$TASK_BASE/lifecycle" \
  ASTRID_VIBECOMFY_CHECKOUT="$TASK_BASE/vibecomfy" \
  PYTHONPATH="$TASK:$TASK_BASE/runtime:$PYTHONPATH_PREFIX:$TASK_BASE/vibecomfy:$TASK_BASE/lifecycle" \
  PYTHONUNBUFFERED=1 \
  US2_EVIDENCE_ROWS="$ROWS" US2_EVIDENCE_EVENTS="$EVENTS" \
  US2_EVIDENCE_STAGE="$STAGE" US2_EVIDENCE_FAMILY="$FAMILY" \
  "$PY" -m pytest -p evidence_plugin -s -q -m integration \
  tests/integrations/test_command_latency_budget.py::test_command_latency_budget \
  --basetemp="$BASE" >"$LOG" 2>&1
TEST_EXIT=$?

# Cleanup check is read-only: report processes that mention this unique trial
# or basetemp path. Never kill a process not owned by the test cleanup itself.
US2_TEST_EXIT="$TEST_EXIT" "$PY" - <<'PY'
import datetime, json, os, pathlib
import subprocess

trial = os.environ["TRIAL"]
root = pathlib.Path(os.environ["ROOT"])
task_base = pathlib.Path(os.environ["TASK_BASE"])
needles = (trial.encode(), (trial + "/basetemp").encode())
left = []
for entry in pathlib.Path("/proc").iterdir():
    if not entry.name.isdigit() or int(entry.name) == os.getpid():
        continue
    try:
        raw = (entry / "cmdline").read_bytes()
    except (OSError, PermissionError):
        continue
    if any(n in raw for n in needles):
        argv0 = raw.split(b"\0", 1)[0].decode("utf-8", "replace")
        left.append({"pid": int(entry.name), "argv0_basename": pathlib.Path(argv0).name})

path = pathlib.Path(os.environ["META"])
data = json.loads(path.read_text(encoding="utf-8"))
try:
    data["end_load_1_5_15"] = [float(x) for x in pathlib.Path("/proc/loadavg").read_text().split()[:3]]
except Exception:
    data["end_load_1_5_15"] = None
data["ended_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
data["pytest_exit"] = int(os.environ["US2_TEST_EXIT"])
data["cleanup_processes_for_trial"] = left
data["cleanup_process_check_clear"] = not left
def git_record(path):
    path = pathlib.Path(path)
    if not path.exists():
        return {"path": str(path), "present": False}
    def git(*args):
        return subprocess.check_output(["git", "-C", str(path), *args], text=True, stderr=subprocess.DEVNULL).strip()
    try:
        return {"path": str(path), "present": True, "head": git("rev-parse", "HEAD"),
                "tree": git("write-tree"), "dirty": bool(git("status", "--porcelain", "--untracked-files=normal"))}
    except Exception as exc:
        return {"path": str(path), "present": True, "error_class": type(exc).__name__}

data["ending_repositories"] = {
    "source": git_record(root / "run/worktrees/us-2"),
    "runtime": git_record(task_base / "runtime"),
    "lifecycle": git_record(task_base / "lifecycle"),
    "vibecomfy": git_record(task_base / "vibecomfy"),
}
data["repository_identity_unchanged"] = data["ending_repositories"] == data["repositories"]
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

echo "US-2 trial: $TRIAL"
echo "pytest exit: $TEST_EXIT"
echo "log: $LOG"
echo "CLI timing rows: $ROWS"
echo "delay events: $EVENTS"
echo "metadata: $META"
exit "$TEST_EXIT"
