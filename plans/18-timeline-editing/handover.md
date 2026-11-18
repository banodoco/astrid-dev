# Handover — Extensible timeline editing

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Statements](statements.md) · [Plan 63](../63-dependable-saving/plan.md) · [Release 14](../../releases/14.md)

Written on 18 November 2026 by the session that added phase 0 (the commit contract) to this plan, and edited the same day when phase 0 moved to [Plan 63, Dependable saving](../63-dependable-saving/handover.md). It is a dated snapshot for whoever manages this plan next. Nothing is built. Re-read branches with `git ls-remote` before acting.

## Where it stands

- The plan is **queued and unowned**. Phase 1 and 2 are a draft on the astrid-dev branch `plan/18-command-layer` (commits `d9ac42a4` and `bd535a5d`), local only when this was written. The main thread reviews first.
- **Phase 0 is no longer here.** The owner asked whether stability should come before extensibility, and the answer was that stability goes first, as its own project, queued in no release brief for now ([Plan 63 D9](../63-dependable-saving/inputs.md#owner-decisions), open: which release; recommended Release 15). Everything about the commit contract, its evidence, its tasks (CC-1 to CC-10, R0) and its decisions (D9 to D15) is there.
- **Phase 1 starts on the dependable-saving base.** TL-1 waits for Plan 63's CC-3, CC-4 and CC-7; RS1 and every task that changes product code wait for its R0 and end-state checks.
- What stays here from the save work: TL-5 (the document is the head plus the queue replayed), TL-10's command half (a drop is a named command; the upload half is Plan 63's CC-10) and TL-4's headlines.

## Waiting on the owner

- **D4:** which release carries phase 1 (the release after Plan 63's; recommended, since phase 1 starts on its base).
- **D5, D6 and D8** from the earlier draft are unchanged.
- D9 to D15 are Plan 63's.

## For the next manager, in order

1. Read [Plan 63](../63-dependable-saving/plan.md) and confirm its end-state checks are true; do not start code tasks before then.
2. Read [plan.md](plan.md) then [tasks.md](tasks.md#start-here). Take TL-1 once CC-3, CC-4 and CC-7 are done.
3. Re-check the template branches against the merged code before TL-1's inventory.
