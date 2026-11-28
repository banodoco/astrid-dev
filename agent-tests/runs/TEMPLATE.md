# Agent-test run — <YYYY-MM-DD> — <subject>

**Date:** <YYYY-MM-DD>
**Commit:** <the head the actors read>
**Run by:** <session or person>
**Trigger:** <a changed document, a lane about to launch, an audit>
**Cases:** <case ids, chains in order>

## Governing finding

One sentence: what this run shows about the documents.

## Round 1

| Case | Verdict | Misses | Cause |
| --- | --- | --- | --- |
| <case id> | pass or fail | E2, M1 | doc-gap, actor-error or ambiguity, per miss |

## Synthesis

The misses grouped by cause ([how](../../agent/shared/workstreams/improve.md#synthesize-dont-react)), most consequential first.

1. **<Parent idea, as one sentence a fresh session could apply.>** Kind: structural, precedence, missing parent, sequence or wording. Settles: <case and miss ids>. Fix: <the one home it changes>.

## Changes

- <commit or PR>: <the parent idea it writes, and what it removes>

## Round 2

Re-runs on the changed documents. A row that ran on a later commit names it, as `at <sha>` in its Cause cell.

| Case | Verdict | Misses | Cause |
| --- | --- | --- | --- |

## Owner questions

| Question | Answer |
| --- | --- |

## Next

What is left, and when the cases run again.
