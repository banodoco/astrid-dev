# Tasks — One update path and release

[Plan](plan.md) · [Inputs](inputs.md)

## Release 12 Track A current work

The active task definitions and gates are in [Track A](../../releases/12/fixes.md).

- **A0:** On Agent `91caa12ce` (starting candidate plus the Windows donor merge), the three collection errors from run 42799672641 no longer reproduce: 25 tests collected, with six default-off pack-build tools tests deselected. CI reporting change is pushed in Agent handoff `ec48555d8298d155390ffbb37d1950c3e80b43a4`; integration and Checkpoint A proof remain open.
- **A1:** Agent handoff `ec48555d8298d155390ffbb37d1950c3e80b43a4` includes the Windows donor, recovery tests and VibeComfy pin check. All 259 recovery cases passed across three runs after supplying pinned Node/esbuild and the pinned Runtime admission checkout; this is Linux simulation, and native Windows matrix proof remains. The complete installer-file run reported 1,922 passed, 134 failed, 19 skipped and 95 deselected; failures await the A2 comparison. VibeComfy release branch is `8d065a8fef3dd602d5462e27d8eca088cf4e8262`.
- **A2:** The common Python 3.11 four-way comparison was interrupted for the session move during R10 at 22%; it is incomplete and does not establish parity. Earlier 3.13 runs were stopped as incomparable, R10's 3.13 setup failed before tests, and a separate serial attempt had an invalid temporary-directory setup. R10 pins lifecycle `96360a27a53c4608f780f7b370f747a2aa3c7ca8` in `pyproject.toml`. Restart the affected comparison under orchestrator coordination; local focused results do not replace full CI.
- **A2 blocked — Runtime fixture setup:** A restarted common Python 3.11.17 serial comparison was stopped during R10 at 49% (SIGTERM, exit 143) after review found that noneditable Runtime installs placed `runtime_protocol` in site-packages without the adjacent producer tests required by selected custody fixtures. It is invalid-setup evidence, not a parity result; no later side started. All four environments have since been corrected to import each pinned Runtime checkout editably, and both required producer fixtures import from those checkouts. Restart all four sides only under orchestrator coordination, preserving pins, selectors, timeout and the interrupted log separately.
- **A2 resumed and process fix:** With orchestrator authorization, all four corrected sides restarted serially using Python 3.11.17, verified pins, the same selectors and unchanged timeout; results remain pending. [PR #392](https://github.com/banodoco/astrid-dev/pull/392), commit `a312e2fc153cf1ef7ec173d4ff40b648b008cc24`, added comparison-specific editable Runtime and fixture-origin preflight without changing global setup. Three preflight unit tests, shell syntax and an older-revision skip harness passed; PR checks passed. The interrupted invalid-setup attempt remains separate.
- **A2 custody comparison gap:** Corrected R10 completed with 4,203 passed, 140 failed, 21 skipped and one error; corrected R11 completed with 4,563 passed, 191 failed, 21 skipped and 48 errors. R11's custody fixture errors include `AttributeError` for `_write_owner_grants`, absent from its pinned Runtime `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` but present in R10's pinned Runtime `52ec0578963847693a0df758d9bc1d55325f518f`; base and candidate Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641` also lacks it. The base side has started, candidate remains pending, and these counts do not establish parity. Source-history triage and the complete four-way diff are open.
- **A2 interrupted and recovered:** The corrected base log stopped at 72% at 00:45 UTC on 11 Nov with no exit record; no comparison process existed on the 01:51 check. Its termination cause is unknown and it is not a complete side. A detached recovery attempt was also terminated by the command environment with no exit record. Both partial logs are preserved separately. A fresh base run was started in a persistent command session after re-verifying all pins, Python and fixture imports; candidate follows serially. No partial results are spliced into the diff.
- **A2 resource comparability:** At 02:23 UTC on 11 Nov, the recovered base pytest was running alongside Track B pytest on the shared host. The A2 sides remain serial, but resource conditions across sides may differ. The orchestrator is coordinating host load and will assess any affected rerun after the complete evidence; no parity verdict is made from the partial base run.
- **A2 Node/esbuild coverage gap:** The isolated comparison environments omit `ASTRID_BUILD_TEST_NODE`, `ASTRID_BUILD_TEST_NODE_VERSION` and `ASTRID_BUILD_TEST_ESBUILD`, and their PATH lacks Node. The completed base reports 17 affected IDs: 12 R8 refusal failures, two transaction fixture errors and three missing-node capability failures. R11 shares the 12 R8 IDs, two transaction errors and one missing-node ID; R10 lacks the three newer files but has the generic-host ID. These are setup/coverage observations, not product verdicts. The orchestrator subsequently authorized a fresh controlled four-side comparison with verified Node 22.22.0 and esbuild 0.27.7; absent cases remain explicit, as recorded below.
- **A2 controlled shards:** After a second session interruption, the orchestrator authorized a fresh four-side comparison in identical deterministic module groups, using the verified Node/esbuild inputs across all sides. [Manifest, inventory gaps and method](evidence/r12/a2-sharded/README.md) are recorded; group 001 completed on all four sides with the same one failure and all 18 IDs accounted. The remaining groups and full diff are open. Grouped session fixtures and cross-group ordering limit comparison with a full-suite execution; old unsharded logs are corroboration only.
- **A2 controlled-shard pause:** Groups 001–003 completed on all four sides with exact ID/receipt verification; their candidate failure IDs and messages matched the baselines, and a group 002 teardown error matched base. In group 004, R10 and R11 each passed all 591 IDs, but R11 overlapped another Runtime pytest on the shared host. The supervisor stopped before base as designed; the overlap disposition is recorded below. These partial groups do not establish overall parity.
- **A2 resumed after overlap:** Group 004 R11's receipt is retained as positive baseline observations with the overlap explicitly noted: all 591 IDs passed, with no timeout or incomplete result. This is not a claim that overlap was harmless. After the host cleared, the supervisor resumed base and candidate serially and will stop on renewed contention; the complete comparison and its resource limits remain open.
- **A2 candidate failure in triage:** Group 005's `test_selected_import_reuses_reserved_and_core_namespace_policy[personal]` passed on R11 and base but failed on Agent `ec48555d8298d155390ffbb37d1950c3e80b43a4`: the assertion expects `reserved|collides`, while the error says the selected personal pack must use the canonical personal root. The test is absent on R10. Source and intended-contract triage are open; this is a potential regression, not yet classified as product behavior or test drift.
- **A2 groups 001–006:** [Sanitized per-side receipts](evidence/r12/a2-sharded/batches-001-006/README.md) retain exact outcome IDs, summaries, pins and original-log hashes for the first six groups. Group 005 contains the candidate-only failure above; group 002's candidate teardown error matches base, and group 006's timing-sensitive deadline failure matches all baselines. Group 004's R11 overlap remains a limit. These partial results do not establish overall parity.
- **A4:** App candidate is `2650030c8f78d235ade22f313e1e83746da5482d`. [Run 42888887784](https://github.com/banodoco/astrid-app/actions/runs/42888887784) was cancelled for the pause. [Run 42891034934](https://github.com/banodoco/astrid-app/actions/runs/42891034934) exposed a repeated Settings reason and a hanging credential scan; [42894419956](https://github.com/banodoco/astrid-app/actions/runs/42894419956) identified an unfinished app-state header capture and a missing screenshot output directory. The candidate fixes the directory and adds pass-through routing while retaining fail-closed full-header and body scans (16 focused tests pass with Chromium 148 and Playwright 1.60). [Run 42897172267](https://github.com/banodoco/astrid-app/actions/runs/42897172267) passed its direct job but failed three-products because response bodies became unavailable during navigation; the restart journey remains unproved. An unreviewed navigation-gate prototype is preserved at App `b2507e318a2548a3f26c2df29b1571e3f6a9f47d`; focused tests reported 18 passes, but exact-SHA journey proof and independent race review remain open.
- **A4 blocked — capture race:** Independent review reproduced an inherited race on both App `2650030c8f78d235ade22f313e1e83746da5482d` and prototype `b2507e318a2548a3f26c2df29b1571e3f6a9f47d`: a request emitted while the final DOM inspection is awaited can leave captures unresolved after the initial drain, while `expectClean` returns clean. A source-level header probe and a Chromium probe with a delayed response body caught their sentinels only on a second check. The prototype's 18 existing focused tests passed, but did not cover this race. Review and exact-SHA journey proof are pending; the prototype and earlier journey do not establish a clean scan.
- **A4 candidate:** App `cand/29-r12` was fast-forwarded from `2650030c8f78d235ade22f313e1e83746da5482d` to [`8a52d94dc52d0e6c63fb03cfdda231e8bca3a9e0`](https://github.com/banodoco/astrid-app/tree/handoff/2026-11-10/track-a-token-fixed-point). The navigation prototype and bounded repeat inspection received independent review without blocking findings. On that exact commit 47 focused tests passed twice, including independently with Playwright 1.60 and Chromium 156; 15 selected new regression cases failed on the prototype. `tsc --noEmit` passed. The early Direct Journey on this SHA failed as recorded below, and the restart test is unproved. Page routing disables browser HTTP cache.
- **A4 blocked — early journey:** [Run 42916461654](https://github.com/banodoco/astrid-app/actions/runs/42916461654) on App `8a52d94dc52d0e6c63fb03cfdda231e8bca3a9e0` passed its direct job but failed three-products: two unexpected failures and 12 skipped. The first reported incomplete credential scanning with requests in flight; the second and its retry reported a failed `GET /other` body capture. The restart journey was skipped. Trace diagnosis and repair are in progress; no incomplete capture counts as clean, and this early run does not qualify a later tuple.
- **A4 repair and candidate:** App `cand/29-r12` was fast-forwarded from `8a52d94dc52d0e6c63fb03cfdda231e8bca3a9e0` to [`e72d541de1d65bee74707ca1ae9c2d429ee2f721`](https://github.com/banodoco/astrid-app/tree/handoff/2026-11-10/track-a-token-fixed-point). It aborts gate-owned requests before dispatch while still requiring real terminal events, full headers and observed bodies; it also guards the affected test's reloads. On the exact commit, 53 focused tests, both affected local journeys with Agent `313bbd46f` and Runtime `42ae24aff`, and `tsc --noEmit` passed. Independent review found no blocker: its browser test does not reproduce the actual unload/commit race, and the staged retry is explicitly aborted under the gate, so it proves durable recovery rather than browser-driven cancellation. The CI timing failures did not reproduce locally; the next early journey failed as recorded below.
- **A4 blocked — next early journey:** [Run 42924824236](https://github.com/banodoco/astrid-app/actions/runs/42924824236) on `e72d541de1d65bee74707ca1ae9c2d429ee2f721` passed direct but failed three-products: one failure, one flaky case and 11 skipped. `:416` reported a blocked app-state request without a terminal event; `:2978` had a failed `GET /other` body capture before its retry passed. The scan failed closed. Trace diagnosis and repair are in progress; the restart journey and A4 remain unproved.
- **A4 diagnosis limit:** The exact run's listed trace artifact returned Forbidden on download. Local Chromium 148 probes did not reproduce the missing terminal event; they showed that pagehide requests can begin after the navigation response, so a pre-commit drain alone cannot cover all lifecycle traffic. An interrupted streaming body could not be recovered from CDP. Additional unguarded reloads, helper navigations and page closes were identified. No further fix is claimed; independent advice is assessing the next evidence needed without treating incomplete captures as clean.
- **A4 diagnostic reviewed:** Independent advice recommends sanitized lifecycle evidence before changing terminal policy. [App `ecb873300466f10c756894469cbb47349186b472`](https://github.com/banodoco/astrid-app/tree/r12-a4-second-repair), based on `e72d541`, adds default-off diagnostics and a workflow opt-in without changing capture requirements. Its exact-SHA 59 focused tests passed, including adversarial token/path/query/header/body/error redaction and missing-terminal/body cases; removing the initial drain made the strengthened body-wait test fail. Independent review found no blocker or sensitive data leakage. The logs observe Playwright events, not direct pagehide/beforeunload phases, and may not explain a missing browser event. The coordinated diagnostic-only run is recorded below; A4 remains blocked.
- **A4 diagnostic result:** [Run 42932713990](https://github.com/banodoco/astrid-app/actions/runs/42932713990) reproduced the missing-terminal failure. Sanitized stdout shows the gated app-state request's abort ended after main-frame commit; no terminal event was observed before timeout. [Evidence](evidence/r12/dj-diagnostic-42932713990.md) records the exact inputs and sequence. A bounded repair and regression test remain open; the diagnostic is not a qualification run.
- **A4 protocol probe in review:** [App `0b2a8b85f5f10b0e28895f1e920ce6cdb982e399`](https://github.com/banodoco/astrid-app/tree/handoff/2026-11-11/r12-a4-protocol-diagnostics) adds an exact-version Playwright protocol diagnostic prototype, without changing the gate or workflow. Its instrumented driver passed 59 focused scanner tests with diagnostics off; opt-in Chromium probes checked numeric joins, redaction, collision handling and an underlying `Fetch.failRequest` rejection while `abort()` resolved in both modes. A closed-session rejection is unproved. Independent review is pending; this is diagnostic only and does not fix A4.
- **A4 protocol probe revision in review:** Independent review found that `0b2a8b8` could silently lose observer records and accept incomplete joins. [App `4eb357435cdf617daab22f7f5a18f5acc459e7b9`](https://github.com/banodoco/astrid-app/tree/handoff/2026-11-11/r12-a4-protocol-diagnostics-v2) adds sticky invalidity, sequence/completion accounting and full request linkage checks. Six diagnostic tests, 59 scanner tests, an opt-in Chromium correlation check and `tsc` passed on the exact commit. Independent review cleared the two prior integrity blockers; no CI or A4 fix is claimed.
- **A4 protocol workflow in review:** Independent review cleared the prior observer-integrity and linkage blockers on `4eb3574`. [App `d59b5e78e03607037c9898d57be5bd1e483fcd64`](https://github.com/banodoco/astrid-app/tree/handoff/2026-11-11/r12-a4-protocol-diagnostics-workflow) adds default-off workflow wiring, sanitized diagnostic-only artifacts and post-journey validation. On the exact commit two collector and six instrumentation tests passed, and a real Chromium probe produced three verified joins; 59 scanner tests passed on its unchanged parent. Independent workflow review is pending; no diagnostic CI or A4 fix is claimed.
- **A4 diagnostic evidence blocker:** Independent workflow review found that collector invalid/drop/write state was not persisted for the later verifier, so a dropped record could coexist with a valid-looking stream. Persisting sanitized completion and sticky invalidity, requiring the verifier to reject missing/invalid status, and mixed-valid/invalid negative tests are in progress. The diagnostic workflow is not ready for CI and A4 remains blocked.
- **A4 collector status reviewed:** [App `63a388382cd945ec938b0ce10205baa6fe993343`](https://github.com/banodoco/astrid-app/tree/handoff/2026-11-11/r12-a4-protocol-diagnostics-status) persists sanitized final collector status for the verifier. On the exact commit three collector/status and six instrumentation tests passed; a Chromium capture verified three joins. Tests cover a valid stream with a rejected record, missing/malformed/unfinished status and preservation of the journey's nonzero exit. Independent review found the collector blocker resolved and no new blocker. A fresh per-job directory is assumed, the status is not cryptographically bound to logs, and earlier scanner and protocol limits remain. The coordinated diagnostic-only run is recorded below; no A4 fix is claimed.
- **A4 protocol diagnostic result:** [Run 42954826041](https://github.com/banodoco/astrid-app/actions/runs/42954826041) reproduced the failure and passed its diagnostic evidence verifier. Sanitized stdout joins the blocked request to an underlying `Fetch.failRequest` rejection around navigation commit, with no observed network terminal. [Evidence](evidence/r12/dj-protocol-42954826041.md) records the exact inputs and limits. A bounded repair retaining real terminal evidence is in progress; this diagnostic is not a gate pass.
- **A4 browser lifecycle investigation:** [Source history and local probes](evidence/r12/a4-browser-lifecycle/README.md) compared Playwright 1.60/Chromium 148, 1.61/149 and 1.65/158. Each reproduced stale-route abort resolution despite a rejected browser command and unavailable interrupted body. Playwright 1.65 adds a document-detachment-inferred `requestfailed` even without a CDP terminal; it does not establish a genuine terminal. These probes do not prove the exact CI omission cause or a behavior-preserving fix. No pin or product change was made; A4 remains blocked.

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
| UR-15 Finished storage handoff is normalised once; `install`/`--update` reach the update for the live install (one installation resolver, `installation.py`) | S | UR-14 | agent `astrid/installer/installation.py` (new), `boundary_handoff.py`, `cli.py`, `update_job.py`, `tests/test_boundary_handoff.py:210-212`; M1 and M2 land in one Agent PR with UR-15a | Field fixture `handed-off-release1-r0-live-disk-full`: after normalisation `data_root` is R1 and the journal is archived; `--update` to a newer target ends `updated`. A no-op update fails the post-condition. Fails on `72462b04` first | [ ] open |
| UR-15a Run receipt: exit 0 only if the live release equals the target; `last-run.json` read by terminal, diagnostics and App | X | UR-15 | agent `astrid/installer/outcome.py` (new), `cli.py` single exit; Runtime `diagnostics.py` reads it | `settle()` outcomes `updated`, `already-current`, `repaired` exit 0; `not-updated` exits 3, `failed` and `rolled-back` exit 1; every early return routes through it | [ ] open |
| UR-15b Diagnostics headline with true labels, App reason `self-update-too-old` and copy, disk free space, handoff and normalisation state | X | UR-15a | runtime `astrid_runtime/diagnostics.py`; app `resolveUpdate.ts`, `UpdateResolutionActions.tsx`, `AstridUpdatesSection.tsx` | Each message state has one test fed from a real fixture, including Hannah's state (Release 1, handoff complete); the journey row asserts the installer's headline and exit code | [ ] open |
| UR-15c INSTALL_STATES with an exhaustive `UPDATE_TRANSITION`; every-state test; re-aim the release0-to-release1 legs from a real R0 handoff, renamed after their start state | X | UR-15 | agent `tests/test_update_from_every_state.py` (new), `scripts/journey_version_jumps.py`, `scripts/journey_fresh_update.py` (drop the handoff-state precondition), `journey.yml` | Adding a state without a transition fails CI; the re-aimed leg starts from R0 → handoff → `--update` and passes with receipts | [ ] open |
| UR-15d Stop and disable the R0-era Runtime for the realm when normalising; receipt fails `other-runtime-running` if more than one is live | N | UR-15 | agent `installation.py`, `cli.py`; Runtime per-realm owner lock (M4a) | After normalisation exactly one Runtime is live for the realm; R0 files kept while rollback is offered | [ ] open |
| UR-15e Owner decision pending: rollback only until the first successful update after a handoff | — | UR-15 | — | Owner decision, not built yet. Pruning of retained R0 waits for it | [ ] waiting on owner |
| UR-15f Honest headline when an update reached the target but a second copy is still running ("Astrid updated to Release N, but another copy of Astrid is still running…" plus the next step) | X | UR-15a | agent `astrid/installer/outcome.py` (headline copy) | Headline for updated-plus-second-copy names the new release and the second copy; test fed from a real fixture. Needed before the Release 11 candidate | [ ] open, before Release 11 |
| UR-15g A stale R0 discovery file with no birth id blocks later updates once its pid is reused | S | UR-15 | agent `astrid/installer/installation.py` (discovery liveness, :96-122) | A discovery file with an unrelated live pid and no birth id is treated as stale, not live. Proof: unrelated pid, R0 label not running → update proceeds | [ ] open (follow-up, not release 11) |
| UR-15h Rollback after a retired R0 leftover re-enables R0's label | N | UR-15 | agent `astrid/installer/installation.py`, `cli.py` (`--rollback`) | After retire then `--rollback`, R0's label is enabled and running | [ ] open (follow-up, not release 11) |
| UR-15i The second-Runtime check runs in every mode (local update and update-job helpers too), and scans every retained root, not only R0 | N | UR-15 | agent `local_update.py`, `update_job.py` | A second live Runtime is refused or retired in every install mode | [ ] open (follow-up, not release 11) |
| UR-15j UX pass over every install, update, update-failure and repair path (decision 17): App page and Settings, installer terminal, diagnostics file, on mac, Linux and Windows | S | UR-15, UR-15a, UR-15b, UR-15c, UR-15f | app, installer, diagnostics copy | Every path offers "Copy instructions for your agent" and manual steps; every failure is plain and points to Download diagnostics and the install log path; success copy only on exit 0; small fixes as commits on int, big ones as task cards | [ ] open, runs before Release 11 is composed |
| UR-15l-1 Local App path: a finished handoff is normalised through the UR-15 resolver, or refused with exit 3; it never runs against R0 data (local review a1) | S | UR-15 | agent `local_update.py` (~:203-218) | Hermetic: completed-handoff local install updates R1 data; R0 never written; a failed normalisation refuses with exit 3 and changes nothing | [ ] open, Release 11 |
| UR-15l-2 Local path settles: exit 0/3/1 like the installer, last-run.json, plain failure lines with the Next/Details lines, and an interrupted-update restore announced (local review a2, a3, a4, a9) | X | UR-15l-1 | agent local-update settle path | Hermetic: no-op local update exits 3; a reaching update exits 0 with "updated"; every local non-zero line ends with Next and Details | [ ] open, Release 11 |
| UR-15l-3 Local App pages: the Latest line reads the served release; Update now in preview is registered or not offered; live "Astrid updated" on local pages (local review a6, a7, a8) | X | UR-15k | app `diagnosticsDownload.ts`, preview route, `useInstallerUpdate.ts` | Vitest: served release shown; preview route tested; instance change on a local page shows the updated line | [ ] open, Release 11 |
| UR-15l-a5 Local agent brief and manual line naming `npm run update` instead of `curl … --update` | — | Hannah's decision | app copy, agent brief | Waits for the owner's decision | [ ] waiting on owner |
| UR-15k Open astrid.haus pages show an update result live (no reload, no click): "Astrid updated: Release N → Release M" briefly, then up to date; not-updated block live too (owner, Hannah, via M-INT) | X | UR-15b | app `updateOperation.ts`, `RuntimeConnectionProvider.tsx`, Updates surfaces; Playwright fresh-update row | Vitest: instance change from Release 10 to 11 shows up-to-date with no user action; Playwright: the open page shows the updated state within 30 s with no reload | [ ] open, part of Release 11 |
| M4 (rest) One Runtime per realm beyond UR-15d, version pruning, disk preflight, disk-full health | N | UR-15 | — | Recorded as findings; not release-blocking unless review says so | [ ] deferred to Release 11 review |
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
| UR-R2.1c **BLOCKING** The release0 seed writes through a legacy route (410) | N | UR-R2.1b | agent `scripts/journey_live_workspace.py` (`seed`, `snapshot`) | Seed uses only the public timeline resource served over HTTP; proven through the served configuration (`authoring_profile` astrid) | [x] Agent `6e9c4f9c`. **Narrowed:** timeline identity and head (`head_revision_id`, the served editable bootstrap head), not composition content. The served create omits `revision_id` and `content_digest`, which the earlier seed read. Served proof, run once: seed on Runtime `f4c7a462` (Agent `709492fa`), snapshot on `52ec0578` (candidate Agent), one realm. Head survives the upgrade; name, preferences, CAS digest and schema digest match. Composition-content seed deferred (UR-R2.1d) |
| UR-R2.1d Commit-based composition content seed (deferred to 0.0.11) | X | UR-R2.1c | agent `scripts/journey_live_workspace.py` (`seed`, `snapshot`) | The release0 seed writes and reads composition content through the commit route, not only timeline identity and head. Also restores a user-authored marker in the content (UR-R2.8, folded in) | [ ] deferred to 0.0.11 (M-INT) |
| UR-R2.4 Status polls start the helper on every OS | N | UR-R2 | runtime `astrid_runtime/update.py` (`UpdateAdmission.status`) | A sequence of polls with no state change starts no helper or PowerShell; test counts launches on darwin and win32 | [x] Runtime PR #40 (`60bd111c`). Base `3d19ba9a` launches 21 helpers for 21 polls; fix launches 1 |
| UR-R2.9 **Non-blocking, user-visible (fixed)** A failed availability probe was cached for five minutes | N | UR-R2.4 | runtime `astrid_runtime/update.py` (`_status_availability`, `_probe_availability`) | A failed probe re-runs on the next poll; a settled job uses the 300 s refresh | [x] Runtime PR #41 (`52ec0578`), with tests that fail on `60bd111c`. Re-reviewed clean |
| UR-R2.10 Finished job kept the 30 s refresh | N | UR-R2.9 | runtime `update.py` | Only launching or active jobs use 30 s | [x] folded into PR #41 |
| UR-R2.2 Refusal reasons relabelled to `inputs-unavailable` | N | UR-R2 | runtime `update.py` (`_helper`) | Legacy reasons keep their label | [ ] deferred (owner decision 16) |
| UR-R2.3 First Update now click after a dead worker only records it | N | UR-R2 | app `updateOperation.ts`; agent `update_job.py` (`reconcile`) | One click starts after a dead worker | [ ] deferred (owner decision 16) |
| UR-R2.5 systemd check needs systemd 251 | N (Plan 30) | UR-R2 | agent `update_job_platform.py` (`finished_result`) | Fails safe below systemd 251 | [ ] deferred to Plan 30 (owner decision 16) |
| UR-R2.6 Bring App `int/29` up to `main` after publish | N | UR-14 | App branch housekeeping | `release-guard origin/main int` passes after the merge | [x] fast-forwarded to `main` (`1db36e66`) by git push; likewise Agent (`72462b04`) and Runtime (`21df9bfb`) |
| UR-R2.7 Linux Playwright browser under the run HOME (fix for UR-R2.1b) | N | UR-13n | agent `scripts/ci_journey.py` (`isolated_environment`) | Browser found under the run HOME; focused test | [x] Agent `88cc447a`; proven in run `42517305848` (fresh Linux pass) |
| UR-14 Publish Release 10 | N | all, including UR-R | app `public/install-manifest.json`, `runtime.lock.json`; astrid-dev `plans/releases.md` | Owner names the tuple and says go; `public/install*` frozen; not required; canary passes | [x] published 2026-11-08 (owner go): Agent #318 → `72462b04`, Runtime #42 → `21df9bfb`, App #222 → `1db36e66`; served manifest release 10 (agent `6e9c4f9c`, runtime `52ec0578`); canary run `42527536657` success. **Reopened:** `install --update` is a no-op on handed-off installs (field failure, see UR-15) |
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

- **Start here on a new machine:** [handoff.md](handoff.md) holds the goal, the gate, the current tuple, the next steps, who's who and the evidence index (2026-11-10).

- **Reopened 2026-11-08 after a field failure on Hannah's Mac.** Release 10 is live, but `curl -fsSL https://astrid.haus/install | sh -s -- --update` exits 0 and installs nothing on a machine that completed the Release 1 storage handoff. The Completion assessment in astrid-dev #137 is withdrawn. Canary receipt for the publish: run `42527536657` (success). Review: `plans/29-update-and-release/reviews/field-failure-2026-11-08.md` on branch `advisor/plan29-field-failure-review`.
- **Plan 29 is active again.** UR-15 to UR-15d are open. The next release is Release 11 (0.0.11, patch), and it publishes only after a field receipt from Hannah on her Mac.


- **Status: complete.** Release 10 (0.0.10) is published and the served manifest reads release 10 (agent `6e9c4f9c`, runtime `52ec0578`, not required). Completion PR astrid-dev #137 is merged.
- **Published mains:** Agent `72462b04` (PR #318), Runtime `21df9bfb` (PR #42), App `1db36e66` (PR #222). `int/29-update-and-release` in each repo is fast-forwarded to its main.
- **Deferred and unproven (see the completion assessment in #137):** composition-content seed (UR-R2.1d, 0.0.11); review items UR-R2.2, UR-R2.3, UR-R2.5 (Plan 30), UR-R2.8, UR-R2.11; Pinokio, fully local and older-Linux setups (Plan 30); the Windows discovery.json race (not yet filed as an issue).
- **Advisor session:** session_011EzfVzreGCJJQnTuXpbib9 (M-INT).

## Release 12 progress

Status as of 20:42 UTC. Rows are recorded as reported; the bucket-A record is [PR #203](https://github.com/banodoco/astrid-dev/pull/203).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Bucket-B fix rows** | | | | | |
| Installer and diagnostics, 26 ids (includes the 6 candidate-only ids in `test_installer_app_update.py`) | — | — | `test_installer_app_update.py` | 26 ids | IN PROGRESS: 18 of 26 passing earlier; remaining work in progress on `fix/r12-autostart` |
| H3 endpoint, 14 ids | — | — | — | 14 ids | OPEN: the worker reports they pass at `f12b35d3d`; cause not yet established (read-only investigation in progress) |
| **Review rows** | | | | | |
| R1 (installer): refusal after the old Runtime stopped reports exit 3, should be exit 1 | — | — | installer | — | OPEN |
| R2 (installer): leftover journal after a rolled-back install may refuse forever | — | — | installer | — | OPEN, check first |
| R3 (Agent tests): runtime-not-running test and scoped fixture | — | — | Agent tests | — | DONE at `96fc740`, accepted |
| R4 (Agent): missing-input message names the wrong path | — | — | Agent | — | OPEN |
| R5 (Runtime): POST reason for malformed choices | — | — | Runtime | — | DONE at `9b4d45d`, accepted (no contract change) |
| R6 (Runtime): legacy `preferences.autostart` never written by a released Agent | — | — | Runtime | — | DONE at `40e41b2`, accepted |
| R7 (Runtime): skip guard pins test ids and exception type | — | — | Runtime | — | DONE at `2ccaf31`, accepted |
| R8 (App): release-guard checks pinned SHAs | — | — | App | — | DONE at `73685aa`, accepted |
| R9 (App): autostart-off card uses `localBuild` | — | — | App | — | DONE at `0531948`, accepted |
| R10 (App): pack re-poll key includes runtime release | — | — | App | — | DONE at `0ec81f1`, accepted |
| R11 (App): vendor-lock check at `744cf248` | — | — | App | — | OPEN, not confirmed |
| R12 (App): acknowledgement-unknown title agrees with body | — | — | App | — | DONE at `42f6fa9`, accepted |
| R13 (App): plain policy refusal never shows recovery-needed | — | — | App | — | Checked: no. Recorded as a note |
| R13b (Runtime and App): recovery-needed reads busy, or echoes the policy reason | — | — | Runtime, App | — | DONE: Runtime at `9ad827c` and `a23011f`, accepted; App recovery-card fix at `c134772`, accepted |
| R14 (Runtime): Windows no-task-folder gap | — | — | Runtime | — | NO: not reachable from release 10 or 11. Goes to Plan 30 |
| **Other rows** | | | | | |
| Pinokio fully-local install-type guard | — | — | App | — | DONE at `e588909` and `1101e01`, accepted. Launcher derivation fix at `810e326`, accepted |
| Hosted-origin setup in two tests | — | — | Agent tests | — | DONE at `84d8f4e`, accepted |
| Windows PowerShell test and copy | — | — | Agent tests, App copy | — | DONE at `ca95aaf` and `87df2bc` (copy wording fix pending confirmation) |
| 17 regressions from `871bb95` (`installCommand --yes`) | — | — | — | 17 regressions | OPEN: narrowed fix in progress on `cand/29-r12` |
| Hang check (CI unit shards 1 and 8) | — | — | CI | — | Shard 1 cause found, `opt_in` at `e825657`. Shard 8 not confirmed. Hang check worker still running |
| Shakedown run: `journey.yml` run `42694815514` on `harness/29-r12` (row=direct, head `bbdaca8e`) | — | — | `journey.yml` | run `42694815514` | IN PROGRESS |
| Plan 39 bucket-A record: [PR #203](https://github.com/banodoco/astrid-dev/pull/203) | — | — | plans | — | OPEN, not merged |
| **Plan 30 items (non-blocking)** | | | | | |
| Windows refusal matched by message text; dead `except` clause; null choices; check order in status; transient 404 flag; remaining Windows-no-task-folder gap (R14) | — | — | Plan 30 | — | Recorded for Plan 30, non-blocking |
| **Release 12 gate notes** | | | | | |
| Inherited App vitest files and three-products expectations: "inherited, not blocking" is REVERSED | — | — | App vitest (17 inherited files); three-products expectations | — | Both are now release-12 gate items. The earlier "inherited, not blocking" call on the 17 inherited App vitest files and on the three-products expectations no longer holds |
| App journey failures: App Direct Journey and three-products (run `42731095228`, App `c79bc16fb`) | — | Astra deep dive verdict | App journey tests | run `42731095228` | GATED on the Astra deep dive verdict. Verdict: test lag behind product changes; the fix is tests only. NOT waved through as "fails on main too" |
| Agent journey matrix | — | — | Agent journey matrix | — | Any failure gets fixed, whether or not main has it |
| Agent CI shard setup failures (run `42721392857`, Agent `0f792afb1`) | — | Plan 39 | Agent CI shards | run `42721392857` | Stays a Plan 39 record, with the evidence list. Plan 39 still waits. Record only |
| Suspect-group baseline diff (`editorial.arrange`, `raw_command.renderer`, `external_pack.demo`) | — | — | Suspect groups | — | Still BLOCKS on any release-12 regression it finds |
| **Release 12 later work (recorded 2026-11-10; round 2 update)** | | | | | |
| Fix 3: the reference realm seeds through the guarded `commit_timeline` | — | — | Agent; branch `r12/quick-journey-realm`, commit `11030fde6` | Not recorded here | [x] landed in the Agent candidate at `90372f0ec` |
| Windows installed git: `ASTRID_GIT_EXECUTABLE` recorded at install | — | — | Installer; branch `r12/windows-installed-git` at `b1523f881` (hardening), merged into `cand/29-r12` with `--no-ff` at `c87b3c131` | Base `aa5bc442f`: 25 failed, 717 passed, 51 errors. `bebb4a4`: 25 failed, 729 passed, 51 errors. 77 pre-existing, per the record; 0 regressions. Re-run at `b1523f881`: done, 0 regressions (correction, 11:42Z round 3) | [x] landed. Hardening in `b1523f881`: (1) a recorded git without the exec bit falls back to PATH lookup; (2) a broken or non-git candidate, or a failing `git --version`, at install records nothing and logs one line |
| P1 follow-up: deliberate pack refresh | — | — | Pack-refresh ack, single worker; branch `r12/p1-deliberate-refresh` at `882abbe305`, merged into `cand/29-r12` with `--no-ff` at `142f9a92f` | Real-Runtime repro `tests/integrations/test_generic_host_pack_refresh_runtime.py` fails at `90372f0ec` and passes at head | [x] landed. Cause: the single-worker pack-refresh ack re-registered non-deliberately after `discover()`, so the epoch fence locked the host. Likely the cause of the matrix task-follow rows, and probably of the fresh and r11 "not registered" results (unproven) |
| Agent CI comparison: run `42760780918` (Agent `aa5bc442f`) vs R10 run `42602166253` | — | — | Agent CI | runs `42760780918`, `42602166253` | [x] measured: 398 regressions in 15 clusters (162 with no baseline). All traced to commits already in R11 `a105de3a`, with no environment change |
| Agent CI product regressions on `r12/r10-regressions`: (a) element_schema fails open for moved am-* elements; (b) 15 shipped local effects unregistered; (c) comfy_wrap lost its GPU mapping | — | — | Agent; branch `r12/r10-regressions` | — | [ ] pending: being fixed on `r12/r10-regressions` |
| VibeComfy COMBO/CHOICE question | — | — | VibeComfy | — | [ ] open |
| Agent CI intended-change clusters (about 330 tests) and Mypy +153 (Nov 5 port debt that R10 never measured) | — | — | Agent CI | — | [ ] WAITING ON HANNAH: fix in R12, or record for Plan 39 |
| Harness `harness/29-r12` at `1b85aed841c5a16e6623e1a4495e0428efead73c` | — | — | Harness; (A) post-check ownership hook; (B) runtime-side registration gate plus R11 pack seeding | Not recorded here | [ ] recorded at this sha, including: existing-pack Runtime-current gate; full task, host and registration diagnostics; named R11 baseline gate skip |
| Open: r12/r10-regressions, then final Agent sha | — | r12/r10-regressions | Agent | — | [ ] open |
| Open: final round on one tuple: ci.yml plus lanes.yml, App Tests, Direct Journey, App lanes, full matrix on harness `1b85aed841c5a16e6623e1a4495e0428efead73c` | — | final Agent sha | — | — | [ ] open |
| Hannah's decisions on `:426` and `:444` (11:10Z) | — | — | App Direct Journey; three-products | — | [x] decided. See the round 3 section below |
| Open: default-floor test `test_the_default_floor_matches_the_runtime` | — | — | — | Integration-marked: it runs in the final `lanes.yml` integration lane, not in the unit shards. Check against Release 10 | [ ] open, to check against Release 10 |
| Plan 39 and release notes: Windows git over ssh needs a follow-up (`ASTRID_SSH_EXECUTABLE`) | — | Windows installed git (landed) | Plan 39 record; release notes | — | [ ] open |
| Owner decision (Hannah, 10 Nov 2026): Agent CI against Release 10 | — | Plan 39 D8 | Agent CI `42760780918` vs `42602166253` | [Plan 39 evidence](../39-green-mains/evidence/release-12-r10-diff.md) | [x] Release 12 fixes every product regression against Release 10 and the `ASTRID_TEST_LIFECYCLE_CHECKOUT` CI setting. About 306 stale or test-infra tests and the Mypy debt move to Plan 39 AT1.1–AT1.7 and AT2; for those, no-regression is judged against served release 11 and `main` |

## Release 12 round 3 (state at 11:42Z, 2026-11-10)

Rows below are recorded as reported at 11:42Z. A row marked `[ ]` is not yet proven.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Owner decisions (Hannah, 11:10Z)** | | | | | |
| Direct Journey `:426` keeps the user's draft visible on a second-writer conflict | — | — | App Direct Journey | — | [x] landed in App `cand/29-r12` at `e3951859b` (merge of the keep-draft fix; no pin change) |
| three-products `:444` (agent task output via `timelines publish`, unshipped) | — | — | App three-products | — | [x] test removed at `01b6b43c2` |
| Stale Agent tests and Mypy debt | — | Plan 39 D8 | Agent CI | — | [x] stay on Plan 39 (D8). No R12 work on them |
| **Landed** | | | | | |
| CI lifecycle-checkout fix | — | — | CI; branch `r12/ci-lifecycle-checkout` at `b2e13e68b` | — | [x] merged into Agent `cand/29-r12` as `6e2e26d53` (`--no-ff`) |
| Harness R11 baseline task | — | — | Harness; branch `r12/harness-r11-baseline-task` at `ecbed4af9` (fast-forward of `harness/29-r12`) | Harness tests 208 → 219 passed | [x] the R11 baseline on non-Linux expects the shipped refusal, named and visible in the receipt and the job log |
| Windows installed git hardening re-run | — | — | Installer; `b1523f881` | 0 regressions | [x] done (corrects the earlier Windows row: the re-run is done, 0 regressions at `b1523f881`) |
| **New product bugs from shakedown matrix run `42804452163`** (App `00c085c40`, Agent `142f9a92f`, harness `1b85aed84`) | | | | | |
| (a) Every fresh install fails on every platform: the installer bootstrap imports `jsonschema` through the Windows-git change `b1523f881`. `astrid/installer/tools.py` imports `_git_executable` from `astrid.core.pack.install`, which pulls in `canonical.py` and `jsonschema` | — | — | Agent `astrid/installer/tools.py`, `astrid/core/pack/install` | — | [ ] pending. Fix in progress on `r12/installer-bootstrap-imports` |
| (b) Selected-pack tasks are refused off Linux with "stable selected pack capture requires Linux file lease support" (`_unavailable_pack_capture` in `generic_host.py`, introduced in `2caeb813fa`, already in R11; R10 did not have it) | — | — | Agent `generic_host.py` | — | [ ] pending. Fix in progress on `r12/portable-pack-capture` |
| **Test drift** | | | | | |
| three-products `:2970` is test drift, not a product regression. Auto single-owner recovery replaced the "Recover saved edits" button (`02db9c360` added it, `7b33f8f50` deleted it, `4394b74a1` mounted auto recovery) | — | — | App three-products | — | [ ] pending. Test fix in progress on the App worker |
| **In progress** | | | | | |
| Agent product regressions on `r12/r10-regressions`: comfy_wrap GPU mapping, 15 hidden local effects, VibeComfy COMBO/CHOICE | — | — | Agent; branch `r12/r10-regressions` | — | [ ] pending |
| Schema fail-closed | — | — | Agent; branch `r12/r10-schema-fail-closed` | — | [ ] pending |
| Default-skills check | — | — | — | — | [ ] pending |
| **Process** | | | | | |
| The Windows-git proof missed `tests/test_installer_bootstrap_imports.py`. Installer proofs now run every `tests/test_installer_*.py` | — | — | Installer proof procedure | — | [x] process changed |

## Release 12 round 4 (state at 13:45Z, 2026-11-10)

Rows below are recorded as reported at 13:45Z. A row marked `[ ]` is not yet proven. Candidate SHAs are the `cand/29-r12` heads named in each row.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Agent merges since `6e2e26d53` (all `--no-ff` into `cand/29-r12`; candidate `35c170e39`)** | | | | | |
| Installer bootstrap imports (`946b92d33`): the git lookup helpers move to a dependency-free module | — | Windows installed git (landed) | Agent `astrid/installer/tools.py`, `astrid/core/pack/install` | — | [x] merged. [ ] install proof pending the next matrix run |
| r12/r10-regressions (`comfy_wrap` GPU mapping, 15 hidden local effects, VibeComfy binding) | — | — | Agent; branch `r12/r10-regressions` | — | [x] merged. [ ] proof pending the next Agent CI run |
| r12/lanes-collection: stale `FOLEY_REFUSAL_CODE` import removed; `lanes.yml` fetches pinned Runtime commits | — | — | Agent `lanes.yml` | — | [x] merged. [ ] proof pending |
| r12/r10-schema-fail-closed: moved motion elements fail closed with a named dependency | — | — | Agent element schema | 377 previously failing tests now pass, none new | [x] merged. [x] measured: 377 fixed, 0 new failures |
| r12/git-lookup-hardening (review blockers 2 and 3) | — | Review round 1 | Agent git lookup | — | [x] merged. [ ] proof pending the review round 2 run |
| r12/portable-pack-capture: selected packs run from a verified, owner-only private snapshot off Linux; Linux lease path unchanged | — | — | Agent `generic_host.py` | — | [x] merged. [ ] proof pending (off-Linux pack capture not yet run in a keep-going job) |
| r12/linux-service-home | — | — | Agent Linux service | — | [x] merged. [ ] proof pending |
| r12/host-registration-marker: ready marker republished after every re-registration; SDK attach uses validated owner credential | — | — | Agent host registration; SDK attach | — | [x] merged. [ ] proof pending |
| r12/windows-pack-publish: journaled Windows collection exchange; POSIX unchanged | — | — | Agent Windows pack publish | — | [x] merged. [ ] Windows pack add not yet proven in a keep-going run (keep-going #3 failed Windows at pack add, before this sha) |
| **Harness** | | | | | |
| Harness `harness/29-r12` at `0e3c456ee`: R11 ready-wait (`eaafa56cd`); probe owner fix; probe scopes fix (`1a1892245`); keep-going sub-step reporting (`0e3c456ee`) | — | — | Harness | — | [x] recorded at `0e3c456ee`. [ ] probe fixes proof pending the next keep-going run |
| **App** | | | | | |
| Direct Journey `:426` keep-draft (cand `e3951859b`) | — | — | App Direct Journey | — | [x] in cand `e3951859b`. [ ] proof pending the App lanes |
| `:444` test removed (`01b6b43c2`) | — | — | App three-products | — | [x] removed. No pinned Agent ships the capability |
| `:2970` / `:2886` recover-retry (`4e94b5a93`) | — | — | App three-products | — | [x] committed at `4e94b5a93`. [ ] proof pending |
| r12/app-conflict-tests, including the `:449` product fix (cand `31e40152b`) | — | — | App conflict tests | — | [x] in cand `31e40152b`. [ ] proof pending |
| App re-pins through the then-current Agent sha | — | Agent `35c170e39` | App pins | — | [ ] currently pinned to `35c170e39`. Pending the next re-pin |
| **Owner decisions (Hannah)** | | | | | |
| `:426` keeps the user's draft visible | — | — | App Direct Journey | — | [x] decided |
| `:444` test removed (no pinned Agent ships the capability) | — | — | App three-products | — | [x] decided |
| D8: stale tests stay on Plan 39 | — | Plan 39 D8 | Agent CI | — | [x] decided |
| `:708` keeps the product's auto-reload after a restart; the test is changed to prove it | — | — | App | — | [x] decided. [ ] test change pending (`r12/app-dj-round2`) |
| **Review rounds** | | | | | |
| Review round 1: 3 blockers. Blockers 2 and 3 fixed in `r12/git-lookup-hardening`; the refresh binding is in flight | — | — | Agent; App | — | [ ] open. Blocker fix for the refresh binding in flight |
| Review round 2: 1 blocker, the bundled/personal snapshot collision | — | Review round 1 | Agent snapshot | — | [ ] in flight (`r12/snapshot-bundled-packs`) |
| **Keep-going results** | | | | | |
| Keep-going #2 (run `42824167156`), fresh install: direct-linux passed end to end, the first green journey row of R12 | — | — | Keep-going journey | — | [x] direct-linux green. [ ] macOS failed on the chiptune snapshot collision (open). [ ] Windows packs add fixed in `35c170e39`, not yet re-run |
| Keep-going #3 (run `42825563080`, Agent `306c7b065`): Linux, every sub-step | — | — | Keep-going journey | — | [x] every Linux sub-step passes |
| Keep-going #3, macOS: pack add, readiness, submit and hot refresh | — | — | Keep-going journey | — | [x] pass |
| Keep-going #3, macOS: follow and settled outputs | — | Snapshot collision | Keep-going journey | — | [ ] fail on the snapshot collision (open) |
| Keep-going #3, Windows: pack add | — | — | Keep-going journey | — | [ ] fail at pack add. Fixed in `35c170e39`, after this pin; not yet re-run |
| **Open items** | | | | | |
| `r12/snapshot-bundled-packs` (snapshot collision) | — | — | Agent | — | [ ] open. Blocks macOS follow and settled, and review round 2 |
| `p1-refresh-binding` | — | Review round 1 | Agent; App | — | [ ] in flight |
| Schema cache (Luna) | — | — | — | — | [ ] open. Non-blocking |
| `r12/app-dj-round2`: `:708` test change; `:449` B's normalized transition; `:2893` non-visual preview-revision attributes | — | — | App | — | [ ] pending |
| Full 11-row matrix on the final tuple | — | Final Agent sha, App re-pin | Matrix | — | [ ] pending |
| Final round | — | Full 11-row matrix | — | — | [ ] pending |
| Lanes: no install/update breakers (R11 parity); recorded on Plan 39 | — | — | Lanes | — | [x] recorded on Plan 39 |

## Release 12 round 5 (state at 17:00Z, 2026-11-10)

Rows below are recorded as reported at 17:00Z. A row marked `[ ]` is not yet proven. The full picture and the next steps are in [handoff.md](handoff.md).

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Agent (all `--no-ff`)** | | | | | |
| `r12/snapshot-bundled-packs` (review round 2 blocker) | — | — | Agent snapshots | Pack and provenance tests: same 17 local failures as `29fbd08c0`, 16 more passing | [x] on `cand/29-r12` at `313bbd46f` |
| Review round 3 on `87d1fbbc4..313bbd46f` | — | — | Agent | [review-round3.md](evidence/r12/review-round3.md) | [x] done: 3 blockers (2×P1 personal snapshots, P2 stale marker) |
| `r12/personal-pack-snapshots` `cbf7b4240`, `r12/marker-fence` `bcb5ac48f`, `r12/schema-cache-invalidation` `7d637370a`, `r12/windows-readonly-cleanup` `989cd0f6c`, `r12/pack-home-update-handoff` `b2dc24ddb` | — | Review round 3; matrix `42835188782` | Agent | Each has regression tests that fail before and pass after | [x] merged on `r12/cand-next` `733ac5a43`. [ ] before/after comparison ([method](evidence/r12/agent-comparison.md)); [ ] push to `cand/29-r12`; [ ] review round 4 |
| **Harness** | | | | | |
| `harness/29-r12` `b550ecadf`: autostart-off reads the Runtime's `details.reason`; HOME bound and recorded for the R11 baseline | — | Matrix `42835188782` | Harness | Harness tests: the 2 remaining failures also fail at `0e3c456ee` | [x] pushed. [ ] proof in the final matrix |
| **Matrix** | | | | | |
| Full matrix `42835188782` (Agent `313bbd46f`, App `ecd0b0cf1`) | — | — | Matrix | [verdicts](evidence/r12/matrix-42835188782.md) | [x] 4 of 11 green; every failing row has a root cause and a fix or rerun. Not a final-tuple proof |
| **App** | | | | | |
| Direct Journey rounds 3–5 (`723025f60`, `26819d552`, `212cf22c9`), merged up to App `e1d42be39` | — | — | App | [dj-round4.md](evidence/r12/dj-round4.md), [dj-round5.md](evidence/r12/dj-round5.md) | [x] merged; tsc clean, touched vitest 117/117. Two product bugs fixed: Keep my changes overwrote the durable draft; Save them did not reopen the retained conflict |
| Early Direct Journey `42849600626` on `e1d42be39` | — | Rounds 3–5 | App | direct-journey 40 pass / 1 fail; three-products 1 pass / 2 fail / 11 skipped | [x] round 6 pushed as `r12/app-dj-round6` `daf30bd9b` ([evidence](evidence/r12/dj-round6.md)): `:1189` env, `:449` and `:2995` test drift, no product change. [ ] merge, `tsc`, early Direct Journey |
| App Tests `42836156052` | — | — | App | vendor-lock check: lock pinned `aa5bc442f` | [x] root cause found: the vendor lock is not re-synced on re-pins; CLI surface byte-identical (dry run `c6454fcdc`, held). [ ] the final re-pin commit regenerates it |
| **Lanes and Plan 39** | | | | | |
| Lanes integration, 659 failures | — | — | Agent lanes | [Plan 39 record](../39-green-mains/evidence/lanes-integration-triage.md) | [x] no install/update breakers at R11 parity; recorded on Plan 39 ([PR #336](https://github.com/banodoco/astrid-dev/pull/336)) |
| **Final round** | | | | | |
| One re-pin commit (pin, vendor lock, checks), then App Tests, Direct Journey, App lanes, full matrix on `b550ecadf`, Agent `ci.yml`/`lanes.yml` vs R10 | — | Final Agent sha; Direct Journey 0 failures | All | — | [ ] pending |

