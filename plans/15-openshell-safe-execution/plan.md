# Sandboxed execution with OpenShell

**Project:** Sandboxed execution with OpenShell

**Goal:** Give creators an optional, understandable isolated Astrid installation in ordinary onboarding, retaining the normal browser, agent and generation experience where the isolation boundary permits it.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** scope agreement

**Vision gaps:** [F-007 — First-class full-stack sandboxing](../../vision/gaps/F-007-first-class-sandbox.md) (primary); [F-002 — trustworthy user control](../../vision/gaps/F-002-safe-user-control.md) (supporting). The sandbox outcome is independently testable; broader consent and recovery require separate evidence.

**Contributing:** [Astrid development skill](../../agent/start.md).

## Goal and scope

Exploratory revision (25 November 2026). The owner asked for an ordinary onboarding checkbox to run Astrid inside OpenShell and for investigation of the compromises for existing agents and ComfyUI. This is a deployment option for Astrid, not a separate product, a new agent framework, or a claim of absolute safety. Keep native installation unchanged. No implementation, scheduling or release is authorized by this draft.

- **Onboarding:** add a visible, initially opt-in choice, proposed copy: “Run Astrid in an isolated environment (OpenShell)”. Explain that the agent and its tools run in a separate VM, personal files and unrelated services are not exposed, and external agents may need to be installed and signed in again. Use the existing App setup surface, copied coding-agent instructions, terminal setup and [Plan 20](../20-zero-to-first-image/plan.md) choices contract. A host launcher must create and verify the VM before running the guest installer; the existing internal `--sandbox` process-control flag is not itself an isolation mechanism. Preserve the choice on repair, update and restart; never fall back to a native install after an isolation failure. Do not show an actionable option on an unqualified platform.
- **Boundary:** default to a dedicated microVM, no host directory mounts, no inherited host credentials or agent config, no ambient LAN or unrestricted outbound access, explicitly selected services and user-mediated file transfer. The Agent, Runtime, chat/ACP processes, terminals, pack code, project data, renderer and their children run in the guest. The host browser and small trusted launcher/gateway are outside. Reuse the browser door; qualify the App build, authentication, instance identity and media/events transport. Investigate pinned/local App serving in the guest, but do not assume browser-executed extensions inherit guest network policy. Review their trust, egress and exposed host interfaces separately before claiming full-stack isolation.
- **Existing ComfyUI:** make API-only attachment to a user-authorized existing host ComfyUI a first-class connected mode, reusing the current relay and HTTP upload/history/`/view` artifact path without exposing the output folder. The strict mode has no host ComfyUI grant. Model discovery and generation using already available models/nodes should remain familiar; host installation, model downloads into host folders, node management and process control cannot be silently performed by the guest. Explicitly separate these operations and consent. Test node/parameter and job-scope restrictions enforced outside guest control; unrestricted native custom nodes can exercise host permissions, so endpoint allowlisting alone is not strong isolation. If a narrowly scoped trusted broker or isolated ComfyUI worker is needed, scope it from evidence; do not require a new GPU isolation architecture for an initial connected option. No weakening of strict mode to make connected mode work.
- **Agents:** preserve the existing chat/ACP, CLI, skill, tool and project interfaces. Discover, install, authenticate and launch agents inside the guest; do not copy or mount host agent homes, credentials, MCP configuration or binaries, or silently launch a native agent. Astrid's bundled agent and Codex have historical OpenShell setup paths. Claude Code and Hermes exist in the current product catalog but lack equivalent qualified sandbox setup. Investigate each agent's guest dependencies, provider access, login flow, skill sync, terminal commands, cancellation, session recovery, and nested sandbox assumptions. Show honest unavailable/setup-needed states rather than breaking the native agent menu. An outside coding agent may perform the explicitly approved initial host setup; it is not the same thing as Astrid's in-guest agent.
- **Lifecycle and custody:** retain project/media IDs, manifests, generation settlement and browser editing contracts; import/export files through an explicit trusted transfer path rather than exposing personal folders. Keep guest data through stop, restart, update and rollback. Provide recovery, permission inspection and revocation, emergency stop and safe removal. A failed install/update must restore restrictive policy or stop the VM. No destructive rebuild as normal setup.
- **External inference:** explicitly selected network/service and spend permissions, scoped credentials where supported, and visible data sent outside the VM. No claim that network permission is equivalent to privacy from an authorized provider or that all packs are isolated from each other inside one VM.

## What we build on

[Agent PR #109](https://github.com/banodoco/astrid-agent/pull/109) is the retained contribution; much of its harness, process-control flag, policy composer and documentation are already in the release-15 manifest's pinned Agent, rather than needing wholesale resurrection. Current attached generation downloads attributed artifacts over HTTP and accepts an empty legacy output-directory argument; the OpenShell launcher still requires a share. Reconcile those seams, not the generation result or timeline architecture. [Inputs](inputs.md) records source identities and limitations. Runtime #8/#9 and VibeComfy #160 are historical merged prerequisites; check actual candidate pins and issue #746 rather than assume every general fix is settled.

## Sequence

1. Reconcile the release candidate, upstream OpenShell version/driver/platform support, and existing code. Investigate mount-free ComfyUI, actual agent compatibility, onboarding/installer and browser trust boundaries in parallel.
2. Agree the strict/connected threat model, platform/agent support matrix and install/instance contract. Independently critique this security boundary before seeking implementation greenlight.
3. If approved and scheduled, adapt the existing launcher, App setup choice, guest agent setup and API-only generation attachment in bounded lanes; preserve native behavior. Integrate once the shared mode/permission and Runtime identity contracts are settled.
4. Qualify a real installed creative journey and negative cases on each declared supported platform before surfacing the option. Linux x86-64 with usable virtualization is a proposed first lane; macOS and Windows require their own qualification, and current upstream support must be rechecked.

Coordinate at actual shared surfaces with [onboarding](../20-zero-to-first-image/plan.md), [agent setup](../16-streamlined-agent-experience/plan.md), [generation placement](../32-generation-placement-targets/plan.md) and [inference routing](../12-multiple-inference-routes/plan.md). These are not blanket scheduling dependencies.

## Completion

On a declared supported platform a person selects the checkbox, completes the normal setup (including agent-led setup), connects the browser to the intended VM, connects an approved agent account, creates a project, generates from authorized existing ComfyUI without a host folder mount, retrieves media into guest custody, edits, saves/reopens, renders and exports. Demonstrate cancellation, service revocation, stop/restart, update/recovery and project preservation. Strict mode refuses host ComfyUI; both modes refuse unrelated host files, credentials, sockets, native execution and unapproved network access; connected mode documents and tests its narrower boundary and residual host custom-node risk. Show unsupported agent/platform states and failed-setup refusal, plus native-install regression checks. Record version-pinned positive and negative installed evidence, not just script or unit-test existence. Integration and publication follow the [shared run contract](../../agent/shared/run-contract.md).

## Read next

- [Tasks](tasks.md): exploratory lanes and proposed gates, not executable assignments.
- [Inputs](inputs.md): retained contribution, current source evidence and unresolved decisions.
