# Execution host map

[Plan](plan.md) · [Tasks](tasks.md) · [Packet R14-P13-01](https://github.com/banodoco/astrid-dev/blob/5eeccba35565ac7ae12c0c94b4a46dcde785d782/releases/14/packets/R14-P13-01.md)

## Source and purpose

HM1 maps `banodoco/astrid-agent` at **`fc391dea696ec5799db222799a34f9de6a69659b`**, the packet's pinned `release/14/main` snapshot. The Agent Plan 13 branch starts at the same commit. This document changes no product code and proposes no replacement execution framework or scheduler.

`astrid/core/execution/generic_host.py`: **18,784 lines; 188 top-level definitions** (functions and classes, counted once each). SHA-256: `e3f8bec5525fb445f31b68d6a4a9fe9df0776356d8a8e4fe85d9f36257804337`.

This initial draft contains the exhaustive definition census. Responsibility descriptions, method boundaries, caller evidence, shared state and existing-test reachability are being completed before submission. Static references will not be presented as executed coverage.

## Responsibility census

| ID | Responsibility | Top-level definitions |
| --- | --- | ---: |
| R01 | Startup observations | 1 |
| R02 | Runtime protocol and terminal evidence | 11 |
| R03 | Managed inputs and output identities | 9 |
| R04 | Managed execution adapters | 4 |
| R05 | Capabilities and readiness | 29 |
| R06 | Worker bindings, imports and network policy | 23 |
| R07 | Process ownership and cleanup | 10 |
| R08 | Execution contracts, lifetime and storage guards | 25 |
| R09 | Interactive review and discovery | 7 |
| R10 | Source custody and pack capture | 26 |
| R11 | Host coordination and persistent supervision | 8 |
| R12 | Local preparation and authenticated handoff | 21 |
| R13 | Native engine graph | 2 |
| R14 | Activation and CLI lifecycle | 12 |
| Total | Each definition has exactly one owner | 188 |

## Definition inventory

Ranges refer to the pinned source above, including each class body. Class methods are not additional top-level definitions. The large host class will also receive a method-level extraction map.

| Definition | Lines | Responsibility |
| --- | --- | --- |
| `_is_posix` | 95–96 | R07 |
| `_emit_startup_phase` | 99–133 | R01 |
| `_managed_input_staging_name` | 228–235 | R03 |
| `_remotion_readiness_message` | 242–248 | R05 |
| `_structured_failure_kwargs` | 251–262 | R02 |
| `HostError` | 265–270 | R02 |
| `HostLeaseLost` | 273–276 | R02 |
| `_RuntimeOperationFailure` | 279–282 | R02 |
| `_runtime_authority_refusal` | 285–294 | R02 |
| `TerminalPublicationRejected` | 297–298 | R02 |
| `_RuntimeRecoveryIdentityError` | 301–302 | R02 |
| `_TerminalEvidenceNotRecorded` | 305–306 | R02 |
| `_terminal_publication_rejection` | 309–335 | R02 |
| `_persist_terminal_request` | 338–348 | R02 |
| `_RuntimeSourceCustody` | 351–531 | R10 |
| `_consume_runtime_external_sources` | 537–542 | R10 |
| `CommandCleanupUnresolved` | 545–550 | R07 |
| `HostCancelled` | 559–560 | R07 |
| `_managed_asset_identity` | 566–588 | R03 |
| `_settlement_media_type` | 646–677 | R03 |
| `_runtime_output_filename` | 680–708 | R03 |
| `_generation_output_port` | 711–755 | R03 |
| `_generation_selector_declarations` | 758–777 | R03 |
| `StorageEnvelopeError` | 780–785 | R08 |
| `_cleanup_ephemeral_attempt` | 788–804 | R07 |
| `_strict_root_exists` | 807–815 | R07 |
| `_ManagedTaskAdapter` | 818–855 | R04 |
| `_ManagedLocalServerTaskAdapter` | 858–891 | R04 |
| `_attached_cleanup_refusal` | 894–910 | R04 |
| `_ManagedWanChildAdapter` | 915–1225 | R04 |
| `HostRegistrationError` | 1235–1251 | R05 |
| `_normalize_verified_facts` | 1284–1335 | R05 |
| `_installed_vibecomfy_source` | 1338–1345 | R05 |
| `_read_readiness_profile_document` | 1348–1357 | R05 |
| `_registration_verified_facts` | 1360–1367 | R05 |
| `_mapping_value` | 1370–1371 | R05 |
| `_first_int` | 1374–1379 | R05 |
| `_completed_process_evidence` | 1382–1417 | R06 |
| `_bind_host_owned_command_outputs` | 1420–1457 | R06 |
| `_bind_host_owned_command_values` | 1460–1528 | R06 |
| `_prepare_vibecomfy_execution_identity` | 1531–1591 | R06 |
| `_dependency_pythonpath` | 1594–1604 | R06 |
| `_host_product_import_origins` | 1607–1614 | R06 |
| `_install_host_vibecomfy_import_root` | 1617–1686 | R06 |
| `_NetworkBrokerContext` | 1690–1701 | R06 |
| `AdapterSpec` | 1705–1713 | R05 |
| `_parse_remotion_requirement` | 1716–1724 | R05 |
| `AdapterRegistry` | 1727–1799 | R05 |
| `_canonical_digest` | 1802–1803 | R05 |
| `_capability_digest` | 1806–1808 | R05 |
| `_json_safe` | 1811–1821 | R05 |
| `_executor_registration_identity` | 1824–1834 | R05 |
| `_terminate_process_group` | 1837–1854 | R07 |
| `_observe_owned_review_session` | 1861–1905 | R07 |
| `_retire_owned_review_session` | 1908–1922 | R07 |
| `_confined_cwd` | 1925–1947 | R07 |
| `_task_selector` | 1953–1960 | R05 |
| `_renderer_selection` | 1963–1994 | R05 |
| `_gated_remotion_faults` | 1997–2004 | R05 |
| `_preflight_unavailable_reason` | 2007–2027 | R05 |
| `_is_withdrawn` | 2033–2036 | R05 |
| `_withdrawn_reason` | 2039–2044 | R05 |
| `_required_secret_names` | 2047–2082 | R06 |
| `_required_env_names` | 2085–2097 | R06 |
| `_fixed_worker_environment` | 2100–2112 | R06 |
| `_record_may_render` | 2115–2122 | R05 |
| `_launch_worker_probe_environments` | 2125–2265 | R06 |
| `_command_worker_pythonpath` | 2268–2278 | R06 |
| `_resolve_credential_value` | 2281–2321 | R06 |
| `_network_policy` | 2324–2341 | R06 |
| `_provider_routes` | 2344–2379 | R06 |
| `_host_managed_broker` | 2382–2389 | R06 |
| `_tcp_broker_supports` | 2392–2399 | R06 |
| `_network_startup_argv` | 2452–2484 | R06 |
| `_captured_worker_argv` | 2487–2502 | R06 |
| `_network_sandbox_argv` | 2505–2537 | R06 |
| `_native_network_command` | 2540–2548 | R06 |
| `_enforceable_network_gateway` | 2551–2564 | R06 |
| `_attempt_tree_bytes` | 2575–2600 | R08 |
| `_storage_tree_bytes` | 2603–2628 | R08 |
| `_storage_path_class` | 2641–2658 | R08 |
| `_storage_envelope_measurement` | 2661–2737 | R08 |
| `_fixed_request_scope` | 2740–2750 | R08 |
| `_admitted_spec_envelope` | 2753–2785 | R08 |
| `_admitted_task_spec` | 2788–2790 | R08 |
| `_assert_verified_placement_binding` | 2793–2828 | R08 |
| `_execution_contract` | 2831–2979 | R08 |
| `_ReviewIntervalAccounting` | 2983–3034 | R08 |
| `_AttemptLifetime` | 3038–3111 | R08 |
| `_interactive_admission_spec` | 3114–3118 | R09 |
| `_interactive_review_authority` | 3121–3347 | R09 |
| `_DiscoveryCollection` | 3350–3806 | R09 |
| `_iteration_video_discovery` | 3809–3941 | R09 |
| `_training_review_media_scope` | 3949–4161 | R09 |
| `_training_review_authority` | 4164–4364 | R09 |
| `_contract_queue_age` | 4367–4380 | R08 |
| `_assert_fixed_request_scope` | 4383–4412 | R08 |
| `_storage_input_limits` | 4415–4429 | R08 |
| `_task_storage_estimate` | 4432–4449 | R08 |
| `_claim_field` | 4473–4476 | R08 |
| `_claim_blocked_capability` | 4479–4488 | R08 |
| `_evidence_cap_message` | 4491–4495 | R08 |
| `_task_storage_limits` | 4498–4502 | R08 |
| `_render_media_roots` | 4505–4511 | R08 |
| `_host_log_root` | 4514–4516 | R08 |
| `_collected_log_roots` | 4519–4537 | R08 |
| `_assert_live_storage_envelope` | 4540–4601 | R08 |
| `_task_storage_envelope` | 4604–4671 | R08 |
| `source_checkout_digest` | 4674–4684 | R10 |
| `process_birth_identity` | 4687–4689 | R10 |
| `_admitted_source_roots` | 4692–4703 | R10 |
| `_admitted_python_roots` | 4706–4724 | R10 |
| `_source_digest_for_roots` | 4727–4736 | R10 |
| `_run_source_digest` | 4739–4753 | R10 |
| `_pack_stat_identity` | 4756–4767 | R10 |
| `_pack_capture_inventory` | 4770–4794 | R10 |
| `PackCaptureError` | 4797–4799 | R10 |
| `_remove_pack_snapshot` | 4802–4814 | R10 |
| `_portable_pack_capture` | 4818–4887 | R10 |
| `_relocate_pack_definition` | 4890–4906 | R10 |
| `_relocate_pack_record` | 4909–4914 | R10 |
| `_unavailable_pack_capture` | 4918–4921 | R10 |
| `_select_pack_capture` | 4924–4933 | R10 |
| `_selected_pack_capture` | 4937–4983 | R10 |
| `_selected_pack_generation` | 4986–5004 | R10 |
| `_run_pack_provenance` | 5012–5080 | R10 |
| `_verify_action_admission` | 5083–5113 | R10 |
| `_verify_admitted_source` | 5117–5142 | R10 |
| `_vcs_revision` | 5145–5163 | R10 |
| `_dependency_digest` | 5166–5180 | R10 |
| `_pack_root_for_executor` | 5183–5193 | R10 |
| `_attach_pack_metadata` | 5196–5216 | R10 |
| `_OrchestratorRecord` | 5220–5228 | R05 |
| `CapabilityRecord` | 5232–5327 | R05 |
| `_prepare_review_resume_input` | 5330–5384 | R09 |
| `RuntimeProtocolClient` | 5387–6259 | R02 |
| `_unapproved_reason` | 6266–6271 | R05 |
| `_quarantine_scope` | 6274–6287 | R05 |
| `_inside_quarantined` | 6290–6294 | R05 |
| `component_load_failures` | 6297–6335 | R05 |
| `executor_skip_section` | 6338–6344 | R05 |
| `_configured_claim_target` | 6347–6374 | R11 |
| `_startup_identity_attestation` | 6377–6444 | R11 |
| `_publish_busy` | 6452–6472 | R11 |
| `_TaskOutputCapture` | 6475–6651 | R11 |
| `_local_machine` | 6654–6663 | R11 |
| `_machine_align_mode` | 6666–6671 | R11 |
| `_align_admission` | 6674–6685 | R11 |
| `GenericPackHost` | 6688–15028 | R11 |
| `_compose_cli_boot_manifest` | 15031–15055 | R14 |
| `_write_ready_marker` | 15058–15072 | R14 |
| `_handoff_canonical` | 15101–15105 | R12 |
| `_handoff_digest` | 15108–15109 | R12 |
| `_handoff_reject_duplicate_pairs` | 15112–15118 | R12 |
| `_handoff_reject_constant` | 15121–15122 | R12 |
| `_handoff_actor_valid` | 15125–15136 | R12 |
| `_handoff_role_valid` | 15139–15148 | R12 |
| `_handoff_sha256` | 15151–15153 | R12 |
| `_handoff_runtime_binding_valid` | 15156–15174 | R12 |
| `_handoff_live_runtime_binding` | 15177–15232 | R12 |
| `_handoff_registered_state` | 15235–15294 | R12 |
| `_handoff_historical_registration` | 15297–15348 | R12 |
| `_handoff_read_protected_json` | 15351–15385 | R12 |
| `_handoff_read_private_bytes` | 15388–15406 | R12 |
| `_handoff_journal_base` | 15409–15423 | R12 |
| `_handoff_journal_entry` | 15426–15435 | R12 |
| `_handoff_ownership_matches` | 15438–15443 | R12 |
| `_handoff_runtime_writer_matches` | 15446–15451 | R12 |
| `_handoff_transfer_writers_match` | 15454–15459 | R12 |
| `_handoff_designation` | 15462–15482 | R12 |
| `_validate_local_engine_profile` | 15492–15531 | R12 |
| `LocalExecutionPreparation` | 15538–17297 | R12 |
| `_named_raw_publication_port` | 17301–17312 | R03 |
| `_task_generation_intent` | 17315–17346 | R03 |
| `_bind_named_parent_output` | 17349–17372 | R03 |
| `_selected_birth_matches` | 17375–17381 | R07 |
| `_NativeEngineGraph` | 17384–17797 | R13 |
| `_retain_unresolved_owner` | 17800–17807 | R13 |
| `_read_activation_frame` | 17810–17832 | R14 |
| `_send_activation_frame` | 17835–17838 | R14 |
| `_await_worker_activation` | 17841–17957 | R14 |
| `_await_worker_activation_socket` | 17960–18021 | R14 |
| `_await_enabled_runtime_credential` | 18024–18039 | R14 |
| `_handle_host_shutdown_signal` | 18045–18065 | R14 |
| `_ManagedStdinShutdown` | 18068–18130 | R14 |
| `_log_cli_exit_failure` | 18133–18145 | R14 |
| `_cli` | 18148–18159 | R14 |
| `_cli_impl` | 18162–18753 | R14 |

## Reproduce the definition count

Run from the Agent checkout. The source is read from the commit, not the worktree.

```sh
git show fc391dea696ec5799db222799a34f9de6a69659b:astrid/core/execution/generic_host.py > /tmp/r14-p13-generic-host.py
python3 - <<'PY'
import ast
from pathlib import Path
tree = ast.parse(Path('/tmp/r14-p13-generic-host.py').read_text(encoding='utf-8'))
definitions = [node for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
print(len(definitions))
for node in definitions:
    print(node.name, node.lineno, node.end_lineno)
PY
```

Observed: **188**. The submitted version will include the map-to-source equality check and the recorded caller searches.
