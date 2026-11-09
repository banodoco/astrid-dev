# Release 12: pre-existing test failures (bucket A)

[Plan 39](../inputs.md) · [Tasks](../tasks.md)

**Scope of this PR:** bucket A only, 323 failing test ids. This PR does not change Plan 39's tasks; its G1 re-measure picks this up.

## Purpose

While checking Release 12 (Plan 29), these test ids failed. They fail on served release 11 (a105de3a), so they are not Release 12 regressions. Whether each passed on Release 10 is not measured here. They are recorded here so none is lost.

## Source

- Run: served-11 pass-set split, worker session `session_011EzfW3McbuncNMVNJhDqTN`.
- Commit: `a105de3a4852cb61b9647dfe2c920118bd29f272`.
- Selector, on the 83-file list:

```
python -m pytest -q -rA -p no:cacheprovider --continue-on-collection-errors --deselect tests/core/generation/test_closure_install_cpu.py::test_linux_x86_64_h3_environment_closure_before_model_stages
```

<details><summary>83 test files in the selector</summary>

```
tests/editing_conformance/test_runner_selftest.py
tests/integrations/test_runpod_h3_host_r5.py
tests/packs/rendering/test_timeline_visualize_motion_views.py
tests/reshape/test_check_doc_references.py
tests/scripts/test_pod_h3_install.py
tests/scripts/test_pod_held_budget.py
tests/scripts/test_pod_jobs.py
tests/scripts/test_pod_session.py
tests/sdk/test_generation_variant_publication.py
tests/sdk/test_h3_endpoint_r4.py
tests/sdk/test_runpod_front_door.py
tests/sdk/test_scene_save_core.py
tests/sdk/test_timeline_checkout.py
tests/sdk/test_timeline_import_prepare.py
tests/sdk/test_timeline_look.py
tests/sdk/test_timeline_param_values.py
tests/sdk/test_timeline_revision_diff_admission.py
tests/stage1/test_asset_cache_retired_luna.py
tests/stage1/test_capability_parity_gate_luna.py
tests/stage1/test_core_import_authority.py
tests/stage1/test_final_render_authority_luna.py
tests/stage1/test_generic_host_process_bootstrap_luna.py
tests/stage1/test_kernel_admission_runtime.py
tests/stage1/test_pack_api_surface.py
tests/stage1/test_thread_authority_cutover.py
tests/stage1/test_zero_shim_execution_pack_deletion.py
tests/stage1/test_zero_shim_lane_c.py
tests/stage1/test_zero_shim_timeline_cutover_luna.py
tests/test_artifact_manifest.py
tests/test_astrid_beta_capability_matrix.py
tests/test_canonical_aliases.py
tests/test_creator_entry_declarations.py
tests/test_diagnostics_callers.py
tests/test_env_vars_conformance.py
tests/test_external_pack_contract.py
tests/test_generic_host.py
tests/test_generic_host_result_json.py
tests/test_installed_generation_journey.py
tests/test_installer_app_update.py
tests/test_installer_bootstrap_schema.py
tests/test_installer_cli_recovery.py
tests/test_installer_local_update.py
tests/test_installer_pinokio_lifecycle.py
tests/test_installer_pinokio_locking.py
tests/test_installer_platforms.py
tests/test_installer_pre_stop_recovery.py
tests/test_installer_r0_entry.py
tests/test_installer_schema.py
tests/test_installer_sources.py
tests/test_installer_transaction_authority.py
tests/test_installer_update_end_to_end.py
tests/test_live_capability_discovery_fix.py
tests/test_mcp_generation_parity.py
tests/test_mcp_server.py
tests/test_omp_agent.py
tests/test_platform_matrix.py
tests/test_provider_route_grant.py
tests/test_sdk_public_surface.py
tests/test_skills_cli.py
tests/test_skills_developer.py
tests/test_skills_installed_composition.py
tests/test_skills_package_data.py
tests/test_skills_selected_composition.py
tests/test_skills_sync_registry.py
tests/test_skip_policy.py
tests/test_structure_contracts.py
tests/test_third_party_integration.py
tests/test_timeline_editing_helpers.py
tests/test_vendor_lock.py
tests/test_vibecomfy_pin.py
tests/test_windows_gpu_availability.py
tests/timeline/test_authoring_bundle.py
tests/timeline/test_authoring_feedback.py
tests/timeline/test_effects_catalog.py
tests/timeline/test_html_canvas_effect.py
tests/timeline/test_shot_composition_projection.py
tests/timeline/test_shot_layering_projection.py
tests/timeline/test_timeline_elements_catalog.py
tests/v10/test_authority_lint.py
tests/v10/test_docs_cli_alignment.py
tests/v10/test_domain_cli_projects_timelines.py
tests/v10/test_pack_write_path_lint.py
tests/v10/test_release_reproducibility.py
```

</details>

- Count in this bucket: **323** failing ids on served 11.

## Per-file count

