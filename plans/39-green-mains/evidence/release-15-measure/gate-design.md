# Plan 39 gate design: Runtime and App "cannot get worse"

Read-only research, 24 Nov 2026. Mirrors Plan 91 AG-1 (astrid-dev `plans/91-agent-main-green/tasks.md`, "How work is proved" lines 15-23, ceiling rule line 23, AG-1 line 64).

Heads read (all `origin/...` refs, not FETCH_HEAD, because FETCH_HEAD moved during the session):
- astrid-runtime `origin/release/15/main` = 24e2c92 (23 Nov). `origin/main` = 5120462.
- astrid-app `origin/release/15/main` = d53685f.
- astrid-dev `origin/main` = bd4c3e1.
- astrid-agent `origin/release/15/main` = 514499de (reference only).

Plan branch name used below: `release/15/plan-39` (the Runtime landing-reference rule requires `release/15/plan-<n>` as a PR head, Runtime `ci.yml:513-535`).

---

## 0. Corrections and new facts that change the brief's premises

1. **Runtime CI on pushes is narrower than "every push".** `ci.yml:7` pushes start CI only on `main`, `release/*/main`, `int/**`, `release/14/plan-39`. A push to `release/15/plan-39` starts nothing. But `ci.yml:8` `pull_request:` has no branch filter, so a PR into `release/15/plan-39` runs every job (no job-level `if:` except `landing-reference`, `ci.yml:513`). Each card PR therefore gets a full Runtime run for free.
2. **App plan-branch pushes and PRs start nothing.** `test.yml:5-8` push branches are `main, release-1, int/**, release/*/main`; PR bases are `main, release/*/main, release/14/plan-61`. `e2e.yml:6-9` and `lanes.yml:5-11` have no `pull_request` trigger. App cards need `workflow_dispatch`.
3. **baseline-diff has three defects that the gate must fix first (verified by probe).**
   - (a) IDs with a space after `::` are truncated. `_node_id` (`env/baseline-diff.py:26-43`) returns `rest[:space]` when no `[` precedes the space. Probe: baseline `PASSED src/a.test.ts::Shell layout renders` plus `FAILED ...::Shell layout renders - boom`, candidate `FAILED` on the same ID. Result: bucket `preexisting 1`, `regression 0`. A real regression is hidden. Every vitest `fullName` and Playwright title with a space is affected.
   - (b) The exit code blocks only on `regression` (`baseline-diff.py:120`). `no-baseline` and `missing` do not block.
   - (c) `missing` is `passed_somewhere - candidate` (`baseline-diff.py:75-76`). A test that failed on the baseline and disappeared from the candidate is not reported.
   - Also: `env/` has no test file for baseline-diff (`git ls-tree env/`).
4. **App already has an R14 ceiling system, on `release/14/plan-39` only.** `origin/release/14/plan-39` (e3497c3) has `scripts/ci/ceiling_{capture.py,adapters.py,vitest.ts,playwright.ts,pytest.py,hosted.py}`, `ci/failure-ceiling.json` and `.github/workflows/failure-ceiling.yml`. None of this is on `release/15/main`. Plan 91 says not to port the R14 K2/K3 comparator. This design does not port it either. The file name `ci/failure-ceiling.json` should not be reused.
5. **Two quarantine guards will go red on fixed dates (guard failures, not test failures).**
   - App: four `three-products` expected-failure entries expire 2026-11-25. Run on the `release/15/main` tree: `validateExceptions` returns `[]` at 2026-11-25 and four "expired on 2026-11-25" errors at 2026-11-26. `check-known-failures` (run today) exits 0. It goes red on 26 Nov.
   - Runtime: nine xfail entries (19 node IDs) expire 2026-12-01. `declared_xfail_errors` returns 0 errors at 2026-11-30 and 9 errors at 2026-12-01 (`tests/lanes.py:298`, `MAX_XFAIL_DAYS = 14` at `:245`).
