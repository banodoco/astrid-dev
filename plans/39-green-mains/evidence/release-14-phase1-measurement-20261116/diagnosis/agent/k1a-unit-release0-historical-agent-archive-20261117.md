# Plan 39 K1a — missing authentic release-0 Agent archive in unit shards (2026-11-17 UTC)

**N-class, source- and actual-hosted-log-proven prerequisite; isolated candidate, NOT an accepted fix.** Source Agent `release/14/plan-39` exact head `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` (reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`). The finished [CI 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), attempt **1**, has **882 XML failures/398 errors**, already measured. [Lanes 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160), attempt 1, has **306 failures (12 log-only opt-in included)/260 errors**. No new CI or Lanes qualification run was initiated; neither completed historical total is revised.

## Actual XML and raw log

Unit shard 7, job [133651924616](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924616), JUnit [artifact 14281865130](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14281865130). Artifact remains unexpired; GitHub reports digest **`sha256:3d208e420b35370e7b153a3f6349a64c415df126e87d3f5d97b7b1b9c8c0693a`**, matching the previously verified actual ZIP. Inner XML SHA-256 **`3bd9218c3830caf27bc2502a50ebc7293c19012bad01a2e890b1f31c703b993b`**. Complete actual-XML inventory SHA-256 **`729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426`**, reverified in the active container.

Exactly **three actual failing testcase IDs** share **one distinct full literal XML message (count 3)**:

- `tests.test_installer_release0_rollback::test_rollback_selects_and_starts_authentic_release0_runtime`
- `tests.test_installer_release0_rollback::test_pre_stop_interruption_recovers_and_starts_authentic_release0_runtime`
- `tests.test_installer_self_contained_launchers::test_service_and_foreground_exec_with_authentic_release0_package`

Full literal XML `message`:

```text
subprocess.CalledProcessError: Command '['git', 'archive', '--format=tar', '3204bb00135bec8ee2d2d3fb21eed5abfceca649', 'astrid']' returned non-zero exit status 128.
```

The **actual ~7-MB finished hosted unit-7 job log** was re-read. It repeats the `CalledProcessError` three times, each followed by the literal:

```text
fatal: not a tree object: 3204bb00135bec8ee2d2d3fb21eed5abfceca649
```

These are **three already-counted failures**, not three additional failures or proven product regressions. No new prior-plan exact-ID comparison was performed for these three; never infer any regression from absent old IDs. The existing full job-by-job XML and comparator record remains authoritative.

## Narrow source trace and independently reviewable candidate

At that exact tested Agent head:

1. `tests/test_installer_self_contained_launchers.py` names `RELEASE0_AGENT = "3204bb00135bec8ee2d2d3fb21eed5abfceca649"`; `_release0_environment` runs the above `git archive` in the Agent checkout and installs the authentic historical `astrid/` tree into a disposable venv. Two `tests/test_installer_release0_rollback.py` cases invoke this same helper. This **must remain an authentic historical source**: replacing it with current product modules or weakening rollback assertions is not acceptable.
2. The actual historical [Agent commit](https://github.com/banodoco/astrid-agent/commit/3204bb00135bec8ee2d2d3fb21eed5abfceca649) resolves on GitHub and its [`astrid/installer/core.py`](https://github.com/banodoco/astrid-agent/blob/3204bb00135bec8ee2d2d3fb21eed5abfceca649/astrid/installer/core.py) is readable (blob `2f908b86f870d028be3dbcbd4c959217a0d1200a`). This establishes the remote historical source's existence, **not** hosted fetch success.
3. The exact-head `.github/workflows/ci.yml` `unit-shard` uses default shallow `actions/checkout@v4`, then installs Runtime/RunPod/VibeComfy. It fetches **no historical Agent commit**. The unit-7 hosted error is exactly the expected `git archive` failure from absent Git tree history.
4. New isolated [Agent **draft PR376**](https://github.com/banodoco/astrid-agent/pull/376), branch `p39/k1a-ci-release0-archive-20261117`, base exact `6bbda788`, commit `9c2bbeef7b1bc5a1065c8dc192268acea5b7da8c`, changes only `.github/workflows/ci.yml` in `unit-shard`. After checkout it fetches the exact historical SHA, verifies commit identity and the `astrid/installer/core.py` object, then executes `git archive --format=tar "$release0_agent" astrid >/dev/null` before tests. All eight shards receive the authenticated historical object, irrespective of future shard reassignment.

**Proof actually performed on candidate:** PR diff and exact base/head/read-back confirmed one changed workflow file, 13 added lines, no changed test, assertion, pin, skip, xfail or product implementation. The isolated added shell body passed **`bash -n`** syntax check in a separate local container. Position checks place source verification after checkout and before unit pytest. **Not performed:** full workflow YAML parse against actual candidate bytes in a worker checkout, real `git fetch`/archive, focused tests, independent N reviewer, or hosted candidate XML. The available local worker has no DNS to GitHub; syntax is not an execution proof.

## Required gates, ownership and next step

Independent **N-class** review must record an actual separate reviewer and actual model provenance, and check the locked fixture SHA, Git source trust, script syntax/placement, and scope. Then genuine GitHub-capable worker/environment execution must prove fetch/archive and focused selectors, followed by a reviewed merge **only into `release/14/plan-39`**, and exact-head hosted CI shard XML showing that all three exact test IDs progress beyond archive setup. This does not imply subsequent rollback and launcher assertions will pass. Do not change the historical pin or skip the tests if they fail downstream.

Existing draft [PR373](https://github.com/banodoco/astrid-agent/pull/373) (Windows security selectors), [PR374](https://github.com/banodoco/astrid-agent/pull/374) (Lanes historical trees), and [PR375](https://github.com/banodoco/astrid-agent/pull/375) (macOS-15 provenance) are separately **open, unmerged and without independent submitted review or hosted candidate proof**. Plan38/55 **WAITING**, Release15 **excluded**. The Runtime clip candidate remains **uncommitted 25 passed/2 failed**, pending a genuine owner ruling on exact retry versus CAS required-history integrity; no bypass or weaker assertion. Formal **G1/G2 incomplete; RS1 0/1**. No owner/token/authentication workaround, manual workflow dispatch, other-session cancel/rerun, main/release-main push/merge, `inputs.md` or task-checkbox modification.
