# integration-4 (job 133536534794)

Counts: `{'PASSED': 391, 'FAILED': 99, 'ERROR': 26, 'SKIPPED': 0}`. Run-level state was `in_progress`; this is partial diagnostic evidence, not G2 acceptance.

XML artifact `14267875745`; ZIP SHA-256 `c97a656b6ee543f27b1da45360a0a0c49659fa7ee41b019cbccbc446eefbab81`. XML carries full testcase failure/error payloads.

Outer pytest summary:
```text
= 99 failed, 391 passed, 32170 deselected, 9 warnings, 26 errors in 4830.29s (1:20:30) =
```

## Failure and error groups

Groups use exact XML `message` attributes; complete testcase IDs are retained. Full XML testcase `detail` is losslessly available in JSON records.

### Failure × 14

```text
Failed: Timeout (>120.0s) from pytest-timeout.
```

IDs:
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[stopped-backend]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[stopped-local]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[running-backend]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[running-local]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[incapable-retained-runtime]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[unrelated-retained-runtime]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[incapable-candidate-runtime]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[unrelated-candidate-runtime]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[missing-stop-marker]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[malformed-stop-marker]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[unknown-stop-binding]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[add-local-two-stop-build]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[midstop-crash-after-stop]`
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[midstop-crash-during-term]`

### Failure × 12

```text
runtime_protocol.errors.RuntimeErrorBase: selected PARAM authority is unavailable
```

IDs:
- `tests/sdk/test_element_inverse_source_retention.py::test_inverse_loads_original_object_after_readmission_and_restart`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[2-2.0]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[1-True]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[True-1]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[2-2]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[2.0-2.0]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[True-True]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_original_value_guards_keep_numeric_equivalence_and_bool_distinction[2-2.0-True]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_original_value_guards_keep_numeric_equivalence_and_bool_distinction[1-True-False]`
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_original_value_guards_keep_numeric_equivalence_and_bool_distinction[True-1-False]`
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_mixed_pack_readmission_keeps_old_and_new_native_param_sources`
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_equal_json_opposite_selection_order_and_inverse_restore`

### Failure × 9

```text
failed on setup with "IndexError: list index out of range"
```

IDs:
- `tests/sdk/test_timeline_capture_projection.py::test_real_saved_projection_config_registry_and_full_pins_golden`
- `tests/sdk/test_timeline_capture_projection.py::test_real_saved_entire_expansion_golden`
- `tests/sdk/test_timeline_capture_projection.py::test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows`
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[parent]`
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[child]`
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[new_shot]`
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[duplicate]`
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[remove]`
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[sdk_bundle]`

### Failure × 9

```text
failed on setup with "subprocess.CalledProcessError: Command '['git', '-C', '/home/runner/work/astrid-agent/astrid-agent/astrid-runtime', 'archive', '6d53a19070faf63fc15ae1f81417722edc2c8a5f']' returned non-zero exit status 128."
```

IDs:
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-none]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-create]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-claim]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-heartbeat]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-output]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-nonzero]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-timeout]`
- `tests/upgrade/test_busy_fixture_creation.py::test_release_rolls_back_partial_settlement[6d53a19070faf63fc15ae1f81417722edc2c8a5f]`
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_error_remains_primary_and_retry_reconciles[6d53a19070faf63fc15ae1f81417722edc2c8a5f]`

### Failure × 6

```text
astrid.installer.core.RuntimeOperationError: Runtime Pinokio interruption refused: no owner or completed-stop evidence.
```

IDs:
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[stopping-backend-current]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[candidate_ready-backend-current]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-backend-current]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-local-current]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[switched-backend-current]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[before_owner-backend-current]`

### Failure × 6

```text
astrid.installer.core.RuntimeOperationError: Runtime interruption refused: owner endpoint or process identity failed validation.
```

IDs:
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[stopping-backend-retained]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[candidate_ready-backend-retained]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-backend-retained]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-local-retained]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[switched-backend-retained]`
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[before_owner-backend-retained]`

### Failure × 5

```text
astrid.core.rendering.errors.RendererProtocolError: audio preparation requires the managed asset server
```

IDs:
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[media-only]`
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[effect-clip]`
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[text-card]`
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[audio-reactive-colour]`
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[transition-windows]`

### Failure × 4

```text
Failed: set ASTRID_RUNTIME_REPO to the local source checkout to run this offline check
```

IDs:
- `tests/upgrade/test_upgrade_release.py::test_guard_accepts_authoritative_source_shapes`
- `tests/upgrade/test_upgrade_release.py::test_production_source_format_change_requires_release_review[runtime_protocol/store.py-SCHEMA_VERSION = 31-SCHEMA_VERSION = 32-runtime]`
- `tests/upgrade/test_upgrade_release.py::test_production_source_format_change_requires_release_review[runtime_protocol/service.py-journal.get("version") != 1-journal.get("version") != 2-runtime]`
- `tests/upgrade/test_upgrade_release.py::test_production_source_format_change_requires_release_review[astrid/installer/core.py-"identity": {"release": self.release, "managed_by": self.managed_by}-"identity": {"release": self.release, "managed_by": self.managed_by}, "format": 2-agent]`

### Failure × 4

```text
failed on setup with "AssertionError: missing qualified authentic G5 archive: /home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz"
```

IDs:
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_checkout_reload_undo_cli_redo_uses_retained_history`
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images`
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_retained_restore_does_not_reopen_consumed_draft_steps`
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore`

### Failure × 3

```text
AssertionError: assert [{'blendMode'...'audio', ...}] == []
  
  Left contains 2 more items, first extra item: {'blendMode': 'normal', 'fit': 'contain', 'id': 'V1', 'kind': 'visual', ...}
  
  Full diff:
  - []
  + [
  +     {
  +         'blendMode': 'normal',
  +         'fit': 'contain',
  +         'id': 'V1',
  +         'kind': 'visual',
  +         'label': 'V1',
  +         'opacity': 1,
  +         'scale': 1,
  +     },
  +     {
  +         'blendMode': 'normal',
  +         'fit': 'contain',
  +         'id': 'A1',
  +         'kind': 'audio',
  +         'label': 'A1',
  +         'opacity': 1,
  +         'scale': 1,
  +     },
  + ]
```

IDs:
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_structural_reservations_and_receipt_retry_survive_runtime_restart`
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_restore_inverse_redo_and_exact_retry_survive_runtime_restart`
- `tests/sdk/test_timeline_legacy_inverse_bindings.py::test_legacy_producer_forward_inverse_and_redo_bind_every_stage_effect`

### Failure × 3

```text
astrid.sdk.timeline._command_state.CommandError: replacement changes provider-managed edges
```

IDs:
- `tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[True]`
- `tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[False]`
- `tests/timeline/test_authoring_media.py::test_public_document_compound_inverse_restores_exact_original`

### Failure × 3

```text
failed on setup with "subprocess.CalledProcessError: Command '['git', 'archive', '0e1543e0da2215db9cb3320cfd1083174c3c62a9']' returned non-zero exit status 128."
```

IDs:
- `tests/test_bootmanifest2_admission.py::test_busy_rejected_attachment_preserves_r12_resident_reader`
- `tests/test_bootmanifest2_rollback.py::test_real_rollback_activates_r12_own_composition[True]`
- `tests/test_bootmanifest2_rollback.py::test_real_rollback_activates_r12_own_composition[False]`

### Failure × 2

```text
AssertionError: Regex pattern did not match.
  Expected regex: 'source changed|guard changed'
  Actual message: 'selected PARAM authority is unavailable'
```

IDs:
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin]`
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element]`

### Failure × 2

```text
AssertionError: assert 'label' not in {'blendMode': 'normal', 'fit': 'contain', 'id': 'V1', 'kind': 'visual', ...}
```

IDs:
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings[False]`
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings[True]`

### Failure × 2

```text
AttributeError: 'Runtime' object has no attribute '_last_handshake'
```

