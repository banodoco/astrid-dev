# Astrid domain map

**The one index for locating Astrid work.** Start with the user's intended outcome, not the repository name. These links identify likely owners and existing references; verify current code, pins and source SHA before changes. Add an entry only when it helps a newcomer navigate an otherwise unclear boundary. Domain-specific instructions remain with the domain owner.

| Question / domain | Canonical owner and first places to inspect |
| --- | --- |
| Vision, missing outcomes, contribution priority | [Astrid Dev vision](../../../vision/README.md), [gaps](../../../vision/README.md), [project catalog](../../../plans/index.md). Status and ownership are *only* in the catalog |
| Project planning, task proof, run/review policy | [Project format](../../../docs/project-format.md), [planning skill](../../astrid-dev-plan/SKILL.md), [shared run contract](../../astrid-dev-shared/run-contract.md). PR evidence rules: [Astrid development skill](../../../skills/astrid-dev/SKILL.md) |
| Authoritative projects, timelines, media, jobs, permissions | [astrid-runtime](https://github.com/banodoco/astrid-runtime), its API contracts and project/task authority |
| Agent CLI, models, creative packs, installer, MCP | [astrid-agent](https://github.com/banodoco/astrid-agent); its current [execution map](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md) and [setup guide](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/SKILL.md) |
| Editor, user interface, timeline, export, editor extensions | [astrid-app](https://github.com/banodoco/astrid-app), especially [video editor docs](https://github.com/banodoco/astrid-app/tree/main/docs/video-editor) and [editor SDK](https://github.com/banodoco/astrid-app/tree/main/src/sdk) |
| Installation and launcher distribution | [astrid-pinokio](https://github.com/banodoco/astrid-pinokio); Agent installer, App's installed-version manifest and current product runbooks |
| Isolation, sandbox, user-consent boundary | [sandbox outcome F-007](../../../vision/gaps/F-007-first-class-sandbox.md), [Plan 15](../../../plans/15-openshell-safe-execution/plan.md), Agent's OpenShell setup. Do not infer sandbox security from the presence of scripts |
| Generation, model/provider execution | [creative execution gap F-003](../../../vision/gaps/F-003-creative-execution.md), [inference routes Plan 12](../../../plans/12-multiple-inference-routes/plan.md), Agent/Runtime product contracts |
| Rendering and finished-video options | [rendering-options Plan 27](../../../plans/27-video-render-options/plan.md), App render/export paths. Rendering on a cloud workspace belongs to [Plan 26](../../../plans/26-fully-hosted-v2/plan.md) |
| Cloud execution versus fully hosted projects | [Astrid Cloud generation, Plan 25](../../../plans/25-cloud-assist-v1/plan.md): account, credits, key and cloud generation with local project custody; [Astrid Cloud workspace, Plan 26](../../../plans/26-fully-hosted-v2/plan.md): one Runtime per user with the agent on a cloud machine |
| Shared knowledge and agent learning | [Hivemind protocol Plan 22](../../../plans/22-hivemind-protocol/plan.md), [agent learning Plan 23](../../../plans/23-agent-learning-integration/plan.md), [Hivemind](https://github.com/banodoco/hivemind) |
| Bugs, small fixes and user incidents | [Astrid Dev issues](https://github.com/banodoco/astrid-dev/issues) are the tracking unit, not projects. Use [Bug fixing](../../astrid-dev-bugfix/SKILL.md) for recovery and [Iterate](../../astrid-dev-iterate/SKILL.md) for focused repair |
| Integration, releases, public deployments | [Release skill](../../astrid-dev-release/SKILL.md) and product-owned [release references](../../astrid-dev-release/references/sources.md) |

## Cross-repository order

The usual dependency direction is **Runtime → Agent → App → Pinokio**, although Runtime tests may also pin Agent. The exact current lock files and installed tuple must be verified in the repositories. A green check in one repository does **not** qualify the combined installed system.

A domain map is **navigation, not permission or a copied runbook**. The active repository's own instructions, current source, named task and [run contract](../../astrid-dev-shared/run-contract.md) determine what an agent may actually change or ship.
