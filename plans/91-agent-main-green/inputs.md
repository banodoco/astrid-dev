# Inputs — Agent main green

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah asked on 23 November 2026, in session https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV, for a project focused only on getting the Agent to green, broken off from Plan 39 (All three mains green). The end state is Plan 39's, for one repository: every Agent workflow on `main` green and kept green. Where it lands and when it starts are D1 and the owner's go.

**Prior art:**
- [Plan 39](../39-green-mains/plan.md), its [triage](../39-green-mains/inputs.md#agent-ci-lanes-windows-task-host-journey), its [handover](../39-green-mains/handover.md) and its [Release 15 ceiling](../39-green-mains/tasks.md#release-15-ceiling), which lists the Agent's measured families and their owner rows.
- The [Release 14 run board](../../releases/14/run.md): the Agent packets that landed on `release/14/plan-39` (R14-P39-01, -07, -12, -13, -14, -17, -34, -35), the ones moved to Release 15 (R14-P39-10, -18, the renderer-input and custody rows), and rulings 6a, 10 and 13.
- The [Release 14 brief](../../releases/14.md): Plan 39 was split on 21 November, `release/14/plan-39` was not merged whole, and Release 14 published on "no new red against Release 13" rather than green.
- The latest Agent `main` runs, read on 23 November 2026 at `c0ad6b54aadd21630d98bb5039613e37efe92a8f`: [CI 45028846987](https://github.com/banodoco/astrid-agent/actions/runs/45028846987), [Lanes 45028847122](https://github.com/banodoco/astrid-agent/actions/runs/45028847122), and Chat service, Windows task host journey and Windows runtime retention, all green on the same commit. Every failed job's full log was downloaded and its pytest summary and `FAILED`/`ERROR` lines grouped by message ([clusters](#failure-clusters-22-november-2026)).
- Negative finding: the committed inherited-red list for Release 14 (`releases/14/evidence/inherited-red.json`) is empty, so there is no committed record of which Agent IDs were red at publication. AG-0 makes one.

**Approach:** Plan 39's approach, for one repository: seal what is red, stop it getting worse, fix by root cause, keep it green with what exists. Splitting it off:
- lets the Agent reach green without the Runtime's and the App's work, which have their own causes and owners;
- gives the Agent one manager, which Plan 39's handover found was what Release 14 lacked ("two workers, one task list, no shared record");
- puts the ceiling on the Agent early in a release in which five other plans change it.

Rejected:
- leaving the Agent in Plan 39. The plan is in no Release 15 lane and has no owner ([Release 15 run board](../../releases/15/run.md)); its estimate is 30–60 days for three repositories;
- a fresh "known failures" baseline that never falls. It keeps red as normal;
- quarantining the long tail to reach green sooner. The quarantine cap is ten (D9), and the long tail is hundreds;
- landing straight on Agent `main` outside a release. Product work lands through `release/<NN>/main` ([project format](../../docs/project-format.md)).

**Challenge:** Not needed — the approach and its anti-hiding rules are Plan 39's, which had an advisor review on 9 November 2026 ([record](../39-green-mains/inputs.md#challenge-record)) and ran through Release 14. This plan narrows the scope to one repository and adds no mechanism. RS1 is the check that the long tail is as estimated.

**Proof and limits:**
- **Proof:** each workflow named in [plan.md](plan.md#outcome-and-scope) passes on the final `release/<NN>/main` head on three consecutive nights; the per-ID comparison fails a pull request that adds one red test; the quarantine guard fails on an expired entry or a strict xfail that passes.
- **Limits:**
  - the counts are from one run per workflow, and AG-0 re-measures them on the head the plan branch is cut from;
  - the cluster counts come from grouping error messages, not from fixes, so one cluster may hide more than one cause, and the 249 integration refusals may or may not share the Remotion wiring cause;
  - 16 unit IDs failed on a pytest timeout and may be flaky;
  - `darwin native` was cancelled, so its state is unknown;
  - GitHub-hosted runners only; branch protection is the owner's setting.

**Review rounds:** RS1 at most 1 round, after the safety net and the wiring, because the long tail's size decides the rest of the estimate. Final R at most 2 rounds. The owner confirms.

**Run start:** Pending — no run is authorized. Next: once the owner places the plan in a release (D1) and says go, record the date, the tasks the run covers, the accountable manager session, what it may do without asking (merging its own workers' PRs into `release/<NN>/plan-91` after focused proof), and what still needs the owner's go (the required checks, quarantine entries beyond D9's cap, and landing in `release/<NN>/main`).

## Failure clusters, 22 November 2026

Grouped from the full logs of CI 45028846987 and Lanes 45028847122 at `c0ad6b54`.

**`CI` unit shards, about 1,081 IDs:**

| IDs | Cause | Class | Task |
| ---: | --- | --- | --- |
| 183 | The Runtime is installed into site-packages, and the tests assert it resolves from the checkout (`assert PosixPath('…/site-packages/runtime_protocol/…') == (PosixPath('…/astrid-runtime/…'))`), mostly in `tests/sdk/test_timeline_*_runtime.py` and `tests/editing_conformance/` | env | AG-3 |
| 72 | `R0 requires the copy-only upgrade boundary. Run the install line again.`, mostly `tests/test_installer_busy_fence.py` (54) and `tests/test_local_install.py` (12) | stale tests after a behaviour change | AG-6 (Plan 39 AT1.10, packet R14-P39-18) |
| 62 | `Browser transaction tests require explicit pinned local Node/esbuild inputs: ASTRID_BUILD_TEST_NODE…`, mostly `tests/core/pack/test_transaction.py` (47) | env | AG-4 |
| 45 | `ModuleNotFoundError: No module named 'tests.test_verified_host_launch'` in `tests/core/execution/test_runtime_*_custody_d40.py` | test infra; Plan 38's tests | AG-7 |
| 34 | `KeyError: 'ASTRID_REMOTION_PROJECT_DIR'`, mostly `tests/packs/rendering/test_normal_audio_run.py` | env | AG-4 |
| 31 | Missing resources or staged files (`staged Agent is missing: runtime.lock.json`, `astrid-beta-capabilities.json`, a `tar -xOf` of a package) | env or fixture | AG-4 |
| 18 | `CommitRejected: fork native binding schema changed` | stale fixtures | AG-8 (Plan 39 AT1.34) |
| 8 | `The derived RunPod Lifecycle checkout is not a Git checkout` | env | AG-4 |
| about 628 | The rest, across 232 files: `tests/packs` 154, `tests/core` 113, `tests/scripts` 86 (including `test_pod_jobs.py` 36 and `test_pod_bootstrap.py` 26), `tests/sdk` 65 | unclassified | AG-9, after RS1 |

**`Lanes`, about 790 IDs:**

| IDs | Cause | Task |
| ---: | --- | --- |
| 249 | `Refused: after this edit render and visualize cannot open the result` (203) and `CommitRefused: Render and visualize could not open the timeline after this edit` (46) | AG-5 |
| 76 | A `tests/editing_conformance` native-conformance subprocess exits non-zero | AG-9 |
| 35 | `candidate.timing: legacy word anchor is missing` | AG-9 |
| 21 | `KeyError: 'bridge.parent'` | AG-9 |
| 16 | pytest-timeout | AG-9, paired runs |
| 11 | `duplicate pack id 'generation'` conflicts with a core pack | AG-9 |
| 7 | `undeclared secret environment variable 'FAL_KEY'` (compare [#1254](https://github.com/banodoco/astrid-dev/issues/1254)) | AG-9 |
| 12 | `opt-in`: six C06 saved-artifact readbacks need the saved artifact, and `editorial.arrange` is not discoverable (`tests/test_onboarding_parity.py`) | AG-9 |
| about 360 | The rest | AG-9, after RS1 |

## Owner decisions

| # | Decision | Recommendation |
| --- | --- | --- |
| D1 | Which release the plan lands in | Release 15, as its own lane with one manager. The ceiling (AG-1) protects the other Release 15 plans that change the Agent. If Release 15's cut line moves Plan 39 out, this plan can stay. |
| D2 | Whether Plan 39 is narrowed to the Runtime and the App | **Decided (Hannah, 23 November 2026, this plan's session):** yes. The Agent rows of Plan 39 move here; Plan 39 keeps the Runtime, the App and the cross-repository pieces. |
| D3 | The custody and host-spawn tests Plan 38 owns | AG-7 repairs the missing import so they run. Any that still fail are listed on the ceiling with Plan 38 as owner and do not count against D9's cap of ten, because Plan 38 is unowned and in the draft Release 16. Completion then means green except that named, owner-accepted list. |
| D4 | The Agent's merge-tier required checks | Plan 39's merge tier for the Agent: `CI` (`fast checks`, `unit`, `windows-native-and-installer`, `darwin-native`, `release`, `boundary`), `Chat service` and `Windows task host journey`, turned on for `release/<NN>/main` once AG-1's comparison passes on an unchanged tree, and for `main` at publication. `Lanes` stays release-tier. |

## Source identities

- astrid-agent `main` at `c0ad6b54aadd21630d98bb5039613e37efe92a8f`, the published Release 14; measured above.
- astrid-agent `release/14/plan-39` at `ab95803ce28fa51eec937b4074f5ec0f0439b98a`: the safety-net commits, taken by row (SF3a, GL, GL.1, GL.2, K0, K1a, K2/K3 Agent side), never merged whole.
- Destination: `release/<NN>/plan-91` in astrid-agent, cut from `release/<NN>/main` (Release 15 if D1 is accepted), and in astrid-dev for this plan's records. AG-0 records the cut commits.

## References

- [Plan 39](../39-green-mains/plan.md), its [handover](../39-green-mains/handover.md) and its [owner decisions](../39-green-mains/inputs.md#owner-decisions) D3, D9 and D10, which this plan keeps.
- [Release 14 run board](../../releases/14/run.md) rulings 6a, 10 and 13.
- [Release 15 run board](../../releases/15/run.md): the release's headline has no lane, and Plan 39 competes with Plan 81 for CI runners.
