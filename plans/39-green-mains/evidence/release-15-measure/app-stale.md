# App E2E: stale, env and unknown cards (not the fake-Runtime route gap)

Read-only triage, 24 Nov 2026. Scope: the App E2E failures in app-green/REPORT.md that are not cause 1 (fake Runtime route gap). Failing-ID counts are from the E2E run 45231479752 (commit 3f5da385, App head d53685f3), the logs in app-green/logs/ (`*_45231479752_*`). The App code is read at `d53685f3adfc4ed725936b4a9d7ebc435dedbcc0` (the release/15/main head, equal to FETCH_HEAD when I started). Paths are relative to the App repo unless marked. Plan 91 triage rules were read from banodoco/astrid-dev `plans/91-agent-main-green/tasks.md` at `33896625` (lines 25-45).

## Dating caveat (applies to every stale-test verdict)

The App's 328-commit history is snapshot-grafted. `git log -- <spec>` returns only `2dc109b` (2026-11-11 22:55) for the affected specs, and `f72e869` (2026-11-11 12:27) for the component code. Both commits add the whole tree, so per Plan 91 rule 2 they do not prove that a source postdates a test. Postdating below uses PR data from the GitHub API (banodoco/astrid-app), not git dates. Where no postdating source exists I say so and the verdict drops to unknown.

Card ids are placeholders (APP-xx).

---

## APP-01 production-widget-scope: removed add-to-timeline button and Export label (5 IDs)

- Repo: astrid-app. Cluster: App cause 4 (stale tests). Failing IDs, all `chromium-desktop` (the file is in `DESKTOP_ONLY_SPECS`):
  - `tests/e2e/production-widget-scope.spec.ts:53` (Gallery refuses foreign project)
  - `:64` (Gallery targets selected dialog, same project)
  - `:89` x2 (Tasks selects dialog query, same and different project)
  - `:111` (Tasks recovers admitted task after close/reopen)
- Kind: **stale-test**. Evidence:
  - The testid is gone from product code. `src/` contains no `add-selected-generation-to-timeline` and no "Add selected to timeline". The only hits are the unit test `src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx:556-557`, which asserts absence and is named "shows no bar button after selection and passes the timeline add to the tiles" (`:544`). The spec's `gallerySend` (`production-widget-scope.spec.ts:46-50`) and `:56-57` still require it. Log: `Locator: getByTestId('add-selected-generation-to-timeline')`, element not found, at spec `:57`.
  - The export control's name changed. `src/features/tasks/components/TasksPane/RuntimeTaskRow.tsx:116` labels the row button `Export ${label} as a video file` (visible text "Export", `:119`). The dock button is `RuntimeActivityDock.tsx:269`, named "Export render". The spec's `exportButton` (`production-widget-scope.spec.ts:46`) matches `/^Export .* result$/`, which neither matches. Log at spec `:95`: row text "RenderJust nowExport", no button matched.
  - Postdating: the unit test and the spec are in the same graft commit, so git cannot date them. I found no PR that removed the bar button (GitHub search for "Add selected to timeline", the testid and "selection bar" returned no PRs). The closest PR, `#314` (2026-11-19), is unrelated.
- Fix: (a) add to a tile the way `GenerationsPaneGallery.test.tsx:544-560` describes (`onAddToTimeline` on the MediaGallery tile), and point `gallerySend` (spec `:46-50`) at the tile control; (b) change `exportButton` (spec `:46`) to `/^Export .* as a video file$/`, or to the dock's "Export render" if the dock is the surface under test. The `:53` and `:64` tests then assert their scope as before.
- Scope: `tests/e2e/production-widget-scope.spec.ts` (`gallerySend` `:46-50`, `exportButton` `:46`, and the `add` locator `:56-57`). No product file changes.
- Focused proof: `npx playwright test tests/e2e/production-widget-scope.spec.ts --project=chromium-desktop`; `npx vitest run src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/features/tasks/components/TasksPane/RuntimeTaskList.test.tsx`.
- Route N. Size 1 day. Deps: none (not cause 1; no fake route used except `:111`, which hits the fake task routes, already in cause 1).
- Delete or fix: **fix**. Nothing here is retired; the Export and tile-add journeys are what users do today.
- Confidence: verified in code that the testid and label changed. Inferred that the spec is stale rather than the product regressed. Open: the bar removal has no postdating source I could find. If the owner or the card cannot cite a PR or plan line, the rule sends it to `unknown` (2 h diagnosis) before any edit.
- Open question: should the Tasks journey use the row button (`as a video file`) or the dock button (`Export render`)? Both exist.

