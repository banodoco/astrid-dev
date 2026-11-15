# Lanes integration shard 2 / 4 — run 43728670644

- Job id: 132856063069
- Head SHA: 37bd5e069492446bd62d94ff7aa40eb3143d8f85
- Conclusion: failure
- Pytest: = 78 failed, 266 passed, 31938 deselected, 22 warnings, 172 errors in 1909.53s (0:31:49) =

## New failures by owner lane

### unattributed
- tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance — regression (absent from R12 failures-only output; file existed at R12) — no touching commit since R12 (likely an environment or ordering effect)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 672 |
| candidate | 516 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 1 |
| preexisting | 249 |
| fixed | 22 |
| missing | 0 |
