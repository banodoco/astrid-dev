# Lanes integration shard 2 / 4 — run 43693934998

- Job id: 132750234824
- Head SHA: a91c35dfd63f8d5969714541a30afe25feb2d626
- Conclusion: failure
- Pytest: = 78 failed, 266 passed, 31807 deselected, 21 warnings, 172 errors in 1190.26s (0:19:50) =

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
