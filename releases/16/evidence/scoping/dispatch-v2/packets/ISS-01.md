# ISS-01 — Issue-first: install, updates, Pinokio and persistent state

**Route:** N — Normal ChatGPT Chat — High reasoning  
**Wave:** A  
**Depends on:** CTX-00  
**Return:** Push your full original Markdown report to the report-only branch/path and draft PR destination named at dispatch. Verify remote readback and post `READY-REPORT <repo> <PR> <head> <report-path>` in STATUS. Follow `../README.md`.
**Authority:** Read-only against investigated sources and proposal; write only the explicitly assigned report path on your dedicated evidence branch, open its draft evidence PR and post mailbox STATUS. No implementation, merge or publication. 

Read the shared procedure and context in `../README.md` and `../context.md`. Preserve earlier actual assignments if already dispatched.

## Assignment

**Problem-first scope:** Install, bootstrap, permissions, disk, locked files, upgrades, rollback, repair, uninstall, version mismatch, defaults, retained preferences, launcher controls and lived-in state.

**Repos:** astrid-dev, astrid-agent, astrid-runtime, astrid-app, astrid-pinokio. Begin without reading the included-plan list in detail: start with issue queries, tester reports, previous release qualification, incident notes, support reports, linked code and PRs. Read actual relevant issue bodies and meaningful comments; query across labels (plan/gap/release/bug/observation/usertest) AND free-text synonyms; include open, closed, reopened and unlabeled issues. Follow links and duplicate chains. Sample recent changes, then search older known symptoms; paginate, record query, result counts, covered pages and limits. Do not treat coordination boards as bug tasks. Look for repeated symptoms with common root cause. Verify likely fixes by exact current code and real proof; do not trust issue state alone.

Only after the independent problem inventory, map problems to R16 plan owners/tasks or a bounded release issue. Flag uncovered/partially covered problems, new dependability risks and duplicated work, distinguish actual harm from performance/feature desire and general green-suite debt. Use later R17/R18 only where the R16 promise remains sound. Experimental RunPod safety still matters. Prioritize 5–10 highest-impact uncovered gaps, but include all relevant dispositions.

**Seeds to cross-check after independent pass:** [#579](https://github.com/banodoco/astrid-dev/issues/579), [#584](https://github.com/banodoco/astrid-dev/issues/584), [#679](https://github.com/banodoco/astrid-dev/issues/679), [#815](https://github.com/banodoco/astrid-dev/issues/815), [#816](https://github.com/banodoco/astrid-dev/issues/816), [#1206](https://github.com/banodoco/astrid-dev/issues/1206), [#1525](https://github.com/banodoco/astrid-dev/issues/1525), [#1729](https://github.com/banodoco/astrid-dev/issues/1729), [#723](https://github.com/banodoco/astrid-dev/issues/723). For media also inspect astrid-app #252/#255. These are not exhaustive.

**Deliverable:** detailed issue ledger with repository/number/URL, state/date, symptom, root cause or unknown, severity, relevant current ref/proof, related issues, owning existing task or proposed bounded fix, disposition, and qualification impact. List unscouted areas and search coverage. No issue changes.

## Deliverable

Return the complete source-linked findings and concrete amendments using the shared report shape in `../README.md`.
