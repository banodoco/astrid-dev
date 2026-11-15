# Lanes integration shard 3 / 4 — run 43728670644

- Job id: 132856063217
- Head SHA: 37bd5e069492446bd62d94ff7aa40eb3143d8f85
- Conclusion: failure
- Pytest: = 82 failed, 371 passed, 1 skipped, 31938 deselected, 13 warnings, 62 errors in 7855.54s (2:10:55) =

## New failures by owner lane

### machines
- tests/integrations/test_managed_host_preparation.py::test_managed_host_prepares_before_sandboxed_worker[device-ambient] — new test (file not at R12) — 8cebc4e2ad06 Lanes: 41 hosted local-managed failures traced and fixed; one shared pinned-source fixture (path tests/integrations/test_managed_host_preparation.py)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 672 |
| candidate | 518 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 4 |
| preexisting | 143 |
| fixed | 1 |
| missing | 0 |
