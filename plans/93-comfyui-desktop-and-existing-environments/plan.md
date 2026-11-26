# ComfyUI Desktop and existing environments

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

**Project:** ComfyUI Desktop and existing environments

**Goal:** A creator who already has ComfyUI, including ComfyUI Desktop on Windows, gets an image from Astrid through it, and when it is closed or broken is told exactly what is true and the one thing to do next.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 5–7 engineering days: the readiness ladder 2, existing-install rungs and next steps 2–3, wording 0.5, review 0.5–1, all on CPU. The installed Desktop witness is later work.

**Waiting on:** the owner's decisions D2–D5 in [inputs.md](inputs.md#owner-decisions) and the Run start; Release 16's base for the branch.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) and [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Outcome and scope

A person who already uses ComfyUI shouldn't need another copy to use Astrid. They should never need to know which plan they are in: they see what is true and what happens next.

### What the person sees

- **Running:** "Using your ComfyUI Desktop." The image arrives in the editor.
- **Closed:** "Found your ComfyUI Desktop. It's closed. Open it and I'll carry on." Once it is open, Astrid checks again and continues.
- **Broken:** "Your Desktop install points at a folder that no longer exists. Reinstall Desktop, or I can set up a separate copy." The second option is [Plan 94](../94-dependable-environment-setup-and-recovery/plan.md)'s, with its own consent.
- **More than one install, or one it can't tell apart:** it names them and asks which, never choosing silently.
- **Not supported here:** it says so, and says what works.

Their install stays theirs. Astrid never starts, restarts, patches, updates or replaces ComfyUI Desktop or Pinokio by itself; it asks the person to open it. "Done" means an image they can open in the editor, never "found an install" or "port answered".

### The readiness ladder (the contract this plan defines, and Plan 94 extends)

One existing command answers "can I make an image here?" for the agent: `generate targets` and the readiness envelope it returns (`astrid/core/generation/preflight.py:readiness_envelope`). Each rung is a verified fact with one owner, checked in this order:

1. **installed:** an install is recorded and its files exist;
2. **reachable:** something answers on its endpoint;
3. **identified:** what answers is ComfyUI, and the same install that was found;
4. **compatible:** its version and API are ones Astrid supports;
5. **computes:** the selected environment ran a real GPU computation (Plan 94 adds this rung's check);
6. **workflow ready:** the entry's nodes and models are present (Plans 56 and 90 own this);
7. **delivered:** an image reached the editor.

The answer stops at the first rung that fails or wasn't checked, naming the rung, the reason, and exactly one next action. That action is either something the person does (open Desktop) or one Astrid command the agent runs. `ready` means every rung up to `workflow ready` was positively observed. Today the envelope reads `ready` whenever no issue was raised (`preflight.py:98-99`), so an unchecked target can read ready. And `generate targets` inspects selection without probing (`astrid/sdk/generation.py:1335`). Both change here.

The agent's skills reduce to: run `generate targets`, and do what its next action says. The agent never writes an install script or researches a setup problem itself.

**Included:**
- the ladder in the existing readiness envelope and `generate targets`, with no second command, registry or preference store;
- the existing-install rungs for ComfyUI Desktop on Windows: a running install, a closed one, a stale registration whose recorded files are gone (#1848), a wrong responder on the install's port, a denied or ambiguous observation, and several installs;
- next actions: the person-side start instruction, re-probing after it, and attaching the chosen endpoint through the existing consented placement (Plan 20's `settings set placement`, Plan 32's path);
- the setup and VibeComfy skills and the editor's connection copy, saying the same states;
- the Desktop checks on CPU fixtures. The installed Desktop witness and the Portable, Git and Pinokio regression checks are later work, see [tasks.md](tasks.md#later-real-hardware-qualification-not-in-release-16). No lane tests on the owner's machine.

**Not included:**
- Astrid launching Desktop itself (the native launch boundary is Linux-only today and needs Desktop's own launcher; see D3);
- installing ComfyUI anywhere, which is Plan 94's;
- repairing or patching a third-party install;
- remote ComfyUI or other engines;
- workflow dependencies (Plans 56 and 90);
- process identity (Plan 38).

## Existing work and decision

- **Plan 20 phase 4** shipped the first-image flow but left out Desktop discovery and stopped installs.
- **The scan** (`astrid/packs/vibecomfy/local.py:scan`) finds answering endpoints only, and skips the ComfyUI-shape check on ordinary ports (`:282`).
- **The target record** (`astrid/core/generation/targets.py:TargetRecord`) already names the Desktop, Portable, Git and Pinokio layouts.
- **The VibeComfy guide** already covers denied loopback access, changed ports and several servers.
- **The tester run** (#1848) found Desktop 0.7.2 still registered after its executable and data folder had gone. The scan returned no servers and no errors, and the image came from Portable.

The plan reuses all of these and changes only what makes an unchecked target look ready. An independent Astra review checked the draft against the code ([critique](evidence/critique.md)). It cut native launch and broad layout discovery, and asked for the responder to be tied to the install; [inputs.md](inputs.md#planning-evidence) records each answer.

## Sequence and readiness

1. **CD-0:** capture the real Desktop states from #1848's report and inventory the code and tests.
2. **CD-1:** the ladder contract, then **RS1** reviews it, because Plan 94 and the rest of this plan build on it.
3. **CD-2 and CD-3:** the existing-install rungs and the next actions, in parallel.
4. **CD-4:** the wording.
5. **R:** the final review.

Plan 94 starts its install branch once RS1 accepts the ladder. The details are in [tasks.md](tasks.md). Recording this plan authorizes no implementation.

## Interfaces and handoff

- **Consumes:**
  - Plan 20's setup skill;
  - Plan 32's placement and generation path;
  - the target record, scan and readiness envelope;
  - Plan 56's workflow readiness when it lands;
  - Plan 34's GPU evidence format.

  Exact commits are pinned at dispatch.
- **Produces:**
  - the readiness ladder in `generate targets`;
  - a verified or explicitly blocked existing-install disposition (installed, reachable, identified, compatible, with the owning layout and the one next action), which Plan 94 consumes and does not re-derive;
  - the updated skills and editor copy.

## Completion

For Release 16, completion is every remaining card's focused CPU tests passing on base and head. CPU fixtures prove that each case below stops at the right rung with its reason and one next action, and leaves placement unchanged where it refuses:
- **A running Desktop** is found, identified as that install, and attached.
- **A closed Desktop** gets "open it", and once the person opens it, the next check continues.
- **A stale registration** is diagnosed as broken, with no data deleted, and the next action offers Desktop's reinstall or Plan 94's separate copy.
- **Another server on Desktop's old port** is never reported as Desktop; denied access, two installs and a declined consent each stop at the right rung.
- **Nothing reads `ready`** without the observations behind it.
- **The skills** tell the agent to run `generate targets` and do its next action.

Real-hardware proof is later work, not part of Release 16: the installed Desktop witness through [user test request #1952](https://github.com/banodoco/astrid-dev/issues/1952), the image in the editor, the unrelated queued job, the time from intent to image, zero off-script steps, and Portable, Git and Pinokio regression checks where available. See [Later](tasks.md#later-real-hardware-qualification-not-in-release-16). No hardware use, spending or publication is authorized by this plan.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

one selected existing Placement and scoped observations, not another target token or universal readiness ladder. Explicit compatible endpoint may be usable with unknown filesystem identity; no guessed interpreter or lifecycle takeover. Person opens closed Desktop. Readiness distinguishes observation, dependency, compute, workflow and actual delivery.
