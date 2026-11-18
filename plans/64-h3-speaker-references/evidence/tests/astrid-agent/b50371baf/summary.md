# Plan 64 scoped starting baseline — 2026-11-18

Agent `b50371baf101d6f706269fab38cdf3a7a5eb2013`; Python 3.13.18; CPU worker environment. The sorted comparison uses the same starting log as both baseline and candidate to record the pre-existing failures, not to claim a candidate passed. Pytest reported 198 passed, 3 failed, 31 deselected. The plan-named paths `tests/packs/h3_av/test_edit_inputs.py`, `tests/packs/h3_av/test_handle_build_compose.py` and `tests/test_pack_declared_skills.py` did not exist at this SHA and were not collected.

Command: `PYTEST_ADDOPTS=-rA bash /home/user/work/managers/plan-64/astrid-dev/env/agent-pytest.sh tests/packs/h3_av/test_character_swap.py tests/packs/h3_av/test_character_swap_cpu_boundary.py tests/packs/h3_av/test_compile_generalized.py tests/packs/h3_av/test_generation.py tests/packs/h3_av/test_native_masked_edit.py tests/packs/h3_av/test_native_v2_contract.py tests/packs/h3_av/test_parent_receipt_readback.py tests/packs/h3_av/test_real_media_preflight.py tests/packs/h3_av/test_request_contract.py tests/packs/h3_av/test_skill_examples_admitted.py tests/packs/h3_av/test_spec.py tests/sdk/test_generation_result_refs.py`.

| Side | Tests run |
|---|---|
| start | 201 |
| candidate | 201 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 3 |
| fixed | 0 |
| missing | 0 |
