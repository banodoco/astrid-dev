#!/bin/bash
declare -a owned=([0]="env" [1]="-u" [2]="ASTRID_PREPARED_CONNECTION" [3]="-u" [4]="ASTRID_TIMELINE_EVAL_ENDPOINT" [5]="-u" [6]="ASTRID_TIMELINE_EVAL_CREDENTIAL" [7]="-u" [8]="ASTRID_TIMELINE_EVAL_REALM_ID" [9]="-u" [10]="ASTRID_TIMELINE_EVAL_ACTOR_ID" [11]="-u" [12]="ASTRID_RUNTIME_DATA_ROOT" [13]="-u" [14]="ASTRID_RUNTIME_SOURCE_MANIFEST" [15]="-u" [16]="ASTRID_RUNTIME_CREDENTIAL" [17]="HOME=/root/codex/p77box/run4/stack/home" [18]="TMPDIR=/root/codex/p77box/run4/stack/tmp" [19]="XDG_DATA_HOME=/root/codex/p77box/run4/stack/home/.local/share" [20]="XDG_STATE_HOME=/root/codex/p77box/run4/stack/home/.local/state" [21]="XDG_CONFIG_HOME=/root/codex/p77box/run4/stack/home/.config" [22]="XDG_CACHE_HOME=/root/codex/p77box/run4/stack/home/.cache" [23]="ASTRID_NODE_EXECUTABLE=/root/codex/p77box/node-v20.19.4-linux-x64/bin/node" [24]="LIBGL_ALWAYS_SOFTWARE=1")
declare -- APP="/root/codex/p77box/firstcut-432-reviewed-pins/app"
declare -- STACK="/root/codex/p77box/run4/stack"
declare -- RECEIPTS="/root/codex/p77box/run4/receipts"
date -u +%FT%TZ >"$RECEIPTS/install-start.txt"
"${owned[@]}" ASTRID_RUNTIME_DOOR_PORT=17501 sh "$APP/public/install" --root "$STACK/program" --data-root "$STACK/installed-data" --yes --autostart off --command off --skills off --skill-copies off --no-browser --manifest "$STACK/install-manifest.json" >"$RECEIPTS/install.log" 2>&1
rc=$?
printf '%s\n' "$rc" >"$RECEIPTS/install-exit.txt"
date -u +%FT%TZ >"$RECEIPTS/install-end.txt"