## APP-02 Vision hover specs run on touch projects (12 IDs)

- Repo: astrid-app. Cluster: App cause 4. Failing IDs (each on both `chromium-condensed` and `chromium-mobile`, and a passing `chromium-desktop`):
  - `tests/e2e/public-astrid-vision-hierarchy.spec.ts:175`, `:381`, `:435` (3 x 2 = 6)
  - `tests/e2e/public-astrid-vision-sigils-nav.spec.ts:51`, `:72`, `:352` (3 x 2 = 6)
- Kind: **env**. The test asks for a fine pointer and hover, and the device project gives a touch pointer. The product is correct: hover styles are only for fine pointers.
  - CSS gating: `src/pages/Home/PublicAstridVision.css:673`, `:707`, `:1292`, `:1950` are `@media (hover: hover) and (pointer: fine)`. `:177` is `(hover: hover)` only.
  - Projects: `playwright.config.ts:170-181` runs `chromium-condensed` (iPad Mini) and `chromium-mobile` (iPhone 13) with `devices[...]`, which set `hasTouch`/`isMobile`. `DESKTOP_ONLY_SPECS` (`playwright.config.ts:90`) excludes only the three listed files.
  - Failure lines: hierarchy `:199-200` (`::after` opacity 0, want 1), `:399` (animation-name none), `:452`; sigils `:64`, `:91` (transition 1s not 3s), `:370`.
- Fix: keep these tests on every project, but give the hover assertions a fine-pointer input. In each of the 6 tests (or one `test.describe` wrapping each), add `test.use({ hasTouch: false, isMobile: false })`. The viewport stays as the project sets it. Mobile-only tests in the same files keep running on the touch projects.
- **Reject the proposed `DESKTOP_ONLY_SPECS` entry for these files.** File-level exclusion would delete coverage of tests that pass on the touch projects today: `public-astrid-vision-hierarchy.spec.ts:129` (mobile card), `:205` (mobile modal), `:255` (first touch outside dialog), `:312`; `public-astrid-vision-sigils-nav.spec.ts:126`, `:155`, `:214`, `:266`, `:313`. Plan 91 rule 3 (tests of what users do today are never deleted) rules this out.
- Scope: `tests/e2e/public-astrid-vision-hierarchy.spec.ts` (tests at `:175`, `:381`, `:435`); `tests/e2e/public-astrid-vision-sigils-nav.spec.ts` (tests at `:51`, `:72`, `:352`). No product file changes.
- Focused proof: `npx playwright test tests/e2e/public-astrid-vision-hierarchy.spec.ts tests/e2e/public-astrid-vision-sigils-nav.spec.ts --project=chromium-condensed --project=chromium-mobile`, and the same for `chromium-desktop`.
- Route N. Size 0.5 day. Deps: none. Also do APP-04 in the same files (both touch the same `FEED` lines).
- Delete or fix: **fix**.
- Confidence: verified in code and in the logs (the failing lines and the project list). Not verified: that `hasTouch:false` alone flips `(pointer: fine)` in the iPad viewport. Check on the first run.
- Open question for the owner: should hover behaviour be tested on touch projects at all? My answer is no, but this is a coverage policy.

## APP-03 public-astrid-integrated A04/A05/A06/A07/A08 (3 IDs, 2 causes)

- Repo: astrid-app. Cluster: App cause 3 (env) plus an unknown. `tests/e2e/public-astrid-integrated.spec.ts:124`, failing on `chromium-desktop`, `chromium-condensed`, `chromium-mobile`.
- Cause A (desktop and condensed), kind **env**. Failure at spec `:160` (`.astrid-vision-part h3 button` not found, 5 s). The test visits `/vision` with no stub for the feed. The product fetches the live feed with no fallback (`src/pages/Home/publicVisionContent.ts:177`), and gaps render only from that feed (`src/pages/Home/PublicAstridVision.tsx:178-180`). The feed is fetched live over `raw.githubusercontent.com`. I fetched it on 24 Nov 2026 and it returns HTTP 200 with 22 gaps, so it is reachable now, but the CI fetch is a network dependency with no stub.
- Cause B (mobile only), kind **unknown**. Failure at spec `:156`: sky canvas height expected 189, received 159. The test expects `ceil((h+48)/6) + 2*ceil(120/6)` (`:154-156`). The product computes `rows = viewRows + 2*ceil(bleed/6)` from `clientHeight` and `previousFrame` (`src/pages/Home/PublicAstridSky.tsx:101-116`). The received value is consistent with a stale or differently measured `viewHeight`, not with a missing bleed. I could not run the page, so the cause is not established.
- Fix A: add `await page.route(FEED, route => route.fulfill({ json: visionFixture() }))` before `page.goto('/vision')` in the test (pattern: `tests/e2e/public-astrid-vision-aspirations.spec.ts:8-12`, `tests/fixtures/public-vision.ts` exports `visionFixture`, `legacyVisionFixture`). Fix B: diagnose in a trace (2 h cap) before changing anything.
- Scope: `tests/e2e/public-astrid-integrated.spec.ts` (test at `:124`, route added at the top of the test).
- Focused proof: `npx playwright test tests/e2e/public-astrid-integrated.spec.ts -g "daylight palettes"` on the three projects.
- Route: A N; B X (diagnosis, then re-route). Size: A 0.5 day, B 1 day. Deps: none.
- Delete or fix: **fix**.
- Confidence: A verified in code (no stub, no fallback, failing line). B inferred from the numbers. Not verified: that the CI failure was a fetch failure rather than a slow render.

## APP-04 Live vision feed in 12 vision specs (hermeticity, not failing this run)

- Repo: astrid-app. Cluster: App cause 3 (env, hermeticity). Specs: `tests/e2e/public-astrid-home-chips.spec.ts:131,241` and `public-astrid-vision-{aspirations,characteristics,content,entry,hierarchy,layout-feedback,mobile-catalogs,mobile-feedback,polish,sigils-nav,stability}.spec.ts`. Each one runs `request.get(FEED)` (or the literal URL) before `page.route`. Counts of live GETs per file: entry 15, hierarchy 11, mobile-catalogs 4, layout-feedback 3, aspirations/characteristics/content/mobile-feedback/polish/sigils-nav/stability 1-2 each, home-chips 2.
- Kind: **env**. The test needs a feed; CI supplies it live. The feed's content changes per commit (astrid-dev plan 48, `plans/48-one-record-model/tasks.md:219`), so a live pin can drift.
- Fix: replace each `request.get(FEED)` with `visionFixture()` or `legacyVisionFixture()` from `tests/fixtures/public-vision.ts` (already used by `public-astrid-vision-aspirations.spec.ts:4`, `:202`). For the hierarchy spec, which deletes `gap.aspiration` and `supportingAspirations` in each test (`tests/e2e/public-astrid-vision-hierarchy.spec.ts:10`, `:68`, and so on), use `legacyVisionFixture()`. Keep the route stubs.
- Scope: the 12 spec files listed; no product change.
- Focused proof: run the vision specs with the live URL blocked (`page.route('https://raw.githubusercontent.com/**', r => r.abort())`), which must pass.
- Route N. Size 0.5-1 day. Deps: none. Overlaps APP-02 and APP-03 (same files).
- Delete or fix: **fix**.
- Confidence: verified in code.

