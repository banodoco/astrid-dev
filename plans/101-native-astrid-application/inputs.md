# Inputs — One native Astrid application

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Direction agreed in owner conversation, 2026-11-26: pursue a Rust native foundation, shared timeline semantics, React and managed Python/Node, replaceable agents, common local/cloud architecture. Recorded in [idea #2038](https://github.com/banodoco/astrid-dev/issues/2038). Pending — this precise independent project scope, overlap disposition and release placement have not been independently reviewed or approved. Next: review these documents and obtain the specific scope decision.

**Prior art:** Pinned App public/install, scripts/dev-local-workspace.mjs and install-manifest.json; Agent astrid/installer/{core,launcher,service,runtime_lifecycle,update_job}.py; Runtime bootstrap.py, profile-services docs and portability tests. See Plan 100 architecture. [Architecture proposal](../100-language-independent-foundation/architecture.md) records dated source observations, not live qualification.

**Approach:** Native independent recovery/bootstrap is valuable before rewriting core. Preserve existing transaction owner while delegating, then transfer and remove redundant paths. Prefer static hosting and optional thin desktop shell over new frontend. Test Tauri OS webviews versus Chromium where playback/rendering matters.

**Challenge:** Pending — this is material architecture with cross-repo risks. Next: independent advisor checks actual code, source identities, alternative reuse/deletions, dependency/ownership map, overlap with accepted plans, security and negative proof; record findings and accepted/rejected dispositions here. This author is not an independent reviewer.

**Proof and limits:** Completion in [plan.md](plan.md#completion) names positive and negative product evidence. Source review only, no executed tests or product qualification; selected release pins and actual fixtures must be refreshed, installed and recorded before implementation or acceptance. No inference of GPU, platform or migration support from CPU or source inspection.

**Review rounds:** Pending — propose one early load-bearing review stop and up to three final independent review rounds due to cross-repo contracts and user-work/security risks; next: owner agrees exact bounds and advisor.

**Run start:** Pending — no run is authorized. Next: owner records date, accountable session, accepted scope, release branches and limits on product work, hardware/spend, migration and promotion.

## Owner decisions

- **D1 — Pending (26 November 2026):** Supported OS/architecture matrix, distribution channels, code signing/notarization and minimum platform versions; recommend Windows/Linux/macOS declared subsets with native qualification.
- **D2 — Pending (26 November 2026):** Desktop shell selection after media/webview compatibility spike; do not force a single OS webview or ship a second React product.
- **D3 — Pending (26 November 2026):** Installation custody and adoption boundary including external managers and rollback eligibility; approve only after Plan 100 contract review.

## Source identities

Planning reference observations (not a run base): Runtime `686ca695469bda48cd40a70824c4ccef2a137284`, Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, Dev `890f8acafa2cd5b5e0b68dbc2d1576e0f7856202`. See [Architecture proposal](../100-language-independent-foundation/architecture.md) for exact file links. Pin the integrated published/candidate tuple, retained work, actual dependencies and selected release branch bases before code; no release assigned, no product branches authorized.

## References

- [Architecture proposal](../100-language-independent-foundation/architecture.md) — common rationale, source findings, cross-project requirements, alternatives and sequencing.
- [LS-006](../../vision/gaps/LS-006-independent-creative-foundation.md) — independently assessable outcome and closure route.
- [Idea #2038](https://github.com/banodoco/astrid-dev/issues/2038) — owner direction and coordination reference.
- [Planning workstream](../../agent/shared/workstreams/plan.md) and [strategy](../../strategy.md).
