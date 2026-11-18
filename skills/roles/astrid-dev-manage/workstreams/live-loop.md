# Workstream: run a loop plan

Use when the plan is a [loop plan](../../../shared/glossary.md): its end state is known, its tasks can't be written up front, and its `tasks.md` ends in one standing loop card. Everything in [whole project](whole-project.md) still applies (progress, decisions, dispatch); this adds the round. The [run contract](../../../shared/run-contract.md) governs routes, proof and review; it is not restated here.

## Roles

- **Coordinator** (the manager session): keeps the judgment. Reads every round row and picks the fixes. Treats what Codex and the strategist return as evidence to check.
- **Execution runs on Codex:** the heavy lifting, `N` normally and `X` for a hard fix, each bound to a model and effort in the run's `run.yaml`. Run in the background, one worktree per fix:
  `codex exec -m <model from run.yaml> --skip-git-repo-check -C <dir> -s workspace-write -o <scratch>/<name>.txt "<brief>" < /dev/null`
  Add `-c model_reasoning_effort='"<effort from run.yaml>"'`.
- **Strategist:** the run's high-judgment advisor binding, read-only (`-s read-only`), consulted on strategy each round. Its advice is evidence, not a verdict; it tends to over-engineer, so ask it what to remove first.

## The round

1. **Run the scenario set live,** against the real installed stack, over its public interface only (the browser or the public API), never in-process.
2. **Record a round row** in the plan's `rounds.md`: what saved; what was refused, with the reason shown; timings; anything that vanished; the stack's versions.
3. **Ask the strategist:** give it the row and the previous rows, not your conclusion.
4. **Pick the fixes.** Each is one failing scenario, a cause, and the smallest change at its source.
5. **Fix** each as an ordinary [Iterate](../../../capabilities/astrid-dev-iterate/SKILL.md) run, a PR into the plan branch, with the failing live scenario as its red test.
6. **Rebuild the stack and rerun** from step 1.

Append each round's rows, picks and PRs under the loop card in `tasks.md`; progress PRs follow [whole project](whole-project.md#progress-is-always-current).

## Stop

Stop when the plan's end state holds on two consecutive rounds, or when a round finds nothing new and the remaining refusals are real clashes. Stop and ask the owner when three rounds in a row fix nothing, a floor below (disk) is reached, or the end state needs a design change bigger than a card.

Each round also writes **plan deltas**: what the live evidence changes in the follow-up plans (a task to drop, add, re-estimate or renumber). They go in `rounds.md`, one list per round, and the manager carries them into those plans' PRs at the end.

## Hygiene

- A fresh browser profile for every run, deleted afterwards. Headless profiles and stack copies are what filled the disk twice on 18 November.
- Check free disk before each round and stop below the floor the plan names.
- Never edit the owner's timelines or projects: scenarios run on a fixture built in a sandbox project.
