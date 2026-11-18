# Tasks — Extensible timeline editing

[Plan](plan.md) · [Inputs](inputs.md)

A draft can use a short outline with unknowns. Before dispatch, every task needs one bounded outcome, its input and deliverable, dependencies, a suitable route, and focused proof. Name source identity where one task consumes another project's output. Reuse the prior-art and source identities in [inputs.md](inputs.md); don't repeat them.

**Task ids:** `TL-<n>` for phase 1 (the command layer), `EX-<n>` for phase 2 (the extension proof). **Critical path:** TL-1, RS1, TL-4, TL-5, TL-10, TL-12, R (about 22 elapsed days; see [below](#critical-path-and-estimates)). **Test inventory:** the existing test files this plan affects are listed [below](#test-inventory).

Paths: App paths are under `src/tools/video-editor/` unless they begin `scripts/`, `src/integrations/` or `config/`. "Agent" is astrid-agent, "Runtime" is astrid-runtime. Line numbers cite the template branch (`task/plan59-shot-trim`) and **will have moved after Release 14: re-check against the code at dispatch**.

## Phase 1: one command layer

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| TL-1 **Command contract.** Re-inventory gestures, refusals and tests on the real post-Release-14 base (the template's counts are in inputs.md). Write `docs/timeline-command-contract.md`: one op per gesture (the table below, finalised), the args of each missing op (D3 settled), the closed refusal-code list with a plain headline each and a `retryable` flag, the rule for what the editor may still check itself (stale head, undo state, session loss, unselected media; nothing about document shape), where the code list lives (Agent, generated into the App), and the send-and-adopt rule. | S | Release 14 published | Agent `docs/timeline-command-contract.md`; Agent `tests/docs/test_timeline_command_contract.py` (new: every op the doc names exists in `astrid/core/timeline/schema/edit-command.schema.json` or is listed as "new, TL-3x" with an args sketch; every refusal code has a headline and a `retryable` value; every gesture row names an op) | [ ] |
| RS1 Review stop after the command contract. Protects every later task: three repositories build on these op shapes and codes, so a late finding would redo them. Rounds at most 1. | S | TL-1 | read-only | Same protocol as R, on TL-1's integrated result; findings become rows `RS1.<n>`; the tasks built on it depend on this row | [ ] |
| TL-2 **One schema owner** ([#854](https://github.com/banodoco/astrid-dev/issues/854)). The Agent owns `edit-command.schema.json`. Runtime's copy `contract/schemas/edit-command.json` is generated from the Agent checkout the Runtime already pins (`tests/astrid-agent.pin`) and checked in CI (today they are byte-identical by hand, with no check). Delete `supportsFullV2Commit()`'s hard-coded digest, contract version and component sha (`src/integrations/runtime/contract-metadata.ts:20-27`) in favour of the generated constants, and the stale digest literals in test mocks (`PropertiesPanel.mounted.test.tsx:28`, `useTimelineTrackManagement.persistence.test.tsx:26`, `useTimelineCommandsService.persistence.test.tsx:30`). Add `runtime.lock.json` to an npm check that runs in CI. | X | RS1 | Runtime `scripts/sync-edit-command-schema.py` (new) and `contract/schemas/edit-command.json`, `tests/test_edit_command_schema_matches_agent.py` (new); App `scripts/check-runtime-lock.mjs` (new) and `package.json`, `src/integrations/runtime/contract-metadata.ts`, the three test mocks | Runtime `tests/test_edit_command_schema_matches_agent.py`, `tests/test_timeline_current_union_contract.py`; App `src/integrations/runtime/contractMetadata.test.ts` (new) plus `npm run check:runtime-lock`; negative case: edit one byte of the Runtime copy and the check fails | [ ] |
| TL-3a **Track ops.** Add `track.remove` and `track.move` (order) to the Agent registry and schema, with inverses. | N | RS1, TL-2 | Agent `astrid/sdk/timeline/` (new handler module, `commands.py:operations`), `edit-command.schema.json`, `astrid/core/timeline/inverses.py`; schema sync via TL-2 | Agent `tests/editing_conformance/test_recipe_track_ops.py` (new), `tests/sdk/test_timeline_current_union_schema.py` (reviewed-additions list), Runtime `tests/test_timeline_current_union_contract.py` | [ ] |
| TL-3b **Move across tracks and trim by timeline edge.** `clip.move` gains the optional `track` (D3) and a timeline-edge trim op (name settled in TL-1) that keeps content anchored and moves or crops the edge; both for parent clips and occurrence children, with the Runtime boundary checks `occurrence.trim` already has (neighbours, minimum duration). | X | RS1, TL-2 | Agent `astrid/sdk/timeline/capture.py:move`, `_trim_commands.py`, `edit-command.schema.json`; Runtime schema via TL-2 | Agent `tests/editing_conformance/test_recipe_m1_commands.py` (move cases), `test_recipe_m2_clip_trim.py`, new `test_recipe_clip_resize.py`; negative cases: move into a track of the wrong kind, trim past a neighbour | [ ] |
| TL-3c **Children of shots.** `clip.split` and `clip.trim` accept `occurrence:X/clip:Y`; a source slip for an occurrence child that changes the source window without moving the clip. Uses the window-origin `source_offset` rule Plan 59 lands ([#851](https://github.com/banodoco/astrid-dev/issues/851)); it must not add a guard copy. | X | RS1, TL-2 | Agent `_split_commands.py`, `_trim_commands.py`, the one `source_offset` helper from Plan 59 | Agent `tests/editing_conformance/test_occurrence_window_rule.py`, new `test_recipe_occurrence_child_split_trim.py`; Agent `tests/core/timeline/test_occurrence_window_projection.py` | [ ] |
| TL-3d **Plain clip duplicate and field coverage.** `clip.duplicate` (promote `clip.duplicate-media`'s sibling to the schema) and `clip.set` coverage for `speed` and `volume` (or `clip.set-params` named in the contract) so every inspector field has a typed op. | N | RS1, TL-2 | Agent `_clip_scalar_commands.py`, `native_parent_media_commands.py`, `edit-command.schema.json` | Agent `tests/editing_conformance/test_recipe_clip_scalar_fields.py`, new `test_recipe_clip_duplicate.py` | [ ] |
| TL-4 **The refusal value** ([#853](https://github.com/banodoco/astrid-dev/issues/853)). `EditResult = {ok:true, head} | {ok:false, code, headline, retryable}` from the closed list in TL-1, the Agent as owner and a generated App copy. Save status becomes `{status:'error', reason}`, so an error cannot be set without one. Replace the boolean returns, thrown strings and the `issuedFailuresRef` WeakSet mark with it; fix the silent paths (capture refusal swallowed until the next save `useTimelinePersistence.ts:1098-1100`; revert declined with no message `:1127`, `:1133`; undo going quiet in `historyTargets`; `useAssetManagement.ts:398`, `:412`; recovery-draft read failure that reloads silently `useTimelineSave.ts:771-775`). Keep the Release 14 edit-refusals fix's revert-by-one-edit behaviour; do not add a second draft store. | X | RS1 | App `lib/editResult.ts` (new), `hooks/timelineLocalSaveHandoff.ts` (`refuse`, the factory only), `hooks/useTimelinePersistence.ts`, `hooks/useTimelineSave.ts`, `hooks/useAssetManagement.ts`, `hooks/useTimelineHistory.ts`, `lib/timeline-diagnostics.ts`; Agent `astrid/sdk/timeline/_commit_wording.py` (code list home) | App `lib/editResult.test.ts` (new: every code has a headline; no code outside the list type-checks), `hooks/useTimelinePersistence.test.tsx` (new cases: refuse, then edit, then Discard; undo declined shows a headline), `hooks/useAssetManagement.test.tsx`; ESLint rule forbidding `new TimelineSaveError(` and bare `refuse(` outside the factory | [ ] |
| TL-5 **Send and adopt, once.** Generalise the `occurrence-trim` branch (`timelineLocalSaveHandoff.ts:339-349`, `flush` `:755-779`) into one `sendIntent(command)`; the gesture kind union becomes an exhaustive table `GESTURE_OPS` (kind to encoder to op). Reuse the capture encoders in `commands/` that already match Agent goldens. Freeze: a test fails if a branch builds anything but one command, and the handoff has a line ratchet. | X | RS1, TL-4 | App `hooks/timelineLocalSaveHandoff.ts`, `commands/gestureOps.ts` (new), `commands/localSaveSession.ts` (read only unless the adopt path needs a change) | App `hooks/timelineLocalSaveHandoff.occurrenceTrim.test.ts` (unchanged and green), new `hooks/timelineLocalSaveHandoff.structure.test.ts` (every kind has an op in the generated schema types; no `same(`/expected construction; line ratchet) | [ ] |
| TL-15a **The generated suite, scaffold.** Agent generator `scripts/gen_gesture_matrix.py` (seeded, deterministic) writes `tests/fixtures/gesture_matrix/matrix.json` (documents in both Agent bundle and App document form, cases `{doc, gesture, target track/clip, args, expected command or expected refusal code}`, a manifest with counts and a digest). Agent replays through `commands.execute` and `validate_final_candidate`; the App handoff test reads a copy and requires the same command, byte for byte. Starts with the gestures that already have ops (occurrence trim, move, trim, split, label, add media), and **a conversion task is not done until its gestures are rows**. Includes the gesture-after-a-refusal case. | X | RS1 | Agent `scripts/gen_gesture_matrix.py`, `tests/editing_conformance/test_gesture_matrix.py`, `tests/fixtures/gesture_matrix/`; App `hooks/__fixtures__/gesture-matrix/matrix.json` and `hooks/timelineLocalSaveHandoff.matrix.test.ts` (new); precedent `commands/fixtures/clip_move_parity.py` | Agent `tests/editing_conformance/test_gesture_matrix.py` (also fails if the manifest shrinks or the digest differs from the App copy); App `hooks/timelineLocalSaveHandoff.matrix.test.ts`; negative case: a trim encoder that sends a track change fails both | [ ] |
| TL-15b **Real documents in the suite.** Add an anonymised long-lived timeline with shots (the incident document class of [#839](https://github.com/banodoco/astrid-dev/issues/839)), multi-track documents with stored order unlike track order, and legacy shapes; video and audio drops; nonzero and mapping-form `source_offset`. Needs a document copy from the owner (see D-data below). | N | TL-15a | Agent `tests/fixtures/gesture_matrix/docs/`; the generator's document list | Same two tests; the manifest records at least 12 documents | [ ] |
| TL-6 **Convert: move, nudge, transition clear, cross-track move.** Rows 4, 5, 19, 20 of the gesture table. Deletes the move/transition-clear expected-diff block (`timelineLocalSaveHandoff.ts:408-440`, 33 lines, plus the shared identity check `:394-405`) and the move reads (`:658-721`); fixes the false refusals on long-lived timelines for these gestures. | N | TL-3b, TL-5, TL-15a | App `hooks/timelineLocalSaveHandoff.ts`, `hooks/useClipDrag.helpers.ts`, `hooks/useTimelineTrackManagement.ts`, `hooks/useClipEditing.ts`, `commands/clipMoveCapture.ts` | Matrix rows for these gestures green in both tests; App `hooks/timelineLocalSaveHandoff.test.ts` (move cases rewritten to assert one command), `hooks/useTimelinePersistence.test.tsx` (P2 table, move rows) | [ ] |
| TL-7 **Convert: trim clip edge, Source In/Out, split, inspector scalars.** Rows 6, 8, 10, 12. Deletes the placement-baseline helper (`:273-323`, 51 lines, eight refusal sites), the trim/split reads (`:697-724`) and the shot-timeline gate for these kinds (`:336`). | N | TL-3b, TL-3c, TL-3d, TL-5, TL-15a | App `hooks/timelineLocalSaveHandoff.ts`, `hooks/useClipResize.ts`, `hooks/clip-editing/useClipSplitting.ts`, `hooks/useClipEditing.ts`, `commands/clipTrimCapture.ts`, `commands/clipScalarCapture.ts` | Matrix rows green; `hooks/useClipResize.test.tsx` (clamp and snap kept); `hooks/timelineLocalSaveHandoff.test.ts` (trim and split cases); a test that a shot-bearing document now accepts a clip trim and a split | [ ] |
| TL-8 **Convert: tracks.** Rows 15 to 18: add, rename, reorder, remove. Deletes the track-label expected diff (`:441-449`). | N | TL-3a, TL-5, TL-15a | App `hooks/timelineLocalSaveHandoff.ts`, `hooks/useTimelineTrackManagement.ts`, `commands/trackLabelCapture.ts` | Matrix rows green; `commands/localSaveSession.trackLabelRefusal.test.ts` (kept); `hooks/useTimelineTrackManagement.persistence.test.tsx` | [ ] |
| TL-9 **Convert: element and overlay parameters.** Row 11. Unify the two save paths (`timelineLocalSaveHandoff.ts:450-494` and `useTimelineSave.ts:77-96`, about 65 lines of expected state) into one send of `clip.set-element` or `clip.set-params` as TL-1 names. | X | TL-5, TL-15a | App `hooks/timelineLocalSaveHandoff.ts`, `hooks/useTimelineSave.ts`, `hooks/useClipEditing.ts`, `runtime/element-contract.ts` | Matrix rows green; `hooks/useTimelineSave.currentContract.test.tsx` (rewrite one assertion) and `hooks/useTimelineSave.test.tsx` (element cases) | [ ] |
| TL-10 **Convert: drops and duplicates.** Rows 1, 2, 3, 13a, 13c, 21 (file drop, asset drop, panel clip, duplicate generated clip and plain clip, image onto a shot). Deletes the prepared-media expected diffs (`:371-377`, `:557-578`) and the shape, registry and preview refusals (about ten of the 14 sites in `:499-729`). Keeps the three "media not selected" guidance cases and maps them to the Runtime's rejection code. | X | TL-3d, TL-5, TL-15a | App `hooks/timelineLocalSaveHandoff.ts`, `hooks/useExternalDrop.ts`, `hooks/useAssetManagement.ts`, `lib/panel-clip-drag.ts`, `hooks/useTimelineCommit.ts`, `commands/parentClipAddCapture.ts` | Matrix rows green (including video and audio drops from TL-15b); `hooks/mountedFileDrop.test.tsx`; `hooks/useTimelineCommandsService.persistence.test.tsx`; `commands/commitSession.placement.test.ts` | [ ] |
| TL-11 **Convert: delete, undo, redo, shot gestures.** Rows 9, 13b, 14. `clip.delete`, `occurrence.delete`, `placement.unplace`, `occurrence.duplicate`, `timeline.inverse` through `sendIntent`; undo keeps the "history not settled" guard (`:192`, `:194`) as a coded refusal. | N | TL-5, TL-15a | App `hooks/useShotGroupHandlers.ts`, `hooks/clip-editing/useClipDeletion.ts`, `hooks/useTimelineHistory.ts`, `lib/shot-group-commands.ts`, handoff `appendInverse` | Matrix rows green; `commands/commitSession.occurrenceDuplicate.test.ts` (kept); history tests in `hooks/useTimelinePersistence.test.tsx` | [ ] |
| TL-12 **Delete the generic path and prove the end state.** Remove the whole-document diff mapper (`changes()` `:215-270`, seven refusal sites), `appendDocument`, and the generic `doc.patch` lowering (`commands/genericPatchCapture.ts`, `commitSession.genericPatch.test.ts`); a gesture with no named op is a compile error. Revive the capture encoders the live path now imports; delete the rest of the test-only `commands/commitSession.ts` family by evidence of what is imported (D7). Add the end-state tests. | X | TL-6, TL-7, TL-8, TL-9, TL-10, TL-11, TL-13a | App `hooks/timelineLocalSaveHandoff.ts`, `commands/commitSession.ts`, `commands/genericPatchCapture.ts`, `commands/localSaveSession.ts` (the `doc.patch` dispatch at `:231-238`), the tests named in the inventory | New `hooks/timelineCommandLayer.endState.test.ts` (checks 1, 2, 3, 5 below); the whole matrix; `knip` finds no unused export | [ ] |
| TL-13a **Agents meet the same checks.** `doc.patch` validated per field from the op schemas (D2): unknown fields and out-of-range values are refused, as `clip.move` with `on = -5` already is. The refusal envelope keeps `CommandError.kind`, uses the TL-1 code instead of `conflict` for both conflict and refusal, adds `retryable` and a machine `next`, and always carries the current head; `--json` never degrades to one stderr line (`cli_common.py:22-47`). | X | RS1, TL-2 | Agent `astrid/sdk/timeline/_doc_patch.py`, `_doc_patch_schema.py` (`scripts/gen_doc_patch_schema.py`), `commands.py:validate_command`, `_commit_errors.py`, `packs/timeline/cli_native.py`, `packs/timeline/cli_common.py`, `astrid/sdk/contracts.py`; Runtime `runtime_protocol/timeline_commit_port.py:refused` | Agent `tests/editing_conformance/test_doc_patch_v2.py` (kept, plus new negative cases), new `tests/sdk/test_refusal_envelope.py` (the three offline probes of the planner become fixtures: out-of-domain `hold`, unknown key, previous-value mismatch each give code, retryable, head), `tests/sdk/test_timeline_public_command.py`; Runtime `tests/test_timeline_commit_contract.py` | [ ] |
| TL-13b **Teach the named ops; check drafts at edit time.** Local draft edits (`timelines edit` non-native forms, `Checkout.set`) run `validate_command` when made, not at commit; the skill (`docs/references/editing.md:84-120`), `docs/timeline-editing-guide.md` and the MCP tool descriptions (`mcp_server.py:563-590`) name the ops as the way to edit and `doc.patch` as internal. | N | TL-13a | Agent `packs/timeline/cli.py`, `astrid/sdk/timeline/api.py`, the three docs, `astrid/mcp_server.py` | Agent `tests/editing_scenarios` (add scenarios for a refused draft edit), `scripts/check_docs`-style link check the repository already runs | [ ] |
| TL-14 **Headlines.** Plain-language wording for every code in the closed list and for the Agent's `_commit_wording.py`, each headline naming what happened and what to do, with no jargon ("child ownership/fork mapping" must not survive). | T | TL-4, TL-13a | The code-list file from TL-4; App `lib/editResult.ts` copy only | `lib/editResult.test.ts` (no banned jargon list; each headline under a length bound); owner reads the list once | [ ] |
| TL-16 **CI that runs it.** The matrix tests and the App handoff tests run on every pull request to the release and `main` branches in both repositories as required checks, with the declared skips in one registry. | N | TL-15a | `.github/workflows/` in Agent, App and Runtime | A pull request that breaks a matrix row fails its check (shown once with a deliberately broken encoder on a scratch branch) | [ ] |
| R Review rounds (at most 2, D6; recommended for cross-repository protocol and data-safety work). Read-only review of the integrated candidate against the end-state checks and the negative cases. | S | TL-1 to TL-16 | read-only | Rounds per the [run contract](../../skills/shared/run-contract.md#review-and-promotion-boundaries): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

## Phase 2: the extension proof

Starts at a gate: the end-state checks 1 to 7 pass and the owner has chosen the view (D5). Estimates are lower confidence than phase 1 and are rescoped at the gate from what phase 1 actually exposed.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| EX-1 **Map the extension points.** Where can a pack or an outside agent contribute a view today (pack conventions, [LS-003](../../vision/gaps/LS-003-full-stack-contributions.md), the editor's own panels), and which of those the hosted editor honours. Record what must exist for EX-2 and what does not. | N | Phase 1 gate | read-only; writes only the findings in this folder's `inputs.md` | The written map names each extension point with a file and line, and says "none" where there is none | [ ] |
| EX-2 **Build the one view** (recommended: a text-first cut list; one row per shot or clip with trim, reorder and delete) using only the phase 1 commands, through the SDK or CLI and the pack route EX-1 finds. | X | EX-1 | a new pack or view under the pack convention EX-1 names; no change to editor internals | New tests next to the view: every edit it makes is one named op; a conflict and an undo behave as in the editor, on one of the matrix documents | [ ] |
| EX-3 **Taste pass** on the view's wording and layout. | T | EX-2 | the view's copy and layout only | The owner looks at it once | [ ] |
| EX-4 **Shared-material evidence.** The same document edited in the editor and in the view, edit by edit, ends identical; unsupported contracts found along the way are listed. | N | EX-2 | tests and the findings list | A test that applies one gesture list through both and compares the canonical documents | [ ] |
| R2 Review round for phase 2 (at most 1). | S | EX-1 to EX-4 | read-only | As R | [ ] |

## Start here

For a newcomer picking up TL-1 once Release 14 is published.

**Prerequisites.** Release 14 published (check `releases/14.md` state); Release 14's merged work present on each product repository's `release/14/main` (shot trim, edit-refusals fix, `source_offset` rule, uniform baseline). D4 answered, so you know the release branch `<NN>`. If any is missing, stop and ask the Lead.

**Repositories.**

| Repository | Clone | Branch for this plan | Used for |
| --- | --- | --- | --- |
| astrid-dev | `https://github.com/banodoco/astrid-dev` | `plan/18-command-layer` (this pack); progress PRs change `tasks.md` only | the plan |
| astrid-agent | `https://github.com/banodoco/astrid-agent` | `release/<NN>/plan-18` from `release/<NN>/main` | ops, schema owner, matrix generator, agent surface |
| astrid-runtime | `https://github.com/banodoco/astrid-runtime` | `release/<NN>/plan-18` | commit contract copy, provider, refusal envelope |
| astrid-app | `https://github.com/banodoco/astrid-app` | `release/<NN>/plan-18` | editor handoff, capture encoders, UI |

**Commands** (from each checkout root; call the scripts by their literal paths; see [`env/README.md`](../../env/README.md)):

```text
# Agent
bash scripts/worker-env/agent-setup.sh
bash scripts/worker-env/agent-pytest.sh -q tests/editing_conformance/test_recipe_occurrence_trim.py tests/editing_conformance/test_gesture_matrix.py
# Runtime (Agent pinned in tests/astrid-agent.pin)
bash scripts/worker-env/runtime-setup.sh
bash scripts/worker-env/runtime-pytest.sh -q tests/test_occurrence_trim_commit.py tests/test_timeline_current_union_contract.py
# App: Node 20 is required (Node 26 fakes failures); run one heavy suite at a time
PATH=<node-v20.19.4>/bin:$PATH npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff
# Regenerate the matrix golden (from the Agent checkout)
python scripts/gen_gesture_matrix.py --update
# astrid-dev, before pushing a plan change
python3 scripts/astrid_dev.py check && python3 -m unittest discover -s scripts -p "test_*.py"
```

**To see the template working.** On the App's `task/plan59-shot-trim` (or `release/14/main` once merged), read `hooks/timelineLocalSaveHandoff.ts` lines 339 to 349 and `commands/localSaveSession.ts` lines 234 to 274, then run the `occurrenceTrim` test above. That is the whole pattern.

**D-data.** TL-15b needs a copy of a long-lived timeline from the owner. Ask the Lead; do not take a document from a running install.

## Gestures and their ops

The inventory of the template branch (re-made in TL-1). "New" means TL-3 adds it. Rows are in the order the conversion tasks use.

| # | Gesture | Op | Status | Task |
| --- | --- | --- | --- | --- |
| 1 | Drop a file (image, video, audio) | `clip.add-media` / `occurrence.add-media` / `placement.create` | exists; encoded in the handoff today | TL-10 |
| 2 | Drop an asset from the panel | same | exists | TL-10 |
| 3 | Panel clip drop | `clip.add` | exists, unverified mapping | TL-10 |
| 4 | Move, same track | `clip.move` | exists | TL-6 |
| 5 | Move, across tracks or to a new track | `clip.move` + `track` (D3), `track.create` | new | TL-3b, TL-6 |
| 6 | Trim a clip edge in timeline time | timeline-edge trim (name in TL-1) | new | TL-3b, TL-7 |
| 7 | Trim a shot edge | `occurrence.trim` | built (template) | done in Plan 59 |
| 8 | Split | `clip.split` (+ occurrence children) | exists for parent; new for children | TL-3c, TL-7 |
| 9 | Delete | `clip.delete`, `occurrence.delete`, `placement.unplace` | exists | TL-11 |
| 10 | Inspector scalars | `clip.set`, `clip.set-params`, `text-binding.set` (+ speed, volume) | partial | TL-3d, TL-7 |
| 11 | Element and overlay parameters | `clip.set-element` / `clip.set-params` | exists, mapping unverified | TL-9 |
| 12 | Source In / Out | `clip.trim`; occurrence child slip | partial; slip new | TL-3c, TL-7 |
| 13 | Duplicate (generated clip, shot, clip) | `clip.duplicate-media`, `occurrence.duplicate`, `clip.duplicate` | partial; plain clip new | TL-3d, TL-10, TL-11 |
| 14 | Undo, redo | `timeline.inverse`, `timeline.restore` | exists | TL-11 |
| 15 to 18 | Add, rename, reorder, remove a track | `track.create`, `track.set`, `track.move`, `track.remove` | create and set exist; move and remove new | TL-3a, TL-8 |
| 19, 20 | Clear a transition; keyboard nudge | `clip.set` (clear), `clip.move` | exists | TL-6 |
| 21 | Image onto a shot | `occurrence.add-media` | exists, unverified | TL-10 |

Not found in the editor: paste, copy, cut, ripple. If TL-1 finds a gesture the inventory missed, it gets a row and an op before any conversion starts.

## Critical path and estimates

**Critical path:** TL-1 (2.5 d), RS1 (1), TL-4 (4), TL-5 (2), TL-10 (5), TL-12 (3), R (3) is about 20.5 days; with TL-2, TL-3, TL-15 and TL-16 running beside it, **about 22 elapsed days** for phase 1.

| Group | Tasks | Days |
| --- | --- | --- |
| Contract | TL-1 2.5, RS1 1 | 3.5 |
| Schema and ops | TL-2 2, TL-3a 1, TL-3b 3, TL-3c 2.5, TL-3d 1 | 9.5 |
| Refusal and send-and-adopt | TL-4 4, TL-5 2, TL-14 1 | 7 |
| Suite | TL-15a 4, TL-15b 1.5, TL-16 1 | 6.5 |
| Conversions | TL-6 3, TL-7 4, TL-8 2, TL-9 3, TL-10 5, TL-11 2 | 19 |
| Delete and agent surface | TL-12 3, TL-13a 3, TL-13b 2 | 8 |
| Review | R (two rounds) | 3 |
| **Phase 1** | | **about 56, stated as 55** |
| **Phase 2** | EX-1 1.5, EX-2 5, EX-3 1, EX-4 1.5, R2 1 | about 10 |

Parallelism: after RS1, five strands start together (TL-2 then TL-3; TL-4 then TL-5; TL-15a then TL-15b; TL-13a; none touches another's functions). The six conversions run in parallel after TL-5, each in its own functions of the handoff, with a merge order (TL-6, TL-7, TL-8, TL-9, TL-11, TL-10, because TL-10 deletes the most). The first useful stop is after TL-6: the move class of today's incidents is retired before the rest lands.

## Test inventory

The existing tests this plan affects (from the 18 November inventory of the template branches; fates are likely, not verified line by line, and TL-1 confirms them).

**App** (`src/tools/video-editor/`):

| Test | Fate | Why |
| --- | --- | --- |
| `hooks/timelineLocalSaveHandoff.test.ts` (1,228 lines) | Rewrite the gesture-body assertions (about 24); keep the outbox, replay and refused-gesture tests | the bodies encode `doc.patch` shapes the named ops replace |
| `hooks/timelineLocalSaveHandoff.occurrenceTrim.test.ts` | Keep; its generator pattern becomes the matrix test | already the named-op test over the three corpus documents |
| `hooks/useTimelinePersistence.test.tsx` (3,110) | Rewrite the P2 gesture table (`:296`) and three `doc.patch` cases; add the refusal cases | |
| `hooks/useTimelineSave.test.tsx` (2,299), `useTimelineSave.currentContract.test.tsx` | Keep durability; rewrite the `doc.patch` cases (eight and one) | |
| `hooks/mountedFileDrop.test.tsx`, `useTimelineCommandsService.persistence.test.tsx` | Keep; small command-name rewrites | prepared media already maps to named ops |
| `hooks/useClipResize.test.tsx`, `useClipResizeGesture.test.tsx` | Keep | UI math, not encoding |
| `commands/genericPatchCapture.test.ts`, `commands/commitSession.genericPatch.test.ts` | Delete (TL-12) | they test the `doc.patch` lowering the plan removes |
| `commands/localSaveSession.test.ts` and its `lifecycle`, `ownerRecovery`, `permanentRejection`, `recoveryBasis`, `replayProtocol`, `trackLabelRefusal`, `v2`, `contract` siblings | Keep; rewrite the two `doc.patch` cases | session durability |
| `commands/commitSession.test.ts`, `commitSession.clipScalar`, `.placement`, `.occurrenceDuplicate` | Keep (rewrite one `doc.patch` case); these are the named-op sessions | |
| `commands/ordinary{Move,Scalar,Structural,Trim}Member.test.ts`, `clip{Move,Trim,Scalar}Capture.test.ts`, `trackLabelCapture.test.ts`, `p1RawHandoffCorpus.test.ts`, `p1FeasibilityCorpus.test.ts` | Keep; they pin the encoders TL-5 reuses (rewrite one `doc.patch` assertion in the last) | Agent-golden parity |
| `PropertiesPanel.mounted.test.tsx`, `useTimelineTrackManagement.persistence.test.tsx` | Edit: drop the digest literal (TL-2) | |

**Agent** (`tests/`): keep `editing_conformance/test_recipe_occurrence_trim.py`, `test_occurrence_window_rule.py`, `test_recipe_m1_commands.py`, `test_recipe_m2_clip_trim.py`, `test_recipe_clip_scalar_fields.py`, the duplicate and delete recipes, `test_doc_patch_v2.py`, `test_doc_patch_occurrence_reorder.py`, `test_commit_runtime_occurrence_media.py`, `test_conformance.py` and its 52 scenarios, `sdk/test_timeline_*_provider.py`, `sdk/test_timeline_public_command.py`; rewrite `sdk/test_timeline_current_union_schema.py` (and regenerate `fixtures/current-union-command-schemas/`) when TL-3 adds ops. **Runtime:** keep `test_timeline_commit_provider.py`, `test_occurrence_trim_commit.py`, `test_timeline_commit_contract.py`, `test_timeline_commit_validation.py`, `test_timeline_commit_port.py`; rewrite `test_timeline_current_union_contract.py` when ops change.

**New:** `test_timeline_command_contract.py`, `test_edit_command_schema_matches_agent.py`, `test_recipe_track_ops.py`, `test_recipe_clip_resize.py`, `test_recipe_occurrence_child_split_trim.py`, `test_recipe_clip_duplicate.py`, `test_refusal_envelope.py`, `test_gesture_matrix.py` (Agent); `editResult.test.ts`, `timelineLocalSaveHandoff.structure.test.ts`, `timelineLocalSaveHandoff.matrix.test.ts`, `timelineCommandLayer.endState.test.ts`, `contractMetadata.test.ts` (App).

**What these changes make untrue** (each named test, fixture or oracle line the plan invalidates, and how it may change): the 24-odd gesture-body assertions and the P2 table above (rewritten to assert one named command); the three stale digest literals and `supportsFullV2Commit()`'s constants (deleted for generated ones); the Agent frozen current-union schema snapshot and the Runtime inventory test (extended by TL-3's reviewed additions only); `genericPatchCapture` tests (deleted). Re-check this list against the code at dispatch, because Release 14 moves several of these files.

## End-state checks

| # | Check | Guarded by |
| --- | --- | --- |
| 1 | No expected-diff block remains in the handoff | `hooks/timelineCommandLayer.endState.test.ts` and `timelineLocalSaveHandoff.structure.test.ts` (no gesture branch builds more than one command; line ratchet) |
| 2 | Every gesture is one named op | the exhaustive `GESTURE_OPS` table, checked against the generated schema types |
| 3 | The editor emits no `doc.patch` | the matrix: no command in any case has `op: doc.patch` |
| 4 | Agents and the editor use the same ops | the Agent-generated matrix replayed by the editor; `test_refusal_envelope.py` for the agent side |
| 5 | A refusal cannot reach the user without a code and a headline | `editResult.test.ts`, the ESLint rule, the `{status:'error', reason}` type |
| 6 | One schema owner | `test_edit_command_schema_matches_agent.py`, `check:runtime-lock`, a grep test for digest literals |
| 7 | A generated suite runs in CI through the Agent | `test_gesture_matrix.py` and the matrix manifest floor (12 documents x all gestures x all tracks) |
| 8 | Phase 2: the view uses only commands | EX-4's comparison test |
