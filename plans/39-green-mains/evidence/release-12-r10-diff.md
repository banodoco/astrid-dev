# Release 12: Agent CI regressions against Release 10

[Plan 39](../inputs.md) · [Tasks](../tasks.md)

## Purpose

Release 12's gate compares Agent CI with Release 10. That comparison found 398 test ids that pass on Release 10 and fail on the release 12 candidate. Every cause traces to commits already in served release 11 (`a105de3a`), mainly the 5 November pack-framework port, the move of 20 packs to `poms_packs`, and dependency pin bumps. None comes from release 12's own work.

**Owner decision (Hannah, 10 Nov 2026):** release 12 fixes every *product* regression against Release 10. Stale tests, test-infra drift and the Mypy debt move to Plan 39. Release 12's no-regression judgement for those is made against served release 11 and `main`. See [inputs D8](../inputs.md#owner-decisions).

## Source

- Candidate: Agent CI run [42760780918](https://github.com/banodoco/astrid-agent/actions/runs/42760780918) on `aa5bc442f`.
- Baseline: Release 10 Agent CI run [42602166253](https://github.com/banodoco/astrid-agent/actions/runs/42602166253) on `72462b04`.
- Method: FAILED/ERROR ids from each shard's short summary (including "ERROR at setup of"; pytest-9 SUBFAILED folded into its parent), compared against the union of all Release 10 shards. The "ran" set comes from each shard's `test-durations` artifact, because CI runs `pytest -q` without `-rA`. `env/baseline-diff.py` produced the sets.
- Environment: runner images, Python 3.11.18, apt packages, step list and `ci.yml` are identical in both runs. No cause is a CI-environment change.
- Release 10's unit shard 8 log is gone (BlobNotFound). Its 2161-test membership was rebuilt locally; 63 ids that ran there have no baseline (listed below).

## Totals

| Set | Count |
|---|---|
| Failing or erroring at the candidate (unit plus darwin) | 1482 + 13 |
| Failing or erroring at Release 10 | 1010 |
| Pass on Release 10, fail at the candidate (regressions) | 398 |
| No baseline: ran only in Release 10's lost shard 8 | 63 |
| No baseline: new tests | 99 |

By shard: s1 47, s2 52, s3 1, s4 156, s5 95, s6 30, s7 13, s8 0, darwin 4.

## Causes

Local check means one or more tests were run at both commits, with Python 3.11.18 and CI-matching packages.

| Cause | Tests | Class | Owner | Local check | Evidence |
|---|---|---|---|---|---|
| C10 pack framework port: v3-only admission, core-hosted hivemind, discovery/registry semantics | 132 | product change (Plan 06 pack-framework port edaa8e7c10, Nov 5), intended; stale R10 test fixtures | Plan 39 (AT1/AT2 card below) | inferred; 1 confirmed locally | 73/132 blocks show v1/v2 fixture quarantine ('explicit schema upgrade'); 21/36 files write schema_version 1/2 packs; 20 see core-hosted hivemind (intended per bd2778b782 M-26) |
| C3 stale test double after product API change | 44 | test-infra: stale test doubles after product API change | Plan 39 (AT1/AT2 card below) | confirmed (1 run both SHAs) | renderer_environment_identity() now takes config (d4665c5c3f) but test monkeypatches a 0-arg lambda; CLI handlers now wrapped (_provided/guard) |
| C2 moved packs (poms_packs): test still references removed pack/element/executor | 43 | product change (20 packs moved to poms_packs, Nov 7); stale tests | Plan 39 (AT1/AT2 card below) | confirmed (1 run both SHAs) | astrid/packs/{iteration,moirae,editorial,video_editing,fal,...} absent at head; v6_pushed_clips uses am-presenter/am-snap-plate |
| C5 runpod-lifecycle pin bump (agent reaps drained jobs) | 39 | dependency bump: runpod-lifecycle 96360a2->f294881 (pyproject); stale test helper | Plan 39 (AT1/AT2 card below) | confirmed (39/39 pass at head with old pin) | lifecycle c47fa76 evict_drained_jobs(): LoopbackPod.record_count=len(agent.jobs) no longer cumulative |
| C1a moved am-* elements: element_schema() fails open (refusals lost) | 31 | PRODUCT REGRESSION: element_schema() fails open for moved am-* elements | Release 12 (`r12/r10-regressions`, `r12/r10-schema-fail-closed`) | confirmed | head element_schema('am-sprite')=={} and validate_param_value accepts x='not-a-number' (R10 refuses); scans in-tree astrid/packs only |
| C9 pack framework port: retired `local` pack (shipped effects unregistered) | 28 | PRODUCT REGRESSION: retired `local` pack id hides 15 shipped effects | Release 12 for 21; Plan 39 for 7 misfiled (see AT1.7) | confirmed | default element registry 43->9; frame-overlay, animated-media-transform etc. still in astrid/packs/local and in wheel package-data but unregistered |
| C4 CI env: ASTRID_TEST_LIFECYCLE_CHECKOUT unset | 23 | CI setup: ASTRID_TEST_LIFECYCLE_CHECKOUT not provided by ci.yml | Release 12 (CI setting); Plan 39 AT1.4 if not landed | confirmed (passes with env set) | unit test imports new integration fixture (test_runpod_host_endpoint_r5); only scripts/worker-env/agent-pytest-pod.sh sets it |
| C13 engine/model lock + VibeComfy pin bump (data/dependency) | 18 | dependency/data: engine model lock + VibeComfy pin e2905d0->e65f494 | Release 12 (VibeComfy binding fix); Plan 39 for the rest | 1 confirmed, rest inferred | VibeComfy now rejects COMBO 'device' vs CHOICE public input (WorkflowCompileError); old VibeComfy -> missing_dependency; models.lock.json +270 lines |
| C8 installer: staged root needs runtime.lock.json (G16) vs R10-era fixtures | 10 | product change (G16 fix 5fa923acfb) vs R10-era installer fixtures merged from main | Plan 39 (AT1/AT2 card below) | confirmed (1) | staged root must contain runtime.lock.json; fixtures don't |
| C14 Plan 33 generation surface: new align/target_policy args vs pinned arg sets | 7 | product change: Plan 33 U2 align/target_policy args; tests pin old arg sets | Plan 39 (AT1/AT2 card below) | inferred | extra 'align'/'target_policy' keys in diffs |
| C6 engine model lock grew: pod disk-size expectations stale | 6 | data change: engine footprint 106 GB; hardcoded 84/120 GB expectations | Plan 39 (AT1/AT2 card below) | confirmed (fail with either lifecycle) | recipe_footprint_gb()=106 |
| C12 PK06 port dropped comfy_wrap -> vibecomfy mapping | 5 | PRODUCT REGRESSION (likely unintended port loss): comfy_wrap.run lost vibecomfy GPU/local_generation mapping | Release 12 (`r12/r10-regressions`, `r12/r10-schema-fail-closed`) | confirmed (1) | 2caeb813fa removed the mapping; test unchanged since R10 |
| C7 pod H3 install: canonical engine install path changed | 5 | product change: pod H3 canonical install path; error codes now engine_error | Plan 39 (AT1/AT2 card below) | inferred | fails with either lifecycle pin |
| C11 generic host: delegated child needs admitted source digest | 4 | product change: delegated child requires admitted_source_digest; fixtures lack it | Plan 39 (AT1/AT2 card below) | inferred | ChildBridgeError/HostError raised before launch |
| C15 committed generated artifacts stale (capability index, artifact manifest, doc catalog) | 3 | repo hygiene: committed generated artifacts not regenerated | Plan 39 (AT1/AT2 card below) | inferred | test asks to rerun gen_capability_index/artifact_manifest |

## Mypy

- The gate counts against the committed `scripts/reshape/baselines/mypy_astrid.json` (2192, count only, last changed 1 Nov). It is identical at both commits.
- Release 10 never ran Mypy: its `fast checks` job stopped at Ruff. Once Ruff was fixed, the debt showed. CI at the candidate reports 2345 ("regressed by 153").
- Locally: Release 10 2350, candidate 2388. That is about 216 new findings and 178 gone across the range.
- Blame of every new finding: none comes from release 12's commits. 150 come from `edaa8e7c10` and 29 from `c61acfd93b` (both 5 Nov ports); 19 are on pre-Release-10 lines. `astrid/core/pack/transaction.py` has 42 new findings, all blaming to `edaa8e7c10`.

## The default-floor test

`test_the_default_floor_matches_the_runtime` is marked `integration`, so it is deselected in every unit shard. Only the Agent Lanes integration lane runs it. At Release 10 all four integration shards stopped at collection (A-c), so it has not run at either commit. Release 12's final round runs `lanes.yml`.

## Test ids by cause

<details><summary>C10 pack framework port: v3-only admission, core-hosted hivemind, discovery/registry semantics (132)</summary>

```
tests/core/execution/test_generic_host_actions_v3.py::test_python_action_receives_original_host_bridge_before_import
tests/core/execution/test_generic_host_child_bridge_d18.py::test_prepared_submission_rechecks_between_upload_and_admission[cancelled]
tests/core/execution/test_generic_host_child_bridge_d18.py::test_prepared_submission_rechecks_between_upload_and_admission[lease]
tests/core/execution/test_generic_host_child_bridge_d18.py::test_prepared_submission_rechecks_between_upload_and_admission[source]
tests/core/execution/test_private_network_command.py::test_private_leaf_command_installs_network_before_pack_code[None--m]
tests/core/execution/test_private_network_command.py::test_private_leaf_command_installs_network_before_pack_code[changed_hook--m]
tests/core/execution/test_private_network_command.py::test_private_leaf_command_installs_network_before_pack_code[missing_hook--m]
tests/core/execution/test_private_network_command.py::test_private_leaf_command_installs_network_before_pack_code[missing_policy--m]
tests/core/generation/test_discovery_scope.py::test_changed_tree_is_readmitted_and_invalid_inputs_fail_closed[alternate]
tests/core/generation/test_discovery_scope.py::test_changed_tree_is_readmitted_and_invalid_inputs_fail_closed[duplicate_yaml]
tests/core/generation/test_discovery_scope.py::test_changed_tree_is_readmitted_and_invalid_inputs_fail_closed[resource]
tests/core/generation/test_discovery_scope.py::test_changed_tree_is_readmitted_and_invalid_inputs_fail_closed[symlink]
tests/core/generation/test_discovery_scope.py::test_changes_during_admission_do_not_publish_a_snapshot
tests/core/generation/test_discovery_scope.py::test_cli_scope_is_per_dry_run_and_is_reset_on_failure
tests/core/generation/test_discovery_scope.py::test_every_layer_and_same_size_manifest_edits_are_observed
tests/core/generation/test_discovery_scope.py::test_literal_project_root_does_not_alias_expanded_home
tests/core/generation/test_discovery_scope.py::test_model_registry_rediscovers_added_changed_and_duplicate_backends
tests/core/generation/test_discovery_scope.py::test_reuse_does_not_share_mutable_definitions
tests/core/generation/test_discovery_scope.py::test_symlinked_external_root_tracks_target_contents
tests/core/model_catalog/test_registry.py::TestPackDeclaredBackendIds::test_load_default_accepts_pack_declared_backend_id
tests/core/pack/test_v3_core_worker_luna.py::test_non_strict_pack_scan_quarantines_optional_failure_without_downgrading_discovery
tests/core/rendering/test_installed_registry_security.py::test_installed_product_network_workers_remain_projectable[capture-capture.web_page]
tests/core/rendering/test_registry.py::test_alias_cycle_is_rejected_as_structured_registry_error
tests/core/rendering/test_registry.py::test_cross_pack_alias_fallback_is_rejected_by_v2_ownership
tests/core/rendering/test_registry.py::test_cross_pack_shared_alias_is_rejected_by_v2_ownership
tests/core/rendering/test_registry.py::test_cross_pack_two_hop_alias_to_env_is_rejected_by_v2_ownership
tests/core/rendering/test_registry.py::test_cross_pack_two_hop_alias_to_missing_is_rejected_by_v2_ownership
tests/core/rendering/test_registry.py::test_default_loader_returns_all_three_registry_types
tests/core/rendering/test_registry.py::test_discovery_is_static_and_never_imports_or_executes_backend_code
tests/core/rendering/test_registry.py::test_manifest_permission_not_declared_by_pack_is_ineligible
tests/core/rendering/test_registry.py::test_priority_index_selects_the_lowest_index_and_conflicts_are_reported
tests/core/rendering/test_registry.py::test_renderer_manifest_cannot_register_the_facade_id
tests/core/rendering/test_registry.py::test_resolve_evidence_has_required_selection_and_trust_shape
tests/core/rendering/test_registry.py::test_same_pack_conflict_report_is_deterministic
tests/core/rendering/test_registry.py::test_source_and_project_local_candidates_are_executable
tests/core/rendering/test_registry_matrix.py::test_cross_layer_precedence_winner_is_recorded_in_evidence_and_conflicts
tests/core/rendering/test_registry_matrix.py::test_cross_pack_alias_to_absent_canonical_fails_v2_admission
tests/core/rendering/test_registry_matrix.py::test_cross_pack_qualified_id_squatting_is_rejected_deterministically
tests/core/rendering/test_registry_matrix.py::test_env_candidate_cannot_shadow_eligible_extra_in_natural_discovery_order
tests/core/rendering/test_registry_matrix.py::test_ineligible_duplicate_manifest_is_excluded_from_conflicts_and_execution
tests/core/rendering/test_registry_matrix.py::test_multiple_conflicts_are_reported_in_deterministic_key_order
tests/core/rendering/test_registry_matrix.py::test_permission_deficiency_reason_lists_all_missing_permissions_sorted
tests/core/rendering/test_registry_matrix.py::test_resolve_evidence_records_canonical_selection_and_eligibility
tests/core/rendering/test_registry_matrix.py::test_static_load_and_read_surface_never_imports_fixture_backend_modules
tests/core/test_editor_element_catalog.py::test_projection_covers_every_editor_element_kind
tests/core/test_element_kind_registry.py::PackDeclaredKindLoadingTest::test_load_pack_elements_derives_pack_declared_kinds
tests/core/test_elements_cli.py::ElementsCliTest::test_invalid_kind_error_lists_dynamic_valid_kinds
tests/core/test_elements_cli.py::ElementsCliTest::test_pack_declared_kind_is_searchable_in_cli
tests/core/test_elements_cli.py::ElementsCliTest::test_pack_declared_kind_works_in_cli
tests/core/test_executor_registry_snapshot.py::ExecutorRegistrySnapshotTests::test_validate_all_detects_missing_dependency
tests/core/test_generation_backend_registry.py::test_pack_descriptor_roundtrip_and_discovery_are_inert
tests/core/test_generation_taxonomy_registry.py::test_load_default_generation_taxonomy_registry_adds_pack_declared_ids
tests/core/test_pack_coherence_elements.py::test_v3_element_resources_wire_helper_identity_into_both_projections
tests/packs/rendering/test_remotion_element_generation.py::RemotionElementGenerationTest::test_generated_effect_registry_hashes_manifest_component_support_and_assets
tests/packs/test_executor_admission.py::ExecutorDescriptionAdmissionTest::test_discovery_skips_the_bad_executor_and_names_it_in_doctor
tests/packs/test_generation_verb_extensions.py::test_v3_pack_discovery_preserves_generation_verb_extensions
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_canonical_content_roots_are_used_for_discovery
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_duplicate_executor_id_uses_priority_based_shadowing
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_env_layer_ordered_after_extra
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_hidden_pack_is_excluded_by_default
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_misplaced_element_pack_id_fails_pack_alignment
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_misplaced_executor_id_fails_pack_alignment
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_misplaced_orchestrator_id_fails_pack_alignment
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_no_env_var_falls_through_gracefully
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_pack_folder_must_match_pack_id
tests/packs/test_pack_discovery.py::PackDiscoveryTest::test_valid_pack_discovery_and_content_loaders
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_discover_packs_ordered_returns_pack_definitions
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_env_layer_uses_pathsep_and_skips_empty_or_missing_entries
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_existing_invalid_local_pack_manifest_is_not_overwritten
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_extra_roots_layer_excludes_local
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_local_layer_only_keeps_local_pack
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_local_layer_requires_an_authored_manifest
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_registries_share_identical_ordering
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_rendering_consumers_receive_source_kind_and_priority_metadata
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_same_canonical_external_root_is_scanned_once
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_skill_roots_are_empty_without_a_skill_documentation_declaration
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_skill_roots_expose_only_the_declared_pack_skill
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_source_layer_excludes_local_and_indexes_in_order
tests/packs/test_pack_discovery_single_scan.py::test_different_roots_keep_project_scan_and_do_not_leak_source_local
tests/packs/test_pack_discovery_single_scan.py::test_discovery_observes_edits_on_every_call
tests/packs/test_pack_discovery_single_scan.py::test_injected_scanner_keeps_argument_specific_authority_even_with_equal_roots
tests/packs/test_pack_discovery_single_scan.py::test_local_eligibility_is_observational[absent]
tests/packs/test_pack_discovery_single_scan.py::test_local_eligibility_is_observational[hidden]
tests/packs/test_pack_discovery_single_scan.py::test_local_eligibility_is_observational[manifestless]
tests/packs/test_pack_discovery_single_scan.py::test_managed_identity_guard_is_unchanged
tests/packs/test_pack_discovery_single_scan.py::test_same_authority_reuses_full_scan_only_with_builtin_scanner[False-checkout]
tests/packs/test_pack_discovery_single_scan.py::test_same_authority_reuses_full_scan_only_with_builtin_scanner[False-site-packages]
tests/packs/test_pack_discovery_single_scan.py::test_same_authority_reuses_full_scan_only_with_builtin_scanner[True-checkout]
tests/packs/test_pack_discovery_single_scan.py::test_same_authority_reuses_full_scan_only_with_builtin_scanner[True-site-packages]
tests/packs/test_pack_discovery_single_scan.py::test_scan_reuse_preserves_strict_manifest_and_path_guards[alternate]
tests/packs/test_pack_discovery_single_scan.py::test_scan_reuse_preserves_strict_manifest_and_path_guards[hidden]
tests/packs/test_pack_discovery_single_scan.py::test_scan_reuse_preserves_strict_manifest_and_path_guards[local]
tests/packs/test_pack_discovery_single_scan.py::test_scan_reuse_preserves_strict_manifest_and_path_guards[path]
tests/packs/test_pack_discovery_single_scan.py::test_scan_reuse_preserves_strict_manifest_and_path_guards[source]
tests/packs/test_pack_discovery_single_scan.py::test_scan_reuse_preserves_strict_manifest_and_path_guards[symlink]
tests/packs/test_pack_discovery_v3.py::test_broken_source_remains_strict_and_core_shell_is_not_a_pack
tests/packs/test_pack_discovery_v3.py::test_external_broken_hidden_and_duplicate_roots_are_isolated[discover_pack_metadata]
tests/packs/test_pack_discovery_v3.py::test_layer_priority_and_managed_identity_are_preserved
tests/packs/test_pack_discovery_v3.py::test_v2_and_v3_discover_one_declared_skill[2]
tests/packs/test_pack_discovery_v3.py::test_v2_and_v3_discover_one_declared_skill[3]
tests/packs/test_pack_quarantine.py::test_approve_regenerates_lock_and_keeps_quarantined_approvals
tests/packs/test_pack_quarantine.py::test_doctor_section_lists_quarantine_with_error_and_fix
tests/packs/test_pack_quarantine.py::test_invalid_keyword_quarantines_only_that_pack
tests/packs/test_pack_quarantine.py::test_invoking_a_quarantined_capability_is_typed_unavailable
tests/packs/test_pack_quarantine.py::test_quarantine_owner_matches_declared_bare_labels
tests/packs/test_pack_quarantine.py::test_unapproved_capability_is_unavailable_without_stopping_host
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[iteration]
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[moirae]
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[rendering]
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[runpod]
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[training]
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[vibecomfy]
tests/packs/test_portfolio_parity.py::test_pack_manifest_v3_compliant[youtube]
tests/packs/test_portfolio_parity.py::test_resolver_discovers_pack[iteration]
tests/packs/test_portfolio_parity.py::test_resolver_discovers_pack[moirae]
tests/packs/test_portfolio_parity.py::test_resolver_discovers_pack[youtube]
tests/packs/timeline/test_verbs_working_copy.py::test_duplicate_is_all_or_nothing
tests/sdk/test_scene_save_core.py::test_publish_still_refuses_core_invalidity_before_writing[type]
tests/sdk/test_timeline_import_prepare.py::test_builtin_hold_clip_round_trips_through_inventory_and_prepare
tests/sdk/test_timeline_import_prepare.py::test_inventory_to_prepare_reports_unknown_unpinned_transition_from_source_pack
tests/stage1/test_capability_parity_gate_luna.py::test_stage1_capability_parity_is_explicit_and_family_proven
tests/stage1/test_core_import_authority.py::test_sdk_dry_run_is_manifest_only_and_does_not_load_runtime_authority
tests/stage1/test_generic_host_process_bootstrap_luna.py::test_generic_host_process_preflights_and_reports_readiness
tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_discovers_explicit_astrid_packs_path_without_default_scan
tests/stage1/test_zero_shim_execution_pack_deletion.py::test_in_process_runtime_and_pack_install_authority_are_absent
tests/stage1/test_zero_shim_execution_pack_deletion.py::test_supported_cleanup_paths_use_kernel_custody_and_anchored_group_signal
tests/test_env_vars_conformance.py::TestNoBareStringAccess::test_no_catalogued_bare_strings_in_core
tests/test_external_pack_contract.py::test_external_pack_via_env_path
tests/test_omp_agent.py::test_installed_prompt_notice_preserves_overrides_and_names_packaged_skills
tests/test_provider_route_grant.py::test_provider_route_grant_reads_runtime_nested_task_inputs
tests/test_provider_route_grant.py::test_provider_run_requires_explicit_grant
tests/test_provider_route_grant.py::test_tcp_only_broker_retires_udp_even_when_manifest_marks_broker_managed
```

</details>

<details><summary>C3 stale test double after product API change (44)</summary>

```
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[assets-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[candidate-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[compiled_map-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[frame-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[profile-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[renderer-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[resolution-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[revision-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_capture_input_cannot_reuse_rows[source-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_changed_renderer_identity_is_a_cache_miss[transport]
tests/packs/rendering/test_scene_cache_payload.py::test_ephemeral_attempt_retry_reuses_the_same_entry[transport]
tests/packs/rendering/test_scene_cache_payload.py::test_mixed_payload_batch_keeps_fresh_observations_separate[transport]
tests/packs/rendering/test_scene_cache_payload.py::test_new_provider_reuses_rows_without_query_or_private_visibility[transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[addresses-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[basis-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[frame-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[key-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[malformed-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[png_sha256-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_bindings_checked_after_owner_integrity[source_identity-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_payload_counts_toward_existing_cache_caps[transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_other_frame_entry_is_a_miss[transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[addresses-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[basis-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[forged_row-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[frame-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[key-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[malformed-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[png-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[root_source-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[source_identity-transport]
tests/packs/rendering/test_scene_cache_payload.py::test_untrusted_cache_owner_renders_fresh_even_with_matching_disk_hashes[transport]
tests/packs/rendering/test_timeline_storyboard.py::test_discord_inputs_sort_bare_then_numeric_through_ten
tests/packs/rendering/test_timeline_storyboard.py::test_placeholder_flag_distinguishes_media_shots_from_slots
tests/packs/rendering/test_timeline_storyboard.py::test_placeholder_shot_carries_prompt_metadata_and_authored_bounds
tests/packs/timeline/test_cli_edit_flags.py::test_edit_parses_to_its_handler[argv0]
tests/packs/timeline/test_cli_edit_flags.py::test_edit_parses_to_its_handler[argv1]
tests/packs/timeline/test_cli_find.py::test_find_verb_registered_and_a_miss_suggests_nearest_phrases
tests/packs/timeline/test_cli_v3_sweep_log.py::test_timeline_cli_binds_check_log_and_sweep_to_the_shared_client
tests/packs/timeline/test_verbs_working_copy.py::test_each_verb_parses_to_its_handler[argv0-_cmd_words]
tests/packs/timeline/test_verbs_working_copy.py::test_each_verb_parses_to_its_handler[argv1-_cmd_lines]
tests/packs/timeline/test_verbs_working_copy.py::test_each_verb_parses_to_its_handler[argv2-_cmd_lint]
tests/packs/timeline/test_verbs_working_copy.py::test_each_verb_parses_to_its_handler[argv3-_cmd_discard]
tests/packs/timeline/test_verbs_working_copy.py::test_each_verb_parses_to_its_handler[argv4-_cmd_duplicate]
```

</details>

<details><summary>C2 moved packs (poms_packs): test still references removed pack/element/executor (43)</summary>

```
tests/editing_conformance/test_commit_fps_d12.py::test_legacy_parity_exemption_still_runs_structure_reference_schema_and_timing_guards
tests/editing_conformance/test_commit_legacy_text_reference.py::test_legacy_text_reference_still_validates_native_clip_parameters
tests/editing_conformance/test_commit_v2_validation.py::test_known_element_parameter_uses_declared_value_schema
tests/editing_conformance/test_commit_v2_validation.py::test_sealed_builtin_rejects_new_undeclared_parameter_but_retains_opaque_history
tests/packs/rendering/test_timeline_transfer_actions.py::test_check_only_stages_project_scoped_summary_without_prepared_body
tests/packs/rendering/test_timeline_visualize_motion.py::test_motion_layer_registry_and_v3_element_lookup
tests/packs/rendering/test_timeline_visualize_motion_views.py::test_a_real_v6_push_comes_from_the_element
tests/packs/rendering/test_timeline_visualize_motion_views.py::test_the_fallback_mirror_still_matches_the_element_on_v6_pushes
tests/packs/test_pack_migration_m4_shells.py::TestCorePackTaxonomyV3::test_core_pack_taxonomy_and_declared_content_kinds
tests/packs/test_pack_migration_m4_shells.py::TestCorePackTaxonomyV3::test_declared_rendering_elements_match_element_manifests_on_disk
tests/packs/test_pack_run_cli_choices.py::PackRunCliChoicesTests::test_importable_pack_parsers_use_static_choices
tests/packs/test_packs_validate.py::TestFirstPartyPacksRootValidation::test_inventory_and_layout_fail_under_one_aggregate_surface
tests/packs/test_portfolio_parity.py::test_action_declarations_v3_compliant[iteration]
tests/packs/test_portfolio_parity.py::test_action_declarations_v3_compliant[moirae]
tests/packs/test_portfolio_parity.py::test_action_declarations_v3_compliant[youtube]
tests/packs/test_portfolio_parity.py::test_representative_executor_dispatches_external[iteration]
tests/packs/test_portfolio_parity.py::test_representative_executor_dispatches_external[moirae]
tests/packs/test_portfolio_parity.py::test_representative_executor_dispatches_external[youtube]
tests/packs/test_portfolio_parity.py::test_validator_accepts_pack[iteration]
tests/packs/test_portfolio_parity.py::test_validator_accepts_pack[moirae]
tests/packs/test_portfolio_parity.py::test_validator_accepts_pack[youtube]
tests/sdk/test_generation_variant_publication.py::test_specialized_publication_actions_opt_in_through_registered_metadata
tests/sdk/test_timeline_look.py::test_set_volume_on_an_element_that_declares_volume_keeps_writing_the_param
tests/sdk/test_timeline_revision_diff_admission.py::test_element_resource_producer_binds_real_admitted_motion_without_config_mutation
tests/stage1/test_asset_cache_retired_luna.py::test_live_media_code_has_no_retired_asset_cache_boundary
tests/stage1/test_final_render_authority_luna.py::test_attached_render_module_and_nested_runner_are_deleted
tests/stage1/test_kernel_admission_runtime.py::test_admission_and_normal_callers_have_no_local_composition
tests/stage1/test_thread_authority_cutover.py::test_live_pack_imports_do_not_reach_retired_thread_store
tests/stage1/test_thread_authority_cutover.py::test_logo_dry_run_publishes_manifest_without_variant_sidecar
tests/stage1/test_thread_authority_cutover.py::test_video_editing_orchestrators_have_no_pack_event_sidecar_writer
tests/stage1/test_zero_shim_lane_c.py::test_iteration_does_not_write_run_sidecars[astrid/packs/iteration/actions/experiment_import/run.py]
tests/stage1/test_zero_shim_lane_c.py::test_iteration_does_not_write_run_sidecars[astrid/packs/iteration/actions/experiment_prepare/run.py]
tests/stage1/test_zero_shim_timeline_cutover_luna.py::test_pack_workers_are_result_only_and_have_no_timeline_write_binding
tests/test_canonical_aliases.py::CanonicalAliasTest::test_executor_api_uses_canonical_implementation
tests/test_creator_entry_declarations.py::test_changed_pack_declarations_pass_pack_validation
tests/test_creator_entry_declarations.py::test_only_declared_generation_actions_carry_generation_publication
tests/test_creator_entry_declarations.py::test_pack_intent_projection_keeps_creator_selection_clear
tests/test_live_capability_discovery_fix.py::test_hype_inputs_are_typed_and_preserved_in_command
tests/test_live_capability_discovery_fix.py::test_networked_transcribe_sdk_dispatch_does_not_trip_orchestrator_guard
tests/test_live_capability_discovery_fix.py::test_networked_understanding_describes_credentials_and_outputs
tests/test_live_capability_discovery_fix.py::test_understand_dry_run_validates_mode_and_selected_modality
tests/test_omp_agent.py::test_packaged_profile_resolves_skills_inside_selected_installation
tests/test_platform_matrix.py::test_generation_platform_matrix_references_existing_packs_and_sources
```

</details>

<details><summary>C5 runpod-lifecycle pin bump (agent reaps drained jobs) (39)</summary>

```
tests/scripts/test_pod_held_budget.py::test_late_staging_failure_measures_four_record_shortfall
tests/scripts/test_pod_held_budget.py::test_staged_candidate_plus_installer_h3_measured_budget
tests/scripts/test_pod_held_budget.py::test_staging_failure_and_exact_reconciliation_measured_allowance[lost-stage-response]
tests/scripts/test_pod_held_budget.py::test_staging_failure_and_exact_reconciliation_measured_allowance[terminal-stage-failure]
tests/scripts/test_pod_jobs.py::test_budget_exhaustion_still_releases_without_allocating_a_record
tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[command]
tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[hash]
tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[json]
tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[png]
tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[runtime]
tests/scripts/test_pod_jobs.py::test_failed_two_job_rehearsal_retains_diagnostic_and_releases[sanity]
tests/scripts/test_pod_jobs.py::test_held_joblist_runs_fresh_mixed_rows_and_keeps_custody[False]
tests/scripts/test_pod_jobs.py::test_held_joblist_runs_fresh_mixed_rows_and_keeps_custody[True]
tests/scripts/test_pod_jobs.py::test_held_joblist_uncertain_row_keeps_in_use_operation_and_snapshot
tests/scripts/test_pod_jobs.py::test_held_reconcile_progress_start_response_loss_keeps_exact_operation
tests/scripts/test_pod_jobs.py::test_held_reconcile_repeated_terminal_failures_exhaust_durable_budget
tests/scripts/test_pod_jobs.py::test_held_reconcile_reservation_persistence_failure_never_dispatches
tests/scripts/test_pod_jobs.py::test_held_reconcile_terminal_proof_needs_separate_turn_before_same_pod_retry
tests/scripts/test_pod_jobs.py::test_held_reconcile_terminal_receipt_persistence_failure_stays_in_use
tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[cancel-error]
tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[cancelled]
tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[interrupt]
tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[lost-start-response]
tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[malformed-terminal]
tests/scripts/test_pod_jobs.py::test_held_reconcile_uncertain_operation_blocks_every_new_start[timeout]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[None]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[evidence]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[identity]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[install]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[result]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[timeout]
tests/scripts/test_pod_jobs.py::test_source_bound_installer_then_h3_held_accounting[uncertain]
tests/scripts/test_pod_jobs.py::test_transient_detached_poll_failure_retains_only_recoverable_followup[followup]
tests/scripts/test_pod_jobs.py::test_transient_followup_diagnostic_or_persistence_error_retains_retry_custody[diagnostic]
tests/scripts/test_pod_jobs.py::test_transient_followup_diagnostic_or_persistence_error_retains_retry_custody[persistence]
tests/scripts/test_pod_jobs.py::test_two_job_cpu_loopback_packets_progress_budget_and_release
tests/scripts/test_pod_session.py::test_actual_legacy_sdk_mount_path_projection_refuses_before_private_upload[/other]
tests/scripts/test_pod_session.py::test_actual_legacy_sdk_mount_path_projection_refuses_before_private_upload[/workspace/../other]
tests/scripts/test_pod_session.py::test_actual_legacy_sdk_mount_path_projection_refuses_before_private_upload[187]
```

</details>

<details><summary>C1a moved am-* elements: element_schema() fails open (refusals lost) (31)</summary>

```
tests/editing_conformance/test_conformance.py::test_conformance[look.set.plate-zoom-fraction-cli]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.plate-zoom-fraction-python]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.plate-zoom-fraction-sheet]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.sprite-scale-range-cli]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.sprite-scale-range-python]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.sprite-scale-range-sheet]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.type-reveal-bad-cli]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.type-reveal-bad-python]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.type-reveal-bad-sheet]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.unknown-key-cli]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.unknown-key-python]
tests/editing_conformance/test_conformance.py::test_conformance[look.set.unknown-key-sheet]
tests/editing_conformance/test_native_sheet_current.py::test_unsupported_cells_refuse_whole_batch_before_queue[text-null]
tests/editing_conformance/test_native_sheet_current.py::test_unsupported_cells_refuse_whole_batch_before_queue[text-{"a":1}]
tests/editing_conformance/test_runner_selftest.py::test_refusal_parity_on_an_unknown_key
tests/packs/timeline/test_cli_add_layer.py::test_add_layer_validates_params_and_rolls_back_a_refused_add
tests/packs/timeline/test_cli_edit_flags.py::test_allow_new_params_lets_set_write_an_undeclared_param
tests/packs/timeline/test_cli_edit_flags.py::test_edit_set_refuses_a_param_the_element_does_not_declare
tests/sdk/test_timeline_checkout.py::test_a_nested_param_takes_a_moment_and_check_rejects_text_in_a_number
tests/sdk/test_timeline_checkout.py::test_check_blocks_a_literal_formula_string_where_the_element_wants_a_frame
tests/sdk/test_timeline_checkout.py::test_python_setters_are_discoverable_and_refuse_what_is_not_a_param
tests/sdk/test_timeline_param_values.py::test_a_number_is_fine_where_an_integer_is_declared_and_a_px_position_is_a_number
tests/sdk/test_timeline_param_values.py::test_all_or_nothing_when_one_key_is_bad
tests/sdk/test_timeline_param_values.py::test_an_undeclared_key_is_left_to_the_key_check
tests/sdk/test_timeline_param_values.py::test_enum_refuses_a_value_outside_the_schema_and_names_the_allowed_ones
tests/sdk/test_timeline_param_values.py::test_integer_range_refuses_above_the_maximum_and_below_the_minimum
tests/sdk/test_timeline_param_values.py::test_the_logical_grid_range_is_checked_on_the_stored_value
tests/sdk/test_timeline_param_values.py::test_the_sheet_refuses_a_bad_range_on_the_rocket
tests/sdk/test_timeline_param_values.py::test_the_sheet_refuses_a_bad_value_and_writes_nothing
tests/sdk/test_timeline_param_values.py::test_tl_add_refuses_an_out_of_enum_value_before_the_clip_exists
tests/sdk/test_timeline_param_values.py::test_type_refuses_a_string_for_a_number_and_a_bool_for_a_number
```

</details>

<details><summary>C9 pack framework port: retired `local` pack (shipped effects unregistered) (28)</summary>

```
tests/packs/rendering/test_pinned_project_elements.py::test_colliding_installed_owner_uses_exact_retained_snapshot[local]
tests/packs/rendering/test_pinned_project_elements.py::test_colliding_installed_owner_uses_exact_retained_snapshot[source]
tests/packs/rendering/test_pinned_project_elements.py::test_non_effect_pins_use_revision_slots_and_assets[animation-entrance]
tests/packs/rendering/test_pinned_project_elements.py::test_non_effect_pins_use_revision_slots_and_assets[transition-transition]
tests/packs/rendering/test_pinned_project_elements.py::test_old_pin_ignores_new_catalog_and_materializes_frozen_inputs
tests/packs/rendering/test_pinned_project_elements.py::test_render_uses_private_registries_under_global_lock
tests/packs/rendering/test_readable_timeline_timing.py::test_absent_actual_compositor_track_keeps_window_but_cannot_claim_mounted_motion
tests/packs/rendering/test_readable_timeline_timing.py::test_accepted_transition_retimes_destination_and_preserves_off_page_identity_once
tests/packs/rendering/test_readable_timeline_timing.py::test_custom_keyframe_shape_does_not_prove_canonical_element_contract
tests/packs/rendering/test_readable_timeline_timing.py::test_effect_component_inherits_parent_opacity_but_does_not_claim_parent_audio_controls
tests/packs/rendering/test_readable_timeline_timing.py::test_fractional_fps_without_existing_mounted_model_is_explicit_unknown
tests/packs/rendering/test_readable_timeline_timing.py::test_left_clipped_transform_restarts_local_clock_without_applying_source_trim
tests/packs/rendering/test_readable_timeline_timing.py::test_missing_complete_context_never_guesses_an_incoming_transition_mount
tests/packs/rendering/test_readable_timeline_timing.py::test_omitted_timing_does_not_drop_clip_or_invent_transform
tests/packs/rendering/test_readable_timeline_timing.py::test_opacity_only_transform_is_a_fade_without_invented_pan_or_zoom
tests/packs/rendering/test_readable_timeline_timing.py::test_property_specific_holds_and_reversals_do_not_collapse_to_equal_endpoints
tests/packs/rendering/test_readable_timeline_timing.py::test_stale_pinned_transform_revision_is_unknown
tests/packs/rendering/test_readable_timeline_timing.py::test_transform_clock_uses_rounded_mount_and_hold_speed_not_source_clock
tests/packs/rendering/test_remotion_backend.py::test_card_staging_overrides_only_exact_local_owner[local]
tests/packs/rendering/test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[transport-frame-overlay]
tests/packs/rendering/test_scene_source_carry.py::test_persistent_renderer_forwards_final_props_callback
tests/packs/rendering/test_scene_source_carry.py::test_sdk_source_reaches_real_final_staging_callback[transport-frame-overlay]
tests/packs/rendering/test_scene_source_carry.py::test_staged_element_asset_map_is_bound_before_query[extra]
tests/packs/rendering/test_scene_source_carry.py::test_staged_element_asset_map_is_bound_before_query[missing]
tests/packs/rendering/test_scene_source_carry.py::test_staged_element_asset_map_is_bound_before_query[outside]
tests/packs/rendering/test_scene_source_carry.py::test_staged_element_asset_substitution_fails_before_query
tests/packs/rendering/test_timeline_visualize_motion.py::test_transform_at_adapter_fails_closed_on_invalid_keyframes
tests/packs/test_pack_discovery_metadata.py::PackDiscoveryMetadataTest::test_source_kinds_include_env_in_priority_order
```

</details>

<details><summary>C4 CI env: ASTRID_TEST_LIFECYCLE_CHECKOUT unset (23)</summary>

```
tests/sdk/test_runpod_front_door.py::test_absent_host_interface_is_a_blocked_sdk_and_cli_envelope[image]
tests/sdk/test_runpod_front_door.py::test_absent_host_interface_is_a_blocked_sdk_and_cli_envelope[video]
tests/sdk/test_runpod_front_door.py::test_cli_no_wait_text_returns_task_without_claiming_completion[image]
tests/sdk/test_runpod_front_door.py::test_cli_no_wait_text_returns_task_without_claiming_completion[video]
tests/sdk/test_runpod_front_door.py::test_cli_paid_flags_match_sdk_and_retain_admission[image]
tests/sdk/test_runpod_front_door.py::test_cli_paid_flags_match_sdk_and_retain_admission[video]
tests/sdk/test_runpod_front_door.py::test_foreign_binding_on_follow_never_reactivates[image]
tests/sdk/test_runpod_front_door.py::test_foreign_binding_on_follow_never_reactivates[video]
tests/sdk/test_runpod_front_door.py::test_h3_no_wait_uses_prepared_child_and_preserves_parent_default
tests/sdk/test_runpod_front_door.py::test_no_wait_retains_exact_custody_when_activation_is_uncertain[image]
tests/sdk/test_runpod_front_door.py::test_no_wait_retains_exact_custody_when_activation_is_uncertain[video]
tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[image-False]
tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[image-True]
tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[video-False]
tests/sdk/test_runpod_front_door.py::test_prepared_image_video_and_raw_admit_once_and_follow_same_binding[video-True]
tests/sdk/test_runpod_front_door.py::test_release_denial_keeps_the_runtime_task_and_blocked_envelope[image]
tests/sdk/test_runpod_front_door.py::test_release_denial_keeps_the_runtime_task_and_blocked_envelope[video]
tests/sdk/test_runpod_front_door.py::test_target_describe_and_release_use_typed_owner_without_claim[image]
tests/sdk/test_runpod_front_door.py::test_target_describe_and_release_use_typed_owner_without_claim[video]
tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[image-False]
tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[image-True]
tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[video-False]
tests/sdk/test_runpod_front_door.py::test_waiting_route_activates_once_and_reconstructs_publication_fake[video-True]
```

</details>

<details><summary>C13 engine/model lock + VibeComfy pin bump (data/dependency) (18)</summary>

```
tests/core/generation/backends/test_qwen_21_turbo.py::test_generate_and_h3_share_vibecomfy_pin
tests/core/generation/test_engine_readiness.py::test_installed_engine_produces_private_profile_consumed_by_existing_validators[comfyui]
tests/core/generation/test_engine_readiness.py::test_installed_engine_produces_private_profile_consumed_by_existing_validators[vibecomfy-h3-a04]
tests/core/generation/test_engine_readiness.py::test_installed_engine_produces_private_profile_consumed_by_existing_validators[vibecomfy-h3]
tests/core/generation/test_listing.py::test_qualified_fake_model_remains_available
tests/core/generation/test_output_delivery.py::test_corruption_fails_cli_without_replacing_requested_file[image]
tests/core/generation/test_output_delivery.py::test_corruption_fails_cli_without_replacing_requested_file[manifest]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[default-auto]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[default-http://127.0.0.1:8188]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[default-managed]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[directory-auto]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[directory-http://127.0.0.1:8188]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[directory-managed]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[file-auto]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[file-http://127.0.0.1:8188]
tests/core/generation/test_output_delivery.py::test_exact_cli_delivers_verified_caller_local_image[file-managed]
tests/core/generation/test_output_delivery.py::test_no_wait_returns_admission_without_local_delivery
tests/packs/h3_av/test_generation.py::test_generation_assets_use_recipe_lock_revisions
```

</details>

<details><summary>C8 installer: staged root needs runtime.lock.json (G16) vs R10-era fixtures (10)</summary>

```
tests/test_installer_bootstrap_schema.py::test_staged_canonical_schema_reaches_strict_consumer
tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-17391-17393-17393]
tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-17391-None-17391]
tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[None-None-None-17340]
tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[pinokio-17391-17393-17393]
tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[pinokio-17391-None-17391]
tests/test_installer_platforms.py::test_stage_profile_points_to_candidate_service_declaration[pinokio-None-None-17340]
tests/test_installer_schema.py::test_optional_remotion_failure_does_not_block_staging[browser]
tests/test_installer_schema.py::test_optional_remotion_failure_does_not_block_staging[npm]
tests/test_installer_schema.py::test_staging_verifies_the_local_schema_before_declaring_services
```

</details>

<details><summary>C14 Plan 33 generation surface: new align/target_policy args vs pinned arg sets (7)</summary>

```
tests/core/generation/test_entry_cli_contract.py::test_json_and_convenience_values_use_shared_resolver
tests/core/generation/test_readiness_inputs_f04.py::test_dry_run_is_the_readiness_envelope_without_source_or_config_writes
tests/packs/test_vibecomfy_ir_bridge.py::test_ir_executors_are_manifested_without_growing_the_gateway
tests/sdk/test_runpod_front_door.py::test_invalid_entry_values_and_raw_source_block_before_claim[image]
tests/sdk/test_runpod_front_door.py::test_invalid_entry_values_and_raw_source_block_before_claim[video]
tests/test_mcp_generation_parity.py::test_generate_schema_and_argv_for_all_leaves
tests/test_mcp_server.py::test_invoke_returns_admission_and_task_refs
```

</details>

<details><summary>C6 engine model lock grew: pod disk-size expectations stale (6)</summary>

```
tests/scripts/test_pod_jobs.py::test_cold_claim_keeps_recipe_storage_reserve
tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[exact-20gb]
tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[installed-pod-headroom]
tests/scripts/test_pod_jobs.py::test_held_installed_followup_uses_warm_scratch[insufficient-20gb]
tests/scripts/test_pod_session.py::test_claim_arguments_and_gpu_fallback
tests/scripts/test_pod_session.py::test_container_disk_is_sized_from_the_recipe
```

</details>

<details><summary>C12 PK06 port dropped comfy_wrap -> vibecomfy mapping (5)</summary>

```
tests/core/generation/test_gpu_environment.py::test_unqualified_label_is_a_warning_and_the_retired_opt_in_changes_nothing[-comfy_wrap.run]
tests/core/generation/test_gpu_environment.py::test_unqualified_label_is_a_warning_and_the_retired_opt_in_changes_nothing[0-comfy_wrap.run]
tests/core/generation/test_gpu_environment.py::test_unqualified_label_is_a_warning_and_the_retired_opt_in_changes_nothing[1-comfy_wrap.run]
tests/core/generation/test_gpu_environment.py::test_unqualified_label_is_a_warning_and_the_retired_opt_in_changes_nothing[true-comfy_wrap.run]
tests/core/generation/test_gpu_environment.py::test_vibecomfy_readiness_does_not_require_detected_nvidia[comfy_wrap.run]
```

</details>

<details><summary>C7 pod H3 install: canonical engine install path changed (5)</summary>

```
tests/scripts/test_pod_h3_install.py::test_fresh_canonical_install_refuses_nonprivate_volume_before_any_process
tests/scripts/test_pod_h3_install.py::test_install_integrity_failure_reports_canonical_phase_without_exception_details
tests/scripts/test_pod_h3_install.py::test_install_selected_rechecks_source_identity_after_install
tests/scripts/test_pod_h3_install.py::test_install_selected_recovers_legacy_receipt_and_returns_ready_attestation
tests/scripts/test_pod_h3_install.py::test_install_selected_rejects_readiness_mismatch
```

</details>

<details><summary>C11 generic host: delegated child needs admitted source digest (4)</summary>

```
tests/core/execution/test_generic_host_child_bridge_d18.py::test_iteration_video_host_wiring_retains_exact_media_and_normal_submission
tests/core/execution/test_generic_host_child_bridge_d18.py::test_iteration_video_logical_key_preserved_at_wire_boundary
tests/core/execution/test_generic_host_child_bridge_d18.py::test_prepared_submission_uses_current_attempt_receipts_and_private_provenance
tests/test_generic_host_result_json.py::test_request_digest_does_not_depend_on_attempt_or_materialized_paths
```

</details>

<details><summary>C15 committed generated artifacts stale (capability index, artifact manifest, doc catalog) (3)</summary>

```
tests/core/generation/test_generation_index.py::test_committed_capability_index_is_generated_from_registry
tests/reshape/test_check_doc_references.py::test_committed_catalog_is_fresh_for_the_in_repo_packs
tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current
```

</details>

<details><summary>No baseline: ran only in Release 10 shard 8 (63)</summary>

```
tests/test_sdk_public_surface.py::test_generate_attached_project_resolution_video
tests/test_sdk_public_surface.py::test_generate_explicit_out_routing_video
tests/test_sdk_public_surface.py::test_generate_explicit_project_routing_video
tests/test_sdk_public_surface.py::test_generate_facade_handles_error_generation_result
tests/test_sdk_public_surface.py::test_generate_facade_maps_contract_failures_and_openai_rejection
tests/test_sdk_public_surface.py::test_generate_facade_maps_contract_failures_and_openai_route
tests/test_sdk_public_surface.py::test_generate_facade_rejects_non_mapping_payload
tests/test_sdk_public_surface.py::test_generate_out_wins_over_project_video
tests/test_sdk_public_surface.py::test_generate_video_no_stderr_output
tests/test_sdk_public_surface.py::test_generate_video_reconstructs_typed_result_from_generation_payload
tests/test_sdk_public_surface.py::test_video_explicit_execution_validated_against_backends
tests/test_sdk_public_surface.py::test_video_explicit_mode_validated
tests/test_sdk_public_surface.py::test_video_mode_inference_flf_both_refs
tests/test_sdk_public_surface.py::test_video_mode_inference_t2v_no_refs
tests/test_skills_cli.py::test_external_dir_off_dry_run_is_read_only_through_cli[install]
tests/test_skills_cli.py::test_external_dir_off_dry_run_is_read_only_through_cli[sync]
tests/test_skills_developer.py::test_default_sync_installs_developing_astrid_but_not_the_developer_skills
tests/test_skills_developer.py::test_developer_pack_declares_developing_astrid_and_developer_only_extras
tests/test_skills_developer.py::test_developer_sync_installs_resolves_survives_resync_and_uninstalls
tests/test_skills_package_data.py::test_default_composition_preserves_opt_outs_without_acquisition
tests/test_skills_package_data.py::test_retained_integrations_flow_through_existing_sync_selection
tests/test_skills_sync_registry.py::CheckTest::test_check_detects_stale_link
tests/test_skills_sync_registry.py::RegistryBlockTest::test_deep_block_includes_skill_names
tests/test_skills_sync_registry.py::SyncGatewayTest::test_deep_links_per_pack_and_prunes_stale
tests/test_skills_sync_registry.py::SyncGatewayTest::test_deep_sync_prunes_disabled_managed_pack_but_keeps_foreign_entry
tests/test_skills_sync_registry.py::SyncGatewayTest::test_gateway_only_links_core_and_writes_registry
tests/test_skills_sync_registry.py::SyncGatewayTest::test_normal_sync_uses_writable_composed_view
tests/test_skip_policy.py::test_no_test_file_skips_by_hand
tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale
tests/test_structure_contracts.py::test_real_repo_top_level_matches_structure_constants
tests/test_third_party_integration.py::test_env_backend_pack_registers_descriptor_and_dispatches_generate_image
tests/test_third_party_integration.py::test_env_discovery_populates_sdk_discovery_dto
tests/test_third_party_integration.py::test_env_element_pack_validates_loads_lists_and_reaches_sdk
tests/test_timeline_editing_helpers.py::test_canonical_source_trim_speed_move_and_retime_intervals
tests/test_timeline_editing_helpers.py::test_ripple_is_track_scoped_and_never_moves_audio
tests/test_timeline_editing_helpers.py::test_ripple_shifts_canonical_intervals_without_touching_audio
tests/test_vendor_lock.py::test_one_root_lock_covers_all_known_runtime_paths
tests/test_vibecomfy_pin.py::test_no_other_tracked_file_copies_the_pin
tests/test_windows_gpu_availability.py::test_execution_runs_and_labels_settlement_without_opt_in[False]
tests/test_windows_gpu_availability.py::test_execution_runs_and_labels_settlement_without_opt_in[True]
tests/test_windows_gpu_availability.py::test_failed_opt_in_run_retains_unqualified_label
tests/test_windows_gpu_availability.py::test_unqualified_label_survives_other_readiness_failures
tests/test_windows_gpu_availability.py::test_vibecomfy_remains_ready_when_nvidia_detection_is_lost
tests/timeline/test_authoring_bundle.py::test_approval_is_bound_to_candidate_and_base_revision
tests/timeline/test_authoring_feedback.py::test_document_emitter_provider_refuses_invalid_param_and_unverified_media[param]
tests/timeline/test_authoring_feedback.py::test_document_emitter_provider_refuses_invalid_param_and_unverified_media[unknown]
tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generated_fingerprint_changes_with_element_content
tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_is_idempotent_for_package_outputs
tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_outputs_package_owned_registries
tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_requires_writable_package_outputs
tests/timeline/test_html_canvas_effect.py::HtmlCanvasEffectExecutorTest::test_scaffold_writes_local_effect_and_report
tests/timeline/test_shot_composition_projection.py::test_shot_only_layer_merge_matches_chapter_render_order_and_keeps_properties
tests/timeline/test_shot_layering_projection.py::test_fixture_matches_canonical_runtime_bytes
tests/timeline/test_timeline_elements_catalog.py::TimelineElementsCatalogTest::test_catalog_exposes_pack_declared_custom_kinds
tests/v10/test_authority_lint.py::test_live_repository_tree_passes_authority_lint
tests/v10/test_docs_cli_alignment.py::test_core_docs_have_no_retired_invocation_strings
tests/v10/test_docs_cli_alignment.py::test_documented_commands_are_real_gateway_commands
tests/v10/test_docs_cli_alignment.py::test_pack_stages_do_not_reference_retired_verbs
tests/v10/test_domain_cli_projects_timelines.py::test_first_run_timeline_journey_uses_selection_recent_history_and_project_list
tests/v10/test_domain_cli_projects_timelines.py::test_timelines_show_human_output_reads_transform_keyframes
tests/v10/test_pack_write_path_lint.py::test_schema_pack_code_never_calls_event_append_entrypoints
tests/v10/test_pack_write_path_lint.py::test_schema_pack_code_never_takes_the_store_module_handle
tests/v10/test_release_reproducibility.py::test_runtime_lock_covers_runpod_source_dependencies_without_source_distributions
```

</details>

<details><summary>No baseline: new tests at the candidate (99)</summary>

```
tests/core/generation/test_entry_cli_contract.py::test_public_sfx_route_receives_declared_inputs[verb0]
tests/core/generation/test_moved_data_composition.py::test_explicit_renderer_inventory_never_reads_ambient_or_unselected_bytes[True]
tests/core/pack/test_build_hook_contract.py::test_checker_inputs_are_the_staged_source_of_each_selected_root
tests/core/pack/test_build_hook_contract.py::test_hook_runs_once_per_pack_in_an_isolated_stage_and_writes_admission_records
tests/core/pack/test_build_hook_contract.py::test_two_builds_of_the_same_source_are_byte_identical
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_add_refusals_preserve_admitted_baseline[bad_source]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_add_refusals_preserve_admitted_baseline[dependency]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_add_refusals_preserve_admitted_baseline[missing_python]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_add_refusals_preserve_admitted_baseline[release_pin]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_refusals_preserve_generation_and_admission_bytes[bad_source-invalid_manifest]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_refusals_preserve_generation_and_admission_bytes[dependency-missing_dep]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_refusals_preserve_generation_and_admission_bytes[pin-pin_mismatch]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_refusals_preserve_generation_and_admission_bytes[python-missing_python]
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_remove_refuses_dependency_break_and_preserves_admitted_baseline
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_rollback_refuses_release_pin_and_preserves_admitted_baseline
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_update_refuses_dependency_digest_only_pin_mismatch
tests/core/pack/test_r8_prod_refusals.py::test_real_cli_update_refuses_missing_python_and_preserves_live_generation
tests/core/pack/test_transaction.py::test_browser_install_update_rollback_and_replay_publish_complete_records
tests/core/pack/test_transaction.py::test_browser_process_death_preserves_complete_records_and_refresh_retry[before_refresh]
tests/core/pack/test_transaction.py::test_browser_process_death_preserves_complete_records_and_refresh_retry[before_swap]
tests/core/pack/test_transaction.py::test_browser_process_death_preserves_complete_records_and_refresh_retry[prepared]
tests/core/pack/test_transaction.py::test_browser_process_death_preserves_complete_records_and_refresh_retry[swapped]
tests/core/pack/test_transaction.py::test_browser_refresh_refusal_retries_same_records_without_rebuild
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-chunk]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-entry]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-extra]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-manifest]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-pin]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-record]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[before_swap-source]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-chunk]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-entry]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-extra]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-manifest]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-pin]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-record]
tests/core/pack/test_transaction.py::test_browser_tamper_refuses_publication_and_keeps_complete_old_tree[built-source]
tests/core/pack/test_transaction.py::test_real_browser_build_refusal_preserves_prior_admitted_tree[compile]
tests/core/pack/test_transaction.py::test_real_browser_build_refusal_preserves_prior_admitted_tree[tool_hash]
tests/core/pack/test_transaction.py::test_real_browser_build_refusal_preserves_prior_admitted_tree[unsafe_import]
tests/core/pack/test_transaction.py::test_retained_browser_records_keep_their_admission_revision_and_replacement_clears_them
tests/core/pack/test_transaction.py::test_rollback_interruption_refuses_without_live_change_and_can_retry
tests/core/pack/test_transaction.py::test_rollback_refuses_corrupt_retired_browser_admission_without_changing_live_generation[chunk]
tests/core/pack/test_transaction.py::test_rollback_refuses_corrupt_retired_browser_admission_without_changing_live_generation[entry]
tests/core/pack/test_transaction.py::test_rollback_refuses_corrupt_retired_browser_admission_without_changing_live_generation[manifest]
tests/core/pack/test_transaction.py::test_rollback_refuses_corrupt_retired_browser_admission_without_changing_live_generation[missing]
tests/core/pack/test_transaction.py::test_rollback_refuses_corrupt_retired_browser_admission_without_changing_live_generation[record]
tests/core/pack/test_transaction.py::test_rollback_restores_build_hook_metadata_with_the_pack_generation
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[chunk-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[chunk-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[committedRevision-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[committedRevision-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[future_revision-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[future_revision-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[identity-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[identity-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[manifest-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[manifest-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[missing-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[missing-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[record-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[record-installed]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[transactionId-candidate]
tests/core/pack/test_transaction.py::test_unrelated_update_refuses_corrupt_retained_browser_admission[transactionId-installed]
tests/integrations/test_runpod_h3_host_r5.py::test_h3_freezes_policy_into_default_local_stages
tests/packs/rendering/test_core_render_graph.py::test_core_only_real_timeline_renders_through_action
tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path
tests/sdk/test_h3_endpoint_r4.py::test_parent_rechecks_input_bytes_after_paid_handoff
tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[attestation]
tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[origin]
tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[owner]
tests/sdk/test_h3_endpoint_r4.py::test_prepared_endpoint_cannot_replace_readiness_target[warm-lease]
tests/sdk/test_h3_endpoint_r4.py::test_recovery_reuses_retained_endpoint_and_refuses_substitution
tests/sdk/test_h3_endpoint_r4.py::test_sdk_preflight_and_parent_freeze_one_endpoint_with_all_local_stages
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[approval-type]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[changed-endpoint]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[cold]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[controls]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[missing-node]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[multipass]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[placeholder]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[t9-empty]
tests/sdk/test_h3_endpoint_r4.py::test_sdk_unsupported_cases_never_prepare_or_admit[t9]
tests/sdk/test_h3_endpoint_r4.py::test_staged_parent_hands_exact_graph_to_local_run[changed-bindings]
tests/sdk/test_h3_endpoint_r4.py::test_staged_parent_hands_exact_graph_to_local_run[exact]
tests/stage1/test_pack_api_surface.py::test_frozen_surface_and_version_history
tests/test_generic_host.py::test_host_without_explicit_roots_discovers_the_personal_collection
tests/test_installed_generation_journey.py::test_generation_package_probe[False]
tests/test_installed_generation_journey.py::test_generation_package_probe[True]
tests/test_installed_generation_journey.py::test_runpod_package_fake_owner
tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[False-never-up]
tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[False-rollback-busy]
tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[True-never-up]
tests/test_installer_sources.py::test_forced_update_restages_damaged_agent_and_tools_from_fresh_candidate[True-rollback-busy]
tests/test_skills_installed_composition.py::test_installed_core_help_profile_and_selected_empty_sync
tests/test_skills_package_data.py::test_default_skill_policy_comes_from_pack_manifests
tests/test_skills_selected_composition.py::test_capability_index_check_is_non_mutating
tests/test_skills_selected_composition.py::test_selected_declarations_drive_views_and_mcp
tests/test_skills_selected_composition.py::test_tool_catalog_selection_preserves_declared_bindings
```

</details>

