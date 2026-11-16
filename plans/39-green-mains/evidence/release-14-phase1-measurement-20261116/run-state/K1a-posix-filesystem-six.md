# K1a — six independent passing POSIX filesystem gates

Manager `/root`; follow-ups are part of the brief. Route N (`gpt-6-luna`, high), add local commits only, no remote writes. Never ask user questions.

This is a bounded replacement for the earlier seven-gate card, which stopped without edits. After repairing missing ensurepip at the same Python3.13.5 version and retaining an identical package freeze, nine cases pass; the installed-schema case now exposes an independent stale-candidate/cleanup assertion and is held for a separate cause card. Do not change that test in this card. This separation does not change any CI selection or suppress its failure.

Sole editable repository `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`, base `6c06460d3e7b46001f9d57e5b011cb114bfa23d0`, tree `6336201f0ee7a042c80695f9449248ff1609d05a`; local branch `p39/k1a-posix-filesystem` is clean at that base.

Change only six existing OS-only skip decorators to the already active `pytest.mark.posix_native`, plus imports made unused by those exact replacements. Preserve bodies, signatures, assertions, parameters, other decorators and all neighboring tests. Leave the separate missing-Git direct skip conditions unchanged. No registry/scanner/workflow/quarantine/product changes. No Plan 38/55 owned behavior changes.

Exact pre/post proof:

```sh
bash scripts/worker-env/agent-pytest.sh -q tests/core/pack/test_cli_manage.py::test_implicit_descriptor_refuses_writable_and_aliases tests/core/pack/test_git_environment.py::test_planted_ssh_in_working_directory_never_runs tests/core/pack/test_git_environment.py::test_recorded_git_that_lost_its_execute_bit_falls_back_to_absolute_path_lookup tests/test_installer_pack_cleanup.py::test_posix_failed_removal_never_chmods_a_symlink_target_outside_the_tree tests/test_installer_sources.py::test_missing_runtime_lock_names_the_missing_path_not_aliasing tests/test_installer_sources.py::test_missing_candidate_or_product_root_directory_is_named
```

Save complete stdout/stderr/exit, diff, AST equivalence and selection review, commit/tree under `p39-g2-evidence/agent/k1a-posix-filesystem-six/`. Stop if this focused proof exposes another failure; no expectation changes. No full policy run (root batches that gate). Root separately reads patch and commissions independent review before publication.
