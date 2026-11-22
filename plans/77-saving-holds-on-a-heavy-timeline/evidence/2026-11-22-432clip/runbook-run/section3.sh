#!/bin/bash
set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
STACK="$BOX/round5-432-readback"
RECEIPTS="$BOX/run2/receipts/round5-432-readback-receipts"
WORKING="$STACK/working-restore"
DATA="$STACK/direct-data"
REALM=0d6fd08f-8754-489c-8af9-276dcde43762
TARGET="$DATA/runtime/realms/$REALM"
NODE20="$BOX/node-v20.19.4-linux-x64/bin/node"
version=$(cat "$STACK/program/current")
CLI="$STACK/program/versions/$version/py/bin/astrid-runtime"
SOURCE="$STACK/installed-data/runtime/source-profiles/astrid.json"
owned=(env -u ASTRID_PREPARED_CONNECTION -u ASTRID_TIMELINE_EVAL_ENDPOINT -u ASTRID_TIMELINE_EVAL_CREDENTIAL -u ASTRID_TIMELINE_EVAL_REALM_ID -u ASTRID_TIMELINE_EVAL_ACTOR_ID -u ASTRID_RUNTIME_DATA_ROOT -u ASTRID_RUNTIME_SOURCE_MANIFEST -u ASTRID_RUNTIME_CREDENTIAL HOME="$STACK/home" TMPDIR="$STACK/tmp" XDG_DATA_HOME="$STACK/home/.local/share" XDG_STATE_HOME="$STACK/home/.local/state" XDG_CONFIG_HOME="$STACK/home/.config" XDG_CACHE_HOME="$STACK/home/.cache" ASTRID_NODE_EXECUTABLE="$NODE20" LIBGL_ALWAYS_SOFTWARE=1)
trap 'rc=$?; date -u +%FT%TZ > "$RECEIPTS/section3-end.txt"; printf "%s\n" "$rc" > "$RECEIPTS/section3-exit.txt"' EXIT
date -u +%FT%TZ >"$RECEIPTS/adopt-start.txt"
adopt_rc=0
"${owned[@]}" ASTRID_RUNTIME_ADMISSION_TIMEOUT_SECONDS=1800 "$CLI" workspace adopt --profile astrid --data-root "$DATA" --source-manifest "$SOURCE" --from "$WORKING" --realm-id "$REALM" --door-port 17501 --json >"$RECEIPTS/adopt.json" 2>"$RECEIPTS/adopt.stderr" || adopt_rc=$?
printf '%s\n' "$adopt_rc" >"$RECEIPTS/adopt-exit.txt"
date -u +%FT%TZ >"$RECEIPTS/adopt-end.txt"
test -d "$TARGET" && test ! -L "$TARGET"
jq -e --arg realm "$REALM" --arg target "$TARGET" '.selected_realm_id==$realm and (.realms|length)==1 and .realms[0].realm_id==$realm and .realms[0].data_root==$target' "$DATA/runtime/catalog.json" >"$RECEIPTS/selected-catalog-check.json"
if (( adopt_rc == 0 )); then
 jq -e --arg realm "$REALM" --arg target "$TARGET" '.ok==true and .realm_id==$realm and .destination==$target' "$RECEIPTS/adopt.json" >/dev/null
else
 jq -e --arg prefix "realm materialized at $TARGET; finish with astrid-runtime up after resolving: " '.ok==false and (.error|startswith($prefix) and endswith("transport_timeout: runtime request timed out"))' "$RECEIPTS/adopt.json" >/dev/null
fi
test -f "$DATA/runtime/source-profiles/astrid.json"
