# Gate 89: candidate d10817a77b280b2ca6a7b945f841e9823bbbee3f (release/15/plan-89)

Logs: gate89/logs/ci/, logs/lanes-cand/, logs/lanes-base/. Script: gate89/scripts/extract.py (run: `python3 -I extract.py <gate89dir> ci|lanes`).
Note: get_job_logs returns only the last 5000 lines whatever tail_lines is, which cut the summary head on shards 5, 6 and 7. Full logs were fetched with read-only `gh api .../actions/jobs/<id>/logs` (GET) instead. Every extracted count below equals pytest's totals line, except shard 6 (226 ids vs 259 failed, because subtests share an id, as the README says).

## Part 1: ci.yml run 45259689240 vs release-15-8807f820-failing-ids.tsv
Baseline: 1088 ids (760 FAILED, 328 ERROR). Candidate: 762 FAILED + 328 ERROR = 1090 ids.

| job | candidate pytest totals | ids FAILED/ERROR |
| --- | --- | --- |
| unit shard 1 | 47 failed, 54 errors | 47/54 |
| unit shard 2 | 80 failed, 51 errors | 80/51 |
| unit shard 3 | 31 failed | 31/0 |
| unit shard 4 | 32 failed, 19 errors | 32/19 |
| unit shard 5 | 28 failed, 33 errors | 28/33 |
| unit shard 6 | 259 failed, 25 errors | 226/25 |
| unit shard 7 | 227 failed, 142 errors | 227/142 |
| unit shard 8 | 78 failed, 4 errors | 78/4 |
| darwin native | 13 failed | 13/0 (prefixed darwin:) |

All 328 ERROR ids are identical to the baseline. test_param_map_parity (3 parametrized ids) matches the baseline in full: not new.

### NEW ids (5)
| id | job | classification |
| --- | --- | --- |
| tests/core/generation/test_readiness_missing_models.py::test_a_partly_installed_default_names_only_what_is_missing | shard 2 | README moving group "readiness" (`no a... unavailable` in place of the expected reason) |
| tests/core/generation/test_readiness_missing_models.py::test_defaults_is_ready_once_the_files_are_listed | shard 2 | README readiness group (the added `ready` false member) |
| tests/core/generation/test_readiness_missing_models.py::test_the_download_plan_and_readiness_agree[True] | shard 2 | README readiness group (`assert False is not []`, named in the README) |
| tests/test_vendor_lock.py::test_one_root_lock_covers_all_known_runtime_paths | shard 8 | Runtime pin: lock digest differs from the old constant (runtime ref now 24e2c9291d5bcaface78324696286f2dc896debc) |
| tests/test_windows_path_budget.py::test_installed_runtime_pinned_source_witness_fits_fresh_version_staging | shard 8 | Runtime pin: "refresh the pinned Runtime path witnesses" |

Unexplained: none.

### GONE ids (3, all from moving groups; baseline failed them, the candidate passes them)
- FAILED tests/core/generation/test_readiness_missing_models.py::test_defaults_says_not_ready_when_the_server_lists_none_of_the_files (readiness group)
- FAILED tests/core/generation/test_readiness_missing_models.py::test_list_and_defaults_agree_when_files_are_missing (readiness group)
- FAILED tests/test_pinokio_platform_adapter.py::test_real_local_start_http_readiness_snapshot_stop_and_port_free (pinokio listener-owner group)

Readiness group net: baseline 2 ids, candidate 3 ids, none overlapping. Pinokio: baseline 3 ids, candidate 2 (both shared with baseline).

## Part 2: lanes.yml run 45259694852 (integration shards 1-4 and opt-in)
Base run used: 45183456544 (head b324d7c1e94713e7ae48d3d98a70db1214ef658f, release/15/main, completed, conclusion failure, Plan 77 landing). The run for 045064b61eaefb07480d71709dd31a4b72d53b24 is 45238122576 and was CANCELLED after about 14 s (no usable logs). The runs for 0615e4e9 (45224513655) and 8fdf6615 (45158779142) are also cancelled. 45183456544 is the latest completed lanes run on release/15/main that actually ran its tests. (The installed wheel job passed on both runs.)

| job | candidate totals | base (45183456544) totals | NEW | GONE |
| --- | --- | --- | --- | --- |
| integration shard 1/4 | 43 failed | 43 failed | 0 | 0 |
| integration shard 2/4 | 121 failed, 293 errors | 120 failed, 293 errors | 1 | 0 |
| integration shard 3/4 | 123 failed, 116 errors | 124 failed, 116 errors | 0 | 1 |
| integration shard 4/4 | 93 failed, 26 errors | 93 failed, 26 errors | 0 | 0 |
| opt-in | 12 failed | 12 failed | 0 | 0 |

### NEW (1)
- shard 2: FAILED tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance, with `Expected regex: 'timeline not found'`, `Actual message: 'history_unavailable'`. Classification: the README's recorded "integration test that fails on the unchanged base" (same id, same message; the Lead ruled it does not hold a landing). It passed on this base run, so it is a flaky member, not an unexplained id. Note: the README gives the symptom as `history_unavailable` / `store_membership_missing`; the log shows the `history_unavailable` message.

### GONE (1)
- shard 3: FAILED tests/integrations/test_command_count_capture.py::test_fresh_process_command_counts (base failed with `Timeout (>120.0s) from pytest-timeout`; the candidate passed it).

## Verdict
No unexplained new failures in either workflow. 4 of 5 new unit ids are explained by a moving group or the Runtime pin as expected; the fifth readiness id is also in the group; the one new lanes id is a README-recorded base flake.
