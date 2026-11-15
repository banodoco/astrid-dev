# Workflow set-up

**Project:** Workflow set-up

**Goal:** One command gets everything a ComfyUI workflow needs, its models and its custom node packs, and anything it cannot find is reconciled in one simple step.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 1–2

**Waiting on:** [Release 13](../../releases/13.md) publishing, the model fingerprint look-up fix that follows it, and the owner's answers to D1 to D3 in [inputs.md](inputs.md#owner-decisions)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each, then run `python3 scripts/astrid_dev.py sync`. Its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a workflow is only portable if the place it lands can be made ready for it without a person hunting for files.

## Outcome and scope

A person or their agent points Astrid at any workflow, bundled or their own, and at a ComfyUI. Astrid answers in two steps.

1. **Plan.** Every model and every node pack Astrid can see the workflow needs, each marked *present*, *found* (with its source, size and where it will go) or *not found*. What it cannot determine yet is listed as unknown, not hidden. Nothing is installed or downloaded.
2. **Apply.** After approval of that exact plan, Astrid installs the node packs and downloads the models, reporting each action as done, failed or pending. It is not all-or-nothing: what succeeded stays, and a second run continues from there.
3. **Restart and continue, when node packs were installed.** A new node pack is not loaded until ComfyUI restarts, and some models can only be named once its nodes are loaded. Astrid stops at "restart needed", the person restarts their ComfyUI (Astrid restarts one it manages), and the same command continues. Anything newly discovered at that point is shown for approval again.

Anything *not found* is reconciled the same way for models and node packs:

- **Offer what is already there.** A model under another name or folder; a node pack already installed.
- **Look in what Astrid and VibeComfy already know.** Declared sources, the model registry and its aliases, the node-pack definitions and lock; for node packs, the ComfyUI-Manager list once WS-5 has proven that path against real data. A candidate is evidence, never applied without confirmation.
- **Ask once.** The person or agent gives an address; Astrid records it and never asks again.

### Included

- One list of requirements from any workflow, for models and node packs together.
- The plan and apply command, on a ComfyUI Astrid manages and on a person's own ComfyUI on the same machine.
- Telling Astrid that a file the person already has is the model a workflow asks for, and giving a source for one it lacks, each recorded once ([issue 665](https://github.com/banodoco/astrid-dev/issues/665)). Identifying an unknown file from its contents and searching other sites are later steps of that issue, not this plan.
- Reports that say what is true: an unknown node is called unknown, not a ComfyUI core node; a missing item names its source.
- One path in the skills.

### Not included

Changing which models or node packs bundled workflows use. Replacing anything a person's ComfyUI already has: if a node pack's requirements would change a Python package that is already installed, or a pack folder already exists, Astrid refuses that item, says why, and leaves it to the person. A ComfyUI on another machine. Rolling back a person's Python environment. Rented-machine model caches. Speed of the generation itself ([Plan 55](../55-local-speed/plan.md)).

## Existing work and decision

Most of the parts exist and are not joined up ([inputs.md](inputs.md#planning-evidence)). Models known to Astrid already have a plan-and-apply download for bundled entries; a managed ComfyUI already installs pinned node packs with their requirements; VibeComfy already has a resolver that reads the ComfyUI-Manager node list, which readiness does not call. VibeComfy also already has a combined report (`vibecomfy nodes reconcile`) and can install packs, reload and fetch models as part of a run. What is missing is one front door, coverage of a person's own workflow, a recorded answer for anything unknown, and safe behaviour on a person's own ComfyUI. The approach is one front door over those existing pieces, not a second mechanism.

## Sequence and readiness

WS-1 is a small correction and goes in the standing fixes lane straight after the fingerprint fix. WS-2 builds the one list on the existing requirements contract; WS-3 the command on it; WS-4 the reconcile step; WS-5 proves the ComfyUI-Manager path on real data before anything depends on it; WS-6 the proof. WS-3 waits for D1, because it is the first time Astrid would install code into a person's own ComfyUI. Task details are in [tasks.md](tasks.md). Recording this plan authorizes no work.

## Interfaces and handoff

**Consumes:** the fingerprint look-up-and-record fix (astrid-agent `r13/cells-model-lookup`, identified at run start); the existing download plan (`astrid generate fetch-models`) and alignment (`astrid generate align`); VibeComfy's node-pack lock, installer and pack resolver.

**Produces:** one requirements list other features can read (readiness, onboarding, the App); a record of confirmed sources and matches; the set-up command and its plan format.

## Completion

- From an empty model folder, the command makes each default workflow (image, edit, music, speech, sound effects, video) runnable on a person's own ComfyUI, with one approval where no node pack is needed and one more after the restart where one is; a further run of the plan reports everything present.
- A bundled workflow that is refused today for an undeclared fingerprint is set up on a managed ComfyUI.
- A person's own workflow that names a model Astrid has never seen: the plan marks it not found and asks once for a source or an existing file; after the answer, the next plan finds it without asking.
- A model present under another name is offered, not downloaded again.
- A workflow using a node pack outside Astrid's lock: the plan names the pack and its repository; apply installs it only after approval, pinned, and reports the restart.
- Negative cases: a download that does not match its fingerprint fails and leaves no file at its destination; a node pack whose requirements would change any package already installed in a person's ComfyUI is refused with the reason and nothing is changed; a failure part-way reports what was done and what was not; nothing is installed without the approved plan.
- Limits: only what Astrid can see a workflow needs is listed; a custom loader node Astrid does not understand may hide a model until its pack is loaded. Public sources only. A private or gated model still needs the person's address or credentials.
