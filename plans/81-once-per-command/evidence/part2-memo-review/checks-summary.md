# Independent checks: Option A 675f

Candidate: `/tmp/option-a`, `675f5dc2658197318a95e0e1b7c5b232b17cd9d5`.
Baseline inventory/results: saved `950023c8` evidence under `run/evidence/phase2-root-9500/`.
Runner: `/tmp/vibecomfy-witness-env/bin/python` (Python 3.13.18, pytest 9.0.3). All pytest invocations used `nice -n 19`.

## Commands and results

1. Inventory the 194 tests and compare its test ID set with the saved 950 candidate inventory:

   `cd /tmp/option-a && nice -n 19 /tmp/vibecomfy-witness-env/bin/python -m pytest --collect-only -q tests/test_porting_object_info.py tests/test_workflow_bundle.py tests/test_b14_object_info_publication.py`

   Result: 194 collected; ID set exactly equal to saved `phase2-root-9500/collect-candidate.txt` (0 missing, 0 extra). Captured in `collect-194.txt`.

2. Run all 194 with complete per-test results:

   `cd /tmp/option-a && PYTEST_ADDOPTS=-rA nice -n 19 /tmp/vibecomfy-witness-env/bin/python -m pytest -vv --tb=no tests/test_porting_object_info.py tests/test_workflow_bundle.py tests/test_b14_object_info_publication.py`

   Result: 188 passed, 6 failed. Failed ID set exactly equals the saved 950 `suite-194.txt`: 3 parameter cases of `test_derived_template_live_identity_requires_package_lock_and_checkout`, `test_v2_companion_keeps_generated_python_small_and_round_trippable`, `test_v2_source_contract_rejects_whole_file_integrity_mutations`, and `test_v2_rebuild_refreshes_edited_model_requirement`. No new failures. Captured in `suite-194.txt`; process exit 1 is expected for this baseline-matching red.

3. Focused set including memo/read-set/race/warm regression and the three same-metadata tests:

   `cd /tmp/option-a && PYTEST_ADDOPTS=-rA nice -n 19 /tmp/vibecomfy-witness-env/bin/python -m pytest -q tests/test_bundle_class_memo.py tests/test_bundle_final_witness.py tests/test_bundle_identity_memo.py tests/test_bundle_memo_lifetime.py tests/test_bundle_witness_cleanup.py tests/test_first_read_pack_race.py tests/test_bundle_readset_exploration.py tests/test_bundle_warm_generation_regression.py tests/test_porting_object_info.py::test_cache_file_witness_detects_same_size_same_mtime_replacement tests/test_porting_object_info.py::test_committed_reader_observes_same_size_same_mtime_current_replacement tests/test_porting_object_info.py::test_batch_reader_observes_same_size_same_mtime_pack_replacement`

   Result: 33 passed. Captured in `focused-33.txt`.

4. Reviewer configured-root and warm-generation regressions, plus end-check option probes:

   `cd /tmp/option-a && PYTEST_ADDOPTS=-rA nice -n 19 /tmp/vibecomfy-witness-env/bin/python -m pytest -vv -rA tests/test_bundle_root_redirect.py tests/test_bundle_warm_generation_regression.py tests/test_bundle_end_strategies.py`

   Result: 6 passed: configured-root redirect, warm Spare pack corruption, root-repoint under both end strategies, and same-size/restored-mtime probes under both strategies. Captured in `reviewer-regressions.txt`.

5. `cache_file_witness` verification: extracted the function from the `950023c8` version and candidate with Python AST source segments and compared their source bytes. Result: identical (`True`). The full generation.py diff is recorded in `cache-file-witness.diff`; surrounding code adds the read observer, but the function itself is unchanged.

No product files or existing tests were edited by this check task. No timing measurements were run. Lock inspected before tests: `/tmp/astrid-timing.lock` existed, was empty, and had Nov 22 timestamp.
