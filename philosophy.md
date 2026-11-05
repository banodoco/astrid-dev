# A foundation for creative tools

Astrid exists to help people and their agents build, use, and share their own creative tools. We want a dependable foundation of simple, composable primitives that makes creating easier and gives people room to take it in directions we have not imagined.

This is what we are building toward.

## A small foundation that works

The core should make the common work reliable: connecting tools, working with media, generating, editing, and running things. Good defaults should let someone make something useful quickly. Clear contracts should let them understand and change what happens underneath.

Keep the foundation small. Put specialized creative behavior in packs, and improve shared primitives when several tools need the same capability. Prefer one understandable way to do a job over overlapping frameworks.

## People choose how much control they want

Someone should be able to use a ready-made tool, change one part, or build their own. They should be able to run the whole tool on their machine, use remote compute where they choose, select an inference backend or agent, and decide what files, accounts, and services it may access.

Convenience should not require giving up control. Make choices and consequences visible; preserve the user's work and intent when agents act on their behalf.

## Extension is part of the design

Provide deliberate, documented ways to extend the parts people create with: inference, execution, agent editing, effects, interfaces, and the tools inside those interfaces. Extension should be an ordinary supported path, not a workaround that requires a fork or knowledge of private internals.

A pack can also be a foundation. Its users should be able to compose its capabilities, adapt its behavior, and build another pack on top. This is a community of building blocks: people can share both finished tools and the pieces that help others make new ones.

Keep extension points concrete and useful. Start with real creative needs, prove them with working examples, and avoid adding abstractions for every hypothetical future use.

## Two examples

**[VibeComfy extensibility with H3_AV](plans/17-vibecomfy-extensibility.md).** H3_AV provides a higher-level abstraction over VibeComfy workflows. Use it to find the reusable primitives VibeComfy should expose so people can build, customize, and share similar abstractions more easily. The result should make the next person's tool easier to build, as well as making H3_AV work well.

**[Extensible timeline editing](plans/18-timeline-editing.md).** Provide dependable timeline editing primitives as a pack, then let people and agents build different ways to understand and work with the same video. A custom view, analysis tool, editing workflow, or effect should build on those primitives and remain composable with other tools. The timeline is a foundation for creative exploration, not one fixed interface.

## Make the system understandable

Explain the big idea first, then reveal detail as it becomes useful. Our documentation should form a simple pyramid:

1. Purpose and mental model: what Astrid is for and how its pieces fit.
2. A central Astrid skill that routes people and agents to the right workflow.
3. Focused guides for doing the work, building packs, and designing useful extensions.
4. Precise contracts, examples, and reference details next to the code that owns them.

Give each fact one canonical home and link to it. Use clear names and small interfaces so code and packs explain much of their own operation; use prose for intent, tradeoffs, and contracts that code alone cannot explain. The [first-principles documentation project](plans/19-first-principles-documentation.md) applies this across the repositories.

A good contribution makes something useful possible, makes it easier to build on, or makes the foundation simpler to understand and trust.
