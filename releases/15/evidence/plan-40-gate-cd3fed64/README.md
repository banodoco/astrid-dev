# Plan 40: the Lead's own comparison of the gate run (23 November 2026)

The Release 15 Lead's check of the hosted unit run on Plan 40's frozen Agent head, made before confirming its landing gate. It is separate from the lane's own gate list and record.

| | |
| --- | --- |
| Commit | `cd3fed648d0f1eedf1a32b24fc3916603526de87` (astrid-agent `release/15/plan-40`, with `release/15/main` at `bd94a6e1` merged in) |
| Run | [45127057649](https://github.com/banodoco/astrid-agent/actions/runs/45127057649) (the unit workflow) |
| Compared with | [the Release 15 baseline](../agent-ci-baseline-8807f820/README.md) (`8807f820`) |
| Failing ids | 761 here, 760 in the baseline |
| Erroring ids | 328 here, 328 in the baseline |
| Landed as | `release/15/main` `8fdf6615082785f5a8458abf614a9323092e0bc6` (tree identical to the tested head) |

- **New: four,** in [new.txt](new.txt). Two macOS render tests (`test_audio_render.py::...::test_rendered_mp4_contains_audio_stream` and `test_text_card_render.py::...::test_text_card_render_smoke`, both "candidate reconciliation budget ran out after about 1.2 s") and two readiness tests (`test_defaults_is_ready_once_the_files_are_listed` and `test_the_download_plan_and_readiness_agree[True]`, both with the fake server's `BrokenPipeError`). All four are members of groups the baseline records as moving; none holds the landing.
- **Gone: three,** in [gone.txt](gone.txt): one readiness test and two pinokio adapter tests, both groups that move.
- **All ids:** [candidate-failing-ids.tsv](candidate-failing-ids.tsv), in the baseline's format; jobs in [jobs.tsv](jobs.tsv).

**How.** As for [Plan 81's Part 1 gate](../plan-81-part1-gate-a2938366/README.md): the full log of every unit shard and the macOS job was fetched and the `FAILED` and `ERROR` lines of pytest's final summary were extracted by script; [job-totals.tsv](job-totals.tsv) sets each job's count beside pytest's totals line. They agree for every job except shard 6, which reports 259 failures for 226 ids because 33 `SUBFAILED` lines come from three tests that fail only in subtests and are not ids in either list; the same split appears on Plan 81's gate run.

**Not covered here.** The integration workflow's run (45127061949) matched all 826 base ids with no additions, per the lane's gate list.