| File | Count |
|---|---|
| `tests/editing_conformance/test_runner_selftest.py` | 1 |
| `tests/integrations/test_runpod_h3_host_r5.py` | 1 |
| `tests/reshape/test_check_doc_references.py` | 1 |
| `tests/scripts/test_pod_h3_install.py` | 5 |
| `tests/scripts/test_pod_held_budget.py` | 4 |
| `tests/scripts/test_pod_jobs.py` | 36 |
| `tests/scripts/test_pod_session.py` | 39 |
| `tests/sdk/test_generation_variant_publication.py` | 1 |
| `tests/sdk/test_h3_endpoint_r4.py` | 18 |
| `tests/sdk/test_runpod_front_door.py` | 25 |
| `tests/sdk/test_scene_save_core.py` | 1 |
| `tests/sdk/test_timeline_checkout.py` | 3 |
| `tests/sdk/test_timeline_import_prepare.py` | 2 |
| `tests/sdk/test_timeline_look.py` | 1 |
| `tests/sdk/test_timeline_param_values.py` | 10 |
| `tests/sdk/test_timeline_revision_diff_admission.py` | 1 |
| `tests/stage1/test_asset_cache_retired_luna.py` | 1 |
| `tests/stage1/test_capability_parity_gate_luna.py` | 1 |
| `tests/stage1/test_core_import_authority.py` | 2 |
| `tests/stage1/test_final_render_authority_luna.py` | 1 |
| `tests/stage1/test_generic_host_process_bootstrap_luna.py` | 1 |
| `tests/stage1/test_kernel_admission_runtime.py` | 1 |
| `tests/stage1/test_thread_authority_cutover.py` | 3 |
| `tests/stage1/test_zero_shim_execution_pack_deletion.py` | 4 |
| `tests/stage1/test_zero_shim_lane_c.py` | 2 |
| `tests/stage1/test_zero_shim_timeline_cutover_luna.py` | 1 |
| `tests/test_artifact_manifest.py` | 1 |
| `tests/test_astrid_beta_capability_matrix.py` | 4 |
| `tests/test_canonical_aliases.py` | 4 |
| `tests/test_creator_entry_declarations.py` | 3 |
| `tests/test_diagnostics_callers.py` | 2 |
| `tests/test_env_vars_conformance.py` | 1 |
| `tests/test_external_pack_contract.py` | 1 |
| `tests/test_generic_host.py` | 5 |
| `tests/test_generic_host_result_json.py` | 1 |
| `tests/test_installer_app_update.py` | 8 |
| `tests/test_installer_bootstrap_schema.py` | 1 |
| `tests/test_installer_local_update.py` | 1 |
| `tests/test_installer_pinokio_lifecycle.py` | 4 |
| `tests/test_installer_platforms.py` | 6 |
| `tests/test_installer_r0_entry.py` | 1 |
| `tests/test_installer_schema.py` | 3 |
| `tests/test_installer_sources.py` | 17 |
| `tests/test_installer_transaction_authority.py` | 2 |
| `tests/test_live_capability_discovery_fix.py` | 4 |
| `tests/test_mcp_generation_parity.py` | 2 |
| `tests/test_mcp_server.py` | 1 |
| `tests/test_omp_agent.py` | 3 |
| `tests/test_platform_matrix.py` | 1 |
| `tests/test_provider_route_grant.py` | 1 |
| `tests/test_sdk_public_surface.py` | 27 |
| `tests/test_skills_cli.py` | 2 |
| `tests/test_skills_developer.py` | 3 |
| `tests/test_skills_installed_composition.py` | 1 |
| `tests/test_skills_package_data.py` | 3 |
| `tests/test_skills_selected_composition.py` | 3 |
| `tests/test_skills_sync_registry.py` | 6 |
| `tests/test_skip_policy.py` | 1 |
| `tests/test_structure_contracts.py` | 2 |
| `tests/test_third_party_integration.py` | 3 |
| `tests/test_timeline_editing_helpers.py` | 3 |
| `tests/test_vendor_lock.py` | 1 |
| `tests/test_vibecomfy_pin.py` | 1 |
| `tests/test_windows_gpu_availability.py` | 5 |
| `tests/timeline/test_authoring_bundle.py` | 1 |
| `tests/timeline/test_authoring_feedback.py` | 2 |
| `tests/timeline/test_effects_catalog.py` | 4 |
| `tests/timeline/test_html_canvas_effect.py` | 1 |
| `tests/timeline/test_shot_composition_projection.py` | 1 |
| `tests/timeline/test_shot_layering_projection.py` | 1 |
| `tests/timeline/test_timeline_elements_catalog.py` | 1 |
| `tests/v10/test_authority_lint.py` | 1 |
| `tests/v10/test_docs_cli_alignment.py` | 3 |
| `tests/v10/test_domain_cli_projects_timelines.py` | 1 |
| `tests/v10/test_pack_write_path_lint.py` | 2 |
| `tests/v10/test_release_reproducibility.py` | 1 |
| **Total (76 files)** | **323** |

## Known causes

- **`tests/scripts/test_pod_jobs.py` (36 ids): cause traced.** It traces to commit `4ce4e651f` "Close the composed H3 source and dependency closure", which is already in `a105de3a`.
- **All other files: cause not traced in this record.** Nothing here claims a cause for them.

## Note on the closure install test

`tests/core/generation/test_closure_install_cpu.py::test_linux_x86_64_h3_environment_closure_before_model_stages` is marked `opt_in`. It is deselected in the selector above. It needs a wheelhouse or cache in the lanes-opt-in job. This is the **Plan 39 wheelhouse need**.

## Scope: what this PR does not cover

This PR covers **bucket A only**. A follow-up will add:

- the 160 failing-on-both list;
- the absent-on-R10 list;
- the Runtime candidate-and-main red names;
- mypy's 158.

## Failing ids (bucket A, 323)

### `tests/editing_conformance/test_runner_selftest.py` (1)

- `tests/editing_conformance/test_runner_selftest.py::test_refusal_parity_on_an_unknown_key`

