# Tasks — A native authoritative workspace runtime

[Plan](plan.md) · [Inputs](inputs.md)

**Draft task outline:** no implementation or dispatch authorized. Before dispatch, replace broad candidate scopes with exact permitted files, pinned source/dependency identities, real focused commands, route decisions and accepted review bounds. Each proof below is a required observable result, not an executed test.

**Task ids:** NR-1 onward. **Critical path:** NR-1 → NR-2 → RS1 → NR-3/NR-4 → NR-5 → NR-6 → NR-7 → R. **Test inventory:** Runtime tests/test_a5_runtime_conformance.py, test_runtime_e2e.py, test_runtime_upgrade.py, test_portable_lifecycle.py, test_native_custody.py, platform/filesystem, backup/restore, task/lease, commit/crash tests and Plan 100 corpus. Re-inventory unit vs black-box before dispatch.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| NR-1 Map core invariants, schemas and baseline | X | Plan 100 | Runtime source/contracts/test inventory; design | Exact data format and behavior map, native platform guarantees, conformance coverage and migration alternatives. | [ ] |
| NR-2 Build native read-only vertical slice | X | NR-1 | Rust contract, API, store/CAS and auth crates | Native headless read/health and unauthorized refusal against copied fixture; no writer coexistence. | [ ] |
| RS1 Review stop — contract/ownership before implementation (proposed one round) | S | NR-1, NR-2 | read-only | Independent critique of source, authority, parity/negative evidence and overlap; resolve findings before downstream tasks. | [ ] |
| NR-3 Implement durable workspace writes and history | X | NR-2, RS1 | Rust storage/event/idempotency/backup crates | Atomic state writes, revision/receipt, backup/restore and crash tests match reference. | [ ] |
| NR-4 Implement task and process/worker authority | X | NR-2, RS1 | Rust execution/custody/task/auth modules | Lease/fence/cancel/retry; native handle proof and denied scope/duplicate settlement cases. | [ ] |
| NR-5 Integrate native timeline and clients | X | NR-3, Plan 102 | Rust commit coordinator, public API and adapters | Same command corpus and authoritative events/undo, no client DB writes. | [ ] |
| NR-6 Prove safe migration and rollback | X | NR-3, NR-4, NR-5 | Migration/controller adapter and isolated candidate roots | Realistic data copy hashes, interrupted switch, refused concurrent owner and schema downgrade, safe recovery. | [ ] |
| NR-7 Integrated parity and qualified cutover proposal | X | NR-6, Plan 101 | Native distribution and supported product journeys | All reference corpus + platform matrix; actual performance baselines; independent approval before any live cutover. | [ ] |
| R Review rounds (proposed at most 3, owner confirmation pending) | S | all other tasks | read-only | Review exact integrated candidate, claims, tests, limits and retained authority per [run contract](../../agent/shared/run-contract.md#review-and-promotion-boundaries); findings become bounded rows. | [ ] |

Do not start product work, choose a release branch, rent hardware or migrate live user data from this outline. Reuse existing owner plans and do not weaken tests. Scope overlaps and exact proof commands must be resolved at review before dispatch.
