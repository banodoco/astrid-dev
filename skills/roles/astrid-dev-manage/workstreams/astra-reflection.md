---
description: Gate each AI Studio lab packet and periodically replan the lab queue, merging accepted work into the lab and keeping the run board current.
---

# Workstream: reflect on AI Studio lab packets

## Workstream contract

**Outcome:** Every pushed lab packet has a recorded verdict (accept, rework or split), and the queue ahead matches what has actually been learned.
**When to use:** When the run's manager hands you a lab packet at Gate, at each RF row of a lab run board, and at the owner's daily look, for a lab run such as Plan 84's.
**Inputs:** The run board, the lab repository and its `LAB_RULES.md` and `packets/`, the pushed branch and result note, the owner's notes the manager passes on, and the run's authority.
**Procedure:** Gate each packet by rerunning its proof and reading its diff; at RF rows, re-estimate and rewrite the next briefs; draft the daily look; return everything to the manager.
**Completion:** Each reviewed packet has a verdict returned to the manager naming its commit, every rework names what done looks like, and the next Ready packets have current briefs.

Runs on the high-judgment role (Astra on Codex, Opus on Claude; [routing](../../../shared/run-contract.md#routing-and-bindings)). AI Studio cannot take screenshots, so **the proof you can check is tests and the diff; the look is the owner's**, at the daily look. A packet that changes what a visitor sees is not finished until the owner has seen it, but it may be merged into the lab before then.

## Gate a packet

1. Pull `lab/<id>` at the commit the manager gives you. Merge the lab's current `main` into it locally if `main` moved.
2. Rerun `npm install`, `npm run check` and `npm run build` yourself. AI Studio's own report is not proof.
3. Read the whole diff against the brief and [`LAB_RULES.md`](https://github.com/banodoco/planet/blob/main/LAB_RULES.md). Check especially: nothing from *Not in this packet*; the engine invariants (one seeded random in the same order, one clock, every allocation through `own()`, no module-level mutable state, the same build and update order, no allocation in the frame loop); no existing test edited or weakened; for parity packets, `sceneFingerprint` snapshot untouched; no new dependency; files under 1,200 lines.
4. If you have a browser, open the preview at the brief's *Look at* settings and say what you saw; this is a sanity check, not the owner's verdict.
5. Decide:
   - **Accept:** say ACCEPT with the reviewed commit. The run's manager merges `lab/<id>` into the lab's `main` with a merge commit (or you do, if the run gives you that access), marks the packet **Accepted** on the board with the merge commit, and makes the next packets **Ready**.
   - **Rework:** write a short rework prompt naming each failure and what done looks like, for the manager to paste into AI Studio; mark **Rework**. At most two rounds.
   - **Split:** if the packet was too big or two things at once, accept what is sound (or nothing), write the new briefs in `packets/`, and update the queue.
6. Return the verdict to the manager, one line per finding, sorted BLOCKING / FOLLOW-UP / NOTE. File follow-ups as later packets, not as silent fixes.

## Daily look

Once a day, draft the **daily look** for the manager to give the owner: what was accepted since the last one, the lab `main` commit to open in AI Studio's preview, and for each visible change the exact sizes, address options (`?planet-test-pose=fixed`, `?sky=HH:MM`) and landmarks to look at. The owner replies to the manager with notes. Each note becomes a rework, a new packet or a ruling on the board; the owner's verdict on the look is final.

## Replan (RF rows)

At each RF row on the board: compare actual effort, rework rounds and AI Studio's failures with the estimates; read the owner's notes since the last RF; re-cut, merge or split the packets ahead and rewrite their briefs against the lab's current code (line ranges move as the engine is split); restate the remaining estimate. Record what changed and why on the board. Ask a second high-judgment reviewer for a zoomed-out opinion at RF-B and RF-D.

**Do not** merge anything into the product repository, change the lab's `upstream.json` base, relax `LAB_RULES.md` or a test, or start integration (IN rows) without the owner's go.
