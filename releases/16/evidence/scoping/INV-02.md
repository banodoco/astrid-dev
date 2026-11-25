# INV-02 — Environment, GPU, workflow readiness and consent architecture

Run `r16-scoping`; session `INV-02-01`; 25 November 2026. Original independent Wave B report. Assigned route **S / Pro**. **Verdict: REWORK the shared contracts and acceptance tasks; KEEP P93, P94 and P90, consuming P20/P32/P56 and the necessary P35/P38 seams.** This is a scope judgment, not implementation authority, completed qualification, or permission to publish.

The smallest coherent solution is the existing generation path with one resolved placement, capability-specific observations, one exact desired-action plan, applicable consent, and recoverable adapters. The current source already contains much of this machinery. Its most consequential gaps are disagreement between inspection and execution about placement, unprobed success-shaped readiness, writes during supposedly read-only planning, inconsistent verified publication, incomplete managed Windows lifecycle, and unproved installed recovery. A new environment manager, approval service, downloader framework or generation engine would make those boundaries harder to settle.

## 1. Authority, identities and evidence limits

This report follows the [assigned dispatch][dispatch], [packet][packet], [procedure][procedure], [context][context], [evidence index][index], [CTX-00][ctx0] and [CTX-01][ctx1]. I read the exact proposed [scope-release][scope], [sense-check][sense], [evidence-only packet][packet-workstream] and [dispatch workstream][dispatch-workstream] at `7060b764ec16a638b0e6774f814eabf6d7b70c04`, plus their run contract. No Plan 73 installation/cutover or installed-skill verification is claimed. The assigned route is recorded; the client selector is not independently attested. Three bounded read-only helpers checked environment sources, consent/fetch sources and vendor hardware evidence. This session read the prerequisite originals and retains their adjudication and this report's authorship; helpers are not independent final release reviewers.

Only `releases/16/evidence/scoping/INV-02.md` is submitted, on `evidence/r16-scoping-inv-02-01`, created from **`a7ea0a52d641bbb7799ea141934833285a77ab03`**, into draft proposal branch `scope/release-16-scoping-record`. The evidence commit will differ from the reviewed proposal and source commits below. The exact submission head belongs in the PR and mailbox receipt, not a self-referential claim inside this file.

### Source register

GitHub references and handoffs were refreshed on 25 November, approximately 19:10–19:40 CET (18:10–18:40 UTC), with proposal/branch intake checked again before submission. All implementation claims below concern immutable source snapshots unless expressly identified as historical or proposed.