IDs:
- `tests/sdk/test_timeline_checkout.py::test_fast_lane_pair_keeps_real_explicit_working_snapshot_and_original_video[clean]`
- `tests/sdk/test_timeline_checkout.py::test_fast_lane_pair_keeps_real_explicit_working_snapshot_and_original_video[historical]`

### Failure × 2

```text
runtime_protocol.errors.RuntimeErrorBase: inverse stage provenance is attached to a non-inverse command
```

IDs:
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_disjoint_staged_label_and_inverse_preserve_opaque[False]`
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_disjoint_staged_label_and_inverse_preserve_opaque[True]`

### Failure × 1

```text
AssertionError: 18-version Runtime did not publish the selected realm
```

IDs:
- `tests/test_installer_lifecycle.py::test_real_backend_upgrade_binding_survives_fresh_controller_recovery`

### Failure × 1

```text
AssertionError: Preparing the new app while Astrid keeps running.
  Restarting Astrid with the prepared app.
  Astrid couldn't finish. Your work is kept.
  The Pinokio supervisor did not become ready; see /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/pinokio-home/api/astrid-pinokio/app/astrid/app-update-session.log.
  
  Astrid did NOT update: the new version didn't start.
  Astrid went back to Release 17. Your projects are unchanged.
  Run the same command again. If it fails twice, do the next step.
  Next: use the Update button in Pinokio.
  Details: /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/xdg-state/astrid-runtime/logs/install.log
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/pinokio-home/api/astrid-pinokio/app/astrid/versions/e2-candidate/py/bin/python', '-I', '-c', "import sys,json; from pathlib import Path\nfrom astrid.installer import cli\nfrom astrid.installer.backend import Backend\nfrom astrid.installer.core import Version\ncandidate=Version.load(json.loads(Path(sys.argv[2]).read_text()))\nBackend.stage=lambda *args,**kwargs:candidate\nBackend.sync_skills=lambda *args,**kwargs:None\ncli.validate_manifest=lambda value:value\nraise SystemExit(cli.main(['--update','--root',sys.argv[1],'--managed-by','pinokio','--manifest',sys.argv[3],'--uv',sys.argv[4]]))", '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/pinokio-home/api/astrid-pinokio/app/astrid', '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/pinokio-home/api/astrid-pinokio/app/astrid/versions/e2-candidate/version.json', '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/manifest.json', '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/uv'], returncode=1, stdout="Preparing the new app while Astrid keeps running.\nRestarting Astrid with the prepared app.\nAstrid couldn't finish. Your work is kept.\nThe Pinokio supervisor did not become ready; see /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/pinokio-home/api/astrid-pinokio/app/astrid/app-update-session.log.\n\nAstrid did NOT update: the new version didn't start.\nAstrid went back to Release 17. Your projects are unchanged.\nRun the same command again. If it fails twice, do the next step.\nNext: use the Update button in Pinokio.\nDetails: /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st0/xdg-state/astrid-runtime/logs/install.log\n").returncode
```

IDs:
- `tests/test_pinokio_switch_integration.py::test_switch_after_installer_starts_session[False]`

### Failure × 1

```text
AssertionError: Preparing the new app while Astrid keeps running.
  Restarting Astrid with the prepared app.
  Astrid couldn't finish. Your work is kept.
  The Pinokio supervisor did not become ready; see /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/pinokio-home/api/astrid-pinokio/app/astrid/app-update-session.log.
  
  Astrid did NOT update: the new version didn't start.
  Astrid went back to Release 17. Your projects are unchanged.
  Run the same command again. If it fails twice, do the next step.
  Next: use the Update button in Pinokio.
  Details: /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/xdg-state/astrid-runtime/logs/install.log
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/pinokio-home/api/astrid-pinokio/app/astrid/versions/e2-candidate/py/bin/python', '-I', '-c', "import sys,json; from pathlib import Path\nfrom astrid.installer import cli\nfrom astrid.installer.backend import Backend\nfrom astrid.installer.core import Version\ncandidate=Version.load(json.loads(Path(sys.argv[2]).read_text()))\nBackend.stage=lambda *args,**kwargs:candidate\nBackend.sync_skills=lambda *args,**kwargs:None\ncli.validate_manifest=lambda value:value\nraise SystemExit(cli.main(['--update','--root',sys.argv[1],'--managed-by','pinokio','--manifest',sys.argv[3],'--uv',sys.argv[4]]))", '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/pinokio-home/api/astrid-pinokio/app/astrid', '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/pinokio-home/api/astrid-pinokio/app/astrid/versions/e2-candidate/version.json', '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/manifest.json', '/tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/uv'], returncode=1, stdout="Preparing the new app while Astrid keeps running.\nRestarting Astrid with the prepared app.\nAstrid couldn't finish. Your work is kept.\nThe Pinokio supervisor did not become ready; see /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/pinokio-home/api/astrid-pinokio/app/astrid/app-update-session.log.\n\nAstrid did NOT update: the new version didn't start.\nAstrid went back to Release 17. Your projects are unchanged.\nRun the same command again. If it fails twice, do the next step.\nNext: use the Update button in Pinokio.\nDetails: /tmp/pytest-of-runner/pytest-0/test_switch_after_installer_st1/xdg-state/astrid-runtime/logs/install.log\n").returncode
```

IDs:
- `tests/test_pinokio_switch_integration.py::test_switch_after_installer_starts_session[True]`

### Failure × 1

```text
AssertionError: Recovering the interrupted Astrid update.
  Recovered your previous version — run Update again
  
  Astrid setup summary:
    Skill copies recovery: to enable skill copies later, rerun the install line with --skill-copies on (replace this flag in the Way back line).
    Maintenance: rerun the install line to repair or restart; add --update to update, or --uninstall to remove Astrid. Uninstall keeps the workspace unless --delete-data is added.
    Way back: curl -fsSL https://astrid.haus/install | sh -s -- --yes --autostart on --command on --skills on --skill-copies off
  
  Astrid did NOT update. It is still Release 17.
  Why: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.
  Your projects are safe — nothing was changed.
  Next: Run the same command again to finish updating.
  Details: see the error in this window.
  Traceback (most recent call last):
    File "<string>", line 45, in <module>
  AssertionError
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '-c', "\nimport sys\nfrom pathlib import Path\nfrom types import SimpleNamespace\nfrom astrid.installer import app_update, cli\nfrom astrid.installer.backend import Backend\nfrom astrid.installer.core import current, read_json\nfrom astrid.installer.service import installer_lock_path\nfrom runtime_protocol import platform\nfrom runtime_protocol.upgrade import inspect_canonical_schema\nroot, data, kind = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]\nbackend = Backend(root, root / 'recovery.log', root / 'absent-uv')\nbackend.managed_by = 'pinokio' if kind == 'app' else None\nbackend.service.systemd = lambda: False\nbackend.service.validate_stop_target = lambda *a, **kw: None\nbackend.service.login_service_exists = lambda: False\nbackend.service.disable = lambda: None\nbackend.service.stop = lambda: None\nready = []\ndef verify(version, workspace, realm_id):\n    realm = read_json(root / 'update-transaction.json')['realm']\n    assert inspect_canonical_schema(realm['realm_root'], expected_realm_id=realm_id)['realm_id'] == realm_id\n    assert version.release == 17\n    ready.append(realm_id)\nbackend.r...7\nassert ready == ['realm-1']\n", '/tmp/pytest-of-runner/pytest-0/test_new_interpreter_recovers_1/program', '/tmp/pytest-of-runner/pytest-0/test_new_interpreter_recovers_1/data', 'app'], returncode=1, stdout='Recovering the interrupted Astrid update.\nRecovered your previous version — run Update again\n\nAstrid setup summary:\n  Skill copies recovery: to enable skill copies later, rerun the install line with --skill-copies on (replace this flag in the Way back line).\n  Maintenance: rerun the install line to repair or restart; add --update to update, or --uninstall to remove Astrid. Uninstall keeps the workspace unless --delete-data is added.\n  Way back: curl -fsSL https://astrid.haus/install | sh -s -- --yes --autostart on --command on --skills on --skill-copies off\n\nAstrid did NOT update. It is still Release 17.\nWhy: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.\nYour projects are safe — nothing was changed.\nNext: Run the same command again to finish updating.\nDetails: see the error in this window.\n', stderr='Traceback (most recent call last):\n  File "<string>", line 45, in <module>\nAssertionError\n').returncode
```

