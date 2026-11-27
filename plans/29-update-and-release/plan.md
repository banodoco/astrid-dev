# One update path and release

[Final Release 16 programme review](../../releases/16/evidence/final-programme-review.md) records current dependencies, estimates and remaining decisions.

**Project:** One update path and release

**Goal:** One working way to update: Update now or Update in Pinokio, with every screen agreeing, and a release number that changes only when what users install changes.

**Status:** active

**Owner:** Plan 29 manager

**Estimate:** 1–2 engineering days remaining implementation plus 0.5 incremental integration/qualification days; shared P09/P10/P29/P30 total 6–11 + 3–5, counted once, excluding existing P38/P93/P94/P31 work and venue waits.

**Waiting on:** Prior release work already implements shared capability/reason, update transaction and many UR rows. [SC-29](https://github.com/banodoco/astrid-dev/blob/68849637ddb2fb007289983727bc66e303328580/plans/29-update-and-release/evidence/release-16-scoping/SC-29.md) credits these; retain only actual status/skew, mixed-version, rollback and ownership/default-pack gaps and integrated proof with P09/P30/P31. Confirm remaining dispatch.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Release 16 residual

**End state:** every update surface names the installed owner, shows the same truthful state and offers the right working action; success means the selected App/Runtime pair is usable and pending work is preserved.

The foundational update UI, `self_update` capability/reasons, installation resolver, transaction, outcome record, helper and original release guard were delivered in earlier releases. The [sense-check #2060](https://github.com/banodoco/astrid-dev/issues/2060) confirms their source and merged history. Do not repeat Release 10–14 authoring, historical int promotion, old review rounds or a second publisher. Preserve their tests and evidence.

The residual is one decision over actual selected installation/owner and both App/Runtime identities, including current/ahead/behind/unknown, mismatched halves, busy/repair/recovery-needed, mixed old/new pages and truthful settled outcomes. Existing `resolveUpdate`, status reasons and `outcome.py` remain the mechanism. P30 LA-1–7 closes paired-local skew and local-owner/recovery gaps. In particular, current App Git ancestry alone must not return “up to date” while the Runtime is stale. Local npm and hosted curl instructions retain the recorded owner distinction; Pinokio users keep the Pinokio action.

P09 owns the common transaction and migration/retention invariants. Existing P38 `38-08U` owns its reserved lifecycle/deferred-recovery joins; P29 consumes the outcome rather than building another queue or outcome engine. P35 owns durable state, while P63/P79 supply pending-work save/import guard obligations. Keep reload and recovery from discarding those operations. P94 owns environment setup and P93 owns pack observation/admission; update UI does not absorb either installer.

P31 already owns UR-8b/c/d and canonical version/publication work. Retain the existing guard until its protected replacement is effective. R16 displays 0.1.0 while the legacy integer still orders releases and required-update floors; current known floor is 15. No floor change is implied by the semantic version. Publication is one P31 action after the final tuple's proofs and owner go.

## Sequence and completion

Disjoint decision/fixture work starts on current interfaces without waiting for all of P09/P38. Shared function landings follow explicit reservations. One integrated proof uses actual R15 origins and the final R16 tuple through each retained public action, including refusal, interrupted update, preserved content, recovery and successful retry. A stand-in/helper POST does not substitute for native engine or actual browser-action proof where required. P29's verdict feeds the shared P09/10/29/30 programme review and P31 release gate; old review-round limits remain preserved, not multiplied into fresh rounds.

The four-plan residual estimate is counted once in [P09](../09-install-and-update-confidence/plan.md). [Tasks](tasks.md) records current dispositions without erasing historical checkboxes. [Inputs](inputs.md) separates retained owner decisions from historical release-specific authority. The [previous full plan](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/29-update-and-release/plan.md) preserves earlier phasing and completed release history.