### `tests/integrations/test_runpod_h3_host_r5.py` (1)

- `tests/integrations/test_runpod_h3_host_r5.py::test_h3_freezes_policy_into_default_local_stages`

### `tests/reshape/test_check_doc_references.py` (1)

- `tests/reshape/test_check_doc_references.py::test_committed_catalog_is_fresh_for_the_in_repo_packs`

### `tests/scripts/test_pod_h3_install.py` (5)

- `tests/scripts/test_pod_h3_install.py::test_fresh_canonical_install_refuses_nonprivate_volume_before_any_process`
- `tests/scripts/test_pod_h3_install.py::test_install_integrity_failure_reports_canonical_phase_without_exception_details`
- `tests/scripts/test_pod_h3_install.py::test_install_selected_rechecks_source_identity_after_install`
- `tests/scripts/test_pod_h3_install.py::test_install_selected_recovers_legacy_receipt_and_returns_ready_attestation`
- `tests/scripts/test_pod_h3_install.py::test_install_selected_rejects_readiness_mismatch`

### `tests/scripts/test_pod_held_budget.py` (4)

- `tests/scripts/test_pod_held_budget.py::test_late_staging_failure_measures_four_record_shortfall`
- `tests/scripts/test_pod_held_budget.py::test_staged_candidate_plus_installer_h3_measured_budget`
- `tests/scripts/test_pod_held_budget.py::test_staging_failure_and_exact_reconciliation_measured_allowance[lost-stage-response]`
- `tests/scripts/test_pod_held_budget.py::test_staging_failure_and_exact_reconciliation_measured_allowance[terminal-stage-failure]`

### `tests/scripts/test_pod_jobs.py` (36)

- `tests/scripts/test_pod_jobs.py::test_budget_exhaustion_still_releases_without_allocating_a_record`
- `tests/scripts/test_pod_jobs.py::test_cold_claim_keeps_recipe_storage_reserve`
- `tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[command]`
- `tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[hash]`
- `tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[json]`
- `tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[png]`
- `tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[runtime]`
- `tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[sanity]`
- `tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[exact-20gb]`
- `tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[installed-pod-headroom]`
- `tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[insufficient-20gb]`
- `tests/scripts/test_pod_jobs.py::test_held_joblist_runs_fresh_mixed_rows_and_keeps_custody[False]`
- `tests/scripts/test_pod_jobs.py::test_held_joblist_runs_fresh_mixed_rows_and_keeps_custody[True]`
- `tests/scripts/test_pod_jobs.py::test_held_joblist_uncertain_row_keeps_in_use_operation_and_snapshot`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_progress_start_response_loss_keeps_exact_operation`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_repeated_terminal_failures_exhaust_durable_budget`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_reservation_persistence_failure_never_dispatches`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_terminal_proof_needs_separate_turn_before_same_pod_retry`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_terminal_receipt_persistence_failure_stays_in_use`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[cancel-error]`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[cancelled]`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[interrupt]`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[lost-start-response]`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[malformed-terminal]`
- `tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[timeout]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[None]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[evidence]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[identity]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[install]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[result]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[timeout]`
- `tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[uncertain]`
- `tests/scripts/test_pod_jobs.py::test_transient_detached_poll_failure_retains_only_recoverable_followup[followup]`
- `tests/scripts/test_pod_jobs.py::test_transient_followup_diagnostic_or_persistence_error_retains_retry_custody[diagnostic]`
- `tests/scripts/test_pod_jobs.py::test_transient_followup_diagnostic_or_persistence_error_retains_retry_custody[persistence]`
- `tests/scripts/test_pod_jobs.py::test_two_job_cpu_loopback_packets_progress_budget_and_release`

### `tests/scripts/test_pod_session.py` (39)

