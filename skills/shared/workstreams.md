# Skill structure

- [Astrid-dev](../astrid-dev/SKILL.md) is the entrypoint and routes requests.
- `skills/roles/astrid-dev-*/SKILL.md` defines **who is responsible** (Lead, Orchestrator, Manager, Planner, Worker).
- `skills/capabilities/astrid-dev-*/SKILL.md` defines **what specialist work to do**, reusable across roles.
- `skills/shared/` owns shared rules, terms and templates.
- A skill's optional `workstreams/` adds **how it operates in a particular setup**, with supporting scripts beside that workstream, not another skill.

Every discoverable skill retains its namespaced `name: astrid-dev-*` and matching leaf directory name. [`sync.sh`](../../sync.sh) installs **flat symlinks** to the canonical packages for Claude/Codex discovery; the extra grouping directory does not appear in installed skill names. Do not duplicate instructions or add folders for workstreams that need no variant. Follow the [run contract](run-contract.md).