IDs:
- `tests/test_installer_transaction_authority.py::test_new_interpreter_recovers_real_completed_c1_stop[app]`

### Failure × 1

```text
AssertionError: Recovering the interrupted Astrid update.
  Starting Release 17
  Checking Release 17 started
  Recovered your previous version — run Update again
  
  Astrid setup summary:
    Skill copies recovery: to enable skill copies later, rerun the install line with --skill-copies on (replace this flag in the Way back line).
    Maintenance: rerun the install line to repair or restart; add --update to update, or --uninstall to remove Astrid. Uninstall keeps the workspace unless --delete-data is added.
    Way back: curl -fsSL https://astrid.haus/install | sh -s -- --yes --autostart on --command on --skills on --skill-copies off
  
  Astrid was NOT installed.
  Why: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.
  Your projects are safe — nothing was changed.
  Next: Run the same command again to finish updating.
  Details: see the error in this window.
  Traceback (most recent call last):
    File "<string>", line 45, in <module>
  AssertionError
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '-c', "\nimport sys\nfrom pathlib import Path\nfrom types import SimpleNamespace\nfrom astrid.installer import app_update, cli\nfrom astrid.installer.backend import Backend\nfrom astrid.installer.core import current, read_json\nfrom astrid.installer.service import installer_lock_path\nfrom runtime_protocol import platform\nfrom runtime_protocol.upgrade import inspect_canonical_schema\nroot, data, kind = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]\nbackend = Backend(root, root / 'recovery.log', root / 'absent-uv')\nbackend.managed_by = 'pinokio' if kind == 'app' else None\nbackend.service.systemd = lambda: False\nbackend.service.validate_stop_target = lambda *a, **kw: None\nbackend.service.login_service_exists = lambda: False\nbackend.service.disable = lambda: None\nbackend.service.stop = lambda: None\nready = []\ndef verify(version, workspace, realm_id):\n    realm = read_json(root / 'update-transaction.json')['realm']\n    assert inspect_canonical_schema(realm['realm_root'], expected_realm_id=realm_id)['realm_id'] == realm_id\n    assert version.release == 17\n    ready.append(realm_id)\nbackend.r...'/tmp/pytest-of-runner/pytest-0/test_new_interpreter_recovers_0/program', '/tmp/pytest-of-runner/pytest-0/test_new_interpreter_recovers_0/data', 'migration'], returncode=1, stdout='Recovering the interrupted Astrid update.\nStarting Release 17\nChecking Release 17 started\nRecovered your previous version — run Update again\n\nAstrid setup summary:\n  Skill copies recovery: to enable skill copies later, rerun the install line with --skill-copies on (replace this flag in the Way back line).\n  Maintenance: rerun the install line to repair or restart; add --update to update, or --uninstall to remove Astrid. Uninstall keeps the workspace unless --delete-data is added.\n  Way back: curl -fsSL https://astrid.haus/install | sh -s -- --yes --autostart on --command on --skills on --skill-copies off\n\nAstrid was NOT installed.\nWhy: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.\nYour projects are safe — nothing was changed.\nNext: Run the same command again to finish updating.\nDetails: see the error in this window.\n', stderr='Traceback (most recent call last):\n  File "<string>", line 45, in <module>\nAssertionError\n').returncode
```

IDs:
- `tests/test_installer_transaction_authority.py::test_new_interpreter_recovers_real_completed_c1_stop[migration]`

### Failure × 1

```text
AssertionError: Regex pattern did not match.
  Expected regex: '10|16'
  Actual message: 'selected PARAM authority is unavailable'
```

IDs:
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_retained_schema_replay_inverse_reload_and_exact_retry`

### Failure × 1

```text
AssertionError: Traceback (most recent call last):
    File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 1008, in <module>
      _installer(base, kill_at, mode)
    File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 993, in _installer
      raise RuntimeError(f"public installer Update exited with status {result}")
  RuntimeError: public installer Update exited with status 3
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py', 'cli-update', '/tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0', ''], returncode=1, stdout="Recovering the interrupted Astrid update.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/data/runtime/realms/realm-1.failed-476d1510. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/data/runtime/realms/realm-1.failed-6767e2f1. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/data/runtime/realms/realm-1.failed-6e194408. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/data/runtime/realms/realm-1.failed-7eed93c1. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/data/runtime/realms/realm-1.failed-83a09417. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/data/runtime/realms/realm-1.failed-b50fd6a4. You can delete it once Astrid works.\nStarting Release 17\nChecking Release 17 started\nRecovered your previous version — run Update again\n\nAstrid did NOT update. It is still Release 18.\nWhy: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.\nYour projects are safe — nothing was changed.\nNext: Run the same command again to finish updating.\nDetails: /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_0/cli-logs/install.log\n", stderr='Traceback (most recent call last):\n  File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 1008, in <module>\n    _installer(base, kill_at, mode)\n  File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 993, in _installer\n    raise RuntimeError(f"public installer Update exited with status {result}")\nRuntimeError: public installer Update exited with status 3\n').returncode
```

IDs:
- `tests/test_installer_update_recovery.py::test_baseline_restore_catalog_gap_recovers_through_public_installer_and_real_c1[legacy-realm-replaced]`

### Failure × 1

```text
AssertionError: Traceback (most recent call last):
    File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 1008, in <module>
      _installer(base, kill_at, mode)
    File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 993, in _installer
      raise RuntimeError(f"public installer Update exited with status {result}")
  RuntimeError: public installer Update exited with status 3
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py', 'cli-update', '/tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1', ''], returncode=1, stdout="Recovering the interrupted Astrid update.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/data/runtime/realms/realm-1.failed-42e4a774. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/data/runtime/realms/realm-1.failed-5bb6fccd. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/data/runtime/realms/realm-1.failed-91d8fc55. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/data/runtime/realms/realm-1.failed-92a28e03. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/data/runtime/realms/realm-1.failed-b37ad5c1. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/data/runtime/realms/realm-1.failed-fec53373. You can delete it once Astrid works.\nStarting Release 17\nChecking Release 17 started\nRecovered your previous version — run Update again\n\nAstrid did NOT update. It is still Release 18.\nWhy: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.\nYour projects are safe — nothing was changed.\nNext: Run the same command again to finish updating.\nDetails: /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_1/cli-logs/install.log\n", stderr='Traceback (most recent call last):\n  File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 1008, in <module>\n    _installer(base, kill_at, mode)\n  File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 993, in _installer\n    raise RuntimeError(f"public installer Update exited with status {result}")\nRuntimeError: public installer Update exited with status 3\n').returncode
```

IDs:
- `tests/test_installer_update_recovery.py::test_baseline_restore_catalog_gap_recovers_through_public_installer_and_real_c1[legacy-catalog-deleted]`

### Failure × 1

```text
AssertionError: Traceback (most recent call last):
    File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 1008, in <module>
      _installer(base, kill_at, mode)
    File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 993, in _installer
      raise RuntimeError(f"public installer Update exited with status {result}")
  RuntimeError: public installer Update exited with status 3
  
