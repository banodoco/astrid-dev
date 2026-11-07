# Consistent generation path

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Plan 02 makes supported generation pick consistent defaults (image, edit, video, voice, music, sound effects), and makes the Agent, Runtime, App, VibeComfy and runpod-lifecycle repositories pin one compatible set of versions that installs on a fresh Linux machine. Users get predictable defaults and clear guidance when no GPU is available. It reuses work that already exists on retained branches and merges it into `pre-main`.

**Not proven here:** a real model producing an image that reaches the gallery. Model downloads, GPU or provider calls, real inference and Foley hardware qualification are outside this plan. The checks use fixtures (a stand-in ComfyUI server) and a CPU-only install. The [first-image onboarding](../20-zero-to-first-image/plan.md) and [multiple inference routes](../12-multiple-inference-routes/plan.md) plans cover real inference.

Status, owner and estimate are in the [catalog](../index.md).

## Execution handoff

[Tasks](tasks.md) own the work and focused proof; [inputs](inputs.md) own actual source identities and retained work. Use the [contributor skill](../../skills/astrid-dev/SKILL.md), then its [Iterate](../../skills/astrid-dev-iterate/SKILL.md) or [Release](../../skills/astrid-dev-release/SKILL.md) specialist as the task requires. Do not infer a model ID or new permission from this plan.

## Prerequisites

- **Authorization:** this plan is `queued`. Start product work only on the owner's explicit go ([Astrid development skill](../../skills/astrid-dev/SKILL.md)). Nothing here authorizes pushing, spending or promotion by itself. To ask for the go, see [How to use this repo](../../README.md#how-to-use-this-repo).
- **Predecessor:** [Plan 01, Installer Consent](../01-installer-consent/plan.md) must be on Agent and App `pre-main` before phase 3. It is not there yet (see [inputs.md](inputs.md)). Phase 1 can start before it.
- **Hardware for the Linux closure check (task V2):** a Linux x86_64 environment: a Linux machine, WSL2 on a Windows PC, or a RunPod CPU pod with at least 40 GB of disk (owner-approved spend). The check installs the pinned Linux recipe (`linux-x86_64-cu130`), so a Mac can't run it. Everything else, including the phase 1 producer tasks, runs on any OS.
- **Access:** push access to the repositories below, or open pull requests for the owner to merge. Producers land only with the owner's go.
- **Tools on the proof machine:** `uv`, `git`, `ffmpeg`, Python 3.13, and network reads to PyPI and GitHub (see [env/README.md](env/README.md)).

## Ready once the owner says go

No predecessor needed:

- P1 land the VibeComfy donor, P2 land the lifecycle donor, P3 land the Runtime stop change. All can run in parallel, on any OS.
- Step 0 items inside later tasks (re-probe merge conflicts, name unnamed selectors) are read-only and can be done any time.

Waiting: everything from phase 3 needs Plan 01 on Agent and App `pre-main` and the phase 1 SHAs. V2 also needs the hardware above.

## Repositories

Base refs are observations from 5 Nov 2026; re-freeze at start ([inputs.md](inputs.md)).

| Repository | URL | Role | Base ref | Retained SHA and where it lives now |
|---|---|---|---|---|
| Agent | https://github.com/banodoco/astrid-agent | Generation, pins, installer; the main integration | `pre-main` | PINS `1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`, DEFAULTS donor `9d3bb24831676cbfc2a0d3dd1c7769f1937569c3`; both on lane branches only |
| VibeComfy | https://github.com/banodoco/VibeComfy | Workflow templates and resources | `main` (no `pre-main`) | donor `1b2e242ce7396442c85395d3220a2481216b57c1`; lane only |
| runpod-lifecycle | https://github.com/banodoco/runpod-lifecycle | RunPod pod lifecycle library | `main` (no `pre-main`) | donor `c47fa76be6e7c0aa661d044a0de5b3b73f6fdbac`; lane only |
| Runtime | https://github.com/banodoco/astrid-runtime | Stop/ownership change that Agent's lock requires | `pre-main` | donor `b005394b06602c84e2abd4ba7eec8fa2f1dd8e94`; lane only |
| App | https://github.com/banodoco/astrid-app | Install manifest; repin only | `pre-main` | no donor |

## The sequence

