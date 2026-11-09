# Zero-to-first-image onboarding

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Make the first useful result effortless: from an existing supported inference installation, one copyable command guides a person and their agent through setup to a generated image visible on an Astrid timeline. This is a top-priority upcoming draft; status, owner, and estimate live in the [project queue](../../README.md).

## Goal and scope

- Included: one excellent supported inference path, reusing current setup, connection, generation, media, and timeline capabilities; clear actionable prerequisite checks; matching agent instruction; focused recovery; measured agent effort.
- Coordinate with [agent setup](../16-streamlined-agent-experience/plan.md) and [inference routing](../12-multiple-inference-routes/plan.md) only where the chosen first-image path needs their existing capabilities. The optional full-stack sandbox is a separately qualified outcome of [Plan 15](../15-openshell-safe-execution/plan.md), **not a prerequisite or completion gate for first-image onboarding**.
- Deferred: additional inference routes until the first journey is demonstrated; making every backend a prerequisite.
- Still undecided: supported starting environment, exact route, account/model prerequisites, and task breakdown, routes, and selectors. Scope these from current source before dispatch.

## What we build on

Reuse existing installation, connection, generation, media, and timeline capabilities where verified. The [Liquid Software vision](../../vision/pillars/liquid-software.md) calls for good defaults, understandable choices, and user control. Exact source identities and evidence limits belong in [inputs](inputs.md).

## Sequence

1. Establish the supported starting state and inspect existing onboarding and timeline paths.
2. Define the one-command journey, matching agent instruction, visible consent, and actionable prerequisite handling.
3. Prove a real image reaches the timeline, then cover named recovery paths and measure total token use including retries.
4. Hand off any sandbox-specific setup or isolation problems to [Plan 15](../15-openshell-safe-execution/plan.md) without blocking first-image proof on unrelated sandbox qualification.

See [tasks](tasks.md) for the intended proof and the scoping still required.

## Project interface and handoff

**Consumes:** an explicitly supported Astrid Runtime/App and an existing inference service/model, as verified in [inputs.md](inputs.md). Prior setup or compatible packs are reusable foundations, not assumed-working features.

**Produces:** one copyable first-image onboarding path and matching agent instruction, with real generation-to-timeline evidence and measured recovery/effort on the selected supported environment. Record the exact tested candidate and proof in the completion PR; [Plan 15](../15-openshell-safe-execution/plan.md) owns any separately qualified sandbox mode.

## Completion

A new user can follow the short instruction from the declared starting state and see a real generated image on the timeline. Focused evidence covers the selected recovery paths, setup steps, interventions, and token cost; the chosen route's unsupported variants remain explicit. Isolated full-stack execution is proven separately by Plan 15. The roughly 50,000-token figure is a measured design target, not a recorded result. This draft does not authorize product work, compute use, or publication; follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md).

## Read next

- [tasks.md](tasks.md): intended work and draft proof requirements.
- [inputs.md](inputs.md): source identities, related plans, and evidence limits.

## Direction (owner, 9 Nov 2026)

The route is **an attached ComfyUI** (the user's own), reached through [Plan 32](../32-generation-placement-targets/plan.md) S2's guided generation setup. Plan 32 S2 delivers the agent side, plus one line in the App's install brief (`agentInstructions`) pointing to "Set up my generation" by skill name and public URL. This plan adds the App side: after Connected, the welcome flow shows a **"Set up generation" card** with a "Copy for your agent" brief (a new `copy.ts` function next to `agentInstructions`). Its proof is a real first image from a saved workflow.
