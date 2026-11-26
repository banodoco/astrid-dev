# One native Astrid application

**Project:** One native Astrid application

**Goal:** A creator installs, opens, updates and repairs Astrid from one native cross-platform application, using either the hosted interface or the same locally bundled editor.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.3

**Estimate:** TBD

**Waiting on:** Independent scope and release placement; Plan 100 lifecycle boundary for ownership transfer; retain qualified Plans 09/29/30/31/38/62/93/94.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting) · [Pack lifecycle](../../vision/gaps/F-004-pack-lifecycle.md) (supporting)

**Contributes to closure:** LS-006: E2: independent installation, repair and interchangeable interfaces.

## Outcome and scope

**Draft proposal — owner agreed the direction on 26 November 2026, but detailed project scope, independent challenge and release placement are pending. No implementation authorized.**

Deliver a small signed/verified Rust bootstrap/controller and optional desktop shell on declared Windows, Linux and macOS architectures. Bootstrap is independent of installed Python/Node and of a broken core version; provisions pinned components, supports progress/cancellation/resume, verifies artifacts, keeps last known-good program selection, diagnoses disk/permission/dependency failures, and recovers interrupted transactions. Use existing uv, managed packages and existing ComfyUI environments; no new package manager or bundled CUDA stack by default.

Initially delegate to the existing installer/runtime where safe, then transfer installation/version/lifecycle ownership once, after parity; retire duplicated native-owned paths rather than keeping two managers. One manifest identifies the exact selected App, Runtime, Agent and tools. OS service/start-at-login/tray/stop behavior respects the actual owner and durable active-task refusal. Explicitly preserve Pinokio and other external-manager ownership via attach/delegate; no unconsented takeover. Runtime remains workspace authority.

Serve the compiled React frontend locally without requiring a production Vite/Node server. Offer the same workspace via astrid.haus, localhost, an optional desktop window and headless CLI. Use the same React code/build and typed API; preserve development Vite/HMR and agent-created extensions. Static production hosting is not a frozen interface: qualify the same admitted extension artifact/version and capability bridge in local, hosted and desktop routes, with an optional managed build service. A frontend pack can be created, updated, mounted and selected as an alternative view without rebuilding Rust or the base app; failed activation restores the last working view. Reuse Plan 41/47's authoring and lifecycle proof rather than another build/extension manager; see [shared design](../100-language-independent-foundation/architecture.md#agent-authored-tools-and-replaceable-default-interfaces). Qualify browser door/localhost permission and exact origins, scoped tokens, media decoding/preview, drag/drop, paths, offline editing, custom elements and Remotion rendering. Desktop shell choice Tauri/Electron/other follows a bounded cross-OS test, not preference.

Out: rewriting Python workspace internals or creative packs, guaranteeing every GPU, automatic conversion of external installs, and remote hosted accounts. While the Python reference remains, repairing its environment may be required before editing; Plan 103 supplies native workspace operation without it.

## Existing work and decision

Current App public/install and install.ps1 bootstrap Python, Agent installer owns installation transactions and service registration, Runtime owns bootstrap/worker lifecycle, and App dev-local-workspace.mjs also launches and updates. Reuse current installation and recovery behavior from Plans 09, 29, 30, 31, 38, 62, 93 and 94; no parallel transaction owner. See [architecture](../100-language-independent-foundation/architecture.md). See [inputs](inputs.md#planning-evidence) for alternatives, review limits and outstanding owner decisions. This is not an authorization to alter accepted existing projects.

## Sequence and readiness

Prototype native bootstrap and static hosting using isolated roots; compare desktop engine behavior on the same editor build; review lifecycle ownership and migration with Plan 100 before transfer. Qualify clean install, adoption, repair, update and rollback on supported OSes and the external-manager route. Product changes require the selected release; preserve the Python reference until Plan 103's separate cutover. The [task outline](tasks.md) is not a dispatch packet. Re-estimate after the first bounded evidence slice; do not assign to a release or start product work without a recorded run decision.

## Interfaces and handoff

Consumes Plan 100's lifecycle/identity boundary, official install manifest, current selected-version and backup/restore contracts, Plan 94's managed environment setup and Plan 93's existing ComfyUI discovery as qualified. Produces verified native distribution artifacts, one controller/manifest contract, same-UI local/hosted/headless entry points, native recovery and migration receipts. Plan 103 plugs in the native daemon without inventing a new installer.

## Completion

- Clean installed-product journeys on declared Windows/Linux/macOS: native install, open hosted and local UI on same project, edit/save/reopen, agent connection and a supported creative result. Native real-device GPU proof is separately authorized; CPU fixture is not GPU evidence.
- Corrupt/remove managed Python and Node separately; bootstrap still diagnoses and repairs selected components, preserves project bytes and restores a working editor; interrupted update/repair resumes or rolls back safely.
- Existing installation adoption preserves projects, credentials, settings, custom packs, selected environment and logs; Pinokio-managed installation refuses takeover and uses its owner path.
- Close all interfaces: active work continues or settles according to existing policy. Duplicate launch attaches or refuses; unsafe shutdown refuses; no stray descendants.
- Compare desktop/local/hosted UI against exact compatible builds, including media/rendering and origin/token refusal, offline access and live dev/pack updates. No production Node process solely for serving static UI. Prove the same separately built tool artifact mounts and receives scoped operations in local and hosted UI, without a native rebuild; failed build/mount leaves base UI and creative resources usable.

Scope completion is contribution to LS-006, not automatic gap closure; qualify the integrated release separately and record limits.
