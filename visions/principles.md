# Principles — how we build Astrid

The [four pillars](vision.md) describe **what we're trying to enable**. These principles describe **how we insist on pursuing it**. They apply across the tools, agents, community and supporting infrastructure.

## Local-first, cloud-capable

People should be able to work on their own machines, including offline for supported workflows with available models. **Local-first is not local-only**: when the work exceeds local hardware or people prefer hosted services, cloud computation and hosted workspaces should be optional choices. Keep where the interface runs, where project data lives, and where tasks execute distinct; don't silently move work or incur costs. This is a target, not a claim that every deployment combination ships today.

## Open by design

The tools, extension mechanisms and the thinking behind them should be inspectable, modifiable, forkable and shareable. Build on open-source software and the open-model ecosystem; enable others to contribute tools and knowledge without tying the shared foundation to one proprietary provider. Optional hosted services may extend choice, but not become an unavoidable gate.

## In the creator's control

Creative decisions, project data, agent permissions, installed tools, execution location and spending remain under the person's authority. Agents should make consequential proposals legible and reversible where possible. Private knowledge stays private unless its owner chooses to share it. This principle requires concrete safety and reliability evidence, not just good intentions.

## Eliminate needless technical wrangling

Creative work should not require people to become environment managers, model installers or execution troubleshooters. **Agents should handle the technical work**: choosing a suitable model with the creator's consent, setting up and maintaining environments, preparing dependencies, running jobs and recovering from errors. Expose understandable choices, costs and failure states without making technical configuration the main creative interface. The goal is for people to spend their attention on creating—not on infrastructure. This is an aspiration requiring demonstrated reliability, not a claim that setup is already effortless.

## Evidence and delivery

A [gap](gaps.md) may apply to any number of [pillars](vision.md) and principles, and one gap may concern several. No principle automatically creates a new gap: first check whether an existing outcome already captures the missing behavior. [Plans](../plans/) link to those specific gaps and deliver evidence.

**Sources:** [public Astrid vision](https://astrid.haus/vision), [current page source](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/pages/Home/PublicAstridVision.tsx), and [Runtime architecture direction](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/creative-workspace-runtime-vision.md). Public-page status statements are historical snapshots until independently revalidated.
