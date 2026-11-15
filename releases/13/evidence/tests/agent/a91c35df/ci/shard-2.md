# Unit shard 2 — run 43693935046

- Job id: 132750235014
- Head SHA: a91c35dfd63f8d5969714541a30afe25feb2d626
- Conclusion: failure
- Pytest: = 82 failed, 3780 passed, 19 skipped, 27179 deselected, 1 warning, 51 errors, 26 subtests passed in 4249.85s (1:10:49) =
- Wall time (log fetch, diff, and attribution): 2.34s

## New failures by owner lane

### engine
- tests/core/generation/test_readiness_missing_models.py::test_defaults_says_not_ready_when_the_server_lists_none_of_the_files — no-baseline — f48dc2955424 Download plan says nothing is missing when the default is ready (path tests/core/generation/test_readiness_missing_models.py)
- tests/core/generation/test_readiness_missing_models.py::test_list_and_defaults_agree_when_files_are_missing — no-baseline — f48dc2955424 Download plan says nothing is missing when the default is ready (path tests/core/generation/test_readiness_missing_models.py)
- tests/core/generation/test_trusted_inventory.py::test_catalog_trust_resolves_only_a_single_declared_missing_name — no-baseline — 7efe5bb65b26 Apply explicit trust to catalog roles and protect native attempt custody (path tests/core/generation/test_trusted_inventory.py)
- tests/core/generation/test_warm_models_remain_loaded.py::test_models_stay_loaded_between_settled_jobs_on_warm_session — no-baseline — c859bf57415b Guard test: models stay loaded between compatible jobs on a warm session (path tests/core/generation/test_warm_models_remain_loaded.py)

### via r13/compose-pin-vc8
- tests/core/model_catalog/test_catalog_fixed_entries.py::test_ltx_required_inputs_dry_run[flf-required1] — no-baseline — f0d22f4b2e85 Adapt repaired catalog admissions to the compose generation API (path tests/core/model_catalog/test_catalog_fixed_entries.py)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 23882 |
| candidate | 3917 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 8 |
| preexisting | 129 |
| fixed | 1 |
| missing | 19311 |
