# Inputs: zero-to-first-image onboarding

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner's direction (9 Nov 2026), merged as a queued plan at her request with the recommended answers to D1–D9 standing until she changes one, then re-planned into three phases around a fast path she accepted the same day. Next: run the advisor critique below on the re-plan, then record D1–D9 as answered here.

- **Source.** Hannah gave it on 9 Nov 2026. It was relayed in planning session `session_011EzfVzreGCJJQnTuXpbib9`, in two messages:
  - the onboarding-skill direction (items 1-4 in the [plan](plan.md#direction-owner-9-nov-2026));
  - two additions: put it in Plan 20, and handle the three choices routes.
- **The fast path (accepted 9 Nov 2026, relayed in the same session).** Hannah asked why onboarding took 9–11 days. The answer: the writing is small; the time is real-OS proof, App release cycles, a new machine-check command and review rounds. The skill and README are read from Agent `main` on GitHub by every install path, including shipped App builds, so their text goes live on merge with no release. She accepted re-planning on that basis: (1) a fast path of about a day, live without a release, after release 12 is published: the skill for the whole guided install with the choices rule, the README fixed, and the existing GPU detection in the skill with no new command; (2) the App brief change in the next ordinary App release; (3) the generation half, the App card and the per-OS proof after Plan 32 S2, T5d and T6d. The planner then moved the card into (2) and deferred the command; see the [plan](plan.md#sequence-and-readiness).
- **The earlier direction the same day** (an attached ComfyUI through Plan 32 S2, and the App's "Set up generation" card) is kept.
- **Next:** Hannah answers D1–D9 below. A scope PR then records her answers here.

**Prior art:** Read at Agent `origin/cand/29-r12` `ff40f2c684` and App `cand/29-r12` `3274a9c07`; the fast-path rows below also at Agent `origin/main` `a105de3a48` and App `origin/main` `57e200b45`.

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
| GPU detection that already exists | `detect_nvidia()` (names only) and the readiness probe (`nvidia-smi --query-gpu=driver_version,memory.total`) exist as functions; no CLI exposes either. The ComfyUI scan is runnable today (`python3 -m astrid.packs.vibecomfy.local scan`) | `gpu_environment.py:46-63`; `engine_readiness.py:49,567-597`; `packs/vibecomfy/docs/SKILL.md:42-53` |
| Shipped App briefs | Every build carries the skill URL as "Setup guide:" and a yes/no consent line, so the phase 1 skill must accept that line as the "choices supplied" route | App `copy.ts:163,280,307,322` at `57e200b45` |
| Plan 32 S2 | Guided generation setup is read-only ("Never … download or install during setup"). Its scope includes the `docs/setup/SKILL.md` step and one `agentInstructions` line | [Plan 32 tasks](../32-generation-placement-targets/tasks.md) S2 row |

**Approach:** Extend the existing setup skill in place, in three phases: Agent text and guide tests first (live on merge), the App brief and card in the next App release, and the generation half after Plan 32. Test the choices rule per route against the existing shared fixture. Read the machine with the probe the Agent already runs, in the skill, and defer a machine-check command. Leave generation discovery to Plan 32 S2. Alternatives considered:

| Alternative | Why not |
|---|---|
| A new `astrid-onboarding` skill beside `astrid-setup` | Two skills would cover the same install, and shipped App builds already link `docs/setup/SKILL.md`. Burn-down rule |
| A separate onboarding plan | The owner put it in Plan 20, and it would split one journey across two plans that edit the same file |
| Have the agent reuse the installer's interactive `[Y/n/c]` prompt | Agent shells are not terminals (`cli.py:795`). Choices must travel as flags |
| A read-only machine-check command in phase 1 (the earlier O5) | Needs an Agent release and a new CLI surface with a schema test, for one consumer, and blocks the fast path. Its facts are one `nvidia-smi` query and `uname -m`; a guide test pins the skill's engine table to `engine-index.json` against drift. Deferred until Plan 32 T2 declares per-entry requirements, Plan 12 needs it, or P3.5 shows a weaker agent misreading the probe. (This reverses the earlier "too many commands per step" objection: it is one command per OS, and the owner accepted it) |
| Drop the "Set up generation" card (the earlier O7) | A person who installed by hand from the README, or stopped at Connected, has no other way in, and the owner's earlier direction names it. Kept, and moved to phase 2 so that phase 3 needs no App release |
| A `route` field in the shared argv fixture (the earlier O2) | Both repositories already cover each route by case id, and a new field must be mirrored in two repositories for no new check |
| Real inference on every OS row (the earlier O8) | Needs NVIDIA hardware per OS and a release cycle per repair. Hosted CPU runners reach each branch's first command; one real image through RunPod proves the generation end. The unproven branches are listed |
| Fold the machine check into S2 | S2 is the existing-setup path. The machine check also decides the install and RunPod branches, and Plan 12 reuses it |
| Wait for Plan 32 for everything | Phase 1 (consent, entry points, doctor and the machine report) is useful now and touches nothing in Plan 32 |

**Challenge:** Pending — The plan touches a user-visible flow, consent and a cross-repo contract, so it needs the advisor's critique. That critique was not run, for the original plan or this re-plan, because both planning briefs excluded session tools. **Next:** the planner or orchestrator runs the advisor ([Orchestrate](../../skills/astrid-dev-orchestrate/SKILL.md)) before dispatch, briefed on the re-plan's calls: the machine-check command deferred, the card moved to phase 2, the fixture `route` field dropped, the lighter proof, and whether phase 1 should wait for release 12 at all.

**Proof and limits:** See P3.5 in [tasks.md](tasks.md). Hosted macOS, Windows and Linux runners on CPU reach each branch's first command against a fake; real inference is proven once, through RunPod. The attached-ComfyUI and managed-engine branches are unproven with real inference unless D8 provides an NVIDIA machine. macOS has no managed engine. Wan2GP and providers are excluded.

## Owner decisions needed

Re-checked for the three-phase plan: all nine still apply. D2, D4, D8 and D9 are revised; none is dropped.

| # | Phase | Decision | Recommendation |
|---|---|---|---|
| D1 | 1 | The skill's name and path | Keep `docs/setup/SKILL.md`, `name: astrid-setup`. Shipped App builds and the README already link it. Retitle it "Set up Astrid, from install to first image" |
| D2 | 3 | How to install it optionally, before Astrid exists | Use it from its URL in every phase. The optional pre-install arrives in phase 3 with the synced-view change (P3.3), because before that sync does not know the file and a pre-installed copy would become a second copy. It is one line per OS that saves the skill under the agent's skills folder as an Astrid-managed copy (with the `.astrid-managed-skill.json` marker, `harnesses/base.py:19`), so skills-on sync adopts it and leaves one copy |
| D3 | 3 | Does the skill run a managed engine install, or only link to it? | Run it, as its own step with its own yes, where Astrid has a managed engine (Linux and Windows NVIDIA). Link only where it has none (macOS). Phase 1 only says that the install is coming. S2's read-only rule stays for "Set up my generation" |
| D4 | 1, 3 | What counts as "capable" | In phases 1 and 2: an NVIDIA GPU with at least 12 GB on Linux or Windows, stated once in the skill and read from the `nvidia-smi` query. In phase 3, the default image entry's declared requirement if Plan 32 T2's manifest declares one by then. On macOS: not capable for a managed engine; offer ComfyUI's own installer, then attach, or RunPod |
| D5 | 3 | RunPod during onboarding | Use paid consent per claim, plus a low budget cap for the test generation (Plan 32 T6d's `machines.runpod` cap; suggest $2), and release the machine afterwards unless the user keeps it warm |
| D6 | 2 | The App's consent line | Replace "May I install Astrid with these setup choices?" with "show and offer a change" (P2.1, worded in P2.4, where Hannah sees the before and after), with the flag spellings in the brief |
| D7 | 1, 2 | The overlap with Plan 32 S2 | Move S2's `docs/setup/SKILL.md` step and its App brief line to this plan (P1.1, P2.1). S2 keeps the generation skill section, the Wan2GP probe and `--as-entry` |
| D8 | 3 | Proof hardware, budget and the weaker agent | Hosted macOS arm64, Windows x64 and Linux x64 runners on CPU for every row up to each branch's first command. One real image through RunPod, up to $5 including retries. An NVIDIA machine only for an optional row. Pick one smaller model as the "weaker agent" for one row |
| D9 | all | Review rounds | Phase 1: 1 (Agent text and guide tests, no product code). Phase 2: 1 (a few App strings and one card, against an unchanged fixture). Phase 3: at most 2 (paid consent, an engine install consent and a user-visible flow across Plan 32's contracts) |

## Source identities

| Repository | Planning read | Base at start | Candidate branch | Destination |
|---|---|---|---|---|
| astrid-agent | `origin/cand/29-r12` `ff40f2c684` and `origin/main` `a105de3a48` (read-only) | the release 12 published revision, recorded in P1.5 | phase 1: one docs-and-tests branch; phase 3: one branch | Phase 1: Agent `main` by an ordinary reviewed PR, live on merge with no release (owner, 9 Nov). Phase 3: skill text the same way; the synced-view change (P3.3) through the release process |
| astrid-app | `cand/29-r12` `3274a9c07` and `origin/main` `57e200b45` (read-only) | App `main` at the start of P2.1, after Plan 29's orchestrator agrees | one App branch for phase 2 | the next ordinary App release, through the release process |
| astrid-dev | `origin/main` `7e7f60d` | — | `plans/20-fast-path` | `main` through a scope PR |

## References

- [Plan 32](../32-generation-placement-targets/plan.md): S2, T5, T5d and T6d are consumed. [Plan 12](../12-multiple-inference-routes/plan.md): later Wan2GP rows. [Plan 29](../29-update-and-release/plan.md): owns release 12. [Plan 35](../35-one-home-for-user-state/plan.md): App-side choice state after install. [Plan 15](../15-openshell-safe-execution/plan.md) and [Plan 16](../16-streamlined-agent-experience/plan.md): out of scope.
- [Liquid Software vision](../../vision/pillars/liquid-software.md): good defaults, choices people understand, and user control.
