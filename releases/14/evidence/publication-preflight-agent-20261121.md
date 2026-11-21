# Provisional Agent R13→R14 CI eight-shard comparison — 21 November 2026

**Diagnostic only — NOT publication qualification.** Published Agent source `959da7326c982a9197b5d6e2a4489f45e1deef0e` CI [43760673752](https://github.com/banodoco/astrid-agent/actions/runs/43760673752); pre-freeze Agent `0020c2e8d7f5d6051db2964a235b97f4ba002a72` CI [44651391760](https://github.com/banodoco/astrid-agent/actions/runs/44651391760). No workflow dispatched, tests unchanged. All missing/skipped original passes remain unresolved, not auto-renamed or excused. This provisional ledger groups pytest FAIL and ERROR in its count columns; the [original GHA logs](https://github.com/banodoco/astrid-agent/actions/runs/44651391760) retain the native distinctions, and the frozen comparator reports them separately. Recheck on **final frozen tuple** using [publication_diff.py](publication_diff.py).

| Job | R13 IDs (pass/fail/skip) | Provisional R14 IDs | PASS→FAIL | PASS→missing/skip | New failing | FAIL→PASS |
|---|---|---|---:|---:|---:|---:|
| unit shard 1 | 5314 (5214 pass, 97 fail, 3 skip) | 5356 (5255 pass, 98 fail, 3 skip) | 1 | 13 | 0 | 0 |
| unit shard 2 | 4003 (3852 pass, 132 fail, 19 skip) | 4039 (3887 pass, 133 fail, 19 skip) | 2 | 0 | 0 | 1 |
| unit shard 3 | 1858 (1827 pass, 31 fail, 0 skip) | 1912 (1881 pass, 31 fail, 0 skip) | 0 | 20 | 0 | 0 |
| unit shard 4 | 2045 (1998 pass, 47 fail, 0 skip) | 2077 (2030 pass, 47 fail, 0 skip) | 0 | 7 | 0 | 0 |
| unit shard 5 | 2415 (2213 pass, 202 fail, 0 skip) | 2418 (2216 pass, 202 fail, 0 skip) | 0 | 0 | 0 | 0 |
| unit shard 6 | 5130 (4907 pass, 217 fail, 6 skip) | 5271 (5023 pass, 242 fail, 6 skip) | 3 | 7 | 23 | 0 |
| unit shard 7 | 5892 (5494 pass, 396 fail, 2 skip) | 6200 (5782 pass, 399 fail, 19 skip) | 14 | 102 | 11 | 0 |
| unit shard 8 | 3914 (3786 pass, 100 fail, 28 skip) | 3638 (3538 pass, 89 fail, 11 skip) | 1 | 283 | 0 | 1 |

Unit shard per-job totals: **21 PASS→FAIL; 432 PASS→missing/skip; 34 new failing; 2 recovered**. Every difference below is an open discrepancy, NOT an accepted regression/disposition. These are pre-freeze candidate observations and not a final gate.

## unit shard 1

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543694) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006877968)

**PASS→FAIL — unresolved (1):**
- `tests/core/generation/test_h3_build_after_outputs.py::test_the_run_actions_after_outputs_spec_composes_the_candidate`

**PASS→missing/skip — omission or possible rename, not yet explained (13):**
- `tests/core/generation/test_attached_model_download.py::test_an_interrupted_download_leaves_no_partial_file`
- `tests/core/generation/test_pin_single_source.py::test_a_manifest_override_that_misses_the_canonical_pin_is_refused[override0]`
- `tests/core/generation/test_pin_single_source.py::test_a_manifest_override_that_misses_the_canonical_pin_is_refused[override1]`
- `tests/core/generation/test_pin_single_source.py::test_engine_contribution_recipe_digests_match_the_pinned_files`
- `tests/core/generation/test_pin_single_source.py::test_every_other_pin_file_agrees_on_shared_sources[vibecomfy]`
- `tests/core/generation/test_pin_single_source.py::test_every_other_pin_file_agrees_on_shared_sources[wan2gp]`
- `tests/core/generation/test_pin_single_source.py::test_literal_comfy_commits_in_workflows_are_the_canonical_pin`
- `tests/core/generation/test_pin_single_source.py::test_pack_manifests_require_the_canonical_lifecycle_version`
- `tests/core/generation/test_pin_single_source.py::test_packaged_runtime_lock_is_byte_identical_to_the_root_lock`
- `tests/core/generation/test_pin_single_source.py::test_pin_digests_bound_in_recipes_and_environments_match_the_files`
- `tests/core/generation/test_pin_single_source.py::test_pod_sources_come_from_the_canonical_pins`
- `tests/core/generation/test_pin_single_source.py::test_pyproject_lifecycle_dependency_is_the_canonical_pin`
- `tests/core/generation/test_placement.py::test_builtin_is_local_with_default_idle`

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## unit shard 2

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543682) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006877815)

**PASS→FAIL — unresolved (2):**
- `tests/core/generation/test_readiness_missing_models.py::test_a_partly_installed_default_names_only_what_is_missing`
- `tests/core/generation/test_readiness_missing_models.py::test_list_and_defaults_agree_when_files_are_missing`

**PASS→missing/skip — omission or possible rename, not yet explained (0):**
None observed

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (1):**
- `tests/core/generation/test_readiness_missing_models.py::test_defaults_is_ready_once_the_files_are_listed`

## unit shard 3

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543626) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006878489)

**PASS→FAIL — unresolved (0):**
None observed

