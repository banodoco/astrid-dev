# Machines plan (Fable critique, 12 Nov; manager-accepted)

**Principle:** the claim is the spend authority; a job is just work on a machine someone already rented.

**Owner decisions:** O1–O8 in `machines-design.md`.

**Manager ruling on the open question (REVIEW, owner may overrule):**
- The idle timer is the only lifetime mode.
- Idle counts only while nothing is running or queued on the machine.
- `machines keep NAME --for` extends it; `--idle never` replaces `--until-release`.
- Everything is still bounded by the machine's budget cap (Plan 40 D1).

## Deletions
- **Paid flags on generate:** `--max-usd`, `--max-hourly-usd`, `--deadline`, `--offer-digest`, the three `--*-seconds`, `--capacity-timeout`, `--no-wait-for-capacity`, and consent scope `paid` (`astrid/core/generation/cli.py:85-98`). `--consent user_env` stays.
- **The SDK's paid controls:** `_runpod_paid_controls` and the paid half of `_runpod_placement_policy` (`astrid/sdk/generation.py:257-345`).
- **The generate-claims path,** the allocate branch reached from `RunPodMachine.claim` (`astrid/packs/runpod/machine.py:553-640`). A job only attaches to a live lease.
- **The consent flag and prompt on claim** (`astrid/core/machines_cli.py:259-263,536`). Print the policy line, then claim.
- **`--until-release` as a mode** (`machines_cli.py:516`).

## Merges
- **Budget concepts, seven down to two:** a budget per machine, plus an idle time.
  - `--for` and `--max-usd` derive each other (rate × time).
  - The hourly ceiling defaults to the quoted rate.
  - `keep NAME --for 2h` needs no `--max-usd`.
- **`--for` means lifetime everywhere;** idle is a preference.
- **`--machine` implies the placement.**

## Reuse
- **Names:** a `name` field on the lease record and `lease_row` (`machine.py:1354`). `Placement.machine` (`placement.py:71,250`) and the host pin check (`machine.py:590-599`) accept a name or an id. Auto-generate a name when `--name` is omitted.
- **Queue:** in Release 13 there is one lease per account, so the Runtime queue at concurrency 1 with the `gpu` key is the per-machine queue. Later, use a `machine:<id>` resource key.
- **Show:** lease row, plus progress, failure logs, and Runtime tasks filtered by `policy.machine`.

## Volume and datacenter
- Preferences hold an optional volume and an optional datacenter. A volume implies its datacenter as a fact, not a pin.
- `claim --datacenter X` wins: if X differs from the volume's datacenter, the claim uses ephemeral disk with a one-line notice. Today this refuses (`generation.py:295-300`).
- The stock wait names the cause and the override.

## Preferences
- They stay at `generation.machines.<provider>`.
- On the first claim, missing preferences are prompted for on a TTY. Without a TTY, the claim's flags are saved as defaults, with a one-line notice.
- `machines setup` is only the editor.

## Tasks (sizes: N Luna, X Terra, S Sol, SS Astra, T Opus)
| id | Outcome | Scope | Deps | Proof | Size | Rel |
|---|---|---|---|---|---|---|
| M1 | A claim's limits are the only paid authority; a job attaches to a live lease with no consent, bounded by the lease expiry; never allocates | `adapter.py:prevalidate_task`; `machine.py:RunPodMachine.claim`; `target_selection.py:777-786`; `worker_owner.py` reuse | — | `tests/packs/runpod/test_machine.py`, `test_target_selection.py`, `test_warm_session.py`; new `test_job_on_claimed_machine.py` (expiry mid-queue, no live lease refuses, never allocates) | SS | 13 |
| M2 | Generate drops the paid flags and the claim path; with no machine it refuses in one line | `generation/cli.py:_common_options,main`; `sdk/generation.py:_runpod_placement_policy,_modality_controls` | M1 | `tests/core/generation/test_cli.py`, `tests/sdk/test_generation_target.py`, `test_modality_controls.py`, `test_runpod_front_door.py`, `tests/test_mcp_generation_parity.py` | S | 13 |
| M3 | Machines have names; `--machine NAME`, or the single live machine, resolves | lease record; `machine.py:lease_row`; `placement.py:validate_placement`; `generation/cli.py` | M1 | new `tests/core/generation/test_placement_machine_name.py`; `tests/packs/runpod/test_machine.py` | X | 13 |
| M4 | Claim uses preferences, flags override, no consent; `--for` and `--max-usd` derive each other; the first claim saves preferences | `machines_cli.py:_claim,_setup,main`; `target_selection.py:RunPodPreferences` | M1 | machines CLI tests (new or existing): first-claim save, override precedence, derived cap | X | 13 |
| M5 | The idle timer is the one lifetime mode; idle pauses while jobs are queued; `keep NAME --for` needs no USD; `--idle never` | `worker_owner.py:keep,settle,_expire`; `machines_cli.py:_keep` | M1 | `tests/packs/runpod/test_failed_job_keeps_warm.py`; new `test_idle_with_queue.py`; `tests/core/execution/test_warm_hold.py` | S | 13 |
| M6 | A `--datacenter` override drops the volume with a notice | `sdk/generation.py:_runpod_job_preferences`; `target_selection.py` offer filter | M4 | `tests/packs/runpod/test_target_selection.py` | X | 13 |
| M7 | `machines` and `machines show NAME`: job, queue, wait reason, expiry, cost, as data | `machines_cli.py:render` plus new `_show`; `machine.py:lease_row` | M3 | new `tests/core/test_machines_show.py` | X | 13 |
| M8 | List and show layout, refusal lines, claim and wait lines | `machines_cli.py` strings; `target_selection.py:80` | M4, M7 | golden output in `tests/core/generation/test_cli_gold_075b.py` | T | 13 |
| M9 | Skills and docs read as one short path: claim, generate, show, release | the RunPod, generation and setup `SKILL.md` files; `docs/reference/where-things-run.md`, `docs/guides/cli-journeys.md`, guides | M2, M4 | `tests/test_installer_maintained_guides.py`, `tests/test_setup_skill_branches.py`, `agent_journeys.json` | T | 13 |
| M10 | Integration and installed tests and scripts move to claim-then-generate; 20 queued jobs run back to back on one fake machine | `tests/integrations/test_runpod_*`, `test_remote_machine_cpu.py`; `scripts/pod_session.py` | M2, M4 | those files, plus a 20-job case | N | 13 |
| M11 | No RunPod imports in core; go through the `generation.machine` extension | `machines_cli.py`; `placement.py:_runpod_leases`; `generation/cli.py:807` | M4, M7 | an import-boundary test | S | later |
| M12 | Several machines per account, each with a `machine:<id>` queue | `target_selection.py:canonical_claim_path`; `worker_owner.py`; resource keys | M3, M11 | multi-lease journal tests | SS | later |
| M13 | Balance view; a default project on fresh install | CLI surfaces | — | to scope | N | later |

**Critical path:** M1 → M2 → M10, with M9 last. After M1, M3, M4 and M5 run in parallel; M6 and M7 follow; the taste tasks M8 and M9 follow once flags and data shapes freeze.
