# Tasks — Editing together

[Plan](plan.md) · [Inputs](inputs.md)

A draft can use a short outline with unknowns. Before dispatch, every task needs one bounded outcome, its input and deliverable, dependencies, a suitable route, and focused proof. Name source identity where one task consumes another project's output. Reuse the prior-art and source identities in [inputs.md](inputs.md); don't repeat them.

**Task ids:** `ET-<n>`. **Critical path:** ET-1, ET-2, ET-3, ET-6 (about 8 days on the editor side after Plan 63; ET-4 and ET-5 run beside it). **Test inventory:** below.

Paths: Agent is astrid-agent, Runtime is astrid-runtime, App paths are under `src/tools/video-editor/` unless they begin `scripts/`, `src/integrations/` or `config/`. Line numbers cite the 18 November reading and **will have moved: re-check against the code at dispatch**. Routes: `N` is the default, `X` very hard, `S` super hard.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| ET-1 **Narrow reads by default** (3 days). **Editor:** every record declares the addresses its patch writes (the editor declares reads today only for split, trim, move, transition clear, a media drop, an element edit and a track label, and an element edit is sent `atomic` anyway: `timelineLocalSaveHandoff.ts:565`, `:957`; `localSaveSession.ts:269`); `atomic` only where a gesture truly needs it. **Agent:** a function commit's default reads are the things its commands touch (today `merge: \"atomic\"` over the whole timeline, `commit_session.py:771-778`); `reads=\"timeline\"` is opt-in (a ripple or \"tighten the intro\" keep it); a document publish (`timelines commit --file`, the MCP publish tool; `timeline_document.py:327`) declares its diff. **First step: survey which built-in intents need `reads=\"timeline\"`** (not done). **The plain default form lives here; the selector-declared form stays in Plan 18.** When this lands, Plan 63's CC-12 paragraph gains \"and what you relied on\". | X | Plan 63 CC-4b (agent side may start at once) | Agent `astrid/sdk/timeline/commit_session.py`, `timeline_document.py`; Runtime `timeline_commit_store.py:86-103` (read); App `hooks/timelineLocalSaveHandoff.ts`, `commands/localSaveSession.ts` | Runtime test that two moves of different clips merge and two of one clip clash (exists, `test_timeline_commit_integration.py:475`) extended to an element edit, an agent function and a document publish beside an editor edit of a different clip: all land | [ ] |
| ET-2 **The editor notices a foreign head in seconds, not 30** (1 day). A head-only check every 2 s while idle (the history read is 0.07 to 0.2 s, measured); today a poll every 30 s, skipped while anything is unsaved or a gesture is active (`useTimelineQueries.ts:8`; gating reported, `usePollSync.ts`). | N | Plan 63 CC-5b | App `hooks/useTimelineQueries.ts`, `hooks/usePollSync.ts` | App test: an agent's commit while the editor is idle is seen within the check interval; none is fetched during a gesture or while a save is out | [ ] |
| ET-3 **Adopting keeps the person's place** (2 days, unverified). Adopting a foreign document today clears the undo and redo stacks and shows no notice (`useTimelineHistory.ts:308-322`). Undo and redo survive (undo by inverse of the person's own steps exists on the server, reported `test_real_inverse_preserves_newer_disjoint_work…`); selection, playhead and scroll are kept. **First step: trace which path clears undo on a foreign head in the Runtime-backed editor** (the local stacks are cleared, read; the editor also sends server-side undo, `timeline.inverse`, and how the two relate was not traced). | X | ET-2, Plan 63 CC-5b | App `hooks/useTimelineHistory.ts`, `hooks/useTimelinePersistence.ts` (adopt) | App test: an adopted foreign head keeps selection, playhead and undo; an undo after it undoes the person's own step only | [ ] |
| ET-4 **Who and what** (1.5 days). The quiet line from the commit's `label`, `source.via` and publisher (all already stored, reported `sync.py:1036-1046`): \"Agent · Added 12 animations\", for a few seconds, no bar; shown within about a second of the person pausing. | N | ET-2 | App `components/` (the line), `hooks/useTimelinePersistence.ts` | App test: an adopted foreign commit shows its label and writer once | [ ] |
| ET-5 **A bundle publish survives `moved`** (2 days). The authoring writer has no outbox and no pending record (`authoring_bundle.py:1923-1924`, reported): a reply that is not accepted raises, and a lost reply with a random key leaves nothing to replay. Make it keep its request and key until it has an answer and, if `moved`, re-read and re-attach without generating anything again (a bundle is an addition with narrow reads: it relies only on what it attaches to). **First step: trace which path the Almost Ready animation bundle took** (the Runtime's publish route is retired; a bundle now goes through the authoring-bundle writer to the commit route, `authoring_bundle.py:1916`; Plan 63's CC-4b has the same first step and records the answer). **No third queue:** this reuses the one pending-record mechanism, and sending bundles through Plan 18's one verb is the later form. | X | Plan 63 CC-4b | Agent `authoring_bundle.py`, `authoring_remote.py`, `authoring_commit.py:24-81` | Agent test: a bundle whose reply is lost is sent again with the same key and lands once; a `moved` bundle re-attaches without re-generating | [ ] |
| ET-6 **A test with both writers on a real stack** (2 days). A burst in the editor, an agent function and a bundle on one timeline: cases (a) to (e) of [plan.md](plan.md#outcome-and-scope) as rows, on the staging stack (never the timeline the owner views; a sandbox timeline). Includes the editor and an agent on one head, disjoint and clashing (Plan 63's model test has the editor-side rows). | N | ET-1 to ET-5 | staging stack tests | One test file with rows (a) to (e); the person's screen never jumps, no change is refused for an unrelated edit, and a clash parks one change with the clip named | [ ] |
| R Review round (one round; recommended: it changes what writers declare on every route). Read-only review of the integrated candidate against the cases and the negatives. **Starting N split (3):** one reader per repository. | S | ET-1 to ET-6 | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md#review-and-promotion-boundaries): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; closing waits for them | [ ] |

## Start here

For a newcomer picking up ET-1 (agent side) once the owner has chosen the release and said go; the editor tasks wait for Plan 63's CC-4, CC-4b and CC-5b.

**Prerequisites.** The owner's choice of release (open) and a go; Release 14's merged save fixes; Plan 63's CC-4, CC-4b and CC-5b for the editor half. If any is missing, stop and ask the Lead.

**Repositories.** `release/<NN>/plan-65` in astrid-agent, astrid-runtime and astrid-app, cut from `release/<NN>/main`; astrid-dev `plan/63-dependable-saving` (this pack, with Plans 63, 64, 18).

**Commands** (call the scripts by their literal paths; see [`env/README.md`](../../env/README.md)):

```text
bash scripts/worker-env/agent-setup.sh
bash scripts/worker-env/runtime-setup.sh
bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_commit_integration.py
# astrid-dev, before pushing a plan change (Python 3.10 or newer)
python3 scripts/astrid_dev.py check && python3 -m unittest discover -s scripts -p "test_*.py"
```

## Critical path and estimates

**Editor side, after Plan 63:** ET-1 (3 d), ET-2 (1), ET-3 (2), ET-6 (2) is about 8 days; ET-4 (1.5) and ET-5 (2) run beside it. **About 11.5 engineering days in total** (3 + 1 + 2 + 1.5 + 2 + 2). The Agent half (ET-1 for agents, ET-5) can start at once. The sizes are the independent check's judgment on top of Plan 63's own figures, not a bottom-up estimate; ET-3 is unverified.

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
| ET-C3 | An adopted foreign head keeps selection, playhead and undo, and shows one quiet line with the writer and the label | ET-3, ET-4 App tests |
| ET-C4 | A bundle whose reply is lost is sent again with the same key and lands once | ET-5 Agent test |

Negative cases: a writer that omits its reads is `atomic` by request, not by default; a ripple intent keeps `reads="timeline"`. Limits: see [plan.md](plan.md#completion).
