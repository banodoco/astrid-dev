# One local and cloud runtime

**Project:** One local and cloud runtime

**Goal:** The same core and capability contract run on a creator's computer or a headless remote machine, with explicit workspace custody, placement, permissions and verified results.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** Plan 100 worker contract, Plan 103 native core and accepted placement contract; independent scope/release review; coordinate Plans 25, 26 and 32 rather than duplicate them.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Local files, cloud assist](../../vision/gaps/F-005-local-files-cloud-assist.md) (supporting) · [Fully hosted workspace](../../vision/gaps/F-006-fully-hosted-workspace.md) (supporting) · [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting)

**Contributes to closure:** LS-006: E6: shared local/headless remote runtime and worker contract.

## Outcome and scope

**Draft proposal — owner agreed the direction on 26 November 2026, but detailed project scope, independent challenge and release placement are pending. No implementation authorized.**

Package and qualify the same native workspace core and worker contract for local use and an isolated headless remote deployment. Runtime roles can be configured as workspace authority or scoped worker, with one selected authority per workspace. Local-first work stays local unless explicit delegation sends scoped inputs to an authorized remote worker. A fully hosted deployment may own its workspace explicitly; it is not a second writer of the local realm. Use same typed task, capability/engine/machine placement, grants, event, cancellation, receipts and output identity contracts in both environments.

Reuse Plans 25/26 cloud product and Plan 32 generation placement, remote-worker deployment/activation, existing recorded provider boundaries and Plan 36 credentials. Package native artifacts for declared deployment platforms; validate connection/identity, bounded input transfers, result verification, retries/disconnect/expiry and cleanup. Make budgets/spend consent and provider availability visible. CPU-only isolated remote witness first; separately authorize real provider/GPU proof. Distinct from launching an account service, billing system or another scheduler.

Out: multi-master sync, automatic data migration to cloud, new hosted product features (Plan 26), cloud-assist user journey scope (Plan 25), all engine/machine portability (Plan 32/F-008), unapproved paid infrastructure or production deployment.

## Existing work and decision

Runtime has remote_worker_activation.py/deployment.py and local worker composition; workspace.v1 task/lease contract and placement plans already provide shared concepts. Plans 25 and 26 own different custody outcomes; Plan 32 owns generation placement and Plan 50 owns recorded provider failures. Avoid adding another scheduler, account service or placement concept. See [architecture](../100-language-independent-foundation/architecture.md). See [inputs](inputs.md#planning-evidence) for alternatives, review limits and outstanding owner decisions. This is not an authorization to alter accepted existing projects.

## Sequence and readiness

Inventory actual remote/local role contracts and cloud plan scope; agree smallest deployment parity slice with Plan 100. Build reproducible local and isolated remote artifacts using Plan 103 native core; run same task corpus and scoped transfer/recovery. Coordinate any real remote provider proof and integration with existing cloud plan owners. Do not assign a cloud release or perform spend by planning. The [task outline](tasks.md) is not a dispatch packet. Re-estimate after the first bounded evidence slice; do not assign to a release or start product work without a recorded run decision.

## Interfaces and handoff

Consumes Plan 100 worker ABI and conformance, Plan 103 native runtime and custody, existing Plan 32 placement, credential and cloud worker contracts. Produces one source/version manifest, reproducible headless artifacts, local/isolated remote execution parity receipts and a deployment/authority handoff for Plans 25/26. Does not claim the latter product outcomes complete.

## Completion

- Same versioned native Runtime binary family/source and task contract in local and isolated remote deployment; same independent capability runs on both, receives verified output/receipt and explicit destination without alternate domain code path.
- Local authority delegates a bounded task to remote worker: project stays locally authoritative, only approved inputs transmitted, remote output verified and linked. Separately demonstrate headless remote authority using an independent test workspace; no hidden replication.
- Disconnect, expired lease, cancel, unauthorized upload, stale/revoked credentials, duplicate settlement, unsupported hardware and unapproved spend fail with named safe outcomes; verify remote cleanup and custody.
- Record exact environment, artifact/manifest, inputs/outputs and provider limitations. CPU fixture proves protocol/deployment only; real GPU/cloud product qualification remains with authorized owner plans.

Scope completion is contribution to LS-006, not automatic gap closure; qualify the integrated release separately and record limits.
