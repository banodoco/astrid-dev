<!-- baseline-diff:generated:start -->
| Side | Tests run |
|---|---|
| run-start-main-1e1c646e | 201 |
| candidate | 221 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 0 |
| preexisting | 0 |
| fixed | 0 |
| missing | 6 |
<!-- baseline-diff:generated:end -->

## Evidence context

- **Baseline:** run-start astrid-dev `main` at `1e1c646ea428bfd022adc024bbc25bc08078ef93`; 201 unittest cases, all passed. The historical baseline shell command was not preserved. The nine-module inventory scope is identified by the baseline log and plan inventory. Reproducible equivalent command (not a verbatim historical command):

  ```sh
  PYTHONPATH=scripts python3 -m unittest -v test_check_docs test_checks test_check_completion test_views test_records test_auto_merge test_issue_intake test_export_public_vision test_golden
  ```

- **Tested candidate:** commit `64aaf557cf845f74d23c241aa005393926ba8145`, tree `4328d950523b72a6be5f76e8433ade83518a20f0`. It includes the reviewed R1.1/R1.2 merge commit `1c28a173dd8cfb3f471c64b0418758ca104a72b7` plus current astrid-dev `main` at `a9dc8fb4197ead24d73b8207dbf1403651900be0`; the intervening main changes are Plan 55 and Plan 58 progress updates. The candidate inventory completed with exit 0: 221 tests in 28.879 seconds, `OK`.
- **Remote exact-tree equivalent:** commit `a9d79f65e359ee021c902dc3a763a0ef4f58a324` has the same tree `4328d950523b72a6be5f76e8433ade83518a20f0` and is retained as the parent of the completion-records commit for inspection on GitHub. The recorded tests ran on local commit `64aaf557...`; they were not executed on remote commit `a9d79f65...` itself.
- **Candidate command:** the invocation used the same ten modules as the previous candidate run, redirected to the canonical run log. Shown repo-relative so it can be rerun without an absolute scratch path:

  ```sh
  PYTHONPATH=scripts python3 -m unittest -v test_check_docs test_checks test_check_completion test_views test_records test_auto_merge test_issue_intake test_export_public_vision test_golden test_release_issues > plans/58-strategy-from-releases/.otto/runs/2026-11-15-chatgpt-3417d5f77996/reviewed-candidate-inventory.log 2>&1
  ```

- **Comparison interpretation:** 0 failures on both sides; 26 candidate-only passing IDs; 6 baseline IDs are missing from the candidate. The six are the SR-2 authorized removals/rewrites listed in `retired-sr2.txt`; replacement and added IDs are in `new-tests.txt`. The complete candidate inventory is in `all-tests.txt`.
- **Method:** astrid-dev's CI uses stdlib `unittest`; `pytest` is absent, while `env/baseline-diff.py` accepts pytest `-rA` output. The retained adapter maps each unittest verbose test row to `PASSED scripts/test_module.py::Class::method` and verifies converted row totals against each `Ran N tests` footer. Raw logs, converted status logs and the adapter are included for reproduction.
- **Environment and limits:** Python 3.12.14 on Linux x86_64; the staging executor reported 9 logical CPUs. The raw logs contain no separate environment fingerprint. This is the complete unittest inventory comparison for the named local candidate; it makes no broader CI or repository-check claim.
