# Evidence summary and source limits

This repository contains planning documents and small audit summaries. It does not contain product repositories, complete test logs, secret-bearing environment details, or runtime workspaces under the original author's home directory. Full runtime evidence remains local-only; no claim below should be read as a fresh run against future candidate heads.

## Installer consent

The 4 Nov 2026 source audit records accepted Agent donors `6087e0f...` and `19229d2...`, App donors `e97450c...` and `9ddff8e...`, and an independent IC END review with `BLOCKING: 0`. The review also records one deferred known issue: non-JSON skills-off rendering/removal output and policy persistence. The four donor heads are accepted inputs, not a composed Agent/App release. The audit's exact observed bases and include/defer ledger are in [donor-manifest.json](donor-manifest.json); merge findings and focused acceptance requirements are in [PLAN.md](PLAN.md).

The review receipt was read from the source runtime during plan preparation. It says `BLOCKING: 0`, lists the deferred skills-off limitation, and records all six acceptance items as met across donor verdicts and review patches. The full review and donor verdict artifacts are not copied here.

## Concurrent editing

The source evidence summarized by the audit reports App repair head `438159b030cd3b0b81653415f1018f9a1349f0c5` passing the original eight hosted cases plus migration/owner and scope checks, with zero blocking items. Agent SDK evidence is not a substitute for final independent Agent/App/Runtime tuple acceptance. Therefore CE remains deferred until that tuple is checked.

## Packs

The inspected PK-2 receipt reports head `04e74695a6cded0139ba31b20ce59a81ee91d564`, with zero blocking items; PK-3 and namespace/schema preparation results are reported as verified in the source disposition manifest. These receipts do not mean later Packs phases are complete. PK-4 has a retained first-failure/blocked result and requires its demonstrated core/pack boundary repair before retry. The detailed run artifacts stay local-only.

## Generation

The source audit reports PINS verification was cancelled with exit 143 before a final verdict, which is neither a pass nor a product failure. DEFAULTS is an unpublished incomplete checkpoint, and the previous installed acceptance contract incorrectly paired no model bytes with successful real managed readiness. The revised plan uses a model-free installed/package boundary proof and keeps actual model readiness/execution explicitly unproven. Details are in [INCLUDING-GENERATION.md](INCLUDING-GENERATION.md).

## Portability

All SHAs and status claims above are dated historical evidence. Candidate acceptance must be established on exact future immutable heads using the scoped checks in the plan. Private/local-only evidence paths have intentionally been replaced by these summaries; the original complete logs and card corpus are not bundled.
