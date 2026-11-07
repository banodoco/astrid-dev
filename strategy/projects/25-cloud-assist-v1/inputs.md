# Plan 25 — source inputs and open decisions

**Starting evidence (review at exact commits before work):**

- [Reigh Worker Orchestrator](https://github.com/banodoco/reigh-worker-orchestrator) — README documents RunPod GPU workers and fal/Wavespeed API task management. [Current main at time of planning](https://github.com/banodoco/reigh-worker-orchestrator/tree/9d9df8cae6f6fd16168f416c8edaa848fa1f4ea0).
- [Satellite disposition](https://github.com/banodoco/astrid-agent/blob/main/tools/astrid-rename/satellites.md) — labels orchestrator **deprecated**, with unclear live Railway deployment; **do not assume it can be deployed unchanged**.
- [Astrid Agent execution map](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md) — distinguishes selected local, provider and RunPod inference; sources should be rechecked against current Agent/Runtime state.
- [Plan 12 multiple inference routes](../12-multiple-inference-routes/plan.md) and [Plan 20 zero-to-first-image](../20-zero-to-first-image/plan.md), [F-003 creative execution](../../visions/gaps/F-003-creative-execution.md), existing App/Runtime media/artifact and video-rendering code.

**Unresolved before implementation:** desired cloud agent API/provider, agent-family orchestration interface, remote render engine/service (reuse FFmpeg/Remotion vs alternative), supported OSes, secure file transfer/temporary storage, per-run spend limit, credentials and user consent, provider failure semantics, callback versus polling, what logs may be retained, who qualifies real cloud runs.

**Boundary:** local files/database remain authoritative; a remote engine is a **worker**, not a cloud workspace. A plan with a cloud worker does not silently authorize retaining project libraries remotely.
