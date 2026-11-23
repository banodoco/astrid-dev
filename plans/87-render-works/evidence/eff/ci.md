# CI/render fact-finding

Branches inspected: Agent `8807f820eb47d6018db723511e024a0a123fbe95`; App `e3dbad64d402724ac5a35fb6447f18e432c64b78`; Runtime `23310dc828765293a2ab39f637f28b948e780d94` (`origin/release/15/main`).

## Agent workflows

Files, triggers/runners: `chat.yml` (push main, release-1, int/**, release/*/main; PR release/*/main; dispatch; Ubuntu+Windows), `ci.yml` (same; Ubuntu+macOS+Windows), `execution-size.yml` (PR release/*/main or release/*/plan-*; Ubuntu), `journey.yml` (push int/r1; daily schedule; workflow_call/dispatch; Ubuntu 24.04 and matrix runners), `lanes.yml` (push main, release-1, int/**, release/*/main; schedule/dispatch; Ubuntu), `task-stall-diagnostics.yml` (PR release/*/main; Ubuntu), `windows-install-guard.yml` (PR/dispatch; Windows), `windows-journey.yml` (push main, release-1, windows/**, release/*/main; PR main/release/*/main; dispatch; Windows), `windows-runtime-retention.yml` (push main/release/*/main; PR main/release/*/main; dispatch; Windows). Evidence: workflow files, e.g. `ci.yml:6-14`, `journey.yml:7-13`, `windows-journey.yml:3-14`.

GitHub REST required-status-check endpoint returned HTTP 404 “Branch not protected” for Agent `release/15/main` and `release/14/main`; required checks not discoverable.

## Journeys, render tests, fixtures

`tests/journeys/` covers journey plumbing; `test_cross_client.py` says “real Runtime daemon” (`line 1`). Installed `journey.yml` checks out App/Agent/Runtime candidates and records install receipts; it triggers on int/r1/schedule/call/dispatch, not release/15 push. No timeline render/visualize call found in that workflow. Integrations include real Runtime + `GenericPackHost` Remotion acceptance: `test_generic_host_remotion_render.py:266-338`; it executes `rendering.render`. `test_c06_public_timeline_visualizer.py:201,245` calls `timelines.visualize` with a matching render.

Latest five REST runs (seconds; result): Agent installed journey `journey.yml`: 364 success, 333 success, 301 success, 500 success, 554 success (all release/14 dispatch; no release/15 runs). App `direct-journey.yml`: 1132 success, 592 cancelled, 1333 success, 706 success, 816 success. App `e2e.yml` on release/15: 2249 failure, 3508 failure, 2705 cancelled, 4238 failure, 8020 failure. Runtime has no journey workflow.

Rendering tests exist under `tests/packs/rendering/` and `tests/core/rendering/`. A real small Remotion render exists: `test_remotion_real_render_under_global_angle_keeps_identity` uses `render(... selector="rendering.remotion")`, then asserts 12 frames at 320×180 (`test_remotion_backend.py:1558-1619`); it’s a production render-facade call, not a literal shell command `remotion render`. Marked `integration`, timeout 600; default pytest excludes integration/remotion (`pyproject.toml:311-315`). Integration lanes provision npm and browser `lanes.yml:188-195`. No `ASTRID_RUN_REMOTION` gate found.

`tests/fixtures/packs/astrid_motion/` is a full copied pack fixture with schemas, implementations, docs and preview assets (`README.md:1-20`); used by timeline placement and `am-type` contrast tests (`test_timeline_element_placement.py:29-33`, `test_am_type_default_contrast.py:20-22`). Timeline fixtures include `tests/fixtures/timeline/`, `timeline_editing/`, and `timeline_visualize/` (including compositor parity cases); listed by tree at Agent SHA. No literal `remotion_cli` tiny-composition command test found.

## Remotion provisioning

Agent `ci.yml` unit shard installs `npm ci --prefix remotion` (default markers exclude render lanes); its macOS job caches by lockfile, installs npm + ensures the browser, then selects `darwin_native or remotion or chrome or codex_cli` (`ci.yml:328-329,453-515`). `lanes.yml` integration/opt-in installs Remotion and ensures Chromium (`lanes.yml:188-195`).

## App and Runtime

App: `direct-journey.yml` (PR path-filter, schedule, dispatch; Ubuntu 24.04), `dockerfile-check.yml` (PR/push; Ubuntu), `e2e.yml` (push main, release-1, int/**, release/*/main, dispatch; Ubuntu 24.04), `installer-windows.yml` (push feat/pinokio, main, PR; Windows), `lanes.yml` (push/schedule/dispatch; Ubuntu/matrix), `p61-c4-readiness.yml`, `p61-startup.yml`, `p61-workflow-pins.yml` (PR release/14/plan-61; macOS), `public-vision.yml` (PR/dispatch; Ubuntu+macOS), `served-manifest-canary.yml` (schedule/dispatch; Ubuntu), `test.yml` (push main, release-1, int/**, release/*/main, PR main/release/*/main/release/14/plan-61, dispatch; Ubuntu+macOS). Evidence: `.github/workflows/direct-journey.yml:13-27`, `e2e.yml:6-9`. App CI does compare actual preview frames with decoded CPU Remotion output: `viewing-parity/cases.ts:278-285`. App `lanes.yml:184-195` provisions Agent Remotion/browser and Chrome.

Runtime has `ci.yml` (push main/release/*/main/int/**/release/14/plan-39; PR all; dispatch; Ubuntu/macOS/Windows) and `nightly.yml` (daily schedule, push release/14/plan-39, dispatch; Ubuntu) (`ci.yml:4-9`, `nightly.yml:3-8`). No Runtime rendering/preview-frame CI test or journey workflow found. Branch protection API returned 404 “Branch not protected” for both release branches across App and Runtime too.
