# Plan 77 read-back of the signed 432-clip fixture

22 November 2026. Run on the Lead's machine. The signed backup remains at `/root/codex/p77box/backup/realm-432`, with its existing local authentication custody. The stopped source realm and `/root/codex/p77box/restore-432-proof` are evidence. Every command that can write a realm targets a new run root or the new authenticated working restore. Use one attempt per step. If a check fails, retain receipts and stop the disposable owner through its native lifecycle if safe. Send the failed gate to the host before trying again. No command needs to read or print credentials.

The proof so far is that the backup and authenticated restored DB share the expected digest and realm UUID. The first adoption materialized a copy and hit a final-claim transport timeout. The subsequent managed `up` on a sibling data root refused. Neither observation proved a readable Runtime. The commands below use the native route that worked on v30, with a longer admission timeout and independent Runtime identity and read gates.

## 1. Pin or verify the installed tuple

Set `APP` to a clean checkout of the exact App, `TOOLS` to the exact tooling PR checkout and `NODE20` to the pinned renderer binary. Set `STACK` and `RECEIPTS` to unused names under the box. Confirm no old run owns the planned local ports. This creates only the new run and evidence roots. The installer may initialize an empty realm under `STACK/installed-data`. It leaves the signed backup and proof restore alone.

```bash
set -Eeuo pipefail
umask 077
BOX=/root/codex/p77box
BACKUP="$BOX/backup/realm-432"
PROOF="$BOX/restore-432-proof"
STACK="$BOX/round5-432-readback"
RECEIPTS="$BOX/round5-432-readback-receipts"
WORKING="$STACK/working-restore"
DATA="$STACK/direct-data"
REALM=0d6fd08f-8754-489c-8af9-276dcde43762
DBSHA=5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8
APP_SHA=be9cc2407306eff06252c0d54be1c7f5afcacf3f
AGENT_SHA=18adee8034973837a97fcd7392cd67f4566fa992
RUNTIME_SHA=d7be2f0458a55c1f26e1138a125ffefe382f56f4
: "${APP:?absolute product App checkout}" "${TOOLS:?absolute App PR 370 checkout}"
: "${NODE20:?absolute pinned renderer Node v20.19.4}"
test "$(git -C "$APP" rev-parse HEAD)" = "$APP_SHA"
test -z "$(git -C "$APP" status --porcelain)"
test "$(git -C "$TOOLS" rev-parse HEAD)" = 5b2c76a6a636d835700bc5f12b48848861dc30f5
test "$(node -p 'process.versions.node.split(".")[0]')" = 22
test "$("$NODE20" --version)" = v20.19.4
test "$(realpath "$PROOF")" = "$PROOF"
test "$(realpath -m "$STACK")" = "$STACK"
test "$(realpath -m "$RECEIPTS")" = "$RECEIPTS"
test ! -e "$STACK" && test ! -L "$STACK"
test ! -e "$RECEIPTS" && test ! -L "$RECEIPTS"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
python3 - <<'PY'
import socket
for port in (2400, 17500, 17501):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", port))
PY
mkdir -m 700 "$STACK" "$RECEIPTS"
mkdir -m 700 "$STACK/home" "$STACK/tmp"
owned=(env -u ASTRID_PREPARED_CONNECTION -u ASTRID_TIMELINE_EVAL_ENDPOINT
  -u ASTRID_TIMELINE_EVAL_CREDENTIAL -u ASTRID_TIMELINE_EVAL_REALM_ID
  -u ASTRID_TIMELINE_EVAL_ACTOR_ID -u ASTRID_RUNTIME_DATA_ROOT
  -u ASTRID_RUNTIME_SOURCE_MANIFEST -u ASTRID_RUNTIME_CREDENTIAL
  HOME="$STACK/home" TMPDIR="$STACK/tmp" XDG_DATA_HOME="$STACK/home/.local/share"
  XDG_STATE_HOME="$STACK/home/.local/state" XDG_CONFIG_HOME="$STACK/home/.config"
  XDG_CACHE_HOME="$STACK/home/.cache" ASTRID_NODE_EXECUTABLE="$NODE20"
  LIBGL_ALWAYS_SOFTWARE=1)
jq -e --arg a "$AGENT_SHA" --arg r "$RUNTIME_SHA" \
  '.agent.sha==$a and .runtime.sha==$r' "$APP/public/install-manifest.json" >/dev/null
cp -- "$APP/public/install-manifest.json" "$STACK/install-manifest.json"
# See section 7 for an exact local mirror override when the published source
# route cannot supply these pinned commits. Do it before the installer.
"${owned[@]}" ASTRID_RUNTIME_DOOR_PORT=17501 sh "$APP/public/install" \
  --root "$STACK/program" --data-root "$STACK/installed-data" \
  --yes --autostart off --command off --skills off --skill-copies off --no-browser \
  --manifest "$STACK/install-manifest.json" >"$RECEIPTS/install.log" 2>&1
version=$(cat "$STACK/program/current")
[[ "$version" =~ ^[a-f0-9]{12,40}$ ]]
CLI="$STACK/program/versions/$version/py/bin/astrid-runtime"
PROTO="${CLI%/*}/astrid-runtime-protocol"
PYTHON="${CLI%/*}/python"
SOURCE="$STACK/installed-data/runtime/source-profiles/astrid.json"
test -x "$CLI" && test -x "$PROTO" && test -x "$PYTHON" && test -f "$SOURCE"
jq -e --arg data "$STACK/installed-data" \
  '.owner=="haus.astrid.runtime" and .data_root==$data' "$STACK/program/install.json" >/dev/null
printf '%s\n' "$APP_SHA" "$AGENT_SHA" "$RUNTIME_SHA" >"$RECEIPTS/tuple.txt"
sha256sum "$STACK/install-manifest.json" "$SOURCE" >"$RECEIPTS/install-inputs.sha256"
"${owned[@]}" "$CLI" down --profile astrid --data-root "$STACK/installed-data" \
  --door-port 17501 --json >"$RECEIPTS/installed-empty-down.json"
jq -e '.status=="stopped" and .idle.safe==true' "$RECEIPTS/installed-empty-down.json" >/dev/null
```