| Source | Exact identity and role |
| --- | --- |
| Reviewed proposal and required report parent | `a7ea0a52d641bbb7799ea141934833285a77ab03`, [draft #1964](https://github.com/banodoco/astrid-dev/pull/1964), head branch `scope/release-16-scoping-record` |
| Submission destination refresh | Proposal head advanced to `438dfc29c856c1d795140246b01009dffe339c61` for later evidence intake/dispatch. The reviewed proposal and this report's required parent remain `a7ea0a52d641bbb7799ea141934833285a77ab03`; no rebase, merge or proposal edit by this session. |
| Canonical planning main read | `1b9c7085beddc220de4c87e628f4112cb6df33e9`; P20/32/35/38/56/90/93/94 records and R15/R16 handoffs |
| Roadmap history | [#1956](https://github.com/banodoco/astrid-dev/pull/1956) merged; head `fd4f68eb698ffd5544215920f9c4549219cc4bbd`, merge `41350e4e778a18593264da59114911e59ee8ec53` |
| Agent integrated R15 | `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` |
| Runtime integrated R15 | `686ca695469bda48cd40a70824c4ccef2a137284` |
| App integrated R15 | `cc1d48f016fde55ad6b0609c619d8a4bcec56823` |
| VibeComfy integrated R15 | `55c3948212d23cf037fae8a4c6faad77d33e7279` |
| Product mains, refreshed separately | Agent `c0ad6b54aadd21630d98bb5039613e37efe92a8f`; Runtime `5120462d67479dc4719406d0d34440edb616ace1`; App `e0da794ac9d26a808ab4082b29f60408b66b3a4c`; VibeComfy `c0e910caab9734a551fb2c1a455fff72c3a1b1cb` |
| Transitive/source comparators | Current App manifest pins lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`, while lifecycle main is `f2948817eeb94af8dee76be21f6d673724f1606e`. Pinokio main is `1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb`. Neither a newer lifecycle main nor a launcher source head proves installed behavior. |
| Served comparator | CTX-00's independently recorded R14 manifest SHA-256 `8556f2183dfc5575508827ec449c23ea5bbc61792d8e85cfad309dff9d44dee7`: Agent `c0ad6b54aadd21630d98bb5039613e37efe92a8f`, Runtime `5120462d67479dc4719406d0d34440edb616ace1`, VibeComfy `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c`, required floor 14. Inherited historical observation, not a fresh live result. |

The [current App source manifest][manifest] now pins the Agent, Runtime and VibeComfy R15 heads above, schema `sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2`, `release: 15` and `required: 15`. The earlier reports' App/Agent mismatch and required-floor-14 observation are superseded **for this source manifest**. A fresh read of `https://astrid.haus/install-manifest.json` failed through the available web reader; no served-byte or installed-receipt refresh was possible.

The reviewed `a7ea0a52` proposal and planning main are diverged, each twelve commits beyond common ancestor `fd4f68eb698ffd5544215920f9c4549219cc4bbd`. Main includes newer P56 task handoff and R15 records; the reviewed proposal includes the research dispatch/index. This is not permission to refresh this report's parent or merge either side. Product main→R15 comparisons report zero behind commits in all four repositories, so no main-only commit was omitted by choosing these R15 heads. The Agent compare returned a 300-file projection; it is not a repository-wide diff audit.

No product code was executed. No tests, documentation validator, CI dispatch, build, install, native GPU action, rental, merge, proposal edit or other issue mutation was performed. The explicit report-only/no-tests assignment controls over ordinary run-contract validation advice. Static control-flow findings, historical issue observations, vendor compatibility, implementation proposals and missing proof are distinguished below. All verification descriptions are **proposed future work**, never claimed passes.

### Original prerequisites read and adjudicated

All nine required original reports and the separate SC-35 severity correction were read in full, including their final qualifications and task/proof sections. Long original displays were recovered in bounded sections; no unread prerequisite-original portion is being represented by a summary. This coverage does not imply an exhaustive read of every underlying issue, historical test log or repository file linked by those reports.

| Original, immutable identity | Judgment preserved in this report |
| --- | --- |
| [SC-93][sc93], `ace8e01a9455b97971691209682f65f568efcfda` | Accept discovery, selection and positive-readiness defects. Amend its universal ordered ladder: explicit compatible endpoints can be valid without local install metadata; computation may require an approved workflow. Preserve its non-Cartesian proof suggestion for comparison with SC-94. |
| [SC-94][sc94], `81105a08717746d0393ccf3bb126f8c71bbe2471` | Accept managed Windows, real compute, disk/recovery and prepublication proof needs. A Windows recipe is not a Windows lifecycle. Compare Portable against finishing the adapter before choosing. Correct literal `sm_89` requirement and distinguish driver-family floor from toolkit tables. Eight compute cells need not mean eight complete heavy install journeys. |
| [SC-90][sc90], `1bd93cf70f169e0db52f95ced5b8f9d189865539` | Accept one plan/apply and trust ownership. Refine exactness: action/recipe/target identity, not a claim that every transitive dependency byte is pre-resolved. An unallocated RunPod preview cannot be an executable exact-target plan. |
| [SC-56][sc56], `74eb2950b33233b076536f3178b1daaa86f675b1` | Keep integrated stage 1, preserve and absorb residual stage 2 into P90. Disagree with F2 insofar as it mandates agent-proof human authentication: P56 D7 and P90 explicitly accepted terminal consent as a speed bump. The pending backstop observation is now superseded by its Lead's DONE record. |
| [SC-35][sc35], `44d813650b7e8b3726bd41699e80c182db8f79a1`, and [classification correction][sc35-correction], `ebe295571bb58028fe72d98c3da2cbe7fd40eaa5` | Preserve F1–F5 as BLOCKING at their stated boundaries. This investigation consumes placement, trust/revocation, migration and pre-activation paid custody; it does not make the entire state migration a predecessor to every environment task. A stronger reading of F3 requiring unforgeable human approval needs the same explicit new decision as SC-56 F2. |
| [SC-38][sc38], `7687ef518c86998f610ff4cf963e58b0565f38a1` | Accept first-party process identity, installed closure and native proof prerequisites. Read-only observation of a human's server does not give custody. Its full provider/role consolidation remains its owner's task; environment work consumes a stable interface, not a second implementation. |
| [ISS-02][iss02], `9e34444b3c9269d42293ab30558561495d678e3b` | Accept retained RunPod money safety and concrete setup/recovery leads. Distinguish current source defects from historical #1446/#1648 and unproved #682. Do not infer success from CPU paths or replace an existing downloader solely because historical transfer failed. |
| [ISS-04][iss04], `e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00` | Accept first-use and actual editor/result proof. Update manifest identity; keep exact final-tuple qualification and required-check policy separate. Typed repair is a bounded task, not grounds for another diagnostics framework. |
| [HOR-01][hor01], `736712b914dc2b46e6fd66dad2206d573ecf1510` | Preserve its source-coverage blocker. Independently retrieved the specified P88 handoff/mailbox and relevant issue-query windows; this closes those retrieval gaps only, not the complete horizon audit. |

## 2. Numbered findings

BLOCKING means the acceptance contract or affected supported outcome must be resolved before it is accepted. It does not assert that every hypothesis is reproduced, or that every suggested implementation is mandatory. FOLLOW-UP is bounded non-blocking improvement; NOTE records context and limits.

### F1 — BLOCKING — Inspection and execution can select different targets

**Evidence, directly observed in source.** [`listing.target_selection`][listing] allows a saved Runtime attached endpoint to override repo/global/discovery selections, but not the environment override. [`GenerationFacade.targets`][sdk] uses that path and can separately save TOML. Actual generation calls [`placement.resolve_placement`][placement] first: request, Runtime default, then built-in; env/TOML discovery is consulted only when no explicit request and no default kind exist. The resulting frozen placement is converted to the preflight selector.

Thus Runtime default endpoint B plus `VIBECOMFY_COMFYUI_URL=A` makes inspection show A while automatic generation resolves B. This is a static counterexample, not an executed reproduction. Runtime managed/RunPod defaults also cannot be faithfully represented by an inspection helper that only extracts attached defaults. The current [setup skill][setup] says `targets` shows where generation would run, making the discrepancy consequential.

**Impact.** A person can approve downloads for the displayed environment and run against another; stale selections can masquerade as a new setup failure. Adding a new readiness record alone will preserve the disagreement.

**Minimal change / owner.** P93 CD-1/CD-3 consume the existing frozen P32 Placement resolver for inspection, planning, apply admission and generation. P35 owns durable selection and a conservative migration of old TOML choices; explicit per-request overrides remain transient. Choose and document precedence once, including how conflicting saved/env/repo values are exposed. Do not silently fall back from an unavailable saved target or create a second selection token/resolver. Bind actions to the resolved environment identity, not the string `managed` or a bare reusable port.

**Verification proposed.** Conflicting explicit request, Runtime default, env, repo/global TOML and discovery; all three placement kinds; another actor's preference; unavailable saved target; changed selection after planning. Displayed, planned, admitted and submitted target identities must agree. Denial leaves saved placement unchanged.

### F2 — BLOCKING — Readiness needs positive, scoped evidence without a universal execution ladder

**Evidence, directly observed.** [`readiness_envelope`][preflight] derives `ready` from an empty issue list. `targets()` explicitly does not probe, including its RunPod-preferences branch. `GenerationReadinessError` reconstructs a named field whitelist, so a newly added plan/observation field can disappear unless every wrapper is updated. Discovery's [`_probe_server`][local] defaults its shape check off for base ports; optional Pinokio scanning collapses several timeout/error conditions into empty results. Actual attachment checks a limited `/system_stats` shape. Conversely, inventory listing already declares a `target_inventory` scope and unverified model bytes: do not erase that useful qualification. Existing [`hc03-worker-readiness.v1`][engine-readiness] explicitly does not qualify inference and emits `gpu_qualified:false`; that is an honest scope, not a defect to remove.

**Impact.** A listening process, registered path, worker or empty error list can be mistaken for a usable workflow. A rigid installed→reachable→identified→compatible→computes→workflow-ready sequence also rejects legitimate explicit loopback endpoints whose filesystem/interpreter identity Astrid cannot know or use. Discovery's guessed Python path is not execution permission. `delivered` cannot be a prerequisite for the first run.

**Minimal change / owner.** P93 CD-1 owns one typed observation extension in the current envelope. Each predicate is pass/fail/unknown/not-applicable, with target, capability/workflow scope, reason, evidence and freshness. Required unknown is not ready. Project these facts into one next action; use dependencies, not a universally mandatory linear sequence. P94 supplies managed install/compute observations; P90 supplies requirements and applicable approval; P38 supplies verified first-party identity. Preserve inventory and HC03 scopes. Target-only inspection need not install dependencies or execute GPU work.

For managed environments, static support checks precede consented minimum-environment installation; exact-interpreter compute precedes large workflow models. For human-owned endpoints, compatible API/explicit endpoint choice can precede a consented target-executed workflow witness; install metadata can remain unknown when no filesystem mutation is requested. Do not run a guessed interpreter, launch Desktop, or demand a managed reinstall merely to fill a rung. Do not label that endpoint as a particular Desktop installation without association evidence.

**Verification proposed.** Running/closed/stale Desktop, Portable/Git/Pinokio, permission-denied discovery, timeout/incomplete scan, several installs, HTTP non-ComfyUI responder, another valid ComfyUI on an old port, lost/replaced process and no probe. Every port gets an appropriate API-shape check; an empty scan is not “none installed.” Revalidate relevant identity/freshness at apply and run. Typed observations survive CLI/SDK/error serialization. Unrelated queued human work remains untouched.

### F3 — BLOCKING — Exact planning must be read-only and bind durable intent, not volatile observations

**Evidence, directly observed.** [`asset_gaps`][asset-gaps] lines 373–441 already hashes the full wanted model set, including present items; keep this property so successful progress does not create a new desired plan. It binds entry name, mode, endpoint and file metadata, but not full workflow revision/content, verified environment/root/interpreter or responder association. At lines 423–424 it calls `_hard_links_supported`; lines 467–483 create/link/remove target files. Apply calls the planner before digest and low-disk refusal. The renderer and [setup skill][setup] nevertheless say the plan writes nothing.

**Impact.** Declined, stale or low-disk requests can mutate a target; a reused URL can apply a previously reviewed action set to a different environment. Conversely, hashing timestamps, free space, cache progress or a fresh listener PID would invalidate safe same-plan resume.

**Minimal change / owner.** P90 WS-2/WS-9/WS-3 owns one immutable desired-action plan, using P32 requirements and Placement. Bind schema, entry/workflow content revision, approved source URL/full commit/hash, recipe and declared package actions, placement/ownership class, concrete environment identity, exact destination roots and operation set. P93 supplies attachment association; P94 supplies managed receipt/interpreter identity. Keep free-space readings, progress, observation time and transient health outside the digest and recheck them at admission. A restart can invalidate reachability/compute evidence without necessarily changing an unchanged durable install plan.

Move target-writing capability probes behind applicable consent, or plan a conditional no-clobber publication adapter without probing. Read-only network metadata resolution may be declared; it cannot run setup code. A server's `/folder_paths` response does not authorize writes: absorb P20's still-open P4.6b.1 into an explicitly approved destination-root rule. Permit legitimate extra-model roots outside the install tree when explicitly approved; reject arbitrary, symlink/reparse-redirected or changed destinations. Unknown local layout permits read-only attachment, not filesystem writes.

P56 D12 explicitly accepts disclosed install-time resolution of transitive packages with protective guards. Exactness here must not promise fully locked transitive bytes or invent a new universal resolver. The displayed recipe/action scope must expose this limit and refuse protected-package replacement. Likewise, a **no-machine RunPod preview** can list requirements, risks and bounds without allocating; only the same compiler bound to a verified allocated machine can yield an executable target plan. Source grants can carry forward within their scope; an unbound preview digest cannot authorize arbitrary later targets.

**Verification proposed.** No target files on planning, no consent, invalid digest or insufficient space; changed workflow/root/interpreter/recipe/source or destination refused; same plan resumes its own verified progress; wrong responder on the same URL; changed free space alone does not change desired intent but can block execution. Test the real CLI→plan→apply producer and all callers, not only a digest helper.

### F4 — BLOCKING — Consent, trust and ownership need one policy that preserves the accepted threat model

**Evidence and disagreement.** [P56 inputs D1/D3/D6/D7/D8/D12][p56-inputs] permit bounded explicitly approved additions to user-owned ComfyUI, approved sources outside Hugging Face, never running `install.py`, and terminal consent as a speed bump; the earlier requirement that an agent cannot approve was explicitly withdrawn. [P90 plan][p90-plan] and [inputs][p90-inputs] exclude signing, registries and sandboxing and acknowledge that an agent can type a flag. [`node_approvals`][node-approvals] documents that its token is not a secret, signature or proof of human identity. Therefore SC-56 F2's mandatory non-forgeable human surface is a new scope choice, not an already breached R16 promise. SC-35 F3 remains a blocking grant/revoke design prerequisite without silently strengthening that threat model.

**Impact.** Treating an exact digest as authorization, or a generic settings checkbox as evidence of a person, is misleading. Reusable approvals that ignore revocation at apply/resume can make the promised revoke operation ineffective. Requiring new human consent for every unchanged resume would also defeat P90's accepted reusable trust.

**Minimal change / owner.** P90 defines explicit approve/revoke operations and exact grant scope: actor, normalized source and full revision/content identity, recipe/declarations, allowed operation and placement/ownership class, plus any concrete-environment restriction. Apply checks both action identity and an applicable current grant. User-environment mutation and paid allocation are separate permissions. A previously approved matching grant need not be reissued; material scope drift requires a new plan and the missing grant. Keep the disclosed terminal limitation; do not claim these operations resist a malicious same-privilege local agent. A stronger authentication boundary is an explicit owner decision with its own cost.

P35 supplies one actor-scoped durable authority using the existing [Runtime version/idempotency mechanisms][runtime-app-state]; no parallel trust file or credential vault. That primitive has a 16 KiB object limit: choose bounded records and explicit overflow/conflict behavior, not an assumed unlimited settings object. Entry sidecars can retain provenance/installed receipts, but cached or derived trust must not resurrect a revoked grant. Define whether a separately explicit entry grant survives revocation of reusable trust, and expose that distinction. Check revocation at apply/resume, not merely the next plan. Loss of authoritative state or uncertain migration fails closed for new privileged actions. Revocation does not silently uninstall code or terminate an already-running task; specify its effect on future actions and any safe cancellation separately. Preserve opt-outs, negative/revoke state, old-client and rollback behavior under P35/P29 migration.

Ownership remains precise. Human-owned Desktop/Portable/Git and external Pinokio ComfyUI are never automatically started, stopped, upgraded or repaired. P56 D1 allows exact new node/model additions only if no existing Python package or pack folder is changed; when that cannot be enforced, offer manual action or an isolated managed environment. The setup skill's existing “models only; no nodes” behavior remains truthful until P90's bounded additions exist and their docs land together. Astrid's own Pinokio-managed application is a different owner: P10's launcher controls it. No hardware-detection result widens either permission.

**Verification proposed.** Denied approval; conflicting exact pins; changed target/recipe; copied entry; grant issued by another actor; revoke between plan and apply/resume; authority unavailable; stale sidecar/cache; migration/backup/rollback with revoked grants; explicit regrant; already installed bytes remain accurately reported. Ordinary setup approval must never rent a pod. No secrets enter plan JSON or generic app-state.

### F5 — BLOCKING — Consolidate verified publication and recovery policy, preserving useful download implementations

**Evidence, directly observed.** Attached [`asset_gaps._fetch_into_folder`][asset-gaps] stages under an exclusive name, retains resumable state, calls `fetch_verified` and uses no-clobber publication. [`asset_alignment.fetch_verified`][asset-alignment] documents that the underlying fetch publishes before verification; managed `_fetch_model` supplies the actual final path. [`VibeComfy.fetch`][vibe-fetch] performs `os.replace(tmp, path)` at line 646 before forced verification at 654. Its `read=None` timeout lets a no-bytes stall evade a deadline checked only between chunks. In contrast, [`model_downloader`][model-downloader] has useful bounded-range/cache handling and verifies the partial before final replacement. A consumer reading the bad final file during that window was not reproduced; the ordering itself is explicit.

**Impact.** A managed model can appear final before its hash is accepted; cancellation, disk exhaustion or stalled transport can leave confusing progress. Rebuilding every downloader to fix these differences risks losing existing Range, cache and resume guarantees. Historical #722 is not proof that today's attached path still lacks resume.

**Minimal change / owner.** P90 WS-16 with P32 F4 owns common planning/apply semantics; P94 ER-4 owns capacity/recovery acceptance. Establish one expected-artifact, bounded-transfer and verify-before-publication contract with storage/transport adapters. VibeComfy supplies byte transfer and verification; Agent owns authorization, destination selection and action orchestration. Reuse staging, no-clobber, resume and observed hash receipts. Remove bypasses only when their consumers use the shared policy. Do not create a fifth downloader or a background Runtime queue merely to call the operation a task.

Plan peak **additional** bytes per actual volume: partial download, cache if separately copied, expanded archive, Python/wheels, environment staging, publication copy/link policy, retained working environment and reserve. Avoid double-counting shared bytes; do not equate total model bytes with peak. Report bounded estimates and unknowns honestly, recheck before stages, and handle mid-stage ENOSPC without deleting unrelated work. Capacity checks before mutation cannot themselves make probe files. Source/hash changes cannot reuse an old partial. Bound no-progress reads and cancellation, and distinguish retryable transport failure from incompatible content. A model without a published hash needs explicitly disclosed first-use trust plus the observed receipt hash; inventing an upstream hash is not verification. P56 D3's approved external URL capability is still a bounded residual: current `_source_url` only accepts the Hugging Face route.

**Verification proposed.** Interrupted multi-action apply preserves verified action one while action two resumes; changed source/hash; hash mismatch never publishes a final model; previously existing file never clobbered; disk drops mid-transfer; source reports wrong ranges/length; transport yields no bytes; cancel/restart; Windows TLS and actual built-in download. A warm run fetches no unchanged bytes. CPU fixtures prove policy; native transfer proves the supported filesystem and transport path.

### F6 — BLOCKING — Managed provisioning must become a recoverable platform adapter and survive update

**Evidence, directly observed.** [`engine_runner`][engine-runner] refuses Windows; [`engine_platforms`][engine-platforms] offers Linux adapters; [`engine_local_endpoint`][engine-endpoint] validates a POSIX root; the install fix in [preflight][preflight] offers Linux x86_64. [`gpu_environment`][gpu-environment] refuses an existing destination and only probes torch versions/CUDA availability. A [Windows recipe][windows-recipe] therefore does not establish an install, restart or recovery route.

The existing Linux `install_engine` is explicitly model-free, takes an installation lock, settles owned engine custody and journals stages. Its environment step re-probes verified state and invalidates completion before reset. A managed pointer is not enough: [`targets._managed_record`][targets] validates the actual receipt. These are valuable primitives. But `require_current_receipt` binds recipe/models-lock/steps/source identity, while repair can reset the same environment; this is not a retained last-known-good upgrade. Historical [#579](https://github.com/banodoco/astrid-dev/issues/579) and [#584](https://github.com/banodoco/astrid-dev/issues/584) remain acceptance leads, not automatically open implementations of their original line-level defects.

**Impact.** A half-created Windows root has no safe next step; a release change can strand a previously working environment. Treating fail-closed stale receipts as successful update support hides loss of capability. Taking custody of an unrelated ComfyUI to repair this would violate the supported attachment contract.

**Minimal change / owner.** P94 ER-0 compares two concrete options: a verified, versioned official Portable artifact behind the existing managed lifecycle, versus completing Windows execution for the existing recipe. Portable is a reasonable candidate, not a proven cheaper implementation. Choose one after measuring extraction, hash/pin, custom-node, native custody and rollback work; do not ship both. Retain the Linux recipe. Do not delete all `gpu_environment.py`, which also supports other pack candidates. Managed Apple Silicon is deferred unless ER-0 establishes a bounded adapter and its proof; compatible existing MPS attachment remains required.

P94 ER-2 owns a consented transaction with one lock, durable action journal, verified stage receipts and an exact installed identity. Interrupted own state is resumable or replaceable under applicable approval; foreign/ambiguous roots refuse. P38 provides native observe/bind/stop/wait semantics for Astrid-owned processes, not new per-installer PID encodings. Busy or unknown ownership refuses update/removal. Old ambiguous records can inform diagnosis but cannot authorize signalling. P09/P29 and P94 jointly stage versioned replacements, retain the old working environment and models, verify before switching the active pointer, and recover after a failed switch. If capacity cannot preserve safe rollback, refuse or require the specifically disclosed alternative; never silently destroy the last working copy. Checkout rollback alone cannot undo arbitrary pip mutations.

**Verification proposed.** Clean and interrupted owned roots, unrelated same-name root, symlink/reparse destination, two concurrent applies, no-op repeat, denied consent, unknown/busy process, crash before/after each durable transition, missing/corrupt receipt, cancelled extraction, and actual old→candidate→rollback environment reuse. Verify project data, model bytes, saved selection, grants/revocations and unrelated processes survive. Native Windows/Linux/Mac proofs cover their consumed process route; a Linux-only helper is not cross-platform proof.

### F7 — BLOCKING — Define actual hardware support by exact software and workload, then prove the advertised cells

**Evidence.** Both current recipe families specify Python 3.12.10 and torch 2.10.0+cu130 / torchvision 0.25.0+cu130 / torchaudio 2.10.0+cu130; Linux uses `manylinux_2_28_x86_64`, Windows `win_amd64` ([Linux recipe][linux-recipe], [Windows recipe][windows-recipe], [official version table][torch-versions], [wheel index][torch-wheels]). CUDA 13 supports Turing through Blackwell, but wheel and workflow kernels still matter. The concrete proposed matrix and vendor limits are in section 4.

The Windows `_TORCH_PROBE` checks availability/version, not a kernel. Existing [`gpu_sanity.py`][gpu-sanity] already runs actual CUDA matrix/linear operations with synchronization and finite-result checks under the engine environment. Reuse its isolation and library evidence; it assumes Linux paths and three dtypes including BF16, so it is not a universal Windows/MPS/Turing admission test. Add/extract a small deterministic known-result baseline and backend adapters, then test the selected workload's operators/dtypes. Do not call all current computation checks absent.

**Impact.** GPU inventory or `torch.cuda.is_available()` can pass while execution fails; an insufficient-memory workflow can wrongly make a valid environment look unsupported. Conversely, SC-94's literal `sm_89` wheel requirement rejects valid Ada binaries: NVIDIA explicitly permits an 8.6 cubin on 8.9 ([Ada guide][ada-guide]). Linux's PyTorch 2.10 build configuration corroborates why no separate 8.9 entry is needed ([build config][torch-build]); that file alone does not establish the Windows wheel's contents.

**Minimal change / owner.** P93/P94 define capability and model-specific support as below. P34/P85/release qualification share the native evidence format, not a new framework or wholesale P34 reopening. Recommend eight lightweight Windows/Linux × RTX-generation compute cells and a smaller set of complete route journeys. This explicitly reconciles SC-93's representative allocation with SC-94's eight full-class witnesses. It covers distinct OS wheel/architecture combinations without eight repeated heavy transfers; it does not claim every card/driver combination is physically tested. Owner acceptance must identify any inference and unavailable witness. Scarce hardware is a scheduling dependency before making the support promise, not a postpublication waiver.

**Verification proposed.** Exact selected device/interpreter, synchronized known-result kernel, required dtype/operator, recorded driver/runtime/wheel identity, CPU-only negative, incompatible CUDA/kernel negative, low-memory workflow refusal and actual image workload. First/warm image and recovery on each distinct supported lifecycle route; one small compute result alone cannot prove workflow readiness or delivery. No automatic driver update/downgrade and no silent CPU fallback recorded as GPU success.

### F8 — BLOCKING — Experimental RunPod retains money, source and cleanup safety obligations

**Evidence, mixed current source and historical witnesses.** Current [`target_selection`][runpod-selection] already binds paid approval to an offer or waiting policy, hourly rate, total cap and deadline; holds account custody and records allocation intent before activation; retains unknown outcomes and cleanup-pending state. [`remote_worker_activation`][remote-activation] later verifies a task-bound process and enables a worker credential. These are different phases. SC-35 is right: moving `claim.json` wholesale into task activation loses pre-activation custody.

Two concrete current seams merit bounded repair. First, [#1861](https://github.com/banodoco/astrid-dev/issues/1861) is explicitly assigned to R16 and [`runpod_setup.install_node_packs`][runpod-setup] still clones into live `custom_nodes`, tolerates fetch failure, force-checks out and invokes pip there. Route existing lock-approved entries through the hardened staged restore/source/HEAD/approval checks and delete that bypass. Second, Runtime [`storage_preflight` and `_claim_task`][runtime-store] impose the free-space floor before task claim without consuming the release operation's [`storage_floor_exempt: true` metadata][runpod-pack]. This is fresh static confirmation of an admission gap, not a live reproduction. [#1648](https://github.com/banodoco/astrid-dev/issues/1648) recorded older valid remote output followed by local-disk failure and blocked normal release; its direct fallback stopped the pod, so it is not evidence of indefinite billing in that incident.

**Impact.** Unreviewed/default-branch code can become loadable after partial setup; local disk pressure can obstruct the action needed to stop spending; erasing the acquisition journal can create duplicate claims. Keeping a poisoned engine without a clear recovery/settlement state can waste time and money.

**Minimal change / owners.** P90/P56 own the staged-node restore replacement. Runtime/RunPod owner provides a trusted, narrow cleanup-admission route or reserved capacity; a caller-controlled “exempt” boolean must not bypass general admission. Preserve the account acquisition journal/locks and explicit handoff to task settlement. P35 documents recovery-state exceptions. Keep valid output/retrieval receipts separate from cleanup status; collection failure must not automatically recompute or rent again.

The P36 prerequisite is only credential resolution at the actual retained-host admission seam: [#1728](https://github.com/banodoco/astrid-dev/issues/1728) reports credentials installed after Runtime startup not reaching that host. Reuse existing scoped resolver/store, reference the correct provider account, fail before spend if unavailable, and keep secrets out of plans and generic state. Do not restart busy Runtime or build a general vault as the workaround.

Resolve [#1450](https://github.com/banodoco/astrid-dev/issues/1450) accurately: capacity polling continued, but a known zero-pod `capacity_retry_ready` claim had no usable continuation/clear operation. Current selection refuses an existing other-invocation journal. Distinguish proven no-create from unknown create; provide reconciliation against the same custody record, never blind journal deletion. [#1446](https://github.com/banodoco/astrid-dev/issues/1446) supplies an older GPU-crash/poisoned-kept-engine recovery case; its CUDA cause and current recurrence are unproved. P38/RunPod should invalidate failed engine health, attempt only policy-approved bounded recovery or settle/release, and preserve diagnostics. No automatic paid retry beyond the already accepted budget/policy.

Historical [#642](https://github.com/banodoco/astrid-dev/issues/642) lock inversion and [#775](https://github.com/banodoco/astrid-dev/issues/775) host-clock/provider-deadline skew remain exact-path adjudication gates for retained public paid routes. This report does not certify either fixed or currently reproduced. Verify the actually pinned lifecycle and all still-reachable claim/release paths; a newer lifecycle main is not evidence of its deployment. Unsafe legacy paths must converge on existing guarded ownership or refuse safely, not remain an undocumented fallback.

**Verification proposed.** No paid fallback from local failure; deny/changed offer/rate/cap; no credential; unknown allocation outcome; host death, cancellation and restart; wrong source/HEAD and failed pip leave no new loadable unapproved tree; low local disk still permits trusted cleanup; deadline/clock skew and lock contention cannot defeat the money bound; valid output survives cleanup failure; same claim resumes without duplicate allocation. Propose controlled native/paid witnesses only after separately authorized budget and teardown, never spend in this scoping run.

### F9 — BLOCKING — Close the real first-result and update journey before publication, with focused native enforcement

**Evidence.** [#1848](https://github.com/banodoco/astrid-dev/issues/1848) records two 768×768 images and a CUDA calculation on an older Windows tuple: RTX 5070 Ti Laptop 12 GB, driver 610.88, Portable 0.46.0, torch 2.14.1+cu130. Its 17.28 GB files were externally staged; built-in transfer/resume was skipped, Desktop was stale, and public editor connection was blocked. It is useful round-zero evidence, not today's recipe or the complete native Astrid route. [#1952](https://github.com/banodoco/astrid-dev/issues/1952), P93 CD-5 and P94 ER-L still allow the promised witness before **or after** release. [#1384](https://github.com/banodoco/astrid-dev/issues/1384) does not establish final-tuple H3 GPU output. The [P88 handover][p88-handover] and [last cited mailbox handoff][p88-mailbox] explicitly defer render-backed work and leave the final 616-clip sweep to the qualifier; they cannot fill a GPU or delivered-result gap.

**Impact.** Source completion, a running Runtime, a task receipt or an `open_url` can coexist with a user who cannot reach the image. Postpublication proof contradicts the R16 dependable-creation promise. The current setup guide still accurately says managed Windows is unavailable; changing only its words would create a false promise.

**Minimal change / owners.** P93 CD-5/P94 ER-L and release qualification make all promised route witnesses prepublication on a matching installed installer/editor/Agent/Runtime/VibeComfy tuple. Reuse P20's one maintained setup skill and P32 run/retrieve path. Require intended workflow/seed/input identity, actual output and its matching project/editor visibility, then warm repeat, cancellation/recovery and update survival. Keep hosted and fully local entry routes, real Pinokio controls, and older-editor mismatch diagnosis in the shared release journey. P10 owns actual launcher behavior; simulating a Pinokio path is insufficient.

P38 supplies native installed host/closure/custody proof on the route actually consumed; do not relax identity to get generation working. [#682](https://github.com/banodoco/astrid-dev/issues/682) is an unverified Windows asynchronous socket-policy hypothesis, not a proved vulnerability. The security owner must exercise real allowed and denied requests in the promised Windows execution mode. If a failure is demonstrated, repair that boundary or explicitly block the affected supported claim. This does not pull the whole P15 sandbox or P13/P83 host refactor into R16.

**Verification proposed.** Section 5's joint acceptance rows, zero improvised downloads/scripts, and P94's two consecutive accepted cold/recovery rounds with first and warm images. Compare against the served release using P85's existing receipts and metrics. Keep R15's active qualifier and P56 WS-L authority; their passing old evidence is carried only when relevant inputs are evidenced unchanged. P31's required-check disagreement with the R17 green programme belongs to INV-06/owner; this report neither imposes an unrelated all-green project nor grants a waiver.

### F10 — FOLLOW-UP — Make existing fail-closed entry refusals actionable within P90

**Evidence.** [#1910](https://github.com/banodoco/astrid-dev/issues/1910) records damaged saved-revision identity raising a bare `ValueError`; current [`entry_approval_directory`][node-approvals] retains the fail-closed path. The issue explicitly says no root-sidecar fallback, installation or publication occurs. SC-90 treats the repair as blocking while issue-first reports classify it more narrowly.

**Impact.** A recoverable corrupt entry can produce a traceback instead of a repair action, but the evidence does not show an unauthorized install or lost work from that refusal.

**Minimal change / owner.** Keep the fail-closed check; P90's typed issue/next-action work should carry a stable `entry_revision_invalid`-style code and re-save/repair instruction through readiness and alignment. Do not auto-trust the root sidecar, delete the entry or rebuild diagnostics. Classify this bounded item FOLLOW-UP here; if a mandatory candidate journey actually hits it, that journey remains blocked until repaired, without reclassifying every possible corrupt input as a new release programme.

**Verification proposed.** Both named callers preserve the error code, do not read weaker approval state, and offer one working repair action; corrected entry is rechecked under its correct identity.

### F11 — NOTE — Coverage improved, but neither horizon completeness nor native qualification follows

**Evidence.** The specified P88 originals and #1952/#1384 were retrieved and read. Direct GitHub issue searches with `per_page=100`, page 1 returned: `GPU no:assignee` 32/32; `ComfyUI no:assignee` 41/41; `RunPod no:assignee` 49/49; `is:closed ComfyUI` 2/2, all scoped to `repo:banodoco/astrid-dev is:issue`, all `incomplete_results:false`. These windows are complete for the returned indexed query, not an enumeration of all issues, reopened history, product repositories, support channels or unlabeled problems. Selected relevant issues were read fully; not every search hit was adjudicated. HOR-01's earlier rate-limit failure remains part of its immutable evidence.

**Impact / minimal change / owner.** AUD-01 should credit these narrow retrieval completions and retain the remaining coverage gaps. The coordinator should carry source drift and proof limits into synthesis, not mark the entire horizon clear. This report reads the current R15 handoff state but does not claim a final R15 qualifier verdict or any installed success. The [P56 Lead DONE][p56-done] closes its backstop with no P56 regression by failing ID; the cited Darwin job still had thirteen baseline failures, so that is not an all-green result. WS-L remains separately owner-run after R.

**Verification proposed.** AUD/SYN trace each consequential accepted finding to one owner/task/evidence row, confirm final source and deployment identities at freeze, and distinguish missing evidence from a failed test. No extra generic tracker or repeated completed investigation is required.

## 3. One contract, clear owners and deliberate reuse

This is a proposed amendment to existing types and tasks, not a second architecture registry. P93, P94 and P90 should agree these fields at their existing review stops before parallel consumer work lands.

| Concept | Minimum meaning | Owner / lifetime |
| --- | --- | --- |
| Resolved placement | Existing frozen P32 value, selection source, explicit override/default, concrete environment association; never re-inferred downstream | P32/P93; durable user choice in P35, request override stays task-local |
| Environment identity | Ownership class, approved root/interpreter/recipe or explicit attached endpoint association; source/installation receipt when managed; an opaque loopback endpoint does not imply local root knowledge | P94 managed receipts; P93 observed attachment; P38 verified process identity where applicable |
| Observation | Capability/workflow scope; pass/fail/unknown/not-applicable; observed reason/evidence; freshness and relevant environment identity | P93 existing envelope, populated by platform adapters; non-authoritative cache |
| Desired-action plan | Stable requirements and exact operations/destinations/source/recipe/target binding; immutable digest; disclosed unknown size/transitive limits | P90, consuming P32 requirements; same compiler for inspection and apply |
| Grant | Applicable actor/source/recipe/operation/ownership scope, explicit consent and revoke semantics; digest equality is not itself permission | P90 policy, P35 durable actor authority; separate paid/user-environment permissions |
| Progress and receipt | Same-plan action IDs, verified completed effects, partials owned by the transaction, error/recovery state, installed facts and publication outcome | Existing local journal/receipt owners; preserve when Runtime is unavailable; do not migrate acquisition custody into a later task phase |

Capability predicates may be partially ordered. A suggested display is “target selected; compatible endpoint observed; required model missing; next action: review this download plan.” It must not announce complete readiness just because selection succeeded. Stable managed installation identity and volatile boot/listener identity are related but different: restarting the same installed environment requires fresh liveness/compute evidence, while replacing it changes the plan's target association. On an explicit endpoint with no trustworthy filesystem identity, limit the operation to what that evidence actually supports.

### Supported ownership paths proposed for R16

| Path | Supported outcome and permitted behavior | Boundary / evidence needed |
| --- | --- | --- |
| Existing Desktop, Portable or Git ComfyUI on Windows/Linux | Read-only discovery, explicit loopback attachment, compatible workflow run/retrieve, scoped approved missing models; later exact additive nodes only under P56 D1/P90 protection | Human starts/updates/repairs their installation. Unknown layout is allowed for attachment, not arbitrary writes. Desktop identity must be independently associated with its responder. |
| Existing compatible Apple Silicon ComfyUI/MPS | Same attachment and real-output contract with MPS-specific compute/workflow limits | Keep macOS support. No automatic managed Darwin installer promise from Linux POSIX code; do not force CPU fallback. |
| Existing external Pinokio ComfyUI | Read-only observation and consented compatible endpoint use | Pinokio/user retains ComfyUI lifecycle. Distinct from Astrid installed inside Pinokio. |
| Astrid managed Linux NVIDIA | Existing model-free recipe lifecycle plus exact environment/workflow plan, verified transfer, resume, warm reuse and safe update | Reuse existing runner/lock/journal/custody. Qualify selected distro/interpreter/wheels and all changed update edges. |
| Astrid managed Windows NVIDIA | One selected Portable or recipe adapter, isolated owned destination, consent, progress/resume, native custody and safe update | Required work to fulfill the proposed no-usable-local-target setup route; not available merely because recipe JSON exists. Owner chooses route at ER-0/D3. |
| Astrid application installed through genuine Pinokio | Actual launcher install/start/stop/update behavior and generation through the same contracts | P10 owns real launcher witnesses on retained OSes; managed-by identity is distinct from the ownership of an attached engine. |
| Experimental RunPod | Explicit separately approved bounded allocation, verified setup, same requirements/run/retrieve and safe settlement | No automatic fallback, no capacity guarantee, no inferred spending permission. Money/custody safety is mandatory despite experimental status. |
| Other existing compatible endpoints | Preserve already working explicit attachment with honest observed capability limits | AMD/Intel/legacy NVIDIA availability does not imply new managed provisioning. No new engine/provider or arbitrary remote endpoint feature is added. |

### Reuse, adapt and delete

| Existing mechanism | Decision and reason |
| --- | --- |
| P20 maintained `astrid/packs/setup/docs/SKILL.md`, existing mirror/distribution and P32 S2 | **Reuse.** One shared public journey; reconcile historical conflicting prose and change commands only when their actual implementations land. |
| P32 `requirements`, frozen Placement, local/remote run and retrieve | **Reuse and repair inspection parity.** Do not reopen the entire plan or reintroduce a controller inventory bridge. |
| P56 readiness envelope, approval records, pinned refs, transactional revision publication | **Reuse.** Extend one envelope and actual producers; preserve F5 entry custody and exact approved source restrictions. |
| Linux engine lock, journal, receipts, `stop_engine_for_converge` | **Reuse through platform adapters.** Separate installed facts from permission and add staged update survival. |
| `gpu_environment` availability probe and `gpu_sanity` computation | **Adapt their relevant parts.** One small backend baseline plus workload-specific proof; avoid blind whole-file deletion or universal BF16 requirement. |
| Attached staging and locked `model_downloader` Range/cache behavior | **Reuse.** Common verified-publication/resume policy can preserve distinct transports. |
| Managed final-path-before-verification; pre-consent hardlink probe | **Replace these unsafe orderings.** Keep their callers on one exact plan/apply contract. |
| Live-clone RunPod custom-node path | **Delete after redirecting callers to existing staged restore.** No parallel hardened installer. |
| P56 stage-2 helper-only/obsolete compatibility projections | **Adapt useful donor code; remove superseded projections.** A helper green in isolation is not a wired user path. |
| Old target TOML preference and entry-local trust overlap | **Converge under P35 with conservative migration.** Keep diagnostics/recovery receipts; no indiscriminate file deletion or resurrection of stale grants. |
| Paid account claim journal versus task activation | **Keep distinct lifecycle responsibilities.** One documented handoff; “one home” does not erase pre-activation or cleanup-pending evidence. |

## 4. Hardware and software qualification proposal

These are candidate qualification combinations, **not completed support claims or driver-install instructions**. Select a maintained vendor/OEM-supported driver for each actual machine; record exact OS build, kernel, driver and wheels. Do not upgrade a working human environment simply to match the managed candidate.

### Driver and wheel constraints

NVIDIA's [CUDA 13.0 release notes][cuda13] and [compatibility guide][cuda-compat] give the CUDA 13.x family floor as R580. CUDA 13.0's corresponding-driver table lists Linux `>=580.65.06` and Windows `N/A`, because its Windows driver is not bundled. The [separate R580 notes][r580] pair Linux 580.65.06 and Windows 580.88 with CUDA 13.x. I therefore propose Linux `>=580.65.06` and Windows `>=580.88` as conservative **selection bounds for qualification**, with the actual maintained card-specific driver recorded. Windows 580.88 is not a numeric minimum supplied by the toolkit table, and a compatible driver alone proves neither PTX nor custom-node support.

Use the current recipe family first: CPython 3.12.10, torch 2.10.0+cu130, torchvision 0.25.0+cu130, torchaudio 2.10.0+cu130, pinned ComfyUI `6bfaacc67c2103481e5f0c84d75257cd0581d86a` and VibeComfy `55c3948212d23cf037fae8a4c6faad77d33e7279`. Exact wheel URLs/hashes are in the cited recipes; official wheels exist for both target OSes. The proposed Linux witness is Ubuntu 24.04 x86_64; it is a bounded selected distro, not every Linux system. A Portable decision changes this identity: freeze its actual Python/torch/ComfyUI artifact and hashes, and qualify that instead of borrowing the recipe or #1848's result.

| GPU family | Representative physical card / memory variant | Compute capability | Windows compute cell | Linux compute cell | Required qualification distinction |
| --- | --- | --- | --- | --- | --- |
| RTX 20 / Turing | RTX 2060, **6 GB** | 7.5 | Windows 11 x64, selected maintained driver at/above proposed 580.88 bound, exact chosen cu130 environment | Ubuntu 24.04 x86_64, selected maintained driver at/above proposed 580.65.06 bound, exact Linux cu130 recipe | Small workflow and low-memory boundary; do not require native BF16 for every entry |
| RTX 30 / Ampere | RTX 3060, **12 GB** | 8.6 | Same family; record exact tuple | Same family; record exact tuple | Typical medium-memory workflow witness |
| RTX 40 / Ada | RTX 4060 Ti, **8 GB** | 8.9 | Same family | Same family | Compatible 8.6 cubin is valid; actual workload kernels and memory still checked |
| RTX 50 / Blackwell | Desktop RTX 5070 Ti, **16 GB** | 12.0 | Same family | Same family | Require compatible Blackwell kernel; older incompatible wheel is a negative fixture |

Card capabilities and memory variants are grounded in [NVIDIA's capability table][nvidia-gpus] and [reference comparison][nvidia-cards]. A 2060/3060 model name alone does not identify memory variant. The 5070 Ti **Laptop 12 GB** in #1848 is a different device from the desktop 16 GB candidate; it can be an additional available Windows journey witness, with its own tuple. Dual boot can cover the two OS cells on one physical card. The eight cells prove eight recorded combinations, with any wider family claim explicitly an inference.

Each lightweight cell records total/free device memory, architecture, driver, torch/CUDA versions and artifact identities, selected interpreter/device and isolation, deterministic allocation/computation with checked result and synchronization, then the selected workflow's required operator/dtype checks. Kernel compatibility is a relation, not an exact `get_arch_list()` string match. Model disk size is not peak VRAM. Workflow readiness includes entry/model identity, resolution, dtype, quantization/offload assumptions and measured/qualified memory boundary. A 6–8 GB GPU can be computationally valid while a large model is unsuitable; choose a documented small supported workflow or report that workflow unqualified.

### Apple Silicon and unsupported cases

Propose an existing native-arm64 ComfyUI on Apple Silicon with **16 GB unified memory and macOS 15 or later** as a representative witness, recording actual Python/torch/ComfyUI/custom-node versions. This is a witness choice, not a published minimum or every-model guarantee. Version-specific requirements differ: [Comfy Desktop documentation][comfy-desktop] states Apple Silicon/macOS 13+, while [PyTorch 2.10 MPS notes][mps210] show an older 12.3+ example and [2.15 MPS notes][mps215] state 15.0+. An installer floor cannot establish a selected wheel's workflow compatibility. Require actual MPS computation and compatible image delivery; record any CPU-only operators/fallback honestly.

Truthful refusals include incompatible driver/wheel/custom kernel, pre-Turing hardware for the proposed cu130 managed lane, insufficient workflow memory, absent compatible MPS, unsupported managed OS/CPU architecture, no safe destination or unverifiable ownership. Preserve a working older user-owned environment when it remains compatible with its requested workflow; do not silently upgrade it into the managed lane. Windows ARM, Linux ARM, general managed AMD/Intel, automatic Darwin provisioning, new engine kinds and generalized remote ComfyUI are not established by this investigation. Unknown is neither a support promise nor evidence that the user's hardware is broken.

## 5. Proposed acceptance and proof allocation

Use one joint witness record in the owning plans' existing evidence: exact installed tuple and launcher, manifest/bootstrap/engine receipt identities, OS/device/driver/interpreter, requested workflow/input, relevant grant/action digest, real command and inner exit, bytes/time/progress, final output identity, matching editor observation, teardown and limitations. Redact local private paths and secrets. P85 supplies existing measurement machinery; P34 supplies real-GPU format. No new qualification framework is needed.

| Acceptance row | Required positive and negative evidence | Owner and proof type |
| --- | --- | --- |
| Placement and readiness contract | Actual inspection/plan/apply/run agree; explicit/default/env conflicts; stale/unknown never becomes ready | P93/P32/P35; focused CPU contract cases plus native stale-responder witness |
| Existing Windows Desktop | Running reuse; human opens closed instance; stale registration and another server on old port diagnosed; unrelated queued work preserved; first/warm result in matching editor | P93 CD-5; actual native Desktop, not only Portable |
| Existing Linux and Pinokio/Git/Portable regression | Compatible selected endpoint works; partial discovery exposed; no lifecycle takeover; intended folder/entry and result | P93 with P10 for genuine launcher; native route evidence, reuse hardware |
| Existing Apple Silicon | Selected native MPS computes and requested compatible workflow produces visible output; unsupported/custom-node/CPU fallback classified | P93/P94/P34; actual Mac |
| Managed Windows and Linux | Chosen adapter's clean install; real built-in transfer; first/warm image; explicit no-target/no-consent branches; no paid fallback | P94 ER-2/3/4/5/ER-L; native Windows/Linux |
| Plan and grant drift | Changed workflow, root, interpreter, source, recipe, responder or pin; denial/conflicting approval/revocation all refuse before privileged writes | P90/P35; CPU fault cases and target-side enforcement witness |
| Capacity and download | Per-volume peak and staging; initially low disk writes nothing; midstream ENOSPC and no-bytes stall; hash mismatch not final; unchanged resume reuses verified bytes | P94/P90; CPU policy plus actual Windows/Linux transfer/cancel |
| Interrupted environment and repeat | Interrupted own extraction/install/publication; two applies; saved progress; no half-installed admission; valid same-plan repeat/no-op; no unrelated deletion | P94; fault injection plus native interruption/restart |
| Wrong CUDA and workload memory | Inventory available but kernel fails; wrong wheel/extension; selected-device computation; oversized model refusal distinct from unsupported GPU | P94; eight lightweight physical cells, representative real small/large workflow boundaries |
| Update and rollback | Working prior environment/model cache, choice and trust/revoke state survive real candidate update and reversal; busy/unknown process refusal; failed switch retains recoverable old state | P09/P29/P35/P38/P94, shared with INV-01/04; native lived-in journey |
| Execution enforcement/custody | Actual allowed task and denied Windows async network request; exact owned process stops/cancels; wrong/reused/unverified process untouched; correct installed closure | P38 and security owner; native OS behavior, not CPU mock certification |
| Experimental paid path | No spend before separate grant; same acquisition after uncertain outcome; no duplicate allocation; bounded deadline/skew/host-death cleanup; low disk release and preserved existing output | RunPod/Runtime/P35/P36/P38/P90; static/CPU first, explicitly authorized controlled live proof with teardown |
| Delivery and old-editor mismatch | Real intended output/job links to correct project/gallery/editor; honest mismatch guidance; fully local and hosted connection route; first/warm result plus update | P20 donor behavior, P93/P94/P10 and release qualifier |

Run comprehensive install/download/recovery sequences on the distinct OS/lifecycle routes; do not repeat every large transfer on all eight GPU cells. Conversely, a clean Windows recipe witness cannot replace real Desktop discovery, and a fake Pinokio layout cannot replace its Stop/Quit controls. P94's two consecutive accepted cold/recovery rounds remain; independent native cases can be shared with P93/P10 rather than rerun under different plan names. If the same tuple/input is unchanged, carry its evidence forward; if a pin, adapter, grant or delivery path changes, recheck the affected proof.

The source's #1952 limits (40 GB free space, 25 GB download, three hours, no spend) are **proposals**, not permission to use the owner's machine. Its no-build status and before/after-release wording must be amended by its authorized owner before execution. Historical #1384's paid cap also does not authorize this work. No native machine or paid budget was used in this investigation.

## 6. Concrete amendments to existing plans and dependencies

The coordinator should materialise these changes in existing plan/inputs/tasks and the release's existing brief/run board, then submit the actual diff to independent review. These are recommendations, not edits made by this session. Source task IDs are preserved; no historical completed task is silently reopened or relabelled.

### P93/P94 and shared owners

| Existing record / task | Disposition and precise amendment | Start, landing or proof dependency |
| --- | --- | --- |
| [P93 CD-0][p93-tasks] | KEEP inventory; capture real Desktop registration/responder states, Mac/existing-layout bounds, discovery completeness and actual inspection/execution selection | Starts with ER-0 and P90 source reconciliation; no wait for full P38 |
| P93 CD-1, RS1 | REWORK ladder into section 3's scoped observations; reuse Placement; preserve wrappers and HC03 meaning; settle target identity and freshness before consumers | CD-0 plus P90/P94/P35/P38 interface contributions; existing RS1 reviews the concrete shared contract |
| P93 CD-2/CD-3 | KEEP outcomes; all-port API checks, truthful denied/incomplete/ambiguous; no automatic launch or fallback; one consented selection/revalidation path | Reviewed contract; specific P35 selection and P38 read-only observation producer when used |
| P93 CD-4/CD-5/R | REWORK final guide integration and prepublication witness; real Desktop plus retained route limits, job→editor identity and unrelated queue preservation | Actual P94/P90 command behavior and consumed P38 integration before final wording/proof |
| [P94 ER-0/ER-1][p94-tasks] | KEEP route decision/inventory; compare one Portable adapter with completed recipe; exact software/support/witness capacity and resettable states; #1848 remains historical round zero | Can start early alongside CD-0; owner D3 decides one route |
| P94 ER-2, RS1 | REWORK install as exact approved transaction, owned-root recovery and staged update survival; reuse lock/journal/receipt/custody | ER-1, P93 RS1, D3; specific P90 plan/grant, P35 store, P38 stop and P09/29 update interfaces before landing; RS1 reviews these write seams together |
| P94 ER-3 | REWORK availability-only probe; static support before minimum-environment download, real selected-device computation after it and before bulk models | Design after common contract; managed native proof requires ER-2; no impossible “compute before Python exists” condition |
| P94 ER-4 | REWORK ownership/order: common plan/apply with P90/P32 F4, verified final publication, peak capacity and bounded cancellation/resume | ER-1 alone is insufficient; accepted plan/grant/destination contract before changes to shared download callers |
| P94 ER-5/ER-L/R | KEEP one skill; wire actual behavior after ER-2/3/4 and P90, remove after-release option, two consecutive accepted rounds and exact update/delivery proof | One final skill writer with P93 CD-4; matched candidate and native witness capacity before acceptance |
| [P35 draft intended work][p35-tasks] | REWORK selection/trust migration as scoped tasks; replace blanket RunPod-lease→activation move and import-once/delete assumptions with custody/recovery exceptions | Trust/selection interface can land independently of the full App state programme; final restoration/rollback proof joins P09/29 |
| [P38 tasks][p38-tasks] P1/RS1, A2, P2r/A1/A3, E1/F1/T1 | KEEP provider/identity/closure work under its owner; supply read-only observation and native owned stop; migrate relevant engine adapters once; expose unknown/busy/stale truthfully | Discovery starts before full provider completion; routes using installed host-only execution wait for its exact-pair proof. C1/C2/R2 broader consolidation remains P38's accepted-scope decision |
| P09/P29/P10/P31/P85 | Consume joint receipts for update/rollback, genuine launcher, frozen tuple/publication and existing measurement | INV-01/04/06 reconcile cross-release gates; environment report does not create a parallel release authority |

### P90 absorbs the actual P56 residual

The [P56 task ledger][p56-tasks] now explicitly marks remaining work Release 16. P90 must replace “after Plan 56” with an exact source/behavior handoff, define its bare `LE-2` dependency as integrated stage-1 consent, and replace WS-4's “as in original card” placeholder with the actual named work. Bare `--consent code` examples need reconciliation with the existing bound-token contract; do not weaken stage-1 refusal while adding `--apply`.

The following donor heads/states were refreshed. All PRs below target the old `release/15/plan-56`, so “merged” alone does not prove inclusion in integrated R15. Root read current Agent `target_schema`/`setup_contract` and VibeComfy `import_as_entry`; helper comparisons corroborate the residual mapping.

| Donor and exact observed head | State / integration distinction | Proposed P90 destination |
| --- | --- | --- |
| [Agent #615](https://github.com/banodoco/astrid-agent/pull/615), `2b0ad83632721b85957c0ecbf0e2cb1afdba0c0c` | Open draft/WIP, not READY-PROOF; current R15 setup contract remains additive/opt-in | WS-9: one closed issue/fix/`who` registry and real producer migration; drop obsolete legacy compatibility projection |
| [Agent #606](https://github.com/banodoco/astrid-agent/pull/606), `5017e00f3dbe211adcf26cc9a0a7ed2845e5ed16` | Merged into plan branch; typed `TargetSchemaResult`/version notices not in current R15 producer | WS-9/UP-1: preserve absent-versus-malformed provenance, target-unreachable and version-drift semantics; remove transitional exceptions after producer convergence |
| [Agent #644](https://github.com/banodoco/astrid-agent/pull/644), `cface034bcdafa738c8126029057ed94c635a0f2`, with [VibeComfy #217](https://github.com/banodoco/VibeComfy/pull/217), `d605e7dcf5692c42c20fb3e7a21d4708a2e90de8` | Open paired drafts; cumulative integration/proof pending | WS-9 before WS-3: one target-schema capture carried through canonical import, typed refusal before publication; preserve independent F5 `before_publish`/revision-v2 custody |
| [Agent #614](https://github.com/banodoco/astrid-agent/pull/614), `d44a5e4a7fa2eb63cbfdf2c6403dc6552a8eee6d` | Open, unwired helper | WS-4 after real WS-9 registry/producer wiring: evidence-only suggestions, explicit import report, original real-path witnesses, manual outcome when unknown |
| [Agent #629](https://github.com/banodoco/astrid-agent/pull/629), `b0418dc1c57ed5ef3415d7a5b9fb6d8656765918` | Open, unwired grouped helper stacked on older #614 | WS-4: grouped human choice, invocation-scoped cache, no runnable install from name-only match; finish real schema/drop-ref path |
| [Agent #607](https://github.com/banodoco/astrid-agent/pull/607), `c58f4e0d56d7f23a5a6955036b26d2e79b802d38` | Open; donor has an actual SDK/saved-entry dry-run caller, unlike the two helpers above | WS-9: target-aware advisory download notice, local-volume measurement and truthful unknown remote capacity; separate notice from admission |
| [VibeComfy #213](https://github.com/banodoco/VibeComfy/pull/213), `f17b6077ce134aed6ba898cd93c4e4f70a0704ae` | Open, staged helper not READY-PIN; canonical persistence/Agent round-trip missing | WS-9/WS-2/WS-3: whole-batch declaration validation, exact hash/positive size, bounded credential-free HTTPS redirects, one canonical writer and round-trip |
| [VibeComfy #200](https://github.com/banodoco/VibeComfy/pull/200), `b343ae941ce2757b3ade023507e7dabb650b6f27`, and [#201](https://github.com/banodoco/VibeComfy/pull/201), `038d3d69625ccb67a0febdb7bfb3b118edd59263` | Merged plan-branch PRs, but relevant explicit-ref retention/resolution primitives **already exist in current R15 VibeComfy** | Reuse current implementation directly for WS-2/9/3 and UP-1; do not replay an older sidecar strategy over F5 transactional publication |

Current-source corroboration: [Agent entries][agent-entries], [Agent setup contract][setup-contract], and [VibeComfy entry publication][vibe-entries]. Preserved donor source is evidence to adapt, not authorization to merge old tips wholesale or reopen a parallel P56 implementation run.

| [P90 task][p90-tasks] | Concrete amendment |
| --- | --- |
| WS-2 → RS1 | Keep existing ordering; consume P32 Placement/requirements and integrated P56 approval/ref structures. Resolve stable target/action binding, P56 LE-13 pinned-tree recipe disclosure, read-only planning and exactness limits. |
| WS-9 | Retain RS1 prerequisite; reconcile the donor registry, schema/import pair and model-declaration producer. Carry plan and observations through error wrappers. One owner for `target_schema` and CLI edits. |
| WS-4 | Add accepted WS-9 producer/registry wiring to current WS-2 dependency; explicitly name #614/#629/manual/ambiguous behavior and real-path proof. |
| WS-3 | Keep WS-9 + integrated LE-2; require F5 publication custody, recipe disclosure, target failures and pin conflicts. Same exact plan + applicable current approval before any target writes; preserve approved additive-only user-environment rule. |
| WS-12 | Keep receipt-first observed hash/size, distinguish first-use trust from publisher verification and repeat-use enforcement. No unrelated content-addressed catalog project. |
| WS-16 | Retain WS-3 + P32 F4 seam; success is both `fetch-models` and `align` using one plan/apply, not just importing a shared fetch helper. Remove F4's whole-P12 prerequisite if current ComfyUI callers can converge without it; name any indispensable narrow interface. |
| TR-1 | Keep WS-3 + P35; add explicit grant/revoke authority, bounds/conflicts, and revocation checks at apply/resume as well as next plan. Resolve stale sidecar/backup behavior under the accepted terminal threat model. |
| UP-1 | Keep WS-3; consume exact retained refs and conflict semantics; join P94/P09/29 environment update/rollback. Approved old source does not by itself authorize overwriting user-owned packages. |
| WS-17 and final proof/skills | Preserve plain next actions and warning limits; absorb P56 LE-11/LE-18b/WS-6b in the same envelope/journey. WS-L stays owner-run or separately approved after R; no paid proof is authorized by this report. |

### P20/P32 donors and avoided expansion

[P20 tasks][p20-tasks] P4.1/P4.2/P4.5/P4.6/P4.6b/P4.10/P4.12 supply existing commands, settings, diagnostics, download and delivery/skill behavior. Consume them; do not restart that run. Absorb open **P4.6b.1** destination validation into P90/P94 with explicit approved extra-model roots. P4.9's CPU walk remains historical evidence; real built-in transfer/image proof joins CD-5/ER-L/P34.

[P32 tasks][p32-tasks] T3/T6d already establish frozen placement and Runtime preferences; S2 supplies guided generation; T4/T5 supply the local/remote path. F4 is the bounded duplicate alignment seam. Do not resurrect old S2 “never download” wording against newer P20 model-download consent, or old blanket attached-no-additions wording against later P56 D1. Preserve source intent and name superseding decisions. No new provider, Wan2GP, general GPU scheduler, package solver, content-identification project, host refactor, second state tracker or broad R17 green programme is necessary for these outcomes.

## 7. Sequence, decisions and final disposition

Three strategies are credible, but they differ in when they expose the dangerous seams:

| Strategy | Benefit | Material problem |
| --- | --- | --- |
| Finish all P35/P38 foundations, then environment work | Reduces late interface movement | Makes unrelated state/provider consolidation a prerequisite to discovery and hides real setup/delivery failures until late |
| Build the entire first-image journey first with local shortcuts | Exposes user friction quickly | Can entrench another selection/consent/download owner and require rework at identity/update integration |
| **Recommended: settle small shared interfaces, run an early integrated journey, then parallel adapters/proof** | Exercises real selection→plan→grant→apply→output while platform and state work continues under explicit owners | Requires concrete shared-file ownership and native witness capacity reserved early |

1. **Start:** coordinator/Lead records exact final R15 handoff plus served comparator and preserved active authority; P93 CD-0, P94 ER-0 and P90 donor reconciliation proceed concurrently. P35 names selection/trust/revoke ownership; P38 names the consumed native identity/stop interface. Decide one Windows route and actual hardware access before promising dates. Do not wait for a fresh paid run to investigate independent local work.
2. **Contract landing:** P93 CD-1/RS1 and P90 WS-2/RS1 agree the existing envelope/Placement/action/grant/destination boundary. P94 contributes capacity/journal semantics. Keep existing review stops and assertion-change authority; this is not a new review-count reset. One writer owns `preflight.py`/envelope, one owns target-schema/CLI integration, and one coordinated writer owns the maintained setup skill/mirrors. Shared-file conflicts are dependencies, not nominally parallel tasks.
3. **Early vertical witness:** on a matched existing local ComfyUI, exercise explicit selection, a deliberately missing small model, read-only plan, denied then granted apply, actual Astrid transfer, real generation and matching editor delivery. It tests interfaces early without waiting for Windows provisioning. Host/custody changes required by this route must be integrated first; the witness is authorized and scheduled separately.
4. **Parallel implementation lanes after interface agreement:** P93 discovery/next-action consumers; P94 chosen Windows adapter and Linux recovery/update; P90 donor wiring/trust/fetch convergence; P38 native producer/closure and P35 migration work. Serialize overlapping fetch/targets/CLI/custody files. RunPod retains its own journal and bounded safety repairs. P09/29/P10 can investigate actual lifecycle routes before all adapters land, but final proof consumes them.
5. **Integration and proof:** Runtime provider/state producer → Agent consumer/vendor pin and required VibeComfy source → App manifest/installer and actual launcher tuple, with test-only pins distinguished from product dependencies. Use early evidence to revise only affected steps. Join staged environment update/rollback, grant migration and first/warm output on the final candidate. Run the eight small compute cells and distinct route journeys with the agreed native resources. Preserve P94's repeated rounds and all relevant negative cases.
6. **Acceptance:** independent review sees the actual amended plan/task diff and exact evidence. All accepted R16 scope ships together; internal milestones do not create partial public releases. INV-06/owner settles required-check/publication policy, INV-01/04 settle shared update/state edges, and INV-07 reconciles remaining R15 work. A missing mandatory native result remains an explicit blocker or supported-boundary decision before acceptance, never an inferred pass or a quiet after-release promise.

The material decisions still needed are **one Windows managed implementation**, the exact qualification matrix and available witnesses, scope/restore semantics of reusable trust and revocation, the safe environment update/rollback policy within measured disk bounds, and disposition/proof of retained paid-path safety. P56 D7's accepted terminal limitation is already a decision; do not reopen it by stealth. Managed Darwin is an explicit feasibility/scope choice, not required to preserve existing macOS attachment. No estimate here implies reserved hardware, CI capacity or the owner's machine/budget.

**Report disposition:** nine BLOCKING findings (F1–F9), one FOLLOW-UP (F10), one NOTE (F11). Retain the product outcomes and existing owners, absorb the bounded residuals, and repair the shared boundaries before accepting the affected scope. This report is ready for evidence intake; it does not mark any implementation task, proof row, issue, release gate or original finding resolved by code.

## Source links

All project/source references below are immutable commits except explicitly live issue/PR handoffs and versioned official vendor documentation. Source excerpts were read; unexecuted proof remains unexecuted.

[dispatch]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/dispatch-v2/INV-02-dispatch.md
[packet]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/dispatch-v2/packets/INV-02.md
[procedure]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/dispatch-v2/README.md
[context]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/dispatch-v2/context.md
[index]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/README.md
[ctx0]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/CTX-00.md
[ctx1]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/CTX-01.md
[scope]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/scope-release.md
[sense]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/sense-check.md
[packet-workstream]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/manager/chatgpt-packet.md
[dispatch-workstream]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/orchestrator/multi-manager-dispatch.md
[sc93]: https://github.com/banodoco/astrid-dev/blob/ace8e01a9455b97971691209682f65f568efcfda/plans/93-comfyui-desktop-and-existing-environments/evidence/release-16-scoping/SC-93.md
[sc94]: https://github.com/banodoco/astrid-dev/blob/81105a08717746d0393ccf3bb126f8c71bbe2471/plans/94-dependable-environment-setup-and-recovery/evidence/release-16-scoping/SC-94.md
[sc90]: https://github.com/banodoco/astrid-dev/blob/1bd93cf70f169e0db52f95ced5b8f9d189865539/plans/90-workflow-setup-exact-plan/evidence/release-16-scoping/SC-90.md
[sc56]: https://github.com/banodoco/astrid-dev/blob/74eb2950b33233b076536f3178b1daaa86f675b1/plans/56-workflow-setup/evidence/release-16-scoping/SC-56.md
[sc35]: https://github.com/banodoco/astrid-dev/blob/44d813650b7e8b3726bd41699e80c182db8f79a1/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35.md
[sc35-correction]: https://github.com/banodoco/astrid-dev/blob/ebe295571bb58028fe72d98c3da2cbe7fd40eaa5/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35-severity-correction-01.md
[sc38]: https://github.com/banodoco/astrid-dev/blob/7687ef518c86998f610ff4cf963e58b0565f38a1/plans/38-one-process-identity/evidence/release-16-scoping/SC-38.md
[iss02]: https://github.com/banodoco/astrid-dev/blob/9e34444b3c9269d42293ab30558561495d678e3b/releases/16/evidence/scoping/ISS-02.md
[iss04]: https://github.com/banodoco/astrid-dev/blob/e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00/releases/16/evidence/scoping/ISS-04.md
[hor01]: https://github.com/banodoco/astrid-dev/blob/736712b914dc2b46e6fd66dad2206d573ecf1510/releases/16/evidence/scoping/HOR-01.md
[manifest]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install-manifest.json
[p20-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/20-zero-to-first-image/tasks.md
[p32-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/32-generation-placement-targets/tasks.md
[p35-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/35-one-home-for-user-state/tasks.md
[p38-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/38-one-process-identity/tasks.md
[p56-inputs]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/56-workflow-setup/inputs.md
[p56-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/56-workflow-setup/tasks.md
[p56-done]: https://github.com/banodoco/astrid-dev/issues/1757#issuecomment-7170439976
[p90-plan]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/90-workflow-setup-exact-plan/plan.md
[p90-inputs]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/90-workflow-setup-exact-plan/inputs.md
[p90-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/90-workflow-setup-exact-plan/tasks.md
[p93-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/93-comfyui-desktop-and-existing-environments/tasks.md
[p94-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/94-dependable-environment-setup-and-recovery/tasks.md
[p88-handover]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/88-timeline-edits-land/evidence/completion-handover.md
[p88-mailbox]: https://github.com/banodoco/astrid-dev/issues/1849#issuecomment-7142352430
[placement]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/placement.py#L128-L193
[listing]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/listing.py#L123-L253
[sdk]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/generation.py
[preflight]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/preflight.py
[local]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/vibecomfy/local.py
[targets]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/targets.py#L277-L318
[setup]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/setup/docs/SKILL.md
[engine-readiness]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/engine_readiness.py
[asset-gaps]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/asset_gaps.py
[asset-alignment]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/asset_alignment.py#L203-L272
[model-downloader]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/model_downloader.py#L513-L692
[node-approvals]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/node_approvals.py
[engine-runner]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/engine_runner.py
[engine-platforms]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/engine_platforms.py
[engine-endpoint]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/engine_local_endpoint.py
[gpu-environment]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/gpu_environment.py
[gpu-sanity]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/runpod/gpu_sanity.py
[windows-recipe]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/vibecomfy/recipe.windows-cu130.json
[linux-recipe]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/runpod/recipe.linux-cu130.json
[runpod-selection]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/runpod/target_selection.py
[runpod-pack]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/runpod/pack.yaml#L920-L940
[agent-entries]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/entries.py#L1310-L1400
[setup-contract]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/setup_contract.py#L1-L80
[runtime-store]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/store.py#L4505-L4584
[runtime-app-state]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/service.py#L5034-L5090
[remote-activation]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/remote_worker_activation.py#L250-L399
[vibe-fetch]: https://github.com/banodoco/VibeComfy/blob/55c3948212d23cf037fae8a4c6faad77d33e7279/vibecomfy/fetch.py#L620-L665
[runpod-setup]: https://github.com/banodoco/VibeComfy/blob/55c3948212d23cf037fae8a4c6faad77d33e7279/vibecomfy/commands/runpod_setup.py#L324-L373
[vibe-entries]: https://github.com/banodoco/VibeComfy/blob/55c3948212d23cf037fae8a4c6faad77d33e7279/vibecomfy/entries.py#L123-L245
[cuda13]: https://docs.nvidia.com/cuda/archive/13.0.0/cuda-toolkit-release-notes/index.html
[cuda-compat]: https://docs.nvidia.com/deploy/cuda-compatibility/latest/minor-version-compatibility.html
[r580]: https://docs.nvidia.com/datacenter/tesla/tesla-release-notes-580-65-06/index.html
[ada-guide]: https://docs.nvidia.com/cuda/ada-compatibility-guide/index.html
[nvidia-gpus]: https://developer.nvidia.com/cuda/gpus
[nvidia-cards]: https://www.nvidia.com/en-us/geforce/graphics-cards/compare/
[torch-versions]: https://pytorch.org/get-started/previous-versions/
[torch-wheels]: https://download.pytorch.org/whl/cu130/torch/
[torch-build]: https://github.com/pytorch/pytorch/blob/v2.10.0/.ci/manywheel/build_cuda.sh#L107-L124
[mps210]: https://docs.pytorch.org/docs/2.10/notes/mps.html
[mps215]: https://docs.pytorch.org/docs/2.15/notes/mps.html
[comfy-desktop]: https://docs.comfy.org/installation/desktop/overview