## APP-05 video-editor-workflow-parity: "the explicitly supported local browser renderer exports" (3 IDs)

- Repo: astrid-app. Cluster: App cause 4. `tests/e2e/video-editor-workflow-parity.spec.ts:133`, failing on all three projects. Failure at spec `:157` (`__savedFilm.closed` never becomes true).
- Kind: **stale-test**. Source: PR #128 "Fix browser downloads for timeline exports and completed renders" (banodoco/astrid-app, merged 2026-10-27, merge commit `4d4903ea`). Its body says: "Previously Chrome wrote them directly through its save-file picker, and render completion only opened the player. The player retains an explicit Download retry; larger files have an explicit streaming Save as… option." Product code now matches: the Download button calls `downloadRender()` without the picker (`src/tools/video-editor/components/TimelineRenderControls.tsx:331`), which uses an anchor download (`downloadRenderedFile`, `:244`). The picker is only on "Save as…" (`saveFilePicker` at `:217`, button at `:322-325`).
- Postdating: PR #128 (2026-10-27) changed `TimelineRenderControls.tsx`, its test and `tests/e2e/timeline/audio-reactive-colour-export.spec.ts`, but not `video-editor-workflow-parity.spec.ts`. The spec's own comment (`:132-134`, citing commit `f0cad8b19`, which is not in the fetched history) describes the pre-#128 behaviour, so the spec was last changed before 27 Oct. Inferred, not verified.
- Fix: in the test, click "Save as…" (the picker path, the one the stub serves) inside the "Rendered film" dialog, and keep the stub. Alternatively assert the anchor download with Playwright's `download` event on "Download" and leave the stub for "Save as…".
- Scope: `tests/e2e/video-editor-workflow-parity.spec.ts:133-157` (Download click at `:156`).
- Focused proof: `npx playwright test tests/e2e/video-editor-workflow-parity.spec.ts -g "explicitly supported local browser renderer"` on `chromium-desktop`, `-condensed`, `-mobile`.
- Route N. Size 0.25-0.5 day. Deps: none.
- Delete or fix: **fix**.
- Confidence: verified in code and PR body. Inferred: the spec predates PR #128.

## APP-06 video-editor-workflow-parity: "full/dialog save, reopen, canonical import..." (3 IDs)

- Repo: astrid-app. Cluster: App cause 4. `tests/e2e/video-editor-workflow-parity.spec.ts:27`, all three projects. Failure at spec `:79`: the asset registry has no asset with `generationId === 'generation-gallery'`, after clicking `gallery-send`.
- Kind: **unknown**. Two leads, neither confirmed:
  - The fixture's `gallery-send` (`tests/e2e/fixtures/editor-workflows/main.tsx:144`) sets only `timeline` and `addGenerationId`. The App's gallery now also sets `addGenerationProject` and `addGenerationTimeline` (`src/features/gallery/components/GenerationsPane/hooks/useGenerationsPaneController.ts:375-378`). The editor's drain effect takes a scoped branch when those are present (`src/tools/video-editor/contexts/VideoEditorProvider.tsx:542` and the scoped check just after). Without them, the legacy branch needs the editor to be active and the route timeline to match. My reading says the legacy branch should still fire, which is why this is not a confirmed stale fixture.
  - Diagnosis: run the test with the provider's `chrome/*` diagnostics printed.
- Fix: after diagnosis. If the fixture is off-contract, set the scoped params in `gallery-send` (stale-test, source: `useGenerationsPaneController.ts:375-378`, date unverified). If the provider drops the add, it is a product-bug; route X (the drain touches saves).
- Scope: `tests/e2e/fixtures/editor-workflows/main.tsx:144`, or `src/tools/video-editor/contexts/VideoEditorProvider.tsx` (drain effect, `:542-600`).
- Focused proof: the spec at `:27` on the three projects.
- Route N for the 2-hour diagnosis, then X. Size 1-1.5 days. Deps: none.
- Delete or fix: **fix**.
- Confidence: unknown.

