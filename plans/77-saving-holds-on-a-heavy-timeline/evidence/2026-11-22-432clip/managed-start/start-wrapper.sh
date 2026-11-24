#!/bin/bash
set -u
R=/root/codex/p77box/run3/receipts
{
 date -u +'%Y-%m-%dT%H:%M:%S.%3NZ'
 printf '%s\n' 'Environment variable names: PATH HOME XDG_DATA_HOME XDG_STATE_HOME TMPDIR ASTRID_NODE_EXECUTABLE ASTRID_RUNTIME_DOOR_PORT'
 printf '%s\n' 'Command: /root/codex/p77box/stack/program/versions/1d2700baa660/py/bin/astrid-runtime up --profile astrid --data-root /root/codex/p77box/stack/data --door-port 17501 --json'
 printf 'wrapper_pid=%s\n' "$$"
} > "$R/02-start.txt"
env -i PATH=/usr/bin:/bin HOME=/root/codex/p77box/stack/home XDG_DATA_HOME=/root/codex/p77box/stack/home/.local/share XDG_STATE_HOME=/root/codex/p77box/stack/home/.local/state TMPDIR=/root/codex/p77box/stack/tmp ASTRID_NODE_EXECUTABLE=/root/codex/p77box/node-v20.19.4-linux-x64/bin/node ASTRID_RUNTIME_DOOR_PORT=17501 /root/codex/p77box/stack/program/versions/1d2700baa660/py/bin/astrid-runtime up --profile astrid --data-root /root/codex/p77box/stack/data --door-port 17501 --json > "$R/02-up.stdout" 2> "$R/02-up.stderr"
rc=$?
printf 'exit_code=%s\nend_utc=%s\n' "$rc" "$(date -u +'%Y-%m-%dT%H:%M:%S.%3NZ')" >> "$R/02-start.txt"
printf '%s\n' "$rc" > "$R/02-up.done"
