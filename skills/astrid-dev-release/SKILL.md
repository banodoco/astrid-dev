---
name: astrid-dev-release
description: Integrate Astrid changes into a named pre-main destination or coordinate an explicitly scoped Astrid build, release, deployment, or publication across Agent and App. Use the repository runbooks for implementation details; this skill owns the cross-repo workflow and action boundaries.
---

# Astrid development release workflow

Use this skill for developer integration and release work across Astrid Agent and App. It was assembled from product runbooks, gates, and tools: neither inspected product checkout contained a dedicated developer release skill. The end-user `astrid-setup` skill is unrelated. See [authoritative sources and discovery provenance](references/sources.md).

## Select the requested lane

First identify the concrete outcome and target from the user’s request:

1. **Pre-main integration:** integrate specified changes into the actual, named integration destination. This does not imply an App deployment, installer tuple change, version release, registry publication, or any other publication.
2. **General Agent or hosted App release/deployment:** prepare or promote the explicitly named product artifact or deployment. Separate source changes, artifact creation, deployment, and public verification; a build or passing checks do not perform the later actions.
3. **Agent/Runtime installer tuple update:** update the shared installed compatibility tuple only when requested. This is separate from an App web-bundle deployment.
4. **Extension-platform RC:** use only when the request names the extension-platform release. This is a distinct, evidence-heavy App/Astrid candidate lane, not the routine hosted App path.

If the user has already authorized a specific action in the conversation, carry it through without asking them to authorize that same scope again. Do not infer missing scope: a merge, green check, or prior authorization to prepare a build does not authorize deployment, registry publication, or a different target.

## Freeze inputs before work

Record each participating repository’s canonical identity, actual branch/ref and HEAD SHA, dirty state, and role as base or donor. Preserve existing user changes. Record the intended integration destination from the active plan or user instruction; never invent a branch name or substitute a convenient checkout. For a paired release, freeze the exact Agent, Runtime, and App commits and the compatibility tuple the artifact is meant to use. If a required source ref, target, tuple value, or publication authority is missing, state the specific unresolved input and stop only the dependent action.

Respect the target repository’s local rules, including any pause or allowed-destination constraint. Use ordinary pushes only when explicitly in scope; never force-push. Preserve donor provenance and the exact candidate identity in the resulting evidence.

## Integrate and select proof narrowly

For pre-main integration, build an isolated candidate from the frozen target and requested donors, retaining each donor’s provenance. Run the scoped checks and any review required by the applicable plan, then promote that same exact reviewed HEAD to the explicitly authorized target with an ordinary push. Do not substitute a staging framework or different candidate. Reuse valid proof for unchanged inputs. Choose the smallest feature-focused selectors that cover the changed behavior, plus narrowly relevant canonical checks for changed pins, locks, or build artifacts. Run only explicitly scoped checks necessary for the requested outcome. Never run broad suites, including opt-in lanes: this includes `make check`, `make ci`, `make release-check`, full affected suites, and broad extension evidence runs such as all 23 workstreams. Historical product gate instructions do not override this rule. Select focused checks from the affected behavior and product contract. If prescribed release evidence cannot be produced without a forbidden broad run, record the exact unmet evidence and resolve the scoped contract; never run the banned gate or claim completion without that evidence. See the [shared run contract](../astrid-dev-shared/run-contract.md).

When a focused check fails, retain its exact command and candidate identity, fix the in-scope cause, and rerun that check. Do not discard unaffected passing evidence or claim checks passed without results.

## Prepare a release or deployment

Use the product-owned build and release interfaces instead of copying implementation logic into this skill:

- **Agent:** consult the reproducible-release runbook for hashed dependency locks, installed-wheel evidence, toolchain records, and Remotion’s pinned Node/npm closure. Keep lock and package rules in the repo. The product’s `Makefile` targets and `scripts/reshape/` tools remain authoritative. Historical `make check` and `make ci` descriptions do not override targeted-check policy.
- **Hosted App bundle:** use the deployment guide’s source-of-truth files (`Dockerfile`, `Makefile`, `railway.toml`, and `package.json`) and its hosted editor-only build path, `npm run build:hosted`, when preparing that artifact. `npm run build` and `npm run dev:local` are not hosted releases. For Docker, Make deploy-target, or Railway configuration changes, use the guide to select relevant deploy checks; do not silently turn a broad gate into the default. The served-manifest canary verifies a deployed public manifest; it does not deploy or promote the App.
- **Agent/Runtime installer tuple:** use App’s `scripts/installer/pin.mjs` for the authorized Agent/Runtime tuple. Derive the paired Runtime commit and schema digest from the pinned Agent source, then use the monotonic release guard. When tuple regeneration is required by the authorized release, do it as part of that work without seeking separate authorization. Preserve the exact `agent.sha`, `runtime.sha`, and `runtime.schema_digest` provenance. Do not confuse this tuple with an App/Astrid extension RC pair.
- **Extension-platform RC:** follow the App extension release runbook and checklist as the authority for this lane. Its final ship verification expects frozen candidate refs, pinned tools, clean evidence trees, and complete receipts. Treat its current manifest/evidence snapshot as historical discovery only; inspect the actual requested candidate. Do not apply its RC process to routine App deployments.

Keep release-specific identity, lock, manifest, evidence, and check implementations in their product repositories. Link to the authoritative product contract instead of copying it. Reuse unaffected qualification where its exact inputs still match; qualify the installed closure that matters to the requested artifact without imposing every release proof on a small change.

## Complete only the authorized actions

Report the exact integrated or built candidate, selected checks and results, source tuple, and remaining actions. Perform a deployment, tag, registry publication, or public release only when that action, destination, and scope are explicitly authorized. If authorization covers preparation only, stop with a reviewable prepared artifact and the precise next action; do not treat evidence or a successful build as publication authority. Verify any public/deployed result using the relevant product-owned canary or receipt and report its observed result.
