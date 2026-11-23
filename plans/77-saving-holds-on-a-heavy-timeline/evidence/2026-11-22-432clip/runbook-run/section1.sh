#!/bin/bash
set -Eeuo pipefail
umask 077
R=/root/codex/p77box/run2/receipts
trap 'rc=$?; printf "%s\n" "$rc" > "$R/section1-exit.txt"; date -u +%FT%TZ > "$R/section1-end.txt"' EXIT
date -u +%FT%TZ > "$R/section1-start.txt"
BOX=/root/codex/p77box
BACKUP="$BOX/backup/realm-432"
PROOF="$BOX/restore-432-proof"
STACK="$BOX/round5-432-readback"
RECEIPTS="$BOX/run2/receipts/round5-432-readback-receipts"
APP="$BOX/wt"
TOOLS="$BOX/round5-432-tools-wt"
NODE20="$BOX/node-v20.19.4-linux-x64/bin/node"
APP_SHA=be9cc2407306eff06252c0d54be1c7f5afcacf3f
AGENT_SHA=18adee8034973837a97fcd7392cd67f4566fa992
RUNTIME_SHA=d7be2f0458a55c1f26e1138a125ffefe382f56f4
test "$(git -C "$APP" rev-parse HEAD)" = "$APP_SHA"
test -z "$(git -C "$APP" status --porcelain)"
test "$(git -C "$TOOLS" rev-parse HEAD)" = 5b2c76a6a636d835700bc5f12b48848861dc30f5
test "$(node -p 'process.versions.node.split(".")[0]')" = 22
test "$("$NODE20" --version)" = v20.19.4
test "$(realpath "$PROOF")" = "$PROOF"
test "$(realpath -m "$STACK")" = "$STACK"
test "$(realpath -m "$RECEIPTS")" = "$RECEIPTS"
test ! -e "$STACK" && test ! -L "$STACK"
test ! -e "$RECEIPTS" && test ! -L "$RECEIPTS"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
python3 - <<'PY'
import socket
for port in (2400,17500,17501):
    with socket.socket() as listener: listener.bind(('127.0.0.1',port))
PY
mkdir -m 700 "$STACK" "$RECEIPTS"
mkdir -m 700 "$STACK/home" "$STACK/tmp"
owned=(env -u ASTRID_PREPARED_CONNECTION -u ASTRID_TIMELINE_EVAL_ENDPOINT -u ASTRID_TIMELINE_EVAL_CREDENTIAL -u ASTRID_TIMELINE_EVAL_REALM_ID -u ASTRID_TIMELINE_EVAL_ACTOR_ID -u ASTRID_RUNTIME_DATA_ROOT -u ASTRID_RUNTIME_SOURCE_MANIFEST -u ASTRID_RUNTIME_CREDENTIAL HOME="$STACK/home" TMPDIR="$STACK/tmp" XDG_DATA_HOME="$STACK/home/.local/share" XDG_STATE_HOME="$STACK/home/.local/state" XDG_CONFIG_HOME="$STACK/home/.config" XDG_CACHE_HOME="$STACK/home/.cache" ASTRID_NODE_EXECUTABLE="$NODE20" LIBGL_ALWAYS_SOFTWARE=1)
jq -e --arg a "$AGENT_SHA" --arg r "$RUNTIME_SHA" '.agent.sha==$a and .runtime.sha==$r' "$APP/public/install-manifest.json" >/dev/null
cp -- "$APP/public/install-manifest.json" "$STACK/install-manifest.json"
test "$(git -C "$BOX/omp-cache" rev-parse 78f0e0960f471c2c62b943272a48c33366f239fe^{commit})" = 78f0e0960f471c2c62b943272a48c33366f239fe
jq -e '.tools.omp.source.sha=="78f0e0960f471c2c62b943272a48c33366f239fe"' "$STACK/install-manifest.json" >/dev/null
jq --arg repo "$BOX/omp-cache" '.tools.omp.source.repo=$repo' "$STACK/install-manifest.json" > "$STACK/install-manifest.tmp"
mv "$STACK/install-manifest.tmp" "$STACK/install-manifest.json"
printf 'OMP transport substitution: /root/codex/p77box/omp-cache at 78f0e0960f471c2c62b943272a48c33366f239fe\n' > "$RECEIPTS/mirror.txt"
"${owned[@]}" ASTRID_RUNTIME_DOOR_PORT=17501 sh "$APP/public/install" --root "$STACK/program" --data-root "$STACK/installed-data" --yes --autostart off --command off --skills off --skill-copies off --no-browser --manifest "$STACK/install-manifest.json" >"$RECEIPTS/install.log" 2>&1
version=$(cat "$STACK/program/current")
[[ "$version" =~ ^[a-f0-9]{12,40}$ ]]
CLI="$STACK/program/versions/$version/py/bin/astrid-runtime"
PROTO="${CLI%/*}/astrid-runtime-protocol"
PYTHON="${CLI%/*}/python"
SOURCE="$STACK/installed-data/runtime/source-profiles/astrid.json"
test -x "$CLI" && test -x "$PROTO" && test -x "$PYTHON" && test -f "$SOURCE"
jq -e --arg data "$STACK/installed-data" '.owner=="haus.astrid.runtime" and .data_root==$data' "$STACK/program/install.json" >/dev/null
printf '%s\n' "$APP_SHA" "$AGENT_SHA" "$RUNTIME_SHA" >"$RECEIPTS/tuple.txt"
sha256sum "$STACK/install-manifest.json" "$SOURCE" >"$RECEIPTS/install-inputs.sha256"
"${owned[@]}" "$CLI" down --profile astrid --data-root "$STACK/installed-data" --door-port 17501 --json >"$RECEIPTS/installed-empty-down.json"
jq -e '.status=="stopped" and .idle.safe==true' "$RECEIPTS/installed-empty-down.json" >/dev/null
