# integration-2 (job 133536534820)

Counts: `{'PASSED': 266, 'FAILED': 78, 'ERROR': 172, 'SKIPPED': 0}`. Run-level state was `in_progress`; this is partial diagnostic evidence, not G2 acceptance.

XML artifact `14262871202`; ZIP SHA-256 `79ea90030456ba7daab9fd57657c2ae4e518427dd025bdfff82332ec2ec3ca60`. XML carries full testcase failure/error payloads.

Outer pytest summary:
```text
= 78 failed, 266 passed, 32170 deselected, 22 warnings, 172 errors in 1298.08s (0:21:38) =
```

## Failure and error groups

Groups use exact XML `message` attributes; complete testcase IDs are retained. Full XML testcase `detail` is losslessly available in JSON records.

### Failure × 78

```text
failed on setup with "astrid.sdk.timeline._command_state.CommandError: replacement changes provider-managed edges"
```

IDs:
- `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py::test_real_media_manifest_inverse_retry_restart_and_history[add]`
- `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py::test_real_media_manifest_inverse_retry_restart_and_history[swap]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-swap]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[video-add]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[video-swap]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-stale-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-stale-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-foreign-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-foreign-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-fingerprint-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-fingerprint-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-stale-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-stale-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-foreign-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-foreign-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-fingerprint-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-fingerprint-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-stale-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-stale-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-foreign-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-foreign-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-fingerprint-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-fingerprint-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-stale-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-stale-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-foreign-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-foreign-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-fingerprint-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-fingerprint-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[image-add]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[image-swap]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[video-add]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[video-swap]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-lifecycle-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-lifecycle-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-revocation-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-revocation-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-lifecycle-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-lifecycle-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-revocation-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-revocation-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-lifecycle-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-lifecycle-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-revocation-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-revocation-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-lifecycle-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-lifecycle-media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-revocation-old_media]`
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-revocation-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo[image]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo[video]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_over_authenticated_http_preserves_flight_and_guarded_undo[parent]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_over_authenticated_http_preserves_flight_and_guarded_undo[occurrence:occ-a]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-stale-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-stale-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-foreign-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-foreign-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-fingerprint-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-fingerprint-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-stale-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-stale-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-foreign-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-foreign-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-fingerprint-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-fingerprint-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[image-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[image-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[video-old_media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[video-media]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[image-disjoint]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[image-aba]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[video-disjoint]`
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[video-aba]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-False]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-True]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-False]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-True]`

### Failure × 44

```text
failed on setup with "FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz'"
```

IDs:
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_authenticated_source_baseline_restores_exact_legacy_bytes[inverse]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_authenticated_source_baseline_restores_exact_legacy_bytes[step-inverse]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_authenticated_source_baseline_restores_exact_legacy_bytes[restore]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_inverse_preserves_unrelated_parent_move[False]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_inverse_preserves_unrelated_parent_move[True]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[new]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[modified]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[equal-authored]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[forged-source]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[forged-publication]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[forged-step]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[digest]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[foreign]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[aba]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[membership]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[order]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[changed]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[alias]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[shot-owner]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[internal-owner]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[target]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[target-remove]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[documents]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[outside]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[no-writes]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[ordinary-write]`
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[until-flag]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_retains_authenticated_pair_and_canonical_source`
- `tests/editing_conformance/test_current_pair_reader.py::test_explicit_historical_read_does_not_acquire_current_publication`
- `tests/editing_conformance/test_current_pair_reader.py::test_explicit_wrong_publication_refuses`
- `tests/editing_conformance/test_current_pair_reader.py::test_reset_reads_reused_revision_under_new_publication`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_requires_exact_publication_history_entry[missing-entry]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_requires_exact_publication_history_entry[wrong-revision]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_requires_exact_publication_history_entry[wrong-receipt]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[missing-head]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[missing-publication]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[changed-head]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[history-error]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[project_id]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[timeline_id]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[revision_id]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[content_digest]`
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[internal-owner]`
- `tests/editing_conformance/test_m1_legacy_archive_read.py::test_explicit_held_baseline_then_current_word_bound_read_is_closure_exact`

### Failure × 21

```text
failed on setup with "runtime_protocol.errors.RuntimeErrorBase: candidate.timing: legacy word anchor is missing"
```

IDs:
- `tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[touched-basis-conflict]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_lost_ack_restart_and_fresh_head`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_requires_write_but_inspection_remains_read_only`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-image]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-video]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-image]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-video]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-image]`
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-video]`
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]`
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]`
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_param_commands_keep_exact_cli_ingress_and_unchanged_write_history`
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable`
- `tests/editing_conformance/test_commit_runtime_native_frontends.py::test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[False]`
- `tests/editing_conformance/test_commit_runtime_native_frontends.py::test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[True]`
- `tests/editing_conformance/test_commit_runtime_native_frontends.py::test_checkout_first_refuses_sheet_suffix_keeps_draft_and_pending_intent`
- `tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py::test_grouped_parent_track_create_move_reload_undo_redo`
- `tests/editing_conformance/test_commit_runtime_parent_track_label.py::test_move_then_parent_label_reload_inverse_preserves_newer_disjoint_move`
- `tests/editing_conformance/test_commit_runtime_parent_track_label.py::test_native_label_cli_lost_ack_then_python_suffix_keeps_original_claims`
- `tests/editing_conformance/test_commit_runtime_scalar.py::test_move_then_scalar_outbox_handoff_reload_and_guarded_inverse`

### Failure × 9

```text
astrid.sdk.workspace_client.WorkspaceClientError: candidate.timing: invalid timing input: ''
```

IDs:
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_cut_owned_native_sheet_hold_reloads_and_undoes`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[python]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[cli]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[sheet]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_attached_parent_label_publish_retries_exact_capture_and_inverse`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_original_attached_add_track_publish_retries_exact_capture_and_guarded_inverse`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[python]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[cli]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[sheet]`

### Failure × 7

```text
failed on setup with "AssertionError: assert '2538efa2efcf...5060153736c7e' == '2b81e46ac0f3...671eff75107b3'
  
  - 2b81e46ac0f3553d1de812cf0533be2a9aecbd8cdfcaab118ac671eff75107b3
  + 2538efa2efcfd581fb0d4296dc6cbfcc9d906f14723000db9445060153736c7e"
```

IDs:
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-4-two-step-clips-before]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-16-two-step-clips-after]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-28-two-step-config-clips-before]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-40-two-step-config-clips-after]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-49-native-whole]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_inverse_refuses_forged_source_publication_and_step_without_writes`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_inverse_refuses_native_write_and_aba_without_writes`

### Failure × 6

```text
astrid.sdk.timeline_address.ElementPackNotInstalled: [element_pack_not_installed] audio: no installed pack declares this element, and it is not one this release knows moved to a pack; no param was written. Install the pack that provides it, or check the clip type (`astrid packs list` shows what is installed).
```

IDs:
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2.0-parent/clip:music-bed]`
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[1-True-parent/clip:music-bed]`
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[True-1-parent/clip:music-bed]`
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2-parent/clip:music-bed]`
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[True-True-parent/clip:music-bed]`
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_commands_file_preserves_opaque_unchanged_write_and_undo`

### Failure × 5

```text
AssertionError: assert 'merged' == 'rebased'
  
  - rebased
  + merged
