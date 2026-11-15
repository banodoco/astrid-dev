# Unit shard 8 — run 43693935046

- Job id: 132750235040
- Head SHA: a91c35dfd63f8d5969714541a30afe25feb2d626
- Conclusion: failure
- Pytest: = 91 failed, 3757 passed, 25 skipped, 27236 deselected, 1 warning, 2 errors, 202 subtests passed in 1536.77s (0:25:36) =
- Wall time (log fetch, diff, and attribution): 1.99s

## New failures by owner lane

### flaky-on-R12
- tests/test_pinokio_platform_adapter.py::test_real_local_start_http_readiness_snapshot_stop_and_port_free — flaky-on-R12 — failed in some R12 logs and passed in others

### unattributed
- tests/test_onboarding_one_home.py::test_shipped_skills_run_astrid_through_the_launcher_not_python_m — no-baseline — 09fee85f0f0f Skills name cancel, and run Astrid through the installed launcher (path tests/test_onboarding_one_home.py)
- tests/test_setup_skill_branches.py::test_runpod_setup_from_pristine_settings_preserves_choices_and_quotes_without_claim — no-baseline — ab830f4c3a95 Shorten the setup skill and say "Next: set up generation" at every door (path tests/test_setup_skill_branches.py)

## Baseline-diff counts

| Side | Tests run |
|---|---|
| r12 | 23882 |
| candidate | 3854 |

| Bucket | Count |
|---|---|
| regression | 0 |
| no-baseline | 4 |
| preexisting | 93 |
| fixed | 23 |
| missing | 19229 |
