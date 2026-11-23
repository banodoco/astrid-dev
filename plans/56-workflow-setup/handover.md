# Handover: Plan 56, workflow set-up (Release 15)

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Fixtures](evidence/fixtures/README.md)

For the Plan 56 orchestrator and the Release 15 Lead. Read this once, then work from `tasks.md`.

## What this is, in three lines

Any ComfyUI workflow, on the person's own ComfyUI, a managed one or a rented machine, either runs or stops with a named next step. A node pack Astrid has not reviewed installs after one informed yes (`--consent code=<token>`), and the saved workflow remembers it. Plan 90 is the follow-up (exact-plan digest, `--apply`, trust list); it is not in this lane.

## Roles

| Role | Who | Does |
| --- | --- | --- |
| Lead | `session_011EzfW1gtAhRQwk8pgJMzhG` | Reads, decides and rules. Confirms the landing gate, gives CI slots, answers the orchestrator. Sends route `N` workers (Luna, or Haiku) to explore and runs the hourly parallelism pass; never gives them a verdict ([lane workstream](../../skills/roles/astrid-dev-lead/workstreams/lane-orchestrators.md)). |
| Orchestrator | `session_011EzfW2WBWyoHTBJggpfEDm`, Claude, route X | Answers for the plan finishing. Hosts one Codex manager, runs the hourly parallelism pass, reports to the Lead hourly, merges its own plan-branch and record PRs. |
| Codex manager | Terra, route X, effort high | Works through the cards by route; ticks `tasks.md`. |
| Workers | by card route: Luna N, Terra X, Sol S, Astra T and reviews | One card each. |
| Owner | Hannah | WS-L, publishing, paid or personal-machine actions, D10–D12 before landing. |

## First actions

1. Check the Run start in [inputs.md](inputs.md) is on astrid-dev `main` (it must not say "Pending"). If it does, stop and tell the Lead.
2. Codex check: `codex exec --skip-git-repo-check -s read-only 'Reply ok.'`. If it fails, the owner must sign in; otherwise run cards on Claude subagents by the same routes and say so.
3. Attach astrid-dev, astrid-agent and VibeComfy. The environment's setup script covers only repos present when the container was built, so run `/opt/astrid-dev/env/agent-setup.sh` and the VibeComfy setup by hand.
4. Check heads with `git ls-remote`: astrid-agent `release/15/main` `045064b6`; VibeComfy `release/15/main` `48b5fa9e` but **VibeComfy `main` and the Agent's pin are `c0e910ca`**, which includes Plan 81's work.
5. Cut `release/15/plan-56`: astrid-agent from `release/15/main`; VibeComfy from `c0e910ca`. Record both in `releases/15.md` Branches and in `inputs.md` Source identities. Set `plan.md` Status to active and Owner to the orchestrator.
6. Bindings: record in a `run.yaml` the model IDs this login accepts and an effort per route, in the shape of [Plan 77's handover](../77-saving-holds-on-a-heavy-timeline/handover.md#runyaml). IDs are not written in repo files; "Codex Astra" means the newest ID the login accepts.
7. Day one cards: LE-1a, WS-7a, LE-2a and WS-6a, plus phase 0 (WS-0a to WS-0e, WS-0g; never WS-0a and WS-0d at once), LE-4, LE-6 and LE-15. When LE-1a, WS-7a and LE-2a have merged, check their shapes yourself before the cards built on them start.

## How the code is tested

- Agent tests build VibeComfy at the Agent's own pin (`env/agent-setup.sh`, `VIBECOMFY_ENGINE_REVISION`). A card that changes both repos is proved only after the Agent's `release/15/plan-56` points at the plan-56 VibeComfy head, by a generator-only pin commit (`scripts/vibecomfy_pin.py`). That is yours to do; pins into `release/15/main` are the Lead's.
- Proofs run on the **CPU stand-in target** defined in [evidence/fixtures/README.md](evidence/fixtures/README.md): a fake ComfyUI `object_info` server and a recorded-answer fake pod runner. No GPU, no SAM weights, no rented machine. The real SAM run is WS-L, the owner's, after R.
- Never dispatch hosted CI. Post `READY-CI` on the mailbox and wait for the Lead's slot. The baseline for the Agent's compared run is [releases/15/evidence/agent-ci-baseline-8807f820](../../releases/15/evidence/agent-ci-baseline-8807f820/README.md).

## Order and the real conflicts

The waves and the conflict map are in [tasks.md](tasks.md) (Parallel note) and come from the Opus parallelism check of 23 November 2026. In short: contract cards first (LE-1a, WS-7a, LE-2a); then up to four writers per repository on cards that do not share a file; `cli.py:_workflow_command` (nine writers) and `entries.py:target_schema` (seven) are held by one worker each; `native_failure_diagnostic` is LE-6 then LE-14; `_install.py` is WS-0c, WS-7b, LE-2b, LE-13, LE-14 in that order. RS1 (Codex Astra) is after WS-7b and LE-2b and gates LE-13, LE-17 and WS-L. R is up to two Astra rounds, the second verifying the first's fixes.

## Every hour

Run the parallelism pass ([lane-orchestrator workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/lane-orchestrator.md)), then report to the Lead: done, in progress, writers that ran, ready cards that waited and why, decisions taken, the one thing you are least sure about. Keep a hosting `send_later` at most 20 minutes away while the Codex manager runs.

## Traps

- Never touch the owner's install at `/home/user/work/recast/install-8` (a live Runtime uses it).
- The SAM pack's `install.py` is never run by Astrid: that is a rule of this plan, enforced by `test_install_script_never_executed`.
- A step that is manual must still say so in an `instruction{step, then_argv}`: the plan's rule is that no handled state ends without a next step, enforced by `test_setup_next_steps.py`.
- Plan 77 and Plan 89 change the save path; re-check overlap only at landing.

## Where the evidence is

[review.md](review.md) (the first Astra review); [evidence/opus-report-1.md](evidence/opus-report-1.md) (the first golden-path report); the design discussion is in [issue 1731](https://github.com/banodoco/astrid-dev/issues/1731) and its three comments; the second Astra critique, the Fable UX review and the Opus parallelism and handover checks are summarised in [inputs.md](inputs.md) (the long raw outputs stay with the planning session).

## Sibling lanes

Plan 81 `session_011EzfW2Ut856AFGZS8ZamHU`; Plans 40 and 78 `session_011EzfVz6RTgoXjxNDgJP47L`; Plan 77 `session_011EzfW1FXS3o7GFnNSB7cZS`; Plan 84 `session_011EzfW1Df4SCkBoafGdR1di`. Agree order with them directly when a card touches their code.
