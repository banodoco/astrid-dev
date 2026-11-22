# PL-2 independent focused test result

- Candidate: `88ac863600492401bc22e352999660f3d5b01020` (`plan-84/pl-2-verify`); verified HEAD remained this SHA and the product worktree stayed clean.
- Exact test selection: the four requested Chromium desktop specs only. Playwright's required `extension-harness-setup` project dependency also ran automatically, so the run collected 64 tests total (63 in the requested specs plus one setup test).
- Result: **FAIL**, inner Playwright exit `1`: **50 passed, 14 failed**, no retries. The baseline attempt 02 recorded **122/122 passed** overall. These four requested files accounted for **63/63 passed** at baseline. Every candidate failure below is therefore new relative to the recorded baseline. This is a local run; it does not establish CI behavior or a failure cause.
- Browser environment: the configured Chromium executable `run/evidence/baseline/production/chrome-swiftshader`, one worker, Playwright's test dev server on dedicated port `43284`, and the config's separately allocated fake Runtime port. The owned servers stopped when the run ended.

## Exact command

Environment assignments and command are preserved verbatim in `command.txt`. The invoked command was:

```sh
PLAYWRIGHT_PORT=43284 ASTRID_APP_TIMELINE_PORTS_ALLOCATED=0 FAKE_RUNTIME_PORT= BASE_URL= PLAYWRIGHT_BASE_URL= PLAYWRIGHT_OUTPUT_DIR=/home/user/codex/planet84/run/evidence/pl-2-verification/output PLAYWRIGHT_CHROMIUM_EXECUTABLE=/home/user/codex/planet84/run/evidence/baseline/production/chrome-swiftshader PLAYWRIGHT_JSON_OUTPUT_FILE=/home/user/codex/planet84/run/evidence/pl-2-verification/results.json npx playwright test --config playwright.config.ts tests/e2e/public-astrid-vision-entry.spec.ts tests/e2e/public-astrid-vision-mobile-catalogs.spec.ts tests/e2e/public-astrid-vision-sigils-nav.spec.ts tests/e2e/public-astrid-vision-polish.spec.ts --project=chromium-desktop --workers=1 --output=/home/user/codex/planet84/run/evidence/pl-2-verification/output --reporter=line,json
```

## Failures against the green baseline

| Spec and test declaration | Exact failing assertion | Observed result |
| --- | --- | --- |
| `public-astrid-vision-entry.spec.ts:208` — iPad return from scrolled Vision | `:225`, expect root `overflowY` not to be `clip` | Remained `clip` after clicking Vision; 5 s predicate timeout. |
| `public-astrid-vision-entry.spec.ts:338` — headline flow on cold entry/reload/viewport changes | `:348`, expect `#astrid-vision-title` to match feed title | Title node absent within 5 s while iterating viewports. |
| `public-astrid-vision-entry.spec.ts:833` — condensed desktop brand | `:848`, expect `html` not to have `data-astrid-page-transition` | Attribute remained `"vision"` after clicking Vision. |
| `public-astrid-vision-mobile-catalogs.spec.ts:103` — legacy section bookmarks | `:106`, expect dialog `All gaps` visible | Dialog absent after navigation to `/vision#astrid-vision-parts`; 5 s timeout. |
| `public-astrid-vision-mobile-catalogs.spec.ts:422` — two-column mobile reading order | `:431`, expect four `.astrid-vision-principles > li` | Received 0. The test did not reach its later `data-play` assertion at `:436`. |
| `public-astrid-vision-polish.spec.ts:19` — viewport preparation before native dialog | `:45`, expect four `.astrid-vision-principles > li` | Received 0. |
| `public-astrid-vision-polish.spec.ts:181` — mobile sigil alignment | `:186`, expect four `.astrid-vision-principles > li` | Received 0. |
| `public-astrid-vision-polish.spec.ts:288` — room transition at 1440 px | `:330`, expect `html` not to have `data-astrid-page-transition` | Attribute remained present after clicking Vision. |
| `public-astrid-vision-sigils-nav.spec.ts:18` — distinct principle sigils | `:24`, expect four `.astrid-vision-standards-list > li` | Received 0. |
| `public-astrid-vision-sigils-nav.spec.ts:72` — technical wrangling animation | `:81`, expect the final standards card visible | Element absent. |
| `public-astrid-vision-sigils-nav.spec.ts:352` — softened sigil colors | `:361`, expect sigil opacity `0.58` | Sigil element absent. |
| `public-astrid-vision-sigils-nav.spec.ts:408` — principle tints and corner arrows | `:413`, expect four standards cards | Received 0. |
| `public-astrid-vision-sigils-nav.spec.ts:435` — phone scroll activation | `:441`, expect four standards cards | Received 0. |
| `public-astrid-vision-sigils-nav.spec.ts:543` — desktop section-link highlight | `:549`, expect Vision nav link `aria-current="location"` | Link element absent. |

The raw reporter output is `run.log`; Playwright JSON is `results.json`; `exit.txt` contains the inner exit code. Traces and error contexts for failures are in `output/`. No reruns, test edits, assertion changes, builds, or visual judgments were made.

## Candidate identity and evidence integrity

The worktree's CSS and page component hashes match the candidate checked at dispatch and remained unchanged during the run:

- `src/pages/Home/PublicAstridVision.tsx`: `3f22b4a2e61d583720362aa10e77c2f2d2439bced88dfd3afe64dc242e10d9b8`
- `src/pages/Home/PublicAstridVision.css`: `3d1a9a042a642c5ffdc45599ac8bbad8d1070acf1006e5781a839a9ee6997e72`
- `src/pages/Home/VisionMobileLayout.css`: `4e96b8eaa6c66c392d4a7791feb0f9a36c3085e8a115ed8d5e7e0f1ae4ed93e2`

SHA256: `command.txt` `cea881a4046a04ea343173cd570bf359cb8a50754ff351d8c73b9c63e97e1ed2`; `run.log` `2b5d3a7c3e4f1ce83037b09e49e658df21131ba4ae223f0f6938dff0e8a081b4`; `results.json` `99cfc09d024fe5fe34891a5830090b3257d4dd43175368defbcaa7855feaeba3`; `exit.txt` `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`.