- `tests/scripts/test_pod_session.py::test_actual_legacy_sdk_mount_path_projection_refuses_before_private_upload[/other]`
- `tests/scripts/test_pod_session.py::test_actual_legacy_sdk_mount_path_projection_refuses_before_private_upload[/workspace/../other]`
- `tests/scripts/test_pod_session.py::test_actual_legacy_sdk_mount_path_projection_refuses_before_private_upload[187]`
- `tests/scripts/test_pod_session.py::test_claim_arguments_and_gpu_fallback`
- `tests/scripts/test_pod_session.py::test_container_disk_is_sized_from_the_recipe`
- `tests/scripts/test_pod_session.py::test_https_bootstrap_sdk_serialization_roundtrips`
- `tests/scripts/test_pod_session.py::test_install_sets_the_gpu_sanity_command`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[absent-pod]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[capacity]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[duplicate-json]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[duplicate-path]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[duplicate]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[empty-id]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[exact]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[legacy-object]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[list-id]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[malformed-collection]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[malformed-json]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[malformed-row]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[missing-id]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[missing]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[mount-device]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[mount-duplicate]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[mount-malformed]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[mount-missing]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[null]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[numeric-id]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[opaque]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[readonly-int]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[readonly]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[stale]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[timeout]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[unavailable]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[unjoinable]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[wrong-path]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[wrong-pod]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[wrong-type]`
- `tests/scripts/test_pod_session.py::test_provider_attachment_through_real_lifecycle_json_guards_probe_bundle_install[wrong]`
- `tests/scripts/test_pod_session.py::test_reused_workdir_cannot_retain_stale_storage_observation`

### `tests/sdk/test_generation_variant_publication.py` (1)

- `tests/sdk/test_generation_variant_publication.py::test_specialized_publication_actions_opt_in_through_registered_metadata`

### `tests/sdk/test_h3_endpoint_r4.py` (18)

- `tests/sdk/test_h3_endpoint_r4.py::test_parent_rechecks_input_bytes_after_paid_handoff`
- `tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[attestation]`
- `tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[origin]`
- `tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[owner]`
- `tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[warm-lease]`
- `tests/sdk/test_h3_endpoint_r4.py::test_recovery_reuses_retained_endpoint_and_refuses_substitution`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_preflight_and_parent_freeze_one_endpoint_with_all_local_stages`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[approval-type]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[changed-endpoint]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[cold]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[controls]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[missing-node]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[multipass]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[placeholder]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[t9-empty]`
- `tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[t9]`
- `tests/sdk/test_h3_endpoint_r4.py::test_staged_parent_hands_exact_graph_to_local_run[changed-bindings]`
- `tests/sdk/test_h3_endpoint_r4.py::test_staged_parent_hands_exact_graph_to_local_run[exact]`

### `tests/sdk/test_runpod_front_door.py` (25)

- `tests/sdk/test_runpod_front_door.py::test_absent_host_interface_is_a_blocked_sdk_and_cli_envelope[image]`
- `tests/sdk/test_runpod_front_door.py::test_absent_host_interface_is_a_blocked_sdk_and_cli_envelope[video]`
- `tests/sdk/test_runpod_front_door.py::test_cli_no_wait_text_returns_task_without_claiming_completion[image]`
- `tests/sdk/test_runpod_front_door.py::test_cli_no_wait_text_returns_task_without_claiming_completion[video]`
- `tests/sdk/test_runpod_front_door.py::test_cli_paid_flags_match_sdk_and_retain_admission[image]`
- `tests/sdk/test_runpod_front_door.py::test_cli_paid_flags_match_sdk_and_retain_admission[video]`
- `tests/sdk/test_runpod_front_door.py::test_foreign_binding_on_follow_never_reactivates[image]`
- `tests/sdk/test_runpod_front_door.py::test_foreign_binding_on_follow_never_reactivates[video]`
- `tests/sdk/test_runpod_front_door.py::test_h3_no_wait_uses_prepared_child_and_preserves_parent_default`
- `tests/sdk/test_runpod_front_door.py::test_invalid_entry_values_and_raw_source_block_before_claim[image]`
- `tests/sdk/test_runpod_front_door.py::test_invalid_entry_values_and_raw_source_block_before_claim[video]`
- `tests/sdk/test_runpod_front_door.py::test_no_wait_retains_exact_custody_when_activation_is_uncertain[image]`
- `tests/sdk/test_runpod_front_door.py::test_no_wait_retains_exact_custody_when_activation_is_uncertain[video]`
- `tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[image-False]`
- `tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[image-True]`
- `tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[video-False]`
- `tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[video-True]`
- `tests/sdk/test_runpod_front_door.py::test_release_denial_keeps_the_runtime_task_and_blocked_envelope[image]`
- `tests/sdk/test_runpod_front_door.py::test_release_denial_keeps_the_runtime_task_and_blocked_envelope[video]`
- `tests/sdk/test_runpod_front_door.py::test_target_describe_and_release_use_typed_owner_without_claim[image]`
- `tests/sdk/test_runpod_front_door.py::test_target_describe_and_release_use_typed_owner_without_claim[video]`
- `tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[image-False]`
- `tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[image-True]`
- `tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[video-False]`
- `tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[video-True]`

### `tests/sdk/test_scene_save_core.py` (1)

- `tests/sdk/test_scene_save_core.py::test_publish_still_refuses_core_invalidity_before_writing[type]`

### `tests/sdk/test_timeline_checkout.py` (3)

- `tests/sdk/test_timeline_checkout.py::test_a_nested_param_takes_a_moment_and_check_rejects_text_in_a_number`
- `tests/sdk/test_timeline_checkout.py::test_check_blocks_a_literal_formula_string_where_the_element_wants_a_frame`
- `tests/sdk/test_timeline_checkout.py::test_python_setters_are_discoverable_and_refuse_what_is_not_a_param`

### `tests/sdk/test_timeline_import_prepare.py` (2)

- `tests/sdk/test_timeline_import_prepare.py::test_builtin_hold_clip_round_trips_through_inventory_and_prepare`
- `tests/sdk/test_timeline_import_prepare.py::test_inventory_to_prepare_reports_unknown_unpinned_transition_from_source_pack`

### `tests/sdk/test_timeline_look.py` (1)

- `tests/sdk/test_timeline_look.py::test_set_volume_on_an_element_that_declares_volume_keeps_writing_the_param`

### `tests/sdk/test_timeline_param_values.py` (10)

- `tests/sdk/test_timeline_param_values.py::test_a_number_is_fine_where_an_integer_is_declared_and_a_px_position_is_a_number`
- `tests/sdk/test_timeline_param_values.py::test_all_or_nothing_when_one_key_is_bad`
- `tests/sdk/test_timeline_param_values.py::test_an_undeclared_key_is_left_to_the_key_check`
- `tests/sdk/test_timeline_param_values.py::test_enum_refuses_a_value_outside_the_schema_and_names_the_allowed_ones`
- `tests/sdk/test_timeline_param_values.py::test_integer_range_refuses_above_the_maximum_and_below_the_minimum`
- `tests/sdk/test_timeline_param_values.py::test_the_logical_grid_range_is_checked_on_the_stored_value`
- `tests/sdk/test_timeline_param_values.py::test_the_sheet_refuses_a_bad_range_on_the_rocket`
- `tests/sdk/test_timeline_param_values.py::test_the_sheet_refuses_a_bad_value_and_writes_nothing`
- `tests/sdk/test_timeline_param_values.py::test_tl_add_refuses_an_out_of_enum_value_before_the_clip_exists`
- `tests/sdk/test_timeline_param_values.py::test_type_refuses_a_string_for_a_number_and_a_bool_for_a_number`

### `tests/sdk/test_timeline_revision_diff_admission.py` (1)

- `tests/sdk/test_timeline_revision_diff_admission.py::test_element_resource_producer_binds_real_admitted_motion_without_config_mutation`

### `tests/stage1/test_asset_cache_retired_luna.py` (1)

- `tests/stage1/test_asset_cache_retired_luna.py::test_live_media_code_has_no_retired_asset_cache_boundary`

### `tests/stage1/test_capability_parity_gate_luna.py` (1)

- `tests/stage1/test_capability_parity_gate_luna.py::test_stage1_capability_parity_is_explicit_and_family_proven`

### `tests/stage1/test_core_import_authority.py` (2)

- `tests/stage1/test_core_import_authority.py::test_sdk_dry_run_is_manifest_only_and_does_not_load_runtime_authority`
- `tests/stage1/test_core_import_authority.py::test_sdk_orchestrator_dry_run_is_manifest_only`

### `tests/stage1/test_final_render_authority_luna.py` (1)

- `tests/stage1/test_final_render_authority_luna.py::test_attached_render_module_and_nested_runner_are_deleted`

### `tests/stage1/test_generic_host_process_bootstrap_luna.py` (1)

- `tests/stage1/test_generic_host_process_bootstrap_luna.py::test_generic_host_process_preflights_and_reports_readiness`

### `tests/stage1/test_kernel_admission_runtime.py` (1)

- `tests/stage1/test_kernel_admission_runtime.py::test_admission_and_normal_callers_have_no_local_composition`

### `tests/stage1/test_thread_authority_cutover.py` (3)

- `tests/stage1/test_thread_authority_cutover.py::test_live_pack_imports_do_not_reach_retired_thread_store`
- `tests/stage1/test_thread_authority_cutover.py::test_logo_dry_run_publishes_manifest_without_variant_sidecar`
- `tests/stage1/test_thread_authority_cutover.py::test_video_editing_orchestrators_have_no_pack_event_sidecar_writer`

### `tests/stage1/test_zero_shim_execution_pack_deletion.py` (4)

- `tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_discovers_explicit_astrid_packs_path_without_default_scan`
- `tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_runs_external_python_orchestrator_from_admitted_pack`
- `tests/stage1/test_zero_shim_execution_pack_deletion.py::test_in_process_runtime_and_pack_install_authority_are_absent`
- `tests/stage1/test_zero_shim_execution_pack_deletion.py::test_supported_cleanup_paths_use_kernel_custody_and_anchored_group_signal`

### `tests/stage1/test_zero_shim_lane_c.py` (2)

- `tests/stage1/test_zero_shim_lane_c.py::test_iteration_does_not_write_run_sidecars[astrid/packs/iteration/actions/experiment_import/run.py]`
- `tests/stage1/test_zero_shim_lane_c.py::test_iteration_does_not_write_run_sidecars[astrid/packs/iteration/actions/experiment_prepare/run.py]`

### `tests/stage1/test_zero_shim_timeline_cutover_luna.py` (1)

- `tests/stage1/test_zero_shim_timeline_cutover_luna.py::test_pack_workers_are_result_only_and_have_no_timeline_write_binding`

### `tests/test_artifact_manifest.py` (1)

- `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current`

### `tests/test_astrid_beta_capability_matrix.py` (4)

- `tests/test_astrid_beta_capability_matrix.py::test_beta_matrix_covers_every_discovered_capability_and_declaration`
- `tests/test_astrid_beta_capability_matrix.py::test_beta_reference_family_preflight_is_truthful_on_this_machine`
- `tests/test_astrid_beta_capability_matrix.py::test_manifest_secrets_report_missing_without_gating_readiness`
- `tests/test_astrid_beta_capability_matrix.py::test_video_understanding_matrix_matches_manifest_credentials`

### `tests/test_canonical_aliases.py` (4)

- `tests/test_canonical_aliases.py::CanonicalAliasTest::test_executor_api_uses_canonical_implementation`
- `tests/test_canonical_aliases.py::CanonicalAliasTest::test_orchestrator_api_uses_canonical_implementation`
- `tests/test_canonical_aliases.py::TimelineProductParserAliasTest::test_product_timeline_parser_exposes_only_the_supported_verbs`
- `tests/test_canonical_aliases.py::TimelineProductParserAliasTest::test_product_timeline_parser_has_no_obsolete_aliases`

### `tests/test_creator_entry_declarations.py` (3)

- `tests/test_creator_entry_declarations.py::test_changed_pack_declarations_pass_pack_validation`
- `tests/test_creator_entry_declarations.py::test_only_declared_generation_actions_carry_generation_publication`
- `tests/test_creator_entry_declarations.py::test_pack_intent_projection_keeps_creator_selection_clear`

### `tests/test_diagnostics_callers.py` (2)

- `tests/test_diagnostics_callers.py::test_new_failed_job_is_not_hidden_by_prior_direct_journal[complete]`
- `tests/test_diagnostics_callers.py::test_new_failed_job_is_not_hidden_by_prior_direct_journal[rolled_back]`

### `tests/test_env_vars_conformance.py` (1)

- `tests/test_env_vars_conformance.py::TestNoBareStringAccess::test_no_catalogued_bare_strings_in_core`

### `tests/test_external_pack_contract.py` (1)

- `tests/test_external_pack_contract.py::test_external_pack_via_env_path`

### `tests/test_generic_host.py` (5)

- `tests/test_generic_host.py::test_host_acknowledges_a_pending_packs_add_through_its_one_registrar`
- `tests/test_generic_host.py::test_host_execution_failure_keeps_coded_fields_and_recovery[astrid]`
- `tests/test_generic_host.py::test_host_execution_failure_keeps_coded_fields_and_recovery[exec]`
- `tests/test_generic_host.py::test_host_execution_failure_keeps_coded_fields_and_recovery[sdk]`
- `tests/test_generic_host.py::test_host_without_explicit_roots_discovers_the_personal_collection`

### `tests/test_generic_host_result_json.py` (1)

- `tests/test_generic_host_result_json.py::test_request_digest_does_not_depend_on_attempt_or_materialized_paths`

### `tests/test_installer_app_update.py` (8)

- `tests/test_installer_app_update.py::test_local_verification_rejects_mismatched_managed_version_identity[managed_by-discovery]`
- `tests/test_installer_app_update.py::test_local_verification_rejects_mismatched_managed_version_identity[managed_by-health]`
- `tests/test_installer_app_update.py::test_local_verification_rejects_mismatched_managed_version_identity[release-discovery]`
- `tests/test_installer_app_update.py::test_local_verification_rejects_mismatched_managed_version_identity[release-health]`
- `tests/test_installer_app_update.py::test_local_verification_rejects_mismatched_transaction_binding`
- `tests/test_installer_app_update.py::test_local_verification_rejects_missing_raw_managed_identity[None]`
- `tests/test_installer_app_update.py::test_local_verification_rejects_missing_raw_managed_identity[owner_health1]`
- `tests/test_installer_app_update.py::test_local_verification_rejects_missing_raw_managed_identity[owner_health2]`

### `tests/test_installer_bootstrap_schema.py` (1)

- `tests/test_installer_bootstrap_schema.py::test_staged_canonical_schema_reaches_strict_consumer`

### `tests/test_installer_local_update.py` (1)

- `tests/test_installer_local_update.py::test_recovery_routing_refuses_local_journal_in_ordinary_paths`

### `tests/test_installer_pinokio_lifecycle.py` (4)

- `tests/test_installer_pinokio_lifecycle.py::test_pinokio_doctor_without_root_follows_per_user_pointer`
- `tests/test_installer_pinokio_lifecycle.py::test_reset_removed_pinokio_root_releases_pointer_for_terminal_install`
- `tests/test_installer_pinokio_lifecycle.py::test_root_marker_retains_pinokio_manager_for_update_and_uninstall[mode1]`
- `tests/test_installer_pinokio_lifecycle.py::test_second_pinokio_root_is_allowed_after_first_root_is_deleted`

### `tests/test_installer_platforms.py` (6)

- `tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-17391-17393-17393]`
- `tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-17391-None-17391]`
- `tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-None-None-17340]`
- `tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[pinokio-17391-17393-17393]`
- `tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[pinokio-17391-None-17391]`
- `tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[pinokio-None-None-17340]`

### `tests/test_installer_r0_entry.py` (1)

- `tests/test_installer_r0_entry.py::test_captures_match_real_r0_evidence`

### `tests/test_installer_schema.py` (3)

- `tests/test_installer_schema.py::test_optional_remotion_failure_does_not_block_staging[browser]`
- `tests/test_installer_schema.py::test_optional_remotion_failure_does_not_block_staging[npm]`
- `tests/test_installer_schema.py::test_staging_verifies_the_local_schema_before_declaring_services`

### `tests/test_installer_sources.py` (17)

- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[False-busy]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[False-preparation-failure]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[False-ready]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[False-rollback]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[True-busy]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[True-preparation-failure]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[True-ready]`
- `tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[True-rollback]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[73-None-False]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[73-None-True]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[73-pinokio-False]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[73-pinokio-True]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[None-None-False]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[None-None-True]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[None-pinokio-False]`
- `tests/test_installer_sources.py::test_stage_uses_source_overrides_and_records_manifest[None-pinokio-True]`
- `tests/test_installer_sources.py::test_vibecomfy_download_uses_the_pinned_fork`

