#!/usr/bin/env bash
# Create a separate local measured tuple using the official pin generator.
set -Eeuo pipefail
umask 077
work=/path/to/astrid-sandbox
evidence="$work/run/evidence/plan-77/round7-acceptance"
pins="$evidence/candidate-pins"
app_source="${1:?reviewed App commit}"
agent_source="${2:?reviewed Agent commit}"
runtime_source="${3:?reviewed Runtime commit}"
[[ "$app_source" =~ ^[0-9a-f]{40}$ && "$agent_source" =~ ^[0-9a-f]{40}$ && "$runtime_source" =~ ^[0-9a-f]{40}$ ]]
app="$work/wt/astrid-app-p77-r7-installed-trial"
agent="$work/wt/astrid-agent-p77-r7-installed-trial"
runtime_repo="$work/astrid-runtime"
repo_app="$work/astrid-app"
repo_agent="$work/astrid-agent"
stock_omp="$work/wt/astrid-app-p69-exact-pe1a.env/omp-source-cache"
dep="$work/wt/astrid-app-p77-quick-baseline-product"
[[ ! -e "$pins" && ! -e "$app" && ! -e "$agent" ]]
[[ "$(git -C "$repo_app" rev-parse "$app_source^{commit}")" == "$app_source" ]]
[[ "$(git -C "$repo_agent" rev-parse "$agent_source^{commit}")" == "$agent_source" ]]
[[ "$(git -C "$runtime_repo" rev-parse "$runtime_source^{commit}")" == "$runtime_source" ]]
git -C "$repo_app" merge-base --is-ancestor e3dbad64d402724ac5a35fb6447f18e432c64b78 "$app_source"
git -C "$repo_agent" merge-base --is-ancestor 8807f820eb47d6018db723511e024a0a123fbe95 "$agent_source"
git -C "$runtime_repo" merge-base --is-ancestor 23310dc828765293a2ab39f637f28b948e780d94 "$runtime_source"
git -C "$runtime_repo" diff --quiet 23310dc8 "$runtime_source" -- contract/manifest.json contract/openapi/workspace-v1.yaml \
  contract/schemas runtime_protocol/contract_metadata.py
df -h /home/user
(( $(df -Pk /home/user | awk 'NR == 2 {print $4}') >= 25*1024*1024 ))
mkdir -m 700 "$pins"
git -C "$repo_app" worktree add --detach "$app" "$app_source"
git -C "$repo_agent" worktree add --detach "$agent" "$agent_source"
mkdir -m 700 "$app.env" "$agent.env"
cmp "$dep/package-lock.json" "$app/package-lock.json"
cp -al -- "$dep/node_modules" "$app/node_modules"

regenerate() {
  python3 "$agent/scripts/regenerate_runtime_pins.py" --runtime-checkout "$runtime_repo" \
    --runtime-sha "$runtime_source" --agent-sha "$1" --agent-checkout "$agent" --app-checkout "$app" --apply
}
regenerate "$agent_source"
test "$(git -C "$agent" diff --name-only)" = $'astrid/resources/runtime.lock.json\nruntime.lock.json'
cmp "$agent/runtime.lock.json" "$agent/astrid/resources/runtime.lock.json"
jq -e --arg runtime "$runtime_source" '.source_commit==$runtime' "$agent/runtime.lock.json" >/dev/null
git -C "$agent" add runtime.lock.json astrid/resources/runtime.lock.json
git -C "$agent" diff --cached --check
git -C "$agent" commit -m 'Pin the exact Runtime for the local Plan 77 trial'
agent_pin="$(git -C "$agent" rev-parse HEAD)"
regenerate "$agent_pin"
test "$(git -C "$app" diff --name-only)" = $'public/install-manifest.json\nruntime.lock.json'
git -C "$app" add public/install-manifest.json runtime.lock.json
git -C "$app" diff --cached --check
git -C "$app" commit -m 'Pin the exact Agent and Runtime for the local Plan 77 trial'
app_pin="$(git -C "$app" rev-parse HEAD)"
[[ -z "$(git -C "$agent" status --porcelain)" && -z "$(git -C "$app" status --porcelain)" ]]
jq -n --arg app "$app_pin" --arg agent "$agent_pin" --arg runtime "$runtime_source" \
  '{app:$app,agent:$agent,runtime:$runtime}' >"$pins/versions.json"
jq -n --arg app "$app_source" --arg agent "$agent_source" --arg runtime "$runtime_source" \
  '{app:$app,agent:$agent,runtime:$runtime}' >"$pins/reviewed-source.json"

make_mirror() {
  local source="$1" revision="$2" mirror="$3"
  git clone --bare --shared "$source" "$mirror"
  git -C "$mirror" update-ref refs/heads/trial "$revision"
  git -C "$mirror" symbolic-ref HEAD refs/heads/trial
  [[ "$(git -C "$mirror" rev-parse HEAD)" == "$revision" ]]
}
agent_mirror="$pins/astrid-agent.git"
runtime_mirror="$pins/astrid-runtime.git"
make_mirror "$repo_agent" "$agent_pin" "$agent_mirror"
make_mirror "$runtime_repo" "$runtime_source" "$runtime_mirror"
node --input-type=module - "$app" "$agent_mirror" "$runtime_mirror" "$stock_omp" "$pins/install-manifest.json" <<'NODE'
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFile, writeFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
const [app, agent, runtime, omp, out] = process.argv.slice(2);
const {checkManifest} = await import(pathToFileURL(app + '/scripts/installer/pin.mjs'));
const manifest = JSON.parse(await readFile(app + '/public/install-manifest.json', 'utf8'));
const mirrors = {'banodoco/astrid-agent': agent, 'banodoco/astrid-runtime': runtime};
console.log(await checkManifest(manifest, (repo, sha, file) => execFileSync('git', ['-C', mirrors[repo], 'show', sha + ':' + file])));
assert.equal(manifest.tools.omp.source.sha, '78f0e0960f471c2c62b943272a48c33366f239fe');
assert.equal(execFileSync('git', ['-C', omp, 'rev-parse', manifest.tools.omp.source.sha + '^{commit}'],
  {encoding: 'utf8'}).trim(), manifest.tools.omp.source.sha);
manifest.agent.repo = agent;
manifest.runtime.repo = runtime;
manifest.tools.omp.source.repo = omp;
await writeFile(out, JSON.stringify(manifest, null, 2) + '\n', {flag: 'wx', mode: 0o600});
NODE
sha256sum "$pins/install-manifest.json" "$pins/versions.json" "$pins/reviewed-source.json" >"$pins/identity.sha256"
printf '\nTrial App checkout %s\n' "$app"
