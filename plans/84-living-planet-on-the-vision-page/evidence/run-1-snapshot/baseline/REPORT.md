# Plan 84 production and test baseline

Candidate source SHA: `e3dbad64d402724ac5a35fb6447f18e432c64b78` (`plan-84/baseline`), in `/home/user/codex/planet84/worktrees/baseline`. The worktree contains no product edits. Baseline evidence and raw command output live under this directory.

## Environment and inventory

- Installed locked dependencies with `npm ci --legacy-peer-deps --no-audit --no-fund` (exit 0; `npm-ci.log`). Node option for the hosted build was `--max-old-space-size=4096`.
- App-native smoke: `npx vitest run --config config/testing/vitest.config.ts src/pages/Home/publicAstridSkySession.test.ts` (6 passed, exit 0; `smoke-vitest.log`, `smoke-vitest.exit`). The shared `env/smoke.sh` has no App mode.
- Chromium workflow inventory: exact `playwright.config.ts` and 14 `vision-content` workflow specs, with `--project=chromium-desktop --workers=1`. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` pointed to the evidence wrapper `production/chrome-swiftshader`, which calls the preinstalled `/usr/bin/google-chrome` 153.0.8010.12 with `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`. The base config's DNS-blackhole arguments remained enabled. No browser installation was run. The full run completed: 122 passed, 0 skipped, 0 flaky, 0 unexpected, exit 0, 12.3 minutes. The total includes the config's extension-harness setup dependency. Raw command/log/exit and JSON are `browser/chromium-attempt-02.*`; output and screenshots are under `browser/output-attempt-02/` and the worktree's `test-results/`.
- Earlier `browser/playwright.log` is an interrupted run, not a result: it stops at 46/122, has no completed reporter JSON, and its exit 1 is not a test verdict. It remains unchanged.
- WebKit workflow inventory was invoked with `playwright.vision.config.ts` (63 collected tests, one worker). It could not start because `/tmp/codex-xdg-cache/ms-playwright/webkit-2287/pw_run.sh` is absent (63 launch errors, exit 1). No WebKit executable was present in `/opt/pw-browsers`; no browser was installed. The raw launch failure is kept separately in `browser/webkit-attempt-01.*` and is excluded from functional test classification.

## Checks and focused unit results

The completed named Vitest suites, lint, syntax check, and production build were carried forward from the durable pre-restart records; they were not rerun.

| Check | Result | Evidence |
|---|---|---|
| `npm run vision:check` | 13 tests passed, exit 0 | `unit/vision-check.*` |
| Live-feed hierarchy/loading | 15 tests passed, exit 0 | `unit/live-feed.*` |
| Lifecycle/share/scheduling | 47 tests passed, exit 0 | `unit/lifecycle-share.*` |
| Pixel emphasis/tour | 56 tests passed, exit 0 | `unit/pixel-tour.*` |
| Sky rendering/scheduling | 54 tests passed, exit 0 | `unit/sky.*` |
| Vision ESLint command | exit 0 | `checks/vision-lint.*` |
| Canary syntax (`node --check scripts/quality/check-public-vision-production.mjs`) | exit 0 | `checks/canary-syntax.*` |
| `npm run build:hosted` | exit 0 | `checks/production-build.*` |
| `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit` | exit 2, eight existing diagnostics; none reference planet files | `checks/app-tsc.*` |

The test adapter emitted 14 named Vitest file-suite IDs from the retained default-reporter logs. It does not invent assertion IDs that those logs did not retain. The completed Chromium JSON adapter emitted 122 individual test IDs. Their combined self-diff was run through `astrid-dev/env/baseline-diff.py`: 136 baseline and candidate IDs, with zero regression, no-baseline, preexisting, fixed, or missing buckets. This is a parser and inventory self-check on the same starting-SHA evidence; it is not a comparison against a later candidate. Converted inputs and diff output are `unit/vitest-file-suites.log`, `browser/chromium-pytest-lines.log`, and `diff/`; exact diff command, stdout and exit are `diff.command`, `diff.log`, and `diff.exit`.

## Production paint and transfer baseline

Measured the built `dist/` served with Vite preview at `http://127.0.0.1:4175/vision`, using one cold Chromium context, 1440×900 CSS px, DPR 1, UTC, and the same SwiftShader flags. The page clock was fixed to `2026-06-21T12:00:00Z`, pinning the sky hour. The route was fulfilled from `production/vision-feed.json`: SHA256 `c233da0fcf0136204d0198c58186757dd5a7f4b29d2137cfd1df1a5f36e63625`, 178,949 bytes, feed source revision `b2d0c444b35fbb08bcf61b177e0e302b652e6f24`.

- First Contentful Paint: 224 ms
- Largest Contentful Paint: 224 ms (the measurement script did not retain the LCP element name, so element attribution is unknown)
- Cumulative Layout Shift: 0
- Browser-reported local resource `transferSize` sum: 525,876 bytes. The pinned 178,949-byte feed was fulfilled from a local file and reported `transferSize: 0`; this sum excludes the feed and is not a full cold-wire transfer total.
- Browser: Chrome 153.0.8010.12; measurement date and viewport recorded in `production/metrics.json`

The screenshot is `production/production-baseline.png`; the raw measurement command, stdout, and exit are `production/metrics.command`, `production/metrics-run.log`, and `production/metrics.exit` (exit 0). At the 1.5-second full-page screenshot, the navigation and hero headline are visible, the hero's juggler is absent, below-hero sections appear blank, and the small footer juggler is visible near the bottom. The screenshot is a load-state snapshot, not proof that all below-fold content reached its settled visual state. It is a DPR-1 measurement capture, not one of the DPR-2 manager comparison pictures. The initial 224 ms LCP must not be read as full-page content readiness.

## Classification

Chromium and the focused unit suites passed at the starting SHA. The App typecheck is a pre-existing baseline failure (eight diagnostics, no planet references). The WebKit result is an infrastructure launch failure, not a product-test pass or failure. No candidate-vs-baseline regression claim can be made until a later candidate has its own named inventory and is compared with these retained baseline inputs. This report does not mark route N task-ready while the WebKit functional gate remains unexecuted.