The existing exact installation can supply the program, installed profile and its original isolated launcher environment if the Lead has those receipts and a safe stop. Keep its managed data selection as installed. Do not use that existing data root or the old failed read-back root as the adoption destination. `up` on an installation-shaped source must match both the install selection and program marker's data root. Native `workspace adopt` needs a separate empty catalog. These are separate obligations. [Managed lifecycle](https://github.com/banodoco/astrid-agent/blob/18adee8034973837a97fcd7392cd67f4566fa992/astrid/installer/runtime_lifecycle.py#L24), [Empty-catalog guard](https://github.com/banodoco/astrid-runtime/blob/d7be2f0458a55c1f26e1138a125ffefe382f56f4/astrid_runtime/workspace_adopt.py#L239)

## 2. Restore a fresh inactive working realm

This uses the exact installed sibling protocol CLI to authenticate the backup and materialize a new working copy. The command writes beside the **new** DB only. Keep the existing proof copy untouched. Hashing the proof DB is read-only, and this run does not attach or inspect it with SQLite. Neither restored DB should have active SQLite sidecars.

```bash
hash_db() { sha256sum "$1/realm.sqlite3" | awk '{print $1}'; }
test ! -e "$PROOF/realm.sqlite3-wal" && test ! -e "$PROOF/realm.sqlite3-shm"
test "$(hash_db "$PROOF")" = "$DBSHA"
test ! -e "$WORKING" && test ! -L "$WORKING"
test ! -e "$DATA" && test ! -L "$DATA"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
date -u +%FT%TZ >"$RECEIPTS/restore-start.txt"
"${owned[@]}" "$PROTO" restore --backup "$BACKUP" --destination "$WORKING" \
  >"$RECEIPTS/restore.json" 2>"$RECEIPTS/restore.stderr"
date -u +%FT%TZ >"$RECEIPTS/restore-end.txt"
jq -e --arg realm "$REALM" --arg sha "$DBSHA" \
  '.realm_id==$realm and .verification.realm.id==$realm and
   .verification.database_sha256==$sha and .verification.schema.version==33' \
  "$RECEIPTS/restore.json" >/dev/null
test "$(hash_db "$WORKING")" = "$DBSHA"
test "$(hash_db "$PROOF")" = "$DBSHA"
test ! -e "$WORKING/realm.sqlite3-wal" && test ! -e "$WORKING/realm.sqlite3-shm"
sha256sum "$PROOF/realm.sqlite3" "$WORKING/realm.sqlite3" >"$RECEIPTS/pre-adopt-databases.sha256"
```

If the Lead chooses to reuse the existing authenticated restore receipt instead of restoring a second time, copy the entire stopped proof realm into an absent `WORKING` using `cp -a --reflink=auto -- "$PROOF" "$WORKING"`, then recheck both digests, same UUID from the existing authenticated receipt, and no sidecars. Use only one of these preparation routes. Do not adopt directly from the proof or stopped source.

