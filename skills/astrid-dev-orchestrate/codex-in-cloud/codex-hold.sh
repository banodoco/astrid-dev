#!/usr/bin/env bash
# Keep-alive and restarter for Codex runs in a Claude Code cloud session. It replaces codex-watch.sh.
# Run with the Bash tool's run_in_background (timeout 7200000), and re-arm it at EVERY check-in:
#   codex-hold.sh <run-dir> [<run-dir> ...]
# It keeps the session busy for up to ~55 minutes (HOLD_SECONDS), and every 30 s, for each run, it:
#   - restarts the runner if its process is gone while the run is unfinished (a container worker
#     restart kills every process, the runner included); the runner resumes the same Codex session;
#   - exits to wake the orchestrator when Codex writes to to-orchestrator.md, or when a run reaches
#     done, blocked, gave-up or waiting.
# A worker restart kills this script too. Only the server-side scheduled check-in survives a
# restart, so that check-in must start this script again.
HERE=$(cd "$(dirname "$0")" && pwd)
end=$(( $(date +%s) + ${HOLD_SECONDS:-3300} ))
declare -A seen restarts
for RUN in "$@"; do seen[$RUN]=$(wc -c < "$RUN/to-orchestrator.md" 2>/dev/null || echo 0); done
while [ "$(date +%s)" -lt "$end" ]; do
  for RUN in "$@"; do
    s=$(cat "$RUN/status" 2>/dev/null)
    case "$s" in
      done|blocked|gave-up|waiting)
        echo "RUN $RUN STATUS=$s"; tail -n 40 "$RUN/result.md" 2>/dev/null; exit 0 ;;
    esac
    now=$(wc -c < "$RUN/to-orchestrator.md" 2>/dev/null || echo 0)
    if [ "$now" -gt "${seen[$RUN]}" ]; then
      echo "MESSAGE FROM CODEX ($RUN):"; tail -c +$(( ${seen[$RUN]} + 1 )) "$RUN/to-orchestrator.md"; echo "STATUS=$s"; exit 0
    fi
    pid=$(cat "$RUN/runner.pid" 2>/dev/null)
    if [ "$s" = running ] && [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null && [ -f "$RUN/runner.args" ]; then
      restarts[$RUN]=$(( ${restarts[$RUN]:-0} + 1 ))
      if [ "${restarts[$RUN]}" -gt 3 ]; then echo "RESTART FAILED ($RUN): runner keeps dying; see codex.log"; exit 4; fi
      echo "$(date -u +%FT%TZ) runner $pid gone; restarting (${restarts[$RUN]}/3)" | tee -a "$RUN/hold.log"
      # runner.args and runner.env hold %q-quoted values that the runner wrote itself.
      ( eval "export $(cat "$RUN/runner.env" 2>/dev/null)"; eval "set -- $(cat "$RUN/runner.args")"
        setsid nohup "$HERE/codex-runner.sh" "$@" > /dev/null 2>&1 < /dev/null & )
      sleep 5
    fi
  done
  sleep ${HOLD_TICK:-30}
done
echo "STILL RUNNING (re-arm codex-hold.sh)"
