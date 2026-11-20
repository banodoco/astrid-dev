# Skill structure

- [Astrid-dev](../astrid-dev/SKILL.md) is the entrypoint and routes requests.
- `skills/roles/astrid-dev-*/SKILL.md` defines **who is responsible** (Lead, Orchestrator, Manager, Worker).
- `skills/shared/workstreams/astrid-dev-*/SKILL.md` defines reusable, independently discoverable **shared workstreams**, such as Plan, Iterate, Release, Merge and Gap. They have a defined result and inherit the invoking role's authority.
- `skills/shared/` owns shared rules, terms, templates and reusable workstreams; the shared workstreams have no second authoritative copy.
- A role's optional `workstreams/` holds **role-specific operating patterns**, such as fresh-packet dispatch, as Markdown documents; they inherit the role and are not separately installed skills.

## Independent workstream skills

A shared workstream that an agent can invoke directly lives under `skills/shared/workstreams/astrid-dev-<name>/SKILL.md`. Its folder name must exactly match its frontmatter `name: astrid-dev-<name>`; its `description:` is a nonempty single line. `sync.sh` installs it as a flat, independently discoverable skill without changing its name. A role may invoke it but cannot gain permissions merely by selecting it. There is no independently installed `capabilities/` category or standalone Planner role. Legacy relative symlinks preserve old Markdown links without maintaining duplicate skills; `sync.sh` ignores them.

A role-specific workstream stays beneath its parent role as a `.md` file when it is only meaningful inside that role. Each role skill also contains a generated **Shared workstreams** section listing the available independent skills by name and link only, derived from their skill folders; it does not duplicate descriptions or grant permissions.

## Workstream discovery

Every direct role-specific `workstreams/*.md` file (excluding an optional `README.md`) owns its display title in its first `# Workstream: ...` heading and a **required one-line description** in frontmatter:

```markdown
---
description: Perform this operating pattern for the stated assignment and return verifiable evidence.
---

# Workstream: Example
```

The description must be exactly one plain-text sentence on one line, no more than 240 characters, ending in punctuation. Keep instructions in the workstream body; do not repeat its discovery description in the parent skill. Nested `workstreams/<guide>/` files are supporting documentation, not separately indexed workstreams.

The parent `SKILL.md` keeps its shared responsibilities, defaults, selection rules and composability guidance as handwritten text. Only the list of file-backed workstreams is generated between `<!-- workstreams:start -->` and `<!-- workstreams:end -->`. Edit the workstream file, not its parent list.

`python3 scripts/astrid_dev.py sync` regenerates the parent indexes; the existing documentation workflow refreshes them on `main` when its GitHub App is configured. Ordinary `python3 scripts/astrid_dev.py check` and PR CI **always** validate every workstream's one-line description, including new files. The generated shared-workstream lists are validated against the standalone skills and registered as explicit role targets. The CI write-back allowlist remains explicit: a new parent skill with workstreams must first be registered in `scripts/workstreams.py`'s `PARENT_SKILLS`.


Every independently discoverable role or shared workstream skill retains its namespaced `name: astrid-dev-*` and matching leaf directory name. [`sync.sh`](../../sync.sh) installs **flat symlinks** to the canonical packages for Claude/Codex discovery; the extra grouping directory does not appear in installed skill names. Do not duplicate instructions or add folders for workstreams that need no variant. Follow the [run contract](run-contract.md).
