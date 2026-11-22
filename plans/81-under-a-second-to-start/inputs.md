# Inputs — Under a second to start

[Plan](plan.md) · [Tasks](tasks.md) · [Handover](handover.md)

## Planning evidence

**Scope decision:** Pending — The owner asked for this plan on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "I think we should include a sub 1s plan on this release with a sub 0.1s for later", then "can you create that plan and associate with 15 and make the other unplanned, use lunas and terras to properly understand everything for the sub 1s plan so that we can give the plan to a manager to drive to completion". She was then given the end state, the estimate of about 20 days and the recommended answers to D1 to D5, and replied "Agree with your recommendations". The scope stays pending only until the independent critique is recorded below. Next: record it, then mark the scope accepted.

**Prior art:** Read and measured on 22 November 2026 at astrid-agent [`048ab307`](https://github.com/banodoco/astrid-agent/tree/048ab307) (`release/15/main` plus nine small unrelated fixes), astrid-runtime [`1758a6df`](https://github.com/banodoco/astrid-runtime/tree/1758a6df) and VibeComfy `e65f4941`, by four Codex Terra tracers and two Luna helpers. Each marked its claims measured, read or inferred; their full reports are [evidence/research-A.txt](evidence/research-A.txt) to [research-G.txt](evidence/research-G.txt). Measurements are medians of five in one shared container running from source, so they are relative, not absolute.

*Measured end to end, on a real Runtime started in the container (G):*

| Command | Wall | The command's own processor time |
| --- | ---: | ---: |
| `timelines create`, empty | 3.5 s | 0.77 s |
| `timelines edit --add-layer media`, one image | 3.8 s | 0.99 s |
| `timelines archive` | 2.95 s | 0.40 s |
| `media list` | 2.7 s | 0.25 s |
| `generate`, no ComfyUI reachable | 15.6 s to the refusal | 10.4 s |

- **The Runtime is not the cost.** In the traced edit every request answered in 0.002 to 0.1 s, including the commit (0.079 s) and the media import (0.096 s).
- **About 2.3 s of every command is client setup from source:** the command waits for an `astrid_runtime connect` subprocess that hashes the Agent's source files (`astrid/sdk/autobootstrap.py:461`; `runtime_protocol/source_identity.py:104`). The tracer counted 190 git processes and 1.8 s for the identity alone. An installed Astrid uses a stamped identity and should skip this; that was read, not measured.
- **`generate` never reached the target check quickly:** at 5 and 10 seconds it was in pack discovery and file hashing (`astrid/core/pack/discovery.py:102`).

*Measured as components, no Runtime (A, B):* one default 10-node workflow takes 3.44 s to build, and the command builds it for approval and again for submission (`astrid/sdk/generation.py:1920`, `:2046`); `find_entry("h3")` 3.9 s cold and 2.7 s warm; the model registry 1.8 s cold and 1.5 s warm; all 70 ready workflows 1.47 s, one named workflow 2.3 ms; `generate --help` 0.17 s and `timelines --help` 0.36 s.

*Read (C, E):* adding one image makes 8 timeline-list reads, 4 inspections and reads the same bundle twice (`astrid/sdk/timeline/sync.py:442`, `:667`; `media_add.py:36`). Seven waits on the two paths have no limit and no message, and four have limits of 30 seconds or more ([research-E.txt](evidence/research-E.txt)).

*What already exists (D):* Plan 55's meter is merged on `release/14/plan-55` (`tests/integrations/test_local_speed_meter.py`) and measures caller to reply against a stand-in ComfyUI on Linux and Windows, not command to queued. The Runtime emits a commit stage event to its log (`runtime_protocol/timeline_commit_execution.py:36-47`); the Agent has no stage timings. A real Runtime daemon fixture exists (`tests/conftest.py:166-190`).

*Negative findings.* The copying in timing validation that took 67% of a save on 18 November is already fixed on both branches (commit `6b878066`; 9.8 ms now against 46.5 ms on a fixture). The 58-second create in [#1236](https://github.com/banodoco/astrid-dev/issues/1236) was intermittent, by its reporters' own correction, and did not reproduce; nobody can attribute it because there are no stage timings, which is US-1.

**Approach:** Four options were compared.

| Option | Verdict |
| --- | --- |
| Remove repeated work on the existing paths, with caches keyed by content, and measure | **Chosen.** No wire change; every refusal stays where it is |
| Move workflow building to after the task is queued | Not here. A tracer sized it at 5 to 8 days of the hardest kind, because it changes what the Runtime's task request carries and turns early refusals into late failures. It belongs to [Plan 55](../55-local-speed/plan.md) |
| A resident process that keeps everything in memory | Not here. It is Plan 55's design for a tenth of a second and has been costly to land |
| Trim imports and start-up | Not here. Start-up is 0.17 to 0.36 s; it matters only below a second |

**Challenge:** Pending — an independent critique is required before greenlight: this plan exceeds five days and changes commands every user and agent runs. Next: record the critic's findings here, with what was accepted and what was set aside and why.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: the budget test uses a stand-in ComfyUI; the container's numbers were taken from source under shared load; nobody has yet timed `generate` to an admitted task, or any command on an installed Astrid, which US-1 and US-2 do first.

**Review rounds:** Recommended: one review stop (RS1) on the cache design note, because a wrong key runs the wrong code and three cards build on it, and one round at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — what the budgets mean.** Under 1 second at the median, on a warm local machine with an installed Astrid, for command to queued and for command to accepted on an ordinary timeline; a heavy timeline stays with Plan 77's two-second target. Recommendation: accept as written. **Decided 22 November 2026: accepted as written.** The owner agreed with the Lead's recommendation in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "Agree with your recommendations".
- **D2 — running from source.** (a) Source checkouts must meet the same budgets. (b) They are measured against their own figure, 2 seconds. Recommendation: (b); a source checkout has to prove which code it is running, and a stamped install has done that once. **Decided 22 November 2026: (b),** source checkouts are measured against their own figure of 2 seconds. Same source as D1.
- **D3 — trusting an install.** May packs that came with an installed Astrid skip re-hashing, on the strength of the install's stamp, while a person's own packs and project packs are still hashed? Recommendation: yes. **Decided 22 November 2026: yes.** Same source as D1.
- **D4 — the batch form.** (a) A file of operations. (b) Repeated flags in one command. Recommendation: (a); each item's arguments stay unambiguous. **Decided 22 November 2026: (a),** a file of operations. Same source as D1.
- **D5 — limits for the waits that have none.** Recommendation: reuse the 135 seconds the acquisition lock already has, with the waiting line after 2 seconds. **Decided 22 November 2026: yes,** 135 seconds, with the waiting line after 2 seconds. Same source as D1.

## Source identities

No code work has started. Read on 22 November 2026: astrid-agent `release/15/main` at `aac1ceb6`; astrid-runtime `release/15/main` at `1758a6df`; VibeComfy at `e65f4941`. Donor commits to read, not merge, on `release/14/plan-55`: Agent `24c68a270` (templates) and the meter in `tests/integrations/test_local_speed_meter.py`; VibeComfy `d8e61a50`. At run start record, for astrid-agent, astrid-runtime and VibeComfy: `release/15/plan-81`, cut from that repository's `release/15/main`, the commit it was cut at, and whether Plan 77 had landed. Intended destination: `release/15/main`.

## References

- [Plan 55](../55-local-speed/plan.md) and [Plan 75](../75-fast-saving/plan.md): the tenth-of-a-second pair, in no release since 22 November 2026.
- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md): heavy-timeline saves; its branch edits the files US-6 and US-7 change.
- [#1236](https://github.com/banodoco/astrid-dev/issues/1236) and its correction; [#1261](https://github.com/banodoco/astrid-dev/issues/1261), the batch route.