1. **Land producers.** Put the VibeComfy, lifecycle and Runtime donors on their repository's `main` (Runtime: `pre-main`) so no pin points at a commit that exists only on a lane.
2. **Wait for Plan 01** on Agent and App `pre-main`.
3. **Compose PINS** onto current Agent `pre-main`, then repin Agent to the landed producer SHAs.
4. **Port DEFAULTS** onto that head: merge the donor, make the RunPod dry run resolve each default (D1b), write the CLI-GOLD test (D2) and the installed-package test (D3).
5. **Repin App** to the Agent head (A1), so both heads exist before the review.
6. **Prove once** on that head: the focused checks, the installed-package test and the Linux closure.
7. **Review once**, with one integrated completion review of the Agent and App heads.
8. **Rebase** the reviewed heads onto current `pre-main` (RB1) and rerun only what the move invalidates.
9. **Promote** the rebased commits.

Proof is bound to the final head. Producers land first, Plan 01 is a precondition, and all code (including the new tests) is written before the proof phase, so the composed head is not changed again after it is proven. The only later move is the final rebase, which is re-checked rather than re-reviewed in full.

## Decisions

| # | Decision | Source |
|---|---|---|
| 1 | Drop the unpublished checkpoint `3fe46b90` and the "finish dirty work" framing. DEFAULTS merges donor `9d3bb248` onto the composed head and writes `test_cli_gold_075b.py` as a new file, as the DEFAULTS card says. Neither exists on GitHub. | Coordinator; [DEFAULTS card](inputs.md#not-available) |
| 2 | Foley follows the owner's later decision ("sfx = HunyuanVideo-Foley", "no silent fallback"). The owner named the model, not a template id. DEFAULTS makes the donor's locked template `audio/hunyuan_video_foley` the sound-effects default; `audio/hunyuan_foley_v2a` and the entry `hunyuan-foley-local` stay explicit-only exactly as on `pre-main` (commit `8395174a5`), so `pre-main`'s explicit-only set is unchanged. If Foley is not installed, `auto` fails with guidance and never falls back. Both templates stay in VibeComfy's index. Coordinator's choice implementing the owner's model decision: the locked template is preferred over the hand-written v2a template, whose node inputs are unverified against live `/object_info`. Real-hardware qualification of Foley stays an open gap outside this plan. | Coordinator; [owner decision, 2 Nov 2026](inputs.md#owner-decisions-this-plan-relies-on) |
| 3 | Order: producers, wait for Plan 01, compose, port DEFAULTS, App repin, prove once, review once, final rebase onto current `pre-main`, promote. The App repin comes before the review so the review covers both heads. | Coordinator; owner |
| 4 | The Runtime stop change is unconditional, because the PINS lock already requires it. | Coordinator; `1608dbbf:runtime.lock.json:71` |
| 5 | One review: the retained END review is folded into GEN-REVIEW (here R1), at most five rounds per the run contract. | Coordinator; run contract |
| 6 | Compose (route X) and repin (route N) are separate tasks. | Coordinator |
| 7 | Tasks carry routes N, X or S, never model names; the review uses the run contract's completion-reviewer role. | Coordinator; run contract |
| 8 | The Linux x86_64 closure check runs on Linux, WSL2 on Windows, or a RunPod CPU pod (at least 40 GB disk, owner-approved spend). It installs the pinned Linux recipe, so macOS can't run it. | Coordinator, owner update |
| 9 | The newer plan wins on scope (no real inference), unless a card's stronger check runs wholly on fixtures. Choices below. | Coordinator |
| 10 | INSTALLED-TEST keeps the plan's narrow proof (fresh non-editable install, import origins, CLI inventory, defaults, dry run, fail-closed guidance, the installed-child protocol test). The card's full managed Qwen 512x512 generation through the fixture is not adopted: it never ran, and the earlier audit found managed readiness needs a receipt and three locked model files, so it cannot be shown to need no model bytes. The card itself stops with "model download needed" in that case. | Decision 9; retained INSTALLED-TEST card; [inputs.md](inputs.md) |
| 11 | Base comparison is kept only to classify a failure. The owner approved nine named failures that fail on both base and head (answer A, 3 Nov 2026 17:40Z); only those nine are deselected. Any other failure is checked once against `pre-main` and, if it also fails there, reported to the owner rather than excepted. Nothing else runs on the base. | Decision 9; [owner answer A](inputs.md#owner-decisions-this-plan-relies-on); run contract |
| 12 | The retained QV check is folded into P1: the same VibeComfy selectors run on the donor composed onto `main`, rather than on the old b2123edf base. | Decision 9; retained QV card |
| 13 | The lifecycle donor is `c47fa76` (it contains `96360a27`). Agent `pre-main` pins `96360a27`, so the Agent pin moves forward. | Verified in the lifecycle repository; [inputs.md](inputs.md) |
| 14 | There was no Foley rename. VibeComfy `main` ships only `audio/hunyuan_foley_v2a` (added 1 Nov, `a05864c6`); the donor line separately ships only `audio/hunyuan_video_foley` (added 2 Nov). Merging the donor onto `main` therefore leaves both templates; P1 keeps both in the index, deletes neither, and Agent's default points at `hunyuan_video_foley` (Decision 2). | Verified in VibeComfy history; [inputs.md](inputs.md) |
| 15 | The earlier split into a completion plan and an integration plan is gone; other plans that wait on generation integration point at phases 3 to 8 here. | Coordinator |
| 16 | The new tests are written before the proof phase: D1b (RunPod dry run, the only new behaviour in DEFAULTS) and D3 (installed-package test) join D2 in phase 4, so V1 to V3 only run them and the head does not move during proof. Both are route X. | Coordinator; reviewer |
| 17 | The plan ends with a rebase onto current `pre-main` (RB1) before promotion. A moved target invalidates only the proof that depends on it; a conflict resolution gets a delta review inside R1's existing budget; promotion is by fast-forward and never a force-push. | Owner |

## Plan-specific terms

- **PINS**: the Agent commit `1608dbbf` that pins a compatible version set (VibeComfy, Runtime, node sources, model and requirements locks) and adds the Linux closure test.
- **DEFAULTS**: the Agent donor `9d3bb248` that selects default entries per generation type, plus the new CLI-GOLD test.
- **CLI-GOLD**: `tests/core/generation/test_cli_gold_075b.py`, a test that runs real `python -m astrid generate ...` subprocesses with dry run and checks which default each type resolves to.
- **ENV**: the plan's `env/` folder in the astrid-dev checkout (`<astrid-dev checkout>/plans/02-consistent-generation/env`), where the check scripts live; it is not inside any product checkout.
- **VFIX**: the VibeComfy donor `1b2e242`, which makes an installed VibeComfy find its own templates without a source checkout.
- **QV**: the retained check that VFIX still passes VibeComfy's focused tests against the production base. Here part of P1.
- **K27**: the three lifecycle regression tests (completed-job eviction, capacity reuse, delete and retire) in `tests/test_https.py`.
- **RI-V, RI-L, RI-R**: the selector lists for VibeComfy, lifecycle and Runtime from the retained release-integration cards.
- **Closure**: a fresh CPU install reaching the ComfyUI engine environment stage with every pinned piece resolving, and the node packages importing.
- **K-owned files**: the pin and recipe files PINS owns (`astrid/packs/runpod`, `comfyui`, `vibecomfy`, `engine-index.json`, `runtime.lock.json`); the DEFAULTS merge must leave their bytes as PINS had them. The `comfyui` folder is deleted by [Plan 06](../06-packs/plan.md) (PK-15B, owner decision 5 Nov 2026): keep PINS's bytes here until then, and do not add new work that depends on the `comfyui` engine recipe.
- **Deselect**: tell pytest to skip a named test node (`--deselect`); used only for the nine owner-approved shared failures.
- **Ancestor / ancestry**: commit A is an ancestor of B when B's history contains A (`git merge-base --is-ancestor A B`); used to prove a donor is really inside a candidate.
- **Journey test**: a test that drives a public CLI command end to end (for example `generate image`) and checks the receipt.
- **Step 0**: a lookup to do before a task starts, naming something this plan could not find (see [tasks.md](tasks.md)).
- **CAS, lease**: other Runtime changes (content-addressed storage metadata, an editing lease) kept out of this plan.
- **R1 / P1 / C1 ...**: task IDs in [tasks.md](tasks.md); R1 is the review task, not Release 1.
- **Protocol fixture**: a stand-in ComfyUI server that answers `/prompt`, `/history` and `/view`, so no real model runs.

## Where to read next

| Document | Purpose |
|---|---|
| [tasks.md](tasks.md) | Every task: outcome, route, dependencies, exact commands, done condition. |
| [inputs.md](inputs.md) | Current heads, producer SHAs, what is missing, Installer Consent status. |
| [env/README.md](env/README.md) | Setup and test runner scripts used by the checks. |
