# Starting scoped baseline — 2026-11-18

Agent `b50371baf101d6f706269fab38cdf3a7a5eb2013`; CPU worker, Python 3.13.18. Existing Plan 65 inventory files ran with `PYTEST_ADDOPTS=-rA bash ../astrid-dev/env/agent-pytest.sh` and the paths in `tasks.md`. Result: 218 passed, 1 failed, 34 deselected; six named files did not exist and were not run: `test_edit_inputs.py`, `test_lead_in.py`, `test_automatic_conform.py`, `test_remote_prepared_source_handoff.py`, `test_non16x9_masked_edit_cpu.py`, and `tests/test_pack_declared_skills.py`. The first five are under `tests/packs/h3_av/`. Full log retained in run/baseline.log.

The sorter compares this starting log with itself solely to classify its failure, not to claim a candidate comparison. The failure expects 5 model locks but finds 36.

| Side | Tests run |
|---|---|
| starting | 219 |
| candidate | 219 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 1 |
| fixed | 0 |
| missing | 0 |