### `tests/test_installer_transaction_authority.py` (2)

- `tests/test_installer_transaction_authority.py::test_cli_recovers_completed_stop_with_fresh_controller[stop-return-app]`
- `tests/test_installer_transaction_authority.py::test_cli_recovers_completed_stop_with_fresh_controller[stopped-app]`

### `tests/test_live_capability_discovery_fix.py` (4)

- `tests/test_live_capability_discovery_fix.py::test_hype_inputs_are_typed_and_preserved_in_command`
- `tests/test_live_capability_discovery_fix.py::test_networked_transcribe_sdk_dispatch_does_not_trip_orchestrator_guard`
- `tests/test_live_capability_discovery_fix.py::test_networked_understanding_describes_credentials_and_outputs`
- `tests/test_live_capability_discovery_fix.py::test_understand_dry_run_validates_mode_and_selected_modality`

### `tests/test_mcp_generation_parity.py` (2)

- `tests/test_mcp_generation_parity.py::test_generate_schema_and_argv_for_all_leaves`
- `tests/test_mcp_generation_parity.py::test_phase_one_tools_list_and_parser_registration`

### `tests/test_mcp_server.py` (1)

- `tests/test_mcp_server.py::test_invoke_returns_admission_and_task_refs`

### `tests/test_omp_agent.py` (3)

