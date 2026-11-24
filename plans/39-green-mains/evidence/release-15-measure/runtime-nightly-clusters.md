# Failure clusters

152 failing IDs in 50 clusters (grouped by exception type and raise site).

| # | IDs | Raise site | Top message | Top files |
| --- | ---: | --- | --- | --- |
| C1 | 21 | `AssertionError at tests/test_timeline_commit_crash.py:78` | assert N == N | `tests/test_timeline_commit_crash.py` (21) |
| C2 | 20 | `RuntimeError at tests/test_snapshot_legacy_certification.py:37` | subprocess.CalledProcessError: Command '['git', '-C', '<path> 'archive', '<hash>', 'astrid', 'astrid_runtime_c | `tests/test_snapshot_legacy_certification.py` (20) |
| C3 | 15 | `Failed at tests/test_timeline_history_assembly.py:300` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_history_assembly.py` (15) |
| C4 | 7 | `RuntimeErrorBase at runtime_protocol/service.py:3282` | astrid.sdk.timeline.compiler.TimingCompileError: legacy word anchor is missing | `tests/test_timeline_commit_restore_integration.py` (3), `tests/test_timeline_commit_input_integration.py` (2) |
| C5 | 6 | `RuntimeError at runtime_protocol/platform.py:1226` | RuntimeError: process control is already strict; refusing to change it to sandbox | `tests/test_runtime_boundary.py` (5), `tests/test_astrid_product_down.py` (1) |
| C6 | 6 | `Failed at tests/test_timeline_history_assembly.py:359` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_history_assembly.py` (6) |
| C7 | 5 | `ConflictError at runtime_protocol/v33_lifecycle.py:300` | runtime_protocol.errors.ConflictError: vN provider/baseline verification is pending; requests and fresh pins a | `tests/test_timeline_commit_crash.py` (3), `tests/test_timeline_public_s2_mixed_cli_journey.py` (1) |
| C8 | 4 | `AssertionError at tests/test_capture_candidate_binding.py:360` | AssertionError: assert {'authority':...N], ...}, ...} == {'ref': {'dig...dNcN'}}} | `tests/test_capture_candidate_binding.py` (4) |
| C9 | 4 | `SourceIdentityError at runtime_protocol/source_identity.py:141` | runtime_protocol.source_identity.SourceIdentityError: untracked source directory is unsupported: <path> | `tests/test_runtime_nine_track_wal_reopen.py` (3), `tests/test_foreground_authoring_integration.py` (1) |
| C10 | 4 | `AssertionError at tests/test_render_historical_admission.py:357` | AssertionError: assert {'reason': 'r...blication_id'} == {'reason': 'r...<hash>'} | `tests/test_render_historical_admission.py` (4) |
| C11 | 4 | `Failed at tests/test_timeline_commit_integration.py:443` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_commit_integration.py` (4) |
| C12 | 3 | `AssertionError at tests/test_portable_lifecycle.py:455` | AssertionError: foreground Runtime exited N: { | `tests/test_portable_lifecycle.py` (2), `tests/test_profile_services.py` (1) |
| C13 | 3 | `ClipFieldError at astrid-agent/astrid/core/timeline/clip_fields.py:298` | astrid.core.timeline.clip_fields.ClipFieldError: entrance has unknown key 'durationFrames'; allowed: type, dur | `tests/test_timeline_visual_fields.py` (2), `tests/test_timeline_commit_integration.py` (1) |
| C14 | 3 | `CommitUnavailable at runtime_protocol/service.py:3325` | AssertionError: assert set() == {'txn-NfNf...<hash>'} | `tests/test_timeline_history_assembly.py` (3) |
| C15 | 3 | `Failed at tests/test_timeline_visual_fields.py:114` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_visual_fields.py` (3) |
| C16 | 3 | `AssertionError at tests/test_update_jobs.py:1078` | AssertionError: assert False | `tests/test_update_jobs.py` (3) |
| C17 | 2 | `CommandError at astrid-agent/astrid/sdk/timeline/_command_state.py:324` | astrid.sdk.timeline._command_state.CommandError: shot item source is unavailable | `tests/test_capture_candidate_binding.py` (2) |
| C18 | 2 | `AssertionError at tests/test_timeline_absent_head_repair_integration.py:46` | AssertionError: assert {'schema_vers...y': {}}}, ...} == {'schema_vers...fcNc'}, ...} | `tests/test_timeline_absent_head_repair_integration.py` (2) |
| C19 | 2 | `AssertionError at tests/test_timeline_clip_replacement.py:305` | AssertionError: assert {'clips': [{'...': 'visual'}]} == {'clips': [{'...': 'visual'}]} | `tests/test_timeline_clip_replacement.py` (2) |
| C20 | 2 | `AssertionError at tests/test_timeline_commit_input_integration.py:315` | AssertionError: assert {'status': 'c...: ['at'], ...} == {'status': 'c...NaNf'}, ...} | `tests/test_timeline_commit_input_integration.py` (2) |
| C21 | 2 | `AttributeError at astrid-agent/astrid/sdk/timeline/commit_session.py:496` | AttributeError: 'NoneType' object has no attribute 'client' | `tests/test_timeline_commit_integration.py` (2) |
| C22 | 2 | `ConflictError at runtime_protocol/daemon.py:320` | runtime_protocol.errors.ConflictError: migrated realm requires fresh Timeline provider registration before rea | `tests/test_timeline_commit_restore_integration.py` (2) |
| C23 | 2 | `Failed at tests/test_timeline_history_assembly.py:172` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_history_assembly.py` (2) |
| C24 | 1 | `ConflictError at runtime_protocol/backup.py:481` | runtime_protocol.errors.ConflictError: realm failed integrity checks | `tests/test_timeline_commit_acceptance.py` (1) |
| C25 | 1 | `WorkspaceClientError at astrid-agent/astrid/sdk/workspace_client.py:295` | urllib.error.HTTPError: HTTP Error N: Gone | `tests/test_timeline_public_s2_mixed_cli_journey.py` (1) |
| C26 | 1 | `AttributeError at tests/test_astrid_activation_join.py:837` | AttributeError: <module 'astrid_runtime.custody_broker' from '<path> has no attribute 'DARWIN_CUSTODY_SOCKET_P | `tests/test_astrid_activation_join.py` (1) |
| C27 | 1 | `AssertionError at tests/test_portable_lifecycle.py:409` | AssertionError: b'{"code": "conflict", "details": {"reason": "selection-or-inputs-invalid"}, "message": "The s | `tests/test_portable_lifecycle.py` (1) |
| C28 | 1 | `AssertionError at tests/test_portable_lifecycle.py:638` | AssertionError: { | `tests/test_portable_lifecycle.py` (1) |
| C29 | 1 | `AssertionError at tests/test_portable_lifecycle.py:684` | AssertionError: assert 'N' in 'requested runtime identity could not be verified.' | `tests/test_portable_lifecycle.py` (1) |
| C30 | 1 | `AssertionError at tests/test_profile_services.py:887` | AssertionError: { | `tests/test_profile_services.py` (1) |
| C31 | 1 | `AssertionError at tests/test_render_historical_admission.py:257` | AssertionError: assert {'reason': 'r...blication_id'} == {'reason': 'r...<hash>'} | `tests/test_render_historical_admission.py` (1) |
| C32 | 1 | `Failed at tests/test_render_historical_admission.py:404` | Failed: DID NOT RAISE ConflictError | `tests/test_render_historical_admission.py` (1) |
| C33 | 1 | `KeyError at runtime_protocol/store.py:3218` | KeyError: 'required_bytes' | `tests/test_render_historical_admission.py` (1) |
| C34 | 1 | `IndexError at tests/test_runtime_pack_startup.py:62` | IndexError: list index out of range | `tests/test_runtime_pack_startup.py` (1) |
| C35 | 1 | `AssertionError at tests/test_runtime_pack_startup.py:128` | assert N == N | `tests/test_runtime_pack_startup.py` (1) |
| C36 | 1 | `ConflictError at runtime_protocol/service.py:885` | runtime_protocol.errors.ConflictError: vN provider registration is required for this process before requests a | `tests/test_shot_candidate_promotion.py` (1) |
| C37 | 1 | `ValidationError at runtime_protocol/capture_validation.py:124` | runtime_protocol.errors.ValidationError: canonical capture projection provider is unavailable | `tests/test_spec_reference.py` (1) |
| C38 | 1 | `AssertionError at tests/test_timeline_clip_replacement.py:394` | AssertionError: assert 'merged' == 'rebased' | `tests/test_timeline_clip_replacement.py` (1) |
| C39 | 1 | `AssertionError at tests/test_timeline_clip_replacement.py:470` | AssertionError: Regex pattern did not match. | `tests/test_timeline_clip_replacement.py` (1) |
| C40 | 1 | `AssertionError at tests/test_timeline_clip_replacement.py:499` | AssertionError: Regex pattern did not match. | `tests/test_timeline_clip_replacement.py` (1) |
| C41 | 1 | `AssertionError at tests/test_timeline_clip_replacement.py:550` | AssertionError: Regex pattern did not match. | `tests/test_timeline_clip_replacement.py` (1) |
| C42 | 1 | `Failed at tests/test_timeline_commit_integration.py:415` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_commit_integration.py` (1) |
| C43 | 1 | `Failed at tests/test_timeline_commit_integration.py:426` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_commit_integration.py` (1) |
| C44 | 1 | `Failed at tests/test_timeline_commit_integration.py:467` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_commit_integration.py` (1) |
| C45 | 1 | `Failed at tests/test_timeline_history_assembly.py:398` | Failed: DID NOT RAISE RuntimeErrorBase | `tests/test_timeline_history_assembly.py` (1) |
| C46 | 1 | `AssertionError at tests/test_timeline_ordinary_http.py:64` | assert "SCHEMA_DIGEST = 'shaN:<hash>'" in '"""Generated contract metadata; do not edit by hand."""\n\nCONTRACT | `tests/test_timeline_ordinary_http.py` (1) |
| C47 | 1 | `Failed at tests/test_timeline_redo_restoration_boundary.py:153` | Failed: DID NOT RAISE CommitRejected | `tests/test_timeline_redo_restoration_boundary.py` (1) |
| C48 | 1 | `AssertionError at tests/test_timeline_visual_fields.py:98` | AssertionError: assert 'None' == 'type-on Nf' | `tests/test_timeline_visual_fields.py` (1) |
| C49 | 1 | `KeyError at tests/test_verified_host_launch.py:431` | KeyError: 'source_checkout_closure' | `tests/test_verified_host_launch.py` (1) |
| C50 | 1 | `CalledProcessError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/subprocess.py:571` | subprocess.CalledProcessError: Command '['git', '-C', '<path> 'rev-parse', 'HEAD']' returned non-zero exit sta | `tests/test_wc10_installed_launcher.py` (1) |

