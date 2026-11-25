# Tasks — Editing together

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Inputs](inputs.md)

A draft can use a short outline with unknowns. Before dispatch, every task needs one bounded outcome, its input and deliverable, dependencies, a suitable route, and focused proof. Name source identity where one task consumes another project's output. Reuse the prior-art and source identities in [inputs.md](inputs.md); don't repeat them.

**Task ids:** `ET-<n>`. **Critical path:** ET-0, ET-1, ET-2, ET-3, ET-6 (about 8.5 days on the editor side after Plan 63; ET-4, ET-4b and ET-5 run beside it). **Test inventory:** below. The target architecture is stated once, in [Plan 63's end state](../63-dependable-saving/plan.md#outcome-and-scope); this plan is its client policy on `moved` and its undo.

Paths: Agent is astrid-agent, Runtime is astrid-runtime, App paths are under `src/tools/video-editor/` unless they begin `scripts/`, `src/integrations/` or `config/`. Line numbers cite the 18 November reading and **will have moved: re-check against the code at dispatch**. Routes: `N` is the default, `X` very hard, `S` super hard.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| ET-0 **State the clash rule and the undo rule** (0.5 day; new). Clash: a change is accepted if and only if nothing it relied on or wrote was changed by another writer between the head it named and the current head, and it introduces no new finding; otherwise `moved`, **and the reply names the addresses and the commits that changed them**; a writer's own earlier queued records do not count as another writer (`basis: {after: id}`; Plan 18's TL-1 settles the rest). Undo: the edit still queued is removed from the queue; in flight or accepted, append `timeline.inverse` naming it, through the same queue, proof rule and four outcomes; a same-address change since is `moved` (`inverse_conflict` maps to `moved`) and the undo parks ("The agent changed this since; Keep mine undoes it anyway"); the undo list is the person's own records, so it survives an adopted foreign head. Written once, in the contract, linked from Plan 18's TL-1. | N | Plan 63 CC-4 | the Runtime commit contract (`contract/commit-v2.md`) and the Agent wording | The `moved` reply carries addresses and commits (a Runtime test); the rules are one section each | [ ] |
| ET-1 **Narrow reads by default, Agent half only** (timing pending owner D17 reconciliation; land with ET-4b inverse safety) (2 days, was 3; **the editor half is cut**: the editor declares nothing new and never declares reads, and the server derives the written addresses from the patch and ignores the values it sends, Plan 63's CC-16). **Relies only on what the commands read and wrote; the whole timeline is opt-in ([D17](../63-dependable-saving/inputs.md#owner-decisions)).** **Agent:** a function commit's default reads are the addresses its commands read and wrote through the recorder (today `merge: "atomic"` over the whole timeline, `commit_session.py:771-778`); `reads="timeline"` is the one opt-in (a ripple or "tighten the intro" keep it); a document publish (`timelines commit --file`, the MCP publish tool; `timeline_document.py:327`) has its diff derived on the server. **First step: survey which built-in intents need `reads="timeline"`** (not done). **The plain default form lives here; Plan 18 no longer has a selector-declared form (cut).** When this lands, Plan 63's CC-12 paragraph gains "and what you relied on". | X | Plan 63 CC-16, CC-4b | Agent `astrid/sdk/timeline/commit_session.py`, `timeline_document.py`; Runtime `timeline_commit_store.py:86-103` (read) | Runtime test that two moves of different clips merge and two of one clip clash (exists, `test_timeline_commit_integration.py:475`) extended to an agent function and a document publish beside an editor edit of a different clip: all land; an agent function that reads a clip the person then edits gets `moved` | [ ] |
| ET-2 **The editor notices a foreign head in seconds, not 30** (1 day). **First check: a `timelines-updated` event listener already exists (`useTimelineRealtime.ts:13-22`, reported). If it fires for an agent's commit, relax the gating and add no 2 s check;** otherwise a head-only check every 2 s while idle (the history read is 0.07 to 0.2 s, measured). Today a poll every 30 s, skipped while anything is unsaved or a gesture is active (`useTimelineQueries.ts:8`; gating reported, `usePollSync.ts`). | N | Plan 63 CC-5b | App `hooks/useTimelineQueries.ts`, `hooks/usePollSync.ts`, `hooks/useTimelineRealtime.ts` | App test: an agent's commit while the editor is idle is seen within seconds; none is fetched during a gesture or while a save is out | [ ] |
| ET-3 **Adopting keeps the person's place** (2 days). Adopting a foreign document today clears the undo and redo stacks and shows no notice (`useTimelineHistory.ts:308-322`). **Undo already goes by `timeline.inverse` of the person's own records in the Runtime-backed editor (`timelineLocalSaveHandoff.ts:346-365`, `:1040-1085`, reported), with targets from server history filtered to this actor; the snapshot stacks (100 whole-document entries, cleared on any foreign head, `useTimelineHistory.ts:205-223`, `:308-323`) are the fallback for an editor with no Runtime save. Delete them on the Runtime-backed path; keep selection, playhead and scroll.** The server refuses an inverse of a field someone has since changed (`inverse_conflict`) and leaves unrelated newer work alone (`inverse.py:1117-1119`, reported); the App maps it to `moved`, so the undo parks. | X | ET-0, ET-2, Plan 63 CC-5b | App `hooks/useTimelineHistory.ts`, `hooks/useTimelinePersistence.ts` (adopt) | App test: an adopted foreign head keeps selection, playhead and undo; an undo after it undoes the person's own step only; an undo of a field an agent changed since parks | [ ] |
| ET-4 **Who and what** (1.5 days). The quiet line from the commit's `label`, `source.via` and publisher (all already stored, reported `sync.py:1036-1046`): \"Agent · Added 12 animations\", for a few seconds, no bar; shown within about a second of the person pausing. | N | ET-2 | App `components/` (the line), `hooks/useTimelinePersistence.ts` | App test: an adopted foreign commit shows its label and writer once | [ ] |
| ET-4b **Undo the agent's change from the line** (1 day; **promoted from a nice-to-have to a must**: it is the safety valve for narrow default reads, whose accepted risk is a valid edit made on slightly old information). The same `timeline.inverse` command, from the "who and what" line. **First check, unverified: that the server lets one actor invert another's commit.** | N | ET-3, ET-4 | App `components/` (the line), `hooks/useTimelineHistory.ts` | App test: one click on the line inverts the agent's commit through the queue; a same-address change since parks | [ ] |
| ET-5 **A bundle publish survives `moved`** (R16 minimal attempt/key custody and proof: [P63 CC-4b](../63-dependable-saving/tasks.md#proposed-release-16-reconciliation--25-november-2026); no second queue) (2 days). The authoring writer has no outbox and no pending record (`authoring_bundle.py:1923-1924`, reported): a reply that is not accepted raises, and a lost reply with a random key leaves nothing to replay. Make it keep its request and key until it has an answer and, if `moved`, re-read and re-attach without generating anything again (a bundle is an addition with narrow reads: it relies only on what it attaches to). **First step: trace which path the Almost Ready animation bundle took** (the Runtime's publish route is retired; a bundle now goes through the authoring-bundle writer to the commit route, `authoring_bundle.py:1916`; Plan 63's CC-4b has the same first step and records the answer). **No third queue:** this reuses the one pending-record mechanism, and sending bundles through Plan 18's one verb is the later form. | X | Plan 63 CC-4b | Agent `authoring_bundle.py`, `authoring_remote.py`, `authoring_commit.py:24-81` | Agent test: a bundle whose reply is lost is sent again with the same key and lands once; a `moved` bundle re-attaches without re-generating | [ ] |
| ET-6 **A test with both writers on a real stack** (2 days). A burst in the editor, an agent function and a bundle on one timeline: cases (a) to (e) of [plan.md](plan.md#outcome-and-scope) as rows, on the staging stack (never the timeline the owner views; a sandbox timeline). Includes the editor and an agent on one head, disjoint and clashing (Plan 63's model test has the editor-side rows). | N | ET-1 to ET-5 | staging stack tests | One test file with rows (a) to (e); the person's screen never jumps, no change is refused for an unrelated edit, and a clash parks one change with the clip named | [ ] |
| R Review round (one round; recommended: it changes what writers declare on every route). Read-only review of the integrated candidate against the cases and the negatives. **Starting N split (3):** one reader per repository. | S | ET-1 to ET-6 | read-only | Rounds per the [run contract](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/run-contract.md#review-and-promotion-boundaries): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; closing waits for them | [ ] |

## Start here

For a newcomer picking up ET-1 (agent side) once the owner has chosen the release and said go; the editor tasks wait for Plan 63's CC-4, CC-4b and CC-5b.

**Prerequisites.** The owner's choice of release (open) and a go; Release 14's merged save fixes; Plan 63's CC-4, CC-4b and CC-5b for the editor half. If any is missing, stop and ask the Lead.

**Repositories.** `release/15/plan-76` in astrid-agent, astrid-runtime and astrid-app, cut from `release/15/main`; astrid-dev `plan/63-dependable-saving` (this pack, with Plans 63, 75, 18).

**Commands** (call the scripts by their literal paths; see [`env/README.md`](../../env/README.md)):

```text
bash scripts/worker-env/agent-setup.sh
bash scripts/worker-env/runtime-setup.sh
bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_commit_integration.py
# astrid-dev, before pushing a plan change (Python 3.10 or newer)
python3 scripts/astrid_dev.py check && python3 -m unittest discover -s scripts -p "test_*.py"
```

## Critical path and estimates

**Editor side, after Plan 63:** ET-0 (0.5 d), ET-1 (2), ET-2 (1), ET-3 (2), ET-6 (2) is about 7.5 days plus ET-3's wait; ET-4 (1.5), ET-4b (1) and ET-5 (2) run beside it. **About 12 engineering days in total** (0.5 + 2 + 1 + 2 + 1.5 + 1 + 2 + 2). The Agent half (ET-0, ET-1 for agents, ET-5) waits for Plan 63's CC-16 and CC-13, and ET-1 for the survey. The sizes are the final recommendations' judgment on top of Plan 63's own figures, not a bottom-up estimate; ET-3 and ET-4b are unverified.

## Test inventory

| Test | Fate | Why |
| --- | --- | --- |
| Runtime `tests/test_timeline_commit_integration.py` (two moves of different clips merge; two of one clip clash) | Keep; extend (ET-1) | the merge-by-address pin |
| App `hooks/useTimelineHistory` tests | Rewrite the foreign-head adopt cases (ET-3) | undo is kept |
| Agent authoring-bundle tests | Extend (ET-5) | a lost reply is sent again |

**New:** the two-writer test (ET-6).

## End-state checks

| # | Check | Guarded by |
| --- | --- | --- |
| ET-C1 | Cases (a) to (e) are rows of one two-writer test on a real stack and pass | ET-6 |
| ET-C2 | A function commit, an element edit and a document publish beside an editor edit of a different clip all land | ET-1's Runtime test |
| ET-C3 | An adopted foreign head keeps selection, playhead and undo, and shows one quiet line with the writer and the label; the snapshot stacks are gone on the Runtime-backed path; one click on the line undoes an agent's change | ET-3, ET-4, ET-4b App tests |
| ET-C4 | A bundle whose reply is lost is sent again with the same key and lands once | ET-5 Agent test |

Negative cases: a writer that omits its reads is `atomic` by request, not by default; a ripple intent keeps `reads="timeline"`. Limits: see [plan.md](plan.md#completion).

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

| Canonical home | Proposed bounded amendment |
| --- | --- |
| ET-5 / ET-1 / ET-4b | P63 CC-4b receives minimal durable exact-attempt/key custody and its proof. New ET-1 narrow defaults and the ET-4b inverse safety valve land and prove together only after the pending D17 timing decision; the rest of P76 remains later. |