```

IDs:
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-False]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-True]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-False]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-True]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection`

### Failure × 5

```text
failed on setup with "runtime_protocol.errors.RuntimeErrorBase: candidate.shots['shot-placement-271ff5ac6e7f5c9457f24655a71debca8383cec79839f3a52381233be3abb738'].internal_timeline.clips['clip-1'].elementRef: historical text binding requires an unchanged declaration and source"
```

IDs:
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization[authored-first]`
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_parent_edit[authored-first]`
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_sibling_edit[authored-first]`
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_refuses_touching_aba_atomically[authored-first]`
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_redo_refuses_intervening_aba_after_exact_undo[authored-first]`

### Failure × 4

```text
AssertionError: assert [] == [{'args': {'c...ed': [], ...}]
  
  Right contains 3 more items, first extra item: {'args': {'clear': [], 'values': {'label': 'B'}}, 'authorship': {'parent/track:picture::label': 'direct'}, 'bindings': {'scalar.target': 'parent/track:picture'}, 'created': [], ...}
  
  Full diff:
  + []
  - [
  -     {
  -         'args': {
  -             'clear': [],
  -             'values': {
  -                 'label': 'B',
  -             },
  -         },
  -         'authorship': {
  -             'parent/track:picture::label': 'direct',
  -         },
  -         'bindings': {
  -             'scalar.target': 'parent/track:picture',
  -         },
  -         'created': [],
  -         'expect': {
  -             'parent/track:picture::label': {
  -                 'state': 'present',
  -                 'value': 'A',
  -             },
  -         },
  -         'intent': {},
  -         'op': 'track.set',
  -         'reads': [
  -             {
  -                 'path': [
  -                     'id',
  -                 ],
  -                 'ref': 'parent/track:picture',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'picture',
  -                 },
  -             },
  -         ],
  -         'resolved': [
  -             'parent/track:picture',
  -         ],
  -         'schema_version': 1,
  -         'select': 'parent/track:picture',
  -         'selections': [],
  -         'version': '1',
  -     },
  -     {
  -         'args': {
  -             'clear': [],
  -             'values': {
  -                 'label': 'B',
  -             },
  -         },
  -         'authorship': {
  -             'parent/track:dependent::label': 'direct',
  -         },
  -         'bindings': {
  -             'scalar.target': 'parent/track:dependent',
  -         },
  -         'created': [],
  -         'expect': {
  -             'parent/track:dependent::label': {
  -                 'state': 'absent',
  -             },
  -         },
  -         'intent': {},
  -         'op': 'track.set',
  -         'reads': [
  -             {
  -                 'path': [
  -                     'id',
  -                 ],
  -                 'ref': 'parent/track:dependent',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'dependent',
  -                 },
  -             },
  -         ],
  -         'resolved': [
  -             'parent/track:dependent',
  -         ],
  -         'schema_version': 1,
  -         'select': 'parent/track:dependent',
  -         'selections': [],
  -         'version': '1',
  -     },
  -     {
  -         'args': {
  -             'clear': [],
  -             'values': {
  -                 'text': 'B',
  -             },
  -         },
  -         'authorship': {
  -             'parent/clip:title::params.text': 'direct',
  -         },
  -         'bindings': {
  -             'scalar.target': 'parent/clip:title',
  -         },
  -         'created': [],
  -         'expect': {
  -             'parent/clip:title::params.text': {
  -                 'state': 'present',
  -                 'value': 'A',
  -             },
  -         },
  -         'intent': {},
  -         'op': 'clip.set-params',
  -         'reads': [
  -             {
  -                 'path': [
  -                     'id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'title',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clipType',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'text',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clip_type',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'asset',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'asset_id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'media_id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'object_id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'elementRef',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'element_ref',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -         ],
  -         'resolved': [
  -             'parent/clip:title',
  -         ],
  -         'schema_version': 1,
  -         'select': 'parent/clip:title',
  -         'selections': [],
  -         'version': '1',
  -     },
  - ]
```

IDs:
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-False]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-True]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-False]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-True]`

### Failure × 4

```text
astrid.sdk.timeline._command_state.CommandError: created identity is occupied
```

IDs:
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[python]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[cli]`
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[sheet]`

### Failure × 4

```text
failed on setup with "IndexError: list index out of range"
```

IDs:
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[none-historical]`
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[disjoint-historical]`
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[trim-historical]`
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[params-historical]`

### Failure × 4

```text
failed on setup with "runtime_protocol.errors.RuntimeErrorBase: patch previous value does not match"
```

IDs:
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse[item_id]`
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse[both]`
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_inverse_restores_exact_original_closure[item_id]`
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_inverse_restores_exact_original_closure[both]`

### Failure × 3

```text
astrid.sdk.timeline_address.ElementPackNotInstalled: [element_pack_not_installed] image: no installed pack declares this element, and it is not one this release knows moved to a pack; no param was written. Install the pack that provides it, or check the clip type (`astrid packs list` shows what is installed).
```

IDs:
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-anchor]`
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-fallback]`
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-lane-end]`

### Failure × 3

```text
astrid.sdk.timeline_address.ElementPackNotInstalled: [element_pack_not_installed] video: no installed pack declares this element, and it is not one this release knows moved to a pack; no param was written. Install the pack that provides it, or check the clip type (`astrid packs list` shows what is installed).
```

IDs:
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[video-anchor]`
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[video-fallback]`
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[video-lane-end]`

