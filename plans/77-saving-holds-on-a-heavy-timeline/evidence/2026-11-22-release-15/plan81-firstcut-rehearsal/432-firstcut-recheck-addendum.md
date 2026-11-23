# Plan 77 first-cut read-back on the Lead’s 432-clip sandbox

Request one read-only installed recheck of the exact locally reviewed upstream sources, on the Lead's machine at or after 05:00 UTC and only after the host confirms the slot. This is the current reviewed pre-freeze tuple. The eventual ordered frozen release tuple and the second cut's new 1,000-edge fixture are separate.

Start with [the signed 432 runbook](https://github.com/banodoco/astrid-dev/blob/7443fd20c1e02790611190e9bdebb22c1b74fec5/plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-22-release-15/432-clip-readback-runbook.md). Keep the signed backup and proof restore unchanged. Use only a new installation, disposable working restore and first-cut receipts root. The last Round 5 adoption passed authenticated restore but refused during its final revision verification at 5m21s. The same copy passed an independent offline doctor in 4m46s. The narrower verified-head browser path needs healthy admission first. No second attempt or restart is implicit if the new adoption refuses.

## Exact setup substitutions

The Lead supplies the absolute paths of their existing clean product clones, the existing PR 370 tooling checkout and the known pinned Node and browser tools. The following is the first command block on the authorized Lead machine. It only creates disposable source worktrees and generates pins. It does not touch a realm or start a process.

```bash
set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
: "${BASE_APP:?clean absolute App source clone}" "${BASE_AGENT:?clean absolute Agent source clone}"
: "${BASE_RUNTIME:?clean absolute Runtime source clone}"
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

Use these generated values for the three SHA assignments in runbook section 1 and `STACK="$BOX/firstcut-432-reviewed"`, `RECEIPTS="$BOX/firstcut-432-reviewed-receipts"`. Build private exact-revision Agent and Runtime mirrors by section 7. The locally generated Agent pin is a child of the reviewed Agent source. Publish neither it nor the App pin. Verify the private manifest with the installer checker and save its inputs before install. The setup keeps the same verified Runtime schema digest.

Run sections 1–4 once each with their existing pinned source checks and approved 1800 s adoption budget. Stop on a final integrity refusal, an ambiguous catalog, or loss of process and file custody. Preserve exact receipts and the untouched proof digest. A final-claim timeout counts only as materialized if section 3's exact proof applies, and health still needs section 4.

If healthy, use the **compiled editor** part of section 5 before any SDK history read. Run its existing headless observer twice using the exact signed 432-clip inventory, with separate receipt files and two independently removed browser profiles. Record startup, cold browser and same-process reopen separately. Require the same process birth, selected realm, public revision/publication/digest, complete fixture identities, zero timeline commit POSTs, completion of the cold verified-head read before reopen, and local selection traffic. A first legitimate selection can make the first reopen replay once. No document edit is needed for this read-back. Then run section 6 once. Preserve phases if approval, restore, admission, compile, browser or public proof stops the run.
