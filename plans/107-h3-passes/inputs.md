# Inputs — H3 passes

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — The owner directed, on 28 Nov 2026 in the [planning session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), that Release 16 ships the single-pass extension contract with NKD, H3 Experiments and Dials, and that pass execution with de-rope follows as its own project in Release 17. The design record is on [#2065](https://github.com/banodoco/astrid-dev/issues/2065#issuecomment-7238057362).

**Prior art:**
- Agent [`shared/planner.py`](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/packs/h3_av/shared/planner.py) at `4a2bad187f12e7b0d1ba5bd1164b4a076787516a` already derives ordered sampling passes.
- [ComfyUI-MAINodes](https://github.com/matlowai/ComfyUI-MAINodes) at `e019112ad20cdec3b1483c68fc1aefff401d2452` implements de-rope as Jerk Oracle → Time Smear → regenerate → Exact Recover and Audio Recover (`motion.py`), plus Clock Remap (`derope_any.py`). True Clock and DyRoPE assign `MiniMaxH3Model.rope_freqs` at class level (`motion.py:1915, 2235`). V2V Init writes `noise_mask` itself (`motion.py:2699-2729`).
- Kent's [ComfyUI-MiniMaxH3-Experiment](https://github.com/Kentskooking/ComfyUI-MiniMaxH3-Experiment) continuation sampler runs windows inside one node.
- Dials' time curves read their clock from the latent, so they restart per window (`dials/timecurve.py:189-207` in [ComfyUI-Dials](https://github.com/matlowai/ComfyUI-Dials) at `a0a8a8f6ebe3f2b78904a6a106501f1bfdcb3a0c`).

**Approach:** First-class passes on Plan 66's job record, with a runtime `media` socket, a composed hold-capable time map, per-pass `denoise.start`, budget and provenance, and a bounded `repeat`. The alternatives were:
- hiding passes inside single nodes (status quo; no planning, checking or explanation);
- any graph fragment between named ports (unsafe for masks and composition, and opaque to agents);
- separate SIGMAS or NOISE sockets (rejected; passes declare `denoise.start`).

**Challenge:** Reviewed — independent adversarial review of the five-socket contract against NKD, H3 Experiments, Dials and MAINodes de-rope, recorded with the design on [#2065](https://github.com/banodoco/astrid-dev/issues/2065) and in the H3 guidance redesign document.

**Proof and limits:** CPU proof per the plan's completion list: real two-pass execution, exact kept content after stretch and recover, inverse-length and budget refusals, and time-map-correct Dials curves. Motion quality, seams and recovered-audio quality need a separately authorized live check. Other model families are out of scope.

**Review rounds:** One closing review, recommended because the time map and exactness span every pass.

**Run start:** Lane [h3](../../releases/16/briefs/h3.md): the brief records the owner's go, authority and limits.

## Owner decisions

None open. Recorded: 28 Nov 2026, the owner placed this project in Release 17 and confirmed that licensing is settled (all components used are open source).

## Source identities

Planning snapshot: Agent `release/16/main` `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`; ComfyUI-MAINodes `e019112ad20cdec3b1483c68fc1aefff401d2452`; ComfyUI-Dials `a0a8a8f6ebe3f2b78904a6a106501f1bfdcb3a0c`; ComfyUI-MiniMaxH3-Experiment `14cc4824d965f7c900b427b4d2d0241c8e7df58c`. At dispatch, record the Release 17 base and cut `release/17/plan-107` in astrid-agent.

## References

- [H3 programme review and amendments, #2065](https://github.com/banodoco/astrid-dev/issues/2065)
- [Plan 66 extension contract](../66-h3-composable-core/tasks.md#extension-contract)
- [Plan 67](../67-h3-community-steering/plan.md)
