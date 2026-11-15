# Release 14 — run board

The live state of the Release 14 run. It's rewritten at every check-in. The [brief](../14.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); `tests.md` will hold the test gate once the run starts.

## Now (12:00 UTC, Sun 15 Nov)

**Planning, waiting on Hannah's D1–D7.** Release 14 is the local-first speed release (Hannah, 10:45 UTC); RunPod speed is out of scope. The plan is [Plan 55](https://github.com/banodoco/astrid-dev/pull/662) (`plans/55-local-speed`, astrid-dev #662, not merged). No run is authorized and nothing is built until Hannah answers D1–D7 (plus D8, and D12 which D2 supersedes) and Release 13 publishes; the base is Release 13 as published. The next thing that matters is her answers, then LS-1 (measure the floor) and LS-2 (the standing meter).

### Timeline to publish: not set

| When (UTC) | Milestone | Owner | Status |
|---|---|---|---|
| — | Hannah answers D1–D7 on #662; #662 merges | Hannah, advisor | waiting |
| — | Release 13 publishes; its SHAs become this release's base | Release 13 orchestrator | in progress |
| — | Run start recorded: tasks covered, accountable session, standing authority | orchestrator | — |
| — | LS-1 floor measured (Linux and Windows); LS-2 standing meter reproduces the ~30 s baseline | — | — |
| **—** | **Cut line:** set after LS-1 | release manager | — |
| **—** | **Freeze** the candidate; final frozen CI head | release manager | — |
| **—** | **Publish**, with the owner's go | release manager | — |

### Lanes

| Lane | Session | Brief | State |
|---|---|---|---|
| — | — | — | none yet; no run is authorized |

### Waiting on the owner

- D1–D7 on [#662](https://github.com/banodoco/astrid-dev/pull/662), with the recommendations in the [brief](../14.md#decisions-pending): commit to the under-2 s first stage and treat under 0.1 s as a measured stretch (D1); success keeps meaning stored and recorded (D2); one door through the Runtime (D3); a Python client now (D4); require nothing of the person's ComfyUI (D5); trust ComfyUI's refusal on the warm path (D6); Plan 54 becomes RunPod-only and queues behind Plan 55 (D7).
- D8 (resident sessions as a core capability) and D12 (durability, superseded by D2).
