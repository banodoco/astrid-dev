# Release 15 measurement for Plan 39

Measured on 23–24 November 2026 by read-only helpers, on Runtime `release/15/main` `24e2c929` and App `release/15/main` `3f5da385` (with `d53685f3` read for code). No test was run; each file says what was verified in code and what was inferred from logs. Card names in these files (`P39-RT1`, `RT-E1`, `CI-1`, `N-4`, `FR-01`, `APP-01`, `A1`, `Q1`, `ENV-ADP` and so on) are the helpers' drafts; [tasks.md](../../tasks.md) gives each its task id. Paths in these files are relative to each repository's root.

| File | What it holds |
| --- | --- |
| [runtime-ci.md](runtime-ci.md) | The Runtime's workflows, job table, top causes, pins and Nightly summary |
| [runtime-clusters.md](runtime-clusters.md), [runtime-failing-ids.tsv](runtime-failing-ids.tsv) | Runtime CI failures grouped by raise site, and every failing (cluster, outcome, job, id) row; one ID appears once per job |
| [runtime-nightly-clusters.md](runtime-nightly-clusters.md), [runtime-nightly-failing-ids.tsv](runtime-nightly-failing-ids.tsv) | The same for Nightly run 45166036353 on `main` |
| [rt-c1c2.md](rt-c1c2.md) | The v33 fence clusters C1 and C2 (358 IDs): verdict and cards RT-1, RT-2 |
| [rt-c3c7.md](rt-c3c7.md) | Starter tracks (C3, C7 and related, 39 IDs): card RT-3 and question D17 |
| [rt-env.md](rt-env.md) | C4, C5, C6, portability, sandbox pidfd and hard-coded paths: cards RT-4 to RT-9 |
| [rt-tail-nightly.md](rt-tail-nightly.md) | The CI singletons (CI-1 to CI-10), the Nightly causes (N-1 to N-17) and the prune candidates |
| [app-ci.md](app-ci.md) | The App's workflows, job table, causes, cancellation and quarantine state |
| [app-fake-runtime.md](app-fake-runtime.md) | The fake Runtime against the App's calls and the Runtime's routes: cards AP-1 to AP-5 |
| [app-stale.md](app-stale.md) | The App's stale, environment and unknown E2E failures: cards AP-6 to AP-10 |
| [app-wiring-journeys.md](app-wiring-journeys.md) | CI wiring, quick journey, Direct Journey, the four quarantined tests and the three-products structure |
| [gate-design.md](gate-design.md) | `env/baseline-diff.py`'s defects, per-test reporting, the ceiling and the gate cards GM-1 to GM-5 |
| [base-overlaps.md](base-overlaps.md) | Branches, overlapping plans and what must change for Plan 91's move to Release 16 |
| [row-map.md](row-map.md) | Every Release 14 row and every `plan:39` issue: done, carried, dropped or moved |
| [audit.md](audit.md) | Plan 39's Release 14 rows checked against the code on `release/15/main` |