### Failure × 3

```text
failed on setup with "AssertionError: assert '6855dfa8df65...4d6505493c17c' == 'f103bb468669...2e66d544e0c9b'
  
  - f103bb46866999c961a8865636f2e66d544e0c9b
  + 6855dfa8df65cf8ae4c002b57134d6505493c17c"
```

IDs:
- `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip[python]`
- `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip[cli]`
- `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip[sheet]`

### Failure × 3

```text
failed on setup with "runtime_protocol.errors.ConflictError: v33 provider/baseline verification is pending; requests and fresh pins are fenced"
```

IDs:
- `tests/editing_conformance/test_commit_runtime_identity.py::test_occupied_shared_occurrence_destination_refuses_atomically[same-project]`
- `tests/editing_conformance/test_commit_runtime_identity.py::test_occupied_shared_occurrence_destination_refuses_atomically[other-project]`
- `tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_occurrence_retry_own_move_and_historical_restore[fresh]`

### Failure × 3

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage source materialization is outside its physical turnover
```

IDs:
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization[original-third]`
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_parent_edit[original-third]`
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_redo_refuses_intervening_aba_after_exact_undo[original-third]`

### Failure × 2

```text
AssertionError: (1, {'data': None, 'error': {'code': 'timeline_edit_error', 'details': {}, 'message': 'exact transcript pin is missing or revoked or ambiguous'}, 'idempotency_key': '', 'ok': False, ...}, '')
assert 1 == 0
```

IDs:
- `tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[disjoint-rebase-undo]`
- `tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[touched-basis-conflict]`

### Failure × 2

```text
AssertionError: assert ([] == [{'args': {'c...ed': [], ...}]
  
  Right contains 2 more items, first extra item: {'args': {'clear': [], 'values': {'label': 'File'}}, 'authorship': {'parent/track:picture::label': 'direct'}, 'bindings': {'scalar.target': 'parent/track:picture'}, 'created': [], ...}
  
  Full diff:
  + []
  - [
  -     {
  -         'args': {
  -             'clear': [],
  -             'values': {
  -                 'label': 'File',
  -             },
  -         },
  -         'authorship': {
  -             'parent/track:picture::label': 'direct',
  -         },
  -         'bindings': {
  -             'scalar.target': 'parent/track:picture',
  -         },
  -         'created': [],
  -         'expect': {
  -             'parent/track:picture::label': {
  -                 'state': 'present',
  -                 'value': 'Picture',
  -             },
  -         },
  -         'intent': {},
  -         'op': 'track.set',
  -         'reads': [
  -             {
  -                 'path': [
  -                     'id',
  -                 ],
  -                 'ref': 'parent/track:picture',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'picture',
  -                 },
  -             },
  -         ],
  -         'resolved': [
  -             'parent/track:picture',
  -         ],
  -         'schema_version': 1,
  -         'select': 'parent/track:picture',
  -         'selections': [],
  -         'version': '1',
  -     },
  -     {
  -         'args': {
  -             'clear': [],
  -             'values': {
  -                 'text': 'File',
  -             },
  -         },
  -         'authorship': {
  -             'parent/clip:title::params.text': 'direct',
  -         },
  -         'bindings': {
  -             'scalar.target': 'parent/clip:title',
  -         },
  -         'created': [],
  -         'expect': {
  -             'parent/clip:title::params.text': {
  -                 'state': 'present',
  -                 'value': 'Edited',
  -             },
  -         },
  -         'intent': {},
  -         'op': 'clip.set-params',
  -         'rationale': 'Original file',
  -         'reads': [
  -             {
  -                 'path': [
  -                     'id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'title',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clipType',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'text',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clip_type',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'asset',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'asset_id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'media_id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'object_id',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'elementRef',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'element_ref',
  -                 ],
  -                 'ref': 'parent/clip:title',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -         ],
  -         'resolved': [
  -             'parent/clip:title',
  -         ],
  -         'schema_version': 1,
  -         'select': 'parent/clip:title',
  -         'selections': [],
  -         'version': '1',
  -     },
  - ])
```

IDs:
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-False]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-True]`

### Failure × 2

```text
KeyError: 'org.example/data'
```

IDs:
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_size_clear_uses_one_native_http_commit_and_guarded_inverse[detached-historical]`
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_font_color_uses_one_native_http_commit_and_guarded_inverse[detached-historical]`

### Failure × 2

```text
assert (1 == 0)
```

IDs:
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-False]`
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-True]`

### Failure × 2

```text
astrid.sdk.timeline._command_state.CommandError: exact transcript pin is missing or revoked or ambiguous
```

IDs:
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo[disjoint-peer]`
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo[touching-peer-conflict]`

### Failure × 2

```text
failed on setup with "runtime_protocol.errors.RuntimeErrorBase: shot item correspondence changed"
```

IDs:
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse[id]`
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_inverse_restores_exact_original_closure[id]`

### Failure × 2

```text
runtime_protocol.errors.RuntimeErrorBase: an intervening publication wrote a guarded address
```

IDs:
- `tests/editing_conformance/test_native_word_anchor.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-False]`
- `tests/editing_conformance/test_native_word_anchor.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-True]`

### Failure × 2

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage source materialization has no authenticated sibling edge
```

