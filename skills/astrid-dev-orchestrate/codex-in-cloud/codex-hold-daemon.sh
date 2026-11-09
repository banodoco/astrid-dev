#!/usr/bin/env bash
# Restart-proof keep-alive for Codex runs in a Claude Code cloud session.
# A SessionStart hook launches it, detached, every time the session starts or resumes,
# including after a container restart:
#   setsid nohup <dir>/codex-hold-daemon.sh >/dev/null 2>&1 </dev/null &
# It never exits on its own. Every HOLD_TICK seconds (default 30) it reads one run folder per line from
# $CODEX_RUNS (default ~/codex/runs.txt) and restarts a run's runner if the run is
# unfinished (status running or waiting) and its runner process is gone. It allows at most
# 3 restarts per run per daemon life. A flock makes a second copy exit at once.
# It wakes nobody: scheduled check-ins (send_later) remain the wake-up path, and codex-hold.sh
# remains the in-turn waiter that exits on mailbox messages.
HERE=$(cd "$(dirname "$0")" && pwd)
RUNS=${CODEX_RUNS:-$HOME/codex/runs.txt}
LOCK=${CODEX_DAEMON_LOCK:-/tmp/codex-hold-daemon.lock}
exec 9>"$LOCK"
flock -n 9 || exit 0
echo $$ > "$LOCK.pid"
declare -A restarts
while :; do
  while IFS= read -r RUN; do
    [ -n "$RUN" ] && [ -d "$RUN" ] || continue
    s=$(cat "$RUN/status" 2>/dev/null)
    pid=$(cat "$RUN/runner.pid" 2>/dev/null)
    if { [ "$s" = running ] || [ "$s" = waiting ]; } && [ -f "$RUN/runner.args" ] \
       && { [ -z "$pid" ] || ! kill -0 "$pid" 2>/dev/null; }; then
      restarts[$RUN]=$(( ${restarts[$RUN]:-0} + 1 ))
      if [ "${restarts[$RUN]}" -gt 3 ]; then
        [ "${restarts[$RUN]}" -eq 4 ] && echo "$(date -u +%FT%TZ) daemon: runner keeps dying; giving up on this run until the next session start" >> "$RUN/hold.log"
        continue
      fi
      echo "$(date -u +%FT%TZ) daemon: runner ${pid:-?} gone; restarting (${restarts[$RUN]}/3)" >> "$RUN/hold.log"
      # runner.args and runner.env hold %q-quoted values that the runner wrote itself.
      ( eval "export $(cat "$RUN/runner.env" 2>/dev/null)"; eval "set -- $(cat "$RUN/runner.args")"
        setsid nohup "$HERE/codex-runner.sh" "$@" > /dev/null 2>&1 < /dev/null & )
      sleep 5
    fi
  done < <(cat "$RUNS" 2>/dev/null)
  sleep "${HOLD_TICK:-30}"
done
