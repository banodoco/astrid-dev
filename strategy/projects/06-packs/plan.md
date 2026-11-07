# Packs v1.3

**Vision gaps:** [Dependable pack lifecycle](../../vision/gaps/F-004-pack-lifecycle.md) (primary). [Supporting gap](../../vision/gaps/LS-003-full-stack-contributions.md).

**Contributing:** [Astrid development skill](../../../skills/astrid-dev/SKILL.md).

Plan 06 moves 19 packs out of Agent core into the `poms_packs` repository, deletes the two comfy packs other than VibeComfy (`comfyui`, `comfy_wrap`; Decision 13), and finishes the pack loading, trust, install, update, rollback and live-editor work that goes with it, across Agent, Runtime and App. Supported workflows keep working, and the result is promoted to `pre-main`. It reuses a large body of work that exists only on retained branches, composes it once onto current `pre-main`, proves it once and reviews it once.

“v1.3” is a working project name, not a confirmed package/release version. Status, owner and estimate are in the [catalog](../index.md).

**Not in this plan:** GPU work, H3 changes, RunPod extraction, training moves, default packs and signing (the owner's CPU-only decision, 3 Nov 2026; the full deferred list is in [inputs.md](inputs.md#already-deferred-never-blocks-a-review-here)). H3, RunPod and training stay in Agent.

## Goal and scope

- **Included:** the 19-pack move to `poms_packs`, the deletion of `comfyui` and `comfy_wrap` (PK-15B), plus the loading, trust, transaction, rendering, Runtime and App work that goes with it (tasks PK-0 to PK-17), and the final review, rebase and promotion.
- **Deferred:** GPU work, H3, RunPod extraction, `training`, default packs and signing; nine of the 30 owner statements ([inputs.md](inputs.md#the-30-statements)).
- **Still undecided:** only the final home of the retired `local` effects (owner to decide). `comfyui` and `comfy_wrap` are deleted (Decision 13); `developer` and `training` stay in Agent (Decision 14).

## Execution handoff

[Tasks](tasks.md) own the work and focused proof; [inputs](inputs.md) own actual source identities and retained work. Use the [contributor skill](../../../skills/astrid-dev/SKILL.md), then its [Iterate](../../../skills/astrid-dev-iterate/SKILL.md) or [Release](../../../skills/astrid-dev-release/SKILL.md) specialist as the task requires. Do not infer a model ID or new permission from this plan.

## Prerequisites

- **Authorization:** this plan is `queued`. Start product work only on the owner's explicit go ([AGENTS.md](../../../AGENTS.md)); none is recorded. Nothing here authorizes pushing, creating a `main`, spending or promotion by itself. To ask for the go, see [How to use this repo](../../../README.md#how-to-use-this-repo).
- **No predecessor.** PK-0 freezes whatever `pre-main` is when the plan starts. It does not wait for [Plan 05](../05-remaining-fixes/plan.md) or any other plan (Decision 1).
- **Tools on the proof machine:** `git`, `uv`, `ffmpeg`, Python 3.13, Node 20 or newer with `npm`, Chromium installed through Playwright (PK-14 and PK-17), and network reads to PyPI, npm and GitHub. Linux or macOS. No GPU, no RunPod, no provider keys.
- **Access:** push access to the repositories below, or pull requests for the owner to merge. Creating `main` in `poms_packs` also needs the owner's go (Decision 6).
- **Check scripts:** the Agent environment scripts in [Plan 02's env folder](../02-consistent-generation/env/README.md) build the test environment and run `pytest` in it. Set `ENV=<astrid-dev checkout>/strategy/projects/02-consistent-generation/env`.

## Ready once the owner says go

Everything starts with the go. After it, these need no predecessor and can run in parallel:

- **PK-0** freeze the bases and probe the merges (read-only apart from creating candidate branches).
- **PK-13** merge the Runtime lane. It depends only on PK-0.
- Step 0 items inside later tasks (re-probe conflicts, name unnamed selectors) are read-only and can be done any time.

Waiting: the Agent line (PK-3 onwards) is one straight chain; App PK-14 waits for PK-13 and the transaction review.

## Repositories

Base refs are observations from 5 Nov 2026; re-freeze at start ([inputs.md](inputs.md)).

| Repository | URL | Role | Base ref | Retained SHA and where it lives now |
|---|---|---|---|---|
| Agent | https://github.com/banodoco/astrid-agent | Packs, loader, transactions, rendering; the main integration | `pre-main` | Chain head `ed04114d`, parks g1 `da05b871`, g2 `dc74ab8b`, g4 `6c70a3a1`, g5 `8ebd78e6` and others; all on lane branches only |
| Runtime | https://github.com/banodoco/astrid-runtime | Admitted pack inventory and assets | `pre-main` | `af0b8917`; lane only |
| App | https://github.com/banodoco/astrid-app | Live effect loading in the editor | `pre-main` | `c1ea16d2`; lane only |
| poms_packs | https://github.com/banodoco/poms_packs | Receives the 19 packs and their tests | none yet | skeleton `80a46912` on its only branch, `lane/M-GPU/packs-M3-10` |

## The sequence

1. **Freeze** (PK-0): record the current `pre-main` of Agent, Runtime and App, the poms_packs base, and all retained inputs.
2. **Compose Agent in one straight line** on that frozen `pre-main`: the retained foundation chain (PK-3), then the parked work (PK-4), then the boundary repair (PK-4R). Everything after is built on top; there is no earlier fork to rebase later.
3. **Finish Agent behavior**: PK-5 to PK-12 (installed CLI, loading, trust, build contract, transactions, rendering, registry, seams). A transaction review (LB-TXN) sits between PK-9 and PK-10.
4. **Runtime and App in parallel**: PK-13 (Runtime) after PK-0; PK-14 (App) after PK-13, PK-9 and LB-TXN.
5. **Move the packs**: PK-15 removes the 19 from Agent; PK-16 lands them in poms_packs and proves each installs.
6. **Delete the two comfy packs** (PK-15B), after PK-15 and PK-14, on the same Agent line (and the stale App contract lines).
7. **Prove once** (PK-17) on the final heads: the installed CPU journey and the statement mapping.
8. **Review once** (END): one integrated completion review of all candidate heads.
9. **Rebase** the reviewed heads onto current destinations (RB1), rerunning only what the move invalidates.
10. **Promote** by fast-forward or create (PK-PREMAIN).

Proof is bound to the final head. Fixes found during review go forward on the final head and rerun the affected checks; there is no downward cascade to earlier tasks.

## What we build on

| Existing input | How we use it |
|---|---|
| Foundation chain `ed04114d` (namespace, schema, installed Hivemind, boundary guard) | Merge once as PK-3. It is the only source of the working `--check` guard. |
| Four parks (g1, g2, g4, g5) and four loose lanes | Merge once as PK-4. Park g3 and M3-04 fix2 are excluded. |
| Health fold `47d67d8d` (closes Plan 05's SF-AGENT-FOLD) | PK-6 takes it and records exact inclusion or equivalence. |
| Runtime `af0b8917`, App `c1ea16d2` | PK-13 and PK-14. |
| poms_packs skeleton `80a46912` | PK-16 builds on it. |

## Decisions

| # | Decision | Source |
|---|---|---|
| 1 | The core-to-pack fold belongs wholly to Plan 06 (PK-6). Plan 05 completes at its own promotion and records "fold transferred to Plan 06 PK-6". PK-0 freezes current `pre-main` when this plan starts and does not wait for Plan 05. | Coordinator; [Plan 05](../05-remaining-fixes/plan.md) |
| 2 | One straight line on current `pre-main`: PK-0 freezes it; the retained chain, parks and the boundary repair are composed straight onto it. The old "fork, then rebase" task (PK-1) is dropped, and the branch-publication task is merged into the promotion task. Fixes during review go forward on the final head. | Coordinator |
| 3 | The plan ends with RB1 before promotion, as in [Plan 02](../02-consistent-generation/plan.md): re-freeze each destination, rebase the reviewed candidates, rerun only checks whose inputs changed and record why the rest carries forward, resolve conflicts with a delta check by the completion reviewer inside the same budget, promote by fast-forward, never force-push. | Coordinator; Plan 02 |
| 4 | Wan2GP stays a pack. Pre-main ships `astrid/packs/wan2gp` and Plan 12 makes Wan2GP a pack; it is newer than the retained removal. PK-4 does not take `a7bf7e2b` (its one change is a test line; a merge would bring the removal commit `03531e466` with it), and the "zero wan2gp hits" check is dropped. It replaces it with a check that `astrid/packs/wan2gp` still exists. | Coordinator; [Plan 12](../12-multiple-inference-routes/plan.md); [inputs.md](inputs.md) |
| 5 | The retained cards are inlined: every task has its real selectors, plain git and pytest commands, inputs, merges, exclusions and a done condition. No cards folder is published. PK-16 runs `tests/integration/test_install_each_pack.py` (a new file PK-16 writes in poms_packs). PK-4R is done when `scripts/check_core_pack_boundary.py --check` passes and `python -m astrid timelines --help` still works. The retained "recover at setup" step and PK-4's local-only evidence are dropped. | Coordinator; [inputs.md](inputs.md) |
| 6 | poms_packs has no `main`. PK-PREMAIN creates `main` from the reviewed head, with the owner's go. If the owner prefers a pull request, create `main` at the skeleton `80a46912` first and open the pull request from the reviewed head. | Coordinator; owner's go |
| 7 | PIN files are written by the installer into installed copies and never committed. The poms README (1 Nov 2026) and the retained PK-16 card (3 Nov 2026) agree on this once read together; the README wording is corrected in PK-16. | [inputs.md](inputs.md#pin-files) |
| 8 | Pack inventory: the 19 move, the four core packs stay, runpod and h3_av come later, training stays, `comfyui` and `comfy_wrap` are deleted (Decision 13). Every other folder has a disposition in [inputs.md](inputs.md#pack-inventory-on-agent-pre-main). `local` is retired by PK-12 because the owner stopped shipping the 15 personal effects (E10) and the retained PK-12 card deletes it; the final home of the bytes is the owner's. | Owner (1 Nov 2026); retained cards |
| 9 | Tasks carry routes N, X or S, never model names. Reviews use the run contract's completion-reviewer role. The transaction review (LB-TXN) is capped at 2 rounds and the final review (END) at 3, then the owner decides. These are owner caps (3 Nov 2026) and override the default of 5. | Coordinator; owner |
| 10 | Status stays `queued`. The retained "owner-paused; do not resume" refers to the stopped M-GPU run; this plan restarts from current `pre-main` on the owner's go. | Coordinator |
| 11 | The end state is stated as the short list below. The retained "30 CPU-provable statements" is corrected: the hand-off has 30 statements in three groups, 9 of them deferred by the owner's CPU-only decision. PK-17 maps all 30 and names the 9 deferred. | Coordinator; [inputs.md](inputs.md#the-30-statements) |
| 12 | Conflicts in the generated pin, recipe and engine-index files are resolved to the `pre-main` side; locks are regenerated, never hand-merged. The three core-to-pack imports at `core/generation/listing.py:15` and `core/timeline/snapshot.py:22,28` import core packs (`vibecomfy`, `rendering`); PK-15 removes the imports of the 19 moved packs first and leaves those three unless the guard reports them. | Coordinator; Agent `pre-main` |
| 13 | **Delete `astrid/packs/comfyui` and `astrid/packs/comfy_wrap` from Agent; `vibecomfy` stays a core pack.** Basis for the task (PK-15B, from the pre-main `23174f32` census): `comfy_wrap` is one action, `comfy_wrap.run`, which only injects `--prompt` into a workflow and calls VibeComfy; `vibecomfy.run <workflow> --workflow-inputs '{"prompt": ...}' --out` does the same and more, so users lose only the `comfy_wrap.run` name and its prompt-only shorthand. `comfyui` is not a pack (no `pack.yaml`): it is the Linux x86_64 cu130 managed-ComfyUI engine recipe (pins, models lock, requirements lock) that `engine-index.json` serves to engine `comfyui`; the Windows engine (`vibecomfy` recipe), the RunPod recipe (`vibecomfy-h3`, in `runpod`) and Wan2GP are separate files and stay. What users lose: the Astrid-managed Linux ComfyUI install recipe; a Linux user brings their own ComfyUI through VibeComfy (the `vibecomfy` skill). The hand-off proposed the same for `comfy_wrap` ("nothing calls it") and moving `comfyui` into core; the owner chose deletion for both, and its manifest said to repeat the caller census first, which PK-15B does. | Owner (5 Nov 2026); [inputs.md](inputs.md#pack-inventory-on-agent-pre-main) |
| 14 | `training` stays in Agent as it is, grouped with `runpod` and `h3_av` (the GPU-era packs). It is not a core pack and cannot be one: core names it today (`core/execution/generic_host.py:4160` and the `_training_review_*` helpers at `3936-4151`, `core/generation/availability.json:11-13`, `core/contracts/output_result_exemptions.json`, `core/execution/capability_ledger.py:154-156,191`, `core/pack/validate_first_party.py:45`), it hard-codes the `runpod` pack (`actions/training_run/compute_backends.py:210-213`) and the moved `editorial` pack uses its `pool_build` and `pool_merge`. Moving it needs the K census and the RunPod work, both deferred; those core names are existing guard-baseline findings that this plan neither adds nor removes (E3 stays partial). `developer` stays in Agent as it is: it is a skill-only pack (`pack.yaml` without actions; three `SKILL.md` documents) installed by `astrid skills sync --developer` (`astrid/skills/cli.py:144`); core names it only in the first-party id list (`core/pack/validate_first_party.py:28`); one test (`tests/test_skills_developer.py`); no other pack uses it. Moving it would break that flag for no gain, deleting it would drop the developer skills. `_core` is docs only and stays. These are coordinator decisions from the pre-main census; the owner may override. | Coordinator; Agent `pre-main` `23174f32` |

## Completion

- Core knows the four core packs (`vibecomfy`, `generation`, `rendering`, `timeline`) and Hivemind; **packs may use core, core never names a moved pack.**
- The 19 packs are absent from Agent and present in poms_packs; each installs with `packs add` and passes its own tests.
- Deleting a pack's folder removes it from discovery; dependents report why they are unavailable.
- Install is the trust moment: origin labelled, pin checked, receipts record the fingerprint, declared secrets only, personal pack created empty and never shipped.
- A pack's effect appears in the open editor live; a failed update keeps the old effect; disabling removes it; opening a project is passive.
- Locks are regenerated once; the boundary guard passes and only shrinks.
- `runpod` and `h3_av` stay in Agent until a later plan moves them; `training` and `developer` stay; `wan2gp` stays a pack.
- `astrid/packs/comfyui` and `astrid/packs/comfy_wrap` are absent from Agent, nothing names them (App included), and `vibecomfy` still runs a workflow with a prompt.
- Deferred, by name: statements E1 (defaults), E3 (part), E4 (internal access), E5, E6, N6, N8, N9, X7.

## Estimate

The README keeps **TBD**. The only retained figure (16 to 20 working days, 1 Nov 2026) was for a larger scope that included H3 and GPU work and a four-manager plan, and the work since then has been restructured; it does not carry over. The first honest number comes after PK-3 and PK-4: those tasks decide how much of the 28 to 89 commits per branch composes cleanly onto a `pre-main` that is about 399 commits ahead of their fork. Record the measured figure in the README queue then.

## Plan-specific terms

- **Chain head**: Agent `ed04114d`, the retained foundation (namespace, schema, installed Hivemind, boundary guard). It contains `c08c38ea`, `c02386e5` and `04e74695`.
- **Park**: a retained feature branch (g1 to g5); g3 is excluded.
- **Core pack**: a pack that stays in Agent core: `vibecomfy`, `generation`, `rendering`, `timeline`.
- **Boundary guard**: `scripts/check_core_pack_boundary.py`, a shrink-only check that finds core code naming packs. `--check` fails if findings grow past the recorded baseline.
- **Baseline**: `scripts/reshape/baselines/core_pack_boundary.json`, the guard's recorded findings; it may only shrink.
- **PIN**: a one-line JSON file the installer writes at an installed pack's root (source, commit, digest, origin). Never committed.
- **Transaction**: the install, update, rollback and removal exchange for a pack (validate, build, swap).
- **Admission**: Runtime recording that an installed pack's inventory and assets are accepted.
- **Selected source**: the pack root chosen for a run; resources and imports resolve only from it.
- **Passive open**: opening a project never installs, fetches or runs a pack.
- **LB-TXN**: the review of the build-hook and transaction diffs (PK-8 and PK-9) before anything builds on them. **END**: the final integrated review.
- **Hivemind**: the shared-knowledge pack that ships in core.
- **Fold**: a retained commit whose whole change is taken once (here the Agent health fold `47d67d8d`, Plan 05's SF-AGENT-FOLD).
- **Personal pack**: the per-user pack folder the installer creates empty; it is never shipped, published or overwritten.
- **Receipt, fingerprint**: the record of a run; the fingerprint is the pack source digest it actually ran.
- **CAS, lease**: Runtime storage and editing-lease changes kept out of this plan (the Runtime CAS commit must not become an ancestor).
- **K census, K A6**: retained GPU-side work items the owner deferred (the `training` move and H3 placement).
- **Hand-off package**: the retained M-GPU cards, statements and evidence. Not in this repository; [inputs.md](inputs.md) copies what tasks need. Labels like M1-13, fix2 or r3 name lanes inside it.
- **Staged bytes, crash point**: the pack bytes prepared for an install or update, and any moment a failure could stop it midway (the old state must survive each one).
- **Step 0**: a lookup to do before a task starts, naming something this plan could not find (see [tasks.md](tasks.md)).
- **Ancestry**: commit A is an ancestor of B when B's history contains A (`git merge-base --is-ancestor A B`).
- **RB1, PK-PREMAIN**: the final rebase and the promotion; see [tasks.md](tasks.md).

## Read next

| Document | Purpose |
|---|---|
| [tasks.md](tasks.md) | Every task: route, dependencies, exact commands, done condition. |
| [inputs.md](inputs.md) | Current heads, retained SHAs, what is missing, pack inventory, the 30 statements, owner decisions. |
| [Plan 02 env folder](../02-consistent-generation/env/README.md) | The Agent test-environment scripts. |