- `tests/test_omp_agent.py::test_generate_managed_dry_run_without_comfyui_returns_target_not_ready`
- `tests/test_omp_agent.py::test_installed_prompt_notice_preserves_overrides_and_names_packaged_skills`
- `tests/test_omp_agent.py::test_packaged_profile_resolves_skills_inside_selected_installation`

### `tests/test_platform_matrix.py` (1)

- `tests/test_platform_matrix.py::test_generation_platform_matrix_references_existing_packs_and_sources`

### `tests/test_provider_route_grant.py` (1)

- `tests/test_provider_route_grant.py::test_tcp_only_broker_retires_udp_even_when_manifest_marks_broker_managed`

### `tests/test_sdk_public_surface.py` (27)

- `tests/test_sdk_public_surface.py::test_discover_and_get_capability_expose_public_dtos`
- `tests/test_sdk_public_surface.py::test_discover_exposes_pack_declared_extension_metadata`
- `tests/test_sdk_public_surface.py::test_generate_attached_project_resolution_video`
- `tests/test_sdk_public_surface.py::test_generate_explicit_out_routing_video`
- `tests/test_sdk_public_surface.py::test_generate_explicit_project_routing_video`
- `tests/test_sdk_public_surface.py::test_generate_facade_handles_error_generation_result`
- `tests/test_sdk_public_surface.py::test_generate_facade_maps_contract_failures_and_openai_rejection`
- `tests/test_sdk_public_surface.py::test_generate_facade_maps_contract_failures_and_openai_route`
- `tests/test_sdk_public_surface.py::test_generate_facade_rejects_non_mapping_payload`
- `tests/test_sdk_public_surface.py::test_generate_out_wins_over_project_video`
- `tests/test_sdk_public_surface.py::test_generate_video_no_stderr_output`
- `tests/test_sdk_public_surface.py::test_generate_video_reconstructs_typed_result_from_generation_payload`
- `tests/test_sdk_public_surface.py::test_get_capability_supports_pack_declared_element_kinds_and_invalid_kind_errors`
- `tests/test_sdk_public_surface.py::test_invoke_executor_allows_project_without_explicit_out`
- `tests/test_sdk_public_surface.py::test_invoke_executor_discovers_universal_manifest_from_out_dir`
- `tests/test_sdk_public_surface.py::test_invoke_executor_ignores_domain_manifest_payload_paths`
- `tests/test_sdk_public_surface.py::test_invoke_executor_prefers_universal_manifest_path_from_payload`
- `tests/test_sdk_public_surface.py::test_invoke_executor_returns_manifest_preview_without_runner`
- `tests/test_sdk_public_surface.py::test_invoke_maps_executor_result_error_into_public_taxonomy`
- `tests/test_sdk_public_surface.py::test_invoke_maps_typed_sdk_exceptions_from_internal_failures`
- `tests/test_sdk_public_surface.py::test_invoke_missing_input_runner_errors_raise_sdk_missing_input`
- `tests/test_sdk_public_surface.py::test_invoke_rejects_elements_and_missing_executor_project`
- `tests/test_sdk_public_surface.py::test_invoke_uses_kernel_execution_boundary`
- `tests/test_sdk_public_surface.py::test_video_explicit_execution_validated_against_backends`
- `tests/test_sdk_public_surface.py::test_video_explicit_mode_validated`
- `tests/test_sdk_public_surface.py::test_video_mode_inference_flf_both_refs`
- `tests/test_sdk_public_surface.py::test_video_mode_inference_t2v_no_refs`

