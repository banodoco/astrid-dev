# Freeze-frame beat (c07, 10.53–16.33 s): Astrid tooling friction, release-14-plan-69 stack

SP = `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/py/lib/python3.11/site-packages/astrid`

## 1. Detached-document publish cannot introduce new media, although its reference says it can
- Command: `edits/stackpy.sh -m astrid.packs.rendering.docs.scripts.timeline_document` commit path (my guarded copy `freeze/publish_guarded.py doc/edit1.json r6-freeze-v1 --commit`), document = 3 new registry entries with `local_path` (as `references/document-checkout.md` "Add or replace local media" documents), 7 new shot clips, 5 field sets. `check` said `valid: true` and planned the 3 imports.
- Error 1 (local, verbatim): `astrid.sdk.timeline._command_state.CommandError: patch references media outside Runtime-verified inputs` (`SP/sdk/timeline/_doc_patch.py:356 verify_media`). Cause: the script passes `verified_media` only for same-alias rebinds (`resolve_media_rebinds`); media it has just imported itself for NEW aliases is never verified.
- After adding the verified rows by hand (`get_project_media_selection` + `get_project_verified_media` for each import) the local check passes and the Runtime refuses, verbatim: `astrid.sdk.timeline.sync.CommitConflict: The timeline changed since this list was made; nothing was committed. patch references media outside Runtime-verified inputs. Someone else changed this timeline after your edit was made, so "R6 freeze-frame label gag on c07 (ding, dong, dong)" was not committed. Your edit is saved as pc_8928d6bc1e34; nothing is lost. Retry it with tl.retry("pc_8928d6bc1e34").`
- Two faults: (a) a `doc.patch` can never bring in media, so the documented local_path route is dead for new assets; (b) the refusal is worded as a head conflict ("Someone else changed this timeline") when the head had not moved; retrying as advised would refuse for ever.
- Expected: the document route admits the media it imported (emit `media.admit` or equivalent), or `check` says "new media needs a native media add".
- Workaround: two commits. First a native flat `Timeline.add(file, at=, hold=, track=, id=)` (parent-scope clips) to get the media into the timeline's dependency manifest; then a `doc.patch` may reference those media ids from a shot registry (`verify_media` allows manifest media).

## 2. Any field change on a word-anchored shot clip is refused, including its asset
- Command: `freeze/publish_guarded.py doc/edit2.json r6-freeze-c2-v1 --commit` (doc.patch: `clips/id:c07-00-pipeline/asset`, `params.in`; `r4-sfx-slick-clip` `to`/`hold`/`params.fadeOut`; 4 `list.insert`).
- Error (verbatim): `astrid.sdk.workspace_client.WorkspaceClientError: candidate.timing: missing exact word binding for ('occ-77f906f3242c48179ab86ca7c3e62eb4-4dc61841478d1d6322b4-occ', '77f906f3242c48179ab86ca7c3e62eb4-4dc61841478d1d6322b4', 'c07-00-pipeline').on`
- Expected: swapping the asset (or a param) of a clip whose `on` moment and timing I did not change is accepted; the existing binding is as valid as before. Same defect as `edits/DEFECTS.md` #10, but here it blocks a non-timing edit.
- Source: `SP/sdk/timeline/_timing_evaluators.py:413-425`; shot-binding gap noted in `_commit_timing_validation.py:126-133`.
- Workaround: leave c07-00-pipeline and r4-sfx-slick-clip untouched and cover/replace them with new un-anchored clips.

## 3. A parent plain-media video clip draws UNDER the shot it overlaps, and nothing says so
- After `Timeline.add(<mp4>, at=10.5333, hold=5.8, track="plate", id="r6-freeze-plate")` (parent scope, the only scope the flat add offers) the editor shows the shot's own plate on top; the new clip is invisible (frames/probe1). Expected: a way to add media into a shot, or a stated parent/shot stacking rule. `Timeline.add` refuses any option but at/hold/track/id (`SP/sdk/timeline/commit_session.py:343`).

## 4. `Clip.remove()` on a parent clip I added one commit earlier is refused
- `t.clip("r6-freeze-plate").remove()` inside `tl.commit(fn, dry_run=True)`: `CommandError: clip.delete cannot prove declared semantic dependencies safe` (DEFECTS.md #4; the clip is a plain un-referenced media clip).

## 5. `tl.commit(fn)` that adds a shot registry entry for media ALREADY in the timeline's manifest is refused as a stale edit
- fn = remove one shot clip, append 6 shot clips, add `registry.assets["PIPELINE-R3-FREEZE"]` (media already admitted by the previous commit). The SDK appends its own `media.admit` and the Runtime answers (verbatim): `CommitRefused The edit no longer matches the timeline it was made from; nothing was committed. The commands were captured from a different copy of the timeline. Inspect the saved edit with tl.pending_show("pc_ec6ad0d79f2e"), fix the edit, then retry or drop it.` detail `"message": "semantic step assertion differs from execution", "code": "capture_mismatch"`, with base == current head in the same payload. Same as sfx/FRICTION.md #12. The message is untrue (nothing changed underneath) and gives no path (`"path": []`).
- Workaround: the same inserts through the detached-document emitter (no `media.admit` step), removal in a separate commit.

## 6. Small things
- `Timeline.add(wav, hold=1.15)` for a 1.149979 s file: `CommandError source window differs from hold or exceeds media` with no numbers and no clip named (4 adds in the function). Expected: "r6-freeze-dong-1: hold 1.150 s exceeds the 1.150 s file by 0.00002 s", or clamp within half a frame.
- An accepted `tl.commit(fn, dry_run=True)` that only removes a clip still dies with `KeyError: '_runtime_document'` (sfx/FRICTION.md #13); I read that crash as "accepted".
- Removing a parent clip leaves its registry entry behind (`parent.registry.assets["media-b6edddd6…"]`, the freeze video's first, parent-scope alias): no tool prunes an unreferenced asset key, and `clip.delete` (the tool that would) refuses (item 4).
- New shot clips cannot carry a word anchor (`on`) that validates (DEFECTS.md #10), so the freeze plate, labels, bells and slick pieces are fixed-time clips: they will not follow if the narration is ever re-timed.
- am-callout has no way to force a line break; I used non-breaking spaces in the title to choose the break.
- Seeing the beat: 78 frame captures through the editor took > 2 minutes (~2 s per seek); there is still no composed-frame route on this stack.