IDs:
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_retains_v1_after_v2_restart_exact_inverse_and_redo`
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_clear_removes_row_and_undo_restores_empty_exactly`

### Failure × 2

```text
runtime_protocol.errors.RuntimeErrorBase: provider intermediate promotion differs from its sequential allocation
```

IDs:
- `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py::test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[scalar]`
- `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py::test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[compound]`

### Failure × 1

```text
AssertionError: Regex pattern did not match.
  Expected regex: '10|16'
  Actual message: 'selected pack params require exact schema inputs (retained declaration): selected PARAM authority is unavailable'
```

IDs:
- `tests/core/test_timeline_element_publication_runtime.py::test_attached_selected_param_p1_survives_lost_ack_restart_and_undo`

### Failure × 1

```text
AssertionError: Regex pattern did not match.
  Expected regex: 'lost acknowledgement'
  Actual message: 'No reply could be verified; this edit may or may not have been committed. Call tl.commit(key="old-flight") again with no other arguments to confirm the saved request.'
```

IDs:
- `tests/core/test_timeline_element_publication_runtime.py::test_preexisting_element_hold_flight_retries_exact_body`

### Failure × 1

```text
AssertionError: Regex pattern did not match.
  Expected regex: 'timeline not found'
  Actual message: 'history_unavailable'
```

IDs:
- `tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance`

### Failure × 1

```text
AssertionError: assert (<class 'int'> is <class 'float'>)
 +  where <class 'int'> = type(2)
 +  and   <class 'float'> = type(2.0)
```

