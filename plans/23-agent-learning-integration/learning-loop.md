# Agent learning loop — local memory and shared Hiveminds

**Status:** Plan 23's proposed end-user behavior for [Collective Intelligence](../../visions/pillars/compounding-intelligence.md), not a shipped workflow, mandatory always-on service, or implementation plan.

## The behavior, not the database

An Astrid agent should **routinely learn before, during and after useful work**. It should draw from the user's own previous attempts and from compatible community knowledge, then make actual outcomes available for future reuse. A person should not have to curate a knowledgebase manually to get the benefit.

| Moment | Agent behavior | What the user experiences |
| --- | --- | --- |
| **Before** work | `find` relevant local and permitted remote knowledge; `inspect` applicability, evidence, versions and competing advice | An informed plan with sources, caveats and available tools |
| **During** work | Use already-authorized tools and keep narrowly scoped observations/results (including failures) | The agent adapts to real evidence, not merely a retrieved assertion |
| **After** work | Extract a candidate lesson and evidence receipt; record it locally under explicit retention policy | Future attempts avoid rediscovering the same solution |
| **When worth sharing** | Prepare a redacted/generalized contribution with original sources, author, conditions and evidence | User approves an opt-in proposal; appropriate dataset editors decide acceptance |
| **As things change** | Check stale or contradicted guidance when a relevant model, dependency, test or result changes; surface review needs | Guidance remains contextual and correctable rather than accumulating as folklore |

“Constantly” means **native to normal work** and optionally revisited on meaningful events, not indiscriminate background surveillance, unconditional model training, or sending every prompt to a public server.

## Three distinct layers

### 1. Personal or team Hivemind (local/private)

A local dataset can retain project-specific methods, private run receipts, debugging lessons, preferences *where authorized*, and relationships to external knowledge. It is **owned and permissioned by its user/team**. An agent may search it with the user's existing scope; private material is never uploaded by default.

Local *knowledge* is not the same as live **project state**. Astrid Runtime remains the owner of timelines, media, task execution and artifacts. The Hivemind layer captures the **meaning of what was learned**, with references or hashes to authorized Runtime objects, rather than becoming a shadow editor database.

A local Hivemind may be stored on-device or in a private service; this vision does not mandate one database engine or equate every agent scratchpad with a curated knowledge record.

### 2. Federated datasets and community knowledge

Banodoco Hivemind, a private studio dataset and other project/community datasets can each remain authoritative over their own records, access policy and editorial endorsements. A shared protocol would let them **cite or reference** each other's knowledge without merging into a central store.

The agent can query the datasets it has permission to access, resolving identity, source scope and evidence quality. A private studio can optionally share a **sanitized finding or proof-of-run receipt**, without publishing its raw logs, prompts or media.

A public community's acceptance or “canonical” status is an *editorial signal inside that dataset*, not universal truth and never authority over the user's machine.

### 3. The agent's contextual decision layer

The agent ranks or interprets findings **for this task and environment**, with sources, tested conditions, recency, counterexamples and uncertainty; it then chooses or proposes the relevant Astrid capabilities (packs, components, tools and workflows). Community material is evidence/data, **not instructions or permission to execute**.

Knowledge should inform the same capability discovery and validated domain operations used by the Liquid Software experience, without duplicating the domain/tool registries.

## A learning receipt

Useful receipts should identify *what was tried*, *where*, *which exact tool/model/workflow versions*, *what was observed* and *whether it helped*. Preserve reported versus observed versus inferred basis; don't turn an agent's explanation into fabricated test evidence.

Source pointers, hashes, provenance and a reviewable summary are preferable to dumping full private sessions. If even a summarized receipt could reveal sensitive information, keep it local.

## Example: a music edit

1. The agent checks its private experience plus authorized community guides for beat analysis and timeline alignment.
2. It discovers a suitable Astrid Music capability and helps create a beat-synced editing workspace.
3. A real attempt produces a versioned beat grid, an edit proposal, user corrections and an observed outcome.
4. A scoped local lesson is retained—e.g., that a certain downbeat detector misidentified a syncopated track, with the conditions and correction.
5. If generally useful, a **proposed, sanitized contribution** is offered to a relevant dataset; it is not automatically endorsed or published.
6. A later agent can retrieve this alongside competing evidence, avoiding a repeated mistake.

## First decisive proof

Use **one local/private dataset and Banodoco Hivemind**, one real creative task and two agent sessions. Show that an agent:

- retrieves a source-and-revision-pinned applicable method;
- executes only already-authorized capabilities;
- records a truthful local success/failure receipt;
- proposes a sanitized contribution with explicit approval;
- and, after review/acceptance, a second agent can retrieve and apply the contribution with accurate scope.

Measure decision quality against **no knowledge** and **raw search**. Demonstrate rejection/no-share paths, stale-method detection and no leak of private artifacts. Only then generalize federation across more datasets.

## Related material

- [Hivemind protocol proposal](../22-hivemind-protocol/protocol-proposal.md): suggested entry/link/scope/access records, cross-dataset references and `find`/`inspect`/`contribute`.
- [Source map](../22-hivemind-protocol/inputs.md): distinguishes current Banodoco Hivemind implementation from the protocol proposal.
- [Agent learning gap](../../visions/gaps/CI-001-agent-learning-loop.md): the current limitation and closure evidence.
