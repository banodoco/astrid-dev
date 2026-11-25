# Runtime and App main green

**Project:** Runtime and App main green

**Goal:** Every CI workflow on the Runtime's and the App's `main` is green and stays green, so a red check means a new regression; the Agent's share is [Plan 91](../91-agent-main-green/plan.md).

**Status:** queued

**Owner:** Unassigned

**Estimate:** 64–78 engineering days, about 6–8 weeks elapsed with five workers: phase 1 (the quarantine, the baselines, the prune pass, the large causes) 20–24; phase 2 (the middle and the long tail, CI and Nightly) 40–48; phase 3 (kept green) 4–6

**Waiting on:** now, the owner's D14 and D15 (the App's quarantine entries expire on 25 November, the Runtime's on 1 December); before start, the owner's confirmation of the other open decisions in [inputs.md](inputs.md#owner-decisions) (D11 and D17 are decided) and an orchestrator and manager under the Release 16 Lead; Plan 91's comparator change (astrid-dev #1833) and its acceptance of D21's Agent cards; Plan 31's acceptance of D22; Plans 89 and 77 landing ([base choice](inputs.md#source-identities)).

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). A red check on `main` should mean a new regression. Today the Runtime's CI and Nightly, and the App's E2E, Lanes and Direct Journey, are red on every run, and the same failures repeat on every run.

## Outcome and scope

