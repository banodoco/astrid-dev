# Into the Minkhole proof point

**Project:** Into the Minkhole proof point

**Goal:** A creator and an agent can finish Into the Minkhole in Astrid and repeat its voice-conditioned editing workflow on another timeline.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 30–45 engineering days, pending pilot and source recovery.

**Waiting on:** Owner's scope and release confirmation, review-round agreement, and run authorization.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

## Outcome and scope

Import both supplied timelines without overwriting work; inspect, edit, visualize and render them through Astrid. Make per-clip fit and crop explicit and independent, preserve a versioned legacy baseline, and prove preview, export and composed visualization agree. Enable source and generated word transcription, durable clip-specific intent and alignment, automatic masks, and a usable H3_AV editing procedure. Finish the parody and prove the reusable system with a fresh weaker agent on a different timeline. The reusable workflow matters most.

Use the existing packs, Runtime authority and timeline wherever possible. Fix blockers needed for this journey now; file durable or disproportionate adjacent problems for later. Full consolidation of the App renderer into the shared package is deferred unless small. Do not treat CPU fixtures as GPU proof or a machine transcript as creative approval.

## Existing work and decision

[Inputs](inputs.md#planning-evidence) records the source, alternatives, prior work, owner direction and decisions still needed. Existing H3 stages, timeline transfer and narration transcripts are starting points, not proof of the missing end-to-end capability. This new project joins them around a separately useful creative outcome; it does not replace their existing plans.

## Sequence and readiness

Phase 1 (approximately 10–15 days): unblock and prove appearance; phase 2 (approximately 12–20 days): clip knowledge and masks; phase 3 (approximately 8–10 days): GPU pilot, voice choice, edit and independent repeatability. Work tracks in parallel where their inputs allow; appearance must be proven before creative H3 work. The pilot gates the experiments, not the unpaid preparation. [Tasks](tasks.md) has the critical path, dependency gates and focused proofs. Estimates are planning estimates, not a schedule or a guarantee.

The intended base and landing are Release 14's per-repository `release/14/main`, via `release/14/plan-59`; the owner has directed these branches. Inclusion in and shipment with Release 14 remain an explicit decision because the release brief does not include this plan. No implementation or publication is authorized by this planning document.

## Interfaces and handoff

Consume the hash-verified public timeline-v1 archives, exact Runtime/Agent/App/VibeComfy source revisions, and the shipped 0.0.17 compositor artifact identified in [inputs](inputs.md#source-identities). Record actual dispatch heads and clean/dirty custody before use. Produce a versioned appearance contract and coherent package pins, editable timelines, durable clip knowledge, candidate and transcript evidence, a finished render, and a runbook that identifies the exact integrated tuple. Archive transfer is not a full history backup. Package provenance, the legacy baseline, source recovery and release inclusion are unresolved until decided and proven. Link implementation PRs and the integrated completion PR here as they become available.

## Completion

On the exact integrated tuple, both archives open with resolved media; a guarded edit, composed visualization and render succeed. The same authored appearance matches across all three paths including legacy and negative cases; the owner reviews the Matrix Fill crop. Real GPU receipts establish a working pilot and chosen voice approach, with spend and pod cleanup accounted for. The finished timeline contains owner-accepted takes, transcript comparison and a rendered video. A fresh weaker agent, given only the published-in-repository instructions and a different suitable timeline, completes a comparable edit through Astrid; retain its actions, output, errors and assessment. This proves those setups and cases, not all clips, models or environments. Integration and release remain subject to the [release workflow](../../skills/astrid-dev-release/SKILL.md) and explicit authority.
