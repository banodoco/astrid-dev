Date: 2026-11-15
Kind: papercut
Source: Plan 55 CPU task preparation and first integration candidates
Resolved by: —

The accepted plan names attached-Comfy proof, but Agent's default pytest marker expression deselects its integration nodes even when a worker supplies an exact node ID. Initial LS-2 and LS-6 invocations therefore had no result for that named proof; explicitly selecting the integration marker produced the intended baseline and candidate checks. Future task cards should include the marker expression and expected selected IDs, and treat zero selected tests as NO-RESULT rather than a pass. The Release 13 brief also lagged publication: only the served-manifest canary and deployed source tuple established the correct starting point. These two checks prevented a misleading baseline and an unnecessary run stop; they should be part of concrete task preparation, without adding another progress record.

The next LS-5 comparison initially mixed a previous candidate log into the baseline inputs, then counted captured application `ERROR` log lines as test failures. The manager checked the raw final pytest summaries, required the correct integration baseline and preserved the original logs. The corrected comparison extracts every final pytest status row, after checking that no collection or setup error was omitted, and documents the derivation beside the result. The parser should distinguish pytest result records from captured application logging; until then, an unexplained test-count mismatch is a reason to inspect the inputs, not to accept the bucket totals.
