# Statements — Dependable saving

[Current proposed plan](plan.md) · [Task dispositions](tasks.md) · [Decisions and evidence](inputs.md)

**27 November 2026 planning revision for review.** These are the proposed R16 outcomes. The [18 November statements](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/63-dependable-saving/statements.md) remain historical; their unconditional burst formula has not been silently accepted in another form.

1. **Your edits stay yours while saving.** Astrid keeps each captured edit durably, shows your work while saves drain, and says Saved only after the matching server receipt. It reports failure to keep work locally instead of hiding it.
2. **A lost reply does not create another edit.** Astrid keeps the exact request and key, resolves that attempt, and never treats an unreadable acknowledgement as proof nothing happened.
3. **A real conflict asks for your decision.** The clashing edit and everything already queued behind it park together. Keep mine requests an overwrite, subject to normal validation. Discard lets you leave the local view and cancel unsent work even offline; Astrid retains evidence of any unanswered write and does not pretend it was remotely cancelled. New editing can continue from the current visible document while parked work stays recoverable.
4. **Another tab or agent cannot claim your pending work.** Each writer has recoverable custody, even when two agents share the same account. Stale callbacks and old owners cannot settle or delete a sibling's work.
5. **Undo works through the same safe path.** It targets your action, settles unknown in-flight writes first, preserves later disjoint edits and explains real overlaps. It does not overwrite a newer timeline with an old snapshot.
6. **An imported file is not imported again just because placement failed.** P79 keeps the import receipt and exact media selection; P63 retries captured placement. Reload protection covers both phases. A forced close may require reselecting the same file, not silently losing or duplicating the work.
7. **Existing safety stays.** Runtime authentication, verified media, accepted history, legacy compatibility, owner fences and pending drafts remain until a safe replacement is proved. This plan reuses landed saving work and repairs the demonstrated gaps.
8. **Saving and concurrency get separate judgments.** One implementation and installed witness serves P63 and P04, but both must pass their own acceptance. Historical unit tests or a parked packet are not a usable-product result.
9. **Performance remains an explicit gate.** Keep the 50 ms local-kept criterion and comparable 300-clip 2-second median / 4-second maximum target, with separate heavy-history/undo/reopen evidence. Broader P75 architecture is later. A missed target returns to you with evidence.
10. **One decision makes the burst promise executable.** The recommendation is byte-bounded ordered work with honest backpressure, preserved captured edits and measured drain, instead of an unconditional two-save-time promise for arbitrarily large edits. That acceptance change and D17's timing stay visible for review in [inputs](inputs.md#decisions-needed).

This is a planning correction, not an implementation start or release approval. The full task and source records are linked above.
