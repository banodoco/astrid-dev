---
name: astrid-dev-green
description: Make Astrid's test results complete and trustworthy, then either gate a candidate on no new failures or retire old red at its roots, using GitHub Actions well and keeping the work moving at CI's pace.
---

# Get to green

Terms follow the [glossary](../astrid-dev-shared/glossary.md). The rules this skill applies have their own homes: the [regression rule and load-bearing runs](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing), [never weaken a check](../astrid-dev-shared/run-contract.md#checks-and-failure-repair), [dispatch and integration](../astrid-dev-manage/SKILL.md#steps), the [publish gate](../astrid-dev-release/SKILL.md), and the [tools in `env/`](../../env/README.md). Each single fix is one [Iterate](../astrid-dev-iterate/SKILL.md) card.

## Page one

- **Measure before you judge.** A comparison is only as good as its least complete side. Every later step depends on complete per-test results for a named commit.
- **No result is not a pass.** A job that was cancelled, skipped, timed out, stopped in setup, or ran zero tests is **NO-RESULT**. So is a log that carries no per-test lines (`-ra` instead of `-rA`, or JS output the sorter can't read). Never count it as green, and never count its tests as missing.
- **Full suites run on hosted CI only.** Locally, reproduce one test at a time.
- **Never weaken a check to get green.** No skip, xfail, deselect, broader marker, longer timeout or raised baseline. A diagnostic run that leaves something out is NON-PROOF (see below).

## 1. Name the question

| Question | Mode | Ends in |
| --- | --- | --- |
| Is this candidate worse than its baseline, test by test? | **A: no new failures** (a release or project gate) | zero rows in the blocking buckets, signed on one binding run |
| Why is this `main` red, and how do we make it green? | **B: retire old red** (a green-mains project such as [Plan 39](../../plans/39-green-mains/plan.md)) | the workflows green on `main`, and guarded |

Both start at step 2. If step 2 can't complete, fixing the reporting is the first card in either mode.

## 2. Measure

For each side (baseline and candidate, or just `main` in mode B), and for every workflow in scope:
1. **List the jobs** of the exact run and give each one a state: complete, failed with results, or NO-RESULT and why.
2. **Fetch the logs** (see [Using GitHub Actions](#using-github-actions)), strip the timestamp prefix, and keep the raw copies.
3. **Count tests per job.** A job's count far below its usual count is a sign of a setup break, a collection abort or a hang, even when the job reads "success".
4. **Close every NO-RESULT** before judging. Each kind of stop needs its own way through:

| Stop | Get the complete list once, as NON-PROOF |
| --- | --- |
| A step runs past one and a half times its usual time (a hang) | Cancel it, and don't wait. Find the test: map the progress characters of the last pytest line onto the shard's collected order (`--collect-only --splits N --group G`), and read the pytest-timeout dumps. Run that test alone on both sides with `-o faulthandler_timeout=300`. Then get the rest of the shard from one scratch-ref run that leaves out only the hanging file, on both sides alike |
| A setup step fails, so no tests run | Fix the setup on a scratch ref (it is usually one card), then measure again |
| A suite stops at its first failure (a serial chain, `-x`, `--maxfail`) | Run it once with the stop removed (`-o addopts=` clears pytest's), or once per test with an isolating filter |
| A gate fails, so later steps in the job are skipped | Run the skipped steps once on a scratch ref |
| An install or update journey stops at a failing stage | The Agent's `journey.yml` `diagnostic_keep_going` input. It is direct rows only, covers only the fresh-install leg, and its gate is always red |

A NON-PROOF run is never evidence for a gate. It only tells you what is there. Name the stop and its NON-PROOF run on the affected test's row.

## 3A. No new failures

1. Sort with [`env/baseline-diff.py`](../../env/README.md), never by hand. Give it every same-commit baseline run you have, each with its own label.
2. **Flips:** compare those baseline runs with each other, too. A test that flips between two runs of one commit is flaky, and gets its own row with both runs. Never retry it until green.
3. Give every failing or missing id one row: bucket, candidate SHA, one-line cause, the commit or lane that introduced it, owner, disposition and link.
   - **Blocking:** a regression, or a failing new test that checks the candidate's own behaviour. Each gets a fix from its owner.
   - **Not blocking:**
     - a failing new test that exposes a defect already on the baseline: prove it on the baseline, keep the test out of the candidate, and give it a row in the green-mains plan;
     - a preexisting failure: listed only;
     - a missing test: explained by the commit that deleted or renamed it; an unexplained one blocks;
     - a flaky test.
4. **Find the introducing commit** by bisecting across the candidate's merges, which are named lanes. A failure in a file an active lane owns goes to that lane with the test id, the commit, the first error and your best guess.
5. **Re-measure after each candidate push.** The gate is signed on the frozen candidate's one binding run, with no NO-RESULT and no blocking row left.

## 3B. Retire old red

1. **Fix in layers, top first.** Each layer hides the one below:
   1. reporting: complete runs and `-rA`;
   2. a few shared causes: setup, environment, a hang, a type-check baseline;
   3. the long tail of stale tests, with real bugs among them.

   One collection error once hid about 24,500 Agent tests.
2. **Cluster by cause, not by file.** The key is the exception type plus the first frame in product code. Rank clusters by the tests a fix would unblock.
3. **Batch.**
   - One cause is one Iterate card. Run every card whose scope doesn't overlap another's at the same time ([scopes](../astrid-dev-manage/SKILL.md#steps)).
   - Land several cards per push.
   - Re-measure once per batch, not once per card.
4. **Stop patching and spec a project** ([Plan](../astrid-dev-plan/SKILL.md)) when any of these holds:
   - a cause needs a contract or schema decision;
   - a cause spans about ten files or more;
   - the same signature comes back after two batches;
   - one bucket holds more than about sixty distinct failures.
5. **A real bug** found here gets its own fix card. A test that can't be fixed in its card is quarantined only under the [quarantine rule](../../plans/39-green-mains/plan.md#quarantine-rule).
6. **Which branch:** fix where the change will ship. While a release candidate far ahead of `main` is in flight, ask the owner where to cut the work, rather than fixing `main` code the candidate replaces.
7. **Repository order:**
   1. the Agent: the most red, and the Runtime pins it;
   2. the Runtime;
   3. the App;
   4. VibeComfy, only once its scope is agreed. Its scheduled workflows rent RunPod pods; never dispatch them.

## 4. Keep it green

The owner turns on required checks. Every aggregate job fails on any non-success, a job that reports zero tests is red, and a nightly report names new red within a day. Workflow logic lives in tested scripts, not inline copies; the R13 Lanes break was one copy left behind.

## Using GitHub Actions

- **REST through the session proxy, no token.**
  - List runs: `GET /repos/<o>/<r>/actions/runs?branch=<b>` or `?head_sha=<sha>`.
  - List jobs: `GET .../runs/<id>/jobs?per_page=100`, or `.../runs/<id>/attempts/<n>/jobs` for an earlier attempt.
  - Fetch a log: `GET .../actions/jobs/<id>/logs` (follow the redirect).
  - Fetch artifacts: [`fetch-artifacts.sh`](../astrid-dev-orchestrate/codex-in-claude-cloud/fetch-artifacts.sh).
- **Job logs prefix every line with a timestamp.** Strip `^\S+Z ` before sorting, or the sorter finds nothing. Grep the failing ids rather than reading whole logs. Logs and artifacts expire (durations after 3 days, some logs vanish), so commit the evidence when you take it.
- **What starts CI.**
  - Agent CI and Lanes start on pushes to `main`, `release-1` and `int/**`, and on dispatch. Agent PRs and other branches start nothing.
  - App pushes to `int/**` start its full workflows, and App PRs start Tests and Dockerfile Check ([manage](../astrid-dev-manage/SKILL.md#steps)).
  - Runtime CI starts on every push and every pull request.
  - A full Agent run takes about nine runners for up to two hours.
- **A scratch ref** is your own branch with at most one reporting-only commit (for example, leave out one hanging file, or add `-rA`), started with `POST .../actions/workflows/<file>/dispatches` and `{"ref": "<branch>"}`. Then find its run by listing runs for that branch. A scratch commit is not the baseline SHA, so say what it changes on every row that uses it. It never enters a candidate.
- **One run per ref.** Concurrency groups cancel a second run on the same ref ([rule](../astrid-dev-manage/SKILL.md#steps)). Never dispatch on another project's ref. During a release gate, dispatch only when the release manager says runners are free. Cancel your own superseded run (`POST .../runs/<id>/cancel`).
- **Run less to learn more.** Diagnose on one shard or one file, not the whole matrix. Re-run a cancelled shard only after you have changed or diagnosed its cause ([two-same-signature rule](../astrid-dev-shared/run-contract.md#checks-and-failure-repair)).

## Keep it moving

The loop runs at CI's pace, about two hours a cycle at Agent scale, so:
- **Never wait on a run.** While it runs, cluster the last results and brief the next batch.
- **Run everything independent at once:** measurement, clustering and disjoint fix cards, using cheap helpers for the mechanical parts ([routes](../astrid-dev-shared/run-contract.md#cheapest-model-first)).
- **Turn repeated judgment into a tool** in `env/`. A recipe you have run twice by hand is the next tool card.
- **Spend review where it bears load:** the bucket of a disputed row, a change to an assertion, the decision to spec a project, and the binding run.
- **Record every friction** in the [process ledger](../../docs/ledger/README.md), so the next run starts from a better skill.
