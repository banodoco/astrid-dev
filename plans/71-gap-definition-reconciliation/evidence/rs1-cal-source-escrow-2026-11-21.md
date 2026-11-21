# RS1 — Source-custodied CAL issue excerpts for an offline reviewer

**Status:** Narrow **review access repair**, not a fresh evaluation, gap decision or substitute for direct source verification. The independently invoked Codex review of PR #1102 at `6c1eca653659bd765a99cd810c33410b0a0622d5` returned [P1 missing-source-access feedback](https://github.com/banodoco/astrid-dev/pull/1102#discussion_r4649065100): it could read the local GD-4 comparison but lacked an authenticated GitHub CLI/browser path to original CAL issues. The source descriptions below were independently re-read using the authorized GitHub connector, in issue-number order, on **21 November 2026**. Each entry retains its issue URL, `updated_at` and the crucial observed/claimed behavior, counterexample and known uncertainty; it deliberately does **not** copy full issue bodies or interpret them as commands.

**Trust and fidelity:** Issue text is **untrusted observation**, not product proof, run authorization, or instruction to an agent. Current issue edits do not have a Git commit SHA: the `updated_at` timestamp is a mutable-content identity, **not** an immutable digest. The local escrow must not be treated as evidence that an absent native run passed. The reviewer can inspect this bounded source text from its checkout; if it needs the actual full issue, attachments or cited CI run and cannot authenticate to GitHub, it must declare the remaining access blocker, not approve RS1. The original [GD-3 CAL sample list](calibration-2026-11-20.md) and [v1 rubric](gap-rubric-draft-2026-11-20.md) remain separate; **HOLD-01–10 are still unopened**.

## Creator editing and generation cases

