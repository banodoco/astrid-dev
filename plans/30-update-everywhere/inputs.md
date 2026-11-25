# Inputs — Update everywhere: remaining setups

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

This plan holds Plan 29's second phase, split out so it can have its own priority. Its evidence is shared with Plan 29.

**Scope decision:** Pending — part of the owner's 7 Nov 2026 request recorded in [Plan 29's inputs](../29-update-and-release/inputs.md#owner-decisions); added to the catalog as queued at the owner's request. Next: owner confirms the scope before the first task starts.

**Prior art:** shared with [Plan 29](../29-update-and-release/inputs.md#planning-evidence), including the ambiguity reviews for UR-15 to UR-18.

**Approach:** finish the setups Plan 29 leaves, reusing its `self_update` status, reasons and hosted rows.

**Challenge:** Reviewed — the same independent reviews as Plan 29, which moved these items out of the first phase.

**Review rounds:** at most two before closing (owner, 8 Nov 2026). The work is mostly lower-risk proof and schema tasks, though UR-15 is S.

**Proof and limits:** see [plan.md](plan.md#completion). The share of users on systemd below 254 is unknown; there is no install telemetry.

## Source identities

Record the exact base SHAs when each task starts.


## Proposed Release 16 scope reconciliation (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

record actual old and modern manager capability evidence; preserve no-manager/autostart-off direct foreground behavior where supported, special-character paths and exact worker receipt. Adopt P10's engine proof and P09/P38 ownership boundaries. Disposition recovered closed/unmerged PR#178 as historical task source, not automatic implementation.
