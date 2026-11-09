#!/usr/bin/env bash
# Run with Bash run_in_background (timeout 7200000). Exits (and so wakes the
# orchestrator) when the run finishes, the heartbeat goes stale for 5 min, or
# after ~110 min so the next check-in re-arms it.
# Usage: codex-watch.sh <run-dir>
RUN=$1; end=$(( $(date +%s) + 6600 )); seen=$(wc -c < "$RUN/to-orchestrator.md" 2>/dev/null || echo 0)
while [ "$(date +%s)" -lt "$end" ]; do
  s=$(cat "$RUN/status" 2>/dev/null)
  [ "$s" != running ] && { echo "STATUS=$s"; tail -n 5 "$RUN/money.log"; tail -n 40 "$RUN/result.md" 2>/dev/null; exit 0; }
  now=$(wc -c < "$RUN/to-orchestrator.md" 2>/dev/null || echo 0)
  [ "$now" -gt "$seen" ] && { echo "MESSAGE FROM CODEX:"; tail -c +$((seen+1)) "$RUN/to-orchestrator.md"; echo "STATUS=$s"; exit 0; }
  hb=$(date -d "$(cat "$RUN/heartbeat" 2>/dev/null)" +%s 2>/dev/null || echo 0)
  [ $(( $(date +%s) - hb )) -gt 300 ] && { echo "STALE heartbeat"; exit 3; }
  sleep 30
done
echo "STILL RUNNING (re-arm)"; tail -n 3 "$RUN/money.log"