IDs:
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2.0-occurrence:occurrence-1/clip:clip-1]`

### Failure × 1

```text
AssertionError: assert ([] == [{'args': {'i...ed': [], ...}]
  
  Right contains one more item: {'args': {'in_s': None, 'out_s': 4}, 'authorship': {'parent/clip:literal::app': 'direct', 'parent/clip:literal::from':...'direct', 'parent/clip:literal::to': 'direct'}, 'bindings': {'trim.target': 'parent/clip:literal'}, 'created': [], ...}
  
  Full diff:
  + []
  - [
  -     {
  -         'args': {
  -             'in_s': None,
  -             'out_s': 4,
  -         },
  -         'authorship': {
  -             'parent/clip:literal::app': 'direct',
  -             'parent/clip:literal::from': 'direct',
  -             'parent/clip:literal::hold': 'direct',
  -             'parent/clip:literal::to': 'direct',
  -         },
  -         'bindings': {
  -             'trim.target': 'parent/clip:literal',
  -         },
  -         'created': [],
  -         'expect': {
  -             'parent/clip:literal::app': {
  -                 'state': 'present',
  -                 'value': {
  -                     'astrid': {
  -                         'opaque': [
  -                             None,
  -                             False,
  -                         ],
  -                     },
  -                     'extension': {
  -                         'keep': True,
  -                     },
  -                 },
  -             },
  -             'parent/clip:literal::from': {
  -                 'state': 'present',
  -                 'value': 1.0,
  -             },
  -             'parent/clip:literal::hold': {
  -                 'state': 'present',
  -                 'value': 4.000001,
  -             },
  -             'parent/clip:literal::to': {
  -                 'state': 'present',
  -                 'value': 5.000001,
  -             },
  -         },
  -         'intent': {},
  -         'op': 'clip.trim',
  -         'reads': [
  -             {
  -                 'path': [
  -                     'id',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'literal',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'at',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 0,
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'at_ms',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'track',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'picture',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'asset',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'asset_id',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'media_id',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'object_id',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clipType',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'media',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clip_type',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'enabled',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'active',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'disabled',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'hidden',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'deleted',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'from',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 1.0,
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'to',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 5.000001,
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'from_ms',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'to_ms',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'hold',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 4.000001,
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'duration',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'duration_ms',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'speed',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 2,
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'time_map',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'timeMap',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'clips',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'children',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'sourceURL',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'sourceUrl',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'source_url',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'src',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'source_uuid',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'source',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'source_window',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'source_offset',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'anchor',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'animation',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'animations',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'keyframes',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'curves',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'params',
  -                     'animation',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'params',
  -                     'animations',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'params',
  -                     'keyframes',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'params',
  -                     'curves',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'app',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': {
  -                         'astrid': {
  -                             'opaque': [
  -                                 None,
  -                                 False,
  -                             ],
  -                         },
  -                         'extension': {
  -                             'keep': True,
  -                         },
  -                     },
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'on',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'fixed_start',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'until',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'until_film_end',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'for',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'cut',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'sequence',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'sequence_index',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'sequence_fit',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'orphan',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'formulas',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'standin',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'standin_intent',
  -                 ],
  -                 'ref': 'parent/clip:literal',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'media_id',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'sha256:a13a68e512b6fae7fa4edd71b68266b33d1f7581be3fa199031809ec14d2f95e',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'object_id',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'digest',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'content_digest',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'type',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 'video',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'duration',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'present',
  -                     'value': 42.0,
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'duration_ms',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'duration_seconds',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'source',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'source_window',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'time_map',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -             {
  -                 'path': [
  -                     'assets',
  -                     'initial-4b5d08bdc5e79139d70de3132e449f70b6dcf747eabb76d4c3eab012f7e3c40d',
  -                     'timeMap',
  -                 ],
  -                 'ref': 'parent/registry',
  -                 'state': {
  -                     'state': 'absent',
  -                 },
  -             },
  -         ],
  -         'resolved': [
  -             'parent/clip:literal',
  -         ],
  -         'schema_version': 1,
  -         'select': 'parent/clip:literal',
  -         'selections': [],
  -         'version': '1',
  -     },
  - ])
```

IDs:
- `tests/editing_conformance/test_cli_trim_runtime.py::test_cli_trim_exact_retry_restart_dependent_suffix_and_peer[relevant-conflict]`

### Failure × 1

```text
AssertionError: assert [{'args': {'c...': None, ...}] == [{'args': {'c...': None, ...}]
  
  At index 5 diff: {'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None, 'args': {'changes': [{'op': 'set', 'ref': 'parent', 'path': ['config', 'tracks', 'id:picture', 'label'], 'before': {'state': 'present', 'value': 'Old'}, 'value': ''}]}} != {'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None, 'args': {'changes': [{'op': 'set', 'ref': 'parent', 'path': ['config', 'app'], 'before': {'state': 'absent'}, 'value': {}}, {'op': 'set', 'ref': 'parent', 'path': ['config', 'tracks', 'id:picture', 'label'], 'before': {'state': 'present', 'value': 'Old'}, 'value': ''}]}}
  
  Full diff:
    [
        {
            'args': {
                'changes': [
                    {
                        'before': {
                            'state': 'absent',
                        },
                        'op': 'set',
                        'path': [
                            'clips',
                            'id:title',
                            'app',
                        ],
                        'ref': 'parent',
                        'value': {
                            'astrid': {
                                'fixed_start': True,
                                'for': 2.013,
                            },
                        },
                    },
                ],
            },
            'op': 'doc.patch',
            'schema_version': 1,
            'select': None,
            'version': '1',
        },
        {
            'args': {
                'changes': [
                    {
                        'before': {
                            'state': 'present',
                            'value': 0.017,
                        },
                        'op': 'set',
                        'path': [
                            'clips',
                            'id:title',
                            'at',
                        ],
                        'ref': 'parent',
                        'value': 3.033333333333333,
                    },
                ],
            },
            'op': 'doc.patch',
            'schema_version': 1,
            'select': None,
            'version': '1',
        },
        {
            'args': {
                'changes': [
                    {
                        'before': {
                            'state': 'present',
                            'value': 1.013,
                        },
                        'op': 'set',
                        'path': [
                            'clips',
                            'id:title',
                            'hold',
                        ],
                        'ref': 'parent',
                        'value': 2.013,
                    },
                ],
            },
            'op': 'doc.patch',
            'schema_version': 1,
            'select': None,
            'version': '1',
        },
        {
            'args': {
                'changes': [
                    {
                        'before': {
                            'state': 'present',
                            'value': 'Original',
                        },
                        'op': 'set',
                        'path': [
                            'clips',
                            'id:title',
                            'params',
                            'text',
                        ],
                        'ref': 'parent',
                        'value': '',
                    },
                ],
            },
            'op': 'doc.patch',
            'schema_version': 1,
            'select': None,
            'version': '1',
        },
        {
            'args': {
                'changes': [
                    {
                        'before': {
                            'state': 'present',
                            'value': {
                                'duration': 0.25,
                                'type': 'crossfade',
                            },
                        },
                        'op': 'remove',
                        'path': [
                            'clips',
                            'id:title',
                            'transition',
                        ],
                        'ref': 'parent',
                    },
                ],
            },
            'op': 'doc.patch',
            'schema_version': 1,
            'select': None,
            'version': '1',
        },
        {
            'args': {
                'changes': [
                    {
                        'before': {
  -                         'state': 'absent',
  -                     },
  -                     'op': 'set',
  -                     'path': [
  -                         'config',
  -                         'app',
  -                     ],
  -                     'ref': 'parent',
  -                     'value': {},
  -                 },
  -                 {
  -                     'before': {
                            'state': 'present',
                            'value': 'Old',
                        },
                        'op': 'set',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'label',
                        ],
                        'ref': 'parent',
                        'value': '',
                    },
                ],
            },
            'op': 'doc.patch',
            'schema_version': 1,
            'select': None,
            'version': '1',
        },
    ]
```

IDs:
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo[cli]`

### Failure × 1

```text
AssertionError: assert {'duration': ... 'video', ...} == {'generationI...1c24bcbfe169'}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'duration': 6}
  
  Full diff:
    {
  +     'duration': 6,
        'generationId': 'generation-251623084f8bf8ecb8164a3ac13874c2d2558a1f6cd94a00e5a0405fc340b5d7',
        'media_id': 'sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437',
        'type': 'video',
        'variantId': 'variant-6008a1c4781214c5cdf4dd6e25595dc14dfa6ebb11d53cb92ba21c24bcbfe169',
    }
```

IDs:
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_ordinary_birth_or_ordered_replacement_accept_reload_inverse_redo_retry[video-False]`

### Failure × 1

```text
AssertionError: assert {'duration': ... 'video', ...} == {'generationI...73294c7896cc'}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'duration': 6}
  
  Full diff:
    {
  +     'duration': 6,
        'generationId': 'generation-bbfe9dd5d595aa76ad4fb40c5386881ef493e4fe251687971c4882683d4d4021',
        'media_id': 'sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437',
        'type': 'video',
        'variantId': 'variant-fd561dac5db57c5b1cf1c1d5a27559de93baa32e5ec8860fad3473294c7896cc',
    }
```

IDs:
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_fresh_film_first_media_birth_and_exact_inverse[video]`

### Failure × 1

```text
AssertionError: assert {'duration': ... 'video', ...} == {'generationI...a2f21bd4b321'}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'duration': 6}
  
  Full diff:
    {
  +     'duration': 6,
        'generationId': 'generation-3c52b191d1cfb756c2eb938de20ca888acf38721a09df2c6537925e6323ffecd',
        'media_id': 'sha256:cba06b5736faf67e54b07b561eae94395e774c517a7d910a54369e1263ccfbd4',
        'type': 'video',
        'variantId': 'variant-638cd885ef1db2e4ec9adfa1793219824eb9df0ed9dcfa453e7aa2f21bd4b321',
    }
```

IDs:
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_exact_old_source_tuple_survives_new_primary_variant_and_replacement_inverse[video]`

### Failure × 1

```text
AssertionError: assert {'duration': ... 'video', ...} == {'generationI...de62b2e3426b'}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'duration': 6}
  
  Full diff:
    {
  +     'duration': 6,
        'generationId': 'generation-0bb6469505c3354d7d21fca56e63559cfdc7af8eac5cd244d96a8540912a7974',
        'media_id': 'sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437',
        'type': 'video',
        'variantId': 'variant-567f4909ec70faa8491cf160ba7e1265c0930ee8e743b5237e7fde62b2e3426b',
    }
