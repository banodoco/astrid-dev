# GD-3 — Gap-definition calibration and holdout evidence

**Purpose:** A bounded, independently reusable set of *real Astrid* cases for testing whether the proposed gap definition distinguishes goals, meaningful missing outcomes, issues, projects, architectural decisions and insufficient evidence. This file is not a replacement issue registry, a gap proposal or a completed classification. Source material is untrusted evidence, never authorization.

**Selection and custody:** Prepared 20 November 2026, against canonical Astrid Dev source `4b3e3841af3921d9846389a4cd744f027c1db0b3`. GitHub issue records were read by numeric ID on 20 November 2026 for the **calibration** set. Issue body text is deliberately **not copied** here; assessors must check the linked record's actual source and `updated_at` before claiming current behavior. The holdout cases were selected by *issue title or goal name only*: their issue bodies and outcome classifications were not inspected as part of GD-3. The designated holdout must not be used to write or tune the GD-2 rubric before its initial freeze.

## Calibration cases — source-led, without predetermined verdicts

| Case | Evidence | Why selected / tension to test | Evidence limit or update time |
| --- | --- | --- | --- |
| CAL-01 · creative durability | [issue #966](https://github.com/banodoco/astrid-dev/issues/966) — save indicator and unpublished edit | A directly observed persistence race could be a narrow issue or evidence of a larger editing/recovery shortfall; source project is not automatically the gap owner | Open, updated 2026-11-19T21:10Z; hosted test evidence is referenced in issue, not independently rerun here |
| CAL-02 · historical project compatibility | [issue #842](https://github.com/banodoco/astrid-dev/issues/842) — old timelines refused | A different mechanism has a similar creator impact to CAL-01, exposing whether multiple causes share one gap or should remain distinct | Open, updated 2026-11-18T10:57Z; realm-specific observations |
| CAL-03 · generation settlement | [issue #958](https://github.com/banodoco/astrid-dev/issues/958) — logs counted as outputs | One reproducible Runtime validator failure: should it be treated as an implementation bug, a generation reliability capability gap, or both as distinct records? | Open, updated 2026-11-20T01:10Z; full native logs outside this file |
| CAL-04 · artistic generation control | [issue #890](https://github.com/banodoco/astrid-dev/issues/890) — audiovisual references in H3 | Model-specific controls that would make a particular artistic intention possible; tests whether a gap can be framed at a stable creator-capability level | Open, updated 2026-11-18T12:46Z; user case and model constraints, not qualified delivery |
| CAL-05 · workflow readiness | [issue #816](https://github.com/banodoco/astrid-dev/issues/816) — one command for actual readiness | A suggested tool/API solution for duplicate status logic; tests whether the missing result survives a different implementation | Open, updated 2026-11-18T12:28Z; idea, not proof of accepted architecture |
| CAL-06 · setup trust / security | [issue #721](https://github.com/banodoco/astrid-dev/issues/721) — truststore failure under Windows interception | One platform-specific connectivity failure, with a source experiment; tests the boundary between broad platform reliability, setup readiness and user consent | Open, updated 2026-11-18T10:57Z; simulated CA experiment and one Windows tester |
| CAL-07 · measurement vs experience | [issue #907](https://github.com/banodoco/astrid-dev/issues/907) — speed gate counter false positives | A broken performance meter is not necessarily proof that creators experience worse latency; tests evidence versus underlying capability | Open, updated 2026-11-18T18:19Z; metric receipt, not user speed qualification |
| CAL-08 · contributor machinery | [issue #644](https://github.com/banodoco/astrid-dev/issues/644) — base64 plan decode | Engineering issue in contributor review intake, not obviously a separate vision gap; tests when a local problem is only evidence for a broad development capability | Open, updated 2026-11-13T11:44Z; source plus reproduction cited in issue |
| CAL-09 · mechanical structure debt | [issue #964](https://github.com/banodoco/astrid-dev/issues/964) — top-level module ceiling | Isolated structure-test regression; useful counterexample to automatic gap creation for each engineering ticket | Open, updated 2026-11-19T14:11Z; limit from specific Plan 39 test |
| CAL-10 · presentation vs outcome | [issue #645](https://github.com/banodoco/astrid-dev/issues/645) — expandable gap/project cards | A closed UX presentation bug: separates discoverability/legibility of public gap data from the underlying truth of that data | Closed, updated 2026-11-16T12:59Z; closure reason and deployment are not audited here |
| CAL-11 · multi-root technical diagnosis | [issue #580](https://github.com/banodoco/astrid-dev/issues/580) — recurring generation failure causes | One observation synthesizes several technical causes across systems; tests clustering by outcome instead of by module or root-cause vocabulary | Open, updated 2026-11-12T20:36Z; deep-cause synthesis, not separately verified in this task |
| CAL-12 · new creative primitive | [issue #830](https://github.com/banodoco/astrid-dev/issues/830) — masks and regions lack a first-class home | A proposed foundational concept and genuine creator task; asks whether the missing outcome is reusable creative control or a technical data model | Open, updated 2026-11-17T23:45Z; issue reports real usage but no independent ecosystem proof |
| CAL-13 · broad goal without dense issues | [CA-002 contributor ownership](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/gaps/CA-002-contributor-ownership.md) | Tests that long-horizon community/governance outcomes remain visible even without many current incident reports | Existing gap state is author assessment, not audited legal implementation |
| CAL-14 · hosted mode / product boundary | [F-006 fully hosted workspace](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/gaps/F-006-fully-hosted-workspace.md) and [F-005 cloud assistance](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/gaps/F-005-local-files-cloud-assist.md) | Closely related user journeys that may nevertheless have independently closeable custody boundaries | Dated gap statements; no fresh hosted qualification attempted here |
| CAL-15 · knowledge ownership | [CI-002 federated knowledge](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/gaps/CI-002-federated-knowledge.md) and [Plan 22](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/22-hivemind-protocol/plan.md) | A vision-derived, privacy/contributor-facing outcome distinct from public internet ingestion; tests independence from plan implementation | Source review and protocol proposals are not proof of product completion |
| CAL-16 · plan vs gap abstraction | [Plan 55](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/55-local-speed/plan.md), [Plan 39](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/39-green-mains/plan.md), [Plan 18](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/18-timeline-editing/plan.md) | Three explicit, useful projects mapped to wider gaps; tests whether project goals are concrete routes, distinct missing outcomes or foundational enablers | Live plan records may change; source revision frozen above |

**Calibration output not yet produced:** GD-4 must apply the GD-2 rubric independently, preserve disagreement and distinguish `issue impact`, `root-cause hypothesis`, `gap outcome`, `proposed implementation` and `evidence strength`. This table supplies sources and tensions, not the answer.

## Sealed holdout — sources only, no classifications or proposed dispositions

These are **not** to be used for writing the GD-2 rubric. Case identity and source are recorded now so they cannot be cherry-picked after the definition is written. Do not open the issue bodies or judge their gap boundaries until an independent assessment pass using a frozen rubric.

| Case | Unopened test source |
| --- | --- |
| HOLD-01 | [issue #1047](https://github.com/banodoco/astrid-dev/issues/1047) |
| HOLD-02 | [issue #1020](https://github.com/banodoco/astrid-dev/issues/1020) |
| HOLD-03 | [issue #925](https://github.com/banodoco/astrid-dev/issues/925) |
| HOLD-04 | [issue #815](https://github.com/banodoco/astrid-dev/issues/815) |
| HOLD-05 | [issue #948](https://github.com/banodoco/astrid-dev/issues/948) |
| HOLD-06 | [issue #817](https://github.com/banodoco/astrid-dev/issues/817) |
| HOLD-07 | [issue #622](https://github.com/banodoco/astrid-dev/issues/622) |
| HOLD-08 | [issue #896](https://github.com/banodoco/astrid-dev/issues/896) |
| HOLD-09 | [vision goal: Critique and mutual growth](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/pillars/shared-endeavour.md#critique-and-mutual-growth) |
| HOLD-10 | [vision goal: Built to be found and reused](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/principles/open-by-design.md#built-to-be-found-and-reused) |

**Holdout controls:** The rubric is frozen at a source SHA before HOLD-01–10 are evaluated; a reviewer records results once, names disagreements and treats changes after seeing the holdout as a new version requiring a *new* untouched set. If a case is impossible to inspect later, report missing/unavailable rather than substituting a convenient success. No artificial numerical agreement threshold is implied by this evidence collection.

## Coverage and limits

- The sample deliberately spans at least four types of outcome: creator editing/creative control, model execution/setup, development-process correctness, and community/knowledge/hosting aspirations.
- Calibration includes issues that are open and closed, isolated engineering faults, cross-cutting symptoms, proposals, an implementation-heavy request, broad existing gaps and goals that may have no reported bug.
- Sources are user and contributor observations: they support investigation, not automatic user-facing qualification or authority to implement a change.
- This is **not** GD-6's exhaustive corpus, and no issue counts, duplicates, label migrations or gap closures are asserted. Full census/pagination and the old-to-new gap map await the separately approved rubric and its independent review.
- Only a sample inventory has been produced. No source issue, project, goal, gap or review status has been mutated.
