# Fresh CI run 44447425471, shard 3

Compared candidate job 135302866188 against the **union** of baseline run 44378598394 shards 1–8, keyed by pytest node ID. This accounts for shard movement. Extraction counts only top-level pytest short-summary `FAILED` and `ERROR` records, not traceback or nested diagnostic text.

| Status | Fresh shard 3 | Baseline union | Fresh IDs present in baseline | Fresh-only |
|---|---:|---:|---:|---:|
| FAILED | 31 | 837 | 31 | 0 |
| ERROR | 0 | 397 | 0 | 0 |

## Count reconciliation

Candidate short summary: **31 failed, 1909 passed, 30031 deselected**, 2 warnings. The extracted count is 31 unique `FAILED` node IDs and 0 `ERROR` node IDs; the 31 failures match the summary and there were no summary errors. Baseline event-record totals deduplicate by node ID across shards; each fresh failed ID is checked against that full union.

## Candidate-only assessment

None. All 31 fresh `FAILED` IDs occur in at least one baseline shard by exact node ID; there are no fresh `ERROR` IDs. There are no candidate-only traces to attribute using Plan 39 evidence or SR3 logs, and no cause is inferred from symptom similarity.

## Exact fresh IDs

### FAILED (31)

- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_authentic_complete_abi1_binding_set_survives_history_and_inverse`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_authenticated_history_abi_preserves_original_fork_proofs[1-False]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_authenticated_history_abi_preserves_original_fork_proofs[absent-False]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_caller_annotations_and_recorder_schema_do_not_supply_history_abi`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[0]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[1.0]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[1]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[2.0]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[2]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[3]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[False]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[None]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[True]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[metadata10]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[metadata11]`
- `tests/editing_conformance/test_fork_abi1_binding_set.py::test_malformed_authenticated_recorder_abi_fails_closed[metadata9]`
- `tests/editing_conformance/test_fork_historical_source_boundary.py::test_production_undo_authenticates_restored_source_without_changing_publication[False-1]`
- `tests/editing_conformance/test_fork_historical_source_boundary.py::test_production_undo_authenticates_restored_source_without_changing_publication[True-1]`
- `tests/editing_conformance/test_headless_root_mirror_effects.py::test_config_replacement_retains_real_root_mirror_removal[False]`
- `tests/editing_conformance/test_headless_root_mirror_effects.py::test_config_replacement_retains_real_root_mirror_removal[True]`
- `tests/editing_conformance/test_native_word_anchor_vectors.py::test_portable_native_captures[a]`
- `tests/editing_conformance/test_native_word_anchor_vectors.py::test_portable_native_captures[b]`
- `tests/editing_conformance/test_occurrence_shared_d20.py::test_provider_full_closure_preview_retry_inverse[1]`
- `tests/editing_conformance/test_prepared_video_birth.py::test_frozen_request_envelope_rejects_unknown_fields[idempotency_key]`
- `tests/editing_conformance/test_prepared_video_birth.py::test_frozen_request_envelope_rejects_unknown_fields[unexpected]`
- `tests/editing_conformance/test_prepared_video_birth.py::test_literal_after_insert_request_is_identical_on_c36_and_new`
- `tests/editing_conformance/test_prepared_video_birth.py::test_normalized_production_video_birth_and_guarded_inverse[0.02]`
- `tests/editing_conformance/test_prepared_video_birth.py::test_normalized_production_video_birth_and_guarded_inverse[4]`
- `tests/editing_conformance/test_prepared_video_birth.py::test_normalized_production_video_birth_and_guarded_inverse[None]`
- `tests/editing_conformance/test_prepared_video_birth.py::test_normalized_production_video_birth_and_guarded_inverse[absent]`
- `tests/editing_conformance/test_producer_insertion.py::test_native_parent_media_golden_is_the_exported_capture`

### ERROR (0)

None.

## Limitations

This comparison classifies only pytest `FAILED`/`ERROR` records present in the supplied logs. Baseline status sets are the exact union over shards 1–8; shard-level event counts are recorded in the JSON. A matching prior node ID establishes that the same test failed before, not that the underlying cause is unchanged.
