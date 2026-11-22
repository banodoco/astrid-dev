# PR372 entry repair CI audit

Date: 2026-11-22 (UTC)

## Result

PR #372 (`a4447fc39905a307118dc41519078717850fbad3`, “Let Vision settle before starting the planet”) has a failed Public vision workflow run [45077162147](https://github.com/banodoco/astrid-app/actions/runs/45077162147). Its `vision-content` job failed at the named “Preserve public page lifecycle and share metadata” step. The independent Dockerfile checks run [45077162171](https://github.com/banodoco/astrid-app/actions/runs/45077162171) passed. `home-apple-webkit` passed all five tests, including the scrolled app-return projection case.

The lifecycle step ran three files: `PublicAstridSite.lifecycle.test.tsx`, `viteShareMeta.test.ts`, and `PublicAstridCallouts.scheduling.test.tsx`. The latter two passed; the lifecycle file had 2 failures out of 17. Overall this step reports 45 passed / 2 failed of 47 (`job-137376850290.log:350-355`). Build and browser inventory steps were skipped after the failure, so this run provides no PR372 browser-inventory result.

## Exact failures

From `job-137376850290.log`:

1. `retains Home state and scroll across repeated round trips, with no hidden callout frames`: `frames.size` was 2, expected 1 (`:311-323`; assertion source line 205).
2. `moves focus to Vision and cancels the Home sky replay`: `frames.size` was 1, expected 0 (`:330-343`; assertion source line 354).

These same 17 lifecycle tests and the same 25 callout tests passed on PR1 run 450684 (`../pl-1-ci/job-137349723395.log:297-302`) and on the matched green release-base run 450755 (`../pl-1-ci/base-job-137371835666.log:257-266`). Thus the two frame-count failures are new in the observed PR372 run, not inherited from the matched green run.

The strongest code-level lead is the new entry gate: `PublicAstridPlanet` now waits for navigation transitions and two animation frames before lazy engine import, then repeats the wait after import (`pr-files.json`, `src/pages/Home/planet/PublicAstridPlanet.tsx` patch); the new test file also explicitly exercises animation-frame cancellation (`pr-files.json`, `PublicAstridPlanet.entry.test.tsx`). The failing lifecycle tests count global RAF callbacks as part of Home/sky ownership. This ties the new failures to startup/frame scheduling, but available CI output alone does not prove which callback is responsible or whether production behavior is incorrect. The new entry test file was not listed in the workflow's failing step command, so this CI run did not execute that test file.

### Harness/source distinction

The matched lifecycle test deletes `document.startViewTransition` (`worktrees/baseline/src/pages/Home/PublicAstridSite.lifecycle.test.tsx:122`) and replaces the global `window.requestAnimationFrame` with a `Map` (`:139-141`); `paint()` drains the whole map (`:83-87`). In the round-trip test, the immediate zero-frame assertion at `:197` passes. After advancing timers, line `:205` expects one frame for Vision's resize measurement but sees two. The PR372 gate's first pre-import frame is scheduled before `loadEngine()` and therefore before `initPlanetEngine()` can attempt WebGL creation; it is not a failed-WebGL callback or a renderer loop. The gate then schedules its second RAF sequentially after the first resolves. The second test drains two frames (`:351-352`), but the pending asynchronous gate may schedule its next RAF after a drain, leaving one callback at `:354`. This is a bounded startup RAF now sharing the same test counter as the geometry and Home ownership assertions. The source-supported remedy is a real native capability gate before this startup work: skip the default loader when WebGL2 is unavailable, preserving the poster. The existing lifecycle assertions remain intact; this diagnosis does not require modifying tests.

### Native renderer capability check

The repository pins Three `0.185.1` (`worktrees/pl-2/package.json:169`). Its `WebGLRenderer` source states it uses WebGL 2 and WebGL 1 is unsupported since r163 (`worktrees/pl-2/node_modules/three/src/renderers/WebGLRenderer.js:58-62`); it requests a `webgl2` context (`:393`). The planet engine also probes `getContext('webgl2')` before constructing the renderer (`:6717-6733`) and returns `null` if renderer construction fails (`:6734-6736`). Therefore a native environment without WebGL2 cannot display the live planet and should retain the still poster without the lazy import or pre-import paint gate. This supports a production capability guard before entry work; preserve custom loader injection as a test seam without changing existing lifecycle tests. Checking `WebGL2RenderingContext` presence is a reasonable browser precondition; probing an isolated canvas with `getContext('webgl2')` is the direct test, with the cost that a successful probe creates a context. The source audit did not find an expected supported native browser where the WebGL2 context works while the `WebGL2RenderingContext` interface is absent.

## Phone geometry remains separate

PR372's changed-file list (`pr-files.json`) contains no `PublicAstridVision.css` change. The original phone rule remains in the release baseline at `worktrees/baseline/src/pages/Home/PublicAstridVision.css:416`: `.astrid-vision-juggler { display: none; }`. The current candidate CSS still replaces that rule with an in-flow planet at `worktrees/pl-2/src/pages/Home/PublicAstridVision.css:423` (`.astrid-vision-planet … margin-top: 8px`) and defines the planet spacer at `:2276-2292`. Therefore PR372 does not contain the PL2 phone-geometry repair; it cannot explain or clear the prior mobile-catalogs `data-play` failure at assertion line 436. This is distinct from the two newly observed RAF lifecycle failures above.

PR1's failed Public vision inventory recorded 5 Chromium failures and 1 WebKit failure, including `tests/e2e/public-astrid-vision-mobile-catalogs.spec.ts:436` expecting the first catalog card to have `data-play="true"` (`../pl-1-ci/job-137349723395.log:2059`, `2112`, and `2204-2241`). PR372's Apple WebKit Home job instead passed 5/5 (`job-137376850785.log:292-296`), but that job is the Home chips suite, not the Vision content inventory.

## Raw evidence

This directory contains the retrieved run/job metadata, PR file patch, and complete raw logs:

- `public-vision-run.json`, `public-vision-jobs.json`
- `job-137376850290.log` (failed `vision-content`)
- `job-137376850785.log` (passed Apple WebKit Home suite)
- `docker-run.json`, `docker-jobs.json`, `job-137376851390.log` (passed Dockerfile checks)
- `commit.json`, `pulls.json`, `pr-files.json`

No workflow was dispatched or rerun for this audit; no product files or tests were changed.
