# Inputs — Editing together

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked how agent edits work beside a person's, and whether to split the save work into stability, speed, multi-edit robustness and extensibility. The main thread accepted the four-plan structure of an independent check; the owner then said to add it to astrid-dev and not do it yet. This plan is queued, in no release, with its release open. Next: the owner chooses the release ([Plan 63's D9](../63-dependable-saving/inputs.md#owner-decisions)) and says go; the scope PR records the answer here; only then does the plan become `Accepted`.

**Prior art:** The server already merges by address, down to a field; this plan is the small change that lets writers use it. Sources: `fable-agent-edits.md` (one clear approach to agent edits; held by the Release 14 Lead) and `fable-four-questions.md` section 2 (an agent on a person; five cases; must-haves), read against the Agent, Runtime and App code of `release/14/plan-59` (verified lines in [plan.md](plan.md)); the Haiku-reader claims are marked reported where not re-read. One reader claimed a moved head becomes a 500; that is wrong (the provider catches `StaleHead` at `commit.py:1552`).

- *One route, merge by address.* Every writer posts to `POST …/timelines/{t}/commit`; the Agent's provider replays on a moved head up to three times, then answers `head_busy`. Two writers clash when the thing is the same and one path is a prefix of the other, or either names the whole timeline.
- *Most writers name the whole timeline.* A `doc.patch` with no declared reads is forced to `atomic`; an agent's function commit is `atomic` over the whole timeline unless it declares reads; a document publish is `atomic`.
- *How the editor hears of someone else's commit.* In the reply to its own next save, or from a poll every 30 s skipped while anything is unsaved or a gesture is active. No push. Adopting a foreign document clears the undo and redo stacks and shows no notice.
- *Today's "Try again" cannot win a real clash.* It resends the same change on the latest head; a real clash is refused again.

**Approach:** Change what each writer declares (narrow by default), notice sooner, keep the person's place, say who and what, make a bundle survive `moved`, and prove it with one test with both writers. No new merge mechanism; the notice uses fields the commit already stores. Alternatives rejected: a push event instead of the 2 s check (nice-to-have, 3 days, later); the editor replaying queued edits on the new head (needs the command layer: Plan 18's TL-5); a third queue for bundles (a bundle keeps its request and key instead; sending bundles through Plan 18's one verb is the later form); merging the editor's and the Agent's queue implementations (they share a contract, not code).

**Challenge:** Reviewed: the independent four-questions check (`fable-four-questions.md`, 18 November 2026, accepted by the main thread) and the agent-edits check (`fable-agent-edits.md`, accepted earlier and applied to Plan 63). Not checked by either (open): how fine the merge is in practice (only "different clips merge, the same clip clashes" is pinned by a test); case (d), delete second, is inferred, not run; whether narrowing a function commit's default reads is safe for intents that depend on things they do not change (not surveyed: ET-1's first step); which path clears undo on a foreign head (ET-3's first step); whether `/v1/events` can carry a head change (reported as unverified, so push is sized as new work). Next: the owner's answers. **The final recommendations** (`fable-final-recommendations.md`, 18 November 2026, with `fable-end-state-review.md`; accepted by the owner) changed this plan to about 12 days: ET-0 (the clash and undo rules), ET-1's editor half cut (the editor never declares reads), ET-2 with a first check (a `timelines-updated` listener may already do it), ET-3 with undo by `timeline.inverse` and the snapshot stacks deleted, ET-4b (undo an agent's change) promoted to a must, "Keep mine" and "delete beats edit" cut. Unverified: that the server lets one actor invert another's commit; whether the listener fires for an agent's commit.

**Proof and limits:** Completion is the list in [plan.md](plan.md#completion). Limits: nothing here was built or run; no co-editing case was reproduced; the sizes are the check's judgment on Plan 63's own figures, not a bottom-up estimate.

**Review rounds:** Recommended: one (R, at the end), because it changes what writers declare on every route. Pending the owner's agreement.

**Run start:** Pending — no run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, what needs her go, and the advisor session.

### Deferred

| Item | Decision | Reason |
| --- | --- | --- |
| Push in place of the 2 s head check | Later, 3 days | Only after the check has been found wanting; whether `/v1/events` can carry a head change is unverified |
| The agent's change visible in the middle of a burst | Plan 18's TL-5 | The screen would be the accepted head with the queue replayed; until then it appears at the next pause |
| A table test of finer merges (two fields of one clip, an add beside a reorder), narrowing patch paths where it fails | Later, 1 day plus what it finds | |
| "Keep mine" as a separate feature; "delete beats edit"; automatic re-apply | **Cut** (D15, D16) | The one bar's Keep mine is the person overwriting on purpose; a delete parks like any clash |
| Highlight what changed; "an agent is working here" | Later, 3 + 2 days | (undo of the agent's change is ET-4b, a must) |

## Owner decisions

Decision ids keep the numbers they had in [Plan 18](../18-timeline-editing/inputs.md#owner-decisions). **D9 (which release) is [Plan 63's](../63-dependable-saving/inputs.md#owner-decisions): one decision for the four plans, decided 18 November 2026: Release 15.** The decisions that shape this plan are recorded there: **D16** (a clash parks, never re-applied automatically; Keep mine and Discard), **D17** (an agent's edit relies only on what its commands read and wrote; the whole timeline is opt-in). This plan has no decision of its own.

## Source identities

Before code work, record the actual repository, ref and SHA for each. This plan changes three product repositories and astrid-dev. Branches: `release/15/plan-76` in each repository the plan changes, cut from that repository's `release/15/main`.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| astrid-agent | TBD: `release/15/main` | none | Plan 63's CC-4b (the Agent client reads `outcome`) | `release/15/plan-76` | `release/15/main` |
| astrid-runtime | TBD: `release/15/main` | none | Plan 63's CC-4 (`outcome`) | `release/15/plan-76` | `release/15/main` |
| astrid-app | TBD: `release/15/main` | none | Plan 63's CC-4, CC-5b | `release/15/plan-76` | `release/15/main` |
| astrid-dev | `origin/main` | this pack | None | `plan/63-dependable-saving` (with Plans 63, 75, 18) | `main` by the scope PR |

## References

- [Plan 63 Dependable saving](../63-dependable-saving/plan.md), [Plan 75 Fast saving](../75-fast-saving/plan.md), [Plan 18 Extensible editing](../18-timeline-editing/plan.md).
- Release 14: [`releases/14.md`](../../releases/14.md); gap: [F-001](../../vision/gaps/F-001-platform-reliability.md).
- Reviews (held by the Release 14 Lead; their findings are summarised above): `fable-agent-edits.md`, `fable-four-questions.md`.

## Plan 77 evidence for ET-6

Round 5 attempted one writing tab and stopped at the guarded after-head check. Postflight preserved a single v30 head. Round 2's second-tab POST happened later after the first tab's edit remained unconfirmed. ET-6 still needs the controlled simultaneous editor, agent and bundle cases from an authenticated writable head, plus the actual clash and recovery proof. [Plan 77 Round 5 and loop closure](../77-saving-holds-on-a-heavy-timeline/rounds.md#round-5--22-november-2026-blocked-save-at-the-round-cap)
