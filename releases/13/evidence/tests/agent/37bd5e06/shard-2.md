# Unit shard 2 — run 43728670712

- Job id: 132856063627
- Head SHA: 37bd5e069492446bd62d94ff7aa40eb3143d8f85
- Conclusion: failure
- Pytest: = 80 failed, 3817 passed, 19 skipped, 27275 deselected, 2 warnings, 51 errors, 26 subtests passed in 3541.03s (0:59:01) =
- Wall time (log fetch, diff, and attribution): 1.76s

## New failures by owner lane

### engine
- tests/core/generation/test_readiness_missing_models.py::test_defaults_is_ready_once_the_files_are_listed — no-baseline — f48dc2955424 Download plan says nothing is missing when the default is ready (path tests/core/generation/test_readiness_missing_models.py)
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
| no-baseline | 6 |
| preexisting | 129 |
| fixed | 1 |
| missing | 19279 |
