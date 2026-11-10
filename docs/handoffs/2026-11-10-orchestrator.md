# Orchestrator handoff — 10 Nov 2026

A new orchestrator, on any machine, takes over from this file and GitHub alone. It replaces the cloud session https://claude.ai/code/session_011EzfVz8zzHLnUqSqMnGUCT. Each plan also has its own `handoff.md` with exact SHAs and its next action. Read those after this file.

## How to resume

1. Load [astrid-dev-orchestrate](../../skills/astrid-dev-orchestrate/SKILL.md). You are the orchestrator: you equip managers, relay between them, take owner decisions and merge what needs you. You don't trace code yourself.
2. Start one Codex manager per running plan, using [codex-in-cloud](../../skills/astrid-dev-orchestrate/codex-in-cloud/README.md) and [manager-brief.md](../../skills/astrid-dev-orchestrate/codex-in-cloud/manager-brief.md). Point each one at its plan's `handoff.md`. Managers use `/astrid-dev-manage`.
   - **Models (Codex, ChatGPT sign-in):** Luna `gpt-6-luna` for normal tasks; Terra `gpt-6.1-terra`, Sol `gpt-6.1-sol` and Astra `gpt-6-astra` by route. `gpt-6.1-luna` is not supported.
   - **Advisor:** ask Astra when you're stuck, with `codex exec -m gpt-6-astra -s read-only --skip-git-repo-check "<q>" </dev/null`. stdin MUST be `/dev/null`, or it hangs.
3. **The machine needs:** `RUNPOD_API_KEY` in the environment (never print or store it); a Codex login; `gh` with push access to banodoco/astrid-dev, astrid-agent, astrid-app and VibeComfy. The managers' worktrees are re-created from the pushed branches listed in each `handoff.md`.
4. While a GPU run is live, schedule a check-in at most 20 minutes apart. Each check-in runs the census, checks spend and disk, and does ONE thing.

## Owner rules (Hannah, 9–10 Nov). These stand until she changes them.

- "KEEP IT MOVING NO MATTER WHAT, think your way around any obstacles. Accept no excuses."
- **Orchestrate, don't do.** Farm work out to managers and to Codex sub-agents. No Claude Agent-tool sub-agents.
- **GPU acquisition:**
  - Every test is ONE product command that waits for capacity itself (Plan 40 T6; proven live twice).
  - No time windows, no rotating between tests, and NO geographic filters ("STOP STUPID GEO RESTRICTIONS").
  - The user defines the GPU(s) in their own order, the storage and optionally the datacenter. Price only breaks ties (D10).
  - Use the cheapest adequate GPU, never an A100 for audio (24 GB is enough).
- **A failed job must NOT release the pod.** It stays idle within the consented idle and paid limits (Plan 40 T9, decision D12; not yet built).
- **Parallel GPU cells are allowed.** Each runs in its own isolated install and data root, with a static budget split and a margin.
- **Disk:** clear space aggressively and do it yourself. Safe to delete: named caches and clean worktrees whose commits are on a remote. Never delete unpushed work.
- **Money:** this GPU validation run may spend up to $24 and stops at $20. Take a census before and after every rental, and release every pod. Report "spent $X of the $20 cap".
- **Guardrails:**
  - no force-push;
  - never expose a secret;
  - no App `main` or install-manifest change without Plan 29's release owner;
  - VibeComfy changes ride with release 13 through the pin, with no VibeComfy `main` merge.
- **Approved (10 Nov):**
  - the release-12 landings go via release 13 (Plan 20 P1.5 and Plan 32);
  - P3.3b: Plan 20 fixes the default-skill sync, with timeline as a default skill;
  - drop `int/**` from heavy CI push triggers after release 12;
  - P2.4 App wording.

## State of each plan

