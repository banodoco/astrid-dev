# Tool friction: type colour sweep (c34), release-14-plan-69 stack, 22 Nov

Stack CLI = `r6/astrid-stack.sh` (run-astrid + start-2400.sh env). SP = `program/versions/5bf20639e293/py/lib/python3.11/site-packages/astrid`.

## 1. `timelines elements` needs `--realm`, and nothing says where to get it
- Command: `astrid-stack.sh timelines elements --project 801a01b3… 77f906f3… --json`
- Error (verbatim): `{"code":"unavailable","message":"Pass --realm or configure ASTRID_WORKSPACE_DISCOVERY"}`
- Expected: the CLI is already authenticated to one Runtime; it should use that realm (the SDK checks `_connection(client)['realm_id']` anyway).
- Source: `SP/core/element/project_packs.py:843-848` (`configured_realm`).
- Workaround: read the realm id from the pack folder path (`data/project-packs/<realm>/<project>/…`).

## 2. `timelines elements` lists no elements for this timeline (`elements: []`)
- The timeline has 7 project-pack clips (ar-footage ×6, ar-discord ×1), all inside shots.
- Cause: it walks only `bundle['parent']['clips']` (`SP/core/element/project_packs.py:855-857`).
- Expected: clips inside occurrences are listed with their `occurrence:<id>/clip:<id>` target.
- Workaround: read `elementRef` from `timelines show --json` dumps.

## 3. `update-element` cannot reach a clip inside a shot, and `place-element` cannot set params
- `update-element --clip-id` resolves only parent clips: `_clip()` raises `Expected one existing parent effect clip` (`SP/sdk/timeline_elements.py:161-168`; target hard-coded `parent/clip:` in `_calls`, line 30). Not run against the timeline; read from source.
- `place-element --target occurrence:<occ>/clip:<id>` reaches the clip but takes no `--params-json`.
- The authoring reference (`generated-elements-authoring.md`) documents only `update-element`; `place-element` is not mentioned.
- Expected: one command that takes a clip target, an admitted ref and params (a film's clips are nearly all inside shots).
- Workaround: `r6/sweep/apply_sweep.py`, which sends the same native ops (`clip.set-element` + `clip.set-params`, with the admission pin as `schema_source`) through `TimelineSession.submit` in one expected-head commit. It imports the private `_admitted_element_inputs`.

## 4. The shared outbox would have made my command replay another agent's commit
- `timelines status` showed `connected_session: {status: in_flight, outcome: unknown, key: timeline-edit-8e8c71ea…}`: another agent's 2 MB commit on the c17 time-lapse clips, held in `data/timeline-outbox/cf5accb7….json` since 15:19 (still held at 15:30).
- `place-element` / `update-element` call `_settle_held_flight(session)` first (`SP/sdk/timeline_elements.py:146-158`), which resends that flight under its own key. All agents here share one actor, so they share one outbox.
- Expected: a command either refuses with "another edit is in flight (key …)" or uses a per-process outbox; `--outbox` is not a CLI option.
- Workaround: `TimelineSession.open(..., outbox_path=<my own file>)` (private outbox: `r6/sweep/outbox/sweep-outbox.json`). The other flight was left untouched; its base (7c5aefc4) is now behind the head.

## 5. `project-pack` CLI is not reachable through `run-astrid`, and its default root is wrong for this stack
- `run-astrid` only routes to `astrid.omp_agent`; the reference says `python -m astrid.core.element.cli project-pack admit`. Running that module with the stack python needs the env from `version.json` by hand (`r6/sweep/stack-py.sh`).
- First admit failed (verbatim): `ValueError: Project pack is not created. Run: python3 -m astrid.core.element.cli project-pack init --realm 221335d5-… --project 801a01b3…`
- Cause: the pack lives in `data/project-packs`, but `authoring_root()` defaults to `$XDG_DATA_HOME/astrid/project-packs` (`project_packs.py:55-56`) and no file in the stack sets `ASTRID_PROJECT_PACKS_ROOT`. Following the printed advice (`init`) would have created a second, empty pack.
- Expected: the root derives from `ASTRID_RUNTIME_DATA_ROOT` (which `version.json` sets), or the error names the folder it looked in.
- Workaround: `ASTRID_PROJECT_PACKS_ROOT=<stack>/data/project-packs`.

## 6. `pack validate` passes what `admit` rejects
- `astrid.core.pack.cli validate <pack-root> --json` → `"valid": true, "errors": []`.
- `project-pack admit` right after (verbatim): `astrid.core.element.schema.ElementValidationError: effects/ar-type-sweep: description is 520 chars; max is 500` (as a Python traceback, exit 1).
- Expected: validate runs the element descriptor checks; admit prints one line, not a traceback.
- Source: `SP/core/contracts/capability_schema.py:163`.

## 7. `timelines history --json` has no `head` field
- The SDK's `owner.history(...).data['head']['revision_id']` exists, but the CLI prints `{complete, reason, revisions}`. A script that wants the head must use `status --json` (`current_head`) or `elements --json` (`expectedHead`).

## 8. Editor preview: project pack load times out under load
- With load average ~27, the :2400 editor showed "Preview pack could not be loaded. Preview pack loading timed out. Check the local connection and inspect/admit the project pack, then reload the editor." and every ar-footage layer drew "Element ar-footage@sha256:51b4150c… requires its exact admitted pack revision. Embedded source is preserved for migration and is not executed."
- `/api/runtime/packs/inventory` and `/project-elements` took 24–30 s on that load; 0.1–0.9 s a minute later. A reload fixed it. Cause is machine load (inferred), not the new admission.
- Expected: a longer or retried pack fetch; the per-clip message blames the revision when the real fault is a timeout.

## 9. Seeing frames
- Composed `timelines visualize` was not retried (astrid-dev #1238 open at start).
- Ruler seeking stops at ~35 s. What works: the Remotion Player handle is reachable from the page's React fibres (`seekTo(frame)`, `getCurrentFrame()`), which gives frame-exact stills anywhere in the film in ~2 s each (`r6/sweep/pw_lib.cjs`, `pw_cap.cjs`). The editor has no "go to time" box or URL `?t=`; either would remove this hack.
- The editor's own chips (timeline name, timecode, Render, play button) sit on top of the preview in screenshots.
