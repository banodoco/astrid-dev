#!/usr/bin/env bash
set +e
cd /workspace/scratch/cd53b069f320/p39-repair/astrid-agent
bash scripts/worker-env/agent-pytest.sh -q -rA --junitxml=/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-recovery/after.xml tests/test_boundary_registration_launchd.py::test_launchd_sigkill_after_publication_link_replays tests/test_installer_r0_stop.py::test_killed_after_disable_next_invocation_recovers tests/test_installer_r0_stop.py::test_launchd_sigkill_at_each_stop_step_then_recover > /workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-recovery/after.log 2>&1
status=$?
printf '%s\n' "$status" > /workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-recovery/after.exit
exit 0