assert 1 == 0
 +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py', 'cli-update', '/tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2', ''], returncode=1, stdout="Recovering the interrupted Astrid update.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/data/runtime/realms/realm-1.failed-0b1f4e6c. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/data/runtime/realms/realm-1.failed-144cf2b7. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/data/runtime/realms/realm-1.failed-52788492. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/data/runtime/realms/realm-1.failed-62e4d7ae. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/data/runtime/realms/realm-1.failed-c5d34fed. You can delete it once Astrid works.\nThe failed update's workspace copy is kept at /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/data/runtime/realms/realm-1.failed-f8a36880. You can delete it once Astrid works.\nStarting Release 17\nChecking Release 17 started\nRecovered your previous version — run Update again\n\nAstrid did NOT update. It is still Release 18.\nWhy: an earlier update was interrupted and Astrid restored the version before it; run the same command again to update.\nYour projects are safe — nothing was changed.\nNext: Run the same command again to finish updating.\nDetails: /tmp/pytest-of-runner/pytest-0/test_baseline_restore_catalog_2/cli-logs/install.log\n", stderr='Traceback (most recent call last):\n  File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 1008, in <module>\n    _installer(base, kill_at, mode)\n  File "/home/runner/work/astrid-agent/astrid-agent/tests/test_installer_update_recovery.py", line 993, in _installer\n    raise RuntimeError(f"public installer Update exited with status {result}")\nRuntimeError: public installer Update exited with status 3\n').returncode
```

IDs:
- `tests/test_installer_update_recovery.py::test_baseline_restore_catalog_gap_recovers_through_public_installer_and_real_c1[legacy-catalog-copy-staged]`

### Failure × 1

```text
AssertionError: UPD: stale ASTRID_ACP_COMMAND survived into candidate declaration; old='/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/pruned/py/bin/astrid', candidate='/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/candidate/py/bin/astrid', selected='/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/pruned/py/bin/astrid'. Reproduce with ci_journey.py --leg update-over-old-declaration --old-declaration pruned and explicit B1 roots.
assert ('/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/pruned/py/bin/astrid' and PosixPath('/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/pruned/py/bin/astrid') == PosixPath('/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/candidate/py/bin/astrid'))
 +  where PosixPath('/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/pruned/py/bin/astrid') = Path('/tmp/pytest-of-runner/pytest-0/test_upd_c1_old_declaration_re0/program/versions/pruned/py/bin/astrid')
```

IDs:
- `tests/upgrade/test_c1_product_gaps.py::test_upd_c1_old_declaration_rebinds_chat_command_to_candidate[pruned]`

### Failure × 1

```text
AssertionError: assert 1 == 0
 +  where 1 = <function main at 0x736f451c7240>(['--update-app', '--managed-by', 'pinokio', '--root', '/tmp/pytest-of-runner/pytest-0/test_update_candidate_and_roll0/pinokio-home/api/astrid-app/app/astrid', '--manifest', ...])
 +    where <function main at 0x736f451c7240> = <module 'astrid.installer.cli' from '/home/runner/work/astrid-agent/astrid-agent/astrid/installer/cli.py'>.main
```

IDs:
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[updated]`

### Failure × 1

```text
AssertionError: assert 1 == 0
 +  where 1 = <function main at 0x736f451c7240>(['--update-app', '--managed-by', 'pinokio', '--root', '/tmp/pytest-of-runner/pytest-0/test_update_candidate_and_roll2/pinokio-home/api/astrid-app/app/astrid', '--manifest', ...])
 +    where <function main at 0x736f451c7240> = <module 'astrid.installer.cli' from '/home/runner/work/astrid-agent/astrid-agent/astrid/installer/cli.py'>.main
```

IDs:
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[recovered]`

### Failure × 1

```text
AssertionError: assert 1 == 0
 +  where 1 = <function main at 0x736f451c7240>(['--update-app', '--managed-by', 'pinokio', '--root', '/tmp/pytest-of-runner/pytest-0/test_update_candidate_and_roll3/pinokio-home/api/astrid-app/app/astrid', '--manifest', ...])
 +    where <function main at 0x736f451c7240> = <module 'astrid.installer.cli' from '/home/runner/work/astrid-agent/astrid-agent/astrid/installer/cli.py'>.main
```

IDs:
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[recovered_running_candidate]`

### Failure × 1

```text
AssertionError: assert [{'blendMode'...1, 0, False]}] == [{'id': 'prop...1, 0, False]}]
  
  At index 0 diff: {'blendMode': 'normal', 'fit': 'contain', 'id': 'V1', 'kind': 'visual', 'label': 'V1', 'opacity': 1, 'scale': 1} != {'id': 'proposed', 'kind': 'visual', 'opaque': [1, 0, False]}
  Left contains 2 more items, first extra item: {'blendMode': 'normal', 'fit': 'contain', 'id': 'A1', 'kind': 'audio', ...}
  
  Full diff:
    [
  +     {
  +         'blendMode': 'normal',
  +         'fit': 'contain',
  +         'id': 'V1',
  +         'kind': 'visual',
  +         'label': 'V1',
  +         'opacity': 1,
  +         'scale': 1,
  +     },
  +     {
  +         'blendMode': 'normal',
  +         'fit': 'contain',
  +         'id': 'A1',
  +         'kind': 'audio',
  +         'label': 'A1',
  +         'opacity': 1,
  +         'scale': 1,
  +     },
        {
            'id': 'proposed',
            'kind': 'visual',
            'opaque': [
                1,
                0,
                False,
            ],
        },
    ]
```

IDs:
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes`

### Failure × 1

```text
AssertionError: assert not ({'install', 'rollback', 'uninstall', 'update'} & {'add', 'agent-index', 'check', 'inspect', 'list', 'ls', ...})
 +  where {'add', 'agent-index', 'check', 'inspect', 'list', 'ls', ...} = set({'add': RecoverableArgumentParser(prog='python3 -m astrid.core.pack.cli add', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True), 'agent-index': RecoverableArgumentParser(prog='python3 -m astrid.core.pack.cli agent-index', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True), 'check': RecoverableArgumentParser(prog='python3 -m astrid.core.pack.cli validate', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True), 'inspect': RecoverableArgumentParser(prog='python3 -m astrid.core.pack.cli inspect', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True), ...})
