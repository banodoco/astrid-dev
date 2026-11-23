# Plan 71 — disposable native C1/C2 verification packet (NO CANONICAL WRITE)

**Prepared 23 November 2026. Unexecuted native/full-repository instructions for an authorized independent operator.** The adjacent [read-only source replay script](gd9_source_replay.py) was authored in this isolated evidence branch and tested locally using `python3 -m py_compile` and `--self-test` (three positive and four deliberately invalid parser declarations); its committed Git blob is `90766c31a69c7e357b3ead2f828571663126494f`, matching the locally compiled bytes. **Do not infer a full native repository PASS** from those local checks. The source preflight reads Git objects only; neither it nor this packet uses or reopens the original HOLD/RS2 material.

## Safe checkout, exact-head preflight and original checks

Run on an **independent disposable checkout** with permission to fetch this repository and with enough local tools. Do not use a source owner's active worktree, a release checkout, a working branch or another manager's GPU environment. Record the exact #1625 head SHA as read directly from GitHub immediately before execution; do **not** substitute an earlier checked SHA or silently accept a moving HEAD.

```bash
set -euo pipefail
# Operator-owned, disposable path. Never run in a shared branch/worktree.
WORKDIR="$(mktemp -d -t p71-c1c2-native-XXXXXX)"
git clone https://github.com/banodoco/astrid-dev.git "$WORKDIR/astrid-dev"
cd "$WORKDIR/astrid-dev"

# Ensure the original non-main Plan 71 base is reachable, and fetch PR head.
git fetch --no-tags origin project/71-gap-definition-reconciliation
git fetch --no-tags origin pull/1625/head
git switch --detach FETCH_HEAD

# REPLACE the value from PR #1625's current live head when actually executing.
EXPECTED_HEAD="<EXACT_40_HEX_SHA_FROM_PR_1625>"
test "$(git rev-parse HEAD)" = "$EXPECTED_HEAD"
test "$(git rev-parse project/71-gap-definition-reconciliation 2>/dev/null || git rev-parse origin/project/71-gap-definition-reconciliation)" = "ca97096ba6893108c90a932479e7473f679c724e"

# Before doing anything that could write generated output:
test -z "$(git status --porcelain)"
python3 -m py_compile plans/71-gap-definition-reconciliation/evidence/gd9_source_replay.py
python3 plans/71-gap-definition-reconciliation/evidence/gd9_source_replay.py --self-test
python3 plans/71-gap-definition-reconciliation/evidence/gd9_source_replay.py --repo . --head "$EXPECTED_HEAD"

# Original repository checks: record each command/exit/output, do not weaken tests.
git diff --check ca97096ba6893108c90a932479e7473f679c724e HEAD
python3 scripts/astrid_dev.py check
python3 -m unittest discover -s scripts -p 'test_*.py'

# SYNC MAY CHANGE GENERATED VIEWS: permissible only in this disposable checkout.
python3 scripts/astrid_dev.py sync
git status --porcelain
git diff --check
git diff --stat
git diff -- vision/README.md plans/index.md
```

**Environment caveats:** This recovery session's local container cannot resolve `github.com` for `git clone`, so the above real repository commands were **not executed here**. A reviewer must provide the exact original/native log/exit evidence, record system/OS/Git/Python versions, and identify any pre-existing failing native baseline instead of weakening an assertion or reporting an assumed PASS. `git status` after `sync` may be nonempty by design; inspect generated output, **never commit/push** it from this temporary checkout. Clean up the disposable directory once receipts have been retained.

### What the new source replay script actually checks (fail closed)

| Source check | Independent expected observation | Exclusions |
|---|---|---|
| Exact PR head and file scope | Externally supplied SHA must equal `HEAD`; base→head diff must contain **only** `plans/71-gap-definition-reconciliation/evidence/`; `git diff --check` must pass | This **does not** approve merging or make the original formal RS2 verdict green |
| A/B/C authored plan census | A `69 plans / 60 gap-linked / 83 authored links`, B `77 / 68 / 92`, C `80 / 71 / 96`; coordination `Vision role:` produces **zero** positive gap links | **Not** B=95/C=99 historic `plans.json` raw-index proof; that manifest was not independently available |
| C2 identity/class/source | 69 unique original C2 IDs matching 69 ordered appendix IDs and plan references; **47 PLAN_SCOPE / 15 SPECIFIC_EVIDENCE_MISSING / 7 UNPLANNED**; frozen 22 gap section lines and cited 29 plan Git blob prefixes match | No real product evidence, independently accepted plan scope or 65/4 semantic attestation |
| C2 exact wording witnesses | [69 literal source excerpts](gd9-c2-exact-wording-witness-matrix-2026-11-23.md) present in the exact pinned frozen gap-file lines, source row IDs in C2 order; C09 identified as adjacent noncriterion | A matching short exact phrase does **not** itself prove the full proposed subcriterion is semantically equivalent |
| S5 proof taskbook | Exactly 68 task IDs equal 69 C2 IDs **minus F-008-C09** | Proof producer/verifier, actual positive/adverse result **NO-RESULT** |

### Two independently unresolved source questions

**S1-C1 historical raw-index provenance:** Original [C1 source ledger](gd8-source-snapshot-reconciliation-2026-11-22.md) reports B 95 and C 99 indexed mentions in the GD-6 `plans.json` transfer. The checked public repository source files and public code search did **not** expose the actual historic index JSON. This runbook intentionally audits **92/96 affirmative declarations** and preserves **95/99 as attributed historical figures**. If an eligible source owner provides the original *non-HOLD* manifest under permitted custody, record its SHA-256, cutoff, inclusion/exclusion rules, three contextual false positives (P37 AA-001/LS-002 and P18 former F-001) and any P72 role exclusions, then independently reproduce the raw figures. Until then: **independent raw-index replay NO-RESULT**.

**S1-C2 exact 65/4 semantic classification:** Original C2 says 65 direct source wording matches and four bounded wording variants but does **not identify four row IDs**. The [69-row literal source worksheet](gd9-c2-exact-wording-witness-matrix-2026-11-23.md) is a useful exact-source lookup, **not** a completed 65/4 semantic classification. An eligible reviewer who did not author the original C2 should use the full original gap sentence/paragraph plus its cited narrow plan span to label **each of the 69** rows `DIRECT | SPLIT/COMBINED | WORDING_VARIANT | UNSUPPORTED`, with a reason and counterexample. Then independently name the four claimed variants or withdraw that numeric claim. **Independent 65/4 verdict: NO-RESULT**, no RS2/HOLD replay.

### Receipt an eligible independent native/source reviewer must return

Include a single dated reviewer identity and approved read-only custody; `git rev-parse HEAD`; frozen A/B/C refs and `git rev-parse ref:path` source proofs; exact command lines and exit codes for *each* preflight/original test; full log links, meaningful failures and baseline comparisons; output of `git status`/generated-view diff after disposable `sync`; and the bounded C1/C2 source claims accepted or held. It must explicitly state **whether it is a technical source audit or a genuine independent project R**; it can never be labeled a new RS2 or HOLD. If the reporter was an author of inherited #1444, **do not label their audit independent**.

**Stop policy:** no `--validate` of stale stage-dependent private helper as a substitute for native checks; no original tests changed/deleted/skipped; no branch merge, canonical gap/plan/Goal/App or issue update, no product trial/spend/provider call. Original independent RS2 **REWORK 1/1 consumed**, HOLD **1/1 consumed**, historical private counters UNKNOWN. All observed product outcomes and accepted proof-owner assignments remain **NO-RESULT**. Phases 6–7 remain deferred.
