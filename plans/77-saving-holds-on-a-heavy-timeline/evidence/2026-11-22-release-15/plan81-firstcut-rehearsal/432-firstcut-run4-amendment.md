# Run 4 amendment — Plan 77 first-cut 432-clip read-back

The Lead approved this read-only installed recheck on 23 November 2026. The host gave the hour's notice at 04:03 UTC. The Lead's Codex manager may begin only after the host's explicit go at or after 05:03 UTC. This is the current reviewed pre-freeze tuple. The eventual ordered frozen release tuple and the second cut's new 1,000-edge fixture are separate.

Start with [the signed 432 runbook](https://github.com/banodoco/astrid-dev/blob/7443fd20c1e02790611190e9bdebb22c1b74fec5/plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-22-release-15/432-clip-readback-runbook.md). Keep the signed backup and proof restore unchanged. Use only a new installation, disposable working restore and first-cut receipts root. The last Round 5 adoption passed authenticated restore but refused during its final revision verification at 5m21s. The same copy passed an independent offline doctor in 4m46s. The narrower verified-head browser path needs healthy admission first. No second attempt or restart is implicit if the new adoption refuses.

## Disk and other load

The Lead observed 32 GiB free before the proposed run. Budget a **10 GiB additional peak**, leaving about **22 GiB free** at that estimate. This includes up to 5.5 GiB for the isolated installation and caches, 1.5 GiB for the scratch source mirrors, App dependencies and compiled output, about 2.7 GiB for up to three 917 MB-equivalent realm copies during restore, adoption and verification, and 0.3 GiB for logs, receipts and disposable profiles. The installer allowance comes from the local signed-stack setup, which added about 4–5 GiB before a complete heavy restore. The matching compiled App used 543 MiB of Node dependencies and 140 MiB of compiled bytes. The total is an estimate of new disk allocation. The existing fixture and proof are already included in the Lead’s observed free space.

The Lead’s approval for Run 4 authorizes these changes to the existing runbook's gates. Measure and record **25 GiB required immediately before install**, **12 GiB required immediately after the working restore**, and **10 GiB required before starting the compiled browser phase**. A free-space reading below the Lead's **5 GiB emergency floor** stops the run at any point. Each phase still has its own higher preflight. The 10 GiB additional peak estimate leaves about 22 GiB free from the Lead's observed 32 GiB. Stop at the first unmet stage check and retain partial receipts. Leave the source realm, signed backup, proof restore, installation and evidence on disk. Each fresh browser removes just its own disposable profile during normal cleanup. The Lead holds the machine free of other work from advance notice through the sample.

## Exact setup substitutions

This first block uses the exact clean clones, tooling checkout and pinned Node confirmed by the Lead. Use the established Chrome and Playwright installations for the browser observer. It belongs in the Lead's new Run 4 session. It only creates disposable source worktrees and generates pins. It does not touch a realm or start a process.

```bash
set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
BASE_APP=/root/codex/p77box/app
BASE_AGENT=/home/user/astrid-agent
BASE_RUNTIME=/home/user/astrid-runtime
TOOLS=/root/codex/p77box/round5-432-tools-wt
NODE20=/root/codex/p77box/node-v20.19.4-linux-x64/bin/node
RUN4="$BOX/run4"
STACK="$RUN4/stack"
RECEIPTS="$RUN4/receipts"
test ! -e "$RUN4" && test ! -L "$RUN4"
test "$(realpath -m "$RUN4")" = "$RUN4"
test -z "$(git -C "$TOOLS" status --porcelain)"
test "$(git -C "$TOOLS" rev-parse HEAD)" = 5b2c76a6a636d835700bc5f12b48848861dc30f5
test "$("$NODE20" --version)" = v20.19.4
mkdir -m 700 "$RUN4"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
PINS="$BOX/firstcut-432-reviewed-pins"
test ! -e "$PINS" && test ! -L "$PINS"
mkdir -m 700 "$PINS"
APP_SOURCE=846ce8cafdf8ca2e58a101a18242c9e50358f89c
AGENT_SOURCE=b7f0e96a4934ddb4c123eab791a6e18efb8f79ac
RUNTIME_SHA=77c38d037f98f744bd8f41c15d95429c124a8003
for input in "$BASE_APP" "$BASE_AGENT" "$BASE_RUNTIME"; do
  test "$(realpath "$input")" = "$input"
  test -z "$(git -C "$input" status --porcelain)"
  git -C "$input" fetch --no-tags origin refs/heads/release/15/fix-1491-verified-head
done
APP="$PINS/app"
AGENT="$PINS/agent"
git -C "$BASE_APP" worktree add --detach "$APP" "$APP_SOURCE"
git -C "$BASE_AGENT" worktree add --detach "$AGENT" "$AGENT_SOURCE"
git -C "$BASE_RUNTIME" cat-file -e "$RUNTIME_SHA^{commit}"
regen() {
  python3 "$AGENT/scripts/regenerate_runtime_pins.py" \
    --runtime-checkout "$BASE_RUNTIME" --runtime-sha "$RUNTIME_SHA" \
    --agent-sha "$1" --agent-checkout "$AGENT" --app-checkout "$APP" --apply
}
regen "$AGENT_SOURCE"
test "$(git -C "$AGENT" diff --name-only)" = $'astrid/resources/runtime.lock.json\nruntime.lock.json'
cmp "$AGENT/runtime.lock.json" "$AGENT/astrid/resources/runtime.lock.json"
jq -e --arg runtime "$RUNTIME_SHA" '.source_commit==$runtime' "$AGENT/runtime.lock.json" >/dev/null
git -C "$AGENT" add runtime.lock.json astrid/resources/runtime.lock.json
git -C "$AGENT" diff --cached --check
git -C "$AGENT" commit -m 'Pin exact Runtime for the 432-clip first-cut recheck'
AGENT_SHA=$(git -C "$AGENT" rev-parse HEAD)
regen "$AGENT_SHA"
test "$(git -C "$APP" diff --name-only)" = $'public/install-manifest.json\nruntime.lock.json'
jq -e --arg a "$AGENT_SHA" --arg r "$RUNTIME_SHA" \
  '.agent.sha==$a and .runtime.sha==$r and .runtime.schema_digest=="sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2"' \
  "$APP/public/install-manifest.json" >/dev/null
git -C "$APP" add public/install-manifest.json runtime.lock.json
git -C "$APP" diff --cached --check
git -C "$APP" commit -m 'Pin exact Agent and Runtime for the 432-clip first-cut recheck'
APP_SHA=$(git -C "$APP" rev-parse HEAD)
regen "$AGENT_SHA"
test -z "$(git -C "$AGENT" status --porcelain)"
test -z "$(git -C "$APP" status --porcelain)"
printf '%s\n' "$APP_SOURCE" "$AGENT_SOURCE" "$APP_SHA" "$AGENT_SHA" "$RUNTIME_SHA" >"$PINS/exact-tuple.txt"
```

Keep the generated `APP_SHA`, `AGENT_SHA`, `RUNTIME_SHA`, `APP`, `TOOLS`, `NODE20`, `STACK` and `RECEIPTS` values in the same shell. In section 1 of the signed runbook, omit the old Round 5 assignments for these values. Its unused-root checks, remaining paths, installer flags and environment isolation still apply. Build private exact-revision Agent and Runtime mirrors by section 7. The locally generated Agent pin is a child of the reviewed Agent source. Publish neither it nor the App pin. Verify the private manifest with the installer checker and save its inputs before install. The setup keeps the same verified Runtime schema digest.

## Run 4 space receipts

Define this helper before the install. Use the existing runbook section 1 to create the new `STACK` and `RECEIPTS` after its absence and ownership checks. Keep setup and output within those verified Run 4 paths.

```bash
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
```

| Place in the original runbook | Command at that point |
| --- | --- |
| Section 1, immediately before the isolated installer command | `run4_space before_install 25` |
| Section 2, once the fresh working restore and proof digest checks pass | `run4_space after_restore 12` |
| Section 5, before compiled build and preview | `run4_space before_browser 10` | For Run 4 omit the old section 2 and section 5 numeric 25 GiB preflights, using the new stage checks shown above. A 5 GiB emergency-floor breach during work stops the owned trial safely. It never triggers a retry. Preserve installer, stop and disk receipts.

Run sections 1–4 once each with their existing pinned source checks and approved 1800 s adoption budget. Stop on a final integrity refusal, an ambiguous catalog, or loss of process and file custody. Preserve exact receipts and the untouched proof digest. A final-claim timeout counts only as materialized if section 3's exact proof applies, and health still needs section 4.

If healthy, use the **compiled editor** part of section 5 before any SDK history read. Run its existing headless observer twice using the exact signed 432-clip inventory, with separate receipt files and two independently removed browser profiles. Record startup, cold browser and same-process reopen separately. Require the same process birth, selected realm, public revision/publication/digest, complete fixture identities, zero timeline commit POSTs, completion of the cold verified-head read before reopen, and local selection traffic. A first legitimate selection can make the first reopen replay once. No document edit is needed for this read-back. Then run section 6 once. Preserve phases if approval, restore, admission, compile, browser or public proof stops the run.

## Receipts and custody

The Lead's manager returns raw stage limits, install/restore/adopt results and wall clocks, the exact post-adoption discovery and health proof if reached, both browser receipts if reached, and the idle-safe stop and hash receipts. Keep the existing proof digest and original backup intact. The backup authentication key is never read, copied or hashed by this run. Do not print fields named `key_id` or `manifest_hmac`; omit them when sharing a receipt that contains either field. Each attempt has one accountable result. The Lead alone controls the start on the Lead's machine.
