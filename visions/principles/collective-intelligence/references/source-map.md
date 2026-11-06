# Source map — Collective Intelligence and Hivemind

**Reviewed:** 2026-11-06. This document distinguishes (a) an uploaded **protocol proposal**, (b) a repository's **currently documented implementation**, and (c) the **proposed Astrid learning experience**. None should be conflated with another. Deployment and test status were not independently verified.

## Design source supplied for this vision

- [**The Hivemind protocol, proven on Banodoco Hivemind**](hivemind-protocol-proposal.md), dated **2026-10-29** and attributed in the source to **@Hannah O'Malley**. Preserved as supplied, with a short explicit status preface.
- It proposes an interoperable, dataset-owned knowledge protocol:
  - **Entry**, **Link**, **Scope**, **Access** records; immutable attributed material, provenance and conditions;
  - relations **cites**, **carries**, **supports**, **opposes**, **qualifies**, **supersedes**;
  - operations **`find`**, **`inspect`**, **`contribute`**, callable over HTTP/MCP;
  - **independent private, local and public datasets** that can cross-reference without merging;
  - agent contributions and sanitized run receipts, editorial review, rechecks and user/data-owner authority.
- Its numerical corpus figures, reported translation/reply-link evaluation, operational risk statements, suggested review cadences and migration steps are **claims or intentions in that dated document**, not independently verified in this assessment. In particular, do not treat its proposed API, schema, public-read changes, IP-address concern or compatible-view migration as implemented.

## Source-verified current foundations

| Source | Pinned identity | Observed in current source | Still to establish |
| --- | --- | --- | --- |
| [Banodoco Hivemind README](https://github.com/banodoco/hivemind/blob/2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc/README.md) | [Hivemind `main` `2efd9ce`](https://github.com/banodoco/hivemind/tree/2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc) | Discord `message_feed`, `resources`, immutable `resource_revisions`, accepted current-head search; `search` and `get_item` executors; locked `contribute` actions and editorial decisions | Local/federated Hivemind datasets, proposed `find`/`inspect`/`contribute` protocol surface and default agent learning |
| [Hivemind DESIGN.md](https://github.com/banodoco/hivemind/blob/2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc/DESIGN.md) | Same | Typed derived `knowledge_references`, message snapshots, evidence basis, revision-pinned ranking and editor acceptance | Generic federated link semantics, independent dataset trust and transport contract |
| [VibeComfy workflow semantics](https://github.com/banodoco/hivemind/blob/2efd9ce7e17e19f3e7820374ddfd566cb0b4adbc/docs/vibecomfy_workflow_semantics.md) | Same | Task type, model family, dependencies, provenance and structured conditions for workflow matching | Generality across arbitrary resources/models and tested agent choice quality |
| [Astrid Agent pack authoring](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/docs/packs/creating-packs.md) | Agent `main` `9f42441` | Packs can declare actions, skills, UI, rendering, documents and discovery metadata | Hivemind as the underlying knowledge source for agents or automatic two-way learning |
| [Astrid Runtime](https://github.com/banodoco/astrid-runtime/blob/9fc53b771134940aaac901e4cfc5d03c1db1a20a/README.md) | Runtime `main` `9fc53b7` | Canonical workspace/task/artifact authority and versioned client contracts | A knowledge dataset, a federation protocol or permission to publish local history |
| [Astrid Dev extensibility philosophy](../../../../docs/extensibility-philosophy.md) | Dev `main` `17ec8fc` before the draft | Collective, agent-shaped creative tooling | End-to-end distributed knowledge learning, capture and approved contribution |

## Important design divergence

The October 29 protocol proposal's **immutable entries + typed links + dataset-wide `find/inspect/contribute`** is *not identical* to Hivemind's currently documented **stable resources + full-content immutable revisions + current accepted head + `search/get_item` and distinct contribution actions**. Nor does the proposal's legacy-view migration map automatically follow from the implementation's conversion boundary, which documents no compatibility shims/dual writes.

Reconcile these deliberately in Hivemind's own plan and tests. Do not label both “implemented” or invent an always-present universal knowledge API. A compatibility adapter might be appropriate, but only after deciding exact identity, versioning, access and migration semantics.

## Integration implications

A local personal/team Hivemind should be a **first-class private dataset**; it can federate with Banodoco and others by policy and shared identities, not by copying all knowledge to a central server. Astrid agents should make retrieval and evidence capture routine, with user-controlled disclosure and publication. The knowledge store does not replace Runtime's live project/task authority. Agents use retrieved evidence as **data**, not permission or executable instructions.

See [the agent-learning loop](agent-learning-loop.md) for the desired behavior and [the bridge](../bridge.md) for a bounded proof and links to existing plans.
