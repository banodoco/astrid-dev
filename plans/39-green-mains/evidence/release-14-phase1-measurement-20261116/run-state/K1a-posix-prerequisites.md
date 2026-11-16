# K1a — four remaining POSIX prerequisites

Manager `/root`; follow-ups are part of the brief. Route N (`gpt-6-luna`, high), local additive commits only, no remote writes, never ask user questions.

Agent repo `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`, exact base `cd778822a9a5fab273144ca367cfdd94a20889e3`, tree `001f36c60b039ab5a6fc8048f7472e82645a1a0c`. Work on `p39/k1a-posix-prerequisites`.

Scope: only the following four existing gates. Replace three platform skip decorators with existing `posix_native`; replace the function-local `pytest.importorskip("fcntl")` with an ordinary function-local `import fcntl` plus `posix_native` on that exact test. Never import fcntl at module level, which would break Windows collection. Remove only now-unused imports. Preserve all test bodies/assertions/parameters except the explicitly replaced import gate, neighboring tests and CI selections.

The O_NOFOLLOW case currently probes the real POSIX flag; verify it exists on the supported Linux/macOS CPython targets and that the new platform lane preserves the current supported-platform eligibility. If there is a meaningful capability mismatch, stop that card and report rather than invent a broad skip. These paths exercise runtime-output path placement, pack filesystem locks and a fake installed launcher, not Plan 38 native process identity or Plan 55 warm-session behavior. Recheck contracts before editing.

Exact before/after proof:

```sh
bash scripts/worker-env/agent-pytest.sh -q tests/core/generation/test_vibecomfy_runtime_root.py::test_default_platform_is_the_host_platform tests/core/pack/test_nofollow_fallback.py::test_group_lock_refuses_linked_lock_file_with_real_nofollow tests/core/pack/test_transaction_windows.py::test_windows_lock_covers_renames_journal_and_backup_retirement tests/test_omp_agent.py::test_installed_launcher_dispatches_generate_json
```

If pre-proof fails, preserve full output and stop without changing its expectations or product code. No whole suite or policy rerun. Save raw logs/exits, exact patch, supported-platform selection and AST comparison, commit/tree under `p39-g2-evidence/agent/k1a-posix-prerequisites/`. Independent review follows. Full K1a is still blocked by the excluded Plan 38 gate; no exception or completion claim.
