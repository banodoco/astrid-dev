# K1a — independent Linux gate cards

Manager `/root`; follow-ups are part of this brief. Route N (`gpt-6-luna`, high), local additive commits only, no remote writes, never ask user questions. Treat each listed gate as an independent small card: a blocked card does not block diagnosis of the others. Do not retry a failed proof or change its expectations; record and hold it for its own cause card.

Agent repository `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`, start `16ef29bf8cd9d9df82c6f2a892feff3dffc44d70`, tree `f155b695df8c89b375e761ae1a4f51470c41bc85`. Branch `p39/k1a-linux-gates`. All output outside repo under `/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-linux-gates/`.

Outcome: replace only an existing exact Linux-only skip gate with existing `pytest.mark.linux_native`. Preserve the same module/test scope, all bodies/assertions/parameters/other marks, and supported-platform eligibility. No default-off `integration` marker may be added. The engine-readiness and Pinokio XDG cases were independently cleared for this narrow ownership scope in `/workspace/scratch/cd53b069f320/p39-g2-evidence/k1-ownership-resolution.md`; read it. For other files, read the tested contract and Plan38/55 boundaries before editing; mere use of a process is not proof of ownership, but direct native identity/provider or warm-job settlement assertions are excluded. Hold any ambiguity; never edit the excluded native audit-token test.

For EACH row, run the exact pre-proof below. If it passes completely, replace that one OS gate and run the same command again, saving raw output/exit and selected-case parity. If it fails/errors/skips via a forbidden direct call, do not alter that gate or any expectation in this card; record cause and continue to the next independent row. Do not repeat failed proof. Do not change manual artifact gates or add exclusions to make a module proof pass.

| File/gate | Exact pre/post command |
|---|---|
| engine readiness module | `bash scripts/worker-env/agent-pytest.sh -q tests/core/generation/test_engine_readiness.py` |
| boundary handoff module | `bash scripts/worker-env/agent-pytest.sh -q tests/test_boundary_handoff.py` |
| boundary registration module | `bash scripts/worker-env/agent-pytest.sh -q tests/test_boundary_registration.py` |
| installer R0 entry module | `bash scripts/worker-env/agent-pytest.sh -q tests/test_installer_r0_entry.py` |
| installer end-to-end update module | `bash scripts/worker-env/agent-pytest.sh -q tests/test_installer_update_end_to_end.py` |
| installer legacy-record update module | `bash scripts/worker-env/agent-pytest.sh -q tests/test_installer_update_legacy_record.py` |
| update from field states module | `bash scripts/worker-env/agent-pytest.sh -q tests/test_update_from_field_states.py` |
| app update Linux XDG test only | `bash scripts/worker-env/agent-pytest.sh -q tests/test_installer_app_update.py::test_running_foreground_lock_refuses_with_xdg_override_before_writes` |
| Pinokio custody Linux XDG test only | `bash scripts/worker-env/agent-pytest.sh -q tests/test_installer_pinokio_custody.py::test_custody_retains_foreground_and_legacy_locks_when_xdg_is_filtered` |

Run only these focused files/selectors, sequentially (no broad suite or full policy test). Remove only imports made unused by the exact gate replacement. Preserve module lists of other marks. For each passing migration, AST compare signatures/bodies/decorators except the exact gate, and document existing Ubuntu/default coverage and native-Windows/Darwin behavior. One additive commit per passing card or one clearly enumerated batch is acceptable; include only authorized files. End with a table of all nine dispositions, exact counts, untouched failures, commit/tree and proof paths. Root and an independent reviewer decide publication; no claim that all K1a is complete.
