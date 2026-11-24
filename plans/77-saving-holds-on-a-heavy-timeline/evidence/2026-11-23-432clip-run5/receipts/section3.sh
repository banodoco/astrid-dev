#!/bin/bash
source /root/codex/p77box/run5/receipts/environment.sh
trap 'rc=$?; printf "%s\n" "$rc" >"$RECEIPTS/section3-exit.txt"; date -u +%FT%TZ >"$RECEIPTS/section3-end.txt"' EXIT
version=$(cat "$STACK/program/current")
CLI="$STACK/program/versions/$version/py/bin/astrid-runtime"
SOURCE="$STACK/installed-data/runtime/source-profiles/astrid.json"
TARGET="$DATA/runtime/realms/$REALM"
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
