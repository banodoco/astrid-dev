# Handover — Dependable saving

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Statements](statements.md) · [Plan 18](../18-timeline-editing/plan.md) · [Release 14](../../releases/14.md)

Written on 18 November 2026 by the session that moved Plan 18's Phase 0 here. It is a dated snapshot for whoever manages this plan next. Nothing is built. Re-read branches with `git ls-remote` before acting.

## Where it stands

- The plan is **queued and unowned**, in no release brief; the owner said to add it to astrid-dev and not to start it. Which release carries it is D9 (open; recommended Release 15). It is a draft on the astrid-dev branch `plan/63-dependable-saving`; the main thread reviews it first.
- Phase 0 of Plan 18 was **moved** here, not copied, with the save-category design's deltas applied, and then **cut to its lean form** by an independent Fable check the same day, accepted by the main thread (about 31.5 days, two independent tracks, App critical path about 11.5 days; about 34 with the agent-edits additions). CC-10 is an in-memory upload retry, CC-9 two tests, CC-8 and the ratchet files outside the Agent are gone, CC-4 sets `outcome` on the commit and import routes only (the closed reason list and sync script went to Plan 18's TL-4 and TL-2), D15 is the park-with-the-tail form. Added: the old-Runtime decoder fallback, migration of owners and drafts, the other outbox users, the two-tab rule, the import-wait re-measurement, I-3 marked covered by `save-recovery-2`, and CC-11 (immutable accepted history). Plan 18 now depends on this plan and took the opaque record payload, the rule owner prefix and purity, and the `retryable` wording fix.
- The save fixes already merged on Release 14 (N1 to N12, the `_reference_basis` fix, Runtime #61 to #63 and #65, App #299 to #300, `release/14/save-recovery-2`) are the base. Their branches were in flight on 18 November; CC-1 starts by checking each against merged code.
- Reviewed: the earlier Phase 0 by Opus (merge with edits); this plan by an independent Fable check (`fable-dependable-saving-check.md`, held by the Release 14 Lead), applied. The agent-edits answer (`fable-agent-edits.md`) is applied: one rule for both kinds of writer, CC-4b (the Agent's client and envelope read `outcome`, one reply fixture), CC-12 (the guidance paragraph and the installed-skills gap), two co-editing cases, about 2.5 days on the Agent track (total about 34).

## What is proven, and what is not

Proven by reading, not running: the profile numbers, the 16 incidents and the root-cause reading come from the 18 November reviews (private, held by the Release 14 Lead). **Not proven:** which path the Almost Ready bundle took (CC-4b's first step); how the editor adopts a head an agent moved while its queue is empty (CC-5a's first step); that the merged fixes reach the counts the contract states (nobody has run the scaling test; CC-1 is the first run); that "about 3 s" per save is reachable after the `_reference_basis` fix (33% of a measured 9 s, not measured); that old Runtimes really meet a new hosted editor (if pins always pair them, the CC-4 fallback shrinks to a test); that the Runtime's moved-head path for a non-restore commit never surfaces as a 503 (unverified); that `shotTimelineDataProvider.ts` and `placementService.ts` are reachable in the shipped editor; the 1.5-day size of CC-11 (its first step is to inventory what updates or deletes history rows today); that `discardScope` is fenced against a row another tab holds (the model test's two-tab case must show it); the trigger of the 400 "inputs changed"; how the conflict card opens after a `rejected` outcome (reproduce first in CC-5b).

## Waiting on the owner

- **D9:** which release (recommended Release 15). **D15:** what a refused change looks like (recommended, lean form: parked together with everything queued behind it, two buttons, Try again and Discard). The only decision on the critical path; needed before CC-5b.
- **D14:** persist verified trust across restarts. **D10:** the corpus data. Confirm or overrule D11 and D12.

## For the next manager, in order

1. Read [plan.md](plan.md), then [tasks.md](tasks.md#start-here). Do not start before the owner has chosen the release (D9) and said go; the plan's branches are then `release/<NN>/plan-63`.
2. Two tracks. App: CC-5a (the model test, grown from the seed) first, CC-4 beside it, then CC-5b (write the two-tab rule first), CC-10 and CC-9; critical path CC-4, CC-5b, CC-10, R0. Agent and Runtime: CC-7, then CC-1 and CC-2, CC-3 then CC-6, CC-11 after CC-1, and CC-4b then CC-12 (the Agent's side of the four outcomes, then the guidance paragraph).
3. Put D15 to the owner now.
4. When the scope PR merges, the Lead reopens #842 as the mechanism and links this plan on #826, #846, #732 and #852 (see the ledger in [inputs.md](inputs.md#issue-ledger)), and files the deferred items ([inputs.md](inputs.md#deferred)).

## What this run taught

- A cache keyed by base revision does not help ordinary edits, because each commit creates a new base. Trust must be keyed by file identity, which survives commits.
- A reader that raises on stored data is a bug class, not a bug: the fix is a mechanism (a registry and a test over legacy shapes), not a fourth rule.
- Saving failed in sixteen ways because an unsaved change had many homes and a reply had many classes; the fix is one home and four outcomes, enforced by one model test, not a fix per incident.
- The same plan cut by about a fifth when read by someone who did not write it: transport and uploads were tidiness, a stored `File` doubles video bytes in the browser, a ratchet at zero is a lint, and a reason list that cannot decide behaviour belongs with headlines.
- Release 14 can carry the behaviour; the structure changes what is stored in the browser and what goes over the wire, so it needs the corpus and the model test under it first.
