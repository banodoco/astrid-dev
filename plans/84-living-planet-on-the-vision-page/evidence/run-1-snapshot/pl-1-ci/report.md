# PL-1 PR CI failure diagnosis

## Run identity and evidence

- Workflow run `45068430986`, “Public vision content”; pull-request event; attempt 1; branch `plan-84/pl-1`; head `05f5ce4bfdfbd1feb65bf869a9e18f19c1b98992`; overall conclusion `failure` (`run.json`). PR lookup identifies #371, “Port planet engine behind the Vision boundary,” base `e3dbad64d402724ac5a35fb6447f18e432c64b78` (`pulls.json`). The PR changes the planet engine and Vision page/component, not just the last commit (`pr-files.json`).
- Raw GitHub REST responses: `run.json`, `jobs.json`, `commit.json`, `pulls.json`, `pr-files.json`, `base-vs-baseline.json`, `artifacts.json`. The two job log endpoint responses are plain UTF-8 text and are retained as `job-137349723145.log` and `job-137349723395.log` (the `.log` suffix reflects the actual response; they are not ZIP archives). `job-137349723145.headers` records the HTTP response headers for a retry. API requests returned HTTP 200; retrieval commands used `curl -fsSL` and exited 0. No workflow was rerun or dispatched.
- Job summary: `home-apple-webkit` (`137349723145`) failed at step 6, “Verify mobile Home disclosure transitions with original media”; `vision-content` (`137349723395`) failed at steps 13, “Verify vision content on desktop and phone,” and 14, “Verify native dialog touch behavior in WebKit.” Setup, dependency install, canary syntax, changed-code lint, unit buckets, hosted build, and browser installation all succeeded (see `jobs.json`).

## Exact failures

### `home-apple-webkit`

One assertion failed; four tests passed. Log lines 241–264 identify `tests/e2e/public-astrid-home-chips.spec.ts:128:5`, “player projection stays steady on scrolled app return.” At test line 179, after clicking the Vision link and observing four principles, the test expects `<html>` to lose `data-astrid-page-transition`; after 5 seconds it is still present with value `vision` and style `shared` (log lines 243–260). The job summary and exit are at lines 280–283: 1 failed, 4 passed, process exit 1.

### `vision-content`, Chromium

The first browser step reports 5 failed and 117 passed (log lines 2112–2119). Exact failed cases and assertions:

1. `tests/e2e/public-astrid-vision-content.spec.ts:40:1`, “vision displays the GitHub-published pillars and operating principles”: `main.astrid-vision` was absent at assertion line 43 after navigation; 5-second visibility timeout (log lines 1838–1856).
2. The same file, line 169, “every chapter, Help us included, opens with one shared rule, pixel eyebrow and title”: expected 3 section heads, received 0 at line 173 (log lines 1875–1894).
3. `tests/e2e/public-astrid-vision-layout-feedback.spec.ts:106:1`, “only the new contribution section and workbench mink remain after the projects”: `.astrid-vision-contribute` was absent when checking “You and your agents” at line 119 (log lines 1960–1979).
4. `tests/e2e/public-astrid-vision-mobile-catalogs.spec.ts:103:1`, “legacy section bookmarks open the right dialog and leave no dead hash on dismissal”: dialog “All gaps” was absent after navigating to `#astrid-vision-parts`, assertion line 106 (log lines 1999–2020).
5. The same file, line 422, “two-column mobile pillars animate in reading order as scroll advances and reverses”: expected `data-play="true"` on the first principle card, but the resolved element had no `data-play`; assertion line 436 (log lines 2041–2066).

### `vision-content`, WebKit

One assertion failed; 62 passed. The final test is the same `two-column mobile pillars animate in reading order as scroll advances and reverses`: the first principle card did not acquire `data-play="true"` after scrolling to the top (log lines 2186–2212). The job invoked the WebKit config at step 14 (log line 2120); the hosted browser installation step had already succeeded. Summary and exit are at lines 2239–2244.

## Classification

