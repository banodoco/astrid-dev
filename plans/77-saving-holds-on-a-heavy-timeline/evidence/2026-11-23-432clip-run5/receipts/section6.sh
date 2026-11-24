#!/bin/bash
source /root/codex/p77box/run5/receipts/environment.sh
trap 'rc=$?; printf "%s\n" "$rc" >"$RECEIPTS/section6-exit.txt"; date -u +%FT%TZ >"$RECEIPTS/section6-end.txt"' EXIT
date -u +%FT%TZ >"$RECEIPTS/section6-start.txt"
version=$(cat "$STACK/program/current")
CLI="$STACK/program/versions/$version/py/bin/astrid-runtime"
TARGET="$DATA/runtime/realms/$REALM"
"${owned[@]}" "$CLI" down --profile astrid --data-root "$DATA" --door-port 17501 --json >"$RECEIPTS/adopted-down.json" 2>"$RECEIPTS/adopted-down.stderr"
jq -e '.status=="stopped" and .idle.safe==true' "$RECEIPTS/adopted-down.json" >/dev/null
for realm_dir in "$PROOF" "$WORKING" "$TARGET"; do
 test ! -e "$realm_dir/realm.sqlite3-wal" && test ! -e "$realm_dir/realm.sqlite3-shm"
done
sha256sum "$PROOF/realm.sqlite3" "$WORKING/realm.sqlite3" "$TARGET/realm.sqlite3" >"$RECEIPTS/post-stop-databases.sha256"
test "$(hash_db "$PROOF")" = "$DBSHA"
test "$(hash_db "$WORKING")" = "$DBSHA"
python3 - "$TARGET/realm.sqlite3" <<'PY' >"$RECEIPTS/adopted-schema.json"
import json, sqlite3, sys
from pathlib import Path
uri = Path(sys.argv[1]).resolve(strict=True).as_uri() + '?mode=ro&immutable=1'
with sqlite3.connect(uri, uri=True) as db:
    print(json.dumps({'sqlite_user_version': db.execute('PRAGMA user_version').fetchone()[0]}))
PY
python3 - <<'PY' >"$RECEIPTS/ports-after-stop.txt"
import socket
for port in (2400,17500,17501):
    with socket.socket() as sock:
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1',port))
        print(f'{port} connect_ex={result}')
        assert result != 0
PY
