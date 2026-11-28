# Inputs — Agent tests

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — On 28 Nov 2026 the owner asked, in the [planning session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), for agentic tests that plug into the skill and workstream documents, declared explicitly and connected to a brief, with a cheap actor and a subjective judge; for the person running them to synthesize rather than react; and for it to fit the existing meta workstream and the design principles.

**Prior art:**
- Two rounds of fresh-context dry runs, each finding real gaps ([17 Nov](../../docs/ledger/2026-11-17-fresh-context-dry-runs.md), [28 Nov](../../docs/ledger/2026-11-28-agent-path-dry-runs.md)).
- [improve](../../agent/shared/workstreams/improve.md)'s Audit: `N` helpers map an area, a high-judgment critic judges.
- `claude plugin eval` can run a skill with MCP tools mocked and grade the tools called; it needs a plugin manifest and suits Claude hosts only.

**Approach:** Cases live in `agent-tests/`, not beside the documents: a skill's text is what the actor reads, and many cases cover a path across documents. Each case declares what it covers; coverage is computed. Rejected alternatives:
- an `expected:` field in each document's frontmatter, which leaks the answers into the skill and only covers one document;
- a separate agent-test skill, a second way in beside improve;
- running models in CI on every PR, which costs real calls; the check stays structural.

**Challenge:** Not needed — it adds one folder, one script and one check, and replaces hand-written dry runs.

**Proof and limits:** The plan's Completion list. Limits: a cold read tests understanding, not capability; a tool that fails at first real use is caught by a toolkit check, not here.

**Review rounds:** One (AT-R), on the high-judgment role.

**Run start:** Whole project, owner-authorized on 28 November 2026 in the [planning session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG). **Accountable agent:** that session, with `N` Haiku helpers for inventories, drafts and actors.

## Owner decisions

None.

## Source identities

astrid-dev only: `main`, landed through the planning session's branch; no product repository changes.

## References

- [improve: agent tests](../../agent/shared/workstreams/improve.md#agent-tests)
- [agent-tests/README.md](../../agent-tests/README.md)
- [The pipeline](../../agent/shared/pipeline.md)
