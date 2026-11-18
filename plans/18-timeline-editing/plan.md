# 18 — Extensible timeline editing

**Project:** Extensible timeline editing

**Goal:** Every timeline gesture is one named command that people, agents and extensions all send, and anyone can add a command of their own, so an edit means the same thing everywhere and a refusal always says why.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Phase 1 about 60 (about 25 elapsed); phase 2 about 9 (about 7 elapsed), scoped at the phase gate.

**Waiting on:** [Plan 63, Dependable saving](../63-dependable-saving/plan.md) (phase 1 starts on its base; nothing here that changes product code starts before its R0 and end-state checks); Release 14 to be published; the owner's answers on D4 (the release for phase 1), D5 (the view) and, only if TL-1 cannot settle it, D8 (the unit convention) in [inputs.md](inputs.md#owner-decisions). The independent critique is done and accepted.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. **To begin once Plan 63's base is in:** read [tasks.md](tasks.md#start-here) (prerequisites, repositories, commands), then take TL-1. It waits for Plan 63's CC-3, CC-4 and CC-7.

**Vision gaps:** [LS-003 — Composable frontend and backend contributions](../../vision/gaps/LS-003-full-stack-contributions.md) (primary). Phase 2 proves one timeline-specific foundation, not the whole workspace and component contract. The reliability work it used to carry, and its F-001 role, is [Plan 63's](../63-dependable-saving/plan.md).

## Outcome and scope

## Phase 0 moved: dependable saving

The commit contract that was this plan's Phase 0 (CC-1 to CC-8, with the rewritten CC-4 and CC-5, the new CC-9 and CC-10, and R0) is now [Plan 63, Dependable saving](../63-dependable-saving/plan.md), a first project of its own, queued in no release brief (which release carries it is [Plan 63's D9](../63-dependable-saving/inputs.md#owner-decisions), open; recommended Release 15). Stability goes first, so extensibility builds on top. **Phase 1 starts on the dependable-saving base:** it waits for Plan 63's CC-3, CC-4 and CC-7 (TL-1) and for its R0 and end-state checks (RS1 and every task that changes product code). Nothing about phase 0 is kept here: the root cause, the seven contract statements, the Release 14 fix table, the evidence, the issue ledger and the decisions D9 to D15 live in Plan 63.

What stays in this plan from the save work: **TL-5** (the document is the head plus the queue replayed, the end form of Plan 63's invariant 1), **TL-10's command half** (a drop is a named command; the upload half is Plan 63's CC-10), TL-4's headlines, and the statement that the editor sends intent and adopts the head ([#852](https://github.com/banodoco/astrid-dev/issues/852)), which Plan 63 holds with a ratchet (CC-8) and this plan delivers.

**What creators and agents get.** Dragging, trimming, splitting, dropping and typing in the editor stop failing for reasons the creator cannot see. The editor no longer judges whether its own edit looks right: it says what the person did ("trim this shot's end to 4.2 s"), the Agent and Runtime decide, and the editor shows the document that comes back. When something is refused, the message says in plain words what and why, and the same code reaches an agent over the CLI, the SDK or MCP.

**Phase 1: one command layer (about 60 days).** Included:

1. **Every gesture is a named op the editor sends.** The editor's gestures (21 rows in the [inventory](tasks.md#gestures-and-their-ops): drop, move, cross-track move, trim clip edge, trim shot edge, split, delete, inspector field edit, Source In/Out, element edit, duplicate, undo, redo, track add, rename, reorder and remove, and the rest) each map to one Agent op. Missing ops are added: cross-track move, trim by timeline edge, split and trim of an occurrence's children, track removal and reorder, a plain clip duplicate, and `clip.set` coverage for speed and volume.
2. **The editor sends and adopts, with dumb encoders.** One `sendIntent`, generalised from `occurrence.trim`. An encoder returns only `{op, select, args}`: it reads no document, builds no `reads`, `expect` or `selections`, and cannot refuse. The local edit is a disposable preview; intents queue in order; adoption waits while a gesture is active; a refusal returns the display to the last adopted head; a mismatch snaps and never refuses. Each converted gesture deletes its expected-diff block and the refusals it made dead. The TypeScript capture ports (about 3,600 lines), the `commitSession.ts` family and the generic whole-document diff path are deleted.
3. **The op layer is the extension point.** `register_operation(name, parameters, handler, intent, singleton)`; the built-ins register through it; the schema, an ops listing and the contract page are generated from the registry; a composite op built only from other handlers (`clip.ripple-delete`) proves a new command gets validation, atomicity, undo and coded refusals for free.
4. **One op vocabulary in the App.** The editor extension SDK's `apply()` takes the same Agent ops through `sendIntent`; its separate `TimelinePatch` vocabulary is retired. No App writer sends `doc.patch` (a repo-wide lint); `placementService.ts` and `shotTimelineDataProvider.ts` convert or are named, dated exceptions.
5. **Agents can send ops.** One CLI verb takes a JSON command batch (`--dry-run`, `--json`, `--expected-head`), one MCP tool is generated from the registry, and `timelines ops --json` lists the ops. One unit and naming convention (lean: integer milliseconds), a clean break with no aliases.
6. **A refusal is a value:** `{ok:false, code, headline, retryable}`. The code list closes on the Agent side (reusing `hint`, `suggested_command` and `status`, with a falling ratchet on uncoded errors); headlines live once, in the Agent; save status is `{status:'error', reason}`; the silent paths in the inventory are fixed or deleted.
7. **Two tiers through one door.** `doc.patch` stays for document routes, but every document invariant lives once in `validate_final_candidate`, which both tiers hit.
8. **One schema owner.** The Agent owns `edit-command.schema.json`; the Runtime copy is generated and CI-checked; the App's digest and contract constants come from the generated file.
9. **A generated suite in CI.** A seeded Agent generator writes a document x gesture x track matrix, with raw-parity rows; the Agent replays intents on real documents; the editor side is a small gesture-to-op table test; both are required checks.

**Phase 2: the extension proof (about 9 days; Plan 18's original scope).** One alternate view or workflow over the same material, built only on the phase 1 commands and **registering at least one op of its own** through the registry, with undo and a coded refusal and no App change. Recommended: a text-first cut list (D5).

**Deferred or out of scope:** a redesign of the timeline UI; the meaning of `source_offset` ([#851](https://github.com/banodoco/astrid-dev/issues/851), decided for Plan 59: the window origin); the Agent's whole-head validation ([Plan 63](../63-dependable-saving/plan.md), CC-3, [#842](https://github.com/banodoco/astrid-dev/issues/842)); retiring `doc.patch` as the lowering for document routes (a later plan); the Runtime's replay-memo cost ([Plan 63](../63-dependable-saving/plan.md), CC-2, [#846](https://github.com/banodoco/astrid-dev/issues/846)); anything in Release 14 or Plan 59.

## Existing work and decision

We build on `occurrence.trim`, the one gesture already built as intent plus adopt-the-head: 18 changed lines in the handoff, no expected diff, and the Runtime owning the rules. We also reuse the Agent's 37 ops, the Runtime's provider design (it loads the Agent's validators, so there is one meaning of an op), and the Agent's `Recording`, which already gives every handler atomicity, authoritative reads and derived undo. The App's capture ports are not reused: they are a second implementation of the Agent's handlers (about 3,600 lines) that the template does not need. The smallest sound approach is to convert every gesture to that shape and delete the code it makes dead, not to add a fifth description of each gesture. The independent critique of 18 November found the first draft built a consumer API, not an extension point; all eight of its gaps were accepted (see Challenge in [inputs.md](inputs.md#planning-evidence)). The evidence, the alternatives, the open challenge and the owner's decision are in [inputs.md](inputs.md#planning-evidence); this draft is not accepted.

## Sequence and readiness

**Phase 1 starts on the dependable-saving base.** [Plan 63](../63-dependable-saving/plan.md) goes first, and phase 1 consumes its output: TL-1 waits for Plan 63's CC-3 (the delta gate), CC-4 (the four outcomes) and CC-7 (the corpus, which TL-15b extends rather than builds a second one); RS1, and with it every task that changes product code, waits for Plan 63's R0 and end-state checks. Phase 1 takes nothing from Release 14's other work: Plan 59 lands the shot-trim gesture, the edit-refusals fix and the `source_offset` rule first, and phase 1 builds on that base. Order: TL-1 writes the command contract and its findings (the load-bearing design: op per gesture, the unit convention, the registry and how the Runtime loads pack-registered ops, the editor SDK vocabulary, the responsiveness rule, the refusal codes); **review stop RS1** follows; then four strands run in parallel (schema owner, registry and new ops; the refusal value, send-and-adopt and the editor SDK; the generated suite; the agent surface); then the gesture conversions run in parallel and each lands with its rows in the matrix; then the generic path is deleted and the end-state checks go in; then the final review. The critical path is in [tasks.md](tasks.md#critical-path-and-estimates). The phase 2 gate: phase 1's end-state checks pass and the owner has chosen the view (D5). Unresolved: D4, D5 and possibly D8; the rest are recommended or ruled by the main session.

## Interfaces and handoff

**Consumes:** the dependable-saving base from [Plan 63](../63-dependable-saving/plan.md#interfaces-and-handoff) (the corpus, the rule registry and delta gate, the four-outcome reply and `send(): Outcome`, the one queue row and the model test, the ratchet file, the one object reader, uploads as queue records), and Release 14's published tip of each product repository (identified by SHA at TL-1, in [inputs.md](inputs.md#source-identities)), including `occurrence.trim`, the edit-refusals fix and the window-origin `source_offset` rule; the Agent's baseline rule from #842.

**Produces:** (1) the command contract, generated from the registry and the code list into `docs/timeline-command-contract.md` in astrid-agent, with the TL-1 findings; (2) `register_operation`, so a pack can add a command; (3) the schema-sync script and CI check; (4) the gesture matrix and its generator, which any later gesture must extend to merge; (5) the editor handoff as one `sendIntent` plus a table of gesture-to-op encoders; (6) the CLI batch verb, the MCP tool and `timelines ops --json`. Limits: the non-remote `saveTimeline` fallback and local undo snapshots follow the TL-1 decision (delete, or named as a second path); Runtime schema bumps still need a paired App pin. Product pull requests link here when they exist.

## Completion

Done when each of these is true, each guarded by a named test that fails if it stops being true (the full list with test names is in [tasks.md](tasks.md#end-state-checks); Plan 63's end-state checks are true before phase 1 starts):

1. **No expected-diff block remains:** no App file constructs `reads`, `expect` or `selections`, and no encoder can refuse.
2. **Every gesture is one named op, and the App has one op vocabulary:** the exhaustive gesture-to-op table is checked against the generated types, and the extension SDK's old patch vocabulary is gone.
3. **No App writer sends `doc.patch`:** a repo-wide lint, with any exception named and dated; `applyEdit` requires an intent by type.
4. **Agents and the editor use the same ops:** one CLI verb takes any command batch with dry-run and an expected head, an MCP tool is generated from the registry, `timelines ops --json` lists the ops; `doc.patch` is a second tier through the same validator.
5. **A refusal cannot reach the user without a code and a headline;** the count of uncoded Agent errors only falls; an error status cannot be set without a reason.
6. **One schema owner:** CI fails when the Runtime copy, generated types, the App contract or the registry-generated schema differ; no digest literal is left.
7. **A generated suite runs in CI through the Agent:** at least 12 documents x every gesture x every track, plus a gesture after a refusal and raw-parity rows; the manifest contains every gesture-to-op key and cannot shrink.
8. **Phase 2:** the alternate view registers at least one op of its own, with undo and a coded refusal and no App change, and edits the same document as the editor with identical results.
9. **Responsiveness:** two fast gestures with the first refused leave the display at the last adopted head.
10. **The registry is the extension point:** a composite op built from other handlers gets validation, atomicity, undo and coded refusals with no per-op plumbing.

Negative case: a deliberately wrong gesture encoder (a trim that sends a track change) must fail the table test and the matrix before it fails a user. Limits: this proves the editor and the Agent agree on the op layer, not that every possible stored document is covered; Release 14 and the anonymised real documents set the floor. Integration and publication follow the [run contract](../../skills/shared/run-contract.md); this plan authorizes neither.
