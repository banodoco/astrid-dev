# P95-SK — one validated workspace skill configuration

**Source:** P95-19d real generic proof; [BLOCKED](https://github.com/banodoco/astrid-dev/issues/1886#issuecomment-7222163084). **Route:** X / normal Chat Extra High. **Repository:** `banodoco/otto`, branch `p95/ot-skill-config` → `main`. **Base:** `13cf97b873558ffa4038963bb252fd4f26eecead`. One packet and one fresh session.

## Outcome

Enable a workspace to opt into its existing validated `SkillConfig` compatibility options once in `otto.toml`, so the generic `otto skills build/check/install` commands and generic `skill-packages-current` check use the same resolved settings; expose the same resolved value for a consumer adapter to reuse. Current Dev uses a custom generated header, lock/staging names and legacy link ownership, while generic Otto constructs defaults for the same output path. Dev build → Otto check and Otto build → Dev check therefore fail today. Do not special-case any workspace or use two different output trees to conceal the incompatibility. Defaults and behavior of existing blank, Marketing and unconfigured workspaces stay unchanged.

**May touch:** Otto config declaration/validation and immutable workspace model (`otto/config.py`), configuration construction in `otto/checks.py`, `otto/skills/` only as needed for shared validation, CLI wiring if necessary, Otto contract/docs and narrowly scoped new Otto tests/fixtures. No changes to the Dev repository. **Must not touch:** assertions/expected values in existing tests, generic check identities/order, link checks, default output format, namespace/custody checks or ownership safety. Never weaken validation or create a default compatibility mode.

## Step 1 — inventory and stop

Before editing, map every existing keyword-only `SkillConfig` field and validator, its Dev value from `scripts/agent_documents.py` at project base `dc2e82f0fb65da9ebe2321f637c810318af2333b`, all consumers (`checks.skill_config`, CLI build/check/install and generic check), lock naming, source locations and cycles. Propose the exact optional TOML schema, type validation, safe path/filename constraints and immutable resolved interface, including an adapter reuse path that cannot recurse during workspace loading. Include behavior for absent, unknown, invalid or hostile values, exact defaults and how existing users remain compatible. Post the table and stop for Lead decision.

## Required proof (Lead)

Run all Otto unit tests and default/blank/Marketing fixture checks. Add focused tests for every opt-in field, invalid and unknown values, source-located failures, default equivalence and shared config object semantics. Prove two deterministic builds, stale-file failure, custody/ownership and common lock serialization, and disposable temporary installation. Lead integrates the eventual exact Otto head into a consumer proof: Dev-build → Otto-check, Otto-build → Dev-check, both output trees byte-identical, shared locks, and negative fixtures; Dev-side adapter/config edits are a separate follow-up. The packet session does not clone, build, test, dispatch CI, merge, edit a plan record or start another packet. Open a draft PR and end `READY-PROOF <repo> <PR> <head> <selectors>`.
