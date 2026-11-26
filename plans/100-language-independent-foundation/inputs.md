# Inputs — A language-independent foundation

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — Direction agreed in owner conversation, 2026-11-26: pursue a Rust native foundation, shared timeline semantics, React and managed Python/Node, replaceable agents, common local/cloud architecture. Recorded in [idea #2038](https://github.com/banodoco/astrid-dev/issues/2038). This precise independent project scope, overlap disposition and release placement have not been independently reviewed or approved. Next: review these documents and obtain the specific scope decision.

**Prior art:** Runtime contract/README.md, daemon.py, timeline_commit_provider.py and Agent generic_host.py show the public/private split; App dev-local-workspace.mjs and Agent installer/runtime_lifecycle.py show lifecycle crossings. See architecture.md for pinned sources and Plans 38, 50, 83, 39/91. [Architecture proposal](architecture.md) records dated source observations, not live qualification.

**Approach:** Preserve the existing contract and implementation as a behavioural reference. Compare a Python support library with process/API boundary by primitive; use local native handles where required, but move shared authoritative operations behind a documented interface. Reject a second generic transport or blind FFI wrapper if it creates another owner.

**Challenge:** Pending — this is material architecture with cross-repo risks. Next: independent advisor checks actual code, source identities, alternative reuse/deletions, dependency/ownership map, overlap with accepted plans, security and negative proof; record findings and accepted/rejected dispositions here. This author is not an independent reviewer.

**Proof and limits:** Completion in [plan.md](plan.md#completion) names positive and negative product evidence. Source review only, no executed tests or product qualification; selected release pins and actual fixtures must be refreshed, installed and recorded before implementation or acceptance. No inference of GPU, platform or migration support from CPU or source inspection.

**Review rounds:** Pending — propose one early load-bearing review stop and up to three final independent review rounds due to cross-repo contracts and user-work/security risks; next: owner agrees exact bounds and advisor.

**Run start:** Pending — no run is authorized. Next: owner records date, accountable session, accepted scope, release branches and limits on product work, hardware/spend, migration and promotion.

## Owner decisions

- **D1 — Pending (26 November 2026):** Which cross-repo boundaries and compatibility floor are in the first independently useful scope? Recommend current supported release plus next candidate; no historical versions by default.
- **D2 — Pending (26 November 2026):** Worker and timeline ABI: use versioned typed command/receipt contracts; retain local handle transfer via minimal reviewed OS-specific ABI. Reject direct DB access.
- **D4 — Pending (26 November 2026):** Select one minimal independent non-video resource witness and decide the actual common resource/operation boundary; do not authorize a full canvas or universal engine. Coordinate Plan 46 session-targeted UI operations and Plan 57 extension storage.
- **D3 — Pending (26 November 2026):** Whether already planned work should absorb any slice: require an ownership/reuse disposition for Plans 38, 50 and 83 before changing their scope.
- **D5 — Decided (26 November 2026):** Owner directed that the architectural investigation be its own plan. [Plan 106](../106-creative-foundation-investigation/plan.md) owns the original NF-1a–NF-1j research scope (now FI-1–FI-10 and R), independently reviewed findings and 8–12 day allowance. Plan 100 waits on that handoff and keeps only NF-1 verification/refresh plus its contract/conformance/implementation tasks; provisional remaining estimate 12–28 days, combined allowance unchanged. No product run, release assignment or gap closure authorized.

## Source identities

Planning reference observations (not a run base): Runtime `686ca695469bda48cd40a70824c4ccef2a137284`, Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, Dev `890f8acafa2cd5b5e0b68dbc2d1576e0f7856202`. See [Architecture proposal](architecture.md) for exact file links. Pin the integrated published/candidate tuple, retained work, actual dependencies and selected release branch bases before code; no release assigned, no product branches authorized.

## References

- [Architecture proposal](architecture.md) — common rationale, source findings, cross-project requirements, alternatives and sequencing.
- [Plan 106 investigation](../106-creative-foundation-investigation/plan.md) — standalone research dependency, source-backed lanes, independent-tool test and reviewed decision pack; research progress belongs in that plan.
- [LS-006](../../vision/gaps/LS-006-independent-creative-foundation.md) — independently assessable outcome and closure route.
- [Idea #2038](https://github.com/banodoco/astrid-dev/issues/2038) — owner direction and coordination reference.
- [Planning workstream](../../agent/shared/workstreams/plan.md) and [strategy](../../strategy.md).
