# Plan 77 first cut, Agent: the Lead's own comparison of the gate run (23 November 2026)

The Release 15 Lead's check of the hosted unit run on Plan 77's first-cut Agent head, made before confirming its landing gate.

| | |
| --- | --- |
| Commit | `8d2b6bca2f3a285bff54c444ec837ce42b01fee7` (astrid-agent PR #555: `release/15/main` `8fdf6615` merged with the first-cut source, plus one generator-only pin commit to Runtime `737843e9`) |
| Run | [45160760129](https://github.com/banodoco/astrid-agent/actions/runs/45160760129) (the unit workflow) |
| Compared with | [the Release 15 baseline](../agent-ci-baseline-8807f820/README.md) (`8807f820`) and [Plan 40's gate](../plan-40-gate-cd3fed64/README.md) |
| Failing ids | 764 here, 760 in the baseline |
| Erroring ids | 328 here, 328 in the baseline |

- **New: five,** in [new.txt](new.txt). Four are members of recorded moving groups: the two macOS render tests ("candidate reconciliation budget ran out"), `test_the_download_plan_and_readiness_agree[True]` (readiness, the fake server's `BrokenPipeError`) and `test_secret_never_appears_in_receipt_state_or_cli_output` (pinokio, "active process is not the configured listener owner"). The fifth, `tests/packs/rendering/test_render_export_task_adapter.py::test_registry_qualifying_discovery_refuses_corpus_change[new_manifest]` ("DID NOT RAISE RemotionValidationError"), is newly recorded as moving in the baseline README: the change touches no rendering or discovery file, the test passed 5 of 5 times on both base and head on the Lead's machine, and it depends on a file timestamp falling after the probe's start time.
- **Gone: one,** in [gone.txt](gone.txt): a readiness group member.
- **All ids:** [candidate-failing-ids.tsv](candidate-failing-ids.tsv); jobs in [jobs.tsv](jobs.tsv).

**How.** As for [Plan 40's gate](../plan-40-gate-cd3fed64/README.md). [job-totals.tsv](job-totals.tsv) sets each job's count beside pytest's totals line; they agree for every job except shard 6, which reports 259 failures for 226 ids because of 33 `SUBFAILED` lines from the same three subtest-only tests as on the baseline and Plan 40.

**Not covered here.** The integration workflow (45160763255) and the PR's own CI: every failing id was in Plan 40's gated run, per the lane's gate list.
