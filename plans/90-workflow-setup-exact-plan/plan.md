# Workflow set-up: one exact plan and one approval

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

**Project:** Workflow set-up: one exact plan and one approval

**Goal:** A person or agent sees one plan of every node pack and model a workflow lacks, approves exactly that plan once, and the saved workflow remembers it; packs they have trusted before install without asking again.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD — R16 exact-plan plus inherited P56 residual only; historical estimate about 10 engineering days after P56

**Waiting on:** P56 stage 1 (17 checked rows) landed in published R15, including recipe/approval/consent primitives; see [P56 task handoff](../56-workflow-setup/tasks.md#proposed-release-16-reconciliation--25-november-2026). [SC-90](https://github.com/banodoco/astrid-dev/blob/1bd93cf70f169e0db52f95ced5b8f9d189865539/plans/90-workflow-setup-exact-plan/evidence/release-16-scoping/SC-90.md) maps unfinished exact plan/apply, trust, safe recovery and producer seams; preserve P56 owner-run SAM proof. P35 CPU grant methods landed in R16, public grant route/consumer remains; await scope and manager.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a workflow is only portable if the place it lands can be made ready for it without a person hunting for files. [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting): nothing runs another person's code without an informed yes.

## Outcome and scope

Plan 56 makes every setup state end in a named next step and gives one informed yes for a pack Astrid has not reviewed. This plan adds the exact-plan form of that approval:

- `astrid generate requirements FILE|ENTRY [--placement] [--add URL[@REF]] [--add-model DEST=URL#sha256]` answers with one plan: each pack and model *present*, *found*, *needs approval* or *not found*, with source, pinned identity, dependencies, size, destination and one digest, installing nothing.
- `--apply DIGEST` installs exactly that plan, with `--consent code` for code outside the catalog; per-action progress (done, failed, pending); stops at "restart needed" and continues; refuses a stale or altered digest and conflicting pins.
- Reconcile what is not found: offer a file already present, a candidate from declared sources, one recorded answer per field.
- A reusable per-user trust list (`trust list|approve|revoke`) so a pack approved once is not asked about again on another workflow, kept where Plan 35 puts user state.
- Update and rollback plans: a changed pin is a new plan; switching versions on a kept machine.
- Save the observed hash and size of a download into the bundle for a model without a published hash; pickle formats judged by their loader.
- After Plan 32 F4, `fetch-models` and `align` call the same plan and apply.

**Not included:** executing a pack's `install.py` (never); signing, registries, sandboxing; identifying files by content (issue 665); a ComfyUI on another machine.

## Existing work and decision

This is the original scope of [Plan 56](../56-workflow-setup/plan.md) (accepted 15 November 2026, decisions D1–D3), which that plan's 23 November amendment narrowed to the 90/10 for [Release 15](../../releases/15.md). Reasoning, the independent critiques and the reuse map are in [Plan 56's inputs](../56-workflow-setup/inputs.md#planning-evidence); the task rows are the original WS-2 to WS-4 with the 80/20 additions, in [tasks.md](tasks.md). Plan 56's approval record is bound to identity plus recipe hash from day one so this plan wraps it with a digest and reinterprets nothing.

## Sequence and readiness

After Plan 56: the plan function and an RS1 review stop on its JSON and approval contract, then `generate requirements` and `--apply`, then reconcile and trust, then updates. Task details in [tasks.md](tasks.md). Recording this plan authorizes no work.

## Interfaces and handoff

**Consumes:** Plan 56's approval record, `--consent code`, `--add`, the fix envelope with `who`; Plan 32's manifest and F4; VibeComfy's lock, installer, resolver and fetch.

**Produces:** the Plan JSON `{requirements[], gaps[], bytes, digest}`, whose digest binds workflow content, target root and interpreter, sources, commits, recipe, packages and destinations; `generate requirements` and `--apply`; a trust list API.

## Completion

- With SAM-Audio in no list, `generate requirements ... --add <url> --placement runpod --dry-run --json` returns `needs_approval` with the pinned commit, dependencies, `install.py` reported not run and the digest, without a machine; `--apply DIGEST --consent code` installs exactly that; a second plan is `ready` with no flag.
- Negative cases: a changed target state invalidates the digest; a stale digest is refused; a failure after two of five actions reports two done, one failed, two pending and the next run does the three; a model that does not match its hash leaves no file.
- Limits: an agent can type the consent flag; approved code runs with the target's access.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

One exact dependency plan, applicable approval and resumable apply consume integrated Plan 56 Stage 1 and its individually mapped residuals; valid grant is not target readiness. A no-machine preview cannot authorize mutation on an unspecified future target.
