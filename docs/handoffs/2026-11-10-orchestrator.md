# Orchestrator brief — Astrid, 10 Nov 2026

This brief is for the next orchestrator. It holds everything needed to take over from GitHub alone, on any machine. It replaces the cloud session https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT.

Read it in this order:
1. this file;
2. [astrid-dev-orchestrate](../../skills/astrid-dev-orchestrate/SKILL.md);
3. each running plan's `handoff.md` (linked in [State and next actions](#state-and-next-actions)).

Release 12 (Plan 29) has its own takeover brief, [`plans/29-update-and-release/orchestrator-brief.md`](../../plans/29-update-and-release/orchestrator-brief.md). Read it too if you take over the release.

The owner is **Hannah**.

## 1. Your job

You are the **orchestrator**: you equip managers, you don't do the work yourself.
- Start one Codex **manager** per plan (`/astrid-dev-manage`). Managers farm tasks out to Codex workers by route.
- Relay between managers. One manager's output is often another's input; for example, Plan 40's code is what Plan 34 tests on a GPU.
- Take the decisions the plans leave open, record them, and bring Hannah only the ones that are genuinely hers.
- Merge the astrid-dev PRs that need you (see [Merging](#merging)).
- Keep the machine healthy: disk, keep-alive, and spend.

How Hannah wants you to work:
- **"KEEP IT MOVING NO MATTER WHAT, think your way around any obstacles. Accept no excuses."** When something blocks, find the way round it, today.
- **Farm out.** No Claude Agent-tool sub-agents; every agent runs on Codex (Luna for normal tasks; Terra, Sol or Astra by route). To research something, hand it to the manager that owns the area. If no manager fits, run read-only Codex Luna explorers.
- **When you're stuck or want a second opinion,** ask Astra: `codex exec -m gpt-6-astra -s read-only --skip-git-repo-check "<question>" </dev/null`. stdin must be `/dev/null`, or it hangs.
- **Talk plainly and briefly.** Answer what she asked first. Say money as "spent $X of the $20 cap", not as an account balance.
- **Never add constraints she didn't ask for.** Today's mistakes, each of which she had to correct:
  - geographic filters;
  - 45–60 minute retry windows;
  - rotating between tests;
  - an A100 for audio work.
  When you're unsure, choose the less restrictive option and say so.

## 2. The big picture

Astrid has three repos: an **Agent** (Python, `banodoco/astrid-agent`), an **App** (`banodoco/astrid-app`) and a **Runtime** (`banodoco/astrid-runtime`). It generates media through ComfyUI workflows from **VibeComfy** (`banodoco/VibeComfy`), on the user's own machine or on a rented **RunPod** GPU. Plans, skills and the process live in **astrid-dev** (`banodoco/astrid-dev`).

| Plan | What it delivers | Why it matters now |
|---|---|---|
| 29 Update and release | Releases. Release 12 is in its gate now; release 13 comes next | Every product change below reaches users through release 13 |
| 32 Generation placement targets | One generation path: `astrid generate --placement local\|runpod` with paid consent, leases and warm reuse | The base the other plans build on. It ships in release 13 |
| 40 Machine lifetime controls | `astrid machines`: when each machine stops and what it costs; `keep`, `setup`, `claim`, `release`; `--gpu`/`--datacenter`; waiting for capacity by default; keeping the machine after a failed job | Hannah's requests from today. It ships in release 13 |
| 34 Real GPU proof | Live GPU validation of every default generation slot through the product | Finds the product bugs a CPU can't (fixes A–N so far) |
| 20 Zero to first image | Onboarding: from the install line to a first generated image, Agent plus App | Ships after release 12 |

Release path:
1. Release 12 publishes (Plan 29 owns it).
2. Lift the CI freeze.
3. Plan 32 merges `main` into int/32 and re-proves.
4. Cut `cand/release-13` through the [Release skill](../../skills/astrid-dev-release/SKILL.md), carrying int/32, Plan 20 P1.5, Plan 40, the CI-trigger prep, and VibeComfy [#165](https://github.com/banodoco/VibeComfy/pull/165) and [#166](https://github.com/banodoco/VibeComfy/pull/166) via the pin.

## 3. Owner rules (Hannah, 9–10 Nov). These stand until she changes them.

**GPU acquisition:**
- Every test or job is ONE product command that waits for capacity itself (Plan 40 T6; proven live twice). Wait until claimed, with no time window. The user can bound it with `--capacity-timeout`.
- NO geographic filters, anywhere ("STOP STUPID GEO RESTRICTIONS"). Narrow only to the saved volume's datacenter, or a datacenter the user names.
- The user defines the GPU(s) in their own order, the storage and optionally the datacenter (D10). Price only breaks ties within a GPU type.
- No rotating between tests. Run one test, then the next. Tests may run in parallel, each in its own isolated install and data root, with a fixed budget split and a $1 margin.
- Use the cheapest adequate GPU, never an A100 for audio; 24 GB is enough.

**Machines:**
- A failed job must NOT release the pod. It stays idle within the consented idle and paid limits, and is released at once only when reuse would be unsafe (D12; Plan 40 T9, not yet built).
- Preferences (GPUs, storage, datacenter, budget) are stored durably, per user, in the Runtime's `generation` settings document. `astrid machines setup` sets them.
- The RunPod pack has ONE skill covering all machine use: `astrid/packs/runpod/docs/SKILL.md`.

**Money:** the current GPU validation run may spend up to $24 and stops at $20; $3.13 is spent. Take a census before and after every rental, and release every pod.

**Disk:** clear it aggressively and do it yourself; don't ask managers.
- Safe: named caches; clean worktrees whose commits are on a remote; `*.env` folders whose worktree is gone.
- Never: unpushed work, or an active install.

**Guardrails:**
- no force-push and no rebase; use merge commits;
- never print, store or commit a secret, and refer to credentials by NAME only;
- no App `main` or install-manifest change without Plan 29's release owner;
- VibeComfy changes ride with release 13 through the pin, never as a merge to VibeComfy `main`.

**Approved on 10 Nov:**
- the release-12 landings go via release 13 (Plan 20 P1.5 and Plan 32);
- P3.3b: Plan 20 fixes the default-skill sync, with timeline as a default skill;
- drop `int/**` from heavy CI push triggers after release 12;
- P2.4 App wording;
- Plan 20 phase 2 may proceed before release 12;
- Plan 32 is in release 13.

## 4. Starting up

### The machine

- **Codex:** run `npm i -g @openai/codex`, then `codex login --device-auth`, giving Hannah the link and code. Never ask for an OpenAI API key. Then install the skills: `mkdir -p ~/.agents && rm -rf ~/.agents/skills && cp -r <astrid-dev>/skills ~/.agents/skills`.
- **Model IDs that this sign-in accepts:** Luna `gpt-6-luna`, Terra `gpt-6.1-terra`, Sol `gpt-6.1-sol`, Astra `gpt-6-astra`. (`gpt-6.1-luna` is refused.) Routes are N→Luna, X→Terra, S→Sol, and T or judgment→Astra.
- **Credentials:** `RUNPOD_API_KEY` in the environment, passed to GPU managers only, with `CODEX_PASS_ENV=RUNPOD_API_KEY`. `gh` with push access to the five repos.
- **Clones:** clone each repo a manager needs into its workdir, using `git clone --filter=blob:none`, then check out the branches from its `handoff.md`.

### Starting a manager

Follow [codex-in-cloud](../../skills/astrid-dev-orchestrate/codex-in-cloud/README.md). For each manager:
1. Make a workdir with the clones plus a `run/` folder.
2. Write `run/prompt.md` from [manager-brief.md](../../skills/astrid-dev-orchestrate/codex-in-cloud/manager-brief.md), and prepend the kickoff below.
3. Start it:
   `CODEX_EFFORT=high CODEX_MAX_THREADS=8 setsid nohup <astrid-dev>/skills/astrid-dev-orchestrate/codex-in-cloud/codex-runner.sh <workdir> <workdir>/run/prompt.md <workdir>/run 6 gpt-6-luna >/dev/null 2>&1 </dev/null &`
4. Add the run folder to `~/codex/runs.txt`.

Managers run on Luna and choose worker models by route.

**Kickoff for every manager:**

> You are the Codex manager for Plan <NN>. Load /astrid-dev-manage. Resume from `plans/<plan>/handoff.md` and `tasks.md` on astrid-dev `main`; they hold your exact branches, SHAs, task states, decisions and next action. Re-create your worktrees from the pushed branches named there. Hannah's standing rules are in `docs/handoffs/2026-11-10-orchestrator.md`, section 3; follow them. Talk to the orchestrator only through `run/to-orchestrator.md`, and read `run/to-codex.md` for its answers. Ask the orchestrator for any decision the plan doesn't settle, rather than guessing. Record task progress through small tasks-only astrid-dev PRs (the orchestrator merges `inputs.md` PRs). End each turn with `RUN-STATUS: DONE`, `RUN-STATUS: BLOCKED: <reason>` or `RUN-STATUS: WAITING`.

**Per manager:**
- **Plan 40:** do R1.1–R1.4 (the review's blocking findings), then T9 (S, keep the machine after a failed job, with its own focused review). Start from `plan40/staging-int40`. Post each new integration SHA, because Plan 34 tests on it. Push to `int/40-machine-lifetime` only after the freeze lifts, then run the CI comparison.
- **Plan 34** (GPU; pass `RUNPOD_API_KEY`; spend limit $20 total, $3.13 used):
  - **Video:** i2v, then v2v, then edit, on candidate `plan34/candidate-17acda421`.
  - **SFX:** re-run on a candidate where BOTH the install manifest AND the engine recipe pin VibeComfy af5cb429. Verify the pod's VibeComfy SHA before generating.
  - **TTS:** re-run after Plan 40 T9 lands, so a failure leaves the pod up to diagnose.
  - **Rules:** run each test as ONE waiting `generate --gpu <type>`; take a census around every rental; keep the record in PR [#260](https://github.com/banodoco/astrid-dev/pull/260).
- **Plan 32:** wait for release 12, then carry out its handoff's release-13 steps.
- **Plan 20:** wait for release 12. Then merge App `main` into App int/20, and complete its staged work per its handoff.

### The mailbox and the keep-alive

- **The mailbox:** a manager writes to `run/to-orchestrator.md`. You answer by appending to `run/to-codex.md`. Always use a QUOTED heredoc (`<<'EOF'`), or backticks in your note will run as commands.
- **Waking up waiting runs:** a run that is `waiting` resumes when you write to its mailbox. **Never relaunch a merely waiting runner.** A relaunch overwrites `runner.pid` and makes a duplicate.
- **The keep-alive:** arm `codex-hold.sh <run-dir>...` over the RUNNING runs only, with the Bash tool's `run_in_background` (timeout 7200000). Never start it with `&`, and never send its output to `/dev/null`, or you lose the message that wakes you. It exits on each mailbox write; read the message, act, and re-arm it.
- **Check-ins:** while a GPU run is live, schedule one at most 20 minutes away. Each one runs the census, checks spend, disk and statuses, does ONE thing, reports to Hannah in at most three lines, and schedules the next. When the work ends, disable them all (none is enabled now).

### Merging

- **Tasks-only progress PRs** (`plans/<plan>/tasks.md`) may be merged once their checks are green.
- **PRs that change `inputs.md` or `plan.md`:** read them, wait for green checks, merge, then write "merged (verified)" in the mailbox. Never chain that note after the merge command with `;`. Check that the merge succeeded first.
- **`gh` GraphQL is blocked here.** Use REST: `gh api repos/<owner>/<repo>/pulls -f ...` and `gh api -X PUT .../pulls/<n>/merge -f merge_method=merge`.

## State and next actions

| Plan | State | Pick up |
|---|---|---|
| [32 Generation placement targets](../../plans/32-generation-placement-targets/handoff.md) | WAITING for release 12. Local int/32 is pushed as `plan32/staging-int32` d28cac190 (the TTS and warm-reuse fixes); the rehearsal is on R12. Handoff [#346](https://github.com/banodoco/astrid-dev/pull/346) | After release 12: merge `main` in, re-prove, cut `cand/release-13` |
| [40 Machine lifetime controls](../../plans/40-machine-lifetime-controls/handoff.md) | T1–T8, T5-R1, T7b and T4 are merged; pushed as `plan40/staging-int40` b15e286b6. The review found R1.1–R1.4 (blocking). T9 has its card (D12, [#347](https://github.com/banodoco/astrid-dev/pull/347)). Handoff [#349](https://github.com/banodoco/astrid-dev/pull/349) | R1.1–R1.4, then T9, then CI after the freeze |
| [34 Real GPU proof](../../plans/34-real-gpu-proof/handoff.md) | **Passed:** image t2i, image edit, music, and the T6 wait and claim. **TTS** fails on the pod with `input_rejected`; the cause is unknown until T9 keeps the pod. **SFX** is blocked by a VibeComfy model-reference bug, fixed in #166 but not yet GPU-proven, because the re-run's two VibeComfy pins disagreed. **Video** is ready, not yet run. 18 pods were rented and all released. Candidates are pushed as `plan34/candidate-*`. Handoff [#350](https://github.com/banodoco/astrid-dev/pull/350), record [#260](https://github.com/banodoco/astrid-dev/pull/260) | Video; SFX with both pins at af5; TTS after T9 |
| [20 Zero to first image](../../plans/20-zero-to-first-image/handoff.md) | Agent and App work is staged and pushed: Agent `plan20/staging-agent` and `plan20/staging-int20`, App `plan20/staging-app`. VibeComfy #165 and #166 are open. Handoff [#303](https://github.com/banodoco/astrid-dev/pull/303) | After release 12: merge App `main` into App int/20 |
| [29 Update and release](../../plans/29-update-and-release/handoff.md) | Release 12 is in its gate, owned by session_011EzfVzreGCJJQnTuXpbib9 (its hourly check-in is disabled). Whoever takes it over starts at the [Release 12 orchestrator brief](../../plans/29-update-and-release/orchestrator-brief.md) | Its owner announces the publish |

## CI runner freeze

The freeze has been on since 11:16 UTC, 10 Nov, for release 12. Until it lifts: no CI dispatches or reruns, and no pushes to `int/**`.
- **Agent and App:** every push to an `int/**` branch starts full CI, and every App PR starts Tests. Share work on non-int branches, which start no Agent CI.
- **Runtime and VibeComfy:** CI runs on EVERY push, so don't push to them during the freeze.

**When release 12 publishes:**
1. Lift the freeze.
2. Plan 32 does its release-13 steps.
3. Plan 20 merges App `main` into App int/20.
4. Plan 40 pushes int/40 and runs its CI comparison.

## What you decide, and what Hannah decides

- **You decide,** recording a reversible orchestrator decision in the plan's `inputs.md`:
  - scope extensions a task needs to meet its card;
  - safe defaults;
  - routing;
  - ordering;
  - how to split a budget;
  - which manager owns a fix.
  Today's examples: D5 (`--gpu` replaces the saved list), D10's ordering, D11 (the default worker image), the static budget split, and fix-ownership routing.
- **Hannah decides:**
  - new scope or a new plan;
  - money beyond the agreed caps;
  - anything user-visible she has an opinion on;
  - product `main` and releases;
  - anything that undoes one of her rules.
  Bring her the choice, your recommendation, and one line on the tradeoff.

## Lessons from 10 Nov

- **Don't invent limits.** Geography, time windows, rotation and oversized GPUs were all wrong. Ask her or choose the open option.
- **Write a task card into the plan,** in `tasks.md`, `inputs.md` and `plan.md`, not just into a mailbox. Managers resume from the plan files.
- **Two plans share the number 40.** Check `plans/index.md` before numbering a new plan.
- **Find who owns the code, then route:**
  - product bugs found live go to the plan that owns that code. For example, the `--gpu` placement bug went to Plan 40, and VibeComfy model references went to Plan 20;
  - the GPU run reproduces on CPU and reports; it doesn't patch other plans' code.
- **Pods are released on any failure until T9 lands,** so a failure can't be inspected on the pod yet. Fix N's failure codes help, and T9 is the real fix.
- **The VibeComfy version is pinned in two places,** the install manifest and the engine recipe. A candidate must pin both.
- **The clones use narrow fetch refspecs,** so `git log --not --remotes` lies. Verify pushes with `git ls-remote`.
- **The classifier refuses some actions:** broad `/tmp` sweeps (delete by name instead) and writes to repos outside the session, such as runpod-lifecycle issues. Ask Hannah about those.
- **Each check-in does one thing.** Keep reports short, and give links for PRs.

## Old local branches

These were pushed under `archive/2026-11-10/<name>`, which starts no CI:
- Agent: `claude/worker-permissions`, `help-p02`, `help-pk06`;
- App: `cont-app`, `help-pk14`;
- runpod-lifecycle: `help-p2-prepin`.

**Not pushed:** Runtime `cont-runtime` (1 commit, 5 Nov, "Combine retained stop ownership and pack admission sources"). Runtime CI runs on every push, so push it after the freeze if it's wanted. (VibeComfy `claude/worker-permissions` is already contained in its GitHub branch.)

Everything else is verified on GitHub. Every task branch in the managers' clones is contained in its pushed staging branch.

## Open questions for Hannah

- **The output folder:** `generate` writes to `./outputs/<task-id>/` in the current folder, not the project. Recommendation: a small follow-up after Plan 40.
- **runpod-lifecycle issue:** "Expose Retry-After on rate-limited availability queries" is ready to file (in Plan 40's Deferred list). This session couldn't write to that repo.
- **The SessionStart hook for the Codex hold daemon.** Hannah has to add it herself:
  `"hooks": {"SessionStart": [{"hooks": [{"type": "command", "timeout": 10, "command": "setsid nohup <astrid-dev>/skills/astrid-dev-orchestrate/codex-in-cloud/codex-hold-daemon.sh >/dev/null 2>&1 </dev/null & exit 0"}]}]}`

## Follow-ups to file when Plan 34's first run is DONE

- RLock in `wait_ready`.
- A prepare-only/doctor mode.
- A deterministic tie-break between equal prices.
- The roughly 70 s window between quote and claim.
- The i2v `lease_lost`.
- Runtime recovery of orphaned tasks.
- Custom Runtime paths.
- Secure Cloud only.
- The VibeComfy target-schema interface.
- G1 isolation.
- An engines-install confirm flag.
- The slow shard 5.
- `machines release` timing out at 30 s.
- Output naming and folder.
- A session-level keep.
- The SDK disconnect not cancelling a waiting Runtime task.
- Lifecycle Retry-After.
- The 38 VibeComfy templates with prefixed model pickers not proven by #166.
- An audit of credentials and fixtures, plus a contract-test rule from a real producer to its consumer.
- Renumber one of the two Plan 40s.
- One source for the VibeComfy pin (manifest vs engine recipe), owned by Plan 29.
