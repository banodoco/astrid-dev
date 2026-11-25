# Dependable environment setup and recovery

**Project:** Dependable environment setup and recovery

**Goal:** When a creator has no usable ComfyUI, Astrid offers one separate install with its real cost stated, sets it up safely and resumably after one consent, proves the GPU computes, and delivers an image in the editor, with the agent never improvising.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 1–2 engineering days for ER-0 and ER-1, then estimated from that baseline. Once ER-0 has chosen the route, the install branch, GPU rung, resumable downloads and skill wiring are likely 6–10 more, and the live loop runs until two passing rounds.

**Waiting on:** the owner's decisions D2–D6 in [inputs.md](inputs.md#owner-decisions) and the Run start; [Plan 93](../93-comfyui-desktop-and-existing-environments/plan.md)'s readiness ladder (its RS1) for ER-2 to ER-5; an approved Windows NVIDIA machine or a consented tester, and a matching editor build; Release 16's base for the branch.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [Platform reliability](../../vision/gaps/F-001-platform-reliability.md), [Portable generation](../../vision/gaps/F-008-portable-generation.md) and [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Outcome and scope

This plan is the branch of [Plan 93's readiness ladder](../93-comfyui-desktop-and-existing-environments/plan.md#the-readiness-ladder-the-contract-this-plan-defines-and-plan-94-extends) for "nothing usable here". It adds no second discovery, readiness check or installer. Plan 93 decides whether an existing install can be used. When the answer is none, broken beyond what the person wants to fix, or declined, this plan offers a separate install as that answer's next action.

### What the person sees

- **The offer:** "No working ComfyUI here. I can install one in `D:\Astrid\ComfyUI`: about 12 GB and 20 minutes, nothing else on your machine touched, no cost. Go ahead?" It states the real location, the peak disk space including temporary files, the time, and that it costs nothing. One consent covers the install and its model downloads, within those numbers.
- **Progress:** "Downloading models: 9 of 12 GB."
- **An interruption:** close the laptop halfway through, and next time it reads "Picking up where we left off: 9 of 12 GB done." A half-finished install never blocks a retry and is never mistaken for a working one.
- **A real GPU check:** "Your GPU is listed but this setup can't use it" is said before any download, not discovered by a failed image.
- **Not enough space, a declined offer, or an unsupported GPU:** each is said before anything is written, with what would work. A declined offer leaves the machine exactly as it was.
- **Done** is an image in the editor, never "install succeeded" or "GPU detected".

### What the agent does

It runs `generate targets`. When the next action is the install offer, it shows the person the offer and, on consent, runs the one install command. That command is a task:
- it reports progress;
- it can be resumed;
- it is safe to run twice;
- it ends by attaching the new install through the same placement Plan 93 uses.

The ladder then continues to `computes`, `workflow ready` and `delivered`. The agent writes no scripts and fetches nothing outside Astrid.

### The ten end-state statements (with Plan 93)

1. **An artist can go from a fresh computer to their first creation without knowing what CUDA, Python or a virtual environment is.**
2. **ComfyUI Desktop is a first-class supported environment** (Plan 93's witness, not re-proved here).
3. **Astrid finds and reuses what already works before installing anything new.**
4. **A broken installation becomes a diagnosable and recoverable state, rather than a dead end.**
5. **Seeing a GPU is not enough; Astrid verifies that the selected environment can actually use it.**
6. **Every install, existing or new, uses the same generation path.**
7. **A failed or interrupted setup resumes from verified completed work rather than starting over.**
8. **Astrid never silently replaces a person's environment, modifies unrelated assets or spends their money.**
9. **The agent uses Astrid's commands instead of inventing installation scripts.**
10. **The proof of readiness is a real creative result the person can open in Astrid.**

They hold for the declared supported combinations. An unsupported, refused or unrepairable case ends truthfully, with the reason and what works.

**Included:**
- **The offer as the ladder's next action,** with real location, peak disk, time and zero cost.
- **One install route,** chosen at ER-0: official ComfyUI Portable, or finishing Astrid's Windows recipe. It goes into an isolated destination from a verified source, with a supported start, and attaches through the existing placement.
- **A resumable, idempotent install:** a destination left by a failed run is resumed from verified state, or replaced under the same consent, never refused for good. Today the provisioner refuses any existing destination (`gpu_environment.py:272-297`).
- **The `computes` rung:** the selected interpreter runs a real CUDA computation, and incompatible wheels fail with their cause. Today the probe checks availability only.
- **Astrid's own model download, as a task:** progress, resume, hash mismatch, and a peak-space check before anything is written, counting probes, the resume file and staging.
- **Skill wiring:** the setup skill's no-target branch says "show the offer, run the install command".
- **Routing the tester's other findings to their owners:** the installer's 219-second silence, impossible update advice and zero-duration receipts go to Plans 09, 29, 30 and 31 and the receipt owner, unless one blocks the editor journey.

**Not included:**
- a second install route;
- a new engine or package manager;
- repairing third-party installs;
- Desktop qualification (Plan 93);
- workflow dependencies (Plans 56 and 90);
- process identity (Plan 38);
- a Runtime download task, unless the live loop shows it is needed (D5);
- other operating systems or GPUs beyond the declared one;
- any paid compute.

## Existing work and decision

The tester run (#1848, a Windows 11 laptop with an RTX 5070 Ti) is the gap:
- its Desktop was broken;
- the system PyTorch listed the GPU but failed a real CUDA calculation;
- the agent installed Portable on its own, chose a CUDA build, and fetched 17.28 GB of models with an outside downloader. Astrid's own transfer was skipped, not failed.

Astrid's Windows path can't do this today:
- the engine runner refuses Windows (`engine_runner.py:336`);
- the local endpoint root is POSIX-only (`engine_local_endpoint.py:94`);
- the candidate provisioner refuses any existing destination, and needs admitted source checkouts;
- the disk check runs after temporary probe files are written (`asset_gaps.py:415-475`).

The plan reuses Plan 20's setup flow, Plan 32's placement, Plan 34's GPU evidence format, and the existing verified download. It fills those gaps and nothing beside them. An independent Astra review narrowed it to one fallback, one supported combination and recovery of the install itself ([critique](evidence/critique.md)); [inputs.md](inputs.md#planning-evidence) records each answer.

## Sequence and readiness

A [loop plan](../../agent/roles/manager/live-loop.md):
1. **ER-0 and ER-1:** the inventory and route choice, and the baseline, beside Plan 93's CD-0 and CD-1.
2. **ER-2 to ER-5:** once Plan 93's RS1 accepts the ladder, the install branch, the GPU rung, resumable downloads and skill wiring. RS1 reviews the install's write and consent boundary.
3. **ER-L:** the live loop, until two consecutive passing rounds or a recorded stop.

Details are in [tasks.md](tasks.md). Recording this plan authorizes no implementation, hardware use or spend.

## Interfaces and handoff

- **Consumes:**
  - Plan 93's ladder and its existing-install disposition;
  - Plan 20's setup entrypoints and Plan 32's placement;
  - the existing recipe and GPU environment code, and the verified, resumable download;
  - Plan 34's evidence format;
  - Plan 56's and, when landed, Plan 90's workflow readiness.
- **Produces:**
  - the install offer and command, and the `computes` rung;
  - the resumable install and downloads;
  - the updated setup skill;
  - the live-round evidence in `rounds.md`, with exact installed tuples;
  - issues routed to the owners of the installer, update and receipt findings.

The proof can feed Release 17's stable qualification, not replace it.

## Completion

The bar: an external coding agent with only Astrid's maintained instructions and a creative intention. On the declared Windows NVIDIA combination, through the installed CLI and the matching editor, it takes these, each to an image in the editor (then a warm image), on two consecutive rounds:
- a clean machine;
- a machine whose Desktop Plan 93 reports as broken.

It follows next actions only, with zero off-script steps. Recorded for each round:
- versions;
- the GPU computation;
- setup time and time from intent to first image;
- bytes downloaded and reused;
- consent steps.

Negative cases, each ending truthfully with nothing unconsented written:
- an install interrupted after its files were written, then resumed or retried through the same command;
- a download interrupted and resumed;
- too little disk, said before writing;
- a declined offer, leaving the machine unchanged;
- incompatible CUDA, named;
- an unsupported GPU, told what works;
- an older editor, which never recommends an impossible update.

Generated project data only, with cleanup recorded.
