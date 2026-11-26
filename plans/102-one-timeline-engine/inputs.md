# Inputs — One native timeline engine

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Direction agreed in owner conversation, 2026-11-26: pursue a Rust native foundation, shared timeline semantics, React and managed Python/Node, replaceable agents, common local/cloud architecture. Recorded in [idea #2038](https://github.com/banodoco/astrid-dev/issues/2038). Pending — this precise independent project scope, overlap disposition and release placement have not been independently reviewed or approved. Next: review these documents and obtain the specific scope decision.

**Prior art:** Pinned Runtime timeline_commit_provider.py, timeline_commit_port.py, timeline_commit_auth.py/store.py and contract schemas; Agent astrid/sdk/timeline/commit.py; App timeline SDK and Remotion. Existing Plans 18, 63, 75, 76, 77, 86, 88, 89. See architecture. [Architecture proposal](../100-language-independent-foundation/architecture.md) records dated source observations, not live qualification.

**Approach:** Single pure Rust semantic kernel; current Python provider behind an adapter during parity qualification; existing protocol remains authoritative. Alternative persistent Python service is an intermediate only if it simplifies the seam; reject costly leaf-by-leaf RPC and independent client commits.

**Challenge:** Pending — this is material architecture with cross-repo risks. Next: independent advisor checks actual code, source identities, alternative reuse/deletions, dependency/ownership map, overlap with accepted plans, security and negative proof; record findings and accepted/rejected dispositions here. This author is not an independent reviewer.

**Proof and limits:** Completion in [plan.md](plan.md#completion) names positive and negative product evidence. Source review only, no executed tests or product qualification; selected release pins and actual fixtures must be refreshed, installed and recorded before implementation or acceptance. No inference of GPU, platform or migration support from CPU or source inspection.

**Review rounds:** Pending — propose one early load-bearing review stop and up to three final independent review rounds due to cross-repo contracts and user-work/security risks; next: owner agrees exact bounds and advisor.

**Run start:** Pending — no run is authorized. Next: owner records date, accountable session, accepted scope, release branches and limits on product work, hardware/spend, migration and promotion.

## Owner decisions

- **D1 — Pending (26 November 2026):** Exact semantic contract, supported command floor and numeric time/rounding representation; preserve accepted behavior unless a reviewed change explicitly revises it.
- **D2 — Pending (26 November 2026):** Transition ABI (pure FFI vs coarse-grained service) and optional browser WASM/Python bindings; measure before adding bindings.
- **D3 — Pending (26 November 2026):** Which timeline performance gates and fixture/revision constitute acceptance; reuse current approved gates rather than inventing optimistic targets.

## Source identities

Planning reference observations (not a run base): Runtime `686ca695469bda48cd40a70824c4ccef2a137284`, Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, Dev `890f8acafa2cd5b5e0b68dbc2d1576e0f7856202`. See [Architecture proposal](../100-language-independent-foundation/architecture.md) for exact file links. Pin the integrated published/candidate tuple, retained work, actual dependencies and selected release branch bases before code; no release assigned, no product branches authorized.

## References

- [Architecture proposal](../100-language-independent-foundation/architecture.md) — common rationale, source findings, cross-project requirements, alternatives and sequencing.
- [LS-006](../../vision/gaps/LS-006-independent-creative-foundation.md) — independently assessable outcome and closure route.
- [Idea #2038](https://github.com/banodoco/astrid-dev/issues/2038) — owner direction and coordination reference.
- [Planning workstream](../../agent/shared/workstreams/plan.md) and [strategy](../../strategy.md).
