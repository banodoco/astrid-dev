# Release 14 Plan 39: first repair batch and cause assessment

Recorded 16 November 2026. This is a review package for local candidates, not a claim that the repositories, phase 1, or Plan 39 are complete.

## Result and authorization

The failures have several kinds of cause. Some are CI setup or reporting faults; some are tests that still enforce deliberately retired contracts; at least one independently reproduced Agent failure exposes a product defect. Treating all red tests as obsolete would conceal that defect.

The user's follow-up authorizes repairing in-scope product and test causes. The earlier remote-write restriction still permits only `banodoco/astrid-dev:p39/g1`. Consequently, this package contains complete product patches without pushing product branches, opening product PRs, merging, or dispatching workflows. No test was deleted or loosened to conceal a defect, no existing product pin was changed, and `inputs.md` is unchanged. Plan 38 and Plan 55 owned tests remain waiting. Release 15 tasks remain excluded.

The governing [Release 14 scope](../../plan.md#release-14-scope) and [wave order](../../tasks.md#release-14-waves) require integrated phase-1 hosted results, G2, and RS1 before phase-2 implementation. The independent review of these local candidates was a pre-publication code review; it did not perform or consume the formal RS1 round.

## Exact candidates

All three `release/14/main` heads were rechecked during packaging and still matched the bases below. Local product working trees were clean after committing. The patches include full object indexes and were checked with `git apply --reverse --check` against their exact candidate trees.

| Repository | Exact base SHA | Local candidate SHA | Reviewable patch | Size |
| --- | --- | --- | --- | --- |
| astrid-agent | `ab95803ce28fa51eec937b4074f5ec0f0439b98a` | `9e41487ac6d942930d4c699e24fd378c0a0fbaf0` | [astrid-agent.patch](patches/astrid-agent.patch) | 9 files, +393 / -41 |
| astrid-runtime | `2537fed24385ec1c24f48a812e09af4bb63fb794` | `71708140bec9e2ffaf5c43e96136292ef6883402` | [astrid-runtime.patch](patches/astrid-runtime.patch) | 12 files, +490 / -40 |
| astrid-app | `0b6ef16152dc3fa11246ccc2007da630c66d1a1a` | `d10c96636291410a24f308051141105b38158e92` | [astrid-app.patch](patches/astrid-app.patch) | 8 files, +191 / -53 |

These are local commit identities, not published product commit links. [candidates.json](candidates.json) records every changed path and each patch's SHA-256. To inspect or apply a patch, use a clean checkout of that repository at the listed base; `git am` may produce a different commit SHA because it creates a new committer identity and timestamp.

The astrid-dev base is `2770aa79e8d9325c7891294609c746963cc4776e`. Its only existing-file repair removes four obsolete duplicate `not yet cut` Plan 39 rows from `releases/14.md`, retaining the existing exact-SHA rows. The unchanged strategy validator reproduced those duplicate errors on the base. After the data repair, its 24 strategy tests pass ([proof](proof/dev-strategy-tests.log)); no validator was weakened.

## Baseline retained, including its gaps

The frozen G1 observation covers **17:26:09–17:26:12 UTC on 16 November 2026**. The [full G1 baseline report](https://chatgpt.com/library?file_id=libfile_fde3_f-1aa7139eb6ec81919e9ca5d88c1f2b5f_6b5886b89d0881919e73a1e3270986c8&account_id=personal) contains each available failing-job summary, the distinct literal error messages and counts, triage mappings, ownership holds, exact heads and run/job links. Its status is **incomplete evidence, not marked done**. A cancelled job, an unfinished job, and an absent exact-head scheduled run are not passing evidence.

At that cutoff there were **52 jobs: 27 failed, 17 passed, two running, one cancelled, and five skipped**. Four skips were expected; the fifth was the required Agent `unit` aggregate, which never ran after failed dependencies. The logs yielded **4,935 failure/error records** and **810 per-job message groups**. Those are occurrences and literal-message groups, not 4,935 or 810 independent root causes. They include 4,932 test failure/error records, one Ruff-gate failure and two Windows journey command failures.

| Repository / workflow | Run ID (attempt 1) | Frozen observation |
| --- | --- | --- |
| Agent CI | [43888589837](https://github.com/banodoco/astrid-agent/actions/runs/43888589837) | All eight unit shards failed; fast checks failed; Darwin cancelled; required aggregate skipped |
| Agent Lanes | [43888589840](https://github.com/banodoco/astrid-agent/actions/runs/43888589840) | Three completed failures, installed wheel passed, integration shards 3 and 4 running |
| Agent Chat service | [43888589704](https://github.com/banodoco/astrid-agent/actions/runs/43888589704) | Both jobs passed |
| Agent Windows task host journey | [43888589737](https://github.com/banodoco/astrid-agent/actions/runs/43888589737) | Both shells failed on unknown command `packs`, exit 2 |
| Runtime CI | [43888599361](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361) | Five failed, four passed, one expected skip |
| Runtime Nightly | No exact-head run found | NO RESULT |
| App Tests | [43883626058](https://github.com/banodoco/astrid-app/actions/runs/43883626058) | Three passed, two expected skips; Vitest 20,870 tests passed |
| App Lanes | [43883625781](https://github.com/banodoco/astrid-app/actions/runs/43883625781) | Checkout and quick journey failed; three installer jobs passed |
| App E2E | [43883625971](https://github.com/banodoco/astrid-app/actions/runs/43883625971) | All six jobs failed; 82 test failures |
| App Direct Journey | No exact-head run found | NO RESULT |

The original A-e assumption is refuted: Ruff findings had fallen from 2,008 to 2,006, and the equality-based gate rejected the improvement. A-f's Windows custody problem and A-g's wheel import problem were absent from their completed jobs at these exact heads: Windows native/installer passed 112 tests and both wheel smoke jobs passed. That does not make the separate Windows task-host journey green.

The frozen ownership holds are Agent Plan 55: 45 records; Runtime Plan 55: three; Runtime Plan 38: 44. One further ownership classification is unresolved. These counts remain separate from repairs in this package.

During packaging, Lanes shard 4 was observed completed at 17:52:43 UTC, while shard 3 still ran. Its [dated supplement](baseline-supplement/lanes-integration-4-133451220087.md) records **99 failed, 391 passed, 32,163 deselected, eight warnings and 26 errors**, with [all 125 outcome IDs and 55 complete message groups](baseline-supplement/lanes-integration-4-133451220087.json). These reconcile to 43 distinct first-line signatures. Root independently matched every outcome/ID pair to the outer pytest summary; nested captured pytest output was not counted twice. These signatures are newly observed A-b / AT1 findings, still unclassified as independent causes. No exact IDs matched the audited Plan 38/55 inventories. This supplement does not silently change the frozen cutoff or its totals.

## Causes, changes, and proof

### Agent

| Card | Cause and candidate change | Bounded proof | Remaining acceptance |
| --- | --- | --- | --- |
| GL | The Ruff total-count gate rejected improvements, and structure rejected removed findings. Allow these reductions; retain Ruff total growth, existing per-file/code regressions, and every new structure finding as failures. Mypy already used per-file/code-only gating. No baseline JSON was rewritten. | Real Ruff output is 2,006 in both cases: [base](proof/agent-gl-ruff-base.log) exits 1, [candidate](proof/agent-gl-ruff-candidate.log) exits 0. [15 focused comparator cases](proof/agent-phase1-gl-cases-final.log) pass. | Hosted fast checks has not passed. The [candidate structure check](proof/agent-phase1-gl-candidate-structure.log) still rejects 79 existing additions; the [base](proof/agent-phase1-gl-base-structure.log) also reports them. Two removals are now informational. |
| SF3a | Add JUnit results to unit shards, Darwin, the four Windows pytest invocations and integration shards, with always-run uploads and 90-day retention. Preserve existing selectors and duration artifacts. | Workflow/lane tests: [base 23 passed](proof/agent-phase1-workflows-base.log), [candidate 43 passed](proof/agent-phase1-workflows-focused.log). | Hosted artifact existence and per-test count reconciliation are still required. An early failure in a sequential Windows command can prevent later commands from running. |
| K1a | The `unit` aggregate was skipped after dependency failure. Run it with `always()` and reject any non-success dependency. Add an empty exact-node quarantine registry with strict execution, issue/owner/expiry requirements, a 14-day maximum and a ten-test cap. | [31 final guard tests](proof/agent-k1a-review-verification.log) pass, including an actual subprocess regression for `declared_xfail(...)(run=False)`. Workflow tests cover all 16 dependency result combinations. | The [full policy test](proof/agent-phase1-k1a-skip-policy-final.log) remains 21 passed / 1 failed on 55 inherited direct `skip`/`importorskip`/`skipif` callsites; its exact list matches [base](proof/agent-phase1-k1a-base-skip-policy.log). No active quarantine was added. Hosted cancellation proof is outstanding. |
| AE2 | Two VibeComfy checkout sources were inconsistent. Both now name `banodoco/VibeComfy`, verify the engine revision and print it in the step summary. | Reviewed workflow changes; the historical Runtime commit `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` was already fetched by the base workflow and is present in the repository. | Full Lanes execution and actual checkout summaries remain unproved. No duplicate historical-fetch change was made. |
| AE1 | The old module-level missing-tool collection abort is absent from the measured eight shards. | The [no-tool local probe](proof/agent-ae1-no-tools.log) reports six `pack_build_tools` deselections and no collection abort. | Its process exits 5 because no test ran. It is not passing behavioral proof; Darwin had no result, and the tools-present path remains to be proved. |

### Runtime

| Card | Cause and candidate change | Bounded proof | Remaining acceptance |
| --- | --- | --- | --- |
| RE1 | CI jobs did not consistently install the pinned Agent or expose `ASTRID_CHECKOUT`. Add explicit sibling checkouts, pin verification and environment wiring; pass a read-only Agent mount into the sandbox, then copy it into the owned container workspace. | With the exact pinned Agent, the representative [base checkout-unavailable failure](proof/runtime-re1-base.log) becomes a [missing SDK import](proof/runtime-re1-b05.log). | This proves the first setup obstruction changed, not that the test passes. Hosted unit/boundary/portability/sandbox qualification remains necessary. |
| RE2 | Tests fell back to a private frozen Agent source. Use the shared checkout resolver. The manual private qualification driver now requires an explicit artifact directory, preserving all five selected tests. | The same exact native-clip selector changes from [private-source unavailable](proof/runtime-re2-exact-base.log) to [missing `astrid.sdk.timeline.capture`](proof/runtime-re2-candidate.log). The manual driver [refuses absent private artifacts explicitly](proof/runtime-re2-private-artifacts-refusal.log). | The pin/API mismatch is unresolved. Private artifacts were not available, so that driver has no passing proof. |
| RE3 | Historical archive fixtures ran in shallow repositories. Fetch full Runtime and Agent history in the actual unit/sandbox/Nightly lanes; fetch and verify historical Agent commit `321cef4b8c89a4a938cb9ede41ba6a5444cf1b62`. Missing archive errors now name the SHA and fetch remedy. | In the shallow checkout, the [base log](proof/runtime-re3-shallow.log) has the opaque archive error; [snapshot](proof/runtime-re3-snapshot-candidate.log) and [v33](proof/runtime-re3-v33-candidate.log) candidate probes name the missing commit. | Full-history passing proof is still hosted work. A local attempt to unshallow a partial/promisor checkout could not retrieve all promised objects; it is not counted as qualification. |
| RE4 | Contract tests depended on a globally discoverable `tsc`. CI installs Node 22 and the locked TypeScript package; both tests resolve that local compiler. The sandbox installs the same package before pytest. | Two exact compiler selectors [pass without global `tsc`](proof/runtime-re4-direct-node22.log), compared with [base failures](proof/runtime-re4-base.log), using Node 22.23.5. | The two whole contract files and hosted Ubuntu acceptance are not established by those two selected passes. |
| SF3a | Unit, portability and Nightly did not persist comparable per-test results. Add `-rA`, JUnit and always-run uploads. The disposable sandbox uses a dedicated writable results mount, preserving its pytest exit code. | Code review plus bounded stub-Docker/entrypoint checks, described below. | No live Docker or hosted per-test artifact count comparison was available. |
| K1b | Existing quarantine declarations lacked required metadata; ten declaration groups actually covered 20 exact tests. Validate exact nodes, strictness, issues, owners, expiry and cap, without globally aborting collection. | [12 synthetic and existing contract tests](proof/runtime-k1b-synthetic-final.log) pass. The [real inventory guard fails](proof/runtime-k1b-inventory-blocker-final.log) with 20-over-10 and missing metadata. | Substantively incomplete. Existing node IDs, reasons, exception contracts and strictness were preserved. No issue, owner or expiry was invented and no cap was raised. |

Runtime focused proofs use Python 3.12.14 and the exact `tests/astrid-agent.pin`, `b05ac03a5bcab278bccf99d85b49f4037b5dec10`, with that Agent's hashed dependency lock. Preliminary probes with a different Agent lock were discarded as qualification. The product pin itself is unchanged.

The Runtime worker reported passing bounded harness checks for argument preservation, paths with spaces, read-only code mounts, writable results, exit-status propagation, Agent `.git` preservation, copying an Agent nested in the source without collision, the `ci` identity/home, and `npm ci` before pytest. These ran as inline scripts; their scripts/output were not persisted. They are therefore reported as limited worker verification, not replayable hosted evidence. `sh -n`, Python compilation and diff checks passed. Docker is unavailable here.

### App

| Card | Cause and candidate change | Bounded proof | Remaining acceptance |
| --- | --- | --- | --- |
| PE1 | The base already selected checkouts from the install manifest; the candidate verifies the actual checked-out SHAs and their consistency with local locks. Local and served-release coherence are validated separately. | [21 release/pin tests](proof/app-phase1-pe1-reviewed.log) and [four manifest tests](proof/app-phase1-manifest-reviewed.log) pass. They include one-sided pin changes, selected-ref locks and a coherent served tuple that differs from the current checkout. | Hosted Lanes summaries and the specified throwaway negative PR remain outstanding. No actual pin changed. |
| K1c | Three obsolete drag-test name allowances could permit expected failures without metadata. Remove those allowances; the current drag tests already use ordinary `it()`. Preserve the four actual Direct Journey exceptions. | Worker focused checks: 21 known-failure tests pass; CLI reports four allowed entries and zero forbidden entries; the Vitest skip-guard file passes 25 tests. | These worker outputs were inline, not retained in this package. The four existing entries still count toward the cap and retain their existing expiry of 25 November. Integrated proof remains outstanding. |
| SF3a | Vitest had no persisted JUnit stream. Add the builtin JUnit reporter when `VITEST_JUNIT_OUTPUT` is set and always upload its output. Preserve the ordinary reporters and skip guard. | The focused worker run had 25 console passes and 25 JUnit testcases. | A full hosted Vitest result count reconciliation is pending. No browser suite was run locally. |

App probes used Node 20.19.4. For networked manifest reads only, the existing G0 proxy preload was required because direct Node fetch could not resolve `raw.githubusercontent.com` in this workspace. The requests used the actual network responses, not mocked pin responses. Runtime/App canonical worker wrappers are part of the independently active [G0 PR 762](https://github.com/banodoco/astrid-dev/pull/762); they were not duplicated or represented as merged here. Direct focused results do not claim the task's `ENV-PASS` smoke acceptance.

## Test defects versus product defects

| Finding | Classification and evidence | Correct next repair |
| --- | --- | --- |
| Agent registry source precedence | **Reproduced product defect.** `_registry_probe` promises caller-tree precedence but only inserts the root when absent; an intended root already later in `sys.path` loses to a foreign tree. Both parameters of `test_source_probe_prefers_caller_tree_already_on_search_path` fail against unchanged product code ([log](proof/agent-registry-source-product-bug.log)). Also tracked in [issue 757](https://github.com/banodoco/astrid-dev/issues/757). | Separate reviewed `AT1.<n>.bug` cause card after G2/RS1. Correct source ordering and retain origin/custody refusal checks. Do not weaken or delete the exposing test. |
| Runtime media metadata conflict | **Stale test expectation against an intentional contract change.** [Commit a1f7fa4972c579c5673e01e6a83171036512029d](https://github.com/banodoco/astrid-runtime/commit/a1f7fa4972c579c5673e01e6a83171036512029d) made descriptors association-specific while CAS identifies bytes. The existing test still expects identical bytes with different descriptors to conflict. A [focused contract probe](proof/runtime-metadata-contract-probe.log) yields one CAS object, two generations, distinct preserved descriptors and valid integrity. | RT6 test correction must assert the intended associations and preserve digest, permission, size and integrity protections. The probe used the existing unit fixture's disabled decoder; it is not real codec validation. No test was changed in this batch. |
| App fake Runtime routes | **Strong test-harness evidence, browser confirmation pending.** Source tracing finds no fake handler for `GET /api/runtime/packs/inventory`; the current `/v1/projects/.../timelines/.../commits` read reaches a fake dispatcher exposing composition revisions instead; the timeline helper still posts to an intentionally retired writer that returns 410. These match failures in [E2E 43883625971](https://github.com/banodoco/astrid-app/actions/runs/43883625971). | PT2 ports the fake server and fixture boot sequence to current contracts, then proves exact browser cases. Do not suppress console/request failures, increase timeouts blindly, or change production APIs to satisfy a stale fake. No phase-2 change made. |
| Agent clip entrance `DID NOT RAISE` | **Unresolved.** Initial history inspection was insufficient to settle whether the old-field acceptance is intentional or a product regression. | Trace the contract and reproduce under its exact fixture before changing either test or implementation. |

This is not an exhaustive classification of every failing test. The frozen baseline has 810 literal message groups, which must be clustered again after setup repairs using actual integrated per-test results. Missing setup prerequisites can mask later, unrelated failures.

## Review and remaining work

Independent pre-publication review raised four concrete findings, all corrected in the committed candidates: App served-release checks accidentally inheriting local locks; Agent `run=False` bypassing quarantine execution; missing sandbox `npm ci`; and historical checkout provisioning missing from the actual Nightly integration lane. Final review found no remaining blocking code finding within the reviewed candidate scope. It did not certify task completion or hosted behavior.

The first-wave acceptance gaps are explicit:

- G0 remains coordinated through PR 762. G1 retains unfinished/cancelled/absent-run and log-access gaps; no checkbox was marked complete.
- GL still has 79 structure additions; K1a still has 55 inherited direct-call offenders; K1b still has 20 quarantined tests and missing metadata. These need disposition and repair, not merely a green-report label.
- AE1 still needs Darwin and tools-present proof. AE2, RE1, RE3, PE1 and SF3a principally require integrated hosted evidence. RE2 exposes an unresolved Agent API mismatch; RE4's full-file acceptance remains outstanding.
- G2 must read actual `release/14/plan-39` heads and map every remaining failure. RS1 then checks that mapping and the integrated repairs before phase 2 begins. Neither has run.
- Phase-2 cause repairs, Windows journey, App fake Runtime/E2E, required checks, nightly reporting, result comparison and shard-budget work are still open. Plan 38/55 rows stay waiting for their owners.
- Release completion still requires the stipulated hosted checks and three consecutive green nights on each `release/14/main`. No local evidence substitutes for that.

The concrete next publication decision is permission to use isolated product task branches and PRs targeting `release/14/plan-39`, integrate the reviewed batch under the plan's review protocol, and obtain one full hosted run per repository. The prior instruction allowing pushes only to astrid-dev `p39/g1` does not authorize those actions. Promotion to `release/14/main`, publication, and repository settings are separate and have not been requested or performed.

## Evidence limitations

The original Agent shard-6 log exceeded the connector's transport limit. Its complete outer pytest failure/error summary was recovered through the browser, but the full raw log was not retained; it cannot support claims about every inner traceback. Darwin's cancelled job had empty steps and an unavailable log. Scheduled Runtime Nightly and App Direct Journey had no exact-head run at the frozen cutoff. Lanes shard 3 was still running during packaging. No run was cancelled or restarted to manufacture a result.

No live Docker, full local suite, hosted candidate run, browser E2E run, branch-protection check, merge, promotion or product push is represented by this package. Proof files are retained exactly as captured; transient paths and timing differ between base and candidate. Counts quoted above refer to their named selectors, not extrapolated coverage.
