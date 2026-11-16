# Runtime Nightly full XML failure/error messages

Run 43954031460, job 133603706731. This ledger groups by the exact decoded JUnit XML `<failure>`/`<error>` `message` attribute; embedded newlines and literal values are preserved. Each per-ID record in `full-xml-messages.json` also keeps the entire XML child detail text without truncation.

## Reconciliation

- Validated 149 XML failure/error testcase records: 121 failures and 28 errors.
- Every exact testcase ID and status matches `new-red-outcomes.json` (149/149).
- Exact XML message-attribute groups: 53; the existing final-line pytest summary ledger has 46 groups.

The existing short-summary ledger is retained unchanged. Pytest’s final summary can abbreviate assertion values; that is why XML message grouping may differ from `message-counts.json`. This file makes the XML grouping explicit instead of replacing the summary grouping.

## Exact XML messages

| Group | Count | Outcome mix | Exact testcase IDs |
|---|---:|---|---|
| XML-001 | 34 | failure 34 | <code>tests/test_timeline_commit_integration.py::test_agent_provider_refuses_top_level_type_on_without_publication</code><br><code>tests/test_timeline_commit_integration.py::test_agent_provider_refuses_animation_in_unsupported_phase_without_publication</code><br><code>tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication&#91;entrance-value0&#93;</code><br><code>tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication&#91;entrance-value1&#93;</code><br><code>tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication&#91;entrance-value2&#93;</code><br><code>tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication&#91;transition-value3&#93;</code><br><code>tests/test_timeline_commit_integration.py::test_visual_candidate_is_refused_before_publication_when_builtin_phase_is_unsupported</code><br><code>tests/test_timeline_history_assembly.py::test_unverified_dependencies_cannot_escape_the_graph&#91;queued-row&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_unverified_dependencies_cannot_escape_the_graph&#91;indirect-cycle&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;metadata-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;parent-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;event-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;file-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;abi-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;ledger-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;records-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;source-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;closure-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;owner-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;realm-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;sequence-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;pin-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;queued-cycle-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check&#91;deleted-row-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check&#91;transcript-content-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check&#91;transcript-binding-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check&#91;transcript-link-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check&#91;config-content-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check&#91;config-binding-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check&#91;config-link-collection&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_refuses_mutation_after_dependent_history_reads&#91;head&#93;</code><br><code>tests/test_timeline_visual_fields.py::test_visual_fields_on_audio_track_are_refused_before_publication&#91;entrance-value0&#93;</code><br><code>tests/test_timeline_visual_fields.py::test_visual_fields_on_audio_track_are_refused_before_publication&#91;exit-value1&#93;</code><br><code>tests/test_timeline_visual_fields.py::test_visual_fields_on_audio_track_are_refused_before_publication&#91;transition-value2&#93;</code> |
| XML-002 | 21 | failure 21 | <code>tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary&#91;pre-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary&#91;pre-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary&#91;before-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary&#91;before-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary&#91;after-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary&#91;after-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;transcript-pre-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;transcript-pre-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;transcript-before-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;transcript-before-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;transcript-after-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;transcript-after-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;config-pre-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;config-pre-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;config-before-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;config-before-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;config-after-commit&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_retained_inputs_process_death&#91;config-after-restore&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death&#91;pre-transcript&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death&#91;before-transcript&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death&#91;after-transcript&#93;</code> |
| XML-003 | 20 | error 20 | <code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;genuine-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;genuine-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;genuine-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;genuine-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;native-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;native-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;native-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;native-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;config-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;config-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;config-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;config-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;registry-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;registry-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;registry-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;registry-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;expansion-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;expansion-ref&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade&#91;expansion-inline&#93;</code><br><code>tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade&#91;expansion-inline&#93;</code> |
| XML-004 | 5 | failure 5 | <code>tests/test_render_historical_admission.py::test_corrupt_retained_dependency_refuses_without_writes</code><br><code>tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication&#91;missing&#93;</code><br><code>tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication&#91;same-size&#93;</code><br><code>tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication&#91;custody&#93;</code><br><code>tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication&#91;size&#93;</code> |
| XML-005 | 5 | error 5 | <code>tests/test_runtime_boundary.py::test_separate_failed_start_preserves_live_discovery</code><br><code>tests/test_runtime_boundary.py::test_foreign_pid_observation_cannot_reclaim_live_publication</code><br><code>tests/test_runtime_boundary.py::test_down_without_discovery_cannot_report_live_owner_stopped&#91;False&#93;</code><br><code>tests/test_runtime_boundary.py::test_down_without_discovery_cannot_report_live_owner_stopped&#91;True&#93;</code><br><code>tests/test_runtime_boundary.py::test_failed_candidate_pid_alias_cannot_retire_live_publication</code> |
| XML-006 | 4 | failure 4 | <code>tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death&#91;pre-config&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death&#91;before-config&#93;</code><br><code>tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death&#91;after-config&#93;</code><br><code>tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent&#91;declared-media&#93;</code> |
| XML-007 | 3 | failure 3 | <code>tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter&#91;linux&#93;</code><br><code>tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter&#91;darwin&#93;</code><br><code>tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter&#91;win32&#93;</code> |
| XML-008 | 3 | failure 3 | <code>tests/test_timeline_commit_integration.py::test_agent_written_visual_fields_validate_and_read_back_from_published_revision</code><br><code>tests/test_timeline_visual_fields.py::test_visual_field_provider_acceptance_and_refusal_regressions</code><br><code>tests/test_timeline_visual_fields.py::test_visual_field_provider_preserves_opaque_custom_data</code> |
| XML-009 | 3 | failure 3 | <code>tests/test_timeline_history_assembly.py::test_provider_history_lookup_authenticates_each_graph_node_once&#91;2&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_history_lookup_authenticates_each_graph_node_once&#91;4&#93;</code><br><code>tests/test_timeline_history_assembly.py::test_provider_history_lookup_authenticates_each_graph_node_once&#91;8&#93;</code> |
| XML-010 | 2 | failure 2 | <code>tests/test_timeline_absent_head_repair_integration.py::test_repair_exact_bootstrap_retry_restart_and_edit_undo&#91;absent&#93;</code><br><code>tests/test_timeline_absent_head_repair_integration.py::test_repair_exact_bootstrap_retry_restart_and_edit_undo&#91;null&#93;</code> |
| XML-011 | 2 | failure 2 | <code>tests/test_portable_lifecycle.py::test_installed_up_wait_and_down_stop_the_exact_discovered_owner</code><br><code>tests/test_profile_services.py::test_installed_run_and_up_supervise_declared_service_and_report_status&#91;up&#93;</code> |
| XML-012 | 2 | failure 2 | <code>tests/test_timeline_commit_integration.py::test_real_mixed_helper_commit_undo_is_exact_or_refuses_overlap&#91;immediate&#93;</code><br><code>tests/test_timeline_commit_integration.py::test_real_mixed_helper_commit_undo_is_exact_or_refuses_overlap&#91;later-overlap&#93;</code> |
| XML-013 | 2 | failure 2 | <code>tests/test_capture_candidate_binding.py::test_real_structural_drafts_keep_certification&#91;inline-recorded_clone&#93;</code><br><code>tests/test_capture_candidate_binding.py::test_real_structural_drafts_keep_certification&#91;ref-recorded_clone&#93;</code> |
| XML-014 | 2 | failure 2 | <code>tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent&#91;history-http&#93;</code><br><code>tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent&#91;stale-head-http&#93;</code> |
| XML-015 | 2 | failure 2 | <code>tests/test_timeline_commit_restore_integration.py::test_real_restore_retained_inputs_inverse_redo_and_restart_retry&#91;transcript&#93;</code><br><code>tests/test_timeline_commit_restore_integration.py::test_real_restore_retained_inputs_inverse_redo_and_restart_retry&#91;config&#93;</code> |
| XML-016 | 2 | failure 2 | <code>tests/test_timeline_commit_input_integration.py::test_retained_input_real_move_inverse_replay_after_restart&#91;transcript&#93;</code><br><code>tests/test_timeline_commit_input_integration.py::test_retained_input_real_move_inverse_replay_after_restart&#91;config&#93;</code> |
| XML-017 | 1 | failure 1 | <code>tests/test_timeline_clip_replacement.py::test_native_generic_visual_media_requires_video_stream</code> |
| XML-018 | 1 | failure 1 | <code>tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept</code> |
| XML-019 | 1 | failure 1 | <code>tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_tampered_cas_without_mutation</code> |
| XML-020 | 1 | failure 1 | <code>tests/test_portable_lifecycle.py::test_installed_up_reports_occupied_browser_door_without_claiming_owner</code> |
| XML-021 | 1 | failure 1 | <code>tests/test_timeline_visual_fields.py::test_supported_top_level_type_on_retains_original_roundtrip_expectations</code> |
| XML-022 | 1 | failure 1 | <code>tests/test_timeline_clip_replacement.py::test_native_clip_swap_rebases_after_disjoint_intervening_edit</code> |
| XML-023 | 1 | failure 1 | <code>tests/test_timeline_ordinary_http.py::test_ordinary_http_empty_bootstrap_must_be_reachable</code> |
| XML-024 | 1 | failure 1 | <code>tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs&#91;parent-ref&#93;</code> |
| XML-025 | 1 | failure 1 | <code>tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs&#91;child-ref&#93;</code> |
| XML-026 | 1 | failure 1 | <code>tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs&#91;parent-inline&#93;</code> |
| XML-027 | 1 | failure 1 | <code>tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs&#91;child-inline&#93;</code> |
| XML-028 | 1 | failure 1 | <code>tests/test_timeline_clip_replacement.py::test_native_clip_swap_is_atomic_cas_and_exactly_replayable</code> |
| XML-029 | 1 | failure 1 | <code>tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route</code> |
| XML-030 | 1 | failure 1 | <code>tests/test_timeline_commit_input_integration.py::test_move_from_corrupt_local_timing_cache_conflicts_without_writes&#91;transcript&#93;</code> |
| XML-031 | 1 | failure 1 | <code>tests/test_timeline_commit_input_integration.py::test_move_from_corrupt_local_timing_cache_conflicts_without_writes&#91;config&#93;</code> |
| XML-032 | 1 | failure 1 | <code>tests/test_portable_lifecycle.py::test_real_post_worker_finishes_after_runtime_daemon_process_is_killed</code> |
| XML-033 | 1 | failure 1 | <code>tests/test_portable_lifecycle.py::test_installed_foreground_runtime_owns_discovery_door_and_stops_cleanly</code> |
| XML-034 | 1 | failure 1 | <code>tests/test_portable_lifecycle.py::test_installed_foreground_use_down_then_up_again</code> |
| XML-035 | 1 | failure 1 | <code>tests/test_profile_services.py::test_installed_run_and_up_supervise_declared_service_and_report_status&#91;run&#93;</code> |
| XML-036 | 1 | failure 1 | <code>tests/test_astrid_activation_join.py::test_runtime_relay_to_generic_host_successor_finalization_cpu</code> |
| XML-037 | 1 | failure 1 | <code>tests/test_timeline_redo_restoration_boundary.py::test_redo_requires_exact_source_restoration_and_absent_owner_guard&#91;read-path&#93;</code> |
| XML-038 | 1 | failure 1 | <code>tests/test_render_historical_admission.py::test_archived_timeline_refuses_first_admission_and_replay&#91;True&#93;</code> |
| XML-039 | 1 | failure 1 | <code>tests/test_runtime_pack_startup.py::test_foreground_uses_source_profile_installed_packs_without_callback</code> |
| XML-040 | 1 | failure 1 | <code>tests/test_render_historical_admission.py::test_historical_late_admission_refusal_writes_no_snapshot&#91;storage&#93;</code> |
| XML-041 | 1 | failure 1 | <code>tests/test_verified_host_launch.py::test_nine_component_measurement_parity_without_importing_astrid</code> |
| XML-042 | 1 | failure 1 | <code>tests/test_astrid_product_down.py::test_down_waits_for_selected_generic_host_exit</code> |
| XML-043 | 1 | failure 1 | <code>tests/test_runtime_pack_startup.py::test_real_cli_child_reads_persisted_admissions_and_restarts&#91;profile&#93;</code> |
| XML-044 | 1 | error 1 | <code>tests/test_timeline_public_s2_mixed_cli_journey.py::test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo&#91;literal-media&#93;</code> |
| XML-045 | 1 | error 1 | <code>tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated</code> |
| XML-046 | 1 | error 1 | <code>tests/test_timeline_public_s2_mixed_cli_journey.py::test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo&#91;historical-audio&#93;</code> |
| XML-047 | 1 | failure 1 | <code>tests/test_shot_candidate_promotion.py::test_catalog_promotion_preserves_accepted_film_and_retries_before_live_guards</code> |
| XML-048 | 1 | failure 1 | <code>tests/test_shot_candidate_promotion.py::test_catalog_promotion_prevents_native_overwrite_after_historical_reuse</code> |
| XML-049 | 1 | failure 1 | <code>tests/test_timeline_projection_occupancy.py::test_actual_provider_historical_slot_rematerializes_after_verified_restore</code> |
| XML-050 | 1 | failure 1 | <code>tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent&#91;tampered-child&#93;</code> |
| XML-051 | 1 | failure 1 | <code>tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source</code> |
| XML-052 | 1 | failure 1 | <code>tests/test_foreground_authoring_integration.py::test_foreground_boundary_creates_timeline_and_commits</code> |
| XML-053 | 1 | failure 1 | <code>tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap</code> |

