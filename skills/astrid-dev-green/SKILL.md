---
name: astrid-dev-green
description: Make Astrid's test results complete and trustworthy, then either gate a candidate on no new failures or retire old red at its roots, using GitHub Actions well and keeping the work moving at CI's pace.
---

# Get to green

Terms follow the [glossary](../astrid-dev-shared/glossary.md). This skill owns how to **read, complete and act on** CI results. These rules have their own homes, and this skill links to them:
- the [regression rule and when a run bears load](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing);
- [never weakening a check](../astrid-dev-shared/run-contract.md#checks-and-failure-repair), and where local runs stop;
- [dispatch, integration and pushes](../astrid-dev-manage/SKILL.md#steps);
- the [publish gate](../astrid-dev-release/SKILL.md);
- the green-mains project's [order, quarantine and completion](../../plans/39-green-mains/plan.md);
- the [tools in `env/`](../../env/README.md).

Each single fix is one [Iterate](../astrid-dev-iterate/SKILL.md) card.

## Page one

- **Measure before you judge.** A comparison is only as good as its least complete side.
- **No result is not a pass.** A test job that was cancelled, timed out, stopped in setup, or ran zero tests has **NO-RESULT**. Never count it as green, and never count its tests as missing. A log that omits passes (pytest `-ra`) can show failures but can never show a regression.
- **Diagnose freely; qualify once.** A NON-PROOF run tells you what is there, and never counts for a gate. Only an ordinary run of the exact candidate, with complete reporting, qualifies ([Iterate](../astrid-dev-iterate/SKILL.md#iterate-freely-qualify-once)).
- **Full suites run on hosted CI** ([where local runs stop](../astrid-dev-shared/run-contract.md#checks-and-failure-repair)).

## 1. Name the question

| Question | Mode | Ends in |
| --- | --- | --- |
| Is this candidate worse than its baseline, test by test? | **A: no new failures** (a release or project gate) | no blocking row, on one qualifying run of the frozen candidate |
| Why is this `main` red, and how do we make it green? | **B: retire old red** (the [green-mains project](../../plans/39-green-mains/plan.md)) | that project's completion |

Both start at step 2. If step 2 can't complete, the first card in either mode is to fix the reporting.

## 2. Measure

For each side, and each workflow in scope:
1. **Inventory the jobs** of the exact run, and sort each one into a kind:
   - a **test job**, which must report per-test results;
   - an **aggregate** (for example, the Agent's `unit` job only echoes, and reads "skipped" when a shard is cancelled);
   - a **non-test check** (lint, mypy, a build), compared by its own output;
   - an **expected omission**, a job that is meant to be skipped on this trigger.
   Only test jobs can be NO-RESULT.
2. **Fetch the logs** (see [Using GitHub Actions](#using-github-actions)), strip the timestamp prefix, and keep the raw copies.
3. **Count each test job's tests.** A count far below that job's usual count means a setup break, a collection abort or a hang, even when the job reads "success".
4. **Find out what is behind each NO-RESULT** with a NON-PROOF run. Change only what stops the run, and keep every marker, selector and lane option:

| Stop | NON-PROOF way through |
| --- | --- |
| A step runs past one and a half times its usual time (a hang) | Cancel it; don't wait. Name the test: collect the shard exactly as CI does (the same command, `--splits`, `--group` and `--durations-path`), map the last progress line's characters onto that order, and read the pytest-timeout dumps. Run that test alone on both sides with `-o faulthandler_timeout=300`. A scratch run that leaves out the hanging file changes coverage, and the shards' membership with it. So compare by test id, account for every id of the original inventory, and keep the left-out ids unsorted |
| A setup step fails, so no tests run | Fix the setup; it is usually one card. Then run again |
| A suite stops at its first failure (`-x`, `--maxfail`, a serial chain) | Override only the stop. Append `--maxfail=0` after the job's own options, or run a serial chain one test at a time with an isolating filter |
| A failing gate skips the job's later steps | Run the skipped steps once on a scratch ref |
| An install or update journey stops at a failing stage | The Agent's `journey.yml` `diagnostic_keep_going`, under the input contract in that workflow: legs `release9-then-install`, `fresh-install` or `both`, direct rows only. Its gate is always red |

5. **Then qualify.** A NO-RESULT closes only through an ordinary run of the exact commit with complete reporting. Usually that means a reviewed reporting fix lands first, for example `-rA` in that repository's workflow.
   - A baseline run from a scratch commit counts only if the commit changes reporting alone, so the same tests run, and its row names that commit.
   - A commit that leaves tests out is diagnostic, and its left-out tests stay unsorted.
   - The gate's owner rules on any other case, and the ruling is recorded on the row.

**What the sorter reads.** [`env/baseline-diff.py`](../../env/README.md) reads pytest `-rA` summary lines only. App results (Vitest, Playwright) have no adapter yet, so compare them by check name ([release](../astrid-dev-release/SKILL.md)) until one exists.

## 3A. No new failures

1. Sort with `baseline-diff.py`, never by hand. Give it each same-commit baseline run under its own label.
2. **Flips:** compare those baseline runs with each other. A test that flips between runs of one commit gets its own row, with both runs, and is never retried until green. **A flip excuses nothing:** a candidate failure that passed on any baseline run is still a regression, and still blocks.
3. One row per failing or missing id. Each row gives the bucket, candidate SHA, one-line cause, the commit or lane that introduced it, owner, disposition and link.
   - **A regression,** or a failing new test that checks the candidate's own behaviour: blocks until its owner fixes it.
   - **A failing new test that exposes a defect already on the baseline:** prove it on the baseline, keep the test out of the candidate, and give it a row in the green-mains plan.
   - **Preexisting:** listed only.
   - **Missing:** cleared only by a recorded ruling, either a behaviour removed on purpose, or a rename that keeps the coverage ([the contract's ruling](../astrid-dev-shared/run-contract.md#checks-and-failure-repair)). A deleting commit alone doesn't clear it.
4. **Find the introducing commit** by bisecting across the candidate's merges, which are named lanes. A failure in files an active lane owns goes to that lane: the test id, the commit, the first error and your best guess.
5. Re-sort at each load-bearing run. The gate stands on the frozen candidate's qualifying run, with no blocking row left and no test job without a result.

## 3B. Retire old red

1. **Fix in layers, top first,** because each layer hides the one below:
   1. reporting: complete runs, `-rA`, real aggregates;
   2. a few shared causes: setup, environment, a hang;
   3. the long tail: stale tests, with real bugs among them.

   One Agent collection error once hid about 24,500 tests.
2. **Cluster by cause, not by file.** The key is the exception type plus the first frame in product code. Rank clusters by the tests a fix would unblock.
3. **Batch.**
   - One cause is one Iterate card. Run every card whose scope doesn't overlap another's at the same time ([scopes](../astrid-dev-manage/SKILL.md#steps)).
   - Land several cards per push, and re-sort once per batch.
4. **Stop patching and spec a project** ([Plan](../astrid-dev-plan/SKILL.md)) when any of these holds:
   - a cause needs a contract or schema decision;
   - a cause spans about ten files or more;
   - the same signature comes back after two batches.
5. **A real bug** gets its own fix card. A test that can't be fixed in its card follows the [quarantine rule](../../plans/39-green-mains/plan.md#quarantine-rule), and only once that rule's guard exists in the repository. The Agent's guard fails every xfail today (`tests/lanes.py`).
6. **Fix where the change will ship.** While a release candidate far ahead of `main` is in flight, ask the owner where to cut the work.

## Using GitHub Actions

- **REST through the session proxy, no token.**
  - List runs: `GET /repos/<o>/<r>/actions/runs?branch=<b>` or `?head_sha=<sha>`.
  - List jobs: `.../runs/<id>/jobs?per_page=100`, or `.../runs/<id>/attempts/<n>/jobs` for an earlier attempt.
  - Fetch a log: `.../actions/jobs/<id>/logs` (follow the redirect).
  - Fetch artifacts: [`fetch-artifacts.sh`](../astrid-dev-orchestrate/codex-in-claude-cloud/fetch-artifacts.sh).
  - Cancel your own run: `POST .../runs/<id>/cancel`.
- **Timestamps.** A job log prefixes every line with a timestamp. Strip it with the regex `^\S+Z ` (for example, Python `re.sub`) before sorting, or the sorter finds nothing. Grep for the failing ids rather than reading whole logs. Logs and artifacts expire (test durations after 3 days, and some logs vanish), so commit the evidence when you take it.
- **Know each workflow's trigger.** Read its `on:` block before relying on a run.
  - In the Agent, `ci.yml` and `lanes.yml` run on pushes to `main`, `release-1` and `int/**`, and on dispatch; they don't run on pull requests.
  - The Agent's `windows-journey.yml` runs on pull requests to `main` and on pushes to `windows/**`.
  - Runtime CI runs on every push and every pull request.
  - App pushes to `int/**` start its full workflows ([manage](../astrid-dev-manage/SKILL.md#steps)).
  - Before a gate, list every required workflow and where the candidate's run of each comes from.
- **A scratch ref** is your own branch, started with `POST .../actions/workflows/<file>/dispatches`, the header `Content-Type: application/json` (the proxy refuses the call without it) and `{"ref": "<branch>"}`. Then find its run by listing runs for that branch. It never enters a candidate.
- **Concurrency is set per workflow.** Read its `concurrency:` block. Where `cancel-in-progress` is on, a new run on the same group cancels the one in flight. The Agent's `ci.yml` groups by workflow and ref; manual journey dispatches never cancel each other. The coordination rule is [manage's](../astrid-dev-manage/SKILL.md#steps).
- **Paid workflows.** VibeComfy's `nightly-runpod.yml` and `e2e_matrix.yml` can rent RunPod pods. Never dispatch them without paid authorization.
- **Run less to learn more.** Diagnose on one shard or one file, not the whole matrix. Re-run a cancelled shard only after you have changed or diagnosed its cause ([two-same-signature rule](../astrid-dev-shared/run-contract.md#checks-and-failure-repair)).

## Keep it moving

The loop runs at CI's pace, about two hours a cycle at Agent scale, so:
- **Never wait on a run.** While it runs, cluster the last results and brief the next batch.
- **Run everything independent at once:** measurement, clustering and disjoint fix cards, using cheap helpers for the mechanical parts ([routes](../astrid-dev-shared/run-contract.md#cheapest-model-first)).
- **Turn repeated judgment into a tool** in `env/`. A recipe you have run twice by hand is the next tool card.
- **Spend review where it bears load:** a disputed bucket, a change to an assertion, the decision to spec a project, and the qualifying run.
- **Record every friction** in the [process ledger](../../docs/ledger/README.md), so the next run starts from a better skill.