## 3. Adopt and classify its exit

Adopt can take a source owner lock beside the **working** DB and can copy, migrate, attach, create support files and start Runtime beside the **adopted** DB. The proof copy stays unopened. Allow at least 45 minutes for the command and subsequent readiness checks. The 1800-second admission setting is for the Runtime admission requests. It does not change the offline verifier or proxy deadlines. Record the real exit without masking it.

```bash
TARGET="$DATA/runtime/realms/$REALM"
date -u +%FT%TZ >"$RECEIPTS/adopt-start.txt"
adopt_rc=0
"${owned[@]}" ASTRID_RUNTIME_ADMISSION_TIMEOUT_SECONDS=1800 "$CLI" workspace adopt \
  --profile astrid --data-root "$DATA" --source-manifest "$SOURCE" \
  --from "$WORKING" --realm-id "$REALM" --door-port 17501 --json \
  >"$RECEIPTS/adopt.json" 2>"$RECEIPTS/adopt.stderr" || adopt_rc=$?
printf '%s\n' "$adopt_rc" >"$RECEIPTS/adopt-exit.txt"
date -u +%FT%TZ >"$RECEIPTS/adopt-end.txt"
test -d "$TARGET" && test ! -L "$TARGET"
jq -e --arg realm "$REALM" --arg target "$TARGET" \
  '.selected_realm_id==$realm and (.realms|length)==1 and
   .realms[0].realm_id==$realm and .realms[0].data_root==$target' \
  "$DATA/runtime/catalog.json" >"$RECEIPTS/selected-catalog-check.json"
if (( adopt_rc == 0 )); then
  jq -e --arg realm "$REALM" --arg target "$TARGET" \
    '.ok==true and .realm_id==$realm and .destination==$target' \
    "$RECEIPTS/adopt.json" >/dev/null
else
  jq -e --arg prefix "realm materialized at $TARGET; finish with astrid-runtime up after resolving: " \
    '.ok==false and (.error|startswith($prefix) and endswith("transport_timeout: runtime request timed out"))' \
    "$RECEIPTS/adopt.json" >/dev/null
fi
ADOPTED_SOURCE="$DATA/runtime/source-profiles/astrid.json"
test -f "$ADOPTED_SOURCE"
```

