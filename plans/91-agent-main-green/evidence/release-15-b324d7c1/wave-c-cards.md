# Wave C cards

393 failing IDs that no Wave A or B card owns, in 232 test files. One card per row: the IDs in that file, fixed by cause under the [triage rules](../../tasks.md#triage-rules). A file with more than one cause splits into one card per cause. The manager gives a worker several rows from one area at a time, up to about ten IDs.

| Card | IDs | Test file | Clusters |
| --- | ---: | --- | --- |
| AG-C1 | 6 | `tests/packs/builtin/test_training_run_support.py` | ci:C251, ci:C252, ci:C253, ci:C254, ci:C255, ci:C256 |
| AG-C2 | 5 | `tests/packs/rendering/test_remotion_render_contract.py` | ci:C33, ci:C435 |
| AG-C3 | 4 | `tests/packs/rendering/test_timeline_route_integration.py` | ci:C210, ci:C211, ci:C212, ci:C213 |
| AG-C4 | 4 | `tests/packs/builtin/training_run/test_runtime_state_resume.py` | ci:C257, ci:C258, ci:C259, ci:C260 |
| AG-C5 | 3 | `tests/packs/rendering/test_timeline_storyboard.py` | ci:C214, ci:C215, ci:C216 |
| AG-C6 | 3 | `tests/packs/h3_av/test_static_mask_preflight.py` | lanes:C33 |
| AG-C7 | 3 | `tests/packs/rendering/test_hyperframes_backend.py` | lanes:C34 |
| AG-C8 | 3 | `tests/packs/runpod/test_https_transport.py` | lanes:C35 |
| AG-C9 | 2 | `tests/packs/rendering/test_ffmpeg_support.py` | ci:C68 |
| AG-C10 | 2 | `tests/packs/h3_av/test_edit_inputs.py` | ci:C72 |
| AG-C11 | 2 | `tests/packs/rendering/test_timeline_visualize_motion_views.py` | ci:C93 |
| AG-C12 | 2 | `tests/packs/runpod/test_ratchet_invariants.py` | ci:C96, ci:C97 |
| AG-C13 | 2 | `tests/packs/timeline/test_cli_parity.py` | ci:C129, ci:C130 |
| AG-C14 | 2 | `tests/packs/timeline/test_show_clip_working_copy.py` | ci:C133, ci:C134 |
| AG-C15 | 2 | `tests/packs/rendering/test_timeline_transfer_actions.py` | ci:C217, lanes:C102 |
| AG-C16 | 2 | `tests/packs/builtin/test_training_run_seinfeld_parity.py` | ci:C249, ci:C250 |
| AG-C17 | 2 | `tests/packs/h3_av/test_compile_generalized.py` | ci:C262, ci:C263 |
| AG-C18 | 2 | `tests/packs/h3_av/test_character_swap_cpu_boundary.py` | lanes:C97, lanes:C98 |
| AG-C19 | 1 | `tests/packs/runpod/test_models_lock_paths.py` | ci:C95 |
| AG-C20 | 1 | `tests/packs/runpod/test_review_rest_v2.py` | ci:C98 |
| AG-C21 | 1 | `tests/packs/test_b2_integrated_closure.py` | ci:C99 |
| AG-C22 | 1 | `tests/packs/test_executor_admission.py` | ci:C100 |
| AG-C23 | 1 | `tests/packs/test_generation_verb_extensions.py` | ci:C101 |
| AG-C24 | 1 | `tests/packs/test_public_id_resolution.py` | ci:C125 |
| AG-C25 | 1 | `tests/packs/test_vibecomfy_ir_bridge.py` | ci:C126 |
| AG-C26 | 1 | `tests/packs/timeline/test_cli_clash_back.py` | ci:C127 |
| AG-C27 | 1 | `tests/packs/timeline/test_cli_find.py` | ci:C128 |
| AG-C28 | 1 | `tests/packs/timeline/test_cli_v3_sweep_log.py` | ci:C131 |
| AG-C29 | 1 | `tests/packs/timeline/test_parent_clips.py` | ci:C132 |
| AG-C30 | 1 | `tests/packs/timeline/test_verbs_working_copy.py` | ci:C135 |
| AG-C31 | 1 | `tests/packs/timeline/test_visualize_drafts.py` | ci:C136 |
| AG-C32 | 1 | `tests/packs/vibecomfy/test_local_launch_facts.py` | ci:C137 |
| AG-C33 | 1 | `tests/packs/vibecomfy/test_local_server_media.py` | ci:C138 |
| AG-C34 | 1 | `tests/packs/h3_av/test_workflow_model_urls.py` | ci:C206 |
| AG-C35 | 1 | `tests/packs/rendering/test_normal_audio_http.py` | ci:C207 |
| AG-C36 | 1 | `tests/packs/rendering/test_remotion_backend.py` | ci:C208 |
| AG-C37 | 1 | `tests/packs/rendering/test_render_remotion_registry.py` | ci:C209 |
| AG-C38 | 1 | `tests/packs/rendering/test_timeline_visualize_motion.py` | ci:C218 |
| AG-C39 | 1 | `tests/packs/builtin/generate_image/test_codex_backend.py` | ci:C247 |
| AG-C40 | 1 | `tests/packs/builtin/test_training_run_ai_toolkit_support.py` | ci:C248 |
| AG-C41 | 1 | `tests/packs/builtin/training_run/test_seinfeld_parity.py` | ci:C261 |
| AG-C42 | 1 | `tests/packs/h3_av/test_generation.py` | ci:C264 |
| AG-C43 | 1 | `tests/packs/h3_av/test_two_edit_cpu_qualification.py` | lanes:C99 |
| AG-C44 | 1 | `tests/packs/rendering/test_shot_layering_export.py` | lanes:C101 |
| AG-C45 | 1 | `tests/packs/test_renderer_parity.py` | lanes:C104 |
| AG-C46 | 11 | `tests/core/rendering/test_remotion_runtime.py` | ci:C81, ci:C348, ci:C349, ci:C350, ci:C351, ci:C352, ci:C353, ci:C354, ci:C355, ci:C356 |
| AG-C47 | 10 | `tests/core/rendering/test_registry.py` | ci:C333, ci:C334, ci:C335, ci:C336, ci:C337, ci:C338, ci:C339, ci:C340, ci:C341, ci:C342 |
| AG-C48 | 5 | `tests/core/generation/backends/test_qwen_21_turbo.py` | ci:C70, ci:C227, ci:C228, ci:C229 |
| AG-C49 | 5 | `tests/core/rendering/test_registry_matrix.py` | ci:C343, ci:C344, ci:C345, ci:C346, ci:C347 |
| AG-C50 | 3 | `tests/core/generation/test_runpod_engine_selection.py` | ci:C79, ci:C326 |
| AG-C51 | 3 | `tests/core/generation/test_public_route_guard.py` | ci:C316, ci:C317, ci:C318 |
| AG-C52 | 3 | `tests/core/test_elements_cli.py` | ci:C358, ci:C359, ci:C360 |
| AG-C53 | 2 | `tests/core/generation/test_engine_fresh_install.py` | ci:C71 |
| AG-C54 | 2 | `tests/core/execution/test_host_cleanup_ack_barrier.py` | ci:C219, ci:C224 |
| AG-C55 | 2 | `tests/core/generation/test_cli_gold_075b.py` | ci:C230, ci:C231 |
| AG-C56 | 2 | `tests/core/generation/test_generation_index.py` | ci:C241, ci:C242 |
| AG-C57 | 2 | `tests/core/generation/test_readiness_inputs_f04.py` | ci:C319, ci:C320 |
| AG-C58 | 1 | `tests/core/execution/test_bug14_settlement_liveness.py` | ci:C220 |
| AG-C59 | 1 | `tests/core/execution/test_fail_closed_g28.py` | ci:C221 |
| AG-C60 | 1 | `tests/core/execution/test_generic_host_actions_v3.py` | ci:C222 |
| AG-C61 | 1 | `tests/core/execution/test_generic_host_verified_preparation_gr03.py` | ci:C223 |
| AG-C62 | 1 | `tests/core/execution/test_platform_boundary.py` | ci:C225 |
| AG-C63 | 1 | `tests/core/execution/test_private_network_command.py` | ci:C226 |
| AG-C64 | 1 | `tests/core/generation/test_edit_image_ref_admission.py` | ci:C239 |
| AG-C65 | 1 | `tests/core/generation/test_engine_error_reasons.py` | ci:C240 |
| AG-C66 | 1 | `tests/core/generation/test_generation_setup_walk.py` | ci:C243 |
| AG-C67 | 1 | `tests/core/generation/test_h3_build_after_outputs.py` | ci:C244 |
| AG-C68 | 1 | `tests/core/generation/test_listing.py` | ci:C245 |
| AG-C69 | 1 | `tests/core/generation/test_moved_data_composition.py` | ci:C246 |
| AG-C70 | 1 | `tests/core/generation/test_release_python.py` | ci:C315 |
| AG-C71 | 1 | `tests/core/generation/test_run_local.py` | ci:C325 |
| AG-C72 | 1 | `tests/core/generation/test_trusted_inventory.py` | ci:C327 |
| AG-C73 | 1 | `tests/core/generation/test_warm_models_remain_loaded.py` | ci:C328 |
| AG-C74 | 1 | `tests/core/model_catalog/test_registry.py` | ci:C329 |
| AG-C75 | 1 | `tests/core/pack/test_v3_core_worker_luna.py` | ci:C330 |
| AG-C76 | 1 | `tests/core/rendering/test_installed_registry_security.py` | ci:C331 |
| AG-C77 | 1 | `tests/core/rendering/test_production_callers.py` | ci:C332 |
| AG-C78 | 1 | `tests/core/test_element_kind_registry.py` | ci:C357 |
| AG-C79 | 1 | `tests/core/test_executor_registry_snapshot.py` | ci:C361 |
| AG-C80 | 1 | `tests/core/test_generation_backend_registry.py` | ci:C362 |
| AG-C81 | 1 | `tests/core/test_generation_taxonomy_registry.py` | ci:C363 |
| AG-C82 | 1 | `tests/core/test_pack_coherence_elements.py` | ci:C364 |
| AG-C83 | 1 | `tests/core/timeline/test_clip_fields.py` | ci:C365 |
| AG-C84 | 4 | `tests/sdk/test_timeline_checkout.py` | ci:C200, ci:C201, lanes:C38 |
| AG-C85 | 4 | `tests/sdk/test_timeline_current_union_schema.py` | ci:C369, ci:C370, ci:C371, ci:C372 |
| AG-C86 | 4 | `tests/sdk/test_timeline_selected_schema_runtime.py` | lanes:C40, lanes:C58, lanes:C59 |
| AG-C87 | 3 | `tests/sdk/test_runtime_response_conformance.py` | ci:C63, ci:C196 |
| AG-C88 | 2 | `tests/sdk/test_generation_target.py` | ci:C186, ci:C187 |
| AG-C89 | 2 | `tests/sdk/test_generation_verified_preparation_gr03.py` | ci:C188, ci:C189 |
| AG-C90 | 2 | `tests/sdk/test_timeline_commit_provider.py` | ci:C367, ci:C368 |
| AG-C91 | 2 | `tests/sdk/test_wc6_completion_capture.py` | ci:C382, ci:C383 |
| AG-C92 | 2 | `tests/sdk/test_timeline_commit_provider_runtime.py` | lanes:C39 |
| AG-C93 | 1 | `tests/sdk/test_d124_shared_custody.py` | ci:C184 |
| AG-C94 | 1 | `tests/sdk/test_generation_source_retention.py` | ci:C185 |
| AG-C95 | 1 | `tests/sdk/test_host_recovery.py` | ci:C190 |
| AG-C96 | 1 | `tests/sdk/test_openai_image_admission.py` | ci:C191 |
| AG-C97 | 1 | `tests/sdk/test_p1_case_corpus.py` | ci:C192 |
| AG-C98 | 1 | `tests/sdk/test_p1_doc_patch_requests.py` | ci:C193 |
| AG-C99 | 1 | `tests/sdk/test_p4_note_rerun.py` | ci:C194 |
| AG-C100 | 1 | `tests/sdk/test_projectless_admission.py` | ci:C195 |
| AG-C101 | 1 | `tests/sdk/test_scene_real_public_summary_rle.py` | ci:C197 |
| AG-C102 | 1 | `tests/sdk/test_selected_param_neutral_stage.py` | ci:C198 |
| AG-C103 | 1 | `tests/sdk/test_timeline_checkout_history.py` | ci:C202 |
| AG-C104 | 1 | `tests/sdk/test_timeline_film_length.py` | ci:C373 |
| AG-C105 | 1 | `tests/sdk/test_timeline_public_command.py` | ci:C378 |
| AG-C106 | 1 | `tests/sdk/test_timeline_render_publication.py` | ci:C379 |
| AG-C107 | 1 | `tests/sdk/test_timeline_selected_param_authority.py` | ci:C380 |
| AG-C108 | 1 | `tests/sdk/test_timeline_sheet_native.py` | ci:C381 |
| AG-C109 | 1 | `tests/sdk/test_timeline_export.py` | lanes:C56 |
| AG-C110 | 1 | `tests/sdk/test_timeline_import.py` | lanes:C57 |
| AG-C111 | 7 | `tests/integrations/test_runpod_slot_path_cpu.py` | lanes:C15, lanes:C93, lanes:C94 |
| AG-C112 | 4 | `tests/integrations/test_dry_run_equals_live_run.py` | lanes:C15, lanes:C45 |
| AG-C113 | 4 | `tests/integrations/test_media_only_render_without_remotion.py` | lanes:C27 |
| AG-C114 | 3 | `tests/integrations/test_generic_host_activation_acceptance.py` | lanes:C83, lanes:C84, lanes:C85 |
| AG-C115 | 2 | `tests/integrations/test_generic_host_remotion_render.py` | lanes:C73, lanes:C86 |
| AG-C116 | 2 | `tests/integrations/test_runpod_dry_live_seam.py` | lanes:C91, lanes:C92 |
| AG-C117 | 1 | `tests/integrations/test_managed_media_saved_visualize.py` | ci:C433 |
| AG-C118 | 1 | `tests/integrations/test_r14_builtin_transitions.py` | ci:C434 |
| AG-C119 | 1 | `tests/integrations/test_pinned_element_render_proof.py` | lanes:C44 |
| AG-C120 | 1 | `tests/integrations/test_runpod_host_endpoint_r5.py` | lanes:C44 |
| AG-C121 | 1 | `tests/integrations/test_command_count_capture.py` | lanes:C78 |
| AG-C122 | 1 | `tests/integrations/test_core_hivemind_installed.py` | lanes:C79 |
| AG-C123 | 1 | `tests/integrations/test_e2_publication_contract_roundtrip.py` | lanes:C80 |
| AG-C124 | 1 | `tests/integrations/test_pinned_source_cpu.py` | lanes:C89 |
| AG-C125 | 1 | `tests/integrations/test_pod_owned_preparation.py` | lanes:C90 |
| AG-C126 | 3 | `tests/editing_conformance/test_commit_runtime_identity.py` | lanes:C28 |
| AG-C127 | 3 | `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py` | lanes:C29 |
| AG-C128 | 2 | `tests/editing_conformance/test_native_word_anchor_vectors.py` | ci:C67 |
| AG-C129 | 2 | `tests/editing_conformance/test_commit_runtime_first_clip.py` | lanes:C36 |
| AG-C130 | 2 | `tests/editing_conformance/test_commit_runtime_occurrence_create.py` | lanes:C37 |
| AG-C131 | 1 | `tests/editing_conformance/test_fork_abi1_binding_set.py` | ci:C203 |
| AG-C132 | 1 | `tests/editing_conformance/test_producer_insertion.py` | ci:C204 |
| AG-C133 | 1 | `tests/editing_conformance/test_recipe_m2_clip_trim.py` | ci:C205 |
| AG-C134 | 1 | `tests/editing_conformance/test_compile_contracts.py` | ci:C366 |
| AG-C135 | 1 | `tests/editing_conformance/test_commit_runtime_numeric_params.py` | lanes:C51 |
| AG-C136 | 1 | `tests/editing_conformance/test_commit_runtime_source_copy.py` | lanes:C52 |
| AG-C137 | 1 | `tests/editing_conformance/test_occurrence_shared_d20.py` | lanes:C74 |
| AG-C138 | 1 | `tests/editing_conformance/test_occurrence_shared_historical.py` | lanes:C75 |
| AG-C139 | 1 | `tests/editing_conformance/test_prepared_video_birth.py` | lanes:C76 |
| AG-C140 | 6 | `tests/scripts/test_claim_runpod_5090_backup.py` | ci:C59, ci:C144, ci:C145, ci:C146, ci:C147 |
| AG-C141 | 3 | `tests/scripts/test_gpu_sanity.py` | ci:C149, ci:C150, ci:C151 |
| AG-C142 | 1 | `tests/scripts/test_cuda_default_sites.py` | ci:C148 |
| AG-C143 | 1 | `tests/scripts/test_pod_action_source.py` | ci:C152 |
| AG-C144 | 1 | `tests/scripts/test_pod_h3_install.py` | ci:C165 |
| AG-C145 | 3 | `tests/stage1/test_zero_shim_execution_pack_deletion.py` | ci:C388, ci:C389, ci:C390 |
| AG-C146 | 2 | `tests/stage1/test_runtime_lifecycle_reproducer.py` | ci:C94 |
| AG-C147 | 2 | `tests/stage1/test_capability_parity_gate_luna.py` | ci:C384, lanes:C60 |
| AG-C148 | 1 | `tests/stage1/test_generic_host_process_bootstrap_luna.py` | ci:C385 |
| AG-C149 | 1 | `tests/stage1/test_pack_api_surface.py` | ci:C386 |
| AG-C150 | 1 | `tests/stage1/test_vendored_workspace_client_parity_luna.py` | ci:C387 |
| AG-C151 | 1 | `tests/stage1/test_media_handoff_render_boundary.py` | lanes:C61 |
| AG-C152 | 1 | `tests/stage1/test_runtime_client_cutover.py` | lanes:C62 |
| AG-C153 | 3 | `tests/v10/test_docs_cli_alignment.py` | ci:C310, ci:C311, ci:C312 |
| AG-C154 | 2 | `tests/v10/test_pack_write_path_lint.py` | ci:C78 |
| AG-C155 | 1 | `tests/v10/test_authority_lint.py` | ci:C309 |
| AG-C156 | 1 | `tests/v10/test_domain_cli_projects_timelines.py` | ci:C313 |
| AG-C157 | 1 | `tests/v10/test_release_reproducibility.py` | ci:C314 |
| AG-C158 | 1 | `tests/v10/test_timelines_create.py` | lanes:C72 |
| AG-C159 | 1 | `tests/timeline/test_authoring_bundle.py` | ci:C303 |
| AG-C160 | 1 | `tests/timeline/test_effects_catalog.py` | ci:C304 |
| AG-C161 | 1 | `tests/timeline/test_html_canvas_effect.py` | ci:C305 |
| AG-C162 | 1 | `tests/timeline/test_shot_composition_projection.py` | ci:C306 |
| AG-C163 | 1 | `tests/timeline/test_shot_layering_projection.py` | ci:C307 |
| AG-C164 | 1 | `tests/timeline/test_timeline_elements_catalog.py` | ci:C308 |
| AG-C165 | 1 | `tests/timeline/test_authoring_media.py` | lanes:C69 |
| AG-C166 | 5 | `tests/test_generic_host.py` | ci:C49, ci:C411, ci:C412 |
| AG-C167 | 2 | `tests/reshape/test_compare_baselines.py` | ci:C140, ci:C141 |
| AG-C168 | 1 | `tests/reshape/test_check_doc_references.py` | ci:C139 |
| AG-C169 | 1 | `tests/reshape/test_repo_hygiene.py` | ci:C142 |
| AG-C170 | 1 | `tests/reshape/test_timeline_installed_skills.py` | ci:C143 |
| AG-C171 | 3 | `tests/test_installed_generation_journey.py` | ci:C50 |
| AG-C172 | 3 | `tests/test_skills_sync_registry.py` | ci:C77, ci:C292 |
| AG-C173 | 3 | `tests/test_omp_agent.py` | ci:C275, ci:C276, ci:C277 |
| AG-C174 | 3 | `tests/test_provider_route_grant.py` | ci:C281, ci:C436, ci:C437 |
| AG-C175 | 3 | `tests/test_skills_developer.py` | ci:C285, ci:C286, ci:C287 |
| AG-C176 | 3 | `tests/test_third_party_integration.py` | ci:C296, ci:C297, ci:C298 |
| AG-C177 | 3 | `tests/test_timeline_editing_helpers.py` | ci:C299, ci:C300, ci:C301 |
| AG-C178 | 3 | `tests/test_failure_mode_executor.py` | ci:C408, ci:C409, ci:C410 |
| AG-C179 | 3 | `tests/test_installer_installed_schema.py` | ci:C419, ci:C420, ci:C421 |
| AG-C180 | 2 | `tests/test_setup_skill_branches.py` | ci:C73 |
| AG-C181 | 2 | `tests/test_local_install.py` | ci:C74 |
| AG-C182 | 2 | `tests/test_skills_cli.py` | ci:C76 |
| AG-C183 | 2 | `tests/test_diagnostics_callers.py` | ci:C82 |
| AG-C184 | 2 | `tests/test_installer_autostart.py` | ci:C86 |
| AG-C185 | 2 | `tests/test_installer_launcher_repair.py` | ci:C87 |
| AG-C186 | 2 | `tests/test_installer_service_repair_integration.py` | ci:C89 |
| AG-C187 | 2 | `tests/test_installer_shim.py` | ci:C91 |
| AG-C188 | 2 | `tests/test_journey_diagnostic_checkpoint.py` | ci:C271, ci:C273 |
| AG-C189 | 2 | `tests/test_skills_selected_composition.py` | ci:C290, ci:C291 |
| AG-C190 | 2 | `tests/test_structure_contracts.py` | ci:C294, ci:C295 |
| AG-C191 | 2 | `tests/test_ci_journey.py` | ci:C398, ci:C399 |
| AG-C192 | 2 | `tests/test_creator_entry_declarations.py` | ci:C403, ci:C404 |
| AG-C193 | 2 | `tests/test_installer_lifecycle.py` | ci:C424, lanes:C63 |
| AG-C194 | 1 | `tests/upgrade/test_c1_product_gaps.py` | lanes:C70 |
| AG-C195 | 1 | `tests/upgrade/test_upgrade_release.py` | lanes:C71 |
| AG-C196 | 1 | `tests/journeys/test_cross_client.py` | lanes:C95 |
| AG-C197 | 1 | `tests/journeys/test_journey_plumbing.py` | lanes:C96 |
| AG-C198 | 1 | `test_case.py` | ci:C45 |
| AG-C199 | 1 | `tests/test_journey_windows_acl_capture.py` | ci:C272 |
| AG-C200 | 1 | `tests/test_n1_permission_boundary_guard.py` | ci:C274 |
| AG-C201 | 1 | `tests/test_onboarding_one_home.py` | ci:C278 |
| AG-C202 | 1 | `tests/test_pipeline_dispatch_aliases.py` | ci:C279 |
| AG-C203 | 1 | `tests/test_platform_matrix.py` | ci:C280 |
| AG-C204 | 1 | `tests/test_public_boundary.py` | ci:C282 |
| AG-C205 | 1 | `tests/test_recoverability_conformance.py` | ci:C283 |
| AG-C206 | 1 | `tests/test_sdk_public_surface.py` | ci:C284 |
| AG-C207 | 1 | `tests/test_skills_installed_composition.py` | ci:C288 |
| AG-C208 | 1 | `tests/test_skills_package_data.py` | ci:C289 |
| AG-C209 | 1 | `tests/test_skip_policy.py` | ci:C293 |
| AG-C210 | 1 | `tests/test_update_from_field_states.py` | ci:C302 |
| AG-C211 | 1 | `tests/test_boundary_handoff.py` | ci:C391 |
| AG-C212 | 1 | `tests/test_boundary_registration.py` | ci:C392 |
| AG-C213 | 1 | `tests/test_canonical_entrypoint.py` | ci:C397 |
| AG-C214 | 1 | `tests/test_core_pack_boundary_guard.py` | ci:C400 |
| AG-C215 | 1 | `tests/test_core_provider_neutrality.py` | ci:C401 |
| AG-C216 | 1 | `tests/test_core_util_surface.py` | ci:C402 |
| AG-C217 | 1 | `tests/test_env_vars_conformance.py` | ci:C405 |
| AG-C218 | 1 | `tests/test_external_app_contract.py` | ci:C406 |
| AG-C219 | 1 | `tests/test_external_pack_contract.py` | ci:C407 |
| AG-C220 | 1 | `tests/test_generic_host_result_json.py` | ci:C413 |
| AG-C221 | 1 | `tests/test_gpu_journey_receipts.py` | ci:C414 |
| AG-C222 | 1 | `tests/test_installer_acl.py` | ci:C415 |
| AG-C223 | 1 | `tests/test_installer_app_update.py` | ci:C416 |
| AG-C224 | 1 | `tests/test_installer_bootstrap_imports.py` | ci:C417 |
| AG-C225 | 1 | `tests/test_installer_busy_fence.py` | ci:C418 |
| AG-C226 | 1 | `tests/test_installer_launchd_cache_window.py` | ci:C422 |
| AG-C227 | 1 | `tests/test_installer_launchd_stop_handoff.py` | ci:C423 |
| AG-C228 | 1 | `tests/test_installer_local_update.py` | ci:C425 |
| AG-C229 | 1 | `tests/test_installer_r0_entry.py` | ci:C431 |
| AG-C230 | 1 | `tests/test_installer_update_legacy_record.py` | ci:C432 |
| AG-C231 | 1 | `tests/test_installer_real_product_root.py` | lanes:C68 |
| AG-C232 | 1 | `tests/installed/test_installed_generation_package.py` | lanes:C77 |

## IDs per owner

| Owner | IDs |
| --- | ---: |
| AG-A1 | 227 |
| AG-A2 | 121 |
| AG-A3 | 60 |
| AG-A5 | 74 |
| AG-A6 | 22 |
| AG-A7 | 284 |
| AG-A9 | 90 |
| AG-A10 | 80 |
| AG-B1 | 62 |
| AG-B2 | 45 |
| AG-B4 | 9 |
| AG-B5 | 32 |
| AG-B7 | 15 |
| AG-B9 | 7 |
| AG-B10 | 13 |
| AG-B11 | 12 |
| AG-B12 | 21 |
| AG-B13 | 41 |
| AG-B14 | 33 |
| AG-B15 | 25 |
| AG-B16 | 19 |
| AG-B17 | 10 |
| AG-B18 | 10 |
| AG-B19 | 20 |
| AG-B20 | 16 |
| AG-B21 | 7 |
| AG-B22 | 6 |
| AG-P1 | 70 |
| AG-P2 | 50 |
| Wave C | 393 |

Total: 1874 distinct (job, id) pairs.
