# Unit shard 6 — run 43728670712

- Job id: 132856063530
- Head SHA: 37bd5e069492446bd62d94ff7aa40eb3143d8f85
- Conclusion: failure
- Pytest: = 246 failed, 4764 passed, 6 skipped, 26255 deselected, 55 warnings, 4 errors, 92 subtests passed in 6153.30s (1:42:33) =
- Wall time (log fetch, diff, and attribution): 8.30s

## New failures by owner lane

### machines
- tests/packs/runpod/test_ratchet_invariants.py::test_every_runpod_exception_name_is_receipt_safe_or_explicitly_excluded — no-baseline — 1e8b2faecc07 P6: restore/publish the engine snapshot around the canonical install (path tests/packs/runpod/test_ratchet_invariants.py)
- tests/packs/runpod/test_ratchet_invariants.py::test_runpod_host_target_operations_match_manifest_metadata — no-baseline — 1e8b2faecc07 P6: restore/publish the engine snapshot around the canonical install (path tests/packs/runpod/test_ratchet_invariants.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_allocation_unknown_persists_secret_free_marker_and_never_opens_another_window — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_defaults_bound_unattended_claim_to_one_hour — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_exact_match_cuda_filter_default_claim_list_covers_every_13x_from_recipe_minimum — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_success_atomically_replaces_marker_with_claim_handle_and_leaves_pod_running — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_unbounded_wait_requires_explicit_flag[arguments0] — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_unbounded_wait_requires_explicit_flag[arguments1] — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_claim_runpod_5090_backup.py::test_wait_forever_is_explicit_and_storage_help_names_override — no-baseline — f0d5d332fb73 Claim script tests: resume and wrong-account attach fakes follow the current seams (path tests/scripts/test_claim_runpod_5090_backup.py)
- tests/scripts/test_pod_session.py::test_claim_arguments_and_gpu_fallback — no-baseline — b6457bf99d91 Block RunPod network access in every test (path tests/scripts/test_pod_session.py)
- tests/scripts/test_pod_session.py::test_container_disk_is_sized_from_the_recipe — no-baseline — b6457bf99d91 Block RunPod network access in every test (path tests/scripts/test_pod_session.py)
- tests/scripts/test_pod_session.py::test_https_bootstrap_sdk_serialization_roundtrips — no-baseline — b6457bf99d91 Block RunPod network access in every test (path tests/scripts/test_pod_session.py)
- tests/scripts/test_pod_session.py::test_install_sets_the_gpu_sanity_command — no-baseline — b6457bf99d91 Block RunPod network access in every test (path tests/scripts/test_pod_session.py)
- tests/scripts/test_pod_session.py::test_reused_workdir_cannot_retain_stale_storage_observation — no-baseline — b6457bf99d91 Block RunPod network access in every test (path tests/scripts/test_pod_session.py)

### pre-lane rehearsal (Merge the generation candidate 1439ccc6 into the Release 13 )
- tests/scripts/test_cuda_default_sites.py::test_claim_script_reuses_the_module_default_list — no-baseline — a3dc1e4bcab7 T6b-4: remove the watch script and the managed-session fixture users (path tests/scripts/test_cuda_default_sites.py)
- tests/scripts/test_pod_action_source.py::test_receipt_diagnostic_checks_source_before_reading_and_never_creates_evidence[False] — no-baseline — a45dd06c49d0 Plan 32 T2b: one base engine keyed comfyui (path tests/scripts/test_pod_action_source.py)
- tests/scripts/test_pod_h3_install.py::test_fresh_canonical_install_refuses_nonprivate_volume_before_any_process — no-baseline — bc4e91a0bdde Plan 32 T6b-3 fix: tests no longer import the deleted h3 action modules (path tests/scripts/test_pod_h3_install.py)
- tests/scripts/test_pod_h3_install.py::test_receipt_only_diagnostic_is_private_and_cannot_start_or_repair[mismatch] — no-baseline — bc4e91a0bdde Plan 32 T6b-3 fix: tests no longer import the deleted h3 action modules (path tests/scripts/test_pod_h3_install.py)
- tests/sdk/test_generation_source_retention.py::test_public_workflow_freezes_execution_before_importer_changes_original[True] — no-baseline — bda5e839a5d1 Plan 32 T6b-3: docs for inputs, default_mode and engine facts; keep the generic action-entry mechanism, drop h3's (path tests/sdk/test_generation_source_retention.py)
- tests/sdk/test_host_recovery.py::test_foreground_retirement_is_bound_to_locked_support[True] — no-baseline — 890b1e1bdf6b Merge the generation candidate 1439ccc6 into the Release 13 rehearsal (path tests/sdk/test_host_recovery.py)
- tests/sdk/test_openai_image_admission.py::test_unqualified_target_request_keeps_local_comfyui_route — no-baseline — 7d419175b9eb Plan 32 T3: move generation test callers to placement= (path tests/sdk/test_openai_image_admission.py)

### test manager
- tests/reshape/test_compare_baselines.py::test_structure_baseline_script_runs_directly_from_outside_the_checkout — no-baseline — 8847df87e585 Gate lint ratchet on selected bug classes (path tests/reshape/test_compare_baselines.py)
- tests/reshape/test_compare_baselines.py::test_the_tree_has_exactly_the_baselined_structure_violations — no-baseline — 8847df87e585 Gate lint ratchet on selected bug classes (path tests/reshape/test_compare_baselines.py)

### unattributed
- tests/packs/timeline/test_visualize_drafts.py::test_visualize_reads_the_working_copy_with_banner_and_changed_cuts — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/packs/vibecomfy/test_local_launch_facts.py::test_probe_server_adds_only_verified_native_launch_facts — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/reshape/test_check_doc_references.py::test_committed_catalog_is_fresh_for_the_in_repo_packs — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/reshape/test_timeline_installed_skills.py::test_timeline_skill_lifecycle_on_installed_wheel — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_gpu_sanity.py::test_env_comes_from_engine_child_env_and_ignores_caller_ld_library_path — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_gpu_sanity.py::test_failing_python_exits_2_with_message_and_lib_paths — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_gpu_sanity.py::test_passing_stub_exits_0 — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_gpu_sanity.py::test_zero_exit_without_all_three_dtypes_still_fails — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_bootstrap_root_override_writes_marker_and_avoids_workspace — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_bootstrap_wires_sanity_before_engine_side_work_and_into_install — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_existing_packages_skip_install_but_still_get_pip_and_a_matching_probe_check — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_fresh_boot_orders_noneditable_package_pip_and_probe_check — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_gpu_sanity_failure_exits_2_and_names_the_venv — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_gpu_sanity_runs_when_engine_venv_present — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_gpu_sanity_skips_when_engine_venv_absent — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_identity_refusal_prevents_workspace_and_success_marker — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_large_freeze_and_present_pip_skip_all_install_commands — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_marker_rerun_still_verifies_installed_astrid — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_marker_with_missing_lifecycle_repairs_install — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_missing_lifecycle_is_installed_into_existing_managed_environment — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_no_hardcoded_cache_paths_or_curl — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_no_secret_variables — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_pip_check_is_after_package_install_and_before_marker — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_probe_check_reinstalls_astrid_when_installed_module_differs — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_probe_check_runs_on_rerun_and_after_package_install_and_never_cleans_engine_state — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_realm_and_venv_overrides_are_honoured — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_setup_runtime_is_called_after_install_and_never_starts_a_runtime — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_setup_runtime_with_real_runtime_creates_workspace_once — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_setup_runtime_writes_profile_and_is_idempotent — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_strict_mode_and_marker — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_syntax_ok — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_unwritable_root_fails_clearly — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_uv_missing_fails_clearly_without_curl — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_bootstrap.py::test_vibecomfy_is_in_noneditable_package_step_before_marker — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_held_budget.py::test_late_staging_failure_measures_four_record_shortfall — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_held_budget.py::test_staged_candidate_plus_installer_h3_measured_budget — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_held_budget.py::test_staging_failure_and_exact_reconciliation_measured_allowance[lost-stage-response] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_held_budget.py::test_staging_failure_and_exact_reconciliation_measured_allowance[terminal-stage-failure] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_budget_exhaustion_still_releases_without_allocating_a_record — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_cold_claim_keeps_recipe_storage_reserve — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[command] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[hash] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[json] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[png] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[runtime] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[sanity] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[exact-20gb] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[installed-pod-headroom] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[insufficient-20gb] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_joblist_runs_fresh_mixed_rows_and_keeps_custody[False] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_joblist_runs_fresh_mixed_rows_and_keeps_custody[True] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_joblist_uncertain_row_keeps_in_use_operation_and_snapshot — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_progress_start_response_loss_keeps_exact_operation — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_repeated_terminal_failures_exhaust_durable_budget — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_reservation_persistence_failure_never_dispatches — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_terminal_proof_needs_separate_turn_before_same_pod_retry — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_terminal_receipt_persistence_failure_stays_in_use — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[cancel-error] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[cancelled] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[interrupt] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[lost-start-response] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[malformed-terminal] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[timeout] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[None] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[evidence] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[identity] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[install] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[result] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[timeout] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[uncertain] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_transient_detached_poll_failure_retains_only_recoverable_followup[followup] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_transient_followup_diagnostic_or_persistence_error_retains_retry_custody[diagnostic] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_transient_followup_diagnostic_or_persistence_error_retains_retry_custody[persistence] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/scripts/test_pod_jobs.py::test_two_job_cpu_loopback_packets_progress_budget_and_release — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_checkout_publish_media_admission.py::test_publish_admits_new_media_and_retries_the_canonical_request — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_checkout_publish_media_admission.py::test_publish_refuses_foreign_media_without_writing — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_d124_shared_custody.py::test_single_inverse_keeps_endpoint_materializations_for_redo[2-2.0] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_generation_verified_preparation_gr03.py::test_complete_frozen_recipe_matches_members_and_detached_approval — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_generation_verified_preparation_gr03.py::test_missing_target_schema_fails_closed — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_generation_verified_preparation_gr03.py::test_opaque_target_model_alias_is_rejected — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_generation_verified_preparation_gr03.py::test_preparation_errors_do_not_try_another_catalog_candidate — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_generation_verified_preparation_gr03.py::test_randomness_is_resolved_before_binding_and_no_files_are_reopened_after_freeze — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_generation_verified_preparation_gr03.py::test_target_model_missing_from_actual_root_fails_closed — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_p1_case_corpus.py::test_manifest_is_complete_and_snapshots_are_provenanced — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_p1_case_corpus.py::test_real_canonical_documents_execute_the_recorded_edits[nested-closure-trim] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_p1_case_corpus.py::test_same_field_edit_is_a_real_refusal_case — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_p1_doc_patch_requests.py::test_request_set_is_provenanced_to_the_merged_corpus — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_p4_note_rerun.py::test_p4_note_conflict_reruns_public_function_from_verified_peer_document — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_projectless_admission.py::test_openai_generation_requires_explicit_publication_intent — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_runtime_response_conformance.py::test_commit_conflict_409_maps_to_conflict_and_keeps_its_details — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_runtime_response_conformance.py::test_commit_conflict_409_migration_keeps_details_request_id_and_request — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_runtime_response_conformance.py::test_every_recorded_case_is_present — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_selected_param_neutral_stage.py::test_occurrence_physical_owners_come_from_sealed_closure[None] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)
- tests/sdk/test_selected_param_neutral_stage.py::test_reselection_hold_param_preserves_exact_new_source[False] — no-baseline — no touching commit since R12 (likely an environment or ordering effect)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 23882 |
| candidate | 4994 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 132 |
| preexisting | 98 |
| fixed | 0 |
| missing | 21296 |
