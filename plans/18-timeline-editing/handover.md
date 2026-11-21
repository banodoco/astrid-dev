# Handover — Extensible timeline editing

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Statements](statements.md) · [Plan 63](../63-dependable-saving/plan.md) · [Release 14](../../releases/14.md)

Written on 18 November 2026 by the session that added phase 0 (the commit contract) to this plan, and edited the same day when phase 0 moved to [Plan 63, Dependable saving](../63-dependable-saving/handover.md). It is a dated snapshot for whoever manages this plan next. Nothing is built. Re-read branches with `git ls-remote` before acting.

## Where it stands

- The plan is **queued and unowned**. Phase 1 and 2 are a draft on the astrid-dev branch `plan/18-command-layer` (commits `d9ac42a4` and `bd535a5d`), local only when this was written. The main thread reviews first.
- **Phase 0 is no longer here.** The owner asked whether stability should come before extensibility, and the answer was that stability goes first, as its own project, queued in no release brief for now ([Plan 63 D9](../63-dependable-saving/inputs.md#owner-decisions), open: which release; recommended Release 15). Everything about the commit contract, its evidence, its tasks (CC-1 to CC-10, R0) and its decisions (D9 to D15) is there.
- **Re-phased on 18 November 2026 (final recommendations, accepted by the owner): phase A, agents and packs (about 18 days; Agent and Runtime only), starts after Plan 63's server track and does not wait for R0 or the week; phase B, editor gestures (about 44 days), waits for Plan 63's R0 and a week of editing; phase C, the alternate view, is deferred.** TL-1 waits for Plan 63's CC-3, CC-4 and CC-7. New: TL-3e (close the set) and EX-P (the pack-op proof). Cut: the Runtime's schema copy and sync script, selector-declared reads, automatic re-apply and "delete beats edit". About 62 days plus 8.5 optional.
- What stays here from the save work: TL-5 (the document is the head plus the queue replayed), TL-10's command half (a drop is a named command, and the durable upload record), TL-4's closed reason list with headlines and TL-2's sync script (moved here from Plan 63's CC-4), and TL-5's opaque-payload swap.

## Waiting on the owner

- **D4:** which release carries phase B (the owner decided Release 15 for the four saving plans, [Plan 63's D9](../63-dependable-saving/inputs.md#owner-decisions); phase B may not fit).
- **D5 is decided: the alternate view is deferred.** D6 and D8 from the earlier draft are unchanged.
- D9 (the release, decided: Release 15) is Plan 63's, one decision for the four saving plans (Plans 63, 75, 76 and this one); D10 to D19 are Plan 63's or Plan 75's (D14).

## For the next manager, in order

1. Read [Plan 63](../63-dependable-saving/plan.md) and confirm its end-state checks are true; do not start code tasks before then.
2. Read [plan.md](plan.md) then [tasks.md](tasks.md#start-here). Take TL-1 once CC-3, CC-4 and CC-7 are done.
3. Re-check the template branches against the merged code before TL-1's inventory.
