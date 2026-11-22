# Inputs — Once per command

[Plan](plan.md) · [Tasks](tasks.md) · [Handover](handover.md)

## Planning evidence

**Scope decision:** Accepted — the owner asked for the under-a-second work on 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "I think we should include a sub 1s plan on this release with a sub 0.1s for later". After the research and the critique she asked whether it could be done "in two plans with one half yielding a lot of the results", was given the split by how long a result is kept, with this half at low risk and not reaching a second for `generate`, and replied: "Let's do that split please". This plan is that first half. She decided D1, D2, D4 and D5 the same day.

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

**Approach:** Split on 22 November 2026 by how long a worked-out result is kept.

| Half | What it is | Verdict |
| --- | --- | --- |
| Once per command | Inside one command, work each thing out once and pass it along; time every stage; fewer round trips; bounded waits | **This plan.** Nothing is kept for a later command, so nothing can be stale and no freshness design is needed |
| Across commands | A later command reuses an earlier one's results: the compiled workflow, an index of entries and registries, an install's stamp, ComfyUI's node list | [Plan 82](../82-reuse-across-commands/plan.md). It carries all the risk of a stale result, and it can be done with caches on disk or with a process that stays running, which is [Plan 55](../55-local-speed/plan.md)'s design. This plan's measurements decide which |

Also rejected for both halves: moving workflow building to after the task is queued (it changes what the Runtime's task request carries and turns early refusals into late failures; Plan 55), and trimming imports (start-up is 0.17 to 0.36 s).

**Challenge:** Reviewed — commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026 and done by an independent Codex critic (`gpt-6.2-astra`, high effort, read-only brief, no stake in the draft). It read code and the research; it ran no tests, CI, installed command line or live ComfyUI. The owner asked that its ideas be weighed, not adopted wholesale; each finding below says what the planner did with it. The critique was of the plan before the split; findings about reuse across commands now apply to Plan 82 and are marked.

- **Accepted, now Plan 82's — one card had the cache wrong.** The draft keyed the compiled workflow on its inputs, so a new prompt would have rebuilt it (3.4 s). The corrected card, which fills in the prompt and seed, is Plan 82's RA-2; this plan's ceiling test already runs a changed prompt.
- **Accepted — the generation budget is not yet proven reachable.** After the caching work the likeliest stage to keep it above a second is the live check of ComfyUI's node list (`astrid/core/generation/backends/comfy_target.py:721`), which nobody has timed on a real ComfyUI. US-0 takes a real baseline first; the question it raises is Plan 82's D3.
- **Accepted, now Plan 82's — the four caches need four different proofs of freshness.** They are written into Plan 82's first task.
- **Accepted — card corrections:** the Runtime writes its stage log after replying, so US-1 no longer joins it into the command's result; the daemon fixture runs from a checkout and Windows does not run fast checks on pull requests, so US-2 says what CI can and cannot assert; an installed Astrid already skips source hashing and two more digests precede host attachment (`astrid/sdk/host_bootstrap.py:2169`), now in US-3; named lookups already filter, so US-4 names the caller's default enumeration (`astrid/sdk/generation.py:1697`) and pins the existing tests; the workflow card was split into building once per command (US-5a, here) and reuse across commands (Plan 82); US-6 pins the disjoint-edit merge, because refusing every changed head would break valid merges; US-8 is narrowed to the client's own locks and tests thread contention.
- **Partly accepted — "cut batching first".** It is right that a batch does not help the one-edit budget, and US-7 now says so and is marked first to cut. It stays, because one command per clip is the cost agents feel most and the owner chose its form (D4).
- **Accepted — the estimate.** Twenty days was plausible for the work and too narrow to promise both budgets. After the split this plan is about 17 days and promises no one-second figure for `generate`.
- **Noted:** Plan 77's branch also changes generation input inspection and raises the client's request timeout to 300 seconds.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: the ceiling test uses a stand-in ComfyUI and a Runtime run from a checkout; the container's numbers were taken from source under shared load; nobody has yet timed `generate` to an admitted task, or any command on an installed Astrid, which US-0 does first. The expected gains (a timeline edit near one second, `generate` roughly halved) are estimates from component timings.

**Review rounds:** One round at the end, by an independent reviewer on Codex Astra; landing waits for its findings. No review stop is needed: nothing here outlives its command. The owner agreed to this on 22 November 2026 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), replying "That's perfect" to that wording.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

All decided on 22 November 2026 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "Agree with your recommendations".

- **D1 — what the figures mean.** Decided: medians, on a warm local machine with an installed Astrid, for command to queued and for command to accepted on an ordinary timeline; a heavy timeline stays with Plan 77's two-second target. After the split, this plan holds ceilings that only fall and aims at one second for a timeline edit; the one-second budget for `generate` is Plan 82's.
- **D2 — running from source.** Decided: source checkouts are measured against their own figure of 2 seconds.
- **D4 — the batch form.** Decided: a file of operations.
- **D5 — limits for the waits that have none.** Decided: 135 seconds, with the waiting line after 2 seconds.

D3 (trusting an install's stamp) and D6 (ComfyUI's node list) are about results kept between commands and moved to [Plan 82](../82-reuse-across-commands/inputs.md#owner-decisions).

## Source identities

No code work has started. Read on 22 November 2026: astrid-agent `release/15/main` at `aac1ceb6`; astrid-runtime `release/15/main` at `1758a6df`; VibeComfy at `e65f4941`. To read, not merge, on `release/14/plan-55`: the meter in `tests/integrations/test_local_speed_meter.py`. At run start record, for astrid-agent and astrid-runtime: `release/15/plan-81`, cut from that repository's `release/15/main`, the commit it was cut at, and whether Plan 77 had landed. Intended destination: `release/15/main`.

## References

- [Plan 82](../82-reuse-across-commands/plan.md): the second half, in no release.
- [Plan 55](../55-local-speed/plan.md) and [Plan 75](../75-fast-saving/plan.md): the tenth-of-a-second pair, in no release since 22 November 2026.
- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md): heavy-timeline saves; its branch edits the files US-6 and US-7 change.
- [#1236](https://github.com/banodoco/astrid-dev/issues/1236) and its correction; [#1261](https://github.com/banodoco/astrid-dev/issues/1261), the batch route.
