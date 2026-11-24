#!/bin/bash
S=~; R=~/astrid-release/release-14-r6-fixes
for p in $(pgrep -f "$R/editor/scripts/dev-local-workspace.mjs"); do kill -TERM $p; done
for i in $(seq 1 45); do lsof -nP -iTCP:2400 -iTCP:17500 -iTCP:17501 -sTCP:LISTEN >/dev/null 2>&1 || break; sleep 1; done
for p in $(lsof -nP -iTCP:2400 -iTCP:17500 -iTCP:17501 -sTCP:LISTEN -t 2>/dev/null); do c=$(ps -p $p -o command=); case "$c" in *release-14-r6-fixes*|*runtime-src*|*wt-r14-r6-fixes*) echo "TERM leftover $p"; kill -TERM $p;; *) echo "UNKNOWN listener $p $c";; esac; done
sleep 2
lsof -nP -iTCP:2400 -iTCP:17500 -iTCP:17501 -sTCP:LISTEN && { echo "ports still busy"; exit 1; }
LOG=$R/logs/editor-$(date +%Y%m%d-%H%M%S).log
nohup $S/fixed/start-source-stack.sh > $LOG 2>&1 &
echo "{\"pid\": $!, \"log\": \"$LOG\"}" > $S/fixed/current-launch.json
for i in $(seq 1 120); do
  if curl -s -o /dev/null -m 2 http://localhost:2400/tools/video-editor && lsof -nP -iTCP:17501 -sTCP:LISTEN >/dev/null; then echo "up after $((i*2))s"; break; fi; sleep 2; done
lsof -nP -iTCP -sTCP:LISTEN | grep -E ':(2400|17500|17501) ' | awk '{print $1,$2,$9}'
