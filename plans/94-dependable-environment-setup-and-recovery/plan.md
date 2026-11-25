# Dependable environment setup and recovery

**Project:** Dependable environment setup and recovery

**Goal:** A creator's agent can safely prepare or recover a compatible creative execution environment on a supported machine, reusing what works and resolving what does not, then make a real creation through Astrid without improvised setup work.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD — baseline recovery walk, inventory existing Windows recipe/adapter and select the smallest provisioning route before estimating; phase the work if needed.

**Waiting on:** Independent critique and owner decisions; [Plan 93](../93-comfyui-desktop-and-existing-environments/plan.md)'s existing-target outcome for the final loop; Release 16 start, matching qualified build and consented Windows GPU proof. Coordinate with Plans 09/29/30/38, 56 and 90 without assuming unlanded work.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [Platform reliability](../../vision/gaps/F-001-platform-reliability.md), [Portable generation](../../vision/gaps/F-008-portable-generation.md) and [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Outcome and scope

The setup skill is an application of a durable product capability, not a second installer or generation implementation. Use Plan 93 for existing user-owned ComfyUI and this plan for machines that have no usable target or encounter a recoverable environment-level failure. Windows NVIDIA is the first proving ground; state the actual OS/GPU/layout support matrix, not universal compatibility.

### Ten end-state statements (combined with Plan 93)

1. **An artist can go from a fresh computer to their first creation without knowing what CUDA, Python or a virtual environment is.**
2. **ComfyUI Desktop is a first-class supported environment, not a special case the agent must figure out for itself.**
3. **Astrid finds and reuses what already works before installing anything new.**
4. **A broken installation becomes a diagnosable and recoverable state, rather than a dead end.**
5. **Seeing a GPU is not enough; Astrid verifies that the selected environment can actually use it.**
6. **Desktop, Portable, Pinokio and managed ComfyUI use the same generation path, regardless of how they were installed.**
7. **A failed or interrupted setup resumes from verified completed work rather than starting over.**
8. **Astrid never silently replaces a person's environment, modifies unrelated assets or spends their money.**
9. **The agent uses Astrid's shared capabilities instead of inventing installation scripts and independently researching common setup problems.**
10. **The proof of readiness is a real creative result that the person can open and use in Astrid, not a successful installation or a healthy process.**

These apply to declared supported combinations; an unsupported, unrepairable or refused case ends truthfully with the reason and alternatives. #2 and reuse/attachment in #3/#6 consume Plan 93; the managed/Pinokio claim is about the common execution path where supported, not a promise that every provisioning route is already qualified.

Included:

- Use the existing scan/target/placement and authoritative capability facts. Distinguish healthy Astrid, compatible editor, usable target, workflow readiness and actual GPU execution. Preserve one owner for each fact. Do not make `doctor` falsely mean all workflows are ready.
- Where no usable existing environment exists, offer one supported local provisioning route, with exact source, destination, disk needs, ownership and consent. Evaluate official Portable or completing the existing Windows managed recipe/adapter first; select one minimum complete route after inventory rather than implement both. No edits to unrelated Python/ComfyUI, silent driver changes or destructive repair. Test a small real CUDA operation in the selected environment, then an actual generation.
- Reuse the existing digest-bound model plan and resumable verified fetch, Plan 56's actionable workflow fixes and Plan 90's exact workflow plan if landed. Preserve completed bytes, verify sizes/digests, report progress and truthful cancellation/next steps. Do not create another downloader or second consent store. New Runtime download task only if the live loop demonstrates need and owner resolves #722's remaining decision.
- Wire recovery into the existing setup/generation skills and editor guidance; use the actual matching editor/install tuple. Fix invalid update advice and installer progress at their owning boundary with Plans 09/29/30/31; don't duplicate lifecycle policy. A Lead-approved tester bundle is a release deliverable, not a new product release mechanism.
- Run real user journeys and repair the smallest root causes, using Plan 34's GPU proof and Plan 93's Desktop witness. Capture end-to-end timings, downloads and workarounds. Reproduce or disprove #1848's zero-duration receipts at the receipt owner, and its 219-second installer silence at the installer owner; require truthful progress and telemetry, not a new performance architecture. Send remaining speed to Plans 81/82/92 and measurement work to Plan 85.

