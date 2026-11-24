# Wave C cards

419 failing IDs that no Wave A or B card owns, in 230 test files. One card per row: the IDs in that file, fixed by cause under the [triage rules](../../tasks.md#triage-rules). A file with more than one cause splits into one card per cause. The manager gives a worker several rows from one area at a time, up to about ten IDs.

| Card | IDs | Test file | Clusters |
| --- | ---: | --- | --- |
| AG-C1 | 19 | `tests/packs/test_pack_run_cli_choices.py` | ci:C7 |
| AG-C2 | 14 | `tests/packs/test_pack_migration_m4_shells.py` | ci:C7 |
| AG-C3 | 6 | `tests/packs/builtin/test_training_run_support.py` | ci:C285, ci:C286, ci:C287, ci:C288, ci:C289, ci:C290 |
| AG-C4 | 4 | `tests/packs/builtin/training_run/test_runtime_state_resume.py` | ci:C291, ci:C292, ci:C293, ci:C294 |
| AG-C5 | 4 | `tests/packs/rendering/test_timeline_route_integration.py` | ci:C303, ci:C304, ci:C305, ci:C306 |
| AG-C6 | 3 | `tests/packs/rendering/test_timeline_storyboard.py` | ci:C307, ci:C308, ci:C309 |
| AG-C7 | 3 | `tests/packs/h3_av/test_static_mask_preflight.py` | lanes:C34 |
| AG-C8 | 3 | `tests/packs/rendering/test_hyperframes_backend.py` | lanes:C35 |
| AG-C9 | 3 | `tests/packs/runpod/test_https_transport.py` | lanes:C36 |
| AG-C10 | 2 | `tests/packs/h3_av/test_edit_inputs.py` | ci:C76 |
| AG-C11 | 2 | `tests/packs/rendering/test_ffmpeg_support.py` | ci:C77 |
| AG-C12 | 2 | `tests/packs/builtin/test_training_run_seinfeld_parity.py` | ci:C283, ci:C284 |
| AG-C13 | 2 | `tests/packs/h3_av/test_compile_generalized.py` | ci:C296, ci:C297 |
| AG-C14 | 2 | `tests/packs/rendering/test_timeline_transfer_actions.py` | ci:C310, lanes:C100 |
| AG-C15 | 2 | `tests/packs/runpod/test_ratchet_invariants.py` | ci:C313, ci:C314 |
| AG-C16 | 2 | `tests/packs/timeline/test_cli_parity.py` | ci:C346, ci:C347 |
| AG-C17 | 2 | `tests/packs/timeline/test_show_clip_working_copy.py` | ci:C350, ci:C351 |
| AG-C18 | 2 | `tests/packs/h3_av/test_character_swap_cpu_boundary.py` | lanes:C95, lanes:C96 |
| AG-C19 | 1 | `tests/packs/builtin/generate_image/test_codex_backend.py` | ci:C281 |
| AG-C20 | 1 | `tests/packs/builtin/test_training_run_ai_toolkit_support.py` | ci:C282 |
| AG-C21 | 1 | `tests/packs/builtin/training_run/test_seinfeld_parity.py` | ci:C295 |
| AG-C22 | 1 | `tests/packs/h3_av/test_generation.py` | ci:C298 |
| AG-C23 | 1 | `tests/packs/h3_av/test_workflow_model_urls.py` | ci:C299 |
| AG-C24 | 1 | `tests/packs/rendering/test_normal_audio_http.py` | ci:C300 |
| AG-C25 | 1 | `tests/packs/rendering/test_remotion_backend.py` | ci:C301 |
| AG-C26 | 1 | `tests/packs/rendering/test_render_remotion_registry.py` | ci:C302 |
| AG-C27 | 1 | `tests/packs/rendering/test_timeline_visualize_motion.py` | ci:C311 |
| AG-C28 | 1 | `tests/packs/runpod/test_models_lock_paths.py` | ci:C312 |
| AG-C29 | 1 | `tests/packs/runpod/test_review_rest_v2.py` | ci:C315 |
| AG-C30 | 1 | `tests/packs/test_b2_integrated_closure.py` | ci:C316 |
| AG-C31 | 1 | `tests/packs/test_executor_admission.py` | ci:C317 |
| AG-C32 | 1 | `tests/packs/test_generation_verb_extensions.py` | ci:C318 |
| AG-C33 | 1 | `tests/packs/test_public_id_resolution.py` | ci:C342 |
| AG-C34 | 1 | `tests/packs/test_vibecomfy_ir_bridge.py` | ci:C343 |
| AG-C35 | 1 | `tests/packs/timeline/test_cli_clash_back.py` | ci:C344 |
| AG-C36 | 1 | `tests/packs/timeline/test_cli_find.py` | ci:C345 |
| AG-C37 | 1 | `tests/packs/timeline/test_cli_v3_sweep_log.py` | ci:C348 |
| AG-C38 | 1 | `tests/packs/timeline/test_parent_clips.py` | ci:C349 |
| AG-C39 | 1 | `tests/packs/timeline/test_verbs_working_copy.py` | ci:C352 |
| AG-C40 | 1 | `tests/packs/timeline/test_visualize_drafts.py` | ci:C353 |
| AG-C41 | 1 | `tests/packs/vibecomfy/test_local_launch_facts.py` | ci:C354 |
| AG-C42 | 1 | `tests/packs/vibecomfy/test_local_server_media.py` | ci:C355 |
| AG-C43 | 1 | `tests/packs/h3_av/test_two_edit_cpu_qualification.py` | lanes:C97 |
| AG-C44 | 1 | `tests/packs/rendering/test_shot_layering_export.py` | lanes:C99 |
| AG-C45 | 1 | `tests/packs/test_renderer_parity.py` | lanes:C102 |
| AG-C46 | 11 | `tests/core/rendering/test_remotion_runtime.py` | ci:C75, ci:C262, ci:C263, ci:C264, ci:C265, ci:C266, ci:C267, ci:C268, ci:C269, ci:C270 |
| AG-C47 | 10 | `tests/core/rendering/test_registry.py` | ci:C247, ci:C248, ci:C249, ci:C250, ci:C251, ci:C252, ci:C253, ci:C254, ci:C255, ci:C256 |
| AG-C48 | 5 | `tests/core/generation/backends/test_qwen_21_turbo.py` | ci:C51, ci:C99, ci:C100, ci:C101 |
| AG-C49 | 5 | `tests/core/rendering/test_registry_matrix.py` | ci:C257, ci:C258, ci:C259, ci:C260, ci:C261 |
| AG-C50 | 3 | `tests/core/generation/test_param_map_migration_parity.py` | ci:C53, ci:C119 |
| AG-C51 | 3 | `tests/core/generation/test_runpod_engine_selection.py` | ci:C73, ci:C240 |
| AG-C52 | 3 | `tests/core/generation/test_public_route_guard.py` | ci:C234, ci:C235, ci:C236 |
| AG-C53 | 3 | `tests/core/test_elements_cli.py` | ci:C272, ci:C273, ci:C274 |
| AG-C54 | 2 | `tests/core/generation/test_engine_fresh_install.py` | ci:C52 |
| AG-C55 | 2 | `tests/core/execution/test_host_cleanup_ack_barrier.py` | ci:C91, ci:C96 |
| AG-C56 | 2 | `tests/core/generation/test_cli_gold_075b.py` | ci:C102, ci:C103 |
| AG-C57 | 2 | `tests/core/generation/test_generation_index.py` | ci:C113, ci:C114 |
| AG-C58 | 2 | `tests/core/generation/test_readiness_inputs_f04.py` | ci:C237, ci:C238 |
| AG-C59 | 1 | `tests/core/execution/test_bug14_settlement_liveness.py` | ci:C92 |
| AG-C60 | 1 | `tests/core/execution/test_fail_closed_g28.py` | ci:C93 |
| AG-C61 | 1 | `tests/core/execution/test_generic_host_actions_v3.py` | ci:C94 |
| AG-C62 | 1 | `tests/core/execution/test_generic_host_verified_preparation_gr03.py` | ci:C95 |
| AG-C63 | 1 | `tests/core/execution/test_platform_boundary.py` | ci:C97 |
| AG-C64 | 1 | `tests/core/execution/test_private_network_command.py` | ci:C98 |
| AG-C65 | 1 | `tests/core/generation/test_edit_image_ref_admission.py` | ci:C111 |
| AG-C66 | 1 | `tests/core/generation/test_engine_error_reasons.py` | ci:C112 |
| AG-C67 | 1 | `tests/core/generation/test_generation_setup_walk.py` | ci:C115 |
| AG-C68 | 1 | `tests/core/generation/test_h3_build_after_outputs.py` | ci:C116 |
| AG-C69 | 1 | `tests/core/generation/test_listing.py` | ci:C117 |
| AG-C70 | 1 | `tests/core/generation/test_moved_data_composition.py` | ci:C118 |
| AG-C71 | 1 | `tests/core/generation/test_release_python.py` | ci:C233 |
| AG-C72 | 1 | `tests/core/generation/test_run_local.py` | ci:C239 |
| AG-C73 | 1 | `tests/core/generation/test_trusted_inventory.py` | ci:C241 |
| AG-C74 | 1 | `tests/core/generation/test_warm_models_remain_loaded.py` | ci:C242 |
| AG-C75 | 1 | `tests/core/model_catalog/test_registry.py` | ci:C243 |
| AG-C76 | 1 | `tests/core/pack/test_v3_core_worker_luna.py` | ci:C244 |
| AG-C77 | 1 | `tests/core/rendering/test_installed_registry_security.py` | ci:C245 |
| AG-C78 | 1 | `tests/core/rendering/test_production_callers.py` | ci:C246 |
| AG-C79 | 1 | `tests/core/test_element_kind_registry.py` | ci:C271 |
| AG-C80 | 1 | `tests/core/test_executor_registry_snapshot.py` | ci:C275 |
| AG-C81 | 1 | `tests/core/test_generation_backend_registry.py` | ci:C276 |
| AG-C82 | 1 | `tests/core/test_generation_taxonomy_registry.py` | ci:C277 |
| AG-C83 | 1 | `tests/core/test_pack_coherence_elements.py` | ci:C278 |
| AG-C84 | 1 | `tests/core/timeline/test_clip_fields.py` | ci:C279 |
| AG-C85 | 4 | `tests/sdk/test_timeline_current_union_schema.py` | ci:C122, ci:C123, ci:C124, ci:C125 |
| AG-C86 | 4 | `tests/sdk/test_timeline_checkout.py` | ci:C417, ci:C418, lanes:C39 |
| AG-C87 | 4 | `tests/sdk/test_timeline_selected_schema_runtime.py` | lanes:C41, lanes:C58, lanes:C59 |
| AG-C88 | 3 | `tests/sdk/test_runtime_response_conformance.py` | ci:C89, ci:C413 |
| AG-C89 | 2 | `tests/sdk/test_timeline_commit_provider.py` | ci:C120, ci:C121 |
| AG-C90 | 2 | `tests/sdk/test_wc6_completion_capture.py` | ci:C135, ci:C136 |
| AG-C91 | 2 | `tests/sdk/test_generation_target.py` | ci:C403, ci:C404 |
| AG-C92 | 2 | `tests/sdk/test_generation_verified_preparation_gr03.py` | ci:C405, ci:C406 |
| AG-C93 | 2 | `tests/sdk/test_timeline_commit_provider_runtime.py` | lanes:C40 |
| AG-C94 | 1 | `tests/sdk/test_timeline_film_length.py` | ci:C126 |
| AG-C95 | 1 | `tests/sdk/test_timeline_public_command.py` | ci:C131 |
| AG-C96 | 1 | `tests/sdk/test_timeline_render_publication.py` | ci:C132 |
| AG-C97 | 1 | `tests/sdk/test_timeline_selected_param_authority.py` | ci:C133 |
| AG-C98 | 1 | `tests/sdk/test_timeline_sheet_native.py` | ci:C134 |
| AG-C99 | 1 | `tests/sdk/test_d124_shared_custody.py` | ci:C401 |
| AG-C100 | 1 | `tests/sdk/test_generation_source_retention.py` | ci:C402 |
| AG-C101 | 1 | `tests/sdk/test_host_recovery.py` | ci:C407 |
| AG-C102 | 1 | `tests/sdk/test_openai_image_admission.py` | ci:C408 |
| AG-C103 | 1 | `tests/sdk/test_p1_case_corpus.py` | ci:C409 |
| AG-C104 | 1 | `tests/sdk/test_p1_doc_patch_requests.py` | ci:C410 |
| AG-C105 | 1 | `tests/sdk/test_p4_note_rerun.py` | ci:C411 |
| AG-C106 | 1 | `tests/sdk/test_projectless_admission.py` | ci:C412 |
| AG-C107 | 1 | `tests/sdk/test_scene_real_public_summary_rle.py` | ci:C414 |
| AG-C108 | 1 | `tests/sdk/test_selected_param_neutral_stage.py` | ci:C415 |
| AG-C109 | 1 | `tests/sdk/test_timeline_checkout_history.py` | ci:C419 |
| AG-C110 | 1 | `tests/sdk/test_timeline_export.py` | lanes:C56 |
| AG-C111 | 1 | `tests/sdk/test_timeline_import.py` | lanes:C57 |
| AG-C112 | 7 | `tests/integrations/test_runpod_slot_path_cpu.py` | lanes:C15, lanes:C91, lanes:C92 |
| AG-C113 | 4 | `tests/integrations/test_dry_run_equals_live_run.py` | lanes:C15, lanes:C46 |
| AG-C114 | 4 | `tests/integrations/test_media_only_render_without_remotion.py` | lanes:C28 |
| AG-C115 | 3 | `tests/integrations/test_generic_host_activation_acceptance.py` | lanes:C81, lanes:C82, lanes:C83 |
| AG-C116 | 2 | `tests/integrations/test_generic_host_remotion_render.py` | lanes:C72, lanes:C84 |
| AG-C117 | 2 | `tests/integrations/test_runpod_dry_live_seam.py` | lanes:C89, lanes:C90 |
| AG-C118 | 1 | `tests/integrations/test_pinned_element_render_proof.py` | lanes:C45 |
| AG-C119 | 1 | `tests/integrations/test_runpod_host_endpoint_r5.py` | lanes:C45 |
| AG-C120 | 1 | `tests/integrations/test_core_hivemind_installed.py` | lanes:C77 |
| AG-C121 | 1 | `tests/integrations/test_e2_publication_contract_roundtrip.py` | lanes:C78 |
| AG-C122 | 1 | `tests/integrations/test_pinned_source_cpu.py` | lanes:C87 |
| AG-C123 | 1 | `tests/integrations/test_pod_owned_preparation.py` | lanes:C88 |
| AG-C124 | 3 | `tests/editing_conformance/test_commit_runtime_identity.py` | lanes:C29 |
| AG-C125 | 3 | `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py` | lanes:C30 |
| AG-C126 | 2 | `tests/editing_conformance/test_native_word_anchor_vectors.py` | ci:C67 |
| AG-C127 | 2 | `tests/editing_conformance/test_commit_runtime_first_clip.py` | lanes:C37 |
| AG-C128 | 2 | `tests/editing_conformance/test_commit_runtime_occurrence_create.py` | lanes:C38 |
| AG-C129 | 1 | `tests/editing_conformance/test_fork_abi1_binding_set.py` | ci:C186 |
| AG-C130 | 1 | `tests/editing_conformance/test_producer_insertion.py` | ci:C187 |
| AG-C131 | 1 | `tests/editing_conformance/test_recipe_m2_clip_trim.py` | ci:C188 |
| AG-C132 | 1 | `tests/editing_conformance/test_compile_contracts.py` | ci:C280 |
| AG-C133 | 1 | `tests/editing_conformance/test_commit_runtime_native_frontends.py` | lanes:C48 |
| AG-C134 | 1 | `tests/editing_conformance/test_native_word_anchor.py` | lanes:C49 |
| AG-C135 | 1 | `tests/editing_conformance/test_commit_runtime_numeric_params.py` | lanes:C54 |
| AG-C136 | 1 | `tests/editing_conformance/test_commit_runtime_source_copy.py` | lanes:C55 |
| AG-C137 | 1 | `tests/editing_conformance/test_occurrence_shared_d20.py` | lanes:C73 |
| AG-C138 | 1 | `tests/editing_conformance/test_occurrence_shared_historical.py` | lanes:C74 |
| AG-C139 | 1 | `tests/editing_conformance/test_prepared_video_birth.py` | lanes:C75 |
| AG-C140 | 6 | `tests/scripts/test_claim_runpod_5090_backup.py` | ci:C85, ci:C361, ci:C362, ci:C363, ci:C364 |
| AG-C141 | 3 | `tests/scripts/test_gpu_sanity.py` | ci:C366, ci:C367, ci:C368 |
| AG-C142 | 1 | `tests/scripts/test_cuda_default_sites.py` | ci:C365 |
| AG-C143 | 1 | `tests/scripts/test_pod_action_source.py` | ci:C369 |
| AG-C144 | 1 | `tests/scripts/test_pod_h3_install.py` | ci:C382 |
| AG-C145 | 3 | `tests/stage1/test_zero_shim_execution_pack_deletion.py` | ci:C141, ci:C142, ci:C143 |
| AG-C146 | 2 | `tests/stage1/test_capability_parity_gate_luna.py` | ci:C137, lanes:C60 |
| AG-C147 | 1 | `tests/stage1/test_generic_host_process_bootstrap_luna.py` | ci:C138 |
| AG-C148 | 1 | `tests/stage1/test_pack_api_surface.py` | ci:C139 |
| AG-C149 | 1 | `tests/stage1/test_vendored_workspace_client_parity_luna.py` | ci:C140 |
| AG-C150 | 1 | `tests/stage1/test_media_handoff_render_boundary.py` | lanes:C61 |
| AG-C151 | 1 | `tests/stage1/test_runtime_client_cutover.py` | lanes:C62 |
| AG-C152 | 3 | `tests/v10/test_docs_cli_alignment.py` | ci:C228, ci:C229, ci:C230 |
| AG-C153 | 2 | `tests/v10/test_pack_write_path_lint.py` | ci:C72 |
| AG-C154 | 1 | `tests/v10/test_authority_lint.py` | ci:C227 |
| AG-C155 | 1 | `tests/v10/test_domain_cli_projects_timelines.py` | ci:C231 |
| AG-C156 | 1 | `tests/v10/test_release_reproducibility.py` | ci:C232 |
| AG-C157 | 1 | `tests/v10/test_timelines_create.py` | lanes:C71 |
| AG-C158 | 1 | `tests/timeline/test_authoring_bundle.py` | ci:C221 |
| AG-C159 | 1 | `tests/timeline/test_effects_catalog.py` | ci:C222 |
| AG-C160 | 1 | `tests/timeline/test_html_canvas_effect.py` | ci:C223 |
| AG-C161 | 1 | `tests/timeline/test_shot_composition_projection.py` | ci:C224 |
| AG-C162 | 1 | `tests/timeline/test_shot_layering_projection.py` | ci:C225 |
| AG-C163 | 1 | `tests/timeline/test_timeline_elements_catalog.py` | ci:C226 |
| AG-C164 | 1 | `tests/timeline/test_authoring_media.py` | lanes:C69 |
| AG-C165 | 5 | `tests/test_generic_host.py` | ci:C39, ci:C164, ci:C165 |
| AG-C166 | 2 | `tests/reshape/test_compare_baselines.py` | ci:C357, ci:C358 |
| AG-C167 | 1 | `tests/reshape/test_check_doc_references.py` | ci:C356 |
| AG-C168 | 1 | `tests/reshape/test_repo_hygiene.py` | ci:C359 |
| AG-C169 | 1 | `tests/reshape/test_timeline_installed_skills.py` | ci:C360 |
| AG-C170 | 4 | `tests/upgrade/test_upgrade_release.py` | lanes:C27 |
| AG-C171 | 1 | `tests/upgrade/test_c1_product_gaps.py` | lanes:C70 |
| AG-C172 | 3 | `tests/test_installed_generation_journey.py` | ci:C40 |
| AG-C173 | 3 | `tests/test_skills_sync_registry.py` | ci:C70, ci:C210 |
| AG-C174 | 3 | `tests/test_failure_mode_executor.py` | ci:C161, ci:C162, ci:C163 |
| AG-C175 | 3 | `tests/test_installer_installed_schema.py` | ci:C172, ci:C173, ci:C174 |
| AG-C176 | 3 | `tests/test_omp_agent.py` | ci:C193, ci:C194, ci:C195 |
| AG-C177 | 3 | `tests/test_skills_developer.py` | ci:C203, ci:C204, ci:C205 |
| AG-C178 | 3 | `tests/test_third_party_integration.py` | ci:C214, ci:C215, ci:C216 |
| AG-C179 | 3 | `tests/test_timeline_editing_helpers.py` | ci:C217, ci:C218, ci:C219 |
| AG-C180 | 2 | `tests/test_setup_skill_branches.py` | ci:C7 |
| AG-C181 | 2 | `tests/test_diagnostics_callers.py` | ci:C54 |
| AG-C182 | 2 | `tests/test_installer_autostart.py` | ci:C58 |
| AG-C183 | 2 | `tests/test_installer_launcher_repair.py` | ci:C59 |
| AG-C184 | 2 | `tests/test_installer_service_repair_integration.py` | ci:C61 |
| AG-C185 | 2 | `tests/test_installer_shim.py` | ci:C63 |
| AG-C186 | 2 | `tests/test_local_install.py` | ci:C68 |
| AG-C187 | 2 | `tests/test_skills_cli.py` | ci:C69 |
| AG-C188 | 2 | `tests/test_ci_journey.py` | ci:C151, ci:C152 |
| AG-C189 | 2 | `tests/test_creator_entry_declarations.py` | ci:C156, ci:C157 |
| AG-C190 | 2 | `tests/test_installer_lifecycle.py` | ci:C177, lanes:C63 |
| AG-C191 | 2 | `tests/test_journey_diagnostic_checkpoint.py` | ci:C189, ci:C191 |
| AG-C192 | 2 | `tests/test_skills_selected_composition.py` | ci:C208, ci:C209 |
| AG-C193 | 2 | `tests/test_structure_contracts.py` | ci:C212, ci:C213 |
| AG-C194 | 1 | `tests/journeys/test_cross_client.py` | lanes:C93 |
| AG-C195 | 1 | `tests/journeys/test_journey_plumbing.py` | lanes:C94 |
| AG-C196 | 1 | `tests/test_boundary_handoff.py` | ci:C144 |
| AG-C197 | 1 | `tests/test_boundary_registration.py` | ci:C145 |
| AG-C198 | 1 | `tests/test_canonical_entrypoint.py` | ci:C150 |
| AG-C199 | 1 | `tests/test_core_pack_boundary_guard.py` | ci:C153 |
| AG-C200 | 1 | `tests/test_core_provider_neutrality.py` | ci:C154 |
| AG-C201 | 1 | `tests/test_core_util_surface.py` | ci:C155 |
| AG-C202 | 1 | `tests/test_env_vars_conformance.py` | ci:C158 |
| AG-C203 | 1 | `tests/test_external_app_contract.py` | ci:C159 |
| AG-C204 | 1 | `tests/test_external_pack_contract.py` | ci:C160 |
| AG-C205 | 1 | `tests/test_generic_host_result_json.py` | ci:C166 |
| AG-C206 | 1 | `tests/test_gpu_journey_receipts.py` | ci:C167 |
| AG-C207 | 1 | `tests/test_installer_acl.py` | ci:C168 |
| AG-C208 | 1 | `tests/test_installer_app_update.py` | ci:C169 |
| AG-C209 | 1 | `tests/test_installer_bootstrap_imports.py` | ci:C170 |
| AG-C210 | 1 | `tests/test_installer_busy_fence.py` | ci:C171 |
| AG-C211 | 1 | `tests/test_installer_launchd_cache_window.py` | ci:C175 |
| AG-C212 | 1 | `tests/test_installer_launchd_stop_handoff.py` | ci:C176 |
| AG-C213 | 1 | `tests/test_installer_local_update.py` | ci:C178 |
| AG-C214 | 1 | `tests/test_installer_r0_entry.py` | ci:C184 |
| AG-C215 | 1 | `tests/test_installer_update_legacy_record.py` | ci:C185 |
| AG-C216 | 1 | `tests/test_journey_windows_acl_capture.py` | ci:C190 |
| AG-C217 | 1 | `tests/test_n1_permission_boundary_guard.py` | ci:C192 |
| AG-C218 | 1 | `tests/test_onboarding_one_home.py` | ci:C196 |
| AG-C219 | 1 | `tests/test_pipeline_dispatch_aliases.py` | ci:C197 |
| AG-C220 | 1 | `tests/test_platform_matrix.py` | ci:C198 |
| AG-C221 | 1 | `tests/test_provider_route_grant.py` | ci:C199 |
| AG-C222 | 1 | `tests/test_public_boundary.py` | ci:C200 |
| AG-C223 | 1 | `tests/test_recoverability_conformance.py` | ci:C201 |
| AG-C224 | 1 | `tests/test_sdk_public_surface.py` | ci:C202 |
| AG-C225 | 1 | `tests/test_skills_installed_composition.py` | ci:C206 |
| AG-C226 | 1 | `tests/test_skills_package_data.py` | ci:C207 |
| AG-C227 | 1 | `tests/test_skip_policy.py` | ci:C211 |
| AG-C228 | 1 | `tests/test_update_from_field_states.py` | ci:C220 |
| AG-C229 | 1 | `tests/test_installer_real_product_root.py` | lanes:C68 |
| AG-C230 | 1 | `tests/installed/test_installed_generation_package.py` | lanes:C76 |

## IDs per owner

| Owner | IDs |
| --- | ---: |
| AG-A1 | 227 |
| AG-A2 | 121 |
| AG-A3 | 60 |
| AG-A5 | 74 |
| AG-A6 | 22 |
| AG-A7 | 283 |
| AG-A9 | 125 |
| AG-A10 | 80 |
| AG-B1 | 62 |
| AG-B2 | 45 |
| AG-B4 | 9 |
| AG-B5 | 32 |
| AG-B7 | 15 |
| AG-B9 | 7 |
| AG-B10 | 13 |
| AG-B11 | 13 |
| AG-B12 | 21 |
| AG-B13 | 39 |
| AG-B14 | 34 |
| AG-B15 | 25 |
| AG-B16 | 19 |
| AG-B17 | 10 |
| AG-B18 | 10 |
| AG-B19 | 20 |
| AG-B20 | 16 |
| AG-B21 | 7 |
| AG-B22 | 2 |
| AG-P1 | 70 |
| AG-P2 | 50 |
| Wave C | 419 |

Total: 1930 distinct (job, id) pairs.
