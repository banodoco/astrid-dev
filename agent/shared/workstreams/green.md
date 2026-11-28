---
description: Make Astrid's test results complete and trustworthy, then either gate a candidate on no new failures or retire old red at its roots, using GitHub Actions well and keeping the work moving at CI's pace.
skill: true
---

# Get to green

## When to use

When a candidate needs qualification or existing CI failures prevent reliable integration.

## Outcome

Complete, trustworthy test evidence showing either no new failures or diagnosed repair of old red without weakening checks.

## Inputs

The exact source and baseline revisions, original test inventories, runner and dependency identities, and authorized proof scope.

## Procedure

Measure original jobs and identities, compare real failures, repair causes within scope and retain all regressions and gate evidence.

## Completion

Native outcomes and raw exits reconcile with the stated claim, including blockers and any remaining red.

Terms follow the [glossary](../glossary.md). This skill owns how to **read, complete and act on** CI results. These rules have their own homes, and this skill links to them:
- the [regression rule and when a run bears load](../run-contract.md#when-a-test-run-is-load-bearing);
- [never weakening a check](../run-contract.md#checks-and-failure-repair), and where local runs stop;
- [dispatch, integration and pushes](../../roles/manager.md#steps);
- the [publish gate](release.md);
- the green-mains projects' order, quarantine and completion: [Plan 91](../../../plans/91-agent-main-green/plan.md) for the Agent, [Plan 39](../../../plans/39-green-mains/plan.md) for the Runtime and the App;
- the [tools in `env/`](../../../env/README.md).

Each single fix is one [Iterate](iterate.md) card.

## Page one

- **Measure before you judge.** A comparison is only as good as its least complete side.
- **No result is not a pass.** A required job that was cancelled, timed out, skipped when it should have run, or stopped in setup has **NO-RESULT**, as does a test job that ran zero tests. Never count it as green, and never count its tests as missing. A log that omits passes (pytest `-ra`) shows its failures, but can never support a complete comparison or a claim of zero regressions.
- **Diagnose freely; qualify once.** A NON-PROOF run tells you what is there, and never counts for a gate. Only an ordinary run of the exact candidate, with complete reporting, qualifies ([Iterate](iterate.md#iterate-freely-qualify-once)).
- **Full suites run on hosted CI** ([where local runs stop](../run-contract.md#checks-and-failure-repair)).

## 1. Name the question

| Question | Mode | Ends in |
| --- | --- | --- |
| Is this candidate worse than its baseline, test by test? | **A: no new failures** (a release or project gate) | no blocking row, on one qualifying run of the frozen candidate |
| Why is this `main` red, and how do we make it green? | **B: retire old red** (the green-mains projects: [Plan 91](../../../plans/91-agent-main-green/plan.md) for the Agent, [Plan 39](../../../plans/39-green-mains/plan.md) for the Runtime and the App) | that project's completion |

Both start at step 2. If step 2 can't complete, the first card in either mode is to fix the reporting.

## 2. Measure

For each side, and each workflow in scope:
1. **Inventory the jobs** of the exact run, and sort each one into a kind:
   - a **test job**, which must report per-test results;
   - an **aggregate** (for example, the Agent's `unit` job only echoes, and reads "skipped" when a shard is cancelled);
   - a **non-test check** (lint, mypy, a build), compared by its own output;
   - an **expected omission**, a job that is meant to be skipped on this trigger.
   The kind says what a usable result is: per-test lines for a test job, its own output for a non-test check, and its dependencies' results for an aggregate. Every required job needs one. A required job that is unexpectedly cancelled, skipped or absent is NO-RESULT, and blocks qualification; only an omission the workflow defines for this trigger is exempt, with the reason recorded.
2. **Fetch the logs** (see [Using GitHub Actions](#using-github-actions)), strip the timestamp prefix, and keep the raw copies.
3. **Count each test job's tests.** A count far below that job's usual count means a setup break, a collection abort or a hang, even when the job reads "success". Count failures as distinct (job, id) pairs, not summary lines: one id can appear twice in a job's summary.
4. **Find out what is behind each NO-RESULT** with a NON-PROOF run. Change only what stops the run, and keep every marker, selector and lane option:

| Stop | NON-PROOF way through |
| --- | --- |
| A hang ([manage's threshold](../../roles/manager.md#steps)) | Cancel it; don't wait. Name the test: collect the shard exactly as CI does (the same command, `--splits`, `--group` and `--durations-path`), map the last progress line's characters onto that order, and read the pytest-timeout dumps. Run that test alone on both sides with `-o faulthandler_timeout=300`. A scratch run that leaves out the hanging file changes coverage, and the shards' membership with it. So compare by test id, account for every id of the original inventory, and keep the left-out ids unsorted |
| A setup step fails, so no tests run | Fix the setup; it is usually one card. Then run again |
| A suite stops at its first failure (`-x`, `--maxfail`, a serial chain) | Override only the stop. Append `--maxfail=0` after the job's own options, or run a serial chain one test at a time with an isolating filter |
| A failing gate skips the job's later steps | Run the skipped steps once on a scratch ref |
| An install or update journey stops at a failing stage | The Agent's `journey.yml` `diagnostic_keep_going`, under the input contract in that workflow: legs `release9-then-install`, `fresh-install` or `both`, direct rows only. Its gate is always red |

5. **Then qualify.** A NO-RESULT closes only through an ordinary run of the exact commit with complete reporting. Usually that means a reviewed reporting fix lands first, for example `-rA` in that repository's workflow.
   - A baseline run from a scratch commit counts only if the commit changes reporting alone, so the same tests run, and its row names that commit.
   - A commit that leaves tests out is diagnostic, and its left-out tests stay unsorted.
   - The gate's owner rules on any other case, and the ruling is recorded on the row.

**What the sorter reads.** [`env/baseline-diff.py`](../../../env/README.md) reads pytest `-rA` summary lines only. App test runners (Vitest, Playwright) report per test, but nothing compares them yet. Until an adapter exists, App per-test qualification is unresolved: say so on the gate, and never stand in a by-name comparison for it.

## 3A. No new failures

1. Sort with `baseline-diff.py`, never by hand. Give it each same-commit baseline run under its own label.
2. **Flips:** compare those baseline runs with each other. A test that flips between runs of one commit gets its own row, with both runs, and is never retried until green. **A flip excuses nothing:** a candidate failure that passed on any baseline run is still a regression, and still blocks.
3. One row per failing or missing id. Each row gives the bucket, candidate SHA, one-line cause, the commit or lane that introduced it, owner, disposition and link.
   - **A regression,** or a failing new test that checks the candidate's own behaviour: blocks until its owner fixes it, or, for a release, the owner accepts it on that release's [known ledger](release.md#what-a-release-must-show).
   - **A failing new test that exposes a defect already on the baseline:** prove it on the baseline, keep the test out of the candidate, and give it a row in the green-mains plan.
   - **Preexisting:** listed only.
   - **Missing:** cleared only by a recorded ruling, either a behaviour removed on purpose, or a rename that keeps the coverage ([the contract's ruling](../run-contract.md#checks-and-failure-repair)). A deleting commit alone doesn't clear it.
4. **Find the introducing commit** by bisecting across the candidate's merges, which are named lanes. A failure in files an active lane owns goes to that lane: the test id, the commit, the first error and your best guess.
5. Re-sort at each load-bearing run. The gate stands on the frozen candidate's qualifying run, with no blocking row left and no required job without a usable result.
6. **A packet or task** is judged on what its own change does. A failure that also fails or flips on its base is not caused by it: it gets its own row and does not block that merge. It is not excused, and its row still blocks the release candidate under step 2. To tell a suspected flip, run that one test in isolation three times on the base and three on the head. If it fails on any head run and on no base run, it is the change's. Never rerun until green.
7. **To get a release branch green,** run this mode on the head of `release/<NN>/main` ([the stage](release.md#get-the-release-branch-green)); a regression goes to the plan that brought it, and old red is mode B.

## 3B. Retire old red

1. **Fix in layers, top first,** because each layer hides the one below:
   1. reporting: complete runs, `-rA`, real aggregates;
   2. a few shared causes: setup, environment, a hang;
   3. the prune pass: tests of behaviour that is no longer supported, and duplicates (step 3);
   4. the long tail: stale tests, with real bugs among them.

   One Agent collection error once hid about 24,500 tests.
2. **Stop it getting worse first.** Before the first fix lands, seal the measured failing (job, id) pairs as the project's **ceiling**, a file in the repository (the Agent's is `ci/agent-ceiling.tsv`). Every batch run is compared with it by `env/baseline-diff.py`: a failure not on the ceiling blocks, and so does a missing id. Only the manager edits the ceiling, and only to remove ids that passed in a hosted batch run; cards never touch it. The ceiling is how a red repository tolerates its old failures while they are fixed. It is not a quarantine: nothing on it is marked, skipped or hidden, and it only shrinks.
3. **Prune before fixing.** The owner rules once on what is still supported (the support line; for the Agent, [Plan 91's D5](../../../plans/91-agent-main-green/inputs.md#owner-decisions): only current behaviour, and updating from the previous published release). Then:
   - a test of behaviour outside that line is **retired**: deleted, citing the change that retired it or the ruling. Where a user could still reach the old path (an API route, a command, a file the App opens), a test asserts that it refuses, as with `410 retired_route`;
   - a test that only repeats a passing test is **redundant**: deleted, naming the covering test and what both assert;
   - a test of something users do today is never deleted for being hard to fix.

   Every deletion is listed in its pull request and read by an `X` reviewer. This is a ruled deletion under [the contract](../run-contract.md#checks-and-failure-repair), never a way to get a pass. Select candidates by failure message and test name, judge each one, and run the prune pass before the cause cards, because its verdicts decide which ids those cards fix at all.
4. **Cluster by cause, not by file.** The key is the exception type plus the first frame in product code. Rank clusters by the tests a fix would unblock. [`cluster_failures.py`](../../../plans/91-agent-main-green/evidence/cluster_failures.py) does this from job logs; it is the next tool to move into `env/`.
5. **Name the kind of each cause, with evidence,** and fix it by kind: env, stale test, retired, redundant, product bug, flaky or unknown. [Plan 91's triage rules](../../../plans/91-agent-main-green/tasks.md#triage-rules) give the allowed fix and the proof for each. A stale-test fix quotes a source that states the new behaviour and postdates the test's last change; without one, the kind is unknown.
6. **Batch.**
   - One cause is one Iterate card. Run every card whose scope doesn't overlap another's at the same time ([scopes](../../roles/manager.md#steps)).
   - Land them in batches ([pushes start CI](../../roles/manager.md#steps)), and re-sort once per batch.
   - A pull request into a release branch runs only a subset, and a push to a plan branch starts nothing in the Agent or the App, so the batch run is dispatched on the plan branch and compared with the ceiling.
7. **Stop patching and spec a project** ([Plan](plan.md)) when any of these holds:
   - a cause needs a contract or schema decision;
   - a cause spans about ten files or more;
   - the same signature comes back after two batches.
8. **A real bug** gets its own fix card. A test that can't be fixed in its card follows its project's quarantine rule ([Plan 39's](../../../plans/39-green-mains/plan.md#quarantine-rule) for the Runtime and the App), and only once that rule's guard exists in the repository. The Agent's guard fails every xfail (`tests/lanes.py`), so an Agent defect stays visibly red on the ceiling, with an issue and the owner's acceptance ([Plan 91's D6](../../../plans/91-agent-main-green/inputs.md#owner-decisions)).
9. **Fix where the change will ship:** a fix branch under the release in progress, or a fix release for the published one ([which](release.md#how-a-release-runs), step 5).

## Using GitHub Actions

- **REST through the session proxy, no token.**
  - List runs: `GET /repos/<o>/<r>/actions/runs?branch=<b>` or `?head_sha=<sha>`.
  - List jobs: `.../runs/<id>/jobs?per_page=100`, or `.../runs/<id>/attempts/<n>/jobs` for an earlier attempt.
  - Fetch a log: `.../actions/jobs/<id>/logs` (follow the redirect).
  - Fetch artifacts: [`fetch-artifacts.sh`](../../guides/codex-in-claude-cloud/fetch-artifacts.sh).
  - Cancel your own run: `POST .../runs/<id>/cancel`.
- **Timestamps.** A job log prefixes every line with a timestamp. Strip it with the regex `^\S+Z ` (for example, Python `re.sub`) before sorting, or the sorter finds nothing. Grep for the failing ids rather than reading whole logs. Logs and artifacts expire (test durations after 3 days, and some logs vanish), so commit the evidence when you take it.
- **Know each workflow's trigger.** Read its `on:` block before relying on a run. This is the one statement of what CI runs:
  - A push to `release/*/main` runs the full workflows. Agent: CI (15 jobs, including Windows and macOS), Lanes, Chat and the Windows journey. App: Tests, E2E and Lanes.
  - A pull request into `release/*/main` runs a fast subset. Agent: fast checks, unit shard 1 of 8, boundary, chat and the Windows journey. App: Tests, with the release guard only for pull requests into `main`.
  - A push to a plan or fix branch starts nothing in the Agent or App unless a pull request is open.
  - Runtime and VibeComfy run their full CI on every push and pull request.
  - The installed journey (`journey.yml`) is not started by release branches: dispatch it with `branch=release/<NN>/main`.
  - So the full suite first runs on the combined tree after a merge to the release branch, which is why [getting the release branch green](release.md#get-the-release-branch-green) and its red-branch rule exist.
  - Before a gate, list every required workflow and where the candidate's run of each comes from.
- **Schedules fire only on the default branch.** A `schedule:` trigger runs on `main` alone, so the Agent's nightly Lanes and journey, the Runtime's `Nightly` and the App's `Direct Journey` never run on a release or plan branch by themselves. Dispatch them there.
- **A scratch ref** is your own branch, started with `POST .../actions/workflows/<file>/dispatches`, the header `Content-Type: application/json` (the proxy refuses the call without it) and `{"ref": "<branch>"}`. Then find its run by listing runs for that branch. It never enters a candidate.
- **Concurrency is set per workflow.** Read its `concurrency:` block. Where `cancel-in-progress` is on, a new run on the same group cancels the one in flight. The Agent's `ci.yml` groups by workflow and ref; manual journey dispatches never cancel each other. The coordination rule is [manage's](../../roles/manager.md#steps).
- **An unexplained cancellation is NO-RESULT.** A run cancelled where `cancel-in-progress` is off was cancelled by someone or something else. On 22–24 November 2026 that happened to most started Agent runs on `release/15/main`, three Runtime runs and every job of one App run before a runner took it. Find the cause before relying on that branch's runs.
- **Paid workflows.** VibeComfy's `nightly-runpod.yml` and `e2e_matrix.yml` can rent RunPod pods. Never dispatch them without paid authorization.
- **Run less to learn more.** Diagnose on one shard or one file, not the whole matrix. Re-run a cancelled shard only after you have changed or diagnosed its cause ([two-same-signature rule](../run-contract.md#checks-and-failure-repair)).

## Keep it moving

The loop runs at CI's pace, about two hours a cycle at Agent scale, so:
- **Never wait on a run.** While it runs, cluster the last results and brief the next batch.
- **Run everything independent at once:** measurement, clustering and disjoint fix cards, using cheap helpers for the mechanical parts ([routes](../run-contract.md#cheapest-model-first)).
- **Turn repeated judgment into a tool** in `env/`. A recipe you have run twice by hand is the next tool card.
- **Spend review where it bears load:** a disputed bucket, a change to an assertion, the decision to spec a project, and the qualifying run.
- **Record every friction** in the [process ledger](../../../docs/ledger/README.md), so the next run starts from a better skill.
