# Inputs: multiple inference routes

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

The source plan contains no recorded source SHAs, branches, donor commits, or verified predecessor outputs. These identities must be established from current source before work starts; historical planning statements are not execution bases.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| Product repository or repositories (exact identity TBD) | TBD at start | TBD at start; inspect and preserve dirty work and identify reusable work/donors | TBD; verify the current generation and pack state | Fresh candidate branch to establish at start | Verify `pre-main` exists before use |

Record each actual repository separately, including ref, full SHA, dirty state, custody, and role. Identify the current generation interface, pack entry points, installation/setup and instance-connection paths, ownership/custody/lease primitives, and verified predecessor work. Establish supported hardware, model availability, and environment for actual inference proof. The planning repository is not the product source identity.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| Shared generation behavior | Intended shared user-facing generation contract and setup/execution/results behavior | [Project 02 plan](../02-consistent-generation/plan.md) and [tasks](../02-consistent-generation/tasks.md) | Verify current implementation, source identity, and predecessor status at start. |
| Pack conventions | Intended pack boundaries and composition | [Project 06 plan](../06-packs/plan.md) | Verify current implementation and source identity at start. |
| Wan2GP setup and connection | Evidence must distinguish a full install from connecting to an already-running instance | Exact code paths and supported environments TBD during scoping | No implementation paths, setup instructions, or real inference evidence are established in this draft. |
| User-provided premise | VibeComfy is primary; some reusable setup/connection infrastructure exists; Wan2GP is the additional route | Original project brief, represented in [plan.md](plan.md) | Planning premise only, not verified current-code claims. |

## Constraints

- Successful inference evidence must be real for VibeComfy and for Wan2GP via both full-install and existing-instance paths. Controlled failures may use fixtures.
- Attaching to an external server does not confer ownership of its process or GPU. Never stop or kill a user's server or unload models the route did not load or own. Explicitly selected external inference remains supported.
- Keep VibeComfy the primary route. Pack installation/default-inclusion policy is undecided; it is separate from Plan 11's Three.js default-inclusion requirement.
- Follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md) for source identity, route bindings, focused proof, review, and promotion. Follow repository authority rules: a plan does not authorize execution; verify the candidate and `pre-main` destination before any publication.
