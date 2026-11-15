# Unit shard 1 — run 43728670712

- Job id: 132856063651
- Head SHA: 37bd5e069492446bd62d94ff7aa40eb3143d8f85
- Conclusion: failure
- Pytest: = 43 failed, 5194 passed, 3 skipped, 25948 deselected, 60 warnings, 54 errors, 153 subtests passed in 5373.50s (1:29:33) =
- Wall time (log fetch, diff, and attribution): 2.04s

## New failures by owner lane

### engine
- tests/core/generation/test_edit_image_ref_admission.py::test_edit_dry_run_binds_the_reference_image — no-baseline — 3ea7381d2abd An edit's reference image reaches the entry's input: one requirement check, through the param_map (path tests/core/generation/test_edit_image_ref_admission.py)
- tests/core/generation/test_engine_error_reasons.py::test_install_start_raise_sites_have_declared_fixed_reasons — no-baseline — 3a7d1bd9c7a2 Recipe and install refusals name the field, path or source again (path tests/core/generation/test_engine_error_reasons.py)
- tests/core/generation/test_engine_fresh_install.py::test_fresh_install_custody_uses_receipt_models_root[default-models] — no-baseline — 13b4bf569601 Engine supervisor binds its launch when the install declares it, not at spawn (path tests/core/generation/test_engine_fresh_install.py)
- tests/core/generation/test_engine_fresh_install.py::test_fresh_install_custody_uses_receipt_models_root[external-model-volume] — no-baseline — 13b4bf569601 Engine supervisor binds its launch when the install declares it, not at spawn (path tests/core/generation/test_engine_fresh_install.py)
- tests/core/generation/test_generation_setup_walk.py::test_as_entry_no_run_saves_and_queues_nothing — no-baseline — a294d40702eb Plan 32 S2: route generate defaults/settings to the full parser; defaults undo walk (path tests/core/generation/test_generation_setup_walk.py)
- tests/core/generation/test_owned_doctor_schema.py::test_doctor_failure_stops_exact_owned_engine_and_retains_uncertain_lock[command] — no-baseline — 2a0dcc0fc63a Hosted engine failures: fixture drift, environment and one stale alias (path tests/core/generation/test_owned_doctor_schema.py)
- tests/core/generation/test_owned_doctor_schema.py::test_doctor_failure_stops_exact_owned_engine_and_retains_uncertain_lock[post_health] — no-baseline — 2a0dcc0fc63a Hosted engine failures: fixture drift, environment and one stale alias (path tests/core/generation/test_owned_doctor_schema.py)
- tests/core/generation/test_owned_doctor_schema.py::test_doctor_failure_stops_exact_owned_engine_and_retains_uncertain_lock[stop_uncertain] — no-baseline — 2a0dcc0fc63a Hosted engine failures: fixture drift, environment and one stale alias (path tests/core/generation/test_owned_doctor_schema.py)

### unattributed
- tests/core/generation/test_param_map_migration_parity.py::test_param_map_parity[hunyuan-foley-local-sfx-local-{'video_ref': 'video_ref', 'prompt': 'prompt', 'seed': 'seed'}-{}-True] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 23882 |
| candidate | 5308 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 26 |
| preexisting | 88 |
| fixed | 2 |
| missing | 18996 |
