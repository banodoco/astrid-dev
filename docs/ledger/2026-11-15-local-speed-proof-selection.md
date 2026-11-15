Date: 2026-11-15
Kind: papercut
Source: Plan 55 CPU task preparation and first integration candidates
Resolved by: —

The accepted plan names attached-Comfy proof, but Agent's default pytest marker expression deselects its integration nodes even when a worker supplies an exact node ID. Initial LS-2 and LS-6 invocations therefore had no result for that named proof; explicitly selecting the integration marker produced the intended baseline and candidate checks. Future task cards should include the marker expression and expected selected IDs, and treat zero selected tests as NO-RESULT rather than a pass. The Release 13 brief also lagged publication: only the served-manifest canary and deployed source tuple established the correct starting point. These two checks prevented a misleading baseline and an unnecessary run stop; they should be part of concrete task preparation, without adding another progress record.