| Plan | State | Where to pick up |
|---|---|---|
| [32 Generation placement targets](../../plans/32-generation-placement-targets/handoff.md) | WAITING for release 12. Local int/32 is pushed as `plan32/staging-int32` d28cac190 (TTS + warm-reuse fixes). Handoff [#346](https://github.com/banodoco/astrid-dev/pull/346) | Merge `main` into int/32, re-prove, cut `cand/release-13` |
| [40 Machine lifetime controls](../../plans/40-machine-lifetime-controls/handoff.md) | T1–T8, T5-R1, T7b and T4 merged; pushed as `plan40/staging-int40` b15e286b6. The review round found R1.1–R1.4 (blocking). T9 (keep the pod on failure, D12) has its card. Handoff [#349](https://github.com/banodoco/astrid-dev/pull/349) | R1.1–R1.4, then T9 (S, own review), then CI after the freeze |
| [34 Real GPU proof](../../plans/34-real-gpu-proof/handoff.md) | **Passes:** image t2i, image edit, music, and the Plan 40 T6 wait and claim (live, twice). **TTS** fails on the pod with `input_rejected`; the cause is unknown until T9 keeps the pod. **SFX** is blocked by a VibeComfy model-reference bug, fixed in [#166](https://github.com/banodoco/VibeComfy/pull/166) but not yet GPU-proven: the re-run's install manifest pinned af5cb429 while the pod's engine recipe still pinned e65f4941. **Video** is not run; the fixtures are ready. $3.13 spent; all 18 pods released. Candidates pushed as `plan34/candidate-*`. Handoff [#350](https://github.com/banodoco/astrid-dev/pull/350), record [#260](https://github.com/banodoco/astrid-dev/pull/260) | Video on candidate 17acda421; SFX on a candidate with BOTH pins at af5; TTS after Plan 40 T9 |
| [20 Zero to first image](../../plans/20-zero-to-first-image/handoff.md) | Agent and App work staged and pushed (`plan20/staging-*`). VibeComfy [#165](https://github.com/banodoco/VibeComfy/pull/165) (region text removed) and [#166](https://github.com/banodoco/VibeComfy/pull/166) (strict model references) are open. Handoff [#303](https://github.com/banodoco/astrid-dev/pull/303) | Wait for release 12, then merge App `main` into App int/20 |
| [29 Update and release](../../plans/29-update-and-release/plan.md) | Release 12 in progress, owned by session_011EzfVzreGCJJQnTuXpbib9 | Its owner announces the publish |

## CI runner freeze

The freeze has been on since 11:16 UTC, 10 Nov, for release 12. It means no dispatches or reruns, and no pushes to `int/**`, because each one starts full CI. Share work on non-int branches (`plan32/staging-int32`, `plan40/staging-int40`, `plan20/staging-*`, `plan34/*`), which start no Agent CI.

**When release 12 publishes:**
1. Lift the freeze for every plan.
2. Plan 32: merge `main` into int/32, re-prove, then cut `cand/release-13` through the [Release skill](../../skills/astrid-dev-release/SKILL.md). The candidate takes int/32, Plan 20 P1.5, Plan 40, the CI-trigger prep, and VibeComfy #165 and #166 via the pin.
3. Plan 20: merge App `main` into App int/20.

## Old local branches (archived)

The orchestrator's clones held a few branches from 4–8 November that were never pushed. They're probably superseded. They were pushed unchanged under `archive/2026-11-10/<name>`, which starts no CI:
- Agent: `claude/worker-permissions`, `help-p02`, `help-pk06`;
- App: `cont-app`, `help-pk14`;
- runpod-lifecycle: `help-p2-prepin`.

One branch is NOT pushed: Runtime `cont-runtime`, a single commit "Combine retained stop ownership and pack admission sources". Runtime CI runs on every push, so it was left for after the freeze. Push it then if it's still wanted. The same applies to VibeComfy `claude/worker-permissions`, a single commit from 8 Nov, "Allow .claude in the root-clean allowlist". VibeComfy CI also runs on every push.

Everything else is verified on GitHub. Every task branch in the managers' clones is contained in its pushed staging branch: `plan40/staging-int40`, `plan32/staging-int32`, and `plan20/staging-agent` / `plan20/staging-int20`.

## Open questions for Hannah

- `generate` writes outputs to `./outputs/<task-id>/` in the current folder, not the project. Recommendation: a small separate follow-up after Plan 40.
- Writing to `banodoco/runpod-lifecycle` was refused in this session. The issue "Expose Retry-After on rate-limited availability queries" is recorded in Plan 40's Deferred list, ready to file.
- The SessionStart hook for the Codex hold daemon. Hannah has to paste it herself:
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
- The 38 VibeComfy templates with prefixed model pickers that aren't proven by #166.
- An audit of credentials and fixtures, plus a contract-test rule from a real producer to its consumer.
- Two plans share the number 40 (`40-contribution-discovery` and `40-machine-lifetime-controls`). Renumber one.
- The VibeComfy version is pinned in two places, the install manifest and the engine recipe (`engine_recipe.load_recipe`, read by `managed_sources._pins`). They can silently disagree. For Plan 29: derive one from the other, or check that they match at install.
