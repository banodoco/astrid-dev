# Investigate the creative foundation

**Project:** Investigate the creative foundation

**Goal:** Astrid's contributors have a source-backed, independently reviewed route to simpler, interchangeable creative tools and domains, with concrete reuse and removal decisions before the native foundation is implemented.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 8–12 engineering days, provisional; formerly included in Plan 100's estimate, not additional to the programme.

**Waiting on:** Accountable investigator, exact shipped/candidate source baseline, independent scope and review agreement, and explicit run authority for read-only research; separate authority for any product probes.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above define this project's catalog record; [priority](../priority.md) and release decisions remain separate.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Full-stack contributions](../../vision/gaps/LS-003-full-stack-contributions.md) (supporting) · [Cross-modal foundations](../../vision/gaps/LS-004-cross-modal-foundations.md) (supporting) · [Agent-managed tools](../../vision/gaps/LS-005-agent-managed-tools.md) (supporting)

## Outcome and scope

The investigation is independently useful even if a Rust rewrite is rejected: establish actual current creative-tool and resource boundaries, explain where contribution friction and special-case coupling arise, and identify the smallest sound improvements. Source traces must connect creator or agent intent to public entry, admission, ownership, implementation, storage/effect, receipt/event, observed result and recovery. The [investigation brief](investigation.md) contains the seven lanes, starting source paths and required evidence; the [tasks](tasks.md) own progress.

Included: resource/operation authority and domain semantics; public SDK versus video-specific/default-view coupling; contribution and operation discovery; state and targeted workspace sessions; extension build/lifecycle/trust; media/rendering/clock/performance; process/install/agent/local-cloud boundaries. Design an independent-tool test and a thin non-video witness, compare alternatives and identify exact redundant concepts, declarations and code paths that can be deleted or reused. Record actual findings, confidence/limits, negative cases, plan overlaps and a revised effort/dependency proposal.

Out: product implementation or refactoring; broad speculative frameworks; choosing Rust as a foregone conclusion; modifying accepted project scopes, active releases, priority or gap closure; hardware spend, production deployment or data migration. Product source is read-only by default, and any disposable product probe needs separate bounded authorization. This plan enables the gap's future proof, but does not itself deliver E1 or close any gap.

## Existing work and decision

The owner requested a standalone investigation on 26 November 2026 after the native-foundation and agent-extensibility discussion. The original investigation was merged in [PR #2042](https://github.com/banodoco/astrid-dev/pull/2042) as Plan 100's first slice; move the complete research brief and its tasks here, not a parallel copy. [PR #2039](https://github.com/banodoco/astrid-dev/pull/2039) and [Plan 100's architecture](../100-language-independent-foundation/architecture.md) record the prior source findings and proposed design, not an accepted implementation. The video-specific public SDK, default shell internal imports, multiple declaration/discovery surfaces and same-origin trusted extension model are concrete starting observations. Reuse and challenge existing Plans 18, 24, 35, 38, 41, 43, 45, 46, 47, 57, 62, 63, 75, 78, 83 and 94; do not reopen their accepted work without authority. See [inputs](inputs.md#planning-evidence) for decisions and limitations.

## Sequence and readiness

Pin shipped and candidate source identities (FI-1); investigate seven lanes independently (FI-2–FI-8); specify the independent-tool and second-domain witnesses (FI-9); reconcile a compact decision pack with estimates and concrete remove/reuse recommendations (FI-10); conduct one independently reviewed round subject to agreed bounds (R). A coordinator resolves overlaps. Source-read evidence and unexecuted test designs must be clearly distinguished. Re-estimate at FI-1 and stop once consequential choices have evidence or explicit blockers and discriminating checks, not after reading every file.

This is a proposed investigation-only Astrid Dev project; confirm the Dev-only run route and record run start separately. No numbered product release is needed merely to scope the research. Implementation work belongs to the consuming product plans and their separately authorized releases.

## Interfaces and handoff

Consumes the shipped manifest and installed/candidate Runtime/Agent/App/Pinokio tuple, relevant pack/VibeComfy/schema references and actual existing plans/test inventory, all pinned at FI-1. Produces an accepted source/authority matrix, contributor journey, traceable findings, consolidation ledger, alternatives/decision brief, independently reviewed witness and negative-case specification, and revised dependencies/estimates. Record exact revisions and findings/decision links so Plan 100 NF-1 can verify the handoff, refresh drift and consume it rather than repeat the audit; Plans 101–105 and existing extension/workspace plans consume the relevant findings through their existing authority. Actual conformance and product witness execution remain in the downstream plans unless separately authorized as bounded investigation probes.

## Completion

- Seven lanes complete with exact source identities, normal and failure paths, clear observed versus hypothetical claims, and concrete keep/reuse/extract/replace/delete/defer dispositions.
- One authority and contribution map identifies redundant authoritative definitions rather than counting legitimate derivative indexes; proposed simplifications name replacement owners, preserved invariants and removal proof.
- A fresh contributor's independent-tool/second-domain test has reproducible inputs, success and negative oracles, measured-or-unmeasured baseline and scope limits, ready for downstream implementation/qualification.
- Alternatives compare retaining/refactoring current implementation, native bootstrap with contract extraction, and modular native replacement; give explicit tradeoffs and falsifiers, security/portability limits and no framework invented by assumption.
- Independent reviewer examines source and challenges duplication, unjustified abstraction, missing authority/security or domain assumptions; document dispositions, owner decisions and unresolved blockers. Each material unknown has the smallest discriminating next check.
- Hand off a source-linked decision pack with revised estimates, critical path and routing into existing projects. A report alone does not close LS-006, authorize product changes, or qualify any runtime/tool journey.
