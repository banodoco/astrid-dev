# Plan 39: astrid-app wiring, quick journey, Direct Journey, quarantine, three-products structure

Read-only research, 24 Nov 2026. Repo head: `release/15/main` = `d53685f3adfc4ed725936b4a9d7ebc435dedbcc0` (PR #384). Cited line numbers are at that head unless marked "lanes.yml (copy)". Logs: `logs/` (full quick-journey job log, 45231479588) and `dj/` (Direct Journey job logs, 18-23 Nov). Verified = read in code or log; inferred = reasoned from the evidence, not run.

Corrections to earlier notes:
- Direct Journey scheduled failures on main are **six** (18, 19, 20, 21, 22, 23 Nov), not five. 19 Nov is infrastructure (apt 503s), not a test failure.
- The quarantine guard goes red on **26 Nov** (UTC), not 25 Nov: `scripts/quality/check-known-failures.mjs:131` fails only when `daysLeft < 0`, and 25 Nov gives `daysLeft = 0`.
- The job log of quick-journey 45231479588 is not truncated (the fetched REST log is 6,402 lines, the same as the saved copy). Its only failure is the afterAll `expect` (see card A4), and the test body's own outcome is not printed in it.

---

## Answers to the five questions

**1. CI wiring (12 failures).** Three separate causes:
- `checkout-lanes` launches Chromium with no install step (card A1). Verified.
- `command-outbox.spec.ts:31` falls back to the literal `/opt/pw-browsers/chromium`, which does not exist on hosted runners (card A2). Verified.
- The 10 viewing-parity failures are not an env-var gap. `VIEWING_BROWSER_FLOCK_HELD` is only a marker. `assertRunBoundary()` (`tests/e2e/timeline/viewing-parity/harness.ts:108-113`) also requires that a *different process* holds `flock` on `/tmp/timeline-viewing-browser.lock` (`flock -n ... true` must return 1), then checks a QUIET marker, and `harness.ts:264` runs it in the worker fixture. CI would need a wrapper that holds the lock for the whole run, and that is not enough: `browser-profile.ts:7-12` and `harness.ts:15-17` pin binaries at `/opt/pw-browsers/chromium-1194/...` (Chromium 141.0.7390.37, sha256 `85918a99...`), `/opt/pw-browsers/chromium_headless_shell-1194/...` (export hash `63eca986...`) and `/opt/google/chrome/chrome` (155.0.8059.84, sha256 `cb19b599...`). Hosted CI installs chromium-1223 (log 45231479752: `chromium_headless_shell-1223`), so none of the pinned bytes exist there. Card A3, owner decision.

**2. Lanes quick-journey.** The job's only error is `three-products.spec.ts:196`, `expect(revisionSet()).toEqual(journey.sources)`. In quick mode `journey.sources` is never set: the guard at `:87` skips the setter at `:99` when `ASTRID_QUICK_DESCRIPTOR` is set. The full log (run 45231479588, job 137891867585) shows no earlier failure. `checkout-lanes` (same run) fails only on the runtimePackRefresh test (A1). The gate ends with "No test passed in this run" and "1 failed: three-products.spec.ts:3435 quick: ...". Whether the quick test's body also failed is not in the log. Card A4.

**3. Direct Journey, scheduled on main (18-23 Nov, all six failures).**

| Night (run) | App / Agent / Runtime head | Cause (log) |
|---|---|---|
| 18 Nov (44298512172) | de7dd1e6 / 9814193a / 6855dfa8 | `:417` concurrent edit, `getByRole('alertdialog', 'This timeline changed somewhere else')` not visible in 90 s. One unexpected failure, and the serial cascade skips 11 later tests, so the four allowlisted tests never ran. |
| 19 Nov (44518171061) | not checked (18 and 22 Nov had the same heads) | Infrastructure: `apt-get` 503 / connection failures from security.ubuntu.com in the install step, in both jobs. Journey never ran; jq found no report. |
| 20, 21, 22 Nov (44730793539, 44898311042, 45018082335) | 22 Nov checked: same as 18 Nov; 20 and 21 not checked | Same as 18 Nov: `:417` fails, 11 skipped. |
| 23 Nov (45179767614) | e0da794a / c0ad6b54 / 5120462d | `:417` passes. Four allowlisted tests fail as expected (`:1922`, `:2103`, `:2442`, `:3216`). One unexpected: `:3690` empty bootstrap, `expect.poll(() => automaticAttempt).toBe(false)` at `:3715` times out at 5 s. The automatic first-timeline POST never reached the route. |

`direct-journey` (the other job) passed on every night except 19 Nov. Verified from logs; the cause of the 23 Nov `:3690` timeout is inferred (card A7). The change of `:417` between 22 and 23 Nov coincides with all three heads moving; which one fixed it is not established.

**4. The four quarantined tests.** All four expire on 2026-11-25 with owner "Plan 39 manager". See cards Q1-Q4 and the expiry card E1. The guard runs in `npm test` → `npm run test:app` → `check:known-failures` (`package.json:31-32`), in the `vitest` job of `.github/workflows/test.yml:195-236` (`- run: npm test` at `:236`). That job runs on push to main and `release/*/main`. Verified.

**5. Three-products spec structure (SF1a/SF1b).** Engineering size is in card S1 and S2. Short form: 14 ordinary tests (plus one quick test), each body using the worker-scoped `seed3` and a shared `astrid` CLI; `harness.seedThreeProducts()` is memoized per harness (`tests/e2e/local/support/harness.ts:1437-1438`) and builds on the one bootstrap head (`:1256`, `:1436`), so a per-test seed needs a repeatable seed path. The four leak patches (App `e2d48f428`, `d9e2798d4`, `7a971cea5` and the gate 5 reset, per `p39-inputs.md:131`) are not in this clone and I could not verify them.

---

## Cards

### A1. checkout-lanes has no Chromium install (runtimePackRefresh)
- Repo: astrid-app. Cluster: `ci:` CI wiring; failing test `src/tools/video-editor/runtime/runtimePackRefresh.integration.test.ts:145` (1 test). Config: `config/testing/lanes.ts:19`.
- Kind: **env**. Evidence: log 45231479588_137891867594 `browserType.launch: Executable doesn't exist at /home/runner/.cache/ms-playwright/chromium_headless_shell-1223`; `.github/workflows/lanes.yml` `checkout-lanes` (lines 63-78) runs `npm ci` and `npm run test:checkout` with no `playwright install`. The only Playwright install in lanes.yml is quick-journey (`:190`).
- Fix: after `Install App dependencies` (`lanes.yml:63-65`), add `npx playwright install --with-deps chromium` with `working-directory: astrid-app`.
- Scope: `.github/workflows/lanes.yml` (checkout-lanes steps only).
- Proof: hosted Lanes `checkout-lanes` passes the runtimePackRefresh test. With the install step removed, the test still fails with the current "Executable doesn't exist" message.
- Route N, 0.25 day. Deps: none. Confidence: verified.

### A2. command-outbox hard-codes a browser path
- Repo: astrid-app. Cluster: `ci:` timeline; `tests/e2e/timeline/command-outbox.spec.ts:48` (1 test).
- Kind: **env** (a default path inside the test, the case the triage rules forbid as a fix). Evidence: `command-outbox.spec.ts:31` `process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ?? '/opt/pw-browsers/chromium'`; log 45231479752 `Failed to launch chromium because executable doesn't exist at /opt/pw-browsers/chromium`. The timeline job does run `npx playwright install --with-deps chromium` (`.github/workflows/e2e.yml:67`), so the bundled browser exists.
- Fix: no literal default. Use `process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ?? chromium.executablePath()`, and throw "run npx playwright install chromium" if that path does not exist. Note `tests/e2e/local/support/app.ts:142` has the same `/opt/pw-browsers` fallback; it is not in the failing list, so leave it to a separate card.
- Scope: `tests/e2e/timeline/command-outbox.spec.ts:30-33` (`resolveChromium`).
- Proof: `npx playwright test --config playwright.config.ts --project=timeline-devices tests/e2e/timeline/command-outbox.spec.ts` on the hosted timeline job; with the browser removed, the test refuses with the new message.
- Route N, 0.25 day. Deps: none. Confidence: verified.

### A3. viewing-parity x10 needs a lock holder and pinned browsers
- Repo: astrid-app. Cluster: `ci:` timeline; `tests/e2e/timeline/viewing-parity/cases.ts:240, 257, 278, 288, 328` (5 tests, each reported twice; 10 failures in log 45231479752_137891869335, `AssertionError: central browser flock marker required`).
- Kind: **env**. Evidence: `harness.ts:110-112` (marker and flock check); `harness.ts:264` (fixture calls it); `browser-profile.ts:4-20` (pinned binaries and hashes); `harness.ts:15-17`. Hosted CI does not install these paths or bytes (it installs chromium-1223).
- Fix options (owner decides): (a) provision the three pinned binaries in a hosted setup step, hash-checked, and run the timeline cases under a wrapper that holds `/tmp/timeline-viewing-browser.lock` and sets `VIEWING_BROWSER_FLOCK_HELD=1` for the whole run; (b) run viewing-parity outside hosted CI on the machine that owns those browsers and the lock. Setting only the variable is a stub: the second `flock -n` check fails without a real holder.
- Scope: `.github/workflows/e2e.yml` (playwright-timeline job) and a new setup step; no change to `harness.ts` tests.
- Proof (a): hosted timeline job passes these 10 IDs; the hash check fails when the binary is changed. Proof (b): the cases are removed from the hosted project list with an owner-approved registry entry (skip registry rules apply; a silent exclusion is not allowed).
- Route X, 1-2 days for (a), inferred. Deps: owner decision. Confidence: verified (mechanism); size inferred.

### A4. Lanes quick-journey: afterAll expects sources that quick mode never sets
- Repo: astrid-app. Cluster: `lanes:` quick-journey (1 failure); `tests/e2e/local/three-products.spec.ts:3435` (quick test) and the afterAll at `:183-197`.
- Kind: **stale-test** (the quick-mode guard at `:87` was changed for the quick tier; the afterAll at `:196` was not). Source: the guard itself and the quick tier comment in `.github/workflows/lanes.yml` (lines 118-125 in copy). The quick branch is in the file at `2dc109b` (11 Nov), the latest commit in our history touching these lines, so the afterAll predates nothing newer. Verified.
- Fix: in quick mode, record the tuple too: set `journey.sources = revisionSet()` on the quick branch of the beforeAll (around `:87-99`), so the afterAll still proves the tuple is fixed through the run.
- Scope: `tests/e2e/local/three-products.spec.ts:84-100` (beforeAll).
- Proof: `ASTRID_QUICK_DESCRIPTOR=<descriptor> npx playwright test --config=playwright.three-products.config.ts` locally, and the hosted quick-journey job. Confirm the quick test body passes, which the current log does not show (the journey echoes only the stderr tail; the uploaded `quick-journey.txt` artifact was not fetched, since artifact downloads need a token).
- Route N, 0.25 day. Deps: none (A1 is separate). Confidence: verified for the afterAll failure; body outcome unverified.

### A5. Direct Journey :417 concurrent-edit failure, 18-22 Nov
- Repo: astrid-app. Cluster: `direct:` three-products; `tests/e2e/local/three-products.spec.ts:417` (concurrent edit). Single unexpected failure; the serial cascade skipped 11 tests.
- Kind: **unknown**. Evidence: jobs 136828612299 et al. `Locator: getByRole('alertdialog', { name: 'This timeline changed somewhere else' })`, element not found after 90 s; passed on 23 Nov with App e0da794a, Agent c0ad6b54, Runtime 5120462d (source tuples in the logs). Five consecutive nights on the same sources is not flaky; the cause is not in the logs.
- Fix: diagnose within two hours (the failing run's trace is in the `three-products` artifact, not fetched; compare the conflict dialog code path between de7dd1e6 and e0da794a). No fix proposed until then.
- Proof: none yet; if the diagnosis finds a product bug, route to Q-type card.
- Route N (diagnosis), then X if product. Size 0.25 day diagnosis. Deps: none. Confidence: inferred.

### A6. Direct Journey :3690 empty bootstrap, 23 Nov
- Repo: astrid-app. `tests/e2e/local/three-products.spec.ts:3690-3715`; app effect `src/tools/video-editor/pages/VideoEditorPage.tsx` (first-timeline effect around `:616-632`).
- Kind: **unknown** (diagnose first). Evidence: log 45179767614 job 137710233961: `Timeout 5000ms exceeded while waiting on the predicate`, `automaticAttempt` still true at `:3715`. The effect fires only when the timelines query returns an empty list and the project is not yet in `attemptedFirstTimelineProjects`. Commit `f10d664` (Plan 77, 23 Nov 16:05 +0100) changes `VideoEditorPage.tsx` but is **not** in `e0da794a`, so it does not explain this run. The test's 5 s `expect.poll` default may be too short for a cold page, or the effect condition may have changed; not separable from the log.
- Fix: diagnose (two hours). If the App never issues the POST, product-bug (fix ≤1 day). If it is a timing issue, a stale 5 s default, which is a flaky-kind fix (20 paired trials).
- Route N (diagnosis). Deps: none. Confidence: inferred.

### E1. Quarantine expiry (2026-11-25): Tests goes red on 26 Nov
- Repo: astrid-app. `config/testing/direct-journey-expected-failures.json` (four entries, expiry `2026-11-25`); `scripts/quality/check-known-failures.mjs:17, 131-132` (MAX 14 days out; expired when `daysLeft < 0`).
- Kind: process (owner decision), not a test verdict. Job: `.github/workflows/test.yml` `vitest` (`npm test`, line 236).
- Options: (a) renew the four entries to ≤14 days out, which the guard allows, with a new expiry and an owner note (this is the owner's call; triage rules forbid widening the ceiling silently); (b) fix the four tests (Q1-Q4). Note the entries also expire the same day the Q cards would be due.
- Route: owner. Deps: Q1-Q4. Confidence: verified.

### Q1. #249 Duplicate shot saves nothing (P39-R12-DUP-SHOT)
- Repo: astrid-app. Test `three-products.spec.ts:2442` (marker at `:2473`). Issue #249 (open, filed 11 Nov).
- Kind: **product-bug**. Evidence: issue #249 cites commit `7b33f8f50` (22 Oct) removing the native duplicate mount; the commit is not in this clone (could not verify). Current marker: `test.fail(true, 'Duplicate shot saves nothing since 7b33f8f50 ...')` at `:2473`.
- Fix (per the issue): re-mount the native duplicate path in `AstridTimelineEditor.handleDuplicateDocumentShotGroup` and `VideoEditorProvider` (about 60-80 lines across 5 files), restore three removed tests. The issue estimates 2.5-3.5 h, but it touches the editor's provider: treat as coupled.
- Scope: the five files named in #249 (not verified against code).
- Proof: the test at `:2442` passes with its marker removed; restored tests pass.
- Route X (coupled reasoning, editor provider). Size 0.5-1 day (inferred from the issue). Deps: none. Confidence: inferred.

### Q2. #250 Extension batch needs a replacement driver (P39-R12-EXT-BATCH)
- Repo: astrid-app. Test `three-products.spec.ts:1922` (marker at `:1949`). Issue #250 (open).
- Kind: **stale-test** for the driver (it depends on the Scene Phase Markers extension, deleted by `aa6683590` on 21 Oct, per the issue; that commit is not in this clone). The user behaviour it covers (multi-clip move and hold as one outbox intent, with lost ACK, restart and undo) is current and must stay tested. Not retired.
- Fix: a replacement driver: either an inline test-only extension that emits the same public patch (issue option 1), or a production multi-clip action driven from the UI (option 2).
- Scope: `tests/e2e/local/three-products.spec.ts:1922-2100` (test body only) and the test-support extension.
- Proof: the test passes with its marker removed.
- Route X, 1-1.5 days. Deps: none. Confidence: inferred from the issue.

### Q3. #251 Agent cannot commit a swap to a task-output handle (P39-R12-TASK-SWAP)
- Repo: **astrid-agent**, not this repo. App test `three-products.spec.ts:3216` (marker at `:3281`). Issue #251 (open).
- Kind: **product-bug** (Agent). Evidence per issue: `commit_session` only builds verified-media rows for local imports; handle inputs have no `generationId`/`variantId` (`media_handles.py:498`, `publish.py:30`, per the issue). Not verified here (Agent repo not read).
- Fix (issue): build a verified row for raw-pin handle inputs in `commit_session`, or attach catalog ids in `resolve_timeline_asset`.
- Route X (provenance of media, data integrity: consider S). Size: not estimated here; Agent card. Deps: Agent card. Confidence: from issue only.

### Q4. #252 Dropped video is lost on reload (P39-R12-VIDEO-DROP)
- Repo: astrid-app. Test `three-products.spec.ts:2103` (marker at `:2213`). Issue #252 (open, Plan 39 item).
- Kind: **product-bug**. Evidence: `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:432-439` refuses any non-image prepared-media add (per the issue; line numbers not re-checked). The user's dropped media is silently lost on reload, and the refusal text is false ("Draft retained"), so the data-safety rule applies.
- Work in progress (verified): branch `origin/scratch/r12-drop-fix` (fetched). Commits `f530e00` (native clip.add-media for video and audio), `e57507a` (truthful refusal messages) and `85125e6` (e2e test: video dropped on a fresh project survives reload) are on that branch and **not** in `release/15/main`. Head `e95eb28` is a WIP commit from 11 Nov. Branch `scratch/r12-audio-drop` (`9e454fac`) holds audio WIP.
- Fix: rebase the drop-fix commits onto `release/15/main`, finish audio routing, make the three-products test pass.
- Scope: `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts`, `src/tools/video-editor/hooks/useTimelineSave.ts`, plus the test files on the branch.
- Proof: the test at `:2103` passes with its marker removed; the branch's new e2e test passes on a fresh project; reload keeps the clip.
- Route S (data safety: user media loss), 1-2 days (inferred). Deps: none. Confidence: branch contents verified; the rebase size inferred.

### S1. SF1a: three-products tests own their seed
- Repo: astrid-app. `tests/e2e/local/three-products.spec.ts` (`seed3` at `:54-62`, `mode: 'serial'` at `:83`, 14 ordinary tests `:417` to `:3690`, `nativeNoneTest` at `:2804`); `tests/e2e/local/support/harness.ts:1437` (`seedThreeProducts`, memoized by `this.threeProductsSeed`), `:1497` (`createFreshProject`); `playwright.three-products.config.ts:12-18` (`workers: 1`).
- Kind: not a failing test: a structural change from `p39-tasks.md:139`.
- Size: this is the bigger of the two.
  - Harness: make the seed repeatable on one Runtime, keyed by project: each call creates a project and bootstrap timeline, runs `enableTimelineAuthoring`, the media imports and `commitNativeSeed` (today `initialize: !this.seedInitialized`, `:1437-1485`, and `seedHead` checks). About 1 day, route X.
  - Spec: 14 tests change from `seed3` to a per-test seed (`seed3` is mentioned on 376 lines; the seed's fields are read on about 106 lines). The `astrid` CLI fixture (about 59 lines) binds to one project slug and must be per test. Replace the bootstrap tests' reliance on `mostRecentlyCreatedProject` (`:3518`, App `VideoEditorPage.tsx`) with explicit `?project=` URLs (already used at `:3713`).
  - The four leak patches (App `e2d48f428`, `d9e2798d4`, `7a971cea5`, gate 5 reset) are removed only after each test's independence is shown; not verifiable here.
  - Estimate: 3-4 engineering days, route X, consistent with `p39-tasks.md:139` "X".
- Proof: `npm run test:e2e:three-products` passes, and passes with tests declared in reverse order; `grep -n "mode: 'serial'"` is empty; a throwaway failing first test lets all later tests run.
- Deps: RS1 (from Plan 39 tasks). Confidence: verified structure; size inferred.

### S2. SF1b: shuffled and parallel
- Repo: astrid-app. `playwright.three-products.config.ts` (`workers: 1`, port shared with direct journey), `.github/workflows/direct-journey.yml` (nightly seed).
- Kind: structural (`p39-tasks.md:140`). Route N, 1-2 days after S1. Deps: S1, and the Runtime door per worker (harness change). Proof: `ASTRID_E2E_SHUFFLE_SEED=<n> npm run test:e2e:three-products -- --workers=2` passes for three seeds (from `p39-tasks.md:140`). Confidence: inferred.

---

## Could not verify
- Commits `7b33f8f50`, `aa6683590`, `e2d48f428`, `d9e2798d4`, `7a971cea5` are not in the clone (fetch only covered the branches named). Issue texts were used for them.
- The quick-journey test body outcome and the uploaded Playwright artifacts (`quick-journey.txt`, `three-products` traces, error contexts) were not downloaded (artifact downloads need a token).
- The 23 Nov `:3690` cause, and which side fixed `:417` between 22 and 23 Nov.
- Whether the pinned Chromium 141 / headless-shell 1194 / Chrome 155 bytes can be obtained with the expected hashes.
- Agent-repo claims in Q3 (`media_handles.py`, `publish.py`) were not read.
