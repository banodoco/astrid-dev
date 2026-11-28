# Agent-test run — 2026-11-28 — second run

**Date:** 2026-11-28
**Commit:** 31a1a8c9
**Run by:** the planning session `session_011EzfW1gtAhRQwk8pgJMzhG`, with actors on each case's own route and Opus judges
**Trigger:** the owner's rulings on closing: the lane hands each ready plan to the Lead, the Lead merges into `release/<N>/main`, whoever runs a level closes it, and progress PRs change only when state does
**Cases:** h3-orchestrator-start, h3-orchestrator-hands-plan, h3-orchestrator-closes, h3-orchestrator-silent-manager, h3-chat-unit, h3-claude-worker-fallback, manager-starts-worker, plan-manager-takes-worker

## Governing finding

The documents now hold up inside every role tested; what fails is the product repositories underneath them. A chat's unit cannot be proved, because astrid-agent runs no CI on plan-branch PRs, and a worker session cannot push, because astrid-agent's allow rules permit only `plan33/` pushes.

## Round 1

| Case | Verdict | Misses | Cause |
| --- | --- | --- | --- |
| h3-orchestrator-start | pass | — | on `S` at `31a1a8c9`; found that `ci.yml` runs pull requests only into `release/*/main` |
| h3-orchestrator-hands-plan | fail | E1 | on `S`: opened Plan 66's completion PR as a draft, because the brief, Plan 66's closing review and the contribution workflow disagree on when it opens (doc-gap), at `31a1a8c9` |
| h3-orchestrator-closes | pass | — | on `S` at `31a1a8c9` |
| h3-orchestrator-silent-manager | pass | — | on `S` at `31a1a8c9` |
| h3-chat-unit | pass | — | on `S` at `31a1a8c9`; found the same CI gap: the proof the brief names cannot run |
| h3-claude-worker-fallback | pass | — | on `S` at `31a1a8c9`; found that `.claude/settings.json` allows `git push` only for `plan33/` |
| manager-starts-worker | fail | E3 | on `S`: the case expected call-site edits the ruling only permits (case defect); the actor worked in its creator's checkout, since nothing gives a subagent its own worktree (doc-gap), at `31a1a8c9` |
| plan-manager-takes-worker | pass | — | on `X` at `31a1a8c9` |

Six of eight pass. Both fails are fixed below.

## Synthesis

1. **What the product repository allows decides how a unit is proved and pushed.** Kind: missing parent (rule 4, host, one level down). The brief assumed CI on every unit PR and a push rule for every worker; neither exists at the base. Settles: the CI finding in h3-orchestrator-start, h3-chat-unit and h3-claude-worker-fallback, and the push finding in h3-claude-worker-fallback. Fix: the owner's choice of how chat units are proved, and a `p*/` push rule in astrid-agent (owner questions below).
2. **A subagent shares its creator's machine, so it needs its own worktree and a final status word.** Kind: missing parent. Settles: manager-starts-worker's worktree finding and its invented status. Fix: start-session step 7 and the brief's subagent start message.
3. **A plan's completion PR opens ready for review once the Lead merges the plan; a later review that covers it is named under Unproven.** Kind: precedence. Settles: h3-orchestrator-hands-plan E1. Fix: the brief's Merges.
4. **Findings that recurred from earlier runs:** a unit whose author nothing can stop waits on its branch (h3-orchestrator-silent-manager, and the first run's round 8); the first progress PR's `inputs.md` lines are in the self-merge rule (the same two runs). Fix: run contract item 8, the brief's Merges.

## Changes

- `8f64d93b`: the lane makes each plan ready and the Lead merges it; a done lane needs its plans done (the `lane-briefs` check).
- `920942c9`: progress PRs only when state changes; a worker runs its card start to finish; a subagent's focused tests are its creator's re-run; late events wait.
- `d385d997`: the H3 brief cites the general rules instead of restating them; the golden path lists only the parent rules; start messages name the worker kind and the one ruled edit.
- `da3400f9`: synthesis 2, 3 and 4; the brief's Scope decision value and push access.

## Round 2

Not run: the remaining misses wait on the owner's two product-repository decisions.

| Case | Verdict | Misses | Cause |
| --- | --- | --- | --- |

## Owner questions

| Question | Answer |
| --- | --- |
| astrid-agent runs no CI on plan-branch PRs. How is a chat's unit proved: A, dispatch full CI per unit; B, a small focused-test workflow (recommended); or C, a worker per proof? | |
| May astrid-agent (and VibeComfy) allow `git push` for `p*/` branches, so a worker session can push its unit? | |
| May one CI run on `release/16/main` at the shared cut SHA serve as the baseline for all four plan branches? | |
| A lane spanning two releases: does its closing note go to both Leads, or the last one? | |

## Next

- Answer the owner questions, write each answer in its home, then run round 2 on the cases that touch it.
- A responsibility map: one table of levels, states, who opens, runs, merges and closes each, with its branch per repository, defined in `scripts/lifecycle.py` and generated as a page.
