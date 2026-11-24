# FRICTION: r6 hair beat (c28-seq0-00..05), release-14 stack

Stack: `~/astrid-release/release-14-plan-69`, program version `5bf20639e293`, door 17501.
Project `801a01b3a87941a1ab25958c488afdbf`, timeline `77f906f3242c48179ab86ca7c3e62eb4`.
Source paths below are relative to `program/versions/5bf20639e293/py/lib/python3.11/site-packages/astrid/`.
`astrid-stack.sh` = `r6/astrid-stack.sh` (env of start-2400.sh + `program/run-astrid`). `stackpy.sh` = `r6/hair/stackpy.sh` (same env, stack python, for SDK scripts).

Outcome: stills generated and imported; the timeline swap is BLOCKED. None of my calls changed the timeline.
Head when I started: `authoring-parent-revision-7c5aefc4…abaad5` (`txn-1389030768d44b5e889ff010f5ec4673`).
Head when I stopped: `authoring-parent-revision-606c2a92…2f19` (`txn-7fcb8d530cea424da3843edcabe05bdb`), moved by two other
agents' publications at 14:26 and 14:32 UTC ("Type colour sweep on c34 adapt/foundation", "Publish document"). c28-seq0-00..05 still point at RW3-00..04.
Every write route was refused or unsafe (items 3–7b).

Root cause in one line: the RW3 registry entries are legacy (no generation/variant pin, `content_sha256`/`source` fields) and the c28 clips are word-anchored inside an occurrence; each write route rejects one of those two facts.

## Blocking

### 3. Asset swap on a word-anchored occurrence clip is refused (CLI expected-head route)
Command:
```
astrid-stack.sh timelines replace-parent-media 77f906f3242c48179ab86ca7c3e62eb4 --project 801a01b3a87941a1ab25958c488afdbf \
  --occurrence-id occ-77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66-occ --clip-id c28-seq0-00 \
  --source-object-id sha256:ed76f7c48bd8ff3ec646dd88e3d1c56225e99b20ddf5431ea12bf0ab2d62e852 \
  --expected-head authoring-parent-revision-7c5aefc4b203b6676e5a13e98236e7d6030b9296ef35ca6c819e349255abaad5 \
  --idempotency-key r6-rw-hair-rpm-00 --json
```
Error (exit 1, verbatim): `"code":"validation_error" … "reason":"invalid_document","status":"invalid","suggested_command":"timeline edit"},"message":"candidate.timing: missing exact word binding for ('occ-77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66-occ', '77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66', 'c28-seq0-00').on"`
Expected: an asset-only swap does not touch timing; the clip's unchanged `app.astrid.on = "\"All\" in N17 -0.08s"` should be exempt as a pre-existing legacy declaration.
Source: raise at `sdk/timeline/_timing_evaluators.py:422` (`moment_rule`: word moment with no captured pin). Bindings are only built for parent clips (`sdk/timeline/_commit_timing_validation.py:840-866`; occurrence clips with `word_anchors` raise "word anchors require parent ownership"). The intended escape is `_legacy_exemptions` (`_commit_timing_validation.py:402-416`, "unchanged declarations the base already failed to resolve"), but a clip whose row changed (asset only) is not treated as unchanged. Not traced further (inferred: the failure signature includes the clip row).
Same refusal from the SDK with a pure patch (no new media): `tl.commit(lambda t: t.clip("c28-seq0-00").swap_asset("RW3-01"), dry_run=True)` → `CommitRefused: This edit is not valid; nothing was committed. candidate.timing: missing exact word binding for (…'c28-seq0-00').on`.
Workaround: none found.