```

IDs:
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_ordinary_birth_or_ordered_replacement_accept_reload_inverse_redo_retry[video-True]`

### Failure × 1

```text
AttributeError: 'types.SimpleNamespace' object has no attribute 'receipt'
```

IDs:
- `tests/editing_conformance/test_commit_runtime_source_copy.py::test_production_duplicate_caller_uses_authenticated_semantic_and_archives_failures`

### Failure × 1

```text
Failed: DID NOT RAISE <class 'astrid.sdk.timeline._common.TimelineEditError'>
```

IDs:
- `tests/editing_conformance/test_native_batch_ingress.py::test_batch_capture_never_refreshes_after_concurrent_ack`

### Failure × 1

```text
TypeError: 'NoneType' object is not subscriptable
```

IDs:
- `tests/core/test_timeline_element_publication_runtime.py::test_acknowledged_rebased_lost_ack_restart_pagination_and_typed_intent`

### Failure × 1

```text
assert 'accepted revision' in 'Committed "Add media" as txn-8dab2a8d053d42beb8f5727e2cd7ef94. Media: 1 file(s) in the catalog; undo keeps them.\nastrid timelines show film --project 199ec844484940a78f86339bd3848b40 --published --revision-id authoring-parent-revision-9ea9285fe32b10f4c293c146294a2887529ebb5057498a192edbc3c6ccbc9216\n'
 +  where 'Committed "Add media" as txn-8dab2a8d053d42beb8f5727e2cd7ef94. Media: 1 file(s) in the catalog; undo keeps them.\nastrid timelines show film --project 199ec844484940a78f86339bd3848b40 --published --revision-id authoring-parent-revision-9ea9285fe32b10f4c293c146294a2887529ebb5057498a192edbc3c6ccbc9216\n' = CaptureResult(out='Committed "Add media" as txn-8dab2a8d053d42beb8f5727e2cd7ef94. Media: 1 file(s) in the catalog; undo keeps them.\nastrid timelines show film --project 199ec844484940a78f86339bd3848b40 --published --revision-id authoring-parent-revision-9ea9285fe32b10f4c293c146294a2887529ebb5057498a192edbc3c6ccbc9216\n', err='').out
 +    where CaptureResult(out='Committed "Add media" as txn-8dab2a8d053d42beb8f5727e2cd7ef94. Media: 1 file(s) in the catalog; undo keeps them.\nastrid timelines show film --project 199ec844484940a78f86339bd3848b40 --published --revision-id authoring-parent-revision-9ea9285fe32b10f4c293c146294a2887529ebb5057498a192edbc3c6ccbc9216\n', err='') = readouterr()
 +      where readouterr = <_pytest.capture.CaptureFixture object at 0x7bc57d0e9750>.readouterr
```

IDs:
- `tests/editing_conformance/test_cli_first_media.py::test_media_add_without_write_flags_and_reusing_a_managed_asset`

### Failure × 1

```text
assert 'immutable' in '{"data":null,"error":{"code":"timeline_edit_error","details":{},"message":"idempotency key belongs to another edit; use a fresh key for new intent; edited sheet kept at /tmp/pytest-of-runner/pytest-0/test_http_sheet_lost_ack_resta0/sheet.txt"},"idempotency_key":"changed","ok":false,"receipt":null}\n'
 +  where '{"data":null,"error":{"code":"timeline_edit_error","details":{},"message":"idempotency key belongs to another edit; use a fresh key for new intent; edited sheet kept at /tmp/pytest-of-runner/pytest-0/test_http_sheet_lost_ack_resta0/sheet.txt"},"idempotency_key":"changed","ok":false,"receipt":null}\n' = CaptureResult(out='{"data":null,"error":{"code":"timeline_edit_error","details":{},"message":"idempotency key belongs to another edit; use a fresh key for new intent; edited sheet kept at /tmp/pytest-of-runner/pytest-0/test_http_sheet_lost_ack_resta0/sheet.txt"},"idempotency_key":"changed","ok":false,"receipt":null}\n', err='').out
 +    where CaptureResult(out='{"data":null,"error":{"code":"timeline_edit_error","details":{},"message":"idempotency key belongs to another edit; use a fresh key for new intent; edited sheet kept at /tmp/pytest-of-runner/pytest-0/test_http_sheet_lost_ack_resta0/sheet.txt"},"idempotency_key":"changed","ok":false,"receipt":null}\n', err='') = readouterr()
 +      where readouterr = <_pytest.capture.CaptureFixture object at 0x7bc57bb965d0>.readouterr
```

IDs:
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba`

### Failure × 1

```text
assert (None)
```

IDs:
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_detached_duration_author_time_basis_through_original_save_and_runtime[same-detached-historical]`

### Failure × 1

```text
assert (not False and 'timeline_outcome_unknown' == 'forbidden'
 +  where False = DomainResult(ok=False, data=None, error=ErrorObject(code='timeline_outcome_unknown', message='No reply could be verified; this edit may or may not have been committed. Call tl.commit(key="helper-denied") again with no other arguments to confirm the saved request.', details={'headline': 'No reply could be verified; this edit may or may not have been committed', 'detail': 'The exact request is saved. No new request will be sent until it is confirmed.', 'fix': 'Call tl.commit(key="helper-denied") again with no other arguments to confirm the saved request.', 'outcome': 'unknown', 'cause': {'code': 'forbidden', 'message': 'Element commit denied', 'details': {'reason': 'helper_authorization'}}}), receipt=None, idempotency_key='helper-denied').ok
  
  - forbidden
  + timeline_outcome_unknown)
```

