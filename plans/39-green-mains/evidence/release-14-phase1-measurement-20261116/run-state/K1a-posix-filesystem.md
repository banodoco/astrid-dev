# K1a acceptance follow-up: seven existing POSIX filesystem gates

Manager `/root`; follow-up messages are part of this brief. Never ask the user a question; send questions to the manager. Route N (`gpt-6-luna`, high). Add commits only, no remote writes.

Repository `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`, exact base `6c06460d3e7b46001f9d57e5b011cb114bfa23d0`, tree `6336201f0ee7a042c80695f9449248ff1609d05a`. Work on local branch `p39/k1a-posix-filesystem`.

Outcome: replace seven existing OS-only direct skips with the already active `posix_native` marker, preserving every executable test body and all existing CI selection where its prerequisite holds. No quarantine, scanner, cap, workflow or product changes. Keep the independent Git-availability direct skips unchanged for a separate capability card. The listed tests exercise pack descriptor permissions, Git executable handling and installer filesystem diagnostics, outside Plan 38/55 owned identity/host contracts; recheck before editing.

Scope and exact proof (run before and after; save full stdout/stderr and exit status):

```sh
bash scripts/worker-env/agent-pytest.sh -q tests/core/pack/test_cli_manage.py::test_implicit_descriptor_refuses_writable_and_aliases tests/core/pack/test_git_environment.py::test_planted_ssh_in_working_directory_never_runs tests/core/pack/test_git_environment.py::test_recorded_git_that_lost_its_execute_bit_falls_back_to_absolute_path_lookup tests/test_installer_pack_cleanup.py::test_posix_failed_removal_never_chmods_a_symlink_target_outside_the_tree tests/test_installer_installed_schema.py::test_stage_rejects_foreign_guarded_directory_before_declaration tests/test_installer_sources.py::test_missing_runtime_lock_names_the_missing_path_not_aliasing tests/test_installer_sources.py::test_missing_candidate_or_product_root_directory_is_named
```

Only these seven gates may change, plus imports made unused by the changes. Six are decorators; the installed-schema case has a body-level POSIX skip that may be replaced with a test-level existing marker, deleting only that conditional skip. Do not migrate or mark whole files, other tests, parameters or fixtures. Compare AST bodies while excluding only the removed skip guard, preserve all assertions, and inspect current Ubuntu/default selection and prior Windows/Darwin coverage.

If the pre-change command fails, stop and report the first distinct cause with full logs. Do not fix or weaken the test. Do not run broad suites or the full skip-policy file; root will run the gate once per integrated batch.

Save proof, full patch and commit/tree under `/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-filesystem/`. Root and an independent reviewer must read the patch before publication.
