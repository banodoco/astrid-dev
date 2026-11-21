# Editing a real clip: project elements and practical fixes

**Project:** Editing a real clip: project elements and practical fixes

**Goal:** The fixes and the custom-element work made while editing a real clip and its tools land in Release 15: a project's own effects and components load in every editor and render the same in preview and in the final render, and a failure to load them never blocks the editor or the agent.

**Status:** queued

**Owner:** Codex manager (hosted in Claude session session_011EzfW1FXS3o7GFnNSB7cZS)

**Estimate:** About 2 engineering days (1 to 3): the inventory, the open Runtime question, and landing.

**Waiting on:** a manager; the [handover](handover.md) has the first actions.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-004 — Pack installation and upgrades aren't yet proven under demanding conditions](../../vision/gaps/F-004-pack-lifecycle.md) (primary), [LS-001 — Creative components can't yet move freely](../../vision/gaps/LS-001-portable-components.md).

## Outcome and scope

**Where it came from:** the owner's own hands-on editing on 18 to 21 November 2026, "trying to edit a clip on the timeline and actually edit the tools", fixing and improving what the video editor and timeline needed for practical use. It is not part of Plan 59's Minkhole project. This plan records that work, which was already under way on `release/14/plan-69` in astrid-app, astrid-agent and astrid-runtime, before any plan described it (commits from 18 to 21 November 2026). Read from its commits, it covers:

- **Admission:** the Agent admits a project's elements (effects and components) by compiling them with the renderer's own Node and esbuild into the pack snapshot; re-admitting an unchanged legacy admission upgrades it.
- **Serving:** the Runtime serves the admitted element bundles, scoped to the project being read, and lists them without reading snapshots.
- **Loading:** every editor loads admitted elements from the Runtime through the extension loader's import path, fenced by project. A failed list never blocks prompts, the editor or the preview; the clip that needs an element shows a placeholder with the reason.
- **One compiler:** render stages the same compiled module the preview uses.
- **Editing verbs:** `place-element` points a built-in effect clip at an admitted project effect; `clip.set-element` refuses unbound clips.
- **Speed and validation fixes found on the way:** strict timing validation judges only clips the candidate added or changed; a shot's revision bump keeps the baseline of clips it does not touch; the Runtime verifies stored objects once per process instead of re-hashing timeline history; Runtime calls get a timeout long enough for large realms.

Out of scope: anything the owner does not confirm, and the next steps, which are their own plans built on this one:

- [Plan 78](../78-live-custom-element-editing/plan.md) — live custom-element editing: the editor's agent writes an element and applies it with the rest of an edit in one commit, with no restart or reload. It consumes this plan's Agent, Runtime and App work.
- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) — saving holds on a heavy timeline; its branches already include this plan's, for the validation and Runtime speed fixes.

## Existing work and decision

The work exists; this pack gives it a plan, a release and a branch so it can land through Release 15. See [inputs](inputs.md#planning-evidence).

## Sequence and readiness

The code is done; what is left is checking it and landing it. PE-1 inventories it against the outcome above; PE-2 answers the one open Runtime question ([astrid-dev#1222](https://github.com/banodoco/astrid-dev/issues/1222)); PE-3 brings the branches current and lands them into `release/15/main`, Runtime then Agent then App. See [tasks](tasks.md) and the [handover](handover.md). In Release 15 this plan runs first, then [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), by one manager ([brief](../../releases/15/briefs/plans-69-77.md)).

## Interfaces and handoff

It consumes `release/15/main` in each repository. It produces admitted project elements served by the Runtime and loaded by the App, the validation-scope and object-verification speed fixes, and the pins that tie App, Agent and Runtime together. [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) merges this plan's branch into its own; [Plan 78](../78-live-custom-element-editing/plan.md) starts from it.

## Completion

Pending the owner's scope: at least, a project with an admitted effect and component opens in a fresh editor, previews and renders identically, and an editor whose element list fails still opens, prompts and saves, with the failing clip showing the reason.
