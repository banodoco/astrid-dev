# INV-07 — Release 15 reconciliation and implementation sequence feasibility

**Route:** X — Normal ChatGPT Chat — Extra High reasoning  
**Wave:** B  
**Depends on:** SC-56;SC-63;SC-87;SC-85;SC-31;HOR-01;ISS-04  
**Return:** Push your full original Markdown report to the report-only branch/path and draft PR destination named at dispatch. Verify remote readback and post `READY-REPORT <repo> <PR> <head> <report-path>` in STATUS. Follow `../README.md`.
**Authority:** Read-only against investigated sources and proposal; write only the explicitly assigned report path on your dedicated evidence branch, open its draft evidence PR and post mailbox STATUS. No implementation, merge or publication. 

Read the shared procedure and context in `../README.md` and `../context.md`. Preserve earlier actual assignments if already dispatched.

## Assignment

Read every listed dependency report in full, including original evidence, and independently verify disputed material claims against code. Do not merely aggregate recommendations.

Read complete latest R15 run/qualification and active P56/77/78/81/82/87/88/89 branches and handoffs. Compare exact integration tuple, actual pins, pending PRs, incomplete qualification and accepted decisions. List what lands before R16, what is already satisfied, what must be re-measured, remaining defects by owner, shared-file/contract edges and evidence invalidation. Produce a provisional task-level dependency graph and lane reservations, early decisions/parallel starts, scarce machines/CI, handoff of P91 to R17 without altering active work. Include no future-release implementation and no assumption that a plan branch is shipped. Identify any sequencing contradiction which makes the proposed R16 independently unshippable.

### Sequence to the first minor

Account for Plan 31 and completed Plan 58 as described in the version/publication section of `../context.md`: order Plan 29, Plan 31 migration/go-live/version-display work, supported-route proof and the exact first minor publication. Include any real prerequisite requiring early owner decisions or capacity and distinguish the served legacy baseline, R15 product starting base and canonical planning/skill main. Do not assume R17 full-green or R18 features have shipped.

## Deliverable

Return the complete source-linked findings and concrete amendments using the shared report shape in `../README.md`.

## V4 sequencing input

Produce two or more plausible release-level sequences and compare what can start versus safely land, critical path with evidence/ranges, collisions, proof dependencies, first integrated user journeys, migration/rollback ordering, scarce test resources and the cost of waiting/rework. Distinguish integrated R15 baseline and served regression comparator. Name contract decisions to settle first and the concrete evidence that would change the preferred sequence. This is input to SYN, not a binding decision or another strategy document.
