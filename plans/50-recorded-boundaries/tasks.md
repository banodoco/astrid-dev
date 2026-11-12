# Tasks — Recorded boundaries and an offline generation harness

[Plan](plan.md) · [Inputs](inputs.md)

A draft can use a short outline with unknowns. Before dispatch, every task needs one bounded outcome, its input and deliverable, dependencies, a suitable route, and focused proof. Name source identity where one task consumes another project's output. Reuse the prior-art and source identities in [inputs.md](inputs.md); don't repeat them.

**Task ids:** `RB-1`, `RB-2`, …

**Critical path:** RB-2 → RB-3 → RB-5 → R. RB-1 runs in parallel with RB-2. RB-4 runs in parallel with RB-3 and must land before RB-5.

**Test inventory:**
- Agent:
  - `tests/integrations/test_remote_machine_cpu.py`
  - `tests/providers/test_provider_contract.py`
  - `tests/packs/runpod/test_pack_actions.py`
  - `tests/packs/runpod/test_machine.py`
  - `tests/packs/runpod/test_failure_receipt.py`
  - `tests/core/execution/test_bug14_settlement_liveness.py`
  - `tests/core/execution/test_claim_head_of_line.py`
  - `tests/sdk/test_invocation_observation.py`
- Runtime: the `_stage_outputs` and `_claim_task` tests.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| RB-1 The CPU journey runs in the shared worker environment and on CI. Its 24 local failures are the rejected empty-log publication ([inputs](inputs.md#planning-evidence)), fixed by Release 13's inline-proof or terminal-reconcile work; this task adds the journey's setup to astrid-dev's [worker environment](../../env/README.md) and makes the Agent CI lane run it with a real Runtime checkout | N | the Release 13 fix for the rejected publication | `env/` scripts; `tests/integrations/conftest.py` setup only; the Agent lane workflow | `test_remote_machine_cpu.py -m integration` passes on the Release 13 rehearsal from the worker script and in the CI lane | [ ] |
| RB-2 A recording library: `tests/providers/recorded.py::load(provider, name)` with `vary`/`omit` rules (design §5); a refusing replay fake for RunPod and the Runtime client; a capture hook that saves scrubbed responses during authorized paid runs; move the existing four RunPod recordings in | X | — | `tests/providers/`; the capture hook in the RunPod and Runtime clients (test-only seam) | Replay serves recorded requests; an unrecorded request fails the test; the scrubber keeps JSON types and drops non-allowlisted values | [ ] |
| RB-3 Replace the fixtures that hid the 11–12 Nov bugs with recordings: the task read model (`spec.spec`), `networkVolume`, the `tasks logs` source, an empty-log failure publication | N | RB-2 | the named tests' fixtures only | Each converted test fails on its pre-fix revision and passes on the fix | [ ] |
| RB-4 Write the terminal-state contract for a failed attempt and its machine (unknown vs definite rejection; cede; kept or released and by whom), reconciled with Plan 40 D12/D13, as Agent docs plus a table the matrix imports | S | — | `astrid/packs/runpod/docs/`, `docs/` in the Agent | The contract names every end state that the terminal-reconcile and keep-warm branches implement; reviewed by the advisor | [ ] |
| RB-5 A fault matrix in the CPU journey: one row per injected failure (stock, 429 with `Retry-After`, a killed pod, an install or doctor failure, a rejected failure publication, an expired lease, a host SIGTERM mid-publication, a storage wait, a held slot), each asserting a named reason and the contract's end state for the task and the machine | X | RB-1, RB-2, RB-4 | `tests/integrations/test_remote_machine_cpu.py` and its fixtures | Every row passes on the integrated revisions; each 11–12 Nov live failure's row fails on its pre-fix revision | [ ] |
| RB-6 A visibility ratchet: no wait loop without a reason line and no `from None` without a typed reason, on the generation path | N | — | a lint script in the Agent `scripts/` and its CI hook | The ratchet fails on a planted silent loop and passes at baseline | [ ] |
| R Review rounds (at most 1, recommended; the owner confirms) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |
