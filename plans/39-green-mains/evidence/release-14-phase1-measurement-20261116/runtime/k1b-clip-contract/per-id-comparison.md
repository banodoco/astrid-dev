# Clip test outcomes

| Test ID | Before | After |
|---|---|---|
| `tests.test_timeline_clip_replacement::test_native_clip_swap_is_atomic_cas_and_exactly_replayable` | failed | failed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_public_http_route` | failed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rebases_after_disjoint_intervening_edit` | failed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_cross_project_source_without_mutation` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_malformed_source_before_native_commit` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept` | failed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_tampered_cas_without_mutation` | failed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_too_short_or_end_short_source[1]` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_too_short_or_end_short_source[3.5]` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_rejects_wrong_stream_without_mutation` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_clip_swap_replays_after_intervening_edit_and_reopen` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_generic_visual_media_accepts_verified_image_swap` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_generic_visual_media_requires_video_stream` | failed | passed |
| `tests.test_timeline_clip_replacement::test_native_parent_clip_swap_route_refuses_parent_ownership_on_public013_schema` | passed | passed |
| `tests.test_timeline_clip_replacement::test_native_parent_clip_swap_route_replaces_parent_media` | passed | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_generic_visual_media_requires_video_stream` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable` | xfail/skip | failed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_public_http_route` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_cross_project_source` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_malformed_source_without_mutation` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_tampered_cas_without_mutation` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_too_short_source_without_mutation` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_rejects_wrong_stream_without_mutation` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_replays_after_intervening_edit_and_reopen` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_replace_timeline_clip_requires_source_to_reach_authored_end` | xfail/skip | passed |
| `tests.test_timeline_clip_replacement::test_rt02_native_occurrence_swap_rolls_back_before_restart_retry` | passed | passed |
| `tests.test_timeline_clip_replacement::test_rt02_project_shot_crud_native_replacement_retries_after_restart` | passed | passed |