```

IDs:
- `tests/stage1/test_runtime_client_cutover.py::test_retired_public_commands_are_absent`

### Failure × 1

```text
AssertionError: assert {'kind': 'run...account', ...} == {'kind': 'run...volume-test'}}
  
  Omitting 4 identical items, use -vv to show
  Left contains 1 more item:
  {'mounts': [{'read_only': False,
               'source': 'volume-test',
               'target': '/tmp/pytest-of-runner/pytest-0/test_json_selection_uses_produ0/volume'}]}
  
  Full diff:
    {
        'kind': 'runpod',
  +     'mounts': [
  +         {
  +             'read_only': False,
  +             'source': 'volume-test',
  +             'target': '/tmp/pytest-of-runner/pytest-0/test_json_selection_uses_produ0/volume',
  +         },
  +     ],
        'pod_id': 'pod-test',
        'provider_account_ref': 'runpod-test-account',
        'storage': {
            'name': 'test-volume',
            'network_volume_id': 'volume-test',
        },
    }
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_json_selection_uses_production_composition_and_real_cpu_staging`

### Failure × 1

```text
AssertionError: remotion/src/types.generated.ts is stale; regenerate with scripts/gen_remotion_types.py
assert "// DO NOT ED...] as const;\n" == "// DO NOT ED...] as const;\n"
  
    // DO NOT EDIT — generated by tools/scripts/gen_remotion_types.py
    //
    // Naming convention: TypedDicts re-exported from
    // banodoco_timeline_schema (AssetEntry, Theme, ThemeOverrides,
    // TimelineClip, TimelineConfig, TimelineOutput) are emitted with the
    // `Shared*` name as the canonical TS interface. The un-prefixed name
    // (plus any other in-repo alias such as AssetRegistryEntry) is emitted
    // as `export type X = SharedX;` for back-compat. New code should
    // prefer the `Shared*` name.
    
    export type AnimationReferenceList =
      | string
      | AnimationReferenceObject
      | (string | AnimationReferenceObject)[];
    
    export interface AnimationReferenceObject {
      durationFrames?: number;
      easing?: string;
      id?: string;
      params?: Record<string, unknown>;
    }
    
    export interface Arrangement {
      brief_sha256?: string;
      brief_slug?: string;
      brief_text?: string;
      clips?: ArrangementClip[];
      generated_at?: string;
      pool_sha256?: string;
      source_slug?: string;
      target_duration_sec?: number;
      version?: number;
    }
    
    export interface ArrangementAudioSource {
      pool_id: string;
      trim_sub_range: number[];
    }
    
    export interface ArrangementClip {
      audio_source: ArrangementAudioSource | null;
      order: number;
      rationale: string;
      text_overlay?: ArrangementTextOverlay | null;
      uuid: string;
      visual_source: ArrangementVisualSource;
    }
    
    export interface ArrangementTextOverlay {
      content?: string;
      style_preset?: string;
    }
    
    export interface ArrangementVisualSource {
      params?: Record<string, unknown>;
      pool_id: string;
      role: 'overlay' | 'primary' | 'stinger';
    }
    
    export interface AssetRegistry {
      assets: Record<string, SharedAssetEntry>;
    }
    
    export interface AudioBindingValue {
      max: number;
      min: number;
      source: 'amplitude' | 'bass' | 'mid' | 'treble';
    }
    
    export interface ClipContinuous {
      intensity?: number;
      params?: Record<string, unknown>;
      type?: string;
    }
    
    export interface ClipEntrance {
      duration?: number;
      intensity?: number;
      params?: Record<string, unknown>;
      type?: string;
    }
    
    export interface ClipExit {
      duration?: number;
      intensity?: number;
      params?: Record<string, unknown>;
      type?: string;
    }
    
    export interface ClipTransition {
      duration: number;
      type: string;
    }
    
    export interface ClipTransitionReference {
      duration?: number;
      durationFrames?: number;
      id?: string;
      params?: Record<string, unknown>;
      type?: string;
    }
    
    export interface DerivedFrom {
      assetId?: string;
      content_sha256?: string;
      role?: 'proxy' | 'render-output' | 'thumbnail';
    }
    
    export interface ParameterDefinition {
      default?: unknown;
      description: string;
      label: string;
      max?: number;
      min?: number;
      name: string;
      options?: ParameterOption[];
      step?: number;
      type: 'audio-binding' | 'boolean' | 'color' | 'number' | 'select';
    }
    
    export interface ParameterOption {
      label: string;
      value: string;
    }
    
    export interface PipelineMetadata {
      clips: Record<string, PipelineMetadataClipEntry>;
      generated_at: string;
      pipeline: Record<string, unknown>;
      sources: Record<string, Record<string, unknown>>;
      version: number;
    }
    
    export interface PipelineMetadataClipEntry {
      arrangement_notes?: null | string;
      caption_kind?: 'dialogue' | 'visual';
      pick_rationale?: string;
      picked_by?: string;
      pool_id?: null | string;
      pool_kind?: 'applause' | 'dialogue' | 'music' | 'reaction' | 'text' | 'visual';
      score?: number;
      source_ids?: SourceIds;
      source_scene_id?: string;
      source_transcript_text?: null | string;
      source_uuid?: string;
      text_overlay_content?: string;
    }
    
    export interface Pool {
      entries?: PoolEntry[];
      generated_at?: string;
      source_slug?: string;
      version?: number;
    }
    
    export interface PoolEntry {
      asset?: string;
      bed_kind?: string;
      camera?: string;
      category: 'applause' | 'dialogue' | 'music' | 'reaction' | 'visual';
      defaults?: Record<string, unknown>;
      duration: number;
      effect_id?: string;
      energy?: number;
      event_label?: string;
      excluded: boolean;
      excluded_reason?: null | string;
      id: string;
      intensity?: number;
      kind: 'generative' | 'source';
      meta?: Record<string, unknown>;
      mood_tags?: string[];
      motion_tags?: string[];
      param_schema?: Record<string, unknown>;
      quote_kind?: string;
      scores: PoolScores;
      source_ids?: SourceIds;
      speaker?: null | string;
      src_end?: number;
      src_start?: number;
      subject?: string;
      text?: string;
    }
    
    export interface PoolScores {
      deep?: number;
      quotability?: number;
      triage?: number;
    }
    
    export interface SharedAssetEntry {
      content_sha256?: string;
      derivedFrom?: DerivedFrom;
      duration?: number;
      etag?: string;
      file?: string;
      fps?: number;
      generationId?: string;
      media_id?: string;
      origin?: 'immutable-public' | 'opaque-foreign' | 'refreshable-from-generation';
      resolution?: string;
      thumbnailUrl?: string;
      type?: string;
      url?: string;
      url_expires_at?: string;
      variantId?: string;
    }
    
    export type AssetEntry = SharedAssetEntry;
    
    export type AssetRegistryEntry = SharedAssetEntry;
    
    export interface SharedTheme {
      audio?: Record<string, unknown>;
      generation?: Record<string, unknown>;
      id?: string;
      pacing?: Record<string, unknown>;
      visual?: Record<string, unknown>;
      voice?: Record<string, unknown>;
    }
    
    export type Theme = SharedTheme;
    
    export interface SharedThemeOverrides {
      audio?: Record<string, unknown>;
      generation?: Record<string, unknown>;
      pacing?: Record<string, unknown>;
      visual?: Record<string, unknown>;
      voice?: Record<string, unknown>;
    }
    
    export type ThemeOverrides = SharedThemeOverrides;
    
    export interface SharedTimelineClip {
      app?: Record<string, unknown>;
      asset?: string;
      at?: number;
      clipType?: string;
      clip_order?: number;
      continuous?: AnimationReferenceList;
      cropBottom?: number;
      cropLeft?: number;
      cropRight?: number;
      cropTop?: number;
      derived_output?: Record<string, unknown>;
      effects?: TimelineEffect[] | Record<string, number>;
      entrance?: AnimationReferenceList;
      exit?: AnimationReferenceList;
      from?: number;
      generation?: Record<string, unknown>;
      height?: number;
      hold?: number;
      id?: string;
      keyframes?: Record<string, unknown>;
      label?: string;
      opacity?: number;
      params?: Record<string, unknown>;
      pool_id?: string;
      source_uuid?: string;
      speed?: number;
      text?: TextClipData;
      to?: number;
      track?: string;
      transition?: ClipTransitionReference | string;
      volume?: number;
      width?: number;
      x?: number;
      y?: number;
    }
    
    export type TimelineClip = SharedTimelineClip;
    
    export type Clip = SharedTimelineClip;
    
    export interface SharedTimelineConfig {
      app?: Record<string, unknown>;
      clips?: SharedTimelineClip[];
      generation_defaults?: Record<string, unknown>;
      output?: SharedTimelineOutput;
      pinnedShotGroups?: Record<string, unknown>[];
      theme?: string;
      theme_overrides?: SharedThemeOverrides;
      tracks?: TrackDefinition[];
    }
    
    export type TimelineConfig = SharedTimelineConfig;
    
    export interface SharedTimelineOutput {
      background?: null | string;
      background_scale?: null | number;
      file?: string;
      fps?: number;
      resolution?: string;
    }
    
    export type TimelineOutput = SharedTimelineOutput;
    
    export interface SourceIds {
      scene_id?: string;
      segment_ids?: number[];
    }
    
    export interface TextClipData {
      align?: 'center' | 'left' | 'right';
      bold?: boolean;
      color?: string;
      content?: string;
      fontFamily?: string;
      fontSize?: number;
      italic?: boolean;
    }
    
    export interface TimelineEffect {
      fade_in?: number;
      fade_out?: number;
    }
    
    export interface TrackDefinition {
      app?: Record<string, unknown>;
      blendMode?: 'darken' | 'hard-light' | 'lighten' | 'multiply' | 'normal' | 'overlay' | 'screen' | 'soft-light';
      fit?: 'contain' | 'cover' | 'manual';
      id: string;
      kind: 'audio' | 'visual';
      label: string;
  +   meta?: Record<string, unknown>;
      muted?: boolean;
      opacity?: number;
      scale?: number;
      volume?: number;
    }
    
    export const _ASSET_ENTRY_ALLOWED = ['content_sha256', 'derivedFrom', 'duration', 'etag', 'file', 'fps', 'generationId', 'media_id', 'origin', 'resolution', 'thumbnailUrl', 'type', 'url', 'url_expires_at', 'variantId'] as const;
  - export const _CLIP_ALLOWED = ['app', 'asset', 'at', 'clipType', 'clip_order', 'continuous', 'cropBottom', 'cropLeft', 'cropRight', 'cropTop', 'effects', 'elementRef', 'entrance', 'exit', 'from', 'generation', 'height', 'hold', 'id', 'keyframes', 'label', 'opacity', 'params', 'pool_id', 'shot_id', 'shot_name', 'shot_occurrence_id', 'source_uuid', 'speed', 'text', 'to', 'track', 'transition', 'volume', 'width', 'x', 'y'] as const;
  + export const _CLIP_ALLOWED = ['app', 'asset', 'at', 'clipType', 'clip_order', 'continuous', 'cropBottom', 'cropLeft', 'cropRight', 'cropTop', 'effects', 'elementRef', 'entrance', 'exit', 'from', 'generation', 'height', 'hold', 'id', 'keyframes', 'label', 'meta', 'opacity', 'params', 'pool_id', 'shot_id', 'shot_name', 'shot_occurrence_id', 'source_uuid', 'speed', 'text', 'to', 'track', 'transition', 'volume', 'width', 'x', 'y'] as const;
  ?                                                                                                                                                                                                                                                                ++++++++
    export const _THEME_OVERRIDES_ALLOWED = ['audio', 'generation', 'pacing', 'visual', 'voice'] as const;
  - export const _TIMELINE_TOP_ALLOWED = ['app', 'clips', 'generation_defaults', 'output', 'pinnedShotGroups', 'theme', 'theme_overrides', 'tracks'] as const;
  + export const _TIMELINE_TOP_ALLOWED = ['app', 'clips', 'generation_defaults', 'meta', 'output', 'pinnedShotGroups', 'theme', 'theme_overrides', 'tracks'] as const;
  ?                                                                              ++++++++
  - export const _TRACK_ALLOWED = ['app', 'blendMode', 'fit', 'id', 'kind', 'label', 'muted', 'opacity', 'role', 'scale', 'volume'] as const;
  + export const _TRACK_ALLOWED = ['app', 'blendMode', 'fit', 'id', 'kind', 'label', 'meta', 'muted', 'opacity', 'role', 'scale', 'volume'] as const;
  ?                                                                                  ++++++++
