# Friction log: release-14-plan-69, timeline 77f906f3242c48179ab86ca7c3e62eb4 ("trial v2"), five edits (A-E)

Status at time of writing: no edit is committed. Head is still the rollback revision
`authoring-parent-revision-7c5aefc4b203b6676e5a13e98236e7d6030b9296ef35ca6c819e349255abaad5`.
One write (edit E) is in flight with outcome unknown (item 12).

## 1. Launcher refuses SDK connection: "An older Astrid is still running"
- Command: `program/versions/5bf20639e293/py/bin/python -I -c` / `Timeline.open(project, timeline)` (wrapper `edits/stackpy.sh`).
- Error (verbatim): `ServiceUnavailableError: An older Astrid is still running. Restart it after its running tasks finish.`
- Expected: connect to the running release-14 runtime.
- Cause (traced): `r/astrid_runtime/identity.py` (IDENTITY_REFUSAL_MESSAGE) compares the live runtime identity `{"release": 13}` (`data/runtime/discovery.json`) with the caller identity built from env `ASTRID_INSTALL_RELEASE` (default `"0"`), `py/.../runtime_protocol/startup_identity.py:30`. My `env -i` wrapper dropped the variable, so the caller claimed release 0.
- Workaround: set `ASTRID_INSTALL_RELEASE=13` (the stack's own value in `state/install-manifest.json` and `state/base-manifest.json`) in `edits/stackpy.sh`. The CLI wrapper `edits/astrid-stack.sh` did not need it for `timelines status`; the SDK path did.

## 2. `packs list --project ...` rejected
- Command: `astrid-stack.sh packs list --project 801a...`
- Error: `unrecognized arguments: --project 801a01b3a87941a1ab25958c488afdbf` (argparse, `astrid.core.pack.cli`).
- Expected: project-scoped pack list. Workaround: `packs list` without a project flag. It does not show the project pack `project_cd4fa4f1666bc788f4a9`.

## 3. Edit A blocked: parent clip delete refused by a declared-dependency guard
- Command: `Timeline.commit(lambda t: t.clip("clip-1").remove(), ...)`
- Error (verbatim): `CommandError: clip.delete cannot prove declared semantic dependencies safe`, details `kind=unsupported_dependency`, `path=['config','app','astrid','slots']`.
- Source: `astrid/sdk/timeline/_delete_commands.py:22` (`_unrelated`) and `_unreferenced` (lines 40-50), which refuse any parent clip removal while the parent config declares `app.astrid.slots`. This timeline declares stand-in slots (`A1-TALK`, `B1-TIMELAPSE`, ...). The guard is timeline-wide and does not check whether the removed clip uses those slots.
- Expected: remove clip-1 (a parent "hold" clip with no relation fields). Workaround: none within the brief. Edit A is skipped.

## 4. Edits B and C blocked: element pack not resolvable by the SDK
- Command: `clip("c02-02-am-discord").set_param("joins[0].name", "VRAMpire")`
- Error (verbatim): `ElementPackNotInstalled [element_pack_not_installed] ar-discord: no installed pack declares this element ... no param was written.`
- Expected: write the param in the clip's element params. The element lives in project pack `project_cd4fa4f1666bc788f4a9` (`data/project-packs/221335d5-.../packs/project_cd4fa4f1666bc788f4a9/rendering/elements/effects/ar-discord/element.yaml`), which `packs list` does not show. `set_param` refuses even though `element_schema` is only one lookup away. Cause inferred from the message; the lookup itself was not traced.
- Workaround: none (installing or admitting the project pack is outside the brief). Edits B and C are skipped.
- Easing check (C), done by reading source, not by rendering: `ar-discord/discord-core.ts:142-160` (`cameraAt`). A step with `ease:'linear'` tweens from the previous step's frame to its own. With the keyframes from the brief (163 no ease, 164 linear, 169, 170 linear, ...), each one-frame segment resolves to the hard value at the step frame (t = 0 at the segment start), so the three punch-ins are hard cuts and the slow coast from 178 to 217 is linear. Confirmed by source only; not verified by a render.

## 5. Edit D: `nudge()` reflows the whole timeline
- Command: `Clip.nudge(-1.0)` on `c23-desloppify-arrow` (`astrid/sdk/timeline/model.py`: `nudge` -> `on()` -> `self._tl.retime()`).
- Result (verbatim pending summary): one pending record (`pc_2bcbaa00d8f3`) with 354 changed clips: 353 `at` values, 7 `hold` values inside the internal timeline and 1 `hold` on the parent (`music-song:b` 188.1667 -> 188.167). Example: `c17-tl-001 at 0.433 -> 0.433333`, `c17-tl-002 at 0.599667 -> 0.6`.
- Expected: only `c23-desloppify-arrow` moves (`at` 14.600333 -> 13.600333, `on` formula `"up" in N12 +0.07s` -> `-0.93s`).
- Action: I did not commit. I dropped my own stale pending record (`pending_drop`, state now `dropped`). Edit D is skipped. Start-only writes via `_set_start` would avoid `retime()`, but that is a private helper and was not used.

## 6. A failed commit leaves a pending record that blocks the next call
- After the dry run in item 5 failed with `CommitRefused: candidate.shots[77f906f3...-e25695edf7b6a913c7e8].internal_timeline.clips['c17-tl-340']: timeline interval must fit the occurrence's half-open bounds`, the record stayed in the outbox. The next dry run failed with `_OutboxChanged: outbox changed during evaluation; nothing was submitted`.
- Pre-existing data note (inferred): shot 04 has `duration_ms: 13666` (ends 42.333), but `c17-tl-340` ends at 42.333333 and `c17-39-am-type` at 42.333667. The validator flags sub-millisecond overhang, which appeared only when the candidate was re-timed.
- Workaround: `tl.pending_list()` then `tl.pending_drop(id, reason=...)`, own records only.

## 7. Edit E: dry run returns CommitOutcomeUnknown; connection wedged
- Command: `Timeline.commit(body, label="E: ...", idempotency_key="r6-edit-E-timelapse-v1", dry_run=True)` (`edits/edit_E.py --dry`). The body removes 242 clips and changes 99 start/hold values.
- Error (verbatim): `CommitOutcomeUnknown No reply could be verified; this edit may or may not have been committed. Call tl.commit() again with no arguments to confirm the saved request; the edit is not re-run blindly.`
- Follow-up 1: `tl.commit()` with no arguments returned `TimelineEditError: in-flight request is immutable; retry its original payload and key`. The message contradicts the one above, which asked for the no-argument call.
- Follow-up 2: replayed the original call with the same key and body. Same `CommitOutcomeUnknown`.
- Follow-up 3: a one-clip dry run (`c23-desloppify-arrow` hold only, key `r6-probe-D-hold`) also returned `CommitOutcomeUnknown`. So every commit to this timeline is refused, not only large ones.
- State: `timelines status` shows `connected_session: {command_count: 1, key: timeline-edit-8e8c71ea6b8d4944abe7059883ead17f, outcome: unknown, status: in_flight}`. The outbox file `data/timeline-outbox/cf5accb76d22c3a67cdcc2d9770c815c80b4ac90144b01a2819e2ccef4444187.json` (4.5 MB) holds this timeline's pending/flight data. Head is unchanged. Reads work.
- Not done: I did not edit the outbox or restart the runtime. Both affect other agents writing to this stack. Needs an owner decision.

## 8. Smaller tooling notes
- `timeout` is not on this macOS shell (`command not found: timeout`).
- zsh glob: `grep -rl ... --include='*.py'` must be quoted; `astrid/*timeline*` with no match aborts the command.
- BSD `sed -i` needs a suffix argument; the one-line `sed -i 's/.../'` failed.
- The skill text points at `~/astrid-local/live-door/.venv/bin/python -m astrid`. I did not use it. All calls used the stack's own interpreter (`program/versions/5bf20639e293/py/bin/python`), per the brief.
- The checkout/publish whole-document route (`scripts/timeline_document.py`) is documented as held for this base. Not used.
- No `--help` was passed through any CLI.
