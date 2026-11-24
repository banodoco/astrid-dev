# Plan 39 (Runtime and App main green): independent critique

Critic: a fresh high-judgment session with no stake in the draft. Read-only: nothing was changed, pushed, commented or dispatched.

**What I read.** astrid-dev `claude/elegant-turing-asiqz3`: plan, tasks and inputs at `9dce78c`. They were unchanged at `6b634fe`, which added `ambiguity-runtime.md` and `ambiguity-app.md` during this review. I also read the Plan 91 records (`277b246`, moved to Release 16), `releases/16.md` and `releases/16/run.md`.

**Code.** Runtime `release/15/main` `24e2c929` (`main` `5120462`, `release/15/plan-89` `81f04492`), App `release/15/main` `d53685f3` (`main` `e0da794`, `release/15/plan-77`, `plan-77-r7`) and Agent `514499de`. I also read GitHub REST run listings and annotations.

Severity:
- **blocking:** fix before the owner is asked to confirm D12–D27.
- **should-fix:** a worker would act on it wrongly, or it costs real days.
- **minor:** wording or a small fact.

## 1. Claims that are wrong in code or workflows

### 1.1 The gate cannot catch a missing or deleted test as designed (blocking)

**The claim:** plan.md:35 and Completion (plan.md:99) say that "a missing test blocks". GM-1 and GM-3 seal only `ci/runtime-ceiling.tsv` and `ci/app-ceiling.tsv`, the failing pairs.

**The code:**
- `env/baseline-diff.py:75-76` computes `missing` as IDs that passed on a baseline minus the candidate.
- A ceiling holds only FAILED lines, so `passed_somewhere` is empty and `missing` is always empty.
- A test deleted from the ceiling, for example by a prune or a card, passes silently.
- A passing test that is deleted is invisible, because no file lists the passing tests.

gate-design.md §5 and §7 Q1 raised this as an open question: ceiling plus an inventory. The plan dropped it without a decision. The inputs.md "three defects" list (lines 36-39) also omits gate-design's defect (c): `missing` should cover every baseline state, not only PASS. Plan 91's AG-1 only makes `missing` exit non-zero, so no card owns defect (c).

**Change:** make it an explicit decision and put it in GM-1 and GM-3. Either:
- seal the passing inventory too, as `ci/<repo>-inventory.tsv` or the seal run's committed `-rA` ID list; or
- feed the seal run's full logs as the baseline.

Also add "missing over all baseline states" to GM-1. Then the negative case "a deleted test turns the gate red" can be met.

### 1.2 "App PRs into a plan branch start nothing" is false (should-fix)

The claim is at tasks.md:135 ("a pull request into a plan branch starts nothing") and inputs.md:48. Four App workflows do run on such a PR:
- `direct-journey.yml` `on: pull_request: paths:`, with no branch filter. Its paths include `tests/e2e/local/**`, `tests/e2e/support/**` and `playwright.three-products.config.ts`.
- `dockerfile-check.yml`, on every PR.
- `public-vision.yml`, by paths; AP-8's vision specs may match.
- `installer-windows.yml`, by paths.

Direct Journey PR runs appear in the run list, for example `p77/svl2` and `release/15/plan-69-app-landing`. So AP-13, AP-14, AP-15 to AP-17 and AP-18/19 PRs get a Direct Journey run, and it will show red for the known failures.

**Change:** state which App workflows a plan-branch PR starts. Use the free Direct Journey PR run as those cards' hosted proof, and tell the manager that red on it is expected baseline red.

### 1.3 Nightly's 152 IDs were not measured at `24e2c929` (should-fix)

tasks.md:125 says "(152) at Runtime `24e2c929`". In fact:
- `runtime-nightly-failing-ids.tsv` has the job `nightly_main`, and the evidence README.md says run 45166036353 was on `main`.
- Nightly has never run on `release/15/main`. Its runs are schedule on `main`, plus pushes to `release/14/plan-39`.
- `release/15/main` is 63 commits and 46 files ahead of `main`.

