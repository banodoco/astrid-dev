#!/bin/bash
source /root/codex/p77box/run5/receipts/environment.sh
trap 'rc=$?; printf "%s\n" "$rc" >"$RECEIPTS/build-exit.txt"; date -u +%FT%TZ >"$RECEIPTS/build-end.txt"' EXIT
version=$(cat "$STACK/program/current")
PYTHON="$STACK/program/versions/$version/py/bin/python"
ADOPTED_SOURCE="$DATA/runtime/source-profiles/astrid.json"
run4_space before_browser 10
date -u +%FT%TZ >"$RECEIPTS/build-start.txt"
(
 cd "$APP"
 "${owned[@]}" PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
 "${owned[@]}" ASTRID_RUNTIME_PYTHON="$PYTHON" ASTRID_RUNTIME_SOURCE_MANIFEST="$ADOPTED_SOURCE" PORT=2400 ASTRID_APP_LOOPBACK_ORIGIN=off node scripts/dev-local-workspace.mjs --data-root "$DATA" --build
) >"$RECEIPTS/build.log" 2>&1
test -f "$APP/dist/index.html" && test -d "$APP/dist/assets"
(cd "$APP/dist" && find . -type f -print0 | sort -z | xargs -0 sha256sum) >"$RECEIPTS/dist-files.sha256"
