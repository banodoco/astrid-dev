# Release 14 Plan 39 — wave 0 integration and qualification

16 November 2026. Accountable manager: ChatGPT `/root`, run
`release-14-g0-20261116`. The owner's instruction authorizes G0 record repair,
coordinated plan-branch integration, and concurrent G1, SF3a and GL execution
with manager branch review. The next checkpoint is wave-0 review; wave 1 and
release-main/public-main promotion have not started.

## Current result

G0 is complete and recorded in [its evidence](release-14-g0-worker-smoke.md).
GL and SF3a implementations are merged into `release/14/plan-39`. GL
acceptance is complete: hosted fast checks passed on the integrated head.
SF3a hosted artifact qualification is complete in Runtime and App and is
still in progress in Agent. G1 has an exact-head baseline
inventory with explicit missing evidence; those gaps are not passes.

| Repository | Integrated head | Included work |
| --- | --- | --- |
| Agent | `b8f2692948d1b5987ee2938920f47aace0732792` | [GL #366](https://github.com/banodoco/astrid-agent/pull/366), decreases-only baseline refresh `f7b20146501b2c64813d89769c6ee1084ae190be`, [SF3a #368](https://github.com/banodoco/astrid-agent/pull/368) |
| Runtime | `16d5734a7a7fac6fcecca6d695533370129aba7a` | [G0 #52](https://github.com/banodoco/astrid-runtime/pull/52), [SF3a #53](https://github.com/banodoco/astrid-runtime/pull/53) |
| App | `152492846f622f84f03dd5223ff1b5c8d880dfa2` | [G0 #278](https://github.com/banodoco/astrid-app/pull/278), [SF3a #279](https://github.com/banodoco/astrid-app/pull/279) |
| astrid-dev | `cb884886d25af7138e439e236dfccb6239b56328` before this record | [G0 #762](https://github.com/banodoco/astrid-dev/pull/762), [closure #766](https://github.com/banodoco/astrid-dev/pull/766); G0/RL-0 ticked and W0 credited |

Fresh git fetches confirmed these heads. Runtime and App merge trees equal
their prior G0 trees plus the reviewed SF3a changes. Agent's combined tree is
`39043802763fb59e5490fcd62e6ae1c75e242937`, matching the computed additive merge
of GL, its baseline refresh and SF3a. No task rewrote history or changed any
Plan 55/38-owned test.

## G1: baseline and limits

The read-only baseline is on the unchanged `release/14/main` heads:

- Agent `ab95803ce28fa51eec937b4074f5ec0f0439b98a`.
- Runtime `2537fed24385ec1c24f48a812e09af4bb63fb794`.
- App `0b6ef16152dc3fa11246ccc2007da630c66d1a1a`.

The complete working table and normalized signature inventories are in run
state under `plans/39-green-mains/.otto/runs/release-14-g0-20261116/g1/`:
`baseline.md`, `baseline.json`, `failure-signatures.json`, and
`agent-signature-parse.{md,json}`. Counts in `inputs.md` were not changed.
The seven accessible Agent unit shard logs (1-5, 7-8) reconcile exactly with
their pytest FAILED/ERROR totals; each signature is mapped to a recognized
triage row or explicitly new/unresolved. This does not infer product or
fixture blame from a matching test name.

A-e is confirmed: Ruff rejected a decrease from 2,008 to 2,006. A-f and A-g
are refuted as current CI failures: the Windows native/installer job and both
Python release-wheel jobs passed on the measured Agent head.

| Workflow | Exact-head evidence | Baseline result / gap |
| --- | --- | --- |
| Agent CI | [43888589837](https://github.com/banodoco/astrid-agent/actions/runs/43888589837) | Failing shards and fast checks; shard 6 log recovered in this follow-up (247 failed, 4,913 passed, 6 skipped, 4 errors, 92 successful subtests, 26,330 deselected). Darwin native was cancelled. |
| Agent Lanes | [43888589840](https://github.com/banodoco/astrid-agent/actions/runs/43888589840) | Opt-in and all four integration shards failed; installed wheel passed. Shard 3 finished at 19:36:23 UTC: 81 failed, 372 passed, 1 skipped, 62 errors, 32,163 deselected; read-only [job 133451219876](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451219876). |
| Agent Chat service | [43888589704](https://github.com/banodoco/astrid-agent/actions/runs/43888589704) | Passed. |
| Agent Windows task host journey | [43888589737](https://github.com/banodoco/astrid-agent/actions/runs/43888589737) | Both hosts fail at unsupported `astrid packs list --json`; A-h. |
| Runtime CI | [43888599361](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361) | Five failed jobs. Sandbox IDs/counts are retained; most extracted error messages are unavailable and are marked unknown/new. |
| Runtime Nightly | No run found at `2537fed` | The latest scheduled run is on another main SHA and is not evidence for this release head. |
| App Tests | [43883626058](https://github.com/banodoco/astrid-app/actions/runs/43883626058) | Passed. |
| App Lanes | [43883625781](https://github.com/banodoco/astrid-app/actions/runs/43883625781) | Checkout lane lacks Playwright Chromium; quick journey uses a different source tuple including Runtime main. |
| App E2E | [43883625971](https://github.com/banodoco/astrid-app/actions/runs/43883625971) | Six failed jobs; one default-project failure is explicitly unattributed rather than assigned an invented ID/cause. |
| App Direct Journey | No run found at `0b6ef16` | The latest scheduled run is on another main SHA and is not evidence for this release head. |

The extra Runtime G0 macOS live-watchdog failure remains unresolved and is
not confirmed flaky; its exact comparison is in G0's evidence. The 79
pre-existing Agent structure findings remain with cause-specific triage for
[astrid-dev #647](https://github.com/banodoco/astrid-dev/issues/647). GL changes
the gate policy; it does not accept those findings into the baseline.

The previously unavailable exact-head Agent unit-shard-6 log became readable on 16 November: [job 133426797162](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797162), with 247 failures and 4 errors in its pytest final summary. This restores the missing log access, **not** a green test result or a completed G1: exact-head Runtime Nightly and App Direct Journey have no runs, and unreconciled Runtime signature details are still explicitly unknown. The original G1 inventory in non-git receipts retains its observed-at timestamp and was not retrospectively edited to claim full coverage.

## GL: reviewed behavior and focused proof

[Agent #366](https://github.com/banodoco/astrid-agent/pull/366) merged at
`347dc197ec040d644a8120646966c58bbea7873a`. Ruff and mypy count reductions pass
with improvement messages; configured increases still fail. Resolved structure
entries pass, while every new structure violation still fails. Tests retain
regression assertions and adapt only the deliberately changed resolved-entry
policy from GL's task specification.

- Actual Ruff gate: 2,006 findings against 2,008; exit 0, improvement 2.
- Candidate focused file: 24 passed, 2 failed; untouched base: 17 passed,
  2 failed. The same two real-tree structure checks fail on both.
- Base and candidate structure commands both reported 102 current findings,
  79 new relative to the old baseline and 2 resolved. New lists are identical.
- Initial mypy checks used an incomplete environment. A Python 3.13 attempt
  lacked YAML stubs and had incompatible NumPy stubs; the first Python 3.11
  check also lacked installed Runtime/client and VibeComfy dependencies.
  Those are diagnostic attempts, not the final matching-environment proof.
- Corrected proof used Python 3.11.14, installed pinned Runtime/client
  `6855dfa8df65cf8ae4c002b57134d6505493c17c`, VibeComfy
  `dba38f8644c46f652376f2cd5112ea161e40f09b`, types-PyYAML, NumPy 2.3.5,
  the three declared checkout variables and no `PYTHONPATH`. Actual mypy
  against the committed GL baseline passed, with no blocking regressions.

The manager refreshed baselines once on the plan branch, in `f7b20146`,
separately from the task PR. Only proven reductions were applied: Ruff total
2,008 to 2,006; 50 Ruff file/code limits and 73 mypy file/code limits lowered;
two resolved structure entries removed. No file/code limit increased and no
new structure violation was accepted. The retained structure baseline has
23 entries; the 79 new findings still fail it. Real Ruff and mypy commands
passed against the refreshed baseline. The [hosted fast-check job](https://github.com/banodoco/astrid-agent/actions/runs/43934820640/job/133536534666)
then passed on `b8f26929`: Ruff current=baseline=2,006; mypy passed; import
cycles reported eight existing two-cycles and zero new cycles; collection
passed. This completes GL acceptance and does not imply a green full suite.

## SF3a: reporting changes and local proof

The manager read all workflow and configuration changes, kept existing test
commands/selection intact, corrected a misplaced Agent result-directory
variable before publication, and restored the original App command/environment
behavior. JUnit output is optional in local Vitest configs and keeps the
SkipGuard reporter. Existing Agent duration artifacts are unchanged.

The scoped jobs write JUnit, print its counts, and upload it even after pytest
or Vitest fails. No XML produces an explicit failure instead of a fabricated
empty success. Artifacts retain 90 days. Push coverage adds only the exact
`release/14/plan-39` branch; existing PR filters/conditions remain intact.
Runtime's sandbox keeps its existing seccomp profile, read-only source mount
and selectors and adds a separate writable results mount.

| Local proof on final task bytes | Result | XML counts verified |
| --- | --- | --- |
| Agent `tests/test_installer_platforms.py::test_ffmpeg_probe_checks_every_required_encoder_and_analysis_filter`, with `-q -rA --junitxml=<output>` | 1 passed, exit 0 | 1 test, 0 failures/errors/skips |
| Runtime `tests/test_platform.py::test_owner_only_applies_and_checks_private_file_and_directory_modes`, same reporting flags | 1 passed, exit 0 | 1 test, 0 failures/errors/skips |
| App Vitest `src/shared/lib/updates/updateStatus.test.ts`, default final config and `VITEST_JUNIT_OUTPUT` | 5 passed, exit 0 | 5 tests, 0 failures/errors/skips |
| App boundary Vitest `src/sdk/__tests__/sdk-boundary.test.ts`, boundary final config and `VITEST_JUNIT_OUTPUT` | 335 passed, exit 0 | 335 tests, 0 failures/errors/skips |

Node was 20.19.4/npm 10.8.2 for App. Strict duplicate-key YAML parsing and
whitespace checks passed for all five workflows; `sh -n` passed for the
sandbox runner. Its local mount/argument check used stub Docker and synthetic
XML only; it is not claimed as a real sandbox suite result. Root parsed the
real focused XML files and matched their counts to test logs.

## Hosted qualification

These are the integrated plan-head runs; no later product push may replace
them while they qualify the batch:

| Repository / workflow | Run | Head | Current acceptance |
| --- | --- | --- | --- |
| Agent CI | [43934820640](https://github.com/banodoco/astrid-agent/actions/runs/43934820640) | `b8f26929` | Fast checks passed; Windows and failed Darwin artifacts verified; unit artifacts pending. |
| Agent Lanes | [43934820639](https://github.com/banodoco/astrid-agent/actions/runs/43934820639) | `b8f26929` | Running; failed integration shard 1 artifact verified; shards 2-4 pending. |
| Runtime CI | [43933604506](https://github.com/banodoco/astrid-runtime/actions/runs/43933604506) | `16d5734a` | Completed with five failed jobs; every scoped CI job has a downloaded, verified artifact. |
| Runtime Nightly | [43933606695](https://github.com/banodoco/astrid-runtime/actions/runs/43933606695) | `16d5734a` | Failed; its integration artifact is verified below. |
| App Tests | [43933616087](https://github.com/banodoco/astrid-app/actions/runs/43933616087) | `15249284` | Completed successfully; both Vitest XML files downloaded and verified. |

Downloaded Runtime ZIP contents, also independently parsed by root:

| Artifact ID / job | XML tests | Failures | Errors | Skips | Log result |
| --- | --- | --- | --- | --- | --- |
| `14259418001`, Ubuntu portability | 662 | 7 | 0 | 45 | 610 passed, 7 failed, 45 skipped |
| `14259078598`, macOS portability | 662 | 8 | 0 | 59 | 595 passed, 8 failed, 59 skipped |
| `14259529280`, Ubuntu unit | 9626 | 77 | 1010 | 39 | 8,440 passed, 77 failed, 1,010 errors, 26 skipped, 13 xfailed, 60 subtests passed |
| `14259484859`, macOS unit | 9626 | 73 | 1010 | 143 | 8,340 passed, 73 failed, 1,010 errors, 130 skipped, 13 xfailed, 60 subtests passed |
| `14261695421`, sandbox process control | 9550 | 82 | 1014 | 39 | 8,355 passed, 82 failed, 1,014 errors, 26 skipped, 13 xfailed, 60 subtests passed |
| `14259903958`, Nightly integration | 667 | 39 | 571 | 20 | 37 passed, 39 failed, 571 errors, 20 skipped; 9,587 deselected are outside the XML count |

Each archive contains the expected XML. Both unit files report 9,626 in
their testsuite aggregate but contain 9,566 testcase elements: 60 successful
subtests contribute to the aggregate without separate testcase elements.
Sandbox similarly reports 9,550 in its aggregate and 9,490 testcase
elements. JUnit skips combine ordinary skips and the 13 xfailed cases
(39 on Ubuntu/sandbox, 143 on macOS). With those explicit semantics, XML aggregates reconcile to
pytest summaries. Portability and Nightly testcase-element counts equal
their aggregates. No cases or counts were fabricated to normalize this. Summary/upload steps succeeded while the underlying tests
remained red. Runtime reporting acceptance is complete across all six scoped jobs, including
failed jobs. All six expire on 14 February 2027, consistent with the declared
90-day retention.

App artifact `14260289801`, `test-results-vitest-all-Linux`, also expires on
14 February 2027. The archive was downloaded, and root parsed both XML files to confirm
20,870 App Vitest cases and 335 SDK boundary cases, each with zero failures,
errors or skips. The suite aggregates, literal testcase counts and logged
summaries agree. Its ZIP SHA-256 is
`85115f785bfda0a02518d629e831f13b12c9ebcef8c56137659444419e141f6d`.
The original `npm test` command remains intact; these XML files cover its
Vitest runs, not the separate Node test runner. App reporting acceptance is
complete. The `npm test` step took 993.767 seconds versus 752.545 seconds in
exact-base run `43883626058` (1.321 times); Vitest's own duration was 896.82
versus 682.95 seconds (1.313 times), both below the 1.5-times hang threshold.

Agent artifacts downloaded and independently parsed by root so far:

| Artifact ID / job | XML tests / testcase elements | Failures | Errors | Skips | Log reconciliation |
| --- | --- | --- | --- | --- | --- |
| `14259214357`, Windows native and installer | 112 / 112 | 0 | 0 | 0 | 15 installer + 40 host-recovery/services + 36 Remotion + 21 native passed |
| `14260398808`, Darwin native | 55 / 55 | 13 | 1 | 0 | 41 passed + 13 failed + 1 error; 31,235 deselected are outside the XML count |
| `14260249942`, Lanes integration shard 1 | 516 / 516 | 36 | 0 | 0 | 480 passed + 36 failed; 32,170 deselected are outside the XML count |

All three have 90-day expiry on 14 February 2027. The failed Darwin and
integration jobs still summarized and uploaded their results. At 19:23 UTC,
Agent unit shards 2-7 were active, shards 1 and 8 queued, and integration
shards 2-4 active. Those artifacts remain NO-RESULT until observed. Existing
duration artifact configuration is unchanged; actual unit duration uploads
also await those jobs. A failed test-result artifact can satisfy SF3a
reporting proof; it never means that its test passed or that Release 14 is
qualified.

## Wave-0 qualification follow-up (16 November, 20:07 UTC)

Agent's exact-head [CI 43934820640](https://github.com/banodoco/astrid-agent/actions/runs/43934820640) now has completed, independently downloaded JUnit archives for unit shards **3, 4, 5 and 8**, with their unchanged three-day duration archives. Each ZIP SHA-256 agrees with GitHub's advertised artifact digest, and each test suite aggregate agrees with its job's logged XML summary:

| Shard | JUnit artifact | Tests / testcase elements | Failures | Errors | Skips | Pytest result | Duration artifact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | `14263779551` | 1,861 / 1,861 | 31 | 0 | 0 | 1,830 passed; 31 failed | `14263564649` |
| 4 | `14265361873` | 2,061 / 2,061 | 28 | 19 | 0 | 2,014 passed; 28 failed; 19 errors | `14264457941` |
| 5 | `14265381355` | 2,416 / 2,416 | 95 | 107 | 0 | 2,214 passed; 95 failed; 107 errors | `14265226633` |
| 8 | `14265546026` | 4,114 / 3,912 | 97 | 2 | 25 | 3,788 passed; 97 failed; 2 errors; 25 skipped; **202 subtests passed** | `14265361415` |

Shard 8's 202 successful subtests contribute to the XML suite aggregate without separate testcase elements; the different numbers are intentional and reconcile. These were **failed product test jobs**, not passing checks. Their report-summary and upload steps succeeded. The JUnit files expire on 14 February 2027; duration files on 19 November 2026. Agent Lanes shard 2 `14262871202` additionally has 516 tests, 78 failures, 172 errors, 266 passed; its result XML and logged count reconcile, with expiry 14 February 2027. Integration shards 3/4 and unit shards 1/2/6/7 remain **not qualified** until their exact-run jobs finish and both types of unit artifact have been checked.

Branch custody observation: Runtime `release/14/plan-39` was subsequently advanced by two commits to `4fe2c0b8`, and App by two to `e94d7ab5`. Those newer trees are **not** the exact heads qualified by the Runtime/App SF3a receipts above (`16d5734a` and `15249284`). This records concurrent changes without resetting them, replacing the exact-head proof, or asserting that later tests passed. No new Agent, Runtime, App or `release/14/main` commit was made in this records follow-up.

Routes used: N workers for G1, GL and SF3a, with manager review and integration.
No outside per-task verification gate was added, as the owner instructed.
