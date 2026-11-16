# integration-1 (job 133536534579)

Counts: `{'PASSED': 480, 'FAILED': 36, 'ERROR': 0, 'SKIPPED': 0}`. Run-level state was `in_progress`; this is partial diagnostic evidence, not G2 acceptance.

XML artifact `14260249942`; ZIP SHA-256 `6b06eefdf363ea5c58c5f0aa38021179f133bced9b9da0c8ec8e66905d2b8aca`. XML carries full testcase failure/error payloads.

Outer pytest summary:
```text
== 36 failed, 480 passed, 32170 deselected, 13 warnings in 714.71s (0:11:54) ===
```

## Failure and error groups

The table uses exact XML `message` attributes, with all testcase IDs for each literal message. Full XML testcase `detail` is retained losslessly in the JSON records.

### Failure × 21

```text
KeyError: 'bridge.parent'
```

IDs:
- `tests/core/execution/test_openai_child_admission.py::test_openai_t2i_one_admitted_task_binds_frozen_outputs_and_replays`
- `tests/core/execution/test_openai_child_admission.py::test_openai_jsonl_and_ordered_edit_refs_are_retained_before_binding_and_upload`
- `tests/core/execution/test_openai_child_admission.py::test_openai_authenticated_managed_jsonl_and_ref_order_reach_real_materialization`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[malformed-jsonl]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[duplicate-key]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[too-many-outputs]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[oversized-jsonl]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[bad-image]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[oversized-image]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[missing-producer]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[unsafe-producer]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[wrong-provider]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[undelegated]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[unauthorized]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[wrong-hash]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[oversized]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[malformed]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit0]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit1]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit2]`
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit3]`

### Failure × 8

```text
RuntimeError: process control is already sandbox; refusing to change it to strict
```

IDs:
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[matching-selected-action]`
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[matching-legacy-executor]`
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[modified-selected-action]`
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[modified-legacy-executor]`
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[final-read-write-selected-action]`
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[final-read-write-legacy-executor]`
- `tests/core/generation/test_generate_target_journey.py::test_public_image_command_registers_view_bytes_and_canonical_receipt[catalog]`
- `tests/core/generation/test_generate_target_journey.py::test_public_image_command_registers_view_bytes_and_canonical_receipt[saved]`

### Failure × 5

```text
astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch
```

IDs:
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[interactive]`
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[absolute_cap]`
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[finite_timeout]`
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[cancel]`
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[heartbeat]`

### Failure × 1

```text
AssertionError: Regex pattern did not match.
  Expected regex: 'evidence cap'
  Actual message: 'delegated child spec lacks admitted_source_digest; refusing before launch'
```

IDs:
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[evidence]`

### Failure × 1

```text
ModuleNotFoundError: No module named 'tests.core.test_action_cli_clip_rehearsal'
```

IDs:
- `tests/core/generation/test_engine_custody.py::test_two_full_h3_runtime_runs_reuse_owned_native_service[outer]`

## G1 and Plan 38/55 triage

Exact testcase IDs only are counted as G1 recurrences. Parameter-family matches, if any, are separately retained in `prior_g1_similar_test_ids_not_exact` and do not count as recurrence. The saved G1 integration-2 and late integration-4 ledgers contain red testcase IDs, not a complete all-pass baseline; a current red ID absent there is not thereby proven new or previously passing.

**G1 red-ID transition summary:** prior exact red IDs `36`; current red IDs with exact prior red ID `36`; current red IDs absent from prior red inventory `0`. Prior-to-current transitions: `{"failed_persists_same_status": 36}`.

## Prior failure/error to current outcome transitions

| Prior G1 status | Current status | Count |
|---|---|---:|
| FAILED | FAILED | 36 |

## Current failure/error IDs: prior mapping and plan holds

- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[interactive]` — Exact G1 recurrence. astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[absolute_cap]` — Exact G1 recurrence. astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[finite_timeout]` — Exact G1 recurrence. astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[cancel]` — Exact G1 recurrence. astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[evidence]` — Exact G1 recurrence. AssertionError: Regex pattern did not match. Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_generic_host_child_bridge_d18.py::test_f05_host_execution_uses_one_lifetime_through_collection[heartbeat]` — Exact G1 recurrence. astrid.core.execution.generic_host.HostError: delegated child spec lacks admitted_source_digest; refusing before launch Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[matching-selected-action]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[matching-legacy-executor]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[modified-selected-action]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[modified-legacy-executor]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[final-read-write-selected-action]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/execution/test_m1_13_pack_provenance.py::test_production_cli_runtime_capture_composition[final-read-write-legacy-executor]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/execution/test_openai_child_admission.py::test_openai_t2i_one_admitted_task_binds_frozen_outputs_and_replays` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_jsonl_and_ordered_edit_refs_are_retained_before_binding_and_upload` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_authenticated_managed_jsonl_and_ref_order_reach_real_materialization` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[malformed-jsonl]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[duplicate-key]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[too-many-outputs]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[oversized-jsonl]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[bad-image]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[oversized-image]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[missing-producer]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[unsafe-producer]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[wrong-provider]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_invalid_producer_request_never_binds_uploads_or_admits[undelegated]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[unauthorized]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[wrong-hash]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[oversized]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_managed_jsonl_custody_refusal_precedes_binding_and_mutation[malformed]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit0]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit1]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit2]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/execution/test_openai_child_admission.py::test_openai_existing_child_limits_refuse_before_upload_or_admission[limit3]` — Exact G1 recurrence. KeyError: 'bridge.parent' Plan 38: No exact Plan 38 ownership match; Plan 55: Plan 55 owned; WAITING.
- `tests/core/generation/test_engine_custody.py::test_two_full_h3_runtime_runs_reuse_owned_native_service[outer]` — Exact G1 recurrence. ModuleNotFoundError: No module named 'tests.core.test_action_cli_clip_rehearsal' Plan 38: No assignment; WAITING owner classification; Plan 55: No assignment; WAITING owner classification.
- `tests/core/generation/test_generate_target_journey.py::test_public_image_command_registers_view_bytes_and_canonical_receipt[catalog]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
- `tests/core/generation/test_generate_target_journey.py::test_public_image_command_registers_view_bytes_and_canonical_receipt[saved]` — Exact G1 recurrence. RuntimeError: process control is already sandbox; refusing to change it to strict Plan 38: No exact Plan 38 inventory match; Plan 55: No exact Plan 55 inventory match.
