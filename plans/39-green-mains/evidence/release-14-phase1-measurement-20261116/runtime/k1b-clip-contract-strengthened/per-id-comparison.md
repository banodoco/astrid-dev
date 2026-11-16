# Per-ID proof comparison

Baseline: partial port (25 passed / 2 failed). Intermediate: strengthening proof-a.patch (19 passed / 8 failed). Final: candidate.patch (25 passed / 2 failed).

| Node ID | Baseline | Intermediate | Final |
| --- | --- | --- | --- |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_is_atomic_cas_and_exactly_replayable` | FAIL | FAIL | FAIL |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rebases_after_disjoint_intervening_edit` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_parent_clip_swap_route_refuses_parent_ownership_on_public013_schema` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_parent_clip_swap_route_replaces_parent_media` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_cross_project_source_without_mutation` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_malformed_source_before_native_commit` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_tampered_cas_without_mutation` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_wrong_stream_without_mutation` | PASS | FAIL | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_too_short_or_end_short_source[1]` | PASS | FAIL | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_too_short_or_end_short_source[3.5]` | PASS | FAIL | PASS |
| `tests.test_timeline_clip_replacement::test_native_generic_visual_media_requires_video_stream` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_generic_visual_media_accepts_verified_image_swap` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_replays_after_intervening_edit_and_reopen` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_rt02_project_shot_crud_native_replacement_retries_after_restart` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_rt02_native_occurrence_swap_rolls_back_before_restart_retry` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_public_http_route` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable` | FAIL | FAIL | FAIL |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_cross_project_source` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_malformed_source_without_mutation` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_tampered_cas_without_mutation` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_wrong_stream_without_mutation` | PASS | FAIL | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_too_short_source_without_mutation` | PASS | FAIL | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_requires_source_to_reach_authored_end` | PASS | FAIL | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_generic_visual_media_requires_video_stream` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_replays_after_intervening_edit_and_reopen` | PASS | PASS | PASS |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_public_http_route` | PASS | PASS | PASS |
