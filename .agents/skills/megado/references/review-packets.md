# Building review packets from artifacts

Use `templates/review-packet.md` for every declared executable review stage. It is an assembly template, not a new reviewer stage or an implemented packet-building service. The coordinator fills it from existing run artifacts; it does not invent new objectives each time.

## Declare inputs before execution

Each stage in run.yaml adds `scope_tasks`, `criteria`, and `criteria_source` to its existing trigger/lens/role/budget. IDs refer to the tasklist and an implementation acceptance contract, not planning-completion criteria. The same packet template covers both lenses. Put behavior/expected outcomes and required proof next to each criterion once; do not create separate catalogs per reviewer.

## Assemble mechanically

| Packet field | Source |
| --- | --- |
| Role, reasoning, lens, budget, trigger and scope | run.yaml + durable consumed counters |
| Full North Star | northstar.md, copied verbatim with digest |
| Objective, authority, non-goals | current agent_goal.md |
| Expected behavior and dependencies | declared criteria_source, selected criterion IDs |
| Decisions and scoped tasks | plan.md and tasklist.md; final holistic includes the full plan |
| Candidate identity, source paths and diff | frozen checkout/snapshot plus changed-path census |
| Proof coverage | test/execution receipts with command, input/environment identity, result and evidence digest |
| Prior issue dispositions | recorded concrete findings and oracle decisions, not prior verdict narratives |
| Correction scope | actual delta and affected criteria/dependency closure, preserving other results |
| Correction routing | actionable-finding classification plus normal/XHARD recommendation and any XHARD justification; no route for non-actionable findings |

Create one packet under briefs/ or checkins/ per actual stage/round. Attach a simple manifest of the exact input paths/digests; the packet and referenced files must remain available unchanged to the reviewer. Do not embed full workflow payloads/logs by default: link exact frozen artifacts. Do not substitute conversation history or the worker's completion summary for source and test evidence. Do not silently truncate requirements; link bulky evidence and provide readable criteria.

Before dispatch verify required sections, criterion coverage (including explicit MISSING rows), valid frozen identities and accessible referenced artifacts. If the stage trigger's required tests have not passed, dispatch the prescribed tests, collect their results and complete the mechanical readiness checks rather than use review to discover known incompleteness. This is a mechanical readiness check, not another independent review or gate document. If a review must assess a genuine evidence gap, label it explicitly rather than fabricate proof.

First consequential-boundary review: complete scoped implementation diff plus affected integration and operation-readiness evidence. First final review: full integrated diff from run base, whole plan/criteria and end-to-end evidence, including unchanged surfaces relevant to integration. Correction rounds: changed source plus affected coverage and accepted findings, with full contract still available. A material change to the reviewed contract or candidate reopens affected criteria in the same declared stage using its remaining rounds; preserve unaffected approvals and consumed counts. If no rounds remain, surface the budget decision rather than creating another stage or claiming the old PASS covers the changed contract. Do not ask for a fresh strategy every correction round.

The completion lens looks for missing/incorrect implementation and insufficient proof. The strategic lens adds whole-system coherence, simplicity, preserved behavior and North Star alignment. Packet content and lens come from the declared role and stage; the resolved model binding is execution metadata and never creates criteria, authority or a new review objective. A final allocated review stage may contain multiple rounds; identify whether this packet is for that stage and whether this invocation is its last allocated round. A final review can cover both lenses in one invocation. A final review may still emit blocking correction tasks; PASS waits until those tasks are implemented and verified. It may also return PASS with clearly labeled optional, non-blocking revision suggestions; those do not hold completion and receive no correction route. On the last allocated round of the final allocated review stage, a directly evidenced unresolved in-scope blocker may be returned as HARD_BLOCK rather than weakening the verdict or creating an extra round. An oracle disposition rejecting all blockers does not itself replace the stage verdict; a remaining review round is needed to obtain PASS, otherwise surface the review-budget decision. A strategic concern must map to an existing criterion or concrete defect to block; alternatives and future features do not silently expand acceptance. Actionable findings separately record blocking classification and correction difficulty: a reviewer recommends `normal` or `xhard`; unresolved or disputed difficulty goes to the oracle, then the executable worker assignment/worker brief receives one of those two routes. Non-actionable findings receive no correction route.

A rendered packet consumes no model call. Dispatching its reviewer consumes one round under run.yaml, whether the result is usable or UNKNOWN; no new count is created by the packet or lens. An UNKNOWN caused by an access or identity problem may be retried within the stage's remaining round budget only after that cause is resolved and the candidate and evidence identities are revalidated; the consumed UNKNOWN round is not restored. Oracle interpretation stays separately accounted and subject to any explicitly configured oracle cap. Templates guide agents today; adding an automated builder/validator executable is separate work, not a claim made by these instructions.
