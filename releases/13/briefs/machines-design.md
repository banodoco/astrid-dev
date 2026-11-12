# Machines: declare once, claim explicitly, generate on a named machine

## Owner decisions (Hannah, 12 Nov 2026, verbatim where quoted)
- **O1. Declare once.** "We shouldn't have to declare things over and over again." Preferences are stored once (set the first time, or with `machines setup`) and documented in the skills. They are defaults that can be overridden at command time and changed later.
- **O2. Claiming is separate from generating.** "We probably shouldn't even have this on generate; generate should probably just be to use an existing machine." Claiming uses the stored preferences; any of them can be overridden at claim time.
- **O3. `generate` never claims automatically.** "No, machines shouldn't claim automatically."
- **O4. No consent flag.** "The consent paid, we don't need that ... that's just bureaucracy ... they've already rented the machine."
- **O5. Named machines.** "Should machines have names, so we can say `astrid generate … bjork`, and it generates with the machine that has that name."
- **O6. Jobs queue on the machine.** 20 generations sent to one machine run back to back on it.
- **O7. No hard datacenter pin.** "This shouldn't necessarily pin to one data center. We should be able to override that."
- **O8. Visibility.** People can view the machine and what's actually happening on it.
- **Open, no ruling yet:** whether a claimed machine ends on its idle timer (`machines keep` extends it) or stays up until released.

## Target experience (what "it all just works" means)
```
astrid machines setup                      # once: GPUs, storage/datacenter, budget, idle time (defaults)
astrid machines claim [--name bjork] [--gpu …] [--datacenter …] [--for 2h] [--max-usd …]   # uses prefs; flags override
astrid machines                            # list: name, GPU, DC, state, current job, queue, time left, cost
astrid machines show bjork                 # what is happening on it now: job, queue, logs, expiry, cost
astrid generate image "…" --machine bjork  # queues on bjork; no paid flags; with one machine, --machine optional
astrid machines keep bjork --for 2h        # extend
astrid machines release bjork
```
With no machine, `generate` refuses with one line: run `astrid machines claim`.

## What exists today (Release 13 candidate `r13/batch6`, `/home/user/wt/c-b6`)
- **Preferences:** `machines setup` saves `RunPodPreferences` (`astrid/packs/runpod/target_selection.py:171`): ordered GPUs, volume/datacenter, image, idle retention, `budget_cap_usd`. They are stored in Runtime per-user settings `generation.machines.runpod` (`astrid/core/generation/settings.py:3`).
- **Claim:** `astrid machines claim` already exists (`astrid/core/machines_cli.py:251`; RunPod skill `astrid/packs/runpod/docs/SKILL.md:176`). Today it needs `--max-hourly-usd`, `--max-usd`, `--for` and `--consent paid`.
- **Generate also claims:** `astrid generate … --placement runpod` claims or reuses a machine and requires `--max-hourly-usd`, `--max-usd`, `--preparation-seconds`, `--execution-seconds`, `--idle-seconds` and `--consent paid` (validators: `astrid/sdk/generation.py:257,315,321`; `astrid/packs/runpod/adapter.py:377,388`; `astrid/packs/runpod/target_selection.py:335,476,777`).
- **Pinning to a machine:** SDK `Placement.machine` can already pin a live lease (`astrid/core/generation/placement.py:250`), but the CLI does not expose it.
- **Queueing:** one host GPU queue (Runtime `claim_task`, executor concurrency 1, GPU resource key), plus warm reuse when custody matches (`astrid/packs/runpod/machine.py:22`). It is not a named per-machine queue.
- **Keep-warm** (just landed, `r13/keep-warm` `9e7b2a48`): failed jobs and failed preparation keep a reachable machine (`idle` / `stale_after_failure`); `machines` rows show cost, expiry and last outcome.
- **Paid-consent rules being changed** are Plan 40 decisions D1–D13: `/home/user/wt/dev-plan49/plans/40-machine-lifetime-controls/inputs.md`.
- **A code map from an earlier read-only design pass:** `/home/user/wt/briefs/wave3/design-declare-once.log` (last 120 lines).
- **Live usability evidence from today's run:** `/home/user/wt/briefs/wave3/usability-log.md`.
  - no default project on a fresh install;
  - repeated flags;
  - no balance view;
  - `machines` vs `runpod` naming;
  - a silent CLI during a stock wait while the host logs "no stock yet";
  - a volume pinning to an empty datacenter.

## Constraints
- **Many providers and engines:** nothing RunPod-specific in core; RunPod is one provider behind `machines`.
- **Spend safety stays real** (without ceremony):
  - the budget cap and idle and paid expiry are enforced by the owning host;
  - host shutdown still releases (Plan 40 D12/D13);
  - a forgotten machine must not bill all night.
- **Every failure or wait is understandable from the product.**
- **Structure over patches:** remove paths rather than add parallel ones.
