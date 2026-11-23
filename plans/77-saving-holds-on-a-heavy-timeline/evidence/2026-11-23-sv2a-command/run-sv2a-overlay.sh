#!/usr/bin/env bash
# One diagnostic save on the retained Plan 77 sandbox. No package installation.
set -Eeuo pipefail
umask 077

work=/home/user/codex-run
evidence="$work/run/evidence/plan-77/round7-acceptance"
prep=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
sha="${1:?approved exact diagnostic Runtime SHA}"
approved_package="${2:?approved SHA-256 of package.sha256}"
[[ $# == 2 && "$sha" =~ ^[a-f0-9]{40}$ && "$approved_package" =~ ^[a-f0-9]{64}$ ]]
[[ "$(sha256sum "$prep/package.sha256" | cut -d' ' -f1)" == "$approved_package" ]]
(cd "$prep" && sha256sum -c package.sha256)
[[ "$(jq -er .runtime "$prep/approved-input.json")" == "$sha" ]]
if [[ "${SV2A_STATIC_DRY_RUN:-0}" == 1 ]]; then
  jq '{runtime, tree, retained_runtime, retained_generation, browser_tooling, trace_helpers, trace_schema}' "$prep/approved-input.json"
  printf '%s\n' 'Static dry run. Only the package hashes and fixed inputs were read.'
  exit 0
fi

prior="$evidence/candidate-two-save-profile-20261123-retry"
jq -e --slurpfile approved "$prep/approved-input.json" \
  '.phase=="verified" and .timeline_commit_posts==2 and .saves[-1].accepted==$approved[0].old_public_head' \
  "$prior/browser-two-save-profile.json" >/dev/null
root=$(jq -er .retained_stopped_stack "$prior/cleanup.json")
owner="$work/wt/astrid-app-p77-quick-indicator.env/quick-indicator"
[[ "$root" == "$owner/baseline/large/round7-candidate-two-save-profile-20261123-retry/stack" ]]
[[ "$(realpath "$root")" == "$root" && "$(cat "$root/.sl1-stack-owned")" == "astrid-app-sl1-stack-v1 $root" ]]
[[ "$(cat "$root/program/current")" == 4b62ab1a6521 ]]
jq -e '.status=="stopped" and .idle.safe==true' "$prior/direct-down.json" >/dev/null

realm=201c0486-58d8-4d23-b05d-9220c1762120
data="$root/direct-data"
support="$data/runtime"
program="$root/program"
interpreter="$program/versions/4b62ab1a6521/py/bin/python"
base_runtime=77c38d037f98f744bd8f41c15d95429c124a8003
app="$work/wt/astrid-app-p77-r7-firstcut-requalification-install"
tooling="$work/wt/astrid-app-p77-quick-indicator"
mirror="$evidence/sv2a-prep/candidate-runtime.git"
trace_tools="$work/wt/astrid-app-p77-current-compiled-trace"
out="$evidence/sv2a-first-save-$sha"
archive="$out/source/$sha"
launcher_cwd="$out/launcher-cwd"
source_profile="$out/candidate-source-profile.json"
trace_path="$out/timeline-memo-trace.jsonl"
verify="$prep/verify-overlay.py"
runtime_log="$root/home/.local/state/astrid-runtime/logs/runtime.log"
owner_shell=$BASHPID
minimum_kib=$((16 * 1024 * 1024))
free_kib() { df -Pk /home/user | awk 'NR == 2 {print $4}'; }

[[ -x "$interpreter" && "$(git -C "$mirror" rev-parse refs/heads/trial)" == "$sha" ]]
[[ "$(git -C "$mirror" rev-parse refs/heads/retained-base)" == "$base_runtime" ]]
[[ "$(git -C "$mirror" rev-parse "$sha^{tree}")" == "$(jq -er .tree "$prep/approved-input.json")" ]]
[[ "$(jq -er .retained_runtime "$prep/approved-input.json")" == "$base_runtime" ]]
jq -e --arg runtime "$base_runtime" '.release==14 and .runtime.sha==$runtime and .agent.sha=="5e301956dc49c8b9ba4d23a7ce96c6564bd74d2f"' \
  "$program/versions/4b62ab1a6521/manifest.json" >/dev/null
[[ "$(git -C "$app" rev-parse HEAD)" == 148eaf381e3f02dc0f0d5dfc61e61ebf37dbc715 ]]
[[ "$(git -C "$tooling" rev-parse HEAD)" == "$(jq -er .browser_tooling "$prep/approved-input.json")" ]]
[[ "$(git -C "$trace_tools" rev-parse HEAD)" == "$(jq -er .trace_helpers "$prep/approved-input.json")" ]]
[[ -z "$(git -C "$tooling" status --porcelain -- scripts/save-loop)" ]]
[[ -z "$(git -C "$trace_tools" status --porcelain -- scripts/save-loop)" ]]
[[ ! -e "$out" && ! -L "$out" && $(free_kib) -ge $minimum_kib ]]
[[ -d "$owner/.locks" && ! -L "$owner/.locks" && ! -L "$owner/.locks/one-root.lock" ]]
exec 9>"$owner/.locks/one-root.lock"
flock -n 9
[[ ! -e "$owner/.quick-operation-lock" && ! -L "$owner/.quick-operation-lock" ]]
python3 "$verify" ports-closed
[[ ! -e "$support/discovery.json" && ! -L "$support/discovery.json" ]]
mkdir -m 700 "$out"
mkdir -m 700 -p "$archive" "$launcher_cwd"

export PATH="/opt/node22/bin:$PATH"
export ASTRID_NODE_EXECUTABLE="$work/run/toolchain/node-v20.19.4-linux-x64/bin/node"
owned=(env HOME="$root/home" TMPDIR="$root/tmp" XDG_DATA_HOME="$root/home/.local/share"
  XDG_STATE_HOME="$root/home/.local/state" XDG_CACHE_HOME="$root/home/.cache" XDG_CONFIG_HOME="$root/home/.config")
overlaid=("${owned[@]}" ASTRID_RUNTIME_TIMELINE_DIAGNOSTICS=1
  ASTRID_TIMELINE_MEMO_TRACE="$trace_path" PYTHONPATH="$prep/overlay-guard:$archive" PYTHONDONTWRITEBYTECODE=1
  SV2A_ARCHIVE="$archive" SV2A_RUNTIME_SHA="$sha" SV2A_SUPPORT_ROOT="$support" SV2A_REALM_ID="$realm"
  SV2A_SOURCE_PROFILE="$source_profile" SV2A_DAEMON_WITNESS="$out/candidate-daemon-module.json")

watcher=''
active=''
preview=''
browser_temp=''
launch_attempted=0
published=0
program_checked=0
log_offset=0
log_identity=''

stop_group() {
  local leader="$1" process_group
  [[ -n "$leader" ]] || return 0
  process_group=$(ps -o pgid= -p "$leader" | tr -d ' ') || return 0
  if [[ "$process_group" == "$leader" ]]; then
    kill -TERM -- "-$leader" 2>/dev/null || true
  fi
}

cleanup() {
  local result=$? down_ok=1 profile_removed=1
  trap - EXIT
  trap '' INT TERM
  if [[ -n "$active" ]]; then stop_group "$active"; wait "$active" || true; fi
  if [[ -n "$preview" ]]; then stop_group "$preview"; wait "$preview" || true; fi
  if (( launch_attempted )); then
    (cd "$launcher_cwd" && "${overlaid[@]}" ASTRID_RUNTIME_DOOR_PORT=17501 "$interpreter" -I -B "$prep/overlay-direct.py" down \
      --profile astrid --data-root "$data" --source-manifest "$source_profile" --door-port 17501 --json) \
      >"$out/down.json" 2>"$out/down.stderr" || down_ok=0
    jq -e '.status=="stopped" and .idle.safe==true' "$out/down.json" >/dev/null || down_ok=0
  fi
  if [[ -n "$browser_temp" ]]; then rmdir -- "$browser_temp" || profile_removed=0; fi
  if (( program_checked )); then
    python3 "$verify" inventory "$program" "$interpreter" "$out/program.after.sha256" || result=1
    cmp -s "$out/program.before.sha256" "$out/program.after.sha256" || result=1
  fi
  if (( published )); then
    python3 "$verify" postflight "$support" "$realm" "$archive" "$out" || result=1
  else
    python3 "$verify" ports-closed || result=1
    if [[ -f "$out/original-source-profile.json" ]]; then
      cmp -s "$out/original-source-profile.json" "$support/source-profiles/astrid.json" || result=1
      cmp -s "$out/original-catalog.json" "$support/catalog.json" || result=1
    fi
  fi
  if [[ -n "$log_identity" && -f "$runtime_log" && ! -L "$runtime_log" ]]; then
    if [[ "$(stat -c '%d:%i' "$runtime_log")" == "$log_identity" ]] && (( $(stat -c %s "$runtime_log") >= log_offset )); then
      tail -c "+$((log_offset + 1))" "$runtime_log" >"$out/runtime-log-delta.txt" || result=1
    else
      cp -- "$runtime_log" "$out/runtime-log-rotated.txt" || result=1
      result=1
    fi
  fi
  if [[ -n "$watcher" ]]; then kill "$watcher" 2>/dev/null || true; wait "$watcher" || true; fi
  printf '%s\t%s\n' "$(date -u +%FT%T.%NZ)" "$(free_kib)" >>"$out/free-kib.tsv"
  (( down_ok && profile_removed )) || result=1
  jq -n --argjson rc "$result" --argjson stopped "$down_ok" --argjson profile_removed "$profile_removed" \
    '{exit_code:$rc,idle_safe_stop_verified:($stopped==1),browser_temp_removed:($profile_removed==1)}' >"$out/cleanup.json"
  (cd "$out" && find . -maxdepth 1 -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum --) >"$out/SHA256SUMS"
  exit "$result"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

printf 'utc\tavailable_kib\n' >"$out/free-kib.tsv"
(
  while kill -0 "$owner_shell" 2>/dev/null; do
    available=$(free_kib)
    printf '%s\t%s\n' "$(date -u +%FT%T.%NZ)" "$available" >>"$out/free-kib.tsv"
    if (( available < minimum_kib )); then
      printf 'stopped below 16 GiB at %s KiB\n' "$available" >"$out/disk-stop.txt"
      kill -TERM "$owner_shell"
      exit 0
    fi
    sleep 0.5
  done
) &
watcher=$!

# Packaging, dependency and wire inputs must be byte-matched before any launch.
lock_inputs=(pyproject.toml setup.py setup.cfg uv.lock packages/python/pyproject.toml packages/python/setup.py
  packages/python/setup.cfg contract ':(glob)**/*requirements*' ':(glob)**/*.lock' ':(glob)**/constraints*.txt')
printf '%s\n' "${lock_inputs[@]}" >"$out/dependency-pathspecs.txt"
git -C "$mirror" diff --exit-code "$base_runtime" "$sha" -- "${lock_inputs[@]}" >"$out/dependency-and-contract.diff"
printf '%s\n%s\n' "$base_runtime" "$sha" >"$out/dependency-compared-shas.txt"
git -C "$mirror" archive --format=tar "$sha" | tar -xf - -C "$archive"
python3 "$verify" archive "$mirror" "$sha" "$archive" "$out"
python3 "$verify" inventory "$program" "$interpreter" "$out/program.before.sha256"
program_checked=1
python3 "$verify" prepare "$support" "$realm" "$archive" "$out"
cp -- "$prior/fixture.json" "$out/fixture.json"
cp -- "$prep/package.sha256" "$out/script-package.sha256"
jq --arg runtime "$sha" '.runtime=$runtime' "$prior/versions.json" >"$out/versions.json"
(cd "$app/dist" && find . -type f -print0 | sort -z | xargs -0 sha256sum --) >"$out/dist-files.sha256"
cmp "$out/dist-files.sha256" "$prior/dist-files.sha256"
[[ -f "$runtime_log" && ! -L "$runtime_log" ]]
log_offset=$(stat -c %s "$runtime_log")
log_identity=$(stat -c '%d:%i' "$runtime_log")

launch_attempted=1
(
  cd "$launcher_cwd"
  exec setsid --wait "${overlaid[@]}" ASTRID_RUNTIME_ADMISSION_TIMEOUT_SECONDS=600 ASTRID_RUNTIME_DOOR_PORT=17501 \
    "$interpreter" -I -B "$prep/overlay-direct.py" up --profile astrid --data-root "$data" \
    --source-manifest "$source_profile" --door-port 17501 --wait --json
) >"$out/up.json" 2>"$out/up.stderr" &
active=$!
wait "$active"
active=''
jq -e --arg sha "$sha" '.ok==true and .runtime_sha==$sha' "$out/up.json" >/dev/null
published=1
python3 "$verify" preflight "$support" "$realm" "$archive" "$interpreter" "$out"
instance=$(jq -er .instance "$out/browser-preflight.json")

(
  cd "$app"
  exec setsid --wait "${owned[@]}" ASTRID_RUNTIME_PYTHON="$interpreter" ASTRID_RUNTIME_SOURCE_MANIFEST="$source_profile" \
    PYTHONDONTWRITEBYTECODE=1 PORT=2400 VITE_ASTRID_DYNAMIC_PROXY_PORT=17500 ASTRID_APP_LOOPBACK_ORIGIN=off \
    node scripts/dev-local-workspace.mjs --data-root "$data" --preview --preview-dir "$app/dist"
) >"$out/preview.log" 2>&1 &
preview=$!
for ((poll=0; poll<120; poll++)); do
  kill -0 "$preview"
  if curl -fsS --max-time 2 'http://127.0.0.1:2400/api/runtime/v1/health' 2>/dev/null |
      jq -e --arg id "$instance" '.status=="ok" and .protocol=="workspace.v1" and .runtime_instance_id==$id' >/dev/null; then
    break
  fi
  sleep 1
done
(( poll < 120 ))

browser_temp=$(mktemp -d /tmp/sl-p77-r7-XXXXXX)
setsid --wait "${owned[@]}" TMPDIR=/tmp P77_R7_BROWSER_TMP="$browser_temp" LIBGL_ALWAYS_SOFTWARE=1 \
  P77_SV2A_TRACE_PATH="$trace_path" P77_SV2A_TRACE_TOOLS="$trace_tools" \
  SAVE_LOOP_CHROME=/usr/bin/google-chrome SAVE_LOOP_PLAYWRIGHT=/opt/node-tools/node_modules/playwright/index.mjs \
  node "$prep/browser-sv2a-first-save.mjs" "$root" "$data" "$out/fixture.json" "$out/versions.json" \
  "$app/dist" "$out/dist-files.sha256" "$tooling" "$out" candidate "$out/browser-preflight.json" \
  >"$out/browser.log" 2>&1 &
active=$!
wait "$active"
active=''
jq -e '.phase=="verified" and .timeline_commit_posts==1 and .profile_removed and .trace_witness.http_status==200' "$out/browser-sv2a-first-save.json" >/dev/null
[[ -f "$trace_path" && ! -L "$trace_path" ]]
