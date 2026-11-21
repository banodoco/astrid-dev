# Release 15 — run board

The live state of the Release 15 run, rewritten at each check-in by the release manager. The [brief](../15.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Now (19:45 UTC, Sat 21 Nov)

Release 15 is set up and nothing has started. `release/15/main` carries `release/14/main` (forwarded twice on 21 November; App R14-FIX-16 still to come), and the first lane, Plans 69 then 77, has its branches and brief ready for a manager ([setup](https://github.com/banodoco/astrid-dev/issues/1224)).

### Timeline to publish

Not set. Release 15 starts after Release 14 publishes ([brief](../15.md)); the release manager sets the timeline and cut line once Release 14's publication date is known.

### Lanes

| Lane | Session | Brief | State |
| --- | --- | --- | --- |
| Plans 69 then 77 (editing work, then the saving loop) | Codex manager (hosted in Claude session session_011EzfW1FXS3o7GFnNSB7cZS) | [briefs/plans-69-77.md](briefs/plans-69-77.md) | Plan 69 Runtime and Agent review batches landed on plan branches. The installed effect and save/reopen proofs passed. The owner resolved the three scope decisions and granted conditional PE-3 approval. The vendor restore, managed-render refusals, exact full CI and review 2 are open. Plan 77 direct stack landed. The unpushed Runtime repair passed the nine-track probe, while the older Runtime refused the heavy seed after 12 clips. The full fixture and baseline remain open. The standalone Release 14 App and Agent forwards are held for the integrated save path ([#796](https://github.com/banodoco/astrid-dev/issues/796)). |
| Plan 78 (live custom-element editing) | not started | — | Queued; builds on Plan 69; not assigned to a lane |
| Plans 39, 13, 50, 40, 63, 75, 76, 18, 72 | not started | — | Queued; branches not yet cut |

### Forwards from Release 14

| Repository | Last forward | Waiting |
| --- | --- | --- |
| astrid-runtime | `1758a6df9` (#74), `release/14/main` at `8e8711fd2` | nothing |
| astrid-agent | `aac1ceb68` (#462), `release/14/main` at `7bc1012e5` | nothing |
| astrid-app | `2ef94b4cf` (#325), `release/14/main` at `e6ca6e803` | R14-FIX-16 (`128c6807a`): conflicts with Plan 59's save work on `release/15/main`; forward after the Release 14 Lead lands `release/14/int-59-64-65`, which combines them |

### Waiting on the owner

- Hand the [lane brief](briefs/plans-69-77.md) to a manager.
- Whether Plan 78 joins that lane after Plan 69.
- Delete the superseded branches when convenient: `release/14/plan-66` (all three product repositories), `release/14/plan-77` and `release/14/plan-77-wip/*` (astrid-runtime), and `release/14/plan-69` once nobody pushes to it.

## Standing rulings

- Fixes flow forward: `release/14/main` is merged into `release/15/main`, never the reverse, and never by rebase or force-push.
- A forward that conflicts on the save path waits for the Release 14 Lead's own combination rather than resolving it twice.