```

IDs:
- `tests/packs/test_renderer_parity.py::test_remotion_typecheck_is_blocking_when_dependencies_are_installed`

### Failure × 1

```text
AssertionError: rendering.render: proof did not execute cleanly: {'returncode': 1, 'status': 'fail', 'output_tail': ' monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(REMOTION.resolve()))\n        with _execution_env():\n            for name in list(os.environ):\n                if name.startswith(("DYLD_", "LD_")) or name in _REMOTION_UNSUPPORTED_OVERRIDES:\n                    monkeypatch.delenv(name, raising=False)\n            # Use the same launch transaction as the real pack host.  It qualifies\n            # the host and the worker projection; a standalone-only artifact does\n            # not match GenericPackHost\'s worker readiness context.\n            env = dict(os.environ)\n            launch = _prepare_render_validation(\n                ROOT,\n                env,\n                tmp_path / "support",\n                sys.executable,\n                (ROOT / "astrid" / "packs" / "rendering",),\n            )\n>           assert launch is not None\nE           assert None is not None\n\ntests/integrations/test_generic_host_remotion_render.py:249: AssertionError\n---------------------------- Captured stderr setup -----------------------------\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "owned_probe", "outcome": "completed", "process_id": 15704, "elapsed_ms": 3037}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "owned_probe", "outcome": "completed", "process_id": 15704, "elapsed_ms": 2999}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "owned_probe", "outcome": "completed", "process_id": 15704, "elapsed_ms": 380}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "registry_settle", "outcome": "failed", "process_id": 15704, "elapsed_ms": 7523}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "launch_transaction", "outcome": "failed", "process_id": 15704, "elapsed_ms": 7523}\n=========================== short test summary info ============================\nERROR tests/integrations/test_generic_host_remotion_render.py::test_generic_host_remotion_register_claim_execute_settle_and_cas - assert None is not None\n1 error in 10.20s\n\n'}
assert ({'output_tail': ' monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(REMOTION.resolve()))\n        with _execution_env():\n            for name in list(os.environ):\n                if name.startswith(("DYLD_", "LD_")) or name in _REMOTION_UNSUPPORTED_OVERRIDES:\n                    monkeypatch.delenv(name, raising=False)\n            # Use the same launch transaction as the real pack host.  It qualifies\n            # the host and the worker projection; a standalone-only artifact does\n            # not match GenericPackHost\'s worker readiness context.\n            env = dict(os.environ)\n            launch = _prepare_render_validation(\n                ROOT,\n                env,\n                tmp_path / "support",\n                sys.executable,\n                (ROOT / "astrid" / "packs" / "rendering",),\n            )\n>           assert launch is not None\nE           assert None is not None\n\ntests/integrations/test_generic_host_remotion_render.py:249: AssertionError\n---------------------------- Captured stderr setup -----------------------------\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "owned_probe", "outcome": "completed", "process_id": 15704, "elapsed_ms": 3037}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "owned_probe", "outcome": "completed", "process_id": 15704, "elapsed_ms": 2999}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "owned_probe", "outcome": "completed", "process_id": 15704, "elapsed_ms": 380}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "registry_settle", "outcome": "failed", "process_id": 15704, "elapsed_ms": 7523}\n{"diagnostic": "astrid.remotion_validation_phase", "phase": "launch_transaction", "outcome": "failed", "process_id": 15704, "elapsed_ms": 7523}\n=========================== short test summary info ============================\nERROR tests/integrations/test_generic_host_remotion_render.py::test_generic_host_remotion_register_claim_execute_settle_and_cas - assert None is not None\n1 error in 10.20s\n\n', 'returncode': 1, 'status': 'fail'} and 'fail' == 'pass'
  
  - pass
  + fail)
