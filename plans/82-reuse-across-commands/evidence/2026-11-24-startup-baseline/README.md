# Plan 82 startup baseline (24 November 2026)

What fails **on the unchanged `release/15/plan-82` branches** for the selectors each Plan 82 card names, before any packet. Packets compare against these ids; a packet's PR must show no new failure and no id from the "pass unchanged" sets that passed here failing there. Run by the Plan 82 orchestrator in a shared 4-vCPU container, with the worker-env scripts (`scripts/worker-env/agent-setup.sh`, `env/runtime-setup.sh`, `env/vc-setup.sh`).

| Repo | Head | Selectors | Result |
|---|---|---|---|
| astrid-agent | `514499de` | the 12 files and tests in [Agent selectors](#agent-selectors), default lane | 14 failed, 199 passed, 39 deselected (the lane, below) |
| astrid-agent, integration lane | `514499de` | `tests/packs/vibecomfy/test_local_server_run.py`, `tests/integrations/test_command_count_capture.py`, `tests/sdk/test_generation_stage_coverage.py` with `ASTRID_CI_JOB=lanes-integration -m "integration and not opt_in and not app_checkout"` | 1 failed, 41 passed, 1 deselected |
| astrid-agent, RA-1b set | `514499de` | `tests/packs/builtin/generate_image/test_e2e.py::test_e2e_cloud_never_imports_vibecomfy`, `tests/test_windows_posix_guard.py`, `tests/sdk/test_command_timings.py`, `tests/sdk/test_generation_stage_coverage.py`, `tests/test_vibecomfy_invocation_preflight.py`, `tests/integrations/test_command_count_capture.py` | 24 passed, 3 deselected by lane, 0 failed |
| astrid-runtime | `24e2c929` | `tests/test_task_admission_replay_identity.py`, `test_durable_terminal_results.py`, `test_task_storage_estimate.py`, `test_runtime_child_delegation.py`, `test_generation_publish_v1_settlement.py`, `test_runtime_boundary.py`, `test_render_admission_exact_retry.py` | 527 passed, 5 deselected, 0 failed |
| VibeComfy | `c0e910ca` | `tests/test_workflow_bundle.py`, `test_target_model_approval.py`, `test_target_model_bundle_custody.py`, `test_v26_canonical_parity.py`, `test_template_roundtrip.py`, `test_templates_module.py`, `test_ready_alias_identity.py`, `test_entries.py` | 11 failed, 493 passed, 72 skipped |

## Agent selectors

`tests/test_vibecomfy_invocation_preflight.py`, `tests/test_generation_dry_run_preflight.py`, `tests/test_generation_entries_invocation_preflight.py`, `tests/test_invocation_preflight_prompt_scope.py`, `tests/sdk/test_generation_target.py`, `tests/sdk/test_transcript_run.py`, `tests/sdk/test_execution_request_binding.py`, `tests/packs/vibecomfy/test_local_server_run.py`, `tests/sdk/test_generation_source_retention.py`, `tests/core/generation/test_entries.py`, `tests/core/generation/test_discovery_scope.py`, `tests/core/generation/test_managed_local_fallback_routing.py`.

## The failing ids

- Agent default lane: [agent-failing-ids.txt](agent-failing-ids.txt), 14 ids: 11 in `test_discovery_scope.py`, `test_generation_source_retention.py::test_public_workflow_freezes_execution_before_importer_changes_original[True]` and two in `test_generation_target.py` (`test_auto_probes_attached_before_managed_readiness`, `test_generate_without_claimed_machine_refuses_before_admission`). **All 14 are in the hosted baseline's failing lists for Release 14 and Release 15** ([agent-ci-baseline-8807f820](../../../../releases/15/evidence/agent-ci-baseline-8807f820/README.md)), so they are inherited, not yours, and not to be fixed in a packet.
- Agent integration lane: [agent-lane-failing-ids.txt](agent-lane-failing-ids.txt), one id: `tests/integrations/test_command_count_capture.py::test_fresh_process_command_counts`, failing here with `SourceIdentityError: hosted source closure is missing nested repositories` (the container has no hosted checkout layout). It is not in the hosted lists; treat it as an environment difference and do not count it for or against a packet.
- VibeComfy: [vibecomfy-failing-ids.txt](vibecomfy-failing-ids.txt), 11 ids. Causes seen: "object-info identity is unavailable ... Stage the matching custom_nodes.lock beside the loaded VibeComfy package" (the worker-env checkout has no staged lock), "missing eligible template" in `test_canonical_parity_baseline_matches_current_ready_templates`, and a few generated-source assertions. The Lead's earlier full fast suite at `c0e910ca` was 758 passed, 9 failed, 9 skipped; the 11 here are the same environment class. **`test_v26_canonical_parity.py::test_canonical_parity_baseline_matches_current_ready_templates` fails here on the unchanged base**: P82-05 may copy its loop pattern but must not depend on that test passing.
- Runtime: none.

## Tests the default lane leaves out (important)

`tests/packs/vibecomfy/test_local_server_run.py` (39 tests, including `test_seedless_rerun_uses_attempt_specific_save_prefix`), `tests/integrations/test_command_count_capture.py` and `tests/sdk/test_generation_stage_coverage.py::test_workflow_and_image_admissions_report_generation_stage_tree` are in the `integration` lane and are **deselected by default** ("left out of this run by lane"). `scripts/worker-env/agent-pytest.sh` runs `env -i`, so it cannot pass the lane variable. To run them, call the venv's Python directly from the checkout root (`E=<checkout>.env`):

```bash
env -i PATH="$E/venv/bin:$(cat $E/uv-dir):/usr/local/bin:/usr/bin:/bin" HOME="$E/home" TMPDIR="$E/tmp" \
  ASTRID_CI_JOB=lanes-integration XDG_CACHE_HOME="$E/cache" LANG=C.UTF-8 PYTHONNOUSERSITE=1 \
  PYTHONDONTWRITEBYTECODE=1 PYTHONSAFEPATH=1 PYTHONPATH="$E/vibecomfy" \
  ASTRID_RUNTIME_CHECKOUT="$E/runtime" ASTRID_VIBECOMFY_CHECKOUT="$E/vibecomfy" \
  ASTRID_TEST_LIFECYCLE_CHECKOUT="$E/lifecycle" \
  "$E/venv/bin/python" -m pytest -p no:cacheprovider -p no:randomly -q -rA \
  -m "integration and not opt_in and not app_checkout" <selectors>
```

A packet that cannot run this posts it in its `READY-PROOF`; the orchestrator runs the lane selectors on the exact head. The two named tests of Plan 82's RA-2 (`test_seedless_rerun_uses_attempt_specific_save_prefix` in the integration lane, passing here; `test_stale_bundle_rejects_before_target_or_admission`, default lane, passing here) both pass on the base.

## The import profile of a real `generate` (RA-0a, import part)

A real `astrid generate image ... --no-wait` runs from a dev checkout against the stand-in ComfyUI on loopback (script and summaries in [import-profile/](import-profile/); `run.sh` takes the stand-in's port). Warm run on a loaded box: 6.2 to 7.0 s wall, 1,267 modules, 1.1 to 1.5 s summed top-level import time. Largest cumulative imports, with their importer: `astrid.core.execution.generic_host` 0.6 s (from `sdk/host_bootstrap.py:2109 ensure_pack_host`, via `sdk/autobootstrap.py:526 ensure_runtime` and `sdk/client.py:469 open_from_launcher`); `astrid.core.generation.backends.comfy_schema` 0.16 s (from `sdk/generation.py` `_prepare_catalog_target_workflow` at 946 and `backends/vibecomfy.py:514`); `vibecomfy.porting.emit.ui` 0.15 s (from `workflow_bundle.py:2840 compile`/`materialize_ui` through `porting/emit/__init__.py:43`); `astrid.core.execution.capability_ledger` → `astrid.core.pack.loader` 0.13 s; `vibecomfy.comfy_nodes.agent.provider` 0.12 s; `vibecomfy.runtime.client`/`run` 0.12 s; `astrid.sdk.host_bootstrap` 0.09 s; `vibecomfy.comfy_nodes` 0.08 s; `numpy` 0.07 s (via `emit/ui.py:5889` → `porting/edit/ops.py:29` → `comfy_nodes/__init__.py:40` → `exec_node.py:12`); `httpx` 0.07 s. Imports are spread across the stages by the command's own collector, and `-X importtime` overstates the cost; the figure that counts is the stage time in `--timings` before and after.
