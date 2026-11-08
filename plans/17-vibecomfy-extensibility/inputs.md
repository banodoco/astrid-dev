# Inputs — Pack extension points

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

Repository ownership, starting branch and SHA, retained dirty work, and candidate branch are **TBD at execution start**. Identify and freeze the owning repository or repositories and current refs before source changes. Historical plan text does not establish a live execution base. Verify the intended `pre-main` destination then; do not assume branches.

| Input | Why it matters | Identity / limits |
|---|---|---|
| Current VibeComfy implementation | Reveals existing workflow primitives and extension contracts to reuse (`vibecomfy.plugins`). | Reviewed at VibeComfy `e65f4941` (8 Nov 2026); re-freeze at setup. |
| Extension protocol | The registry, scopes and sidecar walker this plan switches on (`astrid/core/extensions`, commit `864179976`). | Reviewed at astrid-agent `5eac07e3f` (8 Nov 2026); Plan 32 T2 allows `side: agent`. Re-freeze at setup. |
| h3_av | The first `vibecomfy.workflows` contribution, made in Plan 32 T6b. | Reviewed at astrid-agent `5eac07e3f`, `astrid/packs/h3_av` (8 Nov 2026). |
| Sound-effects template | The base of P4's sound-on-video pack (`ready_templates/audio/hunyuan_video_foley.py`, audio output only). | Reviewed at VibeComfy `e65f4941` (8 Nov 2026). |
| Base | Plan 32's landed Agent head after T6b, and poms_packs `main` after Plan 06. | Pending — record both SHAs before P1. |

## References and evidence

- [Liquid Software vision](../../vision/pillars/liquid-software.md) sets the design direction.
- `merge-run/path-review/PACK-EXTENSION-PROTOCOL.md` and `H3-GENERALIZATION.md` on the merge-run desk (`banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`): the protocol review and the choice of the second pack.
- **Review rounds:** recommend at most 2. The plan touches the install transaction (a trust boundary) but no cross-repository contract beyond Plan 32's points. Pending owner agreement.
- This plan is CPU only; P4's real-GPU run belongs to [Plan 34](../34-real-gpu-proof/plan.md).

## Constraints

Follow repository [Astrid development skill](../../skills/astrid-dev/SKILL.md) and the shared [run contract](../../skills/astrid-dev-shared/run-contract.md) for execution, resources, routes, and publication. Confirm source identities and destination at setup.
