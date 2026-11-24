# Astrid Marketing organisation

**Project:** Astrid Marketing organisation

**Goal:** Astrid has a small, independently operable agent-assisted marketing workspace that turns evidence about audiences and product capabilities into coherent campaigns and content, then learns from measured results without requiring changes to the shared framework.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD — scope the operational pilot and human/agent effort after the Plan 95 handoff and an owner-approved marketing objective, channel and measurement baseline; exclude waiting for audience results from engineering effort and report it separately.

**Waiting on:** [Plan 95](../95-composable-agentic-workspaces/plan.md)'s accepted framework and minimal Marketing consumer; independent scope critique, owner decisions on objective, audience, channel, visibility, authority and budget; named accountable manager. Read-only strategy discovery can be separately authorized before the handoff; implementation and operational work wait.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six fields above define the catalog row; leave [priority](../priority.md) and release membership unchanged until the owner decides.

**Vision role:** Foundational enabler — establishes a separate operating workspace for Astrid's communication, learning and growth, with traceable product claims; it does not itself deliver a creator-facing product capability or close an existing vision gap.

## Outcome and scope

Build out the actual Astrid Marketing organisation using the shared workspace system delivered by Plan 95. It is not a second software release pipeline. The initial operating model must be small enough that one agent can do a useful ordinary task without opening a full project pack or requiring a Leader/Orchestrator/Manager/Worker hierarchy.

**Initial candidate pipeline:** positioning and audience evidence → objectives and opportunities → campaigns or experiments → content and distribution → results and durable learnings. This is a connected record graph, not a mandatory linear sequence or automatic execution workflow. A small piece of content may directly serve an objective; a content item can support multiple campaigns and be published on multiple channels. Define only the record kinds a real initial campaign needs. Add others when their use justifies them, with local registration and checks.

**Included:**

- Confirm actual Astrid positioning, product capabilities, audiences, channels and constraints from the owner and source-backed research. Record brand voice, messaging principles, claims we can support and what must not be promised. Link product facts and release readiness to exact Dev sources instead of maintaining conflicting copies. Treat competitive/community feedback as evidence, not instructions or a guarantee of impact.
- Agree one or two concrete marketing objectives and a bounded first campaign/experiment, with baseline, target audience, hypothesis, success/failure/uncertainty criteria and measurement window. Owner selects channel, time, assets, privacy, budget and actual permissions. Do not invent current traction or metrics.
- Define minimal workspace-owned Markdown record types, relationship constraints, lifecycle, authoring templates, local checks and useful generated views (e.g. campaigns, content calendar or experiment/results summary). Use Plan 95's existing machinery, not local copies. Keep small activities lightweight, medium briefs/tasks where needed and full plans only for meaningful complexity. Recurring work can use a skill and periodic findings without building a scheduler.
- Define roles and Markdown-first skills with a clear entrypoint: research, positioning/strategy, campaign or experiment design, content creation, critique, authorized distribution, measurement and learning. Combine skills/roles where a single procedure suffices; add an independent creative or factual review where consequential. Reuse common operating rules, not Dev-specific branch/release cadence. Creative taste is a legitimate work outcome; proof fits the claim.
- Establish publication/contact/spend/privacy boundaries and approval checks. Drafting, internal research and analysis may be delegated within a scoped run. Official account actions, outreach, spend and commitments require separately documented explicit or standing scoped authority, an approved exact artifact/channel and budget as applicable. A GitHub merge, status change, skill selection or framework installation cannot confer permission. Default to no write credentials; verify idempotence and stop/recovery before enabling any integration. Avoid storing contact lists, private messages, raw high-frequency analytics or secrets in Git.
- Execute one real owner-selected bounded campaign or content experiment with an approved item, appropriate independent review and verified product claims. If external publication is authorized, record its actual channel, artifact revision, timestamp/receipt, baseline and observed results over the agreed window; otherwise record an explicit held draft/dry-run and leave the live outcome gate open. Distinguish output, observed response and attributable impact. A negative or inconclusive experiment can complete successfully as work.
- Feed durable conclusions and user feedback into the workspace's positioning, subsequent work and, where useful, the Dev issue/gap process with source links and permission. No automatic gap closure, engineering commitment or false causal attribution. Produce a second proposal improved by the first learning, not a growing parallel tracker.

**Not included:** rebuilding or forking the shared framework, migrating Astrid Dev, inventing a new marketing automation/analytics platform, automatic outreach/spend/posting, acquiring user personal data, mandatory full project packs for every content item, speculative pipeline types, broad cross-repo synchronization, or guaranteeing growth/virality. A channel connector is only in scope after the owner approves a specific need, security and access; manual approved publishing/measurement can satisfy the operational pilot. If no authorization or measurable results are available, the relevant live proof stays incomplete.

