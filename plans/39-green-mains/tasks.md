# Tasks — Runtime and App main green

[Plan](plan.md) · [Inputs](inputs.md)

**Base:** `release/15/main` in astrid-runtime, astrid-app and astrid-dev, until `release/16/main` is cut ([D11](inputs.md#owner-decisions)). **Plan branch:** `release/16/plan-39` in each, cut by GM-0. It merges `release/15/main` in whenever that moves, and `release/16/main` once it exists; it never rebases. The Release 14 tasks are kept in [the record](evidence/release-14-record/tasks.md).

**Task ids:**
- `GM-<n>` for the gates, the tools, the prune pass and the end;
- `RT-<n>` for Runtime CI causes;
- `RN-<n>` for Runtime Nightly causes;
- `AP-<n>` for App causes.

Each row links the evidence file with its full card: the IDs, the evidence and the fix. The helpers' own card names are in brackets. Unused numbers:
- GM-9;
- RN-1 to RN-3: Nightly's N-1 and N-2 are in RT-10, and N-3 is in GM-P1.

**Critical path:** GM-0 → GM-1 → GM-3 and GM-5 (the ceilings sealed) → the phase 1 cause cards land → RS1 → the phase 2 cards land → GM-10 → R.

**Workers:** five slots, shared by the two repositories. Runtime and App runs don't count against the Agent's limit of two CI runs at once. The manager keeps at most two full runs at once per repository, unless the Release 16 Lead rules otherwise.

**Test inventory:**
- every test file in [runtime-failing-ids.tsv](evidence/release-15-measure/runtime-failing-ids.tsv) (508 distinct IDs) and [runtime-nightly-failing-ids.tsv](evidence/release-15-measure/runtime-nightly-failing-ids.tsv) (152) at Runtime `24e2c929`;
- the App E2E and Lanes failures in [app-ci.md](evidence/release-15-measure/app-ci.md) at App `3f5da385`;
- the green jobs' tests, which must stay green.

A card's proof runs only its own files.

## How work is proved

1. **The card's own check.**
   - **Runtime:** a pull request into `release/16/plan-39` runs the Runtime's full CI (`ci.yml:8` has no branch filter), so a Runtime card's pull request is its hosted proof. Locally, `env/runtime-pytest.sh` with the card's files.
   - **App:** a pull request into a plan branch starts nothing. An App card proves with `env/app-test.sh` (Vitest) or `env/app-e2e.sh` (Playwright, added by GM-8), then a dispatch of `e2e.yml` or `lanes.yml` on its branch with the `tests` input (GM-5).
2. **The batch run.** After merging up to five cards, the manager dispatches the full workflows on `release/16/plan-39`, including the Runtime's `nightly.yml`. They compare the results with the ceiling by (job, id), using `env/baseline-diff.py --gate`. This is the gate.
3. **The ceiling is a ratchet only the manager edits.** Cards never touch `ci/runtime-ceiling.tsv` or `ci/app-ceiling.tsv`. After a green batch comparison, the manager removes every ID that passed and commits the new ceiling.

## Triage rules

[Plan 91's triage rules](../91-agent-main-green/tasks.md#triage-rules) apply unchanged: prune before fixing, reproduce first, one kind per cause with evidence, the allowed fix and proof per kind, no other change, prove by ID, and stop at twice the size. Here, "D5" in those rules means this plan's [D12](inputs.md#owner-decisions), and "D6" means [D21](inputs.md#owner-decisions) for an Agent bug or an accepted ceiling entry for any other bug. Two dating limits apply to the stale-test rule:
- The Runtime's history is squashed to 27 October.
- The App's history is grafted, with whole-tree commits `2dc109b` and `f72e869`.

So a card dates a change by its pull request, plan task or brief line, never by `git log` alone ([why](evidence/release-15-measure/app-stale.md)).

## Task index

Sizes are engineering days. Line numbers are at Runtime `24e2c929` and App `d53685f3`; re-check them against the code at dispatch.

### Phase 1: the gates, the prune pass and the large causes

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| GM-0 Cut `release/16/plan-39` from each `release/15/main` head and re-measure. Bump the Runtime's `tests/astrid-agent.pin` to the Agent's `release/15/main` head ([D16](inputs.md#owner-decisions)). Dispatch the Runtime's `ci.yml` and `nightly.yml` and the App's `test.yml`, `e2e.yml` and `lanes.yml` on the plan branches, and regroup with `plans/91-agent-main-green/evidence/cluster_failures.py`. **Name what cancels started runs:** every job on App `d53685f3` was cancelled 14 seconds in, before a runner took it, and three Runtime runs on 22 November, where no concurrency setting cancels them ([base-overlaps.md](evidence/release-15-measure/base-overlaps.md)). Share the answer with Plan 91's AG-0. 1 | N | the owner's go | astrid-runtime `tests/astrid-agent.pin`; astrid-dev this plan's `evidence/` | ID totals equal each job's summary line; the IDs that changed since `24e2c929` and `3f5da385` are listed; the cancelling actor or rule is named with its evidence | [ ] |
| GM-1 The comparator, once for both repositories [ENV-ADP]. `env/baseline-diff.py` gains:<br>- a `--format ids` input that keeps the ID verbatim (today an ID with a space is cut short, so a Playwright regression reads as preexisting);<br>- a `--gate` exit that blocks on a regression, a new failing test (`no-baseline`) and a missing test;<br>- `--select` to limit the comparison to named files;<br>- unit tests for each, in `scripts/test_baseline_diff.py`.<br>`env/app-results-ids.mjs` turns Vitest and Playwright JSON into ID lines. Lands after Plan 91's AG-1, which changes the same `sort_results` and `main` for the `missing` bucket. 2 | X | Plan 91 AG-1's `env/baseline-diff.py` change | astrid-dev `env/baseline-diff.py` (`_node_id`, `parse`, `sort_results`, `main`), `env/app-results-ids.mjs`, `scripts/test_baseline_diff.py`, `env/README.md` | Reviewed by injected failures, the eight cases in [gate-design.md](evidence/release-15-measure/gate-design.md) card ENV-ADP, including the space-in-ID probe that reads preexisting today | [ ] |
| GM-2 Runtime reporting [REP-R]. Every pytest step keeps its `-rA` text as an artifact. The jobs without it gain it: the Windows step (`-rP`), `darwin-native` and `boundary`. So does `nightly.yml`. | N | — | astrid-runtime `.github/workflows/ci.yml` (pytest and upload steps), `.github/workflows/nightly.yml` (the same) | One dispatch on a scratch branch: each artifact's PASSED, FAILED and XFAIL lines equal that job's pytest summary; one injected failing assertion raises FAILED by one | [ ] |
| GM-3 The Runtime gate [GATE-R]. Add `tests`, `job` and `repeat` inputs to `ci.yml`'s `workflow_dispatch`. Add a `gate` job that fails on any needed job's non-success (so a cancelled job fails) and runs `env/baseline-diff.py --gate`. Seal `ci/runtime-ceiling.tsv` from one hosted run on the plan branch head. 2 | X | GM-0, GM-1, GM-2 | astrid-runtime `.github/workflows/ci.yml` (the `on:` block, the test-selection lines, a new `gate` job), `ci/runtime-ceiling.tsv` | Reviewed by the seven injected failures in [gate-design.md](evidence/release-15-measure/gate-design.md) card GATE-R: an unchanged tree passes; a new red test, a deleted test, a new failing test, a cancelled job and a one-in-three failure under `repeat` each fail; a `tests` dispatch runs only the named file | [ ] |
| GM-4 App reporting [REP-A]. Each Playwright and Vitest config writes JSON results when CI asks, and each job of `test.yml`, `e2e.yml` and `lanes.yml` uploads them. 2 | N | — | astrid-app the four `playwright*.config.ts`, the three `config/testing/vitest*.config.ts` (reporter lines only), and those three workflows' run and upload steps | One dispatch of `e2e.yml` and `test.yml` on a scratch branch: each artifact is valid JSON whose totals equal the list reporter's; one injected `expect(false)` adds exactly one unexpected entry | [ ] |
| GM-5 The App gate [GATE-A]. `tests` and `repeat` inputs on `e2e.yml`, `test.yml` and `lanes.yml`, a gate job per workflow, and `ci/app-ceiling.tsv` sealed from one dispatch on the plan branch head. 2.5 | X | GM-0, GM-1, GM-4 | astrid-app `.github/workflows/e2e.yml`, `test.yml`, `lanes.yml` (the `on:` blocks, test selection, a gate job), `ci/app-ceiling.tsv` | As GM-3, with one Playwright spec and one Vitest file; plus a `test.fail` that now passes turns the gate red | [ ] |
| GM-8 A worker script for App E2E: `env/app-e2e.sh` runs named Playwright specs against the fake Runtime in a disposable copy, as `env/app-test.sh` does for Vitest. 1 | N | — | astrid-dev `env/app-e2e.sh`, `env/README.md` | From an App checkout, it runs one passing and one failing spec and reports each; with Node absent it exits 3 | [ ] |
| GM-P1 The prune pass, Runtime. Sort every candidate in [rt-tail-nightly.md](evidence/release-15-measure/rt-tail-nightly.md) (section 5) and [rt-env.md](evidence/release-15-measure/rt-env.md) into retire, redundant or keep under [D12](inputs.md#owner-decisions) and [D25](inputs.md#owner-decisions). Known candidates:<br>- `test_snapshot_legacy_certification.py`, 20 Nightly IDs, which need an Agent commit GitHub no longer serves;<br>- the R0 install-boundary rollback, 3 IDs;<br>- the v28 inline spec and the v31 migration tests, 3 IDs;<br>- the legacy timeline write route, which keeps a test that it refuses;<br>- `test_wc10_installed_launcher.py`, which builds from a historical Agent commit;<br>- the `neutral` variant in `test_timeline_reference_authority.py`, which RT-1 drops.<br>Be bold with what is old and careful with what is current. One pull request lists every deleted ID with its citation or covering test. The App helpers found no App test to retire ([app-stale.md](evidence/release-15-measure/app-stale.md)). 1.5 | X | GM-0 | astrid-runtime the candidate test files (deletions and refusal tests only; no product code) | For each deletion, the citation or covering test's ID, with a passing run of the covering tests; any refusal test passes; an `X` reviewer reads the list | [ ] |
| RT-1 The migrated realm's provider, part one (232 IDs, cluster C1) [P39-RT1]. A shared test helper registers the Timeline provider before the first mutation. `_seed` registers it before its capabilities. One negative test keeps the fence's refusal. Stale tests: the 1 November fence is correct ([rt-c1c2.md](evidence/release-15-measure/rt-c1c2.md)). 2.5 | X | GM-0 | astrid-runtime `tests/test_timeline_effect_authority.py:_seed`, `tests/test_timeline_reference_authority.py:seed`, `:service_case`, `tests/test_timeline_document_authority.py:documents`, a new `tests/migrated_realm.py`; no product code | `tests/test_timeline_effect_authority.py`, `test_timeline_document_authority.py`, `test_timeline_reference_authority.py`, `test_project_reference_catalog.py`, `test_realm_admission_hardening.py`, plus the negative test | [ ] |
| RT-2 The migrated realm's provider, part two (126 IDs, C2) [P39-RT2]. Daemon fixtures on a migrated realm pass `authoring_profile="astrid"`, as the App always does. One negative test that a neutral daemon refuses. Also Nightly's N-13 registration case. 1.5 | N | RT-1 | astrid-runtime `tests/test_timeline_authority_door.py:realm`, `tests/test_timeline_effect_authority.py:boundary`, and the daemon constructor lines of the four files in [rt-c1c2.md](evidence/release-15-measure/rt-c1c2.md) | `tests/test_timeline_authority_door.py`, `tests/test_timeline_effect_authority.py -k http`, the negative test; the C2 IDs re-counted after RT-1 | [ ] |
| RT-10 The precut-v31 fixture digests and the commit-crash fixture (8 CI and 24 Nightly IDs: CI-1, N-1, N-2), which share one fixture root at `test_timeline_commit_crash.py:78` ([rt-tail-nightly.md](evidence/release-15-measure/rt-tail-nightly.md)). Kind unknown; diagnose first. 2.5 | X | GM-0 | astrid-runtime `tests/precut_realm_fixture.py` (the digest and pin helpers), `tests/test_timeline_commit_crash.py`, and the CI-1 files | `tests/test_timeline_commit_crash.py` and the CI-1 files, in CI and in a `nightly.yml` dispatch | [ ] |
| AP-1 The fake Runtime serves what the App calls (about 44 IDs) [FR-01, FR-02]. Serve `GET /api/runtime/packs/inventory` and `/packs/project-elements` at their full prefixed paths, and `GET .../timelines/{t}/commits` as a history page ([app-fake-runtime.md](evidence/release-15-measure/app-fake-runtime.md)). The empty-pack answer is the E2E baseline ([D24](inputs.md#owner-decisions)). 1.5 | N | GM-0 | astrid-app `tests/e2e/fake-runtime/server.ts:dispatch` | `tests/e2e/fake-runtime/server.contract.test.mjs`; then an `e2e.yml` dispatch on the card's branch, where the extension-accessibility (9), extension-cross-browser (6) and route-attributed timeline IDs pass | [ ] |
| AP-2 A route-coverage check [FR-03]. `server.contract.test.mjs` fails when the App calls a route the fake doesn't serve, unless it is listed with a reason. 1.25 | X | AP-1 | astrid-app `tests/e2e/fake-runtime/server.contract.test.mjs` | The check passes on the plan branch; removing one served route makes it fail with that route's name | [ ] |
| AP-11 CI installs the browsers its tests ask for (2 IDs) [A1, A2]. `checkout-lanes` installs Chromium. `command-outbox.spec.ts` uses the installed browser, not `/opt/pw-browsers/chromium` ([app-wiring-journeys.md](evidence/release-15-measure/app-wiring-journeys.md)). 0.5 | N | GM-0 | astrid-app `.github/workflows/lanes.yml` (checkout-lanes steps), `tests/e2e/**/command-outbox.spec.ts:31` | `runtimePackRefresh.integration.test.ts` in a `lanes.yml` dispatch; `command-outbox.spec.ts` in an `e2e.yml` dispatch | [ ] |
| AP-13 The quick journey sets `journey.sources` in quick mode too, so its `afterAll` can pass (1 ID) [A4]. 0.25 | N | GM-0 | astrid-app `tests/e2e/local/three-products.spec.ts` (the quick-mode setup at `:87-99` only) | A `lanes.yml` dispatch: quick-journey passes | [ ] |
| RS1 Review stop after phase 1. It reviews the gates, the prune list and the phase 1 fixes on the integrated plan branches, and the phase 2 cards regenerated from the re-measure. Then the plan branches land in `release/16/main` (or `release/15/main` if the Release 16 Lead rules so) with the owner's go. Rounds at most 1. | S | GM-0 to GM-8, GM-P1, RT-1, RT-2, RT-10, AP-1, AP-2, AP-11, AP-13 | read-only | Same protocol as R, on the integrated result; findings become rows `RS1.<n>`; phase 2 depends on this row | [ ] |

### Phase 2: the middle and the long tail

Each row is one cause the helpers found, with their first reading of the kind; rule 2 confirms it. Full cards: Runtime in [rt-c3c7.md](evidence/release-15-measure/rt-c3c7.md), [rt-env.md](evidence/release-15-measure/rt-env.md) and [rt-tail-nightly.md](evidence/release-15-measure/rt-tail-nightly.md); App in [app-stale.md](evidence/release-15-measure/app-stale.md), [app-fake-runtime.md](evidence/release-15-measure/app-fake-runtime.md) and [app-wiring-journeys.md](evidence/release-15-measure/app-wiring-journeys.md). Each card's proof is its own files, in its repository's hosted run (Runtime) or dispatch (App). Cards in the files that Plan 89's `release/15/plan-89` changes (`test_timeline_commit_sequential_verifier.py`, `test_timeline_commit_acceptance.py`, `test_timeline_recorder_abi_authority.py`) start after Plan 89 lands.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| RT-3 Starter tracks (39 IDs: C3, C7, C32, C34, C35) [RT-C3C7-1]. The Runtime now starts a timeline with V1 and A1. Update five expectations, as [D17](inputs.md#owner-decisions) rules. Stale test; product bug if D17 says timelines start empty. 0.5 | N | RS1, D17 | astrid-runtime `tests/test_timeline_inverse_sequential_authority.py:30`, `test_timeline_forward_created_authority.py:82,124`, `test_timeline_legacy_authority.py:476,522` | Those three files and `tests/test_timeline_commit_baseline.py` | [ ] |
| RT-4 Publication tests use a pack that moved to poms_packs (20 IDs, C4) [RT-E1]. Rewrite `_publish` to call the Runtime's own publish path, so no pack is needed ([D18](inputs.md#owner-decisions)). 1 | X | RS1 | astrid-runtime `tests/test_timeline_render_publication.py:_publish`, `tests/test_timeline_render_publication_authority.py` | Those two files | [ ] |
| RT-5 Clip type `image` doesn't resolve (12 IDs, C5) [RT-E2]. An Agent bug, handed to Plan 91 under [D19](inputs.md#owner-decisions) and [D21](inputs.md#owner-decisions). This row bumps the pin once the Agent fix lands. 0.25 | N | RS1, the Plan 91 card | astrid-runtime `tests/astrid-agent.pin` | `tests/test_timeline_native_asset_union.py` | [ ] |
| RT-6 "Created identity is occupied" in the sequential-verifier seed (10 IDs, C6) [RT-E3]. Unknown; diagnosis capped at two hours. 1 | X | RS1, Plan 89 landing | astrid-runtime `tests/test_timeline_commit_sequential_verifier.py` and its fixture | That file | [ ] |
| RT-7 The portability stage venv lacks the Agent (8 IDs) [RT-E4]. Install it when `ASTRID_CHECKOUT` is set, and refuse when it isn't. Env. 0.75 | N | RS1 | astrid-runtime `tests/conftest.py` (the stage venv builder at `:146-214`) | `portability-lifecycle` on ubuntu and macOS | [ ] |
| RT-8 Sandbox-only pidfd tests (18 IDs) [RT-E5]. In the sandbox job they assert the refusal the sandbox gives, and they run for real in unit ([D20](inputs.md#owner-decisions)). No deselection. 2 | X | RS1, D20 | astrid-runtime the 18 tests' files and `tests/seccomp/run-suite.sh` (markers only) | `sandbox-process-control` and `unit` | [ ] |
| RT-9 The commit-phase capture test reads an App file at a hard-coded path (1 ID) [RT-E6a]. CI checks the App out at its pin. Env. 0.25 | N | RS1 | astrid-runtime `tests/test_p2_commit_phase_capture.py:62`, `ci.yml` (the checkout steps) | That file | [ ] |
| RT-11 Expectations from before `blendMode` (5 IDs) [CI-2]. Stale test. 0.75 | N | RS1 | the CI-2 files | Those files | [ ] |
| RT-12 Bootstrap stale-owner messages (5 IDs) [CI-5]. Stale test on macOS; unknown in the sandbox. 1 | N | RS1 | the CI-5 files | Those files on macOS and in the sandbox | [ ] |
| RT-13 Diagnostics and operator lifecycle messages (3 IDs) [CI-6]. Unknown. 1 | N | RS1 | the CI-6 files | Those files | [ ] |
| RT-14 Fail-closed rejections, credentials and fresh-state polling (6 IDs) [CI-7]. Suspected product bug. 1.5 | S | RS1 | the CI-7 files and the product code the diagnosis names | Those files | [ ] |
| RT-15 Timeline commit authority: the SQLite authorizer, verified media, compare-and-swap, the producer checkpoint and recorder bindings (7 IDs) [CI-8]. Suspected product bug for verified media. 2 | S | RS1, Plan 89 landing | the CI-8 files and the product code the diagnosis names | Those files | [ ] |
| RT-16 Gates and harness: the skip policy, the rename audit and `check_it.py` (3 IDs) [CI-9]. 0.5 | N | RS1 | the CI-9 files | Those files | [ ] |
| RT-17 A test double and a spec dedup (2 IDs) [CI-10]. 0.25 | N | RS1 | the CI-10 files | Those files | [ ] |
| RN-4 History assembly no longer refuses a mutation whose inputs changed after the ancestor check (15 IDs, `test_timeline_history_assembly.py:300`) [N-4]. **Suspected product bug: a safety refusal is missing.** 2 | S | RS1 | astrid-runtime the history assembly code the diagnosis names, `tests/test_timeline_history_assembly.py` | That file in a `nightly.yml` dispatch | [ ] |
| RN-5 History: the other unverified-dependency and lookup refusals (12 IDs) [N-5]. 1.5 | S | RN-4 | the same file and code | As RN-4 | [ ] |
| RN-6 Nightly runs without `--process-control`, so strict process control fails (6 IDs) [N-6]. Env. 0.5 | N | RS1 | astrid-runtime `.github/workflows/nightly.yml` (the pytest step) | `tests/test_runtime_boundary.py` in a `nightly.yml` dispatch | [ ] |
| RN-7 Visual fields: provider acceptance and refusals (7 IDs) [N-7]. Contract drift with the Agent. 1 | X | RS1 | `tests/test_timeline_visual_fields.py` and the code named | That file | [ ] |
| RN-8 Visual refusals before publication (7 IDs) [N-8]. May be redundant with RN-7. 1.5 | X | RN-7 | `tests/test_timeline_commit_integration.py` (those tests) | That file | [ ] |
| RN-9 Native clip replacement (6 IDs) [N-9]. 1 | N | RS1 | `tests/test_timeline_clip_replacement.py` | That file | [ ] |
| RN-10 Historical render admission (7 IDs) [N-10]. Check against D12 before fixing. 1.5 | X | GM-P1 | `tests/test_render_historical_admission.py` | That file | [ ] |
| RN-11 Capture candidate binding (6 IDs) [N-11]. 1.5 | X | RS1 | `tests/test_capture_candidate_binding.py` | That file | [ ] |
| RN-12 The legacy word anchor the Agent refuses (9 IDs) [N-12]. Stale test, or retired under D12. 2 | X | GM-P1 | the N-12 files | Those files | [ ] |
| RN-13 A corrupt local timing cache (the cache case of N-13; the registration case is RT-2's) [N-13]. 1 | N | RT-2 | the N-13 files | Those files | [ ] |
| RN-14 Contract and CLI drift: the schema digest's pin skew, the public CLI's 410, and a saved-revision hydrate (4 IDs) [N-14]. Mostly closed by GM-0's pin bump. 1 | N | GM-0 | the N-14 files | Those files | [ ] |
| RN-15 Timeline repair, redo, mixed helper undo and source identity (10 IDs) [N-15]. 2 | X | RS1 | the N-15 files | Those files | [ ] |
| RN-16 Update jobs assume a sibling `../astrid-agent` (3 IDs) [N-16]. Env. 0.5 | N | RS1 | `tests/test_update_jobs.py:1058-1078` | That file | [ ] |
| RN-17 Launch and pack fixtures: a moved function, a removed Darwin setting and a pack `IndexError` (4 IDs) [N-17]. 1 | N | RS1 | the N-17 files | Those files | [ ] |
| AP-3 Pack routes are outside the Runtime's contract [FR-05, FR-06]. List them in the fake with citations. Vendor the Runtime's OpenAPI file into `runtime.lock.json`, so AP-2's check reads the contract. File a Runtime issue to add the pack routes to `workspace-v1.yaml` ([D24](inputs.md#owner-decisions)). 1 | N | AP-2 | astrid-app `tests/e2e/fake-runtime/`, `runtime.lock.json` (`files`) | AP-2's check, reading the vendored file | [ ] |
| AP-4 The publish helper posts to the retired `composition-revisions` route (1 ID) [FR-04, APP-08]. Publish through commit, and give the fake a `/commit` handler. 1.25 | X | AP-1 | astrid-app `tests/e2e/timeline/support.ts:264-288`, `tests/e2e/fake-runtime/fakeWorkspaceRuntime.ts` (the commit handler) | `preview-scrub-evidence.spec.ts:231` | [ ] |
| AP-5 Generated routes the App calls that the Runtime's browser door refuses (84 operations, such as `GET /v1/capabilities`) [FR-07]. Unknown; decide whether each is a product bug or another door. 1.5 | X | AP-2 | read-only, then the card it names | A list of each route with the door that serves it, checked against the Runtime's `door.py` | [ ] |
| AP-6 production-widget-scope (5 IDs) [APP-01]. The add-to-timeline button is gone, and the Export label changed. Stale test, once its source is found. 0.5 | N | RS1 | the spec file | That spec | [ ] |
| AP-7 Hover specs run on touch projects (12 IDs) [APP-02]. Each hover test sets `hasTouch: false` and `isMobile: false`; the passing mobile tests in those files stay. Env. 0.5 | N | RS1 | the vision hover spec files (test options only) | Those specs on every project | [ ] |
| AP-8 Vision specs fetch the live public feed (3 failing IDs, 12 specs) [APP-03, APP-04]. Use `tests/fixtures/public-vision.ts`, so no test reads the network. Env. 1 | N | RS1 | the vision spec files | Those specs, with the network blocked | [ ] |
| AP-9 Workflow parity: Download is now an anchor download, and the picker is for "Save as…" (3 IDs) [APP-05]. Stale test, source astrid-app PR #128. 0.5 | N | RS1 | `video-editor-workflow-parity.spec.ts` (the `:133` test) | That spec | [ ] |
| AP-10 Diagnose the four unknowns: workflow-parity `:27` (3 IDs), instance-lifecycle `:34` (1), editor-tour (4) and the extension-visual baseline size (1) [APP-06, APP-07, APP-09, APP-11]. Each becomes its kind's fix. 3 | N, X after rule 6 | AP-1 | the four specs, and the code each diagnosis names | Those specs | [ ] |
| AP-12 viewing-parity needs a lock holder and pinned browsers (10 IDs) [A3]. As [D23](inputs.md#owner-decisions) rules. 1.5 | X | RS1, D23 | astrid-app `.github/workflows/e2e.yml` (one job), `tests/e2e/**/viewing-parity` harness setup | The 10 viewing-parity IDs in that job | [ ] |
| AP-14 Direct Journey: the `:417` concurrent edit (18–22 November) and the `:3690` empty bootstrap (23 November) [A5, A6]. Diagnose on a dispatch on the plan branch. 1 | N, X after rule 6 | RS1 | `tests/e2e/local/three-products.spec.ts` and the code named | A `direct-journey.yml` dispatch | [ ] |
| AP-15 A duplicated shot saves nothing (#249, quarantined) [Q1]. Product bug. 0.75 | X | RS1 | the App code the issue names, and the entry in `config/testing/direct-journey-expected-failures.json` (removed when fixed) | The test passes and its entry is gone | [ ] |
| AP-16 Extension batch needs a replacement driver (#250, quarantined) [Q2]. 1.25 | X | RS1 | the three-products extension driver and its entry | As AP-15 | [ ] |
| AP-17 **A dropped video is lost on reload (#252, quarantined): data loss.** The fix commits on `scratch/r12-drop-fix` (`f530e00`, `e57507a`, `85125e6`) are the starting point, re-proved on the plan branch. 1.5 | S | RS1 | the App save path those commits touch, and the entry | As AP-15, plus a reload after a drop keeps the video | [ ] |
| AP-20 The App's skip registry gains an owner and a reason for each of its 9 skips, and loses the three authorized names that have no marker. 0.5 | N | RS1 | astrid-app `config/testing/skipRegistry.mjs`, `scripts/quality/check-known-failures.mjs:25-29` | `npm run check:skip-registry` and `check:known-failures` | [ ] |

### Phase 3: kept green

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| GM-6 The nightly red report. `scripts/ci_red_report.py` and a nightly workflow in astrid-dev read the latest run of every listed workflow on each repository's `main` and release branch: the Agent, the Runtime and the App. It posts one comment a night, on one rolling issue, naming new red and every quarantined test with its age (the Release 14 record's D4). 2.5 | X | GM-3, GM-5 | astrid-dev `scripts/ci_red_report.py`, `.github/workflows/ci-red-report.yml`, a unit test beside it | Unit tests on recorded run listings: a new failure is named, an unchanged one is not, a cancelled run is named as no result | [ ] |
| GM-7 The required checks. `ci/required-checks.json` in the Runtime and the App, in Plan 91 AG-2's format, with a merge tier and a release tier (the Release 14 record's D2), for the owner to turn on and for Plan 31's `release-contract` to read. 0.5 | N | RS1, Plan 91 AG-2 | astrid-runtime and astrid-app `ci/required-checks.json` | Each named check exists in that repository's workflows; a check that doesn't exist fails the file's own test | [ ] |
| GM-10 Three green runs of every included workflow on one frozen head of `release/16/plan-39` (merged up with its release branch), dispatched on three different nights. Then one green run on `release/16/main` after the plan branch lands. Each ceiling is empty or holds only entries the owner accepted, and each quarantine holds 10 IDs or fewer. | N | all other rows except R | read-only | The run links, each green, recorded here | [ ] |
| R Final review. Rounds at most 2. | S | all other rows | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R<round>.<n>` below this one | [ ] |

### Phase 4: the three-products structure

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| AP-18 Each three-products test owns its seed: a repeatable per-project seed, its own `astrid` CLI and explicit project URLs, in place of the worker-scoped `seed3` (the Release 14 record's SF1a) [S1]. 3.5 | X | AP-14, AP-15, AP-16, AP-17 | astrid-app `tests/e2e/local/three-products.spec.ts`, `tests/e2e/local/support/harness.ts` (the seed functions) | Each test passes alone, with `--grep` on its title | [ ] |
| AP-19 The three-products suite runs shuffled on two workers [S2]. 1.5 | N | AP-18 | astrid-app the three-products Playwright project's settings | Three shuffled dispatches pass; a test that reads another's state fails in a shuffled run | [ ] |

## Dispatch order

1. **Day one.** GM-0 in slot 1. When it has cut the branches: GM-1, GM-2, GM-4 and RT-1 in slots 2–5, then GM-8, GM-P1, AP-1, RT-10, AP-11 and AP-13 as slots free up. GM-3 and GM-5 follow their dependencies. The ceilings seal before any cause card lands.
2. **After RS1.** Each repository's phase 2 rows, most IDs first: Runtime RT-3, RT-4, RN-4 and RT-8; App AP-7, AP-10, AP-12 and AP-17. Rows waiting on Plan 89 or a decision start as soon as it lands. GM-6 and GM-7 start beside them.
3. **Workflow-edit merge order:** in the Runtime, GM-2, GM-3, RT-9, RN-6; in the App, GM-4, GM-5, AP-11, AP-12.

**Landing:** a card's pull request goes into `release/16/plan-39` after its focused proof. The manager merges up to five, runs the batch comparison, ratchets the ceiling, and reverts any card whose batch shows a new failure. Each plan branch lands with the owner's go: once after RS1, and at the end.

## Estimate

| Phase | Days |
| --- | --- |
| 1: the gates, the tools, the prune pass and the large causes | 20–26 |
| 2: Runtime CI, Runtime Nightly and App, by cause | 30–40 |
| 3: the report, the required checks and the green nights | 6–8 |
| 4: the three-products structure | 4–6 |
| **Total** | **60–80** |

The helpers' card sizes add up to about 80 days. The prune pass and the re-measures at GM-0 and RS1 should take 10–20 off, as they did for Plan 91. Phase 2 has many unknown kinds, and the Nightly rows cost more per ID, because each proof is a dispatch. With five workers that is about 4–5 weeks elapsed, set by the batch runs and three green nights, not by worker count.
