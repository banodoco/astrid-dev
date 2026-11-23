#!/bin/bash
source /root/codex/p77box/run5/receipts/environment.sh
trap 'rc=$?; printf "%s\n" "$rc" >"$RECEIPTS/section1-exit.txt"; date -u +%FT%TZ >"$RECEIPTS/section1-end.txt"' EXIT
date -u +%FT%TZ >"$RECEIPTS/section1-start.txt"
test "$(sha256sum "$PINS/exact-tuple.txt" | awk '{print $1}')" = ae558705708ba32c54b9111c41092d85d9bff4af0f6e7f690913e552c5e10e2d
sha256sum "$PINS/exact-tuple.txt" >"$RECEIPTS/exact-tuple.sha256"
cp "$PINS/exact-tuple.txt" "$RECEIPTS/exact-tuple.txt"
test "$(git -C "$APP" rev-parse HEAD)" = "$APP_SHA"
test "$(git -C "$AGENT" rev-parse HEAD)" = "$AGENT_SHA"
test -z "$(git -C "$APP" status --porcelain)"
test -z "$(git -C "$AGENT" status --porcelain)"
test "$(git -C "$TOOLS" rev-parse HEAD)" = 5b2c76a6a636d835700bc5f12b48848861dc30f5
test -z "$(git -C "$TOOLS" status --porcelain)"
test "$(node -p 'process.versions.node.split(".")[0]')" = 22
test "$("$NODE20" --version)" = v20.19.4
test "$(realpath "$PROOF")" = "$PROOF"
test "$(realpath -m "$STACK")" = "$STACK"
test "$(realpath -m "$RECEIPTS")" = "$RECEIPTS"
test ! -e "$STACK" && test ! -L "$STACK"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
python3 - <<'PY'
import socket
for port in (2400, 17500, 17501):
    with socket.socket() as listener:
        listener.bind(('127.0.0.1',port))
PY
mkdir -m 700 "$STACK"
mkdir -m 700 "$STACK/home" "$STACK/tmp"
jq -e --arg a "$AGENT_SHA" --arg r "$RUNTIME_SHA" '.agent.sha==$a and .runtime.sha==$r' "$APP/public/install-manifest.json" >/dev/null
cp -- "$APP/public/install-manifest.json" "$STACK/install-manifest.json"
git clone --mirror "$AGENT" "$STACK/agent.git"
git --git-dir="$STACK/agent.git" fetch "$AGENT" "$AGENT_SHA:refs/heads/run5-agent"
git clone --mirror /home/user/astrid-runtime "$STACK/runtime.git"
git --git-dir="$STACK/runtime.git" fetch /home/user/astrid-runtime refs/remotes/origin/release/15/fix-1491-verified-head:refs/heads/run5-runtime
agent_found=$(git --git-dir="$STACK/agent.git" rev-parse "$AGENT_SHA^{commit}")
runtime_found=$(git --git-dir="$STACK/runtime.git" rev-parse "$RUNTIME_SHA^{commit}")
printf 'agent %s\nruntime %s\n' "$agent_found" "$runtime_found" | tee "$RECEIPTS/mirror-commits.txt"
test "$agent_found" = "$AGENT_SHA"
test "$runtime_found" = "$RUNTIME_SHA"
test "$(git -C "$BOX/omp-cache" rev-parse 78f0e0960f471c2c62b943272a48c33366f239fe^{commit})" = 78f0e0960f471c2c62b943272a48c33366f239fe
jq -e '.tools.omp.source.sha=="78f0e0960f471c2c62b943272a48c33366f239fe"' "$STACK/install-manifest.json" >/dev/null
jq --arg a "$STACK/agent.git" --arg r "$STACK/runtime.git" --arg o "$BOX/omp-cache" '.agent.repo=$a | .runtime.repo=$r | .tools.omp.source.repo=$o' "$STACK/install-manifest.json" >"$STACK/install-manifest.tmp"
mv "$STACK/install-manifest.tmp" "$STACK/install-manifest.json"
node "$RECEIPTS/check-private-manifest.mjs" "$APP" "$STACK/install-manifest.json" "$STACK/agent.git" "$STACK/runtime.git" "$AGENT_SHA" "$RUNTIME_SHA" >"$RECEIPTS/manifest-check.txt"
sha256sum "$APP/public/install-manifest.json" "$STACK/install-manifest.json" >"$RECEIPTS/preinstall-inputs.sha256"
run4_space before_install 25
date -u +%FT%TZ >"$RECEIPTS/install-start.txt"
install_rc=0
"${owned[@]}" ASTRID_RUNTIME_DOOR_PORT=17501 sh "$APP/public/install" --root "$STACK/program" --data-root "$STACK/installed-data" --yes --autostart off --command off --skills off --skill-copies off --no-browser --manifest "$STACK/install-manifest.json" >"$RECEIPTS/install.log" 2>&1 || install_rc=$?
printf '%s\n' "$install_rc" >"$RECEIPTS/install-exit.txt"
date -u +%FT%TZ >"$RECEIPTS/install-end.txt"
test "$install_rc" = 0
version=$(cat "$STACK/program/current")
[[ "$version" =~ ^[a-f0-9]{12,40}$ ]]
CLI="$STACK/program/versions/$version/py/bin/astrid-runtime"
PROTO="${CLI%/*}/astrid-runtime-protocol"
PYTHON="${CLI%/*}/python"
SOURCE="$STACK/installed-data/runtime/source-profiles/astrid.json"
test -x "$CLI" && test -x "$PROTO" && test -x "$PYTHON" && test -f "$SOURCE"
jq -e --arg data "$STACK/installed-data" '.owner=="haus.astrid.runtime" and .data_root==$data' "$STACK/program/install.json" >/dev/null
printf '%s\n' "$APP_SHA" "$AGENT_SHA" "$RUNTIME_SHA" >"$RECEIPTS/tuple.txt"
sha256sum "$STACK/install-manifest.json" "$SOURCE" >"$RECEIPTS/install-inputs.sha256"
"${owned[@]}" "$CLI" down --profile astrid --data-root "$STACK/installed-data" --door-port 17501 --json >"$RECEIPTS/installed-empty-down.json"
jq -e '.status=="stopped" and .idle.safe==true' "$RECEIPTS/installed-empty-down.json" >/dev/null