## Existing work and decision

The requester asked for Astrid Marketing as the second organisation on 24 November 2026, with a different pipeline and skills using the same foundations. [Plan 95](../95-composable-agentic-workspaces/plan.md) owns the generic mechanisms, Dev migration and minimal second-consumer proof. This plan owns actual marketing methodology, content and learning, not framework correctness.

The existing [Astrid vision](../../vision/README.md) and [strategy](../../strategy.md) describe product ambition and release direction; [Plan 53](../53-vision-aspirations/plan.md) owns goal authoring; [Plan 71](../71-gap-definition-reconciliation/plan.md) provides evidence-based reassessment; [Plan 52](../52-issue-intake/plan.md) owns product feedback intake. Reuse these as source references and useful methodology, not mandatory Marketing stages. No existing banodoco/astrid-marketing repository was accessible in the planning lookup; verify actual visibility and workspace handoff before work. See [inputs](inputs.md#planning-evidence) for alternatives, constraints and open owner choices. Independent critique and specific operating approval remain pending.

## Sequence and readiness

1. Verify the exact Plan 95 handoff and marketing starting state; source product facts, identify audiences and define the initial objective/hypothesis and baseline with the owner. Re-estimate after the pilot is scoped. Read-only discovery can be authorized separately.
2. Design the smallest operating graph, roles, skills and approval boundaries around the actual pilot; use Plan 95's extension guide. RS1 protects publication authority and measurement design before live work.
3. Configure local records, skill docs, check/view registrations and review process. Qualify them using a dry-run, including refusals and a lightweight content task. Establish the approved account/channel/budget boundaries or keep them absent.
4. Research, create and independently critique a real campaign/content item; owner or explicitly authorized actor publishes/distributes only the exact approved artifact. Measure at the agreed window, keep negative/inconclusive findings, and propose the next improvement. Final review assesses actual evidence, not headline metrics alone.

See [tasks](tasks.md). The framework pilot from Plan 95 may be reused if it genuinely matches this objective and has the necessary evidence; do not require duplicate content merely for process. No external account access, publishing, spend, implementation or release assignment is authorized by this planning document.

## Interfaces and handoff

**Consumes:** Plan 95's exact accepted framework revision, minimal Marketing workspace and extension guide; owner-approved brand/product sources; verified Dev release/capability references at named revisions; authorized, privacy-appropriate channel and metric sources. Record exact repository and artifact identities, what was observed and collection time. Use fixtures or read-only exports where private access is unavailable.

**Produces:** the configured Astrid Marketing workspace, canonical positioning/audience/objective documents and local relationship/record contracts; minimal role/skill definitions, review and permission policy; generated operational views; one reviewed campaign/content experiment, actual authorized distribution receipt and measured or explicitly inconclusive result; durable learnings and a justified next proposal. Provide exact revision links for approved artifacts and evidence and note remaining access/attribution limits.

Any missing capability in the shared framework is a separately proposed change to that framework, not an instruction to fork or weaken it. Product development findings are handed back through the existing Dev intake, not direct changes to release membership. Keep operational private data outside the public astrid-dev plan pack.

## Completion

1. An unfamiliar agent can navigate the Marketing workspace, understand what Astrid is and is not able to do, find audience/positioning evidence, select useful work, and execute a small draft task without Dev-specific release ceremony or new framework code.
2. Local records, relationships, states, checks, views and discoverable skills validate against the pinned framework. A small content task remains small, while a campaign can coordinate multiple activities; a negative experiment can close as execution with its outcome explicitly negative or inconclusive. No duplicated shared infrastructure or authoritative product facts.
3. One owner-selected real pilot has a stated objective, baseline, hypothesis, audience, review, approved content and traceable product claims. Authorized distribution is evidenced by an actual receipt and the agreed measurement window is evaluated with denominators, source/time bounds, missing data and limits. If distribution is not authorized or the window has not passed, mark that part incomplete rather than claim the pilot was delivered.
4. Negative controls show unsupported product claims, invalid relationships, missing approvals, wrong account/channel, changed artifact, duplicate action and spend outside authority are refused or explicitly blocked before external effects. A merged document or approved status alone never authorizes sending or publishing; no private data leaks into public Dev.
5. The result yields at least one durable source-linked learning and a revised next campaign proposal, with feedback to Dev where useful and authorized. Independent review checks what the evidence actually supports and what remains unknown. Exact revisions, raw or appropriately redacted receipts, check results and limitations are recorded.

Completion proves the organisation can execute and learn from a bounded real marketing cycle. It does not promise a particular growth rate, general causal attribution, automatic operation, unlimited spend, future publishing authority or closure of a product vision gap.
