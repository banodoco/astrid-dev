# Failure clusters — Lanes (integration 1–4 and opt-in), release/15/main b324d7c1

787 failing IDs in 104 clusters (grouped by exception type and raise site).

| # | IDs | Raise site | Top message | Top files |
| --- | ---: | --- | --- | --- |
| C1 | 272 | `RuntimeErrorBase at astrid-runtime/runtime_protocol/service.py:3400` | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visualize cannot open the | `tests/editing_conformance/test_commit_runtime_occurrence_media.py` (48), `tests/editing_conformance/test_commit_runtime_parent_media.py` (38) |
| C2 | 90 | `CalledProcessError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/subprocess.py:571` | subprocess.CalledProcessError: Command '['<path> '-c', "\nimport json, sys\nfrom tests.editing_conformance.nat | `tests/editing_conformance/test_native_word_anchor.py` (38), `tests/editing_conformance/test_word_binding_recipe.py` (23) |
| C3 | 80 | `ServiceUnavailableError at astrid/sdk/client.py:389` | TypeError: runtime.<locals>.<lambda>() got an unexpected keyword argument 'timeout' | `tests/editing_conformance/test_native_batch_ingress.py` (40), `tests/editing_conformance/test_native_sheet_current_runtime.py` (19) |
| C4 | 44 | `FileNotFoundError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/pathlib.py:1044` | FileNotFoundError: [Errno N] No such file or directory: '<path> | `tests/editing_conformance/test_authenticated_legacy_restore.py` (27), `tests/editing_conformance/test_current_pair_reader.py` (16) |
| C5 | 21 | `KeyError at tests/core/execution/test_openai_child_admission.py:72` | KeyError: 'bridge.parent' | `tests/core/execution/test_openai_child_admission.py` (21) |
| C6 | 16 | `Failed at astrid/installer/app_update.py:427` | Failed: Timeout (>N.Ns) from pytest-timeout. | `tests/test_installer_pinokio_stopped_update.py` (14), `tests/test_pinokio_switch_integration.py` (2) |
| C7 | 16 | `IndexError at tests/sdk/test_capture_source_runtime.py:41` | IndexError: list index out of range | `tests/packs/rendering/test_live_source_label_native.py` (16) |
| C8 | 14 | `PackValidationError at astrid/core/pack/discovery.py:522` | astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with | `tests/integrations/test_generation_runtime_composition.py` (13), `tests/packs/test_vibecomfy_import_generic_host.py` (1) |
| C9 | 12 | `RuntimeOperationError at astrid/installer/backend.py:1257` | ValueError: Astrid is still running. Choose Pinokio's Stop button, then try again. | `tests/test_installer_pinokio_integration.py` (12) |
| C10 | 11 | `ConflictError at astrid-runtime/runtime_protocol/timeline_commit_inputs.py:295` | runtime_protocol.errors.ConflictError: project pack compiled element descriptor is invalid | `tests/core/test_timeline_element_publication_runtime.py` (11) |
| C11 | 10 | `CommitRefused at astrid/sdk/timeline/sync.py:1220` | astrid.sdk.workspace_client.WorkspaceClientError: Refused: after this edit render and visualize cannot open th | `tests/sdk/test_timeline_legacy_inverse_bindings.py` (6), `tests/sdk/test_timeline_producer_guard_runtime.py` (2) |
| C12 | 10 | `RuntimeError at astrid-runtime/runtime_protocol/platform.py:1226` | RuntimeError: process control is already sandbox; refusing to change it to strict | `tests/core/execution/test_m1_13_pack_provenance.py` (6), `tests/core/generation/test_generate_target_journey.py` (2) |
| C13 | 9 | `IndexError at tests/sdk/test_timeline_capture_projection.py:316` | IndexError: list index out of range | `tests/sdk/test_timeline_capture_projection.py` (9) |
| C14 | 9 | `WorkerPreparationError at tests/packs/runpod/test_worker_staging.py:179` | astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last): | `tests/packs/runpod/test_worker_staging.py` (9) |
| C15 | 7 | `MediaHandleError at astrid/sdk/media_handles.py:106` | astrid.sdk.media_handles.MediaHandleError: 'shaN:<hash>': no media in project <hash> matches shaN:<hash>; impo | `tests/integrations/test_runpod_slot_path_cpu.py` (5), `tests/integrations/test_dry_run_equals_live_run.py` (2) |
| C16 | 7 | `HostError at astrid/core/execution/generic_host.py:1955` | astrid.core.execution.host_errors.HostError: undeclared secret environment variable 'FAL_KEY' | `tests/integrations/test_generation_runtime_composition.py` (7) |
| C17 | 7 | `AssertionError at tests/integrations/test_managed_host_preparation.py:322` | AssertionError: (['prepare', 'align', 'native-nodes'], {'capability_id': 'vibecomfy.run', 'capability_type': ' | `tests/integrations/test_managed_host_preparation.py` (7) |
| C18 | 6 | `no traceback | Failed: provide the saved actual public CN frame-index artifact for affected readback repl` | Failed: provide the saved actual public CN frame-index artifact for affected readback replay | `tests/integrations/test_c06_public_timeline_visualizer.py` (6) |
| C19 | 5 | `ElementPackNotInstalled at astrid/sdk/timeline_address.py:520` | astrid.sdk.timeline_address.ElementPackNotInstalled: [element_pack_not_installed] audio: no installed pack dec | `tests/editing_conformance/test_commit_runtime_numeric_params.py` (5) |
| C20 | 5 | `CapabilityNotFoundError at astrid/sdk/discovery.py:797` | KeyError: "unknown executor id 'editorial.arrange'" | `tests/test_onboarding_parity.py` (5) |
| C21 | 5 | `HostError at astrid/core/execution/generic_host.py:12091` | astrid.core.execution.host_errors.HostError: delegated child spec lacks admitted_source_digest; refusing befor | `tests/core/execution/test_generic_host_child_bridge_d18.py` (5) |
| C22 | 5 | `CommandError at astrid/sdk/timeline/_recording.py:175` | astrid.sdk.timeline._command_state.CommandError: created identity is occupied | `tests/editing_conformance/test_next_command_cohort_runtime.py` (2), `tests/editing_conformance/test_next_ordinary_union_runtime.py` (1) |
| C23 | 5 | `IntegrityError at astrid/core/generation/managed_preparation.py:824` | astrid.core.generation.engine_contracts.IntegrityError: managed alignment command failed (step=nodes_restore,  | `tests/integrations/test_managed_host_preparation.py` (4), `tests/integrations/test_pod_owned_preparation.py` (1) |
| C24 | 5 | `RendererProtocolError at astrid/core/rendering/errors.py:110` | astrid.core.rendering.errors.RendererProtocolError: audio preparation requires the managed asset server | `tests/packs/test_renderer_parity.py` (5) |
| C25 | 4 | `AssertionError at tests/core/test_timeline_element_publication_runtime.py:495` | assert (not False and N == N) | `tests/core/test_timeline_element_publication_runtime.py` (4) |
| C26 | 4 | `AssertionError at tests/sdk/test_timeline_checkout_history_runtime.py:82` | AssertionError: missing qualified authentic GN archive: <path> | `tests/sdk/test_timeline_checkout_history_runtime.py` (4) |
| C27 | 4 | `AssertionError at tests/integrations/test_media_only_render_without_remotion.py:92` | AssertionError: (N, '{"code": "retired_route", "details": {"hint": "Submit a timeline commit instead of the re | `tests/integrations/test_media_only_render_without_remotion.py` (4) |
| C28 | 3 | `ConflictError at astrid-runtime/runtime_protocol/v33_lifecycle.py:300` | runtime_protocol.errors.ConflictError: vN provider/baseline verification is pending; requests and fresh pins a | `tests/editing_conformance/test_commit_runtime_identity.py` (3) |
| C29 | 3 | `AssertionError at tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py:67` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py` (3) |
| C30 | 3 | `AssertionError at tests/test_installer_update_recovery.py:609` | AssertionError: Traceback (most recent call last): | `tests/test_installer_update_recovery.py` (3) |
| C31 | 3 | `CapabilityRuntimeError at astrid/sdk/results.py:615` | astrid.sdk.exceptions.CapabilityRuntimeError: vibecomfy.run canonical input preflight failed: managed alignmen | `tests/integrations/test_managed_host_preparation.py` (3) |
| C32 | 3 | `AssertionError at tests/integrations/test_managed_host_preparation.py:646` | AssertionError: assert ['unlock'] == ['stopped-and...ed', 'unlock'] | `tests/integrations/test_managed_host_preparation.py` (3) |
| C33 | 3 | `ValueError at vibecomfy-checkout/vibecomfy/workflow.py:1314` | ValueError: set_input('permission_mask_N') has no registered public input or alias in workflow 'hN_av_referenc | `tests/packs/h3_av/test_static_mask_preflight.py` (3) |
| C34 | 3 | `RendererInternalError at astrid/core/rendering/errors.py:110` | astrid.core.rendering.errors.RendererInternalError: hyperframes render failed (exit N) | `tests/packs/rendering/test_hyperframes_backend.py` (3) |
| C35 | 3 | `AttributeError at astrid/packs/runpod/prepared_task.py:638` | AttributeError: 'types.SimpleNamespace' object has no attribute 'session_ref' | `tests/packs/runpod/test_https_transport.py` (3) |
| C36 | 2 | `AssertionError at tests/editing_conformance/test_commit_runtime_first_clip.py:61` | AssertionError: {'data': None, 'error': {'code': 'validation_error', 'details': {'base': {'publication_id': 't | `tests/editing_conformance/test_commit_runtime_first_clip.py` (2) |
| C37 | 2 | `AssertionError at tests/editing_conformance/test_commit_runtime_occurrence_create.py:70` | AssertionError: Traceback (most recent call last): | `tests/editing_conformance/test_commit_runtime_occurrence_create.py` (2) |
| C38 | 2 | `AttributeError at astrid/sdk/documents.py:141` | AttributeError: 'Runtime' object has no attribute '_last_handshake' | `tests/sdk/test_timeline_checkout.py` (2) |
| C39 | 2 | `AssertionError at tests/sdk/test_timeline_commit_provider_runtime.py:81` | AssertionError: assert 'label' not in {'blendMode': 'normal', 'fit': 'contain', 'id': 'VN', 'kind': 'visual',  | `tests/sdk/test_timeline_commit_provider_runtime.py` (2) |
| C40 | 2 | `AssertionError at tests/sdk/test_timeline_selected_schema_runtime.py:1097` | astrid.sdk.timeline._command_state.CommandError: selected PARAM authority is unavailable | `tests/sdk/test_timeline_selected_schema_runtime.py` (2) |
| C41 | 2 | `CalledProcessError at astrid/installer/backend.py:619` | Failed: Timeout (>N.Ns) from pytest-timeout. | `tests/test_installer_pinokio_integration.py` (2) |
| C42 | 2 | `AssertionError at tests/test_installer_transaction_authority.py:951` | AssertionError: Recovering the interrupted Astrid update. | `tests/test_installer_transaction_authority.py` (2) |
| C43 | 2 | `no traceback | Failed: the Runtime checkout <path> has no commit <hash>` | Failed: the Runtime checkout <path> has no commit <hash> | `tests/integrations/test_generic_host_runtime_restart.py` (2) |
| C44 | 2 | `no traceback | ` | fixture 'configured' not found | `tests/integrations/test_pinned_element_render_proof.py` (1), `tests/integrations/test_runpod_host_endpoint_r5.py` (1) |
| C45 | 2 | `KeyError at tests/integrations/test_dry_run_equals_live_run.py:266` | KeyError: ('audio', 'transcribe') | `tests/integrations/test_dry_run_equals_live_run.py` (2) |
| C46 | 2 | `AssertionError at tests/integrations/test_generation_runtime_composition.py:1452` | astrid.core.execution.host_errors.HostError: undeclared secret environment variable 'FAL_KEY' | `tests/integrations/test_generation_runtime_composition.py` (2) |
| C47 | 1 | `AssertionError at tests/core/test_timeline_element_publication_runtime.py:652` | assert (not False and 'timeline_outcome_unknown' == 'forbidden' | `tests/core/test_timeline_element_publication_runtime.py` (1) |
| C48 | 1 | `AssertionError at tests/core/test_timeline_element_publication_runtime.py:821` | astrid.sdk.workspace_client.WorkspaceClientError: lost acknowledgement after durable acceptance | `tests/core/test_timeline_element_publication_runtime.py` (1) |
| C49 | 1 | `TypeError at tests/core/test_timeline_element_publication_runtime.py:868` | TypeError: 'NoneType' object is not subscriptable | `tests/core/test_timeline_element_publication_runtime.py` (1) |
| C50 | 1 | `AssertionError at tests/core/test_timeline_element_publication_runtime.py:1065` | astrid.sdk.timeline._command_state.CommandError: selected PARAM authority is unavailable | `tests/core/test_timeline_element_publication_runtime.py` (1) |
| C51 | 1 | `AssertionError at tests/editing_conformance/test_commit_runtime_numeric_params.py:37` | AssertionError: assert (<class 'int'> is <class 'float'>) | `tests/editing_conformance/test_commit_runtime_numeric_params.py` (1) |
| C52 | 1 | `AttributeError at astrid/sdk/timeline_duplicate.py:424` | AttributeError: 'types.SimpleNamespace' object has no attribute 'receipt' | `tests/editing_conformance/test_commit_runtime_source_copy.py` (1) |
| C53 | 1 | `AssertionError at tests/test_onboarding_parity.py:279` | AssertionError: editorial.arrange not found in discovery. Executor ids: ['generation.generate_audio', 'generat | `tests/test_onboarding_parity.py` (1) |
| C54 | 1 | `AssertionError at tests/core/execution/test_generic_host_child_bridge_d18.py:4329` | astrid.core.execution.host_errors.HostError: delegated child spec lacks admitted_source_digest; refusing befor | `tests/core/execution/test_generic_host_child_bridge_d18.py` (1) |
| C55 | 1 | `ModuleNotFoundError at tests/core/generation/test_engine_custody.py:1207` | ModuleNotFoundError: No module named 'tests.core.test_action_cli_clip_rehearsal' | `tests/core/generation/test_engine_custody.py` (1) |
| C56 | 1 | `RetiredRouteError at astrid-runtime/runtime_protocol/service.py:467` | runtime_protocol.errors.RetiredRouteError: legacy timeline writes are retired; submit EditCommands through com | `tests/sdk/test_timeline_export.py` (1) |
| C57 | 1 | `WorkspaceClientError at astrid/sdk/workspace_client.py:338` | urllib.error.HTTPError: HTTP Error N: Gone | `tests/sdk/test_timeline_import.py` (1) |
| C58 | 1 | `ConflictError at astrid-runtime/runtime_protocol/backup.py:481` | runtime_protocol.errors.ConflictError: realm failed integrity checks | `tests/sdk/test_timeline_selected_schema_runtime.py` (1) |
| C59 | 1 | `AssertionError at tests/sdk/test_timeline_selected_schema_runtime.py:881` | astrid.sdk.timeline._command_state.CommandError: selected PARAM authority is unavailable | `tests/sdk/test_timeline_selected_schema_runtime.py` (1) |
| C60 | 1 | `AssertionError at tests/stage1/test_capability_parity_gate_luna.py:206` | AssertionError: rendering.render: proof did not execute cleanly: {'returncode': N, 'status': 'fail', 'output_t | `tests/stage1/test_capability_parity_gate_luna.py` (1) |
| C61 | 1 | `AssertionError at tests/stage1/test_media_handoff_render_boundary.py:325` | AssertionError: {'executor_id': 'rendering.render', 'missing_binaries': [], 'returncode': N, 'skipped': False, | `tests/stage1/test_media_handoff_render_boundary.py` (1) |
| C62 | 1 | `AssertionError at tests/stage1/test_runtime_client_cutover.py:674` | AssertionError: assert not ({'install', 'rollback', 'uninstall', 'update'} & {'add', 'agent-index', 'check', ' | `tests/stage1/test_runtime_client_cutover.py` (1) |
| C63 | 1 | `AssertionError at tests/test_installer_lifecycle.py:1770` | AssertionError: N-version Runtime did not publish the selected realm | `tests/test_installer_lifecycle.py` (1) |
| C64 | 1 | `AssertionError at tests/test_installer_pinokio_activation.py:341` | AssertionError: assert N == N | `tests/test_installer_pinokio_activation.py` (1) |
| C65 | 1 | `AssertionError at tests/test_installer_pinokio_activation.py:311` | assert [N] == [N, N] | `tests/test_installer_pinokio_activation.py` (1) |
| C66 | 1 | `AssertionError at tests/test_installer_pinokio_activation.py:335` | AssertionError: assert N == N | `tests/test_installer_pinokio_activation.py` (1) |
| C67 | 1 | `AssertionError at tests/test_installer_pinokio_activation.py:315` | AssertionError: assert N == N | `tests/test_installer_pinokio_activation.py` (1) |
| C68 | 1 | `ValueError at astrid/installer/backend.py:446` | ValueError: The manifest's lifecycle pin differs from the staged Agent's canonical pin. Manifest: repository < | `tests/test_installer_real_product_root.py` (1) |
| C69 | 1 | `no traceback | Failed: no Runtime checkout: set ASTRID_RUNTIME_CHECKOUT to one (looked at ['<path>` | Failed: no Runtime checkout: set ASTRID_RUNTIME_CHECKOUT to one (looked at ['<path> | `tests/timeline/test_authoring_media.py` (1) |
| C70 | 1 | `AssertionError at tests/upgrade/test_c1_product_gaps.py:46` | AssertionError: UPD: stale ASTRID_ACP_COMMAND survived into candidate declaration; old='<path> candidate='<pat | `tests/upgrade/test_c1_product_gaps.py` (1) |
| C71 | 1 | `no traceback | Failed: set ASTRID_RUNTIME_REPO to the local source checkout to run this offline check` | Failed: set ASTRID_RUNTIME_REPO to the local source checkout to run this offline check | `tests/upgrade/test_upgrade_release.py` (1) |
| C72 | 1 | `AssertionError at tests/v10/test_timelines_create.py:387` | AssertionError: ErrorObject(code='validation_error', message='Render and visualize could not open the timeline | `tests/v10/test_timelines_create.py` (1) |
| C73 | 1 | `AssertionError at tests/integrations/test_generic_host_remotion_render.py:249` | assert None is not None | `tests/integrations/test_generic_host_remotion_render.py` (1) |
| C74 | 1 | `AssertionError at tests/editing_conformance/test_occurrence_shared_d20.py:109` | AssertionError: Traceback (most recent call last): | `tests/editing_conformance/test_occurrence_shared_d20.py` (1) |
| C75 | 1 | `AssertionError at tests/editing_conformance/test_occurrence_shared_historical.py:270` | astrid.sdk.workspace_client.WorkspaceClientError: lost acknowledgement | `tests/editing_conformance/test_occurrence_shared_historical.py` (1) |
| C76 | 1 | `AssertionError at tests/editing_conformance/test_prepared_video_birth.py:273` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/editing_conformance/test_prepared_video_birth.py` (1) |
| C77 | 1 | `no traceback | Failed: dry run video-references runpod: exit N, expected N` | Failed: dry run video-references runpod: exit N, expected N | `tests/installed/test_installed_generation_package.py` (1) |
| C78 | 1 | `Failed via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/selectors.py:415` | Failed: Timeout (>N.Ns) from pytest-timeout. | `tests/integrations/test_command_count_capture.py` (1) |
| C79 | 1 | `AssertionError at tests/integrations/test_core_hivemind_installed.py:57` | AssertionError: this integration must use the running Python N.N | `tests/integrations/test_core_hivemind_installed.py` (1) |
| C80 | 1 | `AssertionError at tests/integrations/test_e2_publication_contract_roundtrip.py:141` | AssertionError: assert 'publication_contract.render' in {} | `tests/integrations/test_e2_publication_contract_roundtrip.py` (1) |
| C81 | 1 | `AssertionError at tests/integrations/test_generation_runtime_composition.py:1685` | astrid.core.execution.host_errors.HostError: undeclared secret environment variable 'FAL_KEY' | `tests/integrations/test_generation_runtime_composition.py` (1) |
| C82 | 1 | `AssertionError at tests/integrations/test_generation_runtime_composition.py:1937` | astrid.core.execution.host_errors.HostError: undeclared secret environment variable 'FAL_KEY' | `tests/integrations/test_generation_runtime_composition.py` (1) |
| C83 | 1 | `ConflictError at astrid-runtime/runtime_protocol/daemon.py:1076` | AssertionError: assert 'queued' != 'queued' | `tests/integrations/test_generic_host_activation_acceptance.py` (1) |
| C84 | 1 | `AssertionError at tests/integrations/test_generic_host_activation_acceptance.py:391` | AssertionError: assert [] == [_ParkedPackH...n_origins={})] | `tests/integrations/test_generic_host_activation_acceptance.py` (1) |
| C85 | 1 | `Failed at tests/integrations/test_generic_host_activation_acceptance.py:389` | Failed: DID NOT RAISE <class 'OSError'> | `tests/integrations/test_generic_host_activation_acceptance.py` (1) |
| C86 | 1 | `AssertionError at tests/integrations/test_generic_host_remotion_render.py:208` | assert None is not None | `tests/integrations/test_generic_host_remotion_render.py` (1) |
| C87 | 1 | `AssertionError at tests/integrations/test_managed_host_preparation.py:342` | AssertionError: {'capability_id': 'vibecomfy.run', 'capability_type': 'executor', 'native_kind': 'external', ' | `tests/integrations/test_managed_host_preparation.py` (1) |
| C88 | 1 | `AssertionError at tests/integrations/test_managed_host_preparation.py:703` | astrid.core.generation.engine_contracts.IntegrityError: managed alignment command failed (step=nodes_restore,  | `tests/integrations/test_managed_host_preparation.py` (1) |
| C89 | 1 | `AssertionError at tests/integrations/test_pinned_source_cpu.py:152` | AssertionError: assert N == N | `tests/integrations/test_pinned_source_cpu.py` (1) |
| C90 | 1 | `IntegrityError at astrid/core/generation/managed_preparation.py:553` | astrid.core.generation.engine_contracts.IntegrityError: managed engine does not load workflow classes even aft | `tests/integrations/test_pod_owned_preparation.py` (1) |
| C91 | 1 | `MissingRequiredEntryInputsError at astrid/core/generation/entries.py:825` | astrid.core.generation.entries.MissingRequiredEntryInputsError: missing required entry inputs: audio_ref | `tests/integrations/test_runpod_dry_live_seam.py` (1) |
| C92 | 1 | `AttributeError at astrid/sdk/media_handles.py:100` | AttributeError: 'types.SimpleNamespace' object has no attribute 'show' | `tests/integrations/test_runpod_dry_live_seam.py` (1) |
| C93 | 1 | `KeyError at tests/integrations/test_runpod_slot_path_cpu.py:296` | KeyError: ('audio', 'transcribe') | `tests/integrations/test_runpod_slot_path_cpu.py` (1) |
| C94 | 1 | `AssertionError at tests/integrations/test_runpod_slot_path_cpu.py:535` | AssertionError: GenerationReadinessError("'ComfyUI-HN-Motion-Context-MultiRef'") | `tests/integrations/test_runpod_slot_path_cpu.py` (1) |
| C95 | 1 | `AssertionError at tests/journeys/test_cross_client.py:139` | AssertionError: assert {'job.stderr'... 'video/webm'} == {'marker': 'i... 'video/webm'} | `tests/journeys/test_cross_client.py` (1) |
| C96 | 1 | `AssertionError at tests/journeys/test_journey_plumbing.py:222` | assert '"ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES", str(N * N**N)' in 'from __future__ import annotations\n\nimpor | `tests/journeys/test_journey_plumbing.py` (1) |
| C97 | 1 | `AssertionError at tests/packs/h3_av/test_character_swap_cpu_boundary.py:266` | AssertionError: assert (False) | `tests/packs/h3_av/test_character_swap_cpu_boundary.py` (1) |
| C98 | 1 | `RuntimeError at tests/helpers/h3_cpu_runtime.py:747` | RuntimeError: HN managed request import failed | `tests/packs/h3_av/test_character_swap_cpu_boundary.py` (1) |
| C99 | 1 | `SystemExit via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/argparse.py:2627` | argparse.ArgumentError: argument ACTION: invalid choice: 'hN_av.transform' (choose from ) | `tests/packs/h3_av/test_two_edit_cpu_qualification.py` (1) |
| C100 | 1 | `RenderExportRefused at astrid/packs/rendering/actions/render/task_adapter.py:466` | astrid.packs.rendering.actions.render.task_adapter.RenderExportRefused: render_export executor failed: executo | `tests/packs/rendering/test_render_export_task_adapter.py` (1) |
| C101 | 1 | `AssertionError at tests/packs/rendering/test_shot_layering_export.py:139` | AssertionError: assert ('@banodoco/t...on', 'N.N.N') == ('@banodoco/t...on', 'N.N.N') | `tests/packs/rendering/test_shot_layering_export.py` (1) |
| C102 | 1 | `AssertionError at tests/packs/rendering/test_timeline_transfer_actions.py:258` | AssertionError: ErrorObject(code='conflict', message='history_unavailable', details={'base': None, 'conflicts' | `tests/packs/rendering/test_timeline_transfer_actions.py` (1) |
| C103 | 1 | `AssertionError at tests/packs/runpod/test_worker_staging.py:951` | AssertionError: assert {'kind': 'run...account', ...} == {'kind': 'run...volume-test'}} | `tests/packs/runpod/test_worker_staging.py` (1) |
| C104 | 1 | `AssertionError at tests/packs/test_renderer_parity.py:652` | AssertionError: Remotion typecheck failed: | `tests/packs/test_renderer_parity.py` (1) |

## Failing IDs by test file

| IDs | Clusters | File |
| ---: | ---: | --- |
| 48 | 1 | `tests/editing_conformance/test_commit_runtime_occurrence_media.py` |
| 40 | 1 | `tests/editing_conformance/test_native_batch_ingress.py` |
| 38 | 1 | `tests/editing_conformance/test_commit_runtime_parent_media.py` |
| 38 | 1 | `tests/editing_conformance/test_native_word_anchor.py` |
| 27 | 1 | `tests/editing_conformance/test_authenticated_legacy_restore.py` |
| 24 | 1 | `tests/editing_conformance/test_commit_runtime_parent_media_swap.py` |
| 24 | 7 | `tests/core/test_timeline_element_publication_runtime.py` |
| 24 | 5 | `tests/integrations/test_generation_runtime_composition.py` |
| 23 | 1 | `tests/editing_conformance/test_word_binding_recipe.py` |
| 21 | 1 | `tests/core/execution/test_openai_child_admission.py` |
| 19 | 1 | `tests/editing_conformance/test_native_sheet_current_runtime.py` |
| 19 | 6 | `tests/integrations/test_managed_host_preparation.py` |
| 16 | 1 | `tests/editing_conformance/test_current_pair_reader.py` |
| 16 | 1 | `tests/packs/rendering/test_live_source_label_native.py` |
| 14 | 1 | `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py` |
| 14 | 2 | `tests/test_installer_pinokio_integration.py` |
| 14 | 1 | `tests/test_installer_pinokio_stopped_update.py` |
| 12 | 1 | `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` |
| 11 | 1 | `tests/editing_conformance/test_cli_first_media.py` |
| 11 | 2 | `tests/editing_conformance/test_next_command_cohort_runtime.py` |
| 10 | 1 | `tests/editing_conformance/test_commit_runtime_m1.py` |
| 10 | 5 | `tests/sdk/test_timeline_selected_schema_runtime.py` |
| 10 | 2 | `tests/packs/runpod/test_worker_staging.py` |
| 9 | 1 | `tests/editing_conformance/test_commit_runtime_shared_inverse.py` |
| 9 | 1 | `tests/sdk/test_timeline_capture_projection.py` |
| 9 | 1 | `tests/upgrade/test_busy_fixture_creation.py` |
| 9 | 1 | `tests/sdk/test_timeline_numeric_revision_runtime.py` |
| 9 | 2 | `tests/editing_conformance/test_owned_move_publish_runtime.py` |
| 8 | 1 | `tests/editing_conformance/test_timing_retained_inputs.py` |
| 7 | 1 | `tests/editing_conformance/test_inverse_stage_runtime_regressions.py` |
| 7 | 1 | `tests/editing_conformance/test_recipe_m2_shot_pool.py` |
| 7 | 3 | `tests/integrations/test_runpod_slot_path_cpu.py` |
| 6 | 1 | `tests/editing_conformance/test_commit_runtime_opaque_items.py` |
| 6 | 2 | `tests/editing_conformance/test_commit_runtime_numeric_params.py` |
| 6 | 1 | `tests/integrations/test_c06_public_timeline_visualizer.py` |
| 6 | 2 | `tests/test_onboarding_parity.py` |
| 6 | 2 | `tests/core/execution/test_generic_host_child_bridge_d18.py` |
| 6 | 1 | `tests/core/execution/test_m1_13_pack_provenance.py` |
| 6 | 1 | `tests/sdk/test_timeline_legacy_inverse_bindings.py` |
| 6 | 1 | `tests/editing_conformance/test_recipe_m2_auto_placement.py` |
| 6 | 1 | `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py` |
| 6 | 2 | `tests/packs/test_renderer_parity.py` |
| 5 | 1 | `tests/editing_conformance/test_historical_shared_redo_authority.py` |
| 4 | 1 | `tests/editing_conformance/test_commit_runtime_native_checkout.py` |
| 4 | 1 | `tests/editing_conformance/test_commit_runtime_video_unplace.py` |
| 4 | 1 | `tests/editing_conformance/test_native_checkout_current_equivalent.py` |
| 4 | 1 | `tests/sdk/test_timeline_checkout_history_runtime.py` |
| 4 | 2 | `tests/sdk/test_timeline_commit_provider_runtime.py` |
| 4 | 4 | `tests/test_installer_pinokio_activation.py` |
| 4 | 2 | `tests/timeline/test_authoring_media.py` |
| 4 | 1 | `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py` |
| 4 | 2 | `tests/integrations/test_dry_run_equals_live_run.py` |
| 4 | 1 | `tests/integrations/test_media_only_render_without_remotion.py` |
| 3 | 1 | `tests/editing_conformance/test_cli_trim_runtime.py` |
| 3 | 1 | `tests/editing_conformance/test_commit_runtime_identity.py` |
| 3 | 1 | `tests/editing_conformance/test_commit_runtime_native_frontends.py` |
| 3 | 1 | `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py` |
| 3 | 1 | `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py` |
| 3 | 1 | `tests/editing_conformance/test_commit_runtime_text_binding.py` |
| 3 | 2 | `tests/sdk/test_timeline_producer_guard_runtime.py` |
| 3 | 1 | `tests/test_installer_update_recovery.py` |
| 3 | 1 | `tests/editing_conformance/test_occurrence_hold_current_runtime.py` |
| 3 | 1 | `tests/editing_conformance/test_recipe_occurrence_media.py` |
| 3 | 2 | `tests/editing_conformance/test_occurrence_shared_historical.py` |
| 3 | 3 | `tests/integrations/test_generic_host_activation_acceptance.py` |
| 3 | 1 | `tests/packs/h3_av/test_static_mask_preflight.py` |
| 3 | 1 | `tests/packs/rendering/test_hyperframes_backend.py` |
| 3 | 1 | `tests/packs/runpod/test_https_transport.py` |
| 2 | 1 | `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py` |
| 2 | 1 | `tests/editing_conformance/test_commit_runtime_parent_track_label.py` |
| 2 | 1 | `tests/editing_conformance/test_m1_current_equivalent.py` |
| 2 | 1 | `tests/editing_conformance/test_commit_runtime_first_clip.py` |
| 2 | 1 | `tests/editing_conformance/test_commit_runtime_occurrence_create.py` |
| 2 | 2 | `tests/editing_conformance/test_commit_runtime_source_copy.py` |
| 2 | 1 | `tests/editing_conformance/test_historical_shared_inverse_owners.py` |
| 2 | 1 | `tests/core/generation/test_generate_target_journey.py` |
| 2 | 1 | `tests/core/generation/test_workflow_input_a01.py` |
| 2 | 1 | `tests/test_bootmanifest2_rollback.py` |
| 2 | 1 | `tests/sdk/test_timeline_checkout.py` |
| 2 | 1 | `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py` |
| 2 | 1 | `tests/test_installer_transaction_authority.py` |
| 2 | 1 | `tests/test_pinokio_switch_integration.py` |
| 2 | 2 | `tests/integrations/test_generic_host_remotion_render.py` |
| 2 | 1 | `tests/integrations/test_generic_host_runtime_restart.py` |
| 2 | 2 | `tests/integrations/test_pod_owned_preparation.py` |
| 2 | 2 | `tests/integrations/test_runpod_dry_live_seam.py` |
| 2 | 2 | `tests/packs/h3_av/test_character_swap_cpu_boundary.py` |
| 1 | 1 | `tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py` |
| 1 | 1 | `tests/editing_conformance/test_commit_runtime_scalar.py` |
| 1 | 1 | `tests/editing_conformance/test_m1_legacy_archive_read.py` |
| 1 | 1 | `tests/editing_conformance/test_cli_timeline_transfer.py` |
| 1 | 1 | `tests/editing_conformance/test_commit_runtime_occurrence_fork.py` |
| 1 | 1 | `tests/core/generation/test_engine_custody.py` |
| 1 | 1 | `tests/test_bootmanifest2_admission.py` |
| 1 | 1 | `tests/sdk/test_element_inverse_source_retention.py` |
| 1 | 1 | `tests/sdk/test_timeline_export.py` |
| 1 | 1 | `tests/sdk/test_timeline_import.py` |
| 1 | 1 | `tests/stage1/test_capability_parity_gate_luna.py` |
| 1 | 1 | `tests/stage1/test_media_handoff_render_boundary.py` |
| 1 | 1 | `tests/stage1/test_runtime_client_cutover.py` |
| 1 | 1 | `tests/test_installer_lifecycle.py` |
| 1 | 1 | `tests/test_installer_real_product_root.py` |
| 1 | 1 | `tests/upgrade/test_busy_fixture_release.py` |
| 1 | 1 | `tests/upgrade/test_c1_product_gaps.py` |
| 1 | 1 | `tests/upgrade/test_upgrade_release.py` |
| 1 | 1 | `tests/v10/test_timelines_create.py` |
| 1 | 1 | `tests/integrations/test_pinned_element_render_proof.py` |
| 1 | 1 | `tests/integrations/test_runpod_host_endpoint_r5.py` |
| 1 | 1 | `tests/editing_conformance/test_next_ordinary_union_runtime.py` |
| 1 | 1 | `tests/editing_conformance/test_occurrence_fork_source_baseline.py` |
| 1 | 1 | `tests/editing_conformance/test_occurrence_shared_d20.py` |
| 1 | 1 | `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` |
| 1 | 1 | `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` |
| 1 | 1 | `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` |
| 1 | 1 | `tests/editing_conformance/test_prepared_video_birth.py` |
| 1 | 1 | `tests/editing_conformance/test_s3_reviewed_cohort_runtime.py` |
| 1 | 1 | `tests/installed/test_installed_generation_package.py` |
| 1 | 1 | `tests/integrations/test_command_count_capture.py` |
| 1 | 1 | `tests/integrations/test_core_hivemind_installed.py` |
| 1 | 1 | `tests/integrations/test_e2_publication_contract_roundtrip.py` |
| 1 | 1 | `tests/integrations/test_pinned_source_cpu.py` |
| 1 | 1 | `tests/integrations/test_runpod_cpu_path.py` |
| 1 | 1 | `tests/journeys/test_cross_client.py` |
| 1 | 1 | `tests/journeys/test_journey_plumbing.py` |
| 1 | 1 | `tests/packs/h3_av/test_two_edit_cpu_qualification.py` |
| 1 | 1 | `tests/packs/rendering/test_render_export_task_adapter.py` |
| 1 | 1 | `tests/packs/rendering/test_shot_layering_export.py` |
| 1 | 1 | `tests/packs/rendering/test_timeline_transfer_actions.py` |
| 1 | 1 | `tests/packs/test_vibecomfy_import_generic_host.py` |
