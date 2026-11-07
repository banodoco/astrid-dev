---
name: astrid-dev
description: One entrypoint for people and agents contributing to Astrid: find the right existing work, define a bounded change, prove it, and land it safely.
---

# Contribute to Astrid

**Start here for any change to Astrid**—a small fix, a new idea, an existing project, documentation, or a release. For artwork made *with* Astrid, use the separate creative skill.

An agent should be able to join without prior Astrid knowledge. Start with the contributor's goal, find the existing work, and do not demand that they understand the entire system before making a useful contribution.

## One path, six stages

Work enters at the earliest stage that is **not already settled by accepted evidence**. Do not repeat completed planning or make a small change go through an architectural review. Stop at the stage the contributor actually requested.

| Stage | Question and useful result | Go deeper when |
| --- | --- | --- |
| **1. Orient** | What does the person want, what can they contribute, and [which domain owns it](references/domains.md)? Point to a good first task if they have no idea. | Ownership, safety or an installed version is unclear |
| **2. Investigate** | What already exists? Check [the plan catalog](../../plans/index.md), relevant issues, product source, previous decisions and actual behavior. Cite the reusable implementation, its version and the gap it addresses. | Changes span repositories, contracts, or unexplained behavior |
| **3. Decide** | What is the *smallest complete outcome*, why here, and what would prove it? Reuse an accepted plan or follow [Plan](../astrid-dev-plan/SKILL.md) for genuinely new scope. Don't mistake a project for a new [vision gap](../../visions/gaps.md). | The choice is consequential, hard to reverse or has meaningful competing designs |
| **4. Build** | On the authorized source, make the bounded change and keep existing work intact. Use [Iterate](../astrid-dev-iterate/SKILL.md); reported user failures begin with [Bug fixing](../astrid-dev-bugfix/SKILL.md). | Source, permissions or dependencies differ from the accepted task |
| **5. Prove** | Show the claimed behavior on a named candidate and environment, including meaningful failures. Preserve commands, actual results, limitations and unresolved claims using the [run contract](../astrid-dev-shared/run-contract.md). | The evidence does not actually demonstrate the claim |
| **6. Land** | Link the result to the original issue or plan. Use the existing PR, evidence and review gates; [Release](../astrid-dev-release/SKILL.md) owns cross-repo integration and authorized promotion. | Pins change, a release is requested or the reviewed source moves |

**Each stage has one decision, not a new form.** A fact-finding report may end at Investigate. A new draft may end at Decide. An approved task can begin at Build. Don't invent another round of owner approval because an agent changed.

## Your first contribution

Ask whether the person already has a concrete idea. If yes, trace it to an existing task or issue before proposing something new. If not, use the [catalog](../../plans/index.md) to suggest 2–3 bounded contributions, including a small satisfying one, based on their interests, available time, hardware and agent capabilities. Look for current ownership and dependencies to avoid competing implementations. Ask only for missing information that changes the decision.

Don't install skills, run code, spend money, access private data or alter another person's machine merely to orient someone. If skill installation is useful, explain the changes first; use the repository's existing sync mechanism only with their consent.

## One source of truth per concern

- **Domain ownership and where to read:** [domain map](references/domains.md). Don't copy the map into individual workflow skills.
- **Project priority, owner, status and estimate:** [one catalog](../../plans/index.md). A project pack has [`plan.md`, `inputs.md` and `tasks.md`](../../docs/project-format.md); drafts can be short.
- **Vision and missing outcomes:** [vision](../../visions/vision.md), [gap contract](../../visions/gaps.md) and existing gap records. A new project usually addresses an existing gap.
- **Run identity, model routing, permissions, proof and reviews:** [shared run contract](../astrid-dev-shared/run-contract.md). Repository-specific instructions still apply.
- **Mechanical PR requirements:** [repository rules](../../AGENTS.md) and the existing [documentation workflow](../../.github/workflows/docs.yml). CI checks structure, not the truth of an argument.
- **Specialized instructions:** [Plan](../astrid-dev-plan/SKILL.md), [Bug fixing](../astrid-dev-bugfix/SKILL.md), [Iterate](../astrid-dev-iterate/SKILL.md), and [Release](../astrid-dev-release/SKILL.md) only for the stage you need.

**Never conflate the three boundaries:** recording a project is not acceptance of its scope; accepting scope is not authorization to execute; passing tests or merging code is not authorization to deploy. Keep previously accepted decisions and safety/review constraints.
