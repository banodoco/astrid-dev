# Lane briefs

**Project:** Lane briefs

**Goal:** Every group of plans one orchestrator runs has one lane brief, agreed by the Lead with the owner and written to one template, so an orchestrator learns its whole job from one file and the same dispatch note is never hand-rewritten again.

**Status:** active

**Owner:** The Plan 108 manager `p108-manager`, a Claude Sonnet session launched on 28 November 2026 by the planning session `session_011EzfW1gtAhRQwk8pgJMzhG` (advisor); session `session_011EzfW15uV913PPYnNg8J91`

**Estimate:** 6–7 days (units of at most 3 days; planning figures)

**Waiting on:** —

**Run route:** astrid-dev-only

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — the release process itself. Lanes are how releases run; one definition, one template and one home per fact remove repeated hand-written dispatch notes and contradictory instructions that stall runs.

## Outcome and scope

A **lane** is the set of plans one orchestrator runs, possibly across releases, described by one **lane brief** in `releases/<N>/briefs/<lane>.md` (the release where the lane starts). The brief holds:
- the outcome and context;
- the plans and their order;
- a link to each plan's execution units (never a copy);
- how it runs: dispatch, proof, reviews, merges, check-ins;
- roles, standing rulings, cut line, coordination, what is reserved for the owner, and the launch line.

**The Lead divides a release into lanes *with the owner*.** It proposes two or three groupings with trade-offs and a recommendation, the owner chooses, and only then does the Lead write the briefs. The owner gives the go on each brief and sends each launch. The orchestrator reads only its brief. The plan's `Run start` line points to the brief.

Included:
- a process-ledger entry;
- the design;
- the template;
- the Lead's procedure, which merges the two leader lane workstreams into one;
- the orchestrator's procedure;
- definitions and run-contract rows that resolve today's contradictions;
- a structure check;
- a lane column in `release status`;
- applying it to the H3 programme and to the rest of Release 16.

Not included:
- a new folder or noun (lanes and `briefs/` already exist);
- a scheduler;
- a generated status block inside the brief;
- CI judgement of rulings or how-to-run text;
- rewriting historical dispatch sections.

## Existing work and decision

Eight dispatch notes have been hand-written across Releases 13–16 with the same ten fields. There is no template for a lane brief, dispatch note or launch message. Eleven contradictions exist across the role documents, about what a lane is, who is accountable, who sends the launch, who writes `Run start` and where rulings live. Nothing in CI reads run boards, briefs or packets. Release membership is one-way (the brief's Included plans), and the back-reference is generated. The smallest sound approach promotes the existing lane brief instead of adding a "batch" record. The full findings and design are in [research/design.md](research/design.md). The first real brief, written ahead of the template, is [releases/16/briefs/h3.md](../../releases/16/briefs/h3.md). Evidence: [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

L-1 → L-2 (design, `S`). Then L-3 → L-7 → L-8, with L-4, L-5 and L-6 alongside; then the review L-R. H-1 and H-2 apply it to H3. H-3, the first real lane division with the owner for the rest of Release 16, can start once L-4 lands. [Tasks](tasks.md). Recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:**
- `agent/roles/leader.md` and `leader/*`;
- `agent/roles/orchestrator.md` and `orchestrator/*`;
- `agent/roles/manager.md`;
- `agent/shared/glossary.md`, `run-contract.md` and `workstreams/release.md`;
- `templates/release/`;
- `scripts/records.py`, `checks.py` and `release_status.py`.

**Produces:**
- `templates/release/lane.md`;
- one definition of a lane;
- the Lead's lane-division-with-the-owner procedure;
- the orchestrator's read-your-brief procedure;
- the `lane-briefs` check;
- a lane column in `release status`;
- the H3 lane brief conformed to the template;
- Release 16's agreed lane split.

## Completion

- A cold-read agent given only Release 16 produces a lane proposal with options and trade-offs and stops for the owner; it does not write briefs first.
- A cold-read orchestrator given only a brief names its plans, its first dispatchable units and its owner-only points.
- The check catches each injected failure: a missing field, an unknown plan, a plan in two active lanes, and a plan not in the named release.
- `release status 16` and `17` show each plan's lane.
- Searching the role documents finds every one of the eleven recorded contradictions resolved.
- The Plan 91 and Plans 87/89 dispatch notes fit the template with no field lost.
