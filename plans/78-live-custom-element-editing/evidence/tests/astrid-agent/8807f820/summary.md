# Agent baseline, 22 November 2026

Candidate `8807f820eb47d6018db723511e024a0a123fbe95`; Python 3.13.18, Runtime `3c28211f3cb7ac4867ad744d8cdeeb38dd4484c5`, Node 20.19.4, locked Remotion dependencies; CPU. Command from the Agent root: `PYTEST_ADDOPTS=-rA bash scripts/worker-env/agent-pytest.sh -q tests/core/test_timeline_element_placement.py tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_commit_provider.py tests/core/test_elements_registry.py tests/core/pack/test_cli_manage.py tests/integrations/test_generic_host_pack_refresh_runtime.py`. Inner exit 1: 187 passed, 4 failed, 2 deselected by existing configuration. The first run lacked the pinned renderer tools; its 31 admission failures were environmental and the complete inventory was rerun after installing them. The table compares the corrected baseline with itself to classify its failing IDs. Raw logs are retained in the run directory.

| Side | Tests run |
|---|---|
| initial | 191 |
| candidate | 191 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 4 |
| fixed | 0 |
| missing | 0 |

Hosted comparison: Release 15 hosted run `45031908687` at the same Agent SHA lists `test_provider_accepts_trim_after_move_and_undoes_only_trim`, `test_stale_head_retries_original_plan_and_created_ids_once`, and `test_legacy_history_undo_and_restore_use_revisions_or_refuse_visibly` as failures. `test_move_reload_and_inverse_import_no_renderer` passes on hosted CI and is an environment difference, not an inherited hosted failure. The local wrapper sets `PYTHONSAFEPATH=1` and passes only the VibeComfy checkout in `PYTHONPATH`; the test's `python -c` child consequently cannot import `tests.helpers`. An interpreter import probe under those settings returned no module. The self-comparison `preexisting.txt` below is a mechanical baseline-versus-itself bucket, not the hosted classification. Candidate hosted CI is compared against the Release 15 hosted failing-ID list.
