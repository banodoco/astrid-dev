# Release 15 — run board

The live state of the Release 15 run, rewritten at each check-in by the release manager. The [brief](../15.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Now (00:40 UTC, Sun 22 Nov)

One lane is running, the timeline lane (Plans 69 then 77), and a batch of small fixes is waiting to land. Nothing else in the release has a manager or a branch. The owner handed the release to the Lead session `session_011EzfW1gtAhRQwk8pgJMzhG` on 21 November ([#1245](https://github.com/banodoco/astrid-dev/pull/1245)).

- **Release 15 is larger than its title.** It now lists 16 plans: the editing and saving work (69, 77, 78, 63, 76, 18, 79), speed (81), the hardening its brief is named for (39, 13, 50, 40), and 52, 53 and 72. Several are mid-flight on Release 14 branches (39, 52, 13) and have no route into `release/15/main` yet. Plans 55 and 75, the tenth-of-a-second redesigns, left the release on 22 November at the owner's request.
- **The headline has no owner.** Generation tested for real on three systems rests on issues #678 to #683, which no plan or lane owns.
- **`release/15/main` is red in one place.** In astrid-agent, 35 of 50 tests in `tests/packs/runpod/test_h3_release.py` fail on the untouched branch: it carries Plan 59's model lists with Release 14's recipes, so two pinned digests do not match (`packs/runpod/models.lock.json` and `packs/vibecomfy/models.lock.json`). The standing ruling applies: it is repaired by the forward that follows the Release 14 Lead's combination of Plan 59, not by hand.

### Timeline to publish

Not set. Release 15 starts after Release 14 publishes ([brief](../15.md)); the release manager sets the timeline and cut line once Release 14's publication date is known. The cut line is the first decision owed: the release as listed is well over 150 engineering days.

### Lanes

| Lane | Session | Brief | State |
| --- | --- | --- | --- |
| Plans 69 then 77 (editing work, then the saving loop) | Codex manager (hosted in Claude session session_011EzfW1FXS3o7GFnNSB7cZS) | [briefs/plans-69-77.md](briefs/plans-69-77.md) | Plan 69 exact App and Runtime CI add no failing IDs. Plan 69’s Agent retry has one added Windows outcome. Its authorized single-job rerun waits for the active workflow to finish. Final R2 still gates landing. Plan 77’s first saving and opening fixes landed on its plan branches. The fresh standard Round 2 run has started. |
| Plan 78 (live custom-element editing) | not started | — | Queued; builds on Plan 69; not assigned to a lane |
| Easy wins (issue packet) | Release 15 Lead, with Codex Luna workers | — | Nine fixes, one commit each, in [astrid-agent #475](https://github.com/banodoco/astrid-agent/pull/475) (draft), on `release/15/main` at `aac1ceb6`. Waiting on the owner's go to land. Editor, Runtime and VibeComfy fixes not started |
| Plan 79 (local media of any size) | not started | — | Queued; scope accepted; starts after Plan 77 lands. The interim 1 GiB limit is in the easy-wins batch |
| Plan 72 (project delivery) | its own manager, not yet accepted by the Lead | — | Hold. Its manager asked on #1245 for a go, a named single manager and a cut commit. No branch is cut and nothing is authorized until the owner decides its scope, which is still pending |
| Plans 39, 52, 13 | Release 14 Lead, on `release/14/plan-*` | — | Mid-flight under Release 14; no Release 15 branch or lane. Their accountable session moves when the owner says |
| Plan 81 (under a second to start) | not started | [handover](../../plans/81-under-a-second-to-start/handover.md) | Queued; researched and ready for a manager; US-1 needs no decision |
| Plans 50, 40, 53, 63, 76, 18 | not started | — | Queued; branches not yet cut |

### Forwards from Release 14

| Repository | Last forward | Waiting |
| --- | --- | --- |
| astrid-runtime | `1758a6df9` (#74), `release/14/main` at `8e8711fd2` | nothing |
| astrid-agent | `aac1ceb68` (#462), `release/14/main` at `7bc1012e5` | nothing |
| astrid-app | `2ef94b4cf` (#325), `release/14/main` at `e6ca6e803` | R14-FIX-16 (`128c6807a`): conflicts with Plan 59's save work on `release/15/main`; forward after the Release 14 Lead lands `release/14/int-59-64-65`, which combines them |

### Waiting on the owner

- **The cut line:** one release or two. The Lead recommends moving the remaining saving plans (63, 76, 18) to their own release.
- **Branch protection on `release/15/main`** in each product repository (no deletion, no force-push, required checks). Plan 72's manager reports it is missing; sessions cannot read or set it.
- **Plan 69's three decisions,** held by the timeline lane: the App #297 revert, narrowing admitted-animation render out of scope, and whether the motion pack is required on a bare install.
- **The go to land** [astrid-agent #475](https://github.com/banodoco/astrid-agent/pull/475) in `release/15/main`.
- **Plan 78:** its own lane, or the timeline lane after Plan 69.
- **A manager for Plan 81.** Its decisions are made.
- **A go for Plan 63's first tasks** (the corpus, CC-7, and the server piece, CC-13).
- **Who owns the cross-platform tests** (#678 to #683): a short plan is needed before any lane.
- **Plan 72's scope decision,** then its go or hold.
- Delete the superseded branches when convenient: `release/14/plan-66` (all three product repositories), `release/14/plan-77` and `release/14/plan-77-wip/*` (astrid-runtime), and `release/14/plan-69` once nobody pushes to it.

## Standing rulings

- Fixes flow forward: `release/14/main` is merged into `release/15/main`, never the reverse, and never by rebase or force-push.
- A forward that conflicts on the save path waits for the Release 14 Lead's own combination rather than resolving it twice.
- The owner approved Codex with full access in the Lead's session on 21 November 2026, and asked for Codex Luna workers wherever the work allows. The Lead reads every diff and re-runs every proof before pushing.
- A fix that would change an existing test's assertion goes to the owner first, by name.
