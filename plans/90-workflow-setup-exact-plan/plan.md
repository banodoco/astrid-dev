# Workflow set-up: one exact plan and one approval

> **Planning reconciliation — 27 November 2026:** Proposed corrections from [observation #2058](https://github.com/banodoco/astrid-dev/issues/2058). Existing bounded execution continues under [the Lead's handoff](https://github.com/banodoco/astrid-dev/issues/2051#issuecomment-7222502183). Broader release deferrals below require owner agreement; this record neither dispatches work nor waives accepted guarantees.

**Project:** Workflow set-up: one exact plan and one approval

**Goal:** A person or agent reviews one exact workflow dependency plan, approves its bounded actions once, safely resumes them, and opens a real result from the saved workflow; reusable trust remains a separately tracked outcome.

**Status:** active

**Owner:** Manager94 coordinates the bounded P90 dependency under Astra94 technical ownership; broader P90 work remains unassigned

**Estimate:** Remaining bounded P90 work: 6–11 engineering days implementation plus 3–5 qualification; full retained remainder adds 8–14 plus 2–4 respectively, pending scope decisions

**Waiting on:** Accepted bounded WS2/RS1 handoff followed by existing WS9 public integration on board #2051; WS3-L consumes real P93 target, P94 transfer/compute and P35 protected-read seams. P56 stage 1 is delivered, not a whole-plan start gate. Full grant/restore and broader scope decisions are in inputs.md.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). The six fields above feed the generated [catalog](../../plans/index.md); do not edit the catalog. Priority remains in [priority.md](../../plans/priority.md).

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary) and [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## One local journey, with explicit limits

The active authorized cut is P90's bounded local producer/consumer contribution to P94-G; full project acceptance remains outstanding. P93 selects and observes the actual target. P94 owns environment offers, selected compute and transfer internals. P90 owns the workflow requirement plan and approval-to-apply orchestration. P35 owns user-state and grant authority.

1. `astrid generate requirements FILE|ENTRY`, with the actual `--placement`, `--add URL[@REF]`, `--add-model DEST=URL#sha256`, `--dry-run` and `--json` forms, returns one canonical plan without target or entry mutation. Show exact source, full commit/recipe, model identity, destination, known/unknown size and capacity, observations and the next useful action.
2. `--apply DIGEST`, with applicable existing `--consent code=<token>` confirmation, applies only the reviewed local actions through the controlled installer and built-in verified transfer. A preview or selected endpoint is not permission to write; a plan digest is not a grant.
3. Keep verified progress through interruption, process exit and required restart. Recheck actual target, authorization, capacity and required compute before later writes. Preserve the previous valid entry, lock and unrelated environment. A second invocation uses the saved exact declarations and verified completed actions without duplicate transfer or consent for unchanged approved scope.
4. Positive dependency observations permit workflow readiness; actual generated media opening in the matching editor permits delivery. Neither a plan, a running server nor downloaded weights establishes that outcome.

For an unknown or unsafe item, the accepted P56 manual action with a usable retry step is sufficient. Never run `install.py` or arbitrary Python workflow code during preview. Human-owned environments retain P56 D1's prohibition on changing installed packages or existing pack folders. Preserve D12's disclosed transitive resolution policy; do not introduce a package solver or silently demand universally immutable transitive artifacts.

## Contract repairs required before apply acceptance

These are acceptance obligations for the existing owners, not extra assignments or an expansion of the current three-finding WS2 continuation.

- **Stable approved intent, fresh observations.** Verified own progress, saved approval receipts and ordinary free-space changes must not invalidate otherwise unchanged authorized work. Bind workflow, selected identity, source/recipe/packages, destination, action scope and approved bounds; separately revalidate current capacity, grant and postconditions. The existing owners must choose and review either a stable intent projection or exact-snapshot recovery with narrowly proved own-action transitions. Never ignore arbitrary digest differences.
- **A working dependency transition.** Prove a missing supported dependency becomes installed and positively verified in the actual selected interpreter; an already satisfied pack becomes a no-op. Unknown or conflicting dependencies stay blocked/manual. Source presence is not dependency readiness.
- **One complete public plan.** WS9 preserves the producer's plan and digest through CLI/SDK/MCP and typed errors, mapping into P93's existing seven-rung ladder and single next action. The replacement producer uses `approval.consent_code` for the non-secret P56 value; consumer agreement and exact fixture proof remain required. Do not weaken credential redaction or rehash a redacted approximation.
- **One authority.** Use P35's authenticated protected read, never a second ledger or generic grant PUT. Revoked, unavailable or unknown authority cannot authorize writes. The absent-grant/fresh-one-time-consent rule must be explicitly resolved before that apply case lands. Full issuance/reapproval/restore semantics remain open under the P35 boundary.

## Existing work and decision

P56's 17 checked stage-one rows supply approval records, consent, recipe handling, resolver, controlled restore and entry primitives. The [16-row residual map](../56-workflow-setup/tasks.md#proposed-residual-handoff-to-plan-90) remains authoritative history; [tasks.md](tasks.md) identifies what the local cut consumes and what remains. P35's CPU ledger is landed; its public mutation and restore bridge are not delivered. Existing model-transfer and capacity work belongs to P94-A/B/E.

At the final 27 November refresh, [VibeComfy #224](https://github.com/banodoco/VibeComfy/pull/224) remained draft at `3ed74f2c3dbd782afdd8702d22b7c83b1c40b82a`; [Agent #689](https://github.com/banodoco/astrid-agent/pull/689) remained draft at `0087c03d9d7fdd28c4004312ffb3b355c9b6915c` with the deliberate public-preview gate. The [canonical second/final RS1 review](https://github.com/banodoco/astrid-dev/issues/2051#issuecomment-7225950426) accepted the three bounded producer repairs, independently executing 264 cases and actual serializer replay while preserving prior assertions. This supersedes round-one REWORK for that scope; do not create another RS1 round.

WS9's real producer invocation, selected FILE/ENTRY inputs, full committed normal/blocked public CLI fixtures and actual command proof remain open under its existing author. Stable approval/dependency-observation and grant/apply agreement remain with their assigned technical owners before affected writes. Bounded producer acceptance is not public join, installed apply or whole-project completion. [Inputs](inputs.md#source-and-evidence-register) keeps exact source and proof distinctions.

## Completion

**Bounded local acceptance:** use one tractable unfamiliar workflow needing a pinned node pack and model, plus the canonical unlisted SAM preview fixture. Prove public preview → decline with identical state → approved built-in apply → interruption/restart/repeat → canonical saved entry → real first and warm result in the matched editor. Include stale source/target/recipe/destination, revoked or unreadable grant, insufficient space, failed required compute, checksum mismatch, conflicting pin and protected-environment refusals. Exercise actual transport and immutable integrated pins, preserve original assertions and report unrun cells. Reuse P94-G/I/J and P93's qualification rather than creating a parallel programme.

**Full P90 acceptance remains separate.** The [Release 16 brief](../../releases/16.md) currently retains the wider P56/P90 obligations. WS4 reconciliation, WS12 unknown-hash receipts, WS16 caller convergence, TR1 reusable trust, UP1 update/rollback, remote WS3 and owner-run SAM are not completed by local acceptance. Recommend deferring their broader portions while retaining required local safety and usable manual outcomes; the owner must accept that release-scope change. Until then these remain open obligations, with their original guarantees and receiver rows.

A no-machine RunPod preview never authorizes a future target. Any retained remote route must meet its existing paid/custody and unsafe-setup boundary or receive an explicit release restriction. Actual paid execution and P56 WS-L remain separately owner-authorized.

## Sequence and effort

Consume the accepted exact WS2 candidate and continue existing WS9 public integration; complete consumer/apply agreement, then WS3-L after the real transfer, compute and authority joins. Existing 90-H delivers the exact combined receipt to 94-G and the single pin integrator. Native preparation and disjoint P93/P94 work continue independently. One writer owns each shared CLI/preflight/transfer/skill hunk; no duplicate task or wholesale donor-branch merge.

The 6–11 implementation days and 3–5 qualification days estimate remaining P90 effort, including active work, not fresh assignments or elapsed duration. The additional full-scope 8–14 implementation and 2–4 qualification days are low-confidence until the decisions in inputs are settled. Neither estimate charges P94-A/B/E, P35's own authority work, native capacity waits or paid SAM work again.
