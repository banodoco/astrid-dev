#!/usr/bin/env bash
# SV-3 measurement package on a COPY of the retained sandbox data. Static-checked only in this change.
#   SV3_SIGNED_BACKUP=<canonical signed backup dir> SV3_RUNTIME_REF=<ref in the candidate mirror> \
#     bash run-sv3-overlay.sh <candidate Runtime SHA> <approved package.sha256 digest>
# Optional: SV3_REPETITIONS (default 3), SV3_STATIC_DRY_RUN=1 (reads the package files only).
# SV3_TRACE=1 is refused: the trace witness and trace verdict of SV-2a are not ported.
set -Eeuo pipefail
umask 077

work=/home/user/codex-run
evidence="$work/run/evidence/plan-77/round7-acceptance"
prep=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
sha="${1:?approved exact candidate Runtime SHA}"
approved_package="${2:?approved SHA-256 of package.sha256}"
ref="${SV3_RUNTIME_REF:?git ref in the candidate mirror that must resolve to the Runtime SHA}"
[[ $# == 2 && "$sha" =~ ^[a-f0-9]{40}$ && "$approved_package" =~ ^[a-f0-9]{64}$ ]]
[[ "$ref" =~ ^[A-Za-z0-9._/-]+$ && "$ref" != -* ]]
[[ "${SV3_TRACE:-0}" == 0 ]] || { echo 'SV3_TRACE=1 is not supported by this package. Nothing was started.' >&2; exit 2; }
[[ "$(sha256sum "$prep/package.sha256" | cut -d' ' -f1)" == "$approved_package" ]]
(cd "$prep" && sha256sum -c package.sha256)
[[ "$(jq -er .runtime_fixed_by_argument "$prep/approved-input.json")" == true ]]
if [[ "${SV3_STATIC_DRY_RUN:-0}" == 1 ]]; then
  jq '{retained_runtime, retained_generation, browser_tooling, trace_schema, old_public_head}' "$prep/approved-input.json"
  printf '%s\n' 'Static dry run. Only the package hashes and fixed inputs were read.'
  exit 0
fi

# Prior SV-2a-era two-save receipts: the retained stack and its fixture, versions and dist inventory come from here.
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
# The original data is only READ. Every mutable step runs on a copy named under $out.
orig_data="$root/direct-data"
orig_support="$orig_data/runtime"
program="$root/program"
interpreter="$program/versions/4b62ab1a6521/py/bin/python"
base_runtime=77c38d037f98f744bd8f41c15d95429c124a8003
app="$work/wt/astrid-app-p77-r7-firstcut-requalification-install"
tooling="$work/wt/astrid-app-p77-quick-indicator"
mirror="$evidence/sv2a-prep/candidate-runtime.git"
out="$evidence/sv3-measure-$sha"
archive="$out/source/$sha"
launcher_cwd="$out/launcher-cwd"
verify="$prep/verify-overlay.py"
runtime_log="$root/home/.local/state/astrid-runtime/logs/runtime.log"
pack_log="$root/home/.local/state/astrid-runtime/logs/service-pack-host.log"
pristine="$out/pristine-data"
owner_shell=$BASHPID
minimum_kib=$((16 * 1024 * 1024))
reps=${SV3_REPETITIONS:-3}
[[ "$reps" =~ ^[1-9]$ ]]
free_kib() { df -Pk /home/user | awk 'NR == 2 {print $4}'; }

# Candidate identity: the ref must resolve to the approved SHA, the tree is recorded, the dependency and contract
# diff against the retained Runtime must be empty. The commit SHA fixes the tree, so the approval covers it.
[[ "$(git -C "$mirror" rev-parse --verify --quiet "$ref^{commit}")" == "$sha" ]]
[[ "$(git -C "$mirror" rev-parse refs/heads/retained-base)" == "$base_runtime" ]]
[[ "$(jq -er .retained_runtime "$prep/approved-input.json")" == "$base_runtime" ]]
jq -e --arg runtime "$base_runtime" '.release==14 and .runtime.sha==$runtime and .agent.sha=="5e301956dc49c8b9ba4d23a7ce96c6564bd74d2f"' \
  "$program/versions/4b62ab1a6521/manifest.json" >/dev/null
[[ -x "$interpreter" ]]
[[ "$(git -C "$app" rev-parse HEAD)" == 148eaf381e3f02dc0f0d5dfc61e61ebf37dbc715 ]]
[[ "$(git -C "$tooling" rev-parse HEAD)" == "$(jq -er .browser_tooling "$prep/approved-input.json")" ]]
[[ -z "$(git -C "$tooling" status --porcelain -- scripts/save-loop)" ]]
[[ ! -e "$out" && ! -L "$out" ]]
# The signed backup is not recorded in the package, so the operator names its canonical directory.
backup="${SV3_SIGNED_BACKUP:-}"
if [[ -z "$backup" || ! -d "$backup" || -L "$backup" || "$(realpath "$backup")" != "$backup" \
    || "$backup/" == "$orig_data/"* || "$backup/" == "$out/"* ]]; then
  printf '%s\n' 'Set SV3_SIGNED_BACKUP to the canonical signed backup directory. Nothing was started.' >&2
  exit 2
fi
[[ -d "$owner/.locks" && ! -L "$owner/.locks" && ! -L "$owner/.locks/one-root.lock" ]]
# The next line opens the lock for writing and creates or truncates it; its stat is kept for the boundary receipt.
lock_before=$(stat -c '%s %Y' "$owner/.locks/one-root.lock" 2>/dev/null || echo absent)
exec 9>"$owner/.locks/one-root.lock"
flock -n 9
[[ ! -e "$owner/.quick-operation-lock" && ! -L "$owner/.quick-operation-lock" ]]
python3 "$verify" ports-closed
[[ ! -e "$orig_support/discovery.json" && ! -L "$orig_support/discovery.json" ]]
mkdir -m 700 "$out"
mkdir -m 700 -p "$archive" "$launcher_cwd"

export PATH="/opt/node22/bin:$PATH"
export ASTRID_NODE_EXECUTABLE="$work/run/toolchain/node-v20.19.4-linux-x64/bin/node"
owned=(env HOME="$root/home" TMPDIR="$root/tmp" XDG_DATA_HOME="$root/home/.local/share"
  XDG_STATE_HOME="$root/home/.local/state" XDG_CACHE_HOME="$root/home/.cache" XDG_CONFIG_HOME="$root/home/.config")

# Per-repetition state, read by the cleanup trap. Every name is set before any use.
watcher=''
active=''
preview=''
browser_temp=''
rep_n=0
rep_dir=''
rep_work=''
rep_copy_made=0
rep_launch=0
rep_running=0
rep_published=0
rep_down_ok=0
rep_mark_pack=''
rep_mark_runtime=''
rep_logs_captured=0
rep_env=()
program_checked=0
boundary_checked=0
copy_kib=0

# Stat inventories of the signed backup and the owner, data and stack boundaries. Directories listed one level
# deep carry no size or time, so only the entries themselves are compared, not what the Runtime may write inside.
boundary_listing() {
  { find "$1" -mindepth 1 -maxdepth 1 -type f -printf 'f %P %s %T@ %m %U:%G\n'
    find "$1" -mindepth 1 -maxdepth 1 ! -type f -printf '%y %P %m %U:%G\n'; } | LC_ALL=C sort
}
boundary_snapshot() {
  find "$backup" -printf '%y %P %s %T@ %m %U:%G %i\n' | LC_ALL=C sort >"$out/boundary-backup.$1.txt"
  boundary_listing "$owner" >"$out/boundary-owner.$1.txt"
  boundary_listing "$owner/.locks" | awk '$2 != "one-root.lock"' >"$out/boundary-owner-locks.$1.txt"
  boundary_listing "$root" >"$out/boundary-root.$1.txt"
  boundary_listing "$orig_data" >"$out/boundary-data.$1.txt"
}

# Stop one PID this script started: TERM, a 10 second grace period, then KILL, and reap it. Nothing else is signalled.
stop_pid() {
  local pid="$1" watchdog
  [[ "$pid" =~ ^[0-9]+$ ]] && (( pid > 1 )) || return 0
  kill -TERM -- "$pid" 2>/dev/null || true
  ( sleep 10; kill -KILL -- "$pid" 2>/dev/null || true ) &
  watchdog=$!
  wait "$pid" 2>/dev/null || true
  kill "$watchdog" 2>/dev/null || true
  wait "$watchdog" 2>/dev/null || true
}

# Log byte delta, same technique as the SV-2a script: a mark is "device:inode size" taken before the repetition's up.
log_mark() {
  if [[ -f "$1" && ! -L "$1" ]]; then printf '%s %s\n' "$(stat -c '%d:%i' "$1")" "$(stat -c %s "$1")"; else printf 'absent 0\n'; fi
}
log_delta() { # file mark out
  local id off
  read -r id off <<<"$2"
  if [[ ! -f "$1" || -L "$1" ]]; then : >"$3"; return 0; fi
  if [[ "$id" == absent ]]; then cp -- "$1" "$3"; return 0; fi
  if [[ "$(stat -c '%d:%i' "$1")" == "$id" ]] && (( $(stat -c %s "$1") >= off )); then
    tail -c "+$((off + 1))" "$1" >"$3"
  else
    cp -- "$1" "$3.rotated"
    return 1
  fi
}

# Pack host receipts. The script does not start, stop or alter the pack host. It records what the install did.
pack_host_receipt() { # repetition directory
  local delta="$1/service-pack-host-delta.txt" growth claim count status
  growth=$(stat -c %s "$delta" 2>/dev/null || echo 0)
  claim=$(grep -c 'claim' "$delta" || true)
  count=$(pgrep -fa 'pack' 2>/dev/null | grep -c 'host' || true)
  if (( growth == 0 )); then status='pack host not polling'; else status='pack host log grew during the repetition'; fi
  jq -n --argjson growth "$growth" --argjson claim "${claim:-0}" --argjson count "${count:-0}" --arg status "$status" \
    '{status:$status, log_growth_bytes:$growth, claim_lines:$claim, pgrep_pack_host_count:$count,
      note:"counts only; no group or owner assertion"}' >"$1/pack-host.json"
}

# Agent authoring commit (the installed Agent CLI against the same running Runtime). Not established from the files
# read for this package: the interpreter working directory, how the Runtime door is found and the receipt field name.
# TODO (not established): confirm the python entry (retained program versions/4b62ab1a6521 interpreter or the
# installed Agent), the working directory, the door discovery for the copied data root, and the receipt id key.
agent_commit() { # repetition directory
  printf '%s\n' 'agent-commit: not established' >"$1/agent-commit.txt"
}

# Down is idle-safe and retried three times. The original data is never a target here: only the copy.
down_rep() { # repetition directory
  local attempt
  rep_down_ok=0
  for attempt in 1 2 3; do
    # The down receipt of each attempt is kept. The loop stops at the first idle-safe stop.
    if (cd "$launcher_cwd" && "${rep_env[@]}" ASTRID_RUNTIME_DOOR_PORT=17501 "$interpreter" -I -B "$prep/overlay-direct.py" down \
        --profile astrid --data-root "$rep_work" --source-manifest "$1/candidate-source-profile.json" --door-port 17501 --json) \
        >"$1/down.$attempt.json" 2>"$1/down.$attempt.stderr" &&
        jq -e '.status=="stopped" and .idle.safe==true' "$1/down.$attempt.json" >/dev/null; then
      rep_down_ok=1
      break
    fi
    (( attempt == 3 )) || sleep 15
  done
  cp -- "$1/down.$attempt.json" "$1/down.json" || true
  cp -- "$1/down.$attempt.stderr" "$1/down.stderr" || true
}

scan_receipts() {
  local names=(email token_like bearer secret_field key_field codex_path private_key) index
  local patterns=('[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}' '(sk|ghp|gho|xox[bap]|AKIA)[-_A-Za-z0-9]{16,}'
    'Bearer[[:space:]]+[A-Za-z0-9._~+/=-]{8,}'
    '(api[_-]?key|secret|password|passwd|token|authorization|cookie)"?[[:space:]]*[:=]' 'key_id|manifest_hmac'
    '[.]codex' '-----BEGIN [A-Z ]*PRIVATE KEY')
  printf 'pattern\tfile\n' >"$out/privacy-scan.tsv"
  for index in "${!names[@]}"; do
    { grep -rIlEi --exclude-dir=source --exclude-dir=launcher-cwd --exclude-dir='work-data-*' --exclude-dir=pristine-data \
        --exclude=privacy-scan.tsv -e "${patterns[index]}" "$out" || true; } |
      awk -v name="${names[index]}" '{print name "\t" $0}' >>"$out/privacy-scan.tsv"
  done
}

# Combined measurements and summary, built from the per-repetition driver receipts with jq.
combine_outputs() {
  local n
  : >"$out/measurements.jsonl"
  for ((n = 1; n <= reps; n++)); do
    jq -c --argjson rep "$n" '
      {repetition:$rep, scenario:"S0", warm:false, page_ready_ms:.s0.navigation_to_writable_ms,
       verified_head_status:(.s0.verified_head.status), refusal:(.s0.refusal)},
      (.scenarios[] as $s | $s.drags[] | {repetition:$rep, scenario:$s.name, warm:$s.warm, index:.index,
        release_to_post_ms, post_to_200_ms, response_to_saved_ms, http_status, post_count_network})' \
      "$out/rep-$n/browser-sv3-measure.json" >>"$out/measurements.jsonl"
  done
  jq -rs '
    def med: sort as $a | ($a|length) as $l | if $l==0 then null elif $l % 2 == 1 then $a[($l/2)|floor]
             else (($a[$l/2-1] + $a[$l/2]) / 2) end;
    def mx: if length==0 then null else max end;
    def row(name; rep; xs): [name, rep, (xs|length), (xs|map(.release_to_post_ms)|med), (xs|map(.post_to_200_ms)|med),
      (xs|map(.response_to_saved_ms)|med), (xs|map(select(.http_status!=200))|length)];
    ([ "scenario","repetition","n_posts","release_to_post_ms","post_to_200_ms","200_to_saved_ms","refusals" ] | @tsv),
    ([ .[] | select(.scenario!="S0") ] | group_by([.scenario, .repetition])[] | row(.[0].scenario; .[0].repetition; .)  | @tsv),
    ([ .[] | select(.scenario!="S0" and .scenario!="cold" and .warm) ] | group_by(.scenario)[] |
      [.[0].scenario, "warm-median", length,
        (map(.release_to_post_ms)|med), (map(.post_to_200_ms)|med), (map(.response_to_saved_ms)|med),
        (map(select(.http_status!=200))|length)] | @tsv),
    ([ .[] | select(.scenario!="S0" and .scenario!="cold" and .warm) ] | group_by(.scenario)[] |
      [.[0].scenario, "warm-max", length, (map(.release_to_post_ms)|mx), (map(.post_to_200_ms)|mx),
        (map(.response_to_saved_ms)|mx), (map(select(.http_status!=200))|length)] | @tsv),
    ([ .[] | select(.scenario=="cold") ] | if length==0 then empty else
      ["cold", "all", length, (map(.release_to_post_ms)|med), (map(.post_to_200_ms)|med),
       (map(.response_to_saved_ms)|med), (map(select(.http_status!=200))|length)] | @tsv end),
    ([ .[] | select(.scenario=="S0") | ["S0", .repetition, 0, null, null, null, (if .refusal then 1 else 0 end),
       ("page_ready_ms=" + ((.page_ready_ms // null)|tostring))] | @tsv ] | .[])
  ' "$out/measurements.jsonl" >"$out/summary.tsv"
}

cleanup() {
  local result=$? down_ok=1 profile_removed=1 preview_clean=1 chrome_clean=1 boundary_unchanged=1
  local part differing='' lock_after rep_json_ok=0
  trap - EXIT
  trap '' INT TERM
  if [[ -n "$active" ]]; then stop_pid "$active" || true; active=''; fi
  if [[ -n "$preview" ]]; then
    stop_pid "$preview"
    python3 "$verify" stop-preview-listeners || true
    python3 "$verify" preview-after "${rep_dir:-$out}" || true
    preview=''
  fi
  if (( rep_running )); then
    down_rep "$rep_dir" || true
    (( rep_down_ok )) || down_ok=0
    (( rep_down_ok )) && rep_running=0
  fi
  if [[ -n "$browser_temp" ]]; then
    if pgrep -f -- "--user-data-dir=$browser_temp/" >/dev/null; then
      chrome_clean=0
      pgrep -fa -- "--user-data-dir=$browser_temp/" >"$out/chrome-residue.txt" || true
    fi
    rmdir -- "$browser_temp" || profile_removed=0
  fi
  if (( program_checked )); then
    python3 "$verify" inventory "$program" "$interpreter" "$out/program.after.sha256" || result=1
    cmp -s "$out/program.before.sha256" "$out/program.after.sha256" || result=1
  fi
  if [[ -n "$rep_dir" && -f "$rep_dir/candidate-daemon-module.json" ]]; then
    python3 "$verify" owner-exited "$rep_dir" || result=1
  fi
  if [[ -n "$rep_dir" && $rep_logs_captured == 0 && -n "$rep_mark_runtime" ]]; then
    log_delta "$runtime_log" "$rep_mark_runtime" "$rep_dir/runtime-log-delta.txt" || result=1
    log_delta "$pack_log" "$rep_mark_pack" "$rep_dir/service-pack-host-delta.txt" || true
    pack_host_receipt "$rep_dir" || true
  fi
  if [[ -n "$rep_dir" && -f "$rep_dir/original-catalog.json" ]]; then
    cmp -s "$rep_dir/original-catalog.json" "$orig_support/catalog.json" || result=1
  fi
  if (( boundary_checked )); then
    boundary_snapshot after || boundary_unchanged=0
    for part in backup owner owner-locks root data; do
      case "$part" in
        root|data)
          # The Runtime may legitimately create NEW top-level entries. Fail only if a pre-existing entry is missing or
          # changed; new entries are recorded, not failed.
          changed=$(LC_ALL=C comm -23 "$out/boundary-$part.before.txt" "$out/boundary-$part.after.txt")
          LC_ALL=C comm -13 "$out/boundary-$part.before.txt" "$out/boundary-$part.after.txt" >"$out/boundary-$part.new-entries.txt" || true
          ;;
        *)
          if cmp -s "$out/boundary-$part.before.txt" "$out/boundary-$part.after.txt"; then changed=''; else changed=different; fi
          ;;
      esac
      if [[ -n "$changed" ]]; then
        boundary_unchanged=0
        differing+="$part "
        diff -- "$out/boundary-$part.before.txt" "$out/boundary-$part.after.txt" >"$out/boundary-$part.diff" || true
      fi
    done
    lock_after=$(stat -c '%s %Y' "$owner/.locks/one-root.lock" 2>/dev/null || echo absent)
    jq -n --argjson unchanged "$boundary_unchanged" --arg differing "$differing" --arg backup "$backup" \
      --arg lock_before "$lock_before" --arg lock_after "$lock_after" \
      '{signed_backup_path:$backup, boundaries_unchanged:($unchanged==1), differing:$differing,
        one_root_lock:{opened_for_write_by_exec:true, size_and_mtime_before:$lock_before, size_and_mtime_after:$lock_after}}' \
      >"$out/boundary.json" || boundary_unchanged=0
  fi
  # A work copy is removed only when no Runtime was launched on it or its stack stopped idle-safe. Otherwise it is kept
  # as evidence and the run fails.
  if (( rep_copy_made )) && [[ -n "$rep_work" && "$rep_work" == "$out/work-data-"* && -d "$rep_work" ]]; then
    if (( ! rep_launch || rep_down_ok )); then rm -rf -- "$rep_work" || result=1; else result=1; fi
  fi
  if [[ -d "$pristine" && "$pristine" == "$out/pristine-data" ]]; then rm -rf -- "$pristine" || result=1; fi
  if [[ -n "$watcher" ]]; then kill "$watcher" 2>/dev/null || true; wait "$watcher" || true; fi
  printf '%s\t%s\n' "$(date -u +%FT%T.%NZ)" "$(free_kib)" >>"$out/free-kib.tsv"
  (( down_ok && profile_removed && preview_clean && chrome_clean && boundary_unchanged )) || result=1
  scan_receipts || true
  jq -n --argjson rc "$result" --argjson stopped "$down_ok" --argjson profile_removed "$profile_removed" \
    --argjson preview_clean "$preview_clean" --argjson chrome_clean "$chrome_clean" \
    --argjson boundary_unchanged "$boundary_unchanged" \
    '{exit_code:$rc, idle_safe_stop_verified:($stopped==1), browser_temp_removed:($profile_removed==1),
      preview_ports_closed:($preview_clean==1), no_leftover_chrome:($chrome_clean==1),
      boundaries_unchanged:($boundary_unchanged==1)}' >"$out/cleanup.json"
  (cd "$out" && find . -type f ! -name SHA256SUMS ! -path './source/*' ! -path './launcher-cwd/*' \
    ! -path './pristine-data/*' ! -path './work-data-*/*' -print0 | sort -z | xargs -0 sha256sum --) >"$out/SHA256SUMS" || true
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

# Packaging, dependency and wire inputs must be byte-matched before any launch (the source's own pathspecs).
lock_inputs=(pyproject.toml setup.py setup.cfg uv.lock packages/python/pyproject.toml packages/python/setup.py
  packages/python/setup.cfg contract ':(glob)**/*requirements*' ':(glob)**/*.lock' ':(glob)**/constraints*.txt')
printf '%s\n' "${lock_inputs[@]}" >"$out/dependency-pathspecs.txt"
git -C "$mirror" diff --exit-code "$base_runtime" "$sha" -- "${lock_inputs[@]}" >"$out/dependency-and-contract.diff"
printf '%s\n%s\n' "$base_runtime" "$sha" >"$out/dependency-compared-shas.txt"
git -C "$mirror" rev-parse "$sha^{tree}" >"$out/candidate-tree.txt"
git -C "$mirror" archive --format=tar "$sha" | tar -xf - -C "$archive"
python3 "$verify" archive "$mirror" "$sha" "$archive" "$out"
python3 "$verify" inventory "$program" "$interpreter" "$out/program.before.sha256"
program_checked=1
boundary_snapshot before
boundary_checked=1
cp -- "$prep/package.sha256" "$out/script-package.sha256"
jq --arg runtime "$sha" '.runtime=$runtime' "$prior/versions.json" >"$out/versions.json"
(cd "$app/dist" && find . -type f -print0 | sort -z | xargs -0 sha256sum --) >"$out/dist-files.sha256"
cmp "$out/dist-files.sha256" "$prior/dist-files.sha256"

# Pristine copy of the original data. The original is only read. The check is 16 GiB free after the copy.
copy_kib=$(du -sk -- "$orig_data" | cut -f1)
(( $(free_kib) - copy_kib >= minimum_kib )) || { echo 'free space below 16 GiB before the pristine copy' >&2; exit 1; }
cp -a -- "$orig_data" "$pristine"
[[ ! -e "$pristine/runtime/discovery.json" ]]

# Shared setup for one repetition. rep_env is the owned stack environment plus the overlay variables for this rep.
# Each repetition runs on its own copy: rep_work is "$out/work-data-<n>" and rep_dir is "$out/rep-<n>".
run_repetition() {
  local n=$1 wsupport wrealm instance attempt poll src_profile
  rep_n=$n
  rep_dir="$out/rep-$n"
  rep_work="$out/work-data-$n"
  wsupport="$rep_work/runtime"
  wrealm="$wsupport/realms/$realm"
  src_profile="$rep_dir/candidate-source-profile.json"
  mkdir -m 700 "$rep_dir"
  (( $(free_kib) - copy_kib >= minimum_kib )) || { echo 'free space below 16 GiB before the work copy' >&2; return 1; }
  rep_copy_made=1
  cp -a -- "$pristine" "$rep_work"
  [[ ! -e "$wsupport/discovery.json" && ! -L "$wsupport/discovery.json" ]]
  # Rebase the COPIED catalog and profile from the original data root (their data_root paths are absolute). See README.
  python3 "$verify" prepare "$orig_support" "$wsupport" "$realm" "$archive" "$rep_dir"
  cp -- "$prior/fixture.json" "$rep_dir/fixture.json"
  jq --arg runtime "$sha" '.runtime=$runtime' "$prior/versions.json" >"$rep_dir/versions.json"
  cp -- "$prep/package.sha256" "$rep_dir/script-package.sha256"
  rep_env=("${owned[@]}"
    PYTHONPATH="$prep/overlay-guard:$archive" PYTHONDONTWRITEBYTECODE=1
    SV3_ARCHIVE="$archive" SV3_RUNTIME_SHA="$sha" SV3_SUPPORT_ROOT="$wsupport" SV3_REALM_ID="$realm"
    SV3_SOURCE_PROFILE="$src_profile" SV3_DAEMON_WITNESS="$rep_dir/candidate-daemon-module.json")
  rep_mark_pack=$(log_mark "$pack_log")
  rep_mark_runtime=$(log_mark "$runtime_log")
  rep_logs_captured=0
  rep_launch=1
  rep_running=1
  (
    cd "$launcher_cwd"
    exec setsid --wait "${rep_env[@]}" ASTRID_RUNTIME_ADMISSION_TIMEOUT_SECONDS=600 ASTRID_RUNTIME_DOOR_PORT=17501 \
      "$interpreter" -I -B "$prep/overlay-direct.py" up --profile astrid --data-root "$rep_work" \
      --source-manifest "$src_profile" --door-port 17501 --wait --json
  ) >"$rep_dir/up.json" 2>"$rep_dir/up.stderr" &
  active=$!
  wait "$active"
  active=''
  jq -e --arg sha "$sha" '.ok==true and .runtime_sha==$sha' "$rep_dir/up.json" >/dev/null
  rep_published=1
  python3 "$verify" preflight "$wsupport" "$realm" "$archive" "$interpreter" "$rep_dir"
  instance=$(jq -er .instance "$rep_dir/browser-preflight.json")
  [[ -n "$instance" ]]

  (
    cd "$app"
    exec setsid --wait "${owned[@]}" ASTRID_RUNTIME_PYTHON="$interpreter" ASTRID_RUNTIME_SOURCE_MANIFEST="$src_profile" \
      PYTHONDONTWRITEBYTECODE=1 PORT=2400 VITE_ASTRID_DYNAMIC_PROXY_PORT=17500 ASTRID_APP_LOOPBACK_ORIGIN=off \
      node scripts/dev-local-workspace.mjs --data-root "$rep_work" --preview --preview-dir "$app/dist"
  ) >"$rep_dir/preview.log" 2>&1 &
  preview=$!
  for ((poll = 0; poll < 120; poll++)); do
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
    SAVE_LOOP_CHROME=/usr/bin/google-chrome SAVE_LOOP_PLAYWRIGHT=/opt/node-tools/node_modules/playwright/index.mjs \
    node "$prep/browser-sv3-measure.mjs" "$root" "$rep_work" "$rep_dir/fixture.json" "$rep_dir/versions.json" \
    "$app/dist" "$out/dist-files.sha256" "$tooling" "$rep_dir" candidate "$rep_dir/browser-preflight.json" \
    >"$rep_dir/browser.log" 2>&1 &
  active=$!
  wait "$active"
  active=''
  jq -e '.phase=="verified" and .timeline_commit_posts==19 and .profile_removed==true' \
    "$rep_dir/browser-sv3-measure.json" >/dev/null
  [[ -z "$(jq -r '.context_close_error // empty' "$rep_dir/browser-sv3-measure.json")" ]]
  # Chrome residue check on the disposable profile path. Only a count and the command lines are recorded; nothing is killed.
  rmdir -- "$browser_temp"
  if pgrep -f -- "--user-data-dir=$browser_temp/" >/dev/null; then
    pgrep -fa -- "--user-data-dir=$browser_temp/" >"$rep_dir/chrome-residue.txt" || true
    return 1
  fi
  browser_temp=''

  # Preview stop: TERM, KILL of the PID we started, then the port fallback. Ports 2400 and 17500 must be closed.
  stop_pid "$preview"
  preview=''
  python3 "$verify" stop-preview-listeners || true
  python3 "$verify" preview-after "$rep_dir"

  agent_commit "$rep_dir"

  down_rep "$rep_dir"
  (( rep_down_ok )) || return 1
  rep_running=0
  python3 "$verify" ports-closed
  python3 "$verify" owner-exited "$rep_dir"
  log_delta "$runtime_log" "$rep_mark_runtime" "$rep_dir/runtime-log-delta.txt"
  log_delta "$pack_log" "$rep_mark_pack" "$rep_dir/service-pack-host-delta.txt" || true
  pack_host_receipt "$rep_dir"
  rep_logs_captured=1
  # The original catalog and profile must be byte-identical to what was saved before the repetition.
  cmp -s "$rep_dir/original-catalog.json" "$orig_support/catalog.json"
  cmp -s "$rep_dir/original-source-profile.json" "$orig_support/source-profiles/astrid.json"
  rm -rf -- "$rep_work"
  rep_copy_made=0
}

for ((rep = 1; rep <= reps; rep++)); do
  run_repetition "$rep"
done
combine_outputs
