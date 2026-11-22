# PL-1 route N verification

Candidate `05f5ce4bfdfbd1feb65bf869a9e18f19c1b98992` (source ref `plan-84/pl-1-verify`), base `e3dbad64d402724ac5a35fb6447f18e432c64b78`. Verified worktree was clean at the candidate SHA. No product files were edited and no commits were made. `node_modules` is an ignored symlink to `worktrees/baseline/node_modules`; package-lock SHA256 matches both worktrees (`673357a32cbfba73c60a266338b8eddf524a2c60738374076f1b91d8182eda8d`).

## Focused checks

| Check | Exact command | Inner result |
| --- | --- | --- |
| Component boundary | `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/pages/Home/planet/PublicAstridPlanet.test.tsx` | **PASS**, exit 0; 1 file, 1 test passed. Raw output: `vitest.log`. |
| ESLint | `./node_modules/.bin/eslint src/pages/Home/PublicAstridVision.tsx src/pages/Home/planet --ext ts,tsx --report-unused-disable-directives --max-warnings 0` | **PASS**, exit 0, no output. Raw output: `eslint-corrected.log`. The first invocation used the brief's unsupported `--report-unused-directives`; ESLint rejected the option before running. That attempt is retained as `eslint.log`; the corrected scoped command above passed. |
| TypeScript | `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit` | Exit 2 with the same eight TS diagnostics as baseline; **no new diagnostics**. Exact diagnostic-line comparison to `run/evidence/baseline/checks/app-tsc.log` is equal and `tsc-baseline-diff.log` is empty. Raw output: `tsc.log`. This remains a pre-existing check failure, not a green typecheck. |

## Evidence integrity and focused probes

- Candidate source-map graph: `python3 run/evidence/pl-1/graph.py` exited 0 against the existing production `dist` for this SHA. `graph.log` shows the only mapped chunk containing both Three source modules and `planetEngine.ts`; captured production URLs show 0 such chunk requests for Home and reduced-motion Vision, and 1 for normal Vision. Original network records are `run/evidence/pl-1/network-{home,still,normal}.json`; source: `run/evidence/pl-1/graph.py`.
- Pixel-count gate fault injection used synthetic images under `/tmp`, without changing the original gate or its fixtures. The gate accepts identical nonempty inputs (exit 0), rejects a 64/121-pixel difference above threshold (exit 1), and rejects both-empty inputs (exit 1). Exact output: `pixel-fault-gates.log`.
- Resource-count gate fault injection ran the existing `audit.cjs` predicate with an injected created/disposed imbalance in mount 4. Healthy fake counts exit 0; the injected imbalance is rejected at the real predicate with exit 1. Outputs: `audit-fault-free.log` and `audit-injected-imbalance.log`.
- Candidate code inspection: all 365 geometry, 197 material, 5 texture, 1 render-target and 1 skeleton constructors use the engine's `own(...)` accounting wrapper. The 8 event-listener registrations have matching removals; the engine contains one `window.setTimeout` call site, RAF and WebGL2 sync handling covered by `cleanup.cjs`, and no interval or observer call sites. This is source coverage inspection, not a separate runtime test.
- Existing raw evidence is in `run/evidence/pl-1/`: the five donor/App image pairs and `diff-results.json` pass the fixed 0.5% threshold; `audit.log` records ten mounts with equal created/disposed counts and zero live resources; `cleanup.log` records zero tracked listeners, timers, RAFs and syncs after ten disposals; `production.log` records the production requests. These browser captures/audits were not rerun because candidate bytes and relevant inputs are unchanged. Manager visual review is in `manager-verdicts.md`; this verifier makes no taste judgment.

SHA256 anchors: candidate `planetEngine.ts` `e5f33c0be699ae888ad1f7cbf150e6622fd489b8b28f5f595f924fbdf2afe819`; comparison gate `diff.py` `fcecde12f0acb2018ce4e868e8ce99c6cda3604c40a9b0cf46527c9b4ebe9bc0`; original pixel results `diff-results.json` `6af4441c5eb915414701e9276d6b1cc4712e8e68100976532c02b21aca1f7990`; production graph output `graph.log` is retained with this report.

## Limits

This run covers the named focused test, scoped lint, type diagnostic comparison, and integrity probes only. It does not establish that the repository test suite passes, and the TypeScript check is still red from its eight unchanged baseline errors. The manager owns visual acceptance; PL-2/PL-3 page composition, later PL-1 dependent behaviors and integration checks remain outside this verification.
