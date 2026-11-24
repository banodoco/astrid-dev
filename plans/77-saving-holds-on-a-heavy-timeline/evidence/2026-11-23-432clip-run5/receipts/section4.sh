#!/bin/bash
source /root/codex/p77box/run5/receipts/environment.sh
trap 'rc=$?; printf "%s\n" "$rc" >"$RECEIPTS/section4-exit.txt"; date -u +%FT%TZ >"$RECEIPTS/section4-end.txt"' EXIT
version=$(cat "$STACK/program/current")
PYTHON="$STACK/program/versions/$version/py/bin/python"
TARGET="$DATA/runtime/realms/$REALM"
DISCOVERY="$DATA/runtime/discovery.json"
SCHEMA_DIGEST=$(jq -er '.runtime.schema_digest' "$STACK/install-manifest.json")
deadline=$((SECONDS+2700))
ready=0
date -u +%FT%TZ >"$RECEIPTS/readiness-start.txt"
while (( SECONDS < deadline )); do
  if jq -e --arg realm "$REALM" --arg target "$TARGET" \
    'select(.active_realm==$realm and .realm_root==$target and
      (.pid|type)=="number" and .pid>0 and
      (.process_birth_id|type)=="string" and
      (.runtime_instance_id|type)=="string" and (.runtime_instance_id|length)>0 and
      (.endpoint|test("^http://127\\.0\\.0\\.1:[0-9]+$")) and
      .door_endpoint=="http://127.0.0.1:17501") |
      {active_realm,realm_root,pid,process_birth_id,runtime_instance_id,endpoint,door_endpoint}' \
    "$DISCOVERY" >"$RECEIPTS/discovery-safe.json" 2>/dev/null; then
    PID=$(jq -er .pid "$RECEIPTS/discovery-safe.json")
    BIRTH=$(jq -er .process_birth_id "$RECEIPTS/discovery-safe.json")
    INSTANCE=$(jq -er .runtime_instance_id "$RECEIPTS/discovery-safe.json")
    ENDPOINT=$(jq -er .endpoint "$RECEIPTS/discovery-safe.json")
    if "${owned[@]}" "$PYTHON" - "$PID" "$BIRTH" <<'PY'
import sys
from runtime_protocol import platform
identity = platform.process_identity(int(sys.argv[1]))
assert identity and platform.process_birth_matches(sys.argv[2], identity["birth_id"]) is True
PY
    then
      if curl -fsS --max-time 3 "$ENDPOINT/v1/health" >"$RECEIPTS/health.json" &&
         jq -e --arg id "$INSTANCE" --arg digest "$SCHEMA_DIGEST" \
           '.status=="ok" and .protocol=="workspace.v1" and
            .runtime_instance_id==$id and .schema_digest==$digest' "$RECEIPTS/health.json" >/dev/null &&
         curl -fsS --max-time 3 -H 'Origin: https://astrid.haus' \
           http://127.0.0.1:17501/api/runtime/v1/health >"$RECEIPTS/door-health.json" &&
         jq -e --arg id "$INSTANCE" '.status=="ok" and .runtime_instance_id==$id' \
           "$RECEIPTS/door-health.json" >/dev/null; then
        ready=1
        break
      fi
    fi
  fi
  sleep 3
done
date -u +%FT%TZ >"$RECEIPTS/readiness-end.txt"
test "$ready" = 1
