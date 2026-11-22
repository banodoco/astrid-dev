# Runtime range record — 22 November 2026

## Revision range

`release/15/main` `23310dc828765293a2ab39f63728b948e780d94` → `release/15/plan-81` `72b129e5a2296dc58360a9896cc65fab9db4ad0c`. The two changed files are `runtime_protocol/source_identity.py` and `tests/test_source_identity_process_budget.py` (+137/−18). The change batches Git blob hashing through `--stdin-paths`, computes symlink blob IDs in process, and adds process-budget tests.

## Recorded proof

- [`2026-11-22-plan69-forward.md`](2026-11-22-plan69-forward.md) records a Runtime source-startup identity inventory of 29 passing tests on each side, with no changed test IDs. That is an earlier forward comparison, not proof of this exact two-file range.
- [`2026-11-22-installed-attribution-review.md`](2026-11-22-installed-attribution-review.md) records the installed A/B candidate tuple and after-arm stage observations. Agent, Runtime, and VibeComfy changed together in that candidate; the result does not isolate Runtime’s contribution.

## Not established by these records

No final-range Runtime CI result or range-specific test inventory is recorded here. The 29/29 result above is not a test of the process-budget file change. The combined installed comparison does not establish a Runtime-only speed effect. The Plan 81 attribution evidence does not establish 90% operation attribution.

## Inherited CI context

Astrid-dev issue [#1371](https://github.com/banodoco/astrid-dev/issues/1371) tracks inherited Runtime portability-lifecycle and other published-main reds. The host identified this as inherited context for the non-Vibe gates; this record does not assign those failures to this range.

Source notes: host record `/root/codex/plan-81m/run/to-codex.md` (16:12 UTC, 22 November 2026); evidence PRs [#1422](https://github.com/banodoco/astrid-dev/pull/1422) and [#1423](https://github.com/banodoco/astrid-dev/pull/1423).
