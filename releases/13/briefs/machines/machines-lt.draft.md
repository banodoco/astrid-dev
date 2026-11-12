difficulty: sol (S, write; custody, design)

# LT: one lease transition table (deep cause D: no single table of end states)

**Repo:** Astrid. **Clone:** `/home/user/wt/c-lt` (branch `r13/machines-lt`, base `r13/machines` at `__BASE__`, after M1 and M2). Work in this clone only.

## Why (Release 13 manager, from an independent advisor review)
The custody gaps Astra keeps finding come from the design. Lease state lives in three independent string fields, `record.state` (journal root), `lease.state` and `preparation_state` / `lease.preparation.state`, written across `astrid/packs/runpod/worker_owner.py`, `machine.py`, `worker_preparation.py`, `generation.py` and `target_selection.py`. There is no transition table, so every review audits an open-ended state space.

## Outcome
1. **One module**, `astrid/packs/runpod/lease_states.py`, defines:
   - an enum of states: the reachable combinations of the three fields, named; drop combinations that can't occur;
   - an enum of events;
   - one table of (state × event) → (next state, billing action), where the billing action is one of keep-with-deadline, release-exact-pod or reconcile-then-release.
2. **Every writer of the three fields goes through it.** Grep every assignment, `_save(...)` and `update(state=...)` that writes one of them and replace it with one `transition(record, event)` call that looks up the table and refuses an undefined (state, event). Grep before and after, and list the count of writers.
3. The events include at least: claim, job admitted, preparation started, preparation succeeded or failed, job succeeded, job failed (terminal or not), cancel, idle expiry, paid expiry, keep, release, release failed, restart (host recovery), and recipe, model or source change detected (upgrade).

## Acceptance (must fail before, pass after)
New `tests/packs/runpod/test_lease_transition_table.py`:
- (a) **enumerate every state × {restart, paid expiry, idle expiry, job failure, recipe/model/source change, cancel}**. Each must be defined in the table and end, directly or through a defined chain with no further external event, in **released** or **kept with a deadline** that is no later than the paid expiry;
- (b) **required rows, the gaps found by review.** Each one must be an explicit row with the stated outcome, driven through the real owner with the existing fakes:
  1. cleanup or release pending + restart → reconcile, then release the exact pod, with no new allocation (Astra M1 final check, finding 1);
  2. idle claimed + recipe/model/source change, then restart → not adopted, exact-pod release (finding 2);
  3. preparing + paid expiry (preparation finishes after expiry) → refused before execution, exact cleanup (finding 3);
  4. acquiring after the paid create + paid expiry while a provider call is in flight → release at expiry, with no second create (M4 re-check, finding 1);
  5. idle + idle expiry → release; active + idle expiry → kept until settle (the idle clock counts only while idle);
- (c) the table is the only writer: a test fails if a module other than `lease_states.py` writes one of the three fields (an AST or grep check over `astrid/packs/runpod/`).

Keep every existing custody, expiry, reset and release test passing unchanged. If one encodes a transition the table rejects, stop and report it. Proof: the new file plus `tests/packs/runpod/test_job_on_claimed_machine.py`, `test_warm_session.py`, `test_failed_job_keeps_warm.py`, `test_keep_warm_evidence.py`, `test_machine.py` and `test_generation_preparation.py`, then ruff, mypy on the files you edit (gates) and `git diff --check`. Save the diff to `/home/user/wt/briefs/wave3/machines-lt.diff`. In your report, include the table itself as a markdown table.
