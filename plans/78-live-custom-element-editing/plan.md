# Live custom-element editing

**Project:** Live custom-element editing

**Goal:** An editor's agent applies a creator's custom pack-element timeline edits live in one commit, with feedback in seconds and no restart or external runbook.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 11–14 engineering days: phase 1, 7–9; phase 2, 4–5.

**Waiting on:** Owner decisions, independent critique, and identification and integration of the plan-69 product inputs.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md).

**Vision gaps:** [F-004 — Pack lifecycle](../../vision/gaps/F-004-pack-lifecycle.md) (primary).

**Contributes to closure:** F-004: a real project uses a pinned, locally authored frontend rendering contribution after admission, including failed admission and preserved project references; this is only a portion of its demanding-pack evidence.

## Outcome and scope

Phase 1: on an explicitly identified local installed stack, the editor's own agent follows the skills to prepare a project pack and apply the four representative animation edits from a chat prompt, in one timeline commit. The running daemon sees an installed pack without a restart; the open editor sees the admitted exact revision and resulting edit. A release default includes the pinned motion pack if the owner agrees. Measure the warm commit and the whole interaction separately against a seconds, not minutes, target; a failure is not a pass. Use an admit-and-apply agent workflow that hides redundant ceremony but keeps distinct admission and commit failure boundaries and durable retry identity.

Phase 2: subject to an explicit owner decision and the security review, make local user-authored element admission less restrictive without weakening a hosted or shared trust boundary. Keep digest-pinned retained source and compiled artifact, compile at admission, and exact revision checks. Distinguish trusted local authority from untrusted inputs using an enforceable boundary; if it cannot be established, retain restrictions and return the decision to the owner. Never present import restrictions as a sandbox.

This plan does not promise a hosted sandbox, broad delta storage, or general editing concurrency. [Plans 75 and 77](inputs.md#planning-evidence) own the saving-cost work; unresolved independent defects are proposed as issues in inputs. The four-edit proof uses a safe copy with equivalent source and records exactly which timing semantics are supported.

## Existing work and decision

Extend the existing Timeline.commit command path, project-pack admission, installed-pack refresh and editor loader; do not build a new pack or a parallel publishing system. The alternatives, checked source, observed limits, owner quotation and unresolved choices are in [inputs](inputs.md#planning-evidence). This is a draft, not an accepted security or scope decision.

## Sequence and readiness

First freeze the actual plan-69 integration inputs and reconcile later release heads. Batch authoring and installed-pack discovery can proceed independently; the combined admit-and-apply workflow consumes the batch interface. Review the batch and refresh contracts before the integrated editor proof. Phase 2 follows the owner's trust-boundary decision, not a presumption of approval. See [tasks](tasks.md) for the critical path and test inventory. A plan is not authorization to start a run, change production or release.

## Interfaces and handoff

Consume the exact Agent, Runtime, App, release manifest and motion-pack revisions recorded at dispatch, including selected plan-69 changes; do not assume the donor branches have merged. Produce a public batch editing interface, compatible exact-revision admission/refresh and a reproducible live-flow record bound to integrated commits. Keep captured expected heads, idempotency, conflict and recovery semantics. No release has been assigned; the run owner must determine the release integration destination before dispatch.

## Completion

On a disposable representative heavy project, the actual in-editor agent makes the four requested edits, including seven placements and six added text clips, with one durable timeline receipt/history row and visible correct preview without restart or manual SQL/runbook. Record source pins, prompt, elapsed times for admission, commit and visible preview, resulting head, screenshot or recording and independent visual comparison to the intended four edits. Show stale head, lost acknowledgement, failed compilation and mismatched revision do not silently apply or substitute code. Measure a warm repeated run: target seconds for commit and visible result, with the data size and machine recorded. If plan 77 does not meet it on the fixture, report the blocker rather than relaxing the target. This local proof does not establish hosted isolation or performance on all projects.
