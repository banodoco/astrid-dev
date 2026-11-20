---
description: Write Astrid agent instructions once as Markdown and publish selected documents as agent skills.
---

# Astrid agent documents

This directory is the only authored home for the agent instructions used to build and contribute to Astrid. These are ordinary Markdown documents; a skill is a **generated distribution format**, not a second source.

## Where instructions live

- [Start](start.md) routes requests to an existing contribution, procedure, or accountable role.
- [Roles](roles/) define a continuing identity and its authority. Each role is a single file: Leader, Orchestrator, Manager, Worker.
- Role-specific workstreams live in the sibling folder of their role file (for example manager/chatgpt-packet.md). They inherit that role's authority and are usually loaded through it.
- [Shared workstreams](shared/workstreams/) are independently callable procedures available to roles permitted by the active assignment.
- [Shared run policy](shared/run-contract.md), [glossary](shared/glossary.md) and [domain map](shared/domains.md) are referenced sources, not another role.
- [Environment guides](guides/) and executable helpers remain separate supporting resources.

## Author a document

Write one Markdown file with a useful first-level heading and one plain-text description in frontmatter. Add the optional line shown below if independently discovering the document as a skill is useful.

~~~yaml
---
description: Describe what this does and when to use it.
skill: true
---
~~~

There is no authored SKILL.md. The filename stem gives the generated skill name: manager.md becomes astrid-dev-manager; gap.md becomes astrid-dev-gap. Directory placement determines ownership, **not** the generated identity. Duplicate skill stems are an error. Omit skill: true for shared reference guides or workstreams that are only meaningful within their parent role.

A role contains sections for Responsibility, Authority, Responsibilities, and Handoff. A workstream contains sections for When to use, Outcome, Inputs, Procedure, and Completion. Keep actual steps in the procedure rather than repeating a separate five-field contract. Authorization comes from the owner and active run, never from choosing a skill.

## Build and install

From the repository checkout:

~~~sh
python3 scripts/astrid_dev.py skills build
python3 scripts/astrid_dev.py skills check
python3 scripts/astrid_dev.py skills install --dry-run --destination /existing/skills
python3 scripts/astrid_dev.py skills install --destination /existing/skills
~~~

Packages are generated under the ignored .generated/skills/ folder. Each standard SKILL.md has a relative link to canonical references in this checkout, so the skill directory must be installed **as a symlink** to that package while the checkout remains available. Check command and symlink support in each environment. The installer never replaces foreign entries. Skill packaging does not grant additional execution, installation, spend, publication or merge rights.
