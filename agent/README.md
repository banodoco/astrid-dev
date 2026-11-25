---
description: Write Astrid agent instructions once as Markdown and publish selected documents as agent skills.
---

# Astrid agent documents

This directory stages the Markdown-first agent instructions for the planned migration. During the transition, the existing authored [`skills/`](../skills/) tree and its current consumers remain authoritative. The new `agent/` documents and their generated packages are a candidate until the coordinated MS-7–MS-9 cutover is verified and accepted.

## Where instructions live

- [Start](start.md) routes requests to an existing contribution, procedure, or accountable role.
- [Roles](roles/) define a continuing identity and its authority. Each role is a single file: Leader, Orchestrator, Manager, Worker.
- Role-specific workstreams live in the sibling folder of their role file (for example manager/chatgpt-packet.md). They inherit that role's authority and are usually loaded through it.
- [Shared workstreams](shared/workstreams/) are independently callable procedures available to roles permitted by the active assignment.
- [Shared run policy](shared/run-contract.md), [glossary](shared/glossary.md) and [domain map](shared/domains.md) are referenced sources, not another role.
- [Environment guides](guides/) and executable helpers remain separate supporting resources.

## Shared workstreams

Choose a procedure for an already-authorized task; selecting a workstream never grants a new role, approval, or permission. This is the human navigation index for the nine original shared workstreams; role-specific procedures remain linked from their roles. It is not a package allowlist: a new valid workstream with `skill: true` is discovered and packaged from its Markdown source without an entry here. Add a navigation link when that workstream is accepted for general use.

- [Bugfix](shared/workstreams/bugfix.md) — Investigate incidents, reproduce failures and record safe recovery.
- [Gap](shared/workstreams/gap.md) — Define vision gaps and evidence for closure.
- [GPU validate](shared/workstreams/gpu-validate.md) — Run authorized hardware probes with spend and cleanup controls.
- [Green](shared/workstreams/green.md) — Compare exact tests to a baseline and repair real regressions.
- [Improve](shared/workstreams/improve.md) — Change Astrid Dev's canonical rules and checks.
- [Iterate](shared/workstreams/iterate.md) — Implement and prove one scoped change.
- [Merge](shared/workstreams/merge.md) — Review and dispose of a contributor PR under its authority.
- [Plan](shared/workstreams/plan.md) — Define an independently useful, testable project.
- [Release](shared/workstreams/release.md) — Integrate and qualify a release; publish only on the owner's GO.

## Author a document

Write one Markdown file with a useful first-level heading and one plain-text description in frontmatter: a nonempty single line of at most 240 characters, ending in punctuation. Add the optional line shown below if independently discovering the document as a skill is useful.

~~~yaml
---
description: Describe what this does and when to use it.
skill: true
---
~~~

In the new `agent/` tree, sources are not authored as `SKILL.md`; the existing `skills/` tree still contains authored `SKILL.md` files during the transition. The filename stem gives the generated skill name: manager.md becomes astrid-dev-manager; gap.md becomes astrid-dev-gap. Directory placement determines ownership, **not** the generated identity. Duplicate skill stems are an error. Omit skill: true for shared reference guides or workstreams that are only meaningful within their parent role.

A role contains sections for Responsibility, Authority, Responsibilities, and Handoff. A workstream contains sections for When to use, Outcome, Inputs, Procedure, and Completion. Keep actual steps in the procedure rather than repeating a separate five-field contract. Authorization comes from the owner and active run, never from choosing a skill.

Each workstream has a defined, independently verifiable outcome. Keep its full execution instructions and authoritative discovery metadata in its own document; a role's navigation summary is not a second source. Never replace actual steps or proof with placeholder summaries. Shared run policy and shared workstreams have one authoritative home; do not duplicate their instructions. Keep role responsibilities, defaults, selection rules and composability guidance in the role document. Do not add folders for workstreams that need no variant. The source checks validate structure, not the correctness of instructions, sufficiency of evidence or authority of the actor.

## Build and install

From the repository checkout:

~~~sh
python3 scripts/astrid_dev.py skills build
python3 scripts/astrid_dev.py skills check
python3 scripts/astrid_dev.py skills install --dry-run --destination /existing/skills
python3 scripts/astrid_dev.py skills install --destination /existing/skills
~~~

The candidate packages are generated under the ignored `.generated/skills/` folder. Building them alone does not switch active legacy consumers; running the install command can retarget owned links in the selected destinations. Each generated `SKILL.md` links to its references in this checkout, so the skill directory must be installed **as a symlink** to that package while the checkout remains available. Check command and symlink support in each environment. The installer never replaces foreign entries. Skill packaging does not grant additional execution, installation, spend, publication or merge rights.
