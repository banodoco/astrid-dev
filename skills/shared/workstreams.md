# Skill structure

- [Astrid-dev](../astrid-dev/SKILL.md) is the entrypoint and routes requests.
- `skills/roles/astrid-dev-*/SKILL.md` defines **who is responsible** (Lead, Orchestrator, Manager, Worker).
- `skills/shared/workstreams/astrid-dev-*/SKILL.md` defines reusable, independently discoverable **shared workstreams**, such as Plan, Iterate, Release, Merge and Gap. They have a defined result and inherit the invoking role's authority.
- `skills/shared/` owns shared rules, terms, templates and reusable workstreams; the shared workstreams have no second authoritative copy.
- A role's optional `workstreams/` holds **role-specific operating patterns**, such as fresh-packet dispatch, as Markdown documents; they inherit the role and are not separately installed skills.

## One workstream contract

**Every workstream is a procedure with a defined outcome**, whether packaged as a standalone skill or a role-specific Markdown document. Both use the same authored, machine-checked `## Workstream contract` as the **first level-two section** after the title:

```markdown
## Workstream contract

**Outcome:** An independently verifiable result that this workstream produces.
**When to use:** The trigger or context in which an authorized agent selects it.
**Inputs:** The assignment, source and permission facts needed before acting.
**Procedure:** A concise route through the actual execution instructions below.
**Completion:** What evidence or disposition proves the workstream is finished.
```

These five labels must occur once, in that order, with substantive single-line values, and there must be actual execution instructions beyond the summary. A second contract field after a blank line is also a duplicate. The parser validates structure; it cannot decide whether the instructions are correct, the evidence sufficient, or the actor authorized. Keep detailed instructions under their existing headings after the contract summary. Do not replace real steps or proof with placeholder summaries, and do not duplicate shared run policy.

Standalone skills add `name: astrid-dev-<name>` to frontmatter, use a matching directory and may give their H1 a natural title. Role-specific documents use only `description:` in frontmatter and start with `# Workstream: <title>`. Both have a one-line description of at most 240 characters, ending in punctuation. Supporting guides inside nested workstream directories are not workstreams and do not need this contract.

A shared workstream skill inherits the invoking role's and run's authority; a role-specific document inherits its parent's. **Neither can authorize its own execution, merges, spending or publication.** See [the run contract](run-contract.md).

Implementation: [the shared Markdown structure helpers](../../scripts/document_structure.py) parse frontmatter and ordered fields, [the workstream parser](../../scripts/workstreams.py) produces one `Workstream` representation, and the existing check registry enforces it as `workstream-structure`. The reusable heading-order helper is also used by [project pack shape checks](../../scripts/pack_shape.py). The names-only shared-workstream index and role-specific descriptions are projections of these canonical files.

## Independent workstream skills

A shared workstream that an agent can invoke directly lives under `skills/shared/workstreams/astrid-dev-<name>/SKILL.md`. Its folder name must exactly match its frontmatter `name: astrid-dev-<name>`; its `description:` is a nonempty single line. `sync.sh` installs it as a flat, independently discoverable skill without changing its name. A role may invoke it but cannot gain permissions merely by selecting it. There is no independently installed `capabilities/` category or standalone Planner role. Legacy relative symlinks preserve old Markdown links without maintaining duplicate skills; `sync.sh` ignores them.

A role-specific workstream stays beneath its parent role as a `.md` file when it is only meaningful inside that role. Each role skill also contains a generated **Shared workstreams** section listing the available independent skills by name and link only, derived from their skill folders; it does not duplicate descriptions or grant permissions.

## Workstream discovery

Every direct role-specific `workstreams/*.md` file (excluding an optional `README.md`) has its own title and description as defined above. Keep full instructions in its body; do not repeat its discovery description in the parent skill. Nested `workstreams/<guide>/` files are supporting documentation, not separately indexed workstreams.

The parent `SKILL.md` keeps its shared responsibilities, defaults, selection rules and composability guidance as handwritten text. Only the list of file-backed workstreams is generated between `<!-- workstreams:start -->` and `<!-- workstreams:end -->`. Edit the workstream file, not its parent list.

`python3 scripts/astrid_dev.py sync` regenerates the parent indexes; the existing documentation workflow refreshes them on `main` when its GitHub App is configured. Ordinary `python3 scripts/astrid_dev.py check` and PR CI **always** validate the full common contract and package metadata of every workstream, including new files. The generated shared-workstream lists are validated against the standalone skills and registered as explicit role targets. The CI write-back allowlist remains explicit: a new parent skill with workstreams must first be registered in `scripts/workstreams.py`'s `PARENT_SKILLS`.


Every independently discoverable role or shared workstream skill retains its namespaced `name: astrid-dev-*` and matching leaf directory name. [`sync.sh`](../../sync.sh) installs **flat symlinks** to the canonical packages for Claude/Codex discovery; the extra grouping directory does not appear in installed skill names. Do not duplicate instructions or add folders for workstreams that need no variant. Follow the [run contract](run-contract.md).
