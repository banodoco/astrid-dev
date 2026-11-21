# Tasks — Use media in place

[Plan](plan.md) · [Inputs](inputs.md)

A draft outline: scopes name areas, not yet functions. LK-1 turns each later row into a dispatchable card with exact paths, pinned tests and focused proof; no row after LK-1 is dispatched from this outline.

**Task ids:** `LK-1` to `LK-11`, `RS1`, `R`. **Critical path:** LK-1, RS1, LK-3, LK-4, LK-8, LK-11, R. **Test inventory:** to be listed by LK-1: the Runtime's selection, verification and commit tests; the Agent's media-view and authoring tests; the App's asset-resolver and timeline-media tests.

Every card: Astrid never writes to, moves or deletes a linked file; never edit, skip or weaken an existing test to pass; a change to an existing contract names every pinned test it makes untrue.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| LK-1 The linked-media contract, written before code: what a link records, when it counts as verified, how a commit, preview, render, export and a rented machine each treat available, changed and missing, how an older client refuses it, and why the earlier path-backed realm was removed. It also turns the rows below into cards | S | D1 to D5; Plan 63's four outcomes | astrid-runtime `contract/` (a new document); this plan's `tasks.md` | The contract answers each completion case in [plan.md](plan.md#completion) with a rule; every claim in [inputs.md](inputs.md#planning-evidence) is confirmed or corrected with file and line | [ ] |
| RS1 Review stop after the contract (rounds at most 2) | S | LK-1 | read-only | Same protocol as R, on the contract; findings become rows `RS1.<n>`; LK-2 to LK-10 depend on this row. Reason: every later task builds on the contract, and a late finding would redo them | [ ] |
| LK-2 Linked folders: the creator names the folders Astrid may read; any other path is refused | X | RS1; D3 | astrid-runtime (owner-only settings and the path check); astrid-agent CLI for adding and listing folders | A path inside a linked folder is accepted; outside, through a symlink out of it, and `..` are refused | [ ] |
| LK-3 Link and read: a file is linked without copying, and its bytes are served with ranges from where it is, after a freshness check | X | LK-2 | astrid-runtime (the link record, the read route, the freshness check beside `cas.py`) | The store does not grow by the file's size; a ranged read returns the right bytes; an edited file is reported changed, a moved one missing | [ ] |
| LK-4 Commit rules: a commit that newly uses a changed or missing link is refused, naming the file; existing clips are flagged, not removed | X | LK-3; Plan 63 landed | astrid-runtime commit path; astrid-agent validation | The refusal is one of Plan 63's four outcomes; a timeline with a missing link still opens and saves | [ ] |
| LK-5 SDK and CLI: link a file, place a linked file, relink, list states | N | LK-3; D2 | astrid-agent `astrid/sdk` media and timeline; `astrid/core/cli/domain_media.py` | Each command against a real Runtime; copy remains the default | [ ] |
| LK-6 Copy in when owned bytes are needed: export, a rented machine and recovery copy a linked file into the store and say so | X | LK-3; Plan 79 landed | astrid-agent export, recovery and remote-worker deployment; astrid-runtime (link to stored object) | Export of a timeline with linked media round-trips; the copied object's digest equals the link's | [ ] |
| LK-7 Preview and render read linked media | N | LK-3 | astrid-agent rendering (allowed folders); media views | A linked clip previews and renders the same as its copied twin | [ ] |
| LK-8 The editor shows available, changed and missing, and can relink or accept new content | X | LK-4 | astrid-app asset resolution and timeline media components | Each state on a real stack; relink to a different file is refused unless accepted | [ ] |
| LK-9 The editor adds media by browsing linked folders through the Runtime | X | LK-2, LK-8; D5 | astrid-app (a browser for linked folders); astrid-runtime (a listing route limited to linked folders) | A file chosen in the browser is linked, not uploaded; the listing never leaves the linked folders | [ ] |
| LK-10 Wording for the three states, the refusals and the copy-in notice | T | LK-8 | astrid-app and astrid-agent message text only | The exact before and after of each message, checked against: plain words, names the file, says what happened, gives a next step | [ ] |
| LK-11 Live proof on a real stack | N | LK-5 to LK-10 | no product code; evidence under `plans/80-use-media-in-place/evidence/` | Every completion case in [plan.md](plan.md#completion), with the store's size before and after and the file's digest and times before and after | [ ] |
| R Review rounds (at most 2, pending the owner's agreement) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; landing waits for them | [ ] |

**Phases:** A is LK-1 to LK-7 (about 13 days); B is LK-8 to LK-10 (about 9 days with LK-11 and R). Phase A alone lets an agent use linked media end to end.
