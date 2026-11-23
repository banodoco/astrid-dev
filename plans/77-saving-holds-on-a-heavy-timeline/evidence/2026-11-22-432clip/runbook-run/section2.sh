#!/bin/bash
set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
STACK="$BOX/round5-432-readback"
RECEIPTS="$BOX/run2/receipts/round5-432-readback-receipts"
PROOF="$BOX/restore-432-proof"
BACKUP="$BOX/backup/realm-432"
WORKING="$STACK/working-restore"
DATA="$STACK/direct-data"
REALM=0d6fd08f-8754-489c-8af9-276dcde43762
DBSHA=5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8
NODE20="$BOX/node-v20.19.4-linux-x64/bin/node"
version=$(cat "$STACK/program/current")
PROTO="$STACK/program/versions/$version/py/bin/astrid-runtime-protocol"
owned=(env -u ASTRID_PREPARED_CONNECTION -u ASTRID_TIMELINE_EVAL_ENDPOINT -u ASTRID_TIMELINE_EVAL_CREDENTIAL -u ASTRID_TIMELINE_EVAL_REALM_ID -u ASTRID_TIMELINE_EVAL_ACTOR_ID -u ASTRID_RUNTIME_DATA_ROOT -u ASTRID_RUNTIME_SOURCE_MANIFEST -u ASTRID_RUNTIME_CREDENTIAL HOME="$STACK/home" TMPDIR="$STACK/tmp" XDG_DATA_HOME="$STACK/home/.local/share" XDG_STATE_HOME="$STACK/home/.local/state" XDG_CONFIG_HOME="$STACK/home/.config" XDG_CACHE_HOME="$STACK/home/.cache" ASTRID_NODE_EXECUTABLE="$NODE20" LIBGL_ALWAYS_SOFTWARE=1)
trap 'rc=$?; printf "%s\n" "$rc" > "$RECEIPTS/section2-exit.txt"; date -u +%FT%TZ > "$RECEIPTS/section2-end.txt"' EXIT
date -u +%FT%TZ > "$RECEIPTS/section2-start.txt"
hash_db() { sha256sum "$1/realm.sqlite3" | awk '{print $1}'; }
test ! -e "$PROOF/realm.sqlite3-wal" && test ! -e "$PROOF/realm.sqlite3-shm"
test "$(hash_db "$PROOF")" = "$DBSHA"
test ! -e "$WORKING" && test ! -L "$WORKING"
test ! -e "$DATA" && test ! -L "$DATA"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
date -u +%FT%TZ >"$RECEIPTS/restore-start.txt"
"${owned[@]}" "$PROTO" restore --backup "$BACKUP" --destination "$WORKING" >"$RECEIPTS/restore.json" 2>"$RECEIPTS/restore.stderr"
date -u +%FT%TZ >"$RECEIPTS/restore-end.txt"
jq -e --arg realm "$REALM" --arg sha "$DBSHA" '.realm_id==$realm and .verification.realm.id==$realm and .verification.database_sha256==$sha and .verification.schema.version==33' "$RECEIPTS/restore.json" >/dev/null
test "$(hash_db "$WORKING")" = "$DBSHA"
test "$(hash_db "$PROOF")" = "$DBSHA"
test ! -e "$WORKING/realm.sqlite3-wal" && test ! -e "$WORKING/realm.sqlite3-shm"
sha256sum "$PROOF/realm.sqlite3" "$WORKING/realm.sqlite3" >"$RECEIPTS/pre-adopt-databases.sha256"
