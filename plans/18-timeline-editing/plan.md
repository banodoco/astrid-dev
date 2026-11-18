# 18 — Extensible timeline editing

**Project:** Extensible timeline editing

**Goal:** Every timeline gesture is one named command that people, agents and extensions all send, so an edit means the same thing everywhere and a refusal always says why.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Phase 1 about 55 engineering days (about 22 elapsed with parallel workers); phase 2 about 10 (about 8 elapsed), scoped at the phase gate.

**Waiting on:** Release 14 to be published (nothing here starts before it); the owner's answers on D2 to D7 in [inputs.md](inputs.md#owner-decisions); the independent critique.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. **To begin once Release 14 is published:** read [tasks.md](tasks.md#start-here) (prerequisites, repositories, commands), then take TL-1.

**Vision gaps:** [LS-003 — Composable frontend and backend contributions](../../vision/gaps/LS-003-full-stack-contributions.md) (primary). Phase 2 proves one timeline-specific foundation, not the whole workspace and component contract. Phase 1 also serves [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md).

## Outcome and scope

**What creators and agents get.** Dragging, trimming, splitting, dropping and typing in the editor stop failing for reasons the creator cannot see. The editor no longer judges whether its own edit looks right: it says what the person did ("trim this shot's end to 4.2 s"), the Agent and Runtime decide, and the editor shows the document that comes back. When something is refused, the message says in plain words what and why, and the same code reaches an agent over the CLI, the SDK or MCP.

**Phase 1: one command layer (about 55 days).** Included:

1. **Every gesture is a named op.** The editor's twenty-one gestures (drop, move, cross-track move, trim clip edge, trim shot edge, split, delete, inspector field edit, Source In/Out, element edit, duplicate, undo, redo, track add, rename, reorder and remove, and the rest in [tasks.md](tasks.md#gestures-and-their-ops)) each map to one Agent op. Missing ops are added: cross-track move, trim by timeline edge, split and trim of an occurrence's children, track removal and reorder, a plain clip duplicate, and `clip.set` coverage for speed and volume.
2. **The editor sends and adopts.** One send-and-adopt path generalised from `occurrence.trim`. Each converted gesture deletes its expected-diff block and the `refuse()` sites it made dead, in the same change. The generic whole-document diff path and `doc.patch` emission leave the editor.
3. **A refusal is a value:** `{ok:false, code, headline}` from one closed list; save status is `{status:'error', reason}`; no boolean returns, thrown strings or side-channel marks. The silent paths in the inventory are fixed or deleted.
4. **One schema owner.** The Agent owns `edit-command.schema.json`; the Runtime copy is generated and CI-checked; the App's digest and contract constants come from the generated file, and no digest literal remains in code or tests.
5. **A generated suite.** A seeded Agent generator writes a document x gesture x track matrix; the Agent replays it through the op layer and the editor handoff must emit the same commands, in CI on every pull request, including a gesture after a refusal.
6. **Agents meet the same checks.** `doc.patch` is validated per field from the op schemas (D2); the refusal envelope keeps `kind`, gains a stable code, a retry flag and the current head; the skills and MCP descriptions teach the named ops.

