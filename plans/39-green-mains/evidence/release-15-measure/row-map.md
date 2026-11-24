# Plan 39 row map: what happens to every row when Plan 39 becomes "Runtime and App main green"

Read-only research, 24 November 2026. No repo, PR, comment or workflow was changed.

**Sources.** astrid-dev `origin/main` (bd4c3e1). Plan 39 rows: `plans/39-green-mains/tasks.md` (cited as `T:N`). Plan 91: `plans/91-agent-main-green/tasks.md` (`P91:N`), `plan.md`, `inputs.md`, and `evidence/release-15-b324d7c1/` (`assignment.json`, `ci-failing-ids.tsv`, `lanes-failing-ids.tsv`, `wave-c-cards.md`, `prune-candidates.md`). Plan 31 tasks. Measurements: `runtime-green/REPORT.md`, `clusters.md`, `failing-ids.tsv` (Runtime run 45259255785 on `24e2c929`, 23 Nov) and `app-green/REPORT.md` (App head `d53685f3`, 24 Nov; last complete runs on `3f5da385`). Audit: `plan39-audit.md`. Issues: `GET /repos/banodoco/astrid-dev/issues?labels=plan:39&state=open` (38 open, none are PRs).

**Caveats.** Plan 91's failing-ID inventory is from `b324d7c1`, not today's heads. A row not present in that inventory is "not failing there", which is not the same as passing today. Runtime Nightly runs only on `main`, so Nightly-only rows could not be measured on `release/15/main`. Windows rows cannot be checked: Plan 91's inventory has no Windows job. I did not read the full text of every issue body; some mappings are marked inferred.

## 0. Findings that change the plan