Not included: a new engine, generic package manager, mandatory rewrite of all installer routes, arbitrary third-party repair, replacing Desktop as a proof of Desktop support, all modalities on all hardware, implementing Plan 90's entire workflow approval design, or silently expanding paid compute. Do not close F-003/F-001/F-008 from one successful row.

## Existing work and decision

In the Nov 24 [exploratory Windows report #1848](https://github.com/banodoco/astrid-dev/issues/1848), the tester used the specifically scoped exploratory Release 15 snapshot, installed a healthy Runtime and generated two local images. The existing Desktop was broken; the agent provisioned isolated Portable, chose compatible CUDA, staged 17.28 GB using an external downloader, and could not connect the older published editor. Astrid's model planning and verification passed, built-in model transfer/resume was skipped, and the matching unpublished R15 editor was not tested. Plan 20's actual scope deliberately excluded stopped/Desktop adoption. There is existing Windows ComfyUI recipe and candidate NVIDIA environment code; the engine runner explicitly lacks the Windows A7 adapter, the endpoint root check is POSIX-only, and the current probe checks availability rather than a real computation. Existing attached download code already resumes and verifies; the external downloader incident is not proof Astrid's implementation failed. Plan 32 owns execution, not new local provisioning; Plan 56/90 own workflow requirements, not machine repair.

[Inputs](inputs.md#planning-evidence) records pinned code, options, owner release request and unresolved critique. The proposal chooses reuse, one fallback route, and a live loop rather than a large invented orchestration layer. The owner requested Release 16 inclusion, not an implementation go.

## Sequence and readiness

First reconcile Plan 20 evidence and independently trace existing engine/GPU, installer and approval surfaces. Freeze the scenario set, supported matrix and smallest local provisioning decision. Use Plan 93's verified existing-target handoff; independent source inventory may proceed alongside it. Reuse existing lifecycle and workflow work as it lands, resolving actual shared functions/contracts before dispatch. Run the [live-loop workstream](../../agent/roles/manager/live-loop.md) on an approved matching installed stack: record a round, get strategist advice, fix root causes at owners, rebuild, rerun. Two consecutive satisfying live rounds or a recorded stop requiring owner judgment. [Tasks](tasks.md) remains draft until critique, actual task scopes, bases and authorization.

## Interfaces and handoff

Consumes Plan 93's target identity/readiness and Plan 20's existing entrypoints; Plan 32's requirements/placement/run/retrieve; existing engine recipe/runner, model fetch and verified download; Plan 56 and, when scheduled/landed, Plan 90 workflow fixes; Plans 09/29/30/31/38 lifecycle identity/approval and release qualification. Record the exact accepted product revisions; no new preference or authority store.

Produces a supported prepared target and explicit readiness/refusal for the same generation path, a working updated setup journey, exact installed-tuple live-round evidence and narrowly scoped fix PRs. Reconcile Plan 20's missing completion evidence rather than redo its shipped work. The completed target and scenario proof can feed Release 17 stable qualification, not replace its whole matrix.

## Completion

A reasonably capable external coding agent, given only the maintained Astrid instructions and a creative intention, uses product commands and supported third-party actions to get a clean supported Windows NVIDIA machine and a previously broken/stopped setup to a real image in the matching editor, then repeats it. Plan 93 separately proves Desktop itself; Portable-only evidence cannot satisfy that. Record exact versions, GPU computation proof, admission and usable-output times, setup time, bytes transferred/reused, permission steps and unscripted workaround count (zero in supported successful cases). A controlled interrupted transfer resumes, a disk shortage is diagnosed before writing, incompatible CUDA is correctly identified, a user denial leaves state unchanged, an older editor never recommends an impossible downgrade, and unsupported hardware offers truthful alternatives. Use generated/sandbox project data; retain original files and cleanup proof. Two consecutive passing live rounds plus focused regression tests and final independent review, with declared evidence limits; no live spend or machine mutation without separate permission.