These are observed Playwright assertion failures, not runner or browser-install failures. The PR run’s browser install steps succeeded and other tests passed. All five Chromium cases also passed in the starting-SHA local baseline. More decisively, the manager-triggered run of the same unmodified workflow at base SHA e3 has now completed the full Chromium step successfully; this is a matched hosted comparison, unlike the local Chrome/worker/feed setup. The five failures therefore appear only on the PR cumulative diff versus the hosted base run and are candidate regressions, though the exact cause of the four missing-content/navigation results remains unisolated. The likely mobile geometry cause for `data-play` is documented below.

The Home page-transition assertion is also a candidate regression in the PR cumulative diff: the matched base workflow’s `home-apple-webkit` job completed all five cases successfully, including this test. The base Linux WebKit step has now also passed all 63 cases, including the `data-play` case. The current evidence supports a likely phone layout cause for `data-play`; it does not isolate the Home transition failure’s cause.

All non-browser named CI steps passed. The separate baseline App typecheck failure (eight diagnostics, none in planet files) is not implicated by this run: no typecheck step failed in `jobs.json`. This diagnosis does not attribute all failures to the final one-line deterministic-capture default; PR #371 contains the complete cumulative changes above and the run has no per-change isolation.

## Evidence file references

- Run and job summaries: `run.json`, `jobs.json`
- Full failed-job output: `job-137349723145.log` (especially lines 241–283), `job-137349723395.log` (lines 1838–2069 and 2112–2244)
- Starting-SHA baseline classification: `../baseline/REPORT.md`, `../baseline/browser/chromium-attempt-02.json`
- PR identity and cumulative changed-file list: `pulls.json`, `pr-files.json`
- Base ancestry comparison: `base-vs-baseline.json`

## Follow-up causal audit (read-only)

### `data-play` geometry: likely code regression

The exact PR-head diff swaps the old `Juggler` for `<PublicAstridPlanet live={visible && !reducedMotion} />` in the hero (`src/pages/Home/PublicAstridVision.tsx:531`) and replaces the phone CSS that hid `.astrid-vision-juggler` with a `--px`/margin rule for `.astrid-vision-planet` (`src/pages/Home/PublicAstridVision.css:414–422`). The new planet wrapper still has both `astrid-vision-juggler` and `astrid-vision-planet` classes (`src/pages/Home/planet/PublicAstridPlanet.tsx:42–44`), and the shared juggler base rule gives it a 65×100 pixel-art box (`PublicAstridVision.css:67–72`). At a 390px width the phone rule resolves `--px` to about 2.9px, so the now-visible in-flow hero slot is about 300px tall; the old phone rule removed that slot from layout.

The failing test sets a 390×844 viewport, scrolls to `scrollY=0`, and asserts the first pillar has `data-play="true"` because the first row should already be visible (`tests/e2e/public-astrid-vision-mobile-catalogs.spec.ts:427–436`). The `centred` selector only sets an index when the measured row intersects the viewport; it clears the selection when `row.top >= viewportHeight` (`PublicAstridVision.tsx:384–423`), and the card attribute is derived from `centred`/`playing` (`PublicAstridVision.tsx:571–576`). CI’s screenshot evidence gives a concrete matching geometry: `real-arrival-pillars-chromium-desktop.png` is 390×927 and shows the first pillar cards only at the bottom edge; its companion JSON records the test’s computed height as 927. This supports the extra in-flow hero height as the likely cause of the repeated Chromium and WebKit `data-play` assertion, rather than a WebGL startup delay.

A low-risk repair seam to evaluate later is the PR’s phone hero placement: keep the planet canvas and its render layer out of normal flow on phones, preserving the old hero-to-pillars geometry; leave camera framing to the planned PL-3 camera work. Do not loosen the assertion to accept an offscreen card.

### Four Chromium content/navigation and Home transition failures: cause not isolated

The other four Chromium failures are not explained by the phone-only height change: one test reports `main.astrid-vision` absent at the five-second assertion, two report content-backed regions absent, and one reports a hash catalog dialog absent. Two tests use explicit desktop viewports (1440px); one pins the live feed before navigation. The logs and uploaded report do not retain their Playwright traces, only trace attachment paths, so there is no browser console/network/DOM snapshot evidence here to identify why those pages did not reach their expected state. Keep these as new hosted failures versus the local baseline, but root cause remains unisolated.

