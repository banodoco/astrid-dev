# Release 12: pre-existing installer test failures (118 ids)

[Plan 39](../inputs.md) · [Tasks](../tasks.md)

**Scope of this PR:** 118 pre-existing Agent installer failing test ids. This PR does not change Plan 39's tasks; its G1 re-measure picks this up. It does not block Release 12.

## Purpose

118 Agent installer tests fail on both the served release 11 baseline (`a105de3a4852cb61b9647dfe2c920118bd29f272`) and the release-12 candidate. They are pre-existing, not Release 12 regressions. They don't block Release 12. They are recorded here so none is lost.

## Source

- Run: worker run of the 119 installer node ids, on the Agent baseline `a105de3a` and the candidate `fix/r12-autostart`.
- Runner: `agent-pytest.sh -q --tb=no -rA`.
- Baseline `a105de3a`: **118 failed, 1 passed**.
- Candidate `fix/r12-autostart`: **119 failed**.
- The one id that passed on the baseline and fails on the candidate is the Release 12 regression. It is handled separately and is not in this record.

## Per-file count

| File | Count |
|---|---|
| `test_installer_busy_fence.py` | 59 |
| `test_installer_acl.py` | 12 |
| `test_installer_app_update.py` | 8 |
| `test_installer_platforms.py` | 6 |
| `test_installer_shim.py` | 4 |
| `test_installer_pinokio_lifecycle.py` | 4 |
| `test_installer_schema.py` | 3 |
| `test_installer_lifecycle.py` | 3 |
| `test_installer_transaction_authority.py` | 2 |
| `test_installer_service_repair_integration.py` | 2 |
| `test_installer_release0_rollback.py` | 2 |
| `test_installer_launcher_repair.py` | 2 |
| `test_installer_update_legacy_record.py` | 1 |
| `test_installer_startup_stop.py` | 1 |
| `test_installer_release0_service_adoption.py` | 1 |
| `test_installer_r0_entry.py` | 1 |
| `test_installer_local_update.py` | 1 |
| `test_installer_launchd_stop_handoff.py` | 1 |
| `test_installer_launchd_cache_window.py` | 1 |
| `test_installer_installed_schema.py` | 1 |
| `test_installer_bootstrap_schema.py` | 1 |
| `test_installer_bootstrap_imports.py` | 1 |
| `test_installer_backup.py` | 1 |
| **Total (23 files)** | **118** |

`test_installer_busy_fence.py` is the largest bucket at **59 ids**.

## Caveats

- Measured in a cloud worker, not CI. Some failures may be environment artefacts. Plan 39 G1 re-measures on CI.

## Failing ids (118)

Parametrised ids are listed as the run reports them, grouped by file.

<details><summary>118 failing installer ids, grouped by file</summary>

`test_installer_acl.py` (12)

- `test_installer_acl.py::test_unix_installer_retains_original_per_user_lock[darwin,linux]`
- `test_installer_acl.py::test_windows_installer_lock_stays_outside_program_and_workspace[False,True]`
- `test_installer_acl.py::test_windows_refuses_selected_roots_containing_installer_lock[bootstrap-data, bootstrap-root, child-data, child-root, parent-data, parent-root, state-data, state-root]`

`test_installer_app_update.py` (8)

- `test_installer_app_update.py::test_local_verification_rejects_mismatched_managed_version_identity[managed_by-discovery, managed_by-health, release-discovery, release-health]`
- `test_installer_app_update.py::test_local_verification_rejects_mismatched_transaction_binding`
- `test_installer_app_update.py::test_local_verification_rejects_missing_raw_managed_identity[None, owner_health1, owner_health2]`

`test_installer_backup.py` (1)

- `test_installer_backup.py::test_windows_failed_update_restores_private_support_and_can_retry`

`test_installer_bootstrap_imports.py` (1)

- `test_installer_bootstrap_imports.py::test_installer_has_no_lazy_third_party_imports`

`test_installer_bootstrap_schema.py` (1)

- `test_installer_bootstrap_schema.py::test_staged_canonical_schema_reaches_strict_consumer`

`test_installer_busy_fence.py` (59)

