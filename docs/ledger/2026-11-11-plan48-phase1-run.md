Date: 2026-11-11
Kind: papercut
Source: Plan 48 Phase 1 run, run by the orchestrator with Codex workers
Resolved by: —

Four frictions from running Phase 1 end to end. First, a Codex workspace-write sandbox protects `.git`, so a worker cannot commit or push; the orchestrator committed each worker's reviewed output itself. Next, the PM-3 merge was verified without running `test_golden.py`, and that let a duplicate-line regression reach the integration branch until the next check; a run should name every focused test file from the card, not a subset. Third, the first worker briefs listed scope too narrowly: the card's own acceptance text (`astrid_dev.py sync`, the generated `docs/checks.md`) needed files the scope column did not name, which stopped two workers. Fourth, a Haiku manager cannot do taste or review work, so those rows need an Opus sub-agent by name, not by routing label. Each is a process gap, not a code defect. A later run should put the card's test list and every file its acceptance text names in the scope.
