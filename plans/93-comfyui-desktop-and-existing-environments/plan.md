# ComfyUI Desktop and existing environments

**Project:** ComfyUI Desktop and existing environments

**Goal:** A creator or their agent can discover, connect to and safely recover their own supported ComfyUI installation, including Desktop, even when it is stopped or broken, and use the ordinary Astrid generation path.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD — re-estimate after the exact-head discovery and lifecycle inventory; do not assume native Desktop launch is already implemented.

**Waiting on:** Independent scope critique, owner decisions on supported layouts and launch authority, Release 16 start and a consented Windows Desktop test environment; coordinate with Plan 38 before any shared process-identity changes.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) and [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Outcome and scope

A person who already uses ComfyUI should not need to install another copy to use Astrid. First-class Desktop support is an outcome, not a fallback to Portable.

- Discover a running or stopped supported local ComfyUI, including Desktop on Windows, and distinguish no installation, a broken registration or missing paths, a stopped installation, a reachable but incompatible target, and a ready target. Reuse the existing scan and typed target evidence; report unknown or denied observations honestly.
- Identify the layout, endpoint, verified executable/interpreter or launcher, model/workflow locations and ownership when observable. A registered path is not proof it exists; a guessed Python path is not launch authority.
- Give a supported start/repair instruction or, where verified and authorized, invoke the existing safe launch boundary. Desktop and Pinokio retain lifecycle ownership; never kill, replace, restart or bypass their updater without an independently approved operation. Preserve models, workflows and unrelated jobs. Do not silently choose among multiple candidates.
- Hand the reachable selected endpoint to the existing Runtime generation settings and Plan 32 path. Use Plan 56's readiness and named next steps for workflow dependencies; existing digest-bound model preparation remains the same path. Do not add another workflow runner or a second default-placement store.
- A real Windows Desktop installation must generate and deliver a usable image in the matching editor; success on Portable alone cannot qualify Desktop. Portable, manual Git and Pinokio existing-install layouts are regression/compatibility cases; declare the supported matrix and limitations rather than imply all combinations are qualified.

Not included: fresh engine provisioning or a general Windows managed-engine adapter (Plan 94); arbitrary third-party repair/patching; new inference engine; a second environment registry; remote ComfyUI, Wan2GP or changes to paid-machine policy.

## Existing work and decision

Plan 20 phase 4 shipped most of the first-image flow but expressly excluded Desktop discovery and adoption of a stopped server. Its task record still lacks final completion proof. The tested setup and VibeComfy skills say to start the person's ComfyUI manually. Existing `local.py:scan` only finds answering endpoints and bounded Pinokio evidence; `targets.py:TargetRecord` already names Desktop/Portable/Git/Pinokio layouts. `target_launch.py` has verified argv/path and consent boundaries, but the native observer refuses non-Linux platforms. The November 24 [exploratory Windows report #1848](https://github.com/banodoco/astrid-dev/issues/1848) found a registered Desktop 0.7.2 whose recorded executable and data directory were missing; scan returned no servers and no errors. Portable succeeded only after separate provisioning. A missing listener is not equivalent to no installation, and an empty error list must not erase stale registration evidence.

Reuse and extend those boundaries; see exact sources, alternatives and outstanding critique in [inputs.md](inputs.md#planning-evidence). The owner requested Desktop support and Release 16 inclusion; the two-project split is the planner's proposed boundary, not an accepted implementation design.

## Sequence and readiness

Reconcile Plan 20's shipped record and inspect the current Agent/Runtime/Pinokio ownership boundaries; map real Desktop discovery and supported lifecycle actions before specifying writes. First deliver read-only discovery plus supported manual recovery, then implement a native verified launch only if it is needed and approved. Use a real installed Windows test and a matching editor. Coordinate overlapping functions/contracts with Plans 38, 56 and 94; land or stack in the order established by the release manager. [Tasks](tasks.md) are draft until the critique, exact bases, test inventory and run authority are settled.

## Interfaces and handoff

Consumes Plan 20's setup skill and Plan 32's placement/generation, the existing target record and discovery/launch primitives, Plan 56's landed workflow readiness contract when available, and Plan 38's native process-identity output where needed. Pin exact landed commits at dispatch.

Produces a verified or explicitly blocked existing-target selection with an actionable next step and ownership facts, usable by Plan 94 and the existing setup skill without a parallel registry. Supply the exact installed tuple, positive/negative witnesses and integrated PR links. A found installation is not a ready target; a ready target is not proof of inference.

## Completion

On the declared Windows Desktop version/GPU, prove running Desktop is discovered and reused, stopped Desktop is discovered and brought up through the supported route, stale/broken registration is diagnosed without deleting data, and a real Desktop image appears in the matching editor. Exercise multiple installations, changed port, denied loopback access, missing paths, refused consent and an unrelated queued job; no unapproved changes or duplicate process. Regression-check existing running Portable/Git/Pinokio as available and explicitly mark unqualified cases. Run focused CPU negative tests and the real GPU witness through Plan 34's protocol. Reconcile Plan 20's completion evidence without marking its whole outcome complete by assumption. No implementation, hardware use, spending or publication is authorized by this draft.
