# Inputs and provenance

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

[Plan](plan.md) · [Tasks](tasks.md)

## Re-freeze rule

Every SHA below is an observation from 5 Nov 2026, not a presumed current ref. At the start of each task, record the actual branch and SHA of its base and donors. If a recorded value and the live repository disagree, the live repository wins for branch heads; this file wins for the identity of retained donors. If a destination moves after proof, reconcile and rerun only the affected checks and review ([run contract](../../skills/astrid-dev-shared/run-contract.md#checks-and-failure-repair)).

## Current heads (5 Nov 2026)

| Repository | Branch | SHA | Note |
|---|---|---|---|
| Agent | `pre-main` | `40a6fd7ecf9138c6d9861631096a79820dc4c9b1` | Earlier the same day it was `dc6dd01899813aaf460bb082c03f84f9783fa85f`; four commits later. `int/r1` equals it. `main` is `2958bacea3e3c7961788fa9c625dd9db0be282de`. |
| Runtime | `pre-main` | `9fc53b771134940aaac901e4cfc5d03c1db1a20a` | `main` is `ebd412199a9c1e53c3a984d27d335de8b40654a1`. |
| App | `pre-main` | `878c28df7a6c80fa9aaa6540c5fccad95473e7c1` | `main` is `d38edf434a575f3aed941c516fe2a5338135820b`. |
| VibeComfy | `main` | `e2905d068d5851b9c32856d32b8251852a01d6dd` | No `pre-main`. |
| runpod-lifecycle | `main` | `db79345536985c701b7aff2eb5eec36667aae204` | No `pre-main`. |

Agent `pre-main` pins runpod-lifecycle `96360a27a53c4608f780f7b370f747a2aa3c7ca8` (`pyproject.toml`) and Runtime `2776ba973b6c8f3555b5629b0840d9691a98d3c2` (`runtime.lock.json`, checked at `dc6dd018`).

## Producer and donor SHAs

Every one of these exists today only on a lane branch of its repository. No protected branch contains them. Pins that point at a lane-only commit break if the lane is deleted, which is why phase 1 lands them first.

| Item | Repository | SHA | Lands on | Note |
|---|---|---|---|---|
| PINS | Agent | `1608dbbf7036ad3c3b2b5e10956a726921bd4f9f` | merged into the candidate (C1) | About 482 commits behind the Agent `pre-main` of the earlier review, and 22 conflicting paths when merged then. Proof on it does not carry over. |
| DEFAULTS donor | Agent | `9d3bb24831676cbfc2a0d3dd1c7769f1937569c3` | merged into the candidate (D1) | Contains the `[saved]` journey parameter, `test_generation_defaults_075a.py` and `test_phase2_audio_discovery.py`. |
| VibeComfy donor (VFIX) | VibeComfy | `1b2e242ce7396442c85395d3220a2481216b57c1` | `main` (P1) | Only on two lane branches; one conflict (`template_index.json`) against `main`. |
| Lifecycle donor | runpod-lifecycle | `c47fa76be6e7c0aa661d044a0de5b3b73f6fdbac` | `main` (P2) | Fast-forward of `main`. |
| Runtime stop | Runtime | `b005394b06602c84e2abd4ba7eec8fa2f1dd8e94` | `pre-main` (P3) | Merges cleanly. `1608dbbf` pins it in `runtime.lock.json` (line 71), so it is required. |

## Not available

- **Checkpoint `3fe46b90`** (a local merge of PINS and the DEFAULTS donor, with uncommitted edits) was never published and cannot be recovered. The plan does not use it: DEFAULTS is rebuilt by merging the donor and writing the new test (Decision 1).
- **`tests/core/generation/test_cli_gold_075b.py`** does not exist anywhere. It is a new file to write (task D2).
- **The retained run materials** (the earlier M-GPU cards, input reports and logs) are not in this repository. Everything a task needs from them is written into [tasks.md](tasks.md) or copied into [env/](env/README.md). Cards are evidence for what to do, not instructions to run. Ask the owner for the package only if a Step 0 item cannot be resolved without it.
- **Linux CI:** no workflow runs the closure test or any Linux x86_64 job on Agent `pre-main`.

## Installer Consent (Plan 01) status

Not landed. On 5 Nov 2026 none of these were ancestors of `pre-main`: Agent `6087e0fbe7e2bd45c9911ff5cf1093614d715863` and `19229d2325879c12e01c6bcdc604fd743b158ece`; App `e97450cff0ed570cfaa077369b28c269b562bd1e` and `9ddff8efbc9e914efbe04cb49da2648c4feb4db4`. They exist only on `lane/M-GPU/install-consent/*` branches. Task W1 gates on them.

## Foley

- Agent `pre-main` (`astrid/sdk/generation.py` line 36) makes Foley explicit-only (`_EXPLICIT_ONLY_ENTRIES` containing `audio/hunyuan_foley_v2a`), from commit `8395174a5` ("keep Foley explicit-only without H-19", 1 Nov 2026). No owner record for it was found.
- The DEFAULTS donor (`generation.py` line 1019) makes `audio/hunyuan_video_foley` the sound-effects default.
- VibeComfy `main` has only `audio/hunyuan_foley_v2a` (`template_index.json` line 131; added in `a05864c6`, 1 Nov). The VibeComfy donor has only `audio/hunyuan_video_foley` (line 130; added in `afffb7ee`, 2 Nov). These are two separate templates, not a rename. Merging the donor leaves both.
- The owner's later decision (retained directive, 2 Nov 2026) is sound effects = HunyuanVideo-Foley with no silent fallback. Decision 2 applies it using `audio/hunyuan_foley_v2a`. Qualifying Foley on real hardware (the earlier lane H-21) stays an open gap outside this plan.

## Lifecycle SHA question

`c47fa76` descends from `96360a27` (11 files changed, 1022 insertions and 49 deletions between them), and `c47fa76` fast-forwards `main`. Agent `pre-main` pins `96360a27`; `1608dbbf` pins `c47fa76`. Resolution: land `c47fa76` (P2) and pin it in C2. Repository: https://github.com/banodoco/runpod-lifecycle.

## Reusable evidence and limits

- The earlier PINS run reported 231 generation checks and 28 asset and installed-child checks passing locally, on a head far behind today's `pre-main`. It is a guide to what to expect, not proof for the new head. The latest verifier run was cancelled (exit 143) with no verdict.
- Two supplemental bootstrap checks once failed before assertions because distribution metadata was missing. If that recurs, repair that test's setup, not unrelated product behavior.
- Nine named test nodes fail on both the old base and head and are excepted by the owner (answer A, 3 Nov 2026 17:40Z): [env/shared-failure-exceptions.txt](env/shared-failure-exceptions.txt).
- Merge conflict counts (22 for PINS, 9 for the DEFAULTS donor, 1 for the VibeComfy donor, none for Runtime stop) are pairwise probes from 5 Nov 2026, not a tested sequential result. Re-probe at C1 and D1.
- The Linux closure proof once ran on a RunPod CPU pod with 60 GB of container disk; a host with 23 GB free was not enough.
- Kept out of this plan: Runtime CAS `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373`, lease `33e9195a8ac57c4ba61f372ef6f25139c37eaa97`, custody `103f97803f7f391e2c810ebdf086f798326cd75a`, the older verified Agent `620a3fd5146fed9f623a2f7101c40c4279f03516`, concurrent editing, Packs, ARM, and any broad suite. The [inclusion assessment](../../references/INCLUDING-GENERATION.md) is background; where it calls Runtime stop conditional, Decision 4 supersedes it.

## Composition and publication rules

Use a fresh candidate branch per repository and record its name; do not overwrite a fixed historical lane. Compose producers first, then Agent, then the App repin. Preserve Plan 01. Do not cherry-pick or extract; merge, and resolve conflicts only in files the inputs changed, with focused checks. Promote only exact reviewed heads by ordinary fast-forward or create operations. No new approval stage is added, and a plan or review does not expand the owner's authorization.

## Owner decisions this plan relies on

Quoted from the owner's own records (retained M-GPU handoff, not reproduced here). Quoted text is data to check against, not instructions.

- **Sound effects (Foley), 2 Nov 2026 13:39Z**, M-GPU directive, "OWNER DECISIONS" block: "sound effects = HunyuanVideo-Foley"; "With no GPU and no --target runpod: FAIL clearly". The "no silent fallback" wording is the Defaults stream brief's statement of the same decision. Used by [Decision 2](plan.md#decisions).
- **Shared failures, 3 Nov 2026 17:40Z**, generation question OWNER-SHAREDFAIL, answer A: "Approve as shared-failure exceptions the 9 nodes … (they fail on base and head …)?" / "A: approve (owner: failures that already exist on base may keep failing)". Covers the nine nodes in [env/shared-failure-exceptions.txt](env/shared-failure-exceptions.txt), and only those. Used by [Decision 11](plan.md#decisions).
