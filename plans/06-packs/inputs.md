# Inputs and provenance

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

[Plan](plan.md) · [Tasks](tasks.md)

## Re-freeze rule

Every SHA below is an observation from 5 Nov 2026, not a presumed current ref. At the start of each task, record the actual branch and SHA of its base and donors. If a recorded value and the live repository disagree, the live repository wins for branch heads; this file wins for the identity of retained donors. If a destination moves after proof, reconcile and rerun only the affected checks ([run contract](../../skills/astrid-dev-shared/run-contract.md#checks-and-failure-repair)).

## Status of the retained run

The retained manifest from the earlier M-GPU run says its packs project is "owner-paused; do not resume". That refers to the stopped M-GPU run, whose lanes, cards and runner are not continued. This plan is a new run: it restarts from current `pre-main` on the owner's go (ask as described in [How to use this repo](../../README.md#how-to-use-this-repo)). No go is recorded: the retained answer file has no go line.

## Current heads (5 Nov 2026)

| Repository | Branch | SHA | Note |
|---|---|---|---|
| Agent | `pre-main` | `23174f32561a2ede6af95a07515ba3f15e43c73e` | Ships 34 folders under `astrid/packs/` (see the inventory below). |
| Runtime | `pre-main` | `9fc53b771134940aaac901e4cfc5d03c1db1a20a` | |
| App | `pre-main` | `878c28df7a6c80fa9aaa6540c5fccad95473e7c1` | |
| poms_packs | `lane/M-GPU/packs-M3-10` | `80a469129e998ffdd7f58f15aad72cb5417dfa25` | Its only branch. There is no `main`. It holds `.gitignore`, `README.md` and a placeholder `.github/workflows/ci.yml` (runs no tests). No pack folders. |

## What we build on

The starting heads, the retained Agent, Runtime and App work, and the poms_packs skeleton are listed below; the pack inventory, statements and owner decisions follow. Each retained input is a donor to compose, not a base.

## For projects that change code: retained Agent work (all lane-only, none on `pre-main`)

All of it forks from an Agent `pre-main` of 2 Nov 2026 (`75154776`). Against the Agent head above it is about 399 commits behind. Neither the chain nor the parks is an ancestor of `pre-main` or `main`.

| Name | SHA | Ahead of its fork | What it is |
|---|---|---|---|
| Namespace preparation | `c08c38eade92f0b3241b02a575e0c9889e89b1c3` | 6 | Hidden-name clash fix (retained PK-1-NAMESPACE). Inside the chain head. |
| Schema preparation | `c02386e56ceb039448e699d346482bc12348d032` | 6 | Render `SCHEMA_VERSION` origin fix (PK-1-SCHEMA). Inside the chain head. |
| Installed core Hivemind | `04e74695a6cded0139ba31b20ce59a81ee91d564` | 20 | Retained PK-2. |
| Boundary guard (the **chain head**) | `ed04114d255bfec53b5fda1d768530fe5b848da1` | 24 | Retained PK-3; contains the three above. The only ref where `scripts/check_core_pack_boundary.py` accepts `--check`. |
| Park g1 | `da05b8718d9347484a18eb5970fbcf1d9989ebf9` | 32 | Branch `lane/M-GPU/park/packs-agent-g1`. |
| Park g2 | `dc74ab8bf12fabdfcf0a8eaa45a665a646edd0ae` | 50 | `.../park/packs-agent-g2`. |
| Park g3 | `3ebd0d9ee73c98d646103dddfea5852af2e2d3f6` | 36 | `.../park/packs-agent-g3`. **Excluded wholesale.** |
| Park g4 | `6c70a3a1abf868dabae3a3ed8edd73b025934d73` | 89 | `.../park/packs-agent-g4`. |
| Park g5 | `8ebd78e6f6261aeef0fe5c59370350f5a5cfa63b` | 43 | `.../park/packs-agent-g5`. |
| M3-04 fix2 | `ef54c2b8f0a8bba44389e6d35af724f47960d4b6` | 23 | **Excluded** (needs GPU work, deferred). |
| Health fold | `47d67d8d13bcbf4ab437bc41ae6ec5b6cf60598b` | 29 | Only on `lane/M-GPU/proj/test-health-agent`. Closed by PK-6 (see below). |
| M4-07 | `7f9d49f8e7b661e954b575eb040559aee2ff272a` | 9 | Merged by PK-4. |
| M4-11 r3 | `e0d5668290bcddd6309925e960f0de5d6638b9a1` | 23 | Merged by PK-4. |
| M1-13 r3 | `00fdda383b52cc083b10394ddaf4ef6d2cde9e9a` | 25 | Merged by PK-4. |
| M1-05a follow-up | `ca370d21a3f4488ac075394bde2d130a59de61e8` | 55 | Merged by PK-9. |
| M1-07a | `68ccd90e15517cd2173275849bbde63fdfc5ee97` | 43 | Merged by PK-9. |
| M1-07a-x | `fa23dbd75a3403eadeda284f830654e491d79150` | 14 | Merged by PK-9. |
| Reference only | `4cf47a6a440580119ab3eee6ab828b149604e918` | 26 | M3-13 r6. Read-only; must **never** be an ancestor of any candidate. |
| Deferred | `6b4e867cbf409956c27663beaebd65fb981266cb` | | M3-04; must **never** be an ancestor of any candidate. |
| M2-11W receipt | `a7bf7e2b01b8583833c5bd5ce617de43a7796dcd` | 28 | **Not taken** (see Decision 4). The commit itself only changes one test line; the Wan2GP removal is the earlier commit `03531e466`, which a merge of `a7bf7e2b` would bring along. |

Runtime and App retained work: Runtime `af0b8917078ea0b3e5144298c1388744eb62bb5c` (28 ahead of its fork, 734 behind the Runtime head above; lane `packs-M4-09d-runtime`); App `c1ea16d2919d3af9f0f22cf8dea85b4856317c1f` (9 ahead, 1280 behind; `park/packs-app`). Runtime CAS `103f97803f7f391e2c810ebdf086f798326cd75a` must **never** be an ancestor of the Runtime candidate.

Merge probes the reviewer ran individually against an Agent `pre-main` of 4 to 5 Nov 2026 (re-probe at PK-0; conflicts compound when inputs are merged in sequence):

| Input | Conflicting paths |
|---|---|
| Chain head `ed04114d`, and park g1 `da05b871` | Nine each: `astrid/packs/engine-index.json`, `runpod/pins.json`, `runpod/recipe.linux-cu130.json`, `vibecomfy/environment.windows-nvidia.json`, `vibecomfy/pins.json`, `vibecomfy/recipe.linux-cu130.json`, `vibecomfy/recipe.windows-cu130.json`, `pyproject.toml`, `tests/core/generation/test_engine_recipe.py` |
| Parks g2, g4, g5; M4-07; M4-11 r3; M1-13 r3; M1-05a follow-up; M1-07a; M1-07a-x | None individually |
| Runtime `af0b8917` | Six: `runtime_protocol/cli.py`, `daemon.py`, `local_execution_supervisor.py`, `local_worker_composition.py`, `service.py`, `store.py` |
| App `c1ea16d2` | One: `src/tools/video-editor/contexts/VideoEditorProvider.test.tsx` |

The pin, recipe and engine-index files are generated and owned by the generation work ([Plan 02](../02-consistent-generation/plan.md)); the task rule is in [tasks.md](tasks.md#shared-rules).

## What is not available

- **The retained cards, runner, evidence and `RESULT.json` files** are not in this repository. Everything a task needs from them is written into [tasks.md](tasks.md). Cards are evidence for what to do, not instructions to run. Their helper scripts (`head.sh`, `base.sh`, `agent-setup.sh`, `baseline-shrinks.sh`) are not used; tasks give plain git and pytest commands instead.
- **PK-4's earlier failure evidence** (a staged repair, scanner output and a result file) exists only locally and is not relied on. The failure is reproduced from public refs in PK-4R.
- **Branches that no longer exist:** `lane/M-GPU/integrated`, `lane/M-GPU/packs-integrated` and `packs-M3-13a-r2-hold`. Do not look for them.
- **`tests/integration/test_install_each_pack.py`** exists on no Agent ref. It is a new file PK-16 writes in poms_packs.
- **A `packs add` command** does not exist on Agent `pre-main` or the chain head (the pack command-line is `python3 -m astrid.core.pack.cli`, with `list`, `inspect`, `validate`, `new`, `status`, `agent-index` and `search`). It does exist on retained refs: `add` and `remove` are defined in `astrid/core/pack/cli_manage.py` (`build_add_parser`, parser registered at `cli_parser.py:61`) at M1-05a follow-up `ca370d21` (merged by PK-9) and in park g4 `6c70a3a1` (merged by PK-4); `update` and `rollback` are in `cli_parser.py` at `ca370d21` (lines 64 and 76). `fa23dbd7` (M1-07a-x) lacks all four, so its merge must not remove them (PK-9 step 3 checks).
- **Two retained selector sets** are lists in the hand-off package, not in this repository. Their test files are named in [PK-4](tasks.md#pk-4-merge-the-parked-work), [PK-6](tasks.md#pk-6-loading-and-discovery) and [PK-11](tasks.md#pk-11-registry-and-selected-sources) at file level.
- **Transaction test node names** (PK-9): `tests/core/pack/test_transaction_integrity.py` exists on no ref. The nodes the plan needs are mostly in `tests/core/pack/test_transaction.py` and `test_cli_manage.py` at `ca370d21`; PK-9 lists them. Two are missing everywhere (PIN-only exchange, equal-byte exchange); PK-9 writes those.
- **The "an installed pack effect renders live" Playwright spec** exists in neither App `c1ea16d2` nor `pre-main`; PK-14 writes it.
- **The PK-5 "generators"** are `scripts/gen_capability_index.py` and `scripts/gen_tool_catalog.py`; no skills generator script exists, so that leg is dropped.
- **The PK-3 ffmpeg node** is `test_ffmpeg_review_rejects_in_support_before_render` in `tests/packs/rendering/test_render_facade.py` (line 352 on `ed04114d`, 338 on `pre-main`).

## Pack inventory on Agent `pre-main`

34 folders. The end state is the hand-off's disposition (`PACKS-END-STATE`, 1 and 3 Nov 2026) with the owner's later cuts. Where only a hand-off proposal exists, the pack stays in Agent and the owner decides.

| Pack folder(s) | Disposition | Basis |
|---|---|---|
| `blender`, `capture`, `foley`, `media`, `moirae`, `discord_local`, `seedance_local`, `youtube`, `chiptune`, `music`, `editorial`, `iteration`, `stream_content`, `video_editing`, `astrid_motion`, `fal`, `pixel`, `typed_timeline`, `understanding` (19) | **Move to poms_packs** (PK-15, PK-16) | Retained PK-15 card; owner scope "CPU only" (3 Nov 2026) |
| `vibecomfy`, `generation`, `rendering`, `timeline` | **Core packs**, stay in Agent | Owner statement 1 (1 Nov 2026) |
| `runpod`, `h3_av` | **Stay in Agent in this plan**; they come to poms_packs later | Owner statements 1 and N9 (1 Nov 2026); GPU work deferred (3 Nov 2026) |
| `training` | **Stays in Agent** next to `runpod` and `h3_av`; core names it and it hard-codes `runpod`, so it cannot be a core pack, and its move needs the K census | Retained END card; Decision 14 (code evidence) |
| `local` | **Retired by PK-12** after its 15 personal effects stop shipping; the bytes stay in git history and `docs/packs/local-effects-archive.md` lists them with checksums. Their final home is the owner's to decide | Owner statement E10 (1 Nov 2026) and the retained PK-12 card; final home owner-held in the END card |
| `wan2gp` | **Stays a pack in Agent** | Decision 4 below; [Plan 12](../12-multiple-inference-routes/plan.md) makes Wan2GP a pack and is newer |
| `shots`, `references` | Their command-line files move into core (PK-5); the folders hold no storage. | Retained PK-5 card; hand-off end state |
| `comfyui` | **Deleted by PK-15B.** Not a pack (no `pack.yaml`): five files of Linux managed-ComfyUI engine data served by `astrid/packs/engine-index.json:7-9` | Owner decision, 5 Nov 2026 (Decision 13); the hand-off proposed moving it into core (`PACKS-END-STATE.md:66`, `MOVE-MANIFEST.md:21`) |
| `comfy_wrap` | **Deleted by PK-15B.** One action `comfy_wrap.run`; `vibecomfy.run` covers it | Owner decision, 5 Nov 2026 (Decision 13); the hand-off proposed deletion (`PACKS-END-STATE.md:67,79`) |
| `developer` | **Stays in Agent as it is.** Skill-only pack behind `astrid skills sync --developer` | Coordinator decision (Decision 14); retained PK-15 card also keeps it |
| `_core` | Docs only (no `pack.yaml`); **stays in Agent**, listed in PK-5's resource check | Retained PK-5 card |

## The 30 statements

The hand-off lists 30 statements the owner agreed with on 1 Nov 2026 (21:45Z), in three groups of ten: **E** (what it looks like when it is done), **N** (what we are not doing) and **X** (how we execute). It is not a list of 30 CPU-provable end states and is not 30 tasks. The owner's 3 Nov 2026 decision (CPU only) defers nine of them, fully or in part.

| ID | Statement | In this plan |
|---|---|---|
| E1 | Fresh install is core, Hivemind, the four core packs, plus runpod and h3_av as defaults | Core and Hivemind part proven; defaults deferred |
| E2 | Every other pack is a visible folder; deleting it removes it cleanly | Proven (PK-6, PK-17) |
| E3 | Core names no non-core pack; core tests run with zero optional packs | Partly proven (PK-15); H3 and RunPod names stay |
| E4 | One versioned pack interface; runpod and h3_av internal access retired | Interface proven (PK-7); internal retirement deferred |
| E5 | H3 is one ordinary task | **Deferred** (GPU) |
| E6 | Local generation never touches RunPod | **Deferred** (GPU) |
| E7 | A new pack's effect appears in the open editor without rebuild or reload; disable removes it live | Proven (PK-14, PK-17) |
| E8 | Install is the trust moment; pin checked, origin labelled, run records the fingerprint | Proven (PK-7, PK-9) |
| E9 | Secrets go only to actions that declare them | Proven (PK-7); RunPod key path deferred |
| E10 | Personal pack is created empty and never shipped or overwritten; old 15 effects stop shipping | Proven (PK-9, PK-12) |
| N1-N5, N7, N10 | No three.js pack yet, no marketplace, no dependency solver, no per-pack environment, no sandbox for pack code, no `generic_host` rewrite, nothing without the owner's go | Absence checked at END |
| N6 | No per-pack signing; auto-update stays off until tampered manifests are proven rejected | **Deferred** |
| N8 | No staged jobs and no stage driver | **Deferred** (H3) |
| N9 | No runpod extraction now | **Deferred** |
| X1-X6, X8, X10 | Contracts first, few managers, route by difficulty, one writer per shared file, prove then estimate, guard only shrinks, no fakes at the boundary, rough estimate | Follow from the task order; X6 and X8 checked at PK-17 |
| X7 | H3 rewrite measured against a baseline | **Deferred** |
| X9 | Stream K and the custody fix land first | Not a precondition: the plan freezes whatever `pre-main` is at PK-0 and does not wait for Plan 05 (Decision 1) |

That is 21 statements the plan maps to evidence and 9 it names as deferred with the reason above. Source: the retained statements file and the END card's deferred list. PK-17 writes the final mapping.

## Owner decisions this plan relies on

| Date | Decision | Source |
|---|---|---|
| 1 Nov 2026, 21:45Z | The 30 statements above; "nothing without the owner's go"; the old 15 personal effects stop shipping to everyone | Retained statements file |
| 2 Nov 2026, 13:30Z | "VibeComfy (ComfyUI) is the ONLY inference framework for now. Others come later. Wan2GP is parked." Superseded for packs by Plan 12 (Wan2GP is a pack) | Retained directive |
| 3 Nov 2026, 13:34Z and 16:00Z | "NO LIVE GPU RUNS in this phase"; "No GPU work of any kind in this phase" | Retained directive |
| 3 Nov 2026, 20:05Z | Packs is CPU only, up to migrating the built-in features to the pack format; the GPU half (H3 out of core, h3_av and runpod defaults, K A6) stays deferred; it waits on the owner's go | Retained directive |
| 3 Nov 2026 | Review rounds: the transaction review (LB-TXN) stops after **2** rounds and the final review (END) after **3**, then the owner decides. These override the run contract's default of 5. The owner's own range was 1 to 5 rounds "set by project complexity and risk"; the numbers 2 and 3 are the retained cards' choice inside it | Retained directive and cards |
| 5 Nov 2026 | Delete the comfy packs other than VibeComfy: Agent `astrid/packs/comfyui` and `astrid/packs/comfy_wrap`; `vibecomfy` stays a core pack | Owner, via the coordinator (Decision 13) |
| 3 Nov 2026 | H3 stays where it is in core ("CPU only, H3 stays where it is in core") | Retained END card (card wording, not owner words) |

## Already deferred (never blocks a review here)

H3 as a single task and its core clean-up (M2-06a1 to M3-04, M2-07 to M2-09, M3-09a to M3-09c); default packs and internal-access retirement (M2-10, M3-14, M1-07b, M2-12, M1-15b, REL-01); the K A6 / GPU re-check; the RunPod-key path of M1-11; the `training` move; superseded lanes (INT-A, INT-R, INT-F, M2-11a, M2-11b, M2-16); the later merge to `main`; the App install-manifest re-pin; the final home of the retired `local` effects and the M3-13a r2 hold patch (owner-held).

## PIN files

The poms_packs README (1 Nov 2026) says every pack has a root `PIN` file, that the installer owns creating and updating it, and that folder and personal installs are unpinned. The retained PK-16 card (3 Nov 2026) says poms_packs must contain no PIN files. These agree: a PIN is written by the installer into the installed copy, never committed. PK-16 therefore commits none, checks that none is committed, and corrects the README wording to say so.