## APP-07 video-editor-instance-lifecycle:34 (1 ID)

- Repo: astrid-app. Cluster: App cause 4. `tests/e2e/video-editor-instance-lifecycle.spec.ts:6`, `chromium-desktop` only (`playwright.config.ts:90`). Failure at spec `:34`: `document.activeElement` is outside any `[data-video-editor-instance]` (received undefined, wanted `dialog`), after `chrome.focus('button')` at spec `:30`.
- Kind: **unknown**. Leads:
  - `chrome.focus()` resolves the root through `shellRoot()`, which is `assembly.shellRootRef.current` (`src/tools/video-editor/contexts/editorRuntimeAssembly.tsx:977`), then `root.querySelector(selector)` (`src/tools/video-editor/runtime/extensionContextFactory.ts:381-400`). If the root or button is missing it reports a diagnostic and does nothing (`chrome/focus-no-shell`, `chrome/focus-missing-selector`). An undefined `activeElement` fits "no focus happened". The first `button` in the dialog root may be hidden or disabled.
  - The announce checks at spec `:27-28` pass, so the dialog root exists. That makes "root missing" less likely than "first button not focusable".
- Fix: after diagnosis, either target a focusable button by test id, or fix `focus()` to skip non-focusable matches (product, small).
- Scope: `tests/e2e/video-editor-instance-lifecycle.spec.ts:30` (test side) or `extensionContextFactory.ts:381-400` (product side).
- Route X (2 h diagnosis, then N or X). Size 0.5-1 day. Deps: none.
- Delete or fix: **fix**.
- Confidence: unknown. The fixture file is `tests/e2e/fixtures/editor-instances/main.tsx`, which I did not read in full.

## APP-08 preview-scrub-evidence:231 (chrome-export, 1 ID)

- Repo: astrid-app. Cluster: App cause 2 (stale helper). `tests/e2e/timeline/preview-scrub-evidence.spec.ts:231`, `timeline-chrome-export`. Call chain: `replaceConfig` (`:203`) at `:363` -> `publishFakeRuntimeComposition` (`tests/e2e/timeline/support.ts:264`) -> `POST .../composition-revisions` (`support.ts:276-283`) -> `if (!response.ok) throw` (`support.ts:286`) with 410 `retired_route`.
- Kind: **stale-test**. Sources:
  - The Runtime refuses this route: `legacy timeline writes are retired; submit EditCommands through commitTimeline` (Runtime `runtime_protocol/service.py:468`, the message introduced in commit `7d2ed00`, 2026-10-27, per `git log -S` in `astrid-runtime` at the pin `24e2c929`).
  - The App's shared fake refuses it on purpose: `src/test/fakeWorkspaceRuntime.ts:191` lists `POST .../composition-revisions` as retired, and `src/test/fakeWorkspaceRuntime.test.ts:107-131` asserts the refusal. The 410 body is `src/integrations/runtime/fixtures/responses/retired_route_410.json`, vendored from the Runtime.
  - Plan 39 (astrid-dev `plans/39-green-mains/plan.md:64`) already records "chrome-export gets retired_route from it".
