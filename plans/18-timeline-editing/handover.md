# Handover — Extensible timeline editing

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Statements](statements.md) · [Release 14](../../releases/14.md)

Written on 18 November 2026 by the session that added phase 0 (the commit contract) to this plan. It is a dated snapshot for whoever manages this plan next. Nothing is built. Re-read branches with `git ls-remote` before acting.

## Where it stands

- The plan is **queued and unowned**. Phase 0 and the phase 1 re-scope are drafts on astrid-dev branches that are **local only**: `plan/18-command-layer` (phase 1 and 2, commits `d9ac42a4` and `bd535a5d`) and `plan/18-phase-0-commit-contract` (phase 0, one commit on top of it). Neither is pushed and no planning PR exists. The main thread reviews first.
- Phase 0 exists because of one finding of 18 November: nothing treats an accepted head as settled (the five symptoms are in [plan.md](plan.md#phase-0-the-commit-contract)). The owner asked for it to be fixed "now and PROPERLY ... in the follow up plan"; the "now" is Release 14's fix branches.
- Release 14's fix branches were cut and in flight on 18 November (runtime `release/14/commit-cost`, agent `release/14/legacy-probes` and `release/14/commit-loads`, app `release/14/rejected-discharge`; Agent #393 is merged at `b126d7482`). They are not rows in `releases/14.md` yet. CC-1 starts by checking each against merged code.
- No independent critique of phase 0 has been made.

## What is proven, and what is not

Proven by reading, not running: the profile numbers and the root-cause reading come from the 18 November reviews (private, held by the Release 14 Lead). **Not proven:** that the Release 14 fixes reach the counts the contract states (nobody has run the scaling test; CC-1 is the first run); that "low seconds" is reachable, and nothing shows under one second; the trigger of the 400 "inputs changed" (candidates: a second writer, a WAL stat change; CC-4 logs it); how the conflict card opens after a `rejected` outcome (reproduce first in CC-5).

## Waiting on the owner

- **D9:** which release carries phase 0 (proposed Release 15; alternative Release 17).
- **D10:** the corpus data: synthetic only, or one anonymised export.
- D4, D5, D6 and D8 from the earlier draft are unchanged.
- Confirm or overrule D11 (`stale_head` rebases an intent, conflicts a document patch) and D12 (counts, no clock).

## For the next manager, in order

1. Read [plan.md](plan.md#phase-0-the-commit-contract) then [tasks.md](tasks.md#start-here). Do not start before Release 14 is published and D9 is answered.
2. Re-check the Release 14 branches against the merged code and update the table in plan.md; anything not landed becomes part of CC-2.
3. Take CC-7 (corpus) and CC-1 (counters) together, then CC-3, CC-2, CC-4, CC-5, CC-6 and CC-8; close with R0.
4. When the scope PR merges, the Lead reopens #842 as the mechanism and links this plan on #826, #846, #732 and #852 (see the ledger in [inputs.md](inputs.md#issue-ledger)).
5. File the issues for the deferred items (cold-start hashing, snapshot size) so they have a home.

## What this run taught

- A cache keyed by base revision does not help ordinary edits, because each commit creates a new base. Trust must be keyed by file identity, which survives commits.
- A reader that raises on stored data is a bug class, not a bug: the fix is a mechanism (a registry and a test over legacy shapes), not a fourth rule.
- Phase 0 does not move the editor to send intent. That belongs to phase 1 and its review stop RS1; phase 0 keeps the old checks from growing (CC-8).
