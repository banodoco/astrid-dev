# Tasks — One update path and release

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal (everything below very hard), **X** = very hard, **S** = super hard (see the [run contract](../../skills/astrid-dev-shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change. Start each task from the live heads, recorded when it starts. The SHAs here only locate the cited lines: App `915bfa84`, Agent `a2c4ab7d` (the same product code as `709492fa` in inputs.md, plus test-harness commits), Runtime `61e2c301`. Re-check those lines against the branch being built.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Phase 1a — App (about 4 days)** | | | | | |
| UR-1 Update now only when the installed Astrid reports `self_update`, and the real reason whenever it can't run | N | — | app `src/shared/lib/updates/{useInstallerUpdate,updateOperation,resolveUpdate}.ts`, `src/integrations/runtime/client.ts`, `UpdateResolutionActions.tsx`, `SettingsModal/sections/AstridUpdatesSection.tsx`; surface update UI | Without `self_update`, Update now is hidden and the one line plus the command show; busy shows it disabled. Each status `reason` and POST `details.reason` has its own line; an unknown reason reads as needs repair | [x] merged into int (App #207) |
| UR-1b One accepted-digest list for the App, local launcher and dev workspace | N | — | app `src/integrations/runtime/{contract-metadata.ts,runtime-update-contract.mjs}`, `scripts/dev-local-workspace.mjs`, `package.json` | `resolveUpdate.source-contract.test.mjs` passes through `npm run test:node` | [x] merged into int (App #205) |
| UR-3 Setup block off update surfaces; Updates gains a repair entry | N | UR-1 | app `UpdateResolutionActions.tsx`, `ChatUpdateNeeded.tsx`, `SettingsModal/sections/{AstridStatusSection,AstridUpdatesSection,astridStatusCopy}` | No SetupBlock on update surfaces or the status section; a degraded direct install finds the plain install line under Updates | [x] merged into int (App #209, follow-up #212) |
| UR-4 Chat update cards use the shared decision | N | UR-1, UR-3 | app `src/tools/video-editor/components/AgentChat/**` | One error renders one card; chat's action is "See updates" | [x] merged into int (App #211) |
| UR-5 Pinokio memory reads `identity.managed_by` | N | — | app `RuntimeConnectionProvider.tsx` | Through both the proxy and the door, Pinokio is recognised and never sees the installer command | [x] merged into int (App #203) |
| UR-6 Pinokio fully local serves update status | N | UR-5 | app `config/vite/localUpdateStatus.ts` | Under `vite preview` the status answers instead of 501, and the 501 test is inverted | [x] merged into int (App #206) |
| UR-7 Decision table test | N | UR-1–UR-4 | app update decision tests | Install type × situation, plus the negative cases in the plan | [x] merged into int (App #213) |
| UR-8 `release-guard` job | N | — | app `scripts/installer/**`, `.github/workflows/{test,served-manifest-canary}.yml`, `config/qualification/**`; contract release number | Tuple or bootstrap change without +1 fails; any other `release` change fails; it runs on pull requests and on push | [x] merged into int (App #204) |
| **Phase 1b — fully local (about 1.5 days)** | | | | | |
| UR-9 Fully local Update now through the in-page updater | X | UR-1, UR-3 (shares `AstridUpdatesSection.tsx`) | app `updateOperation.ts` (`LocalPageUpdate`), `config/vite/localUpdatePage.ts`, `scripts/local-update*.mjs`, `resolveUpdate.ts`, `SettingsModal/sections/AstridUpdatesSection.tsx`, `scripts/dev-local-workspace.mjs` | Spike confirms why `f2eca0bd5` hid it; a dev:local test updates through the page | [x] merged into int (App #210) |
| **Phase 1c — Release 10 (about 6.5–7.5 days)** | | | | | |
| UR-10 Update now works end to end | S | — | agent `astrid/installer/update_job*.py`, new e2e test; contract update helper | Agent test: the Runtime's real request through the real helper, prepare → accept → launch and recovery-needed, with fake `systemctl`/`systemd-run` | [x] merged into int (Agent #301) |
| UR-11 Runtime reports `self_update` and a reason in every state | X | UR-10 | runtime `astrid_runtime/update.py`; agent `update_job.py` availability; contract update status | `self_update` comes from the helper reporting its actions, on every OS; unclassified causes are `needs-repair`, source is `source` and Pinokio is `managed-elsewhere` | [x] merged into int (Agent #303, Runtime #35) |
| UR-12 Hosted update can target a stand-in release | X | — (UR-11 if the fallback seam is chosen) | agent journey CI (`journey.yml`, `scripts/ci_*journey*.py`); runtime `update.py` only if the fallback seam is chosen, then after UR-11 | A probe on each OS runner chooses CI-level interception, or the owner-approved fallback seam | [x] probe passed on Linux, macOS and Windows runners (CI interception works) |
| UR-13a Windows task-host journey: accept the recommended plan on install | N | — | agent `scripts/ci_windows_journey.py`, `tests/test_ci_windows_journey.py` | 61 focused tests pass; the Windows task-host jobs go green on the PR | [x] merged into int (Agent #302) |
| UR-0 Investigate why App main is red (read-only) | N | — | none (read-only) | First red job, commit and cause for each failing job on App main | [ ] stopped before the table was returned; base runs settled UR-5's failures |
| UR-13b Log the swallowed exception behind the update refusal (Runtime) | N | UR-13 | runtime `astrid_runtime/update.py` catch-all | Public refusal unchanged; exception type and message in the Runtime log only | [ ] Runtime PR #36 open into int; tests pass. Not yet visible on darwin (see UR-13c) |
| UR-13c Investigate the macOS update journal identity refusal (read-only) | S | UR-13 | none (read-only) | Check, expected and seen value, producer, real-install impact, and smallest producer fix | [x] macOS cause: the HOME split between the harness and launchd. Fixed by Agent #306 (plist pins HOME) and #307 (the update reads its install record from the recorded home); macOS fresh row passed on run 42491171373 (UR-13g, UR-13h) |
| UR-13d Investigate the Linux systemd owner refusal and the failed recovery (read-only) | S | UR-13 | none (read-only) | Check, expected and seen owner, producer, real-install impact, and smallest producer fix | [x] cause: unit loaded from the wrong config dir (XDG split); fixed in the harness (`journey.yml`), product check kept |
| UR-13e Investigate the Windows DACL refusal (read-only) | S | UR-13 | none (read-only) | Check, expected and seen ACEs, producer, real-install impact, and smallest producer fix | cause found: `mkdtemp` ACEs; fix in Runtime #37, open |
| UR-13f Windows launch WinError 2: bare `powershell.exe` under the service PATH | N | UR-13 | agent `update_job_platform.py`, `update_job.py` | Launch resolves PowerShell by absolute path; a test runs without stubbing the SID | [x] merged into int (Agent #305, 13:46 UTC) |
| UR-13 Hosted button-path update on every OS | X | UR-10–UR-12 | agent `journey_fresh_update.py`, `windows_update_journey.py`, `ci_journey_keepgoing.py`, `journey.yml` | The update leg of the three direct fresh rows POSTs through the door to a stand-in release | [ ] Linux and macOS proven (run 42491171373). Windows proven: run 42503778581 (cand/29-ur13p, direct-windows pass, with UR-13i/k/l). Open: #304 (harness), Runtime #36 and #37 (UR-13b and UR-13e fix), #309 (UR-13j, in review). Final three-row run waits for UR-13j |
| UR-13i Keep the whole Windows worker error in the job log | N | UR-13 | agent `astrid/installer/update_job_platform.py` (`_worker_script`) | The wrapper's error reaches the log whole, and it exits with the worker's code | [x] merged into int (Agent #308, 16:11 UTC) |
| UR-13j A dead Windows worker ends its job, not 'active' forever | S | UR-13i | agent `astrid/installer/update_job*.py` | A never-claimed worker that exits non-zero ends the job as failed, a claimed one as recovery-needed; still running changes nothing | [x] merged into int (Agent #309, decision 12 cut-down) |
| UR-13k The Windows worker does not reopen the job log | N | UR-13i | agent `astrid/installer/update_job.py` (`_worker_command_source`) | The Windows preamble does not open the log; POSIX preambles are unchanged | [x] merged into int (Agent #310, 16:56 UTC) |
| UR-13l One writer per file for the Windows worker | N | UR-13k | agent `update_job.py`, `update_job_platform.py` (`_worker_script`) | The wrapper writes only its own wrapper log; the worker owns the job log on every platform | [x] merged into int (Agent #311) |
| UR-13o Liveness does not depend on `home` | N | UR-13j | agent `update_job*.py` | A record without `home` is checked like any other job; anything needing the selection refuses with `legacy-update-record` | [ ] in progress (worker) |
| UR-13p Runtime passes the observed worker outcome through, read-only | N | UR-13j | runtime `astrid_runtime/update.py` | A dead worker shows as failed or recovery-needed in a status poll, with install.json unchanged and the schema digest pinned | [ ] PR open (Runtime #39) |
| UR-13g macOS plist pins the install-time HOME | N | UR-13 | agent `astrid/installer/service.py` (`render`, `Service.register`), `tests/fixtures/installer/launchd.plist` | The darwin plist carries HOME; a re-registration keeps a pinned HOME and rewrites a plist from before the pin with HOME | [x] merged into int (Agent #306) |
| UR-13h Update job reads the install record from the home it was accepted under | N | UR-13g | agent `astrid/installer/update_job.py`, `update_job_platform.py` | Recorded home on every platform; a job with no recorded home is refused, and an ambient HOME that differs still finds the install record | [x] merged into int (Agent #307) |
| **Review — before publishing** | | | | | |
| UR-13m Re-aim the release0-to-release1 legs: installed Release 9, then the install command, then the release candidate | N | UR-13 | agent `scripts/ci_journey.py`, `journey.yml` (no new row) | On the release candidate, Release 9 installs, the plain install command moves it to the candidate, and the update record and identity show the candidate | [ ] Release 9 bootstrap passes (UR-R2.1). Seed fails at `seed.json` (legacy 410), see UR-R2.1c |
| UR-13n One fresh row clicks Update now in the candidate's hosted App | X | UR-13 | agent `scripts/journey_fresh_update.py` (Linux fresh row), hosted App build for the candidate | Playwright clicks Update now on the candidate's hosted App page; the same hosted receipt checks pass (`check_journey_evidence.py:227-249`) | [x] `direct-linux-fresh` passes on Agent `88cc447a` (run `42517305848`), browser found under the run HOME (UR-R2.7) |
| UR-R Up to three independent reviews of the integrated candidate | S | round 1: the integrated tasks (decision 10); later rounds: UR-1–UR-13 | all Plan 29 scopes (read-only review) | Each round produces either no blocking findings, or new routed task cards that are done before the next round; see [review rounds](#ur-r-review-rounds) | [ ] round 1 consumed: 2 blocking (UR-R1.1, UR-R1.2), 5 not blocking; heads App 7a59eba8, Agent 043d218d, Runtime cc3ce2f2 |
| UR-R1.1 **BLOCKING** Reason `none` with `self_update` blocks Update now | N | — | app `src/shared/lib/updates/updateOperation.ts` (`installerReasonOf`, `installerUpdateReasonOf`, `canStartInstallerUpdate`) | `{available:true, self_update:true, state:'none', reason:'none'}` gives no reason and Update now can start; a test fails if a Runtime reason lacks an App mapping | [x] merged into int (App #214) |
| UR-R1.2 **BLOCKING** A refusal reason on an up-to-date install shows an update notice and command | N | UR-R1.1 | app `resolveUpdate.ts`, `QuietUpdateNotice.tsx`, `AstridUpdatesSection.tsx` | Decision-table rows for up-to-date with `unsupported-service-manager`, `autostart-off`, `needs-repair`: card `none` or a status line with no command | [x] merged into int (App #214) |
| UR-R1.3 Busy shows Update now disabled, with no install command | N | UR-R1.1 | runtime `update.py` (busy), app `resolveUpdate.ts` | `busy` reads as disabled Update now, not the command, while the POST lock is held | [x] merged into int (App #215) |
| UR-R1.4 A fully local `source` refusal shows its reason | N | — | app `updateStatus.ts` (`checkLocalUpdate`), `UpdateResolutionActions.tsx` | Fully local `{self_update:false, reason:'source'}` with release behind renders the source line | [x] merged into int (App #216) |
| UR-R1.5 `needs-repair` without `self_update` shows the plain repair line | N | UR-R1.2 | app `resolveUpdate.ts`, `AstridUpdatesSection.tsx` (`repairNeeded`) | The `needsRepair` row shows the repair entry, not `--update` | [x] merged into int (App #218); agent brief also says the plain line |
| UR-R1.6 `pin.mjs --require` sets the floor to the release being published | N | — | app `scripts/installer/pin.mjs` (`--require`) | Pin then bump gives `required.release === release`, or the guard refuses a lower floor | [x] merged into int (App #219) |
| UR-R1.7 Every push to `main` gets a `release-guard` result | N | — | app `.github/workflows/test.yml` (concurrency) | The release-guard job is not cancelled by a later push to `main` | [x] merged into int (App #217) |
| UR-R2.1 **BLOCKING** Release 9 legs stop for setup consent (exit 2) | N | UR-R | agent `scripts/journey_version_jumps.py` (`bootstrap_release9`) | Release 9 install passes `--yes`; both legs get past `release9/install-bootstrap.log` | [x] Agent `cand/29-r10` `4070f5bc` (candidate checkout read by the consent probe) |
| UR-R2.1a **BLOCKING** The CI leg passes no `--agent-checkout` | N | UR-R2.1 | agent `scripts/journey_version_jumps.py` (`release9_consent_agent`) | The CI argument names reach the probe | [x] same commit as UR-R2.1 (`4070f5bc`) |
| UR-R2.1b **BLOCKING** Proof on the candidate run | N | UR-R2.1 | agent run | Five direct jobs pass with receipts | [ ] runs `42516232888` (`291b5cbd`): macOS fresh and Windows pass; Linux fresh fails (browser cache, UR-R2.7); both release0 legs fail at seed (UR-R2.1c). Run `42517305848` (`88cc447a`): Linux fresh, macOS fresh and Windows pass; release0 legs fail at seed. Run `42520643111` (`d7dd10cc`, final heads): pending |
| UR-R2.1c **BLOCKING** The release0 seed writes through a legacy route (410) | N | UR-R2.1b | agent `scripts/journey_live_workspace.py` (`seed`, `snapshot`) | Seed uses the Release 9 timeline create and a revision read; proven locally on Release 9 `f4c7a462` seed to candidate `3d19ba9a` snapshot | [x] Agent `ce954ed2` (narrowed per M-INT). **Narrowed:** this covers timeline identity and its bootstrap revision (id and content digest), not composition content. The head pointer is null on Release 9 and on the candidate alike, so it is not used. Composition content is not seeded. Local proof: revision id and digest match, schema digest is the candidate's, preferences and object digest survive. The settled task is stubbed locally, as the local realm has no task |
| UR-R2.1d Commit-based composition content seed (deferred to 0.0.11) | X | UR-R2.1c | agent `scripts/journey_live_workspace.py` (`seed`, `snapshot`) | The release0 seed writes and reads composition content through the commit route, not only timeline identity and the bootstrap revision | [ ] deferred to 0.0.11 (M-INT ruling: smallest authentic route for Release 10; content seed later) |
| UR-R2.4 Status polls start the helper on every OS | N | UR-R2 | runtime `astrid_runtime/update.py` (`UpdateAdmission.status`) | A sequence of polls with no state change starts no helper or PowerShell; test counts launches on darwin and win32 | [x] merged into int as Runtime PR #40 (`60bd111c`). Base `3d19ba9a` launches 21 helpers for 21 polls; fix launches 1. Checks: same failing names as base (not new), windows-realm-publication passes. Re-pinned into Agent `d7dd10cc` and App `cb69a388` |
| UR-R2.2 Refusal reasons relabelled to `inputs-unavailable` | N | UR-R2 | runtime `update.py` (`_helper`) | Legacy reasons keep their label | [ ] deferred (owner decision 16) |
| UR-R2.3 First Update now click after a dead worker only records it | N | UR-R2 | app `updateOperation.ts`; agent `update_job.py` (`reconcile`) | One click starts after a dead worker | [ ] deferred (owner decision 16) |
| UR-R2.5 systemd check needs systemd 251 | N (Plan 30) | UR-R2 | agent `update_job_platform.py` (`finished_result`) | Fails safe below systemd 251 | [ ] deferred to Plan 30 (owner decision 16) |
| UR-R2.6 Bring App `int/29` up to `main` after publish | N | UR-14 | App branch housekeeping | `release-guard origin/main int` passes after the merge | [ ] after publish (M-INT) |
| UR-R2.7 Linux Playwright browser under the run HOME (fix for UR-R2.1b) | N | UR-13n | agent `scripts/ci_journey.py` (`isolated_environment`) | Browser found under the run HOME; focused test | [x] Agent `88cc447a`; proven in run `42517305848` (fresh Linux pass) |
| UR-14 Publish Release 10 | N | all, including UR-R | app `public/install-manifest.json`, `runtime.lock.json` | Owner names the tuple and says go; `public/install*` frozen; not required; canary passes | [ ] blocked: waits on UR-R |
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
- **When repair shows** (advisor, 8 Nov):
  - Only while no update is available. The plain line also applies a newer release, so while one is available, Update now and its secondary command are the only path, with no separate repair row.
  - Only for direct installs (`installType === 'installer'`). Fully local repair isn't defined in this plan.
- **Autostart off:** the card shows the plain line, not `--update`. The plain line respects autostart, so its sentence says to run it and then start Astrid.
- **Chat cards** are UR-4's: their action is "See updates", which opens Settings → Updates. Leave `copy.ts` alone in UR-3.

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

### UR-8b–UR-8d Moved
Release versions, the release log and versions on screen moved to [Plan 31](../31-releases-from-astrid-dev/plan.md), which starts after this plan (owner, 8 Nov 2026). Release 10 publishes as before, through UR-8's guard.

### UR-9 Fully local Update now
- **Independent of the broken path.** The updater runs the installed Agent's `local_update` module and doesn't use the broken `reconcile` path, so it should work on existing installs (from source; to confirm).
- **No recorded reason it was hidden.** `f2eca0bd5` has no reason recorded. Its test name points at the npm route that was since removed.
- **Paths:**
  - Primary: Update now.
  - Secondary: the normal install command (owner decision of 7 Nov).
- **The 30 Oct hide is reversed.** `21fa6391` and `f2eca0bd5` came before the owner's 7 Nov decision 1 ("fully local: Update now through the existing in-page updater"), which supersedes them.
- **Page notice:** `resolvePageUpdateStatus` keeps routing to Settings → Updates, the one place to act (owner decision of 7 Nov). It never offers Update now itself.
- **When the button shows:** by UR-1's one rule, Update now appears only when the status reports `self_update`. The fully local status endpoint (UR-6) reports `self_update: false` with reason `source` when no installed backend exists, so a source-checkout Runtime gets UR-1's source line, never a button that fails. Don't add a new probe or a 503.

### UR-10 End to end
- **Merge the whole lane** in order: `7c9438f55`, `548c8f93f`, `eaa9996de`, `b97c43db8`, `a721da65a`. All five merge cleanly onto Agent main.
- **Fix the remaining mismatches the test finds**, which include:
  - the implicit prepare action;
  - refusal labelling;
  - the Runtime test stub's `launch_status: "started"`, which the Agent never emits.
- **Test setup:** Agent tests already import `astrid_runtime` at the pinned SHA. The test redirects prepare URLs by wrapping `_helper`, with no production change.

### UR-11 `self_update` and reasons
- **Where `self_update` comes from:** the helper's `availability` action lists its supported actions, and old helpers can't, so they read false. Move the probe from Linux-only (`update.py:103`) to every OS.
- **Which actions it requires:** exactly the ones the Runtime's request path calls: `availability`, `reconcile`, `accept`, `launch`, and prepare (sent with no action key). `reconcile` is the action whose absence broke Update now, so it must be included. The Runtime never calls `fail`. Keep one constant beside the calls, with a test that every action the request path sends is in it.
- **Reasons:**
  - Emit `reason` in every state, including `none` when it can update.
  - Keep `busy`, `autostart-off` and `unsupported-service-manager`.
  - Add `needs-repair` (anything unclassified) and `managed-elsewhere` (Pinokio).
  - Source installs keep `source`, the reason the POST refusal already uses (`update.py:163-164`) and the App already reads (`client.ts:200`), so status and refusal share one vocabulary.
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
- **Running the hosted proof:** the journey workflow checks that the candidate's Agent and Runtime match what the App manifest pins. Proving unmerged Agent or Runtime work needs a composed candidate, following the Release skill's "Freeze and compose the candidate" step:
  - Create `cand/29-<task>` branches in App and Agent from the frozen heads, then run the Agent's `scripts/regenerate_runtime_pins.py ... --apply` to repin the Agent's runtime lock and the App manifest together. Check with `pin.mjs --check`.
  - Dispatch `journey.yml` (`workflow_dispatch`) with full SHAs, `manifest_sha256` and the three bootstrap hashes.
  - `cand/*` branches are evidence only. They are never merged; the real pin happens in UR-14.
- **What UR-13 is judged on:** only its three fresh rows (direct-linux-fresh, direct-macos-fresh, direct-windows), each with its hosted receipt. The release0-to-release1 legs belong to the old Release 1 migration and are out of scope (owner decision 6). An aggregate gate failure caused only by those legs doesn't block UR-13.

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

### Round 2 review (UR-R2)

Reviewed on Runtime `3d19ba9a`, Agent `41170fdb`, App `73a8500d` (superseded; see below). Round 2 found one blocking item, fixed; the rest are recorded and not done unless the owner asks.

- **UR-R2.1 BLOCKING (fixed).** The Release 9 legs of the release-candidate run failed with exit 2: `bootstrap_release9` called `journey.bootstrap` without the Agent checkout, so the consent probe never ran, `--yes` was not passed, and Release 9's plain install stopped for setup consent with no terminal. Fix: pass `agent=args.agent_checkout`, with three focused tests (`tests/test_journey_release9_consent.py`). Agent `cand/29-r10` `291b5cbd`; App `cand/29-r10` `26585ed9` (agent pin only). Kept on the candidate branch, not `int`, so promotion takes this exact commit (M-INT).
- **UR-R2.2** Runtime `update.py` `_helper`: refusal reasons other than `busy`, `autostart-off` and `unsupported-service-manager` come back as `inputs-unavailable`. Not user-visible.
- **UR-R2.3** App `updateOperation.ts` `refusalMessageOf`; Agent `update_job.py` `reconcile`: after a dead worker, the first Update now click records the failure (409 `kind: failed`) and a second click starts the update. User-visible: one extra click.
- **UR-R2.4** Runtime `update.py` `UpdateAdmission.status`: every status poll now starts the helper on macOS and Windows; on Windows an unresolved job also starts PowerShell each poll. A cost, not correctness.
- **UR-R2.5** Agent `update_job_platform.py` `finished_result` and `parse_systemd_result`: needs systemd 251+ (`--timestamp=unix`); below that the check fails safe and records nothing. Plan 30 item.
- **UR-R2.6** App `int/29-update-and-release` still holds release 9 and the old tuple. After UR-14, merge `main` back into `int/29-update-and-release` so `release-guard` does not demand release 11.

**Candidate identity (superseded runs are not evidence):** Runtime `3d19ba9a`; Agent `cand/29-r10` `291b5cbd`; App `cand/29-r10` `26585ed9`; manifest sha256 `4771c1e6…`. Earlier runs `42515380385` and `42515533405` are cancelled.

## Resume note (manager state, for compaction)

- **Advisor session:** session_011EzfVzreGCJJQnTuXpbib9 (M-INT).
- **run.yaml:** /root/astrid-dev/plans/29-update-and-release/.otto/runs/plan29-2026-11-08/run.yaml (gitignored), with state.md beside it.
- **Rulings on record:** Runtime #37 merged on verdict (a). Release0 seed: the smallest authentic route, timeline identity and bootstrap revision (UR-R2.1c, narrowed; content seed deferred as UR-R2.1d to 0.0.11). Owner decision 16: fix R2.4 (merged as Runtime PR #40), defer R2.2, R2.3 and R2.5.
- **Current candidate:** Runtime `60bd111c` (int); Agent `cand/29-r10` `d7dd10cc`; App `cand/29-r10` `cb69a388`; manifest sha256 `0b2f8cab…`; release 10, required unset.
- **Current proof:** run `42520643111` (`row=direct`) on the final heads. Round 2 re-check on the three new commits is running.
- **Next, in order:**
  1. Read run `42520643111`: five direct jobs, the evidence gate, and the release0 legs past the seed.
  2. Round 2 re-check result: no blocking finding, or route any finding and re-pin.
  3. Publish per decision 15 only if all proofs pass and round 2 has no blocking finding. Owner go still needed.
- **Open items outside Release 10:** Windows discovery.json race (a Runtime bug issue, not yet opened; needs owner go). Plan 31, Green mains, Plan 30 and catalog clean-up wait for owner go.
