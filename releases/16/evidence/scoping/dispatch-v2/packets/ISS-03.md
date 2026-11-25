# ISS-03 — Issue-first: editing, media, rendering and project custody

**Route:** N — Normal ChatGPT Chat — High reasoning  
**Wave:** A  
**Depends on:** CTX-00  
**Return:** Push your full original Markdown report to the report-only branch/path and draft PR destination named at dispatch. Verify remote readback and post `READY-REPORT <repo> <PR> <head> <report-path>` in STATUS. Follow `../README.md`.
**Authority:** Read-only against investigated sources and proposal; write only the explicitly assigned report path on your dedicated evidence branch, open its draft evidence PR and post mailbox STATUS. No implementation, merge or publication. 

Read the shared procedure and context in `../README.md` and `../context.md`. Preserve earlier actual assignments if already dispatched.

## Assignment

**Problem-first scope:** Lost or rejected edits, corrupt/stuck saves, history/restore, conflicts, shared outboxes, project restart, imports and upload interruption, source files, wrong render/preview/audio, cancel/recovery and retained outputs.

**Repos:** astrid-dev, astrid-app, astrid-agent, astrid-runtime. Begin without reading the included-plan list in detail: start with issue queries, tester reports, previous release qualification, incident notes, support reports, linked code and PRs. Read actual relevant issue bodies and meaningful comments; query across labels (plan/gap/release/bug/observation/usertest) AND free-text synonyms; include open, closed, reopened and unlabeled issues. Follow links and duplicate chains. Sample recent changes, then search older known symptoms; paginate, record query, result counts, covered pages and limits. Do not treat coordination boards as bug tasks. Look for repeated symptoms with common root cause. Verify likely fixes by exact current code and real proof; do not trust issue state alone.

Only after the independent problem inventory, map problems to R16 plan owners/tasks or a bounded release issue. Flag uncovered/partially covered problems, new dependability risks and duplicated work, distinguish actual harm from performance/feature desire and general green-suite debt. Use later R17/R18 only where the R16 promise remains sound. Experimental RunPod safety still matters. Prioritize 5–10 highest-impact uncovered gaps, but include all relevant dispositions.

**Seeds to cross-check after independent pass:** [#732](https://github.com/banodoco/astrid-dev/issues/732), [#720](https://github.com/banodoco/astrid-dev/issues/720), [#1246](https://github.com/banodoco/astrid-dev/issues/1246), [#1401](https://github.com/banodoco/astrid-dev/issues/1401), [#1402](https://github.com/banodoco/astrid-dev/issues/1402), [#1480](https://github.com/banodoco/astrid-dev/issues/1480), [#1690](https://github.com/banodoco/astrid-dev/issues/1690), [#1561](https://github.com/banodoco/astrid-dev/issues/1561), [#1793](https://github.com/banodoco/astrid-dev/issues/1793), [#1235](https://github.com/banodoco/astrid-dev/issues/1235), [#1237](https://github.com/banodoco/astrid-dev/issues/1237), [#1938](https://github.com/banodoco/astrid-dev/issues/1938), [#1931](https://github.com/banodoco/astrid-dev/issues/1931), [#1909](https://github.com/banodoco/astrid-dev/issues/1909), [#1916](https://github.com/banodoco/astrid-dev/issues/1916), [#1915](https://github.com/banodoco/astrid-dev/issues/1915), [#1514](https://github.com/banodoco/astrid-dev/issues/1514), [#1476](https://github.com/banodoco/astrid-dev/issues/1476), [#1515](https://github.com/banodoco/astrid-dev/issues/1515). For media also inspect astrid-app #252/#255. These are not exhaustive.

**Deliverable:** detailed issue ledger with repository/number/URL, state/date, symptom, root cause or unknown, severity, relevant current ref/proof, related issues, owning existing task or proposed bounded fix, disposition, and qualification impact. List unscouted areas and search coverage. No issue changes.

## Deliverable

Return the complete source-linked findings and concrete amendments using the shared report shape in `../README.md`.
