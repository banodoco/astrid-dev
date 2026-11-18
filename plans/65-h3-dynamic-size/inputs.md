# Inputs — H3 dynamic output size

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — in the Plan 59 session on 18 November 2026 the owner asked “should the output size not be a param we tweak?” and requested a plan for fully dynamic size. Next: record the remaining owner choices and scope greenlight.

**Prior art:** The cached MiniMaxH3ReferenceToVideo interface admits integer width and height from 32 to 16384 in steps of 32. The Agent request currently reserves the whole output object for continuation. The generation builder fixes the output and preserved-tail canvas. The two captured continuation workflows have distinct sizing controls. Preparation checks 1024×576 again during frozen-source verification. Composition can read actual dimensions but looks up its own mask and resizes it. The standalone preview already has a fill transform and an explicit size option. Research found operator reports about upscaling and no controlled evidence of small-size speech quality. [Pinned source findings](research/size.md) · [Voice-only use case #885](https://github.com/banodoco/astrid-dev/issues/885)

**Approach:** Use one request-level size and one resolved mask per edit. A second voice-only flag duplicates the size vocabulary. Presets can be documented without restricting admission to a list. Post-generation resizing saves no sampling time. Keeping this plan independent permits an image-only edit at a new size without waiting for speaker-quality approval.

**Challenge:** Reviewed — the independent planning critique of 18 November 2026 inspected the Plan 59 Git objects and cached node schema and returned both plans for revision. Accepted all six Plan 65 findings: correct the proof dimensions, decide continuation scope in advance, preserve request identity, give the compiler explicit ownership of the mask handoff, respect standalone preview geometry and stage integration behind those interfaces. Accepted the shared CPU proof, source-pin, test-inventory and reviewer recommendations. No critique findings were rejected. The earlier assumption that the two original proof sizes pass the grid failed integer validation. A successful builder comparison alone cannot close the continuation use case in [#885](https://github.com/banodoco/astrid-dev/issues/885). Fable’s 18 November composability review confirmed duplicate preparation defaults at prepare.py:477–478 and the separate moving-mask handling at compose.py:445–472. Accepted a single resolved size and one shared limits table. D1 now leaves continuation sizing to Plan 66. On 18 November the plan was tightened for a less experienced implementer: GPU work removed (D2), the mask handoff cut to static masks rasterized once (moving masks unchanged), the literal-number scan replaced by binding checks, one plan order (Plan 64 SR-1 to SR-3 first), explicit non-goals, and function names instead of line numbers.

**Proof and limits:** Separate size effects from aspect changes with a same-aspect comparison and a different-aspect mask fixture. CPU proofs cover exact bindings, decoded geometry, protected pixels and retained result records. Speech quality and GPU timing are left to the owner's live test after the plan (D2). Node admission alone establishes neither quality nor feasible memory use across the allowed range.

**Review rounds:** One final round recommended because request identity, mask permission geometry and the worker handoff are shared. Owner confirmation pending.

**Run start:** Pending — the owner requested planning only. Before dispatch record the accountable session, date, authorized tasks, spend and publication boundaries, reviewer and advisor bindings.

## Owner decisions

- **D1 — no continuation work in this plan (decided 18 Nov 2026, owner: "let's drop this plan 65 work and the continuations workflow as well").** This reverses the earlier same-day choice to include small-size continuation. [Plan 66](../66-h3-composable-core/inputs.md#owner-decisions) CC-7 gives continuation any size through its ported stage, and deletes the captured workflows (Plan 66 D3, D5). Until then, a non-default size on continuation is refused.
- **D2 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session: "we're not going to do a GPU test. This is just CPU… We'll do a test afterwards").** No task in this plan claims a machine or spends money. The 512×288 vs 1024×576 speech and timing comparison happens in the owner's live test afterwards.

**Model limits and defaults, not decisions** (owner, 18 Nov 2026: "offer that and constrain them within that"):
- `output.size` is a pixel pair, constrained exactly to the node's limits: width and height 32–16384 in steps of 32 (`MiniMaxH3ReferenceToVideo` schema). There are no presets.
- Duration keeps H3's own frame rule: 24 fps, frame counts 17k+5, trained about 124–362 frames.
- Existing mask boxes are 1024×576 pixels and scale to the chosen size. A new mask states its own canvas with `mask.canvas: [w, h]` (DS-3).
- Quality is only established at the sizes the proof tests.

## Source identities

Inspected `astrid-agent` `origin/release/14/plan-59` at `ec758a9b86a43416ace0650eb8109cb5967575dc` and the cached core node schema pinned to ComfyUI `6bfaacc67c2103481e5f0c84d75257cd0581d86a`. Plan 59 is the research snapshot. The actual release base and retained donor/dependency SHAs are pending. At dispatch identify the release, record its `astrid-agent` `release/<NN>/main` SHA and dependencies (including Plan 64 if integrated), then target `release/<NN>/plan-65`. Product changes belong to Agent. Run and review evidence belongs to this plan in astrid-dev.

## References

- Plan 59 owner session and independent planning critique, 18 November 2026. The accepted changes and open decisions are recorded above.
- [Plan 64 coordination](../64-h3-speaker-references/plan.md#interfaces-and-handoff) · [Source research](research/size.md) · [Voice-only takes](https://github.com/banodoco/astrid-dev/issues/885)
