# Directable Astrid App demonstrations

**Project:** Directable Astrid App demonstrations

**Goal:** A creator or agent writes one data spec, runs one Astrid Video command, and gets a verified ordinary video of the real Astrid App performing scripted chat, actions and timeline edits, ready to cut into any Astrid Video project like the pack's other tools.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 3–4 engineering days (App chat and patch controller 1–1.5, director events 0.5–1, porting the existing launcher into the pack plus the runner engine 1, two examples and pack parity 0.5–1); re-size at review against the actual release base.

**Waiting on:** independent critique of this revision; owner decisions D1–D4 in [inputs](inputs.md#owner-decisions), including permission to copy the internal marketing launcher into the public pack (D3).

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — makes authentic, reusable product demonstrations and tutorial authoring possible using the existing creative application; supports communication and contribution without claiming closure of general portable-component or agent-workspace gaps.

## Outcome and scope

**Draft scope — owner requested the project on 28 November 2026 and asked for this revision the same day. Independent critique and scope greenlight are still pending. This plan authorizes no implementation or release.**

Most of the machinery already exists. App main ships an importable, isolated full-App host (`mountAstridDemo` in `src/app/demo`) with a controller for views, lanes, seek, selection and spotlight. Internal astrid-marketing has a generic launcher over it (`importable/`: serve, smoke and full modes, a network guard, an encoder, and two demos, Lantern Valley and Passing Shapes); its README reports the 728-frame showcase rendered locally with no Runtime requests. What is missing is what makes it an Astrid Video **tool**: the launcher, spec type and examples live outside the pack and pin an old pack commit, the encoder always draws title text, there is no runner engine, and the host cannot show scripted chat or apply timeline edits.

Included:

- **App:** two additions to the existing `DemoController`: render a serializable conversation snapshot with the native chat components, and apply a validated timeline patch through the store's existing `ops.apply`. Nothing else in the host changes; reset stays dispose-and-remount.
- **Pack director:** extend `shared/scene/browser-demo.mjs` with ordered cumulative events (chat messages, typing and streaming, action start/result including failure and overlap, timeline patches) beside the existing beats and views. It stays a pure function of the frame: the director computes the state at frame _t_ and the App only renders it. The spec is JSON validated by a JSON Schema, like the effects' `element.yaml` schemas, and grows from the launcher's existing `DemoDefinition` fields. Fixture data that is easier to generate (such as Lantern Valley's beat and motion lanes) comes from an author script that writes the JSON, as the pack's `*-author.cjs` scripts already do.
- **Pack renderer:** port the marketing launcher into one `render_app_demo` command beside the other renderers in `tests/packs/astrid_video/preview/`. It keeps the launcher's approach (stage a fixed entry page into the pinned App checkout, serve it with the App's own Vite config, guard the network, capture, encode) but reads the pack it lives in rather than a pinned older pack, and leaves title text off unless the spec asks for it. `render_project.py` gains an `app-demo` engine so a project manifest can cut the result next to `agent-at-work`, `living-composition` and the rest, and reuses a capture whose receipt matches.
- **Examples in the pack:** the migrated nine-example Lantern Valley showcase and the small Passing Shapes demo, plus one new short collaboration film (prompt, two overlapping actions with one failure, real timeline edits, playback) written by a second author from the skill and schema alone. The showcase keeps its existing named capture interactions (World Explorer and transcript clicks) and its prototype preview effects; the collaboration film uses neither, so it proves the data-only path.
- **Pack parity:** the catalogue row, skill entry, one parameter reference replacing the two investigation documents, and a version bump, so App Demo is documented and validated the way every other `astrid_video` tool is.

Deferred until a film needs them: gallery reveal and variants, multiple named conversations, cursor, extension-defined typed controls, in-place reset, mobile/touch, live agent or generation, native admitted effect, onboarding refactor. App Demo stays a **footage tool**: it is cut into Astrid as ordinary media and is not placeable as a parameterized effect, because the whole App cannot run inside an element's source closure.

## Existing work and decision

Retain App main's demo host and isolation fix, the pack's browser director and its five passing tests, the marketing launcher's capture design and its `DemoDefinition` shape, and the project runner. Do not rebuild the controller under a new interface name or write a second launcher. Move the launcher and both existing demos into the pack, so that every example and renderer for the tool sits in the pack, as for the other tools. Evidence, the critique of the first draft and the alternatives are in [inputs](inputs.md#planning-evidence).

This is not Plan 24's dockable workspace, Plan 46's agent-control authority, Plan 20's onboarding, Plan 96's marketing organisation or Plan 69's pack admission; it consumes their current contracts without widening them.

## Sequence and readiness

APD-1 (App) and APD-2 (pack) run in parallel against the conversation snapshot and patch contract below. APD-3 joins them in the renderer. APD-4 and APD-5 author the two films against the frozen renderer. APD-6 brings the pack's documentation and validation into line. One final review R. See [tasks](tasks.md).

At run start select a release, refresh App and pack ancestry against unlanded plans touching `src/app/demo`, `AgentChat` or `shared/scene`, and record the base in [inputs](inputs.md#source-identities). Verify local Chromium, ffmpeg and the App's Vite build before dispatch; a sandbox network failure is not a product limitation.

## Interfaces and handoff

**Consumes:** App `mountAstridDemo` and `DemoController` (App main `8c594aa` or the release base), the store's `ops.apply` timeline patch path and `src/sdk/video/timeline/patch.ts` validation, native `AgentChat` presentation, the App's tour Lantern Valley media (`src/tools/video-editor/tour/asset-manifest.json`), pack `browser-demo.mjs` and `render_project.py`.

**Contract APD-1 and APD-2 share** (agree it in the PR description before either merges):

- `DemoController.setChat(snapshot | null)`: `snapshot = {model?, messages:[{id, role, text, attachments?}], actions:[{id, turn, label, status:'pending'|'done'|'failed', detail?}], composer:{text, sending}}`. The App renders it with native components and invents no status.
- `DemoController.applyPatch(id, patch)`: validates, then applies once per id per mount. An id it has already applied is a no-op; a different patch under a used id, or an invalid patch, throws.

**Produces:** a versioned App Demo spec and schema; the pack command and `app-demo` runner engine; an MP4 plus a receipt (spec, App and pack SHAs, asset hashes, frame count, per-frame source-clock and anchor observations, blocked-request log, `nativeExport: false`); two public examples; one reference and the skill. Unsupported cues, assets or patches fail before capture.

## Completion

- From clean public checkouts at pinned commits, `render_app_demo` renders both examples with no App source edits, Runtime or ACP calls, credentials, CI or GPU. The collaboration spec was written by someone other than the renderer's author, using only the skill, schema and assets.
- The showcase is 728 frames at 24 fps with all eleven destinations, and the collaboration film is about 20 seconds; both are inspected as moving footage and at transition midpoints against a native baseline at the same viewport and theme.
- The collaboration film shows typed and sent prompt, streamed reply, two overlapping action cards ending out of order with one truthful failure, real clip placement, trim and replacement visible in timeline state and player, and playback of the result. The player and workspace identity hold for the whole capture.
- Negative cases fail before writing an output: unknown cue, foreign asset, invalid or reused patch id, failure rendered as success, missing anchor, source-clock mismatch, an off-origin or `/api/runtime` request.
- A project manifest using the `app-demo` engine renders end to end, and changing another scene does not re-capture the unchanged demo. Existing homepage, onboarding and director tests stay green against the base.
- `validate_pack.py` passes; the catalogue, skill and reference describe App Demo as a footage tool with an external App dependency. No native export, effect admission or marketing publication is claimed; merge and release stay separately authorized.
