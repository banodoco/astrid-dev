# Agent range record — 22 November 2026

## Revision range

`release/15/main` `8807f820eb47d6018db723511e024a0a123fbe95` → `release/15/plan-81` `9c95c680e645335a4a2ea8091f02b88934a2492b` (52 files, +4,697/−599). The range contains Plan 81 work for command discovery and local registry reuse, optional command timing and lifecycle/stage instrumentation, plus related tests. The branch history also contains the Plan 69 and R14 forwards; those forwards are already in the stated release base.

## Recorded proof

- Agent PR #524 is at the range head. Its A-3 collector/stage coverage and lifecycle proof logs include `/root/codex/plan-81m/run/a3-forward-base-proof.log`, `a3-integrated-proof-forward.log`, `a3-manager-forward-focused.log`, and `a3-manager-forward-integration.log` in that same run directory. The Plan 69 Agent inventory comparison recorded 166 pass and the same 16 failures per side after correcting setup selection; details are in [`2026-11-22-plan69-forward.md`](2026-11-22-plan69-forward.md) and `/root/codex/plan-81/run/forward69-inventory-logs/`.
- The installed A/B evidence is in [`2026-11-22-installed-attribution-review.md`](2026-11-22-installed-attribution-review.md) and `/root/codex/installed-baseline/evidence/ab-run-1/`. Its candidate changed Agent, Runtime, and VibeComfy together, so it does not isolate Agent’s contribution.

## Not established by these records

The Plan 69 inventory is from an earlier forward comparison, not a full CI result for this exact range. Full final-range CI status is not recorded here. The installed A/B and its after-arm stages do not attribute a per-repository or per-fix share. The local A-5 observer remains unqualified: its two focused runs each had 22 passes and 6 failures; the documented aliases/process/hash coverage gaps are deferred to Plan 82. The host dropped A-6a source samples. No 90% attribution result is established. See [`2026-11-22-attribution-completeness.md`](2026-11-22-attribution-completeness.md).

## Inherited CI context

Astrid-dev issue [#1371](https://github.com/banodoco/astrid-dev/issues/1371) tracks inherited Runtime portability-lifecycle and other published-main reds. The host identified this as the inherited context for the non-Vibe gates; this record does not assign those failures to this range.

Source notes: host record `/root/codex/plan-81m/run/to-codex.md` (16:12 UTC, 22 November 2026); evidence PRs [#1422](https://github.com/banodoco/astrid-dev/pull/1422) and [#1423](https://github.com/banodoco/astrid-dev/pull/1423).
