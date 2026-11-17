# All three mains green

**Project:** All three mains green

**Goal:** Every CI workflow on Agent, Runtime and App `main` is green and stays green: root causes fixed (never a loosened test), one strict-xfail quarantine rule with an owner and an expiry, a nightly report of new red, and releases that need every required check green on each pinned commit (through Plan 31's `release-contract`).

**Status:** active

**Owner:** Release 14 Lead (`session_011EzfW3Zy19ncNecpQnKb7D`), by [packet dispatch](../../releases/14/run.md)

**Estimate:** 22–31 (8–11 elapsed): phase 1 6.5, phase 2 13–21, phase 3 3.5

**Waiting on:** a manager; G1 redone on `release/14/main` ([Release 14 scope](#release-14-scope)); Plan 38 for the custody tests; Plan 31 RL-1b for K4, which is Release 15's

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). A red check on `main` should mean a new regression. Today it means nothing, because every full CI workflow on Agent, Runtime and App `main` has been red for weeks.

## Outcome and scope

Every CI workflow that runs on a push to `main`, in astrid-agent, astrid-runtime and astrid-app, is green, and it stays green:
- **Green.** Each failing job is fixed at its root cause ([triage](inputs.md#root-cause-triage)), never by loosening an assertion to match a bug. A test changes only when the behaviour it checks changed on purpose, and the task card names the commit or contract that changed it.
- **Kept green.** Hannah turns on the [required checks](tasks.md#required-checks) for each `main`. One [quarantine rule](#quarantine-rule), the same in all three repositories, is the only way a known failure may be tolerated. A nightly report names any new red within a day.
- **Releases.** The release rule changes from "no new red against `main`" ([Release skill](../../skills/astrid-dev-release/SKILL.md)) to "every required check is green on each pinned commit". The check lives in [Plan 31](../31-releases-from-astrid-dev/plan.md)'s `release-contract` job as one more rule on the release record. It is not a second gate.
- **Structural (phase 4, from [Release 12](inputs.md#release-12-structural-evidence)).** The causes that kept the mains hard to read are removed too. Each App three-products test owns its seed, so the journey runs in parallel and in any order, and CI shuffles it. An expected failure names the step and error it expects. Every `main` and `int` run stores per-test results, so a candidate is compared with the published `main` without reruns, and a cancelled or truncated shard turns the run red. Once the mains are green, feature work lands on `main` through ordinary CI, so a release candidate is `main` plus a short, listed set of fixes; the mains are frozen from cut-off to publication, and the release record states both. Each Agent code and harness smell Release 12 found gets a fix and a guard for its class. Upgrade safety of installed state, found after Release 12 shipped (the Release 1 → 12 Hivemind incident), is [Plan 09 phase 2](../09-install-and-update-confidence/plan.md#phase-2-upgrade-safe-installed-state), not this plan.

**Included:** the CI workflows that run on push to `main`:
- Agent: `CI`, `Lanes`, `Chat service` and `Windows task host journey`;
- Runtime: `CI`, plus `Nightly` on its schedule;
- App: `Tests`, `Lanes` and `E2E`, plus `Direct Journey` on its schedule.

It also includes astrid-dev's worker environment for the Runtime and App (G0), the quarantine guard in each repository, and the nightly report. Phase 4 adds the three-products journey's structure, per-test result artifacts and their comparison, the release record's scope and freeze sections, and the Agent code and journey-harness fixes its rows name.

**Not included:**
- the custody and host-spawn tests [Plan 38](../38-one-process-identity/plan.md) owns (its [test inventory](../38-one-process-identity/tasks.md#test-inventory)). This plan's tasks skip them, and its completion counts them green only when Plan 38 lands them;
- the Agent's `journey.yml` release receipts (push `int/r1` only, owned by the Release skill);
- GPU and live lanes (Plan 34);
- product features. A real product bug found here gets its own fix task. When it is large, it goes to an issue and is quarantined under the rule.

**Replaces:** the "full CI health is a separate project" deferral in [Plan 29](../29-update-and-release/inputs.md#planning-evidence) (decision 6), Plan 29's unfinished UR-0 ("why App main is red"), and the strategy row "Green mains (proposed): a Release rule plus a one-off fix batch". [Plan 30](../30-update-everywhere/plan.md) inherited the same deferral through Plan 29's shared evidence.

## Release 14 scope

Added on 16 November 2026, when the owner brought this plan into [Release 14](../../releases/14.md). The plan was written on 9 November, two releases ago. Where this section and the text around it differ, this section governs until G1 is redone and the task table is corrected from it.

**What is in.** Phases 1 to 3, and from phase 4 only SF3a to SF3c: results stored per test, a comparison without re-runs, and shards that finish. The rest of phase 4, and K4 and K5, which wait for Plan 31, are [Release 15](../../releases/15.md)'s.

**Where it lands.** `release/14/plan-39` in each repository, then `release/14/main`. This replaces `int/39-green-mains`. Until Release 14 is published, "green `main`" in this plan means green `release/14/main`; publishing fast-forwards each `main` to it, and the required checks then apply to `main` as well.

**Done for Release 14.** Every merge-tier and release-tier check in [Required checks](tasks.md#required-checks) is green on the head of `release/14/main` in Agent, Runtime and App three nights in a row, the merge tier is required on pull requests into it, and each repository's quarantine holds at most ten entries, all within age.

**What it leaves alone.** Tests in [Plan 55](../55-local-speed/tasks.md)'s test inventory (the VibeComfy pack, the ComfyUI target, delivery, the generic host and SDK invocation) until its fast lane has landed, because that plan rewrites what they test: a failure there gets a row and waits. Plan 38's tests, as before. Rented-machine defects that no failing test shows: those issues were filed here during Release 13 and moved to Release 15 on 16 November.

### Measured on 16 November

Read from the latest completed runs on `release/14/main`. Two of the Agent's eight unit shards and three of its five failing lane jobs were sampled, from the last 1,500 lines of each log, so the Agent's numbers are a floor. G1 replaces this table.

| Repository | Failing | What the logs show |
| --- | --- | --- |
| Runtime | 5 of 10 `CI` jobs | `unit` on Ubuntu: 77 failed, 8,440 passed, 1,010 errors, the error count of the 9 November triage unchanged. At least 718 of the errors are causes R-a, R-b and R-c: no Agent checkout, a hard-coded scratch path, and `git archive` on a shallow checkout. |
| Agent | 10 of 16 `CI` jobs, with all eight unit shards; 5 of 6 `Lanes` jobs; both `Windows task host journey` jobs | Collection no longer aborts (A-a is fixed), so real failures show: 250 failed and 160 errors in shard 7, 98 failed in shard 8. They cluster: 62 are one copy-only upgrade-boundary error, 25 one `KeyError: 'macos-15'`. The lint gate fails because findings fell ([#742](https://github.com/banodoco/astrid-dev/issues/742)). |
| App | all six `E2E` jobs; 2 of 5 `Lanes` jobs; `Tests` is green | Three `E2E` jobs share one cause: the fake Runtime has no route for `GET /api/runtime/packs/inventory`. `chrome-export` gets `retired_route` from it. |

Since the triage: A-a and PE1 are fixed, and vitest runs on pull requests into a release branch (part of K1c). R-a, R-b, R-c, R-f, A-c and A-i are still present on `release/14/main`. An Agent run takes about two hours, jobs waited 30 to 68 minutes to start, and a new push cancels the run in flight.

### What changes in the order

1. **Store results first.** SF3a moves from phase 4 to the start. The Runtime runs `pytest -q`, with no per-test lines, so its runs cannot be compared by test at all; the Agent prints `-rA` and uploads only durations. Every later measurement, and every worker's proof, reads the stored results.
2. **Gates that parallel work can pass.** The Agent's Ruff and mypy gates fail when findings fall as well as when they rise. Two pull requests that each remove findings then break each other once both merge. Before the fan-out, the gate fails on a rise only, and the baseline is rewritten once per batch on the plan branch.
3. **One full run per batch, not per card.** A worker proves a card with its focused tests and the stored results. The manager merges a batch into the plan branch and waits for one full run, because a full run per card would queue fifteen two-hour runs on runners that are already full.

### How the work fans out

The 35 to 47 worker-days do not divide by the number of workers, because four steps cannot be shared out: the two measurements, the review stop, and three consecutive green nights. Between them the work is one cause to one worker.

| Wave | Workers | Work | Elapsed |
| --- | --- | --- | --- |
| 0 | 1 to 3 | G0 and G1 redone on `release/14/main`; SF3a in the three repositories; GL, the gate change above | about 1 day |
| 1 | about 10 | The wiring cards, all independent: RE1 to RE4 in the Runtime, AE2 in the Agent, K1a to K1c, and AE1 and PE1 confirmed fixed | 1 to 2 days |
| stop | 1 | G2, then the one review round RS1 | about 1 day |
| 2 | 10 to 15 | One worker per cause from G2's clusters, the three repositories at once, with the Windows journey (AT4) and the App's fake Runtime (PT2) among them; K2, K3, SF3b and SF3c beside them | 4 to 7 days, set by the Agent's count |
| 3 | 1 | Three green nights, then the final review R | 3 days at least |

The rows in each wave are listed in [tasks.md](tasks.md#release-14-waves). That is 10 to 14 days elapsed, as the [estimate](tasks.md#estimate) says. More workers shorten wave 2 only; more CI capacity shortens every wave. The rule in the estimate still holds: if G2 shows more than 60 distinct Agent causes, the manager splits AT1 and re-estimates before going on.

### Issues

Filed against this plan and in scope, each to be given a task row at G1: the red release branch ([#742](https://github.com/banodoco/astrid-dev/issues/742)); 133 timeline tests that assert one hard-coded Runtime commit ([#637](https://github.com/banodoco/astrid-dev/issues/637)); the stale structure baseline ([#647](https://github.com/banodoco/astrid-dev/issues/647)); shards that never finish ([#614](https://github.com/banodoco/astrid-dev/issues/614)); stale or environment-dependent fixtures ([#615](https://github.com/banodoco/astrid-dev/issues/615), [#626](https://github.com/banodoco/astrid-dev/issues/626)); tests that fail with no cause recorded yet ([#639](https://github.com/banodoco/astrid-dev/issues/639), [#636](https://github.com/banodoco/astrid-dev/issues/636), [#621](https://github.com/banodoco/astrid-dev/issues/621)); a test no CI job can run ([#606](https://github.com/banodoco/astrid-dev/issues/606)); the integration lane's unprovisioned checkouts ([#585](https://github.com/banodoco/astrid-dev/issues/585)); the 57-minute CPU journey ([#578](https://github.com/banodoco/astrid-dev/issues/578)); the lint and type findings Release 13 added and the parked type fixes ([#613](https://github.com/banodoco/astrid-dev/issues/613), [#633](https://github.com/banodoco/astrid-dev/issues/633)); and the deferred engine-lane items ([#612](https://github.com/banodoco/astrid-dev/issues/612)). The live-scene tests that run in no lane ([#734](https://github.com/banodoco/astrid-dev/issues/734)) are shared with the release's standing lane.

## Quarantine rule

A test that cannot be fixed in its task may be quarantined only like this:
- it gets a **strict** expected-failure mark (pytest `xfail(strict=True)` through each repository's existing declared-xfail registry, or the App's `skipRegistry.mjs` and `check-known-failures.mjs`), never a skip. When the test starts passing, CI fails until the mark is removed;
- the entry carries an issue link, an owner and an expiry date at most 14 days out;
- each repository's guard test fails CI on a missing field, an expired entry, or more than 10 entries per repository;
- the nightly report lists every quarantined test with its age.

The Runtime (`tests/lanes.py` `DECLARED_XFAILS`, `SKIP_REGISTRY`) and the App (`config/testing/skipRegistry.mjs`, `scripts/quality/check-known-failures.mjs`) already have registries. The Agent has `tests/test_skip_policy.py` and the lane xfail rule in `tests/lanes.py`. Each task extends these and adds no new mechanism.

## Existing work and decision

The work reuses each repository's own registry and guard, Plan 38's Runtime worker setup (W0), Plan 31's App worker setup (RL-0) and `release-contract` job, and the Agent's mypy and Ruff baselines. The evidence, the ranked causes, the alternatives and the challenge are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

- **Queued to start after release 12 is published.** Release 12 already clears several Agent causes: the Ruff import-sort debt, the Windows POSIX-filesystem custody refusal, and the wheel-smoke `entries.py` import, and likely the ESBUILD collection error. So G1 re-measures every cause on the release-12 heads before any fix starts.
- **Phase 1, CI environment and wiring** (G0 to G2, then the `RS1` review stop). Most of the red is here: about 1,000 Runtime errors and every Agent shard aborting at collection. Fixing it first shows the real test failures it hides.
- **Phase 2, test-by-test**, by cause, with the three repositories in parallel. Each cause is one or a few small N tasks that many workers can take at once.
- **Phase 3, keep it green:** the required checks, the nightly report and the release rule. Then the final review.
- **Phase 4, structural fixes from Release 12**, beside phases 2 and 3: most rows start after RS1, and SF3a after G2. The final review R covers them. SF4 and SF5 change the release rules, so they wait for the Release skill owner and an advisor review, and apply from the first release after the mains are green.

Plan 38 runs at the same time. Its tests are excluded here, and its W0 and Plan 31's RL-0 are reused, not rebuilt ([tasks](tasks.md)).

## Interfaces and handoff

- **Consumes:**
  - each repository's `main` at the release-12 heads, recorded in G1;
  - the cross-repository pins (`runtime.lock.json`, the Runtime's `tests/astrid-agent.pin`, the App's `runtime.lock.json` and `config/astrid-cli-surface/vendor.lock.json`);
  - Plan 31's release record and `release-contract` job.
- **Produces:**
  - green `main` workflows;
  - a list of required checks per repository, for the owner to set;
  - one quarantine guard per repository;
  - `scripts/ci_red_report.py` and its nightly workflow in astrid-dev;
  - the `release-contract` rule "every required check on each pinned commit is success";
  - the Release skill's new rule text;
  - per-test result artifacts on each `main` and `int` run, compared by `env/baseline-diff.py`;
  - the release record's `## Candidate scope` and `## Freeze` sections, checked by `release-contract`.

## Completion

- Each workflow listed above has a green run on the final head of its `main`, three nights in a row, with any quarantine entries listed and within age.
- Plan 38's tests are counted only once Plan 38 has landed them.
- **Negative cases:**
  - an expired quarantine entry, or a strict xfail that starts passing, turns its repository red;
  - a release record pinning a commit whose required check failed is refused by `release-contract`;
  - a three-products test that reads another test's state fails in the shuffled run;
  - a release record over the scope limit without the owner's sign-off, or whose `main` moved after its cut-off with the commits unlisted, is refused by `release-contract`.
- **Limits:** green on GitHub-hosted runners only. GPU, live and Pinokio lanes are out of scope. Branch protection is Hannah's setting, and the plan can only list and check it.
