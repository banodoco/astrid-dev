# Ten statements — Extensible timeline editing

[Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md)

For the owner to scan in a minute. Each is true of the plan as written; say "no, not that" to any of them before tasks are dispatched, and the plan changes.

1. **Now, one gesture is described in about fourteen places. After, it is described once, as a named command, and everything else sends it.** The editor stops re-deriving what its own edit should look like.
2. **The editor stops judging the document.** It keeps four checks only (the head is stale, undo has nothing settled, the session was lost, media was not selected). Everything else the Agent and Runtime decide, so a bug in an Agent rule now shows up in the editor as a refusal, not hidden behind a second opinion.
3. **Each converted gesture deletes its expected-diff block in the same change.** The handoff goes from 927 lines toward under 300; if a block survives, that gesture is not converted.
4. **Gestures that refuse today on a timeline with shots start to work:** trim, split, delete, add track, cross-track move. That is a behaviour change you will see, and it needs new commands (cross-track move, trim by edge, track remove and reorder, plain duplicate) that do not exist yet.
5. **A refusal is a value with a code and a plain headline, and an error cannot be shown without a reason.** The jargon ("child ownership/fork mapping is unavailable") goes; the silent paths (a swallowed capture refusal, a declined revert, a quiet undo) are fixed or deleted.
6. **The editor and an agent meet the same checks.** The editor sends no `doc.patch`; an agent's `doc.patch` now refuses unknown fields and out-of-range values; the refusal an agent sees carries the same code, a retry flag and the current head.
7. **`doc.patch` is not retired here.** It stays, validated, because five pack helpers still emit it. Retiring it is a later plan (D2 asks you whether to pull it forward).
8. **The schema has one owner, the Agent.** The Runtime copy is generated, the App digest literals are deleted, and CI fails on drift; a hand-edited digest is no longer possible.
9. **A generated suite runs every document x gesture x track through the Agent in CI, and a new gesture cannot merge without rows in it.** It includes a gesture after a refusal, the case no test held when this week's bugs shipped.
10. **It waits for Release 14 and takes nothing from Plan 59.** It also does not touch `source_offset` meaning, the timeline UI design or undo checkpoints. The extension proof (one alternate view on commands only, recommended a text cut list) is phase 2 and starts only when phase 1's checks pass and you have chosen the view.
