# Handover: Plan 56, workflow set-up (Release 15)

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Fixtures](evidence/fixtures/README.md)

For the Plan 56 orchestrator and the Release 15 Lead. Read this once, then work from `tasks.md`.

## What this is, in three lines

Any ComfyUI workflow, on the person's own ComfyUI, a managed one or a rented machine, either runs or stops with a named next step. A node pack Astrid has not reviewed installs after one informed yes (`--consent code=<token>`), and the saved workflow remembers it. Plan 90 is the follow-up (exact-plan digest, `--apply`, trust list); it is not in this lane.

## Roles

| Role | Who | Does |
| --- | --- | --- |
| Lead (accountable) | `session_011EzfW1gtAhRQwk8pgJMzhG` | Reads, decides and rules; writes and orders packets; reviews and merges packet PRs into `release/15/plan-56`; runs RS1 and R with Codex Astra; confirms the landing gate; gives CI slots. Sends route `N` workers (Luna, or Haiku) to explore and runs the hourly parallelism pass; never gives them a verdict ([workstream](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md)). |
| Orchestrator | `session_011EzfW2WBWyoHTBJggpfEDm`, Claude | Starts one fresh ChatGPT session per packet in the owner's account, in the mode its Route sets (N High, X Extra High, S Pro); checks every open packet hourly; resumes or replaces stalled sessions; relays between Lead and packet sessions; posts one STATUS an hour. Does not merge or edit the repository ([workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md)). |
| Packet session | a fresh ChatGPT session per packet | Implements and proves one packet ([chatgpt-packet workstream](../../skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md)); opens PRs; posts STATUS and BLOCKED; never merges, ticks `tasks.md` or takes a second packet. |
| Owner | Hannah | Pastes the Orchestrator launch message; WS-L, publishing, paid or personal-machine actions; D10–D12 before landing. |

The board, mailbox ([#1757](https://github.com/banodoco/astrid-dev/issues/1757)), startup checks and dispatch queue are in [releases/15/run.md](../../releases/15/run.md#plan-56-dispatch); the packets are in [releases/15/packets/](../../releases/15/packets/).

## First actions (Lead, then Orchestrator)

1. **Lead:** confirm the Run start in [inputs.md](inputs.md) and the board section are on astrid-dev `main`; cut `release/15/plan-56` (astrid-agent from `release/15/main` `045064b6`; VibeComfy from `c0e910ca`, which is VibeComfy `main` and the Agent's pin, not `release/15/main` `48b5fa9e`); record both in `releases/15.md` Branches and in `inputs.md` Source identities; set `plan.md` Status to active and Owner to the Lead.
2. **Lead:** answer the Orchestrator's startup-check STATUS with a DECISION. Bindings: record the models this login accepts and an effort per route in a `run.yaml` in the shape of [Plan 77's handover](../77-saving-holds-on-a-heavy-timeline/handover.md#runyaml); model IDs stay out of repo files ("Codex Astra" means the newest ID the login accepts).
3. **Orchestrator:** run the startup checks, then dispatch P56-01 alone; when its early STATUS proves a packet session can push, open a PR and comment, dispatch P56-02 to P56-04.
4. **Lead, ongoing:** post a heartbeat STATUS at least every 90 minutes; keep the mailbox cursor in the board; after each merge post DONE and open the `tasks.md` progress PR; copy the Orchestrator's STATUS into the board and move Blocked packets to Ready; add recurring rulings to Standing rulings; run `python3 scripts/release_branches.py check 15`; schedule your own check-ins on a scheduler that outlives your machine; tell the owner when #1755 is merged so she pastes the launch message.
5. **Lead:** when P56-01 merges, check the three shapes yourself (the fix schema, the `extra.nodes` shape, the approval record) before P56-05, P56-06 and P56-07 start.

## How the code is tested

- Agent tests build VibeComfy at the Agent's own pin (`env/agent-setup.sh`, `VIBECOMFY_ENGINE_REVISION`). A card that changes both repos is proved only after the Agent's `release/15/plan-56` points at the plan-56 VibeComfy head, by a generator-only pin commit (`scripts/vibecomfy_pin.py`). The Lead does it; pins into `release/15/main` are also the Lead's.
- Proofs run on the **CPU stand-in target** defined in [evidence/fixtures/README.md](evidence/fixtures/README.md): a fake ComfyUI `object_info` server and a recorded-answer fake pod runner. No GPU, no SAM weights, no rented machine. The real SAM run is WS-L, the owner's, after R.
- A packet session never dispatches hosted CI: it posts `READY-CI` on the mailbox and waits for the Lead's slot. The baseline for the Agent's compared run is [releases/15/evidence/agent-ci-baseline-8807f820](../../releases/15/evidence/agent-ci-baseline-8807f820/README.md).

## Order and the real conflicts

The waves and the conflict map are in [tasks.md](tasks.md) (Parallel note) and come from the Opus parallelism check of 23 November 2026. In short: contract cards first (LE-1a, WS-7a, LE-2a); then up to four writers per repository on cards that do not share a file; `cli.py:_workflow_command` (nine writers) and `entries.py:target_schema` (seven) are held by one worker each; `native_failure_diagnostic` is LE-6 then LE-14; `_install.py` is WS-0c, WS-7b, LE-2b, LE-13, LE-14 in that order. RS1 (Codex Astra) is after WS-7b and LE-2b and gates LE-13, LE-17 and WS-L. R is up to two Astra rounds, the second verifying the first's fixes.

## Every hour

The Orchestrator reads the mailbox, checks every open packet, runs the parallelism pass ([orchestrator rule](../../skills/roles/astrid-dev-orchestrate/workstreams/lane-orchestrator.md); here the unit is the packet: start every Ready packet with no unmet dependency and no file conflict with a Running one, up to the cap), resumes or replaces stalled sessions, and posts one STATUS. The Lead does the same pass with `N` workers each check-in and rules on the result.

## Traps

- Never touch the owner's install at `/home/user/work/recast/install-8` (a live Runtime uses it).
- The SAM pack's `install.py` is never run by Astrid: that is a rule of this plan, enforced by `test_install_script_never_executed`.
- A step that is manual must still say so in an `instruction{step, then_argv}`: the plan's rule is that no handled state ends without a next step, enforced by `test_setup_next_steps.py`.
- Plan 77 and Plan 89 change the save path; re-check overlap only at landing.

## Where the evidence is

[review.md](review.md) (the first Astra review); [evidence/opus-report-1.md](evidence/opus-report-1.md) (the first golden-path report); the design discussion is in [issue 1731](https://github.com/banodoco/astrid-dev/issues/1731) and its three comments; the second Astra critique, the Fable UX review and the Opus parallelism and handover checks are summarised in [inputs.md](inputs.md) (the long raw outputs stay with the planning session).

## Sibling lanes

Plan 81 `session_011EzfW2Ut856AFGZS8ZamHU`; Plans 40 and 78 `session_011EzfVz6RTgoXjxNDgJP47L`; Plan 77 `session_011EzfW1FXS3o7GFnNSB7cZS`; Plan 84 `session_011EzfW1Df4SCkBoafGdR1di`. Agree order with them directly when a card touches their code.