Every message below is copied from the XML message attribute and retains its multiline layout. The complete per-ID detail text and triage provenance are in the JSON ledger.

### XML-001 — 34 (failure 34)

Test IDs:
- `tests/test_timeline_commit_integration.py::test_agent_provider_refuses_top_level_type_on_without_publication` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_agent_provider_refuses_animation_in_unsupported_phase_without_publication` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication[entrance-value0]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication[entrance-value1]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication[entrance-value2]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_unsupported_visual_fields_refuse_before_publication[transition-value3]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_visual_candidate_is_refused_before_publication_when_builtin_phase_is_unsupported` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_unverified_dependencies_cannot_escape_the_graph[queued-row]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_unverified_dependencies_cannot_escape_the_graph[indirect-cycle]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[metadata-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[parent-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[event-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[file-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[abi-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[ledger-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[records-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[source-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[closure-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[owner-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[realm-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[sequence-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[pin-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[queued-cycle-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_inputs_changed_after_ancestor_check[deleted-row-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check[transcript-content-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check[transcript-binding-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check[transcript-link-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check[config-content-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check[config-binding-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_retained_inputs_changed_after_check[config-link-collection]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_refuses_mutation_after_dependent_history_reads[head]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_visual_fields.py::test_visual_fields_on_audio_track_are_refused_before_publication[entrance-value0]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_visual_fields.py::test_visual_fields_on_audio_track_are_refused_before_publication[exit-value1]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_visual_fields.py::test_visual_fields_on_audio_track_are_refused_before_publication[transition-value2]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
Failed: DID NOT RAISE RuntimeErrorBase
````

### XML-002 — 21 (failure 21)

Test IDs:
- `tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary[pre-commit]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary[pre-restore]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary[before-commit]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary[before-restore]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary[after-commit]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary[after-restore]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[transcript-pre-commit]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[transcript-pre-restore]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[transcript-before-commit]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[transcript-before-restore]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[transcript-after-commit]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[transcript-after-restore]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[config-pre-commit]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[config-pre-restore]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[config-before-commit]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[config-before-restore]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[config-after-commit]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_retained_inputs_process_death[config-after-restore]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death[pre-transcript]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death[before-transcript]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death[after-transcript]` — failure; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
assert 33 == 31
````

### XML-003 — 20 (error 20)

Test IDs:
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[genuine-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[genuine-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[genuine-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[genuine-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[native-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[native-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[native-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[native-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[config-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[config-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[config-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[config-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[registry-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[registry-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[registry-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[registry-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[expansion-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[expansion-ref]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[expansion-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_snapshot_legacy_certification.py::test_exact_legacy_capture_retry_after_upgrade[expansion-inline]` — error; triage: R-c / RE3; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
failed on setup with "RuntimeError: cannot archive required commit 321cef4b8c89a4a938cb9ede41ba6a5444cf1b62 from /home/runner/work/astrid-runtime/astrid-runtime/astrid-agent; fetch this SHA or full history with `git -C /home/runner/work/astrid-runtime/astrid-runtime/astrid-agent fetch origin 321cef4b8c89a4a938cb9ede41ba6a5444cf1b62`"
````

### XML-004 — 5 (failure 5)

Test IDs:
- `tests/test_render_historical_admission.py::test_corrupt_retained_dependency_refuses_without_writes` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication[missing]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication[same-size]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication[custody]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_render_historical_admission.py::test_retained_integrity_is_checked_before_any_publication[size]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'reason': 'r...blication_id'} == {'reason': 'r...3f91bd4312ea'}
  
  Differing items:
  {'reason': 'render_revision_mismatch'} != {'reason': 'render_revision_integrity'}
  Left contains 1 more item:
  {'field': 'publication_id'}
  Right contains 1 more item:
  {'dependency_id': 'sha256:2fdf9812c168d161dd908889aa86bdd09dceea94b8dddf4ab2043f91bd4312ea'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
  -     'reason': 'render_revision_integrity',
[+6 more lines; full report in element text]
````

### XML-005 — 5 (error 5)

Test IDs:
- `tests/test_runtime_boundary.py::test_separate_failed_start_preserves_live_discovery` — error; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_runtime_boundary.py::test_foreign_pid_observation_cannot_reclaim_live_publication` — error; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_runtime_boundary.py::test_down_without_discovery_cannot_report_live_owner_stopped[False]` — error; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_runtime_boundary.py::test_down_without_discovery_cannot_report_live_owner_stopped[True]` — error; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_runtime_boundary.py::test_failed_candidate_pid_alias_cannot_retire_live_publication` — error; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
failed on setup with "RuntimeError: process control is already strict; refusing to change it to sandbox"
````

### XML-006 — 4 (failure 4)

Test IDs:
- `tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death[pre-config]` — failure; triage: R-d / RT1; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death[before-config]` — failure; triage: R-d / RT1; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_crash.py::test_host_boundary_first_capture_process_death[after-config]` — failure; triage: R-d / RT1; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent[declared-media]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.ConflictError: v33 provider/baseline verification is pending; requests and fresh pins are fenced
````

### XML-007 — 3 (failure 3)

Test IDs:
- `tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter[linux]` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter[darwin]` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_update_jobs.py::test_authenticated_update_route_runs_selected_agent_platform_adapter[win32]` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert False
 +  where False = is_relative_to(PosixPath('/home/runner/work/astrid-runtime/astrid-agent'))
 +    where is_relative_to = PosixPath('/home/runner/work/astrid-runtime/astrid-runtime/astrid-agent/astrid/installer/update_job.py').is_relative_to
 +      where PosixPath('/home/runner/work/astrid-runtime/astrid-runtime/astrid-agent/astrid/installer/update_job.py') = Path('/home/runner/work/astrid-runtime/astrid-runtime/astrid-agent/astrid/installer/update_job.py')
[+1 more line; full report in element text]
````

### XML-008 — 3 (failure 3)

Test IDs:
- `tests/test_timeline_commit_integration.py::test_agent_written_visual_fields_validate_and_read_back_from_published_revision` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_visual_fields.py::test_visual_field_provider_acceptance_and_refusal_regressions` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_visual_fields.py::test_visual_field_provider_preserves_opaque_custom_data` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
astrid.core.timeline.clip_fields.ClipFieldError: entrance has unknown key 'durationFrames'; allowed: type, duration
````

### XML-009 — 3 (failure 3)

Test IDs:
- `tests/test_timeline_history_assembly.py::test_provider_history_lookup_authenticates_each_graph_node_once[2]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_history_lookup_authenticates_each_graph_node_once[4]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_history_assembly.py::test_provider_history_lookup_authenticates_each_graph_node_once[8]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.timeline_commit_port.CommitUnavailable: Timeline commit outcome unavailable; retry the exact request
````

### XML-010 — 2 (failure 2)

Test IDs:
- `tests/test_timeline_absent_head_repair_integration.py::test_repair_exact_bootstrap_retry_restart_and_edit_undo[absent]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_absent_head_repair_integration.py::test_repair_exact_bootstrap_retry_restart_and_edit_undo[null]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'schema_vers...y': {}}}, ...} == {'schema_vers...fc261c'}, ...}
  
  Omitting 6 identical items, use -vv to show
  Differing items:
[+54 more lines; full report in element text]
````

### XML-011 — 2 (failure 2)

Test IDs:
- `tests/test_portable_lifecycle.py::test_installed_up_wait_and_down_stop_the_exact_discovered_owner` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_profile_services.py::test_installed_run_and_up_supervise_declared_service_and_report_status[up]` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: {
    "error": "Requested Runtime identity could not be verified.",
    "ok": false
  }
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/tmp/pytest-of-runner/pytest-0/stage1-runtime0/venv/bin/python', '-m', 'astrid_runtime.cli', '...turncode=1, stdout='{\n  "error": "Requested Runtime identity could not be verified.",\n  "ok": false\n}\n', stderr='').returncode
````

### XML-012 — 2 (failure 2)

Test IDs:
- `tests/test_timeline_commit_integration.py::test_real_mixed_helper_commit_undo_is_exact_or_refuses_overlap[immediate]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_integration.py::test_real_mixed_helper_commit_undo_is_exact_or_refuses_overlap[later-overlap]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AttributeError: 'NoneType' object has no attribute 'client'
````

### XML-013 — 2 (failure 2)

Test IDs:
- `tests/test_capture_candidate_binding.py::test_real_structural_drafts_keep_certification[inline-recorded_clone]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_capture_candidate_binding.py::test_real_structural_drafts_keep_certification[ref-recorded_clone]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
astrid.sdk.timeline._command_state.CommandError: shot item source is unavailable
````

### XML-014 — 2 (failure 2)

Test IDs:
- `tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent[history-http]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent[stale-head-http]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.ConflictError: migrated realm requires fresh Timeline provider registration before readiness
````

### XML-015 — 2 (failure 2)

Test IDs:
- `tests/test_timeline_commit_restore_integration.py::test_real_restore_retained_inputs_inverse_redo_and_restart_retry[transcript]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_restore_integration.py::test_real_restore_retained_inputs_inverse_redo_and_restart_retry[config]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.RuntimeErrorBase: candidate.shots['shot-1'].internal_timeline.clips['clip-1'].elementRef: historical text binding requires an unchanged declaration and source
````

### XML-016 — 2 (failure 2)

Test IDs:
- `tests/test_timeline_commit_input_integration.py::test_retained_input_real_move_inverse_replay_after_restart[transcript]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.
- `tests/test_timeline_commit_input_integration.py::test_retained_input_real_move_inverse_replay_after_restart[config]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.RuntimeErrorBase: candidate.timing: legacy word anchor is missing
````

### XML-017 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_clip_replacement.py::test_native_generic_visual_media_requires_video_stream` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: Regex pattern did not match.
  Expected regex: 'image/video'
  Actual message: 'media swap preserves media kind'
````

### XML-018 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: Regex pattern did not match.
  Expected regex: 'immutable|changed|integrity|size'
  Actual message: 'CAS object failed hash verification'
````

### XML-019 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_tampered_cas_without_mutation` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: Regex pattern did not match.
  Expected regex: 'immutable|changed|integrity|size'
  Actual message: 'Timeline commit outcome unavailable; retry the exact request'
````

### XML-020 — 1 (failure 1)

Test IDs:
- `tests/test_portable_lifecycle.py::test_installed_up_reports_occupied_browser_door_without_claiming_owner` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert '55871' in 'requested runtime identity could not be verified.'
 +  where '55871' = str(55871)
````

### XML-021 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_visual_fields.py::test_supported_top_level_type_on_retains_original_roundtrip_expectations` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert 'None' == 'type-on 60f'
  
  - type-on 60f
  + None
````

### XML-022 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_clip_replacement.py::test_native_clip_swap_rebases_after_disjoint_intervening_edit` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert 'merged' == 'rebased'
  
  - rebased
  + merged
````

### XML-023 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_ordinary_http.py::test_ordinary_http_empty_bootstrap_must_be_reachable` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert [{'blendMode'...e': 'output'}] == [{'id': 'pict...None, False]}]
  
  At index 0 diff: {'blendMode': 'normal', 'fit': 'contain', 'id': 'V1', 'kind': 'visual', 'label': 'V1', 'opacity': 1, 'scale': 1} != {'id': 'picture', 'kind': 'visual', 'role': 'output', 'opaque': [None, False]}
  Left contains 2 more items, first extra item: {'blendMode': 'normal', 'fit': 'contain', 'id': 'A1', 'kind': 'audio', ...}
  
  Full diff: (-: missing in left side, +: extra in left side)
    [
[+29 more lines; full report in element text]
````

### XML-024 — 1 (failure 1)

Test IDs:
- `tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs[parent-ref]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'authority':...1], ...}, ...} == {'ref': {'dig...9d82600167'}}}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'transition_contract': 'runtime-parent-closure/v1'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
  +     'authority': {
  +         'expansion': {
  +             'canonical': True,
  +             'children': [
  +                 {
[+850 more lines; full report in element text]
````

### XML-025 — 1 (failure 1)

Test IDs:
- `tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs[child-ref]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'authority':...1], ...}, ...} == {'ref': {'dig...b964bcd37b'}}}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'transition_contract': 'runtime-parent-closure/v1'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
  +     'authority': {
  +         'expansion': {
  +             'canonical': True,
  +             'children': [
  +                 {
[+842 more lines; full report in element text]
````

### XML-026 — 1 (failure 1)

Test IDs:
- `tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs[parent-inline]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'authority':...1], ...}, ...} == {'ref': {'dig...d74c467852'}}}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'transition_contract': 'runtime-parent-closure/v1'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
  +     'authority': {
  +         'expansion': {
  +             'canonical': True,
  +             'children': [
  +                 {
[+850 more lines; full report in element text]
````

### XML-027 — 1 (failure 1)

Test IDs:
- `tests/test_capture_candidate_binding.py::test_real_candidate_reaches_verified_host_without_mutating_inputs[child-inline]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'authority':...1], ...}, ...} == {'ref': {'dig...f58603befa'}}}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'transition_contract': 'runtime-parent-closure/v1'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
  +     'authority': {
  +         'expansion': {
  +             'canonical': True,
  +             'children': [
  +                 {
[+842 more lines; full report in element text]
````

### XML-028 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_clip_replacement.py::test_native_clip_swap_is_atomic_cas_and_exactly_replayable` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'clips': [{'...': 'visual'}]} == {'clips': [{'...': 'visual'}]}
  
  Omitting 3 identical items, use -vv to show
  Differing items:
[+46 more lines; full report in element text]
````

### XML-029 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'clips': [{'...': 'visual'}]} == {'clips': [{'...': 'visual'}]}
  
  Omitting 3 identical items, use -vv to show
  Differing items:
[+52 more lines; full report in element text]
````

### XML-030 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_commit_input_integration.py::test_move_from_corrupt_local_timing_cache_conflicts_without_writes[transcript]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'status': 'c...: ['at'], ...} == {'status': 'c...155681'}, ...}
  
  Omitting 5 identical items, use -vv to show
  Left contains 4 more items:
  {'code': 'dependency_changed',
   'hint': 'Read the current dependency and reapply the intended change',
   'path': ['at'],
   'suggested_command': 'timeline show'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
        'status': 'conflict',
        'reason': 'dependency_changed',
[+36 more lines; full report in element text]
````

### XML-031 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_commit_input_integration.py::test_move_from_corrupt_local_timing_cache_conflicts_without_writes[config]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: assert {'status': 'c...: ['at'], ...} == {'status': 'c...46a51b'}, ...}
  
  Omitting 5 identical items, use -vv to show
  Left contains 4 more items:
  {'code': 'dependency_changed',
   'hint': 'Read the current dependency and reapply the intended change',
   'path': ['at'],
   'suggested_command': 'timeline show'}
  
  Full diff: (-: missing in left side, +: extra in left side)
    {
        'status': 'conflict',
        'reason': 'dependency_changed',
[+36 more lines; full report in element text]
````

### XML-032 — 1 (failure 1)

Test IDs:
- `tests/test_portable_lifecycle.py::test_real_post_worker_finishes_after_runtime_daemon_process_is_killed` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: b'{"code": "conflict", "details": {"reason": "selection-or-inputs-invalid"}, "message": "The selected installation or update inputs do not match this running Astrid.", "request_id": "08ca3992e9ca44fc89576808081e9643"}'
assert 409 == 202
[+1 more line; full report in element text]
````

### XML-033 — 1 (failure 1)

Test IDs:
- `tests/test_portable_lifecycle.py::test_installed_foreground_runtime_owns_discovery_door_and_stops_cleanly` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: foreground Runtime exited 1: {
  "error": "Requested Runtime identity could not be verified.",
  "log": "/tmp/pytest-of-runner/pytest-0/test_installed_foreground_runt0/state/astrid-runtime/logs/runtime.log",
  "ok": false
}
````

### XML-034 — 1 (failure 1)

Test IDs:
- `tests/test_portable_lifecycle.py::test_installed_foreground_use_down_then_up_again` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: foreground Runtime exited 1: {
  "error": "Requested Runtime identity could not be verified.",
  "log": "/tmp/pytest-of-runner/pytest-0/test_installed_foreground_use_0/state/astrid-runtime/logs/runtime.log",
  "ok": false
}
````

### XML-035 — 1 (failure 1)

Test IDs:
- `tests/test_profile_services.py::test_installed_run_and_up_supervise_declared_service_and_report_status[run]` — failure; triage: R-k / RT7; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AssertionError: foreground Runtime exited 1: {
  "error": "Requested Runtime identity could not be verified.",
  "log": "/tmp/pytest-of-runner/pytest-0/test_installed_run_and_up_supe0/state/astrid-runtime/logs/runtime.log",
  "ok": false
}
````

### XML-036 — 1 (failure 1)

Test IDs:
- `tests/test_astrid_activation_join.py::test_runtime_relay_to_generic_host_successor_finalization_cpu` — failure; triage: R-j / RT6 (new signature); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
AttributeError: <module 'astrid_runtime.custody_broker' from '/home/runner/work/astrid-runtime/astrid-runtime/astrid_runtime/custody_broker.py'> has no attribute 'DARWIN_CUSTODY_SOCKET_PARENT'
````

### XML-037 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_redo_restoration_boundary.py::test_redo_requires_exact_source_restoration_and_absent_owner_guard[read-path]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
Failed: DID NOT RAISE CommitRejected
````

### XML-038 — 1 (failure 1)

Test IDs:
- `tests/test_render_historical_admission.py::test_archived_timeline_refuses_first_admission_and_replay[True]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
Failed: DID NOT RAISE ConflictError
````

### XML-039 — 1 (failure 1)

Test IDs:
- `tests/test_runtime_pack_startup.py::test_foreground_uses_source_profile_installed_packs_without_callback` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
IndexError: list index out of range
````

### XML-040 — 1 (failure 1)

Test IDs:
- `tests/test_render_historical_admission.py::test_historical_late_admission_refusal_writes_no_snapshot[storage]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
KeyError: 'required_bytes'
````

### XML-041 — 1 (failure 1)

Test IDs:
- `tests/test_verified_host_launch.py::test_nine_component_measurement_parity_without_importing_astrid` — failure; triage: Plan 38 P2r/A3 source-closure parity; owner: WAITING — Plan 38 closure-contract ownership

Exact XML message attribute:

````text
KeyError: 'source_checkout_closure'
````

### XML-042 — 1 (failure 1)

Test IDs:
- `tests/test_astrid_product_down.py::test_down_waits_for_selected_generic_host_exit` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
RuntimeError: process control is already strict; refusing to change it to sandbox
````

### XML-043 — 1 (failure 1)

Test IDs:
- `tests/test_runtime_pack_startup.py::test_real_cli_child_reads_persisted_admissions_and_restarts[profile]` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
assert 0 == 7
````

### XML-044 — 1 (error 1)

Test IDs:
- `tests/test_timeline_public_s2_mixed_cli_journey.py::test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo[literal-media]` — error; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
failed on setup with "astrid.sdk.workspace_client.WorkspaceClientError: legacy timeline writes are retired; submit EditCommands through commitTimeline"
````

### XML-045 — 1 (error 1)

Test IDs:
- `tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated` — error; triage: R-j / RT6; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
failed on setup with "runtime_protocol.errors.ConflictError: realm failed integrity checks"
````

### XML-046 — 1 (error 1)

Test IDs:
- `tests/test_timeline_public_s2_mixed_cli_journey.py::test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo[historical-audio]` — error; triage: R-d / RT1; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
failed on setup with "runtime_protocol.errors.ConflictError: v33 provider/baseline verification is pending; requests and fresh pins are fenced"
````

### XML-047 — 1 (failure 1)

Test IDs:
- `tests/test_shot_candidate_promotion.py::test_catalog_promotion_preserves_accepted_film_and_retries_before_live_guards` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.ConflictError: v33 provider registration is required for this process before requests and fresh pins
````

### XML-048 — 1 (failure 1)

Test IDs:
- `tests/test_shot_candidate_promotion.py::test_catalog_promotion_prevents_native_overwrite_after_historical_reuse` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.RuntimeErrorBase: candidate.shots['shot-3'].internal_timeline.clips['clip-3']: timeline interval must fit the occurrence's half-open bounds
````

### XML-049 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_projection_occupancy.py::test_actual_provider_historical_slot_rematerializes_after_verified_restore` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.RuntimeErrorBase: candidate.shots['shot-placement-96f3e4829dd24d83fda944c26dc090557c5c7ee3a8b0724f5255511d2da50e46'].internal_timeline.clips['clip-3']: timeline interval must fit the occurrence's half-open bounds
````

### XML-050 — 1 (failure 1)

Test IDs:
- `tests/test_timeline_commit_restore_integration.py::test_original_restore_behaviour_with_real_agent[tampered-child]` — failure; triage: R-n (new; RE1/RE2); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.RuntimeErrorBase: revision content digest mismatch
````

### XML-051 — 1 (failure 1)

Test IDs:
- `tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.errors.ValidationError: canonical capture projection provider is unavailable
````

### XML-052 — 1 (failure 1)

Test IDs:
- `tests/test_foreground_authoring_integration.py::test_foreground_boundary_creates_timeline_and_commits` — failure; triage: R-o (new; unclassified); owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
runtime_protocol.source_identity.SourceIdentityError: untracked source directory is unsupported: /home/runner/work/astrid-runtime/astrid-runtime/astrid-agent
````

### XML-053 — 1 (failure 1)

Test IDs:
- `tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap` — failure; triage: R-b / RE2; owner: No new exact Plan38/Plan55 WAITING assignment in this full-message ledger; see existing exact owner evidence.

Exact XML message attribute:

````text
subprocess.CalledProcessError: Command '['git', '-C', '/home/user/work/wt/agt-pin-6efc8150', 'rev-parse', 'HEAD']' returned non-zero exit status 128.
````