6. **Runtime's windows, darwin and boundary jobs do not print `-rA` and do not upload JUnit.** See section 2.
7. **Neither repo has a ceiling file on `release/15/main`.** `ci/` does not exist in astrid-runtime or astrid-app `release/15/main`.

---

## 1. baseline-diff: input format, buckets, and a second format

**Input.** One regex, `env/baseline-diff.py:22`: `^(PASSED|FAILED|ERROR|XFAIL|XPASS) (.+)$`, applied to each line of a pytest `-rA` log. `parse()` (`:46-58`) maps FAILED/ERROR to fail and everything else to pass (XFAIL counts as pass, as the docstring says). A failure anywhere wins across repeated lines and logs. Multiple logs per side are comma-separated (`--candidate a.log,b.log`). `_node_id` (`:26-43`) strips ` - message` from summary lines and handles `[...]` parameter brackets. That is why pytest IDs work and nothing else does.

**Buckets** (`sort_results`, `:61-78`): `regression` (fails now, passed on some baseline), `no-baseline` (fails now, ran on no baseline), `preexisting` (fails now and on every baseline it ran on), `fixed` (passes now, fails on every baseline it ran on), `missing` (passed on a baseline, not run now). Exit 1 only for `regression` (`:120`).

**Second format.** None exists. The parser has one entry point (`parse`), so a second format is a dispatch on the first byte of the file. Two candidates:
- **JUnit XML.** Possible, but lossy. A `classname` is a dotted module path, so the file path has to be rebuilt, and parameter IDs are ambiguous. Pytest also writes xfail as `<skipped type="pytest.xfail">`, which must map to XFAIL or the xfail tests look "missing". Use JUnit only as a count cross-check (SF3a.1 in astrid-dev `plans/39-green-mains/tasks.md:57`), not as the comparator.
- **`--format ids`** (recommended). One line per test: `STATUS <id>`, where the id is the verbatim remainder of the line (no ` - ` split, spaces allowed). The App adapter (section 4) writes this. It fixes defect 3a and is a few lines in `parse`.

Also needed for the gate (card ENV-ADP): `--gate` (exit 1 on `regression`, `no-baseline` or `missing`), `missing` over all baseline states (not only PASS), and `--select <file-list>` so a partial `tests` run is compared only on the selected files. The default behaviour stays for current users (the R14 SF3b path).

---

## 2. Runtime: which CI jobs print `-rA` and upload JUnit

File: `astrid-runtime/.github/workflows/ci.yml` at `origin/release/15/main` (line numbers below).

| Job (lines) | Pytest command (line) | `-rA` | JUnit | Upload | Run 45259255785 |
|---|---|---|---|---|---|
| windows-realm-publication (22-95) | `-q -rP -m ""` (60); four more `-q` steps (63, 70, 76) | no (`-rP` at 60) | no | no | success |
| unit ubuntu, macos (96-203) | `-q -rA --junitxml=... -n 2` (165) | yes | yes | `test-results-unit-all-<os>`, `*.xml` only (189-196) | ubuntu 111F/367E, macos 110F/367E |
| darwin-native (205-247) | `-q -m darwin_native` (240) | no | no | no | success |
| typescript-client (249-260) | `npm test` (not pytest) | n/a | n/a | n/a | success |
| boundary (261-319) | `-q tests/test_second_client_e2e.py -m ""` (311) | no | no | no | success |
| sandbox-process-control (320-394) | `sh tests/seccomp/run-suite.sh -rA --junitxml=/test-results/...` (361) | yes | yes | `*.xml` only (386-394) | 125F/371E (whole suite in container) |
| portability-lifecycle ubuntu, macos (395-509) | `-q -rA --junitxml=... -m ""` + file list (451) | yes | yes | `*.xml` only (493-500) | 7F / 8F |
| landing-reference (511-535) | PR only | n/a | n/a | n/a | skipped |

