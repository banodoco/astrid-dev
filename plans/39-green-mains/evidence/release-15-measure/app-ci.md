# astrid-app CI on release/15/main: why it is red (read-only investigation, 24 Nov 2026)

Branch head d53685f3 (PR #384 "repin save pins"; diff vs 3f5da385 touches only runtime.lock.json, config/astrid-cli-surface/vendor.lock.json, public/install-manifest.json).
Evidence: logs/ (job logs), *_clean.txt (ANSI-stripped), jobs_<run>.json. V = verified in code at FETCH_HEAD, L = inferred from logs only.

## Workflows (release/15/main)
| Workflow | Triggers | Concurrency | Jobs / commands |
|---|---|---|---|
| Tests (test.yml) | push main, release-1, int/**, release/*/main; PR; dispatch | group per ref; cancel-in-progress false on main and release/*/main | vitest (`npm test` = check:* guards + vitest), release-tooling-macos, boundary (vendor-lock check), release-guard/landing-reference/plan61 (skipped on push) |
| E2E (e2e.yml) | push, dispatch | cancel false on release/*/main | 6 jobs: playwright-default, playwright-timeline, playwright-timeline-chrome-export, extension-accessibility, extension-visual, extension-cross-browser |
| Lanes (lanes.yml) | push, schedule 03:43, dispatch | cancel false on release/*/main | checkout-lanes (`npm run test:checkout`, vitest), installer-posix x2, installer-powershell, quick-journey |
| Direct Journey | PR (paths), schedule 03:17 (main only), dispatch | cancel true | direct-journey, three-products |
Others: dockerfile-check, installer-windows, p61-*, public-vision, served-manifest-canary.

## Run history (release/15/main): Tests green on every push since e3dbad64; E2E and Lanes red on every completed push
3f5da385 E2E 45231479752 fail / Lanes 45231479588 fail / Tests ok; f10d6641, a906a6ff, e3dbad64, c5ba8cd9: same. ba34e184: Tests fail, E2E cancelled. 2ef94b4c: all fail.
Failure sets are IDENTICAL across 4 runs spanning 22-23 Nov (counts per job identical): no flips, no flakes. Deterministic.

## d53685f3 cancellation (E2E 45293886304, Lanes 45293886576, Tests 45293886336)
All 17 jobs: no steps, runner_id 0, cancelled 14 s after start (00:02:45 to 00:02:59-00:03:02 UTC), actor AstridPseudon. NOT concurrency: all three workflows exempt release/*/main from cancel-in-progress (V: test.yml:21, e2e.yml:13, lanes.yml:15), and no newer run/push exists. Most likely an explicit cancel (UI/API/automation) of all three runs. Cause not provable from public API. Net: no CI signal exists for the repin.

## E2E inventory, run 45231479752 (3f5da385)
| Job | Result | Counts |
|---|---|---|
| playwright-default | fail | 30 failed / 552 passed |
| playwright-timeline | fail | 36 failed / 3 passed |
| playwright-timeline-chrome-export | fail | 3 failed |
| extension-accessibility | fail | 9 failed / 6 passed |
| extension-cross-browser | fail | 6 failed / 3 passed |
| extension-visual | fail | 1 failed / 4 did not run (NO-RESULT tests) |
Total 85 failed, 564 passed, 4 not run. Lanes: checkout-lanes 1 failed / 89 passed (vitest); quick-journey 1 failed; installer-posix x2 and powershell pass. Tests/vitest: 1454 files, 21474 tests pass.
No cancelled/setup-failure jobs in completed runs. Artifacts: only Playwright test-results (traces/screenshots) and quick-journey.json/txt; NO JSON/JUnit per-test report is uploaded (reporter is github/list + playwrightSkipGuard). Direct Journey does use `--reporter=json` (jq outcome gate). Per-test App comparison therefore requires adding a json reporter + artifact.

## Failures by cause
### 1. Fake Runtime out of date with App/real Runtime API: 38 confirmed (up to ~46)
Fake server tests/e2e/fake-runtime/server.ts:213-225 returns 404 "no fake route" for every non-/v1 path that ACP does not handle; no packs routes exist (V: grep of tests/e2e/fake-runtime finds no "packs"). App calls GET /api/runtime/packs/inventory (src/tools/video-editor/runtime/extensionLoader.ts:89, useRuntimePackExtensions.ts:42) and /packs/project-elements?project= (admittedElementLoader.ts:111). Also `GET /v1/projects/demo-project-id/timelines/demo-timeline/commits?limit=50` throws "unexpected GET" (500) from the fixture (client: src/integrations/runtime/generated.ts:212).
Still present on 3f5da385: YES (29x inventory, 30x project-elements in timeline job alone). First error: `local-test editor made unexpected 404 request(s): .../packs/inventory`, tests/e2e/timeline/support.ts:576, or issues list `toEqual([])` fails.
- playwright-timeline 21 of 36 (layout-geometry x5, shell-responsive-overflow x3, toolbar-reachable x5, tablet-gestures x2, desktop-interaction, phone-gestures, seeded-preview-samples, data-lane-viewport, audio-reactive-colour-export:229, extension-performance-budget:67)
- extension-accessibility 9, extension-cross-browser 6 (spec line 148 / 90 `expect(issues).toEqual([])`)
- timeline-chrome-export 2 (audio-reactive-colour-export:304, :412)
- Probably same cause, unverified: editor-tour x4 (timeline; "act 1 welcome is ready"/tour record, same 404/500 noise), extension-visual 1 (layout 1414x319 vs baseline 1374x303), extension-harness x3 (smoke extension state runtime-error).
Fix: add packs/inventory + project-elements (empty inventory/list) and a commits-list route to fake Runtime/fixture, then re-run to see what remains. Est 1-2 days.

### 2. Stale test helper using a retired route: 1
tests/e2e/timeline/preview-scrub-evidence.spec.ts:231 via support.ts:276-286 POSTs `/composition-revisions`; Runtime answers 410 retired_route "submit EditCommands through commitTimeline" (fixture src/integrations/runtime/fixtures/responses/retired_route_410.json). V. Needs helper moved to commitTimeline. Est 0.5-1 day (shares fake route work).

### 3. CI wiring / env: 12 (+1)
- checkout-lanes 1: runtimePackRefresh.integration.test.ts:145 launches chromium; lanes.yml checkout-lanes has no `playwright install` (V: only quick-journey installs chrome, lanes.yml:190). Error "Executable doesn't exist ...chromium_headless_shell-1223". Est 0.25 day.
- timeline command-outbox.spec.ts:48 1: hard-coded default `/opt/pw-browsers/chromium` (spec line 31, V). 0.25 day.
- viewing-parity/cases.ts:240-328 x10 (5 tests twice): harness.ts:110 requires env VIEWING_BROWSER_FLOCK_HELD=1 (local flock harness); never set in CI (V). Exclude from CI or set marker. 0.5 day.

### 4. Stale tests / removed behaviour / test scoping: ~31
- production-widget-scope.spec.ts x5 (chromium-desktop): testid `add-selected-generation-to-timeline` no longer rendered; a vitest asserts its absence (GenerationsPaneGallery.test.tsx:556) (V). Tasks tests expect an "Export ... result" button on admitted tasks (not found, L). Rewrite. ~1 day.
- public-astrid-vision-hierarchy x6 and sigils-nav x6 (condensed=iPad Mini, mobile=iPhone 13): hover CSS only under `@media (hover:hover) and (pointer:fine)` (PublicAstridVision.css:673,707,1292,1950) while these specs run on touch projects; chromium-desktop passes (V). Add to DESKTOP_ONLY_SPECS. 0.5 day.
- public-astrid-integrated.spec.ts:124 x3: `.astrid-vision-part h3 button` not found; spec does not stub the vision feed, page depends on live raw.githubusercontent.com feed (L; component code has the selector, PublicAstridVision.tsx:178-180). Stub feed. 0.5 day. Vision-hierarchy specs also fetch the live feed (spec line 4-5, V): external-network dependency.
- video-editor-workflow-parity x6 (:27 asset registry lacks generation-gallery; :133 render dialog Download/`__savedFilm` never closes) and video-editor-instance-lifecycle x1 (:34 focus not in dialog): cause not established (L); product vs stale needs a read of the editor code. 1-1.5 days.
- extension-visual-regression:154 x1 (+4 not run): baseline size mismatch; may resolve with cause 1, else re-baseline. 0.5 day.

### 5. quick-journey (Lanes) 1: test bug
three-products.spec.ts:96-99 sets `journey.sources` only when ASTRID_QUICK_DESCRIPTOR is unset; afterAll at :196 always `expect(revisionSet()).toEqual(journey.sources)`. In the quick tier sources is undefined, so this always fails (V code; that the journey sets ASTRID_QUICK_DESCRIPTOR is L, the journey source is in the Agent repo). Failed identically in 4 runs. Printed log is truncated, so a masked earlier failure cannot be excluded. 0.25-0.5 day.

## Direct Journey (main, schedule)
Last 7 scheduled runs on main: failure x5 (18-23 Nov), success 16-17 Nov; 24 Nov 03:17 run not present yet at 10:30 UTC. Run 45179767614 (e0da794a): direct-journey ok, three-products fail: one unexpected failure `three-products.spec.ts:3690 empty bootstrap` (assert at :3715 `automaticAttempt` expected false got true; likely product/test regression: automatic first-timeline creation attempted). Gate wants exactly 4 allowlisted expected failures + 0 unexpected. Other days' causes not read. Est 1 day.

## Pins
- runtime.lock.json source_commit 24e2c929 (was 737843e9), producer_version sha256:69cdb4b7... unchanged.
- config/astrid-cli-surface/vendor.lock.json source_commit a09ea669 (was 0615e4e9), producer_version sha256:51f4f0ca... unchanged.
- public/install-manifest.json: agent a09ea669, runtime 24e2c929 (schema_digest sha256:2c6a76e1... unchanged), pack astrid_motion 2379ab54.
Lanes/E2E checkouts use manifest pins. All red runs ran the OLD pins; the repin is untested (cancelled). None of the failure causes above is pin drift by evidence; if the new Runtime added the packs routes the fake still lacks them. Nothing shows the repin changes failures.

## Skip / known-failure guards
- config/testing/skipRegistry.mjs: 9 declared skips, 10 lanes; no owner/expiry fields; strict: reporters fail any undeclared skip, check-skip-registry fails declared skips with no CI job, check-no-raw-skips bans .skip/.only (Tests job output confirms "9 declared skips, 10 lanes; 0 with no CI job").
- scripts/quality/check-known-failures.mjs: 0 allowed in src; 4 named exceptions in config/testing/direct-journey-expected-failures.json (P39-R12-DUP-SHOT, EXT-BATCH, TASK-SWAP, VIDEO-DROP; owner "Plan 39 manager", issues #249-252), ALL expire 2026-11-25 (tomorrow). Guard fails on expired entries or >14 days out, so Tests will go red tomorrow unless renewed or the tests fixed. Max 10 quarantine entries.

## Unknown
Why d53685f3 was cancelled; whether the repin passes; causes of editor-tour, extension-harness, workflow-parity, instance-lifecycle, extension-visual (need fake-runtime fix first); real Runtime route table (private repo); Direct Journey failures other than 23 Nov.

## Effort (worker-days): cause1 1-2, cause2 0.5, cause3 1, cause4 3-4, cause5 0.25-0.5, Direct Journey 1, expiry 0.25. Total about 7-9, ordered so cause 1 first (re-measure remainder).