### `tests/test_skills_cli.py` (2)

- `tests/test_skills_cli.py::test_external_dir_off_dry_run_is_read_only_through_cli[install]`
- `tests/test_skills_cli.py::test_external_dir_off_dry_run_is_read_only_through_cli[sync]`

### `tests/test_skills_developer.py` (3)

- `tests/test_skills_developer.py::test_default_sync_installs_developing_astrid_but_not_the_developer_skills`
- `tests/test_skills_developer.py::test_developer_pack_declares_developing_astrid_and_developer_only_extras`
- `tests/test_skills_developer.py::test_developer_sync_installs_resolves_survives_resync_and_uninstalls`

### `tests/test_skills_installed_composition.py` (1)

- `tests/test_skills_installed_composition.py::test_installed_core_help_profile_and_selected_empty_sync`

### `tests/test_skills_package_data.py` (3)

- `tests/test_skills_package_data.py::test_default_composition_preserves_opt_outs_without_acquisition`
- `tests/test_skills_package_data.py::test_default_skill_policy_comes_from_pack_manifests`
- `tests/test_skills_package_data.py::test_retained_integrations_flow_through_existing_sync_selection`

### `tests/test_skills_selected_composition.py` (3)

- `tests/test_skills_selected_composition.py::test_capability_index_check_is_non_mutating`
- `tests/test_skills_selected_composition.py::test_selected_declarations_drive_views_and_mcp`
- `tests/test_skills_selected_composition.py::test_tool_catalog_selection_preserves_declared_bindings`

### `tests/test_skills_sync_registry.py` (6)

