# Directable Astrid App demonstrations

**Project:** Directable Astrid App demonstrations

**Goal:** A creator or agent writes one data spec, runs one Astrid Video command, and gets a verified video of the real Astrid App that moves the way the App moves, performing scripted chat, actions and timeline edits, ready to cut into any Astrid Video edit.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 4.5–6 engineering days (App seams 0.5–1, stepped clock and playback 1–1.5, shared-model imports 0.5, director grammar and events 1–1.5, output and runner integration 0.5–1, examples, tests and docs 1); re-size at review against the actual release base.

**Waiting on:** independent critique of this revision; owner decisions D2–D6 in [inputs](inputs.md#owner-decisions).

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — makes authentic, reusable product demonstrations and tutorial authoring possible using the existing creative application; supports communication and contribution without claiming closure of general portable-component or agent-workspace gaps.

## Outcome and scope

**Draft scope — the owner requested the project on 28 November 2026 and directed that video demo features are built in Astrid Video. Independent critique and scope greenlight are still pending. This plan authorizes no implementation or release.**

### End state

1. **Input.** A demo spec names a **workspace** (an inline fixture timeline, or an exported `.astrid` archive) and a **script**: timed poses (layout, visible panels and lanes), transitions, accents on real interface anchors, chat (typed prompt, streamed reply, overlapping actions that finish, fail or wait), timeline edits with a duration, and playback.
2. **Command.** `astrid_video/shared/browser-demo/local.sh APP OUTPUT smoke|full --demo ID` (or `--timeline FILE`) against a pinned App checkout. No Runtime, credentials, CI or GPU.
3. **Output.** A silent MP4 at the spec's frame rate, size and pixel density, with no title text unless the spec asks for it in the pack's own type and palette; a storyboard contact sheet and timing summary like the other pack demos; a receipt in the pack's receipt format.
4. **Feel.** The App's own animations run, stepped frame by frame on a controlled clock, so every run is identical. Typing and streaming follow a seeded human rhythm; edits glide; the player really plays across several clips. No cursor; the spotlight is one optional accent.
5. **Use.** The MP4 is an `app-demo` engine row in a `render_project.py` manifest, cut beside Agent at Work, Timeline Assembly or a Chapter Card, and reused when its spec is unchanged.

### Ownership

- **Astrid Video (`poms_packs/astrid_video`) owns every video demo feature:** spec and schema, director, chat rendering, timing and pacing, stepped clock, capture, encoding, storyboard, receipt, runner engine, public examples, tests and docs. The launcher already lives at `shared/browser-demo/` ([inputs](inputs.md#planning-evidence)).
- **Astrid App** adds only what cannot be done from outside the mounted App: applying a validated timeline patch through its store, real play and pause, and a browser-only archive reader split from its existing importer.
- **Astrid Marketing** keeps its films and fixtures (Lantern Valley, Passing Shapes) and runs them through the pack launcher via `ASTRID_DEMO_FIXTURES`. No tooling.

### Shared with the pack's other tools

- **Timing grammar:** the spec uses Living Composition's terms (poses with `at` in seconds, `transition.duration`, `name`, and `accents` with `at`, `target`, `effect` and `duration`), with an adapter so existing `views`/`beats` definitions still compile.
- **Timeline model:** clip move, trim and replace use `shared/timeline/model.ts`, extended from one revision to an ordered list; Timeline Assembly gains the same.
- **Activity model:** chat actions use Agent at Work's event clock (`compileActivity`/`activityFrame`) plus a new conversation and pacing layer that Agent at Work can opt into.
- **Encoding and receipts:** one encode helper and one receipt format for the pack's renderers, including this one.
- **Media identity:** media named by SHA-256 binding in both App Demo workspaces and effect specs.

Deferred: cursor; gallery and multiple named conversations; mobile layout; live agent or generation; a native admitted effect; cuts that hand objects between illustrated and real scenes, and pixel or mink overlays aimed at recorded anchors (a follow-up plan).

## Existing work and decision

Retain App main's demo host and isolation fix; the pack's launcher, director and archive importer as committed in `5134312`; the App's transport-free `ConversationPresentation`; and the pack's timeline, activity, composition and runner code. Extend these; do not add a second launcher, director, chat renderer or receipt. Evidence, the critique of earlier drafts and alternatives are in [inputs](inputs.md#planning-evidence).

This is not Plan 24's dockable workspace, Plan 46's agent-control authority, Plan 20's onboarding, Plan 96's marketing organisation or Plan 69's pack admission.

## Sequence and readiness

APD-1 (App seams), APD-2 (stepped clock and playback) and APD-3 (shared-model imports) start in parallel. APD-4 (director grammar and events) needs all three. APD-5 (output and runner) follows. APD-6 (public example and tests) and APD-7 (collaboration film) prove it. APD-8 (docs) runs alongside. One final review R. APD-2 begins with a half-day check that the Remotion player and the Three.js preview frame behave under a paused clock; if the player does not, it falls back to the current seek-per-frame playback and reports which feel goals that loses. See [tasks](tasks.md).

At run start select a release, compare unlanded plans touching `src/app/demo`, `timeline-transfer.ts`, `astrid_video/shared` or `render_project.py`, and record the bases in [inputs](inputs.md#source-identities). Verify Chromium, ffmpeg and the App's Vite build first.

## Interfaces and handoff

**Consumes:** App `mountAstridDemo` (`src/app/demo`, App main `8c594aa` or the release base); `ConversationPresentation` and its contracts (`src/shared/components/conversation`); the App's timeline patch contract (`src/sdk/video/timeline/patch.ts`) and `ops.apply`; the App's `astrid.timeline/1` reader (`timeline-transfer.ts`, `timeline-transfer-zip.ts`); pack `shared/browser-demo/`, `shared/scene/browser-demo.mjs`, `shared/timeline/model.ts`, `shared/activity/model.ts`, `shared/composition/`, `render_project.py`.

**App seams (APD-1):** `DemoController.applyPatch(id, patch)` validates, applies once per id per mount, treats a repeat of the same patch as a no-op, and throws on a conflicting or invalid patch; `DemoController.play()`/`pause()` drive the real player transport; `readTimelineArchive(blob)` returns the verified timeline, media and transcripts without Runtime. Chat needs no App change: the pack passes a `ConversationPresentation` built from its snapshot through the existing `chat` prop.

**Produces:** the demo spec and JSON Schema; the extended director; the stepped-clock capture; the `app-demo` runner engine; MP4, storyboard, timing summary and receipt (spec, App and pack commits, asset hashes, frame count, per-frame clock and anchor observations, blocked requests, `nativeExport: false`); one public example and negative fixtures; the extended timeline and activity models; one reference and the skill. Unsupported cues, assets or patches fail before capture.

## Completion

- From clean public checkouts at pinned commits, the pack command renders the public example and the collaboration film with no App source edits, Runtime or ACP calls, credentials, CI or GPU. Someone other than the director's author writes the collaboration film from the skill, reference and schema alone.
- The collaboration film (about 20 s) shows a typed and sent prompt, a streamed reply, two overlapping actions ending out of order with one truthful failure, clips gliding to new positions and trims, a replacement, and real playback across at least two clips with the transport showing play.
- Two full renders of each film are byte-identical frame by frame. Watched beside a person's screen recording of the same steps in the real App, nothing snaps that the App animates.
- Negative fixtures fail with no MP4: unknown cue, foreign asset, invalid or conflicting patch, a failure shown as success, missing anchor, clock mismatch, an off-origin or `/api/` request.
- Marketing's Lantern Valley (728 frames) and Passing Shapes still render through the pack launcher. A manifest with an `app-demo` row and an `agent-at-work` row renders, and editing only the latter reuses the capture.
- Timeline Assembly renders a two-revision example, and Agent at Work renders with the new pacing opt-in; their existing examples are unchanged.
- `python tests/packs/astrid_video/run_local.py` passes with the new tests included. The catalogue, skill and reference describe App Demo as a footage tool with an App checkout dependency. No native export, effect admission or publication is claimed; merge and release stay separately authorized.