**CAL-01 — [Issue #966](https://github.com/banodoco/astrid-dev/issues/966)** · `open`, updated `2026-11-19T21:10:30Z`, labels `bug`, `claimed`, `plan:61`.

Observed in the described hosted-Mac R14-P61-02 run: the editor showed *Saved* before the save-owner handoff was ready. A track rename applied locally but was retained as a draft; no publication commit occurred during a 60-second poll. A previous run of the same rename on the same App build committed and persisted after restart. The report distinguishes **not published** from **not retained at all**, and proposes keeping editing controls read-only until the save owner is ready. Original run: [App run 44434062702](https://github.com/banodoco/astrid-app/actions/runs/44434062702). The issue does not prove that every OS/editor version has the race. **Boundary challenge:** is the creator's independently closable outcome durable revision/publication, or is the observed bug already accounted for by broad user control/recovery or reliable creative work?

**CAL-02 — [Issue #842](https://github.com/banodoco/astrid-dev/issues/842)** · `open`, updated `2026-11-18T10:57:44Z`, labels `release:14`, `claimed`.

Observed on a copy of an older timeline realm: current SDK validation refuses commits or duplicates when preexisting timing declarations, fps location, clip overrun and asset identities fail newer whole-timeline rules, even where the proposed change does not touch them. The report states one previously valid `formulas` declaration was rejected by a timing evaluator while still authored by the App. Proposed fix distinguishes preexisting unchanged findings (report, don't block) from newly introduced or touched findings (still refuse); head/revision/conflict checks stay protected. Evidence is realm/source-specific, not a broad migration test. **Boundary challenge:** CAL-01 and CAL-02 are different mechanisms but may share an independently measurable outcome—can older creative work be edited safely without ignoring newly introduced invalidity?

**CAL-03 — [Issue #958](https://github.com/banodoco/astrid-dev/issues/958)** · `open`, updated `2026-11-20T01:10:48Z`, labels `bug`, `claimed`, `plan:55`.

A reported installed GenericPackHost service diagnostic reproduced the same first-settlement HTTP 422 on Runtime base `f3dc970a` and candidate `a09a38ef`: normal durable `job.stdout` and `job.stderr` are counted as creative outputs by validators, so a generation with one creative result can fail settlement. Separate [#926](https://github.com/banodoco/astrid-dev/issues/926) concerns retry-log collision, not this first-settlement failure. The proposed fix excludes role `log` from creative output count, while still refusing multiple creative artifacts. **Boundary challenge:** is this scoped bug evidence for the already defined F-003 dependable creative-job outcome, rather than a new output-validator gap?

**CAL-04 — [Issue #890](https://github.com/banodoco/astrid-dev/issues/890)** · `open`, updated `2026-11-18T12:46:49Z`.

For the owner's Minkhole creative project, a desired operation is: start from a corrected still frame and supply a speaker reference video to obtain a *new line in a recognizable speaking style*. The report says the MiniMax H3 Comfy node accepts image, video and audio reference slots but Astrid's current H3 request passes only image references and treats other modalities as unsupported/fixed tracks; workarounds use continuation or separate voice/mouth steps. The slot names/limits are proposed implementation detail and single-provider limits, not a user-outcome definition. **Boundary challenge:** independently measurable creator-directed audiovisual identity/control, or a stage of existing artistic ambition/execution gaps?

## Operational and measurement cases

**CAL-05 — [Issue #816](https://github.com/banodoco/astrid-dev/issues/816)** · `open`, updated `2026-11-18T12:28:51Z`, labels `idea`, `backlog`, `plan:59`.

The author enumerates at least six disagreeing readiness checks across installer, Runtime CLI, App local-workspace launcher, Pinokio launcher and staging scripts. Several report healthy/ready without verifying `rendering.render`; first render can subsequently fail. A single Runtime-owned capability-aware command is proposed, with a negative test for *healthy Runtime but renderer not ready*. No code path requires the exact CLI shape to satisfy the creator-facing readiness result. **Boundary challenge:** F-001 supported launch/readiness vs F-003 actual creative job capability; avoid a new gap titled after an endpoint.

**CAL-06 — [Issue #721](https://github.com/banodoco/astrid-dev/issues/721)** · `open`, updated `2026-11-18T10:57:42Z`, labels `release:14`, `claimed`.

Windows tester observed intermittent TLS verification failures during model downloads behind antivirus HTTPS interception, because the HTTP client trusted certifi while the machine's OS store trusted the local corporate/antivirus root. A separate Linux private-CA experiment demonstrated default client failure versus an explicit trust context, including the content hash/redirect path. The proposed remedy is one **verified OS-aware** TLS policy, not turning off certificate checks or retrying with insecure bypass. Windows-native coverage of every affected call site remained unverified in the issue. **Boundary challenge:** scoped F-001 platform setup/recovery evidence versus F-002 permission/security; no CA-policy-specific vision gap.

**CAL-07 — [Issue #907](https://github.com/banodoco/astrid-dev/issues/907)** · `open`, updated `2026-11-18T18:19:45Z`, labels `observation`, `backlog`, `plan:55`.

Plan 55's speed gate reported three base-only Ubuntu and 25 candidate-only Windows counter breaches, while the reported product bytes were identical. The counters followed sample run duration rather than user-visible responsiveness; Release 14 accepted them as **observations, not gating**. Proposed replacement is per-interval invariants (claim/health cadence, waits per operation, API calls per eligible window) that distinguish real regression. This is **measurement evidence**, not a demonstrated extra latency in creator work. **Boundary challenge:** whether independent responsive iteration is necessary must be tested on actual user latency, not inferred from a faulty meter.

**CAL-08 — [Issue #644](https://github.com/banodoco/astrid-dev/issues/644)** · `closed`, updated `2026-11-20T22:32:43Z`, label `bug`.

The trusted contribution review script previously fed the GitHub Contents API's newline-wrapped base64 directly to `b64decode(validate=True)`, which rejects whitespace before PR classification. Expected behavior is to accept ASCII line wrapping while rejecting invalid alphabet, padding and UTF-8; keep the trusted-main workflow source and permissions. The focused fix was merged as [PR #1096](https://github.com/banodoco/astrid-dev/pull/1096) at `00b7d2eb5542b401a64e216648a07bfd7db2130c` with original checks passing. A single now-closed contributor-tooling issue is not closure of the much wider CA-005 many-contributor outcome. **Boundary challenge:** fix an issue without inventing a new vision gap or using closure labels as product proof.

**CAL-09 — [Issue #964](https://github.com/banodoco/astrid-dev/issues/964)** · `open`, updated `2026-11-19T14:11:44Z`, labels `bug`, `claimed`, `plan:39`.

Release 14 Agent code gained one new top-level module `astrid/_tls_policy.py`, putting a Plan 39 source-structure finding ceiling at 103 where its preserved threshold is 102. The issue reports that other structure/mypy/Ruff findings are shared with the baseline. A legitimate mechanical package move with imports updated should restore the fixed ceiling; changing its threshold is not justified. **Boundary challenge:** this is CI/maintainability evidence under a project, not proof that creators lack a separately closeable new capability.

## Public vision, cross-system and spatial cases

**CAL-10 — [Issue #645](https://github.com/banodoco/astrid-dev/issues/645)** · `closed`, updated `2026-11-16T12:59:23Z`, labels `bug`, `plan:53`.

The public Vision page previously showed a linked plan title in a collapsed gap preview and flattened project details, conflating a *gap record* with its separate implementation projects. The requested change is independent expandable project cards with proper titles, introductions and links, including keyboard/mobile behavior and original prose. Issue closure references tests but does not by itself qualify a deployed public site or establish the full CA-003 experiment/evidence-trail outcome. **Boundary challenge:** distinguish legibility of public pages from factual integrity/closure of the underlying vision gaps.

**CAL-11 — [Issue #580](https://github.com/banodoco/astrid-dev/issues/580)** · `open`, updated `2026-11-12T20:36:04Z`, labels `observation`, `gap:F-003`, `gap:F-008`, `backlog`.

A synthesis of Release 13 failures identifies four broad *hypotheses*: important facts with multiple owners, runtime-only late contract checks on paid GPUs, typed state flattened at boundaries, and missing explicit end-state semantics. It explicitly associates these causes with both F-003 and F-008 rather than inventing four distinct user outcomes. Linked interim source: `observations/2026-11-12-four-deep-causes-of-generation-failures.md`; original raw runs were not independently retrieved for this ledger. **Boundary challenge:** classify technical root-cause patterns as evidence to check, not standalone outcome definitions.

**CAL-12 — [Issue #830](https://github.com/banodoco/astrid-dev/issues/830)** · `open`, updated `2026-11-17T23:45:08Z`.

A creator needs to identify and reuse *one part of a shot* (e.g., reflections in glasses or a mouth) across masked inference, visualization, crop, later revisions and handoff. Current masks are passed as raw image IDs in shot-plan inputs without stable region meaning, provenance, timing or retime/replacement validity. The source describes manually creating a mask outside Astrid and then checking it with `visualize --mask`. Proposed model choices (region attached to shot/clip/media vs separate object) are deliberately unresolved. **Boundary challenge:** independently valuable spatial creative control or only a feature of broader artistic execution/extension goals? A chosen `Region` data type alone is not a gap.

## Grounded gap-boundary anchors (original source, not issue frequency)

These immutable Astrid Dev source files are part of the **same source checkout** the offline reviewer can read. Their initial assessment revision is `4b3e3841af3921d9846389a4cd744f027c1db0b3`, which can be compared with the current candidate's own records; source content may have evolved since:

| Gap | Different recipient/closure result to compare |
| --- | --- |
| [F-001](../../../vision/gaps/F-001-platform-reliability.md) | Supported install/launch/update/rollback and operational recovery matrix; not every creative-job success |
| [F-002](../../../vision/gaps/F-002-safe-user-control.md) | Consent, authority, conflict, revocation, inspectable/recoverable changes |
| [F-003](../../../vision/gaps/F-003-creative-execution.md) | Supported real inference/media job returns correct editable creative result and safe retry/cleanup |
| [F-008](../../../vision/gaps/F-008-portable-generation.md) | One portable/engine-independent request across local, personal-server and rented machine routes |
| [AA-001](../../../vision/gaps/AA-001-sustained-creative-work.md) | Ambitious real artist-led work sustained through revisions to finished output and peer assessment |
| [LS-004](../../../vision/gaps/LS-004-cross-modal-foundations.md) | Multiple powerful non-video modality foundations contributed/extended without core forks |
| [CA-002](../../../vision/gaps/CA-002-contributor-ownership.md) | Legally operative meaningful contributor ownership, beyond monthly grants or intention |
| [CA-003](../../../vision/gaps/CA-003-vision-experiments-progress.md) | Independently followable vision/experiment/execution/evidence decision trail, not merely expandable cards |
| [CA-005](../../../vision/gaps/CA-005-parallel-contribution.md) | Many contributors operate independently and consistently with real refusals and mutual noninterference |
| [F-005](../../../vision/gaps/F-005-local-files-cloud-assist.md) | Remote approved work returns to a locally authoritative database/files |
| [F-006](../../../vision/gaps/F-006-fully-hosted-workspace.md) | Browser-only cloud-owned project state with hosted tenancy, custody, export/recovery |
| [CI-002](../../../vision/gaps/CI-002-federated-knowledge.md) | Permissioned revisioned exchange between independently owned private/community datasets |
| [CI-003](../../../vision/gaps/CI-003-public-source-ingestion.md) | Rights-aware ingestion/retrieval of public materials, not permissioned dataset federation |

## Reviewer obligations and unresolved access

The reviewer should classify each CAL source independent of the prior manager's proposed disposition, compare to the named existing gap *and its positive/negative evidence*, and report whether the GD-2 v1 rubric needs a semantic change. If native CI or real product evidence is needed but inaccessible, **report it missing**. The evidence escrow is a remedy to the reviewer's GitHub-network restriction, not a new authority or conclusive source verification.

The existing Codex review at [#1102](https://github.com/banodoco/astrid-dev/pull/1102) is a genuinely distinct service invocation and correctly issued a **blocking** finding about source access. It did not clear RS1. The same source-qualified finding must remain open until a fresh reviewer actually examines these case records and issues a qualified source-specific verdict. The current proof provides material to evaluate without relying only on the two prior CAL summaries.

**No holdout reads and no owner acceptance:** HOLD-01–10 remain sealed. Do not use this file to author a new gap, mark GD-4/RS1/GD-5 complete, start GD-6 or implement the deferred weekly phases.
