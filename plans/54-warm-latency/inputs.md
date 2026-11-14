# Inputs — Warm-job latency

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Decided by the owner on 14 November 2026, relayed by the Release 13 orchestrator (session `session_011EzfW2L4ou5fDudzKLrc9d`) to the advisor between about 22:40 and 23:40 UTC and recorded in `releases/13/decisions.md` on `r13-progress/decision-log`: warm overhead under 5 seconds, with a plan for under 0.5 seconds on a rented machine and under 0.1 seconds locally; every second accounted for; the faster path must still pass through Astrid. See [Owner decisions](#owner-decisions).

**Prior art:**
- **The measurement.** `releases/13/evidence/live/p1-timing.md` (`r13-progress/decision-log`, d6384df): warm same-model image jobs at 242 and 261 seconds of wall time for 2.88 and 3.01 seconds in ComfyUI; preparation 17 to 18 s, execution 104 to 121 s, collection 47 s, release 21 to 22 s, 52 to 53 s outside every host phase; 91 to 108 s of execution in no pod phase.
- **Where the time goes.** The machines manager's per-gap note (G1 to G6, compose `ee14644a4`) and four independent code reviews of the same commit, summarised in `releases/13/briefs/warm-latency-strategy.md`. Per warm job: seven or more provider calls; five remote commands to re-confirm the machine; about twelve operations to dispatch (`astrid/packs/runpod/machine.py:865-938`); four Python starts and a full catalogue listing on the machine (`machine.py:431-449`); three installation audits, two model-verification passes, node restore, dependency preparation and doctor (`astrid/core/generation/managed_preparation.py:414-857`); six more Python starts for logs; one fetch per file and an installation re-check (`machine.py:1031-1203`); a reset the caller waits for (`astrid/packs/runpod/pod_reset.py:287-329`). Each remote operation opens its own connection (`astrid/packs/runpod/remote_placement.py:1036-1054`).
- **What already exists to build on.** The engine supervisor is resident (`astrid/core/generation/engine_custody.py`). An authenticated engine endpoint with a host-side loopback bridge exists and is tested but is not used by the rented path (`astrid/core/generation/engine_endpoint.py:376`, `engine_transport.py:305`, `astrid/packs/runpod/adapter.py:5`). Release 13 adds the per-claim attestation (card W-A) and per-phase timing (W2, P3).
- **Negative findings.** The bridge refuses websocket upgrades today (`engine_transport.py:319`). The local-managed path pays the same audits as the rented path; the attached path does not, but fetches the schema and compiles twice per job (`astrid/packs/vibecomfy/local_server_engine.py:98-145, 213-219`) and polls history at one second.

**Approach:** Three options were compared for reaching under 5 seconds on a rented machine.
1. *Keep batching the existing path.* Release 13's first tier. Reaches about 30 to 45 seconds; cannot reach 5.
2. *Direct route:* after attestation the host talks to the machine's ComfyUI itself. Fewer moving parts on the machine, but rented jobs take a different code path, evidence and receipts are rewritten host-side, custody checks move, the lifecycle agent needs new endpoints, and each job still makes six to ten requests through the provider's proxy.
3. *A resident Astrid job service on the machine* (chosen). One job path, custody checks stay where they are, two round trips per job, and it is the natural base for under 0.5 seconds because it can watch ComfyUI locally and return the result in the same exchange.
Doing less (stopping at the first tier) was put to the owner and declined: see D1.

**Challenge:** Required: the plan touches custody, release and a cross-repository contract. The advisor wrote the plan and is the standing critic; the orchestrator ruled that the advisor's critique below counts, with an independent pass checking its claims against the code.
- *Critique (advisor).* (a) The largest risk is a second custodian: the service must be supervised by the existing engine supervisor, not beside it, or the release and reset paths gain a process they do not know about. (b) A long-lived process can hold stale verified state; every job must bind to the current supervisor incarnation, and a cached record alone is not enough. (c) "Under 0.1 seconds" is not reachable from a fresh Python process; the plan says so and sets the command line's target at the process-start floor. (d) Timing targets flake; the gates are counts (operations, process starts, polls, hash passes) and time is a witness. (e) Returning the result before clean-up must not weaken the reset: a failed reset has to fence the next job exactly as today. (f) Phase 2's websocket needs a lifecycle change; if that is refused, completion can be pushed by the resident service over the existing exchange, which is why the service comes first.
- *Independent pass.* Pending — an independent reviewer checks the code claims in this pack before greenlight. Next: record its findings and what was accepted.

**Proof and limits:** Completion is defined in [plan.md](plan.md#completion): a live rented run and a local run with overhead measured as wall time minus ComfyUI's own time, the budget tests, and four fail-closed cases. Limits: targets are for small outputs; estimates of seconds per step in the strategy note are estimates, and only the totals above are measured.

**Review rounds:** Recommended: one review stop after the job-service protocol and supervision design (later tasks build on both, and a mistake there reaches custody), and one final round before any release task. Pending — the owner confirms the number.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run after Release 13 publishes, record the date, the phase it covers, the accountable session, what it may do without asking, and the advisor session.

## Owner decisions

- **D1 The target.** Decided 14 November 2026: warm same-model overhead under 5 seconds on a rented machine, a follow-up to under 0.5 seconds, and under 0.1 seconds locally. Source: orchestrator relay, 23:16 and 23:34 UTC.
- **D2 Warm attestation.** Decided 14 November 2026: approved. The first job on a claim verifies fully; later jobs with the same requirements skip re-verification; anything changed re-verifies. Same trust boundary as the model-verification record. Source: orchestrator relay, 23:16 UTC.
- **D3 Through Astrid.** Decided 14 November 2026: the faster path keeps Astrid's own job path, "for the sake of consistency". The direct route is not built. Source: orchestrator relay, 23:29 UTC.
- **D4 Every second accounted for.** Decided 14 November 2026. Source: orchestrator relay, 23:14 UTC ("properly understand and eliminate every level of this delay").
- **D5 Does the machine's own Runtime stay in the job path?** Open. Options: (a) keep it, so the reset remains but runs after the result; (b) the service settles straight to the host, so there is nothing to reset. Recommendation: (b), decided at the review stop with the protocol in hand.
- **D6 Review rounds.** Open. Recommendation: one review stop and one final round.
- **D7 Priority.** Open. Recommendation: directly after Release 13's follow-ups.

## Source identities

Pending — recorded at run start. Expected base: astrid-agent at the Release 13 tag; VibeComfy and `runpod-lifecycle` at the versions that release pins. The analysis in this pack was made against astrid-agent `r13/compose` at `ee14644a4`.

## References

- `releases/13/briefs/warm-latency-strategy.md` and `releases/13/evidence/live/p1-timing.md` on branch `r13-progress/decision-log`.
- `releases/13/decisions.md`, entries of 14 November from 19:15 UTC, same branch.
