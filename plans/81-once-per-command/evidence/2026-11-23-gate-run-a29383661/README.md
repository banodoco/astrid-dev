# Agent gate comparison, 23 November 2026

The independent reviewer compared full pytest node IDs within each lane for these Agent revisions and hosted runs:

| Revision | CI | Lanes |
| --- | --- | --- |
| Exact release base `8807f820` | [45031908687](https://github.com/banodoco/astrid-agent/actions/runs/45031908687) | [45031908621](https://github.com/banodoco/astrid-agent/actions/runs/45031908621) |
| Previous freeze `b5c30e61` | [45095434060](https://github.com/banodoco/astrid-agent/actions/runs/45095434060) | [45095437908](https://github.com/banodoco/astrid-agent/actions/runs/45095437908) |
| Merged repair `a29383661` | [45106316187](https://github.com/banodoco/astrid-agent/actions/runs/45106316187) | [45106319353](https://github.com/banodoco/astrid-agent/actions/runs/45106319353) |

Both workflows on the merged repair failed. Of its failing or erroring IDs, 1,073 of 1,074 Linux unit, 812 of 813 integration, 13 of 13 Darwin and 12 of 12 opt-in also failed or errored on the exact base.

The two merged red IDs that passed on the hosted base were:

- `tests/test_pinokio_platform_adapter.py::test_secret_never_appears_in_receipt_state_or_cli_output`: the active process was not the configured listener owner. Three other exact-base members failed for the same reason; the Lead accepted this under the Pinokio group rule. This ID also failed on the previous freeze.
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_host_bridge_outer_send_diagnostic_preserves_revoke_close[False]`: the fd-2 flags remained nonblocking. The reviewer reproduced the same assertion on the exact base and merged head by ordering the test's own two concurrent diagnostic writers. The Lead ruled this a base defect, not load. The hosted log does not establish its actual thread interleaving.

## Previous freeze to merged repair

The full node IDs and base, previous and merged statuses are in `all-deltas.json`. The observed changes were one Darwin audio-render failure becoming a pass; the child-bridge pass becoming a failure; integration shared-redo and managed-TTS failures becoming passes; four readiness unit failures becoming passes; and six new failure-precedence cases changing from unobserved to passed. A single passing run does not establish a permanent repair for intermittent failures.

## Files and limits

`all-deltas.json` is the three-way transition ledger, `all-jobs.json` the job ledger and `results.json` the per-node results. `compare.py` and `hosted.py` are the reviewer's comparison scripts; `hosted.py` was copied from the adjacent `scratch/frozen` directory. They describe the reviewer's local analysis and refer to local log locations; the hosted logs are not included here.

The comparison matches IDs and outcomes, not root causes: identical red IDs can have different tracebacks. Some quiet jobs report counts only, so their individual node outcomes are unavailable. No new run was performed to prepare this record.
