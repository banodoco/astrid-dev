# Failure clusters — CI (unit shards; darwin native timed out with no result), release/15/main 514499de

1103 failing IDs in 419 clusters (grouped by exception type and raise site).

| # | IDs | Raise site | Top message | Top files |
| --- | ---: | --- | --- | --- |
| C1 | 98 | `AssertionError at tests/sdk/test_timeline_restructure.py:439` | AssertionError: assert PosixPath('<path> == PosixPath('<path> | `tests/sdk/test_timeline_helper_capture.py` (25), `tests/sdk/test_timeline_helper_normalization.py` (14) |
| C2 | 84 | `AssertionError at tests/sdk/test_timeline_editing_acceptance_runtime.py:33` | AssertionError: assert PosixPath('<path> == (PosixPath('<path> / 'runtime_protocol/timeline_commit_store.py') | `tests/sdk/test_timeline_editing_acceptance_runtime.py` (27), `tests/sdk/test_timeline_clash_back_runtime.py` (18) |
| C3 | 70 | `R0StopError at astrid/installer/core.py:651` | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the install line again. | `tests/test_installer_busy_fence.py` (54), `tests/test_local_install.py` (12) |
| C4 | 50 | `AssertionError at tests/core/pack/test_transaction.py:1939` | AssertionError: Browser transaction tests require explicit pinned local Node/esbuild inputs: ASTRID_BUILD_TEST | `tests/core/pack/test_transaction.py` (47), `tests/core/pack/test_build_hook_contract.py` (3) |
| C5 | 45 | `ModuleNotFoundError at tests/core/execution/test_runtime_source_custody_d40.py:30` | ModuleNotFoundError: No module named 'tests.test_verified_host_launch' | `tests/core/execution/test_runtime_source_custody_d40.py` (30), `tests/core/execution/test_runtime_orchestrator_custody_d40.py` (15) |
| C6 | 40 | `FileNotFoundError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/pathlib.py:1044` | FileNotFoundError: [Errno N] No such file or directory: '<path> | `tests/scripts/test_pod_bootstrap.py` (13), `tests/test_installer_acl.py` (8) |
| C7 | 35 | `no traceback | ` |  | `tests/packs/test_pack_run_cli_choices.py` (19), `tests/packs/test_pack_migration_m4_shells.py` (14) |
| C8 | 33 | `no traceback | KeyError: 'ASTRID_REMOTION_PROJECT_DIR'` | KeyError: 'ASTRID_REMOTION_PROJECT_DIR' | `tests/packs/rendering/test_normal_audio_run.py` (33) |
| C9 | 23 | `CalledProcessError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/subprocess.py:571` | subprocess.CalledProcessError: Command '['tar', '-xOf', '<path> 'package/dist/chunk-ANLVBEHN.js']' returned no | `tests/packs/rendering/test_remotion_layer_tail_compat.py` (11), `tests/editing_conformance/test_prepared_video_birth.py` (7) |
| C10 | 22 | `CommitRejected at astrid/sdk/timeline/commit.py:1590` | astrid.core.timeline.authoring_bundle.AuthoringBundleError: fork native binding schema changed | `tests/editing_conformance/test_fork_abi1_binding_set.py` (15), `tests/editing_conformance/test_recipe_occurrence_fork.py` (3) |
| C11 | 12 | `AssertionError at tests/core/pack/test_r8_prod_refusals.py:128` | AssertionError: RN-HN requires the pinned Node/esbuild environment from its run instructions | `tests/core/pack/test_r8_prod_refusals.py` (12) |
| C12 | 10 | `FileNotFoundError at astrid/core/product_resources.py:14` | FileNotFoundError: Astrid resource 'astrid-beta-capabilities.json' is missing; reinstall or update Astrid | `tests/stage1/test_pack_host_interpreter_identity.py` (10) |
| C13 | 10 | `ValueError at astrid/installer/backend.py:285` | FileNotFoundError: Astrid resource 'runtime.lock.json' is missing; reinstall or update Astrid | `tests/test_installer_platforms.py` (6), `tests/test_installer_schema.py` (3) |
| C14 | 10 | `SystemExit via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/argparse.py:2627` | argparse.ArgumentError: argument command: invalid choice: 'publish' (choose from 'import', 'export', 'checkout | `tests/packs/timeline/test_cli_status_publish.py` (7), `tests/test_skills_selected_composition.py` (1) |
| C15 | 8 | `AssertionError at tests/_checkouts.py:49` | AssertionError: The derived RunPod Lifecycle checkout is not a Git checkout; set ASTRID_RUNPOD_LIFECYCLE_CHECK | `tests/core/generation/test_engine_release.py` (8) |
| C16 | 8 | `AssertionError at tests/sdk/test_timeline_open_commit.py:78` | astrid.sdk.workspace_client.WorkspaceClientError: Runtime acceptance boundary | `tests/sdk/test_timeline_open_commit.py` (8) |
| C17 | 6 | `AssertionError at tests/test_installer_installed_schema.py:287` | assert N == N | `tests/test_installer_installed_schema.py` (6) |
| C18 | 6 | `RendererRegistryError at astrid/core/rendering/registry.py:384` | astrid.core.rendering.registry.RendererRegistryError: unknown renderer id 'rendering.remotion' | `tests/core/rendering/test_registry.py` (3), `tests/core/rendering/test_registry_matrix.py` (3) |
| C19 | 6 | `PackValidationError at astrid/core/pack/discovery.py:532` | astrid.core.pack._common.PackValidationError: duplicate pack id/directory name 'alpha' across <path> and <path | `tests/packs/test_pack_discovery_single_scan.py` (4), `tests/core/rendering/test_registry_matrix.py` (1) |
| C20 | 6 | `Failed at tests/packs/test_pack_discovery_single_scan.py:192` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/packs/test_pack_discovery_single_scan.py` (6) |
| C21 | 6 | `AssertionError at tests/scripts/test_pod_jobs.py:908` | assert N == N | `tests/scripts/test_pod_jobs.py` (6) |
| C22 | 6 | `AssertionError at tests/scripts/test_pod_jobs.py:1454` | assert N == N | `tests/scripts/test_pod_jobs.py` (6) |
| C23 | 6 | `AssertionError at tests/scripts/test_pod_jobs.py:1870` | AssertionError: assert (N - N) == (N - 'install' == 'uncertain' | `tests/scripts/test_pod_jobs.py` (6) |
| C24 | 5 | `CommitRejected at astrid/sdk/timeline/commit.py:1603` | astrid.sdk.timeline._command_state.CommandError: inverse stage image differs from authenticated effects | `tests/sdk/test_timeline_occurrence_delete_provider.py` (2), `tests/sdk/test_timeline_clip_scalar_provider.py` (2) |
| C25 | 5 | `no traceback | AssertionError: PackValidationError not raised` | AssertionError: PackValidationError not raised | `tests/packs/test_pack_discovery.py` (4), `tests/packs/test_pack_discovery_metadata.py` (1) |
| C26 | 5 | `AssertionError at tests/packs/timeline/test_verbs_working_copy.py:110` | AssertionError: assert <function _provided.<locals>.run at <addr>> is <function guard.<locals>.wrap.<locals>.r | `tests/packs/timeline/test_verbs_working_copy.py` (5) |
| C27 | 4 | `Failed at tests/core/generation/test_discovery_scope.py:138` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/core/generation/test_discovery_scope.py` (4) |
| C28 | 4 | `AssertionError at tests/test_installer_app_update.py:1644` | astrid.installer.core.VerificationError: Astrid's browser door did not become ready before the verification de | `tests/test_installer_app_update.py` (4) |
| C29 | 4 | `AssertionError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/unittest/mock.py:950` | AssertionError: Expected 'mock' to be called once. Called N times. | `tests/test_installer_busy_fence.py` (4) |
| C30 | 4 | `CapabilityNotFoundError at astrid/sdk/discovery.py:797` | KeyError: "unknown executor id 'understanding.audio_understand'" | `tests/test_live_capability_discovery_fix.py` (4) |
| C31 | 4 | `AssertionError at tests/editing_conformance/test_recipe_m2_video_unplace.py:84` | AssertionError: assert {'order': ['c...ip:placed'}]]} == {'order': ['c...ip:placed'}]]} | `tests/editing_conformance/test_recipe_m2_video_unplace.py` (4) |
| C32 | 4 | `AssertionError at tests/packs/test_portfolio_parity.py:125` | AssertionError: <path> vN manifest must not declare extensions: | `tests/packs/test_portfolio_parity.py` (4) |
| C33 | 4 | `AssertionError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/unittest/mock.py:1183` | AssertionError: unexpected endpoint operation | `tests/sdk/test_generation_verified_preparation_gr03.py` (4) |
| C34 | 3 | `ChildBridgeError at astrid/core/execution/_child_bridge.py:648` | astrid.core.execution._child_bridge.ChildBridgeError: child admission carries no source digest; refusing befor | `tests/core/execution/test_generic_host_child_bridge_d18.py` (3) |
| C35 | 3 | `AssertionError at tests/core/execution/test_generic_host_child_bridge_d18.py:787` | AssertionError: assert [] == ['upload'] | `tests/core/execution/test_generic_host_child_bridge_d18.py` (3) |
| C36 | 3 | `AssertionError at tests/core/execution/test_private_network_command.py:77` | ValueError: external command module is outside selected pack namespace | `tests/core/execution/test_private_network_command.py` (3) |
| C37 | 3 | `CommandError at astrid/sdk/timeline/_trim_commands.py:63` | astrid.sdk.timeline._command_state.CommandError: cannot source-trim an image: images have no source window | `tests/sdk/test_p1_case_corpus.py` (2), `tests/sdk/test_timeline_commit_provider.py` (1) |
| C38 | 3 | `AssertionError at tests/sdk/test_timeline_native_checkout.py:240` | AssertionError: assert {'app': {'cli...overlay', ...} == {'id': 'overl...le': 'output'} | `tests/sdk/test_timeline_native_checkout.py` (3) |
| C39 | 3 | `AssertionError at tests/test_generic_host.py:5092` | AssertionError: assert {'attempt_id'...uts': [], ...} == {'attempt_id'...': False, ...} | `tests/test_generic_host.py` (3) |
| C40 | 3 | `AssertionError at tests/test_installed_generation_journey.py:137` | AssertionError: Provision the existing installed lane before selecting it | `tests/test_installed_generation_journey.py` (3) |
| C41 | 3 | `AssertionError at tests/test_installer_app_update.py:1684` | astrid.installer.core.VerificationError: Astrid's browser door did not become ready before the verification de | `tests/test_installer_app_update.py` (3) |
| C42 | 3 | `no traceback | StopIteration` | StopIteration | `tests/test_skills_sync_registry.py` (3) |
| C43 | 3 | `AssertionError at tests/test_update_from_field_states.py:646` | AssertionError: ('not-updated', ['Astrid did NOT update. It is still Release N; Release N is available.', 'Why | `tests/test_update_from_field_states.py` (3) |
| C44 | 3 | `FileNotFoundError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/shutil.py:571` | FileNotFoundError: [Errno N] No such file or directory: '<path> | `tests/integrations/test_d09_managed_scene_only.py` (3) |
| C45 | 3 | `AssertionError at tests/packs/h3_av/test_no_astrid_imports.py:40` | AssertionError: assert [(N, 'astri...n.workflows')] == [] | `tests/packs/h3_av/test_no_astrid_imports.py` (3) |
| C46 | 3 | `AssertionError at tests/packs/test_pack_discovery_single_scan.py:168` | AssertionError: assert ['hivemind'] == ['alpha'] | `tests/packs/test_pack_discovery_single_scan.py` (3) |
| C47 | 3 | `AssertionError at tests/packs/test_portfolio_parity.py:92` | AssertionError: pack 'iteration' not discovered | `tests/packs/test_portfolio_parity.py` (3) |
| C48 | 3 | `AssertionError at tests/packs/test_portfolio_parity.py:105` | AssertionError: validate_pack reported errors for 'iteration': ['.: pack manifest not found (pack.yaml, pack.y | `tests/packs/test_portfolio_parity.py` (3) |
| C49 | 3 | `KeyError at astrid/core/execution/executor/registry.py:94` | KeyError: "unknown executor id 'iteration.assemble'" | `tests/packs/test_portfolio_parity.py` (3) |
| C50 | 3 | `AssertionError at tests/scripts/test_pod_jobs.py:291` | assert <hash> == (N * (N ** N)) | `tests/scripts/test_pod_jobs.py` (3) |
| C51 | 2 | `AssertionError at tests/core/generation/backends/test_qwen_21_turbo.py:185` | AssertionError: assert {'diffusion_m....safetensors'} == {'diffusion_m....safetensors'} | `tests/core/generation/backends/test_qwen_21_turbo.py` (2) |
| C52 | 2 | `OSError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/pathlib.py:1156` | OSError: [Errno N] Directory not empty: '<path> | `tests/core/generation/test_engine_fresh_install.py` (2) |
| C53 | 2 | `AssertionError at tests/core/generation/test_param_map_migration_parity.py:207` | AssertionError: [qwen-image-N.N-turbo-edit/edit/local] Manifest param_map keys not in DEFAULT_PARAM_MAP['edit' | `tests/core/generation/test_param_map_migration_parity.py` (2) |
| C54 | 2 | `KeyError at tests/test_diagnostics_callers.py:135` | KeyError: 'outcome' | `tests/test_diagnostics_callers.py` (2) |
| C55 | 2 | `HistoricalSourcePrerequisiteError at scripts/failure_mode_executor.py:190` | scripts.failure_mode_executor.HistoricalSourcePrerequisiteError: Historical release-N prerequisite missing: re | `tests/test_failure_mode_executor.py` (2) |
| C56 | 2 | `AssertionError at tests/test_installer_acl.py:70` | AssertionError: assert N == N | `tests/test_installer_acl.py` (2) |
| C57 | 2 | `AssertionError at tests/test_installer_acl.py:224` | AssertionError: assert N == N | `tests/test_installer_acl.py` (2) |
| C58 | 2 | `AssertionError at tests/test_installer_autostart.py:249` | AssertionError: assert not True | `tests/test_installer_autostart.py` (2) |
| C59 | 2 | `AttributeError at astrid/installer/installation.py:209` | AttributeError: 'Popen' object has no attribute 'home' | `tests/test_installer_launcher_repair.py` (2) |
| C60 | 2 | `AssertionError at tests/test_installer_release0_rollback.py:89` | AssertionError: Traceback (most recent call last): | `tests/test_installer_release0_rollback.py` (2) |
| C61 | 2 | `AssertionError at tests/test_installer_service_repair_integration.py:28` | AssertionError: Runtime service did not reach running: {} | `tests/test_installer_service_repair_integration.py` (2) |
| C62 | 2 | `R0StopError at astrid/installer/core.py:675` | astrid.installer.rN_stop.RNStopError: RN requires the copy-only upgrade boundary. Run the install line again. | `tests/test_installer_shim.py` (2) |
| C63 | 2 | `ValueError at astrid/installer/service.py:643` | ValueError: The Astrid sign-in task query was ambiguous or malformed. | `tests/test_installer_shim.py` (2) |
| C64 | 2 | `AssertionError at tests/test_installer_transaction_authority.py:694` | AssertionError: assert N == N | `tests/test_installer_transaction_authority.py` (2) |
| C65 | 2 | `AssertionError at tests/editing_conformance/test_fork_historical_source_boundary.py:53` | astrid.sdk.timeline._command_state.CommandError: missing or ambiguous identity 'shot-N' | `tests/editing_conformance/test_fork_historical_source_boundary.py` (2) |
| C66 | 2 | `AssertionError at tests/editing_conformance/test_headless_root_mirror_effects.py:98` | AssertionError: assert {'clips': [],...registry': {}} == {'clips': [],...registry': {}} | `tests/editing_conformance/test_headless_root_mirror_effects.py` (2) |
| C67 | 2 | `AssertionError at tests/editing_conformance/test_native_word_anchor_vectors.py:69` | AssertionError: assert {'clip': {'ap...act'}], ...}]} == {'clip': {'ap...act'}], ...}]} | `tests/editing_conformance/test_native_word_anchor_vectors.py` (2) |
| C68 | 2 | `RuntimeError at astrid/installer/core.py:698` | AttributeError: 'FakeBackend' object has no attribute 'remove_skills' | `tests/test_local_install.py` (2) |
| C69 | 2 | `KeyError at astrid/skills/__init__.py:120` | KeyError: "unknown pack(s): ['foley']" | `tests/test_skills_cli.py` (2) |
| C70 | 2 | `no traceback | AssertionError: False is not true` | AssertionError: False is not true | `tests/test_skills_sync_registry.py` (2) |
| C71 | 2 | `no traceback | AssertionError: unexpectedly None` | AssertionError: unexpectedly None | `tests/timeline/test_effects_catalog.py` (1), `tests/packs/rendering/test_remotion_element_generation.py` (1) |
| C72 | 2 | `AssertionError at tests/v10/test_pack_write_path_lint.py:62` | AssertionError: write-path lint did not scan every required source root | `tests/v10/test_pack_write_path_lint.py` (2) |
| C73 | 2 | `AssertionError at tests/core/generation/test_runpod_engine_selection.py:333` | AssertionError: assert ['hN', 'hN'] == ['hN'] | `tests/core/generation/test_runpod_engine_selection.py` (2) |
| C74 | 2 | `RemotionValidationError at astrid/core/rendering/remotion_runtime.py:907` | ValueError: registry source/interpreter differs | `tests/core/rendering/test_remotion_registry_context_key.py` (2) |
| C75 | 2 | `AssertionError at tests/core/rendering/test_remotion_runtime.py:374` | AssertionError: assert (not True) | `tests/core/rendering/test_remotion_runtime.py` (2) |
| C76 | 2 | `AssertionError at tests/packs/h3_av/test_edit_inputs.py:420` | AssertionError: assert {'bounded-mas...NbN', ...} == {'bounded-mas...NbN', ...} | `tests/packs/h3_av/test_edit_inputs.py` (2) |
| C77 | 2 | `ValueError at astrid/core/rendering/_effect_registry.py:187` | OSError: [Errno N] File name too long: "\nimport {DEFAULT_THEME} from '@banodoco/timeline-composition';\nimpor | `tests/packs/rendering/test_ffmpeg_support.py` (2) |
| C78 | 2 | `RuntimeErrorBase via astrid/sdk/timeline/commit.py:1101` | runtime_protocol.timeline_commit.CommitRejected: Refused: after this edit render and visualize cannot open the | `tests/sdk/test_inverse_removed_shot_owners_runtime.py` (2) |
| C79 | 2 | `no traceback | AssertionError: Lists differ: [] != ['builtin']` | AssertionError: Lists differ: [] != ['builtin'] | `tests/packs/test_pack_discovery.py` (2) |
| C80 | 2 | `no traceback | astrid.core.pack._common.PackValidationError: duplicate pack id 'local': pack 'local' conf` | astrid.core.pack._common.PackValidationError: duplicate pack id 'local': pack 'local' conflicts with a core pa | `tests/packs/test_pack_discovery_metadata.py` (2) |
| C81 | 2 | `no traceback | IndexError: tuple index out of range` | IndexError: tuple index out of range | `tests/packs/test_pack_discovery_metadata.py` (2) |
| C82 | 2 | `ValueError at tests/packs/test_pack_discovery_v3.py:90` | ValueError: not enough values to unpack (expected N, got N) | `tests/packs/test_pack_discovery_v3.py` (2) |
| C83 | 2 | `no traceback | FileNotFoundError: [Errno N] No such file or directory: '<path>` | FileNotFoundError: [Errno N] No such file or directory: '<path> | `tests/packs/test_packs_validate.py` (1), `tests/scripts/test_gpu_sanity.py` (1) |
| C84 | 2 | `AttributeError at tests/packs/timeline/test_cli_edit_flags.py:101` | AttributeError: 'function' object has no attribute '__wrapped__' | `tests/packs/timeline/test_cli_edit_flags.py` (2) |
| C85 | 2 | `Failed at tests/scripts/test_claim_runpod_5090_backup.py:1078` | Failed: DID NOT RAISE <class 'SystemExit'> | `tests/scripts/test_claim_runpod_5090_backup.py` (2) |
| C86 | 2 | `AssertionError at tests/scripts/test_pod_held_budget.py:236` | AssertionError: assert (N - N) == (N - N) | `tests/scripts/test_pod_held_budget.py` (2) |
| C87 | 2 | `AssertionError at tests/scripts/test_pod_jobs.py:561` | AssertionError: assert (N == N and N > N) | `tests/scripts/test_pod_jobs.py` (2) |
| C88 | 2 | `AssertionError at tests/scripts/test_pod_jobs.py:1165` | assert N == N | `tests/scripts/test_pod_jobs.py` (2) |
| C89 | 2 | `AssertionError at tests/sdk/test_runtime_response_conformance.py:138` | AssertionError: assert '/vN/projects...s/main/commit' == '/vN/projects...ion-revisions' | `tests/sdk/test_runtime_response_conformance.py` (2) |
| C90 | 2 | `CommandError at astrid/sdk/timeline/_appearance.py:100` | astrid.sdk.timeline._command_state.CommandError: timeline property output is incomplete; resolution, fps and f | `tests/sdk/test_timeline_capture_projection.py` (2) |
| C91 | 1 | `no traceback | tests/core/execution/test_host_cleanup_ack_barrier.py::test_native_exec_changes_token_with` | tests/core/execution/test_host_cleanup_ack_barrier.py::test_native_exec_changes_token_without_changing_process | `tests/core/execution/test_host_cleanup_ack_barrier.py` (1) |
| C92 | 1 | `Failed at tests/core/execution/test_bug14_settlement_liveness.py:221` | Failed: DID NOT RAISE <class 'RuntimeError'> | `tests/core/execution/test_bug14_settlement_liveness.py` (1) |
| C93 | 1 | `AssertionError at tests/core/execution/test_fail_closed_g28.py:213` | AssertionError: assert 'running' == 'failed' | `tests/core/execution/test_fail_closed_g28.py` (1) |
| C94 | 1 | `AssertionError at tests/core/execution/test_generic_host_actions_v3.py:130` | AssertionError: assert [] == ['unrelated.calculate'] | `tests/core/execution/test_generic_host_actions_v3.py` (1) |
| C95 | 1 | `Failed at tests/core/execution/test_generic_host_verified_preparation_gr03.py:187` | Failed: private producer submitted a provider request | `tests/core/execution/test_generic_host_verified_preparation_gr03.py` (1) |
| C96 | 1 | `CustodyError at astrid/core/execution/custody_broker.py:609` | astrid.core.execution.custody_broker.CustodyError: Darwin audit-token custody is unavailable | `tests/core/execution/test_host_cleanup_ack_barrier.py` (1) |
| C97 | 1 | `AssertionError at tests/core/execution/test_platform_boundary.py:70` | AssertionError: {'astrid/core/execution/generic_host.py': ['N: import fcntl', 'N: signal.SIGURG', 'N: signal.S | `tests/core/execution/test_platform_boundary.py` (1) |
| C98 | 1 | `HostError at astrid/core/execution/generic_host.py:10220` | ValueError: external command module is outside selected pack namespace | `tests/core/execution/test_private_network_command.py` (1) |
| C99 | 1 | `AssertionError at tests/core/generation/backends/test_qwen_21_turbo.py:155` | AssertionError: assert N == N | `tests/core/generation/backends/test_qwen_21_turbo.py` (1) |
| C100 | 1 | `AssertionError at tests/core/generation/backends/test_qwen_21_turbo.py:172` | AssertionError: assert {'vae/qwen_im....safetensors'} == {'diffusion_m....safetensors'} | `tests/core/generation/backends/test_qwen_21_turbo.py` (1) |
| C101 | 1 | `AssertionError at tests/core/generation/backends/test_qwen_21_turbo.py:212` | AssertionError: assert {'comfyui-whi...NeNbNb')} == {'comfyui-hun...NaN'), ...} | `tests/core/generation/backends/test_qwen_21_turbo.py` (1) |
| C102 | 1 | `AssertionError at tests/core/generation/test_cli_gold_075b.py:581` | AssertionError: exit N | `tests/core/generation/test_cli_gold_075b.py` (1) |
| C103 | 1 | `AssertionError at tests/core/generation/test_cli_gold_075b.py:609` | AssertionError: exit N | `tests/core/generation/test_cli_gold_075b.py` (1) |
| C104 | 1 | `AssertionError at tests/core/generation/test_discovery_scope.py:72` | AssertionError: assert N == N | `tests/core/generation/test_discovery_scope.py` (1) |
| C105 | 1 | `KeyError at tests/core/generation/test_discovery_scope.py:88` | KeyError: 'generation' | `tests/core/generation/test_discovery_scope.py` (1) |
| C106 | 1 | `AssertionError at tests/core/generation/test_discovery_scope.py:102` | AssertionError: assert [('hivemind',...d', 'source')] == [('bundled', ...rnal', 'env')] | `tests/core/generation/test_discovery_scope.py` (1) |
| C107 | 1 | `AssertionError at tests/core/generation/test_discovery_scope.py:177` | AssertionError: assert 'Hivemind' == 'Before' | `tests/core/generation/test_discovery_scope.py` (1) |
| C108 | 1 | `AssertionError at /home/runner/work/astrid-agent/astrid-agent/tests/core/generation/test_discovery_scope.py:189` | AssertionError: assert ['hivemind'] == ['local'] | `tests/core/generation/test_discovery_scope.py` (1) |
| C109 | 1 | `AssertionError at tests/core/generation/test_discovery_scope.py:205` | AssertionError: assert 'Hivemind' == 'Before' | `tests/core/generation/test_discovery_scope.py` (1) |
| C110 | 1 | `ValueError at astrid/core/model_catalog/schema.py:351` | ValueError: models[N].modes['tNi'].backends['studio']: unknown backend key; available backend ids: cloud, code | `tests/core/generation/test_discovery_scope.py` (1) |
| C111 | 1 | `AssertionError at tests/core/generation/test_edit_image_ref_admission.py:17` | AssertionError: { | `tests/core/generation/test_edit_image_ref_admission.py` (1) |
| C112 | 1 | `AssertionError at tests/core/generation/test_engine_error_reasons.py:55` | AssertionError: ('astrid/core/generation/engine_runner_target.py', N) | `tests/core/generation/test_engine_error_reasons.py` (1) |
| C113 | 1 | `AttributeError at tests/core/generation/test_generation_index.py:12` | AttributeError: module 'scripts.gen_capability_index' has no attribute '_generation_section' | `tests/core/generation/test_generation_index.py` (1) |
| C114 | 1 | `AssertionError at tests/core/generation/test_generation_index.py:20` | AssertionError: assert '<!-- BEGIN CAPABILITY INDEX (auto-generated by scripts/gen_capability_index.py) -->\n\ | `tests/core/generation/test_generation_index.py` (1) |
| C115 | 1 | `AssertionError at tests/core/generation/test_generation_setup_walk.py:99` | assert N == N | `tests/core/generation/test_generation_setup_walk.py` (1) |
| C116 | 1 | `PreparationError at astrid/packs/h3_av/shared/conform.py:206` | _hN_av_pack.shared.errors.PreparationError: output directory already exists | `tests/core/generation/test_h3_build_after_outputs.py` (1) |
| C117 | 1 | `AssertionError at tests/core/generation/test_listing.py:397` | AssertionError: assert ([{'availability': 'unavailable', 'backend': 'cloud', 'fix': 'use a qualified generatio | `tests/core/generation/test_listing.py` (1) |
| C118 | 1 | `AssertionError at tests/core/generation/test_moved_data_composition.py:448` | AssertionError: PosixPath('<path> | `tests/core/generation/test_moved_data_composition.py` (1) |
| C119 | 1 | `AssertionError at tests/core/generation/test_param_map_migration_parity.py:224` | AssertionError: [z-image/iNi/local] Remote-name mismatch: 'strength': manifest→'strength' vs default→'denoise' | `tests/core/generation/test_param_map_migration_parity.py` (1) |
| C120 | 1 | `AssertionError at tests/sdk/test_timeline_commit_provider.py:426` | AssertionError: assert {'commands': ...m': None, ...} == {'commands': ...m': None, ...} | `tests/sdk/test_timeline_commit_provider.py` (1) |
| C121 | 1 | `AssertionError at tests/sdk/test_timeline_commit_provider.py:897` | AssertionError: assert ModuleSpec(name='astrid.core.timeline.inverses', loader=<_frozen_importlib_external.Sou | `tests/sdk/test_timeline_commit_provider.py` (1) |
| C122 | 1 | `AssertionError at tests/sdk/test_timeline_current_union_schema.py:100` | assert {'$defs': {'A.../schema', ...} == {'$defs': {'A.../schema', ...} | `tests/sdk/test_timeline_current_union_schema.py` (1) |
| C123 | 1 | `AssertionError at tests/sdk/test_timeline_current_union_schema.py:109` | AssertionError: assert 'Replace an e... its element.' == 'Replace an e... its element.' | `tests/sdk/test_timeline_current_union_schema.py` (1) |
| C124 | 1 | `AssertionError at tests/sdk/test_timeline_current_union_schema.py:182` | assert {'$defs': {'A.../schema', ...} == {'$defs': {'A.../schema', ...} | `tests/sdk/test_timeline_current_union_schema.py` (1) |
| C125 | 1 | `AssertionError at tests/sdk/test_timeline_current_union_schema.py:196` | AssertionError: assert {'additionalP...bject'}}, ...} == {'additionalP...bject'}}, ...} | `tests/sdk/test_timeline_current_union_schema.py` (1) |
| C126 | 1 | `AssertionError at tests/sdk/test_timeline_film_length.py:61` | AssertionError: [] | `tests/sdk/test_timeline_film_length.py` (1) |
| C127 | 1 | `AssertionError at tests/sdk/test_timeline_native_checkout.py:247` | AssertionError: assert {'app': {'cli...Overlay', ...} == {'id': 'overl...e': 'Overlay'} | `tests/sdk/test_timeline_native_checkout.py` (1) |
| C128 | 1 | `AssertionError at tests/sdk/test_timeline_native_checkout.py:302` | AssertionError: assert 'overlay' == '' | `tests/sdk/test_timeline_native_checkout.py` (1) |
| C129 | 1 | `AssertionError at tests/sdk/test_timeline_open_commit_v2.py:941` | AssertionError: assert None | `tests/sdk/test_timeline_open_commit_v2.py` (1) |
| C130 | 1 | `AssertionError at tests/sdk/test_timeline_open_commit_v2.py:1199` | AssertionError: Run astrid timelines discard t --project p, then call tl.commit(fn, ...) again. | `tests/sdk/test_timeline_open_commit_v2.py` (1) |
| C131 | 1 | `CommitConflict at astrid/sdk/timeline/commit_session.py:1068` | astrid.sdk.timeline.sync.CommitConflict: The timeline changed since this edit was made; nothing was committed. | `tests/sdk/test_timeline_public_command.py` (1) |
| C132 | 1 | `AssertionError at tests/sdk/test_timeline_render_publication.py:170` | AssertionError: assert {'code': 'ass...invalid', ...} == {'code': 'pro...nds', N], ...} | `tests/sdk/test_timeline_render_publication.py` (1) |
| C133 | 1 | `AssertionError at tests/sdk/test_timeline_selected_param_authority.py:297` | astrid.sdk.timeline._command_state.CommandError: selected PARAM authority is unavailable | `tests/sdk/test_timeline_selected_param_authority.py` (1) |
| C134 | 1 | `AssertionError at tests/sdk/test_timeline_sheet_native.py:634` | astrid.sdk.timeline._common.TimelineEditError: idempotency key belongs to another edit; use a fresh key for ne | `tests/sdk/test_timeline_sheet_native.py` (1) |
| C135 | 1 | `AssertionError at tests/sdk/test_wc6_completion_capture.py:248` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/sdk/test_wc6_completion_capture.py` (1) |
| C136 | 1 | `AssertionError at tests/sdk/test_wc6_completion_capture.py:323` | AssertionError: assert 'timeline_outcome_unknown' == 'not_ready' | `tests/sdk/test_wc6_completion_capture.py` (1) |
| C137 | 1 | `AssertionError at tests/stage1/test_capability_parity_gate_luna.py:158` | assert N == N | `tests/stage1/test_capability_parity_gate_luna.py` (1) |
| C138 | 1 | `AssertionError at tests/stage1/test_generic_host_process_bootstrap_luna.py:54` | assert N > N | `tests/stage1/test_generic_host_process_bootstrap_luna.py` (1) |
| C139 | 1 | `AssertionError at tests/stage1/test_pack_api_surface.py:85` | AssertionError: API changed: bump VERSION and append a snapshot; never rewrite published history | `tests/stage1/test_pack_api_surface.py` (1) |
| C140 | 1 | `AssertionError at tests/stage1/test_vendored_workspace_client_parity_luna.py:76` | AssertionError: assert {'abandon_tas...ference', ...} == {'abandon_tas...ference', ...} | `tests/stage1/test_vendored_workspace_client_parity_luna.py` (1) |
| C141 | 1 | `AssertionError at tests/stage1/test_zero_shim_execution_pack_deletion.py:26` | AssertionError: assert not True | `tests/stage1/test_zero_shim_execution_pack_deletion.py` (1) |
| C142 | 1 | `ValueError at astrid/core/source_identity.py:89` | ValueError: installed Runtime origin differs or is missing: runtime_protocol | `tests/stage1/test_zero_shim_execution_pack_deletion.py` (1) |
| C143 | 1 | `AssertionError at tests/stage1/test_zero_shim_execution_pack_deletion.py:253` | AssertionError: assert [] == ['env_pack.demo'] | `tests/stage1/test_zero_shim_execution_pack_deletion.py` (1) |
| C144 | 1 | `AssertionError at tests/test_boundary_handoff.py:828` | assert 'Astrid did NOT update: the installer refused to continue' in "Astrid couldn't finish. Your work is kep | `tests/test_boundary_handoff.py` (1) |
| C145 | 1 | `AssertionError at tests/test_boundary_registration.py:488` | assert (N == N and 'registration needs recovery' in "Astrid couldn't finish. Your work is kept.\nAstrid was up | `tests/test_boundary_registration.py` (1) |
| C146 | 1 | `no traceback | AssertionError: 'editorial.transcribe' not found in mappingproxy({'hivemind.contribute': E` | AssertionError: 'editorial.transcribe' not found in mappingproxy({'hivemind.contribute': ExecutorDefinition(id | `tests/test_canonical_aliases.py` (1) |
| C147 | 1 | `no traceback | AssertionError: Items in the second set but not the first:` | AssertionError: Items in the second set but not the first: | `tests/test_canonical_aliases.py` (1) |
| C148 | 1 | `no traceback | AssertionError: Items in the first set but not the second:` | AssertionError: Items in the first set but not the second: | `tests/test_canonical_aliases.py` (1) |
| C149 | 1 | `no traceback | AssertionError: Tuples differ: ('imp[N chars]t', 'appearance', 'edit', 'assets', 'find', '` | AssertionError: Tuples differ: ('imp[N chars]t', 'appearance', 'edit', 'assets', 'find', 'a[N chars]der') != ( | `tests/test_canonical_aliases.py` (1) |
| C150 | 1 | `AssertionError at tests/test_canonical_entrypoint.py:112` | assert "'request': '<request>'" in "error: this pack (hN_av.transform) is not meant to be invoked directly; us | `tests/test_canonical_entrypoint.py` (1) |
| C151 | 1 | `AssertionError at tests/test_ci_journey.py:931` | RuntimeError: RUNNER_OS Linux disagrees with observed darwin | `tests/test_ci_journey.py` (1) |
| C152 | 1 | `AssertionError at tests/test_ci_journey.py:1270` | RuntimeError: RUNNER_OS Linux disagrees with observed winN | `tests/test_ci_journey.py` (1) |
| C153 | 1 | `AssertionError at tests/test_core_pack_boundary_guard.py:16` | AssertionError: core pack-boundary ratchet grew: | `tests/test_core_pack_boundary_guard.py` (1) |
| C154 | 1 | `AssertionError at tests/test_core_provider_neutrality.py:21` | assert False | `tests/test_core_provider_neutrality.py` (1) |
| C155 | 1 | `AssertionError at tests/test_core_util_surface.py:39` | AssertionError: assert ['astrid/core.../delivery.py'] == [] | `tests/test_core_util_surface.py` (1) |
| C156 | 1 | `AssertionError at tests/test_creator_entry_declarations.py:43` | assert None is not None | `tests/test_creator_entry_declarations.py` (1) |
| C157 | 1 | `AssertionError at tests/test_creator_entry_declarations.py:82` | AssertionError: fal: ['.: pack manifest not found (pack.yaml, pack.yml, or pack.json)'] | `tests/test_creator_entry_declarations.py` (1) |
| C158 | 1 | `no traceback | AssertionError: Bare os.environ string access for catalogued constants found in astrid/cor` | AssertionError: Bare os.environ string access for catalogued constants found in astrid/core/: | `tests/test_env_vars_conformance.py` (1) |
| C159 | 1 | `AssertionError at tests/test_external_app_contract.py:136` | AssertionError: External app exited N | `tests/test_external_app_contract.py` (1) |
| C160 | 1 | `AssertionError at tests/test_external_pack_contract.py:185` | AssertionError: External pack script exited N | `tests/test_external_pack_contract.py` (1) |
| C161 | 1 | `AssertionError at tests/test_failure_mode_executor.py:156` | AssertionError: assert 'Runtime' == 'Agent' | `tests/test_failure_mode_executor.py` (1) |
| C162 | 1 | `AssertionError at tests/test_failure_mode_executor.py:174` | AssertionError: assert 'Runtime' == 'Agent' | `tests/test_failure_mode_executor.py` (1) |
| C163 | 1 | `AssertionError at tests/test_failure_mode_executor.py:248` | AssertionError: assert 'Runtime' == 'Agent' | `tests/test_failure_mode_executor.py` (1) |
| C164 | 1 | `HostError at astrid/core/execution/generic_host.py:1483` | astrid.core.execution.host_errors.HostError: installed host VibeComfy checkout requires attested readiness | `tests/test_generic_host.py` (1) |
| C165 | 1 | `AssertionError at tests/test_generic_host.py:5136` | AssertionError: assert () == (PosixPath('/...trid/packs'),) | `tests/test_generic_host.py` (1) |
| C166 | 1 | `HostError at astrid/core/execution/generic_host.py:12091` | astrid.core.execution.host_errors.HostError: delegated child spec lacks admitted_source_digest; refusing befor | `tests/test_generic_host_result_json.py` (1) |
| C167 | 1 | `AssertionError at tests/test_gpu_journey_receipts.py:55` | AssertionError: ('RN', ('checks', 'one_runtime')) | `tests/test_gpu_journey_receipts.py` (1) |
| C168 | 1 | `ValueError at tests/test_installer_acl.py:351` | ValueError: not enough values to unpack (expected N, got N) | `tests/test_installer_acl.py` (1) |
| C169 | 1 | `AssertionError at tests/test_installer_app_update.py:1719` | astrid.installer.core.VerificationError: Astrid's browser door did not become ready before the verification de | `tests/test_installer_app_update.py` (1) |
| C170 | 1 | `AssertionError at tests/test_installer_bootstrap_imports.py:33` | AssertionError: ('cli.py', N, 'astrid.core.contracts.errors') | `tests/test_installer_bootstrap_imports.py` (1) |
| C171 | 1 | `AssertionError at tests/test_installer_busy_fence.py:270` | assert 'Astrid is busy (N tasks running). Try again when they finish.' in "Astrid will restart to update.\nAst | `tests/test_installer_busy_fence.py` (1) |
| C172 | 1 | `AssertionError at tests/test_installer_installed_schema.py:200` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/test_installer_installed_schema.py` (1) |
| C173 | 1 | `ValueError at tests/test_installer_installed_schema.py:419` | ValueError: not enough values to unpack (expected N, got N) | `tests/test_installer_installed_schema.py` (1) |
| C174 | 1 | `ValueError at tests/test_installer_installed_schema.py:430` | ValueError: not enough values to unpack (expected N, got N) | `tests/test_installer_installed_schema.py` (1) |
| C175 | 1 | `AttributeError at astrid/installer/core.py:218` | AttributeError: '_Backend' object has no attribute 'run' | `tests/test_installer_launchd_cache_window.py` (1) |
| C176 | 1 | `Failed at tests/test_installer_launchd_stop_handoff.py:323` | Failed: DID NOT RAISE any of (<class 'RuntimeError'>, <class 'astrid.installer.core.VerificationError'>) | `tests/test_installer_launchd_stop_handoff.py` (1) |
| C177 | 1 | `RuntimeOperationError at astrid/installer/backend.py:1257` | astrid_runtime.bootstrap.BootstrapError: Runtime interruption refused: owner endpoint or process identity fail | `tests/test_installer_lifecycle.py` (1) |
| C178 | 1 | `AssertionError at tests/test_installer_local_update.py:427` | astrid.installer.rN_stop.RNStopError: An interrupted legacy RN update is retained. Automatic in-place restore  | `tests/test_installer_local_update.py` (1) |
| C179 | 1 | `AssertionError at tests/test_installer_pinokio_lifecycle.py:433` | assert N == N | `tests/test_installer_pinokio_lifecycle.py` (1) |
| C180 | 1 | `AssertionError at tests/test_installer_pinokio_lifecycle.py:457` | AssertionError: assert N == N | `tests/test_installer_pinokio_lifecycle.py` (1) |
| C181 | 1 | `AssertionError at tests/test_installer_pinokio_lifecycle.py:472` | AssertionError: assert N == N | `tests/test_installer_pinokio_lifecycle.py` (1) |
| C182 | 1 | `AssertionError at tests/test_installer_pinokio_lifecycle.py:567` | AssertionError: assert N == N | `tests/test_installer_pinokio_lifecycle.py` (1) |
| C183 | 1 | `AssertionError at tests/test_installer_pinokio_lifecycle.py:611` | AssertionError: assert N == N | `tests/test_installer_pinokio_lifecycle.py` (1) |
| C184 | 1 | `no traceback | tests/test_installer_rN_entry.py::test_captures_match_real_rN_evidence: undeclared skip (S` | tests/test_installer_rN_entry.py::test_captures_match_real_rN_evidence: undeclared skip (Skipped: local RN evi | `tests/test_installer_r0_entry.py` (1) |
| C185 | 1 | `AssertionError at tests/test_installer_update_legacy_record.py:107` | AssertionError: assert 'recovery-needed' == 'failed' | `tests/test_installer_update_legacy_record.py` (1) |
| C186 | 1 | `AssertionError at tests/editing_conformance/test_fork_abi1_binding_set.py:84` | AssertionError: assert [{'dependenci... N, ...}, ...] == [{'dependenci...rence:occ-N'}] | `tests/editing_conformance/test_fork_abi1_binding_set.py` (1) |
| C187 | 1 | `AssertionError at tests/editing_conformance/test_producer_insertion.py:530` | AssertionError: assert [{'bindings':...xact'}], ...}] == [{'bindings':...xact'}], ...}] | `tests/editing_conformance/test_producer_insertion.py` (1) |
| C188 | 1 | `AssertionError at tests/editing_conformance/test_recipe_m2_clip_trim.py:191` | assert (N.N, N, N, N) == (N, N, N, N) | `tests/editing_conformance/test_recipe_m2_clip_trim.py` (1) |
| C189 | 1 | `no traceback | tests/test_journey_diagnostic_checkpoint.py::test_native_windows_locked_owner_file_is_not_` | tests/test_journey_diagnostic_checkpoint.py::test_native_windows_locked_owner_file_is_not_read: undeclared ski | `tests/test_journey_diagnostic_checkpoint.py` (1) |
| C190 | 1 | `no traceback | tests/test_journey_windows_acl_capture.py::test_windows_explicit_users_ace_and_hardlink: u` | tests/test_journey_windows_acl_capture.py::test_windows_explicit_users_ace_and_hardlink: undeclared skip (Skip | `tests/test_journey_windows_acl_capture.py` (1) |
| C191 | 1 | `no traceback | tests/test_journey_diagnostic_checkpoint.py::test_real_rN_realm_checkpoint_when_runtime_ch` | tests/test_journey_diagnostic_checkpoint.py::test_real_rN_realm_checkpoint_when_runtime_checkout_available: un | `tests/test_journey_diagnostic_checkpoint.py` (1) |
| C192 | 1 | `AssertionError at tests/test_n1_permission_boundary_guard.py:59` | AssertionError: assert ['astrid/core...s-imode', ...] == [] | `tests/test_n1_permission_boundary_guard.py` (1) |
| C193 | 1 | `AssertionError at tests/test_omp_agent.py:146` | AssertionError: assert (True and False) | `tests/test_omp_agent.py` (1) |
| C194 | 1 | `AssertionError at tests/test_omp_agent.py:159` | assert '<path> in "Custom guidance\n\nHivemind contributor login status: not logged in. Public Hivemind search | `tests/test_omp_agent.py` (1) |
| C195 | 1 | `AssertionError at tests/test_omp_agent.py:463` | assert '{\n  "entry"...d": null\n}\n' == '' | `tests/test_omp_agent.py` (1) |
| C196 | 1 | `AssertionError at tests/test_onboarding_one_home.py:208` | AssertionError: astrid/packs/runpod/docs/SKILL.md:N: Opt in to full per-job re-verification with `"models": {" | `tests/test_onboarding_one_home.py` (1) |
| C197 | 1 | `no traceback | AssertionError: 'Astrid command gateway' not found in 'usage: astrid [COMMAND] [OPTIONS]\n` | AssertionError: 'Astrid command gateway' not found in 'usage: astrid [COMMAND] [OPTIONS]\n\nAstrid: make and e | `tests/test_pipeline_dispatch_aliases.py` (1) |
| C198 | 1 | `AssertionError at tests/test_platform_matrix.py:20` | AssertionError: matrix cell lacks file:line evidence:  RunPod machine route: `generate video --entry hN --plac | `tests/test_platform_matrix.py` (1) |
| C199 | 1 | `IndexError at tests/test_provider_route_grant.py:183` | IndexError: tuple index out of range | `tests/test_provider_route_grant.py` (1) |
| C200 | 1 | `AssertionError at tests/test_public_boundary.py:164` | assert 'unstructured...oundError"}\n' == '' | `tests/test_public_boundary.py` (1) |
| C201 | 1 | `AssertionError at tests/test_recoverability_conformance.py:520` | AssertionError: Recoverability conformance scanner found findings that must be addressed: | `tests/test_recoverability_conformance.py` (1) |
| C202 | 1 | `AssertionError at tests/test_sdk_public_surface.py:3238` | astrid.sdk.exceptions.CapabilityPreconditionError: project is required for generation; pass --project <project | `tests/test_sdk_public_surface.py` (1) |
| C203 | 1 | `AssertionError at tests/test_skills_developer.py:56` | assert 'developer' in ('_core', 'rendering', 'setup', 'timeline', 'vibecomfy') | `tests/test_skills_developer.py` (1) |
| C204 | 1 | `AssertionError at tests/test_skills_developer.py:82` | AssertionError: assert False | `tests/test_skills_developer.py` (1) |
| C205 | 1 | `AssertionError at tests/test_skills_developer.py:136` | AssertionError: assert False | `tests/test_skills_developer.py` (1) |
| C206 | 1 | `AssertionError at tests/test_skills_installed_composition.py:228` | AssertionError: PosixPath('<path> | `tests/test_skills_installed_composition.py` (1) |
| C207 | 1 | `AssertionError at tests/test_skills_package_data.py:78` | AssertionError: assert {'media', 'understanding'} <= {'_core', 're..., 'vibecomfy'} | `tests/test_skills_package_data.py` (1) |
| C208 | 1 | `StopIteration at tests/test_skills_selected_composition.py:35` | StopIteration | `tests/test_skills_selected_composition.py` (1) |
| C209 | 1 | `TypeError at tests/test_skills_selected_composition.py:95` | TypeError: generate() got an unexpected keyword argument 'selected_pack_ids' | `tests/test_skills_selected_composition.py` (1) |
| C210 | 1 | `no traceback | AssertionError: '`astrid-foley`' not found in '---\nname: "astrid"\nshort_description: "gw` | AssertionError: '`astrid-foley`' not found in '---\nname: "astrid"\nshort_description: "gw"\n---\n\n# Astrid\n | `tests/test_skills_sync_registry.py` (1) |
| C211 | 1 | `AssertionError at tests/test_skip_policy.py:82` | AssertionError: mark the test with a lane from tests/lanes.py instead of skipping by hand: tests/core/executio | `tests/test_skip_policy.py` (1) |
| C212 | 1 | `AssertionError at tests/test_structure_contracts.py:787` | AssertionError: Unexpected top-level .py file: astrid/console.py | `tests/test_structure_contracts.py` (1) |
| C213 | 1 | `AssertionError at tests/test_structure_contracts.py:1009` | AssertionError: Files over N lines missing from giant-file-rationale.md: ['astrid/core/cli/domain_timelines.py | `tests/test_structure_contracts.py` (1) |
| C214 | 1 | `KeyError at tests/test_third_party_integration.py:51` | KeyError: 'third_party_backend' | `tests/test_third_party_integration.py` (1) |
| C215 | 1 | `KeyError at astrid/core/generation/backends/registry.py:133` | KeyError: 'synth' | `tests/test_third_party_integration.py` (1) |
| C216 | 1 | `ElementRegistryError at astrid/core/pack/registry.py:147` | astrid.core.element.registry.ElementRegistryError: element kind must be one of [effects, animations, transitio | `tests/test_third_party_integration.py` (1) |
| C217 | 1 | `ImportError at tests/test_timeline_editing_helpers.py:183` | ImportError: cannot import name 'retime_with_ripple' from 'astrid.sdk.timeline_editing' (<path> | `tests/test_timeline_editing_helpers.py` (1) |
| C218 | 1 | `ImportError at tests/test_timeline_editing_helpers.py:205` | ImportError: cannot import name 'retime' from 'astrid.sdk.timeline_editing' (<path> | `tests/test_timeline_editing_helpers.py` (1) |
| C219 | 1 | `ImportError at tests/test_timeline_editing_helpers.py:226` | ImportError: cannot import name 'retime_with_ripple' from 'astrid.sdk.timeline_editing' (<path> | `tests/test_timeline_editing_helpers.py` (1) |
| C220 | 1 | `AssertionError at tests/test_update_from_field_states.py:597` | AssertionError: assert 'Details: see... this window.' == 'Details: sho...as not used).' | `tests/test_update_from_field_states.py` (1) |
| C221 | 1 | `ImportError at tests/timeline/test_authoring_bundle.py:1980` | ImportError: cannot import name 'promote_approved_authoring_candidate' from 'astrid.core.timeline.authoring_bu | `tests/timeline/test_authoring_bundle.py` (1) |
| C222 | 1 | `no traceback | AssertionError: "EFFECT_IDS = ['am-burst', 'am-callout', 'am-churn', 'am-discord', 'am-dro` | AssertionError: "EFFECT_IDS = ['am-burst', 'am-callout', 'am-churn', 'am-discord', 'am-droste', 'am-flap', 'am | `tests/timeline/test_effects_catalog.py` (1) |
| C223 | 1 | `no traceback | AssertionError: PosixPath('<path> chars]ard') != PosixPath('<path> chars]ard')` | AssertionError: PosixPath('<path> chars]ard') != PosixPath('<path> chars]ard') | `tests/timeline/test_html_canvas_effect.py` (1) |
| C224 | 1 | `ImportError at tests/timeline/test_shot_composition_projection.py:320` | ImportError: cannot import name '_track_merge' from 'astrid.core.timeline.shot_composition_projection' (<path> | `tests/timeline/test_shot_composition_projection.py` (1) |
| C225 | 1 | `AssertionError at tests/timeline/test_shot_layering_projection.py:34` | assert b'{\n  "$sche...  }\n  ]\n}\n' == b'{"$schema":..."top-first"}}' | `tests/timeline/test_shot_layering_projection.py` (1) |
| C226 | 1 | `no traceback | ValueError: element kind must be one of [effects, animations, transitions]` | ValueError: element kind must be one of [effects, animations, transitions] | `tests/timeline/test_timeline_elements_catalog.py` (1) |
| C227 | 1 | `AssertionError at tests/v10/test_authority_lint.py:1125` | assert ('astrid/core...exempt)', ...) == () | `tests/v10/test_authority_lint.py` (1) |
| C228 | 1 | `KeyError at tests/v10/test_docs_cli_alignment.py:216` | KeyError: 'generate' | `tests/v10/test_docs_cli_alignment.py` (1) |
| C229 | 1 | `AssertionError at tests/v10/test_docs_cli_alignment.py:408` | AssertionError: SKILL.md contains 'astrid status' | `tests/v10/test_docs_cli_alignment.py` (1) |
| C230 | 1 | `AssertionError at tests/v10/test_docs_cli_alignment.py:419` | AssertionError: astrid/packs/_core/docs/SKILL.md: 'astrid status' | `tests/v10/test_docs_cli_alignment.py` (1) |
| C231 | 1 | `ServiceUnavailableError at astrid/sdk/client.py:356` | astrid.core.execution.network_policy.NetworkPolicyError: network policy denied dns destination N.N.N.N | `tests/v10/test_domain_cli_projects_timelines.py` (1) |
| C232 | 1 | `AssertionError at tests/v10/test_release_reproducibility.py:51` | AssertionError: assert not ({'runpod', 'runpod-lifecycle'} & dict_keys(['agent-detector', 'aiodns', 'aiofiles' | `tests/v10/test_release_reproducibility.py` (1) |
| C233 | 1 | `no traceback | tests/core/generation/test_release_python.py::test_real_recipe_bootstrap_reaches_managed_c` | tests/core/generation/test_release_python.py::test_real_recipe_bootstrap_reaches_managed_cpython_N_N_N: undecl | `tests/core/generation/test_release_python.py` (1) |
| C234 | 1 | `AssertionError at tests/core/generation/test_public_route_guard.py:271` | assert ["public Gene...'], found=[]"] == [] | `tests/core/generation/test_public_route_guard.py` (1) |
| C235 | 1 | `AssertionError at tests/core/generation/test_public_route_guard.py:284` | assert N == N | `tests/core/generation/test_public_route_guard.py` (1) |
| C236 | 1 | `IndexError at tests/core/generation/test_public_route_guard.py:292` | IndexError: list index out of range | `tests/core/generation/test_public_route_guard.py` (1) |
| C237 | 1 | `AssertionError at tests/core/generation/test_readiness_inputs_f04.py:322` | assert False | `tests/core/generation/test_readiness_inputs_f04.py` (1) |
| C238 | 1 | `AttributeError at astrid/core/generation/entries.py:1255` | AttributeError: 'types.SimpleNamespace' object has no attribute 'kind' | `tests/core/generation/test_readiness_inputs_f04.py` (1) |
| C239 | 1 | `AssertionError at tests/core/generation/test_run_local.py:285` | AssertionError: assert ['astrid/core...n/entries.py'] == [] | `tests/core/generation/test_run_local.py` (1) |
| C240 | 1 | `AssertionError at tests/core/generation/test_runpod_engine_selection.py:378` | AssertionError: assert ['hN', 'hN'] == ['hN'] | `tests/core/generation/test_runpod_engine_selection.py` (1) |
| C241 | 1 | `AttributeError at astrid/core/generation/backends/comfy_target.py:721` | AttributeError: 'types.SimpleNamespace' object has no attribute 'folder_paths' | `tests/core/generation/test_trusted_inventory.py` (1) |
| C242 | 1 | `KeyError at /home/runner/work/astrid-agent/astrid-agent/tests/core/generation/test_warm_models_remain_loaded.py:49` | KeyError: 'ckpt_name' | `tests/core/generation/test_warm_models_remain_loaded.py` (1) |
| C243 | 1 | `no traceback | ValueError: models[N].modes['tNi'].backends['studio']: unknown backend key; available back` | ValueError: models[N].modes['tNi'].backends['studio']: unknown backend key; available backend ids: cloud, code | `tests/core/model_catalog/test_registry.py` (1) |
| C244 | 1 | `AssertionError at tests/core/pack/test_v3_core_worker_luna.py:53` | AssertionError: assert [] == ['good'] | `tests/core/pack/test_v3_core_worker_luna.py` (1) |
| C245 | 1 | `StopIteration at tests/core/rendering/test_installed_registry_security.py:337` | StopIteration | `tests/core/rendering/test_installed_registry_security.py` (1) |
| C246 | 1 | `AssertionError at tests/core/rendering/test_production_callers.py:190` | AssertionError: render.run references found outside the allowlist (N): | `tests/core/rendering/test_production_callers.py` (1) |
| C247 | 1 | `FinalizerRegistryError at astrid/core/rendering/registry.py:384` | astrid.core.rendering.registry.FinalizerRegistryError: unknown finalizer id 'rendering.ffmpeg-finalizer' | `tests/core/rendering/test_registry.py` (1) |
| C248 | 1 | `AssertionError at tests/core/rendering/test_registry.py:191` | AssertionError: assert 'Extra Shadow' == 'Source Winner' | `tests/core/rendering/test_registry.py` (1) |
| C249 | 1 | `IndexError at tests/core/rendering/test_registry.py:210` | IndexError: tuple index out of range | `tests/core/rendering/test_registry.py` (1) |
| C250 | 1 | `Failed at tests/core/rendering/test_registry.py:226` | Failed: DID NOT RAISE <class 'astrid.core.rendering.registry.RendererRegistryError'> | `tests/core/rendering/test_registry.py` (1) |
| C251 | 1 | `Failed at tests/core/rendering/test_registry.py:262` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/core/rendering/test_registry.py` (1) |
| C252 | 1 | `Failed at tests/core/rendering/test_registry.py:290` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/core/rendering/test_registry.py` (1) |
| C253 | 1 | `Failed at tests/core/rendering/test_registry.py:319` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/core/rendering/test_registry.py` (1) |
| C254 | 1 | `Failed at tests/core/rendering/test_registry.py:351` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/core/rendering/test_registry.py` (1) |
| C255 | 1 | `IndexError at tests/core/rendering/test_registry.py:462` | IndexError: tuple index out of range | `tests/core/rendering/test_registry.py` (1) |
| C256 | 1 | `Failed at tests/core/rendering/test_registry.py:488` | Failed: DID NOT RAISE <class 'astrid.core.rendering.registry.RendererRegistryError'> | `tests/core/rendering/test_registry.py` (1) |
| C257 | 1 | `AssertionError at tests/core/rendering/test_registry_matrix.py:252` | AssertionError: assert 'Extra Shadow' == 'Source Winner' | `tests/core/rendering/test_registry_matrix.py` (1) |
| C258 | 1 | `Failed at tests/core/rendering/test_registry_matrix.py:291` | Failed: DID NOT RAISE <class 'astrid.core.rendering.registry.RendererRegistryError'> | `tests/core/rendering/test_registry_matrix.py` (1) |
| C259 | 1 | `AssertionError at tests/core/rendering/test_registry_matrix.py:362` | AssertionError: assert [] == ['aaaalpha.re...ega.renderer'] | `tests/core/rendering/test_registry_matrix.py` (1) |
| C260 | 1 | `Failed at tests/core/rendering/test_registry_matrix.py:438` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/core/rendering/test_registry_matrix.py` (1) |
| C261 | 1 | `IndexError at tests/core/rendering/test_registry_matrix.py:504` | IndexError: tuple index out of range | `tests/core/rendering/test_registry_matrix.py` (1) |
| C262 | 1 | `IndexError at tests/core/rendering/test_remotion_runtime.py:301` | IndexError: list index out of range | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C263 | 1 | `AssertionError at tests/core/rendering/test_remotion_runtime.py:319` | AssertionError: runtime validation needs an explicit absolute HOME | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C264 | 1 | `AssertionError at tests/core/rendering/test_remotion_runtime.py:396` | FileNotFoundError: [Errno N] No such file or directory: '<path> | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C265 | 1 | `AssertionError at tests/core/rendering/test_remotion_runtime.py:487` | subprocess.TimeoutExpired: Command 'node' timed out after N seconds | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C266 | 1 | `AttributeError at tests/core/rendering/test_remotion_runtime.py:507` | AttributeError: module 'astrid.core.rendering.remotion_runtime' has no attribute '_probe_schema' | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C267 | 1 | `AttributeError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/windows_security.py:40` | AttributeError: module 'ctypes' has no attribute 'WinDLL' | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C268 | 1 | `AssertionError at tests/core/rendering/test_remotion_runtime.py:574` | AssertionError: Traceback (most recent call last): | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C269 | 1 | `FileNotFoundError via /opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/pathlib.py:1147` | FileNotFoundError: [Errno N] No such file or directory: '<path> | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C270 | 1 | `AssertionError at tests/core/rendering/test_remotion_runtime.py:616` | assert not True | `tests/core/rendering/test_remotion_runtime.py` (1) |
| C271 | 1 | `no traceback | AssertionError: Lists differ: [] != [('widgets', 'glow', 'pack:demo')]` | AssertionError: Lists differ: [] != [('widgets', 'glow', 'pack:demo')] | `tests/core/test_element_kind_registry.py` (1) |
| C272 | 1 | `no traceback | AssertionError: 'element kind must be one of [effects, animations, transitions, widgets]' ` | AssertionError: 'element kind must be one of [effects, animations, transitions, widgets]' not found in 'elemen | `tests/core/test_elements_cli.py` (1) |
| C273 | 1 | `no traceback | AssertionError: Lists differ: [] != ['glow']` | AssertionError: Lists differ: [] != ['glow'] | `tests/core/test_elements_cli.py` (1) |
| C274 | 1 | `no traceback | AssertionError: N != N : element kind must be one of [effects, animations, transitions]` | AssertionError: N != N : element kind must be one of [effects, animations, transitions] | `tests/core/test_elements_cli.py` (1) |
| C275 | 1 | `no traceback | AssertionError: ExecutorRegistryError not raised` | AssertionError: ExecutorRegistryError not raised | `tests/core/test_executor_registry_snapshot.py` (1) |
| C276 | 1 | `AssertionError at tests/core/test_generation_backend_registry.py:398` | AssertionError: assert GenerationBackendDescriptor(backend_id='placement-probe', module='never_import', class_ | `tests/core/test_generation_backend_registry.py` (1) |
| C277 | 1 | `AssertionError at tests/core/test_generation_taxonomy_registry.py:96` | AssertionError: assert 'vendor_mask_ref' in ('prompt', 'negative_prompt', 'seed', 'count', 'size', 'image_ref' | `tests/core/test_generation_taxonomy_registry.py` (1) |
| C278 | 1 | `AssertionError at tests/core/test_pack_coherence_elements.py:68` | assert N == N | `tests/core/test_pack_coherence_elements.py` (1) |
| C279 | 1 | `Failed at tests/core/timeline/test_clip_fields.py:416` | Failed: DID NOT RAISE any of (<class 'ValueError'>, <class 'jsonschema.exceptions.ValidationError'>) | `tests/core/timeline/test_clip_fields.py` (1) |
| C280 | 1 | `AssertionError at tests/editing_conformance/test_compile_contracts.py:451` | AssertionError: assert {'app': {'ast... N}}}, ...} == {'app': {'ast... N}}}, ...} | `tests/editing_conformance/test_compile_contracts.py` (1) |
| C281 | 1 | `AstridError at astrid/packs/generation/actions/generate_image/run.py:214` | astrid.core.contracts.errors.AstridError: Codex backend requested but unavailable (`codex` binary not found on | `tests/packs/builtin/generate_image/test_codex_backend.py` (1) |
| C282 | 1 | `AstridError at astrid/core/generation/availability.py:189` | astrid.core.contracts.errors.AstridError: training.checkpoint_review_sampler: Training checkpoint review sampl | `tests/packs/builtin/test_training_run_ai_toolkit_support.py` (1) |
| C283 | 1 | `AssertionError at tests/packs/builtin/test_training_run_seinfeld_parity.py:162` | assert N == N | `tests/packs/builtin/test_training_run_seinfeld_parity.py` (1) |
| C284 | 1 | `AssertionError at tests/packs/builtin/test_training_run_seinfeld_parity.py:215` | assert N == N | `tests/packs/builtin/test_training_run_seinfeld_parity.py` (1) |
| C285 | 1 | `AssertionError at tests/packs/builtin/test_training_run_support.py:267` | assert N == N | `tests/packs/builtin/test_training_run_support.py` (1) |
| C286 | 1 | `AssertionError at tests/packs/builtin/test_training_run_support.py:331` | assert N == N | `tests/packs/builtin/test_training_run_support.py` (1) |
| C287 | 1 | `AssertionError at tests/packs/builtin/test_training_run_support.py:459` | assert N == N | `tests/packs/builtin/test_training_run_support.py` (1) |
| C288 | 1 | `AssertionError at tests/packs/builtin/test_training_run_support.py:537` | AssertionError: assert N == N | `tests/packs/builtin/test_training_run_support.py` (1) |
| C289 | 1 | `AssertionError at tests/packs/builtin/test_training_run_support.py:568` | AssertionError: assert N == N | `tests/packs/builtin/test_training_run_support.py` (1) |
| C290 | 1 | `AssertionError at tests/packs/builtin/test_training_run_support.py:592` | AssertionError: assert N == N | `tests/packs/builtin/test_training_run_support.py` (1) |
| C291 | 1 | `AssertionError at tests/packs/builtin/training_run/test_runtime_state_resume.py:29` | assert N == N | `tests/packs/builtin/training_run/test_runtime_state_resume.py` (1) |
| C292 | 1 | `AssertionError at tests/packs/builtin/training_run/test_runtime_state_resume.py:59` | AssertionError: assert [] == ['provision'] | `tests/packs/builtin/training_run/test_runtime_state_resume.py` (1) |
| C293 | 1 | `AssertionError at tests/packs/builtin/training_run/test_runtime_state_resume.py:86` | AssertionError: assert [] == ['provision', 'exec', 'exec'] | `tests/packs/builtin/training_run/test_runtime_state_resume.py` (1) |
| C294 | 1 | `AssertionError at tests/packs/builtin/training_run/test_runtime_state_resume.py:111` | AssertionError: assert N == N | `tests/packs/builtin/training_run/test_runtime_state_resume.py` (1) |
| C295 | 1 | `AssertionError at tests/packs/builtin/training_run/test_seinfeld_parity.py:35` | assert N == N | `tests/packs/builtin/training_run/test_seinfeld_parity.py` (1) |
| C296 | 1 | `CompilationError at astrid/packs/h3_av/shared/compile.py:753` | astrid.packs.hN_av.shared.spec.HNSpecError: Advanced legacy changes are outside SPEC-MIN | `tests/packs/h3_av/test_compile_generalized.py` (1) |
| C297 | 1 | `KeyError at tests/packs/h3_av/test_compile_generalized.py:195` | KeyError: 'mask_keyframes' | `tests/packs/h3_av/test_compile_generalized.py` (1) |
| C298 | 1 | `AssertionError at tests/packs/h3_av/test_generation.py:38` | AssertionError: assert N == N | `tests/packs/h3_av/test_generation.py` (1) |
| C299 | 1 | `ValueError at astrid/packs/h3_av/shared/generation.py:330` | ValueError: HN model lock entry must have a pinned Hugging Face source: stt/whisper/large-vN-turbo.pt | `tests/packs/h3_av/test_workflow_model_urls.py` (1) |
| C300 | 1 | `AssertionError at tests/packs/rendering/test_normal_audio_http.py:442` | AssertionError: assert [b'RIFF\xaN\x...xN \xN\xfN'] == [b'RIFF\xaN\x...\xcN\xN\xN'] | `tests/packs/rendering/test_normal_audio_http.py` (1) |
| C301 | 1 | `no traceback | KeyError: "unknown effects element 'fixture-smoke-effect'"` | KeyError: "unknown effects element 'fixture-smoke-effect'" | `tests/packs/rendering/test_remotion_backend.py` (1) |
| C302 | 1 | `no traceback | ValueError: timeline uses unregistered effect clip type(s): fixture-smoke-effect` | ValueError: timeline uses unregistered effect clip type(s): fixture-smoke-effect | `tests/packs/rendering/test_render_remotion_registry.py` (1) |
| C303 | 1 | `AssertionError at tests/packs/rendering/test_timeline_route_integration.py:221` | AssertionError: assert N == N | `tests/packs/rendering/test_timeline_route_integration.py` (1) |
| C304 | 1 | `AssertionError at tests/packs/rendering/test_timeline_route_integration.py:256` | AssertionError: assert N == N | `tests/packs/rendering/test_timeline_route_integration.py` (1) |
| C305 | 1 | `AssertionError at tests/packs/rendering/test_timeline_route_integration.py:299` | AssertionError: assert N == N | `tests/packs/rendering/test_timeline_route_integration.py` (1) |
| C306 | 1 | `AssertionError at tests/packs/rendering/test_timeline_route_integration.py:325` | AssertionError: assert N == N | `tests/packs/rendering/test_timeline_route_integration.py` (1) |
| C307 | 1 | `AttributeError at tests/packs/rendering/test_timeline_storyboard.py:197` | AttributeError: module 'astrid.packs.rendering.actions.timeline_storyboard.run' has no attribute 'timeline' | `tests/packs/rendering/test_timeline_storyboard.py` (1) |
| C308 | 1 | `AttributeError at tests/packs/rendering/test_timeline_storyboard.py:578` | AttributeError: module 'astrid.packs.rendering.actions.timeline_storyboard.run' has no attribute 'timeline' | `tests/packs/rendering/test_timeline_storyboard.py` (1) |
| C309 | 1 | `AttributeError at tests/packs/rendering/test_timeline_storyboard.py:663` | AttributeError: module 'astrid.packs.rendering.actions.timeline_storyboard.run' has no attribute 'timeline' | `tests/packs/rendering/test_timeline_storyboard.py` (1) |
| C310 | 1 | `AssertionError at tests/packs/rendering/test_timeline_transfer_actions.py:45` | AssertionError: assert {'check_only'...Fixture', ...} == {'check_only'...Fixture', ...} | `tests/packs/rendering/test_timeline_transfer_actions.py` (1) |
| C311 | 1 | `AssertionError at tests/packs/rendering/test_timeline_visualize_motion.py:22` | AssertionError: assert 'am-presenter' in {'animated-media-transform': PosixPath('<path> 'local/effects/animate | `tests/packs/rendering/test_timeline_visualize_motion.py` (1) |
| C312 | 1 | `AssertionError at tests/packs/runpod/test_models_lock_paths.py:32` | AssertionError: large-vN-turbo | `tests/packs/runpod/test_models_lock_paths.py` (1) |
| C313 | 1 | `AssertionError at tests/packs/runpod/test_ratchet_invariants.py:110` | AssertionError: unclassified RunPod exception class names: ['RunPodPolicyMismatch'] | `tests/packs/runpod/test_ratchet_invariants.py` (1) |
| C314 | 1 | `AssertionError at tests/packs/runpod/test_ratchet_invariants.py:152` | AssertionError: assert {'claim', 'ke...up', 'status'} == set() | `tests/packs/runpod/test_ratchet_invariants.py` (1) |
| C315 | 1 | `AssertionError at tests/packs/runpod/test_review_rest_v2.py:55` | AssertionError: assert 'reachable' == 'unknown' | `tests/packs/runpod/test_review_rest_v2.py` (1) |
| C316 | 1 | `AssertionError at tests/packs/test_b2_integrated_closure.py:58` | assert (N, N, N, N) == (N, N, N, N) | `tests/packs/test_b2_integrated_closure.py` (1) |
| C317 | 1 | `no traceback | AssertionError: N != N` | AssertionError: N != N | `tests/packs/test_executor_admission.py` (1) |
| C318 | 1 | `AssertionError at tests/packs/test_generation_verb_extensions.py:145` | AssertionError: assert {} == {'vibecomfy':...rate_video'}]} | `tests/packs/test_generation_verb_extensions.py` (1) |
| C319 | 1 | `no traceback | AssertionError: Lists differ: [] != ['builtin.sample_executor']` | AssertionError: Lists differ: [] != ['builtin.sample_executor'] | `tests/packs/test_pack_discovery.py` (1) |
| C320 | 1 | `no traceback | AssertionError: N not greater than or equal to N` | AssertionError: N not greater than or equal to N | `tests/packs/test_pack_discovery.py` (1) |
| C321 | 1 | `no traceback | KeyError: "unknown executor id 'builtin.duplicate'"` | KeyError: "unknown executor id 'builtin.duplicate'" | `tests/packs/test_pack_discovery.py` (1) |
| C322 | 1 | `no traceback | AssertionError: Lists differ: ['beta.execN', 'gamma.execN'] != ['alpha.execN', 'beta.execN` | AssertionError: Lists differ: ['beta.execN', 'gamma.execN'] != ['alpha.execN', 'beta.execN', 'gamma.execN'] | `tests/packs/test_pack_discovery.py` (1) |
| C323 | 1 | `no traceback | AssertionError: Lists differ: [] != ['alpha.execN']` | AssertionError: Lists differ: [] != ['alpha.execN'] | `tests/packs/test_pack_discovery.py` (1) |
| C324 | 1 | `no traceback | AssertionError: Lists differ: ['hivemind'] != ['alpha']` | AssertionError: Lists differ: ['hivemind'] != ['alpha'] | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C325 | 1 | `no traceback | AssertionError: Lists differ: ['hivemind', 'alpha', 'local'] != ['alpha', 'local']` | AssertionError: Lists differ: ['hivemind', 'alpha', 'local'] != ['alpha', 'local'] | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C326 | 1 | `no traceback | AssertionError: Lists differ: ['hivemind'] != []` | AssertionError: Lists differ: ['hivemind'] != [] | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C327 | 1 | `no traceback | AssertionError: Lists differ: ['hivemind'] != ['alpha', 'beta']` | AssertionError: Lists differ: ['hivemind'] != ['alpha', 'beta'] | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C328 | 1 | `no traceback | AssertionError: Lists differ: [('hivemind', 'source', N), ('source_pack', [N chars], N)] !` | AssertionError: Lists differ: [('hivemind', 'source', N), ('source_pack', [N chars], N)] != [('source_pack', ' | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C329 | 1 | `no traceback | AssertionError: Lists differ: ['hivemind', 'alpha', 'gamma'] != ['alpha', 'gamma']` | AssertionError: Lists differ: ['hivemind', 'alpha', 'gamma'] != ['alpha', 'gamma'] | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C330 | 1 | `no traceback | AssertionError: Lists differ: ['hivemind', 'alpha', 'beta'] != ['alpha', 'beta']` | AssertionError: Lists differ: ['hivemind', 'alpha', 'beta'] != ['alpha', 'beta'] | `tests/packs/test_pack_discovery_metadata.py` (1) |
| C331 | 1 | `AssertionError at tests/packs/test_pack_discovery_single_scan.py:129` | AssertionError: assert [call(PosixPa...strict=False)] == [call(None, i... strict=True)] | `tests/packs/test_pack_discovery_single_scan.py` (1) |
| C332 | 1 | `AssertionError at tests/packs/test_pack_discovery_single_scan.py:152` | AssertionError: assert ['hivemind', 'alpha'] == ['alpha'] | `tests/packs/test_pack_discovery_single_scan.py` (1) |
| C333 | 1 | `AssertionError at tests/packs/test_pack_discovery_single_scan.py:209` | AssertionError: assert [('hivemind', 'source')] == [('local', 'local')] | `tests/packs/test_pack_discovery_single_scan.py` (1) |
| C334 | 1 | `AssertionError at tests/packs/test_pack_discovery_single_scan.py:224` | AssertionError: assert 'Hivemind vN ...gest_youtube.' == 'before' | `tests/packs/test_pack_discovery_single_scan.py` (1) |
| C335 | 1 | `PackValidationError at astrid/core/pack/discovery.py:522` | astrid.core.pack._common.PackValidationError: duplicate pack id 'local': pack 'local' conflicts with a core pa | `tests/packs/test_pack_discovery_v3.py` (1) |
| C336 | 1 | `Failed at tests/packs/test_pack_discovery_v3.py:174` | Failed: DID NOT RAISE <class 'astrid.core.pack._common.PackValidationError'> | `tests/packs/test_pack_discovery_v3.py` (1) |
| C337 | 1 | `AssertionError at tests/packs/test_pack_quarantine.py:116` | AssertionError: assert [] == ['goodpack'] | `tests/packs/test_pack_quarantine.py` (1) |
| C338 | 1 | `AssertionError at tests/packs/test_pack_quarantine.py:154` | AssertionError: assert 'keywords.N' in 'Pack manifest needs an explicit schema upgrade. Migrate to vN and add  | `tests/packs/test_pack_quarantine.py` (1) |
| C339 | 1 | `AssertionError at tests/packs/test_pack_quarantine.py:175` | AssertionError: assert QuarantinedPack(pack_id='goodpack', pack_dir=PosixPath('<path> manifest_path=PosixPath( | `tests/packs/test_pack_quarantine.py` (1) |
| C340 | 1 | `AssertionError at tests/packs/test_pack_quarantine.py:186` | AssertionError: assert 'keywords.N' in 'Pack manifest needs an explicit schema upgrade. Migrate to vN and add  | `tests/packs/test_pack_quarantine.py` (1) |
| C341 | 1 | `AssertionError at tests/packs/test_pack_quarantine.py:219` | AssertionError: assert set() == {'goodpack.ec...odpack.extra'} | `tests/packs/test_pack_quarantine.py` (1) |
| C342 | 1 | `KeyError at astrid/core/execution/orchestrator/registry.py:79` | KeyError: "unknown orchestrator id 'hN_av.transform'" | `tests/packs/test_public_id_resolution.py` (1) |
| C343 | 1 | `AssertionError at tests/packs/test_vibecomfy_ir_bridge.py:145` | AssertionError: assert {'after_outpu..._inputs', ...} == {'attempt_ide..._assets', ...} | `tests/packs/test_vibecomfy_ir_bridge.py` (1) |
| C344 | 1 | `AssertionError at tests/packs/timeline/test_cli_clash_back.py:245` | assert 'err.pending_id' in "---\nname: rendering\ndescription: Render timelines, inspect render output, author | `tests/packs/timeline/test_cli_clash_back.py` (1) |
| C345 | 1 | `AssertionError at tests/packs/timeline/test_cli_find.py:10` | AssertionError: assert <function _provided.<locals>.run at <addr>> is <function run_find at <addr>> | `tests/packs/timeline/test_cli_find.py` (1) |
| C346 | 1 | `AssertionError at tests/packs/timeline/test_cli_parity.py:153` | AssertionError: assert 'tracks' not in {'theme_overrides': {'visual': {'canvas': {'fps': N, 'height': N, 'widt | `tests/packs/timeline/test_cli_parity.py` (1) |
| C347 | 1 | `AssertionError at tests/packs/timeline/test_cli_parity.py:489` | assert '-m/--message' in "usage: astrid timelines [-h]\n                        {import,export,checkout,commit | `tests/packs/timeline/test_cli_parity.py` (1) |
| C348 | 1 | `AssertionError at tests/packs/timeline/test_cli_v3_sweep_log.py:24` | AssertionError: assert 'run' == '_cmd_edit' | `tests/packs/timeline/test_cli_v3_sweep_log.py` (1) |
| C349 | 1 | `AssertionError at tests/packs/timeline/test_parent_clips.py:224` | AssertionError: assert N == N | `tests/packs/timeline/test_parent_clips.py` (1) |
| C350 | 1 | `AssertionError at tests/packs/timeline/test_show_clip_working_copy.py:94` | AssertionError: PUBLISHED rev-N | `tests/packs/timeline/test_show_clip_working_copy.py` (1) |
| C351 | 1 | `AssertionError at tests/packs/timeline/test_show_clip_working_copy.py:101` | AssertionError: PUBLISHED rev-N | `tests/packs/timeline/test_show_clip_working_copy.py` (1) |
| C352 | 1 | `AssertionError at tests/packs/timeline/test_verbs_working_copy.py:302` | AttributeError: 'Timelines' object has no attribute 'history' | `tests/packs/timeline/test_verbs_working_copy.py` (1) |
| C353 | 1 | `AssertionError at tests/packs/timeline/test_visualize_drafts.py:357` | AssertionError: assert 'contact shee...was returned)' == 'WORKING COPY... live version' | `tests/packs/timeline/test_visualize_drafts.py` (1) |
| C354 | 1 | `KeyError at tests/packs/vibecomfy/test_local_launch_facts.py:135` | KeyError: '/userdata?dir=workflows&full_info=true&recurse=true' | `tests/packs/vibecomfy/test_local_launch_facts.py` (1) |
| C355 | 1 | `AssertionError at tests/packs/vibecomfy/test_local_server_media.py:116` | astrid.core.media.MediaProbeError: ffprobe failed with exit N | `tests/packs/vibecomfy/test_local_server_media.py` (1) |
| C356 | 1 | `AssertionError at tests/reshape/test_check_doc_references.py:283` | AssertionError: assert [Finding(leve... the result')] == [] | `tests/reshape/test_check_doc_references.py` (1) |
| C357 | 1 | `AssertionError at tests/reshape/test_compare_baselines.py:230` | AssertionError: STRUCTURE ERROR (new): astrid/core/cli/domain_timelines.py imports forbidden module 'astrid.pa | `tests/reshape/test_compare_baselines.py` (1) |
| C358 | 1 | `AssertionError at tests/reshape/test_compare_baselines.py:241` | AssertionError: new structure violations: ["astrid/core/cli/domain_timelines.py imports forbidden module 'astr | `tests/reshape/test_compare_baselines.py` (1) |
| C359 | 1 | `AssertionError at tests/reshape/test_repo_hygiene.py:227` | AssertionError: assert ['.claude/', ..., 'evidence/'] == [] | `tests/reshape/test_repo_hygiene.py` (1) |
| C360 | 1 | `ArtifactIdentityError at scripts/reshape/installed_artifact.py:1004` | scripts.reshape.installed_artifact.ArtifactIdentityError: foreign site-packages path leaked into child sys.pat | `tests/reshape/test_timeline_installed_skills.py` (1) |
| C361 | 1 | `AssertionError at tests/scripts/test_claim_runpod_5090_backup.py:121` | AssertionError: assert N == N | `tests/scripts/test_claim_runpod_5090_backup.py` (1) |
| C362 | 1 | `AssertionError at tests/scripts/test_claim_runpod_5090_backup.py:136` | AssertionError: assert {'N.N', 'N....N.N', 'N.N'} <= {'N.N'} | `tests/scripts/test_claim_runpod_5090_backup.py` (1) |
| C363 | 1 | `AssertionError at tests/scripts/test_claim_runpod_5090_backup.py:225` | AssertionError: assert ('N.N',) == ('N.N', 'N....N.N', 'N.N') | `tests/scripts/test_claim_runpod_5090_backup.py` (1) |
| C364 | 1 | `AssertionError at tests/scripts/test_claim_runpod_5090_backup.py:653` | assert N <= N | `tests/scripts/test_claim_runpod_5090_backup.py` (1) |
| C365 | 1 | `AssertionError at tests/scripts/test_cuda_default_sites.py:26` | AssertionError: assert ('N.N',) is ('N.N', 'N.N', 'N.N', 'N.N') | `tests/scripts/test_cuda_default_sites.py` (1) |
| C366 | 1 | `AssertionError at tests/scripts/test_gpu_sanity.py:59` | assert 'CUBLAS_STATUS_EXECUTION_FAILED' in ('' + "<path> can't open file '<path> [Errno N] No such file or dir | `tests/scripts/test_gpu_sanity.py` (1) |
| C367 | 1 | `AssertionError at tests/scripts/test_gpu_sanity.py:67` | assert (N == N and 'N/N' in "<path> can't open file '<path> [Errno N] No such file or directory\n") | `tests/scripts/test_gpu_sanity.py` (1) |
| C368 | 1 | `AssertionError at tests/scripts/test_gpu_sanity.py:79` | assert (N == N) | `tests/scripts/test_gpu_sanity.py` (1) |
| C369 | 1 | `AssertionError at tests/scripts/test_pod_action_source.py:366` | assert (N == N) | `tests/scripts/test_pod_action_source.py` (1) |
| C370 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:258` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C371 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:273` | AssertionError: assert 'fixture source identity refused' in '/bin/bash: <path> No such file or directory\n' | `tests/scripts/test_pod_bootstrap.py` (1) |
| C372 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:280` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C373 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:290` | AssertionError: assert 'uv not found' in '/bin/bash: <path> No such file or directory\n' | `tests/scripts/test_pod_bootstrap.py` (1) |
| C374 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:300` | AssertionError: assert ('cannot create or write' in '/bin/bash: <path> No such file or directory\n') | `tests/scripts/test_pod_bootstrap.py` (1) |
| C375 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:345` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C376 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:368` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C377 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:384` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C378 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:394` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C379 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:466` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C380 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:479` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C381 | 1 | `AssertionError at tests/scripts/test_pod_bootstrap.py:494` | AssertionError: /bin/bash: <path> No such file or directory | `tests/scripts/test_pod_bootstrap.py` (1) |
| C382 | 1 | `AssertionError at tests/scripts/test_pod_h3_install.py:281` | AssertionError: assert 'valid' == 'invalid' | `tests/scripts/test_pod_h3_install.py` (1) |
| C383 | 1 | `AssertionError at tests/scripts/test_pod_held_budget.py:136` | AssertionError: assert (N - N) == (N - N) | `tests/scripts/test_pod_held_budget.py` (1) |
| C384 | 1 | `AssertionError at tests/scripts/test_pod_held_budget.py:276` | AssertionError: assert (N - N) == (N - N) | `tests/scripts/test_pod_held_budget.py` (1) |
| C385 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:274` | assert ((N + N) * (N ** N)) == (N * (N ** N)) | `tests/scripts/test_pod_jobs.py` (1) |
| C386 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:688` | assert N == (N + N) | `tests/scripts/test_pod_jobs.py` (1) |
| C387 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:978` | AssertionError: assert ('held' == 'held' | `tests/scripts/test_pod_jobs.py` (1) |
| C388 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1009` | assert N == N | `tests/scripts/test_pod_jobs.py` (1) |
| C389 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1047` | assert N == N | `tests/scripts/test_pod_jobs.py` (1) |
| C390 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1078` | assert N <= (N + N) | `tests/scripts/test_pod_jobs.py` (1) |
| C391 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1122` | assert N == N | `tests/scripts/test_pod_jobs.py` (1) |
| C392 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1379` | assert N == N | `tests/scripts/test_pod_jobs.py` (1) |
| C393 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1624` | assert N == N | `tests/scripts/test_pod_jobs.py` (1) |
| C394 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1668` | assert N == N | `tests/scripts/test_pod_jobs.py` (1) |
| C395 | 1 | `AssertionError at tests/scripts/test_pod_jobs.py:1857` | AssertionError: assert (N - N) == N | `tests/scripts/test_pod_jobs.py` (1) |
| C396 | 1 | `AssertionError at tests/scripts/test_pod_session.py:518` | AssertionError: assert 'N' == 'N' | `tests/scripts/test_pod_session.py` (1) |
| C397 | 1 | `AssertionError at tests/scripts/test_pod_session.py:768` | assert ("bash -lc 'ex...thonN -u -c '" == 'bash -lc \'e...'))\'"\'"\'\'' | `tests/scripts/test_pod_session.py` (1) |
| C398 | 1 | `AssertionError at tests/scripts/test_pod_session.py:874` | assert N <= N | `tests/scripts/test_pod_session.py` (1) |
| C399 | 1 | `AssertionError at tests/scripts/test_pod_session.py:1047` | AssertionError: assert False | `tests/scripts/test_pod_session.py` (1) |
| C400 | 1 | `AssertionError at tests/scripts/test_pod_session.py:1663` | AssertionError: assert not True | `tests/scripts/test_pod_session.py` (1) |
| C401 | 1 | `AssertionError at tests/sdk/test_d124_shared_custody.py:82` | assert N == N | `tests/sdk/test_d124_shared_custody.py` (1) |
| C402 | 1 | `KeyError at tests/sdk/test_generation_source_retention.py:169` | KeyError: 'shaN:<hash>' | `tests/sdk/test_generation_source_retention.py` (1) |
| C403 | 1 | `AssertionError at tests/sdk/test_generation_target.py:526` | AssertionError: assert ['/system_sta...ered-managed'] == ['/system_sta...ered-managed'] | `tests/sdk/test_generation_target.py` (1) |
| C404 | 1 | `IntegrityError at astrid/core/generation/managed_preparation.py:305` | astrid.core.generation.engine_contracts.IntegrityError: managed model has no declared digest: flux-N-klein-bas | `tests/sdk/test_generation_target.py` (1) |
| C405 | 1 | `AssertionError at tests/sdk/test_generation_verified_preparation_gr03.py:172` | AssertionError: assert 'qwen-image-N.N-turbo' == 'z-image' | `tests/sdk/test_generation_verified_preparation_gr03.py` (1) |
| C406 | 1 | `AttributeError at vibecomfy-checkout/vibecomfy/entries.py:88` | AttributeError: 'NoneType' object has no attribute 'runtime_nodes' | `tests/sdk/test_generation_verified_preparation_gr03.py` (1) |
| C407 | 1 | `AfterRetirement at tests/sdk/test_host_recovery.py:1125` | test_host_recovery.test_foreground_retirement_is_bound_to_locked_support.<locals>.AfterRetirement | `tests/sdk/test_host_recovery.py` (1) |
| C408 | 1 | `KeyError at tests/sdk/test_openai_image_admission.py:251` | KeyError: 'target' | `tests/sdk/test_openai_image_admission.py` (1) |
| C409 | 1 | `AssertionError at tests/sdk/test_p1_case_corpus.py:104` | AssertionError: nested-closure-trim | `tests/sdk/test_p1_case_corpus.py` (1) |
| C410 | 1 | `AssertionError at tests/sdk/test_p1_doc_patch_requests.py:189` | AssertionError: assert '<hash>...<hash>' == '<hash>...<hash>' | `tests/sdk/test_p1_doc_patch_requests.py` (1) |
| C411 | 1 | `WorkspaceClientError at astrid/sdk/timeline/sync.py:214` | astrid.sdk.workspace_client.WorkspaceClientError: assert ('p', 't', N) == ('p', 't', N) | `tests/sdk/test_p4_note_rerun.py` (1) |
| C412 | 1 | `AssertionError at tests/sdk/test_projectless_admission.py:89` | astrid.sdk.exceptions.CapabilityValidationError: OpenAI request contains undeclared inputs: execution, mode, m | `tests/sdk/test_projectless_admission.py` (1) |
| C413 | 1 | `AssertionError at tests/sdk/test_runtime_response_conformance.py:104` | AssertionError: assert ['commit_conf...und_N', ...] == ['events_page...ict_N', ...] | `tests/sdk/test_runtime_response_conformance.py` (1) |
| C414 | 1 | `AssertionError at tests/sdk/test_scene_real_public_summary_rle.py:67` | AssertionError: assert [(N, N, 'COV..., ('empty',))] == [(N, N, 'COV..., ('empty',))] | `tests/sdk/test_scene_real_public_summary_rle.py` (1) |
| C415 | 1 | `CommandError at astrid/sdk/timeline/_selected_param_authority.py:219` | astrid.sdk.timeline._command_state.CommandError: selected PARAM authority is unavailable | `tests/sdk/test_selected_param_neutral_stage.py` (1) |
| C416 | 1 | `AssertionError at tests/sdk/test_timeline_capture_projection.py:205` | AssertionError: Traceback (most recent call last): | `tests/sdk/test_timeline_capture_projection.py` (1) |
| C417 | 1 | `AssertionError at tests/sdk/test_timeline_checkout.py:1230` | AssertionError: assert {'composed_ca...a': True, ...} == {'composed_ca...a': True, ...} | `tests/sdk/test_timeline_checkout.py` (1) |
| C418 | 1 | `AssertionError at tests/sdk/test_timeline_checkout.py:1356` | KeyError: 'source_mapping' | `tests/sdk/test_timeline_checkout.py` (1) |
| C419 | 1 | `AssertionError at tests/sdk/test_timeline_checkout_history.py:75` | AssertionError: assert {'acknowledge...ing', 'scope'} == {'base', 'fli...ing', 'scope'} | `tests/sdk/test_timeline_checkout_history.py` (1) |

## Failing IDs by test file

| IDs | Clusters | File |
| ---: | ---: | --- |
| 59 | 3 | `tests/test_installer_busy_fence.py` |
| 47 | 1 | `tests/core/pack/test_transaction.py` |
| 36 | 17 | `tests/scripts/test_pod_jobs.py` |
| 33 | 1 | `tests/packs/rendering/test_normal_audio_run.py` |
| 30 | 1 | `tests/core/execution/test_runtime_source_custody_d40.py` |
| 27 | 1 | `tests/sdk/test_timeline_editing_acceptance_runtime.py` |
| 26 | 14 | `tests/scripts/test_pod_bootstrap.py` |
| 25 | 1 | `tests/sdk/test_timeline_helper_capture.py` |
| 19 | 5 | `tests/packs/test_portfolio_parity.py` |
| 19 | 1 | `tests/packs/test_pack_run_cli_choices.py` |
| 18 | 1 | `tests/sdk/test_timeline_clash_back_runtime.py` |
| 17 | 7 | `tests/packs/test_pack_discovery_single_scan.py` |
| 16 | 2 | `tests/editing_conformance/test_fork_abi1_binding_set.py` |
| 15 | 1 | `tests/core/execution/test_runtime_orchestrator_custody_d40.py` |
| 14 | 1 | `tests/sdk/test_timeline_helper_normalization.py` |
| 14 | 1 | `tests/sdk/test_timeline_restructure.py` |
| 14 | 2 | `tests/test_local_install.py` |
| 14 | 1 | `tests/packs/test_pack_migration_m4_shells.py` |
| 13 | 4 | `tests/test_installer_acl.py` |
| 13 | 11 | `tests/core/rendering/test_registry.py` |
| 12 | 1 | `tests/sdk/test_timeline_normal_publish.py` |
| 12 | 1 | `tests/core/pack/test_r8_prod_refusals.py` |
| 12 | 11 | `tests/core/rendering/test_remotion_runtime.py` |
| 12 | 1 | `tests/editing_conformance/test_timeline_clash_back_acceptance_runtime.py` |
| 12 | 10 | `tests/packs/test_pack_discovery_metadata.py` |
| 11 | 8 | `tests/core/generation/test_discovery_scope.py` |
| 11 | 1 | `tests/sdk/test_timeline_restructure_guarded_runtime.py` |
| 11 | 1 | `tests/packs/rendering/test_remotion_layer_tail_compat.py` |
| 11 | 7 | `tests/packs/test_pack_discovery.py` |
| 10 | 1 | `tests/sdk/test_timeline_commit_wording_runtime.py` |
| 10 | 1 | `tests/stage1/test_pack_host_interpreter_identity.py` |
| 9 | 4 | `tests/test_installer_installed_schema.py` |
| 9 | 7 | `tests/core/rendering/test_registry_matrix.py` |
| 8 | 1 | `tests/core/generation/test_engine_release.py` |
| 8 | 1 | `tests/sdk/test_timeline_open_commit.py` |
| 8 | 3 | `tests/test_installer_app_update.py` |
| 8 | 7 | `tests/packs/builtin/test_training_run_support.py` |
| 7 | 1 | `tests/sdk/test_timeline_revision_read_boundary.py` |
| 7 | 1 | `tests/editing_conformance/test_prepared_video_birth.py` |
| 7 | 3 | `tests/packs/timeline/test_verbs_working_copy.py` |
| 7 | 1 | `tests/packs/timeline/test_cli_status_publish.py` |
| 7 | 6 | `tests/scripts/test_claim_runpod_5090_backup.py` |
| 6 | 2 | `tests/core/execution/test_generic_host_child_bridge_d18.py` |
| 6 | 1 | `tests/test_installer_platforms.py` |
| 6 | 3 | `tests/test_skills_sync_registry.py` |
| 6 | 3 | `tests/sdk/test_generation_verified_preparation_gr03.py` |
| 5 | 4 | `tests/core/generation/backends/test_qwen_21_turbo.py` |
| 5 | 1 | `tests/sdk/test_timeline_session_pair.py` |
| 5 | 3 | `tests/sdk/test_timeline_native_checkout.py` |
| 5 | 4 | `tests/test_failure_mode_executor.py` |
| 5 | 3 | `tests/test_generic_host.py` |
| 5 | 5 | `tests/test_installer_pinokio_lifecycle.py` |
| 5 | 4 | `tests/packs/test_pack_discovery_v3.py` |
| 5 | 5 | `tests/packs/test_pack_quarantine.py` |
| 5 | 5 | `tests/scripts/test_pod_session.py` |
| 4 | 2 | `tests/core/execution/test_private_network_command.py` |
| 4 | 1 | `tests/sdk/test_timeline_retry.py` |
| 4 | 4 | `tests/sdk/test_timeline_current_union_schema.py` |
| 4 | 4 | `tests/stage1/test_zero_shim_execution_pack_deletion.py` |
| 4 | 4 | `tests/test_canonical_aliases.py` |
| 4 | 2 | `tests/test_installer_shim.py` |
| 4 | 1 | `tests/test_live_capability_discovery_fix.py` |
| 4 | 2 | `tests/test_update_from_field_states.py` |
| 4 | 1 | `tests/editing_conformance/test_reviewed_list_runtime_v3.py` |
| 4 | 1 | `tests/editing_conformance/test_recipe_m2_video_unplace.py` |
| 4 | 4 | `tests/packs/builtin/training_run/test_runtime_state_resume.py` |
| 4 | 4 | `tests/packs/rendering/test_timeline_route_integration.py` |
| 4 | 4 | `tests/scripts/test_gpu_sanity.py` |
| 4 | 3 | `tests/scripts/test_pod_held_budget.py` |
| 3 | 2 | `tests/core/generation/test_param_map_migration_parity.py` |
| 3 | 1 | `tests/sdk/test_timeline_f2_refusal.py` |
| 3 | 1 | `tests/sdk/test_timeline_recheck_rerun_runtime.py` |
| 3 | 3 | `tests/sdk/test_timeline_commit_provider.py` |
| 3 | 2 | `tests/stage1/test_thread_authority_cutover.py` |
| 3 | 3 | `tests/test_creator_entry_declarations.py` |
| 3 | 1 | `tests/test_installed_generation_journey.py` |
| 3 | 2 | `tests/test_installer_lifecycle.py` |
| 3 | 1 | `tests/test_installer_schema.py` |
| 3 | 3 | `tests/test_omp_agent.py` |
| 3 | 3 | `tests/test_skills_developer.py` |
| 3 | 3 | `tests/test_skills_selected_composition.py` |
| 3 | 3 | `tests/test_third_party_integration.py` |
| 3 | 3 | `tests/test_timeline_editing_helpers.py` |
| 3 | 3 | `tests/v10/test_docs_cli_alignment.py` |
| 3 | 1 | `tests/core/pack/test_build_hook_contract.py` |
| 3 | 3 | `tests/core/generation/test_public_route_guard.py` |
| 3 | 2 | `tests/core/generation/test_runpod_engine_selection.py` |
| 3 | 3 | `tests/core/test_elements_cli.py` |
| 3 | 1 | `tests/integrations/test_d09_managed_scene_only.py` |
| 3 | 1 | `tests/editing_conformance/test_recipe_occurrence_fork.py` |
| 3 | 1 | `tests/packs/h3_av/test_no_astrid_imports.py` |
| 3 | 3 | `tests/packs/rendering/test_timeline_storyboard.py` |
| 3 | 1 | `tests/sdk/test_shot_plan.py` |
| 3 | 2 | `tests/sdk/test_p1_case_corpus.py` |
| 3 | 2 | `tests/sdk/test_runtime_response_conformance.py` |
| 3 | 2 | `tests/sdk/test_timeline_capture_projection.py` |
| 2 | 2 | `tests/core/execution/test_host_cleanup_ack_barrier.py` |
| 2 | 2 | `tests/core/generation/test_cli_gold_075b.py` |
| 2 | 1 | `tests/core/generation/test_engine_fresh_install.py` |
| 2 | 2 | `tests/core/generation/test_generation_index.py` |
| 2 | 1 | `tests/sdk/test_timeline_publish_connection.py` |
| 2 | 1 | `tests/sdk/test_timeline_structural_track_order_runtime.py` |
| 2 | 1 | `tests/sdk/test_timeline_occurrence_delete_provider.py` |
| 2 | 2 | `tests/sdk/test_timeline_open_commit_v2.py` |
| 2 | 2 | `tests/sdk/test_wc6_completion_capture.py` |
| 2 | 1 | `tests/stage1/test_core_import_authority.py` |
| 2 | 1 | `tests/stage1/test_zero_shim_lane_c.py` |
| 2 | 2 | `tests/test_ci_journey.py` |
| 2 | 1 | `tests/test_diagnostics_callers.py` |
| 2 | 1 | `tests/test_installer_autostart.py` |
| 2 | 1 | `tests/test_installer_launcher_repair.py` |
| 2 | 1 | `tests/test_installer_release0_rollback.py` |
| 2 | 1 | `tests/test_installer_service_repair_integration.py` |
| 2 | 1 | `tests/test_installer_transaction_authority.py` |
| 2 | 1 | `tests/editing_conformance/test_fork_historical_source_boundary.py` |
| 2 | 1 | `tests/editing_conformance/test_headless_root_mirror_effects.py` |
| 2 | 1 | `tests/editing_conformance/test_native_word_anchor_vectors.py` |
| 2 | 2 | `tests/test_journey_diagnostic_checkpoint.py` |
| 2 | 1 | `tests/test_setup_skill_branches.py` |
| 2 | 1 | `tests/test_skills_cli.py` |
| 2 | 2 | `tests/test_structure_contracts.py` |
| 2 | 2 | `tests/timeline/test_effects_catalog.py` |
| 2 | 1 | `tests/v10/test_pack_write_path_lint.py` |
| 2 | 2 | `tests/core/generation/test_readiness_inputs_f04.py` |
| 2 | 1 | `tests/core/rendering/test_remotion_registry_context_key.py` |
| 2 | 1 | `tests/editing_conformance/test_authoring_item_observation_boundary.py` |
| 2 | 1 | `tests/editing_conformance/test_authoring_undo_projection.py` |
| 2 | 2 | `tests/packs/builtin/test_training_run_seinfeld_parity.py` |
| 2 | 2 | `tests/packs/h3_av/test_compile_generalized.py` |
| 2 | 1 | `tests/packs/h3_av/test_edit_inputs.py` |
| 2 | 1 | `tests/packs/rendering/test_ffmpeg_support.py` |
| 2 | 1 | `tests/sdk/test_checkout_publish_media_admission.py` |
| 2 | 1 | `tests/sdk/test_inverse_removed_shot_owners_runtime.py` |
| 2 | 2 | `tests/packs/runpod/test_ratchet_invariants.py` |
| 2 | 1 | `tests/packs/timeline/test_cli_edit_flags.py` |
| 2 | 2 | `tests/packs/timeline/test_cli_parity.py` |
| 2 | 2 | `tests/packs/timeline/test_show_clip_working_copy.py` |
| 2 | 2 | `tests/reshape/test_compare_baselines.py` |
| 2 | 2 | `tests/scripts/test_pod_h3_install.py` |
| 2 | 2 | `tests/sdk/test_generation_target.py` |
| 2 | 2 | `tests/sdk/test_timeline_checkout.py` |
| 2 | 1 | `tests/sdk/test_timeline_clip_scalar_provider.py` |
| 1 | 1 | `tests/core/execution/test_bug14_settlement_liveness.py` |
| 1 | 1 | `tests/core/execution/test_fail_closed_g28.py` |
| 1 | 1 | `tests/core/execution/test_generic_host_actions_v3.py` |
| 1 | 1 | `tests/core/execution/test_generic_host_verified_preparation_gr03.py` |
| 1 | 1 | `tests/core/execution/test_platform_boundary.py` |
| 1 | 1 | `tests/core/generation/test_edit_image_ref_admission.py` |
| 1 | 1 | `tests/core/generation/test_engine_error_reasons.py` |
| 1 | 1 | `tests/core/generation/test_generation_setup_walk.py` |
| 1 | 1 | `tests/core/generation/test_h3_build_after_outputs.py` |
| 1 | 1 | `tests/core/generation/test_listing.py` |
| 1 | 1 | `tests/core/generation/test_moved_data_composition.py` |
| 1 | 1 | `tests/sdk/test_timeline_multipart_retry_race_runtime.py` |
| 1 | 1 | `tests/sdk/test_timeline_shots_sdk_runtime.py` |
| 1 | 1 | `tests/sdk/test_timeline_store_raw_reader.py` |
| 1 | 1 | `tests/sdk/test_timeline_commit_provider_scalar.py` |
| 1 | 1 | `tests/sdk/test_timeline_film_length.py` |
| 1 | 1 | `tests/sdk/test_timeline_public_command.py` |
| 1 | 1 | `tests/sdk/test_timeline_render_publication.py` |
| 1 | 1 | `tests/sdk/test_timeline_selected_param_authority.py` |
| 1 | 1 | `tests/sdk/test_timeline_sheet_native.py` |
| 1 | 1 | `tests/stage1/test_asset_cache_retired_luna.py` |
| 1 | 1 | `tests/stage1/test_capability_parity_gate_luna.py` |
| 1 | 1 | `tests/stage1/test_final_render_authority_luna.py` |
| 1 | 1 | `tests/stage1/test_generic_host_process_bootstrap_luna.py` |
| 1 | 1 | `tests/stage1/test_kernel_admission_runtime.py` |
| 1 | 1 | `tests/stage1/test_pack_api_surface.py` |
| 1 | 1 | `tests/stage1/test_vendored_workspace_client_parity_luna.py` |
| 1 | 1 | `tests/stage1/test_zero_shim_timeline_cutover_luna.py` |
| 1 | 1 | `tests/test_boundary_handoff.py` |
| 1 | 1 | `tests/test_boundary_registration.py` |
| 1 | 1 | `tests/test_canonical_entrypoint.py` |
| 1 | 1 | `tests/test_core_pack_boundary_guard.py` |
| 1 | 1 | `tests/test_core_provider_neutrality.py` |
| 1 | 1 | `tests/test_core_util_surface.py` |
| 1 | 1 | `tests/test_env_vars_conformance.py` |
| 1 | 1 | `tests/test_external_app_contract.py` |
| 1 | 1 | `tests/test_external_pack_contract.py` |
| 1 | 1 | `tests/test_generic_host_result_json.py` |
| 1 | 1 | `tests/test_gpu_journey_receipts.py` |
| 1 | 1 | `tests/test_installer_backup.py` |
| 1 | 1 | `tests/test_installer_bootstrap_imports.py` |
| 1 | 1 | `tests/test_installer_bootstrap_schema.py` |
| 1 | 1 | `tests/test_installer_launchd_cache_window.py` |
| 1 | 1 | `tests/test_installer_launchd_stop_handoff.py` |
| 1 | 1 | `tests/test_installer_local_update.py` |
| 1 | 1 | `tests/test_installer_r0_entry.py` |
| 1 | 1 | `tests/test_installer_startup_stop.py` |
| 1 | 1 | `tests/test_installer_update_legacy_record.py` |
| 1 | 1 | `tests/editing_conformance/test_producer_insertion.py` |
| 1 | 1 | `tests/editing_conformance/test_recipe_m2_clip_trim.py` |
| 1 | 1 | `tests/test_journey_windows_acl_capture.py` |
| 1 | 1 | `tests/test_n1_permission_boundary_guard.py` |
| 1 | 1 | `tests/test_onboarding_one_home.py` |
| 1 | 1 | `tests/test_pipeline_dispatch_aliases.py` |
| 1 | 1 | `tests/test_platform_matrix.py` |
| 1 | 1 | `tests/test_provider_route_grant.py` |
| 1 | 1 | `tests/test_public_boundary.py` |
| 1 | 1 | `tests/test_recoverability_conformance.py` |
| 1 | 1 | `tests/test_sdk_public_surface.py` |
| 1 | 1 | `tests/test_skills_installed_composition.py` |
| 1 | 1 | `tests/test_skills_package_data.py` |
| 1 | 1 | `tests/test_skip_policy.py` |
| 1 | 1 | `tests/timeline/test_authoring_bundle.py` |
| 1 | 1 | `tests/timeline/test_html_canvas_effect.py` |
| 1 | 1 | `tests/timeline/test_shot_composition_projection.py` |
| 1 | 1 | `tests/timeline/test_shot_layering_projection.py` |
| 1 | 1 | `tests/timeline/test_timeline_elements_catalog.py` |
| 1 | 1 | `tests/v10/test_authority_lint.py` |
| 1 | 1 | `tests/v10/test_domain_cli_projects_timelines.py` |
| 1 | 1 | `tests/v10/test_release_reproducibility.py` |
| 1 | 1 | `tests/core/generation/test_release_python.py` |
| 1 | 1 | `tests/core/generation/test_run_local.py` |
| 1 | 1 | `tests/core/generation/test_trusted_inventory.py` |
| 1 | 1 | `tests/core/generation/test_warm_models_remain_loaded.py` |
| 1 | 1 | `tests/core/model_catalog/test_registry.py` |
| 1 | 1 | `tests/core/pack/test_v3_core_worker_luna.py` |
| 1 | 1 | `tests/core/rendering/test_installed_registry_security.py` |
| 1 | 1 | `tests/core/rendering/test_production_callers.py` |
| 1 | 1 | `tests/core/test_element_kind_registry.py` |
| 1 | 1 | `tests/core/test_executor_registry_snapshot.py` |
| 1 | 1 | `tests/core/test_generation_backend_registry.py` |
| 1 | 1 | `tests/core/test_generation_taxonomy_registry.py` |
| 1 | 1 | `tests/core/test_pack_coherence_elements.py` |
| 1 | 1 | `tests/core/timeline/test_clip_fields.py` |
| 1 | 1 | `tests/editing_conformance/test_compile_contracts.py` |
| 1 | 1 | `tests/packs/builtin/generate_image/test_codex_backend.py` |
| 1 | 1 | `tests/packs/builtin/test_training_run_ai_toolkit_support.py` |
| 1 | 1 | `tests/packs/builtin/training_run/test_seinfeld_parity.py` |
| 1 | 1 | `tests/packs/h3_av/test_generation.py` |
| 1 | 1 | `tests/packs/h3_av/test_workflow_model_urls.py` |
| 1 | 1 | `tests/packs/rendering/test_normal_audio_http.py` |
| 1 | 1 | `tests/packs/rendering/test_remotion_backend.py` |
| 1 | 1 | `tests/packs/rendering/test_remotion_element_generation.py` |
| 1 | 1 | `tests/packs/rendering/test_render_remotion_registry.py` |
| 1 | 1 | `tests/packs/rendering/test_scene_source_carry.py` |
| 1 | 1 | `tests/packs/rendering/test_timeline_transfer_actions.py` |
| 1 | 1 | `tests/packs/rendering/test_timeline_visualize_motion.py` |
| 1 | 1 | `tests/packs/runpod/test_models_lock_paths.py` |
| 1 | 1 | `tests/packs/runpod/test_review_rest_v2.py` |
| 1 | 1 | `tests/packs/test_b2_integrated_closure.py` |
| 1 | 1 | `tests/packs/test_executor_admission.py` |
| 1 | 1 | `tests/packs/test_generation_verb_extensions.py` |
| 1 | 1 | `tests/packs/test_packs_validate.py` |
| 1 | 1 | `tests/packs/test_public_id_resolution.py` |
| 1 | 1 | `tests/packs/test_vibecomfy_ir_bridge.py` |
| 1 | 1 | `tests/packs/timeline/test_cli_clash_back.py` |
| 1 | 1 | `tests/packs/timeline/test_cli_find.py` |
| 1 | 1 | `tests/packs/timeline/test_cli_v3_sweep_log.py` |
| 1 | 1 | `tests/packs/timeline/test_parent_clips.py` |
| 1 | 1 | `tests/packs/timeline/test_visualize_drafts.py` |
| 1 | 1 | `tests/packs/vibecomfy/test_local_launch_facts.py` |
| 1 | 1 | `tests/packs/vibecomfy/test_local_server_media.py` |
| 1 | 1 | `tests/reshape/test_check_doc_references.py` |
| 1 | 1 | `tests/reshape/test_repo_hygiene.py` |
| 1 | 1 | `tests/reshape/test_timeline_installed_skills.py` |
| 1 | 1 | `tests/scripts/test_cuda_default_sites.py` |
| 1 | 1 | `tests/scripts/test_pod_action_source.py` |
| 1 | 1 | `tests/sdk/test_d124_shared_custody.py` |
| 1 | 1 | `tests/sdk/test_generation_source_retention.py` |
| 1 | 1 | `tests/sdk/test_host_recovery.py` |
| 1 | 1 | `tests/sdk/test_openai_image_admission.py` |
| 1 | 1 | `tests/sdk/test_p1_doc_patch_requests.py` |
| 1 | 1 | `tests/sdk/test_p4_note_rerun.py` |
| 1 | 1 | `tests/sdk/test_projectless_admission.py` |
| 1 | 1 | `tests/sdk/test_scene_real_public_summary_rle.py` |
| 1 | 1 | `tests/sdk/test_selected_param_neutral_stage.py` |
| 1 | 1 | `tests/sdk/test_timeline_checkout_history.py` |