### 4. SDK function commit with newly imported media on an occurrence clip: `capture_mismatch`
Script `r6/hair/swap.py` (`Timeline.open(P,T).commit(fn, dry_run=True)`, fn = `clip.swap_asset("<local png>")` for the six clips; also with a registry-only repoint in `t3.py`).
Error (verbatim): `WorkspaceClientError: semantic step assertion differs from execution` → `CommitRefused: The edit no longer matches the timeline it was made from; nothing was committed. The commands were captured from a different copy of the timeline.` Details: `"code":"capture_mismatch","hint":"Recreate the edit from the current timeline"`; base == current head, `conflicts: []`.
Expected: the captured commands were exactly 11 changes (6 clip `asset` sets + 5 registry adds) plus one `media.admit`; the head had not moved. The message blames a stale copy, which is false.
Source: `sdk/timeline/_commit_patch.py:604-606`. When a step holds `doc.patch` + `media.admit`, the step's `patch` claims are compared with `effect_diff(before, after)`; the pure-`doc.patch` branch at :592-603 rebuilds effects from the bindings instead and passes. Inferred, not proven: for an occurrence child the after-closure is keyed by a new `internal-revision:` ref, so field-level claims on the old ref are never found.
Workaround: none. `media.admit` alone is refused too: `CommitConflict: The timeline changed since this list was made; nothing was committed. admitted media is not referenced by the candidate.` (also mis-worded: nothing had changed).

