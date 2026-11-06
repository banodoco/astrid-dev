# Bridge — Collective Intelligence: from separate knowledge stores to learning agents

**Purpose:** Connect the [Collective Intelligence principle](principle.md) to present Hivemind/Astrid capabilities and a first convincing demonstration. This is a living research/design bridge, **not** an approved implementation plan. Source claims are pinned in [references](references/source-map.md).

## Target behavior

Every Astrid agent should *naturally learn* before, during and after creative work. It uses relevant local/private and permitted wider knowledge, captures truthful results locally, and offers reusable findings back to appropriate community datasets with consent. Each Hivemind dataset retains its own authority. The system improves both **the individual agent's future decisions** and **the network's shared knowledge**.

The [uploaded 2026-10-29 Hivemind protocol proposal](references/hivemind-protocol-proposal.md) describes a possible cross-dataset format (entries, links, scopes, access) and `find`, `inspect`, `contribute` operations. It is **one enabling technical design**, not the overarching goal and not an implemented cross-dataset standard. See the [agent learning-loop reference](references/agent-learning-loop.md).

## What already exists

- **Banodoco Hivemind:** source-custodied Discord messages; versioned resources with one accepted current revision; reported/observed evidence; source-pinned retrieval and editor-controlled contribution operations; ingest paths for articles, workflows and YouTube. These are currently documented at a different data/API contract from the newer federated protocol proposal.
- **Astrid Agent:** pack/skill/action discovery and real creative execution, including versioned timeline commits and music analysis.
- **Astrid Runtime:** authoritative workspace projects, artifacts, tasks and receipts; a possible source of exact run outcomes, not a replacement for the Hivemind knowledge store.
- **Astrid App:** the user's editing and agent experience; a natural place to surface provenance, relevant discoveries and approval to share.

None of this establishes a live automatic local+community learning loop across all agents today.

## What needs to become true

| Seam | Required outcome | First proof |
| --- | --- | --- |
| **Local/private knowledge** | User/team owns a durable, searchable knowledge dataset with scoped agent access; no implicit public syncing | Two sessions: agent recalls a real earlier attempt from the user's private knowledge |
| **Knowledge-aware agents** | Relevant `find`/`inspect` becomes an ordinary step before action; sources, setup conditions, contradictions and confidence are visible | Agent uses a pinned technique for a matching environment, distinguishes evidence from instructions |
| **Run-to-knowledge capture** | Capture exact success/failure/conditions from real tools and Runtime receipts, not speculative summaries | Finished run creates a private, inspectable, evidence-linked candidate lesson |
| **Selective sharing** | Redact and generalize; user/team approves what can leave; dataset editor reviews proposals | Private lesson yields one sanitized contribution without raw media, prompts or logs escaping |
| **Dataset federation** | A local dataset can reference and query Banodoco or another dataset by stable identities, without merging ownership or access | Two independently owned datasets exchange a permitted citation or receipt; revoke/deny paths work |
| **Quality and upkeep** | Conflicts, rechecks, supersession, provenance and reviewer decisions remain explicit and recoverable | Failed receipt or dependency version change produces a review request, not silent endorsement |
| **Creative integration** | Retrieved knowledge helps agents select compatible packs/workflows; confirmed results improve later recommendations | Compare later creative decisions with raw-search and no-knowledge baselines |

## Proposed implementation path (subject to an owned plan)

**First vertical slice:** use an existing approved Astrid creative task, the current Banodoco Hivemind read path and a deliberately scoped private knowledge store. Prove **search → contextual selection → authorized action → observed local learning → approved contribution**. Don't begin with cross-community ingestion at scale.

**Second:** define the minimum interoperable representation and transport for cross-dataset references, consent and evidence, reconciling the protocol proposal with Hivemind's *current* resource/revision model. The proposal's six relations and `find`/`inspect`/`contribute` are candidate design choices, not pre-existing guarantees; migration and compatibility need separate decisions and focused evidence.

**Third:** broaden adapters and agent integration, introduce relevance-triggered rechecking, and test independent private/team/public deployments without accidentally creating a central knowledge authority.

**Acceptance criterion:** a second agent demonstrably benefits from an evidence-backed finding created during a first agent's work, while private records remain private and dataset editors retain final publication decisions.

## Relationship to existing plans

- [Astrid Dev Plan 06 — Packs](../../../plans/06-packs/plan.md): how discovered creative capabilities are distributed/installed, not the owner of community knowledge.
- [Plan 17 — VibeComfy extensibility](../../../plans/17-vibecomfy-extensibility/plan.md): a concrete creative-workflow case for knowledge application.
- [Plan 19 — First-principles documentation](../../../plans/19-first-principles-documentation/plan.md): agents' human-readable working guidance, not an interchangeable knowledge database.
- [Astrid Dev project queue](../../../README.md): no dedicated approved Collective Intelligence end-to-end project is recorded in this draft. New implementation scope would need its own agreement.
- [Banodoco Hivemind](https://github.com/banodoco/hivemind): owns its real corpus, data model, API and any migration work; do not override its repository-specific decisions from this vision document.

**Security/authority boundary:** Community records and model-generated notes never grant execution rights. Dataset visibility, contributor credit, source deletion requests, retention, permission to observe private actions, and user approval for sharing require explicit policy and tests. The protocol source mentions an IP-metadata concern and migration strategy; treat both as **claims/proposals to verify** against current code, not as verified defects or implementation orders.
