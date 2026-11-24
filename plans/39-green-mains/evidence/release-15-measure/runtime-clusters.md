# Failure clusters

1469 failing IDs in 59 clusters (grouped by exception type and raise site).

| # | IDs | Raise site | Top message | Top files |
| --- | ---: | --- | --- | --- |
| C1 | 696 | `ConflictError at runtime_protocol/v33_lifecycle.py:300` | runtime_protocol.errors.ConflictError: vN provider/baseline verification is pending; requests and fresh pins a | `tests/test_timeline_effect_authority.py` (318), `tests/test_timeline_document_authority.py` (186) |
| C2 | 378 | `ConflictError at runtime_protocol/daemon.py:320` | runtime_protocol.errors.ConflictError: migrated realm requires fresh Timeline provider registration before rea | `tests/test_timeline_effect_authority.py` (318), `tests/test_timeline_authority_door.py` (36) |
| C3 | 84 | `AssertionError at tests/test_timeline_inverse_sequential_authority.py:30` | AssertionError: assert [{'blendMode'...'audio', ...}] == [] | `tests/test_timeline_inverse_sequential_authority.py` (84) |
| C4 | 60 | `ModuleNotFoundError at tests/test_timeline_render_publication.py:187` | ModuleNotFoundError: No module named 'astrid.packs.video_editing' | `tests/test_timeline_render_publication_authority.py` (51), `tests/test_timeline_render_publication.py` (9) |
| C5 | 36 | `ElementPackNotInstalled at ../astrid-agent/astrid/sdk/timeline_address.py:520` | astrid.sdk.timeline_address.ElementPackNotInstalled: [element_pack_not_installed] image: no installed pack dec | `tests/test_timeline_native_asset_union.py` (36) |
| C6 | 30 | `CommandError at ../astrid-agent/astrid/sdk/timeline/_recording.py:175` | astrid.sdk.timeline._command_state.CommandError: created identity is occupied | `tests/test_timeline_commit_sequential_verifier.py` (30) |
| C7 | 24 | `AssertionError at tests/test_timeline_forward_created_authority.py:82` | AssertionError: assert [{'blendMode'...None, False]}] == [{'id': 'stab...None, False]}] | `tests/test_timeline_forward_created_authority.py` (24) |
| C8 | 12 | `CustodyError at astrid_runtime/custody_broker.py:1864` | astrid_runtime.custody_broker.CustodyError: Linux pidfd custody is unavailable | `tests/test_real_bootstrap.py` (8), `tests/test_linux_runtime_boundary_native.py` (4) |
| C9 | 9 | `ConflictError at runtime_protocol/backup.py:481` | runtime_protocol.errors.ConflictError: realm failed integrity checks | `tests/test_direct_render_admission.py` (6), `tests/test_restore_history_fixture.py` (3) |
| C10 | 9 | `AssertionError at tests/test_precut_variants.py:117` | assert False | `tests/test_precut_variants.py` (9) |
| C11 | 6 | `AttributeError at runtime_protocol/daemon.py:183` | AttributeError: 'NoneType' object has no attribute 'store' | `tests/test_production_worker_credentials_luna.py` (6) |
| C12 | 6 | `ValidationError at runtime_protocol/store.py:4619` | runtime_protocol.errors.ValidationError: unsupported settlement effect_type | `tests/test_root_generation_query.py` (6) |
| C13 | 6 | `RuntimeErrorBase at runtime_protocol/service.py:3421` | runtime_protocol.timeline_commit.CommitRejected: revision content digest mismatch | `tests/test_shot_composition_runtime.py` (3), `tests/test_timeline_recorder_abi_authority.py` (3) |
| C14 | 6 | `CommitOutcomeUnknown at runtime_protocol/timeline_commit_execution.py:498` | sqliteN.DatabaseError: not authorized | `tests/test_timeline_commit_acceptance.py` (6) |
| C15 | 6 | `AssertionError at tests/test_portable_lifecycle.py:455` | AssertionError: foreground Runtime exited N: { | `tests/test_portable_lifecycle.py` (4), `tests/test_profile_services.py` (2) |
| C16 | 5 | `no traceback | ` |  | `tests/test_bootstrap.py` (5) |
| C17 | 3 | `AssertionError at tests/test_diagnostics.py:110` | AssertionError: assert 'Last update result: Updated to release N.' in 'Astrid diagnostics: OK. Installed: unkn | `tests/test_diagnostics.py` (3) |
| C18 | 3 | `AssertionError at tests/test_diagnostics.py:211` | AssertionError: assert 'Last update result: rolled_back' in 'Astrid diagnostics: NOT OK. Installed: unknown. L | `tests/test_diagnostics.py` (3) |
| C19 | 3 | `Failed at tests/test_imported_media_catalog.py:227` | Failed: DID NOT RAISE ConflictError | `tests/test_imported_media_catalog.py` (3) |
| C20 | 3 | `AssertionError at tests/test_precut_realm_fixture.py:97` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/test_precut_realm_fixture.py` (3) |
| C21 | 3 | `AssertionError at tests/test_operator_lifecycle_sol_closures.py:208` | AssertionError: assert None == {'safe': False, 'headline': 'Astrid is busy (N tasks running). Try again when t | `tests/test_operator_lifecycle_sol_closures.py` (3) |
| C22 | 3 | `AssertionError at tests/test_p2_commit_phase_capture.py:63` | AssertionError: assert False | `tests/test_p2_commit_phase_capture.py` (3) |
| C23 | 3 | `AssertionError at tests/test_rename_semantics.py:22` | AssertionError: assert {'astrid_runt...col/store.py'} == {'astrid_runt...col/store.py'} | `tests/test_rename_semantics.py` (3) |
| C24 | 3 | `AssertionError at tests/test_shot_layering_fixture.py:97` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/test_shot_layering_fixture.py` (3) |
| C25 | 3 | `AssertionError at tests/test_skip_policy.py:264` | AssertionError: mark the test with an entry from tests/lanes.py instead of skipping by hand: tests/test_deadli | `tests/test_skip_policy.py` (3) |
| C26 | 3 | `AssertionError at tests/test_spec_dedup.py:57` | AssertionError: assert N == N | `tests/test_spec_dedup.py` (3) |
| C27 | 3 | `ValidationError at runtime_protocol/v33_manifest.py:111` | runtime_protocol.errors.ValidationError: unsupported canonical vN manifest | `tests/test_spec_reference.py` (3) |
| C28 | 3 | `RetiredRouteError at runtime_protocol/service.py:467` | runtime_protocol.errors.RetiredRouteError: legacy timeline writes are retired; submit EditCommands through com | `tests/test_spec_reference.py` (3) |
| C29 | 3 | `AssertionError at tests/test_timeline_commit_acceptance.py:847` | assert N == N | `tests/test_timeline_commit_acceptance.py` (3) |
| C30 | 3 | `AssertionError at tests/test_timeline_commit_acceptance.py:866` | assert N == N | `tests/test_timeline_commit_acceptance.py` (3) |
| C31 | 3 | `AttributeError at runtime_protocol/timeline_commit_store.py:375` | AttributeError: 'types.SimpleNamespace' object has no attribute 'db_path' | `tests/test_timeline_commit_sequential_verifier.py` (3) |
| C32 | 3 | `AssertionError at tests/test_timeline_forward_created_authority.py:124` | AssertionError: assert [{'blendMode'...'audio', ...}] == [] | `tests/test_timeline_forward_created_authority.py` (3) |
| C33 | 3 | `ConflictError at runtime_protocol/store.py:6110` | runtime_protocol.errors.ConflictError: managed output association conflicts with existing immutable output | `tests/test_timeline_producer_checkpoint.py` (3) |
| C34 | 3 | `AssertionError at tests/test_timeline_legacy_authority.py:476` | AssertionError: assert [{'blendMode'...d': 'visual'}] == [{'id': 'vide...d': 'visual'}] | `tests/test_timeline_legacy_authority.py` (3) |
| C35 | 3 | `AssertionError at tests/test_timeline_legacy_authority.py:522` | AssertionError: assert [{'blendMode'...nd': 'audio'}] == [{'id': 'audi...nd': 'audio'}] | `tests/test_timeline_legacy_authority.py` (3) |
| C36 | 3 | `AssertionError at tests/test_timeline_recorder_abi_authority.py:216` | assert False | `tests/test_timeline_recorder_abi_authority.py` (3) |
| C37 | 3 | `AssertionError at tests/test_timeline_recorder_abi_authority.py:233` | assert N == N | `tests/test_timeline_recorder_abi_authority.py` (3) |
| C38 | 3 | `ConflictError at runtime_protocol/cas.py:217` | runtime_protocol.errors.ConflictError: CAS object failed hash verification | `tests/test_timeline_text_legacy_custody.py` (3) |
| C39 | 3 | `Failed at tests/test_timeline_verified_media.py:98` | Failed: a metadata read must not request mutation admission | `tests/test_timeline_verified_media.py` (3) |
| C40 | 2 | `no traceback | [XPASS(strict)] [declared-xfail:synthetic-gap] known error` | [XPASS(strict)] [declared-xfail:synthetic-gap] known error | `check_it.py` (2) |
| C41 | 2 | `PermissionError at runtime_protocol/platform.py:896` | PermissionError: [Errno N] Operation not permitted | `tests/test_profile_services.py` (2) |
| C42 | 2 | `AssertionError at tests/test_v33_protected_acceptance.py:627` | AssertionError: RN daemon did not report startup | `tests/test_v33_protected_acceptance.py` (2) |
| C43 | 2 | `AssertionError at tests/test_profile_services.py:887` | AssertionError: { | `tests/test_profile_services.py` (2) |
| C44 | 2 | `AssertionError at tests/test_portable_lifecycle.py:409` | AssertionError: b'{"code": "conflict", "details": {"reason": "selection-or-inputs-invalid"}, "message": "The s | `tests/test_portable_lifecycle.py` (2) |
| C45 | 2 | `AssertionError at tests/test_portable_lifecycle.py:638` | AssertionError: { | `tests/test_portable_lifecycle.py` (2) |
| C46 | 2 | `AssertionError at tests/test_portable_lifecycle.py:684` | assert 'N' in "runtime daemon exited during startup: no module named 'astrid' (see <path> | `tests/test_portable_lifecycle.py` (2) |
| C47 | 1 | `no traceback | astrid_runtime.bootstrap.BootstrapError: Runtime interruption refused: owner endpoint or p` | astrid_runtime.bootstrap.BootstrapError: Runtime interruption refused: owner endpoint or process identity fail | `tests/test_bootstrap.py` (1) |
| C48 | 1 | `no traceback | AssertionError: "reused process identity changed" does not match "Runtime interruption ref` | AssertionError: "reused process identity changed" does not match "Runtime interruption refused: owner endpoint | `tests/test_bootstrap.py` (1) |
| C49 | 1 | `no traceback | AssertionError: "manager failed" does not match "Runtime interruption refused: owner endpo` | AssertionError: "manager failed" does not match "Runtime interruption refused: owner endpoint or process ident | `tests/test_bootstrap.py` (1) |
| C50 | 1 | `no traceback | astrid_runtime.bootstrap.DuplicateOwnerError: A different runtime owner is active for the ` | astrid_runtime.bootstrap.DuplicateOwnerError: A different runtime owner is active for the selected realm; stop | `tests/test_bootstrap.py` (1) |
| C51 | 1 | `no traceback | astrid_runtime.bootstrap.DuplicateOwnerError: Runtime discovery recovery refused: live own` | astrid_runtime.bootstrap.DuplicateOwnerError: Runtime discovery recovery refused: live owner identity is unver | `tests/test_bootstrap.py` (1) |
| C52 | 1 | `AssertionError at tests/test_v33_protected_acceptance.py:653` | assert N == N | `tests/test_v33_protected_acceptance.py` (1) |
| C53 | 1 | `no traceback | [XPASS(strict)] [declared-xfail:synthetic-gap]...` | [XPASS(strict)] [declared-xfail:synthetic-gap]... | `check_it.py` (1) |
| C54 | 1 | `AssertionError at tests/test_fail_closed_g28.py:61` | AssertionError: assert 'failed' == 'queued' | `tests/test_fail_closed_g28.py` (1) |
| C55 | 1 | `OSError at runtime_protocol/platform.py:1182` | OSError: [Errno N] Function not implemented | `tests/test_linux_listener.py` (1) |
| C56 | 1 | `TimeoutExpired at /usr/local/lib/python3.11/subprocess.py:1253` | subprocess.TimeoutExpired: Command '['<path> '<path> 'owner-loss']' timed out after N seconds | `tests/test_linux_listener.py` (1) |
| C57 | 1 | `CustodyError at astrid_runtime/custody_broker.py:1041` | astrid_runtime.custody_broker.CustodyError: Darwin audit-token custody is unavailable | `tests/test_prepared_owner_authenticated_cleanup.py` (1) |
| C58 | 1 | `AssertionError at tests/test_process_control.py:357` | AssertionError: assert 'denied' == 'allowed' | `tests/test_process_control.py` (1) |
| C59 | 1 | `AssertionError at tests/test_process_control.py:376` | AssertionError: assert 'PID namespaces' in 'Runtime cannot stop processes safely here (pidfd: enosys, process- | `tests/test_process_control.py` (1) |

## Failing IDs by test file

| IDs | Clusters | File |
| ---: | ---: | --- |
| 636 | 2 | `tests/test_timeline_effect_authority.py` |
| 186 | 1 | `tests/test_timeline_document_authority.py` |
| 114 | 1 | `tests/test_timeline_reference_authority.py` |
| 84 | 1 | `tests/test_timeline_inverse_sequential_authority.py` |
| 51 | 1 | `tests/test_timeline_render_publication_authority.py` |
| 39 | 1 | `tests/test_project_reference_catalog.py` |
| 36 | 1 | `tests/test_timeline_authority_door.py` |
| 36 | 1 | `tests/test_timeline_native_asset_union.py` |
| 33 | 2 | `tests/test_timeline_commit_sequential_verifier.py` |
| 27 | 2 | `tests/test_timeline_forward_created_authority.py` |
| 24 | 1 | `tests/test_realm_admission_hardening.py` |
| 15 | 2 | `tests/test_timeline_shot_authority.py` |
| 12 | 2 | `tests/test_precut_variants.py` |
| 12 | 3 | `tests/test_shot_composition_runtime.py` |
| 12 | 3 | `tests/test_timeline_commit_acceptance.py` |
| 10 | 6 | `tests/test_bootstrap.py` |
| 10 | 4 | `tests/test_portable_lifecycle.py` |
| 9 | 3 | `tests/test_timeline_recorder_abi_authority.py` |
| 9 | 1 | `tests/test_timeline_render_publication.py` |
| 8 | 1 | `tests/test_real_bootstrap.py` |
| 6 | 2 | `tests/test_diagnostics.py` |
| 6 | 1 | `tests/test_direct_render_admission.py` |
| 6 | 1 | `tests/test_production_worker_credentials_luna.py` |
| 6 | 1 | `tests/test_root_generation_query.py` |
| 6 | 2 | `tests/test_spec_reference.py` |
| 6 | 2 | `tests/test_timeline_legacy_authority.py` |
| 6 | 3 | `tests/test_profile_services.py` |
| 4 | 1 | `tests/test_linux_runtime_boundary_native.py` |
| 3 | 2 | `check_it.py` |
| 3 | 1 | `tests/test_streaming_media_io.py` |
| 3 | 1 | `tests/test_timeline_visibility_generated_http.py` |
| 3 | 1 | `tests/test_imported_media_catalog.py` |
| 3 | 1 | `tests/test_precut_realm_fixture.py` |
| 3 | 1 | `tests/test_operator_lifecycle_sol_closures.py` |
| 3 | 1 | `tests/test_p2_commit_phase_capture.py` |
| 3 | 1 | `tests/test_rename_semantics.py` |
| 3 | 1 | `tests/test_restore_history_fixture.py` |
| 3 | 1 | `tests/test_shot_layering_fixture.py` |
| 3 | 1 | `tests/test_skip_policy.py` |
| 3 | 1 | `tests/test_spec_dedup.py` |
| 3 | 1 | `tests/test_timeline_cutover.py` |
| 3 | 1 | `tests/test_timeline_producer_checkpoint.py` |
| 3 | 1 | `tests/test_timeline_reads_after_cut.py` |
| 3 | 1 | `tests/test_timeline_text_legacy_custody.py` |
| 3 | 1 | `tests/test_timeline_verified_media.py` |
| 3 | 2 | `tests/test_v33_protected_acceptance.py` |
| 2 | 2 | `tests/test_linux_listener.py` |
| 2 | 2 | `tests/test_process_control.py` |
| 1 | 1 | `tests/test_fail_closed_g28.py` |
| 1 | 1 | `tests/test_prepared_owner_authenticated_cleanup.py` |
