# Skill structure

- [Astrid-dev](../astrid-dev/SKILL.md) is the entrypoint and routes requests.
- `skills/roles/astrid-dev-*/SKILL.md` defines **who is responsible** (Lead, Orchestrator, Manager, Planner, Worker).
- `skills/capabilities/astrid-dev-*/SKILL.md` defines **what specialist work to do**, reusable across roles.
- `skills/shared/` owns shared rules, terms and templates.
- A skill's optional `workstreams/` adds **how it operates in a particular setup**, with supporting scripts beside that workstream, not another skill.

## Workstream discovery

Every direct `workstreams/*.md` file (excluding an optional `README.md`) owns its display title in its first `# Workstream: ...` heading and a **required one-line description** in frontmatter:

```markdown
---
description: Perform this operating pattern for the stated assignment and return verifiable evidence.
---

# Workstream: Example
```

The description must be exactly one plain-text sentence on one line, no more than 240 characters, ending in punctuation. Keep instructions in the workstream body; do not repeat its discovery description in the parent skill. Nested `workstreams/<guide>/` files are supporting documentation, not separately indexed workstreams.

The parent `SKILL.md` keeps its shared responsibilities, defaults, selection rules and composability guidance as handwritten text. Only the list of file-backed workstreams is generated between `<!-- workstreams:start -->` and `<!-- workstreams:end -->`. Edit the workstream file, not its parent list.

`python3 scripts/astrid_dev.py sync` regenerates the parent indexes; the existing documentation workflow refreshes them on `main` when its GitHub App is configured. Ordinary `python3 scripts/astrid_dev.py check` and PR CI **always** validate every workstream's one-line description, including new files. The CI write-back allowlist remains explicit: a new parent skill with workstreams must first be registered in `scripts/workstreams.py`'s `PARENT_SKILLS`.


Every discoverable skill retains its namespaced `name: astrid-dev-*` and matching leaf directory name. [`sync.sh`](../../sync.sh) installs **flat symlinks** to the canonical packages for Claude/Codex discovery; the extra grouping directory does not appear in installed skill names. Do not duplicate instructions or add folders for workstreams that need no variant. Follow the [run contract](run-contract.md).
