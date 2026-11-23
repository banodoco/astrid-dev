# Inputs — Heavy saves in seconds

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

- Save profiles and runs of 23 November 2026: [Plan 77 evidence](../77-saving-holds-on-a-heavy-timeline/evidence/) (`2026-11-23-save-profile`, the SV-3 runs and the SV-3 profile).
- Where the time goes, kept current: [docs/speed.md](../../docs/speed.md).
- The independent Astra critique of the "lite" proposal, and what it advised cutting: [Plan 75 inputs](../75-fast-saving/inputs.md).

**Run start:** Started 23 November 2026, all cards, continuing Plan 77's save run in the same session. **Accountable agent:** the hosting orchestrator, `session_011EzfW2o5WfJcvHwr8fSDzC`, which hosts a Codex manager on route X (Terra); workers by card route; Astra for reviews. It may, without asking: everything its Plan 77 save run may do (Codex with full access, push `release/15/plan-77-save` and `release/15/plan-89` branches, measurement commands to the first-cut lane's box, PRs, merging once the Release 15 Lead confirms the gate, hosted CI when the Lead gives the slot). It needs the owner's go for publishing, anything paid, rented machines, live installs on her machine or her media. **Advisor:** the Release 15 Lead, `session_011EzfW1gtAhRQwk8pgJMzhG`. Check-ins hourly.

## Owner decisions

- **D1 (23 November 2026):** do the cheap parts of Plan 75 now, as their own plan, separate from Plan 75, in Release 15.
- **D2 (23 November 2026, carried from Plan 77):** changing existing guard-test assertions that encode the old "any movement refuses" rule is pre-approved for the timeline-scoped fence, each changed assertion listed with its old and new line and a paired test that a real history change still refuses.
- Standing rules: speed over review machinery for very unlikely cases; proof and measurement before hosted CI; Luna for ordinary work, Terra for the one subtle change, Sol only after two failed reviews.

## Source identities

Astrid-runtime `release/15/main` `737843e9` and the save branch head at the start of SV-L1, recorded on the card when it starts.
