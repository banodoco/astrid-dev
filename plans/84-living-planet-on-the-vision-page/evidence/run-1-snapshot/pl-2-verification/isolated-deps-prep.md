# PL-2 verifier isolated dependencies and entry-repair acceptance notes

Prepared on 2026-11-22 for candidate `88ac863600492401bc22e352999660f3d5b01020` in `worktrees/pl-2-verify`.

## Dependency isolation

Copied `worktrees/baseline/node_modules` (543 MB) to `worktrees/pl-2-verify.env/node_modules`, then repointed only `worktrees/pl-2-verify/node_modules` to that private copy. The four repository-vendor package links (`@banodoco/timeline-theme-2rp`, `@banodoco/timeline-schema`, `@banodoco/timeline-ops`, and `fake-indexeddb`) now target this verifier worktree's matching `vendor/` directories. The copied dependency tree has no broken symlinks. The copied private `.vite` cache is present (33 MB); it is private to this node_modules tree, not shared with baseline/other worktrees. No test or product files were changed; candidate worktree remains clean at the SHA above. No tests/build/browser checks were run.

## Focused acceptance notes from entry-repair evidence

`initial-analysis.md` records two baseline-green assertions that failed in the earlier PL-2 verification: the navigation overflow marker remained `clip` during a 5s poll, and the cold `/vision` title was absent at the first 5s assertion but appeared in the later snapshot. It explicitly treats synchronous planet-engine initialization as a hypothesis. The relevant isolated comparison proposed there is the same route/browser/feed/viewport on the plan-start baseline and candidate head, with candidate normal live behavior compared against an evidence-only engine-disabled response. Capture title/transition timing, feed/title events, constructor duration, long tasks, and first render; don't attribute the difference to a constructor without the controlled comparison.

The two-line `probe-frame-rerun.log` reports direct-route title time 1,390 ms with engine disabled and 6,449 ms live; live recorded a 5,211 ms long task and a 214.8 ms measure, with no reported JS errors. It also reports `transition: null` and `overflow: visible` for both variants. This probe is useful context, not acceptance proof: it is a single baseline/candidate-independent frame comparison and does not resolve whether an overlapping Vite optimizer or another environmental factor affected the live result. Preserve existing assertions and use the manager's later isolated-run decision before spending a heavy slot.
