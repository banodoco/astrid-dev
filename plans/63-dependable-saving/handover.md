# Handover — Dependable saving

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Statements](statements.md) · [Plan 18](../18-timeline-editing/plan.md) · [Release 14](../../releases/14.md)

Written on 18 November 2026 by the session that moved Plan 18's Phase 0 here. It is a dated snapshot for whoever manages this plan next. Nothing is built. Re-read branches with `git ls-remote` before acting.

## Where it stands

- The plan is **queued and unowned**, in Release 14 by the owner's decision (D9). It is a draft on the astrid-dev branch `plan/63-dependable-saving`; the main thread reviews it first.
- Phase 0 of Plan 18 was **moved** here, not copied, with the save-category design's deltas applied (CC-4 and CC-5 rewritten, CC-9 new, CC-10 moved in from TL-10, the corpus and ratchet extended). Plan 18 now depends on this plan.
- The save fixes already merged on Release 14 (N1 to N12, the `_reference_basis` fix, Runtime #61 to #63, App #299 to #300) are the base. Their branches were in flight on 18 November; CC-1 starts by checking each against merged code.
- Independent review of the earlier Phase 0 by Opus (merge with edits), edits applied. The deltas are Fable's. This pack has had no further review.

## What is proven, and what is not

Proven by reading, not running: the profile numbers, the 16 incidents and the root-cause reading come from the 18 November reviews (private, held by the Release 14 Lead). **Not proven:** that the merged fixes reach the counts the contract states (nobody has run the scaling test; CC-1 is the first run); that "about 3 s" per save is reachable after the `_reference_basis` fix (33% of a measured 9 s, not measured); that a `File` in the queue row survives a reload in every supported browser (CC-10 starts by checking); that `discardScope` is fenced against a row another tab holds (the model test's two-tab case must show it); the trigger of the 400 "inputs changed"; how the conflict card opens after a `rejected` outcome (reproduce first in CC-5b).

## Waiting on the owner

- **D15:** what a refused change looks like (recommended: removed from the timeline and listed with Restore and Dismiss). The only decision on the critical path; needed before CC-5b.
- **D14:** persist verified trust across restarts. **D10:** the corpus data. Confirm or overrule D11 and D12.

## For the next manager, in order

1. Read [plan.md](plan.md), then [tasks.md](tasks.md#start-here). Do not start before today's save fixes are on `release/14/main`; the plan's branches are `release/14/plan-63`.
2. Take CC-5a (the model test, grown from the seed) first, with CC-7, CC-1 and CC-4 beside it; CC-3 then CC-6, CC-2, CC-8 and CC-9 run beside the critical path (CC-4, CC-5, CC-10, R0).
3. Put D15 to the owner now.
4. When the scope PR merges, the Lead reopens #842 as the mechanism and links this plan on #826, #846, #732 and #852 (see the ledger in [inputs.md](inputs.md#issue-ledger)), and files the deferred items ([inputs.md](inputs.md#deferred)).

## What this run taught

- A cache keyed by base revision does not help ordinary edits, because each commit creates a new base. Trust must be keyed by file identity, which survives commits.
- A reader that raises on stored data is a bug class, not a bug: the fix is a mechanism (a registry and a test over legacy shapes), not a fourth rule.
- Saving failed in sixteen ways because an unsaved change had many homes and a reply had many classes; the fix is one home and four outcomes, enforced by one model test, not a fix per incident.
- Release 14 can carry the behaviour; the structure changes what is stored in the browser and what goes over the wire, so it needs the corpus and the model test under it first.
