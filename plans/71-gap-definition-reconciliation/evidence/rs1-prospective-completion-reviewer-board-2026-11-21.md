# Plan 71 RS1 — prospective `completion_reviewer` dispatch board

**State:** `SUPERVISOR-AUTHORIZED / PROSPECTIVE BINDING SELECTED / RUNTIME PREFLIGHT PENDING / NOT DISPATCHED`.

**Authority:** The owner, acting explicitly as the authorized supervisor on **21 November 2026**, instructed the accountable Plan 71 manager to make a *new*, separate, prospectively authorized source-capable RS1 review assignment. The review must not be retrospectively attached to the earlier unbound supervisor/local or GPT-6 source assessments. This is an **Astrid-dev-only** run under [Manage](../../../agent/roles/manager/whole-project.md#steps), **not** a product release, another project, or a new review round.

This committed file is the **durable dispatch board and role-selection/authority record** for this one RS1 attempt. It is **not** a claim that an unavailable model is available, an already-running reviewer, a completed `run.yaml` or a verdict. The [shared run contract](../../../agent/shared/run-contract.md#routing-and-bindings) requires the *exact runtime model identifier*, supported effort, availability and actual execution identity to be resolved **in the owning run's gitignored `run.yaml` (or the authoritative runtime dispatch board) before dispatch**. Its [actual-route provenance rule](../../../agent/shared/run-contract.md#actual-route-provenance) prohibits placing exact runtime model IDs or raw private usage logs into repository PR artifacts. Do not copy a fill-in template and falsely mark it active; do not fabricate or backdate a run.

## Prospective role binding selected by the authorized supervisor

| Field | Supervisor-approved prospective selection | Required pre-dispatch verification |
| --- | --- | --- |
| Accountable project manager | Existing owner-authorized Plan 71 whole-project manager, per [Plan 71 inputs](../inputs.md) | Confirm the actual managing session/run custody; no competing accountable manager |
| Review stage | `RS1`, one previously planned high-judgment definition-review stop, **no qualified round yet consumed** | Preserve the existing run's accepted budget, stage and count; do not reset them |
| Routing and role | `S` (review row) with `roles.completion_reviewer -> models.completion_reviewer` | Verify the mapping is present in the *actual* active run configuration or authorized dispatch board |
| Model family/provider | **Astra (Codex), separate high-judgment reviewer**, supervisor-selected for a new run | Bind the supervisor-requested *exact available* runtime model identifier in the private run configuration; inspect its real availability in the chosen executor |
| Reasoning effort | **high**, supervisor-selected | Verify that the *selected exact model* and runtime support `high`; do not relabel another effort or silently fall back |
| Reviewer identity | A **new independent** subagent/human reviewer, not any candidate author, Plan 71 manager, prior CAL assessor, or routine generic code-review bot | Record the distinct actual session/run ID, invocation path and executor; require `fork_turns=none` or an equally verifiable clean context if the supervisor's Codex environment supports it |
| Source/permissions | **Read-only** on one Astrid Dev repository and existing evidence, with original CAL issue access or explicit escrow limitations | Verify checkout/ref availability, same commit/blob, actual source-read capability and scope before starting; no write/merge/issue mutation or access to sealed HOLD issue bodies |
| Actual private binding path | `plans/71-gap-definition-reconciliation/.otto/runs/<existing-matching-run-id>/run.yaml` in the authorized runner, **or the selected run's authoritative dispatch configuration** | Discover and resume any matching existing run. The concrete run ID, provider model ID, supported effort/availability and environment permission are **NOT YET VERIFIED HERE**; do **not** choose an arbitrary ID or invent `available` |
| Supervisor dispatch | **After** binding and preflight receipt, by the authorized supervisor | Dispatch a **fresh, separate** reviewer once against the exact accepted candidate and require a portable signed/session-linked report |

**Model identity boundary:** The supervisor's request names a particular Astra generation and `high` effort. The exact executable `model_id` must be recorded in the gitignored active run configuration, **not** guessed from a display name or published in this tracked PR. The prior supervisor-reported subagent `/root/review71/exact_head` was independently invoked before this assignment; it remains supplementary evidence, **not** the newly bound reviewer.

**No historical rewrite:** Do not change the identity, verdict, timestamps, model configuration, or `consumed_rounds` of the earlier source-custodied but **unbound** evaluations. If genuine pre-dispatch records from them are later found, reconcile them *as historical evidence*, not as retroactive authorization.

## Frozen candidate and source custody — verify exact values again at dispatch

- **Repository and project:** `banodoco/astrid-dev`, `project/71-gap-definition-reconciliation` (the authorized dev-only project branch).
- **Review target:** [GD-2 v1 PR #1102](https://github.com/banodoco/astrid-dev/pull/1102), exact **review HEAD** `04573347bfc1f5d34df7c18e39b4c4c97878f5e8`. It must still be the live PR head at binding/dispatch; if not, stop and re-qualify, do not silently switch SHA.
- **Rubric source:** `plans/71-gap-definition-reconciliation/evidence/gap-rubric-draft-2026-11-20.md`, exact Git blob `ee8889bc8c8e07ffe0156960f47703d775b1f3b9`. Confirm byte-identical content from the selected HEAD and inspect lines 104 and 110; the former v0/v1 holdout-failure error was corrected on that candidate.
- **Escrow source:** `plans/71-gap-definition-reconciliation/evidence/rs1-cal-source-escrow-2026-11-21.md`, Git blob `e2625b19104316eaabe38eafabbab1b796d84700`, from the exact candidate tree. It contains **12 CAL original-issue excerpts** with source links and observed limitations, **not** full bodies or independent product proof.
- **Other in-sample evidence:** `calibration-2026-11-20.md` with CAL-01–16 labels and *unread* HOLD identities; relevant canonical goal/gap records and Plan 55 measurements; `gd4-manager-first-pass-2026-11-20.md`, `gd4-second-case-assessment-2026-11-20.md` and `gd4-comparison-2026-11-20.md`.
- **Original structural CI:** `documentation`, `vision-consumer-contract` and `review-intake` all passed on the above PR candidate. Green structural CI is **not** RS1 semantics.
- **Handoff:** [original RS1 review packet](rs1-exact-head-review-packet-2026-11-21.md), [supplementary and binding-limits record](rs1-supplementary-unbound-assessments-2026-11-21.md) and conditional [GD-5 decision brief](gd5-owner-decision-brief-2026-11-21.md).

## New, independent RS1 review assignment — READ ONLY

The supervisor's actual new reviewer receives this **full card**, its role binding and exact source identity at dispatch:

1. **Preflight gate.** Independently confirm your *actual* high-judgment role mapping, supported model/effort, fresh session identity and source access. Report model/configuration availability and any unsupported setting **before** doing the merits review. If unable to verify, return `BLOCKED — BINDING/ACCESS`; do not improvise a substitute model or claim completion.
2. **Source-first merits.** Read and apply the candidate's five gap-boundary tests to each CAL-01–16 source **before** consulting the earlier GD-4 authors' verdicts. Check the 12 original CAL issue sources if accessible; where only escrow is available, independently inspect the local escrow, timestamp/source identity and its factual limits; explicitly report any originals necessary but unavailable. The other four CAL sources are gap/plan records in the repo.
3. **Counterexamples and independent closure.** Challenge issue vs implementation vs vision-goal vs actual gap, the distinction between missing/reliably broken/merely unverified capability and *undemonstrated real creator outcomes*, one primary goal with separately closeable outcomes, alternatives to a new gap, and evidence of actual positive **and negative** closure while neighbors remain open.
4. **Named CAL cases.** For #966 versus #842, separate saved/edit-persistence/restart from historical-edit-and-duplicate refusal tests without auto-splitting. For #890 versus #830, distinguish lawful audiovisual reference-directed generation from reusable spatial regions with retime/refusal. For #907 and [Plan 55 historical source](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/55-local-speed/inputs.md#L9-L13), do not treat duration-dependent counters or historical **30.2-second instant-stand-in measurements** as contemporary measured time-to-reusable-result. Confirm local-authoritative F-005 vs tenant-hosted F-006 custody and isolated CA-002 legal rights, CI-002 revocable federation and CI-003 public ingestion. Explain what would falsify each grouping.
5. **Resolve two independent supplementary concerns rather than ignoring them.** Does rubric line 104 wrongly let a reviewer **authorize** a HOLD run, instead of only **recommending a frozen candidate** for separately owner-authorized execution? Does the rubric's warning against creating a gap from *merely missing tests* risk incorrectly dismissing a genuinely unproven high-level outcome such as sustained artistic work? Give the minimal proposed edit or explicit source-supported nonblocking rationale.
6. **Compare after independent assessment.** Only once you have formed and recorded your own case judgments, read the manager/second GD-4 passes and comparison. Identify every material disagreement by case and proof, and report nearest-gap alternatives, missing evidence and the original source limitations. Assess collision with the separate Plan 53 Goals/schema author and Plan 73 Markdown-first skill owner without touching their files.
7. **Return one exact-head, provenance-backed verdict.** `ACCEPT v1 FOR HOLDOUT ONLY`, `REWORK BEFORE HOLDOUT`, `REJECT v1`, or `BLOCKED — <exact missing source/binding>`, with per-finding `BLOCKING / NONBLOCKING`, source paths/lines or original issue references, alternative interpretation and minimum concrete corrections. Include confirmed reviewer/run/session identity, role, actual model/effort support, source route and limits, task identity and route usage. A generic “no major issues” PR bot receipt does **not** count. Do not impersonate another human, adopt the previous supplementary verdict by default, or sign from the manager's session.
8. **No new implementation permissions.** The reviewer **does not approve the holdout run**. On valid merits acceptance, it may *recommend* this exact frozen v1 for a separately authorized one-time holdout protocol. The accountable manager must verify the binding, review and freeze and obtain the necessary run-level authority before designating a holdout evaluator. The reviewer does not accept GD-5 or GD-9.

## Explicit stops and receipt to append only after execution

**HOLD-01–10 remain sealed.** Do not follow source links, search issue bodies, classify cases, infer answers, or use indirect results about them prior to a valid independently reviewed freeze and authorized holdout protocol. A failed v1 holdout must remain a **failure of the frozen version actually tested**, with a new untouched set for any revised version. No test skipping, no weakening of original checks or assertions.

**Owner gates:** GD-5 (definition) and GD-9 (catalogue migration) are separate, still **pending**. Do **not** begin GD-6 full-catalogue census, mutate canonical gap/goal/project records, or integrate this project into protected `main` without their applicable authorization. Phases 6–7 recurring Gap Review stay **deferred**.

**Known prospective receipt fields, intentionally not fabricated:**

| Required field | Current recorded state |
| --- | --- |
| Supervisor authorizes reviewer family/effort and single RS1 scope | **YES**, by this conversation's explicit 21 November 2026 direction |
| Durable role/identity and source-scoped assignment | **THIS BOARD**, committed by Plan 71 task PR |
| Actual owning run ID/private `run.yaml` or authoritative runtime dispatch binding | **UNVERIFIED — MUST RESOLVE BEFORE DISPATCH** |
| Exact runtime `model_id`, verified high effort support and availability | **UNVERIFIED — MUST RESOLVE BEFORE DISPATCH** |
| Reviewer fresh session ID / provenance and separation from candidate author | **NOT YET STARTED — MUST VERIFY** |
| Source-enabled checkout and independently verified SHA/blob/escrow read | **REQUIRED PREFLIGHT — REVIEWER MUST PROVIDE RECEIPT** |
| Qualified RS1 verdict and consumed qualified round | **NONE; 0 QUALIFIED ROUNDS CONSUMED** |
| Owner GD-5 / GD-9 decisions | **NOT GIVEN** |
| Holdout bodies opened / classified | **NO** |

**Handoff to supervisor:** Once this board has merged on `project/71-gap-definition-reconciliation`, locate the true Plan 71 active run or establish a fresh one *without resetting any existing accepted decisions*, fill the **private runtime binding** and verify executor/model/effort/source availability, then dispatch the new independent source-capable reviewer to the exact candidate above. Record its actual run/session and result as a new additive receipt, not as an edit to historical review provenance. If any binding preflight fails, stop at `BLOCKED` and name the missing capability.
