---
name: astrid-dev
description: Orient developers changing Astrid itself, identify repository ownership and pin order, and route new-project planning, implementation/debugging, or release work to the right workflow.
---

# Develop Astrid

Use this entrypoint for changes to Astrid's repositories, packs, skills, CI, or release machinery. For creative work made with Astrid, use the `astrid` skill.

## Repository map

| Repository | Owns | Pins / follows |
| --- | --- | --- |
| `banodoco/astrid-runtime` | Workspace Runtime: projects, media, timelines, tasks, runs, receipts/events, HTTP contract and generated clients | Integration tests pin Agent (`tests/astrid-agent.pin`) |
| `banodoco/astrid-agent` | Python package and CLI, SDK, packs, skills, installer, MCP server, Remotion renderer | Runtime in `runtime.lock.json`; vendored Python client |
| `banodoco/astrid-app` | Editor App and user-facing install manifest | Runtime lock/client and Agent + Runtime SHAs in `public/install-manifest.json` |
| `banodoco/astrid-pinokio` | Pinokio launcher and channels | Published tuple |

The normal pin order is **Runtime → Agent → App → Pinokio**. A Runtime change lands first; Agent updates its Runtime pin and generated client; App updates its Runtime pin/client and manifest; Pinokio follows the published tuple. Changes to an upstream pin or generated artifact can invalidate downstream evidence. Confirm current ownership, paths, and pin mechanisms in the working repositories before acting; this map is orientation, not a substitute for their instructions.

## Choose a workflow

- [Plan](../astrid-dev-plan/SKILL.md): genuinely new project or materially new scope; find prior art, challenge complexity, and agree the intended end state.
- [Iterate](../astrid-dev-iterate/SKILL.md): implement, debug, or repair one scoped feature through focused proof; return a candidate for integration.
- [Release](../astrid-dev-release/SKILL.md): integrate and recheck an accepted candidate, then perform only the explicitly authorized promotion or publication.

A repository plan already accepted does not need another planning agreement. This skill is orientation and routing only; it is not a second execution path. The exact identity, evidence, retry, review, and authority policy lives in the [shared run contract](../astrid-dev-shared/run-contract.md). Concise coordinator and advisor role references live in [roles](../astrid-dev-shared/roles/manager.md) and [roles](../astrid-dev-shared/roles/advisor.md). Plans split work into `N`/`X`/`S` tasks; hand each to a subagent on its route’s model (Haiku, Sonnet, Opus by default; see the [routing table](../astrid-dev-shared/run-contract.md#routing-and-bindings)).

## Source provenance

The repository ownership and pin-order summary was adapted from `banodoco/astrid-agent`'s developer skill at commit `43b6fb2cdb877afd6d37832c7f279754ba01592d` (2026-11-02). Verify it against the current product repositories before making a change.