The CI job executed the same 14-spec Chromium inventory against `playwright.config.ts`, but without the local `--workers=1` cap. The retained CI reporter JSON says `fullyParallel: true` and `workers: 2`; local baseline command explicitly used one worker. CI installed Playwright Chromium 148.0.7778.96 (v1223), while the local baseline used external Chrome 153.0.8010.12 through the SwiftShader wrapper. Both configs use the Vite dev server, but browser version/GL mode and worker count differ. The PR job also used the live `raw.githubusercontent.com/.../vision.json` feed; uploaded captures show revisions `5d4abe2c6ee672b8fbcbc23ff61be4bf40e039c1` in Chromium and `b21b792b2bb6f4c8cbf8fc726c917493e7db7370` in WebKit, so its browser runs did not use one immutable content revision. These differences block a causal claim from the passing local result alone.

### Existing base-CI history and related issue check

Before the manager dispatch, the REST query for workflow `409739180` at the PR base SHA `e3dbad64d402724ac5a35fb6447f18e432c64b78` returned zero runs (`base-vision-runs.json`); the same workflow query for `release/15/main` returned zero (`release-main-vision-runs.json`). The base SHA’s three then-existing workflow runs (`base-runs.json`) were other workflows. The manager later ran this exact workflow on the base; its complete successful result is recorded below.

Astrid Dev issues #1289 and #1291 (`astrid-dev-issue-1289.json`, `astrid-dev-issue-1291.json`) describe unrelated `astrid-agent` release/model-lock and Python test failures; neither mentions these Astrid App Playwright test names. They are not evidence that these failures were inherited.

### PL-5 startup/quality scope

The likely `data-play` cause is layout: the reveal/center loop is correctly refusing to animate a row outside the viewport. PL-5 runtime quality step-down operates inside the planet renderer after mount and does not repair the phone document flow; no PL-5-specific code path appears in these browser assertion diagnostics. The planet is dynamically imported from a `useEffect` after the route component renders (`PublicAstridPlanet.tsx:16–28`), so the code shape also does not explain a missing `<main>` by itself. Startup time remains an unmeasured possibility for the four five-second timeouts under CI’s different worker/browser configuration, not a finding.

A related current PL-2 local verification failure, outside CI run 45068430986, is recorded in `run/evidence/pl-2-verification/run.log`: the cold-entry/reload/viewport test cannot find `#astrid-vision-title` by line 348, while the iPad route-return case keeps root `overflowY` at `clip` by line 225. In source, that title ID is deliberately omitted until feed content resolves (`PublicAstridVision.tsx:517–520`), so this cold-entry assertion is evidence of delayed content readiness, not a wrapping failure. The planet chunk is imported in `useEffect` and then its large initializer is called synchronously (`PublicAstridPlanet.tsx:16–28`; `planetEngine.ts:42–50`). That makes engine startup a plausible main-thread contention seam for cold content/render callbacks, but the existing run has no profile/trace to confirm it. The iPad overflow failure is a separate page-lifecycle symptom; the phone spacer does not explain it. PL-5 quality downshift is not yet implicated by proof: it could matter if initial engine startup is separately measured as a bottleneck, but it cannot fix the confirmed phone flow geometry on its own.

### Additional retained evidence

- Existing base history: `base-runs.json`, `base-check-runs.json`, `base-vision-runs.json`, `release-main-vision-runs.json`
- Issue lookups: `astrid-dev-issue-1289.json`, `astrid-dev-issue-1291.json`
- Hosted reporter bundle: `vision-artifact-14773666438.zip`; extracted screenshot: `real-arrival-pillars-chromium-desktop.png`

## Existing base-WebKit dispatch path (not dispatched)

The registered `.github/workflows/public-vision.yml` on default branch `main` (`workflow.json`, `repository.json`) and the exact base workflow both declare `workflow_dispatch` with no inputs. The live branch endpoint reports `release/15/main` currently at `e3dbad64d402724ac5a35fb6447f18e432c64b78` (`release-main-branch.json`); this is the requested immutable app/test source for a dispatch now. The PR’s historical base ref was `release/15/plan-84`, which has since advanced to `95a061b3ba24a0bdec598da449f04ee82c6acf5c` (`base-branch.json`), so dispatch against that ref would no longer test e3.

