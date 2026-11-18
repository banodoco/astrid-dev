# Statements — Extensible timeline editing

[Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md)

For the owner to scan in a minute. Each is true of the plan as revised on 18 November 2026 after the independent critique and with phase 0 added; say "no, not that" to any of them before tasks are dispatched, and the plan changes.

**Phase 0, the commit contract (added 18 November 2026, runs first):**

- **P1. An accepted head is a fact.** Today every save re-proves the whole saved document from scratch, which is why one save took three minutes and why an old document can refuse a new rule. After phase 0, a save does the change plus one pass over the document, however long the history, and a count-based test fails if that stops being true.
- **P2. A new rule cannot refuse a document for an old problem it did not cause.** Every whole-document rule goes through one gate and registers itself; a test runs each rule against each known old shape of document.
- **P3. A refused edit refuses that edit only, and you can always get out.** The Runtime says why in a fixed list of reasons; the editor does not read error text; a retryable one is retried; a refusal never leaves the next edit blocked, including after a reload.
- **P4. Astrid cannot store what it later refuses.** Media and catalog entries are checked once, when written.
- **P5. One set of long-lived test documents** (synthetic, no content from your timelines) runs all of this. Phase 0 does not make the editor send intent; that is phase 1 (statements 1 to 10), and phase 0 only stops the old checks growing. It waits for Release 14 and for you to choose its release (D9).

1. **Now, one gesture is described in about fourteen places. After, its meaning is described once, in the Agent; the editor keeps only a throwaway preview.** The encoders that remain return a command and nothing else.
2. **The editor stops judging the document.** It keeps a few state checks (the head is stale, undo has nothing settled, the session was lost, media was not selected). An encoder cannot refuse. Everything else the Agent and Runtime decide, so a bug in an Agent rule now shows up in the editor as a coded refusal, not behind a second opinion.
3. **Each converted gesture deletes its expected-diff block in the same change, and about 3,600 lines of TypeScript capture ports and the test-only `commitSession` family are deleted, not revived.** The check is that no App file builds `reads`, `expect` or `selections`.
4. **Gestures that refuse today on a timeline with shots start to work** (trim, split, delete, add track, cross-track move). That is a behaviour change you will see, and it needs commands that do not exist yet (cross-track move, trim by edge, track remove and reorder, plain duplicate).
5. **A refusal is a value with a code and a plain headline,** written once in the Agent; the jargon ("child ownership/fork mapping is unavailable") goes, and the silent paths (a swallowed capture refusal, a declined revert, a quiet undo) are fixed or deleted. A refused gesture returns the display to the last adopted head; a preview that disagrees with the result snaps and never refuses.
6. **The editor and an agent meet the same checks, with two tiers through one door.** Agents can send any command batch (with dry-run and an expected head); raw `doc.patch` stays for document routes but every document rule lives once, in the final validator, which both tiers hit. `doc.patch` is not retired here: it is the lowering for document publish, the sheet and function commits.
7. **No App writer sends `doc.patch`** (a repo-wide lint, with any exception named and dated), and the schema has one owner, the Agent: the Runtime copy is generated, the digest literals are deleted, and CI fails on drift.
8. **A pack can register a command, and it gets the same validation, undo and refusals with no App change.** Phase 1 proves the registry with one composite op (`clip.ripple-delete`); phase 2 proves it with an op the alternate view registers itself.
9. **Agents get one verb for any batch, a generated MCP tool and `timelines ops --json`,** with one unit and naming convention (lean: integer milliseconds) as a clean break with no aliases: existing ops that differ are renamed.
10. **The editor's own extension SDK sends the same commands; its separate patch vocabulary goes.** A generated suite runs every document x gesture x track through the Agent in CI, and a gesture cannot merge without rows in it (the manifest must contain every gesture-to-op key).
11. **It waits for Release 14, takes nothing from Plan 59, and does not touch `source_offset` meaning or the timeline UI design.** Phase 2 starts only when phase 1's checks pass and you have chosen the view.
