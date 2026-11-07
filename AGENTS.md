# Astrid Dev repository instructions

**Start with [the Astrid development skill](skills/astrid-dev/SKILL.md).** It is the single agent entrypoint and routes work through the [domain map](skills/astrid-dev/references/domains.md). The [contribution principles](docs/contribution-design-principles.md) govern how much process to introduce; the [contributor workflow](docs/contribution-workflow.md) owns GitHub claims, proposals, review and documentation authoring.

## Sources and scope

- **Vision:** [visions/](visions/README.md) owns artistic ambition, pillars, creator-facing principles and assessed gaps. The public vision feed is generated, not a parallel editorial source.
- **Projects:** [plans/index.md](plans/index.md) alone owns project status, owner, priority and estimate. A substantial project has [three files](docs/project-format.md): outcome in `plan.md`, inherited sources/decisions in `inputs.md`, tasks/proof in `tasks.md`. Bugs, small fixes and copy edits are issues/PRs, not projects.
- **Technical instructions:** Product-specific code and API documentation belongs in the product repositories. Stage-specific [skills](skills/astrid-dev/SKILL.md) extend the same contributor process; they do not supersede the [shared run contract](skills/astrid-dev-shared/run-contract.md).

## Authority and proof

A claim, project draft, catalog status, PR label or successful CI **does not** authorize product execution, spending, user-data access, integration or release. Respect existing STOP/pause instructions and the actual product repository's permissions. Preserve accepted scope, source and donor SHAs, dirty/retained changes and review state. Never invent approval or claim that a checked source proves a different integrated candidate. Keep credentials, private logs and `.otto/` run state out of public PRs.

- **New or materially redefined gap:** Use the [gap boundary rules](visions/gaps.md#reviewing-a-new-or-redefined-gap) and include its specified assessment in the PR description. Evidence-only status changes do not demand that ceremony.
- **New project or changed scope:** Follow [the planning skill](skills/astrid-dev-plan/SKILL.md); cite real prior art and the owner's accepted decision. Planning does not grant permission to start.
- **Project to `done`:** Use the [completion PR template](.github/PULL_REQUEST_TEMPLATE/project-completion.md) and include the `## Completion assessment — Plan NN` with actual evidence, implementation PRs, integrated candidate, models used, unproven claims and dispositions for each linked gap. CI checks the presence/relationship, **not the truth**; reviewers establish sufficiency.
- **Implementation and release:** Use [Iterate](skills/astrid-dev-iterate/SKILL.md) and [Release](skills/astrid-dev-release/SKILL.md) with exact source identity and focused checks. Product integration is not public publication.

## Documentation checks

For changes to the vision, pillars, principles or gaps, first run `python3 scripts/export_public_vision.py --sync-readme` to refresh the derived [vision overview](visions/README.md). Then run `python3 scripts/check_docs.py` and `python3 scripts/export_public_vision.py` to validate documentation and the public projection. The catalog is the only project register; no README status/owner preview needs manual synchronization. The [documentation workflow](.github/workflows/docs.yml) runs on every PR and every `main` push, validating all local Markdown links, catalog/gap/project integrity, PR evidence on transitions, and the versioned vision feed. It publishes only after validated `main` pushes; external product claims are reverified against their actual source when used, not magically refreshed by documentation CI.
