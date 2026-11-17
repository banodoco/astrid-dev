# Role skills and workstreams

Each Astrid role lives in its existing `skills/astrid-dev-<role>/` folder:

- **`SKILL.md`** defines responsibilities and routes to any optional workstream.
- **`workstreams/<name>.md`** gives only the extra steps for a particular setup, such as fresh ChatGPT packet sessions. It links back to the role; it does not create another role, project, task list or permission system.
- **Environment guides** retain the concrete commands and tools at their existing paths; workstreams link to them rather than copy them.

Start from [astrid-dev](../astrid-dev/SKILL.md), choose the role, then the relevant workstream. Roles without distinct operating variants need no `workstreams/` folder. Follow the shared [run contract](run-contract.md) and existing release and project records throughout. Do not reorganize the established skill paths into another `roles/` hierarchy.
