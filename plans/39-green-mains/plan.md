# All three mains green

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). A red check on `main` should mean a new regression. Today it means nothing, because every full CI workflow on Agent, Runtime and App `main` has been red for weeks.

## Outcome and scope

Every CI workflow that runs on a push to `main`, in astrid-agent, astrid-runtime and astrid-app, is green, and it stays green:
- **Green.** Each failing job is fixed at its root cause ([triage](inputs.md#root-cause-triage)), never by loosening an assertion to match a bug. A test changes only when the behaviour it checks changed on purpose, and the task card names the commit or contract that changed it.
- **Kept green.** Hannah turns on the [required checks](tasks.md#required-checks) for each `main`. One [quarantine rule](#quarantine-rule), the same in all three repositories, is the only way a known failure may be tolerated. A nightly report names any new red within a day.
- **Releases.** The release rule changes from "no new red against `main`" ([Release skill](../../skills/astrid-dev-release/SKILL.md)) to "every required check is green on each pinned commit". The check lives in [Plan 31](../31-releases-from-astrid-dev/plan.md)'s `release-contract` job as one more rule on the release record. It is not a second gate.
- **Structural (phase 4, from [Release 12](inputs.md#release-12-structural-evidence)).** The causes that kept the mains hard to read are removed too. Each App three-products test owns its seed, so the journey runs in parallel and in any order, and CI shuffles it. An expected failure names the step and error it expects. Every `main` and `int` run stores per-test results, so a candidate is compared with the published `main` without reruns, and a cancelled or truncated shard turns the run red. Once the mains are green, feature work lands on `main` through ordinary CI, so a release candidate is `main` plus a short, listed set of fixes; the mains are frozen from cut-off to publication, and the release record states both. Each Agent code and harness smell Release 12 found gets a fix and a guard for its class.

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