## Failing IDs by test file

| IDs | Clusters | File |
| ---: | ---: | --- |
| 27 | 5 | `tests/test_timeline_history_assembly.py` |
| 24 | 2 | `tests/test_timeline_commit_crash.py` |
| 20 | 1 | `tests/test_snapshot_legacy_certification.py` |
| 10 | 6 | `tests/test_timeline_commit_integration.py` |
| 7 | 4 | `tests/test_render_historical_admission.py` |
| 6 | 2 | `tests/test_capture_candidate_binding.py` |
| 6 | 5 | `tests/test_timeline_clip_replacement.py` |
| 6 | 3 | `tests/test_timeline_commit_restore_integration.py` |
| 6 | 3 | `tests/test_timeline_visual_fields.py` |
| 5 | 1 | `tests/test_runtime_boundary.py` |
| 5 | 4 | `tests/test_portable_lifecycle.py` |
| 4 | 2 | `tests/test_timeline_commit_input_integration.py` |
| 3 | 1 | `tests/test_runtime_nine_track_wal_reopen.py` |
| 3 | 1 | `tests/test_update_jobs.py` |
| 2 | 2 | `tests/test_timeline_public_s2_mixed_cli_journey.py` |
| 2 | 2 | `tests/test_profile_services.py` |
| 2 | 2 | `tests/test_runtime_pack_startup.py` |
| 2 | 2 | `tests/test_shot_candidate_promotion.py` |
| 2 | 1 | `tests/test_timeline_absent_head_repair_integration.py` |
| 1 | 1 | `tests/test_timeline_commit_acceptance.py` |
| 1 | 1 | `tests/test_astrid_activation_join.py` |
| 1 | 1 | `tests/test_astrid_product_down.py` |
| 1 | 1 | `tests/test_foreground_authoring_integration.py` |
| 1 | 1 | `tests/test_spec_reference.py` |
| 1 | 1 | `tests/test_timeline_ordinary_http.py` |
| 1 | 1 | `tests/test_timeline_projection_occupancy.py` |
| 1 | 1 | `tests/test_timeline_redo_restoration_boundary.py` |
| 1 | 1 | `tests/test_verified_host_launch.py` |
| 1 | 1 | `tests/test_wc10_installed_launcher.py` |
