# opt-in (job 133536534262)

Counts: `{'FAILED': 12, 'ERROR': 0, 'PASSED': 0, 'SKIPPED': 0}`. Run-level state was `in_progress`; this is partial diagnostic evidence, not G2 acceptance.

No XML artifact was produced. IDs and one-line messages are from the raw pytest summary; full traceback/assertion detail is not preserved by that summary.

Outer pytest summary:
```text
12 failed, 19 passed, 31261 deselected, 2 warnings in 137.00s (0:02:16)
```

## Failure and error groups

The table uses exact XML `message` attributes, with all testcase IDs for each literal message. Full XML testcase `detail` is retained losslessly in the JSON records.

### Failure × 6

```text
Failed: provide the saved actual public C06 frame-index artifact for affected readback replay
```

IDs:
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[None]`
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[sidecar-bytes]`
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[saved-revision]`
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[requested-frame]`
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[render-digest]`
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[sidecar-path]`

### Failure × 5

```text
astrid.sdk.exceptions.CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge
```

IDs:
- `tests/test_onboarding_parity.py::test_editorial_arrange_is_inspectable_via_get_capability`
- `tests/test_onboarding_parity.py::test_editorial_arrange_handle_has_provenance`
- `tests/test_onboarding_parity.py::test_editorial_arrange_handle_has_safety_declaration`
- `tests/test_onboarding_parity.py::test_capability_schema_is_json_serializable`
- `tests/test_onboarding_parity.py::test_provenance_is_populated_on_editorial_arrange`

### Failure × 1

```text
AssertionError: editorial.arrange not found in discovery. Executor ids: ['generation.generate_audio', 'generation.generate_image', 'generation.generate_image_cloud_i2i', 'generation.generate_image_codex', 'generation.generate_image_edit', 'generation.generate_image_openai', 'generation.generate_image_upscale', 'generation.generate_speech', 'generation.generate_video', 'hivemind.contribute', 'hivemind.get_item', 'hivemind.ingest_article', 'hivemind.ingest_workflow', 'hivemind.ingest_youtube', 'hivemind.refresh_media', 'hivemind.search', 'rendering.assemble_timeline', 'rendering.html_canvas_effect', 'rendering.render', 'rendering.sprite_sheet', 'rendering.timeline_export_plan', 'rendering.timeline_prepare_import', 'rendering.timeline_storyboard', 'runpod.claim', 'runpod.exec', 'runpod.keep', 'runpod.ls', 'runpod.provision', 'runpod.pull', 'runpod.release', 'runpod.session', 'runpod.setup', 'runpod.status', 'runpod.teardown', 'training.dataset_build', 'training.pool_build', 'training.pool_merge', 'training.search_loras', 'training.training_run', 'vibecomfy.character_animation', 'vibecomfy.edit', 'vibecomfy.import', 'vibecomfy.inspect', 'vibecomfy.run', 'vibecomfy.validate', 'vibecomfy.video_enhance', 'wan2gp.generate_video', 'wan2gp.validate_settings']
```

IDs:
- `tests/test_onboarding_parity.py::test_editorial_arrange_is_discoverable_via_discover`

## G1 and Plan 38/55 triage

Exact testcase IDs only are counted as G1 recurrences. Parameter-family matches, if any, are separately retained in `prior_g1_similar_test_ids_not_exact` and do not count as recurrence. The saved G1 integration-2 and late integration-4 ledgers contain red testcase IDs, not a complete all-pass baseline; a current red ID absent there is not thereby proven new or previously passing.

**G1 red-ID transition summary:** prior exact red IDs `12`; current red IDs with exact prior red ID `12`; current red IDs absent from prior red inventory `0`. Prior-to-current transitions: `{"failed_persists_same_status": 12}`.

## Prior failure/error to current outcome transitions

| Prior G1 status | Current status | Count |
|---|---|---:|
| FAILED | FAILED | 12 |

## Current failure/error IDs: prior mapping and plan holds

- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[None]` — Exact G1 recurrence. Failed: provide the saved actual public C06 frame-index artifact for affected readback replay Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[sidecar-bytes]` — Exact G1 recurrence. Failed: provide the saved actual public C06 frame-index artifact for affected readback replay Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[saved-revision]` — Exact G1 recurrence. Failed: provide the saved actual public C06 frame-index artifact for affected readback replay Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[requested-frame]` — Exact G1 recurrence. Failed: provide the saved actual public C06 frame-index artifact for affected readback replay Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[render-digest]` — Exact G1 recurrence. Failed: provide the saved actual public C06 frame-index artifact for affected readback replay Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/integrations/test_c06_public_timeline_visualizer.py::test_saved_actual_filmstrip_v2_composed_capture_readback[sidecar-path]` — Exact G1 recurrence. Failed: provide the saved actual public C06 frame-index artifact for affected readback replay Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/test_onboarding_parity.py::test_editorial_arrange_is_discoverable_via_discover` — Exact G1 recurrence. AssertionError: editorial.arrange not found in discovery. Executor ids: ['generation.generate_audio', 'generation.generate_image', 'generation.generate_image_cloud_i2i', 'generation.generate_image_codex', 'generation.generate_image_edit', 'generation.generate_image_openai', 'generation.generate_image_upscale', 'generation.generate_speech', 'generation.generate_video', 'hivemind.contribute', 'hivemind.get_item', 'hivemind.ingest_article', 'hivemind.ingest_workflow', 'hivemind.ingest_youtube', 'hivemind.refresh_media', 'hivemind.search', 'rendering.assemble_timeline', 'rendering.html_canvas_effect', 'rendering.render', 'rendering.sprite_sheet', 'rendering.timeline_export_plan', 'rendering.timeline_prepare_import', 'rendering.timeline_storyboard', 'runpod.claim', 'runpod.exec', 'runpod.keep', 'runpod.ls', 'runpod.provision', 'runpod.pull', 'runpod.release', 'runpod.session', 'runpod.setup', 'runpod.status', 'runpod.teardown', 'training.dataset_build', 'training.pool_build', 'training.pool_merge', 'training.search_loras', 'training.training_run', 'vibecomfy.character_animation', 'vibecomfy.edit', 'vibecomfy.import', 'vibecomfy.inspect', 'vibecomfy.run', 'vibecomfy.validate', 'vibecomfy.video_enhance', 'wan2gp.generate_video', 'wan2gp.validate_settings'] Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/test_onboarding_parity.py::test_editorial_arrange_is_inspectable_via_get_capability` — Exact G1 recurrence. astrid.sdk.exceptions.CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/test_onboarding_parity.py::test_editorial_arrange_handle_has_provenance` — Exact G1 recurrence. astrid.sdk.exceptions.CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/test_onboarding_parity.py::test_editorial_arrange_handle_has_safety_declaration` — Exact G1 recurrence. astrid.sdk.exceptions.CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/test_onboarding_parity.py::test_capability_schema_is_json_serializable` — Exact G1 recurrence. astrid.sdk.exceptions.CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
- `tests/test_onboarding_parity.py::test_provenance_is_populated_on_editorial_arrange` — Exact G1 recurrence. astrid.sdk.exceptions.CapabilityNotFoundError: unknown executor 'editorial.arrange'; nearest matches: executor:training.pool_merge Plan 38: No Plan 38 match unless explicit mapping in G1 row; inspect prior inventory; Plan 55: No Plan 55 match unless explicit mapping in G1 row; inspect prior inventory.