```

IDs:
- `tests/stage1/test_capability_parity_gate_luna.py::test_every_ready_capability_has_a_passing_family_proof`

### Failure × 1

```text
AssertionError: {'executor_id': 'rendering.render', 'missing_binaries': [], 'returncode': 1, 'skipped': False, ...}
assert False
 +  where False = ExecutorRunResult(executor_id='rendering.render', kind='external', command=('/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '-m', 'astrid.packs.rendering.actions.render.run', '--timeline', '/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/projects/demo/timeline.json', '--assets', '/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/projects/demo/assets.json', '--out', '/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/result.mp4', '--theme', '/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/managed-objects/theme.json', '--selector', 'rendering.remotion', '--backend-config', '{"rendering.remotion":{"project_dir":"/home/runner/work/astrid-agent/astrid-agent/remotion"}}', '--output-name', 'result.mp4', '--keep-previous-renders', '--materialized-root', '/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/managed-objects', '--materialized-objects', '{"0db3b5d49ded34c10559bef852385e10d163b73904c7d767c7f46a8ebdf45fb3":"/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/managed-objects/managed-41cf6794ba4200b8-0db3b5d49ded34c10559bef852385e10d163b73904c7d767c7f46a8ebdf45fb3","5e187584245a83e8408da74d0a8d88dbf2a3f38e2606b7c5b7045d620b3bed66":"/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/managed-objects/theme.json","media-remotion":"/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/managed-objects/managed-41cf6794ba4200b8-0db3b5d49ded34c10559bef852385e10d163b73904c7d767c7f46a8ebdf45fb3","theme":"/tmp/pytest-of-runner/pytest-0/test_host_derived_registry_rea0/attempt/managed-objects/theme.json"}'), cwd=None, env={}, payload={'executor_id': 'rendering.render', 'missing_binaries': [], 'returncode': 1, 'skipped': False, 'skipped_reason': ''}, returncode=1, dry_run=False, skipped=False, skipped_reason='', missing_binaries=(), error=ExecError(code='nonzero_exit', type='process', message='executor exited with returncode 1', recovery='inspect the executor output/logs and retry'), run_root=None, outputs=[], executor_version='f2208c876a1dc2443c9c5244566759031ce1e40f72d1bb299861de826e0b9312', run_id=None).ok
```

IDs:
- `tests/stage1/test_media_handoff_render_boundary.py::test_host_derived_registry_reaches_canonical_remotion_executor_process`

### Failure × 1

```text
Failed: no Runtime checkout: set ASTRID_RUNTIME_CHECKOUT to one (looked at ['/home/user/work/wt/rt-pin-8ea0766f'])
```

IDs:
- `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`

### Failure × 1

```text
ValueError: The manifest's lifecycle pin differs from the staged Agent's canonical pin. Manifest: repository <invalid> revision e63d614009673ea312d749f688ea4ec8b0ae80bd version 0.3.1.dev0. Agent (astrid/packs/runpod/pins.json): repository https://github.com/banodoco/runpod-lifecycle.git revision 7f0b025e9391baac9f5c2fb7393617ea6fef0704 version 0.3.1.dev0. Install a release manifest whose pins match this Agent, or change astrid/packs/runpod/pins.json in the Agent checkout to the pin you want to test.
```

IDs:
- `tests/test_installer_real_product_root.py::test_staged_product_root_is_admitted_by_validate_candidate`

### Failure × 1

```text
assert [1] == [2, 1]
  
  At index 0 diff: 1 != 2
  Right contains one more item: 1
  
  Full diff:
    [
  -     2,
        1,
    ]
```

IDs:
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[rolled_back]`

### Failure × 1

```text
astrid.core.pack._common.PackValidationError: duplicate pack id 'vibecomfy': pack 'vibecomfy' conflicts with a core pack across /tmp/pytest-of-runner/pytest-0/test_import_edit_capture_histo0/packs/vibecomfy and /home/runner/work/astrid-agent/astrid-agent/astrid/packs/vibecomfy
```

IDs:
- `tests/packs/test_vibecomfy_import_generic_host.py::test_import_edit_capture_history_runs_as_runtime_tasks_and_settles_lineage`

### Failure × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_changed_config_corrupt_jo0/base/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_changed_config_corrupt_journal_and_account_or_volume_mismatch_refuse_reuse`

### Failure × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel0/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_leaf]`

### Failure × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel1/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_parent]`

### Failure × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel2/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[node_leaf]`

### Failure × 1

```text
astrid.packs.runpod.worker_staging.WorkerPreparationError: Traceback (most recent call last):
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 381, in load_workflow_path
    resolved = load_bundle(source, trust=Provenance.USER_CONFIRMED)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/workflow_bundle.py", line 3089, in load_bundle
    workflow = load_scratchpad(
               ^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 276, in load_scratchpad
    workflow = execute_build()
               ^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/scratchpad_loader.py", line 263, in execute_build
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/smoke/empty_image_red.py", line 12, in <module>
    READY_METADATA = ReadyMetadata.build(
                     ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 1338, in build
    coverage_row = _coverage_manifest_row(qualified_template_id)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/templates.py", line 2067, in _coverage_manifest_row
    data = resources.coverage_manifest()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 111, in coverage_manifest
    return _read_json("coverage_manifest")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 91, in _read_json
    path = _resource_path(name)
           ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/vibecomfy/resources.py", line 86, in _resource_path
    raise ShippedResourceMissingError(name, path)
vibecomfy.errors.ShippedResourceMissingError: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<local-child>", line 177, in <module>
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/invocation_preflight.py", line 380, in preflight_invocation
    loaded = load_workflow_path(source, Path(raw_scratch), comfy_url=comfy_url)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/astrid/astrid/packs/vibecomfy/production_engine.py", line 383, in load_workflow_path
    raise ProductionEngineError(
astrid.packs.vibecomfy.production_engine.ProductionEngineError: canonical workflow bundle could not be loaded: Shipped VibeComfy resource 'coverage_manifest' is missing at /tmp/pytest-of-runner/pytest-0/test_same_byte_custom_node_rel3/volume/.astrid/prepared-workers/ce68bfcfa5b07741dc3e985c/source/vibecomfy/ready_templates/sources/manifests/coverage.json next action: Reinstall VibeComfy from a complete distribution.
```

IDs:
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[node_parent]`

### Failure × 1

```text
astrid.sdk.timeline.sync.CommitRefused: The Runtime declined this edit; nothing was committed. settled producer authority changed. Inspect the saved edit with tl.pending_show("pc_31afbbe0a293"), fix the edit, then retry or drop it.
```

IDs:
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[digest]`

### Failure × 1

```text
astrid.sdk.timeline.sync.CommitRefused: The Runtime declined this edit; nothing was committed. settled producer dependency is unavailable. Inspect the saved edit with tl.pending_show("pc_6765912495aa"), fix the edit, then retry or drop it.
```

IDs:
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[target]`

### Failure × 1

```text
astrid.sdk.workspace_client.WorkspaceClientError: legacy timeline writes are retired; submit EditCommands through commitTimeline
```

IDs:
- `tests/sdk/test_timeline_import.py::test_cross_realm_timeline_export_import_reload_and_reimport`

### Failure × 1

```text
failed on setup with "astrid.sdk.timeline.sync.CommitRefused: The Runtime declined this edit; nothing was committed. provider dependency union omits a captured read. Inspect the saved edit with tl.pending_show("pc_58c099e6545e"), fix the edit, then retry or drop it."
```

IDs:
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart`

### Failure × 1

```text
runtime_protocol.errors.ConflictError: realm failed integrity checks
```

IDs:
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_pre_enforcement_alias_history_reopens_with_current_authority`

### Failure × 1

```text
runtime_protocol.errors.RetiredRouteError: legacy timeline writes are retired; submit EditCommands through commitTimeline
```

IDs:
- `tests/sdk/test_timeline_export.py::test_export_plan_closure_equals_runtime_publish_manifest`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: nested inverse mirrors exceed accepted effects
```

IDs:
- `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py::test_native_add_delete_one_publication_inverse_redo_restart_reservations[net-zero]`

### Failure × 1

```text
runtime_protocol.errors.RuntimeErrorBase: provider consumed manifest differs from its sequential parent allocation
```

IDs:
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_inverse_then_selection_and_params_use_staged_pin`

### Failure × 1

```text
subprocess.CalledProcessError: Command '['/tmp/pytest-of-runner/pytest-0/test_pinokio_session_binds_rea0/pinokio-home/api/astrid-pinokio/app/astrid/versions/candidate/tools/node']' returned non-zero exit status 1.
```

IDs:
- `tests/test_installer_pinokio_integration.py::test_pinokio_session_binds_real_runtime_to_pending_launch_intent[app]`

### Failure × 1

```text
subprocess.CalledProcessError: Command '['/tmp/pytest-of-runner/pytest-0/test_pinokio_session_binds_rea1/pinokio-home/api/astrid-pinokio/app/astrid/versions/candidate/tools/node']' returned non-zero exit status 1.
```

IDs:
- `tests/test_installer_pinokio_integration.py::test_pinokio_session_binds_real_runtime_to_pending_launch_intent[migration]`

### Failure × 1

```text
subprocess.CalledProcessError: Command '['git', '-C', '/home/runner/work/astrid-agent/astrid-agent/astrid-runtime', 'archive', '6d53a19070faf63fc15ae1f81417722edc2c8a5f']' returned non-zero exit status 128.
```

IDs:
- `tests/upgrade/test_busy_fixture_release.py::test_release_fails_closed_and_preserves_unrelated_work[6d53a19070faf63fc15ae1f81417722edc2c8a5f]`

## Exact G1 reconciliation

Only exact testcase IDs count as recurrences. Parameter-family similarities are separate and not counted. G1 contains red IDs only, so unmatched current red IDs are not automatically new or previously passing.

Prior red IDs: 125; current red IDs with exact prior G1 ID: 125; current red IDs absent from prior red inventory: 0. Transitions: `{"error_persists_same_status": 26, "failed_persists_same_status": 99}`.

| Prior G1 status | Current status | Count |
|---|---|---:|
| ERROR | ERROR | 26 |
| FAILED | FAILED | 99 |

## Per-ID triage and Plan 38/55


- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_leaf]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[lock_parent]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[node_leaf]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/runpod/test_worker_staging.py::test_same_byte_custom_node_release_aliases_fail_before_resolved_reuse[node_parent]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/runpod/test_worker_staging.py::test_changed_config_corrupt_journal_and_account_or_volume_mismatch_refuse_reuse` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/runpod/test_worker_staging.py::test_json_selection_uses_production_composition_and_real_cpu_staging` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[media-only]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[effect-clip]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[text-card]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[audio-reactive-colour]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_renderer_parity.py::test_real_remotion_renders_each_semantic_variant[transition-windows]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_renderer_parity.py::test_remotion_typecheck_is_blocking_when_dependencies_are_installed` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/packs/test_vibecomfy_import_generic_host.py::test_import_edit_capture_history_runs_as_runtime_tasks_and_settles_lineage` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_element_inverse_source_retention.py::test_inverse_loads_original_object_after_readmission_and_restart` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_saved_projection_config_registry_and_full_pins_golden` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_saved_entire_expansion_golden` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[parent]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[child]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[new_shot]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[duplicate]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[remove]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[sdk_bundle]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_checkout.py::test_fast_lane_pair_keeps_real_explicit_working_snapshot_and_original_video[clean]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_checkout.py::test_fast_lane_pair_keeps_real_explicit_working_snapshot_and_original_video[historical]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_checkout_reload_undo_cli_redo_uses_retained_history` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_retained_restore_does_not_reopen_consumed_draft_steps` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_checkout_history_runtime.py::test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py::test_native_add_delete_one_publication_inverse_redo_restart_reservations[net-zero]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings[False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings[True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_structural_reservations_and_receipt_retry_survive_runtime_restart` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_restore_inverse_redo_and_exact_retry_survive_runtime_restart` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_export.py::test_export_plan_closure_equals_runtime_publish_manifest` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_import.py::test_cross_realm_timeline_export_import_reload_and_reimport` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_legacy_inverse_bindings.py::test_legacy_producer_forward_inverse_and_redo_bind_every_stage_effect` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[2-2.0]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[1-True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[True-1]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[2-2]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[2.0-2.0]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_params_exact_values_history_reload_retry_and_inverse[True-True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_original_value_guards_keep_numeric_equivalence_and_bool_distinction[2-2.0-True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_original_value_guards_keep_numeric_equivalence_and_bool_distinction[1-True-False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_numeric_revision_runtime.py::test_native_original_value_guards_keep_numeric_equivalence_and_bool_distinction[True-1-False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[digest]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[target]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_pre_enforcement_alias_history_reopens_with_current_authority` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_disjoint_staged_label_and_inverse_preserve_opaque[False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_disjoint_staged_label_and_inverse_preserve_opaque[True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_inverse_then_selection_and_params_use_staged_pin` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_mixed_pack_readmission_keeps_old_and_new_native_param_sources` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_retained_schema_replay_inverse_reload_and_exact_retry` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_equal_json_opposite_selection_order_and_inverse_restore` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/stage1/test_capability_parity_gate_luna.py::test_every_ready_capability_has_a_passing_family_proof` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/stage1/test_media_handoff_render_boundary.py::test_host_derived_registry_reaches_canonical_remotion_executor_process` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/stage1/test_runtime_client_cutover.py::test_retired_public_commands_are_absent` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_bootmanifest2_admission.py::test_busy_rejected_attachment_preserves_r12_resident_reader` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_bootmanifest2_rollback.py::test_real_rollback_activates_r12_own_composition[True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_bootmanifest2_rollback.py::test_real_rollback_activates_r12_own_composition[False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_lifecycle.py::test_real_backend_upgrade_binding_survives_fresh_controller_recovery` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[updated]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[rolled_back]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[recovered]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_activation.py::test_update_candidate_and_rollback_activate_under_retained_custody[recovered_running_candidate]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pinokio_session_binds_real_runtime_to_pending_launch_intent[app]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pinokio_session_binds_real_runtime_to_pending_launch_intent[migration]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[stopping-backend-retained]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[stopping-backend-current]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[candidate_ready-backend-retained]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[candidate_ready-backend-current]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-backend-retained]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-backend-current]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-local-retained]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[migrated-local-current]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[switched-backend-retained]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[switched-backend-current]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[before_owner-backend-retained]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_integration.py::test_pre_e2_pinokio_foreground_rolls_back_and_recovers_migration[before_owner-backend-current]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[stopped-backend]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[stopped-local]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[running-backend]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[running-local]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[incapable-retained-runtime]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[unrelated-retained-runtime]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[incapable-candidate-runtime]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[unrelated-candidate-runtime]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[missing-stop-marker]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[malformed-stop-marker]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[unknown-stop-binding]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[add-local-two-stop-build]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[midstop-crash-after-stop]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_pinokio_stopped_update.py::test_canonical_stop_then_fresh_update_cli_uses_retained_c1_authority[midstop-crash-during-term]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_real_product_root.py::test_staged_product_root_is_admitted_by_validate_candidate` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_transaction_authority.py::test_new_interpreter_recovers_real_completed_c1_stop[migration]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_transaction_authority.py::test_new_interpreter_recovers_real_completed_c1_stop[app]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_update_recovery.py::test_baseline_restore_catalog_gap_recovers_through_public_installer_and_real_c1[legacy-realm-replaced]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_update_recovery.py::test_baseline_restore_catalog_gap_recovers_through_public_installer_and_real_c1[legacy-catalog-deleted]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_installer_update_recovery.py::test_baseline_restore_catalog_gap_recovers_through_public_installer_and_real_c1[legacy-catalog-copy-staged]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_pinokio_switch_integration.py::test_switch_after_installer_starts_session[False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/test_pinokio_switch_integration.py::test_switch_after_installer_starts_session[True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[True]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[False]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/timeline/test_authoring_media.py::test_public_document_compound_inverse_restores_exact_original` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-none]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-create]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-claim]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-heartbeat]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-output]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-nonzero]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-timeout]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_release_rolls_back_partial_settlement[6d53a19070faf63fc15ae1f81417722edc2c8a5f]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_creation.py::test_creation_error_remains_primary_and_retry_reconciles[6d53a19070faf63fc15ae1f81417722edc2c8a5f]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_busy_fixture_release.py::test_release_fails_closed_and_preserves_unrelated_work[6d53a19070faf63fc15ae1f81417722edc2c8a5f]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_c1_product_gaps.py::test_upd_c1_old_declaration_rebinds_chat_command_to_candidate[pruned]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_upgrade_release.py::test_guard_accepts_authoritative_source_shapes` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_upgrade_release.py::test_production_source_format_change_requires_release_review[runtime_protocol/store.py-SCHEMA_VERSION = 31-SCHEMA_VERSION = 32-runtime]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_upgrade_release.py::test_production_source_format_change_requires_release_review[runtime_protocol/service.py-journal.get("version") != 1-journal.get("version") != 2-runtime]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
- `tests/upgrade/test_upgrade_release.py::test_production_source_format_change_requires_release_review[astrid/installer/core.py-"identity": {"release": self.release, "managed_by": self.managed_by}-"identity": {"release": self.release, "managed_by": self.managed_by}, "format": 2-agent]` — exact prior G1 red-ID recurrence. Prior triage: new — A-b / AT1 — unclassified observed signature. Plan 38: No exact Plan 38 inventory match in prior G1 audit; no testcase ownership assigned; Plan 55: No exact Plan 55 inventory match in prior G1 audit; no testcase ownership assigned.