An unmodified `workflow_dispatch` on ref `release/15/main` will include both relevant WebKit cases: the Ubuntu `vision-content` job runs `playwright.vision.config.ts` across its five configured spec files, including `public-astrid-vision-mobile-catalogs.spec.ts` (`playwright.vision.config.ts:12`, workflow step at line 102); the macOS 15 `home-apple-webkit` job runs `playwright.home-webkit.config.ts`, whose test match is `public-astrid-home-chips.spec.ts` (`playwright.home-webkit.config.ts:7`, workflow step at line 128). Those configs run the full files (and other configured WebKit specs), not only the two failing cases. The same dispatch also runs the named unit/lint/build steps and all 14 Chromium specs. There is no input to narrow the run.

At the time of the workflow-option audit no branch, workflow edit, CI dispatch, or run had been created. The later manager-triggered dispatch is recorded separately below; the retained branch response records `release/15/main` at e3.

Current `main` workflow content is retained as `default-main-public-vision.yml`; workflow and repository metadata are `workflow.json` and `repository.json`.

## Manager-triggered base workflow dispatch (2026-11-22)

This is distinct from the earlier read-only audit above, which issued no dispatch. The manager manually dispatched the existing unmodified workflow; the REST dispatch endpoint returned HTTP 204 (empty response body retained in `baseline-dispatch-response.txt`). GitHub assigned run [45075542144](https://github.com/banodoco/astrid-app/actions/runs/45075542144) to `release/15/main` at exact base SHA `e3dbad64d402724ac5a35fb6447f18e432c64b78`, event `workflow_dispatch`, attempt 1, created `2026-11-22T22:03:41Z`. At initial observation it was `in_progress`: jobs `home-apple-webkit` (`137371835333`) and `vision-content` (`137371835666`) had started. Initial run/job REST snapshots are `baseline-dispatch-run.json`, `baseline-dispatch-jobs-01.json`, and `baseline-dispatch-runs-01.json`. No dispatch, rerun, or cancellation was performed by this audit.

### Base-dispatch interim result (2026-11-22, browser steps)

At this intermediate observation, the base `home-apple-webkit` gate had completed success (step 6, 2026-11-22 22:05:12–22:08:00Z), and the `vision-content` Chromium gate had completed success (step 13, 22:06:38–22:12:03Z). This made the Home transition assertion and five Chromium assertions candidate failures relative to the hosted base, though the PR cumulative diff cause was not yet isolated. The `vision-content` WebKit gate (step 14) was still in progress, so its comparison was pending. Job status snapshots through that observation are `base-dispatch-jobs-01.json` … `base-dispatch-jobs-08.json`; the final logs/results are recorded below.


### Final matched hosted-base result (2026-11-22)

Run `45075542144` completed successfully on `release/15/main` at exact SHA `e3dbad64d402724ac5a35fb6447f18e432c64b78`, event `workflow_dispatch`, at `2026-11-22T22:23:22Z`. Both jobs succeeded. The Apple WebKit Home job reports 5 passed (2.8m); the specific `player projection stays steady on scrolled app return` is listed at `base-job-137371835333.log:328`, and the summary is at line 332. The `vision-content` job reports 122 Chromium tests passed at `base-job-137371835666.log:1895`; the mobile pillars test is listed at line 1858. Its WebKit step reports 63 tests passed at line 1982; the same mobile pillars test is listed at line 1962. No rerun or cancellation occurred.

This hosted comparison changes the classification: all five Chromium failures, the matching WebKit `data-play` failure, and the Apple Home transition assertion in PR run `45068430986` passed on the starting SHA under the same workflow. They are new failures relative to the hosted base and therefore candidate regressions in PR #371’s cumulative diff, not known inherited failures or browser-launch infrastructure failures. The geometry evidence remains the strongest specific cause for `data-play`; the four content/navigation timeouts and persistent Home transition attribute remain unexplained at code-path level.

Final raw evidence: `base-dispatch-run-final.json`, `base-dispatch-jobs-final.json`, `base-job-137371835333.log`, `base-job-137371835666.log`, and `base-dispatch-artifacts.json`.
