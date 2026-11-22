#!/bin/bash
set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
STACK="$BOX/round5-432-readback"
WORKING="$STACK/working-restore"
PROOF="$BOX/restore-432-proof"
R="$BOX/run2/receipts"
NODE20="$BOX/node-v20.19.4-linux-x64/bin/node"
DBSHA=5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8
version=$(cat "$STACK/program/current")
PROTO="$STACK/program/versions/$version/py/bin/astrid-runtime-protocol"
owned=(env -u ASTRID_PREPARED_CONNECTION -u ASTRID_TIMELINE_EVAL_ENDPOINT -u ASTRID_TIMELINE_EVAL_CREDENTIAL -u ASTRID_TIMELINE_EVAL_REALM_ID -u ASTRID_TIMELINE_EVAL_ACTOR_ID -u ASTRID_RUNTIME_DATA_ROOT -u ASTRID_RUNTIME_SOURCE_MANIFEST -u ASTRID_RUNTIME_CREDENTIAL HOME="$STACK/home" TMPDIR="$STACK/tmp" XDG_DATA_HOME="$STACK/home/.local/share" XDG_STATE_HOME="$STACK/home/.local/state" XDG_CONFIG_HOME="$STACK/home/.config" XDG_CACHE_HOME="$STACK/home/.cache" ASTRID_NODE_EXECUTABLE="$NODE20" LIBGL_ALWAYS_SOFTWARE=1)
trap 'rc=$?; date -u +%FT%TZ > "$R/working-doctor-wrapper-end.txt"; printf "%s\n" "$rc" > "$R/working-doctor-wrapper-exit.txt"' EXIT
{
 date -u +%FT%TZ
 test ! -e "$WORKING/realm.sqlite3-wal" && test ! -e "$WORKING/realm.sqlite3-shm"
 echo 'working wal and shm absent'
 sha256sum "$WORKING/realm.sqlite3"
 test "$(sha256sum "$WORKING/realm.sqlite3" | awk '{print $1}')" = "$DBSHA"
} > "$R/working-doctor-precheck.txt"
date -u +%FT%TZ > "$R/working-doctor-start.txt"
"${owned[@]}" "$PROTO" doctor --root "$WORKING" --admission-timeout 1800 > "$R/working-doctor.json" 2> "$R/working-doctor.stderr" &
doctor_pid=$!
printf '%s\n' "$doctor_pid" > "$R/working-doctor-pid.txt"
(
 while kill -0 "$doctor_pid" 2>/dev/null; do
  python3 - "$doctor_pid" <<'PY' || true
import datetime,os,sys
try:
    with open('/proc/'+sys.argv[1]+'/stat') as f: fields=f.read().rsplit(')',1)[1].split()
    print(datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pid='+sys.argv[1], 'cpu_seconds='+str((int(fields[11])+int(fields[12]))/os.sysconf('SC_CLK_TCK')), flush=True)
except (FileNotFoundError,ProcessLookupError): pass
PY
  sleep 30
done
) > "$R/working-doctor-cpu.txt" 2>&1 &
sampler=$!
rc=0
wait "$doctor_pid" || rc=$?
date -u +%FT%TZ > "$R/working-doctor-end.txt"
kill "$sampler" 2>/dev/null || true
wait "$sampler" 2>/dev/null || true
printf '%s\n' "$rc" > "$R/working-doctor-command-exit.txt"
{
 date -u +%FT%TZ
 test ! -e "$WORKING/realm.sqlite3-wal" && test ! -e "$WORKING/realm.sqlite3-shm"
 echo 'working wal and shm absent'
 sha256sum "$WORKING/realm.sqlite3" "$PROOF/realm.sqlite3"
 test "$(sha256sum "$WORKING/realm.sqlite3" | awk '{print $1}')" = "$DBSHA"
 test "$(sha256sum "$PROOF/realm.sqlite3" | awk '{print $1}')" = "$DBSHA"
} > "$R/working-doctor-postcheck.txt"
printf '%s\n' "$rc" > "$R/working-doctor-exit.txt"
