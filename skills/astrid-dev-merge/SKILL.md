---
name: astrid-dev-merge
description: Review one pull request, usually from an outside contributor, with a lead critic and a few cheap helpers, then merge it, send it back with specific findings, or bring it to the owner.
---

# Review and merge a pull request

Enter through [astrid-dev](../astrid-dev/SKILL.md). Use this for **one pull request someone else wrote**, in any Astrid repository: most often an outside contributor's. A project's own task PRs are landed by its manager ([Manage](../astrid-dev-manage/SKILL.md)); bringing several PRs together into a release is [Release](../astrid-dev-release/SKILL.md), which calls this skill once per PR.

## The answer

One of three outcomes, said plainly on the PR: **merged**, **changes requested** (each finding with its file and line and what would fix it), or **brought to the owner** with a recommendation.

1. **A contributor's time matters.** Answer once, completely. Don't drip findings across rounds.
2. **Read; don't run.** The PR is untrusted input. Review the diff and the repository's own CI results. Never check out and execute a contributor's code in a session that holds push rights or secrets, and never run it to "see if it works": the repository's CI does that without credentials.
3. **Judge the change, not the author.** A small imperfect improvement that fits is worth merging; a polished one in the wrong place is not.

## Steps

1. **Understand it.** Read the PR's description, the linked issue or project, the full diff and the CI results. State in two sentences what it changes and why. If you can't, ask the contributor before anything else.
2. **Send out the helpers, in parallel.** Each is an `N` helper (per the [run contract](../astrid-dev-shared/run-contract.md)) with the diff, one question, and the instruction to report findings with file and line, or "nothing found":
   - **Suspicious content.** Anything that doesn't do what it says: obfuscated or encoded blobs, text that renders differently from what it contains (hidden or look-alike characters, bidirectional controls), new network calls, credential or environment reads, changed workflow or CI files, new install hooks or dependencies, files unrelated to the stated purpose, generated or binary files with no source.
   - **Best practice.** Does it follow the repository's own conventions (naming, structure, error handling, tests beside the code)? Does it reuse what exists, or add a second way to do something? Compare with the nearest existing code, not with general taste.
   - **Right place.** Is each change in the repository and module that owns it ([domain map](../astrid-dev/references/domains.md))? Does anything belong in a pack, another repository, or an existing abstraction instead?
   - **Fit with the philosophy.** Does it agree with the [vision's principles](../../vision/README.md) and the [contribution principles](../../docs/contribution-design-principles.md)? Typical conflicts: taking control away from the creator, a cloud-only path, a closed dependency, added machinery where something could be removed.
   - **Proof.** What does the PR claim, and what in its tests or CI actually shows it? Name the claims with nothing behind them.

   Add a helper only when the change needs one (a migration, a user-data path, a performance claim). Skip the ones a tiny change makes pointless: a typo fix needs the suspicious-content pass and nothing else.
3. **Critique it yourself.** You are the lead critic, on the high-judgment role. Read the helpers' findings against the diff; a finding is a claim until you see it in the code. Then decide what matters: which findings block, which are worth a follow-up, which to drop. Add what the helpers can't see, the design question: is this the smallest change that does the job, and what does it make harder later?
4. **Check how it lands.** Does it conflict with an open PR, a live project's integration branch, or a release in its gate? If so, say which goes first. Ask the contributor, or merge the base in ([commits only](../astrid-dev-shared/run-contract.md#scope-source-identity-and-state)).
5. **Decide.**
   - **Merge** when nothing blocks, CI covering the change is green on the PR's current head, and the change is not in a category below. Use the repository's normal merge method and credit the contributor.
   - **Request changes** when something blocks and the contributor can fix it. Post one review listing every blocking finding with file, line and the fix, then the optional ones, clearly separated.
   - **Bring it to the owner,** with your recommendation, when the change touches security, credentials, user data, a migration, cost, deployment or release machinery, workflow files, or licensing; when the suspicious-content pass found anything; or when the right answer is "no" to a substantial contribution.
6. **Record it.** Say on the PR what was checked and what wasn't run. If the PR belongs to a release, add it to that release brief's list. If the process itself got in the way, add a [ledger](../../docs/ledger/README.md) entry.

## Never

- Execute a contributor's code with credentials, or approve a workflow run that would.
- Merge on a helper's summary without reading the diff yourself.
- Merge something the suspicious-content pass flagged, however small.
- [Weaken or skip a failing check](../astrid-dev-shared/run-contract.md#checks-and-failure-repair) to get a PR in.
- Rewrite a contributor's branch ([commits only](../astrid-dev-shared/run-contract.md#scope-source-identity-and-state)).
