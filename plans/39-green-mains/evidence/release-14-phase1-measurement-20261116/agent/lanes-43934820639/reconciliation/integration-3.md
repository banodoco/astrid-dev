# Integration shard 3 / 4 — job 133536534907

Run [43934820639](https://github.com/banodoco/astrid-agent/actions/runs/43934820639) attempt 1 at `b8f2692948d1b5987ee2938920f47aace0732792`; job completed with failure. See [job details](https://github.com/banodoco/astrid-agent/actions/runs/43934820639/job/133536534907).

JUnit artifact [14277921134](https://github.com/banodoco/astrid-agent/actions/runs/43934820639/artifacts/14277921134), SHA-256 `88e987ceeff7e87ba3d45b31c2a2ded5029d90f791a78e17355ac465b63544be`; expected metadata digest `88e987ceeff7e87ba3d45b31c2a2ded5029d90f791a78e17355ac465b63544be`. Artifact hash matches metadata.

## XML counts: 372 passed, 81 failed, 62 errors, 1 skipped (516 testcases).

The raw job-log request was made once and returned `Transport closed`; it was not retried. These are XML counts, not a reconstructed outer pytest summary. The XML does not report deselections, warnings, or outer elapsed-time summary. Full testcase IDs, literal XML `message` attributes, and testcase detail text are retained in `integration-3.json`.

## Literal XML failure/error messages and exact testcase IDs

### ERROR × 26

```text
failed on setup with "astrid.sdk.timeline._command_state.CommandError: replacement changes provider-managed edges"
```

IDs:
- `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-anchor]`
- `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-absent]`
- `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[video-anchor]`
- `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[video-absent]`
- `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_provider_accepts_completion_placement_with_exact_undo_and_redo[image]`
- `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_provider_accepts_completion_placement_with_exact_undo_and_redo[video]`
- `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_exact_capture_replay_inverse_and_redo[create]`
- `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_exact_capture_replay_inverse_and_redo[unplace]`
- `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_provider_accepts_create_with_exact_undo_and_redo`
- `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_provider_accepts_unplace_with_exact_undo_and_redo`
- `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-append]`
- `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py::test_exact_capture_replay_inverse_and_redo[video-append]`
- `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-shift]`
- `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py::test_exact_capture_replay_inverse_and_redo[video-overlay-anchor]`
- `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py::test_provider_accepts_shared_placement_with_exact_undo_and_redo[image]`
- `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py::test_provider_accepts_shared_placement_with_exact_undo_and_redo[video]`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_exact_capture_replay_inverse_and_redo[add-first]`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_exact_capture_replay_inverse_and_redo[add-second]`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_exact_capture_replay_inverse_and_redo[remove-middle]`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_provider_accepts_add_and_remove_with_exact_undo_and_redo`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_placing_pooled_media_promotes_it_in_one_batch_that_undoes_as_one[image]`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_placing_pooled_media_promotes_it_in_one_batch_that_undoes_as_one[video]`
- `tests/editing_conformance/test_recipe_m2_shot_pool.py::test_promotion_and_keep_as_pooled_round_trip_through_the_provider`
- `tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo`
- `tests/editing_conformance/test_recipe_occurrence_media.py::test_provider_exact_reload_inverse_redo_and_retired_asset_reservation[add]`
- `tests/editing_conformance/test_recipe_occurrence_media.py::test_provider_exact_reload_inverse_redo_and_retired_asset_reservation[swap]`

### ERROR × 16

```text
failed on setup with "IndexError: list index out of range"
```

IDs:
- `tests/packs/rendering/test_live_source_label_native.py::test_runtime_capture_ref_reaches_existing_host_source[False]`
- `tests/packs/rendering/test_live_source_label_native.py::test_runtime_capture_ref_reaches_existing_host_source[True]`
- `tests/packs/rendering/test_live_source_label_native.py::test_forged_capture_refuses_before_any_writes[config]`
- `tests/packs/rendering/test_live_source_label_native.py::test_forged_capture_refuses_before_any_writes[registry]`
- `tests/packs/rendering/test_live_source_label_native.py::test_forged_capture_refuses_before_any_writes[expansion]`
- `tests/packs/rendering/test_live_source_label_native.py::test_forged_capture_refuses_before_any_writes[missing-media]`
- `tests/packs/rendering/test_live_source_label_native.py::test_replacement_refuses_before_label[config]`
- `tests/packs/rendering/test_live_source_label_native.py::test_replacement_refuses_before_label[metadata]`
- `tests/packs/rendering/test_live_source_label_native.py::test_replacement_refuses_before_label[registry]`
- `tests/packs/rendering/test_live_source_label_native.py::test_replacement_refuses_before_label[source]`
- `tests/packs/rendering/test_live_source_label_native.py::test_replacement_refuses_before_label[ref]`
- `tests/packs/rendering/test_live_source_label_native.py::test_replacement_refuses_before_label[prepared]`
- `tests/packs/rendering/test_live_source_label_native.py::test_cas_and_unclaimed_inputs_stay_uncertified[False]`
- `tests/packs/rendering/test_live_source_label_native.py::test_cas_and_unclaimed_inputs_stay_uncertified[True]`
- `tests/packs/rendering/test_live_source_label_native.py::test_retained_source_reaches_exact_final_root_inside_normal_lifetime[False]`
- `tests/packs/rendering/test_live_source_label_native.py::test_retained_source_reaches_exact_final_root_inside_normal_lifetime[True]`

### ERROR × 14

```text
failed on setup with "runtime_protocol.errors.RuntimeErrorBase: candidate.timing: legacy word anchor is missing"
```

IDs:
- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_asset_clear_lost_ack_reload_retry_undo`
- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_transition_clear_lost_ack_reload_retry_undo`
- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_trim_stale_rebase_lost_ack_reload_retry_undo`
- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_split_stale_rebase_lost_ack_reload_retry_undo`
- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_parent_delete_stale_rebase_lost_ack_reload_retry_undo`
- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_ambiguous_owner_and_mixed_edits_keep_original_draft`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_exact_retained_v1_compiles_after_cas_v2_restart_and_cache_corruption`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_accepted_rebase_has_exact_document_but_no_reconstructible_word_choice`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_reselecting_ordinal_after_real_rebase_silently_changes_raw_source_clip[True]`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_source_authority_refuses_without_latest_fallback[unavailable]`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_source_authority_refuses_without_latest_fallback[missing-pin]`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_source_authority_refuses_without_latest_fallback[foreign]`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_retained_v1_and_explicit_v2_keep_window_and_raw_source_identity[True-1]`
- `tests/editing_conformance/test_timing_retained_inputs.py::test_retained_v1_and_explicit_v2_keep_window_and_raw_source_identity[True-2]`

### FAILED × 7

```text
astrid.core.execution.generic_host.HostError: undeclared secret environment variable 'FAL_KEY'
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_production_t2i_command_runs_through_host_broker_http_substitute`
- `tests/integrations/test_generation_runtime_composition.py::test_production_t2i_command_uses_https_connect_and_auth[None]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_i2i_command_uses_ordered_cas_through_https_connect_and_auth[False]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_qwen_edit_command_uses_ordered_cas_through_https_connect_and_auth[False]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_unified_edit_profiles_settle_variant_and_readback[qwen-inpaint]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_unified_edit_profiles_settle_variant_and_readback[klein-4b]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_unified_edit_profiles_settle_variant_and_readback[klein-9b]`

### FAILED × 6

```text
astrid.sdk.timeline._command_state.CommandError: created identity is occupied
```

IDs:
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_pristine_init_first_birth_reload_undo_and_missing_word_source[image]`
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_pristine_init_first_birth_reload_undo_and_missing_word_source[video]`
- `tests/editing_conformance/test_next_ordinary_union_runtime.py::test_born_occurrence_text_order_clear_grouped_inverse_and_redo[]`
- `tests/editing_conformance/test_next_ordinary_union_runtime.py::test_born_occurrence_text_order_clear_grouped_inverse_and_redo[new occurrence text\r\n]`
- `tests/editing_conformance/test_occurrence_fork_source_baseline.py::test_current_runtime_retained_fork_then_emitter`
- `tests/editing_conformance/test_s3_reviewed_cohort_runtime.py::test_init_occurrence_media_parent_swap_word_grouped_inverse_reload_restart`

### FAILED × 6

```text
runtime_protocol.errors.RuntimeErrorBase: provider executed a different command
```

IDs:
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_first_parent_media_then_stable_same_echo_word_choices_reload_inverse_and_retry[False]`
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_first_parent_media_then_stable_same_echo_word_choices_reload_inverse_and_retry[True]`
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_clip_cache_inverse_keeps_only_owned_transcript_pins[introduced]`
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_clip_cache_inverse_keeps_only_owned_transcript_pins[preexisting]`
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_clip_cache_inverse_keeps_only_owned_transcript_pins[surviving]`
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_clip_cache_inverse_keeps_only_owned_transcript_pins[opaque]`

### FAILED × 4

```text
AssertionError: Regex pattern did not match.
  Expected regex: 'bounded body limit'
  Actual message: "undeclared secret environment variable 'FAL_KEY'"
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_production_t2i_command_uses_https_connect_and_auth[0]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_t2i_command_uses_https_connect_and_auth[1]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_i2i_command_uses_ordered_cas_through_https_connect_and_auth[True]`
- `tests/integrations/test_generation_runtime_composition.py::test_production_qwen_edit_command_uses_ordered_cas_through_https_connect_and_auth[True]`

### FAILED × 3

```text
AttributeError: 'types.SimpleNamespace' object has no attribute 'session_ref'
```

IDs:
- `tests/packs/runpod/test_https_transport.py::test_https_production_composition_selects_claim_token_and_cleanup_needs_no_sidecar[claimed]`
- `tests/packs/runpod/test_https_transport.py::test_https_production_composition_selects_claim_token_and_cleanup_needs_no_sidecar[release_pending]`
- `tests/packs/runpod/test_https_transport.py::test_https_production_composition_selects_claim_token_and_cleanup_needs_no_sidecar[cleanup_pending]`

### ERROR × 2

```text
failed on setup with "Failed: the Runtime checkout /home/runner/work/astrid-agent/astrid-agent/astrid-runtime has no commit df3d4ddac7bf73cd858106cc51a802521a4d3552"
```

IDs:
- `tests/integrations/test_generic_host_runtime_restart.py::test_real_host_renews_short_lease_during_cpu_execution`
- `tests/integrations/test_generic_host_runtime_restart.py::test_expired_real_lease_rejects_renewal_and_host_fails_closed`

### FAILED × 2

```text
KeyError: 'on'
```

IDs:
- `tests/editing_conformance/test_native_word_anchor.py::test_reference_is_authoritative_and_kernel_never_searches_echo[None]`
- `tests/editing_conformance/test_word_binding_recipe.py::test_reference_is_authoritative_and_kernel_never_searches_echo[None]`

### FAILED × 2

```text
astrid.sdk.timeline._command_state.CommandError: invalid timing input: the parent holds two different clip lists (clips and config.clips)
```

IDs:
- `tests/editing_conformance/test_word_binding_recipe.py::test_follow_rebases_original_choice_after_source_move_and_reorder[True]`
- `tests/editing_conformance/test_word_binding_recipe.py::test_on_until_clear_preserves_other_reference_and_opaque_fields`

### FAILED × 2

```text
runtime_protocol.errors.RuntimeErrorBase: an intervening publication wrote a guarded address
```

IDs:
- `tests/editing_conformance/test_word_binding_recipe.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-False]`
- `tests/editing_conformance/test_word_binding_recipe.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-True]`

### FAILED × 2

```text
runtime_protocol.errors.RuntimeErrorBase: invalid timing input: the parent holds two different clip lists (clips and config.clips)
```

IDs:
- `tests/editing_conformance/test_word_binding_recipe.py::test_reference_is_authoritative_and_kernel_never_searches_echo["stop" #99 +300f]`
- `tests/editing_conformance/test_word_binding_recipe.py::test_reference_is_authoritative_and_kernel_never_searches_echo[obsolete display label]`

### ERROR × 1

```text
failed on setup with "assert None is not None"
```

IDs:
- `tests/integrations/test_generic_host_remotion_render.py::test_generic_host_remotion_register_claim_execute_settle_and_cas`

### ERROR × 1

```text
failed on setup with "file /home/runner/work/astrid-agent/astrid-agent/tests/integrations/test_pinned_element_render_proof.py, line 379
  def test_pinned_element_render_proof_on_standin(
E       fixture 'configured' not found
>       available fixtures: LineMatcher, _config_for_test, _editing_motion_pack, _generation_case_reader_cache, _h3_engine_facts, _installer_live_identity, _installer_private_home, _no_runpod_network_or_credentials, _pytest, _sandboxed_home_and_projects, _sys_snapshot, anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, connected, cov, doctest_namespace, draft, dry_runtime, editing_case, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, generation_settings_store, linecomp, monkeypatch, no_cover, no_renderer, owned_process_groups, platformdirs_isolated, preview_runtime, pytestconfig, pytester, r12_export, reader, real_live_probe, real_runtime, record_property, record_testsuite_property, record_xml_attribute, recwarn, remotion_project, restructure_runtime, saved_source, settled, subtests, testdir, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, vibecomfy_handle_factory, vibecomfy_workflow_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/runner/work/astrid-agent/astrid-agent/tests/integrations/test_pinned_element_render_proof.py:379"
```

IDs:
- `tests/integrations/test_pinned_element_render_proof.py::test_pinned_element_render_proof_on_standin`

### ERROR × 1

```text
failed on setup with "file /home/runner/work/astrid-agent/astrid-agent/tests/integrations/test_runpod_host_endpoint_r5.py, line 261
  def test_runtime_claim_binds_one_endpoint_and_delivers(retained, comfy, tmp_path, monkeypatch, real_runtime, tuple_sources):
file /home/runner/work/astrid-agent/astrid-agent/tests/packs/runpod/test_generation_preparation.py, line 52
  @pytest.fixture
  def retained(small_lease, sources, tmp_path, monkeypatch, request):
file /home/runner/work/astrid-agent/astrid-agent/tests/packs/runpod/test_warm_session.py, line 424
  @pytest.fixture
  def small_lease(lease_selection_case, monkeypatch):
file /home/runner/work/astrid-agent/astrid-agent/tests/packs/runpod/test_target_selection.py, line 20
  @pytest.fixture
  def case(tmp_path, monkeypatch, pod_watchdog_transport):
E       fixture 'pod_watchdog_transport' not found
>       available fixtures: LineMatcher, _config_for_test, _editing_motion_pack, _generation_case_reader_cache, _h3_engine_facts, _installer_live_identity, _installer_private_home, _no_runpod_network_or_credentials, _pytest, _sandboxed_home_and_projects, _sys_snapshot, anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, comfy, connected, cov, doctest_namespace, draft, dry_runtime, editing_case, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, generation_settings_store, host_route, lease_selection_case, linecomp, monkeypatch, no_cover, no_renderer, owned_process_groups, platformdirs_isolated, pytestconfig, pytester, r12_export, reader, real_live_probe, real_runtime, record_property, record_testsuite_property, record_xml_attribute, recwarn, restructure_runtime, retained, retained_host, saved_source, settled, small_lease, sources, subtests, testdir, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, tuple_sources, vibecomfy_handle_factory, vibecomfy_workflow_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/runner/work/astrid-agent/astrid-agent/tests/packs/runpod/test_target_selection.py:20"
```

IDs:
- `tests/integrations/test_runpod_host_endpoint_r5.py::test_runtime_claim_binds_one_endpoint_and_delivers`

### ERROR × 1

```text
failed on setup with "subprocess.CalledProcessError: Command '['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '-c', "\nimport json, sys\nfrom tests.editing_conformance.native_word_anchor_fixture import seed\noptions = json.loads(sys.argv[2])\nprint(json.dumps(seed(sys.argv[1], options.pop('reused', False), **options)))\n", '/tmp/pytest-of-runner/pytest-0/test_grouped_inverse_retains_s2/realm', '{"opaque_pin_scope": "occurrence", "current_form": true}']' returned non-zero exit status 1."
```

IDs:
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_inverse_retains_surviving_opaque_transcript_pin[retained2-occurrence]`

### FAILED × 1

```text
AssertionError: (410, '{"code": "retired_route", "details": {"hint": "Submit a timeline commit instead of the retired save route.", "reason": "timeline_commit_required", "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit", "status": "refused", "suggested_command": "timeline commit"}, "message": "legacy timeline writes are retired; submit EditCommands through commitTimeline", "request_id": "012c81f350c04f828c96bb99dc3669d4"}')
assert 410 in (200, 201)
```

IDs:
- `tests/integrations/test_media_only_render_without_remotion.py::test_a_task_selecting_remotion_is_admitted_and_then_fails_with_the_remotion_reason`

### FAILED × 1

```text
AssertionError: (410, '{"code": "retired_route", "details": {"hint": "Submit a timeline commit instead of the retired save route.", "reason": "timeline_commit_required", "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit", "status": "refused", "suggested_command": "timeline commit"}, "message": "legacy timeline writes are retired; submit EditCommands through commitTimeline", "request_id": "10593d7b0d5d4921a05c8f43f8be0eee"}')
assert 410 in (200, 201)
```

IDs:
- `tests/integrations/test_media_only_render_without_remotion.py::test_a_media_only_render_without_remotion_pins_revision_r_and_is_rendered_by_ffmpeg`

### FAILED × 1

```text
AssertionError: (410, '{"code": "retired_route", "details": {"hint": "Submit a timeline commit instead of the retired save route.", "reason": "timeline_commit_required", "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit", "status": "refused", "suggested_command": "timeline commit"}, "message": "legacy timeline writes are retired; submit EditCommands through commitTimeline", "request_id": "67f3d63ceed24c1883437c205fbe17b8"}')
assert 410 in (200, 201)
```

IDs:
- `tests/integrations/test_media_only_render_without_remotion.py::test_a_timeline_with_a_render_tail_fails_with_ffmpegs_reason_and_the_remotion_fault`

### FAILED × 1

```text
AssertionError: (410, '{"code": "retired_route", "details": {"hint": "Submit a timeline commit instead of the retired save route.", "reason": "timeline_commit_required", "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit", "status": "refused", "suggested_command": "timeline commit"}, "message": "legacy timeline writes are retired; submit EditCommands through commitTimeline", "request_id": "b9a74df7ffa4454fb804804ec6bd0a70"}')
assert 410 in (200, 201)
```

IDs:
- `tests/integrations/test_media_only_render_without_remotion.py::test_a_timeline_ffmpeg_refuses_fails_with_ffmpegs_reasons_and_the_remotion_fault`

### FAILED × 1

```text
AssertionError: ErrorObject(code='conflict', message='history_unavailable', details={'base': None, 'conflicts': [], 'current': None, 'reason': 'history_unavailable', 'status': 'refused'})
assert False
 +  where False = DomainResult(ok=False, data=None, error=ErrorObject(code='conflict', message='history_unavailable', details={'base': None, 'conflicts': [], 'current': None, 'reason': 'history_unavailable', 'status': 'refused'}), receipt=None, idempotency_key='').ok
```

IDs:
- `tests/packs/rendering/test_timeline_transfer_actions.py::test_real_pack_host_invokes_timeline_transfer_actions_read_only`

### FAILED × 1

```text
AssertionError: Regex pattern did not match.
  Expected regex: 'lost acknowledgement'
  Actual message: 'No reply could be verified; this edit may or may not have been committed. Call tl.commit(key="production") again with no other arguments to confirm the saved request.'
```

IDs:
- `tests/editing_conformance/test_occurrence_shared_historical.py::test_production_session_freezes_foreign_intent_and_retries_lost_ack`

### FAILED × 1

```text
AssertionError: assert '6855dfa8df65...4d6505493c17c' == 'f103bb468669...2e66d544e0c9b'
  
  - f103bb46866999c961a8865636f2e66d544e0c9b
  + 6855dfa8df65cf8ae4c002b57134d6505493c17c
```

IDs:
- `tests/editing_conformance/test_prepared_video_birth.py::test_prepared_video_public_preview_accept_retry_undo_and_no_write`

### FAILED × 1

```text
AssertionError: assert 'conflict' == 'refused'
  
  - refused
  + conflict
```

IDs:
- `tests/editing_conformance/test_word_binding_recipe.py::test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`

### FAILED × 1

```text
AssertionError: assert 'publication_contract.render' in {}
```

IDs:
- `tests/integrations/test_e2_publication_contract_roundtrip.py::test_publication_contract_producer_upload_fenced_settlement_roundtrip`

### FAILED × 1

```text
AssertionError: assert (False)
 +  where False = is_file()
 +    where is_file = PosixPath('/home/runner/work/receiving/coordination/evidence/B/shared-public-workspace-fixture/public_workspace.py').is_file
```

IDs:
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_h3_public_workspace_helper_pin_matches_current_shared_fixture`

### FAILED × 1

```text
AssertionError: assert [] == [_ParkedPackH...n_origins={})]
  
  Right contains one more item: _ParkedPackHostHandle(process=<Popen: returncode: None args: ['/opt/hostedtoolcache/Python/3.11.18/x64/bin...>, contro...62dd6e2be5cc28061b48439546905a7'}, cleanup_error=None, aborted=False, execution_profile='source', execution_origins={})
  
  Full diff:
  + []
  - [
  -     _ParkedPackHostHandle(
  -         process=<Popen: returncode: None args: ['/opt/hostedtoolcache/Python/3.11.18/x64/bin...>,
  -         control=<socket.socket [closed] fd=-1, family=1, type=1, proto=0>,
  -         reference=DeploymentReference(
  -                       deployment_id='cpu-receiver',
  -                       revision='cpu-receiver-1',
  -                       task_id='a730be8141b544ba9ac734b0cab89a34',
  -                       run_id='55c48293907042eda72c59c20d647fbb',
  -                       target_ref='machine:runnervmccnms',
  -                       effective_target_ref='machine:runnervmccnms',
  -                       executable=ArtifactReference(
  -                                      name='python',
  -                                      path=PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/bin/python3.11'),
  -                                      digest='sha256:af21e115e9498f5ed362ab3586ce0b18f10251186e69ca9a39570e79203bf434',
  -                                  ),
  -                       dependency_closure=(
  -                                              ArtifactReference(
  -                                                  name='cpu-pack',
  -                                                  path=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/cpu-pack'),
  -                                                  digest='sha256:6f30f9ed864c2b2cfdb151e535ff42dd8b360915eb98b7677ae77033845fb128',
  -                                              ),
  -                                              ArtifactReference(
  -                                                  name='imports',
  -                                                  path=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/python-libs'),
  -                                                  digest='sha256:0f766667277902780694ce497867218c1d309c67cbdb5caf431814d6434802e2',
  -                                              ),
  -                                              ArtifactReference(
  -                                                  name='python',
  -                                                  path=PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/bin/python3.11'),
  -                                                  digest='sha256:af21e115e9498f5ed362ab3586ce0b18f10251186e69ca9a39570e79203bf434',
  -                                              ),
  -                                          ),
  -                       source_closure_digest='sha256:936e0a01994d197afd6deda116a6b137ef96a040407b25bb3230471d05933c39',
  -                       data_root=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data'),
  -                       support_root=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime'),
  -                       runtime_endpoint='http://127.0.0.1:36911',
  -                       runtime_instance_id='31a60c52276140408a3b7fc1bcb1754d',
  -                       runtime_epoch=1,
  -                       runtime_schema_digest='sha256:9628bb5fd6e1dbbec392dd39f2e01031622dcf52d7ccff7cd1f0ad10743dcb1c',
  -                       model_root=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/models'),
  -                       capacity=1,
  -                       session_ref='cpu-local-session',
  -                       session_config_digest='sha256:fac2285a2f5b26154a33487645c5c155388d719ad1fafbf559a07c6d6aa9bf85',
  -                       output_root=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/outputs'),
  -                       credential_ref='/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/credentials/astrid-pack-host.token',
  -                       executor_id='astrid-pack-host',
  -                       boot_manifest_path=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/boot-manifest.json'),
  -                       boot_manifest_hash='sha256:1d3663c955249be0d394d4ee3f6ca441da09b9b4ebde361359ce7c257d218d00',
  -                       readiness_profile_path=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/profile.json'),
  -                       readiness_profile_hash='sha256:f78efb5e8d9c013c4683cbd71c4fd68f62a72428fb5357aab04976abbdd7ad67',
  -                       source_checkout=PosixPath('/home/runner/work/astrid-agent/astrid-agent'),
  -                       source_checkout_digest='633e0611bf1a8c2c1e03c7a8852fc832b1fc8aff76356abb45517f94fcfbc26a',
  -                       pack_roots=(
  -                                      PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/cpu-pack'),
  -                                  ),
  -                       source_inventory_identity='',
  -                       capability_matrix=None,
  -                       ready_file=PosixPath('/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/receiver.ready.json'),
  -                       execution_target={
  -                                            'id': 'runnervmccnms',
  -                                            'kind': 'machine',
  -                                        },
  -                       register=True,
  -                       admission_identity=AdmissionIdentity(
  -                                              task_id='a730be8141b544ba9ac734b0cab89a34',
  -                                              run_id='55c48293907042eda72c59c20d647fbb',
  -                                              project_id='3fcc5fb1048d41b38aa29787ef43a10c',
  -                                              idempotency_key='cpu-parked-receiver',
  -                                              admission_digest='sha256:6e1f743c1b1077e44b765b755ebe883739748f583fe1c46c60b82cba71d628e7',
  -                                              spec_digest='sha256:4037d077a7d9031dd7ccfab319dc1d8cf642a0759365f44ba067f9e7ae61b297',
  -                                              request_digest='sha256:d6b1fd91f59203b583a0e073c7754cc3c4f4c9917268446bf8747326cbcdf15b',
  -                                          ),
  -                       capability_identity=CapabilityIdentity(
  -                                               capability_id='cpu.activation',
  -                                               capability_digest='sha256:9129a43f1385feba216ed6bdd96750956b347ca1b1c8d90926c13a5340c194fe',
  -                                           ),
  -                       input_bindings=(),
  -                       original_target={
  -                                           'id': 'runnervmccnms',
  -                                           'kind': 'machine',
  -                                       },
  -                       effective_target={
  -                                            'id': 'runnervmccnms',
  -                                            'kind': 'machine',
  -                                        },
  -                       placement_version=0,
  -                       recovery_decision_digest=None,
  -                   ),
  -         state={
  -                   'boot_manifest_hash': '1d3663c955249be0d394d4ee3f6ca441da09b9b4ebde361359ce7c257d218d00',
  -                   'boot_manifest_path': '/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/boot-manifest.json',
  -                   'credential_file': '/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/credentials/astrid-pack-host.token',
  -                   'endpoint': 'http://127.0.0.1:36911',
  -                   'launch_argv_sha256': 'sha256:7493bf03d9589dab169f01a76a71dccd852286547c6f691d16b74975c741fe90',
  -                   'launch_native_identity': None,
  -                   'pid': 580839,
  -                   'process_birth_id': '4ddbca61-4e28-43ae-8936-75e55b6e30af:355502',
  -                   'ready_file': '/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/receiver.ready.json',
  -                   'source_checkout': '/home/runner/work/astrid-agent/astrid-agent',
  -                   'source_closure_digest': '936e0a01994d197afd6deda116a6b137ef96a040407b25bb3230471d05933c39',
  -                   'support_root': '/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime',
  -               },
  -         operation_id='cf639c72b5766031067227ca68c6c292',
  -         channel_id='5948be05e9cec2f356764becc146e967',
  -         grant_sent=True,
  -         grant={
  -                   'activation_id': 'c3ed3864e8644d899c360630e98a8ffe',
  -                   'credential_file': '/tmp/pytest-of-runner/pytest-0/test_precommit_failure_revokes0/data/runtime/credentials/astrid-pack-host.token',
  -                   'evidence_digest': 'sha256:198ba67c692278342ddd08055e03d9aca62dd6e2be5cc28061b48439546905a7',
  -                   'executor_incarnation': '443efaeeeea746dba7aec9256e218004',
  -               },
  -         cleanup_error=None,
  -         aborted=False,
  -         execution_profile='source',
  -         execution_origins={},
  -     ),
  - ]
```

IDs:
- `tests/integrations/test_generic_host_activation_acceptance.py::test_precommit_failure_revokes_before_stopping_exact_host[ready]`

### FAILED × 1

```text
AssertionError: assert [{'content_di...'version': 1}] == []
  
  Left contains one more item: {'content_digest': 'sha256:a459897d3aedd340963a5c2320d5df0f1ea0382fffcbf69ca93b539fbc0aa68b', 'document_id': 'transcript:89238a4191ef48bfae50f540289869fb73259020feea40bfb0b1063739d0623d', 'version': 1}
  
  Full diff:
  - []
  + [
  +     {
  +         'content_digest': 'sha256:a459897d3aedd340963a5c2320d5df0f1ea0382fffcbf69ca93b539fbc0aa68b',
  +         'document_id': 'transcript:89238a4191ef48bfae50f540289869fb73259020feea40bfb0b1063739d0623d',
  +         'version': 1,
  +     },
  + ]
```

IDs:
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_inverse_retains_surviving_opaque_transcript_pin[retained1-shot]`

### FAILED × 1

```text
AssertionError: assert {'job.stderr'... 'video/webm'} == {'marker': 'i... 'video/webm'}
  
  Omitting 2 identical items, use -vv to show
  Left contains 2 more items:
  {'job.stderr': 'text/plain', 'job.stdout': 'text/plain'}
  
  Full diff:
    {
  +     'job.stderr': 'text/plain',
  +     'job.stdout': 'text/plain',
        'marker': 'image/png',
        'marker_clip': 'video/webm',
    }
```

IDs:
- `tests/journeys/test_cross_client.py::test_marker_executor_registers_runs_once_and_settles_a_png`

### FAILED × 1

```text
AssertionError: this integration must use the running Python 3.12
assert (3, 11) == (3, 12)
  
  At index 1 diff: 11 != 12
  
  Full diff:
    (
        3,
  -     12,
  ?      ^
  +     11,
  ?      ^
    )
```

IDs:
- `tests/integrations/test_core_hivemind_installed.py::test_zero_source_installed_core_discovers_and_invokes_read_write_with_fake_http`

### FAILED × 1

```text
Failed: DID NOT RAISE <class 'OSError'>
```

IDs:
- `tests/integrations/test_generic_host_activation_acceptance.py::test_precommit_failure_revokes_before_stopping_exact_host[cleanup]`

### FAILED × 1

```text
Failed: DID NOT RAISE <class 'astrid.packs.vibecomfy.production_engine.ProductionEngineError'>
```

IDs:
- `tests/packs/h3_av/test_static_mask_preflight.py::test_generated_static_mask_staging_and_live_preflight[unbound_picker]`

### FAILED × 1

```text
KeyError: 'opaque_transcript'
```

IDs:
- `tests/editing_conformance/test_next_command_cohort_runtime.py::test_grouped_inverse_retains_surviving_opaque_transcript_pin[retained0-parent]`

### FAILED × 1

```text
KeyError: 'rows'
```

IDs:
- `tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo`

### FAILED × 1

```text
RuntimeError: H3 managed request import failed
```

IDs:
- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_managed_import_both_ports_use_valid_stable_distinct_keys_and_real_results`

### FAILED × 1

```text
SystemExit: 2
```

IDs:
- `tests/packs/h3_av/test_two_edit_cpu_qualification.py::test_two_edit_local_action_cpu_qualification`

### FAILED × 1

```text
assert '"ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES", str(4 * 1024**3)' in 'from __future__ import annotations\n\nimport json\nimport copy\nimport ctypes\nimport errno\nimport hashlib\nimport math\nfrom .dirfd import filesystem as os\nimport re\nimport sqlite3\nimport shutil\nimport stat\nimport sys\nimport tempfile\nimport threading\nimport time\nimport uuid\nimport unicodedata\nfrom collections import defaultdict\nfrom contextlib import contextmanager, nullcontext\nfrom datetime import datetime, timedelta, timezone\nfrom pathlib import Path\nfrom urllib.parse import unquote\n\nfrom . import platform\nfrom . import cancellation\nfrom .errors import CapabilityUnavailableError, ConflictError, InvalidRequestError, LeaseError, NotFoundError, OwnerBusyError, RealmAdmissionError, ValidationError\nfrom .canonical_schema import CANONICAL_FORMAT_ID, CANONICAL_SCHEMA_SQL\nfrom .cas import ContentAddressedStore\nfrom .dirfd import remove_tree_at, open_directory_chain\nfrom .snapshot_refs import check_working_copy_base, parent_revision_row, prepare_snapshot, publish_snapshot, rewrite_spec_snapshots, source_kind_of, validate_capture_scope, working_copy_binding\nfrom .sqlite_uri import sqlite_file_uri\nfrom .storage import free_disk_floor_bytes\nfrom .util import ca...herefore cannot be called broken.\n            if not row.get("activation_manifest"):\n                return {"status": "not_configured", "ok": True, "issues": []}\n            activation_path = Path(str(row.get("activation_manifest", "")))\n            if not activation_path.is_file():\n                raise FileNotFoundError\n            activation = json.loads(activation_path.read_text(encoding="utf-8"))\n            issues = []\n            if activation.get("realm_id") != self.realm["id"]: issues.append("activation_realm_mismatch")\n            if Path(str(activation.get("destination_realm_root", ""))).resolve() != self.root.resolve(): issues.append("activation_root_mismatch")\n            expected_digest = row.get("activation_digest")\n            if expected_digest and hashlib.sha256(activation_path.read_bytes()).hexdigest() != expected_digest: issues.append("activation_digest_mismatch")\n            return {"status": "ready" if not issues else "invalid", "ok": not issues, "issues": issues, "path": str(activation_path)}\n        except (OSError, StopIteration, json.JSONDecodeError):\n            return {"status": "invalid", "ok": False, "issues": ["activation_missing"]}\n'
```

IDs:
- `tests/journeys/test_journey_plumbing.py::test_the_default_floor_matches_the_runtime`

### FAILED × 1

```text
assert None is not None
```

IDs:
- `tests/integrations/test_generic_host_remotion_render.py::test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source`

### FAILED × 1

```text
assert {'accepted_pu...aseline', ...} == {'accepted_pu...aseline', ...}
  
  Omitting 20 identical items, use -vv to show
  Left contains 4 more items:
  {'confirmed': False,
   'replayed': False,
   'summary': 'Committed "Apply sheet" as txn-09ab7846546b4913976a11a05e08aa85.',
   'undo': {'publications': ['txn-09ab7846546b4913976a11a05e08aa85']}}
  
  Full diff:
    {
        'accepted_publication_id': 'txn-09ab7846546b4913976a11a05e08aa85',
        'accepted_revision_id': 'authoring-parent-revision-21daa518e39efba4ac8a9513995ace99c9a770d33a0f3e1874066d7e98750fc3',
        'base_publication_id': 'txn-24d74eb8996948008bc024940f4aa20c',
        'base_revision_id': 'p4-cli-sheet-baseline',
        'canonical_document': {
            'dependency_manifest': {
                'documents': [],
                'internal_timelines': [],
                'media': [],
                'shots': [],
            },
            'internal_timeline_revisions': [],
            'parent_revision': {
                'content_digest': 'sha256:9fe5035b41d55590a2dfdc98861fe3fbe2ddeaa2eb1b8f43d58e0fc7e5341070',
                'payload': {
                    'clips': [
                        {
                            'app': {
                                'astrid': {
                                    'fixed_start': True,
                                    'for': 1.0,
                                },
                            },
                            'at': 5.0,
                            'clipType': 'am-type',
                            'hold': 1,
                            'id': 'a',
                            'params': {
                                'text': 'café',
                            },
                            'track': 'picture',
                        },
                        {
                            'at': 0,
                            'clipType': 'am-type',
                            'hold': 1,
                            'id': 'b',
                            'params': {
                                'text': 'café',
                            },
                            'track': 'picture',
                        },
                    ],
                    'config': {
                        'output': {
                            'fps': 30,
                        },
                        'tracks': [
                            {
                                'id': 'picture',
                                'kind': 'visual',
                            },
                        ],
                    },
                    'occurrences': [],
                    'registry': {},
                },
                'revision_id': 'authoring-parent-revision-21daa518e39efba4ac8a9513995ace99c9a770d33a0f3e1874066d7e98750fc3',
            },
            'project_id': '2862e8240ca54c43a81b939ad0c52a16',
            'schema_version': 1,
            'shot_revisions': [],
            'timeline_id': 'film',
        },
        'commands': [
            {
                'args': {
                    'on': 5,
                },
                'authorship': {
                    'parent/clip:a::app': 'direct',
                    'parent/clip:a::app.astrid': 'direct',
                    'parent/clip:a::app.astrid.fixed_start': 'direct',
                    'parent/clip:a::app.astrid.for': 'direct',
                    'parent/clip:a::app.astrid.on': 'direct',
                    'parent/clip:a::app.astrid.until': 'direct',
                    'parent/clip:a::app.astrid.until_film_end': 'direct',
                    'parent/clip:a::app.on': 'direct',
                    'parent/clip:a::app.until': 'direct',
                    'parent/clip:a::app.until_film_end': 'direct',
                    'parent/clip:a::at': 'direct',
                },
                'bindings': {
                    'move.target': 'parent/clip:a',
                    'move.track': 'parent/track:picture',
                },
                'created': [],
                'expect': {
                    'parent/clip:a::app': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.astrid': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.astrid.fixed_start': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.astrid.for': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.astrid.on': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.astrid.until': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.astrid.until_film_end': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.on': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.until': {
                        'state': 'absent',
                    },
                    'parent/clip:a::app.until_film_end': {
                        'state': 'absent',
                    },
                    'parent/clip:a::at': {
                        'state': 'present',
                        'value': 0,
                    },
                },
                'intent': {
                    'anchor': 'fixed',
                    'position': 'absolute',
                    'ripple': 'none',
                },
                'op': 'clip.move',
                'reads': [
                    {
                        'path': [
                            'id',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'present',
                            'value': 'a',
                        },
                    },
                    {
                        'path': [
                            'at',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'present',
                            'value': 0,
                        },
                    },
                    {
                        'path': [
                            'at_ms',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'track',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'present',
                            'value': 'picture',
                        },
                    },
                    {
                        'path': [
                            'asset',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'asset_id',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'media_id',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'object_id',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'clipType',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'present',
                            'value': 'am-type',
                        },
                    },
                    {
                        'path': [
                            'clip_type',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'enabled',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'active',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'disabled',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'hidden',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'deleted',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'from',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'to',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'from_ms',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'to_ms',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'hold',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'present',
                            'value': 1,
                        },
                    },
                    {
                        'path': [
                            'duration',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'duration_ms',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'speed',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'time_map',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'timeMap',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'clips',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'children',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'on',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'fixed_start',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'until',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'until_film_end',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'for',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'cut',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'sequence',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'sequence_index',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'sequence_fit',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'orphan',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'formulas',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'on',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'fixed_start',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'until',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'until_film_end',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'for',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'cut',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'sequence',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'sequence_index',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'sequence_fit',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'orphan',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'app',
                            'astrid',
                            'formulas',
                        ],
                        'ref': 'parent/clip:a',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'id',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'present',
                            'value': 'picture',
                        },
                    },
                    {
                        'path': [
                            'kind',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'present',
                            'value': 'visual',
                        },
                    },
                    {
                        'path': [
                            'role',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'enabled',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'active',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'disabled',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'hidden',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'deleted',
                        ],
                        'ref': 'parent/track:picture',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'path': [
                            'config',
                            'output',
                            'fps',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 30,
                        },
                    },
                ],
                'resolved': [
                    'parent/clip:a',
                ],
                'schema_version': 1,
                'select': 'parent/clip:a',
                'selections': [
                    {
                        'boundaries': [
                            'parent/clip:a',
                        ],
                        'key': 'move.target',
                        'members': [
                            'parent/clip:a',
                        ],
                        'order': [
                            'parent/clip:a',
                        ],
                        'owner': 'parent',
                        'policy': 'guard-membership',
                        'query_version': 1,
                    },
                ],
                'version': '1',
            },
        ],
        'compiler_version': 'authoring-bundle-1',
  +     'confirmed': False,
        'document_digest': 'sha256:223782ee4f7354f00cf6eba0bf990986481473b6bc5e9026672d8ca3b678381f',
        'id_map': {},
        'label': 'Apply sheet',
        'merge_mode': 'fields',
        'previous_publication_id': 'txn-24d74eb8996948008bc024940f4aa20c',
        'previous_revision_id': 'p4-cli-sheet-baseline',
        'provider_version': 'astrid-v1',
        'publisher': 'owner',
        'rebased_onto': None,
  +     'replayed': False,
        'show_command': 'astrid timelines show film --project 2862e8240ca54c43a81b939ad0c52a16 '
        '--published --revision-id '
        'authoring-parent-revision-21daa518e39efba4ac8a9513995ace99c9a770d33a0f3e1874066d7e98750fc3',
        'source': {
            'via': 'sheet',
        },
        'status': 'accepted',
        'steps': [
            {
                'command_ordinals': [
                    0,
                ],
                'dependencies': [
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'id',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 'a',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'at',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 0,
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'at_ms',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'track',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 'picture',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'asset',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'asset_id',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'media_id',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'object_id',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'clipType',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 'am-type',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'clip_type',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'enabled',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'active',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'disabled',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'hidden',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'deleted',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'from',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'to',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'from_ms',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'to_ms',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'hold',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 1,
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'duration',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'duration_ms',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'speed',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'time_map',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'timeMap',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'clips',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'children',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'on',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'fixed_start',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'until',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'until_film_end',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'for',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'cut',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'sequence',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'sequence_index',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'sequence_fit',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'orphan',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'formulas',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'on',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'fixed_start',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'until',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'until_film_end',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'for',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'cut',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'sequence',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'sequence_index',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'sequence_fit',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'orphan',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                            'astrid',
                            'formulas',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'id',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 'picture',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'kind',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 'visual',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'role',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'enabled',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'active',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'disabled',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'hidden',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'tracks',
                            'id:picture',
                            'deleted',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'absent',
                        },
                    },
                    {
                        'kind': 'field',
                        'path': [
                            'config',
                            'output',
                            'fps',
                        ],
                        'ref': 'parent',
                        'state': {
                            'state': 'present',
                            'value': 30,
                        },
                    },
                ],
                'id': 'sheet-1',
                'intent': '',
                'label': 'Apply sheet',
                'patch': [
                    {
                        'before': {
                            'state': 'absent',
                        },
                        'op': 'set',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'app',
                        ],
                        'ref': 'parent',
                        'value': {
                            'astrid': {
                                'fixed_start': True,
                                'for': 1.0,
                            },
                        },
                    },
                    {
                        'before': {
                            'state': 'present',
                            'value': 0,
                        },
                        'op': 'set',
                        'path': [
                            'config',
                            'clips',
                            'id:a',
                            'at',
                        ],
                        'ref': 'parent',
                        'value': 5.0,
                    },
                ],
                'tags': [
                    'sheet',
                ],
            },
        ],
  +     'summary': 'Committed "Apply sheet" as txn-09ab7846546b4913976a11a05e08aa85.',
  +     'undo': {
  +         'publications': [
  +             'txn-09ab7846546b4913976a11a05e08aa85',
  +         ],
  +     },
    }
```

IDs:
- `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_production_i2i_rejects_ex0/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_production_i2i_rejects_extra_or_misordered_single_cas_inputs`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_image_executor0/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_image_executor_consumes_cas_image_and_cleans_attempt[generate_image-generation.generate_image-flux-dev-t2i-None]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_image_executor1/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_image_executor_consumes_cas_image_and_cleans_attempt[generate_image-generation.generate_image-flux-dev-t2i-0]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_image_executor2/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_image_executor_consumes_cas_image_and_cleans_attempt[generate_image-generation.generate_image-flux-dev-t2i-1]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_image_executor3/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_image_executor_consumes_cas_image_and_cleans_attempt[generate_image_cloud_i2i-generation.generate_image_cloud_i2i-z-image-i2i-None]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_image_executor4/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_image_executor_consumes_cas_image_and_cleans_attempt[generate_image_edit-generation.generate_image_edit-qwen-image-edit-2511-edit-None]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_qwen_edit_fail0/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_qwen_edit_failure_is_terminal_and_does_not_settle[oversized_input]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_qwen_edit_fail1/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_qwen_edit_failure_is_terminal_and_does_not_settle[oversized_output]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_qwen_edit_fail2/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_qwen_edit_failure_is_terminal_and_does_not_settle[scope]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_registered_qwen_edit_fail3/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_registered_qwen_edit_failure_is_terminal_and_does_not_settle[estimate]`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'generation': pack 'generation' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_typed_image_admission_cro0/generation and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/generation
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_typed_image_admission_crosses_runtime_host_and_cas`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'vibecomfy': pack 'vibecomfy' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_typed_character_animation0/vibecomfy and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/vibecomfy
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_typed_character_animation_admission_consumes_ordered_cas_and_readback`

### FAILED × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'vibecomfy': pack 'vibecomfy' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_typed_video_enhance_admis0/vibecomfy and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/vibecomfy
```

IDs:
- `tests/integrations/test_generation_runtime_composition.py::test_typed_video_enhance_admission_settles_variant_and_readback`

### FAILED × 1

```text
astrid.core.rendering.errors.RendererUnsupportedError: rendering.remotion does not support this render request
```

IDs:
- `tests/packs/rendering/test_hyperframes_backend.py::test_hyperframes_remotion_combined_render`

### FAILED × 1

```text
astrid.packs.rendering.actions.render.task_adapter.RenderExportRefused: render_export executor failed: executor exited with returncode 1
```

IDs:
- `tests/packs/rendering/test_render_export_task_adapter.py::test_forced_caption_uses_server_owned_executable_routing_and_isolation`

### FAILED × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_interrupted_upload_reconc0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_interrupted_upload_reconciles_remote_bytes_without_reupload`

### FAILED × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/workflow/workflow.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_materialized_h3_bundle_st0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_materialized_h3_bundle_stages_as_an_owned_workflow_root`

### FAILED × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_preparation_runs_real_chi0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_preparation_runs_real_child_probe_and_reuses_verified_content`

### FAILED × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_remote_drift_fails_closed0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_remote_drift_fails_closed_then_explicit_refresh_repairs_owned_source`

### FAILED × 1

```text
astrid.sdk.timeline.compiler.TimingCompileError: invalid timing input: the parent holds two different clip lists (clips and config.clips)
```

IDs:
- `tests/editing_conformance/test_word_binding_recipe.py::test_unique_legacy_word_compiles_without_persisting_a_reference`

### FAILED × 1

```text
astrid.sdk.timeline.sync.CommitConflict: The timeline changed since this edit was made; nothing was committed. function rerun overlaps an intervening write. Someone else changed this timeline after your edit was made, so "append_review_suffix" was not committed. Your edit is saved as pc_a60d01a83cd4; nothing is lost. Retry it with tl.retry("pc_a60d01a83cd4", your_function).
```

IDs:
- `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document`

### FAILED × 1

```text
runtime_protocol.errors.ConflictError: remote activation may have admitted work; reconcile before cleanup
```

IDs:
- `tests/integrations/test_generic_host_activation_acceptance.py::test_bootstrap_register_observe_commit_and_same_incarnation_recovery[True]`

### FAILED × 1

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage timeline effects differ from authenticated source history
```

IDs:
- `tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`

### FAILED × 1

```text
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/astrid-runtime-archive-n06z_a2s', 'rev-parse', 'HEAD']' returned non-zero exit status 128.
```

IDs:
- `tests/integrations/test_runpod_cpu_path.py::test_cpu_runpod_http_journey`

## G1 and Plan 38/55 triage

The frozen G1 Lanes shard 3 job 133451219876 was still running at the saved G1 snapshot and its full log is unavailable. Current exact testcase IDs were compared against the other saved G1 red-ID ledgers; none matched. Unmatched IDs are not called new regressions or prior passes. Plan 38 and Plan 55 have no exact matched testcase ownership in the inspected task documents/audited rows; both remain WAITING/unassigned. No ownership is inferred from path or test family.

Exact matches to available prior G1 red IDs: 0. Current failure/error IDs without an exact match to those available rows: 143; these remain unevaluable against the unavailable old G1 shard 3 result.