- Postdating: the Runtime retirement (2026-10-27) postdates the helper if the helper was written earlier. The App history does not show the helper's own last change (graft), so this is inferred.
- Fix: rewrite `publishFakeRuntimeComposition` to publish with `commitTimeline` (`src/integrations/runtime/generated.ts:208`, `POST /v1/projects/{p}/timelines/{t}/commit`) using EditCommands. **Dependency:** the shared fake has no `/commit` route. `src/test/fakeWorkspaceRuntime.ts:553` throws `unexpected ${method} ${path}`, which the Playwright server turns into a 500 (matches the logged `commits?limit=50` 500). Adding the commit route to the fake is the work in cause 1. The helper cannot be fixed without it.
- Scope: `tests/e2e/timeline/support.ts:264-288` (helper); the fake commit route is outside this card's scope (cause 1 owns the fake).
- Focused proof: `npx playwright test tests/e2e/timeline/preview-scrub-evidence.spec.ts -g "correlates cold/repeat"` with `PLAYWRIGHT_TIMELINE_DEVICES=1` and the Chrome channel; plus `npx vitest run src/test/fakeWorkspaceRuntime.test.ts` (the refusal must still pass).
- Route X (commit semantics, idempotency, CAS). Size 1-1.5 days (incl. the fake commit route if it is taken in this card). Deps: fake commit route (cause 1).
- Delete or fix: **fix**. The refusal test stays.
- Confidence: verified in code and in the Runtime history. Inferred: helper written before 27 Oct.

## APP-09 editor-tour x4 (timeline-devices)

- Repo: astrid-app. Cluster: App cause 1 suspect, **not confirmed**. `tests/e2e/timeline/editor-tour.spec.ts:232`, `:323`, `:357`, `:375`. Failures: `act 1 welcome is ready` timeout (60 s) at spec `:250`, `:328`, `:363`; `skipped` outcome undefined at `:401`.
- Kind: **unknown**. Refuted lead: the spec reads `GET /v1/app-state/user/editor-tour` (`:213-216`, `:221`). The e2e server forwards `/v1/` to the shared router (`tests/e2e/fake-runtime/server.ts:308`), which implements app-state (`src/test/fakeRuntimeRouter.ts:734`). So the app-state route is not missing. The 404s in the log are for `commits`, `objects/sha` and `packs/inventory`, not app-state.
- Fix: diagnose the first beat (a 60 s wait on the tour store, `:55`). Check whether `tourState` (`:43-47`, module `/src/shared/state/editorTourStore.ts`) ever reaches `running`.
- Scope: TBD after diagnosis.
- Route X. Size 1 day. Deps: none confirmed.
- Delete or fix: **fix**, not retire (it covers the first-run tour, a user journey).
- Confidence: unknown. REPORT's "probably same cause" should be dropped for app-state.

## APP-10 extension-harness "disable/enable persists..." (3 IDs)

- Repo: astrid-app. Cluster: App cause 1 (fake Runtime). `tests/e2e/extension-harness.spec.ts:273`, all three projects. Failure at `:284`: package state `runtime-error` (wanted `loaded`).
- Kind: **env** (the fake does not provide the pack inventory the App asks for). Evidence: the loader calls `${runtimeApiBase()}/packs/inventory` (`src/tools/video-editor/runtime/extensionLoader.ts:89`), which returns `loader/not-admitted` on a non-OK response. The fake returns 404 `no fake route` for non-`/v1/` paths (`tests/e2e/fake-runtime/server.ts:213-223`). `packs` appears nowhere in `tests/e2e/fake-runtime` or `src/test`. The spec uses the real manager and loader (`src/tools/video-editor/pages/ExtensionHarnessPage.tsx:590-625`).
- Fix: add the pack inventory route (empty or with the manager-cycle pack record) to the fake. Owned by cause 1.
- Route N (within cause 1). Size: part of cause 1's 1-2 days. Deps: cause 1 card.
- Delete or fix: **fix** (through cause 1).
- Confidence: verified in code (route absent, loader path). Inferred: the `runtime-error` state comes from that failure. Not verified by running.

## APP-11 extension-visual composed desktop baseline (1 ID, 4 not run)

