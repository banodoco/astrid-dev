# Unit shard 2 — run 43740169488

- Job id: 132891360767
- Head SHA: 401dbd782088e18f247a7bbc3cf516eb953a7325
- Conclusion: failure
- Pytest: = 81 failed, 3816 passed, 19 skipped, 27275 deselected, 2 warnings, 51 errors, 26 subtests passed in 4648.82s (1:17:28) =
- Wall time (log fetch, diff, and attribution): 2.36s

## New failures by owner lane

### engine
- tests/core/generation/test_readiness_missing_models.py::test_a_partly_installed_default_names_only_what_is_missing — no-baseline — f48dc2955424 Download plan says nothing is missing when the default is ready (path tests/core/generation/test_readiness_missing_models.py)
- tests/core/generation/test_readiness_missing_models.py::test_list_and_defaults_agree_when_files_are_missing — no-baseline — f48dc2955424 Download plan says nothing is missing when the default is ready (path tests/core/generation/test_readiness_missing_models.py)
- tests/core/generation/test_trusted_inventory.py::test_catalog_trust_resolves_only_a_single_declared_missing_name — no-baseline — 7efe5bb65b26 Apply explicit trust to catalog roles and protect native attempt custody (path tests/core/generation/test_trusted_inventory.py)
- tests/core/generation/test_warm_models_remain_loaded.py::test_models_stay_loaded_between_settled_jobs_on_warm_session — no-baseline — c859bf57415b Guard test: models stay loaded between compatible jobs on a warm session (path tests/core/generation/test_warm_models_remain_loaded.py)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 23882 |
| candidate | 3952 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 7 |
| preexisting | 129 |
| fixed | 1 |
| missing | 19279 |
