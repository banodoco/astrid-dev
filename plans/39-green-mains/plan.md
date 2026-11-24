# Runtime and App main green

**Project:** Runtime and App main green

**Goal:** Every CI workflow on the Runtime's and the App's `main` is green and stays green, so a red check means a new regression; the Agent's share is [Plan 91](../91-agent-main-green/plan.md).

**Status:** queued

**Owner:** Unassigned

**Estimate:** 60–80 engineering days, about 4–5 weeks elapsed with five workers: phase 1 (the gates, the prune pass, the large causes) 20–26; phase 2 (the middle and the long tail, CI and Nightly) 30–40; phase 3 (kept green) 6–8; phase 4 (the three-products structure) 4–6

**Waiting on:** the owner's written confirmation of D12–D27 in [inputs.md](inputs.md#owner-decisions) (D11 is decided); a Release 16 Lead or an accountable session named under D26, and a manager; Plan 91's AG-1 for the shared comparator in `env/baseline-diff.py`; Plans 77 and 89 landing in the Runtime and the App ([base choice](inputs.md#source-identities)).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). A red check on `main` should mean a new regression. Today the Runtime's CI and Nightly, and the App's E2E, Lanes and Direct Journey, are red on every run, and the same failures repeat on every run.

## Outcome and scope

**Rebuilt on 24 November 2026.** The owner split the Agent's share into [Plan 91](../91-agent-main-green/plan.md) on 23 November and moved both plans to [Release 16](../../releases/16.md), built on `release/15/main` ([D11](inputs.md#owner-decisions)). This plan was re-measured on the `release/15/main` heads ([evidence](evidence/release-15-measure/README.md)), and every row of the Release 14 plan was carried, closed or dropped ([row map](evidence/release-15-measure/row-map.md)). The Release 14 plan, tasks, inputs and handover are kept unchanged in [evidence/release-14-record](evidence/release-14-record/plan.md).

**Measured on 23–24 November** (Runtime `24e2c929`, App `3f5da385`, the App's last head that ran; its next head `d53685f3` only moved pins, and every job on it was cancelled before it started):

| Repository | Workflow | Result |
| --- | --- | --- |
| Runtime | `CI` | 5 of 9 jobs fail: 508 distinct failing tests, the same on 7 runs, and inherited from `main`. 358 of them come from one cause: a 1 November safety check (`v33_lifecycle.py:300`) correctly blocks tests that never register a Timeline provider |
| Runtime | `Nightly` | All 15 runs on `main` from 12 to 23 November failed: 152 distinct tests. It never runs on a release branch by itself |
| App | `Tests` | Green (21,474 tests). It goes red on 26 November, when four quarantine entries expire ([D14](inputs.md#owner-decisions)) |
| App | `E2E` | 85 failing of 649. About 44 come from the fake Runtime missing three routes the App now calls |
| App | `Lanes` | 2 failing: a missing browser install and a quick-journey test bug |
| App | `Direct Journey` | 6 of the last 7 scheduled runs on `main` failed |

**What changes:**
- **Cannot get worse, first.** Each repository gets a ceiling: the failing (job, id) pairs at the start, in `ci/runtime-ceiling.tsv` and `ci/app-ceiling.tsv`. A batch run is compared with it by `env/baseline-diff.py`, and a new failure, a new failing test or a missing test blocks. Only the manager edits the ceiling, and only to remove what passed. The App's tests gain per-test JSON results and an adapter, so the App can be compared by test at all.
- **Prune boldly, then fix.** The [support line](inputs.md#owner-decisions) (D12): only current behaviour, and updating from the previous published release, is supported. Tests of anything older are deleted with their citation, and duplicates are deleted naming the test that covers them. About 31 Runtime candidates are known ([prune candidates](evidence/release-15-measure/rt-tail-nightly.md)); the App helpers found none.
- **Green by cause.** One card per cause, routed N, X or S, under [Plan 91's triage rules](../91-agent-main-green/tasks.md#triage-rules), which this plan uses unchanged.
- **Kept green.** A nightly red report across the Agent, the Runtime and the App; a list of required checks per repository for the owner to turn on; and one quarantine rule ([below](#quarantine-rule)).

**Included:** the Runtime's `CI` and `Nightly`; the App's `Tests`, `E2E`, `Lanes` and `Direct Journey`; the comparator, adapters and nightly report in astrid-dev; the App's three-products structure (phase 4).

**Not included:**
- the Agent, which is [Plan 91](../91-agent-main-green/plan.md). Where a Runtime or App failure is an Agent bug, the card hands it to Plan 91 ([D21](inputs.md#owner-decisions));
- the `release-contract` rule that every required check is green on each pinned commit, and the release record's scope and freeze sections, which are [Plan 31](../31-releases-from-astrid-dev/plan.md)'s job ([D22](inputs.md#owner-decisions)). This plan provides their inputs: the required-checks lists and green runs;
- the custody and host-spawn tests and the Runtime's `darwin-native` job, which [Plan 38](../38-one-process-identity/plan.md) replaces;
- GPU, live and Pinokio lanes; VibeComfy;
- product features. A real product bug found here gets its own card, or, if it is large, an issue and a visible ceiling entry the owner accepts.

## Quarantine rule

A test that cannot be fixed in its card stays red on the ceiling by default. Quarantine is only for a test that must run green in a required check before its fix lands, and only like this:
- a **strict** expected-failure mark through the repository's existing registry: the Runtime's `tests/lanes.py` `DECLARED_XFAILS`, or the App's `config/testing/direct-journey-expected-failures.json`, checked by `scripts/quality/check-known-failures.mjs`. Never a skip. When the test starts passing, CI fails until the mark is removed;
- the entry carries an issue link, an owner and an expiry at most 14 days out. Renewing it once needs the owner's go, recorded on the entry's issue;
- each repository's guard fails CI on a missing field or an expired entry, and on more entries than its cap. The cap counts test node IDs (the Release 14 record's [D9](evidence/release-14-record/inputs.md#owner-decisions)). It is a ratchet: the Runtime's is 19 today, and both repositories are at 10 or fewer at completion ([D15](inputs.md#owner-decisions));
- the nightly report lists every quarantined test with its age.

The App's `config/testing/skipRegistry.mjs` (9 declared skips) is not a quarantine; its entries gain an owner and a reason in AP-20.

## Existing work and decision

The approach is Plan 91's, applied to two repositories, and it reuses what each already has:
- the Runtime prints `-rA` and uploads JUnit in three of its jobs;
- each repository has its quarantine registry and guard;
- the worker environment has `env/runtime-setup.sh`, `env/runtime-pytest.sh` and `env/app-test.sh`;
- the comparator is `env/baseline-diff.py`.

What the Release 14 run built on `release/14/plan-39` was never merged; this plan ports none of it ([audit](evidence/release-15-measure/audit.md)). The evidence, the alternatives and the critique are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

The task list and critical path are in [tasks.md](tasks.md):
1. **Phase 1, the gates, the prune pass and the large causes.** Cut the plan branches and re-measure. Fix the comparator once, for both repositories. Add per-test results where they are missing, and seal each ceiling. The prune pass runs beside the gates, and so do the four largest causes: the Runtime's v33 provider fixtures (358 tests) and its commit-crash fixture (32), and the App's fake Runtime routes (about 44) and its missing browser installs. Then the review stop RS1, and the plan branches land in `release/16/main` for the first time with the owner's go.
2. **Phase 2, the middle and the long tail,** by cause, the two repositories in parallel: Runtime CI (about 25 cards), Runtime Nightly (14) and the App (about 18).
3. **Phase 3, kept green:** the nightly report, the required-checks lists, and three green nights per workflow on one frozen head. Then the final review R.
4. **Phase 4, the three-products structure,** beside phase 3: each three-products test owns its seed, then the suite runs shuffled on two workers.

Nothing starts until the owner confirms the decisions and names who runs it. Recording this plan authorizes no implementation.

## Interfaces and handoff

- **Consumes:**
  - each repository's `release/15/main` head, recorded at GM-0, and later `release/16/main`;
  - the cross-repository pins: the Runtime's `tests/astrid-agent.pin`, and the App's `runtime.lock.json`, `config/astrid-cli-surface/vendor.lock.json` and `public/install-manifest.json`;
  - Plan 91's `env/baseline-diff.py` change (AG-1) and its `ci/required-checks.json` format (AG-2).
- **Produces:**
  - green Runtime and App workflows;
  - `ci/runtime-ceiling.tsv` and `ci/app-ceiling.tsv`, both empty at the end, or holding only entries the owner accepted;
  - per-test JSON results from every App test job, with an adapter in `env/`;
  - `tests` and `repeat` dispatch inputs on the Runtime's and the App's test workflows;
  - `ci/required-checks.json` in the Runtime and the App, for the owner to set and for Plan 31's `release-contract` to read;
  - `scripts/ci_red_report.py` and its nightly workflow in astrid-dev, covering the Agent too.

## Completion

- Each workflow listed in Included has a green run on one frozen head of `release/16/plan-39`, on three different nights, then one green run on `release/16/main` after the plan branch lands.
- Each ceiling is empty, or holds only entries the owner accepted, each with its issue. Each quarantine holds at most 10 IDs, all within age.
- The nightly report has run for three nights and named any new red.
- **Negative cases** (each shown by an injected failure on a scratch branch):
  - a test that passes on the ceiling's run and fails on the candidate, a new failing test, and a missing test each turn the gate red;
  - a cancelled or truncated job turns it red;
  - an expired quarantine entry, and a strict xfail that starts passing, each turn its repository red;
  - the App's fake Runtime check fails when the App calls a route the fake does not serve.
- **Limits:** GitHub-hosted runners only. Branch protection is the owner's setting; this plan lists the checks and shows them green.
