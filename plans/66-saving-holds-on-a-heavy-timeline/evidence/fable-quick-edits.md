# Many quick edits: is there an elegant approach now?

18 Nov 2026. Read-only: no code, plan or install was changed. The owner's question: "IS THERE NOW AN ELEGANT APPROACH THAT ACCOMMODATES MANY QUICK EDITS?"

**Read:** astrid-app `origin/release/14/plan-59` at `2ce3c44fa` (with #303): `commands/localSaveSession.ts`, `hooks/timelineLocalSaveHandoff.ts`, `commands/commitOutbox.ts`, `hooks/useTimelinePersistence.ts`. Plan 63 on `origin/plan/63-dependable-saving` at `35fc6828`.

**Labels.** **Verified** = I read the code. **Inferred** = reasoned from the code, not observed. Nothing was built or run, and I did not reproduce a burst.

## The short answer

**Not yet in the code, and not yet stated in Plan 63, but the approach is one sentence and most of it is already built.**

> While anything is queued, the screen keeps showing the person's own edits. An accepted save moves only the base the next save is sent on. The screen takes the server's document when the queue is empty.

Today the opposite happens: at every accept the session replaces the screen with the server's document, which does not contain the edits still queued, and then locks editing until the queue drains. That one step is the cause of all three failures the fix agent described. Removing it is about ten lines in one function, and it can be tried on Release 14 this week.

## 1. Root cause

### What happens in a burst (verified in code; the timings are inferred)

Each edit is captured into the outbox the moment it is made, one record per edit, before the save debounce (`useTimelinePersistence.ts:1131-1138`, "Capture every local edit before debounce coalescing"). Each record is sent as its own commit, one at a time.

| Step | What the code does | Result |
|---|---|---|
| Edit 1 | Captured, queued, sent | Fine |
| Edit 2, while save 1 is in flight | Captured on top of edit 1, queued behind it with basis "after edit 1" | **Fine.** This already works, for any number of edits made before the first accept |
| Save 1 is accepted, edit 2 still queued | The session loads the accepted document, **puts it on screen in place of the local one**, and sets `replaying` (`localSaveSession.ts:247-257`) | The screen is now the server's head. It does not contain edit 2 |
| Edit 3, any time before the queue drains | Three guards stand in a row, and each would refuse it | **Undone, or the conflict bar** |

The three guards, in the order an edit meets them:

1. **`checkHead`** (`timelineLocalSaveHandoff.ts:254-270`, called at `:483-484`). The handoff still holds the head from before the burst, because it updates only when a flush returns (`:987-1000`), and a flush returns only when the whole queue has drained. The screen was moved to the new head in the step above. They differ, so: "original verified authoring head is unavailable". This is I-4, and it is the conflict bar the fix agent saw.
2. **The same-document check** (`timelineLocalSaveHandoff.ts:494`). The session's document is now the server's; the handoff's chain still ends at edit 2. They differ.
3. **`replaying`** (`localSaveSession.ts:415`). The typed `LocalSaveDeclined` that #303 added; the edit is undone on screen with a reason.

So the failing window is from the first accept until the queue is empty. With commits at 3 to 9 seconds and a person who edits fast, the first accept almost always lands in the middle of a burst.

### Why a re-base is needed at all

Yes: it is because of how an edit is stored. A queued record holds two whole documents (`before`, `after`) and a patch tied to that chain (`localSaveSession.ts:25-34`, `:417-420`). The editor has no function that applies a queued edit to a different document: the code that knows what an edit means lives in the Agent, and the session's own comment says so ("Runtime owns suffix revalidation… never execute/recapture it here", `:248-249`).

So when save 1 is accepted, the editor cannot compute "the accepted head plus edit 2". It has two choices: keep showing its own chain, or show the server's document without edit 2. It does the second, and then has no honest "before" for a new edit until the queue is empty. Hence the lock.

The server does not need the re-base. It already takes edit 2 as authored and revalidates it on the head it has (the basis is "after edit 1", and only the base pair advances, `localSaveSession.ts:278-279`). The re-base is entirely a client-side bookkeeping problem.

A second effect of the same step, inferred and not observed: between the accept of save 1 and the accept of save 2, edit 2 is not on the screen. If that is visible, it is a flicker the owner would notice.

## 2. The elegant approach

### Is "intents, coalesced, replayed on the latest head" the right shape?

**Yes as the end state, and it has two parts with very different costs.**

| Part | What it needs | Where it belongs |
|---|---|---|
| **A. Edits never wait for, or conflict with, their own earlier saves** | No new mechanism. Keep the local chain on screen while the queue is non-empty; adopt the server's document at drain | **Plan 63, CC-5b**, and a Release 14 version (section 3) |
| **B. The screen is the accepted head with the queued intents re-applied** | A queued record must be something the editor can re-apply to any head: a named command with its arguments, not two documents | **Plan 18, TL-5** |
| **C. Unsent edits coalesce into one send** | A rule for undo. One commit is one undo step today, so sending a drop and a trim as one commit would undo them together | **Plan 18** (TL-1 item 4 decides it), with one exception below |

Part A is what stops the failures. Part B is what makes it exact: with A alone, a change someone else made (an agent, another tab) appears when the queue drains, not at each accept. Part C is a speed-up, not a fix: with A, ten quick edits are ten background saves and the person never waits on them.

The one coalescing rule cheap enough for Plan 63: **an unsent record that changes the same field of the same clip as the one before it replaces it.** That covers held-down nudges and repeated field changes, keeps one undo per value the person settled on, and needs no command layer. Anything broader waits for commands.

### Does Plan 63 say it clearly?

**No. CC-5 and TL-5 split it awkwardly, and the gap is exactly the failing case.**

- CC-5b deletes `LocalSave.before`, the `same(...)` check and `replaying`, and keeps "one display `after`" in the row until TL-5. That implies part A, but it never says **which document is on screen between an accept and the drain**. That rule is the whole behaviour.
- The first guard a quick edit hits, `checkHead`, is in `hooks/timelineLocalSaveHandoff.ts`. That file is not in CC-5b's scope, and Plan 63 does not mention it or `checkHead` (verified by search at `35fc6828`). The evidence pack assigned I-4 to "CC-5… TL-5 and TL-12 (the handoff is replaced)". So the conflict bar the owner sees today is, as written, fixed only when Plan 18 replaces the handoff.
- The model test (CC-5a) plays every outcome at every queue position, but has no step "the person edits between an accept and the drain".

### The minimal statement, and its size

Add to invariant 1, in these words or close to them:

> **While the queue is not empty, the screen shows the queue's own latest document. An accept advances only the base the next record is sent on. The screen takes the server's document when the queue is empty, and snaps to it without refusing if it differs. Nothing compares a new edit with the head: adding to the queue has no precondition, in the session or in the handoff.**

And to the tasks:
- **CC-5b:** name `hooks/timelineLocalSaveHandoff.ts` in scope; the handoff's head check and same-document check on capture go, with the session's. The same-field coalescing rule above. **About +1 day** (CC-5b from 6 to 7).
- **CC-5a:** one case family, "an edit at every point between an accept and the drain", including a burst of ten, and the fix agent's sequence (drop 1, drop 2 during save 1, an edit while 2 sends). **No extra days.**
- **Plan 18, TL-5:** unchanged. It replaces "the queue's own latest document" with "the accepted head plus the queue replayed", which is the same rule made exact.

## 3. A Release 14 version

### The change

**Do not put the server's document on screen while records are still queued.** In `localSaveSession.ts`, `pump`, the branch at `:247-257` runs on every new accept. Make it run only when the queue is empty. With records still queued, an accept then only advances `basis` (already done at `:299-303`), and the loop sends the next record.

What follows, each read from the code:
- `replaying` is never set on the live path, so guard 3 does not fire.
- The session's document stays the latest local one, so guard 2 passes.
- The screen is not moved to the new head, so the editor's head stamp still equals the handoff's, and guard 1 (`checkHead`) passes. No change to the handoff is needed.
- New edits are queued with basis "after the previous record", which is what already happens to edit 2 today.
- When the queue drains, the existing "nothing left" branch adopts the server's document, and the handoff's flush returns and takes the new head, as now.

This is the coordinator's first option in spirit (one send at a time, later edits built on what the previous accept returned) without the coalescing, and it needs no new state. The second option (treat "the head moved because of our own save" as no conflict) I would not take: relaxing `checkHead` alone runs into guard 2 and then guard 3, and getting past those means authoring edit 3 on a screen that is missing edit 2.

**Leave the reload path as it is** (`claim`, `:377`): after a reload with part of a chain accepted, the server's document still wins and an edit is declined until the chain drains. That is rare, and it is CC-5b's to finish.

### Size

- **Product code:** about ten lines in one function of `commands/localSaveSession.ts`.
- **Tests:** the hook-level test the fix agent could not pass becomes the proof; add a burst of ten. `localSaveSession.replayProtocol.test.ts` and `.lifecycle.test.ts` assert today's adopt-at-each-accept and must be updated; #303's `LocalSaveDeclined` tests stay true for the reload path.
- **About 1 to 1.5 days** with tests, one hard-tier agent.

### Risk: medium, and bounded

1. **It reverses a deliberate rule.** The comment at `:248-249` says the accepted document is installed before the next original record is sent. I read why the lock exists (section 1) but did not find a reason the *screen* must change before the next send; the send itself reads only the stored record and the base pair. If something downstream depends on it, the replay-protocol tests are where it will show. **Unverified until run.**
2. **The save watchdog.** The hook's save attempt waits on a flush that now returns only when the whole burst has drained. A long burst could trip the watchdog and show the amber "not confirmed" bar while saves are in fact landing. Check `WATCHDOG_GRACE_MS` (`useTimelinePersistence.ts:76`, `:564-585`) against a ten-edit burst at today's commit time.
3. **A foreign change shows later.** An agent's commit that merges during a burst appears at drain, not at the next accept. The screen snaps then. No data is at risk: the server merged it either way.
4. **A refusal in the middle of a burst** behaves as today: the display resets to the server's head and the bar offers Try again and Discard for the whole retained chain.

The stored shape, the wire and the outbox do not change, so nothing a tester has saved is affected, and the change is the rule CC-5b ends on, so it is not thrown away.

### Recommendation

**Do it now, as one narrow change with a stop condition.** It is the owner's main remaining failure, Plan 63 is queued in no release, and the change is small and in the direction of the end design.

- **Proof before it lands:** the drop, drop, edit sequence; ten quick mixed edits (drag, nudge, drop, trim) during a slow save; the same with one refusal in the middle; all on the staging stack with real commit times, and no watchdog bar.
- **Stop condition:** if the replay-protocol tests show that the next send needs the accepted document installed first, stop and leave it to CC-5b. Do not work around it with a relaxed `checkHead`.

What Release 14 still would not have: the same-field coalescing, an exact screen while others edit (part B), and a clean reload in the middle of a burst.

## 4. Agents editing the same timeline

The co-editing rule holds unchanged, and this approach leans on it.

- **Disjoint changes still merge on the server.** A queued editor record sent after an agent's commit is revalidated on the head that includes the agent's change, as now.
- **A clash still comes back as "moved"** (a `conflict` today): the chain is parked behind the bar, Try again resends it on the latest head. A burst makes this no more likely per edit.
- **What changes is when the owner sees the agent's work:** at the next moment their queue is empty, not at each accept. For a person editing in bursts that is a second or two after they pause. Part B (Plan 18) removes even that.
- **It helps agents.** An agent's function commit clashes with any concurrent commit and reruns up to three times. Fewer, non-blocking editor saves and the same-field coalescing mean fewer commits for it to collide with. Batching whole bursts (part C) would help more, and is another reason to decide it in Plan 18.
- **One case for the model test,** already asked for in `fable-agent-edits.md`: an accept whose head contains a foreign change, arriving mid-burst. With this rule the expected result is simple: nothing happens on screen until drain, then one snap.

## Not checked

- Nothing was run. The burst walk-through is from reading the code at `2ce3c44fa`.
- Whether the queued edit visibly disappears between accepts today.
- Why the session installs the accepted document before the next send; I found the comment, not a dependency.
- The watchdog's grace period against real burst lengths.
- The drop path's own guards (`useAssetManagement.ts`), beyond what #303's notes say.
