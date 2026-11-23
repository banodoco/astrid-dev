#!/bin/bash
source /root/codex/p77box/run5/receipts/environment.sh
trap 'rc=$?; printf "%s\n" "$rc" >"$RECEIPTS/section2-exit.txt"; date -u +%FT%TZ >"$RECEIPTS/section2-end.txt"' EXIT
date -u +%FT%TZ >"$RECEIPTS/section2-start.txt"
version=$(cat "$STACK/program/current")
PROTO="$STACK/program/versions/$version/py/bin/astrid-runtime-protocol"
test ! -e "$PROOF/realm.sqlite3-wal" && test ! -e "$PROOF/realm.sqlite3-shm"
test "$(hash_db "$PROOF")" = "$DBSHA"
test ! -e "$WORKING" && test ! -L "$WORKING"
test ! -e "$DATA" && test ! -L "$DATA"
date -u +%FT%TZ >"$RECEIPTS/restore-start.txt"
restore_rc=0
"${owned[@]}" "$PROTO" restore --backup "$BACKUP" --destination "$WORKING" >"$RECEIPTS/restore.json" 2>"$RECEIPTS/restore.stderr" || restore_rc=$?
printf '%s\n' "$restore_rc" >"$RECEIPTS/restore-exit.txt"
date -u +%FT%TZ >"$RECEIPTS/restore-end.txt"
test "$restore_rc" = 0
jq -e --arg realm "$REALM" --arg sha "$DBSHA" '.realm_id==$realm and .verification.realm.id==$realm and .verification.database_sha256==$sha and .verification.schema.version==33' "$RECEIPTS/restore.json" >/dev/null
test "$(hash_db "$WORKING")" = "$DBSHA"
test "$(hash_db "$PROOF")" = "$DBSHA"
test ! -e "$WORKING/realm.sqlite3-wal" && test ! -e "$WORKING/realm.sqlite3-shm"
sha256sum "$PROOF/realm.sqlite3" "$WORKING/realm.sqlite3" >"$RECEIPTS/pre-adopt-databases.sha256"
run4_space after_restore 12
