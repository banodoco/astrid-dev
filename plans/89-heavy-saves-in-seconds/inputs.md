# Inputs — Heavy saves in seconds

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner's decision [D1](./inputs.md#owner-decisions), 23 November 2026: do the cheap, measured parts of the fast-saving work now, as their own plan separate from Plan 75, in Release 15, continuing Plan 77's save run; Plan 75's structural work (FS-3b, FS-6) stays a later release.

**Prior art:** Plan 77's save run (fence fix for the pack host's writes, copy removal, timing sink; [tasks](../77-saving-holds-on-a-heavy-timeline/tasks.md#save-run-fresh-run-23-november-2026)) and [Plan 75](../75-fast-saving/plan.md)'s FS-0, FS-1, CC-1 and CC-11 cards, which these cards narrow. Measurements: [Plan 77 evidence](../77-saving-holds-on-a-heavy-timeline/evidence/) and [docs/speed.md](../../docs/speed.md).

**Approach:** Measure the installed save path stage by stage and remove the largest measured cost each round, stopping at the gate. Rejected for now: the full Plan 75 (about 24.5 days, depends on Plan 63) and cards the evidence does not yet justify (FS-5, FS-2, FS-3a).

**Challenge:** Reviewed — an independent Astra critique with Luna fact checks (23 November 2026, recorded in [Plan 75's inputs](../75-fast-saving/inputs.md#taken-on-by-plan-89-23-november-2026)) cut the proposal from about 10 days to these cards plus the loop, and showed FS-3a, FS-5 and FS-2 are not standalone.

**Proof and limits:** The completion measurement in [plan.md](plan.md#completion): the four Plan 77 scenarios plus bursts on the installed 300-clip fixture with the pack host running, median at most 2 s and none over 4 s, stored documents checked independently. Limits: one fixture and one machine class; not the 616-clip target or 300 ms.

**Review rounds:** At most 2 for SV-L5 and for each loop card that changes acceptance (row R in [tasks.md](tasks.md)); none for the measurement-only cards.

**Run start:** Started 23 November 2026, all cards, continuing Plan 77's save run in the same session. **Accountable agent:** the hosting orchestrator, `session_011EzfW2o5WfJcvHwr8fSDzC`, which hosts a Codex manager on route X (Terra); workers by card route; Astra for reviews. It may, without asking: everything its Plan 77 save run may do (Codex with full access, push `release/15/plan-77-save` and `release/15/plan-89` branches, measurement commands to the first-cut lane's box, PRs, merging once the Release 15 Lead confirms the gate, hosted CI when the Lead gives the slot). It needs the owner's go for publishing, anything paid, rented machines, live installs on her machine or her media. **Advisor:** the Release 15 Lead, `session_011EzfW1gtAhRQwk8pgJMzhG`. Check-ins hourly.

## Owner decisions

- **D1 (23 November 2026):** do the cheap parts of Plan 75 now, as their own plan, separate from Plan 75, in Release 15.
- **D2 (23 November 2026, carried from Plan 77):** changing existing guard-test assertions that encode the old "any movement refuses" rule is pre-approved for the timeline-scoped fence, each changed assertion listed with its old and new line and a paired test that a real history change still refuses.
- Standing rules: speed over review machinery for very unlikely cases; proof and measurement before hosted CI; Luna for ordinary work, Terra for the one subtle change, Sol only after two failed reviews.

## Source identities

Astrid-runtime `release/15/main` `737843e9` and the save branch head at the start of SV-L1, recorded on the card when it starts.

## References

- Save profiles and runs of 23 November 2026: [Plan 77 evidence](../77-saving-holds-on-a-heavy-timeline/evidence/) (`2026-11-23-save-profile`, the SV-3 runs and the SV-3 profile).
- Where the time goes, kept current: [docs/speed.md](../../docs/speed.md).
