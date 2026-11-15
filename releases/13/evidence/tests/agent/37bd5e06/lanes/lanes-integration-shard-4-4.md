# Lanes integration shard 4 / 4 — run 43728670644

- Job id: 132856063104
- Head SHA: 37bd5e069492446bd62d94ff7aa40eb3143d8f85
- Conclusion: failure
- Pytest: = 99 failed, 391 passed, 31938 deselected, 8 warnings, 26 errors in 4279.15s (1:11:19) =

## New failures by owner lane

### cells
- tests/test_bootmanifest2_admission.py::test_busy_rejected_attachment_preserves_r12_resident_reader — new test (file not at R12) — d937eca62f14 fix: keep the boot-manifest rollback restore installer-owned (path astrid/installer/core.py)
- tests/test_bootmanifest2_rollback.py::test_real_rollback_activates_r12_own_composition[False] — new test (file not at R12) — d937eca62f14 fix: keep the boot-manifest rollback restore installer-owned (path astrid/installer/core.py)
- tests/test_bootmanifest2_rollback.py::test_real_rollback_activates_r12_own_composition[True] — new test (file not at R12) — d937eca62f14 fix: keep the boot-manifest rollback restore installer-owned (path astrid/installer/core.py)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 672 |
| candidate | 516 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 3 |
| preexisting | 122 |
| fixed | 2 |
| missing | 0 |