IDs:
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_native_refusal_preserves_error_and_flight`

### Failure × 1

```text
assert False
 +  where False = all(<generator object test_file_parser_requires_both_original_pins_and_describes_registry.<locals>.<genexpr> at 0x7bc56b87e5e0>)
```

IDs:
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_parser_requires_both_original_pins_and_describes_registry`

### Failure × 1

```text
astrid.sdk.timeline.sync.CommitRefused: The Runtime declined this edit; nothing was committed. inverse stage native writes do not cover its authenticated effect image. Inspect the saved edit with tl.pending_show("pc_fef4e7f90c05"), fix the edit, then retry or drop it.
```

IDs:
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_mixed_text_duration_uses_one_native_http_batch_and_guarded_inverse[detached-historical]`

### Failure × 1

```text
failed on setup with "runtime_protocol.errors.RuntimeErrorBase: closure membership and edges require semantic commands"
```

IDs:
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_gate3_reload_undo_and_visualize_report_unavailable`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: candidate.shots['shot'].internal_timeline.clips['voice']: timeline interval must fit the occurrence's half-open bounds
```

IDs:
- `tests/editing_conformance/test_native_word_anchor.py::test_occurrence_window_is_rechecked_for_source_move_stale_replay_and_inverse`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage native writes do not cover its authenticated effect image
```

IDs:
- `tests/editing_conformance/test_commit_runtime_occurrence_fork.py::test_registered_fork_normal_wire_accept_edit_and_guarded_undo`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage source materialization owner is malformed
```

IDs:
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_sibling_edit[original-third]`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage timeline effects differ from authenticated source history
```

IDs:
- `tests/editing_conformance/test_native_word_anchor.py::test_last_write_clear_undo_restore_and_restore_inverse`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: moved-head staged physical input requires private sequential proof
```

IDs:
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_retained_v1_after_v2_clear_restart_group_inverse_is_exact`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: selected PARAM authority is unavailable
```

IDs:
- `tests/core/test_timeline_element_publication_runtime.py::test_native_element_update_reload_guarded_inverse_and_exact_retry[False]`

## Exact G1 reconciliation

Only exact testcase IDs count as recurrences. Parameter-family similarities are separate and not counted. G1 contains red IDs only, so unmatched current red IDs are not automatically new or previously passing.

Prior red IDs: 250; current red IDs with exact prior G1 ID: 250; current red IDs absent from prior red inventory: 0. Transitions: `{"error_persists_same_status": 172, "failed_persists_same_status": 78}`.

| Prior G1 status | Current status | Count |
|---|---|---:|
| ERROR | ERROR | 172 |
| FAILED | FAILED | 78 |

## Per-ID triage and Plan 38/55


