# Prune candidates

370 failing IDs whose failure points at removed, retired, moved or legacy code, or that AG-P1 owns outright. Selected by message and test name, so some are false leads. AG-P1 sorts every row before its owning card fixes anything: **retire** (delete, citing the retiring change or D5's support line), **redundant** (delete, citing the passing test that covers the same behaviour) or **keep** (current behaviour, or updating from the previous published release: the owning card fixes it). AG-P1 sorts the `ci:` rows and AG-P2 the `lanes:` rows. See [D5](../../inputs.md#owner-decisions).

| IDs | Test file | Cluster | Owning card | Message |
| ---: | --- | --- | --- | --- |
| 54 | `tests/test_installer_busy_fence.py` | ci:C3 | AG-A5 | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the  |
| 27 | `tests/editing_conformance/test_authenticated_legacy_restore.py` | lanes:C4 | AG-P2 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 16 | `tests/editing_conformance/test_current_pair_reader.py` | lanes:C4 | AG-P2 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 14 | `tests/editing_conformance/test_fork_abi1_binding_set.py` | ci:C9 | AG-A6 | astrid.core.timeline.authoring_bundle.AuthoringBundleError: fork native binding schema cha |
| 13 | `tests/scripts/test_pod_bootstrap.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 12 | `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 12 | `tests/test_installer_pinokio_integration.py` | lanes:C9 | AG-B13 | ValueError: Astrid is still running. Choose Pinokio's Stop button, then try again. |
| 12 | `tests/test_local_install.py` | ci:C3 | AG-A5 | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the  |
| 11 | `tests/core/test_timeline_element_publication_runtime.py` | lanes:C10 | AG-B16 | runtime_protocol.errors.ConflictError: project pack compiled element descriptor is invalid |
| 8 | `tests/test_installer_acl.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 7 | `tests/packs/timeline/test_cli_status_publish.py` | ci:C11 | AG-P1 | argparse.ArgumentError: argument command: invalid choice: 'publish' (choose from 'import', |
| 6 | `tests/packs/test_portfolio_parity.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 6 | `tests/sdk/test_timeline_legacy_inverse_bindings.py` | lanes:C11 | AG-A7 | astrid.sdk.workspace_client.WorkspaceClientError: Refused: after this edit render and visu |
| 5 | `tests/core/pack/test_transaction.py` | ci:C4 | AG-A2 | AssertionError: Browser transaction tests require explicit pinned local Node/esbuild input |
| 5 | `tests/editing_conformance/test_historical_shared_redo_authority.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 5 | `tests/editing_conformance/test_inverse_stage_runtime_regressions.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 5 | `tests/test_onboarding_parity.py` | lanes:C20 | AG-P2 | KeyError: "unknown executor id 'editorial.arrange'" |
| 4 | `tests/editing_conformance/test_native_word_anchor.py` | lanes:C2 | AG-A9 | subprocess.CalledProcessError: Command '['<path> '-c', "\nimport json, sys\nfrom tests.edi |
| 4 | `tests/integrations/test_media_only_render_without_remotion.py` | lanes:C27 | Wave C | AssertionError: (N, '{"code": "retired_route", "details": {"hint": "Submit a timeline comm |
| 4 | `tests/sdk/test_timeline_checkout_history_runtime.py` | lanes:C26 | AG-A2 | AssertionError: missing qualified authentic GN archive: <path> |
| 4 | `tests/test_live_capability_discovery_fix.py` | ci:C30 | AG-P1 | KeyError: "unknown executor id 'understanding.audio_understand'" |
| 3 | `tests/core/execution/test_m1_13_pack_provenance.py` | lanes:C12 | AG-B17 | RuntimeError: process control is already sandbox; refusing to change it to strict |
| 3 | `tests/editing_conformance/test_word_binding_recipe.py` | lanes:C2 | AG-A9 | subprocess.CalledProcessError: Command '['<path> '-c', "\nimport json, sys\nfrom tests.edi |
| 3 | `tests/packs/rendering/test_remotion_layer_tail_compat.py` | ci:C8 | AG-A3 | subprocess.CalledProcessError: Command '['tar', '-xOf', '<path> 'package/dist/chunk-ANLVBE |
| 3 | `tests/packs/runpod/test_https_transport.py` | lanes:C35 | Wave C | AttributeError: 'types.SimpleNamespace' object has no attribute 'session_ref' |
| 3 | `tests/packs/test_portfolio_parity.py` | ci:C35 | AG-A3 | AssertionError: pack 'iteration' not discovered |
| 3 | `tests/packs/test_portfolio_parity.py` | ci:C37 | AG-A3 | KeyError: "unknown executor id 'iteration.assemble'" |
| 3 | `tests/test_installer_update_recovery.py` | lanes:C30 | AG-B5 | AssertionError: Traceback (most recent call last): |
| 2 | `tests/editing_conformance/test_authoring_undo_projection.py` | ci:C9 | AG-A6 | astrid.core.timeline.authoring_bundle.AuthoringBundleError: fork native binding schema cha |
| 2 | `tests/editing_conformance/test_commit_runtime_parent_media.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 2 | `tests/editing_conformance/test_commit_runtime_parent_media_swap.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 2 | `tests/editing_conformance/test_fork_historical_source_boundary.py` | ci:C65 | AG-B10 | astrid.sdk.timeline._command_state.CommandError: missing or ambiguous identity 'shot-N' |
| 2 | `tests/editing_conformance/test_historical_shared_inverse_owners.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 2 | `tests/editing_conformance/test_occurrence_shared_historical.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 2 | `tests/editing_conformance/test_recipe_occurrence_media.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 2 | `tests/packs/builtin/test_training_run_support.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 2 | `tests/packs/timeline/test_cli_edit_flags.py` | ci:C58 | AG-B4 | AttributeError: 'function' object has no attribute '__wrapped__' |
| 2 | `tests/sdk/test_inverse_removed_shot_owners_runtime.py` | ci:C52 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 2 | `tests/sdk/test_timeline_checkout.py` | lanes:C38 | Wave C | AttributeError: 'Runtime' object has no attribute '_last_handshake' |
| 2 | `tests/sdk/test_timeline_clip_scalar_provider.py` | ci:C25 | AG-B10 | astrid.sdk.timeline._command_state.CommandError: inverse stage image differs from authenti |
| 2 | `tests/sdk/test_timeline_occurrence_delete_provider.py` | ci:C25 | AG-B10 | astrid.sdk.timeline._command_state.CommandError: inverse stage image differs from authenti |
| 2 | `tests/stage1/test_zero_shim_lane_c.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 2 | `tests/test_failure_mode_executor.py` | ci:C83 | AG-A2 | scripts.failure_mode_executor.HistoricalSourcePrerequisiteError: Historical release-N prer |
| 2 | `tests/test_installer_launcher_repair.py` | ci:C87 | Wave C | AttributeError: 'Popen' object has no attribute 'home' |
| 2 | `tests/test_installer_lifecycle.py` | ci:C3 | AG-A5 | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the  |
| 2 | `tests/test_installer_release0_rollback.py` | ci:C88 | AG-A5 | AssertionError: Traceback (most recent call last): |
| 2 | `tests/test_installer_shim.py` | ci:C90 | AG-A5 | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the  |
| 2 | `tests/test_local_install.py` | ci:C74 | Wave C | AttributeError: 'FakeBackend' object has no attribute 'remove_skills' |
| 1 | `tests/core/execution/test_openai_child_admission.py` | lanes:C5 | AG-B12 | KeyError: 'bridge.parent' |
| 1 | `tests/core/generation/test_engine_custody.py` | lanes:C55 | AG-B22 | ModuleNotFoundError: No module named 'tests.core.test_action_cli_clip_rehearsal' |
| 1 | `tests/core/generation/test_generation_index.py` | ci:C241 | Wave C | AttributeError: module 'scripts.gen_capability_index' has no attribute '_generation_sectio |
| 1 | `tests/core/generation/test_readiness_inputs_f04.py` | ci:C320 | Wave C | AttributeError: 'types.SimpleNamespace' object has no attribute 'kind' |
| 1 | `tests/core/generation/test_trusted_inventory.py` | ci:C327 | Wave C | AttributeError: 'types.SimpleNamespace' object has no attribute 'folder_paths' |
| 1 | `tests/core/rendering/test_remotion_runtime.py` | ci:C352 | Wave C | AttributeError: module 'astrid.core.rendering.remotion_runtime' has no attribute '_probe_s |
| 1 | `tests/core/rendering/test_remotion_runtime.py` | ci:C353 | Wave C | AttributeError: module 'ctypes' has no attribute 'WinDLL' |
| 1 | `tests/core/rendering/test_remotion_runtime.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/editing_conformance/test_commit_runtime_identity.py` | lanes:C28 | Wave C | runtime_protocol.errors.ConflictError: vN provider/baseline verification is pending; reque |
| 1 | `tests/editing_conformance/test_commit_runtime_native_checkout.py` | lanes:C1 | AG-A7 | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visua |
| 1 | `tests/editing_conformance/test_commit_runtime_source_copy.py` | lanes:C52 | Wave C | AttributeError: 'types.SimpleNamespace' object has no attribute 'receipt' |
| 1 | `tests/editing_conformance/test_fork_abi1_binding_set.py` | ci:C203 | Wave C | AssertionError: assert [{'dependenci... N, ...}, ...] == [{'dependenci...rence:occ-N'}] |
| 1 | `tests/editing_conformance/test_m1_legacy_archive_read.py` | lanes:C4 | AG-P2 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/editing_conformance/test_native_sheet_current_runtime.py` | lanes:C3 | AG-A10 | TypeError: runtime.<locals>.<lambda>() got an unexpected keyword argument 'timeout' |
| 1 | `tests/editing_conformance/test_occurrence_shared_historical.py` | lanes:C75 | Wave C | astrid.sdk.workspace_client.WorkspaceClientError: lost acknowledgement |
| 1 | `tests/integrations/test_runpod_dry_live_seam.py` | lanes:C92 | Wave C | AttributeError: 'types.SimpleNamespace' object has no attribute 'show' |
| 1 | `tests/packs/h3_av/test_compile_generalized.py` | ci:C262 | Wave C | astrid.packs.hN_av.shared.spec.HNSpecError: Advanced legacy changes are outside SPEC-MIN |
| 1 | `tests/packs/h3_av/test_two_edit_cpu_qualification.py` | lanes:C99 | Wave C | argparse.ArgumentError: argument ACTION: invalid choice: 'hN_av.transform' (choose from ) |
| 1 | `tests/packs/rendering/test_scene_source_carry.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/packs/rendering/test_timeline_storyboard.py` | ci:C214 | Wave C | AttributeError: module 'astrid.packs.rendering.actions.timeline_storyboard.run' has no att |
| 1 | `tests/packs/rendering/test_timeline_storyboard.py` | ci:C215 | Wave C | AttributeError: module 'astrid.packs.rendering.actions.timeline_storyboard.run' has no att |
| 1 | `tests/packs/rendering/test_timeline_storyboard.py` | ci:C216 | Wave C | AttributeError: module 'astrid.packs.rendering.actions.timeline_storyboard.run' has no att |
| 1 | `tests/packs/test_pack_discovery.py` | ci:C104 | AG-B1 | KeyError: "unknown executor id 'builtin.duplicate'"` |
| 1 | `tests/packs/test_pack_quarantine.py` | ci:C121 | AG-B1 | AssertionError: assert 'keywords.N' in 'Pack manifest needs an explicit schema upgrade. Mi |
| 1 | `tests/packs/test_pack_quarantine.py` | ci:C123 | AG-B1 | AssertionError: assert 'keywords.N' in 'Pack manifest needs an explicit schema upgrade. Mi |
| 1 | `tests/packs/timeline/test_verbs_working_copy.py` | ci:C135 | Wave C | AttributeError: 'Timelines' object has no attribute 'history' |
| 1 | `tests/scripts/test_claim_runpod_5090_backup.py` | ci:C11 | AG-P1 | argparse.ArgumentError: argument command: invalid choice: 'publish' (choose from 'import', |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C153 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C154 | AG-P1 | AssertionError: assert 'fixture source identity refused' in '/bin/bash: <path> No such fil |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C155 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C156 | AG-P1 | AssertionError: assert 'uv not found' in '/bin/bash: <path> No such file or directory\n' |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C157 | AG-P1 | AssertionError: assert ('cannot create or write' in '/bin/bash: <path> No such file or dir |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C158 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C159 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C160 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C161 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C162 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C163 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_bootstrap.py` | ci:C164 | AG-P1 | AssertionError: /bin/bash: <path> No such file or directory |
| 1 | `tests/scripts/test_pod_h3_install.py` | ci:C11 | AG-P1 | argparse.ArgumentError: argument command: invalid choice: 'publish' (choose from 'import', |
| 1 | `tests/sdk/test_generation_verified_preparation_gr03.py` | ci:C189 | Wave C | AttributeError: 'NoneType' object has no attribute 'runtime_nodes' |
| 1 | `tests/sdk/test_runtime_response_conformance.py` | ci:C63 | Wave C | AssertionError: assert '/vN/projects...s/main/commit' == '/vN/projects...ion-revisions' |
| 1 | `tests/sdk/test_timeline_commit_provider.py` | ci:C368 | Wave C | AssertionError: assert ModuleSpec(name='astrid.core.timeline.inverses', loader=<_frozen_im |
| 1 | `tests/sdk/test_timeline_commit_provider_scalar.py` | ci:C25 | AG-B10 | astrid.sdk.timeline._command_state.CommandError: inverse stage image differs from authenti |
| 1 | `tests/sdk/test_timeline_export.py` | lanes:C56 | Wave C | runtime_protocol.errors.RetiredRouteError: legacy timeline writes are retired; submit Edit |
| 1 | `tests/stage1/test_asset_cache_retired_luna.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/stage1/test_final_render_authority_luna.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/stage1/test_kernel_admission_runtime.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/stage1/test_runtime_client_cutover.py` | lanes:C62 | Wave C | AssertionError: assert not ({'install', 'rollback', 'uninstall', 'update'} & {'add', 'agen |
| 1 | `tests/stage1/test_thread_authority_cutover.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/stage1/test_thread_authority_cutover.py` | ci:C8 | AG-A3 | subprocess.CalledProcessError: Command '['tar', '-xOf', '<path> 'package/dist/chunk-ANLVBE |
| 1 | `tests/stage1/test_zero_shim_execution_pack_deletion.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/stage1/test_zero_shim_timeline_cutover_luna.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/test_canonical_aliases.py` | ci:C393 | AG-P1 | AssertionError: 'editorial.transcribe' not found in mappingproxy({'hivemind.contribute': E |
| 1 | `tests/test_canonical_aliases.py` | ci:C394 | AG-P1 | AssertionError: Items in the second set but not the first:` |
| 1 | `tests/test_canonical_aliases.py` | ci:C395 | AG-P1 | AssertionError: Items in the first set but not the second:` |
| 1 | `tests/test_canonical_aliases.py` | ci:C396 | AG-P1 | AssertionError: Tuples differ: ('imp[N chars]t', 'appearance', 'edit', 'assets', 'find', ' |
| 1 | `tests/test_creator_entry_declarations.py` | ci:C6 | AG-P1 | FileNotFoundError: [Errno N] No such file or directory: '<path> |
| 1 | `tests/test_failure_mode_executor.py` | ci:C410 | Wave C | AssertionError: assert 'Runtime' == 'Agent' |
| 1 | `tests/test_installer_backup.py` | ci:C3 | AG-A5 | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the  |
| 1 | `tests/test_installer_launchd_cache_window.py` | ci:C422 | Wave C | AttributeError: '_Backend' object has no attribute 'run' |
| 1 | `tests/test_installer_local_update.py` | ci:C425 | Wave C | astrid.installer.rN_stop.RNStopError: An interrupted legacy RN update is retained. Automat |
| 1 | `tests/test_installer_pinokio_integration.py` | lanes:C41 | AG-B13 | Failed: Timeout (>N.Ns) from pytest-timeout. |
| 1 | `tests/test_installer_startup_stop.py` | ci:C3 | AG-A5 | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the  |
| 1 | `tests/test_installer_transaction_authority.py` | lanes:C42 | AG-B5 | AssertionError: Recovering the interrupted Astrid update. |
| 1 | `tests/test_installer_update_legacy_record.py` | ci:C432 | Wave C | AssertionError: assert 'recovery-needed' == 'failed' |
| 1 | `tests/test_onboarding_parity.py` | lanes:C53 | AG-P2 | AssertionError: editorial.arrange not found in discovery. Executor ids: ['generation.gener |
| 1 | `tests/test_skills_selected_composition.py` | ci:C11 | AG-P1 | argparse.ArgumentError: argument command: invalid choice: 'publish' (choose from 'import', |
| 1 | `tests/test_timeline_editing_helpers.py` | ci:C299 | Wave C | ImportError: cannot import name 'retime_with_ripple' from 'astrid.sdk.timeline_editing' (< |
| 1 | `tests/test_timeline_editing_helpers.py` | ci:C300 | Wave C | ImportError: cannot import name 'retime' from 'astrid.sdk.timeline_editing' (<path> |
| 1 | `tests/test_timeline_editing_helpers.py` | ci:C301 | Wave C | ImportError: cannot import name 'retime_with_ripple' from 'astrid.sdk.timeline_editing' (< |
| 1 | `tests/timeline/test_authoring_bundle.py` | ci:C303 | Wave C | ImportError: cannot import name 'promote_approved_authoring_candidate' from 'astrid.core.t |
| 1 | `tests/timeline/test_shot_composition_projection.py` | ci:C306 | Wave C | ImportError: cannot import name '_track_merge' from 'astrid.core.timeline.shot_composition |
| 1 | `tests/v10/test_docs_cli_alignment.py` | ci:C311 | Wave C | AssertionError: SKILL.md contains 'astrid status' |
| 1 | `tests/v10/test_docs_cli_alignment.py` | ci:C312 | Wave C | AssertionError: astrid/packs/_core/docs/SKILL.md: 'astrid status' |
