# 23 — Continuous agent learning in creative workflows

**Project:** Continuous agent learning

**Goal:** Make retrieval, observed local learning and optional contributions a real Astrid Agent workflow.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** scope agreement; approved knowledge API

**Start here:** read [Astrid development skill](../../skills/astrid-dev/SKILL.md), the [shared run contract](../../skills/astrid-dev-shared/run-contract.md), and this project's [tasks](tasks.md) and [inputs](inputs.md). Current status, owner and estimate live in the [project queue](../../README.md).

**Vision gaps:** [CI-001 — Agents learn from real creative work](../../vision/gaps/CI-001-agent-learning-loop.md) (primary); [CI-002 — Interoperable Hiveminds](../../vision/gaps/CI-002-federated-knowledge.md) (supporting dependency). This plan integrates learning; it does not own the underlying protocol.

## Goal and scope

Make **learning from prior experience** a normal, verifiable part of using Astrid Agent: before a creative task, retrieve and inspect relevant local/authorized community knowledge; during work, record actual outcomes; after work, retain a scoped private lesson and optionally propose a sanitized contribution to a broader Hivemind. The agent then benefits from that knowledge in a later session.

This plan integrates the experience; [Plan 22](../22-hivemind-protocol/plan.md) owns the underlying dataset/protocol contract. Do not create a second knowledge protocol or duplicate Hivemind's corpus/editing authority. Reuse Astrid Agent's existing pack and skill discovery and Runtime's task/artifact receipts.

**Included:** a narrow agent-facing knowledge adapter using selected existing or proven protocol operations, context-aware applicability checks, evidence/receipts, a private retention policy, proposal-only contribution with permission and review, one creator-facing retrieval explanation, and a two-session end-to-end proof.

**Deferred:** training models on private user data, universal session recording, always-on background surveillance, automatic public publishing, generalized marketplace search, and full integration into every Astrid task at once.

## Proposed sequence

1. **Define a real user journey.** Pick one creative workflow (e.g. music-assisted timeline editing or VibeComfy model troubleshooting) and record baseline outcomes without Hivemind knowledge.
2. **Connect an authorized read surface.** Use existing Banodoco read operations or Plan 22's verified API; inspect revision, provenance, model/version/environment and counterevidence before recommending an action.
3. **Capture a truthful local receipt.** Link the actual action, versions, environment and observed result to a private knowledge candidate without exporting raw project data.
4. **Propose optional sharing.** Show exactly what a sanitized candidate contains; user approval and dataset editorial acceptance are separate.
5. **Demonstrate compounded intelligence.** A fresh agent session uses the earlier evidence to make a better creative decision; compare against raw search and no knowledge, including permission denials/stale advice.

Agent capabilities should remain usable without Hivemind. Knowledge fetch latency/failure should degrade clearly and safely, not block unrelated creative work.

## Completion

A real Astrid Agent end-to-end journey shows **retrieve → apply → observe → learn locally → optionally contribute → reuse**, with attributable and scoped evidence, permissions and correct separation between knowledge recommendations and tool-execution authorization. A second session's improvement is measured. Dependencies, privacy constraints and unsupported modes are documented.

**Authorization:** Draft proposal only. Do not start product work from this document. Scope, owners, refs, test commands, acceptance and sequencing must be reconciled with Plans 22, 06, 18 and existing Agent/Hivemind roadmaps.
