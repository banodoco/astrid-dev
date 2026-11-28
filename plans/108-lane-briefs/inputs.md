# Inputs — Lane briefs

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — On 28 Nov 2026 the owner asked for this to become an astrid-dev project in the [planning session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG). The scope is to promote the existing lane brief to the single record one orchestrator runs from, have the Lead divide releases into lanes with the owner, and apply it first to the H3 programme.

**Prior art:**
- An inventory of all release folders found eight hand-written dispatch notes with the same ten fields (for example [releases/15/run.md](../../releases/15/run.md) and [releases/16/run.md](../../releases/16/run.md)).
- The existing lane concept and brief location are in [agent/roles/leader.md](../../agent/roles/leader.md) and [agent/shared/workstreams/release.md](../../agent/shared/workstreams/release.md).
- There is no lane template in [templates/release/](../../templates/release/run.md).
- Nothing in [scripts/checks.py](../../scripts/checks.py) reads run boards, briefs or packets.
- Details and the eleven contradictions: [research/design.md](research/design.md).

**Approach:** Promote the existing lane brief, with one definition, one template and one home per fact. Rejected alternatives:
- a new "batch" record and folder, which duplicates the lane concept;
- generated status inside the brief, which duplicates `release status`;
- CI judgement of rulings or prose, which has a poor benefit-to-cost ratio.

**Challenge:** Not needed — The project consolidates existing astrid-dev concepts rather than adding new architecture. Its design task (L-2) runs on the `S` route, and both it and the whole change (L-R) get the high-judgment review before anything lands.

**Proof and limits:** See the plan's Completion list: cold reads by a Lead and an orchestrator, injected-failure tests for the check, `release status` lanes, and a search for the eleven contradictions. Limits: it cannot prove that future dispatch notes are written well, only that they have one shape and one home.

**Review rounds:** One (L-R), on the high-judgment role.

**Run start:** Whole project (L-1 to H-3), owner-authorized on 28 November 2026 in the [planning session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG). **Accountable agent:** the manager `p108-manager` (Claude Sonnet), following the [whole-project manager workstream](../../agent/roles/manager/whole-project.md) for an astrid-dev-only project. **May, without asking:**
- dispatch subagents on each card's route (N Haiku, X Sonnet, S Opus);
- cut `project/108-lane-briefs` from `main`, and task branches `p108/<task>` from it;
- merge task branches into the project branch;
- merge its own `tasks.md` progress PRs to `main` once checks pass;
- open and post on `board: plan 108 lane briefs`.

**Needs the owner's go:**
- the final project PR to `main`;
- the owner's lane choice in H-3, which the manager proposes and then waits on;
- anything outside astrid-dev.

**Review:** L-R on the high-judgment role. **Advisor:** the planning session `session_011EzfW1gtAhRQwk8pgJMzhG`, by send_message; questions that block go there, never to AskUserQuestion. **Decision log:** a "Rulings" section at the top of `tasks.md`.

## Owner decisions

- **D1 — Name (decided 28 Nov 2026, owner).** "Lane", which already exists in astrid-dev, not "batch".
- **D2 — Lane division (decided 28 Nov 2026).** The Lead divides each release into lanes *with* the owner: it proposes options and the owner chooses; the Lead never decides lanes alone.

## Source identities

Planning snapshot: astrid-dev `main` at `541ced23` plus PR [#2067](https://github.com/banodoco/astrid-dev/pull/2067). The H3 lane brief at [releases/16/briefs/h3.md](../../releases/16/briefs/h3.md) is the worked example.

## References

- [research/design.md](research/design.md): inventory findings and the lane-brief design.
- [releases/16/briefs/h3.md](../../releases/16/briefs/h3.md): the first lane brief.