- Repo: astrid-app. `tests/e2e/extension-visual-regression.spec.ts:154`, `desktop composed timeline`, `chromium-visual`. Failure: `.timeline-wrapper` 1414x319 received, 1374x303 expected (34826 px differ, ratio 0.08). Baseline: `tests/e2e/visual-snapshots/composed-desktop.png` (1374x303, checked by reading its PNG header).
- Kind: **unknown**. Leads: the wrapper size is +40 px wide and +16 px tall, which fits a lane or footer change more than a font change. Cause 1 (the missing pack route) changes which extension lanes render, so it is a possible link. Not checked.
- Fix: diagnose from the CI artifact (`artifacts/extension-visual/test-results`, the actual vs expected PNGs). Re-baseline only if the UI change is intended (Plan 39 inputs.md line 88 says the same: "stale if the UI change was intended, otherwise bug").
- Scope: `tests/e2e/visual-snapshots/composed-desktop.png` (only if intended), or product.
- Route N (diagnosis). Size 0.5 day. Deps: cause 1 (check after packs route lands).
- Delete or fix: **fix** (either the baseline or the product).
- Confidence: unknown.

---

## Not in the list: deletions

No App test is **retired** or **redundant** by this triage.
- `production-widget-scope` `:53` and `:64` are not duplicated by the unit tests (the unit test asserts absence of the button, which is the other side).
- The Tasks Export is covered at unit level (`src/features/tasks/components/TasksPane/RuntimeTaskList.test.tsx`), but the E2E journey is user-facing, so it stays.
- The composition-revisions refusal already has a passing test (`src/test/fakeWorkspaceRuntime.test.ts:107-131`). It must stay.

## Proposed deviation from the brief

The brief's proposal (`DESKTOP_ONLY_SPECS` for vision hover) is rejected in favour of APP-02 (per-test fine-pointer emulation). File-level exclusion deletes passing mobile coverage, which Plan 91 rule 3 forbids.

## What I could not verify

- Any run. All verdicts are from logs, code at `d53685f3`, and API data. No test was run.
- Whether the App's CI network (for the live feed) was the cause of APP-03 A. It is plausible and the feed is live (I fetched it: HTTP 200, 22 gaps).
- The mobile sky row count (APP-03 B), the instance focus (APP-07), the workflow-parity add (APP-06), editor-tour (APP-09) and extension-visual size (APP-11).
- Postdating for APP-01 (no PR found that removed the bar button), APP-08 (helper's own change date) and APP-05 (the spec's date before PR #128 is inferred).
- The commit `f0cad8b19` cited in `video-editor-workflow-parity.spec.ts:134` is not in the fetched App history.
- Plan 91's `prune-candidates.md` (rule 0) covers Agent IDs; I did not find App IDs in it, but I did not read the file in full.

## Summary table

| Card | Failing IDs | Kind | Route | Size (days) | Deps | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| APP-01 production-widget-scope | 5 | stale-test (postdating open) | N | 1 | none | fix |
| APP-02 vision hover on touch | 12 | env | N | 0.5 | APP-04 | fix (per-test fine pointer) |
| APP-03 integrated A (feed) | 2 | env | N | 0.5 | none | fix (stub feed) |
| APP-03 integrated B (sky rows, mobile) | 1 | unknown | X | 1 | none | diagnose |
| APP-04 live feed in vision specs | 0 now (risk) | env | N | 0.5-1 | APP-02 | fix (fixture) |
| APP-05 workflow-parity render Download | 3 | stale-test (PR #128) | N | 0.25-0.5 | none | fix |
| APP-06 workflow-parity full/dialog save | 3 | unknown | N then X | 1-1.5 | none | diagnose |
| APP-07 instance-lifecycle | 1 | unknown | X | 0.5-1 | none | diagnose |
| APP-08 preview-scrub:231 | 1 | stale-test (helper) | X | 1-1.5 | fake commit route (cause 1) | fix |
| APP-09 editor-tour | 4 | unknown | X | 1 | none | diagnose |
| APP-10 extension-harness | 3 | env | N (cause 1) | in cause 1 | cause 1 | fix via fake |
| APP-11 extension-visual | 1 | unknown | N | 0.5 | cause 1 check | diagnose |
