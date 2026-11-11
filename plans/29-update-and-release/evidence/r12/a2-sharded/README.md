# A2 controlled shard comparison

The orchestrator authorized a fresh four-side comparison in identical deterministic module groups after the unsharded candidate run was interrupted without an exit record. Old unsharded outputs are corroboration only. Each side uses its own verified pins, Python 3.11.17, the same selectors, execution mode and verified Node 22.22.0/esbuild 0.27.7, with unchanged test timeouts. Every group must produce a complete `-rA` summary, exit and SHA receipt before the next side; interrupted groups are not results.

Collection completed on all sides: R10 4,365 IDs, R11 4,823, base 5,110 and candidate 5,150; the union has 5,188. The [52-group manifest](final-batches.json) has SHA256 `885b264862a0e6e90698ed8a76a6b5b30e2dbeb1f3846ea96b356913b1a9e771`; adjacent absence lists make missing IDs explicit. Whole modules are grouped in fixed order across every side. Eleven oversized modules remain singletons; historical timing coverage is incomplete, so progress and process state must be checked at least every 60 seconds.

Group 001, `tests/core/execution/test_bug14_settlement_liveness.py`, completed on all four sides: each accounted for 18 IDs, with 17 passed and the same one failure (`test_conflict_fails_exact_owner_without_conflicting_evidence`, `DID NOT RAISE RuntimeError`), exit 1. This one group has no new failure by ID and message; it does not establish an overall verdict.

Each group restarts session-scoped fixtures. This method may miss cross-group ordering or fixture interactions and is not equivalent to a full-suite run. Full per-group logs and receipts, regression analysis, missing/no-baseline buckets and the final gate remain open.
