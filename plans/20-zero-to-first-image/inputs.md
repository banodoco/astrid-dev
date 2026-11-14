# Inputs: zero-to-first-image onboarding

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah asked for this direction on 9 Nov 2026, accepted the fast-path re-plan, and asked for the project to start running alongside release 12 ([orchestrator session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). D7 (reversed, 9 Nov) and D1–D6, D8 and D9 (agreed, 10 Nov) are decided (see [Owner decisions](#owner-decisions-needed)).

- **Source.** Hannah gave it on 9 Nov 2026. It was relayed in planning session `session_011EzfVzreGCJJQnTuXpbib9`, in two messages:
  - the onboarding-skill direction (items 1-4 in the [plan](plan.md#direction-owner-9-nov-2026));
  - two additions: put it in Plan 20, and handle the three choices routes.
- **The fast path (accepted 9 Nov 2026, relayed in the same session).** Hannah asked why onboarding took 9–11 days. The answer: the writing is small; the time is real-OS proof, App release cycles, a new machine-check command and review rounds. The skill and README are read from Agent `main` on GitHub by every install path, including shipped App builds, so their text goes live on merge with no release. She accepted re-planning on that basis; the phases, what goes live when, and the estimates are in the [plan](plan.md#sequence-and-readiness). The planner then moved the card into phase 2 and deferred the command.
- **The earlier direction the same day** (an attached ComfyUI through Plan 32 S2, and the App's "Set up generation" card) is kept.
- **Next:** none for owner decisions; all nine are decided (10 Nov).

**Prior art:** Read at Agent `origin/cand/29-r12` `ff40f2c684fc7ce22e42a5cacda5c63a0c8800a9` and App `cand/29-r12` `3274a9c07`; the fast-path rows below also at Agent `origin/main` `a105de3a48` and App `origin/main` `57e200b45`.

| Area | Finding | Source |
|---|---|---|
| The setup skill exists and is already linked | `docs/setup/SKILL.md` (`name: astrid-setup`) is the README banner's target and the App brief's "Setup guide". It stops at Connected, and local engines are "not covered here yet" | Agent `docs/setup/SKILL.md:1-4,45-47`; `scripts/render_readme.py:9-19`; App `copy.ts:294,338` |
| It is not a synced skill | It is not a pack skill. Only pack `docs/**/SKILL.md` resources and `_CORE_FILES` reach the harness view. Sync links are named `astrid-<id>` and adopt only Astrid-managed targets | `astrid/skills/discovery.py:1-11`; `view.py:39-45`; `harnesses/base.py:19,115`; `harnesses/claude.py:30-36` |
| What the App brief carries | **Fresh install:** a yes/no consent line, all four values, and a command of `--yes` plus only the flags that differ from the recommendation. **Fully local:** the same. **Already set up, update or repair:** no choice line, and a plain or `--update` line. Choices are saved per browser in `localStorage` (`astrid:pending-setup-v1`) | `copy.ts:56-61,63-85,95-98,173-175,279-292,316-322`; `SetupBlock.tsx:33-68` |
| Where a user can change choices | Before copying, in the App's Customize panel (fresh install only). In a terminal, the installer's `[Y/n/c]` prompt. After install, only by rerunning the install line with an explicit flag. The installer prints each way back. The App has no surface for this after install | `SetupBlock.tsx:53-68`; `installer/cli.py:60-92,201-224`; `choices.py:45-65` |
| An agent's shell without `--yes` | Not a terminal, so the installer stops at `consent-required` and prints the plan and the exact rerun | `installer/cli.py:793-800`; `choices.py:68-79` |
| Shared contract | The App's `installArgv.fixture.json` mirrors the Agent's `tests/fixtures/installer/app_argv.fixture.json` | both files |
| Installer success and failure lines | `Astrid installed:`, `Astrid is installed and running`, `Astrid is already up to date`, `Astrid was NOT installed.` | `installer/outcome.py:137-159` |
| Doctor | The installer's `--doctor` writes a bundle and works even when the `astrid` command is off. `astrid doctor --bundle` needs the CLI | `installer/cli.py:472,920`; `core/gateway/dispatch.py:231-275` |
| A brief pattern that suits weaker agents | An exact command, its success words, a doctor fallback and "Don't try other fixes" | App `copy.ts:108-113` |
| Engine discovery | `scan` finds only *running* loopback ComfyUI (ports 8188 and 8000) and Pinokio apps. It finds no stopped ComfyUI and no Wan2GP (S2 adds a Wan2GP folder probe) | `packs/vibecomfy/local.py:386-417,459-467` |
| Capability | `detect_nvidia()` reads only GPU names (no memory). It is used only in the Windows preflight. Nothing detects Apple silicon or AMD | `core/generation/gpu_environment.py:46-99` |
| Managed engines | `engine-index.json` has Linux `comfyui` (cu130), Windows `vibecomfy` (cu130), `vibecomfy-h3` and Windows `wan2gp`, and nothing for macOS. The Windows environment plan says Astrid doesn't install ComfyUI on Linux or macOS "yet", although `astrid engines install comfyui` exists for Linux | `packs/engine-index.json`; `gpu_environment.py:130-153`; `core/engine_cli.py:33-50` |
| RunPod | The key is read from `RUNPOD_API_KEY` (by reference). Paid consent applies per claim, with `runpod.setup` | `packs/runpod/docs/SKILL.md:38-45,70-108` |
| The skill and README on Agent `main` | `docs/setup/SKILL.md`, `README.md`, `scripts/render_readme.py` and the guides test are identical on `main` and `cand/29-r12`. The README still says "Pass `--yes` to accept the recommended choices without a prompt", against the skill's "must not be used to bypass the consent question" | Agent `README.md:25-31`; `docs/setup/SKILL.md:17-20` |
| The installer first lines the skill quotes | Present on `cand/29-r12`, absent on Agent `main`. Phase 1 therefore merges only after release 12 is published | `installer/outcome.py:137-166` at `ff40f2c684`; none at `a105de3a48` |
| Route behaviour is already tested in the Agent | Choice precedence, the unattended consent stop and saved policy on update each have tests; the shared argv fixture already names `untouched`, `edit-*` and `already-set-up` cases | `tests/test_installer_choices.py` (`test_precedence_…`, `test_unattended_consent_only_blocks_fresh_without_yes_or_tty`, `test_existing_install_update_needs_no_consent_flag_and_keeps_saved_policy`); `tests/fixtures/installer/app_argv.fixture.json` |
| GPU detection that already exists | `detect_nvidia()` (names only) and the readiness probe (`nvidia-smi --query-gpu=driver_version,memory.total`) exist as functions; no CLI exposes either. The ComfyUI scan is runnable today (`python3 -m astrid.packs.vibecomfy.local scan`) | `gpu_environment.py:46-63`; `engine_readiness.py:49,567-597`; `packs/vibecomfy/docs/SKILL.md:42-53`. After D7 only phase 3's capability read (P3.1) uses the first two |
| Shipped App briefs | Every build carries the skill URL as "Setup guide:" and a yes/no consent line, so the phase 1 skill must accept that line as the "choices supplied" route | App `copy.ts:163,280,307,322` at `57e200b45` |
| Plan 32 S2 | Guided generation setup is read-only ("Never … download or install during setup"). Its scope includes the `docs/setup/SKILL.md` step and one `agentInstructions` line | [Plan 32 tasks](../32-generation-placement-targets/tasks.md) S2 row |

**Approach:** Extend the existing setup skill in place, in three phases: Agent text and guide tests first (live on merge), the App brief and card in the next App release, and the generation half after Plan 32. Test the choices rule per route against the existing shared fixture. Defer a machine-check command; the skill has no machine look in phase 1 (D7). Leave generation discovery, and the skill's step after Connected, to Plan 32 S2. Alternatives considered:

| Alternative | Why not |
|---|---|
| A new `astrid-onboarding` skill beside `astrid-setup` | Two skills would cover the same install, and shipped App builds already link `docs/setup/SKILL.md`. Burn-down rule |
| A separate onboarding plan | The owner put it in Plan 20, and it would split one journey across two plans that edit the same file |
| Have the agent reuse the installer's interactive `[Y/n/c]` prompt | Agent shells are not terminals (`cli.py:795`). Choices must travel as flags |
| A read-only machine-check command in phase 1 (the earlier O5) | Needs an Agent release and a new CLI surface with a schema test, for one consumer, and blocks the fast path. Its facts are one `nvidia-smi` query and `uname -m`; a guide test pins the skill's engine table to `engine-index.json` against drift. Deferred until Plan 32 T2 declares per-entry requirements, Plan 12 needs it, or P3.5 shows a weaker agent misreading the probe. (This reverses the earlier "too many commands per step" objection: it is one command per OS, and the owner accepted it) |
| Drop the "Set up generation" card (the earlier O7) | A person who installed by hand from the README, or stopped at Connected, has no other way in, and the owner's earlier direction names it. Kept, and moved to phase 2 so that phase 3 needs no App release |
| A `route` field in the shared argv fixture (the earlier O2) | Both repositories already cover each route by case id, and a new field must be mirrored in two repositories for no new check |
| Real inference on every OS row (the earlier O8) | Needs NVIDIA hardware per OS and a release cycle per repair. Hosted CPU runners reach each branch's first command; real images are Plan 34's (no live GPU here, D8). The unproven branches are listed |
| Fold the machine check into S2 | S2 is the existing-setup path. The machine check also decides the install and RunPod branches, and Plan 12 reuses it |
| Wait for Plan 32 for everything | Phase 1 (consent, entry points and doctor) is useful now and touches nothing in Plan 32 |

**Challenge:** Reviewed — advisor critique, 9 Nov 2026, in the [orchestrator session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9), briefed to build as little as possible. Its three findings are applied: (1) one taste pass for all of phase 1's text (P1.3 now covers the README pointer; P1.4 is folded into it); (2) the skill's `## Set up generation` section must give a working next step before phase 3, so phase 2's card is not a dead end (superseded by D7: the skill has no such section; the card links Plan 32 S2's section, so P2.3 waits for it); (3) landing on Agent `main` (P1.5) is a release-workflow merge that needs Hannah's go, recorded at the time.

**Proof and limits:** See P3.5 in [tasks.md](tasks.md). Hosted macOS, Windows and Linux runners on CPU reach each branch's first command against a fake, RunPod included. No live GPU tests in this plan (D8, owner 10 Nov): real inference on every branch is recorded as "needs a live run" and belongs to [Plan 34](../34-real-gpu-proof/plan.md). macOS has no managed engine. Wan2GP and providers are excluded.

### Phase 4: local-first (14 Nov 2026)

**Scope decision:** Pending — Hannah gave the direction and decided OD7 and OD8 (14 Nov); OD1–OD6 are still open (below). Next: Hannah answers OD1–OD6 in the scope PR.

- **Source.** Hannah asked the Release 13 advisor (session `session_011EzfW4KxQbf3mB7UevxVdh`) on 14 Nov 2026 to map the onboarding path, make it local-first and add it to Plan 20 as tasks. The orchestrator (session `session_011EzfW2L4ou5fDudzKLrc9d`) relayed the brief to this planner. Her words, verbatim:
  > "In general, it should probably point to RunPod, but it should only have like a one-line mention of RunPod, and the other general should just be focused on people who are running locally and setting it up."

  > "Map out the path for actually connecting and launching your local ComfyUI instance. Is it easy to connect to it? Does it have an intuitive way to run to it? Does it use their existing models? Does it generate via that?"

  > "Wherever they install Astrid from, either from the web app or from the agent, it guides them through that process and gets them set up using the stuff that's already on their machine, ideally, or offers them RunPod, and points them towards the RunPod skill, which will contain all the thing. We probably have the bones of this already; it's the refinement path to actually make this good, and make sure there's one path. The documentation is clean and minimal and elegant, one place per concept, pointing towards relevant documents. Everything runs via the Astrid generate skill."

  > "Setting up their defaults is an important thing. We give them defaults, but they might already have workflows on their machine that they recently edited. We should work with them to keep ours, offer to use theirs, biasing towards recent ones, or create new defaults."

  > "In any case, sending a link to astrid.haus to actually see the generated image."
- **Draft.** The advisor's map and draft tasks are committed verbatim as [phase-4-local-first-draft.md](phase-4-local-first-draft.md) (astrid-dev commits `b7dd383`, `a9b9488` and `eec99b3`; the last records OD7 and OD8. `a9b9488` added with the later direction: one hand-off sentence at every door, one home per concept, defaults from the person's recent work and a link to the image). It answers her four questions: connecting is easy when ComfyUI runs on 8188, but saving the choice is clumsy. Running is not yet intuitive. It uses the existing models and generates through the person's server without changing it. None of this is proven live. The draft's sources were Agent `r13/compose` `176e5ba1`, App `d6ee9af`, Pinokio `d15c58b` and VibeComfy `r13/cells-vc-10`, through read-only explorer passes. Nothing was run.

**Approach:** Extend the same skill in place; no new skill and no new plan. Phase 4 keeps phases 1–3 and narrows the RunPod and managed-engine text to one line each. Alternatives considered:

| Alternative | Why not |
|---|---|
| Keep the 9 Nov layout (skill ends at Connected; Plan 32 S2 owns the next step) | Against the 14 Nov direction. The map shows the path stopping at Connected, with nothing saying what to run first (OD1) |
| A separate local-onboarding skill beside `astrid-setup` | Two skills for one journey. Shipped App builds and the README already link `docs/setup/SKILL.md` |
| Keep the RunPod walkthrough in the setup skill | About half of the 404-line skill repeats the RunPod skill for three operating systems. One line and a link removes the copy |
| Download missing models into the person's ComfyUI now | OD4: it changes the person's machine, and the walk has not yet shown it is needed. Name the file and folder instead |
| Prove only on CPU fakes, as D8 requires | The question is whether the local path works. A fake cannot show minutes to the first image or where an agent guesses, so one local run is asked for (OD3) |
| _Critique-driven alternatives are recorded under Challenge below_ | |

**Challenge:** Pending — independent critique running. Next: record its findings and the decisions taken.

**Proof and limits:** P4.0 and P4.9 are live walks on a machine with a running ComfyUI and a GPU, which a cloud worker cannot run (OD3). Everything else is proven by focused Agent tests against the existing fake ComfyUI. No rentals. ComfyUI Desktop, a stopped ComfyUI and Wan2GP are not proven.

**Run start:** 14 Nov 2026. The orchestrator (`session_011EzfW2L4ou5fDudzKLrc9d`), acting on Hannah's request to farm the tasks out (relayed by the advisor), started a phase 4 manager, `session_011EzfW4R5yz8EETVbzZaLCF`. It may start P4.3, P4.6 and P4.11 now, on Agent `int/20-phase4` cut from Agent `main`. It still needs the owner's go for: P4.0 (OD3); any other task, which waits for release 13 to publish and for OD6; merging to Agent `main` or any release branch; and P4.1, P4.2, P4.4, P4.10 and P4.12 before the critique below has settled their shape. The advisor is `session_011EzfW4KxQbf3mB7UevxVdh`. This start was made by the orchestrator, not recorded from Hannah directly; OD6 stays Pending for the rest.

**Review rounds:** Recommend one round (R4) on the integrated phase 4 result before P4.9's final walk: a user-visible flow and a contract change (P4.2), but no paid action. No review stop. Pending: owner to confirm.

## Owner decisions needed

Re-checked for the three-phase plan: all nine still apply. D7 is decided by the owner; D1–D6, D8 and D9 were agreed on 10 Nov at the answers below. D3, D5 and D6 name the test that pins each.

| # | Phase | Decision | Status and recommendation |
|---|---|---|---|
| D1 | 1 | The skill's name and path | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "yeah, i agree on all". Answer: keep `docs/setup/SKILL.md`, `name: astrid-setup`. Shipped App builds and the README already link it. Retitle it "Set up Astrid, from install to first image" |
| D2 | 3 | How to install it optionally, before Astrid exists | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "yeah, i agree on all". Answer: use from its URL in every phase. The optional pre-install arrives in phase 3 with the synced-view change (P3.3), because before that sync does not know the file and a pre-installed copy would become a second copy. It is one line per OS that saves the skill under the agent's skills folder as an Astrid-managed copy (with the `.astrid-managed-skill.json` marker, `harnesses/base.py:19`), so skills-on sync adopts it and leaves one copy |
| D3 | 3 | Does the skill run a managed engine install, or only link to it? | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "I AGREE". Answer: run it, as its own step with its own yes, where Astrid has a managed engine (Linux and Windows NVIDIA). Link only where it has none (macOS). Phase 1 only says that the install is coming. S2's read-only rule stays for "Set up my generation". *Reason: a managed install is the one step that changes the machine, so it gets its own yes. Pinned by P3.2: the install never runs without its yes.* |
| D4 | 3 | What counts as "capable" | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "yeah, i agree on all". Answer: an NVIDIA GPU with at least 12 GB on Linux or Windows, stated once in the skill and read from the `nvidia-smi` query (phase 3 only, since D7 removed the phase 1 machine look), or the default image entry's declared requirement if Plan 32 T2's manifest declares one by then. On macOS: not capable for a managed engine; offer ComfyUI's own installer, then attach, or RunPod |
| D5 | 3 | RunPod during onboarding | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "I AGREE". Answer: use paid consent per claim, plus a low budget cap for the test generation (Plan 32 T6d's `machines.runpod` cap; suggest $2), and release the machine afterwards unless the user keeps it warm. *Reason: a paid action needs a consent and a ceiling the user can see. Pinned by P3.2 (no RunPod claim without paid consent) and P3.1's guide test (the skill states the cap); the $2 figure is a suggestion, so no test pins the number.* |
| D6 | 2 | The App's consent line | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "I AGREE". Answer: replace "May I install Astrid with these setup choices?" with "show and offer a change" (P2.1, worded in P2.4, where Hannah sees the before and after), with the flag spellings in the brief. *Reason: the yes/no line hides that the user can change a value. Pinned by P2.1's `copy.test.ts` cases (no yes/no question; every value and flag present).* |
| D7 | 1, 2 | The overlap with Plan 32 S2 | **Decided by the owner, 9 Nov (commit c07ea31).** The earlier recommendation, to move S2's `docs/setup/SKILL.md` step to this plan, was reversed: S2 keeps the `docs/setup/SKILL.md` generation step. Plan 20's skill ends at Connected (step 3), with no machine probe and no "Set up generation" section. Not settled by the reversal: S2's App `agentInstructions` line |
| D8 | 3 | Proof hardware, budget and the weaker agent | **Agreed by the owner, 10 Nov 2026, with one change**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT): "yeah, i agree on all", then "let's get it going but no live GPU tests". Answer: hosted macOS arm64, Windows x64 and Linux x64 runners on CPU for every row up to each branch's first command, and one smaller model as the "weaker agent" for one row. **No live GPU tests in this plan:** no real RunPod image and no NVIDIA machine row. The GPU-only proofs are recorded as "needs a live run" and left to [Plan 34](../34-real-gpu-proof/plan.md) |
| D9 | all | Review rounds | **Agreed by the owner, 10 Nov 2026**, in the [Plan 32 orchestrator session](https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT), answering the orchestrator's message that listed it at the recommended answer: "I AGREE". Answer: R1 = 1 round, R2 = 1, R3 = 2 (not 3). Phase 1: 1 (Agent text and guide tests, no product code). Phase 2: 1 (a few App strings and one card, against an unchanged fixture). Phase 3: at most 2 (paid consent, an engine install consent and a user-visible flow across Plan 32's contracts). R1 has run (one round); R1, R2 and R3 stay. *Review stop:* none recommended for P3.1 (see its row in tasks.md): a late finding would redo only P3.2 and P3.4, and R3 reviews them together before any live run |

### Phase 4 owner decisions (14 Nov 2026)

OD7 and OD8 are decided (below). OD1–OD6 are **Pending: owner to decide.** The recommendations are the advisor's, adjusted where the critique below changed them.

| # | Decision | Options | Recommendation | Status |
|---|---|---|---|---|
| OD1 | Does the skill continue past Connected to a first image, with RunPod and the managed engine one line each? | Yes, superseding the 9 Nov "ends at Connected" layout and, for the local path, D7's split with Plan 32 S2; or keep the 9 Nov layout | Yes. It follows from the 14 Nov direction; confirm it | Pending |
| OD2 | When no shipped entry is ready, does the first image come from the person's own saved workflow? | Yes; or stop and name the missing models | Yes. It matches the 9 Nov line "its proof is a real first image from a saved workflow" | Pending |
| OD3 | D8 forbids live GPU tests. May P4.0 and P4.9 run on a local machine with ComfyUI and a GPU (no rental)? | Allow local runs, no rentals; or keep D8 as it is and prove on CPU fakes only | Allow local runs; rentals stay excluded. P4.0 does not start until this is decided | Pending |
| OD4 | May Astrid download a missing model into the person's ComfyUI models folder, with a yes per file? | Not now (name the file and folder); or yes, per file, through VibeComfy's existing `fetch` | Not now. Revisit after the walk | Pending |
| OD5 | Create a default project when none exists at the first generation, and say so? | Yes, named "My first project" like the App; or refuse, naming the command to create one | Yes | Pending |
| OD7 | Where the link to Astrid comes | Once at the end; at Connected only; or both | — | **Decided by Hannah, 14 Nov 2026 (about 13:00 UTC)**, in the advisor session `session_011EzfW4KxQbf3mB7UevxVdh`, relayed by the advisor: "Maybe we should just send it at the end, pointing towards: you can click the generations thing at the bottom here to see this image in the app." Answer: once, at the end, opening the project with the image in it, plus one sentence pointing to the Generations pane. Reason: a person who installed through an agent may never have had Astrid open. The pane's real label and position are confirmed by P4.10, not assumed |
| OD8 | The defaults step | Per slot: keep ours, use theirs, pick another or create a new one; or keep Astrid's defaults only | — | **Decided by Hannah, 14 Nov 2026**, same session and relay. Answer: one question per slot: keep Astrid's default (with its readiness), use one of theirs (most recently edited first), pick another entry, or create a new default from their own workflow (previewed first, with one undo command) |
| OD6 | Timing | (a) P4.0 now, everything else after release 13 publishes; (b) as (a), but P4.1, P4.3, P4.6 and P4.11 start on branches from Agent `main` before release 13 (the advisor's suggestion, 14 Nov), landing only after it; (c) all after release 13 | (a). This planner's brief keeps all phase 4 implementation until release 13 publishes. (b) is cheaper in wall-clock time but rebases work onto a moving release, and P4.1's shape depends on the critique | Pending. Hannah has asked the orchestrator to farm the tasks out; until she picks (b), workers wait for release 13 |

## Source identities

| Repository | Planning read | Base at start | Candidate branch | Destination |
|---|---|---|---|---|
| astrid-agent | `origin/cand/29-r12` `ff40f2c684` and `origin/main` `a105de3a48` (read-only) | `int/20-zero-to-first-image` cut at `ff40f2c684` (smoke `ENV-PASS` on int/20); the release 12 published revision is recorded in P1.5 | phase 1: one docs-and-tests branch; phase 3: one branch | Phase 1: Agent `main` by an ordinary reviewed PR, live on merge with no release (owner, 9 Nov). Phase 3: skill text the same way; the synced-view change (P3.3) through the release process |
| astrid-app | `cand/29-r12` `3274a9c07` and `origin/main` `57e200b45` (read-only) | App `main` at the start of P2.1, after Plan 29's orchestrator agrees | one App branch for phase 2 | the next ordinary App release, through the release process |
| astrid-dev | `origin/main` (refreshed by `plan20/spec-refresh`; `7e7f60d` was the first planning base) | — | `plan20/spec-refresh` | `main` through a scope PR |

## References

- [Plan 32](../32-generation-placement-targets/plan.md): S2, T5, T5d and T6d are consumed. [Plan 12](../12-multiple-inference-routes/plan.md): later Wan2GP rows. [Plan 29](../29-update-and-release/plan.md): owns release 12. [Plan 35](../35-one-home-for-user-state/plan.md): App-side choice state after install. [Plan 15](../15-openshell-safe-execution/plan.md) and [Plan 16](../16-streamlined-agent-experience/plan.md): out of scope.
- [Liquid Software vision](../../vision/pillars/liquid-software.md): good defaults, choices people understand, and user control.