A matching timeout is conditional materialization evidence. It is never a passed boot or open. A different exit, catalog, or target path stops the run. Use the native attach/bootstrap that `workspace adopt` already launched. An installed `astrid-runtime up --profile astrid --data-root <matching managed install data> --source-manifest <profile in that data> --door-port 17501 --wait --json` is supported for a real managed selection, but in this sibling-data layout it would refuse before launch. Do not run it on `DATA` or switch the managed selection to force it. In particular, do not point it at the proof restore. If there is no exact live instance after the readiness window, record the stopped result. If the host orders one resume, first verify the exact adopted destination and same source against the existing journal, verify that no matching owner is still live and that port 17501 is free, then use the same command and a new receipt name. Do this only if those observations are conclusive. Save the exit and apply the same selected-catalog and readiness checks. No follow-on attempt is implicit. [Native adopt launch](https://github.com/banodoco/astrid-runtime/blob/d7be2f0458a55c1f26e1138a125ffefe382f56f4/astrid_runtime/workspace_adopt.py#L334), [Managed up dispatch](https://github.com/banodoco/astrid-runtime/blob/d7be2f0458a55c1f26e1138a125ffefe382f56f4/astrid_runtime/cli.py#L632)

```bash
# Only after the host orders one resume and the prior owner is confirmed absent.
jq -e --arg source "$WORKING" --arg target "$TARGET" --arg realm "$REALM" \
  '.source==$source and .destination==$target and .realm_id==$realm and
   (.state=="published" or .state=="attached" or .state=="started" or .state=="failed")' \
  "$DATA/runtime/adopt-journal.json" >/dev/null
resume_rc=0
"${owned[@]}" ASTRID_RUNTIME_ADMISSION_TIMEOUT_SECONDS=1800 timeout --signal=TERM 2700s \
  "$CLI" workspace adopt --profile astrid --data-root "$DATA" --source-manifest "$SOURCE" \
  --from "$WORKING" --realm-id "$REALM" --door-port 17501 --json \
  >"$RECEIPTS/adopt-resume.json" 2>"$RECEIPTS/adopt-resume.stderr" || resume_rc=$?
printf '%s\n' "$resume_rc" >"$RECEIPTS/adopt-resume-exit.txt"
```

## 4. Verify the already-started instance

This check reads only the adopted support files, process facts and health. Cap the readiness wait at 2700 s. Record elapsed time separately from browser or SDK work. It is suitable as a polling loop for the single adoption attempt, with no starts or restarts. A good status requires the active realm, software contract, process birth, and both serving endpoints to agree.

```bash
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
```

Use the explicit scoped SDK read in section 5 as the first authenticated data proof when measuring the Runtime alone. For the browser arm, verify through the App's authenticated proxy and avoid opening history before timed navigation. Capture Runtime user+system ticks from process birth before the first measured operation. The setup performs integrity checks, so record which reads ran before navigation and do not claim the process had an empty verification memo.

## 5. Choose the first read after readiness

### Standalone authenticated history probe

Use the exact project and timeline IDs from the Lead's 432 fixture record. This avoids the browser proxy's 60-second idle deadline. It calls the installed SDK's existing-only launcher. The `client._remote._transport` path below is a private accessor to the typed transport, used here to time exactly one HTTP history request without extra selector reads. The public equivalent is `result = client.timelines.history(project, timeline, limit=1)`, then `assert result.ok` and `page = result.data`. The public SDK also resolves the project and timeline, so its total must be labeled end-to-end SDK history time rather than the direct route time. Choose one path for the first read. The 900-second override is local to this observation process. The SDK handles credential custody internally. A successful page proves the route can return a head. Compare both head IDs against the fixture's independently recorded head. Limit 1 returns the first page's oldest item plus the current fixed head, so item count alone does not prove a 432-clip document. Retain only proof summary by default.

```bash
: "${PROJECT:?exact sandbox project ID}" "${TIMELINE:?exact 432 timeline ID}"
: "${PUBLICATION:?expected exact head publication}" "${REVISION:?expected exact head revision}"
date -u +%FT%TZ >"$RECEIPTS/history-start.txt"
"${owned[@]}" ASTRID_RUNTIME_CLI="$CLI" ASTRID_RUNTIME_DATA_ROOT="$DATA" \
  "$PYTHON" - "$PID" "$PROJECT" "$TIMELINE" "$PUBLICATION" "$REVISION" \
  >"$RECEIPTS/history-limit1.json" 2>"$RECEIPTS/history-limit1.stderr" <<'PY'
import json, os, sys, time
from pathlib import Path
from astrid.sdk import AstridClient
from astrid.sdk import workspace_client

pid, project, timeline, publication, revision = sys.argv[1:]
def process():
    fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    return fields[19], int(fields[11]) + int(fields[12])

workspace_client.WORKSPACE_REQUEST_TIMEOUT_SECONDS = 900.0
t0 = time.monotonic()
client = AstridClient.open_existing_from_launcher(client_name="plan-77-readback")
attach_seconds = time.monotonic() - t0
birth, before = process()
start = time.monotonic()
# Probe the typed transport directly to avoid extra timeline selector reads.
page = client._remote._transport.list_timeline_commits(project, timeline, limit=1)
elapsed = time.monotonic() - start
end_birth, after = process()
assert end_birth == birth
assert page["head"] == {"publication_id": publication, "revision_id": revision}
assert len(page["items"]) == 1
hz = os.sysconf("SC_CLK_TCK")
print(json.dumps({"outcome": "exact_head", "head": page["head"], "items": len(page["items"]),
                  "has_next_cursor": page.get("next_cursor") is not None,
                  "launcher_seconds": attach_seconds, "history_seconds": elapsed,
                  "runtime_cpu_seconds_before_history": before / hz,
                  "runtime_cpu_seconds_during_history": (after-before) / hz}))
PY
date -u +%FT%TZ >"$RECEIPTS/history-end.txt"
```

If profiling this arm, attach the existing local `py-spy` before the SDK call. Use the confirmed PID and birth above, one recording with `py-spy record --pid "$PID" --rate 100 --nonblocking --full-filenames --format raw --output "$RECEIPTS/history.py-spy.raw" --duration 900`. Run separately alongside the front-end-free read and interrupt **only that sampler** after it finishes. Record attach status, attempted sample count/errors, mode and hash, and keep raw frames local. [Typed history route](https://github.com/banodoco/astrid-agent/blob/18adee8034973837a97fcd7392cd67f4566fa992/astrid/sdk/workspace_client.py#L534), [Observe-only SDK launcher](https://github.com/banodoco/astrid-agent/blob/18adee8034973837a97fcd7392cd67f4566fa992/astrid/sdk/client.py#L515)

### Compiled editor read-back

Use this as the first measured arm if the question is editor open. A browser after the above SDK read measures an already-read Runtime. Check disk again, then run in the exact clean App checkout. Building writes App build output. Preview can create browser and adopted-support state and can invoke startup recovery. Watch that the Runtime PID and birth stay exact. Use a freshly created private headless Chrome profile, record it and delete it after the run. App proxy checks and read-back must point to this owned data root.

```bash
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
(
  cd "$APP"
  "${owned[@]}" PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
  "${owned[@]}" ASTRID_RUNTIME_PYTHON="$PYTHON" ASTRID_RUNTIME_SOURCE_MANIFEST="$ADOPTED_SOURCE" \
    PORT=2400 ASTRID_APP_LOOPBACK_ORIGIN=off node scripts/dev-local-workspace.mjs \
    --data-root "$DATA" --build
) >"$RECEIPTS/build.log" 2>&1
test -f "$APP/dist/index.html" && test -d "$APP/dist/assets"
(cd "$APP/dist" && find . -type f -print0 | sort -z | xargs -0 sha256sum) >"$RECEIPTS/dist-files.sha256"
(
  cd "$APP"
  exec "${owned[@]}" ASTRID_RUNTIME_PYTHON="$PYTHON" ASTRID_RUNTIME_SOURCE_MANIFEST="$ADOPTED_SOURCE" \
    PORT=2400 VITE_ASTRID_DYNAMIC_PROXY_PORT=17500 ASTRID_APP_LOOPBACK_ORIGIN=off \
    node scripts/dev-local-workspace.mjs --data-root "$DATA" --preview --preview-dir "$APP/dist"
) >"$RECEIPTS/preview.log" 2>&1 &
EDITOR_PID=$!
printf '%s\n' "$EDITOR_PID" >"$RECEIPTS/editor-pid.txt"
deadline=$((SECONDS+300))
preview_ready=0
while (( SECONDS < deadline )); do
  kill -0 "$EDITOR_PID"
  if curl -fsS --max-time 3 'http://127.0.0.1:2400/tools/video-editor?connect=1' >/dev/null &&
     curl -fsS --max-time 3 http://127.0.0.1:2400/api/runtime/v1/health \
       | jq -e --arg id "$INSTANCE" '.status=="ok" and .runtime_instance_id==$id' >/dev/null &&
     curl -fsS --max-time 3 http://127.0.0.1:2400/api/runtime/v1/realm \
       | jq -e --arg realm "$REALM" '(.realm_id // .realm.id // .id // .data.id)==$realm' >/dev/null; then
    preview_ready=1
    break
  fi
  sleep 2
done
test "$preview_ready" = 1
```

Navigate to `/tools/video-editor?connect=1&project=<encoded project>&timeline=<encoded timeline>`. Use the actual 432 fixture's full ID inventory and row IDs. A qualified writable marker requires every expected root clip ID, the exact rows, a visible draggable clip control and an enabled track-name input. Seeing the canvas alone is partial. Independently read and verify the public head, full document count and closure after the marker. Record the navigation and writable clocks, request start/status/duration for each limit-50 history page and verification read, Runtime CPU from birth to navigation and from navigation to marker, the exact installed identity, the settled head, zero commit POSTs, and profile deletion. Stop this one browser after 900 seconds if it never qualifies. Preserve a separate partial receipt with its boundary. A development server or a browser using different bytes or Runtime identity cannot supply the compiled comparison.

The following headless observer uses the fixture inventory the Lead independently recorded. Set `FIXTURE` to a JSON file with the exact `project_id`, `timeline_id`, `clip_ids` array of length 432, `track_ids` array, a visible `control_clip_id` and `control_track_id`, `occurrence_ids` array, and `revision`, `publication`, and `content_digest` of the signed fixture. Use the existing Chrome and Playwright, with absolute paths in `CHROME` and `PLAYWRIGHT_ESM`. This observer performs no edit. A writable marker and a failed public postflight remain separate outcomes.

```bash
: "${FIXTURE:?approved 432 fixture inventory JSON}" "${CHROME:?absolute Chrome path}"
: "${PLAYWRIGHT_ESM:?absolute installed Playwright ESM entrypoint}"
df -h "$BOX"
(( $(df -Pk "$BOX" | awk 'NR==2 {print $4}') >= 25*1024*1024 ))
ticks=$(getconf CLK_TCK)
"${owned[@]}" node --input-type=module - "$FIXTURE" "$PID" "$ticks" "$APP/dist" "$TOOLS" "$CHROME" "$PLAYWRIGHT_ESM" \
  >"$RECEIPTS/browser-opening.json" 2>"$RECEIPTS/browser-opening.stderr" <<'JS'
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [inventory, pid, clock, dist, tools, chrome, playwright] = process.argv.slice(2);
const expected = JSON.parse(await readFile(inventory, 'utf8'));
const sorted = values => [...new Set(values)].sort();
assert.equal(sorted(expected.clip_ids).length, 432);
assert(expected.clip_ids.includes(expected.control_clip_id));
assert(expected.track_ids.includes(expected.control_track_id));
const { chromium } = await import(pathToFileURL(playwright));
const { publicSnapshot } = await import(pathToFileURL(path.join(tools, 'scripts/save-loop/assert.mjs')));
const origin = 'http://127.0.0.1:2400';
const url = new URL('/tools/video-editor', origin);
url.searchParams.set('connect', '1');
url.searchParams.set('project', expected.project_id);
url.searchParams.set('timeline', expected.timeline_id);
async function processTicks() {
  const fields = (await readFile(`/proc/${pid}/stat`, 'utf8')).split(') ').at(-1).trim().split(/\s+/);
  return { birth: fields[19], cpu: Number(fields[11]) + Number(fields[12]) };
}
const profile = await mkdtemp(path.join(tmpdir(), 'p77-432-chrome-'));
const receipt = { phase: 'browser_start', runtime_pid: Number(pid), requests: [] };
let context, start, before;
try {
  context = await chromium.launchPersistentContext(profile, {
    executablePath: chrome, headless: true, viewport: { width: 1700, height: 1500 },
    args: ['--disable-gpu', '--disk-cache-size=1', '--media-cache-size=1', '--no-first-run'],
  });
  const page = context.pages()[0] ?? await context.newPage();
  const observed = new Map();
  page.on('request', request => {
    if (start === undefined) return;
    const target = new URL(request.url());
    if (target.origin !== origin) return;
    const entry = { method: request.method(), kind: request.resourceType(), route: target.pathname,
      started_ms: performance.now() - start };
    if (target.pathname.endsWith('/commits')) {
      entry.history_limit = target.searchParams.get('limit');
      entry.history_has_cursor = target.searchParams.has('cursor');
    }
    observed.set(request, entry);
    receipt.requests.push(entry);
  });
  page.on('response', response => {
    const entry = observed.get(response.request());
    if (entry) { entry.status = response.status(); entry.headers_ms = performance.now() - start; }
  });
  page.on('requestfinished', request => {
    const entry = observed.get(request);
    if (entry) entry.finished_ms = performance.now() - start;
  });
  page.on('requestfailed', request => {
    const entry = observed.get(request);
    if (entry) entry.failed_ms = performance.now() - start;
  });
  receipt.phase = 'navigation';
  before = await processTicks();
  start = performance.now();
  await page.goto(url.href, { waitUntil: 'domcontentloaded', timeout: 120000 });
  receipt.navigation_ms = performance.now() - start;
  receipt.phase = 'writable_editor';
  await page.waitForFunction(fixture => {
    const route = new URL(location.href);
    if (route.searchParams.get('project') !== fixture.project_id ||
        route.searchParams.get('timeline') !== fixture.timeline_id) return false;
    const rows = new Set(Array.from(document.querySelectorAll('[data-row-id]'), row => row.dataset.rowId));
    const ids = new Set(Array.from(document.querySelectorAll('.clip-action[data-row-id][data-clip-id]'), clip => clip.dataset.clipId));
    const clip = document.querySelector(`.clip-action[data-clip-id="${CSS.escape(fixture.control_clip_id)}"][data-row-id="${CSS.escape(fixture.control_track_id)}"]`);
    const input = document.querySelector(`[data-track-label][data-track-id="${CSS.escape(fixture.control_track_id)}"] input[aria-label="Track name"]`);
    return rows.size === fixture.track_ids.length && fixture.track_ids.every(id => rows.has(id)) &&
      fixture.clip_ids.every(id => ids.has(id)) && clip?.getClientRects().length &&
      clip.getAttribute('role') === 'button' && clip.tabIndex >= 0 && clip.getAttribute('aria-disabled') !== 'true' &&
      input && !input.disabled && !input.readOnly && input.getBoundingClientRect().width > 0;
  }, expected, { timeout: Math.max(1, 900000 - Math.ceil(receipt.navigation_ms)) });
  receipt.writable_ms = performance.now() - start;
  const atWritable = await processTicks();
  assert.equal(atWritable.birth, before.birth);
  receipt.runtime_birth = before.birth;
  receipt.runtime_cpu_before_navigation = before.cpu / Number(clock);
  receipt.runtime_cpu_navigation_to_writable = (atWritable.cpu - before.cpu) / Number(clock);
  receipt.phase = 'compiled_bytes';
  const scripts = receipt.requests.filter(x => x.kind === 'script' && x.started_ms <= receipt.writable_ms);
  assert(!scripts.some(x => /^\/(src|@vite|node_modules)\//.test(x.route)));
  const bundle = scripts.find(x => /^\/assets\/[\w.-]+\.js$/.test(x.route) && x.status === 200);
  assert(bundle);
  const served = await context.request.get(origin + bundle.route, { timeout: 5000 });
  assert(served.ok());
  const digest = bytes => createHash('sha256').update(bytes).digest('hex');
  assert.equal(digest(await served.body()), digest(await readFile(path.join(dist, bundle.route.slice(1)))));
  receipt.compiled_asset = bundle.route;
  receipt.phase = 'terminal_public_head';
  let timer;
  try {
    const head = await Promise.race([publicSnapshot(page, origin, expected),
      new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('public postflight deadline')), 120000); })]);
    assert.equal(head.headRevision, expected.revision);
    assert.equal(head.publicationId, expected.publication);
    assert.equal(head.content_digest, expected.content_digest);
    assert.equal(head.headCount, 1);
    assert.deepEqual(sorted(head.clipIds), sorted(expected.clip_ids));
    assert.deepEqual(sorted(head.payload.occurrences.map(item => item.occurrence_id)), sorted(expected.occurrence_ids));
    receipt.head = { publication: head.publicationId, revision: head.headRevision, content_digest: head.content_digest,
      active_heads: head.headCount, clips: head.clipIds.length, occurrences: head.payload.occurrences.length };
  } finally { clearTimeout(timer); }
  assert.equal((await processTicks()).birth, before.birth);
  receipt.phase = 'verified';
} catch {
  process.exitCode = 1;
} finally {
  if (before && start !== undefined && receipt.writable_ms === undefined) {
    receipt.stopped_ms = performance.now() - start;
    const atStop = await processTicks().catch(() => null);
    if (atStop?.birth === before.birth) {
      receipt.runtime_cpu_before_navigation = before.cpu / Number(clock);
      receipt.runtime_cpu_navigation_to_stop = (atStop.cpu - before.cpu) / Number(clock);
    }
  }
  try { await context?.close(); }
  finally { await rm(profile, { recursive: true, force: true }); }
  receipt.profile_removed = await stat(profile).then(() => false, error => error.code === 'ENOENT');
  receipt.timeline_commit_posts = receipt.requests.filter(x => x.method === 'POST' && x.route.endsWith('/commit')).length;
  if (!receipt.profile_removed || receipt.timeline_commit_posts) process.exitCode = 1;
  console.log(JSON.stringify(receipt));
}
JS
```

## 6. Stop safely and re-hash

Stop only the preview process started above, if present. Native down on the adopted data can reconcile lifecycle and checkpoint its DB. It must report an idle and safe stop. Hash the working and original proof DBs only after stop, along with the stopped adopted DB and schema. SQLite inspection uses immutable read mode after confirming no sidecars. A digest difference in the adopted DB requires reporting, even with an unchanged schema. Do not substitute an inferred digest or report successful open if the exact data read failed.

```bash
if [[ -n "${EDITOR_PID:-}" ]]; then
  kill -TERM "$EDITOR_PID"
  status=0
  wait "$EDITOR_PID" || status=$?
  [[ "$status" == 0 || "$status" == 143 ]]
fi
"${owned[@]}" "$CLI" down --profile astrid --data-root "$DATA" --door-port 17501 --json \
  >"$RECEIPTS/adopted-down.json" 2>"$RECEIPTS/adopted-down.stderr"
jq -e '.status=="stopped" and .idle.safe==true' "$RECEIPTS/adopted-down.json" >/dev/null
for realm_dir in "$PROOF" "$WORKING" "$TARGET"; do
  test ! -e "$realm_dir/realm.sqlite3-wal" && test ! -e "$realm_dir/realm.sqlite3-shm"
done
sha256sum "$PROOF/realm.sqlite3" "$WORKING/realm.sqlite3" "$TARGET/realm.sqlite3" \
  >"$RECEIPTS/post-stop-databases.sha256"
test "$(hash_db "$PROOF")" = "$DBSHA"
test "$(hash_db "$WORKING")" = "$DBSHA"
python3 - "$TARGET/realm.sqlite3" <<'PY' >"$RECEIPTS/adopted-schema.json"
import json, sqlite3, sys
from pathlib import Path
uri = Path(sys.argv[1]).resolve(strict=True).as_uri() + "?mode=ro&immutable=1"
with sqlite3.connect(uri, uri=True) as db:
    print(json.dumps({"sqlite_user_version": db.execute("PRAGMA user_version").fetchone()[0]}))
PY
```

Confirm the three endpoints are closed and the fresh browser profile is gone. Preserve the receipts and original stopped proof under their current custody. Remove only the new disposable stack after a safe stop and after saving the receipts. A mismatch leaves the new evidence available for diagnosis.

## 7. Local mirrors and Round 7 candidate on this machine

In App [PR #370](https://github.com/banodoco/astrid-app/pull/370), use [`scripts/save-loop/quick-backup-cycle.sh`](https://github.com/banodoco/astrid-app/blob/5b2c76a6a636d835700bc5f12b48848861dc30f5/scripts/save-loop/quick-backup-cycle.sh) as a receipt and ownership reference. Its `large` fixture is exactly 300 clips, with a fixed target and shot count. The `restore-run` and [`scripts/save-loop/diagnostics/capture-compiled-v30.mjs`](https://github.com/banodoco/astrid-app/blob/5b2c76a6a636d835700bc5f12b48848861dc30f5/scripts/save-loop/diagnostics/capture-compiled-v30.mjs) are also tied to the v30 manifest and do not take this fixture. Use the native commands above. The recorder supplies existing selectors, request-tape logic, CPU and profile lifecycles for a 432 observer with the actual fixture's IDs. [`diagnostics/restart-probe.py`](https://github.com/banodoco/astrid-app/blob/5b2c76a6a636d835700bc5f12b48848861dc30f5/scripts/save-loop/diagnostics/restart-probe.py) is optional resource evidence. [`diagnostics/rank-decoded-runtime-profile.py`](https://github.com/banodoco/astrid-app/blob/5b2c76a6a636d835700bc5f12b48848861dc30f5/scripts/save-loop/diagnostics/rank-decoded-runtime-profile.py) can summarize compact profile facts if supplied its required opening record with `.runtime_profile.raw`, sample count, error count, rate and nonblocking flag and a raw path of the record path plus `.py-spy.raw`.

For Round 5 stock, keep the three checked hashes from section 1. If the installer needs local repositories, prepare canonical exact-SHA git mirrors in the Lead's box and confirm all required objects and the OMP pin. Override only `.agent.repo`, `.runtime.repo` and, if needed, `.tools.omp.source.repo` in the private manifest. The official installer still builds the pinned versions. Preserve VibeComfy, lifecycle and all other sources as the approved manifest derives them.

For a Round 7 trial, wait for the exact reviewed App, Agent and Runtime SHAs and the generated testing pins. Generate the Agent's test-only Runtime witness against the **exact** Runtime checkout first. Ensure the exact resulting Agent commit's `runtime.lock.json.source_commit` equals the Runtime to be measured. If given a product Agent SHA fetchable by the official generator, derive a scratch manifest from the candidate App's pinned base with `node scripts/installer/pin.mjs <full Agent test SHA> --in public/install-manifest.json --out <private trial manifest>`. For local-only SHA inputs, use the repo's offline pin-reader workflow against the reviewed mirrors to verify the test manifest, or transfer the manager-generated manifest alongside the three test SHAs. Do not substitute the stock schema or dependency pins by hand. Before running the installer, verify all three commit IDs against the candidate receipt, confirm the Agent lock via `git show`, check the candidate manifest with `checkManifest` using the local exact-SHA reader, and apply only mirror path overrides. Leave the original backup and proof restore on the Lead's machine. Run the candidate in a new owned install with a fresh working restore and preserve independent stock and candidate receipts. Use matching edit input, launch and read markers across arms. The 432 plan measure separates SDK bundle pin from prepare/accept/response for the 12-command commit and from a read-only opening. Perform the mutation only under the reviewed candidate measurement card, in an independent authorized working restore.