Other: `nightly.yml:93` (`integration`, `-rA --junitxml -m integration`) uploads XML at 117-123, but its cron (`nightly.yml:4-5`) fires only from the default branch. On `release/15/main` it runs by dispatch only.

**Gap.** Every job uploads JUnit XML, but `-rA` text goes only to the job log, which is what the measurement pulled through the API. baseline-diff needs the text. Reporting change (card REP-R): `set -o pipefail; <pytest> 2>&1 | tee "$TEST_RESULTS_DIR/<job>.log"` and add `*.log` to each upload. Windows steps need `shell: bash` (pwsh is the default on windows-latest). The windows `-rP` at line 60 becomes `-rA`. Boundary, darwin and the windows steps also need `--junitxml` if the count check (SF3a.1) is wanted.

Measured sizes for the ceiling (from `runtime-green/REPORT.md`): distinct failing IDs 508 across five jobs; passing counts ubuntu 9,348, macos 9,245, sandbox 9,254, portability 610 / 595.

---

## 3. Dispatch inputs: `tests` and `repeat`

**Today.** `ci.yml:9-14` and `nightly.yml:8-13` have only `agent_sha`. `test.yml:9-16` has only `p61_real_run`. `e2e.yml:9` and `lanes.yml:11` have no inputs. Ref is set by the dispatch call itself (`gh workflow run --ref`), so no ref input is needed.

**Runtime: what adding them takes (about 1.5 days, card GATE-R).**
- `tests` (string, default empty): pass as an env var and expand unquoted in the pytest command, e.g. `python -m pytest -q -rA ... -n 2 $PYTEST_SELECTION`. Add a `job` choice input (`all`, `unit`, `sandbox`, `portability`, `darwin`, `windows`, `boundary`) and an `if:` on each job, so a `tests` run does not spend 40 minutes on every job.
- `repeat` (number, default 1): wrap the run in `for i in $(seq 1 "$REPEAT")`, writing `<job>.<i>.log` and continuing past failures. The gate then passes all logs as one candidate side. Because "a failure anywhere wins", "20/20 after" means no failing iteration. No pytest-repeat dependency is needed (`pyproject.toml:12-13` `test` extras do not include it).
- Pitfalls:
  - `pyproject.toml:22` deselects `integration`, `darwin_native` and `live` by default. A named integration test runs 0 tests and pytest exits 5. That fails loudly, which is correct, but the card must say so. Passing `-m ""` changes semantics and must be explicit.
  - `ci.yml:16-20` sets `cancel-in-progress` true for plan branches. Two dispatches on `release/15/plan-39` cancel each other. Dispatch one at a time per ref.
  - `ci.yml:38` (windows) and `ci.yml` darwin job hard-code Agent SHAs (`ff40f2c6`, `4866090e`). `agent_sha` does not reach them. Decide whether the input must.
  - Sandbox: `run-suite.sh` forwards its arguments to pytest (`tests/seccomp/run-suite.sh`), so `tests` works there, but the paths must exist in the read-only `/src` copy.

**App: what adding them takes (about 1 day each workflow, card GATE-A).** `e2e.yml` `workflow_dispatch` gets `tests` (spec paths) and `repeat`; each `npx playwright test` / `npm run test:e2e:*` step appends the selection. `test.yml` gets `tests` for the `vitest` job (`npm test` at line 236). `lanes.yml` gets `tests` for `checkout-lanes` (`npm run test:checkout` line 78, `test:astrid-composition` line 83). Local focused runs already exist: `env/app-test.sh` (Vitest only) and `env/README.md` for it.

---

## 4. App: test runners, reporters, and the adapter

### Vitest
- `config/testing/vitest.config.ts:66`: `reporters: ['default', new SkipGuardReporter()]`. No JSON or JUnit.
- `config/testing/vitest.boundary.config.ts:44` has the same list. `vitest.astrid-renderer.config.ts` (used by `test:astrid-composition`) has `['default', new SkipGuardReporter()]` too.
- No Vitest result file is written or uploaded on `release/15/main`. The vitest job (`test.yml:195-249`) runs `npm test` (line 236 = `test:app` + `test:node`, `package.json:31-32`) and `npm run test:sdk-boundary` (line 239). Its only upload is `test.yml:138` (P61 proof, not vitest).
- The 1,454-file, 21,474-test pass count is from the measurement (`app-green/REPORT.md`). The vitest job has been green on every push.

### Playwright
- `playwright.config.ts:110`, `playwright.extension-accessibility.config.ts:44`, `playwright.extension-cross-browser.config.ts:44`, `playwright.extension-visual.config.ts:42`: `reporter: [[CI ? 'github' : 'list'], ['./config/testing/playwrightSkipGuard.ts']]`. No JSON.
- The timeline and chrome-export jobs use `playwright.config.ts` with `--project` (`scripts/portable-developer-command.mjs:12-18`). So four configs cover six E2E jobs.
- Uploads (`e2e.yml`): traces and screenshots only, `path: test-results` (`:41-43`, `:69-71`, `:111-113`), `artifacts` for the three extension jobs (`:139-141`, `:167-169`, `:195-197`).
- Precedent: `direct-journey.yml:131-146` writes JSON with `PLAYWRIGHT_JSON_OUTPUT_NAME` and `--reporter=json,list,playwrightSkipGuard`, and `config/testing/direct-journey-outcome.jq` reads `.tests[].expectedStatus` and `.status`. Use the same JSON shape.

### Proposed reporter and upload change (card REP-A, about 2 days)
1. Each Playwright config: add `...(process.env.ASTRID_RESULTS_JSON ? [['json', { outputFile: process.env.ASTRID_RESULTS_JSON }]] : [])` to `reporter`. The env var keeps the npm scripts unchanged.
2. `vitest.config.ts`, `vitest.boundary.config.ts`, `vitest.astrid-renderer.config.ts`: add `['json', { outputFile: process.env.VITEST_JSON_OUTPUT }]` when the env var is set. Verify the `json` reporter option name against the installed Vitest (`package.json:200`, `^4.0.18`). This is inferred, not run.
3. Workflows: `ASTRID_RESULTS_JSON: ${{ runner.temp }}/results/<job>.json` on each Playwright step; `VITEST_JSON_OUTPUT` on the `npm test` step (`test.yml:236`), the sdk-boundary step (`:239`) and the lanes steps (`lanes.yml:78`, `:83`); `upload-artifact` with `if: always()` after each. Node's `node --test` steps are not in the gate (they have no ids in this scheme).

### Adapter (card ENV-ADP, in astrid-dev `env/`)
`env/app-results-ids.mjs`, Node stdlib only, writes `STATUS <id>` lines for `--format ids`.

- Vitest JSON: `testResults[].assertionResults[]`. ID = `<file relative to repo>::<ancestorTitles joined by " ">` + ` ` + `title`. `passed` → PASSED; `failed` → FAILED; `skipped`, `pending`, `todo` → no line (matches -rA, where skips are not listed). Duplicate IDs in one file: exit 2.
- Playwright JSON: walk `suites[]` recursively; a spec's tests are `specs[].tests[]` with `projectName`. ID = `<projectName> › <file> › <describe titles joined by " › "> › <spec title>`. Map `expectedStatus` `expected`/`status` `passed` → PASSED; `status` `expected` with `expectedStatus` `failed` (a `test.fail` that failed) → XFAIL; `unexpected` → FAILED; `flaky` → FAILED ("a later pass never erases an earlier red", the R14 rule). Duplicate IDs: exit 2.
- No line numbers in the ID. R14's `ceiling_playwright.ts` used line, column and `repeatEachIndex`, so any spec edit would change IDs.

Example IDs: `src/tools/video-editor/x.test.tsx::Timeline empty state renders the hint` and `chromium-desktop › tests/e2e/shell-layout.spec.ts › Shell layout › renders at 1280px`.