- `tests/core/test_timeline_element_publication_runtime.py::test_native_element_update_reload_guarded_inverse_and_exact_retry[False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/core/test_timeline_element_publication_runtime.py::test_public_helper_native_refusal_preserves_error_and_flight` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/core/test_timeline_element_publication_runtime.py::test_preexisting_element_hold_flight_retries_exact_body` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/core/test_timeline_element_publication_runtime.py::test_acknowledged_rebased_lost_ack_restart_pagination_and_typed_intent` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/core/test_timeline_element_publication_runtime.py::test_attached_selected_param_p1_survives_lost_ack_restart_and_undo` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_authenticated_source_baseline_restores_exact_legacy_bytes[inverse]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_authenticated_source_baseline_restores_exact_legacy_bytes[step-inverse]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_authenticated_source_baseline_restores_exact_legacy_bytes[restore]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_inverse_preserves_unrelated_parent_move[False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_inverse_preserves_unrelated_parent_move[True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[new]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[modified]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[equal-authored]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[forged-source]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[forged-publication]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[forged-step]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[digest]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[foreign]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[aba]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[membership]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_invalid_or_unauthenticated_restoration_refuses_without_writes[order]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[changed]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[alias]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[shot-owner]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[internal-owner]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[target]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[target-remove]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[documents]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[outside]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[no-writes]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[ordinary-write]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_authenticated_legacy_restore.py::test_restoration_source_unit_keeps_exact_reference_and_write_guards[until-flag]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_cli_first_media.py::test_media_add_without_write_flags_and_reusing_a_managed_asset` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_cli_trim_runtime.py::test_cli_trim_exact_retry_restart_dependent_suffix_and_peer[relevant-conflict]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py::test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[scalar]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py::test_app_hold_asset_transition_commit_reload_inverse_redo_and_aba[compound]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_identity.py::test_occupied_shared_occurrence_destination_refuses_atomically[same-project]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_identity.py::test_occupied_shared_occurrence_destination_refuses_atomically[other-project]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_occurrence_retry_own_move_and_historical_restore[fresh]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[disjoint-rebase-undo]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_cli_python_outbox_restart_and_guarded_inverse[touched-basis-conflict]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_lost_ack_restart_and_fresh_head` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_keyed_view_requires_write_but_inspection_remains_read_only` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-image]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[anchor-video]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-image]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[fallback-video]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-image]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[shared-video]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py::test_real_media_manifest_inverse_retry_restart_and_history[add]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py::test_real_media_manifest_inverse_retry_restart_and_history[swap]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_param_commands_keep_exact_cli_ingress_and_unchanged_write_history` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_frontends.py::test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_frontends.py::test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_native_frontends.py::test_checkout_first_refuses_sheet_suffix_keeps_draft_and_pending_intent` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2.0-parent/clip:music-bed]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2.0-occurrence:occurrence-1/clip:clip-1]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[1-True-parent/clip:music-bed]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[True-1-parent/clip:music-bed]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2-parent/clip:music-bed]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[True-True-parent/clip:music-bed]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_fork.py::test_registered_fork_normal_wire_accept_edit_and_guarded_undo` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-swap]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[video-add]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[video-swap]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-stale-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-stale-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-foreign-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-foreign-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-fingerprint-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-add-fingerprint-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-stale-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-stale-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-foreign-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-foreign-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-fingerprint-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[image-swap-fingerprint-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-stale-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-stale-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-foreign-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-foreign-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-fingerprint-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-add-fingerprint-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-stale-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-stale-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-foreign-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-foreign-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-fingerprint-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_invalid_exact_selection_refuses_without_any_writes[video-swap-fingerprint-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[image-add]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[image-swap]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[video-add]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_source_metadata_is_part_of_the_exact_selection_fingerprint[video-swap]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-lifecycle-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-lifecycle-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-revocation-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-add-revocation-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-lifecycle-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-lifecycle-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-revocation-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[image-swap-revocation-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-lifecycle-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-lifecycle-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-revocation-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-add-revocation-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-lifecycle-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-lifecycle-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-revocation-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_capture_to_accept_races_refuse_atomically[video-swap-revocation-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse[item_id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse[id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_move_preserves_unknown_item_ids_retry_restart_and_inverse[both]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_inverse_restores_exact_original_closure[item_id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_inverse_restores_exact_original_closure[id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py::test_occurrence_inverse_restores_exact_original_closure[both]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-anchor]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-fallback]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[image-lane-end]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[video-anchor]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[video-fallback]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id[video-lane-end]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_fresh_film_first_media_birth_and_exact_inverse[video]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_ordinary_birth_or_ordered_replacement_accept_reload_inverse_redo_retry[video-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_ordinary_birth_or_ordered_replacement_accept_reload_inverse_redo_retry[video-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media.py::test_exact_old_source_tuple_survives_new_primary_variant_and_replacement_inverse[video]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo[image]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo[video]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_over_authenticated_http_preserves_flight_and_guarded_undo[parent]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_over_authenticated_http_preserves_flight_and_guarded_undo[occurrence:occ-a]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-stale-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-stale-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-foreign-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-foreign-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-fingerprint-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[image-fingerprint-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-stale-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-stale-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-foreign-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-foreign-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-fingerprint-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_invalid_selected_media_refuses_without_writes[video-fingerprint-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[image-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[image-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[video-old_media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_lifecycle_race_refuses_at_acceptance[video-media]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[image-disjoint]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[image-aba]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[video-disjoint]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_accepted_history_rebase_and_guarded_aba_undo[video-aba]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py::test_grouped_parent_track_create_move_reload_undo_redo` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_track_label.py::test_move_then_parent_label_reload_inverse_preserves_newer_disjoint_move` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_parent_track_label.py::test_native_label_cli_lost_ack_then_python_suffix_keeps_original_claims` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_scalar.py::test_move_then_scalar_outbox_handoff_reload_and_guarded_inverse` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization[original-third]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization[authored-first]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_parent_edit[original-third]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_parent_edit[authored-first]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_sibling_edit[original-third]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_preserves_newer_disjoint_sibling_edit[authored-first]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_inverse_refuses_touching_aba_atomically[authored-first]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_redo_refuses_intervening_aba_after_exact_undo[original-third]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_redo_refuses_intervening_aba_after_exact_undo[authored-first]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_source_copy.py::test_production_duplicate_caller_uses_authenticated_semantic_and_archives_failures` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_retains_v1_after_v2_restart_exact_inverse_and_redo` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_clear_removes_row_and_undo_restores_empty_exactly` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_retained_v1_after_v2_clear_restart_group_inverse_is_exact` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_retains_authenticated_pair_and_canonical_source` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_explicit_historical_read_does_not_acquire_current_publication` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_explicit_wrong_publication_refuses` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_reset_reads_reused_revision_under_new_publication` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_requires_exact_publication_history_entry[missing-entry]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_requires_exact_publication_history_entry[wrong-revision]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_requires_exact_publication_history_entry[wrong-receipt]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[missing-head]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[missing-publication]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[changed-head]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_fails_closed_without_head_proof[history-error]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[project_id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[timeline_id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[revision_id]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[content_digest]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_current_pair_reader.py::test_current_fetch_preserves_exact_scope_digest_and_owner_guards[internal-owner]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip[python]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip[cli]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip[sheet]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-4-two-step-clips-before]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-16-two-step-clips-after]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-28-two-step-config-clips-before]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-40-two-step-config-clips-after]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-49-native-whole]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_inverse_refuses_forged_source_publication_and_step_without_writes` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_inverse_refuses_native_write_and_aba_without_writes` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[disjoint-rebase-undo]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_m1_current_equivalent.py::test_new_ours_current_equivalent_preserves_m1_commit_journey[touched-basis-conflict]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_m1_legacy_archive_read.py::test_explicit_held_baseline_then_current_word_bound_read_is_closure_exact` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_file_parser_requires_both_original_pins_and_describes_registry` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_batch_ingress.py::test_batch_capture_never_refreshes_after_concurrent_ack` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo[disjoint-peer]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo[touching-peer-conflict]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_commands_file_preserves_opaque_unchanged_write_and_undo` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_gate3_reload_undo_and_visualize_report_unavailable` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_cut_owned_native_sheet_hold_reloads_and_undoes` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[python]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[cli]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends[sheet]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_attached_parent_label_publish_retries_exact_capture_and_inverse` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_original_attached_add_track_publish_retries_exact_capture_and_guarded_inverse` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[python]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[cli]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[sheet]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[python]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[cli]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[sheet]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo[cli]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[none-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[disjoint-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[trim-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict[params-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_detached_duration_author_time_basis_through_original_save_and_runtime[same-detached-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_mixed_text_duration_uses_one_native_http_batch_and_guarded_inverse[detached-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_size_clear_uses_one_native_http_commit_and_guarded_inverse[detached-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_font_color_uses_one_native_http_commit_and_guarded_inverse[detached-historical]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_word_anchor.py::test_occurrence_window_is_rechecked_for_source_move_stale_replay_and_inverse` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_word_anchor.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-False]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_word_anchor.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-True]` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/editing_conformance/test_native_word_anchor.py::test_last_write_clear_undo_restore_and_restore_inverse` — exact prior G1 red-ID recurrence. Prior triage: A-b/AT1 unclassified distinct cause. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
