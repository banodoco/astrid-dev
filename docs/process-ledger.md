# Process ledger

Friction, ideas and fixes in astrid-dev itself: its skills, templates, checks and workflow. Product bugs go to their repository's issues instead.

**Add-only.** Add new rows at the end; never edit or delete a row. To resolve one, add a `fix` row that names it, and to retract one, add a row saying so. Any planner, manager, advisor or contributor may add a row.

Kinds:
- **papercut:** small friction;
- **issue:** something that went wrong or will;
- **idea:** a possible improvement;
- **fix:** resolves an earlier row.

| # | Date | Kind | What | Evidence | Link |
|---|---|---|---|---|---|
| 1 | 2026-11-07 | issue | The manager and advisor guidance was only found through links, so a manager coordinated a whole effort without reading it | Plan 07 run | — |
| 2 | 2026-11-07 | fix | Resolves #1: manager and advisor became the Manage and Advise skills | — | [PR #50](https://github.com/banodoco/astrid-dev/pull/50) |
| 3 | 2026-11-07 | papercut | `check_docs.py` passes locally while CI's planning-evidence check fails. A field written on the line after its label is not read, and the local docs check doesn't run that validator | PR #49 runs | — |
| 4 | 2026-11-07 | issue | The review-intake check returns 403 when adding its label on scope PRs | PR #49 run | — |
| 5 | 2026-11-07 | idea | `check_completion.py` doesn't tie the evidence run to the integrated candidate's exact versions, or require the run to have passed | Plan 07 completion review | — |
| 6 | 2026-11-07 | papercut | The completion template asks for "Models used", which conflicts with keeping model identifiers out of repository artifacts | Plan 07 PR #35 | — |
| 7 | 2026-11-07 | issue | Two projects redesigned the same App screens at once with no shared model; a merge undid an owner decision | Plans 01 and 29 | — |
| 8 | 2026-11-07 | fix | Resolves #7: task scopes, a dependency for overlapping scopes, and one model per shared surface | — | [PR #53](https://github.com/banodoco/astrid-dev/pull/53) |
| 9 | 2026-11-08 | papercut | `sync.sh` exits non-zero and reports "incomplete" for skill folders that don't exist (here `~/.codex/skills` and `~/.agents/skills`), so a run that only wants `~/.claude/skills` must pass `--destination` to get a clean exit | Install run, 2026-11-08 | — |
| 10 | 2026-11-08 | issue | Plan 29 gives two different Agent start SHAs: `inputs.md` lists `709492fa` and `tasks.md` lists `a2c4ab7d`. A manager who starts from either one may build on the wrong base | `plans/29-update-and-release/inputs.md` and `tasks.md` line 5 | — |
| 11 | 2026-11-08 | papercut | `sync.sh` installs `astrid-dev-shared`, which has no `SKILL.md`, as if it were a skill | `SKILL_NAMES` in `sync.sh`; `skills/astrid-dev-shared/` | — |
| 12 | 2026-11-08 | papercut | A session without the repo attached can't read PR state: the GitHub API returns 403 for `gh api` and `gh pr view`, so merge status can only be inferred from `main` | `gh api repos/banodoco/astrid-dev/pulls/57` returned 403 | — |
| 13 | 2026-11-08 | fix | Resolves #10: Plan 29's tasks say to start from the live heads recorded at task start, and that the listed SHAs only locate cited lines | — | this PR |