**Rebuilt on 24 November 2026.**
- **The split.** The owner split the Agent's share into [Plan 91](../91-agent-main-green/plan.md) on 23 November.
- **The release.** She moved both plans to [Release 16](../../releases/16.md), built on `release/15/main` ([D11](inputs.md#owner-decisions)).
- **The re-measure.** This plan was re-measured on the `release/15/main` heads ([evidence](evidence/release-15-measure/README.md)), and checked by an independent [critique](evidence/critique.md) and two ambiguity passes.
- **The old rows.** Every row of the Release 14 plan was carried, closed or dropped ([row map](evidence/release-15-measure/row-map.md)). The Release 14 plan, tasks, inputs and handover are kept in [evidence/release-14-record](evidence/release-14-record/plan.md).

**Measured on 23–24 November** (Runtime `24e2c929`; App `3f5da385`, the App's last head that ran):

| Repository | Workflow | Result |
| --- | --- | --- |
| Runtime | `CI` | 5 of 9 jobs fail: 508 distinct failing tests, the same on 7 runs, and inherited from `main`. 358 of them come from one cause: a 1 November safety check (`v33_lifecycle.py:300`) correctly blocks tests that never register a Timeline provider. About three quarters of the failing rows are setup errors, so more failures lie beneath them |
| Runtime | `Nightly` | All 15 runs on `main` from 12 to 23 November failed, with 152 distinct tests on `main` `5120462`. It has never run on `release/15/main`, because a schedule fires only on `main` |
| App | `Tests` | Green (21,474 tests). It goes red on 26 November, when four quarantine entries expire, and then no Vitest result is reported at all ([D14](inputs.md#owner-decisions)) |
| App | `E2E` | 85 failing of 649. About 44 come from the fake Runtime missing three routes the App now calls |
| App | `Lanes` | 2 failing: a missing browser install and a quick-journey test bug |
| App | `Direct Journey` | 6 of the last 7 scheduled runs on `main` failed |

**What changes:**
- **Cannot get worse, first.** Each repository gets a sealed baseline: one status line per test ID from two runs at the start, in `ci/runtime-baseline.txt` and `ci/app-baseline.txt`. Its FAILED lines are the ceiling, and its PASSED lines are the inventory, so a deleted test is caught as well as a new failure. Comparisons use `env/baseline-diff.py --strict`, through one gate tool that also turns any job without a result red. Only the orchestrator edits the baseline, and only to move what passed. The App's Playwright jobs gain per-test JSON results and an adapter, so the App can be compared by test at all.
- **Prune boldly, then fix.** The [support line](inputs.md#owner-decisions) (D12): only current behaviour, and updating from the previous published release, is supported. Tests of anything older are deleted with their citation, and duplicates are deleted naming the test that covers them. The Runtime has at least 31 known candidates, and most of its 19 quarantined IDs; the App helpers found none.
- **Green by cause.** One card per cause, routed N, X or S, under [Plan 91's triage rules](../91-agent-main-green/tasks.md#triage-rules), which this plan uses unchanged.
- **Kept green.** A nightly red report across the Agent, the Runtime and the App, and the Runtime and App entries in astrid-dev's one required-checks list, for the owner to turn on. One quarantine rule ([below](#quarantine-rule)) covers what must stay green meanwhile.

**Included:** the Runtime's `CI` and `Nightly`; the App's `Tests`, `E2E`, `Lanes` and `Direct Journey`; the gate tool, the App adapter and the nightly report in astrid-dev.

**Not included:**
- **The Agent,** which is [Plan 91](../91-agent-main-green/plan.md). Where a Runtime or App failure is an Agent bug, the card hands it to Plan 91 ([D21](inputs.md#owner-decisions)).
- **The release rule** in `release-contract` (that every required check is green on each pinned commit), and the release record's scope and freeze sections. These belong with [Plan 31](../31-releases-from-astrid-dev/plan.md), once it accepts them ([D22](inputs.md#owner-decisions)). This plan provides their inputs: the required-checks entries and the green runs.
- **Other plans' tests:** the custody, bootstrap and host-spawn tests [Plan 38](../38-one-process-identity/plan.md) owns, and the Runtime's `darwin-native` job, which it replaces.
- **The three-products structure** (each test owning its seed, then shuffled runs). It is deferred unless the Direct Journey cards show that order matters.
- **GPU, live and Pinokio lanes; VibeComfy.**
- **Product features.** A real product bug found here gets its own card, or, if it is large, an issue and a visible ceiling entry the owner accepts.

## Quarantine rule

A test that cannot be fixed in its card stays visibly red on the ceiling. That is the default, and the ceiling absorbs what a quarantine would otherwise carry. Quarantine is only for a test that must stay green in a required check before its fix lands, and only like this:
- a **strict** expected-failure mark through the repository's existing registry: the Runtime's `tests/lanes.py` `DECLARED_XFAILS`, or the App's `config/testing/direct-journey-expected-failures.json`, checked by `scripts/quality/check-known-failures.mjs`. Never a skip. When the test starts passing, CI fails until the mark is removed;
- the entry carries an issue link, an owner and an expiry at most 14 days after the day it merges. At expiry the mark comes off and the ID goes on the ceiling, unless the owner renews it once, recorded on its issue;
- each repository's guard fails CI on a missing field, an expired entry, or more entries than its cap. The cap counts test node IDs (the Release 14 record's [D9](evidence/release-14-record/inputs.md#owner-decisions)) and only falls: the Runtime's is 19 today, and both repositories are at 10 or fewer at completion ([D15](inputs.md#owner-decisions));
- the nightly report lists every quarantined test with its age;
- an ID that is quarantined when a baseline is sealed is recorded as FAILED, not as passing.

## Existing work and decision

The approach is Plan 91's, applied to two repositories. It reuses:
- each repository's quarantine registry and guard;
- the Runtime's existing `-rA` and JUnit output in three of its jobs;
- `direct-journey.yml`'s Playwright JSON reporter;
- the Runtime's `needs_real_pidfd` marker;
- the comparator `env/baseline-diff.py`, as Plan 91 fixes it in astrid-dev #1833.

What the Release 14 run built on `release/14/plan-39` was never merged, and this plan ports none of it ([audit](evidence/release-15-measure/audit.md)). The evidence, the alternatives and the critique are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

The task list and critical path are in [tasks.md](tasks.md):
1. **Now: the quarantine.** The expiring entries are sorted before they turn the mains red (GM-Q).
2. **Phase 1: the baselines, the prune pass and the large causes.**
   - Cut the plan branches, bump the Runtime's Agent pin, and re-measure twice.
   - Add per-test reporting where it is missing, the gate tool and the dispatch inputs, and seal each baseline.
   - The prune pass runs beside them, with the four largest causes: the Runtime's v33 provider fixtures (358 tests) and commit-crash fixture (32), and the App's fake Runtime routes (about 44) and missing browser installs.
   - The review stop RS1 covers the baselines before anything lands.
3. **Phase 2: the middle and the long tail,** by cause, the two repositories in parallel. Cards start after the re-measure and land once their repository's baseline is sealed. Those in files Plans 89 and 77 are changing wait for those plans to land.
4. **Phase 3: kept green.** The nightly report, the required-checks entries, and three green nights per workflow on one frozen head. Then the final review R.

Nothing starts until the owner confirms the decisions and the Release 16 Lead names who runs it. Recording this plan authorizes no implementation.

## Interfaces and handoff

- **Consumes:**
  - each repository's `release/15/main` head, recorded at GM-0, and later `release/16/main`;
  - the cross-repository pins: the Runtime's `tests/astrid-agent.pin`, and the App's `runtime.lock.json`, `config/astrid-cli-surface/vendor.lock.json` and `public/install-manifest.json`. This plan moves only the first;
  - Plan 91's `env/baseline-diff.py` change (astrid-dev #1833), and its `ci/required-checks.json` in astrid-dev (AG-2).
- **Produces:**
  - green Runtime and App workflows;
  - `ci/runtime-baseline.txt` and `ci/app-baseline.txt`, with no FAILED line at the end, or only entries the owner accepted;
  - per-test JSON from every App Playwright job, and `env/app-results-ids.mjs`;
  - `env/run-gate.py`, the gate tool for any repository;
  - `tests` and `repeat` dispatch inputs on the Runtime's and the App's test workflows, `nightly.yml` included;
  - the Runtime and App entries in astrid-dev's `ci/required-checks.json`, for the owner to set and for Plan 31's `release-contract` to read;
  - `scripts/ci_red_report.py` and its nightly workflow in astrid-dev, covering the Agent too.

## Completion

- Each workflow listed in Included has a green run on one frozen head of `release/16/plan-39`, on three different nights, then one green run on `release/16/main` after the plan branch lands.
- Each baseline holds no FAILED line, or only entries the owner accepted, each with its issue. Each quarantine holds at most 10 IDs, all within age.
- The nightly report has run for three nights and named any new red.
- **Negative cases** (each shown by an injected failure on a scratch branch):
  - each of these turns the gate red: a test that passed in the baseline and fails on the candidate, a new failing test, a deleted test, and a job that was cancelled or truncated;
  - an expired quarantine entry, and a strict xfail that starts passing, each turn their repository red;
  - the App's fake Runtime check fails when the App calls a route the fake does not serve.
- **Limits:** GitHub-hosted runners only. Branch protection is the owner's setting; this plan lists the checks and shows them green.