- `tests/test_skills_sync_registry.py::CheckTest::test_check_detects_stale_link`
- `tests/test_skills_sync_registry.py::RegistryBlockTest::test_deep_block_includes_skill_names`
- `tests/test_skills_sync_registry.py::SyncGatewayTest::test_deep_links_per_pack_and_prunes_stale`
- `tests/test_skills_sync_registry.py::SyncGatewayTest::test_deep_sync_prunes_disabled_managed_pack_but_keeps_foreign_entry`
- `tests/test_skills_sync_registry.py::SyncGatewayTest::test_gateway_only_links_core_and_writes_registry`
- `tests/test_skills_sync_registry.py::SyncGatewayTest::test_normal_sync_uses_writable_composed_view`

### `tests/test_skip_policy.py` (1)

- `tests/test_skip_policy.py::test_no_test_file_skips_by_hand`

### `tests/test_structure_contracts.py` (2)

- `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`
- `tests/test_structure_contracts.py::test_real_repo_top_level_matches_structure_constants`

### `tests/test_third_party_integration.py` (3)

- `tests/test_third_party_integration.py::test_env_backend_pack_registers_descriptor_and_dispatches_generate_image`
- `tests/test_third_party_integration.py::test_env_discovery_populates_sdk_discovery_dto`
- `tests/test_third_party_integration.py::test_env_element_pack_validates_loads_lists_and_reaches_sdk`

### `tests/test_timeline_editing_helpers.py` (3)

- `tests/test_timeline_editing_helpers.py::test_canonical_source_trim_speed_move_and_retime_intervals`
- `tests/test_timeline_editing_helpers.py::test_ripple_is_track_scoped_and_never_moves_audio`
- `tests/test_timeline_editing_helpers.py::test_ripple_shifts_canonical_intervals_without_touching_audio`

### `tests/test_vendor_lock.py` (1)

- `tests/test_vendor_lock.py::test_one_root_lock_covers_all_known_runtime_paths`

### `tests/test_vibecomfy_pin.py` (1)

- `tests/test_vibecomfy_pin.py::test_no_other_tracked_file_copies_the_pin`

### `tests/test_windows_gpu_availability.py` (5)

- `tests/test_windows_gpu_availability.py::test_execution_runs_and_labels_settlement_without_opt_in[False]`
- `tests/test_windows_gpu_availability.py::test_execution_runs_and_labels_settlement_without_opt_in[True]`
- `tests/test_windows_gpu_availability.py::test_failed_opt_in_run_retains_unqualified_label`
- `tests/test_windows_gpu_availability.py::test_unqualified_label_survives_other_readiness_failures`
- `tests/test_windows_gpu_availability.py::test_vibecomfy_remains_ready_when_nvidia_detection_is_lost`

### `tests/timeline/test_authoring_bundle.py` (1)

- `tests/timeline/test_authoring_bundle.py::test_approval_is_bound_to_candidate_and_base_revision`

### `tests/timeline/test_authoring_feedback.py` (2)

- `tests/timeline/test_authoring_feedback.py::test_document_emitter_provider_refuses_invalid_param_and_unverified_media[param]`
- `tests/timeline/test_authoring_feedback.py::test_document_emitter_provider_refuses_invalid_param_and_unverified_media[unknown]`

### `tests/timeline/test_effects_catalog.py` (4)

- `tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generated_fingerprint_changes_with_element_content`
- `tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_is_idempotent_for_package_outputs`
- `tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_outputs_package_owned_registries`
- `tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_requires_writable_package_outputs`

### `tests/timeline/test_html_canvas_effect.py` (1)

- `tests/timeline/test_html_canvas_effect.py::HtmlCanvasEffectExecutorTest::test_scaffold_writes_local_effect_and_report`

### `tests/timeline/test_shot_composition_projection.py` (1)

- `tests/timeline/test_shot_composition_projection.py::test_shot_only_layer_merge_matches_chapter_render_order_and_keeps_properties`

### `tests/timeline/test_shot_layering_projection.py` (1)

- `tests/timeline/test_shot_layering_projection.py::test_fixture_matches_canonical_runtime_bytes`

### `tests/timeline/test_timeline_elements_catalog.py` (1)

- `tests/timeline/test_timeline_elements_catalog.py::TimelineElementsCatalogTest::test_catalog_exposes_pack_declared_custom_kinds`

### `tests/v10/test_authority_lint.py` (1)

- `tests/v10/test_authority_lint.py::test_live_repository_tree_passes_authority_lint`

### `tests/v10/test_docs_cli_alignment.py` (3)

- `tests/v10/test_docs_cli_alignment.py::test_core_docs_have_no_retired_invocation_strings`
- `tests/v10/test_docs_cli_alignment.py::test_documented_commands_are_real_gateway_commands`
- `tests/v10/test_docs_cli_alignment.py::test_pack_stages_do_not_reference_retired_verbs`

### `tests/v10/test_domain_cli_projects_timelines.py` (1)

- `tests/v10/test_domain_cli_projects_timelines.py::test_timelines_show_human_output_reads_transform_keyframes`

### `tests/v10/test_pack_write_path_lint.py` (2)

- `tests/v10/test_pack_write_path_lint.py::test_schema_pack_code_never_calls_event_append_entrypoints`
- `tests/v10/test_pack_write_path_lint.py::test_schema_pack_code_never_takes_the_store_module_handle`

### `tests/v10/test_release_reproducibility.py` (1)

- `tests/v10/test_release_reproducibility.py::test_runtime_lock_covers_runpod_source_dependencies_without_source_distributions`
