difficulty: astra (read-only design)

# Design: declare a machine's settings once, then generate on that machine

You are a read-only designer. Do not edit any file.
- Code: Agent `/home/user/wt/c-b6` (Release 13 candidate `r13/batch6`).
- Plans: `/home/user/wt/dev-plan49/plans/40-machine-lifetime-controls/{plan.md,inputs.md,tasks.md}` (owner decisions D1–D13 on paid consent, caps and retention) and `/home/user/wt/dev-plan49/plans/32-generation-placement-targets/`.

**Owner (Hannah, 12 Nov, paraphrased closely):**
- "We shouldn't have to declare things over and over again."
- For each machine, set once what we want for it. Then say "I want to generate on that machine". Change machine settings with the commands we already have.
- She asked whether generating on a machine queues tasks for that machine, so 20 items run back to back.

## Today
`astrid machines setup` saves preferences: volume, ordered GPU list, `--budget-usd`, a ceiling per paid run. But every `astrid generate … --placement runpod` still needs:
- `--max-hourly-usd`;
- `--max-usd`, which must fit the saved budget;
- `--preparation-seconds`, `--execution-seconds` and `--idle-seconds`, with no defaults;
- `--consent paid`;
- optionally `--gpu`, which overrides the saved list.

`astrid machines` is the provider-neutral family, but RunPod is its only kind.

Read `astrid/packs/runpod/docs/SKILL.md`, `astrid/core/generation/cli.py`, `astrid/sdk/generation.py`, `astrid/packs/runpod/adapter.py` (`prevalidate_task`, `quote`), `astrid/packs/runpod/target_selection.py` (`PaidRunConsent`, `consented_offer`), `astrid/core/machines_cli.py` and the preferences code. Find the validators that require each flag.

## Answer, with file:line evidence
1. **Where each value lives today.** Which flags are required and why: cite the validator, and the Plan 40 decision that requires it, if any.
2. **The smallest design that declares everything once.**
   - A machine (or machine profile) carries: GPU list, storage, hourly ceiling, per-run cap, and default preparation, execution and idle allowances. It is set and changed with the existing `machines setup` (and `keep`), and shown by `machines setup --show` and `generate describe`.
   - `generate --placement runpod --consent paid` (or `--machine <id|profile>`) uses it, and any flag overrides it for one run.
   - **Keep paid consent honest:** consent must still disclose the actual values and be fresh per paid run (Plan 40). Show how a single `--consent paid` against the disclosed saved values satisfies that, or say which owner decision would have to change.
3. **Queueing.** Today, do N generations for a held machine run back to back on the same pod? Cite the Runtime claim and executor concurrency, the GPU resource key and warm reuse. What would "generate on that machine" (an explicit machine id) need, and what happens when that machine is gone or incompatible?
4. **Naming.** `machines setup` with RunPod-only flags: what is the smallest honest naming (for example `--provider runpod`), and does anything else in the CLI or SDK depend on the current names?
5. **A task list.** Each task with scope (`path:symbol`), route and focused proof, plus the owner decisions with options and a recommendation. Say what can land in Release 13 versus later.

Keep it under about 900 words, and cite code. Don't invent problems.