**PASS→missing/skip — omission or possible rename, not yet explained (20):**
- `tests/editing_conformance/test_doc_patch_occurrence_history.py::test_history_move_requires_exact_physical_row_order_and_output[owner]`
- `tests/editing_conformance/test_doc_patch_occurrence_history.py::test_native_row_write_after_history_move_still_guards_stale_reorder[True]`
- `tests/editing_conformance/test_native_sheet_current.py::test_explicit_clear_restores_tagged_value[None-asset]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_image_hold_only_and_legacy_literal_for_presence`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_native_move_split_mime_fixture_has_no_renderer_or_legacy_writer_imports`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[app-value13]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[app-value14]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[app-value15]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[app-value16]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[app-value17]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[asset-missing]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[hold-7]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[params-value18]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[params-value19]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[speed-0]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_recognized_unsupported_shapes_refuse_without_mutation[speed-False]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_split_accepts_the_default_main_registry_fixture`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_split_uses_main_registry_mime_kind_normalizer[audio/wav]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_split_uses_main_registry_mime_kind_normalizer[image/png]`
- `tests/editing_conformance/test_recipe_m2_clip_split.py::test_split_uses_main_registry_mime_kind_normalizer[video/mp4]`

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## unit shard 4

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543670) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006877885)

**PASS→FAIL — unresolved (0):**
None observed

**PASS→missing/skip — omission or possible rename, not yet explained (7):**
- `tests/installer/test_tls_fallback.py::test_certificate_failure_retries_once_with_verified_context[direct]`
- `tests/installer/test_tls_fallback.py::test_certificate_failure_retries_once_with_verified_context[urlerror]`
- `tests/installer/test_tls_fallback.py::test_default_success_uses_one_attempt_without_changing_ssl`
- `tests/installer/test_tls_fallback.py::test_repeated_certificate_failure_stops_after_two_attempts`
- `tests/installer/test_tls_fallback.py::test_retry_still_rejects_a_checksum_mismatch`
- `tests/installer/test_tls_fallback.py::test_retry_works_in_dependency_free_bootstrap`
- `tests/packs/h3_av/test_planner.py::test_v2_ignored_constant_settings_and_disabled_turbo_strength`

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## unit shard 5

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543681) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006878027)

**PASS→FAIL — unresolved (0):**
None observed

**PASS→missing/skip — omission or possible rename, not yet explained (0):**
None observed

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## unit shard 6

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543657) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006877925)

**PASS→FAIL — unresolved (3):**
- `tests/packs/runpod/test_pod_fields.py::test_read_exact_pod_requests_network_volume`
- `tests/packs/timeline/test_verbs_working_copy.py::test_duplicate_is_all_or_nothing`
- `tests/sdk/test_timeline_checkout.py::test_duplicate_is_all_or_nothing`

**PASS→missing/skip — omission or possible rename, not yet explained (7):**
- `tests/packs/runpod/test_machine.py::test_catalog_job_capacity_uses_selected_local_workflow[qwen-image-2.1-turbo-t2i-image/qwen_image_2_1_turbo]`
- `tests/packs/test_vibecomfy_local.py::test_scan_returns_errors_for_unavailable_ports`
- `tests/reshape/test_compare_baselines.py::test_count_baselines_are_exact_so_deleted_code_cannot_leave_slack[10-10-0]`
- `tests/reshape/test_compare_baselines.py::test_count_baselines_are_exact_so_deleted_code_cannot_leave_slack[11-10-1]`
- `tests/reshape/test_compare_baselines.py::test_count_baselines_are_exact_so_deleted_code_cannot_leave_slack[9-10-1]`
- `tests/reshape/test_compare_baselines.py::test_file_code_ratchet[1-2-0-Ratchet down available]`
- `tests/reshape/test_compare_baselines.py::test_structure_gate_fails_on_a_new_violation_and_on_a_fixed_one`

**New failing IDs — no R13 row (23):**
- `tests/reshape/test_compare_baselines.py::test_tree_has_no_new_structure_violations`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_abrupt_exit_after_saved_refusal_reopens_and_completes_recovery`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_cross_actor_history_recovers_saved_part_during_delayed_ack`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_five_agents_deterministic`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_function_commit_keeps_overlap_as_pending_clash_after_shared_outbox_advance`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_function_commit_uses_head_advanced_by_same_actor_default_outbox`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_function_pending_retry_rereads_shared_outbox_and_keeps_original_suffix`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_function_rerun_overlap_during_same_actor_shared_outbox_advance_is_saved`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_new_file_swap_recovers_after_same_actor_default_outbox_race`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_new_file_swap_recovery_reimports_after_saved_runtime_refusal`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_pending_rederive_lost_reply_replays_exact_commit_once`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_reciprocal_refused_retries_finish_and_persist`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_reviewed_new_file_swap_runtime_conflict_is_saved_and_explicit_retry_recovers`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_runtime_function_retry_lands_prefix_then_previews_suffix`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_runtime_multipart_conflict_retries_prefix_and_suffix_across_reopens`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_runtime_part_advance_clears_predecessor_conflict_before_same_value_suffix`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_same_actor_default_outbox_recovers_captured_function_after_process_exit`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_same_actor_default_outbox_recovers_captured_reviewed_list_after_process_exit`
- `tests/sdk/test_timeline_clash_back_runtime.py::test_same_value_reviewed_list_recovers_through_shared_outbox_cli`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_move_then_hold_accepts_original_capture_and_generic_inverse_stages[False-occurrence:f2-occurrence/clip:f2-agent-clip-4]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_original_app_fields_provider_reload_exact_inverse_redo_and_disjoint_rebase`
- `tests/sdk/test_timeline_commit_provider.py::test_provider_accepts_trim_after_move_and_undoes_only_trim`
- `tests/sdk/test_timeline_commit_provider.py::test_stale_head_retries_original_plan_and_created_ids_once`

**FAIL→PASS — provisional recovery (0):**
None observed

## unit shard 7

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543723) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006877666)

**PASS→FAIL — unresolved (14):**
- `tests/sdk/test_timeline_film_length.py::test_a_layer_longer_than_its_middle_shot_blocks_check`
- `tests/test_installer_backup.py::test_failed_full_backup_removes_its_partial_snapshot[cancel]`
- `tests/test_installer_backup.py::test_full_backup_checks_realm_support_and_margin_before_starting[linux]`
- `tests/test_installer_backup.py::test_full_backup_checks_realm_support_and_margin_before_starting[win32]`
- `tests/test_installer_backup.py::test_windows_restore_does_not_restrict_retained_unsafe_directory[.]`
- `tests/test_installer_backup.py::test_windows_restore_does_not_restrict_retained_unsafe_directory[runtime]`
- `tests/test_installer_bootstrap_imports.py::test_installer_has_no_lazy_third_party_imports`
- `tests/test_installer_pinokio_launcher.py::test_generated_foreground_retains_exact_admission_across_rollback[None-old-True-True-False]`
- `tests/test_installer_pinokio_launcher.py::test_generated_foreground_retains_exact_admission_across_rollback[complete-old-True-True-False]`
- `tests/test_installer_pinokio_launcher.py::test_generated_foreground_retains_exact_admission_across_rollback[rolled_back-old-True-True-False]`
- `tests/test_installer_pinokio_launcher.py::test_launch_resolves_the_selected_version_each_time`
- `tests/test_installer_pinokio_launcher.py::test_launch_uses_current_version_service_command_and_pinokio_environment[darwin]`
- `tests/test_installer_pinokio_launcher.py::test_launch_uses_current_version_service_command_and_pinokio_environment[linux]`
- `tests/test_installer_pinokio_launcher.py::test_launch_uses_current_version_service_command_and_pinokio_environment[win32]`

**PASS→missing/skip — omission or possible rename, not yet explained (102):**
- `tests/sdk/test_timeline_checkout_history_boundaries.py::test_failed_draft_write_preserves_restore_sources[replace-redo]`
- `tests/sdk/test_timeline_checkout_history_boundaries.py::test_failed_draft_write_preserves_restore_sources[replace-undo]`
- `tests/sdk/test_timeline_checkout_history_boundaries.py::test_failed_draft_write_preserves_restore_sources[write-redo]`
- `tests/sdk/test_timeline_checkout_history_boundaries.py::test_failed_draft_write_preserves_restore_sources[write-undo]`
- `tests/sdk/test_timeline_checkout_publication_retry.py::test_publication_retry_survives_handle_reload[redo]`
- `tests/sdk/test_timeline_checkout_publication_retry.py::test_publication_retry_survives_handle_reload[undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[False-ABA-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[False-ABA-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[False-unchanged-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[False-unchanged-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[True-ABA-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[True-ABA-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[True-unchanged-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_equal_value_restore_uses_replacement_identity[True-unchanged-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[first-stage-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[first-stage-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[marker-replace-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[marker-replace-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[marker-write-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[marker-write-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[second-stage-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[second-stage-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[target-replace-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[target-replace-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[target-write-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_failed_restore_preparation_keeps_both_stacks[target-write-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_next_mutation_reconciles_before_reading_or_clearing_stacks[inverse-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_next_mutation_reconciles_before_reading_or_clearing_stacks[inverse-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_next_mutation_reconciles_before_reading_or_clearing_stacks[save-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_next_mutation_reconciles_before_reading_or_clearing_stacks[save-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[first-promotion-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[first-promotion-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[prepared-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[prepared-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[second-promotion-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[second-promotion-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[target-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_process_exit_recovers_through_public_reload[target-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_restore_recovers_each_committed_stage[second-promotion-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_restore_recovers_each_committed_stage[second-promotion-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_restore_recovers_each_committed_stage[source-removal-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_restore_recovers_each_committed_stage[source-removal-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_restore_recovers_each_committed_stage[target-redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_restore_recovers_each_committed_stage[target-undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_retired_draft_history_cannot_be_revived_by_a_pending_move[redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_retired_draft_history_cannot_be_revived_by_a_pending_move[undo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_reverse_stack_is_recoverable_after_post_replace_interruption[redo]`
- `tests/sdk/test_timeline_checkout_restore_recovery.py::test_reverse_stack_is_recoverable_after_post_replace_interruption[undo]`
- `tests/sdk/test_timeline_clash.py::test_conflict_summary_uses_clip_facing_target`
- `tests/sdk/test_timeline_clash.py::test_conflict_target_describes_verified_removal_and_equal_values`
- `tests/sdk/test_timeline_clash.py::test_history_verifies_pages_and_returns_only_entries_after_base`
- `tests/sdk/test_timeline_clash.py::test_packet_does_not_attribute_nonconflicting_receipt`
- `tests/sdk/test_timeline_clash.py::test_packet_names_touching_receipt`
- `tests/sdk/test_timeline_clash.py::test_packet_without_history_still_has_summary`
- `tests/sdk/test_timeline_clash.py::test_receipts_keep_only_touched_refs_and_paths`
- `tests/sdk/test_timeline_clip_add_provider.py::test_empty_to_nonempty_one_explicit_command_batch_has_no_hidden_lane_or_id`
- `tests/sdk/test_timeline_clip_add_provider.py::test_first_clip_provider_closed_reload_reservations_inverse_redo`
- `tests/sdk/test_timeline_clip_add_provider.py::test_invalid_first_clip_batch_cannot_partially_create_the_track[changes0]`
- `tests/sdk/test_timeline_clip_add_provider.py::test_invalid_first_clip_batch_cannot_partially_create_the_track[changes1]`
- `tests/sdk/test_timeline_clip_add_provider.py::test_invalid_first_clip_batch_cannot_partially_create_the_track[changes2]`
- `tests/sdk/test_timeline_clip_add_provider.py::test_invalid_first_clip_batch_cannot_partially_create_the_track[changes3]`
- `tests/sdk/test_timeline_clip_add_provider.py::test_invalid_first_clip_batch_cannot_partially_create_the_track[changes4]`
- `tests/sdk/test_timeline_clip_add_provider.py::test_native_create_label_params_group_reload_inverse_redo_preserves_disjoint_edit`
- `tests/sdk/test_timeline_clip_add_provider.py::test_native_group_external_consumer_and_late_bad_stage_are_atomic`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_hold_after_move_records_unchanged_for_and_refuses_publication_aba[False]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_hold_after_move_records_unchanged_for_and_refuses_publication_aba[True]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_hold_captured_after_move_refuses_changed_basis_without_recapture[occurrence:f2-occurrence/clip:f2-agent-clip-4]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_hold_captured_after_move_refuses_changed_basis_without_recapture[parent/clip:f2-transition-clip-16]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_move_then_hold_accepts_original_capture_and_generic_inverse_stages[False-parent/clip:f2-transition-clip-16]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_move_then_hold_accepts_original_capture_and_generic_inverse_stages[True-occurrence:f2-occurrence/clip:f2-agent-clip-4]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_move_then_hold_accepts_original_capture_and_generic_inverse_stages[True-parent/clip:f2-transition-clip-16]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_unchanged_publication_and_aba_refuse_old_inverse[False-occurrence:f2-occurrence/clip:f2-agent-clear-clip-asset]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_unchanged_publication_and_aba_refuse_old_inverse[False-occurrence:f2-occurrence/clip:f2-agent-clip-hold]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_unchanged_publication_and_aba_refuse_old_inverse[False-parent/clip:f2-transition-clip-transition]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_unchanged_publication_and_aba_refuse_old_inverse[True-occurrence:f2-occurrence/clip:f2-agent-clear-clip-asset]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_unchanged_publication_and_aba_refuse_old_inverse[True-occurrence:f2-occurrence/clip:f2-agent-clip-hold]`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_unchanged_publication_and_aba_refuse_old_inverse[True-parent/clip:f2-transition-clip-transition]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes0]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes1]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes2]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes3]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes4]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes5]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_late_bad_trim_cannot_partially_publish_prior_label[changes6]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_missing_duration_refuses_without_fetch_or_partial_acceptance`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_move_then_trim_is_an_ordinary_native_writer_and_undo_keeps_the_move`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_original_trim_dependency_change_and_forged_capture_are_atomic`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_same_value_and_aba_trim_publications_block_original_inverse[False]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_same_value_and_aba_trim_publications_block_original_inverse[True]`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_stale_trim_rebases_over_disjoint_params_with_original_claims_and_guarded_inverse`
- `tests/sdk/test_timeline_clip_trim_provider.py::test_trim_committed_reload_exact_inverse_redo_keeps_registry_and_child_pins`
- `tests/sdk/test_timeline_commit_provider.py::test_dependent_unsent_original_guards_allow_equal_state_aba_at_fresh_base`
- `tests/sdk/test_timeline_commit_provider.py::test_dry_run_uses_runtime_preview_and_writes_nothing`
- `tests/sdk/test_timeline_commit_provider.py::test_factory_matches_fixed_installed_runtime_contract`
- `tests/sdk/test_timeline_commit_provider.py::test_legacy_rebase_records_landing_step_metadata`
- `tests/sdk/test_timeline_commit_provider.py::test_move_inverse_returns_exact_runtime_result_and_complete_original_state`
- `tests/sdk/test_timeline_commit_provider.py::test_original_capture_claims_are_verified_before_refresh`
- `tests/sdk/test_timeline_commit_provider.py::test_replay_accepts_legacy_request_head_and_builds_steps`
- `tests/sdk/test_timeline_commit_provider.py::test_retired_identity_refuses_new_create_but_guarded_redo_restores_exact_state`
- `tests/sdk/test_timeline_commit_provider.py::test_stale_disjoint_rebases_and_same_clip_conflicts`
- `tests/sdk/test_timeline_commit_provider.py::test_timeline_scope_inverse_binding_skips_entity_dispatch_but_keeps_guards`
- `tests/sdk/test_timeline_commit_provider.py::test_undo_detects_aba_and_unchanged_write_publications`

**New failing IDs — no R13 row (11):**
- `tests/test_installer_update_legacy_record.py::test_sweep_resolves_a_record_without_home_once_its_unit_has_finished`
- `tests/test_journey_diagnostic_checkpoint.py::test_native_windows_locked_owner_file_is_not_read`
- `tests/test_journey_diagnostic_checkpoint.py::test_real_r0_realm_checkpoint_when_runtime_checkout_available`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[direct-macos]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[pinokio-backend-macos]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[pinokio-fully-local-macos]`
- `tests/test_journey_failure_modes.py::test_interruption_recovery_is_explicit_per_os[direct-macos]`
- `tests/test_journey_failure_modes.py::test_keep_data_uninstall_fails_closed[data_root_exists-False]`
- `tests/test_journey_failure_modes.py::test_keep_data_uninstall_fails_closed[keep_data-False]`
- `tests/test_journey_failure_modes.py::test_keep_data_uninstall_fails_closed[runtime_processes_after-1]`
- `tests/test_journey_failure_modes.py::test_stale_verified_pass_fields_cannot_hide_mutated_observations`

**FAIL→PASS — provisional recovery (0):**
None observed

## unit shard 8

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673752/job/132954543676) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391760/job/136006878263)

**PASS→FAIL — unresolved (1):**
- `tests/test_pinokio_platform_adapter.py::test_real_external_process_can_be_adopted_without_substitute_launch`

**PASS→missing/skip — omission or possible rename, not yet explained (283):**
- `tests/test_installer_update_end_to_end.py::test_refused_launch_is_reported_with_its_reason_not_as_an_os_rejection`
- `tests/test_installer_update_end_to_end.py::test_unfinished_installer_journal_refuses_before_any_preparation`
- `tests/test_installer_update_job.py::test_a_job_with_no_recorded_home_never_falls_back_to_the_ambient_home[job0]`
- `tests/test_installer_update_job.py::test_a_job_with_no_recorded_home_never_falls_back_to_the_ambient_home[job1]`
- `tests/test_installer_update_job.py::test_a_job_with_no_recorded_home_never_falls_back_to_the_ambient_home[job2]`
- `tests/test_installer_update_job.py::test_a_result_with_an_unknown_binding_is_left_unchanged`
- `tests/test_installer_update_job.py::test_a_run_that_started_before_this_attempt_was_submitted_is_left_unchanged`
- `tests/test_installer_update_job.py::test_accept_persists_additive_job_and_private_log_under_real_installer_lock`
- `tests/test_installer_update_job.py::test_accept_refuses_changed_selection_bytes_release_and_owner_without_journal`
- `tests/test_installer_update_job.py::test_accept_refuses_competing_operation_and_pending_c2_transaction`
- `tests/test_installer_update_job.py::test_accept_rejects_metadata_paths_that_do_not_name_the_validated_inputs`
- `tests/test_installer_update_job.py::test_an_attempt_replaced_before_the_lock_is_left_unchanged`
- `tests/test_installer_update_job.py::test_an_attempt_with_no_submission_time_is_left_unchanged`
- `tests/test_installer_update_job.py::test_availability_action_lists_supported_actions_on_every_os[darwin]`
- `tests/test_installer_update_job.py::test_availability_action_lists_supported_actions_on_every_os[linux]`
- `tests/test_installer_update_job.py::test_availability_action_lists_supported_actions_on_every_os[win32]`
- `tests/test_installer_update_job.py::test_captured_windows_worker_death_is_failed_with_its_error[as-powershell-wrote-it]`
- `tests/test_installer_update_job.py::test_captured_windows_worker_death_is_failed_with_its_error[decoded]`
- `tests/test_installer_update_job.py::test_dead_worker_after_claim_is_recovery_needed_not_failed`
- `tests/test_installer_update_job.py::test_dead_worker_that_never_claimed_is_failed_with_exit_code_and_log_tail`
- `tests/test_installer_update_job.py::test_existing_c2_journal_associates_job_without_preseeding_transaction`
- `tests/test_installer_update_job.py::test_explicit_saved_autostart_off_refuses_acceptance_without_mutating_preferences`
- `tests/test_installer_update_job.py::test_held_installer_lock_leaves_dead_worker_unchanged`
- `tests/test_installer_update_job.py::test_install_line_sweep_records_the_same_attempt_bound_outcome`
- `tests/test_installer_update_job.py::test_job_and_recovery_identity_probes_use_runtime_validator[payload0-job]`
- `tests/test_installer_update_job.py::test_job_and_recovery_identity_probes_use_runtime_validator[payload0-recovery]`
- `tests/test_installer_update_job.py::test_job_and_recovery_identity_probes_use_runtime_validator[payload1-job]`
- `tests/test_installer_update_job.py::test_job_and_recovery_identity_probes_use_runtime_validator[payload1-recovery]`
- `tests/test_installer_update_job.py::test_job_and_recovery_identity_probes_use_runtime_validator[payload2-job]`
- `tests/test_installer_update_job.py::test_job_and_recovery_identity_probes_use_runtime_validator[payload2-recovery]`
- `tests/test_installer_update_job.py::test_job_descriptor_is_durable_before_registration_and_lost_ack_never_relaunches`
- `tests/test_installer_update_job.py::test_known_launch_rejection_is_failed_only_after_inactive_query`
- `tests/test_installer_update_job.py::test_launchd_result_bound_by_its_loaded_command_is_settled`
- `tests/test_installer_update_job.py::test_legacy_selection_without_a_choice_record_snapshots_autostart_on`
- `tests/test_installer_update_job.py::test_linux_systemd_254_with_unusable_user_manager_is_unsupported`
- `tests/test_installer_update_job.py::test_linux_systemd_254_with_usable_user_manager_is_supported`
- `tests/test_installer_update_job.py::test_linux_update_job_availability_rejects_old_unknown_and_failed_systemd[version_result0]`
- `tests/test_installer_update_job.py::test_linux_update_job_availability_rejects_old_unknown_and_failed_systemd[version_result1]`
- `tests/test_installer_update_job.py::test_linux_update_job_availability_rejects_old_unknown_and_failed_systemd[version_result2]`
- `tests/test_installer_update_job.py::test_linux_update_job_availability_rejects_old_unknown_and_failed_systemd[version_result3]`
- `tests/test_installer_update_job.py::test_linux_update_job_availability_rejects_old_unknown_and_failed_systemd[version_result4]`
- `tests/test_installer_update_job.py::test_lost_acknowledgement_is_left_for_reconcile`
- `tests/test_installer_update_job.py::test_malformed_saved_autostart_choice_is_a_needs_repair_refusal_in_accept`
- `tests/test_installer_update_job.py::test_malformed_saved_autostart_choice_is_a_needs_repair_refusal_in_reconcile`
- `tests/test_installer_update_job.py::test_malformed_saved_autostart_choice_is_a_needs_repair_refusal_in_worker_admission`
- `tests/test_installer_update_job.py::test_non_linux_update_job_availability_remains_supported`
- `tests/test_installer_update_job.py::test_prior_rolled_back_journal_cannot_claim_new_job_rollback`
- `tests/test_installer_update_job.py::test_reconciler_leaves_a_journal_bearing_dead_worker_to_its_transaction_recovery`
- `tests/test_installer_update_job.py::test_rollback_is_not_reported_when_the_old_version_is_not_selected`
- `tests/test_installer_update_job.py::test_running_or_zero_exit_worker_is_left_unchanged[exit-zero]`
- `tests/test_installer_update_job.py::test_running_or_zero_exit_worker_is_left_unchanged[still-running]`
- `tests/test_installer_update_job.py::test_saved_autostart_on_is_snapshotted_and_launch_does_not_change_selection`
- `tests/test_installer_update_job.py::test_startup_traceback_only_in_the_wrapper_log_is_the_failed_message[absent]`
- `tests/test_installer_update_job.py::test_startup_traceback_only_in_the_wrapper_log_is_the_failed_message[empty]`
- `tests/test_installer_update_job.py::test_status_availability_read_leaves_a_running_worker_alone`
- `tests/test_installer_update_job.py::test_status_get_and_the_writer_change_nothing_without_attempt_bound_evidence`
- `tests/test_installer_update_job.py::test_status_get_on_a_held_lock_still_only_observes`
- `tests/test_installer_update_job.py::test_status_get_reports_a_dead_claimed_worker_as_recovery_needed_and_writes_nothing`
- `tests/test_installer_update_job.py::test_status_get_reports_a_dead_unclaimed_worker_as_failed_and_writes_nothing`
- `tests/test_installer_update_job.py::test_status_read_is_bounded_and_does_not_recover`
- `tests/test_installer_update_job.py::test_status_reports_without_reading_a_malformed_saved_autostart_choice`
- `tests/test_installer_update_job.py::test_success_requires_canonical_target_identity_and_bound_c2_complete`
- `tests/test_installer_update_job.py::test_supported_actions_cover_every_action_runtime_sends`
- `tests/test_installer_update_job.py::test_supported_update_post_still_admits`
- `tests/test_installer_update_job.py::test_sweep_marks_inactive_registration_failure_and_cleans_only_owned_object`
- `tests/test_installer_update_job.py::test_sweep_of_an_inactive_claimed_job_is_recovery_needed`
- `tests/test_installer_update_job.py::test_sweep_preserves_already_clean_historical_residue`
- `tests/test_installer_update_job.py::test_sweep_uses_existing_installer_lock_and_retains_historical_residue`
- `tests/test_installer_update_job.py::test_sweep_without_leftovers_preserves_install_record_bytes`
- `tests/test_installer_update_job.py::test_terminal_cleanup_failure_is_durable_and_sweep_retains_unknown_residue`
- `tests/test_installer_update_job.py::test_terminal_cleanup_records_status_error_and_retains_residue_for_next_operation`
- `tests/test_installer_update_job.py::test_the_job_log_is_preferred_and_the_wrapper_log_is_kept`
- `tests/test_installer_update_job.py::test_the_job_reads_the_install_record_of_the_home_it_was_accepted_under`
- `tests/test_installer_update_job.py::test_the_worker_preamble_is_the_same_on_every_platform`
- `tests/test_installer_update_job.py::test_unsupported_native_launch_is_refused_before_lock_or_launch`
- `tests/test_installer_update_job.py::test_unsupported_post_keeps_reason_and_has_no_admission_or_launch_effects[probe_results0]`
- `tests/test_installer_update_job.py::test_unsupported_post_keeps_reason_and_has_no_admission_or_launch_effects[probe_results1]`
- `tests/test_installer_update_job.py::test_unsupported_post_keeps_reason_and_has_no_admission_or_launch_effects[probe_results2]`
- `tests/test_installer_update_job.py::test_update_job_availability_action_preserves_get_reason`
- `tests/test_installer_update_job.py::test_windows_current_release_availability_remains_supported`
- `tests/test_installer_update_job.py::test_windows_earlier_release_availability_action_reports_upgrade_reason`
- `tests/test_installer_update_job.py::test_windows_earlier_release_availability_reports_upgrade_reason`
- `tests/test_installer_update_job.py::test_windows_handoff_copies_same_private_bytes_to_ps1_and_preserves_cli_selection`
- `tests/test_installer_update_job.py::test_windows_install_without_pointer_or_login_task_is_not_refused_as_upgrade`
- `tests/test_installer_update_job.py::test_windows_r0_without_pointer_but_with_login_task_reports_upgrade_reason`
- `tests/test_installer_update_job.py::test_windows_upgrade_refusal_gate_names_the_reason_not_the_service_manager`
- `tests/test_installer_update_job.py::test_worker_claims_once_and_terminal_result_is_idempotent`
- `tests/test_installer_update_job.py::test_worker_command_uses_selected_old_python_and_profile_checkouts_isolated`
- `tests/test_installer_update_job.py::test_worker_does_not_relaunch_an_already_active_job`
- `tests/test_installer_update_job.py::test_worker_launch_refuses_if_autostart_was_changed_to_off`
- `tests/test_installer_update_job.py::test_worker_recovers_existing_c2_journal_before_rechecking_and_launching`
- `tests/test_installer_update_job.py::test_worker_script_preparation_failure_is_recorded_before_platform_registration`
- `tests/test_installer_update_job.py::test_worker_subprocess_failure_attempts_terminal_cleanup`
- `tests/test_installer_update_job.py::test_worker_terminal_handoff_cleans_once_and_preserves_preferences_and_job_name[failed]`
- `tests/test_installer_update_job.py::test_worker_terminal_handoff_cleans_once_and_preserves_preferences_and_job_name[rolled_back]`
- `tests/test_installer_update_job.py::test_worker_terminal_handoff_cleans_once_and_preserves_preferences_and_job_name[updated]`
- `tests/test_installer_update_job.py::test_worker_validation_failure_cleans_from_its_own_job_context`
- `tests/test_installer_update_legacy_record.py::test_describe_of_a_record_without_home_reproduces_its_stored_descriptor`
- `tests/test_installer_update_legacy_record.py::test_reconcile_helper_reports_the_legacy_record_reason`
- `tests/test_installer_update_legacy_record.py::test_reconcile_leaves_a_record_without_home_unchanged_when_liveness_is_unknown`
- `tests/test_installer_update_legacy_record.py::test_reconcile_refuses_a_finished_record_without_home_at_the_selection_read`
- `tests/test_installer_update_legacy_record.py::test_reconcile_treats_a_record_without_home_as_active_while_its_unit_runs`
- `tests/test_installer_update_legacy_record.py::test_status_reports_a_record_without_home_as_stored[active-False]`
- `tests/test_installer_update_legacy_record.py::test_status_reports_a_record_without_home_as_stored[inactive-False]`
- `tests/test_installer_update_legacy_record.py::test_status_reports_a_record_without_home_as_stored[inactive-True]`
- `tests/test_installer_update_legacy_record.py::test_sweep_keeps_a_record_without_home_active_while_its_unit_runs`
- `tests/test_installer_update_legacy_record.py::test_sweep_leaves_a_record_without_home_unchanged_when_the_check_is_uncertain`
- `tests/test_installer_update_maintenance.py::test_interrupted_and_partial_copy_leave_originals_and_use_a_new_attempt`
- `tests/test_installer_update_maintenance.py::test_maintenance_faults_preserve_evidence_and_resume`
- `tests/test_installer_update_maintenance.py::test_missing_bundle_and_foreign_or_unsafe_paths_never_start_apply`
- `tests/test_installer_update_maintenance.py::test_noncontinuable_states_have_supported_escape[M1]`
- `tests/test_installer_update_maintenance.py::test_noncontinuable_states_have_supported_escape[M2]`
- `tests/test_installer_update_maintenance.py::test_noncontinuable_states_have_supported_escape[M3]`
- `tests/test_installer_update_maintenance.py::test_noncontinuable_states_have_supported_escape[M4]`
- `tests/test_installer_update_maintenance.py::test_noncontinuable_states_have_supported_escape[M5]`
- `tests/test_installer_update_maintenance.py::test_noncontinuable_states_have_supported_escape[M6]`
- `tests/test_installer_update_maintenance.py::test_partial_copy_verification_refuses_without_clearing_then_resumes`
- `tests/test_installer_update_maintenance.py::test_update_recovery_cli_is_plan_by_default_and_apply_is_explicit`
- `tests/test_installer_update_reconcile.py::test_accept_holds_installer_lock_through_checks_and_new_admission`
- `tests/test_installer_update_reconcile.py::test_confirmed_operation_id_cannot_be_accepted_again`
- `tests/test_installer_update_reconcile.py::test_h3_confirmed_terminal_result_with_no_newer_target_returns_without_admission[no-target]`
- `tests/test_installer_update_reconcile.py::test_h3_confirmed_terminal_result_with_no_newer_target_returns_without_admission[same-release]`
- `tests/test_installer_update_reconcile.py::test_h4_helper_serializes_held_busy_refusal_and_exits_nonzero`
- `tests/test_installer_update_reconcile.py::test_h5_helper_serializes_lost_launch_acknowledgement_as_observe_only`
- `tests/test_installer_update_reconcile.py::test_live_or_unknown_native_liveness_refuses_busy_and_preserves_evidence[True]`
- `tests/test_installer_update_reconcile.py::test_live_or_unknown_native_liveness_refuses_busy_and_preserves_evidence[unreadable]`
- `tests/test_installer_update_reconcile.py::test_live_runtime_must_match_transaction_before_recovery[False]`
- `tests/test_installer_update_reconcile.py::test_live_runtime_must_match_transaction_before_recovery[True]`
- `tests/test_installer_update_reconcile.py::test_malformed_prior_operation_cannot_be_overwritten_by_new_admission[prior1]`
- `tests/test_installer_update_reconcile.py::test_malformed_prior_operation_cannot_be_overwritten_by_new_admission[prior2]`
- `tests/test_installer_update_reconcile.py::test_malformed_prior_operation_cannot_be_overwritten_by_new_admission[unreadable]`
- `tests/test_installer_update_reconcile.py::test_matching_unfinished_recovery_returns_i3_and_ends_this_update_request`
- `tests/test_installer_update_reconcile.py::test_mismatched_recovery_evidence_refuses_without_replacing_job_or_journal[binding]`
- `tests/test_installer_update_reconcile.py::test_mismatched_recovery_evidence_refuses_without_replacing_job_or_journal[data-root]`
- `tests/test_installer_update_reconcile.py::test_mismatched_recovery_evidence_refuses_without_replacing_job_or_journal[descriptor-command]`
- `tests/test_installer_update_reconcile.py::test_mismatched_recovery_evidence_refuses_without_replacing_job_or_journal[owner]`
- `tests/test_installer_update_reconcile.py::test_mismatched_recovery_evidence_refuses_without_replacing_job_or_journal[program-root]`
- `tests/test_installer_update_reconcile.py::test_mismatched_recovery_evidence_refuses_without_replacing_job_or_journal[transaction]`
- `tests/test_installer_update_reconcile.py::test_read_job_remains_observational_for_unresolved_operation`
- `tests/test_installer_update_reconcile.py::test_real_selected_readiness_verifier_rejects_identity_and_health_failures[missing-instance]`
- `tests/test_installer_update_reconcile.py::test_real_selected_readiness_verifier_rejects_identity_and_health_failures[unknown-owner]`
- `tests/test_installer_update_reconcile.py::test_real_selected_readiness_verifier_rejects_identity_and_health_failures[unready]`
- `tests/test_installer_update_reconcile.py::test_real_selected_readiness_verifier_rejects_identity_and_health_failures[wrong-release]`
- `tests/test_installer_update_reconcile.py::test_real_selected_readiness_verifier_rejects_wrong_selected_version`
- `tests/test_installer_update_reconcile.py::test_reconcile_helper_dispatches_prepare_new`
- `tests/test_installer_update_reconcile.py::test_reconcile_runs_under_installer_lock_before_new_input_preparation`
- `tests/test_installer_update_reconcile.py::test_recovered_before_stop_terminal_record_is_verified_then_new_update_is_admitted`
- `tests/test_installer_update_reconcile.py::test_recovery_result_cannot_be_mistaken_for_new_operation_launch`
- `tests/test_installer_update_reconcile.py::test_successful_empty_systemd_state_is_unknown_liveness`
- `tests/test_installer_update_reconcile.py::test_terminal_rollback_can_admit_one_newer_operation_on_later_update`
- `tests/test_installer_update_reconcile.py::test_unreadable_journal_and_prior_transaction_are_busy_and_preserved`
- `tests/test_installer_update_reconcile.py::test_unready_selected_runtime_preserves_terminal_recovery_evidence`
- `tests/test_installer_wheel.py::test_built_wheel_declares_its_bundled_chat_service`
- `tests/test_installer_wheel.py::test_built_wheel_loads_every_engine_helper_and_packaged_lock`
- `tests/test_installer_windows_paths.py::test_directory_limit_includes_implicit_parents[False]`
- `tests/test_installer_windows_paths.py::test_directory_limit_includes_implicit_parents[True]`
- `tests/test_installer_windows_paths.py::test_file_limit_counts_utf16_units[259-True]`
- `tests/test_installer_windows_paths.py::test_file_limit_counts_utf16_units[260-False]`
- `tests/test_installer_windows_paths.py::test_omp_budget_is_checked_at_final_source_location_not_staging`
- `tests/test_installer_windows_paths.py::test_other_platforms_keep_long_paths_and_archive_prefix[darwin]`
- `tests/test_installer_windows_paths.py::test_other_platforms_keep_long_paths_and_archive_prefix[linux]`
- `tests/test_installer_windows_paths.py::test_path_refusal_happens_before_any_extraction[tar]`
- `tests/test_installer_windows_paths.py::test_path_refusal_happens_before_any_extraction[zip]`
- `tests/test_installer_windows_paths.py::test_reported_archives_fit_every_windows_source_path[VibeComfy-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-206-1]`
- `tests/test_installer_windows_paths.py::test_reported_archives_fit_every_windows_source_path[VibeComfy-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-206-20]`
- `tests/test_installer_windows_paths.py::test_reported_archives_fit_every_windows_source_path[VibeComfy-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-206-6]`
- `tests/test_installer_windows_paths.py::test_reported_archives_fit_every_windows_source_path[astrid-agent-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-178-1]`
- `tests/test_installer_windows_paths.py::test_reported_archives_fit_every_windows_source_path[astrid-agent-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-178-20]`
- `tests/test_installer_windows_paths.py::test_reported_archives_fit_every_windows_source_path[astrid-agent-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-178-6]`
- `tests/test_installer_windows_paths.py::test_source_git_enables_longpaths_only_on_windows[darwin]`
- `tests/test_installer_windows_paths.py::test_source_git_enables_longpaths_only_on_windows[linux]`
- `tests/test_installer_windows_paths.py::test_source_git_enables_longpaths_only_on_windows[win32]`
- `tests/test_installer_windows_paths.py::test_stripping_cannot_hide_bad_layout_or_traversal[entries0]`
- `tests/test_installer_windows_paths.py::test_stripping_cannot_hide_bad_layout_or_traversal[entries1]`
- `tests/test_installer_windows_paths.py::test_stripping_cannot_hide_bad_layout_or_traversal[entries2]`
- `tests/test_installer_windows_paths.py::test_windows_source_moves_every_file_and_preserves_tree_digest[VibeComfy-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-tar]`
- `tests/test_installer_windows_paths.py::test_windows_source_moves_every_file_and_preserves_tree_digest[VibeComfy-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-zip]`
- `tests/test_installer_windows_paths.py::test_windows_source_moves_every_file_and_preserves_tree_digest[astrid-agent-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-tar]`
- `tests/test_installer_windows_paths.py::test_windows_source_moves_every_file_and_preserves_tree_digest[astrid-agent-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-zip]`
- `tests/test_isolation_env_passthrough_schema.py::test_executor_isolation_env_passthrough_rejects_invalid_or_duplicate_names`
- `tests/test_isolation_env_passthrough_schema.py::test_executor_isolation_env_passthrough_round_trips_and_inspect_exposes_it`
- `tests/test_isolation_env_passthrough_schema.py::test_isolation_secrets_round_trip_for_executor_and_orchestrator`
- `tests/test_isolation_env_passthrough_schema.py::test_orchestrator_isolation_env_passthrough_rejects_invalid_or_duplicate_names`
- `tests/test_isolation_env_passthrough_schema.py::test_orchestrator_isolation_env_passthrough_round_trips`
- `tests/test_journey_diagnostic_checkpoint.py::test_census_rejects_changes_between_passes`
- `tests/test_journey_diagnostic_checkpoint.py::test_census_rejects_enumeration_failure_and_symlink`
- `tests/test_journey_diagnostic_checkpoint.py::test_diagnostic_checkpoint_accepts_only_unchanged_preseed_realm_and_keeps_custody_checks`
- `tests/test_journey_diagnostic_checkpoint.py::test_diagnostic_checkpoint_refuses_each_changed_retained_realm_before_seed[changed-data]`
- `tests/test_journey_diagnostic_checkpoint.py::test_diagnostic_checkpoint_refuses_each_changed_retained_realm_before_seed[complete-seed]`
- `tests/test_journey_diagnostic_checkpoint.py::test_diagnostic_checkpoint_refuses_each_changed_retained_realm_before_seed[partial-seed]`
- `tests/test_journey_diagnostic_checkpoint.py::test_live_root_lock_is_inventoried_without_reading_and_data_stays_bound`
- `tests/test_journey_diagnostic_checkpoint.py::test_unreadable_other_files_are_not_exempt[instance.lock]`
- `tests/test_journey_diagnostic_checkpoint.py::test_unreadable_other_files_are_not_exempt[nested/owner.lock]`
- `tests/test_journey_diagnostic_checkpoint.py::test_unreadable_other_files_are_not_exempt[realm.sqlite3]`
- `tests/test_journey_end_state_inventory.py::test_checker_cli_lists_the_closed_inventory_and_fails_not_run_rows`
- `tests/test_journey_end_state_inventory.py::test_duplicate_json_is_rejected_not_promoted_to_a_pass`
- `tests/test_journey_end_state_inventory.py::test_end_state_inventory_lists_every_required_obligation_once`
- `tests/test_journey_end_state_inventory.py::test_m4_5_wrong_checker_tuple_is_explicitly_failed`
- `tests/test_journey_end_state_inventory.py::test_m4_6_malformed_or_local_evidence_is_never_a_pass`
- `tests/test_journey_end_state_inventory.py::test_obligation_statuses_are_complete_and_missing_routes_are_not_run`
- `tests/test_journey_end_state_inventory.py::test_obligation_statuses_attribute_pass_failed_skipped_duplicate_and_wrong_tuple`
- `tests/test_journey_evidence.py::test_both_fresh_rows_require_complete_update_receipt`
- `tests/test_journey_evidence.py::test_direct_receipts_require_observed_checks_without_pid_count`
- `tests/test_journey_evidence.py::test_each_release1_leg_needs_its_own_receipt_kind`
- `tests/test_journey_evidence.py::test_four_required_negative_controls`
- `tests/test_journey_evidence.py::test_handoff_rows_require_the_completed_handoff_and_a_real_update`
- `tests/test_journey_evidence.py::test_hosted_image_mappings`
- `tests/test_journey_evidence.py::test_macos15_receipt_key_rejects_the_retired_macos14_label`
- `tests/test_journey_evidence.py::test_pinokio_dispatch_selects_r1_1_pinokio_rows_and_skips_old_launcher_inputs`
- `tests/test_journey_evidence.py::test_pinokio_row_receipts_accept_exact_complete_green_set`
- `tests/test_journey_evidence.py::test_pinokio_row_receipts_accept_only_the_selected_job`
- `tests/test_journey_evidence.py::test_pinokio_row_receipts_reject_duplicate_and_mismatched_jobs`
- `tests/test_journey_evidence.py::test_pinokio_row_receipts_reject_malformed_schema_and_fields`
- `tests/test_journey_evidence.py::test_pinokio_row_receipts_reject_missing_row_step_and_failed_step`
- `tests/test_journey_evidence.py::test_pinokio_row_steps_run_driver_and_keep_the_evidence_boundary_path`
- `tests/test_journey_evidence.py::test_r1_1_pinokio_matrix_has_exact_three_rows_and_own_checker`
- `tests/test_journey_evidence.py::test_release1_aggregate_accepts_full_staged_receipts_with_capture_status`
- `tests/test_journey_evidence.py::test_release1_aggregate_rejects_missing_skipped_and_ambiguous_receipts`
- `tests/test_journey_evidence.py::test_release1_aggregate_requires_exactly_the_five_direct_rows`
- `tests/test_journey_evidence.py::test_release1_fresh_rows_use_fresh_expectations_and_upgrade_rows_stay_strict`
- `tests/test_journey_evidence.py::test_release1_gate_requires_an_ordinary_final_uninstall_or_the_handoff_refusal`
- `tests/test_journey_evidence.py::test_release1_macos_rows_require_macos15_and_hosted_provenance`
- `tests/test_journey_evidence.py::test_runner_provenance_required`
- `tests/test_journey_evidence.py::test_runner_shell_and_cleanup_must_match`
- `tests/test_journey_evidence.py::test_workflow_declares_the_exact_release1_matrix_and_aggregate_gate`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[direct-linux]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[direct-windows]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[pinokio-backend-linux]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[pinokio-backend-windows]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[pinokio-fully-local-linux]`
- `tests/test_journey_failure_modes.py::test_all_nine_os_mode_slots_admit_complete_machine_observations[pinokio-fully-local-windows]`
- `tests/test_journey_failure_modes.py::test_interruption_recovery_is_explicit_per_os[direct-linux]`
- `tests/test_journey_failure_modes.py::test_interruption_recovery_is_explicit_per_os[direct-windows]`
- `tests/test_journey_failure_modes.py::test_prose_or_source_evidence_cannot_be_admitted`
- `tests/test_journey_failure_modes.py::test_refused_or_unknown_stop_never_updates[automatic_retry-refused]`
- `tests/test_journey_failure_modes.py::test_refused_or_unknown_stop_never_updates[automatic_retry-unknown]`
- `tests/test_journey_failure_modes.py::test_refused_or_unknown_stop_never_updates[candidate_downloaded_or_written-refused]`
- `tests/test_journey_failure_modes.py::test_refused_or_unknown_stop_never_updates[candidate_downloaded_or_written-unknown]`
- `tests/test_journey_failure_modes.py::test_refused_or_unknown_stop_never_updates[update_admitted-refused]`
- `tests/test_journey_failure_modes.py::test_refused_or_unknown_stop_never_updates[update_admitted-unknown]`
- `tests/test_journey_failure_modes.py::test_rollback_requires_real_release0_executable_and_intact_data[mutation0-executable_sha256 changed]`
- `tests/test_journey_failure_modes.py::test_rollback_requires_real_release0_executable_and_intact_data[mutation1-project: semantic data changed]`
- `tests/test_journey_fresh_update.py::test_execute_hands_the_linux_row_the_hosted_build_before_anything_runs`
- `tests/test_journey_fresh_update.py::test_execute_posts_the_hosted_update_and_checks_post_update[1]`
- `tests/test_journey_fresh_update.py::test_execute_posts_the_hosted_update_and_checks_post_update[7]`
- `tests/test_journey_fresh_update.py::test_execute_rejects_a_baseline_that_is_not_the_candidate_release`
- `tests/test_journey_fresh_update.py::test_gate_reads_the_published_release_from_the_row_and_expects_exactly_one_more[0]`
- `tests/test_journey_fresh_update.py::test_gate_reads_the_published_release_from_the_row_and_expects_exactly_one_more[1]`
- `tests/test_journey_fresh_update.py::test_gate_reads_the_published_release_from_the_row_and_expects_exactly_one_more[7]`
- `tests/test_journey_fresh_update.py::test_gate_requires_update_and_every_assertion`
- `tests/test_journey_fresh_update.py::test_only_the_fresh_linux_row_must_be_the_clicked_button`
- `tests/test_journey_fresh_update.py::test_standin_follows_the_candidate_release_not_a_fixed_one`
- `tests/test_journey_fresh_update.py::test_standin_preserves_pins_and_canonical_bytes`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change0-clicked in a browser]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change1-clicked in a browser]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change2-did not read the stand-in]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change3-did not read the stand-in]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change4-build identity]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change5-carry a credential]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change6-headers are absent]`
- `tests/test_journey_fresh_update.py::test_the_button_receipt_needs_every_piece_of_the_click[change7-credential-free POST]`
- `tests/test_journey_fresh_update.py::test_the_linux_row_needs_the_hosted_build_and_macos_does_not`
- `tests/test_journey_fresh_update.py::test_transition_requires_new_current_old_retained_same_label_and_no_boundary`
- `tests/test_journey_fully_local.py::test_adapter_evidence_must_match_receipt`
- `tests/test_journey_fully_local.py::test_cli_is_non_destructive_by_default`
- `tests/test_journey_fully_local.py::test_fake_adapter_does_not_mutate_agent_checkout`
- `tests/test_journey_fully_local.py::test_fake_success_proves_route_failure_restore_and_local_readiness`
- `tests/test_journey_fully_local.py::test_linux_label_cannot_be_smuggled_into_source_validation`
- `tests/test_journey_fully_local.py::test_premature_ready_and_missing_checkout_field_fail_closed`
- `tests/test_journey_fully_local.py::test_source_fake_evidence_can_never_pass_linux_gate`
- `tests/test_journey_fully_local.py::test_unsafe_routes_and_changed_invariants_fail_closed[cleanup.lock.removed-True-deletion]`
- `tests/test_journey_fully_local.py::test_unsafe_routes_and_changed_invariants_fail_closed[failure.exit_status-0-nonzero]`
- `tests/test_journey_fully_local.py::test_unsafe_routes_and_changed_invariants_fail_closed[mode.after_bytes-{"schema_version":1,"mode":"backend"}-mode]`
- `tests/test_journey_fully_local.py::test_unsafe_routes_and_changed_invariants_fail_closed[readiness.ready.hosted_door-True-local]`
- `tests/test_journey_fully_local.py::test_unsafe_routes_and_changed_invariants_fail_closed[route.backend-True-backend]`
- `tests/test_journey_fully_local.py::test_unsafe_routes_and_changed_invariants_fail_closed[route.foreground_service-True-foreground]`
- `tests/test_journey_hosted_update.py::test_post_is_what_the_hosted_page_sends`
- `tests/test_journey_hosted_update.py::test_post_refusals_are_reported_with_the_door_answer[reply0]`
- `tests/test_journey_hosted_update.py::test_post_refusals_are_reported_with_the_door_answer[reply1]`
- `tests/test_journey_hosted_update.py::test_post_refusals_are_reported_with_the_door_answer[reply2]`
- `tests/test_journey_hosted_update.py::test_post_refusals_are_reported_with_the_door_answer[reply3]`
- `tests/test_journey_hosted_update.py::test_wait_terminal_fails_on_any_other_outcome[failed]`
- `tests/test_journey_hosted_update.py::test_wait_terminal_tolerates_the_restart_and_returns_on_updated`

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (1):**
- `tests/test_pinokio_platform_adapter.py::test_secret_never_appears_in_receipt_state_or_cli_output`



---

# Provisional Agent R13→R14 Lanes four-shard comparison — 21 November 2026

Published Agent source `959da7326c982a9197b5d6e2a4489f45e1deef0e` [Lanes 43760673730](https://github.com/banodoco/astrid-agent/actions/runs/43760673730) versus pre-freeze Agent `0020c2e8d7f5d6051db2964a235b97f4ba002a72` [Lanes 44651391728](https://github.com/banodoco/astrid-agent/actions/runs/44651391728). **No qualifying verdict.**

| Job | R13 native IDs | R14 pre-freeze native IDs | PASS→FAIL | PASS→missing/skip | New failing | FAIL→PASS |
|---|---|---|---:|---:|---:|---:|
| integration shard 1 | 516 (480 pass, 36 fail, 0 skip) | 517 (481 pass, 36 fail, 0 skip) | 0 | 0 | 0 | 0 |
| integration shard 2 | 516 (267 pass, 249 fail, 0 skip) | 517 (267 pass, 250 fail, 0 skip) | 1 | 2 | 0 | 0 |
| integration shard 3 | 516 (372 pass, 143 fail, 1 skip) | 517 (370 pass, 146 fail, 1 skip) | 3 | 0 | 0 | 0 |
| integration shard 4 | 516 (391 pass, 125 fail, 0 skip) | 516 (391 pass, 125 fail, 0 skip) | 0 | 0 | 0 | 0 |

Lane per-job totals: **4 PASS→FAIL; 2 PASS→missing/skip; 0 new failing; 0 recovered**. Every discrepancy stays open until a source-linked explanation and the frozen comparison.

## integration shard 1

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673730/job/132954543497) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391728/job/136006878103)

**PASS→FAIL — unresolved (0):**
None observed

**PASS→missing/skip — omission or possible rename, not yet explained (0):**
None observed

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## integration shard 2

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673730/job/132954543399) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391728/job/136006877063)

**PASS→FAIL — unresolved (1):**
- `tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance`

**PASS→missing/skip — omission or possible rename, not yet explained (2):**
- `tests/core/generation/test_generate_target_journey.py::test_f02_sdk_bound_target_failure_is_read_only[repo]`
- `tests/editing_conformance/test_native_word_anchor.py::test_equal_text_restore_recovers_the_selected_publications_binding`

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## integration shard 3

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673730/job/132954543366) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391728/job/136006876749)

**PASS→FAIL — unresolved (3):**
- `tests/integrations/test_dry_run_equals_live_run.py::test_dry_run_equals_live_run[audio/tts-attached]`
- `tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_real_media_render_through_public_service`
- `tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_real_render_through_public_service`

**PASS→missing/skip — omission or possible rename, not yet explained (0):**
None observed

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

## integration shard 4

[R13 job](https://github.com/banodoco/astrid-agent/actions/runs/43760673730/job/132954543369) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-agent/actions/runs/44651391728/job/136006877378)

**PASS→FAIL — unresolved (0):**
None observed

**PASS→missing/skip — omission or possible rename, not yet explained (0):**
None observed

**New failing IDs — no R13 row (0):**
None observed

**FAIL→PASS — provisional recovery (0):**
None observed

