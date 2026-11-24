set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
RUN5="$BOX/run5"
STACK="$RUN5/stack"
RECEIPTS="$RUN5/receipts"
PINS="$BOX/firstcut-432-reviewed-pins"
APP="$PINS/app"
AGENT="$PINS/agent"
TOOLS="$BOX/round5-432-tools-wt"
NODE20="$BOX/node-v20.19.4-linux-x64/bin/node"
BACKUP="$BOX/backup/realm-432"
PROOF="$BOX/restore-432-proof"
WORKING="$STACK/working-restore"
DATA="$STACK/direct-data"
REALM=0d6fd08f-8754-489c-8af9-276dcde43762
DBSHA=5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8
mapfile -t tuple < "$PINS/exact-tuple.txt"
[[ ${#tuple[@]} == 5 ]]
APP_SHA=${tuple[2]}
AGENT_SHA=${tuple[3]}
RUNTIME_SHA=${tuple[4]}
owned=(env -u ASTRID_PREPARED_CONNECTION -u ASTRID_TIMELINE_EVAL_ENDPOINT -u ASTRID_TIMELINE_EVAL_CREDENTIAL -u ASTRID_TIMELINE_EVAL_REALM_ID -u ASTRID_TIMELINE_EVAL_ACTOR_ID -u ASTRID_RUNTIME_DATA_ROOT -u ASTRID_RUNTIME_SOURCE_MANIFEST -u ASTRID_RUNTIME_CREDENTIAL HOME="$STACK/home" TMPDIR="$STACK/tmp" XDG_DATA_HOME="$STACK/home/.local/share" XDG_STATE_HOME="$STACK/home/.local/state" XDG_CONFIG_HOME="$STACK/home/.config" XDG_CACHE_HOME="$STACK/home/.cache" ASTRID_NODE_EXECUTABLE="$NODE20" LIBGL_ALWAYS_SOFTWARE=1)
run4_space() {
  local stage="$1" required_gib="$2" free_kib
  free_kib=$(df -Pk "$BOX" | awk 'NR==2 {print $4}')
  [[ "$free_kib" =~ ^[0-9]+$ ]]
  {
    printf '%s %s free_kib=%s required_gib=%s\n' "$(date -u +%FT%TZ)" "$stage" "$free_kib" "$required_gib"
    df -h "$BOX"
  } | tee -a "$RECEIPTS/run4-disk-preflight.log"
  (( free_kib >= 5 * 1024 * 1024 && free_kib >= required_gib * 1024 * 1024 ))
}
hash_db() { sha256sum "$1/realm.sqlite3" | awk '{print $1}'; }
