# Principle 3 — Collective Intelligence

**Claim:** **Every creative agent should get better from what it and the wider community learn.** Knowledge from people's experiences, agents' work, shared tools and public or private communities should continually become more useful, contextual and reusable—without requiring everyone to surrender control of their data.

This is not merely a search engine or a central repository. It is a **learning loop connecting personal/local intelligence with collectively maintained knowledge**. Hivemind is a proposed interoperable protocol for that loop; Banodoco Hivemind is one concrete dataset and proving ground.

The purpose is to expand [artistic ambition](../artistic-ambition/principle.md): shared understanding should help people solve creative challenges they otherwise could not tackle.

## How it should feel

An agent helping with a project routinely looks for useful prior understanding: what has worked with similar models, workflows, versions and hardware, including lessons from the user's own previous work. It tries an approach, observes the result and captures an accurate, scoped lesson—including failure or uncertainty. That lesson improves the user's local knowledge. With the user's approval and appropriate filtering/review, a generalizable finding can also contribute to a community dataset. Other agents can then benefit.

The goal is **continuous learning before, during and after creative work**, not requiring the user to search documentation manually or remember to write a guide after every success.

## Principles of the learning system

- **Local first, connected by choice.** A personal or team agent can maintain a private/local knowledge dataset. Public communities and specialized teams can maintain their own. Ownership, permission and provenance stay with each dataset; knowledge need not live in a single central database.
- **Agents both consume and contribute.** Before action, find and inspect applicable guidance. During/after work, capture what was attempted, conditions, outputs, failures and evidence. Promote helpful findings to durable local knowledge; offer useful community contributions rather than silently broadcasting private work.
- **Use knowledge in context.** Model versions, GPU, workflow dependencies, task type and evidence basis determine applicability. Retrieval should surface competing approaches, uncertainty and what has become outdated.
- **Distil rather than accumulate noise.** Transform raw conversations, run receipts, documents and artifacts into discoverable, reviewable knowledge. Attribute sources and distinguish reported, observed, inferred and editorially endorsed statements.
- **Federate and improve knowledge.** Independent datasets can cite, qualify, support or dispute one another, including through selectively shared, sanitized evidence. Revisions and review preserve corrections without erasing useful history.
- **Keep authority with people.** Learning from content never grants an agent permission to install software, run code, spend resources or publish sensitive data. Dataset owners decide access and endorsement; agents can draft and triage, but local policy and human authority govern consequential sharing and changes.

## One possible implementation: Hivemind

The [2026-10-29 Hivemind protocol proposal](references/hivemind-protocol-proposal.md) describes dataset-prefixed identities, immutable entries, typed and attributed links, scopes and access decisions, exposed through `find`, `inspect` and `contribute`. Datasets can reference one another without merging.

That is a useful technical proposal, **not the definition of this principle** and not yet a verified standard implemented across Astrid. A local Hivemind and Banodoco Hivemind would be *peers* under a common protocol, not a local instance subordinate to a centrally owned Banodoco database.

In combination with [Liquid Software](../liquid-software/principle.md), collective intelligence helps agents discover **what is useful and how it works**; liquid software helps people and agents assemble the **tools to act on it**.

## Read next

- [Bridge from current implementations to proof](bridge.md)
- [Agent learning loop](references/agent-learning-loop.md)
- [Original Hivemind protocol proposal](references/hivemind-protocol-proposal.md)
- [Verified source map](references/source-map.md)

This is one [Astrid vision principle](../../vision.md), not an implementation mandate or a claim of shipped agent-learning/federation functionality.