1. **Runtime and App are both still red on their `release/15/main` heads, for the causes Plan 39 described.** Runtime: 508 distinct failing IDs on the latest complete run. Roughly 75% of the ubuntu unit failures come from one root, the migrated-realm readiness and provider registration (clusters C1 and C2 in `runtime-green/clusters.md`). Those are RT1 and RT2. The `windows-realm-publication` job passed on that run.
2. **App: vitest is green (PT1 is done).** The Tests workflow passed on every push since `e3dbad64` (`app-green/REPORT.md`). E2E and Lanes are red. The E2E failures are mostly the fake Runtime missing `packs/inventory` and `project-elements` routes (38 confirmed of 85). The head `d53685f3` had all 17 jobs cancelled 14 seconds after start, with no steps run. Plan 91 AG-0 asks what cancels runs on `release/15/main`. The same answer is needed for Runtime and App.
3. **App quarantine entries expire tomorrow, 25 November.** The four entries in `config/testing/direct-journey-expected-failures.json` (issues #249 to #252) have owner "Plan 39 manager" (audit section 1, K1c). One of them is `P39-R12-VIDEO-DROP` (SF2c). Decide them today.
4. **Runtime ceiling is 19 declared IDs against a target of 10.** `tests/lanes.py:244` caps at 20. Owner decision D9 is needed. Entries expire 1 December and name "R14 Lead" as owner, which is stale.
5. **Plan 91 keeps the cross-repo pieces in Plan 39.** `plans/91.../plan.md:52` says the nightly report, K4 and K5 stay in Plan 39. Plan 91 D2 (`inputs.md:82`) says Plan 39 keeps the Runtime, the App and the cross-repo pieces. Plan 91 D4 (`inputs.md:84`) makes Plan 91 write the Agent entries of `ci/required-checks.json` (card AG-2, `P91:65`).
6. **K4 cannot pass yet.** It requires every release-tier check green on each pinned commit. Runtime and App are both red on `release/15/main`, so K4 is a gate that comes last, not a card to start now.
7. **Release 16 has no release manager** (`releases/16.md:5`). Every card below needs an owner named before work starts.

---

## 1. Non-Agent rows

Verdicts: **DONE** (record and close), **CARRY** (becomes a new card, named in section 5), **DROP** (superseded or stale), **CROSS** (owned outside Plan 39, with the owner named). Audit status is from `plan39-audit.md`, with the correction where I found one.

### Phase 1 and stop rows

| Id | Title (short) | Audit status | Verdict | Evidence and what it becomes |
|---|---|---|---|---|
| G0 | Worker smoke, Runtime and App | DONE | DONE | `T:38`. astrid-dev `env/` has `runtime-pytest.sh` and `app-test.sh`. `env/app-setup.sh` (Plan 31 RL-0) does not exist yet. That is Plan 31's row, so it is not a Plan 39 gap. |
| G1 | Baseline on `release/14/main` heads | STALE | DROP | `T:39`. Its heads are no longer the base. The release/15 measurements in `SCRATCH` replace it. No new card. |
| G2 | Re-measure after phase 1 | DONE (record) | DONE | `T:59`. Record only. |
| RS1 | Review stop | DONE (record) | DONE | `T:60`. Record only. |
| RE1 | Runtime installs the Agent at the pin | DONE | DONE | `T:43`. |
| RE2 | No scratchpad fallback | DONE | DONE | `T:44`. |
| RE3 | `git archive` tests have their commits | DONE for unit | DONE | `T:45`. The Nightly half moves to RT-11 (the snapshot certification test cannot fetch `321cef4b`). |
| RE4 | `tsc` available to `unit` | UNCLEAR | CARRY RT-16 | `T:46`. `unit` has it. The sandbox job has no setup-node step (`ci.yml`), and the handover said four sandbox tests lacked `tsc`. Confirm with one sandbox run. 0.25 day. |
| PE1 | App Lanes use the App's pins | DONE | DONE | `T:47`. Open question: the D7 check that `vendor.lock.json` and the manifest name the same Agent commit. Not looked for. |
| K1b | Runtime quarantine guard | DONE | DONE | `T:50`. |
| K1b-cap | Runtime quarantine at most 10 | OPEN | CARRY RT-12 | 19 declared, cap 20 (`tests/lanes.py:244`). Needs D9 first. |
| K1b.1 | Runtime guard under xdist | DONE (static) | DONE | `T:55`. Not exercised. Add one `pytest -n 2` run to RT-12's proof. |
| K1c | App quarantine guard; vitest on PRs | DONE | DONE for the guard; entries are CARRY APP-09 | `T:51`. The guard works. The four entries expire 25 November (section 0.3). |
| K1c.1 | App guard cannot be fooled | UNCLEAR | DONE | `T:56`. The review graded it A with injections (R14-P39-09, App #298). One grep for the run-time equality check before closing. |
| SF3a | Every main and int run stores per-test results | OPEN | CARRY APP-10 | Runtime is DONE (`ci.yml`, `nightly.yml` upload JUnit). App has no per-test upload in `test.yml`, `lanes.yml` or `e2e.yml` (audit). APP-10 is also a prerequisite for X-1 and X-2. |
| GL.3 | Gate variants | CLOSED | DONE | `T:54`. Owner closed it on 18 November. |

### Phase 2 (by cause)

| Id | Title (short) | Audit status | Verdict | Evidence and what it becomes |
|---|---|---|---|---|
| RT1 | Migrated-realm readiness | OPEN | CARRY RT-01 | Clusters C1 (696 hits; about 358 of the 479 ubuntu unit IDs, per `runtime-green/REPORT.md`) and C2. Biggest single item. Not on `release/15/main` (`6846891f` absent). |
| RT2 | Fresh provider registration on restart | OPEN | CARRY RT-01 | Cluster C2. Same card as RT1. |
| RT3 | v28 fixtures match C28 | OPEN | CARRY RT-03 | Measured as C27: "unsupported canonical vN manifest" in `tests/test_spec_reference.py` (3 IDs). |
| RT4 | No test drives the retired timeline writer | OPEN | CARRY RT-02 | Measured as C28, `RetiredRouteError` in `test_spec_reference.py` (3 IDs). Plus the 14 IDs behind #805 in `tests/lanes.py`. Under D5, assert 410 or delete. |
| RT5 | Stubs match real interfaces | OPEN | CARRY RT-03 | Measured as C31, `SimpleNamespace` has no `db_path` (3 IDs). |
| RT6 | Runtime long tail (about 207 IDs) | OPEN | CARRY RT-04, RT-05, RT-06, RT-07 | The row as written is replaced. The clusters in `runtime-green/clusters.md` are the real list: C3 and C7 (inverse and forward authority), C4 and C5 (packs not in the pin or not installed), C6 and C12 to C14 and C33 and C38 (product), C15 to C17 and C41 to C51 (portability and bootstrap), C25 (skip policy). |
| RT6.1 | macOS watchdog failure | OPEN | CARRY RT-09 | Same test as RT11. Cluster C22 (`test_p2_commit_phase_capture.py`, 3 IDs). |
| RT6.53 | Refuse visual fields on audio tracks (10 Nightly IDs) | OPEN | CARRY RT-10 | Not measured on `release/15/main`. Nightly runs only on `main`. Check on one Nightly run first. Route S. |
| RT6.58 | Refuse mutation after ancestor checks (22 Nightly IDs) | OPEN | CARRY RT-10 | Same as RT6.53. Route S. |
| RT7 | Installed lifecycle and update (8 IDs) | OPEN | CARRY RT-07 | Measured as the portability job: "No module named 'astrid'" from the stage1 venv (`tests/conftest.py:146`). RE1 is done, so the fixture is the remaining fault. |
| RT8 | `windows-realm-publication` | OPEN | DONE (verify on the current head) | The job was `success` on run 45259255785 (`runtime-green/REPORT.md`, job table). |
| RT9 | Snapshot certification input (Agent `321cef4b` not served) | UNCLEAR | CARRY RT-11 (retire) | `test_snapshot_legacy_certification.py:37` archives an Agent commit GitHub says is "not our ref". The test rebuilds a historical commit's state, which D5 retires. Delete it with the citation. Nightly only, 20 IDs. |
| RT10 | `SKIP_REGISTRY` names removed legs | UNCLEAR | DROP | `tests/lanes.py:106` is now `SKIP_REGISTRY = {}`, so the stale names are gone. The live skip-policy failures are C25 (`test_skip_policy.py`, 3 IDs), folded into RT-07. |
| RT11 | macOS watchdog fails once | OPEN | merged into RT-09 | Same as RT6.1. |
| RT12 | Delayed cleanup ACK fails at random | OPEN | CARRY RT-09 | One ID in the measured run (C57, `test_prepared_owner_authenticated_cleanup.py`). The 20-trial rule applies. |
| RT13 | Custody spawn declared xfail, 120 s timeout | OPEN | CROSS (Plan 38) | Zero IDs in the release/15 inventory. The custody and host-spawn tests are Plan 38's. Hand over; Plan 39 keeps no card. |
| PT1 | App vitest (16 files) | OPEN | DONE | The Tests workflow passed on every push since `e3dbad64`. `app-green/REPORT.md` shows 1,454 files and 21,474 tests passing on `3f5da385`. |
| PT2 | Shared E2E setup, seven mechanisms | OPEN | CARRY APP-01, APP-02 | Cause 1: fake Runtime routes (38 of 85 E2E failures). Cause 3: CI environment (12). |
| PT3 | Add-to-timeline (5) and extension reload (3) | OPEN | CARRY APP-03 | Five `production-widget-scope` cases: the testid `add-selected-generation-to-timeline` is no longer rendered, and a vitest asserts its absence (`GenerationsPaneGallery.test.tsx:556`). A product decision and a stale test, not a plain restore. Extension harness (3) also here. |
| PT4 | App visual baseline | OPEN | CARRY APP-05 | `extension-visual` 1 failure, 4 not run; baseline size mismatch. May clear with APP-01. |
| PT5 | Conflict shown, draft kept after lost ACK | OPEN | CARRY APP-06 | Not in the App causes list. Confirm the case fails before scoping. |
| PT6 | Source tuple across Quick Journey | OPEN | CARRY APP-04 | Cause 5: `three-products.spec.ts:96-99` and `:196`. A test bug: the quick tier never sets `journey.sources`. Lanes `quick-journey` fails on it. |
| PT12 | Browser-rendered film download (3 cases) | OPEN | CARRY APP-07 | Not in the App causes list. `video-editor-workflow-parity` (6) and lifecycle (1) are "cause not established". Read them before scoping. |
| FIX-11 | Cleanup ACK fences activation (#905) | OPEN | CARRY S-01 | `T:105`. S route, Runtime and App. Confirm #905 is open and what RS1.6 asked. |
| FIX-12 | Owner retry with durable logs settles (#926) | DONE | DONE | `T:106`. Runtime #70 `8e8711fd` is an ancestor of `release/15/main`. Agent #439 is Plan 91's to check. |
| AT21 | CPU journey cases (#578) | OPEN | CROSS (Plan 50) | Agent and Runtime. Plan 50 RB-1 is its dependency. Not in Plan 91's table. Not a Plan 39 card. |
| K2 | Trusted per-ID comparison on product PRs | OPEN | CARRY X-2 | `T:132` shows `[x]` for Agent #433, Runtime #69 and App #313 on plan branches. Those never reached release/15. #984 (activation) is open. Plan 91 says the K2/K3 comparator "never passed on an unchanged tree" (`P91:64`), so it is re-measured, not ported. |
| K3 | Same comparator nightly | OPEN | CARRY X-2 | Merged with K2. |

### Phase 3 (keep it green)

| Id | Title (short) | Audit status | Verdict | Evidence and what it becomes |
|---|---|---|---|---|
| K4 | `release-contract`: every release-tier check green on each pinned commit | OPEN | CROSS (Plan 31 RL-1b) | Plan 31 RL-1b is `[ ]`, and its dependencies are RL-1a and RL-2a. The job lives in astrid-dev `docs.yml`. Worth doing in Release 16, as the last gate, after Runtime and App are green. |
| K5 | Release skill rule text | OPEN | DROP (fold) | Its dependencies are K4, SF4 and SF5. Fold into Plan 31 RL-1d (release skill text). |
| Owner: merge-tier required checks | OPEN | CARRY X-3 | `T:136`. Owner-side. Add the Runtime and App rows to `ci/required-checks.json` after Plan 91 AG-2 creates the file. The Release 14 evidence (21 November) found no effective branch rule on any product ref. |
| R | Final review (at most 3 rounds) | STALE | DROP | Its scope is "all retained Release 14 tasks" (`T:137`). A Release 16 review card replaces it at the end. |

### Phase 4 (structural fixes)

| Id | Title (short) | Audit status | Verdict | Evidence and what it becomes |
|---|---|---|---|---|
| SF1a | Three-products tests own their seed | OPEN | CARRY APP-04 | `three-products.spec.ts:54-61` (worker-scoped seed) and `:83` (`mode: 'serial'`). Same file as PT6. |
| SF1b | Journey runs parallel and shuffled | OPEN | CARRY APP-04 | After SF1a. |
| SF2a | Expected failure names step and error | OPEN | CARRY APP-08 | Entries in `direct-journey-expected-failures.json` have no `step` or `error`. Do after the APP-09 decision. |
| SF2b | Unmarked test: Runtime refuses wrong media selection | OPEN | CARRY RT-15 | A Runtime test. The `T:142` dependency on SF1a looks wrong for a Runtime test; check. |
| SF2c | VIDEO-DROP on the commit-time refusal path | OPEN | CARRY APP-09 (urgent) | `P39-R12-VIDEO-DROP` expires 25 November (App #252). |
| SF3b | Compare candidate with published `main` from stored results | OPEN | CARRY X-2 | `env/baseline-diff.py` exists; `env/ci-results.sh` does not. Plan 91 reuses `baseline-diff.py`, so one comparator. |
| SF3c | Every shard finishes; a truncated shard fails the aggregate | OPEN | DROP (split) | Agent: Plan 91 AG-1's `missing` bucket blocks missing IDs, and AG-0 finds what cancels runs. Runtime and App: folded into X-1 and X-2. |
| SF4 | Candidate is `main` plus a listed set of fixes | OPEN | DROP as a card; SPLIT | Put a "fixes on main" section in Plan 31 RL-1a's release record. Needs the Release skill owner's agreement (`T:147`). |
| SF5 | Product `main`s frozen during a release | OPEN | DROP as a card; owner decision | A ruleset decision, not build work. Plan 31's owner rows (protect `main` and `release-published`) cover the same ground. |
| Nightly report (no row) | Nightly new-red report (`scripts/ci_red_report.py`) | OPEN | CARRY X-1 | Plan 91 keeps it in Plan 39 (`P91:52`). Issue #971 is open and planned. Still worth doing: it is the "red means new red" measure. |

---

## 2. Agent rows not in Plan 91's "Taken from Plan 39" table

Plan 91's table is `P91:131-150`. Coverage is judged from the cards' scope text (`P91:63-103`), `assignment.json` (file and cluster ownership), `prune-candidates.md`, and `wave-c-cards.md` (one card per test file). "Wave C" means the failing IDs fall to a per-file card if they still fail on the release/15 head.

| Row | Plan 39 text (short) | Plan 91 coverage | Verdict |
|---|---|---|---|
| AT1.6 | Smaller causes: engine footprint 106 GB; pod H3 install path; staged root `runtime.lock.json`; delegated child digest; engine model lock; Plan 33 args; stale generated files | C11 (delegated child digest) is AG-B11 (`P91:92`). Pod H3 is in AG-B2's files (`pod_session.py`). C6, C8, C13, C14, C15 have no card by name. | PARTLY covered. Named causes need cards; the rest is Wave C by file. |
| AT1.7 | Seven tests misfiled under the `local`-pack cause | No file or test named. | UNOWNED by name. Ask Plan 91 for the seven IDs. |
| AT2 | mypy back to baseline, four cards by package | No mypy card in Plan 91 (grep: none). | UNOWNED. Needs a Plan 91 card (with AT23 and #633). |
| AT3 | Windows custody and wheel smoke, only if G1 shows red | G1 was never redone. Plan 91 says `windows-native-and-installer` is green (`p91-plan.md`). Windows is not in its inventory. | DROP (conditional, never measured). Reopen only if Windows goes red. |
| AT5 | 16 direct test gates the K1a scanner finds in 13 files | Named in cards: `test_installer_busy_fence.py` (AG-A5), `test_pod_session.py` (AG-B2), `test_installer_pinokio_*` (AG-B13), `test_pod_bootstrap.py` (AG-P1). Others are Wave C if failing: `test_release_python.py` (AG-C70), `test_journey_*` (AG-C188, AG-C199), `test_installer_r0_entry.py` (AG-C229), `test_host_cleanup_ack_barrier.py` (AG-C54). Several gates fail nothing. | PARTLY covered. The gate-only removals (not failing) are UNOWNED. |
| AT6 | `h3_av.transform` retired; test calls it | `test_two_edit_cpu_qualification.py` is AG-C43 (`prune: Wave C`). | COVERED by AG-C43. The card must retire the test under D5. |
| AT7 | `ensure_pack_host` drops a foreign registration | `test_host_recovery.py` is AG-C95. | COVERED by AG-C95. |
| AT8 | Stalled stage deadline `[settlement]` | `test_fail_closed_g28.py` is AG-C59 (ci:C221). | COVERED by AG-C59. |
| AT10 | `test_pack_build.py` six tests run nowhere (lane `_never`) | Not in the inventory, because they never run. No Plan 91 card covers "a declared lane no job selects". | UNOWNED. Decide: wire the lane (AG-1 or AG-2 scope) or retire under D5. |
| AT13 | Terminal publication replay has no bound in `generic_host.py` (#611) | Not Plan 91. `generic_host.py` is Plan 13's (`releases/16.md`, Plan 13 split). | CARRY to Plan 13. Not a Plan 91 or Plan 39 card. |
| AT14 | 40 of 52 `test_comfy_target.py` cases error on Windows | Windows path guard. Not in the inventory. | UNOWNED (Windows). Candidate owner: Plan 38 (one process identity, Windows). |
| AT15 | Windows host smoke failed once, passed on retry | Flake, Windows, one failure. | DROP unless it recurs (20-trial rule). |
| AT16 | Hyperframes real render fails at random | `test_hyperframes_backend.py` is AG-C7 (lanes:C34). | COVERED by AG-C7. The flaky rule (20 paired trials) applies. |
| AT17 | Cancel completion error `[True]`/`[False]` swap | Same file as AT8, AG-C59. | COVERED (file level). |
| AT18 | Multisurface browser deadline (180 ms budget) | `test_installed_browser_adapter.py` not in the b324d7c1 inventory. | UNOWNED. Flake candidate; drop unless it recurs. |
| AT19 | Pinokio secret test exits 2 without `/proc/net/tcp6` | `test_pinokio_platform_adapter.py` is AG-B13 (C75). | COVERED by AG-B13. |
| AT20 | macOS audio, text card and provider manifest: Remotion probe cleanup | Not in the b324d7c1 inventory (the 13 darwin IDs are other tests). Plan 91 AG-0 runs darwin native "to an outcome". | UNOWNED until AG-0's darwin run says whether they fail. |
| AT21 | CPU journey cases (#578) | Not in Plan 91. | CROSS (Plan 50 RB-1). |
| AT22 | Release 13 engine checklist (#612) | Not in Plan 91. | DROP after one read of the checklist. Stale by its own label ("deferred to green mains"). |
| AT23 | Release 13 Ruff and mypy additions (#613) | Not in Plan 91. | UNOWNED. With AT2. |
| AT24 | Pinokio process snapshot races listener (#621) | `test_pinokio_platform_adapter.py`, AG-B13 (listener-owner group named in AG-B13). | COVERED by AG-B13. |
| AT25 | Foley selection fixtures (#626) | No foley test in the b324d7c1 inventory. | UNOWNED, and probably passing. Verify; drop if so. |
| AT26 | Shared redo leaks state (#636) | `test_historical_shared_redo_authority.py` is AG-A7 (prune: AG-A7 owns it). | COVERED (file level) by AG-A7. |
| AT27 | Delayed acceptance handshake (`test_engine_custody.py`) | AG-B22 names the file (`P91:103`). | COVERED by AG-B22. |
| #869 | Installed rendering skill publishes a saved candidate | No matching failing ID in the inventory. Not named in Plan 91. | UNOWNED. Verify it fails on the current head. |
| K1a.1 | K1a scanner blind spots | Plan 91 names K1a under AG-1 (`P91:137`), not K1a.1. | UNOWNED by name. Add the scanner forms to AG-1's scope. |
| SF3c | Every shard under its job limit; a truncated shard fails the aggregate | AG-1's `missing` bucket (`P91:64`) for the aggregate. AG-0 for cancellations. The per-shard limit is not named. | PARTLY covered. |
| SF6a | One clip-type alias policy | Not in Plan 91. | UNOWNED. Owner decides: give to Plan 91 after green, or drop. |
| SF6b | Element registry cache follows the inventory | Not in Plan 91. | UNOWNED. Same choice as SF6a. |
| SF6c | Printed recovery and install commands run through the real CLI | Not in Plan 91. | UNOWNED. Same choice. |
| SF6d | Agent custody fixture | AG-A1 (`P91:137`). | COVERED by AG-A1. |
| SF6e | Test patch survives into teardown | Not in Plan 91. No named failing ID. | DROP unless a failing ID turns up. |
| SF7 | Journey row proves its card (`journey_version_jumps.py`) | Plan 91 excludes the Agent's `journey.yml` receipts (`p91-plan.md`, Plan 34). | CARRY to Plan 34 or DROP. |
| AT1.4 | `ASTRID_TEST_LIFECYCLE_CHECKOUT` in CI | AG-A2 names the existing variable (`ci.yml:75,242`). | DONE. |
| AT1.9, AT1.54 | Integration collection root; nonisolated refusal probe | Done on Release 14 (`T:70`, `T:71`). | DONE. |

---

## 3. The 38 open `plan:39` issues

Scope: **Agent** = Plan 91, **Runtime** and **App** = Plan 39 cards (section 5), **cross** = more than one repo, **other** = outside all three repos.

| # | Title (short) | Scope | Maps to | Confidence |
|---|---|---|---|---|
| 1313 | `test_fail_closed_g28` settlement fails on `release/15/main` | Agent | AG-C59 (`test_fail_closed_g28.py`, ci:C221) | High, file level |
| 1307 | Three timeline tests fail, 37 error at setup (Release 15 forward base) | Agent | Plan 91 Wave C by file, or AG-A7 | Medium |
| 1291 | Five tests fail on `release/15/main` beside H3 release ones | Agent | AG-C165 (`tests/timeline/test_authoring_media.py`, 4 IDs; the issue names this file) | High, file level |
| 1290 | Giant-file check cannot stop growth; failing | Agent (Plan 13 guard) | CARRY to Plan 13 (its guard for `generic_host.py`). Plan 91 has none. | High |
| 1158 | Two call failures from grouped Undo and endpoint fixtures | Agent | Plan 91 Wave C by file (`tests/editing_conformance/`) | Medium |
| 1141 | Decide expected clip position, 1 s at 30000/1001 fps | Agent (owner decision) | Plan 91 Wave C; owner must authorise the one expectation change the issue asks for | High (scope) |
| 1130 | Missing five-second child-discovery signal, two D18 cases | Agent | AG-B11 (`test_generic_host_child_bridge_d18.py`) | High, file level |
| 1127 | Two retained-source rendering cases lack the Remotion project dir | Agent | AG-A2 (names `ASTRID_REMOTION_PROJECT_DIR`) | Medium-high |
| 1011 | Child-bridge and device-ambient receipt outcomes | Agent | AG-B11 (child bridge) plus Wave C | Medium |
| 1007 | Remaining S01 call failures (104 cases) | Agent | Plan 91 Wave C by file. S01 is not named in Plan 91. | Low-medium |
| 1006 | Retained media selection digests after H31 upgrade | Agent | Plan 91 Wave C by file. Not named. | Low-medium |
| 1002 | Undo of a shared video unplace refused after restart (4 cases) | Agent | AG-A7 (`editing_conformance`) | Medium |
| 984 | K2/K3: activating the failure-ceiling comparator | cross | X-2 (Plan 39) | High |
| 971 | Nightly new-red report (D4) | cross (astrid-dev) | X-1 (Plan 39) | High |
| 964 | `_tls_policy.py` adds a structure finding over the 102 ceiling | Agent | Probably stale: the GL.2 note says FIX-13 (Agent #441) moved the TLS module to restore 102 (`T:53`). Close after one `ls` on `release/15/main`. Else AG-1's ceiling. | Medium |
| 925 | VibeComfy `release/14/main` CI cannot qualify anything | other | DROP from Plan 39. VibeComfy is not one of the three repos. Owner re-homes or closes. | High |
| 910 | Windows receipt temp files project to 261-262 UTF-16 units | Runtime (Agent review) | RT-14 | High (bug is stated) |
| 809 | Top-level timeline text hook remains quarantined | Runtime | RT-02 (decide: retire under D5, or implement) | Medium |
| 807 | Historical audio trim held by Runtime strict quarantine | Runtime | RT-02 (decide: historical, so retire under D5) | Medium |
| 806 | Legacy capture recertification quarantined | Runtime | RT-11 (retire; needs the Agent projector, which is historical) | Medium |
| 805 | Runtime quarantine retains 14 tests of retired writers | Runtime | RT-02 (assert 410 or delete). The registry now has 19 IDs, so the count is stale. | High |
| 785 | H3 end-to-end test fails intermittently | Agent | AG-C67 (`test_h3_build_after_outputs.py`, in inventory); flaky rule | High, file level |
| 733 | Readiness tests fail on a busy machine (2 s probe) | Agent | AG-B22 (readiness group under load, `P91:103`) | High |
| 647 | Structure baseline stale (59 vs 13) | Agent | DROP. Superseded by the 102-entry ceiling (GL.2) and Plan 91 AG-1. | High |
| 639 | `TestPackDeclaredBackendIds` fails on R12 and R13 | Agent | AG-C74 (`tests/core/model_catalog/test_registry.py`) | High, file level |
| 637 | 133 SDK timeline tests assert a hard-coded Runtime commit | Agent (+ Runtime pin) | AG-A1 and AG-A2 (Runtime objects, editable install), plus RT-05 for the pin | Medium |
| 636 | Shared redo rechecks archive at acceptance: order-dependent | Agent | AG-A7 (`test_historical_shared_redo_authority.py`); AT26 | Medium-high |
| 633 | Parked mypy type-only fixes | Agent | UNOWNED. Plan 91 needs AT2's card. | High (gap) |
| 626 | Foley selection test fails | Agent | Not in the inventory. Verify; drop if passing. | Medium |
| 621 | Pinokio adapter readiness test flaky | Agent | AG-B13 (`test_pinokio_platform_adapter.py`) | High |
| 615 | Stale or environment-dependent Agent fixtures | Agent | AG-C74, AG-C81 and AG-A3 (stale fixtures, pack fixtures), by cause | Medium |
| 614 | Unit shards 1 and 5 never finish | Agent | AG-0 (what cancels), AG-1 (missing bucket), and Wave C for the two hangs (`tests/sdk/test_h3_endpoint_r4.py`, not in the inventory: verify) | Medium |
| 613 | Release 13 ruff and mypy additions | Agent | UNOWNED. With AT2 and #633. | High (gap) |
| 612 | Release 13 engine-lane items deferred | Agent | UNOWNED. AT22. Likely DROP after a read. | Medium |
| 611 | Terminal publication replay unbounded | Agent (Plan 13 file) | CARRY to Plan 13 (AT13) | High |
| 606 | Agent skills test never runs in CI | Agent | AG-C207 (`test_skills_installed_composition.py`, in inventory) for the failure. The "never runs" part is a CI selection gap, for AG-1's deselect guard (K0). | Medium-high |
| 585 | Integration lane dependencies not provisioned (Runtime checkout, lifecycle checkout) | Agent | AG-A2 (`ASTRID_RUNPOD_LIFECYCLE_CHECKOUT` and Runtime objects, `P91:69`) | High |
| 578 | CPU journey takes 57 min for 26 tests | cross (Agent, Runtime) | CROSS (Plan 50 RB-1, AT21). Not a Plan 39 card. | High |

Counts: Agent 29, Runtime 5 (805, 806, 807, 809, 910), cross 3 (984, 971, 578), other 1 (925). Of the 29 Agent issues, most map to a named Plan 91 card or file. Unowned or Plan 13 by my reading: 1290, 611 (Plan 13), 633, 613, 612 (unowned). 647 and 964 are probably stale. 626 is not in the inventory.

---

## 4. Phase 4 (SF1 to SF5): worth doing in Release 16?

| Row | Worth it in Release 16? | Action |
|---|---|---|
| SF1a, SF1b | Yes. The three-products spec is serial and seeds order-dependent state. | Card APP-04, with PT6. Same file. |
| SF2a | Yes, but small. Do it after the quarantine decision. Drop with the entries if they are cleared. | APP-08. |
| SF2b | Yes. It is a Runtime product guard. | RT-15 (Runtime). |
| SF2c | Yes, and urgent: the entry expires 25 November. | APP-09 today. |
| SF3a | App half only. Runtime is done. Needed by X-1 and X-2. | APP-10. |
| SF3b | Yes, folded into the comparator. | X-2 (reuses `env/baseline-diff.py`). |
| SF3c | Split: Agent is in Plan 91 AG-1 and AG-0; Runtime and App go into X-1 and X-2. | No row. |
| SF4 | Only as a release-record section. | Plan 31 RL-1a. Owner agreement needed. |
| SF5 | No build work. A ruleset decision. | Owner, under Plan 31's owner rows. |
| SF6a, SF6b, SF6c, SF6e, SF7 (Agent) | Not in Plan 91. Each is Agent product or test hygiene. | Owner picks: a post-green Plan 91 card, Plan 34 (SF7), or drop. |

---

## 5. New cards for the rebuilt Plan 39 (Release 16)

Routes: N (ordinary), X (coupled reasoning), S (correctness). Sizes are engineering days, from the measurement estimates where they exist. "Owner" is unnamed for Release 16 and must be named before start.

### Runtime

| Card | Scope | Absorbs | Route, size | Depends on |
|---|---|---|---|---|
| RT-01 Migrated realm ready marker and provider registration (clusters C1, C2) | `runtime_protocol/v33_lifecycle.py`, `daemon.py`, fixture helpers (`tests/test_precut_*`) | RT1, RT2 | X, 1.5 to 3 | None. Start here. |
| RT-02 Retired-writer tests: assert 410 or delete (C28; #805; #809; #807) | `tests/test_spec_reference.py`, `tests/lanes.py` declarations | RT4, #805, #809, #807 | N, 1 | D5 citation |
| RT-03 Fixture and stub conformance (C27 vN manifest; C31 `db_path`) | `tests/test_spec_reference.py`, `tests/test_timeline_commit_sequential_verifier.py` | RT3, RT5 | N, 1 | None |
| RT-04 Inverse and forward authority expectations (C3, C7, C32, C34, C35) | `tests/test_timeline_inverse_sequential_authority.py`, `tests/test_timeline_forward_created_authority.py`, `tests/test_timeline_legacy_authority.py` | RT6 tail | X, 1 to 2 | Agent-or-test decision |
| RT-05 Pin and pack wiring (C4 video_editing 60 IDs; C5 image pack 36) | `tests/astrid-agent.pin`, `tests/test_timeline_render_publication*.py`, `tests/test_timeline_native_asset_union.py` | RT6 tail, #637 pin part | N, 1 | Pin decision (Plan 91 owns the Agent head) |
| RT-06 Runtime product bugs (C6, C12, C13, C14, C33, C38, C39) | `runtime_protocol/timeline_commit*.py`, `store.py`, `cas.py` | RT6 tail | S, 2 to 4 (each over a day goes to an issue under D6) | RT-01 |
| RT-07 Portability and bootstrap fixtures (C15, C16, C17, C18, C25, C41 to C51) | `tests/test_portable_lifecycle.py`, `tests/conftest.py:146`, `tests/test_bootstrap.py`, `tests/test_skip_policy.py` | RT7, RT10 | N, 1 to 2 | RE1 (done) |
| RT-09 Flaky and watchdog (C22 p2 capture; C57 cleanup ACK) | `tests/test_p2_commit_phase_capture.py`, `tests/test_prepared_owner_authenticated_cleanup.py` | RT6.1, RT11, RT12 | N, 1 plus 20 paired trials each | None |
| RT-10 Nightly refusals (10 + 22 IDs) | Runtime refusal code (`runtime_protocol`) | RT6.53, RT6.58 | S, 2 to 3 | Verify on one Nightly run first; not measured on `release/15/main` |
| RT-11 Retire legacy snapshot certification | `tests/test_snapshot_legacy_certification.py` (delete, cite D5 and `321cef4b` not served) | RT9, RE3 Nightly half, #806 | N, 0.5 | Owner confirms D5 |
| RT-12 Quarantine ceiling (19 to 10, or owner-approved cap) | `tests/lanes.py:244` (cap), declarations | K1b-cap, K1b.1 proof | N, 0.5 plus owner decision D9 | Owner |
| RT-14 Windows temp receipts path length (#910) | Runtime writer (`prepared`/`finalized` receipt names) | #910 | N, 1 | Windows reproduction |
| RT-15 Refuse wrong media selection (unmarked) | Runtime test and guard | SF2b | N, 1 | None (check the SF1a dependency) |
| RT-16 `tsc` on sandbox job | `ci.yml` sandbox job | RE4 | N, 0.25 | One sandbox run |

RT-13 (custody spawn) goes to Plan 38. RT-08 (pidfd in the sandbox container, C8, 12 IDs) goes to Plan 38 as well, because custody is Plan 38's.

### App

| Card | Scope | Absorbs | Route, size | Depends on |
|---|---|---|---|---|
| APP-09 Quarantine entries decision (urgent, expires 25 Nov) | `config/testing/direct-journey-expected-failures.json` | K1c entries, SF2c (`P39-R12-VIDEO-DROP`) | N, 0.5 plus owner | Owner names an owner |
| APP-01 Fake Runtime: `packs/inventory`, `project-elements`, commits list | `tests/e2e/fake-runtime/server.ts` | PT2 cause 1 (38 of 85) | N, 1 to 2 | None |
| APP-02 E2E CI environment: `playwright install` in `checkout-lanes`; hard-coded `/opt/pw-browsers` (`command-outbox.spec.ts:31`); `VIEWING_BROWSER_FLOCK_HELD` (`viewing-parity/cases.ts`) | `.github/workflows/lanes.yml`, specs | PT2 cause 3 (12) | N, 1 | None |
| APP-03 Stale tests: `production-widget-scope` (testid removed), hover-media specs, vision feed stub, extension harness (3) | specs and `GenerationsPaneGallery.test.tsx:556` | PT3 | N and X, 2 | Product decision on `add-selected-generation-to-timeline` |
| APP-04 Three-products: quick-journey source tuple; seed ownership; parallel and shuffled | `tests/e2e/local/three-products.spec.ts` (`:54-61`, `:83`, `:96-99`, `:196`) | PT6, SF1a, SF1b | N and X, 1.5 to 2 | APP-01 (same spec) |
| APP-05 Visual baseline | `extension-visual` spec and baseline | PT4 | N, 0.5 | APP-01 |
| APP-06 Conflict shown, draft kept after lost ACK | App conflict path | PT5 | X, 2 | Verify the case fails first |
| APP-07 Video editor parity, lifecycle, film download | `video-editor-workflow-parity`, lifecycle, export | PT12 | X, 2 | Read the failures first (cause not established) |
| APP-08 Expected-failure step and error naming | `direct-journey-expected-failures.json` schema and checker | SF2a | N, 0.5 to 1 | APP-09 |
| APP-10 Per-test results for App CI | `test.yml`, `lanes.yml`, `e2e.yml` (JUnit upload) | SF3a App half | N, 0.5 to 1 | None. Blocks X-1, X-2. |

### Cross-repo

| Card | Scope | Absorbs | Route, size | Depends on |
|---|---|---|---|---|
| X-0 What cancels runs on `release/15/main` (Runtime, App) | Run events and the Release 15 run board | Section 0.2. Plan 91 AG-0 does the Agent. | N, 0.5 | None |
| X-1 Nightly new-red report | `scripts/ci_red_report.py` (new), nightly workflow, rolling issue #971 | Nightly report (no row) | N and X, 2 to 3 | APP-10, Plan 91 AG-1 output format |
| X-2 Per-ID comparator, Runtime and App (K2, K3, SF3b, #984) | `env/baseline-diff.py` reused (Plan 91 AG-1) | K2, K3, SF3b, SF3c (product half) | X, 3 to 5 | AG-1 (Plan 91), APP-10. The old K2/K3 comparator never passed on an unchanged tree, so re-measure before enforcing. |
| X-3 Required checks: Runtime and App rows | `ci/required-checks.json` (created by Plan 91 AG-2) | Owner row | N, 0.5 plus owner | Plan 91 AG-2 |
| S-01 Cleanup ACK fences activation (#905) | Runtime and App | FIX-11 | S, 2 | Confirm #905 and RS1.6 |

### Handed to other plans (not Plan 39 cards)

| Item | Owner | Note |
|---|---|---|
| K4 `release-contract` | Plan 31 RL-1b | Worth doing. A gate, last. Depends on RL-1a and RL-2a. |
| K5 release skill text | Plan 31 RL-1d | Fold. |
| SF4 release candidate content | Plan 31 RL-1a | Release-record section. |
| SF5 product `main` freeze | Owner, Plan 31 owner rows | Ruleset decision. |
| AT21 / #578 CPU journey | Plan 50 RB-1 | Release 16. |
| RT13, RT-08 custody and pidfd | Plan 38 | Custody and host-spawn. |
| AT13, #611, #1290 `generic_host.py` | Plan 13 | Release 16 split and guard. |
| AT14, AT15 Windows | Plan 38 (candidate) | Needs a Windows measurement first. |
| SF7 journey receipts | Plan 34 | Or drop. |
| #925 VibeComfy | Owner | Outside the three repos. |

---

## 6. Things I could not verify, and questions for the owner

- **Current heads.** Runtime is measured at `24e2c929` (23 Nov) and App at `d53685f3` (24 Nov). Plan 91's inventory is `b324d7c1`. Rows marked "not in the inventory" may pass today, or may fail on a head I did not read.
- **Nightly-only rows.** RT6.53, RT6.58 and RT9 run only on `main`. They need one Nightly run on the release head.
- **Windows and macOS rows.** AT3, AT14, AT15 and AT20 have no measured failure on the current heads. The inventory has no Windows job.
- **App rows not in the causes list.** PT5 and PT12. Read before scoping.
- **Issue bodies I did not read in full.** Mappings for #1307, #1291, #1158, #1011, #1007, #1006, #1002, #626 and #614 are medium or low confidence. Confirm before closing any issue.
- **Owner decisions needed.** Name the owners of the 25 November quarantine entries (APP-09). Decide the Runtime ceiling (D9, RT-12). Decide the K2/K3 comparator approach (X-2). Decide #1141's expectation change. Decide the SF6a, SF6b, SF6c, SF6e and SF7 fate. Name the Release 16 owner of Plan 39.
- **Plan 91 gaps to report back.** AT2 and AT23 (mypy and ruff), AT10 (a lane that runs nowhere), K1a.1 (scanner forms), AT1.7 (seven IDs), #633, #613 and #869 have no Plan 91 card.
- **Measurement.** I did not run CI, dispatch anything, or check the Agent at its current head.
