# Tasks — One update path and release

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal (everything below very hard), **X** = very hard, **S** = super hard (see the [run contract](../../skills/astrid-dev-shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change. Start each task from the live heads, recorded when it starts. The SHAs here only locate the cited lines: App `915bfa84`, Agent `a2c4ab7d` (the same product code as `709492fa` in inputs.md, plus test-harness commits), Runtime `61e2c301`. Re-check those lines against the branch being built.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Phase 1a — App and release versions (about 6 days)** | | | | | |
| UR-1 Update now only when the installed Astrid reports `self_update`, and the real reason whenever it can't run | N | — | app `src/shared/lib/updates/{useInstallerUpdate,updateOperation,resolveUpdate}.ts`, `src/integrations/runtime/client.ts`, `UpdateResolutionActions.tsx`, `SettingsModal/sections/AstridUpdatesSection.tsx`; surface update UI | Without `self_update`, Update now is hidden and the one line plus the command show; busy shows it disabled. Each status `reason` and POST `details.reason` has its own line; an unknown reason reads as needs repair | [ ] PR #207 open into int; CI queued |
| UR-1b One accepted-digest list for the App, local launcher and dev workspace | N | — | app `src/integrations/runtime/{contract-metadata.ts,runtime-update-contract.mjs}`, `scripts/dev-local-workspace.mjs`, `package.json` | `resolveUpdate.source-contract.test.mjs` passes through `npm run test:node` | [x] merged into int (App #205) |
| UR-3 Setup block off update surfaces; Updates gains a repair entry | N | UR-1 | app `UpdateResolutionActions.tsx`, `ChatUpdateNeeded.tsx`, `SettingsModal/sections/{AstridStatusSection,AstridUpdatesSection,astridStatusCopy}` | No SetupBlock on update surfaces or the status section; a degraded direct install finds the plain install line under Updates | [ ] blocked: waits on UR-1 landing |
| UR-4 Chat update cards use the shared decision | N | UR-1, UR-3 | app `src/tools/video-editor/components/AgentChat/**` | One error renders one card; chat's action is "See updates" | [ ] blocked: waits on UR-1, UR-3 |
| UR-5 Pinokio memory reads `identity.managed_by` | N | — | app `RuntimeConnectionProvider.tsx` | Through both the proxy and the door, Pinokio is recognised and never sees the installer command | [x] merged into int (App #203) |
| UR-6 Pinokio fully local serves update status | N | UR-5 | app `config/vite/localUpdateStatus.ts` | Under `vite preview` the status answers instead of 501, and the 501 test is inverted | [ ] PR #206 open into int; CI queued |
| UR-7 Decision table test | N | UR-1–UR-4 | app update decision tests | Install type × situation, plus the negative cases in the plan | [ ] blocked: waits on UR-1–UR-4 |
| UR-8 `release-guard` job | N | — | app `scripts/installer/**`, `.github/workflows/{test,served-manifest-canary}.yml`, `config/qualification/**`; contract release number | Tuple or bootstrap change without +1 fails; any other `release` change fails; it runs on pull requests and on push | [x] merged into int (App #204) |
| UR-8b Version names and the only release writer | N | UR-8 | app `scripts/installer/{pin,release-guard,served-manifest,releaseVersion}.mjs` (`releaseVersion` is new), `release.test.mjs`, `.github/workflows/test.yml` | `versionOf(10, [])` is `0.0.10`; a minor start at 15 gives `0.1.0`, then 16 gives `0.1.1`; a start that isn't the next minor or major, or comes without +1, is refused; a PR into `int/**` that changes `release`, `required` or `version_starts` is refused; changing `required` alone passes; `pin.mjs --release --require` sets the floor to the new release | [ ] in progress (local worker) |
| UR-8c Release log in astrid-dev | N | — | astrid-dev `plans/releases.md` (new), `scripts/check_docs.py` and its test, `skills/astrid-dev-release/SKILL.md` | Check tests: a gap in release numbers, a wrong version step, a short SHA, an empty owner go and a broken plan link each fail; the legacy Release 9 row passes | [ ] in progress (local worker; astrid-dev PR) |
| UR-8d Users see versions, not release numbers | N | UR-8b, UR-1, UR-3 | app `src/shared/lib/updates/updateStatus.ts`, `SettingsModal/sections/AstridUpdatesSection.tsx` | Shows "Astrid is up to date (0.0.10)", "Update available: Astrid 0.0.11" and "Installed 0.0.9" from release 9; no screen shows "Release N" | [ ] blocked: waits on UR-8b, UR-1, UR-3 |
| **Phase 1b — fully local (about 1.5 days)** | | | | | |
| UR-9 Fully local Update now through the in-page updater | X | UR-1 | app `updateOperation.ts` (`LocalPageUpdate`), `config/vite/localUpdatePage.ts`, `scripts/local-update*.mjs` | Spike confirms why `f2eca0bd5` hid it; a dev:local test updates through the page | [ ] blocked: waits on UR-1 |
| **Phase 1c — Release 10 (about 6.5–7.5 days)** | | | | | |
| UR-10 Update now works end to end | S | — | agent `astrid/installer/update_job*.py`, new e2e test; contract update helper | Agent test: the Runtime's real request through the real helper, prepare → accept → launch and recovery-needed, with fake `systemctl`/`systemd-run` | [x] merged into int (Agent #301) |
| UR-11 Runtime reports `self_update` and a reason in every state | X | UR-10 | runtime `astrid_runtime/update.py`; agent `update_job.py` availability; contract update status | `self_update` comes from the helper reporting its actions, on every OS; unclassified causes are `needs-repair`, Pinokio and source are `managed-elsewhere` | [ ] ready, not started |
| UR-12 Hosted update can target a stand-in release | X | — (UR-11 if the fallback seam is chosen) | agent journey CI (`journey.yml`, `scripts/ci_*journey*.py`); runtime `update.py` only if the fallback seam is chosen, then after UR-11 | A probe on each OS runner chooses CI-level interception, or the owner-approved fallback seam | [ ] ready, not started; needs a pushed probe branch |
| UR-13a Windows task-host journey: accept the recommended plan on install | N | — | agent `scripts/ci_windows_journey.py`, `tests/test_ci_windows_journey.py` | 61 focused tests pass; the Windows task-host jobs go green on the PR | [ ] PR #302 open into int; Windows jobs running |
| UR-0 Investigate why App main is red (read-only) | N | — | none (read-only) | First red job, commit and cause for each failing job on App main | [ ] stopped before the table was returned; the base runs settled UR-5's failures |
| UR-13 Hosted button-path update on every OS | X | UR-10–UR-12 | agent `journey_fresh_update.py`, `windows_update_journey.py`, `ci_journey_keepgoing.py`, `journey.yml` | The update leg of the three direct fresh rows POSTs through the door to a stand-in release | [ ] blocked: waits on UR-11, UR-12, UR-13a |
| **Review — before publishing** | | | | | |
| UR-R Up to three independent reviews of the integrated candidate | S | UR-1–UR-13, UR-8b–UR-8d | all Plan 29 scopes (read-only review) | Each round produces either no blocking findings, or new routed task cards that are done before the next round; see [review rounds](#ur-r-review-rounds) | [ ] blocked: waits on all tasks |
| UR-14 Publish Release 10 (0.0.10) | N | all, including UR-R | app `public/install-manifest.json`, `runtime.lock.json`; astrid-dev `plans/releases.md` | Owner names the tuple, the kind (patch) and whether it's required (no), and says go; `pin.mjs --release` writes the number; `public/install*` frozen; canary passes; the log row is added from `pin.mjs` output | [ ] blocked: waits on UR-R and UR-8b–UR-8d |
| **Owner** | | | | | |
| Turn on branch protection on App `main`, requiring `release-guard`, up to date, including admins | owner | UR-8 | App repository settings | Settings show the required check | [ ] |

**Overlap with other projects:** Plan 09 IU-1 and IU-8 change the same update helper and transaction as UR-10, UR-11 and Plan 30's UR-16, so they run after them. Plan 10's Pinokio row work shares `pinokio_row_driver.py` with Plan 30's UR-18a.

## Task details

### UR-1 Update now only with `self_update`
- **The new field.** `self_update` is a new boolean on `GET /v1/update/status`. The existing `available` doesn't serve this purpose, because it reports true on macOS and Windows even though the helper fails.
- **Where the App gates it.** Gate in `useInstallerUpdate.ts` (about :60-64) and `canStartInstallerUpdate` (`updateOperation.ts:24-27`), so `start()` is gated too.
- **Behaviour today.** A missing field reads as false, so the button disappears for everyone until Release 10.
- **Fixtures.** About 14 caller tests that assume `available: true` need fixtures.

### UR-1 (continued): real refusal reason
- Read the POST refusal's `details.reason` (it's ignored today at `updateOperation.ts:134-141`).
- Stop dropping unknown reasons (`:17-22`).
- A 409 reconciliation has `kind`, not `reason`.
- **What each answer shows** (advisor, 8 Nov):
  - `self_update` true: Update now.
  - `recovery-needed`: "Astrid needs repair before it can update." plus the repair entry from UR-3, never the old "Select Update…" copy.
  - `source`: its own line saying this Astrid runs from source, with the source update command. Not needs-repair.
  - Any other or unknown reason: "Astrid can't update itself on this computer. Run the command below to update it." Show the Runtime's message and keep the reason code for diagnostics. An unknown reason is never read as needs-repair.
  - A 409 reconciliation `kind` reports how an earlier update ended. It is not a refusal reason, so show that result (updated, rolled back or failed) instead of mapping it to a reason.
- **Contract drift found on `main`:** `resolveUpdate.source-contract.test.mjs` fails because `contract-metadata.ts` accepts digest `a36913ec…`, but the shared `LEGACY_RUNTIME_SCHEMA_DIGESTS` in `runtime-update-contract.mjs`, which the local launcher uses, does not. `scripts/dev-local-workspace.mjs` holds a third copy. No CI list runs the test. This is task UR-1b.

### UR-1b One accepted-digest list
- **Scope:** app `src/integrations/runtime/{contract-metadata.ts,runtime-update-contract.mjs}`, `scripts/dev-local-workspace.mjs`, `package.json` (`test:node`).
- **Route and dependencies:** N, no dependencies; it lands before UR-1.
- **Change:**
  - Move the digest into the shared list so the App, the launcher and the dev workspace all read one source.
  - Delete the copies.
  - Add the test file to `test:node`.
- **Proof:** `resolveUpdate.source-contract.test.mjs` passes, run through `npm run test:node`.

### UR-3 Setup block and repair
- **Remove** the SetupBlock renders at `UpdateResolutionActions.tsx:47,51`, `ChatUpdateNeeded.tsx:24` and `AstridStatusSection.tsx:120-123`.
- **The status section** says "Repair it under Updates." for a degraded direct install.
- **The Updates section** gains that repair entry: the plain install line, without `--update`.
- **Check in Agent code** that the plain line repairs a degraded install and respects autostart off.
- **Copy:** `astridStatusCopy.ts:9` promises instructions that will no longer appear, so it changes.

### UR-4 Chat cards
- **Today:** one error renders at `AgentChat.tsx:1318, 1632, 719-722`, `AgentChatMenu.tsx:321` and `NewChatMenu.tsx:286`.
- **Wording:** take the title and sentence from `updateNeededSentence`.
- **Hooks:** chat renders without providers (`TourChatPanel.tsx:164`), so use no required hook.

### UR-8 `release-guard`
- **Job:** a new `release-guard` job on `pull_request` and on push to `main`.
- **Base:** the PR base, or `github.event.before` on push.
- **Tuple bytes:** the manifest minus `release` and `required`, plus `public/install`, `install.ps1` and `install.sh`.
- **The rule:** if those bytes change, `release` goes up by exactly 1; otherwise it is unchanged.
- **`required`:** validate `0 ≤ required.release ≤ release` and a non-empty reason.
- **Tools:** `pin.mjs` stops writing `release`. The Agent's `regenerate_runtime_pins.py` already leaves it alone.
- **Delete:** `update-manifest.mjs`, the release-0 and baseline files, and `check-public-updater-candidate.*`.
- **Canary:** it also checks `release` and the bootstrap bytes.
- **App draft PR #194 doesn't block this.** It edits the same manifest but targets `pre-main`, not `main`, and has been idle since 7 Nov. Build UR-8 on `main`. If #194 is later retargeted to `main`, it must pass UR-8's check like any other change.

### UR-8b Version names
- **Versions are names, not a new number.** The integer `release` stays the only ordering key everywhere: App, Agent, Runtime, Pinokio and on users' disks. A version is worked out from it with `versionOf(release, version_starts)`: `0.0.N` by default, and from each owner-declared minor or major start, counting on from there.
- **`version_starts`** is a short, add-only list in the manifest, for example `[{"release": 15, "version": "0.1.0"}]`. It sits outside the tuple bytes and is validated separately. The Agent ignores unknown manifest keys, and Pinokio and the Runtime read only `release`, so nothing else changes.
- **The only writer.** `pin.mjs --release [minor|major] [--require "reason"]` is the only way `release`, `version_starts` or `required` change. Plain pinning never touches them.
- **Integration branches.** On PRs into `int/**`, `release`, `required` and `version_starts` must be byte-identical to the base. The number moves once, on the release PR to `main`. This prevents a double bump.
- **Required stays its own decision.** It is set per release with a reason and never implied by the kind. With `--release`, `--require` sets the floor to the new release.
- **Reuse:** extends `pin.mjs` and UR-8's guard. There's no new publish script.

### UR-8c Release log
- **`plans/releases.md`:** one row per published release, add-only. Its columns are Release, Version, Kind, Date, App commit, Agent, Runtime, Pinokio, Required (no, or the reason), Projects (plan links) and Owner go.
- **A record, not a source.** The App manifest is what the product acts on. Release writes the row from `pin.mjs` output after the canary passes, and never edits it afterwards.
- **History:** the log starts with a legacy row for Release 9 = 0.0.9. Earlier releases are named 0.0.N but not backfilled.
- **App commit** is the merge commit that published the release. Later hosted App deploys aren't releases. The Pinokio SHA is informational only.
- **`check_docs.py`:** release numbers go up by exactly 1; each version is the correct patch, minor or major successor; SHAs are full; Owner go isn't empty. Plan links use the existing link check.
- **Release skill:** one paragraph in the installer-tuple lane covers the steps: propose the kind (patch by default), get the owner's go on version, kind and required, run `pin.mjs --release`, publish, verify with the canary, then add the row.

### UR-8d Versions on screen
- Users see versions, never release numbers. The kind isn't displayed.

### UR-9 Fully local Update now
- **Independent of the broken path.** The updater runs the installed Agent's `local_update` module and doesn't use the broken `reconcile` path, so it should work on existing installs (from source; to confirm).
- **No recorded reason it was hidden.** `f2eca0bd5` has no reason recorded. Its test name points at the npm route that was since removed.
- **Paths:**
  - Primary: Update now.
  - Secondary: the normal install command (owner decision of 7 Nov).

### UR-10 End to end
- **Merge the whole lane** in order: `7c9438f55`, `548c8f93f`, `eaa9996de`, `b97c43db8`, `a721da65a`. All five merge cleanly onto Agent main.
- **Fix the remaining mismatches the test finds**, which include:
  - the implicit prepare action;
  - refusal labelling;
  - the Runtime test stub's `launch_status: "started"`, which the Agent never emits.
- **Test setup:** Agent tests already import `astrid_runtime` at the pinned SHA. The test redirects prepare URLs by wrapping `_helper`, with no production change.

### UR-11 `self_update` and reasons
- **Where `self_update` comes from:** the helper's `availability` action lists its supported actions, and old helpers can't, so they read false. Move the probe from Linux-only (`update.py:103`) to every OS.
- **Reasons:**
  - Emit `reason` in every state, not only `none`.
  - Keep `busy`, `autostart-off` and `unsupported-service-manager`.
  - Add `needs-repair` (anything unclassified) and `managed-elsewhere` (Pinokio, source).
- **Compatibility:** older Apps ignore unknown keys (`client.ts:247-259`).
- **Tests to update:** those asserting the old shape (`test_update_jobs.py` around :433-441 and :489-530).

### UR-12 Stand-in target
- **What's in the way:** the update's URLs are constants (`update.py:27-29, 308-309`), must be HTTPS (`tools.py:126`), and are stripped from the environment (`:139`).
- **Preferred:** CI-level interception. The runner maps astrid.haus to a local HTTPS server whose certificate only that runner trusts, so product code is unchanged.
- **Fallback:** a runtime-gated seam that fails closed, needs a stand-in marker and a pinned digest, and has no HTTP way to set it. It needs owner approval.

### UR-13 Hosted button path
- **What changes:** the update leg of `journey_fresh_update.py` (about :126) and `windows_update_journey.py` (about :225). It is a POST with Origin `https://astrid.haus`, `Content-Length: 0`, no Authorization or Cookie, and the server-side `installer:update` scope.
- **Hard-coded release:** fix `release == 1` (`journey_fresh_update.py:24-25`, `windows_update_journey.py:185`, `ci_journey_keepgoing.py:238`).
- **Probes first:** launchd (macOS) and the Windows interactive scheduled task on hosted runners.

### UR-R Review rounds

This plan sets its own review policy, as the [run contract](../../skills/astrid-dev-shared/run-contract.md) allows.

1. **Run a round.** An independent S reviewer (Opus) reviews the integrated candidate across App, Agent, Runtime and launcher. It reviews against [the completion criteria and negative cases](plan.md#completion) and the recorded owner decisions. It returns each finding as a task card, with these fields:
   - outcome;
   - route (N, X or S, by the run contract);
   - scope;
   - dependencies;
   - focused proof.
2. **Do the findings.** The manager adds each card as a row directly below UR-R in the task table, numbered `UR-R<round>.<n>`. It orders any that overlap by dependency, and runs them like any other task. UR-14 waits for all of them.
3. **Run the next round** on the new candidate.

The stage stops after a round with no blocking findings, or after three rounds. A blocking finding still open after three rounds goes to the owner, not to a fourth round. Non-blocking findings are recorded, and are done only if the owner asks.
