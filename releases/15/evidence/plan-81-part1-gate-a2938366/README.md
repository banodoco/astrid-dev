# Plan 81, Part 1: the Lead's own comparison of the gate run (23 November 2026)

The Release 15 Lead's check of the hosted unit run on Plan 81's frozen Agent head, made before confirming the Agent's landing gate. It is separate from the lane reviewer's three-way ledger, which the lane archives with its landing record.

| | |
| --- | --- |
| Commit | `a29383661ad990da7ab43185f1a07132e074fadf` (astrid-agent `release/15/plan-81`) |
| Run | [45106316187](https://github.com/banodoco/astrid-agent/actions/runs/45106316187) (the unit workflow) |
| Compared with | [the Release 15 baseline](../agent-ci-baseline-8807f820/README.md) (`8807f820`) |
| Failing ids | 759 here, 760 in the baseline |
| Erroring ids | 328 here, 328 in the baseline |

- **New: one,** in [new.txt](new.txt): `tests/test_pinokio_platform_adapter.py::test_secret_never_appears_in_receipt_state_or_cli_output`, with "active process is not the configured listener owner". The baseline's group rule covers it.
- **Gone: two,** in [gone.txt](gone.txt), both in `test_readiness_missing_models.py`, the other group that moves between runs.
- **All ids:** [candidate-failing-ids.tsv](candidate-failing-ids.tsv), in the baseline's format.

**How.** The full log of every failed job (eight unit shards and the macOS job) was fetched and the `FAILED` and `ERROR` lines of pytest's final summary were extracted by script; [job-totals.tsv](job-totals.tsv) sets each job's extracted count beside pytest's own totals line. They agree for every job; shard 6 reports 259 failures because it counts subtests of 226 ids.

**Not covered here.** The integration workflow's run (45106319353) is compared in the lane reviewer's ledger, not in this check. One test there failed on the candidate and passed on the base, `tests/core/execution/test_generic_host_child_bridge_d18.py::test_host_bridge_outer_send_diagnostic_preserves_revoke_close[False]`; the Lead ruled it a defect of the base (see the baseline's note).
