# Agent CI by id on `release/15/main` `b934555c` (25 November 2026)

Source: astrid-agent CI run [45546410083](https://github.com/banodoco/astrid-agent/actions/runs/45546410083) (push on `b934555c`, finished red): the full logs of the 8 unit shards and the darwin native job, read with `env/baseline-diff.py`'s parser by the Qualifier's Codex worker (Luna), against [agent-ci-baseline-8807f820](../agent-ci-baseline-8807f820/README.md) (Release 14 `c0ad6b54` and Release 15 `8807f820` failing ids). The logs are not kept here. Earlier push runs read the same way: `edfc2dc9` ([45510560565](https://github.com/banodoco/astrid-agent/actions/runs/45510560565)), `23ace564` ([45518931127](https://github.com/banodoco/astrid-agent/actions/runs/45518931127)), `89768ef9` ([45534699892](https://github.com/banodoco/astrid-agent/actions/runs/45534699892)).

## Counts, and why they differ from other counts

| Method | `b934555c` | Release 14 | Release 15 baseline |
| --- | ---: | ---: | ---: |
| Distinct ids, FAILED plus ERROR, one row per subtest, `darwin:` kept | 1,120 (792 + 328) | 1,093 | 1,088 |
| Same, subtest rows left out (Plan 87's and the Lead's method) | 1,087 | | 1,088 |

- 1,070 candidate ids are also Release 14 failures; 23 Release 14 ids do not fail on the candidate; **50** candidate ids are not in Release 14; 4 of the 50 are in the Release 15 baseline or its "new on Release 15" list; **46** are in neither ([candidate-ids-not-in-release-14.txt](candidate-ids-not-in-release-14.txt)).
- **33 of the 46 are `SUBFAILED(...)` subtest rows of three tests** (`test_pack_migration_m4_shells` x2: 7 rows each; `test_pack_run_cli_choices` x1: 19 rows). The baseline files contain no subtest rows, so a subtest row can never match. Leaving subtest rows out gives 1,087, Plan 87's figure.
- **13 are plain ids** that the baselines list only with the `darwin:` prefix (they fail on the macOS job there) and that fail on the Linux shards on the candidate: `test_remotion_render_contract` (5), `test_timeline_visualize_motion_views` (2), `test_managed_media_saved_visualize` (1), `test_provider_route_grant` (2), `stage1/test_runtime_lifecycle_reproducer` (2), `test_readiness_missing_models::test_defaults_is_ready_once_the_files_are_listed` (1; a known mover). A comparison that ignores the OS prefix finds them inherited.
- **Where they first fail:** all 50 ids already fail at `edfc2dc9` (Plan 82 stage 1), the earliest push run read; none first appears at `89768ef9` (Plan 87) or `b934555c` (P87-07); no selected test file has a commit in `edfc2dc9..b934555c` ([20-test-chronology.tsv](20-test-chronology.tsv), [50-id-chronology.tsv](50-id-chronology.tsv)). Two readiness ids are absent at `23ace564` and back at `89768ef9` (movers).
- The five ids of astrid-dev #1920 by head: [issue-1920-ids-by-head.txt](issue-1920-ids-by-head.txt).

## What this does not show

Whether the 13 plain ids fail on Linux on Release 14: the Release 14 logs are not kept, only its id list, which has them as `darwin:` only. Whether the three subtest tests failed on Release 14 with subtests the list did not keep. The Qualifier does not judge acceptability: the Lead rules it (r15-lead-q-0013 counts 0 new real failures by the method above).

Files: [b934555c-failing-ids.txt](b934555c-failing-ids.txt) (all 1,120 distinct ids, FAILED and ERROR together, bare ids with `darwin:` kept), [b934555c-error-ids.txt](b934555c-error-ids.txt) (the 328 errors), [per-run-job-counts.tsv](per-run-job-counts.tsv).