### 5. Mapping / handle asset entries are refused without Runtime-verified media
`clip.swap_asset({"key": "R6-RW-00", "media_id": "sha256:…", …})` (media already imported with `media import`) and `t.replace_asset("RW3-00", "sha256:ed76…")` both fail in `tl.commit`:
`astrid.sdk.timeline._command_state.CommandError: patch references media outside Runtime-verified inputs` (`sdk/timeline/_doc_patch.py:356`).
Expected: media imported through `media import` (or named by `sha256:` handle, as `Clip.swap_asset`'s docstring and `--swap-asset KEY=HANDLE` promise) is usable; or the error says how to verify it.
Only a local file path goes through `Timeline._register_asset` (`sdk/timeline/commit_session.py:255-306`), which verifies, but then names the key after the variant id (`initial-3243…`), so a readable key (`R6-RW-00`) needs a private registry rename. `replace_asset` with a local path: `TimelineEditError: replacement media must be a project media handle (run:…, task:…, ref:…, sha256:…)`, and with the handle it is refused as above: the two rules exclude each other.

### 6. Working-copy route (`timelines checkout` / `edit --swap-asset` / publish) would restructure the film
```
astrid-stack.sh timelines checkout <T> --project <P> --draft r6-hair --fresh
astrid-stack.sh timelines edit <T> --project <P> --draft r6-hair --clip c28-seq0-00 --swap-asset R6-RW-00=sha256:ed76…
```
The edit printed unrequested changes: `✎ c34.adapt-1  146.967–155.667 → 145.233–158.300 s` (and adapt-2, found-1..4). `timelines diff --draft r6-hair --all` then reported `1216 clip changes (612 added, 604 removed) in 7 shot(s) … 7 placement changes`, six placements `removed` (seven shots flattened into one).
Expected: a one-clip asset swap shows a one-clip diff. Every later `edit` also printed the address as `c28.rw-00` for all six steps (the layer name is shared by the whole sequence), so the output cannot confirm which step was edited.
Action: not published; `timelines discard <T> --project <P> --draft r6-hair` (verified: head unchanged, working copy absent).

### 7. Native swap route unusable for these clips
`replace_parent_media(..., old_media=, media=, expected_publication=)` → `sdk/timeline_media_replacement.py:47-65` `_target_pin` needs `generationId`/`variantId` on the clip's current registry entry. `RW3-0N` entries have only `media_id/content_sha256/handle/filename/resolution/source/type`. `sdk/timeline/native_occurrence_media_commands.py:146-149` also refuses any old entry carrying `content_sha256` or `source` ("unsupported old registry identity codec"), and :143 compares `type` with the kind `image` while the entry says `image/png`. Read from source for the direct call; observed through the document route below.

### 7b. Document route (`packs/rendering/docs/scripts/timeline_document.py checkout / check / publish`)
Run as `stackmod.sh astrid.packs.rendering.docs.scripts.timeline_document …` on a checkout at head `…606c2a92…`. `check` passed both times (valid, 1 shot changed, 6 reused, exact 11-line or 24-line diff). `publish` failed both times:
- New keys `R6-RW-00..04` with `local_path` + six clip `asset` changes (`doc/edit.json`): `astrid.sdk.timeline._command_state.CommandError: patch references media outside Runtime-verified inputs`. The script only verifies same-alias rebinds (`resolve_media_rebinds`, script lines 39-76), so media under a new key is never verified. This contradicts references/document-checkout.md ("For a new clip, create a registry entry with `local_path` and select that asset key").
- With verification added for the new keys (`pub3.py`, monkeypatch): the Runtime itself answers `WorkspaceClientError: patch references media outside Runtime-verified inputs`, reported as `CommitConflict: The timeline changed since this list was made … Someone else changed this timeline` (untrue). A `media.admit` command would be needed, which is item 4.
- Same keys, `local_path` added to `RW3-00..03` (`doc/edit2.json`, the documented recipe, clips untouched): `RuntimeError: occurrence:occ-77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66-occ/asset:RW3-00 lacks an exact generation/variant pin; re-check out the document before publishing`. A fresh checkout cannot add the pin; the advice is a dead end for legacy entries.
`check` saying valid while `publish` cannot succeed is the core complaint: the local check does not cover media verification.

## Hazards

### 8. All SDK sessions share one outbox per timeline
A sibling agent's in-flight dry run (`E: time-lapse re-slot…`, key `timeline-edit-8e8c71ea…`) sat in `data/timeline-outbox/cf5accb7….json`. My unrelated dry run then failed with
`CommitOutcomeUnknown: No reply could be verified; this edit may or may not have been committed. Call tl.commit() again with no arguments to confirm the saved request; the edit is not re-run blindly.`
Following that advice would have confirmed the other agent's request. `timelines status` showed their flight as my "connected_session … outcome unknown".
Workaround: `Timeline.open(P, T, outbox_path="<private file>")`.

### 9. `dry_run=True` leaves pending records
Each refused dry run saved a `pc_…` pending edit in the shared list (`tl.pending_list(actors="all")` showed mine beside the sibling's). Dropped mine with `tl.pending_drop(id, reason=…)`: pc_08749567edce, pc_d2c376ccf8a6, pc_a0456bf8cdd5, pc_a3c2f79ab1cb, pc_4c2b47bc348c (last three were in private outboxes).

### 10. `Timeline.open` reports a stale head
After the head moved to `…606c2a92…`, `Timeline.open(P, T).head` (default shared outbox, another agent's flight still held) kept printing `…7c5aefc4…`, while `timelines status` and `timelines history` showed the new head. With a private outbox, function commits then failed with `KeyError: '_runtime_document'` (twice, `t5.py`; not traced).

## Minor

1. Skill text points at another install. The `astrid` / `astrid-rendering` skills hard-code `~/Developer/astrid-video/astrid-local/live-door/.venv/bin/python -m astrid` and describe `timelines checkout/edit/publish`; the stack's own skill (`packs/timeline/docs/SKILL.md`) teaches `Timeline.open(...).commit(fn)`. The two routes behave differently on this timeline (items 4 and 6).
2. `tl.head` is a dict attribute, not a method (`TypeError: 'dict' object is not callable`); sibling scripts guard for both.
3. `media import <dir>` output has no generation/variant ids and no asset key, so its result cannot be fed to any timeline verb (item 5). For bytes that already exist (R6-RW-04 == RW3-04) it returns the old `created_at` and `"stored_filename":"RW3-04.png"`.
4. No route shows a composed frame: `visualize` composed fails for the whole timeline (probe/REPORT.md, issue #1238), so verification would have been Playwright on :2400.
5. No notes on how RW3 was made exist in `~/Developer/astrid-video` or older scratchpads (searched for "RW3").
6. Codex: default model in `~/.codex/config.toml` is `gpt-6.1-terra`; `-m gpt-6-astra` must be passed. The JSONL stream carries no model field; confirmed from `~/.codex/sessions/…/rollout-*.jsonl` (`"model":"gpt-6-astra"`). Output was 1672×941, not 1920×1080: upscaled, registered (ORB + affine) and composited.
