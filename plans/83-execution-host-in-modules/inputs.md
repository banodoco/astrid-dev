# Inputs — Execution host in modules

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner wrote on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "I think plans should typically go all into one release". [Plan 13](../13-execution-host-refactor/plan.md) then held four tasks in Release 15 and seven in none, so the Lead moved the seven here the same day, unchanged. She has not chosen this plan's release or where it is cut. Next: she decides on Plan 13's re-estimate (its EX-3).

**Prior art:** Plan 13's: the [map](../13-execution-host-refactor/map.md) of all 188 top-level definitions, four read-only checks of it against astrid-agent [`048ab307`](https://github.com/banodoco/astrid-agent/tree/048ab307) on 22 November 2026, and the inventory of that day, all in its [evidence](../13-execution-host-refactor/evidence/) and summarised in its [inputs](../13-execution-host-refactor/inputs.md#extraction-evidence-22-november-2026).

**Approach:** Plan 13's, in its [Release 15 scope](../13-execution-host-refactor/plan.md#release-15-scope): leaves first, then what the Runtime adapter stands on and the adapter, source custody, review, local preparation, and the class last, as objects and not mixins.

**Challenge:** Reviewed — these rows were reviewed where they were written, in Plan 13, by an independent Codex critic (`gpt-6.2-astra`, high effort, read-only) commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026; its report is [critique-extraction.txt](../13-execution-host-refactor/evidence/critique-extraction.txt) and what was done with each finding is in [Plan 13's inputs](../13-execution-host-refactor/inputs.md#extraction-evidence-22-november-2026). The move into this plan changed no card and has had no critique of its own. RS2 is the review of the class design.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: the estimate is an allowance until Plan 13's first move is measured; the critique ran no tests.

**Review rounds:** Recommended: the review stop RS2 before the class, and up to two rounds at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — its release, and where it is cut.** As written it is more than one release's work. (a) EX-4 to EX-7 join the release that follows Plan 13's re-estimate, and EX-8, RS2 and EX-9 become their own plan; (b) all of it waits for one later release. Recommendation: (a), decided on the re-estimate. Pending.
- **Carried from Plan 13, decided 22 November 2026:** only the owner may approve an exception to the growth guard (its D2); EX-8 is not in Release 15, because it follows [Plan 38](../38-one-process-identity/plan.md) (its D3).

## Source identities

No code work has started. Read on 22 November 2026: astrid-agent `release/15/main` at `aac1ceb6`. At run start record the release, the plan branch `release/<NN>/plan-83` in astrid-agent, the commit it was cut at, and the Plan 13 commit it builds on.

## References

- [Plan 13](../13-execution-host-refactor/plan.md): the map, the guard, the safety net, the first move and the re-estimate.
- [Plan 38](../38-one-process-identity/plan.md): EX-8 follows it.
- [#1290](https://github.com/banodoco/astrid-dev/issues/1290), [#1294](https://github.com/banodoco/astrid-dev/issues/1294): the failing giant-file check and the `os` alias.