**Change:** say the Nightly inventory is at `main` `5120462`, and treat GM-0's Nightly dispatch as the first real measurement. Mark the RN rows as provisional until RS1 or GM-0.

### 1.4 GM-2 adds `-rA` to `nightly.yml`, which already has it (should-fix)

`nightly.yml:93` is `python -m pytest -q -rA --junitxml=...`, and it uploads at `:117-123`. The unit, sandbox and portability jobs also already print `-rA` (`ci.yml:165`, `:361`, `:451`). The logs the comparison needs are available through the jobs API, which is how the measurement was taken. The tee-to-artifact is a convenience, not a requirement.

**Change:** GM-2 adds `-rA` only to the Windows steps (`ci.yml:60-88`, three of which have no `-r` flag), `darwin-native` (`:240`) and `boundary` (`:311`). Drop `nightly.yml` and the tee. Size it at about 0.5 days; today it has no size.

### 1.5 Plan 89's overlap is undercounted, and RN-4, RN-5 and RN-8 miss the dependency (should-fix)

inputs.md:93 says Plan 89 "changes three test files that hold 54 of this plan's IDs". The 54 is a row count: the TSV has 54 rows, which are 18 distinct IDs times 3 jobs. The count also ignores Nightly.

`release/15/plan-89` (`81f04492`, still active today: PR #118, then SV-L9a and SV-L10) also changes:
- `tests/test_timeline_history_assembly.py`, which holds 27 Nightly IDs (RN-4 and RN-5);
- `tests/test_timeline_commit_integration.py`, 10 IDs (RN-8);
- `test_timeline_projection_occupancy.py`;
- the product files `history_guards.py`, `timeline_commit_auth.py`, `timeline_commit_execution.py`, `store.py`, `server.py` and `v33_manifest.py`.

RN-4 is an `S` "missing safety refusal" diagnosis in exactly the code Plan 89 is changing. Its failing line, `test_timeline_history_assembly.py:296-302`, exercises the cold "D88b memo".

**Change:**
- RN-4, RN-5 and RN-8 depend on Plan 89 landing.
- RN-4 first asks Plan 89 or Plan 77 whether the refusal was removed on purpose (green skill 3A step 4: a failure in an active lane's files goes to that lane).
- RT-1 and RT-2 re-check once Plan 89's `v33_manifest.py` change lands.
- inputs.md:92 says RN-4 "start[s] after [Plan 77] lands", but tasks.md RN-4 depends only on RS1. Reconcile the two.

### 1.6 D17 is already decided (should-fix)

astrid-dev #1507 carries the comment "Owner decision, 23 November 2026: the first option. Keep the Runtime starter tracks as published, and have the App accept exactly the authenticated V1/A1 starter shape." It is labelled `plan:77` and `release:16`, and stays open for the App work.

**Change:**
- Delete D17.
- RT-3 is a stale test, and its source is that owner comment.
- RT-3 depends on nothing beyond GM-0 and the gate. Move it into phase 1, since it is 39 IDs for 0.5 days.
- AP-14's `:3690` "empty bootstrap" Direct Journey failure is very likely the App half of #1507. That half belongs to Plan 77: `release/15/plan-77-r7` changes `bootstrapInitialization.ts`. Check it before dispatching AP-14.

### 1.7 D20 rejects a mechanism the Runtime already has, and Plan 38 uses it (should-fix)

- `tests/lanes.py:37` registers `needs_real_pidfd`, described as "only the seccomp sandbox-process-control job deselects it".
- `tests/seccomp/container-entrypoint.py:73` deselects it, and the seccomp README describes this as by design.
- About a dozen files already carry the marker, for example `test_native_custody.py:654` and `test_linux_process_binding.py:16`. The tests run for real in `unit` on ubuntu, so nothing is hidden.
- Plan 38's L1 adds exactly this marker to `tests/test_linux_runtime_boundary_native.py`, which is 4 of RT-8's 18 IDs.

**Change:** D20 should recommend that the owner rule this an allowed use of the existing by-design marker. The rule-4 "no deselect list grows" concern does not apply, because the tests still run in `unit`. RT-8 becomes an `N` card of about 0.5 days, and the 4 IDs Plan 38's L1 owns are left to it. The sandbox-only conditional refusal assertions D20 proposes are more code, and are themselves a test-weakening risk.

### 1.8 RT-9 invents an App pin in the Runtime (should-fix)

RT-9 says "CI checks the App out at its pin". The Runtime has no App pin; `tests/astrid-agent.pin` is its only pin. Adding one creates a circular producer pin, because the App already pins the Runtime in `runtime.lock.json`. The test (`test_p2_commit_phase_capture.py:62`) tests the App's own `scripts/testing/sitecustomize.py`.

**Change:** move the test to the App, or retire it under D12. Do not add a pin. The ambiguity pass's Q8 asks the same question.

### 1.9 The quarantine renewals as worded fail their own guards (should-fix)

- **Runtime (D15):** `tests/lanes.py:298` rejects `expiry <= today` or `expiry > today + 14`. Renewing "to 15 December" passes only on a run dated 1 December, and the old entries already fail on 1 December. A PR merged on 25–30 November with 15 December fails `tests/test_skip_registry.py:52` on its own CI.
- **App (D14):** `validateExceptions` uses `daysLeft < 0` (`check-known-failures.mjs:130-132`), so 8 December is valid from 24 November.

Other problems with D14 and D15:
- D14 calls the change a "one-line" PR, but it edits four entries.
- Its sentence "The owner becomes this plan's accountable session" is garbled.
- Both renewals go into `release/15/main` at Release 15's freeze, so they need the Release 15 Lead.
- `main` has the same expiries in both repositories: Runtime `5120462` (nine entries) and App `e0da794` (four).
- `check:known-failures` runs first in `npm run test:app` (`package.json:32`). When it fails, Vitest never runs, so the App loses all 21,474 test results, not one check.

**Change:**
- Word D15 as "at most 14 days after the day it merges".
- Split D14 and D15 out as decisions needed now. D14's renewal has to merge by 25 November; the plan cannot wait for D12–D27.
- Name the Release 15 Lead as gatekeeper.
- Say what happens to `main`.

### 1.10 No row owns the Runtime's 19 quarantined IDs (blocking)

D15 says "unless their cards land first", and Completion says each quarantine holds at most 10. No tasks.md row owns:
- #805, 14 IDs: `runtime-domains-*`, `second-client-core`, `stage1-runtime-contract` and `timeline-clip-replacement` (10);
- #806 (2), #807 (1) and #809 (1);
- #910, which row-map.md:171 maps to an "RT-14" that does not exist in tasks.md. tasks.md's RT-14 is CI-7.

row-map.md:224 proposed RT-02 for these, but it was dropped. GM-P1's scope ("the candidate test files (deletions and refusal tests only)") excludes `tests/lanes.py`, so even its retirement of `test_snapshot_legacy_certification.py`, which holds 2 of the quarantined IDs, cannot remove the entry.

**Change:** add `tests/lanes.py` (`DECLARED_XFAILS`, the cap `MAX_DECLARED_XFAIL_TESTS`) to GM-P1, plus `nightly.yml`'s historical-archive step for D25's certification retirement. Have GM-P1 sort the #805, #806, #807 and #809 entries under D12 before 1 December. Most of them are tests of retired writers that return 410. That likely brings the count from 19 to 10 or fewer, and makes most of D15's renewal unnecessary. #808 is Plan 38's.

### 1.11 D22 hands K4 to a plan that has no such card (should-fix)

Plan 31's RL-1b (`plans/31-.../tasks.md:22`, `:67-78`) checks the manifest, the installer validation and ancestry. It reads no `ci/required-checks.json`, and no Plan 31 row checks that the required checks are green on each pinned commit.

**Change:** D22 needs Plan 31's acceptance, through its owner or a new row. Until then, put K4 under Waiting on, not under "drops the rows".

### 1.12 GM-7 puts the required-checks list in three homes (should-fix)

Plan 91's AG-2 creates a single astrid-dev `ci/required-checks.json` "in the schema Plan 39 will share" (Plan 91 tasks.md:65). The Release 14 record also uses one file. GM-7 creates one file each in the Runtime and the App (plan.md:90).

**Change:** GM-7 adds the Runtime and App entries to astrid-dev's file. That gives each fact one home, and Plan 31 reads it from astrid-dev.

### 1.13 D26, Waiting on and Run start are stale (should-fix)

`releases/16/run.md:7,19` names the Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`). Under that Lead, packet sessions have no network and run no hosted test (`run.md:21`, ruling 2). That conflicts with tasks.md "How work is proved", which assumes the card worker opens the PR and runs:
- `env/runtime-pytest.sh`, which fetches the Agent from GitHub;
- `env/app-test.sh`, which needs the npm registry;
- dispatches.

**Change:**
- Name the Lead in D26 and Waiting on.
- Copy Plan 91's split: packets post a ready-for-proof message, and the orchestrator runs every hosted and networked proof.
- GM-0 produces per-card ID lists, like Plan 91's `cards/*.tsv`, because packets cannot measure.

### 1.14 GM-0's cancellation hunt is already answered (minor)

Plan 91's AG-0 (`plans/91-.../evidence/release-15-514499de/README.md`, "What cancels started runs") traced the cancellations to manual cancels by the shared `@AstridPseudon` account. I checked App `d53685f3`: its E2E job check-run carries "The run was canceled by @AstridPseudon". The recent cancelled Runtime runs are PR concurrency cancellations by design (cancel-in-progress is true on PRs, `ci.yml:16-19`).

**Change:** GM-0 cites AG-0 and checks the annotations on the three 22 November Runtime runs only. Separately, ask the Release 16 Lead for the standing no-cancel ruling AG-0 asked for.

### 1.15 The v33 fence verdict holds; one sub-claim is imprecise (minor)

**Confirmed:**
- `require_ready` at `v33_lifecycle.py:297-300`;
- the caller at `service.py:996-1000`, which also refuses when the marker exists and no provider is registered;
- `provider_ready` at `:303-309`, called from `service.py:3211`;
- the App launch at `runtime_boundary.py:271`, which always passes `--authoring-profile astrid`;
- the neutral refusal at `daemon.py:316-320`.

**Imprecise:** inputs.md:31 says "only provider registration reaches `ready`". For an operator-owned activation, registration reaches `provider_verified`, and `astrid_runtime/operator_upgrade.py:461` then writes `ready`. Relocation also writes it (`v33_lifecycle.py:446`). The verdict, and RT-1's and RT-2's "register the provider" fix, stand.

**Change:** reword the sub-claim. Carry the rt-c1c2 open question that `runtime_protocol replace` (`cli.py:359-361`) builds a neutral `RuntimeDaemon` into RT-2, as a check that `replace` on a migrated realm is not a user path.

### 1.16 Smaller facts (minor)

- tasks.md:134: a Runtime PR into the plan branch does run all jobs (`ci.yml:8`; only `landing-reference` is conditional). But it runs three different Agent revisions: the pin, `ff40f2c6` (`ci.yml:38`) and `4866090e` (`:227`). D16's pin bump reaches neither hard-coded SHA, and "the plan branch follows the Agent" is untrue for those jobs. Say so, and leave the SHAs to Plan 38's E1.
- `ci.yml:7` and `nightly.yml:7` still push-trigger on `release/14/plan-39`. Adding `release/16/plan-39` there, the precedent Release 14 used, would make every batch merge run CI and Nightly with no dispatch (see 2.2).
- RS1 offers landing "or `release/15/main`". `landing-reference` refuses that: `ci.yml:523-526` and the App `test.yml:180` require `release/<same N>/…`. Remove the option.
- In the TSVs, `job` is a run-specific numeric job ID. Key the ceiling by job family names, as Plan 91's ruling 3 does (`run.md`, "never per shard").
- The estimate text says the prune and re-measure took "10–20 off, as they did for Plan 91". Plan 91's AG-P1 has not run: AG-0 only finished on 24 November, and its prune candidates grew to 392 IDs. That claim is unsupported.

## 2. Work that can be removed, merged or done more simply

### 2.1 Merge the comparator change into one card shared with Plan 91 (should-fix)

GM-1 and AG-1 change the same `sort_results` and `main`. AG-1 sits in the Plan 91 orchestrator's lane and has not started. Ask that orchestrator to take the whole `env/baseline-diff.py` change once: the gate exit, `missing` over all states, the inventory baseline and `--select`. GM-1 then keeps only `env/app-results-ids.mjs` and the ids format. Either way, AG-1 sits on Plan 39's critical path, and tasks.md:120 does not show it.

### 2.2 The gate cards are over-built (should-fix)

Plan 91 runs the comparison in the manager's lane, with no gate job in the workflows (`run.md:21`). GM-3 and GM-5 add a `gate` job to four workflows, plus a `job` input. Nothing says how a Runtime or App job obtains astrid-dev's `env/baseline-diff.py`; ambiguity-runtime Q3 asks the same.

**Change:** one manager tool, which can live in `env/`, does the gate for all three repositories:
1. fetch the run's job conclusions, where any non-success is NO-RESULT;
2. fetch the logs or JSON;
3. compare with the ceiling and the inventory.

Keep only the `tests` and `repeat` dispatch inputs, and add `tests` to `nightly.yml` too, because every RN proof needs it. Optionally add `release/16/plan-39` to the push triggers so batch runs start themselves. This saves about 2–3 days and removes a cross-repository fetch from product CI. GM-6 then no longer needs GM-3 and GM-5.

### 2.3 Drop GM-8 (should-fix)

Packets cannot run it, since they have no network (1.13). The `tests` dispatch is the hosted proof. The green skill's own rule ("a recipe you have run twice by hand is the next tool card") argues against building it ahead of need.

### 2.4 Use Vitest at job level (minor)

Vitest is green on 21,474 tests. A job-level result plus the summary's test count catches a new failure and a lost test. A per-test JSON adapter for Vitest is optional; Playwright needs JSON. Reuse `direct-journey.yml:131-146` (`--reporter=json` with `PLAYWRIGHT_JSON_OUTPUT_NAME`) from the workflow command line instead of editing four configs.

### 2.5 Remove AP-5, and cut AP-3 to filing the issue (should-fix)

- **AP-5** has no failing IDs. It is contract research over 84 operations, so file it as an issue.
- **AP-3's vendoring** of the OpenAPI file into `runtime.lock.json` edits a producer pin that Plan 77's App branch also changes (`release/15/plan-77` touches `runtime.lock.json`). AP-2 can read `src/integrations/runtime/generated.ts`, which is already generated from the contract, plus a cited list. Keep only "file the Runtime issue", and fold that into AP-2.

### 2.6 Defer phase 4 (AP-18, AP-19, about 5 days) (should-fix)

Green does not require it. Make it conditional on AP-14 or AP-15 to AP-17 showing a dependence on test order. It also edits `three-products.spec.ts` and the harness, which Plan 77's App work and the Direct Journey cards share.

### 2.7 AP-20 is hygiene (minor)

It turns no red test green. Keep only the deletion of the dead `AUTHORIZED_NAMES` entries (`check-known-failures.mjs:25-29`), or drop the card.

### 2.8 Drop the astrid-dev plan branch (should-fix)

D11 and releases/16.md:80 cut `release/16/plan-39` in astrid-dev. Plan 91 has none, and its `env/` change (R16-P91-06) lands on astrid-dev `main`. Tools that live on a plan branch are not what workers' `cloud-setup.sh` installs, nor what the gate tool runs. Land GM-1, GM-6 and the `env/` tools on astrid-dev `main` through ordinary PRs.

### 2.9 Should Nightly be in scope? Yes, but provisionally (should-fix)

It is in the goal, and it is the only place the integration-marked tests run. But:
- it was measured only on `main` (1.3);
- 37 or more of its IDs are in Plan 89's live files (1.5);
- Plan 75's FS-6 ("the Runtime applies the effect list and re-compares nothing", about 91 re-check sites) will rewrite the history and re-check behaviour that RN-4, RN-5 and RN-8 test.

**Change:** keep Nightly in Included, but put its cards after Plan 89 and after a check with Plan 75. RN product-bug diagnoses go to those lanes as issues rather than fixes here.

## 3. Sequencing and dependencies

### 3.1 Phase 2's dependency on RS1 is false and lengthens the critical path (should-fix)

Every phase 2 row depends on RS1. What they need is GM-0's re-measure, to start, and the sealed gate (GM-3, GM-5), to land. Plan 91 starts Waves A and B at AG-0 and lands them once AG-1 works; its RS1 reviews only the gate and two cards.

**Change:** RS1 reviews GM-1 to GM-5 and the prune list. Phase 2 cards depend on GM-0 to start and on the gate to land. The critical path becomes GM-0 → AG-1/GM-1 → GM-3/GM-5 → the last cause cards → GM-10 → R, with RS1 running beside it.

### 3.2 Missing dependencies (should-fix)

- **GM-P1 and RT-1** both drop the `neutral` variant in `test_timeline_reference_authority.py:service_case`. That is the same function, and neither depends on the other. Give it to RT-1, under GM-P1's ruled-deletion list, and remove it from GM-P1.
- **App cards and the comparator.** AP-1, AP-11 and AP-13 prove by ID (rule 5, "`baseline-diff.py` on base and head") but depend only on GM-0. They need GM-1 and GM-4, or GM-5, for an App comparison at all.
- **RT-10 and RT-1/RT-2.** RT-10 changes `tests/precut_realm_fixture.py` helpers. RT-1 and RT-2's 358 IDs come from that fixture's migration (`:173-176`). Name the functions each changes, or order them.
- **Plan 77 cards.** AP-17 changes the App save path, and AP-14 (`:3690`) is #1507. Both overlap `release/15/plan-77` and `plan-77-r7`, which touch `localSaveSession.ts`, `commitOutbox.ts`, `mountedFileDrop.test.tsx` and `bootstrapInitialization.ts`. inputs.md:92 says "No card here changes those product files". AP-17 does. Add "Plan 77 landing" to both, and consider giving AP-17 (#252, data loss on reload) to Plan 63 (dependable saving).
- **Plan 38.** RT-12 (`test_bootstrap.py::StaleOwnerTests`) is listed in Plan 38's F1. Four of RT-8's IDs are in Plan 38's L1. Exclude them, or depend on Plan 38.
- **RT-5 and other Agent fixes.** The Agent fixes land in `release/16/plan-91` and reach `release/16/main` only at Plan 91's RS1 or its end. Name the ref the Runtime pin moves to, and do not pin an unlanded plan-branch commit.
- **Plan 91's acceptance of D21.** D21 creates Agent cards in Plan 91, whose Run start covers only its listed tasks. That needs the Plan 91 orchestrator and the Release 16 Lead to accept it, and it is missing from Waiting on.

### 3.3 Seal the ceiling from more than one run where flips are unknown (should-fix)

GM-3 and GM-5 seal from one hosted run. The Runtime's CI showed the same failures on 7 runs, so one run is defensible there. The App's E2E and Nightly have no flip evidence. Seal from two runs (the union), or adopt Plan 91's moving-group rule, so a flip does not read as a regression on the first batch.

## 4. Owner decisions D11–D27

- **D13:** the Plan 91 and Plan 39 split was decided as Plan 91's D2 on 23 November. If the owner's open question is whether to split the Runtime from the App, D13 does not answer it. Restate it. My view: keep one plan, because the shared gate and prune justify it, but give each repository its own landing.
- **D14 and D15:** see 1.9 and 1.10. Prefer retiring the quarantine entries under D12 over renewing them. At a second expiry, remove the mark and put the ID on the ceiling: the ceiling is meant to absorb this. Decide this before sealing. An ID sealed as XFAIL counts as a pass, so it would read as a regression when its mark is removed.
- **D16:** fine, but say it does not reach the two hard-coded SHAs. Each later bump is a merge, a load-bearing moment, so re-measure against the ceiling.
- **D17:** delete (1.6).
- **D20:** reverse (1.7).
- **D22:** needs Plan 31's acceptance (1.11).
- **D24:** fine. AP-3 shrinks (2.5).
- **D26:** stale (1.13). Also add a CI capacity rule.
  - The problem: every Runtime card PR runs full CI automatically, with three macOS jobs, so five workers mean five full runs at once. "At most two full runs at once per repository" (tasks.md:122) cannot be enforced as written. Plan 89's PRs are running full CI today, and Plan 91 shares the organisation's macOS runners.
  - The rule should say: open a card PR only when its focused proof is ready, push it once, and let the Lead set a cross-plan runner budget.
- **Missing decisions:**
  - the ceiling plus inventory question (1.1);
  - the quarantine to ceiling conversion (above);
  - who runs proofs under no-network packets (1.13);
  - the Nightly sequencing (2.9);
  - whether Direct Journey's three-products project is part of any gate (ambiguity-app Q4).

## 5. Estimate

- **The card sizes add up to about 77.5 days:** phase 1 about 23, with GM-2 unsized; phase 2 about 46.5; phase 3 about 3, plus the nights; phase 4 about 5.
- **The phase 2 range is below its own card sum.** "30–40" is under the 46.5 days of phase 2 cards, and the "10–20 off" rests on the unsupported Plan 91 claim (1.16).
- **Hidden failures will surface.** About 1,105 of the 1,469 Runtime rows are setup ERRORs, so 358 or more tests have never run their assertions. RT-1 and RT-2 will expose failures beneath them. The green skill's own example is one collection error that hid about 24,500 tests.
- **Elapsed time:** "4–5 weeks" ignores the waits on Plan 89 and Plan 77, on AG-1, on Plan 91 landing Agent fixes in `release/16/main`, on the cut of `release/16/main`, on the shared macOS runners, and on two review rounds.

Removing GM-8, AP-5, most of AP-3, phase 4 and RT-8's extra work saves about 9 days, and making RS1 non-blocking saves about a week elapsed. I would still estimate 60–80 days and 6–8 weeks elapsed.

## 6. Planning skill and run contract

- **Per-card reviews (should-fix).** The run contract's per-card rule requires a high-judgment review for the S cards (RT-14, RT-15, RN-4, RN-5, AP-17) and for any change to what the product accepts or refuses (RN-4 may add a refusal). The plan names none.
- **Deletions inside fix cards (should-fix).** These cards delete or deduplicate tests without going through GM-P1's listed, `X`-read deletion:
  - RT-1's `neutral` params (51 IDs);
  - RT-17's "spec dedup";
  - RN-8's "may be redundant".

  Route each deletion through GM-P1's list, or give the card the same proof.
- **Overlapping scopes need dependencies (minor).** The tasks template says "tasks with overlapping scopes need a dependency", but AP-3's scope is a whole directory (`tests/e2e/fake-runtime/`) and overlaps AP-4. Name `path:symbol`.
- **A proof that is a review (minor).** GM-P1's proof includes "an `X` reviewer reads the list". The green skill requires this, and Plan 91 does the same, so it is acceptable. But it is a review inside a card proof, which the planning skill discourages. Keep the evidence part, the citations and the passing covering tests, as the proof.
- **The critique's home (minor).** inputs.md:51 points the critique at `evidence/critique.md`. Record this file there, and answer each finding in Challenge.