**Phase 2: the extension proof (about 10 days; Plan 18's original scope).** One alternate view or workflow over the same material, built only on the phase 1 commands, with evidence that it edits, undoes and survives conflicts exactly like the editor. Recommended: a text-first cut list (D5). If it needs anything but a command, that is a missing command and is filed.

**Deferred or out of scope:** a redesign of the timeline UI; the meaning of `source_offset` ([#851](https://github.com/banodoco/astrid-dev/issues/851), decided for Plan 59: the window origin); the Agent's whole-head validation ([#842](https://github.com/banodoco/astrid-dev/issues/842), Release 14); retiring `doc.patch` and migrating its pack helpers (D2); the Runtime's replay-memo cost; anything in Release 14 or Plan 59.

## Existing work and decision

We build on `occurrence.trim`, the one gesture already built as intent plus adopt-the-head: 18 changed lines in the handoff, no expected diff, and the Runtime owning the rules. We also reuse the Agent's 37 ops, the Runtime's provider design (it loads the Agent's validators, so there is one meaning of an op), and the App capture encoders that already match Agent goldens. The smallest sound approach is to convert every gesture to that shape and delete the code it makes dead, not to add a fifth description of each gesture. The evidence, the alternatives, the open challenge and the owner's decision are in [inputs.md](inputs.md#planning-evidence); this draft is not accepted.

## Sequence and readiness

Starts after Release 14 is published and takes nothing from it: Plan 59 lands the shot-trim gesture, the edit-refusals fix and the `source_offset` rule first, and phase 1 builds on that base. Order: TL-1 writes the command contract (the one load-bearing design: op per gesture, refusal codes, what the editor may still check); **review stop RS1** follows; then three strands run in parallel (schema owner and new ops; the refusal value and send-and-adopt; the generated suite scaffold); then the gesture conversions run in parallel and each lands with its rows in the matrix; then the generic path is deleted and the end-state checks go in; then the final review. The critical path is in [tasks.md](tasks.md#critical-path-and-estimates). The phase 2 gate: phase 1's end-state checks pass and the owner has chosen the view (D5). Unresolved: D2 to D7.

## Interfaces and handoff

**Consumes:** Release 14's published tip of each product repository (identified by SHA at TL-1, in [inputs.md](inputs.md#source-identities)), including `occurrence.trim`, the edit-refusals fix and the window-origin `source_offset` rule; the Agent's baseline rule from #842.

**Produces:** (1) the command contract: the closed op list per gesture, the refusal code list with headlines, and the send-and-adopt rule, in `docs/timeline-command-contract.md` in astrid-agent; (2) the schema-sync script and CI check; (3) the gesture matrix golden and its generator, which any later gesture must extend to merge; (4) the editor handoff as a table of gesture-to-op encoders. Limits: the editor's offline and undo-checkpoint paths for non-remote timelines are not changed; Runtime schema bumps still need a paired App pin. Product pull requests link here when they exist.

## Completion

Done when each of these is true, each guarded by a named test that fails if it stops being true (the full list with test names is in [tasks.md](tasks.md#end-state-checks)):

1. **No expected-diff block remains in the handoff.** A structural test reads the handoff and fails if a gesture's branch builds anything but one command, or the file grows past its ratchet (target under 300 lines, from 927).
2. **Every gesture is one named op,** from one exhaustive gesture-to-op table whose op names are checked against the Agent schema.
3. **The editor emits no `doc.patch`,** checked across the whole matrix.
4. **Agents and the editor use the same ops:** the matrix is generated by the Agent and the editor must reproduce its commands exactly; raw `doc.patch` refuses unknown fields and out-of-range values.
5. **A refusal cannot reach the user without a code and a headline:** the closed code list has a headline for every code (test), `refuse(` and bare error throws are forbidden outside the one factory (lint), and an error status cannot be set without a reason (type).
6. **One schema owner:** CI fails when the Runtime copy, the generated types or the App contract differ from the Agent's schema, and no digest literal is left.
7. **A generated suite runs in CI through the Agent:** at least 12 documents (the 3 stored corpus documents, an anonymised long-lived timeline with shots, and recipe bases) x every gesture in the table x every track, plus a gesture after a refusal; the case count is recorded in the golden's manifest and the test fails if it shrinks.
8. **Phase 2:** the alternate view's edits, undo and conflict handling are shown on the same document with the same commands, and nothing but commands was needed.

Negative case: a deliberately wrong gesture encoder (a trim that sends a track change) must fail the matrix before it fails a user. Limits: this proves the editor and the Agent agree on the op layer, not that every possible stored document is covered; Release 14 and the anonymised real documents set the floor. Integration and publication follow the [run contract](../../skills/shared/run-contract.md); this plan authorizes neither.
