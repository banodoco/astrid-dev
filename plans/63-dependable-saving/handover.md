# Handover — Dependable saving

> **Historical snapshot, not current dispatch instructions.** The 27 November 2026 [plan](plan.md), [tasks](tasks.md) and [inputs](inputs.md) reconcile the R16 scope and retained decisions. Preserve this 18 November record for provenance; do not execute its old R15 branch, deletion or publication instructions.

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Statements](statements.md) · [Plan 18](../18-timeline-editing/plan.md) · [Release 14](../../releases/14.md)

Written on 18 November 2026 by the session that moved Plan 18's Phase 0 here. It is a dated snapshot for whoever manages this plan next. Nothing is built. Re-read branches with `git ls-remote` before acting.

## Where it stands

- The plan is **queued and unowned**, in no release brief; the owner said to add it to astrid-dev and not to start it. Which release carries it is D9 (**decided by the owner on 18 November 2026: Release 15**), one decision for **four plans** cut from the save work on 18 November 2026 (the four-questions check, then the final recommendations, accepted by the owner): **A, this plan, first (about 39.5 days); B, [Plan 75](../75-fast-saving/plan.md) One acceptor, in parallel from day one (about 24.5 days plus 2 conditional; 300 ms, no two stages); C, [Plan 76](../76-editing-together/plan.md) Editing together, after A (about 12 days); D, [Plan 18](../18-timeline-editing/plan.md) Extensible editing, after A (about 62 days plus 8.5 optional; agents and packs first).** The dependency graph is in [plan.md](plan.md#outcome-and-scope).
- It is a draft on the astrid-dev branch `plan/63-dependable-saving`, with local commits not yet pushed (the GitHub credential was down); the main thread reviews it first.
- Plan 18's Phase 0 was **moved** here, not copied, then cut to a lean form by an independent check, then restructured: **CC-1, CC-2, CC-9 and CC-11 moved to Plan 75** with their ids; CC-4b and CC-12 stay here; the batch (CC-5c, about 3 days) and the burst property were added; the same-field coalescing rule was dropped (the batch replaces it). CC-10 is an in-memory upload retry, CC-8 is cut, CC-4 sets `outcome` on the commit and import routes only (the closed reason list and sync script went to Plan 18's TL-4 and TL-2), D15 is the park-with-the-tail form. Added earlier: the old-Runtime decoder fallback, migration of owners and drafts, the other outbox users, the two-tab rule, I-3 marked covered by `save-recovery-2`, CC-4b (the Agent's client reads `outcome`, one reply fixture) and CC-12 (the guidance paragraph and the installed-skills gap).
- **The first step is already on Release 14:** `release/14/quick-edits` (committed locally, `ff34621e9`: the empty-queue adopt in `pump` and the progress watchdog). CC-5b builds on it.
- The save fixes already merged on Release 14 (N1 to N12, the `_reference_basis` fix, Runtime #61 to #63 and #65, App #299 to #300, `release/14/save-recovery-2`) are the base.
- Reviewed: the earlier Phase 0 by Opus (merge with edits); this plan by independent Fable checks (the lean check, agent edits, quick edits, four questions; held by the Release 14 Lead), applied.

## What is proven, and what is not

Proven by reading, not running: the profile numbers, the 16 incidents and the root-cause reading come from the 18 November reviews (private, held by the Release 14 Lead). **Not proven:** that k chained `doc.patch` records can go as k steps of one commit and undo one by one (CC-5c's first check, 0.5 day, before anything is built); which path the Almost Ready bundle took (CC-4b's first step); how the editor adopts a head an agent moved while its queue is empty (CC-5a's first step); that the merged fixes reach the counts the contract states (nobody has run the scaling test; CC-1 is the first run); that "about 3 s" per save is reachable after the `_reference_basis` fix (33% of a measured 9 s, not measured); that old Runtimes really meet a new hosted editor (if pins always pair them, the CC-4 fallback shrinks to a test); that the Runtime's moved-head path for a non-restore commit never surfaces as a 503 (unverified); that `shotTimelineDataProvider.ts` and `placementService.ts` are reachable in the shipped editor; the 1.5-day size of CC-11 (its first step is to inventory what updates or deletes history rows today); that `discardScope` is fenced against a row another tab holds (the model test's two-tab case must show it); the trigger of the 400 "inputs changed"; how the conflict card opens after a `rejected` outcome (reproduce first in CC-5b).

## Waiting on the owner

- **Decided on 18 November 2026 (see [inputs.md](inputs.md#owner-decisions)):** D9 Release 15; D15 and D16 a refusal or clash parks with everything behind it, two buttons Keep mine and Discard, never re-applied automatically; D17 an agent's edit relies only on what its commands read and wrote (whole timeline opt-in); D18 Plan 18 runs agents and packs first; D19 the speed target is 300 ms with no conditional stage; D5 the alternate view is deferred.
- **D10:** the corpus data. Confirm or overrule D11 and D12. (D14, persisting verified trust, moved to Plan 75.)

## For the next manager, in order

1. Read [plan.md](plan.md), then [tasks.md](tasks.md#start-here). Do not start before the owner says go (the release is decided); the plan's branches are then `release/15/plan-63`. Day one: CC-13, CC-5a and CC-7.
2. Two tracks. App: CC-5a (the model test, grown from the seed, with the burst property and the undo rows) first, CC-4 beside it, then CC-5c's first check (do k chained steps commit and undo one by one? through CC-13's harness), CC-5b (write the two-tab rule first), the rest of CC-5c, and CC-10; critical path CC-4, CC-5b, CC-5c, CC-10, R0 (about 16 days). Agent and Runtime: CC-7 and CC-13 first, then CC-14, CC-15 and CC-16, CC-3 then CC-6, and CC-4b then CC-12 (the Agent's side of the four outcomes, then the guidance paragraph).
3. Release 14's stop-gap (about 3 to 4 days, not in this plan's total) is separate: the one-off sweep of every edit kind on a sandbox timeline seeds CC-13, and the speed bisection's run 2 decides whether FS-3a starts with a small fix.
4. When the scope PR merges, the Lead reopens #842 as the mechanism and links this plan on #826, #846, #732 and #852 (see the ledger in [inputs.md](inputs.md#issue-ledger)), and files the deferred items ([inputs.md](inputs.md#deferred)).

## What this run taught

- A cache keyed by base revision does not help ordinary edits, because each commit creates a new base. Trust must be keyed by file identity, which survives commits.
- A reader that raises on stored data is a bug class, not a bug: the fix is a mechanism (a registry and a test over legacy shapes), not a fourth rule.
- Saving failed in sixteen ways because an unsaved change had many homes and a reply had many classes; the fix is one home and four outcomes, enforced by one model test, not a fix per incident.
- The same plan cut by about a fifth when read by someone who did not write it: transport and uploads were tidiness, a stored `File` doubles video bytes in the browser, a ratchet at zero is a lint, and a reason list that cannot decide behaviour belongs with headlines.
- Release 14 can carry the behaviour; the structure changes what is stored in the browser and what goes over the wire, so it needs the corpus and the model test under it first.
