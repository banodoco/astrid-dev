#!/usr/bin/env bash
set +e
cd /workspace/scratch/cd53b069f320/p39-repair/astrid-agent
bash scripts/worker-env/agent-pytest.sh -q -rA --junitxml=/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-parameters/after.xml tests/core/generation/test_model_verification_record.py::test_non_utf8_filename_hashes_then_reuses 'tests/core/pack/test_verified_relocations.py::test_forged_personal_relocation_is_rejected[public]' 'tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[partial]' 'tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[oversized]' tests/packs/runpod/test_failure_diagnostics.py::test_partial_ipc_from_unkillable_caller_returns_with_pending_fence > /workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-parameters/after.log 2>&1
status=$?
printf '%s\n' "$status" > /workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-parameters/after.exit
exit 0
