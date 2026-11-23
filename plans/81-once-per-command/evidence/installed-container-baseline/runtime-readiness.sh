#!/usr/bin/env bash
# Keep the final attempt's output for diagnosis if a Runtime never becomes ready.
runtime_ready() {
  local launcher=$1 arm=$2 log=$3 i
  for i in 1 2 3 4; do
    if "$launcher" projects list --json >"$log" 2>"$log.stderr"; then
      if python3 -c 'import json, sys; data = json.load(sys.stdin); sys.exit(0 if isinstance(data, dict) and data.get("ok") is True else 1)' <"$log" 2>/dev/null; then
        return 0
      fi
      echo 'Readiness response was not a JSON object with ok=true.' >>"$log.stderr"
    fi
    cat "$log.stderr" >>"$log"
    [ "$i" = 4 ] || sleep 4
  done
  echo "FAIL: Runtime for $arm did not become ready after 4 attempts; see $log" >&2
  return 1
}