### Skips and expected failures (the quarantine guards)
- `config/testing/skipRegistry.mjs:25-83`: nine `SKIP_REGISTRY` entries with `skipWhen`, `reason`, `applies`, `ci`, `requireInLane`. **No owner, no expiry, no issue.** `check-skip-registry.mjs` ran: "9 declared skips, 10 lanes; 0 with no CI job", exit 0.
- `scripts/quality/check-known-failures.mjs` (ran on the `release/15/main` tree, exit 0 today): `MAX_QUARANTINE_ENTRIES = 10` (`:16`), `MAX_EXPIRY_DAYS = 14` (`:17`), `validateExceptions` (`:114`). Four authorized markers at `tests/e2e/local/three-products.spec.ts:1949, 2213, 2473, 3282`, one per entry. `AUTHORIZED_NAMES` (`:25-29`) lists three `useClipDrag` titles that have no marker in the tree (no `test.fail` in `useClipDrag.test.tsx`): a dead, unexpiring allowlist to delete.
- `config/testing/direct-journey-expected-failures.json` `"three-products"`: P39-R12-DUP-SHOT (#249), P39-R12-EXT-BATCH (#250), P39-R12-TASK-SWAP (#251), P39-R12-VIDEO-DROP (#252). Owner "Plan 39 manager" (a role). Expiry 2026-11-25 for all four (see section 0.5). `"direct": []`. The guard counts these toward the limit of 10 (plan-39 `tasks.md:51`).

---

## 5. Ceiling location, batch comparison, and triggers

**Location.** astrid-runtime `ci/runtime-ceiling.tsv` and astrid-app `ci/app-ceiling.tsv` (following Plan 91's `ci/agent-ceiling.tsv`). Manager-only edits, as Plan 91 line 23 requires.

**Content.** Plan 91 defines the ceiling as the failing IDs, ratcheted down. Recommended schema, one row per ID: `job<TAB>id<TAB>owner_row<TAB>issue<TAB>sealed_at`. Plus a second file, `ci/<repo>-inventory.tsv`, with every collected ID per job at seal time, so that deleting a passing test is caught. Without it, `missing` covers only ceiling IDs. Open question 1.

**Gate arithmetic per (job).** Build two `ids`-format logs from the files and run baseline-diff with `--gate`:
- `ceiling`: each row as `FAILED <id>` (so an ID that is still red is `preexisting`, and an absent ID is `missing`);
- `inventory`: each row as `PASSED <id>` (so a passing ID that now fails is `regression`).
- Result: a new red outside both files is `no-baseline`, which blocks. An ID absent from both is `missing`, which blocks. `--select` narrows both files for a `tests` run.

**Per job keys.** Runtime: `unit-ubuntu`, `unit-macos`, `sandbox-process-control`, `portability-ubuntu`, `portability-macos`, `darwin-native`, `windows-realm-publication`, `boundary`. `typescript-client` is job-level only (pass/fail). App: `vitest` (test.yml), `boundary`, `checkout-lanes`, `playwright-default`, `playwright-timeline`, `playwright-timeline-chrome-export`, `extension-accessibility`, `extension-visual`, `extension-cross-browser`. `quick-journey` and the installer jobs are job-level only.

**Which pushes and dispatches produce a batch result.**

| Repo | Trigger for a plan branch `release/15/plan-39` | Trigger for `release/15/main` |
|---|---|---|
| Runtime | `workflow_dispatch` of `ci.yml` only. PRs into the plan branch run all jobs (`ci.yml:8`), but a gate on PRs is advisory | push runs `ci.yml` (`:7`); gate job runs here too |
| App | dispatch of `test.yml`, `e2e.yml`, `lanes.yml`. No PR trigger for e2e or lanes; `test.yml:8` excludes the plan branch | push runs `test.yml`, `e2e.yml`, `lanes.yml` (`:5-8`, `:7-8`, `:6-7`) |

The manager dispatches once per workflow per batch, one at a time per ref (cancel-in-progress is true on plan branches, `ci.yml:16-20`, `e2e.yml:11-13`). The ratchet is committed only after a green batch on hosted CI, as Plan 91 says.

**Open ceiling problem for owner.** Plan 39's K1a/K1b/K1c guard is only the quarantine count; this gate needs the ceiling and the inventory to be sealed from one hosted run per repo on the plan branch head, not from a local run.

---

## 6. Cards

Route key: N ordinary, X coupled reasoning, S deepest correctness. Sizes are estimates in engineering days, not measured.

### ENV-ADP: baseline-diff ids format, gate mode, Vitest and Playwright adapter (astrid-dev `env/`)
- **Repo:** astrid-dev. **Cluster:** none (tooling). **Kind:** n/a (infrastructure; no test is triaged).
- **Fix:** (1) `parse` accepts `--format ids` (verbatim remainder); (2) `--gate` exit covers regression, no-baseline and missing; (3) `missing` = every baseline ID not run; (4) `--select`; (5) `env/app-results-ids.mjs` for Vitest JSON and Playwright JSON per section 4; (6) a new `env/test_baseline_diff.py` (stdlib unittest).
- **Scope:** `env/baseline-diff.py` (`_node_id`, `parse`, `sort_results` lines 61-76, `main` 120); `env/app-results-ids.mjs` (new); `env/test_baseline_diff.py` (new); `env/README.md` (format section).
- **Focused proof:** `python3 -I env/test_baseline_diff.py` and `node env/app-results-ids.test.mjs` (new). **Injected-failure review, required cases:** (a) the space-in-ID probe in section 0.3(a) gives `regression 1` after the fix (it gives `preexisting 1` now, so the test fails before the fix); (b) a candidate failure absent from both baselines exits 1 with `--gate`; (c) an ID absent from the candidate exits 1 with `--gate`; (d) a passing inventory ID that fails exits 1 (regression); (e) `--select` on one file ignores missing IDs in other files; (f) duplicate IDs in a Vitest file exit 2; (g) `test.fail` expected-failed maps to XFAIL, unexpected to FAILED, flaky to FAILED; (h) self-compare: the Runtime run 45259255785 `-rA` logs (`runtime-green/logs/`) against themselves exit 0 (unchanged tree passes).
- **Route:** X. The gate's false-green risk is the reason; S would be defensible if the owner wants a second reviewer on the semantics.
- **Size:** 2 days. **Depends on:** none. **Blocks:** GATE-R, GATE-A.
- **Confidence:** verified in code (defects 3a-c, probe-run). Vitest JSON field names: inferred from the Vitest 4 reporter, not run. Playwright JSON shape: verified from `direct-journey-outcome.jq`.
- **Open:** does `missing` count ceiling-only IDs or also inventory IDs (section 5)?

### REP-R: Runtime keeps `-rA` text and runs the missing jobs' pytest with `-rA` (astrid-runtime `.github/workflows/ci.yml`)
- **Repo:** astrid-runtime. **Cluster:** all jobs with pytest steps.
- **Kind:** n/a (reporting).
- **Fix:** every pytest step pipes through `tee "$TEST_RESULTS_DIR/<job>.log"` with `set -o pipefail` and `shell: bash` on Windows; the windows step's `-rP` becomes `-rA`; darwin-native (`:240`) and boundary (`:311`) gain `-rA --junitxml` and an upload; each upload step adds `*.log`.
- **Scope:** `ci.yml:60`, `63-66`, `70-72`, `76-88` (windows); `:165` (unit); `:240` (darwin); `:311` (boundary); `:361` (sandbox, through `run-suite.sh`); `:451` (portability); `:189-196`, `:386-394`, `:493-500` (uploads). `nightly.yml:93` and `:117-123` if the nightly comparison is wanted.
- **Focused proof:** one `workflow_dispatch` run on a scratch branch (no test code changes). Check: each job's artifact contains a `.log` whose PASSED + FAILED + XFAIL line count equals the pytest summary (`N passed, M failed, K xfailed`). **Injected review:** add one failing assertion in a scratch commit; the artifact's FAILED count rises by one. Hosted time about 45 minutes (unit ubuntu 12.5 min, macos 23 min in the measurement).
- **Route:** N. **Size:** 1 day. **Depends on:** none. **Blocks:** GATE-R.
- **Confidence:** verified in code (line numbers above).

### GATE-R: Runtime `tests` and `repeat` inputs, gate job, ceiling and inventory (astrid-runtime)
- **Repo:** astrid-runtime. **Cluster:** the 508 failing IDs (`runtime-green/failing-ids.tsv`) and the passing inventory.
- **Kind:** n/a (gate). Ceiling entries keep their own kinds (C1-C8 in `runtime-green/REPORT.md`).
- **Fix:** add `tests`, `job` and `repeat` to `ci.yml` `workflow_dispatch` (section 3); add a `gate` job with `needs:` on every pytest job, `if: always()`, that fails if any needed job did not succeed (a cancelled shard fails), builds the two pseudo-logs from `ci/runtime-ceiling.tsv` and `ci/runtime-inventory.tsv`, and runs `env/baseline-diff.py --gate --select`; seal both TSVs from one hosted run on the plan branch head.
- **Scope:** `ci.yml:9-14` (inputs), `:16-20` (concurrency unchanged), every pytest run line, new `gate` job at the end; new `ci/runtime-ceiling.tsv`, `ci/runtime-inventory.tsv`.
- **Focused proof, injected-failure review (all on a scratch branch):** (a) unchanged tree passes; (b) a scratch commit turns one passing unit test red: gate fails with `regression`; (c) a scratch commit deletes one passing test: gate fails with `missing`; (d) a commit that adds a new failing test: gate fails with `no-baseline`; (e) `tests=tests/test_skip_registry.py` on `job=unit` runs only that file and the gate passes; (f) cancel the unit-ubuntu job mid-run: gate fails; (g) `repeat=3` with a test that fails on one iteration: gate fails.
- **Route:** X. **Size:** 2 days (plus about 4 hosted hours for the review runs; `tests` runs take minutes). **Depends on:** ENV-ADP, REP-R.
- **Confidence:** verified in code for the inputs and the `cancel-in-progress` behaviour. The gate job and seal are designed, not built.
- **Open:** section 5 (ceiling-only versus inventory). Whether the windows and darwin jobs stay in the batch (they hard-code Agent SHAs).

### REP-A: App writes JSON for Vitest and Playwright, and uploads it (astrid-app)
- **Repo:** astrid-app. **Cluster:** all E2E and vitest jobs (85 failing in run 45231479752 at 3f5da385; vitest and boundary green).
- **Kind:** n/a (reporting).
- **Fix:** section 4 "Proposed reporter and upload change" (four Playwright configs, three Vitest configs, env vars in `test.yml`, `e2e.yml`, `lanes.yml`, `upload-artifact` after each).
- **Scope:** `playwright.config.ts:110`, `playwright.extension-accessibility.config.ts:44`, `playwright.extension-cross-browser.config.ts:44`, `playwright.extension-visual.config.ts:42`; `config/testing/vitest.config.ts:66`, `vitest.boundary.config.ts:44`, `vitest.astrid-renderer.config.ts`; `.github/workflows/test.yml:236`, `:239`; `e2e.yml:20-197` (six jobs' run and upload steps); `lanes.yml:78`, `:83`.
- **Focused proof:** one dispatch of `e2e.yml` and `test.yml` on a scratch branch. Check: each artifact is valid JSON; counts from the JSON equal the `list` reporter's totals. Injected review: a one-line `expect(false)` in one spec changes exactly one `unexpected` entry.
- **Route:** N. **Size:** 2 days. **Depends on:** none. **Blocks:** GATE-A.
- **Confidence:** verified in code (lines above). Vitest `json` reporter option: inferred, check against the installed version.

### GATE-A: App `tests` and `repeat` inputs, gate job, ceiling and inventory (astrid-app)
- **Repo:** astrid-app. **Cluster:** E2E (playwright-default 30F, timeline 36F, chrome-export 3F, extension-accessibility 9F, cross-browser 6F, visual 1F; figures from 3f5da385, `app-green/REPORT.md`), `checkout-lanes` 1F, `quick-journey` 1F. Ceiling per section 5.
- **Kind:** n/a (gate). Entries keep the causes in `app-green/REPORT.md` (1 fake Runtime, 2 retired route, 3 CI wiring, 4 stale tests, 5 quick-journey).
- **Fix:** `tests` and `repeat` on `e2e.yml`, `test.yml` (vitest) and `lanes.yml`; a gate job per workflow (or one aggregate workflow) that fails on any needed job's result; seal `ci/app-ceiling.tsv` and `ci/app-inventory.tsv` from a dispatch on the plan branch head. Remove the dead `AUTHORIZED_NAMES` entries (`check-known-failures.mjs:25-29`) only with an owner decision.
- **Scope:** `e2e.yml` (`workflow_dispatch` at `:9`; each run step); `test.yml:9-16` and `:236`; `lanes.yml:11` and `:78`, `:83`; new `ci/app-ceiling.tsv`, `ci/app-inventory.tsv`.
- **Focused proof, injected-failure review:** same seven cases as GATE-R, using one Playwright spec and one vitest file. Plus: (h) a `test.fail` removed from `three-products.spec.ts` (an expected failure now passes) gives `unexpected` and fails the gate.
- **Route:** X. **Size:** 2.5 days. **Depends on:** ENV-ADP, REP-A, and the expiry decision in section 0.5 (the guard goes red 26 Nov regardless of the gate).
- **Confidence:** verified in code for the workflow lines and the guard outputs. Gate job: designed, not built.

### Not cards: owner decisions needed now
- **Q-A (App expiry, 25 Nov).** Renew the four `three-products` entries (max 14 days, `MAX_EXPIRY_DAYS` `check-known-failures.mjs:17`), or fix the four tests, before 26 Nov. Route N for the edit, the decision is the owner's.
- **Q-R (Runtime expiry, 1 Dec).** Renew the nine xfail entries (`tests/lanes.py:138-242`, expiry `2026-12-01`) before 1 Dec. The owner is "R14 Lead", a role.

---

## 7. Open questions for the owner

1. **Ceiling only, or ceiling plus inventory?** Plan 91 line 23 says the ceiling holds failing IDs. Without the inventory, deleting a passing test is not caught. The inventory is about 30k lines for Runtime (passing counts in section 2).
2. **Renewals for Q-A and Q-R** (section 6), and whether the owners should be named people.
3. **Should the Runtime windows and darwin jobs stay in the batch**, given their hard-coded Agent SHAs and that `agent_sha` does not reach them?
4. **Should App's job-level-only jobs** (`quick-journey`, installers, `typescript-client`) gate on pass/fail only?
5. **Should PRs into the plan branch run the gate** (Runtime gets full CI on PRs), or only dispatches and `release/*/main` pushes?

## 8. What I could not verify

- No hosted run was dispatched, no scratch branch was made, and no test was run except the read-only guard scripts on archived trees (`git archive` of `origin/release/15/main`). Proofs above are designed, not executed.
- Vitest 4 JSON reporter option names and status strings: not checked against the installed package.
- Playwright JSON `flaky` handling: from the reporter's documented statuses and `direct-journey-outcome.jq`, not run.
- Issue states for astrid-app #249-252 and astrid-dev #805-809: not fetched.
- The `vitest.astrid-renderer.config.ts` reporter line number: not captured (only its reporter content).
- Hosted durations: taken from the measurement reports, not re-measured.
- The R14 App ceiling (`release/14/plan-39`) was read, not run.
