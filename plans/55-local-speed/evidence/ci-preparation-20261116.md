# CI preparation addendum — 16 November 2026

This is supporting preparation for the existing `2026-11-15-local-speed` run, accountable manager `chatgpt-workspace-6ee41b0f0cca/root`. It extends draft #719; it does not start a replacement run, recreate the unfinished LS-2 worker, change an accepted decision, close a task, or consume a review round. [Tasks on main](https://github.com/banodoco/astrid-dev/blob/main/plans/55-local-speed/tasks.md) remain authoritative.

The earlier [recovery note](recovery-20261116.md) is retained as a historical record. This addendum supersedes only its pending opt-in classification and its then-in-progress integration-shard observations. Its original artifact audit, 160 manager-run CPU checks, raw-evidence hashes, unavailable-state record and merge hold are unchanged. Those tests were not rerun for this addendum.

## Completed comparison: the executed opt-in selection

| Input | Published Release 13 | Plan 55 candidate |
| --- | --- | --- |
| Agent SHA | `9814193a73f606719e81883a8be197d27dd361d4` | `cb1a590e0008dde7e3fc2d3fbf341ef98401b32a` |
| Lanes run | [43757233283](https://github.com/banodoco/astrid-agent/actions/runs/43757233283) | [43769390907](https://github.com/banodoco/astrid-agent/actions/runs/43769390907) |
| Opt-in job | [132943873159](https://github.com/banodoco/astrid-agent/actions/runs/43757233283/job/132943873159) | [132981680460](https://github.com/banodoco/astrid-agent/actions/runs/43769390907/job/132981680460) |
| Passed / failed | 19 / 12 | 19 / 12 |
| Deselected | 31,189 | 31,202 |
| Warnings | 2 | 2 |
| Pytest duration | 187.15 seconds | 187.95 seconds |

Both jobs ran `python -m pytest -q -rA -m opt_in` with Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c` and VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`. The proposed VibeComfy re-pin was not used. These are CI-suite durations, not LS-1 latency measurements.

The [machine-readable comparison](ci-comparison-20261116.json) lists all 31 executed test IDs, both outcomes, the three reported-cause groups, source jobs, exact checked-out dependencies and limitations. It is a normalized manager transcription of observed logs, not a raw-log archive or independent check.

**Finding:** all twelve observed candidate opt-in failures also occur on the actual published-source baseline with the same test IDs and matching reported causes. All nineteen passing test IDs match too. There are no changed pass/fail outcomes or new failing IDs within this executed selection.

The failures are:

- Six parametrizations of `test_saved_actual_filmstrip_v2_composed_capture_readback`: the saved actual public C06 frame-index artifact is missing. The parameters are `None`, `sidecar-bytes`, `saved-revision`, `requested-frame`, `render-digest` and `sidecar-path`.
- Six onboarding checks involving `editorial.arrange`: discovery does not contain that executor; the other five checks raise `CapabilityNotFoundError` for it, with `training.pool_merge` as the nearest match.

Both jobs remain **failed**. Matching failures classify these observed symptoms as inherited under the tested dependency combination; they do not prove the hidden paths are correct, fix the baseline, waive CI, or qualify Plan 55. The thirteen-count increase in deselected tests is outside the executed comparison and is not new passing coverage.

Do not manufacture the missing C06 artifact, replace it with a synthetic passing fixture, remove the onboarding checks, or broaden Plan 55 into unrelated repairs merely to obtain a green job.

## Integration jobs: finished, still unclassified per test

| Shard | Release 13 job | Candidate job | Observed conclusions | Per-test/cause comparison |
| --- | --- | --- | --- | --- |
| 1 / 4 | 132943873394 | 132981680578 | Both failed | Pending |
| 2 / 4 | 132943873354 | 132981680766 | Both failed | Pending |
| 3 / 4 | 132943873344 | 132981680602 | Both failed | Pending |
| 4 / 4 | 132943873317 | 132981680773 | Both failed | Pending |

In particular, candidate shards 3 and 4 are no longer in flight. No integration failure is classified from these job-level conclusions alone. The baseline run is 43757233283 and the candidate run is 43769390907 for every row above. Compare complete executed test-ID sets across the four shards, rather than assuming a test stays on the same shard when collection changes.

Installed-wheel jobs 132943873385 (baseline) and 132981680712 (candidate) passed. That does not resolve the independently observed omission of `.astrid-registry-state.json` from both archived receipts, and does not qualify the final product tuple.

## Bounded resume handoff

1. **Finish integration classification without changing product refs.** Retrieve the existing job logs identified above, retain their raw bytes and hashes when file access allows, collect every executed status and reported cause, and compare the union across all four shards. Keep infrastructure failures, missing inputs, changed test sets and unclassified cases distinct. Do not blindly rerun, manufacture missing evidence or mark an incomplete comparison green. These existing completed jobs do not require access to the original workspace; this comparison remains unfinished work, not a workspace-access blocker.
2. **Recover, do not replace, the original worker.** The original workspace is `/workspace/scratch/6ee41b0f0cca`; the ignored configuration is `plans/55-local-speed/.otto/runs/2026-11-15-local-speed/run.yaml`; the unfinished LS-2 observer is at `worktrees/agent-meter-next`. Read its actual diff and logs when access returns. Do not create another owner/worker or claim its result. Native/hash/Windows coverage and independent scoped checking remain missing; LS-12 waits for full LS-2.
3. **Retain the measurement and design gates.** Real ComfyUI/GPU/Windows LS-1 measurements remain incomplete. This CI comparison is not a latency floor and does not unlock LS-3 or its one RS1 design review. Do not promise the sub-0.1-second target before its required measurement.
4. **Check this preparation before landing it.** An independent N check and the full `python3 scripts/astrid_dev.py check` from a complete checkout are still required. Neither is claimed here. Leave #719 draft and unmerged; source accessibility through the connector is not the original executable workspace or its ignored run state.

## Boundaries preserved

Only LS-11 is complete. RS1 remains 0/1 and final R remains 0/1. Spend remains $0. Plan 54 remains queued. Release 13 remains the published/default baseline. No product-main merge, dependency re-pin, GPU rental, tester engagement, scope/decision change or Release 14 publication occurred.

The [LS-5 exact re-pin proposal](ls5-repin-request.md) and [LS-6 scope proposal](ls6-scope-request.md) remain proposals. Refused ComfyUI source reads, shell push and native-probe permission changes were not used as workarounds. No original run configuration, worker result, raw transcript or independent approval was invented.