- `test_installer_busy_fence.py::test_busy_stop_path_matrix_has_no_manager_signal_or_cleanup` (54 ids: `{attempt, cancel, claimed, reservation, running, stale}` x `{recovery, repair, update}` x `{darwin, linux, win32}`)
- `test_installer_busy_fence.py::test_cli_busy_preflight_precedes_marker_and_selection_writes`
- `test_installer_busy_fence.py::test_cli_preflights_once_and_actual_stop_fences_staged_work[final-fence, none, staging]`
- `test_installer_busy_fence.py::test_cli_repair_and_uninstall_preflight_once_before_stop_admission[repair]`

`test_installer_installed_schema.py` (1)

- `test_installer_installed_schema.py::test_stage_binds_installed_reader_validator_and_service_to_verified_schema`

`test_installer_launchd_cache_window.py` (1)

- `test_installer_launchd_cache_window.py::test_published_plist_interruption_recovers_only_through_c1_stop`

`test_installer_launchd_stop_handoff.py` (1)

- `test_installer_launchd_stop_handoff.py::test_downstream_update_failure_runs_real_c1_rollback_and_keeps_old_selected[backup]`

`test_installer_launcher_repair.py` (2)

- `test_installer_launcher_repair.py::test_repair_restart_decision_preserves_or_replaces_real_processes[False,True]`

`test_installer_lifecycle.py` (3)

- `test_installer_lifecycle.py::test_real_c1_post_stop_failure_retries_fence_before_old_activation`
- `test_installer_lifecycle.py::test_repair_skips_down_for_proven_dead_runtime_and_keeps_discovery`
- `test_installer_lifecycle.py::test_stop_treats_discovery_removed_during_read_as_stopped`

`test_installer_local_update.py` (1)

- `test_installer_local_update.py::test_recovery_routing_refuses_local_journal_in_ordinary_paths`

`test_installer_pinokio_lifecycle.py` (4)

- `test_installer_pinokio_lifecycle.py::test_pinokio_doctor_without_root_follows_per_user_pointer`
- `test_installer_pinokio_lifecycle.py::test_reset_removed_pinokio_root_releases_pointer_for_terminal_install`
- `test_installer_pinokio_lifecycle.py::test_root_marker_retains_pinokio_manager_for_update_and_uninstall[mode1]`
- `test_installer_pinokio_lifecycle.py::test_second_pinokio_root_is_allowed_after_first_root_is_deleted`

`test_installer_platforms.py` (6)

- `test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-17391-17393-17393, None-17391-None-17391, None-None-None-17340, pinokio-17391-17393-17393, pinokio-17391-None-17391, pinokio-None-None-17340]`

`test_installer_r0_entry.py` (1)

- `test_installer_r0_entry.py::test_captures_match_real_r0_evidence`

`test_installer_release0_rollback.py` (2)

- `test_installer_release0_rollback.py::test_pre_stop_interruption_recovers_and_starts_authentic_release0_runtime`
- `test_installer_release0_rollback.py::test_rollback_selects_and_starts_authentic_release0_runtime`

`test_installer_release0_service_adoption.py` (1)

- `test_installer_release0_service_adoption.py::test_release0_posix_service_is_adopted_and_freshly_registered[darwin]`

`test_installer_schema.py` (3)

- `test_installer_schema.py::test_optional_remotion_failure_does_not_block_staging[browser, npm]`
- `test_installer_schema.py::test_staging_verifies_the_local_schema_before_declaring_services`

`test_installer_service_repair_integration.py` (2)

- `test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0, True-1]`

`test_installer_shim.py` (4)

- `test_installer_shim.py::test_verified_lifecycle_records_shim_and_prints_final_hint[darwin-update, linux-update, win32-install, win32-update]`

`test_installer_startup_stop.py` (1)

- `test_installer_startup_stop.py::test_manager_failure_after_owner_removes_advertisements_allows_installer_recovery`

`test_installer_transaction_authority.py` (2)

- `test_installer_transaction_authority.py::test_cli_recovers_completed_stop_with_fresh_controller[stop-return-app, stopped-app]`

`test_installer_update_legacy_record.py` (1)

- `test_installer_update_legacy_record.py::test_sweep_resolves_a_record_without_home_once_its_unit_has_finished`

</details>
