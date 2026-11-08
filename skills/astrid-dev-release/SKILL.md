---
name: astrid-dev-release
description: Freeze, compose, qualify, integrate, or publish an explicitly scoped Astrid Runtime/Agent/App candidate. Release is the sole workflow for cross-repository integration and publication; it does not grant unrequested deployment or publication authority.
---

# Astrid development release

Use this workflow for cross-repository integration, candidate qualification, and explicitly authorized release or publication. [Iterate](../astrid-dev-iterate/SKILL.md) owns assigned implementation and repair; [Plan](../astrid-dev-plan/SKILL.md) prepares a new plan. Release consumes accepted work and owns integration and publication. The shared run contract is the authority for source identity, proof policy, and review budgets; do not restate or reset those choices here. Use the [domain map](../astrid-dev/references/domains.md) to locate current product-owned release runbooks; verify the actual source SHAs before integration.

## Choose the requested lane

Name the outcome, destination, and authorized actions before acting:

1. **Pre-main integration:** compose requested donors into the named integration destination. This does not imply deployment, installer tuple change, version release, registry publication, or public release.
2. **Agent or hosted App artifact/release/deployment:** prepare or promote the named artifact or deployment. Source integration, artifact creation, deployment, and public verification are distinct actions.
3. **Agent/Runtime installer tuple:** update the shared installed compatibility tuple only when requested; this is separate from an App web-bundle deployment.
4. **Extension-platform RC:** use only when the request names this lane. Its App/Astrid candidate is distinct from a routine hosted App deployment.

Carry out actions already authorized in the conversation. A merge, green check, or authorization to prepare does not authorize a different destination, deployment, tag, registry publication, or public release. Do not ask again for authority already given.

## Freeze and compose the candidate

Freeze the named base and each donor: canonical repository, actual ref, HEAD SHA, dirty state, and role. Preserve existing project plans, user changes, and their candidate/review scope. For a paired product artifact, record the exact Runtime, Agent, and App SHAs and intended compatibility tuple. Do not infer missing targets, tuple values, or publication authority.

Compose an isolated candidate from the frozen base and donors, preserving provenance. Record its exact head/tree identity and affected paths. Reuse existing evidence only when its inputs still match. Build or regenerate through product-owned interfaces; release-specific locks, manifests, artifact receipts, and gate implementations remain in the product repositories.

## State the claim and select evidence

Before checking, state the release claim and map each required claim to its exact candidate-bound evidence. Run only authorized, focused checks for affected behavior and the prescribed review. Never run broad suites, including opt-in suites or broad RC matrices. The historical release gates do not authorize running them. If a required claim has no lawful focused evidence available, mark that claim and the candidate **unqualified**; do not fabricate a pass, silently reduce the claim, or imply that an input feature candidate automatically qualifies the composed Runtime/Agent/App tuple.

The source release contract identifies these protected product invariants:

- The installed Runtime/Agent/App combination is one integrated tuple; repository branches qualified separately do not qualify it together.
- Install, update, rollback, keep-data uninstall, migration, and update-bridge journeys retain their product semantics. The frozen `POST /v1/update` contract includes its signatures, errors, stop payload, proxy policy, and journal linkage. Lost-ack recovery requires stable operation identity, positive evidence nothing is running, one continuation, journal precedence, and refusal under unknown state; recovery does not send an update POST by itself.
- The App update guard resolves actions, flushes guarded persistence, then starts an update. Failed or delayed saves/flushes, recovery-needed state, edits during flush, pending identity, owner change, unmount, IndexedDB failure, stale markers, and restart replay mean no POST; a successful save means exactly one POST. Status GETs only observe. A local recovery snapshot is not a saved draft.
- Timeline persistence is qualified on the integrated tuple. Advertised GPU capabilities require live evidence at RC; prepared-only output is not live evidence. Evidence must bind the actual candidate and inner command result, not a wrapper status or historical baseline.

Apply change-directed invalidation: a changed input invalidates only proof that depends on it, while protected exact-head claims require proof for the exact integrated head. If a scoped check fails, hand the same failure to [Iterate](../astrid-dev-iterate/SKILL.md) as a concrete repair assignment, preserving its exact command, candidate identity, evidence, owner, and context. Keep unaffected passing evidence. Do not start a separate debug loop or ask an advisor for routine approval; consult the advisor ([Orchestrate](../astrid-dev-orchestrate/SKILL.md), advise path) only for a genuine blocker or consequential judgment.

## Promote or publish

After scoped checks and prescribed review pass, promote the **same reviewed head** to the explicitly authorized target using an ordinary push. Never force-push or substitute a different candidate. Movement of a target ref invalidates only affected proof; re-evaluate its dependencies and retain unaffected evidence. A failed check or unresolved review blocker means no promotion.

A publish never turns a passing check red. On each promotion PR into a product `main`, compare its checks by name with that `main`: any check that passes on `main` and fails on the PR blocks the publish. Report each `main`'s red checks by name; they are not this publish's work.

**Publishing an installer release** (Runtime, Agent and App to `main`):
1. **Owner's go, in this session.** As soon as the candidate qualifies, ask the owner for the go here, naming the exact SHAs. A go recorded elsewhere, in a plan's `inputs.md` or another session, does not satisfy this session's permission check. If a merge is refused as a production action, stop and ask the owner; don't retry another way.
2. **Merge in order:** Agent, then Runtime, then App, whose manifest names the other two. Use merge PRs or fast-forwards of the exact reviewed SHAs.
3. **Wait for the deploy.** The App merge starts a production deployment. The served-manifest canary runs only when that deployment succeeds, so a canary run before then shows as skipped. Wait for both, then confirm `https://astrid.haus/install-manifest.json` serves the release and the exact SHAs.
4. **Bring integration branches up to `main`.** Fast-forward each `int/<project>` to its `main` with `git push`, never forced. Cloud sessions can't write refs through the GitHub API.
5. **Close the project** through [Manage](../astrid-dev-manage/SKILL.md)'s completion PR.

For product artifact preparation, follow the current product runbooks rather than copying their procedures here:

- **Agent:** [reproducible release](https://github.com/banodoco/astrid-agent/blob/main/docs/runbooks/reproducible-release.md) and [release recipe](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/release-recipe.md) own locks, toolchain, installed artifact, and paired-release receipts.
- **Hosted App:** [deployment and migration guide](https://github.com/banodoco/astrid-app/blob/main/docs/structure_detail/deployment_and_migration_guide.md) owns the hosted editor-only build path (`npm run build:hosted`) and Docker/Railway configuration. A build does not deploy; the served-manifest canary observes public state but does not deploy.
- **Installer tuple:** App's `scripts/installer/pin.mjs` and release guard own tuple generation and monotonicity. Preserve `agent.sha`, `runtime.sha`, and `runtime.schema_digest`; do not confuse this tuple with the extension RC pair.
- **Extension RC:** App's [extension release runbook](https://github.com/banodoco/astrid-app/blob/main/docs/extensions/extension-release-runbook.md) and [checklist](https://github.com/banodoco/astrid-app/blob/main/docs/video-editor/extension-platform-release-checklist.md) own this lane. Inspect the requested candidate; historical snapshot material is discovery context, not current evidence.

Deployment, tagging, registry publication, and public release each require explicit scope and authority. Verify a deployed/public outcome through its product-owned receipt or canary. Report exact candidate identity, claims, focused checks and results, review result, tuple/artifact identity where relevant, and any unqualified claim or remaining authorized action.
