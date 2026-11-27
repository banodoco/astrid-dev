# Inputs — Releases defined and published from astrid-dev

[Plan](plan.md) · [Tasks](tasks.md) · [Independent observation #2063](https://github.com/banodoco/astrid-dev/issues/2063)

## Planning evidence

**Scope decision:** Pending — the owner retains P31 in Release 16 (0.1.0), with semantic versions visible before first public go. This final reconciliation updates planning records and preserves current implementation/approval authority. Next: settle the named publication-control and qualification-policy decisions, then execute through the existing Lead; no publication is authorized here.

**Prior art:** Completed [P58 release records](../58-strategy-from-releases/tasks.md), existing [P29 update/release machinery](../29-update-and-release/plan.md), and the [actual-source register below](./inputs.md#source-and-progress-register) establish what is reused. [Sense-check #2063](https://github.com/banodoco/astrid-dev/issues/2063) verifies the bounded residual guard, canary, inventory and protection findings.

**Approach:** Reuse completed P58 records/strategy and P29/App pin, manifest, update, guard and canary machinery. Complete protected exact identity, deterministic delivery and proof; do not restart a release system.

**Challenge:** Reviewed — [#2063](https://github.com/banodoco/astrid-dev/issues/2063) was checked against canonical P31/P58 records and actual guard, canary, status, inventory and protection sources. The [previous inputs](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/31-releases-from-astrid-dev/inputs.md) preserve all earlier design reviews, accepted history and alternatives. No further broad planning round is commissioned.

**Proof and limits:** Source/API inspection and recorded historical receipts, not a fresh installed, native or served-origin pass. No tests, publication, product changes or control changes were performed for this planning correction. Actual deployment credentials/environments and complete effective release-branch protection remain unverified.

## Preserved owner decisions and resolved historical drift

- The 10 November release-led strategy decision owns one living `releases/<N>.md` brief that becomes the immutable final publication record. There is no parallel handwritten release log. P58's completed implementation is reused.
- Versions use `major.minor.patch`; patch is default unless the owner declares otherwise. The owner now explicitly assigns **R16 = 0.1.0**. The integer release stays the wire/disk ordering key. Hosted App deploys alone are not numbered releases.
- Required-update policy is a separate per-release decision with a reason. Minor does not imply required. The published R15 floor is 15; preserve the actual served floor unless an explicit owner change and migration/compatibility proof justify another.
- **astrid-dev is the release source**, superseding the old App-authority proposal. Generated App artifacts are delivery output. A protected generated-only App PR is the recommended delivery mechanism; the earlier direct-push/no-App-PR proposal cannot waive effective controls.
- Actual legacy history starts from the truly published predecessor and its receipts. R15 was published; earlier “if R15 publishes” and predicted Release 10 anchors are obsolete. Do not manufacture semantic mappings for every past candidate: unmapped installs show “an earlier version” with exact integer in diagnostics.
- The 25 November tester direction remains: contributors independently resolve a coherent tentative snapshot without write access or a prebuilt bundle, reproduce it from a receipt and exercise the matching local App/Agent with existing consent. Same-number snapshots must use the supported installer/update path.
- Owner-approved exact Final and effective protection remain prerequisites before public writes. The qualified candidate can use unpublished release branches; main ancestry is checked at its actual public promotion stage.
- Version display is inside R16 before RL-R/RL-G. The old “phase 2 after publication”, `int/31`, whole-P29-on-main wait, obsolete skill path and blanket deletion grep are no longer active dispatch instructions.
- Existing independent review limits remain binding. Historical recommendation was at most three P31 rounds, not an accepted unlimited budget; the Lead records the applicable agreed budget before commissioning. This reconciliation adds none.

## Source and progress register

These are immutable observations from 27 November 2026, not frozen dispatch pins.

| Source | Verified meaning / remaining limit |
|---|---|
| [P58 tasks](../58-strategy-from-releases/tasks.md) and [completion #692](https://github.com/banodoco/astrid-dev/pull/692) | SR-1–7 foundation delivered; reuse existing record/check/view/issue machinery and assertions. |
| [R15 publication receipt](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7174076695), [qualification](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7172609349) | Actual 25 November predecessor, integer/floor15 and exact product sources. Receipt abbreviates hashes and reserves owner long-lived proof; recover actual artifacts/readback, do not guess missing bytes or mark reserved proof done. R15 brief's Draft/Not pinned drift needs historical nonpublishing adoption. |
| App main and R16 branch `cc1d48f016fde55ad6b0609c619d8a4bcec56823` | R16 App ref now exists but equals R15 source; source/ref presence does not prove a refreshed R16 consumer or matched installed tuple. |
| Agent R16 `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`; Runtime R16 `55a541a7ab904873e63510e581a60742e1b83fb8` | Ongoing product work, not final pins. Agent's observed lock still names R15 Runtime `686ca695469bda48cd40a70824c4ccef2a137284`; a checkout overlay is not packaged proof. Refresh before integration. |
| [App release guard](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/scripts/installer/release-guard.mjs) | Existing tuple/bootstrap/increment checks reusable. Missing required or changed floor0 bypasses its nonzero floor predicate; preserve floor policy with focused negatives. Source-derived finding, no executed exploit claimed. |
| [App canary](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/scripts/installer/served-manifest.mjs) | Compares only four manifest fields and three bootstrap byte buffers, then pin coherence. Extend to complete approved manifest and actual deployment/build identity. |
| [Hosted status](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/shared/lib/updates/updateStatus.ts), [local status](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/config/vite/localUpdateStatus.ts) | Hosted independently reads build and manifest without release equality; local enforces equality and a 16 KiB bound. Agree minimal compatible shared contract with P29/P30; preserve resource bounds. |
| [Dev ruleset 27040267](https://github.com/banodoco/astrid-dev/rules/27040267) | Active but zero approving reviews, no code-owner or stale-review rule, nonstrict checks and an always-bypass integration. App main reports unprotected. Not proof of the required publish boundary; settings outside observed APIs remain unknown. |
| [baseline-diff.py](../../env/baseline-diff.py) | Missing derives only from formerly-passing tests. Full original collection/execution coverage, including formerly-failed missing IDs, needs the existing bounded P31 inventory correction. |
| [P38 #2050](https://github.com/banodoco/astrid-dev/issues/2050), [P93 #2032](https://github.com/banodoco/astrid-dev/issues/2032), [P94/P90 #2051](https://github.com/banodoco/astrid-dev/issues/2051) | Actual current implementation owners and proof gates; P31 consumes accepted producer identities and retained native results, not draft heads or historical whole-plan completion labels. |

The R15 manifest includes VibeComfy, lifecycle, motion pack digest and complete tool assets; preserve them in the full publication payload. P29's #82/#208 proposals are already closed unmerged. `pin.mjs` no longer automatically increments release on every run; the earlier source claim is historical.

## Qualification-policy decision

**D-SYN-1 remains proposed, not accepted.** Recommend the smallest dependable gate:

Every effective required status on the exact candidate and every retained positive/negative supported journey passes. No known harm, supported-path failure, new/lost failure or unclassified failure is accepted. Establish complete executed/collected inventory against the actually served predecessor, namespaced by repository, job family, OS/architecture, selector/configuration and full test identity. Combine all shards within each family; retain subtests/duplicates, actual producer exits and collection results. Missing/skipped/cancelled/uncollected/newly quarantined cases are not passes; a formerly-red disappeared case needs an explicit removal/equivalence disposition too.

An actually executed **nonrequired inherited red** may remain only with a named evidence-backed nonharm classification, owner acceptance and later owner/task. “Old” or “same as baseline” does not prove harmless. If actual protection or owner policy still requires literal all-green, that remains binding: repair the minimum or hold R16. P39/P91 broader cleanup stays R17; P52/P53/P85 remain removed from R16. Existing qualification/measurement infrastructure remains required.

Concrete alternatives: adopt this bounded policy with retained safety/required gates; or require all jobs green and accept the added repair effort. Only the owner can resolve the difference. The final programme must display which rule applies; this planning text does not grant a waiver.

## Remaining control and product decisions

| Decision or fact needed | Recommendation / alternative | Consequence and authority |
|---|---|---|
| Protected publisher and deployment interval | Reuse the existing trusted workflow and deterministic generated-only App PR with exact checks; hold auto-deploy during an incompatible interval or prove that interval safe. An equivalently enforced route is acceptable. | Owner/deploy owner supplies actual effective controls and allowed actors. Unknown controls block publication, not independent record/status preparation. No extra scheduler or broad bypass by default. |
| Who can approve Final | Preserve owner-only final approval and narrow CODEOWNERS coverage for release/gate paths. Any maintainer delegation must be explicit. | A stale historical approval or source author is not final owner go. Ordinary draft editing stays independent. |
| Required floor or supported-route changes | Carry actual floor15 and retained support. Only propose16 with a concrete migration reason and proof, or a route restriction with explicit consequences. | These are conditional owner decisions, not mandatory new questions or silent reductions. |
| Missing legacy/long-lived evidence | Recover actual R15 receipt artifacts and owner witness; record unknowns honestly. Backfill older releases only from real receipts. | Historical adoption cannot publish or fabricate a hash/version. Do not block R16 on unrelated exhaustive history backfill. |

Routine renderer/parser/adapter choices are implementation judgments within retained contracts. No new broad ambiguity pass is needed; investigate only a named uncertainty that changes one of these decisions.

## Effort and proof limits

Remaining P31-specific effort is **4–7 implementation plus 2–3 integration/rehearsal/independent-review engineering days**. Shared native product matrix, product repairs and hardware/owner waiting time are outside this estimate. If actual protected deployment or candidate preparation requires substantive repair, **10–14+ total days** is the contingency, not an automatic extra workstream.

Current implementation branches, sessions, owner-go procedures and original regression obligations remain intact. This record authorizes no protection mutation, product implementation dispatch, release promotion or publication.
