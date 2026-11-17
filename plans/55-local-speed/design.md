# Local speed: the fast lane

[Plan](plan.md) · [Inputs](inputs.md) · [Decisions](decisions.md) · [Task card](tasks.md)

Working draft for **LS-3 / R14-P55-01**. The packet manager is
`r14-P55-01-1`; the Release 14 Lead owns RS1 and integration. This note
proposes the design for that review. It is not evidence that the fast lane
has been implemented or that a speed target is qualified.

## Basis and boundaries

The packet and its authority are pinned at astrid-dev
`1c6b21f3e6fda84384871805719ebba6e03b626c`. The design starts from the plan
branch at `4b774b114dcc97b11cfe50ad69eeac18b0308711`, including the floor
table merged from PR #756. The dated handover and developer handoff are
evidence inputs; the newer packet and owner decisions govern conflicting
progress and permission statements.

The [floor table](plan.md#the-floor-and-the-targets) measures a resident
probe against real CPU ComfyUI, with twenty samples per cell. For a
one-megapixel image through the unchanged Runtime:

| Callers | Linux median / slowest, ms | Windows median / slowest, ms |
| --- | ---: | ---: |
| One | 41.35 / 319.63 | 225.63 / 592.06 |
| Two | 178.49 / 225.22 | 284.01 / 546.03 |

These are not installed-Agent measurements. Queue wait is not silently
subtracted. The two-caller cell includes contention, so its difference
cannot be assigned entirely to Runtime writes. A native flush count is
not derivable from a transaction count. Missing video, GPU and real
Windows-machine evidence remains missing; D9 allows this design to proceed.

Stage one retains create, claim and settle, and retains durable output and
record before success (D1–D3). Removing repeated resolution, process starts
and polling is the first implementation path. Combining admission and claim
or changing Runtime publication needs an attributed measurement and the
existing review/owner gates; this note does not select that change.

## The eight design questions

1. **Key and first job.** Key the prepared workflow by source and companions,
   variant, compiler, input shape, target schema and generation, and Astrid
   installation. The first job verifies and prepares; later jobs fill typed
   slots. Values such as prompt and seed do not invalidate the template.
2. **Target generation.** Bind the websocket and HTTP listener to one target
   generation. On a drop, invalidate target facts, reconcile outstanding
   attempts without replay, then reconnect and refetch. A stable URL alone
   does not identify a stable ComfyUI instance.
3. **Exit and fallback.** A changed key, broken connection or refusal leaves
   the fast lane. A known pre-acceptance refusal can take the full path once;
   an uncertain submit acknowledgement must never trigger a second submit.
4. **Resident helper.** LS-8 adds a supervised core module beside
   `generic_host.py`. It retains pinned source, the restricted environment
   and a killable process scope; the pack holds its own ComfyUI state.
   Undeclared/arbitrary pack actions retain a process per job (D8).
5. **Runtime hand-off.** Wait for work and results using notifications with
   authoritative state reads, on the existing create/claim/settle lifecycle.
   Establish the write budget without relaxing success durability (D2–D3).
6. **Identity and failures.** Keep task, attempt, lease/fence, prompt and
   output-prefix identity separate. Two callers cannot share per-job state.
   Cancel only the named owned job; a lost caller does not cancel it. Crash
   recovery reconciles evidence and never automatically reruns an unknown
   outcome (D5).
7. **Thin request.** The CLI, SDK and tool server send the request as asked
   through Runtime; the resident side resolves it and preserves typed
   refusals. The CLI remains Python; the tool server calls in-process (D4).
8. **Version agreement.** Compare client, resident protocol and installation
   identity before admission. A mismatch uses the supported full path with
   a clear message, without replaying a task already admitted.

The submission revision will specify the code boundaries, per-case behavior,
write budget, guarantee-to-decision mapping and LS-14 checks for all eight.

## Windows

The current hosted-Windows image floor is **225.63–284.01 ms median**, already
above a 100 ms total budget before the additional resident-Agent work. Its
slowest samples are 592.06 and 546.03 ms. This contradicts the earlier
25–120 ms estimate; it does not establish the performance of a person's
Windows machine.

The owner has three choices; **this packet chooses none**:

| Option | Consequence |
| --- | --- |
| Keep 100 ms as the target for a real Windows machine | Keep it unpromised until LS-13/LS-14 measure the actual machine, with the default scanner on, against the complete stored-and-recorded caller path. Hosted CI alone cannot qualify it. |
| Move the Windows target | The owner chooses a revised measured budget and its hardware/workload scope. D1 and the acceptance checks must be updated through the Lead; the packet cannot silently increase the threshold. |
| Meet 100 ms another way | Attribute the Runtime/storage cost, then design and prove a narrower durable hand-off or publication path under RS1 and any needed owner decisions. Returning early, bypassing Runtime, requiring an extension or adding a native client is not implicitly approved. |

For now the implementation can pursue the unchanged under-two-second
stage-one commitment. LS-14 must report the Windows target decision and
measurements rather than label missing evidence a pass.
