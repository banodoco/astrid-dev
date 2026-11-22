# PL-1 entry-repair independent verification

Candidate: `a4447fc39905a307118dc41519078717850fbad3` in `worktrees/pl-1-entry-verify` (requested frozen candidate; verification worktree source remained clean). Browser captures used Google Chrome for Testing `153.0.8010.12` through `run/evidence/baseline/production/chrome-swiftshader` (SwiftShader).

## Focused checks

- Vitest: original `PublicAstridPlanet.test.tsx` plus new `PublicAstridPlanet.entry.test.tsx`: **6/6 passed**. Original component test SHA-256 is `df700755ebe16694d656fbf348455e615151f5d63dfec29a641d48de204c68cb`, identical to `git show 95a061b:src/pages/Home/planet/PublicAstridPlanet.test.tsx`.
- Scoped ESLint over `PublicAstridVision.tsx`, `publicAstridNavigation.ts`, `PublicAstridPlanet.tsx`, and both component test files: **exit 0**, no output.
- Playwright `public-astrid-vision-entry.spec.ts`: unchanged cases at lines 208 and 338, `--project=chromium-desktop --workers=1 --no-deps`: **2/2 passed**.
- App TypeScript check: `tsc -p tsconfig.app.json --noEmit` exited 2 with 8 diagnostics. `tsc-baseline.diff` is empty; current log exactly matches `run/evidence/baseline/checks/app-tsc.log`, SHA-256 `a5957cc6bb01b5ca926e9d3a907e5461590f583171e12f65d9eba7876abac399`. No new diagnostics.

Raw commands, logs, exit statuses and Playwright JSON are in this directory: `vitest.*`, `eslint.*`, `entry.*`, and `tsc.*`.

## Poster to first rendered canvas

The focused handoff capture held the engine module request after feed content and title were ready, recorded the poster with the live canvas mounted behind it, then released the module and captured after the poster was removed by `onReady`. In `planetEngine.ts`, `onReady` fires after the first `renderer.render` call. Both pairs show the poster before and the drawn planet after, with no captured console/page errors.

- Laptop 1440x900, DPR 1: poster before (`laptop-handoff-poster-before.png`, not saved in this snapshot), live canvas after (`laptop-handoff-live-after.png`, not saved in this snapshot), metrics (`laptop-handoff.json`, not saved in this snapshot).
- Phone 390x844, DPR 3: poster before (`phone-handoff-poster-before.png`, not saved in this snapshot), live canvas after (`phone-handoff-live-after.png`, not saved in this snapshot), metrics (`phone-handoff.json`, not saved in this snapshot).

Chrome's `PerformanceObserver` reported **0 stage-attributed layout-shift score** and 0 layout-shift entries in both render-only windows. Stage rect deltas were laptop x=0, y=-2.545 px, width=0, height=+0.00003 px; phone x=0, y=-14 px, width=0, height=0. So the observed CLS score is zero, while the stage's measured top coordinate changed during the capture interval; the report does not claim exact geometric immobility. The broader loading-to-live captures (`laptop-capture.json`, `phone-capture.json`) also span the feed-loading update and are retained only as context, not used for the render-only CLS claim.

Capture commands and scripts are `capture.cjs`, `handoff-capture.cjs`, `capture-vite.log`, and `handoff-vite.log`; raw summary output is `capture.log` and `handoff.log`. Capture JSON and PNG files are retained alongside this report. No product or test files were edited in the verifier worktree.
