# AUD-01 — independent R16 scope coverage audit (BLOCKED; partial original evidence)

Run: r16-scoping | session: AUD-01-01 | date: 2026-11-25.
Disposition: **BLOCKED — not READY-REPORT, not a completed audit, not approval of R16 scope or publication.** Preserve this partial original, not a substitute for the remaining mandatory review.

## 1. Authority, exact sources and access

[Dispatch](https://github.com/banodoco/astrid-dev/blob/f50817f687c04911dc5edf0152542d3346cd1c62/releases/16/evidence/scoping/dispatch-v2/AUD-01-dispatch.md) at f50817f687c04911dc5edf0152542d3346cd1c62; evidence branch begins at this exact commit. Read packet, context, both CTX source registers, evidence index and the four authorized pinned workstreams (scope-release, sense-check, manager chatgpt-packet, orchestrator multi-manager-dispatch at 7060b764ec16a638b0e6774f814eabf6d7b70c04). Initial [mailbox status](https://github.com/banodoco/astrid-dev/issues/1963#issuecomment-7171409598). The Chat connector supports the read/write evidence route, but I cannot attest actual installed skill contents or the UI reasoning selector. No proposal, product or prior evidence edits, tests, build, clone, CI dispatch, merge, publication, spend or other issue mutation.

**Concrete source-access failures:** the no-cache current served installer manifest at https://astrid.haus/install-manifest.json failed through web access and the shell HTTP attempt (curl 6: Could not resolve host: astrid.haus). This is an environment/access failure, not proof that the public service is down. A repo blob or CTX historical observation cannot replace a fresh served response. The classic branch-protection REST endpoint returned 403 Resource not accessible by integration across astrid-dev, Agent, Runtime and App. The effective branch rules endpoint was rejected by the connector as not allowed (400). Alternative branch metadata and ruleset list/detail were readable; observations below are bounded. Actual deployed installer/bootstrap, complete effective settings, final R15 qualification and live receipts are not established. The dispatch requires a BLOCKED disposition when required source coverage is unavailable. Separately the semantic review of the full original evidence corpus and underlying issue/task/proof census did not finish in this pass. Git blob retrieval is not equivalent to reading and auditing every statement. No completeness claim.

| Role | Observed exact identity (not an installed tuple) |
|---|---|
| Proposal reviewed / report starting base | f50817f687c04911dc5edf0152542d3346cd1c62 |
| Planning main, refreshed | 96747224d38f02a3792bfa3b3af3dce6d7023d34 |
| Earlier planning main used by many reports | 1b9c7085beddc220de4c87e628f4112cb6df33e9 |
| R15 Agent candidate | dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5 |
| R15 Runtime candidate | 686ca695469bda48cd40a70824c4ccef2a137284 |
| R15 App candidate | cc1d48f016fde55ad6b0609c619d8a4bcec56823 |
| VibeComfy candidate | 55c3948212d23cf037fae8a4c6faad77d33e7279 |
| Launcher main | 1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb |
| Lifecycle main (not App manifest pin) | f2948817eeb94af8dee76be21f6d673724f1606e |
| Lifecycle App manifest pin | 9f88ef7640bc664f697112d966ecefa123d44340 |
| Historical CTX-00 served R14 observation, not refreshed | SHA256 8556f2183dfc5575508827ec449c23ea5bbc61792d8e85cfad309dff9d44dee7 |

[Candidate App manifest](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install-manifest.json), blob a6112a518dd34baf3bf66fffc94ad4c05f577f73, actually declares release 15, required.release 15, Agent/Runtime/VibeComfy/lifecycle pins as above, schema digest sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2, uv 0.11.32, Python 3.11.13, Bun 1.3.14, Node 20.19.4 and ffmpeg 7.0.2 with platform artifact hashes. The required reason concerns render/save/update reliability; this is a candidate data field, not a qualification verdict. Previous App observations 7676df48f4104fb8ebe2b19de64dea25b9ec3dc7 and ebfdaa7920695e2b0f908e75aa104c57613bd69b and older Agent b2155fdcc560286d348c1a6a087f79033459208e are not interchangeable with these. Reconcile drift before reusing any receipt.

## 2. Evidence coverage ledger

Exact original commit links/paths in the dispatch and [pinned index](https://github.com/banodoco/astrid-dev/blob/f50817f687c04911dc5edf0152542d3346cd1c62/releases/16/evidence/scoping/README.md). All 28 originals and both correction blobs were retrieved; the first oversized batch exceeded the tool call limit and was recovered in smaller batches. Counts below are line counts from retrieved text, not counts of independently validated findings. The three full originals and two corrections were read in displayed text; SC-10 partially. Remaining original semantic review is incomplete. No original is declared unreadable merely because the output budget prevented full display/review. The index receipt and another investigator's attestation are not my own independent semantic review. In particular INV-04's coverage addendum does not erase HOR's original coverage gap.

| Evidence | Original commit | Blob SHA | Lines | Coverage this session |
|---|---|---|---:|---|
| SC-09 | 52c40028c067047533e222a017c92ac17f8cf5ba | b129483fbd7c8ede8062f0a23800f5be8c66b77b | 226 | full |
| SC-10 | d358b3b9de02c156d8a5576495256d6dea73c577 | 3b1ab93f58f69036ec19763b4e432a19ed446507 | 157 | partial through start of F6 |
| SC-29 | 68849637ddb2fb007289983727bc66e303328580 | 91073d2b8a93ff9c44a03ce77e094d8ab3cb6133 | 112 | retrieved; not fully semantically reviewed |
| SC-30 | 75d69e848eaa0760993e7be3a7c13c5fa7a0f19c | 2be7ebed40abcb6b66a32cee76e0005b8d7b323d | 106 | retrieved; not fully semantically reviewed |
| SC-31 | 25ced2a35b4677532911aaa61127fc9452be59b7 | df0d4c8fab68a86692e3fd30f62dfb12be1a368f | 162 | retrieved; not fully semantically reviewed |
| SC-38 | 7687ef518c86998f610ff4cf963e58b0565f38a1 | 402b1fa7885cbf9ae51cc0f0b5cecba00765be80 | 103 | retrieved; not fully semantically reviewed |
| SC-93 | ace8e01a9455b97971691209682f65f568efcfda | 7b3eb37cd49e0106776970467be9c4e719d2c136 | 127 | retrieved; not fully semantically reviewed |
| SC-94 | 81105a08717746d0393ccf3bb126f8c71bbe2471 | 1767399f0ebfcfc55b18f90146f3db67d05d3909 | 117 | retrieved; not fully semantically reviewed |
| SC-90 | 1bd93cf70f169e0db52f95ced5b8f9d189865539 | 34f5e6e5a88953c3806e9e7fcefe280a85ff9558 | 154 | retrieved; not fully semantically reviewed |
| SC-35 | 44d813650b7e8b3726bd41699e80c182db8f79a1 | e18d1cba6376f5a02fdf62ba3e55717b5d300cf5 | 120 | retrieved; correction reviewed, original not fully reviewed |
| SC-63 | 6cf0dda31179711582a6ed0d8fcf76d3456c4de9 | 24e88f1fd77f92f8470b570ab4cbdc7fc6710e37 | 145 | retrieved; not fully semantically reviewed |
| SC-04 | cbd951924424ecbad213d3ad999a75ade2aabb51 | 6c30a5017ca9ad1c5e8a8c8ceefea69478d38b30 | 59 | retrieved; not fully semantically reviewed |
| SC-79 | ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1 | b5a6b0ceee61552fb12673d418310d2c42bfb217 | 82 | retrieved; not fully semantically reviewed |
| SC-87 | 27212e5767406da192e6e822b2a56e59aa284a13 | 79b49761ce429cb95d823119684d384ad4d5054c | 130 | retrieved; not fully semantically reviewed |
| SC-85 | 799938e9ebcb2d8d97d078a27d448635ed7f7b5c | 3f0415a04b1a5205d67022730fe20a65b05efc3e | 86 | retrieved; not fully semantically reviewed |
| SC-56 | 74eb2950b33233b076536f3178b1daaa86f675b1 | 89ac54c3faba9a508eccb54c7d9057551d34494b | 96 | retrieved; not fully semantically reviewed |
| ISS-01 | 1d8323ccf295f355628d5421701b1b0a0a40a8d0 | 60959365c7fdfca78746dbe0f00ad0a4479aef61 | 55 | full |
| ISS-02 | 9e34444b3c9269d42293ab30558561495d678e3b | 4242fc5b81e3d6b8e1d514bbf27734a8d1aa0bba | 116 | full |
| ISS-03 | 496ab219fff68b2ad85d762ec995da8d78a1d93a | 64f588bb52b05f237c1674034305c14d3ba04a98 | 92 | retrieved; not fully semantically reviewed |
| ISS-04 | e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00 | 154d3b6a1f3d857a4cdd8a0f22e7c2366cf8ef65 | 171 | retrieved; not fully semantically reviewed |
| HOR-01 | 736712b914dc2b46e6fd66dad2206d573ecf1510 | eb8957316c76e1552248ca76dcc67f8a7c850741 | 158 | retrieved; not fully semantically reviewed; original coverage blocker remains |
| INV-01 | 17617b57cc0b4d0485ea68211b84b675f9b6c053 | 9cce6af58063e83f1f3a518e6109fe43bed224c3 | 264 | retrieved; not fully semantically reviewed |
| INV-02 | f73732fbf825241f7be3f6204840e166a5f62c86 | 692517ba245ac2b70cd11f9c83a7e0579869919b | 450 | retrieved; not fully semantically reviewed |
| INV-03 | 5d924e96aee1a2afdaeeb86131f698f5a57a5daf | d5bd845d13805b1985077162b3416296b00e65f0 | 433 | retrieved; not fully semantically reviewed |
| INV-04 | 9e8411372fc9a0257175d0f49da65ba7bee77bbb | 9c63d2e3d4a2e785899a7a571da20c355752f559 | 137 | retrieved; addendum reviewed, original not fully reviewed |
| INV-05 | 22d9be23d3001ca7dabb4b2e90fc38b8b59657bf | 3a973a4e90fa8e3191a31263fe90413b6fd98e01 | 91 | retrieved; not fully semantically reviewed |
| INV-06 | f530e9b60391de8f60f8e38983038cf4615fa7e3 | dd08d1765b04638f194a337788e7ac24fce2ad5f | 143 | retrieved; not fully semantically reviewed |
| INV-07 | ca85e04c05968ad8cb5d4b562e17045283018ce9 | 49619dd01f68d75cb1ff11c50833b356f2b757b8 | 147 | retrieved; not fully semantically reviewed |
| SC-35 correction | ebe295571bb58028fe72d98c3da2cbe7fd40eaa5 | 53a024ba18e09bde3e44c1f7eb0b83a61f77d98e | 18 | full |
| INV-04 addendum | 1e38786e3560d979b246a0ad0526920f4e3aa2ce | a9fe797b794f2ca9314108fb1c5104d39ba322d1 | 78 | full |

## 3. Independent bounded issue search

Search method: GitHub search REST with org:banodoco is:issue and literal phrases, per_page=40, no state filter; raw responses returned total counts and incomplete_results=false for these particular queries. Initial connector search omitted issue state/number; raw REST recovered identities. Results are relevance-based and do not prove absence of differently phrased, unindexed, reopened or unlinked issues. No exhaustive per-repo/date/state or no-assignee census was completed. The coordinator's 32-hit GPU and no-assignee follow-ups do not cure that gap. Positive and negative results:

| Query phrase | Count | Relevant hits / limitations |
|---|---:|---|
| lost edits | 1 | coordination board #796 only |
| partial update | 1 | coordination board #796 only |
| false ready | 10 | #1380, #733, #668, #653, #1920, #651, #645 (closed unrelated), #796, #1757, #1777; mixed leads/boards |
| wrong render | 4 | #771, #851, #1836, #1776; two direct issue-body reads |
| credential | 9 | #1728, #1254, #631, #905, #1849, #1731, #984, #796, #1757 |
| billing | 5 | #642, #641, #628, #775, #811 |
| unconsented spend | 0 | literal phrase only; no safety conclusion |
| orphaned pod | 0 | literal phrase only; no safety conclusion |

Separate repo:banodoco/astrid-dev is:issue queries returned silent overwrite 1, rollback 11, false ready 10, wrong output 9, credential 9, billing 5. Direct body checks: #771, #851, #811, #1254, #642, #641, #775, #1648, #1952, #1384; not all comments read. The P88 mailbox comment linked below was directly read. Other issue IDs below are attributed to the read originals/corrections or index, not silently promoted to independently proven current defects. Deduplicate by repository and issue ID; a board, a symptom, a task, a proof obligation and a historical issue are different objects.

## 4. Preliminary findings and bounded ownership routing

These are unadjudicated proposals. Severity BLOCKING means an R16 gate or an audit-completeness blocker; FOLLOW-UP is conditional or later work, NOTE is evidence/state. Native/installed behavior has not been exercised. Where a task owner is named by plan rather than exact existing row, reconciliation remains outstanding.

### A01 BLOCKING — source completeness and release identity

Evidence: Section 1, CTX-00/01 and the original HOR coverage blocker in the pinned index. Consequence: cannot establish the actual old-to-new supported installed path, final R15 go or exhaustive issue coverage. Owner: coordinator obtains timestamped no-cache response bytes + digest, actual deployment/bootstrap/version mapping and read-only effective settings/qualification receipts. AUD must complete full reads, underlying issue/comment/proof review, coverage searches and per-task disposition against refreshed source; do not move to independent synthesis claiming this audit passed. No test or deployment authorized by this report.

### A02 BLOCKING — one safe publication authority; sequencing and approval gaps

Direct current planning [P31 tasks](https://github.com/banodoco/astrid-dev/blob/96747224d38f02a3792bfa3b3af3dce6d7023d34/plans/31-releases-from-astrid-dev/tasks.md) read at blob 8f4f6ac0a8ad3104e83cf0d5ba0bb1bf80672d49. RL-1a legacy record/import, RL-1b contract/ancestry and checks, RL-1c finalization, RL-2a typed schema, RL-2b bootstrap, RL-2c sync, RL-2d canary, RL-G initial adoption and first new final, RL-3 visible version. RL-3's dependency on RL-G and next record does not by itself deliver visible 0.1.0 at first R16 publication. Legacy mapping of integers to 0.0.n needs owner confirmation and actual served receipt, not invented historical publication facts. A draft/strategy change cannot publish; approval must bind final head and pin contract. Require exact old/new manifest and CLI/UI, rollback, required-floor independent of semantic kind. Avoid two version authorities or a separate product release merely to sequence P31.

Current read-only [astrid-dev ruleset 27040267](https://github.com/banodoco/astrid-dev/rules/27040267) is active for default branch; requires PR, disallows deletion and non-fast-forward, requires checks documentation and vision-consumer-contract, zero approving reviews, no code owner requirement, no stale dismissal. Classic branch metadata for dev shows protected=true but legacy protection disabled. Agent/Runtime/App main branch metadata shows protected=false and exposed ruleset lists empty. This is limited observation, not proof of all effective or org-level controls. O-1/O-2 and future RL-1c approval/stale review controls and swap release-guard -> install-copy-guard with only intended sync bypass are not established by these observations. Do not conflate existing required checks with full green or the proposed P31 rules. Owner must adjudicate full-green requirement vs R17-only larger hardening, not waive checks or shift actual safety defects. P31/P29/P30 own shared update/version surfaces; use P58 single strategy generator and P09 install transaction. Proposed minimum: adopt legacy from verified bytes; pin and review actual contract, arrange RL-3 before first new R16 Final, one integrated publication, canary and rollback at exact tuple. Read full SC-31/INV-06 and verify all P29/P58 current source and task rows before finalizing this proposal.

### A03 BLOCKING — money safety: separate failure modes, one custody owner seam

Direct open issues [#642](https://github.com/banodoco/astrid-dev/issues/642) lock inversion release/expiry, [#641](https://github.com/banodoco/astrid-dev/issues/641) cancellation nonacknowledgement, [#775](https://github.com/banodoco/astrid-dev/issues/775) host clock/cap, [#811](https://github.com/banodoco/astrid-dev/issues/811) queued release; [#1648](https://github.com/banodoco/astrid-dev/issues/1648) historical R15 low disk after durable clip (Agent 8fdf6615/Runtime 53a035ba), regular release blocked but fallback stopped pod. Do not say orphan/spend happened in #1648. Current exact implementation of these issues not independently established. ISS-02 and INV-04 correction add #1446 engine death, #1514 cancel, #1450 capacity timeout and known zero-create vs ambiguous #616, #628/#619/#617/#627/#618 historical watchdog/claim paths. These must not collapse into one generic retry or render fix. #811 queue/batch/relative-deadline feature is not itself required for R16; immediate safe release, exact machine owner and bounded spend are.

Route narrow admission/cleanup/custody to P38 Runtime/Agent plus RunPod pack/lifecycle pin owner; avoid full P36 or remote expansion. Minimal: retain durable exact producer and machine receipts, cleanup reserve with bounded/authorized path rather than blanket low-disk exemption, separate known no-create from unknown outcome, never retry ambiguous paid create, cancellation and independent expiry/cap not dependent on successful host progress or untrusted host clock. Prove separate nonack, lock inversion, clock jump, process kill, low-disk cleanup and exact stopped/expired provider state at pinned tuple with no implicit paid fallback. Issue closure and actual paid/native witness remain unverified.

### A04 BLOCKING — preserve work without rebuilding already-present restore guard

Direct current App [dataProvider.ts L245–270](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L245-L270) requires reviewed revision/publication, checks latest head equality and submits reviewed IDs to Runtime. Blob 72631482b507644edf9779c3d8456cd4eb82a9a4. Thus #1480 older stale-restore report is a negative proof obligation, not evidence that this App guard is absent. Runtime enforcement/TOCTOU and all call sites still need checking. Direct Agent [sync.py L453–483](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/sync.py#L453-L483), blob 047634e7d3d4deea20af52ff394d090a59e86567: default outbox name hashes connection identity, project and timeline; no explicit writer identifier in this scope construction; supports targeted #1402 lead, not proof of actual data loss. Must establish same-actor writer isolation, pending persistence, replay, ack and recovery/retirement proof. P04/P63 own isolation and save correctness, P79 media ingress, P35 keep-list; P29/30 update must preserve pending media (ISS-01 App #252/#255). Avoid a second outbox or duplicate restore guard. Prove parallel writer, stale head restore refusal, dropped/reloaded pending upload, restart and exact preserved ordering at final installed tuple. SC-35 correction marks all five findings blocking (selection, outbox, trust revocation, credential/custody, migration); treat as original's corrected severities, not independent proof of every claim. P89 historical 6.15s median in INV-04 addendum is not final R15; 2s median/none >4s former gate needs explicit owner disposition and comparable receipts, not silent relaxation.

### A05 BLOCKING — true first-use hardware and actual native installer/update

Direct [#1952](https://github.com/banodoco/astrid-dev/issues/1952) has pre/post-publication wording, initial Win11/RTX 5070 Ti witness and no ready build. Scope's supported-path proof needs real before-publication witness, distinguish subsequent broader qualification. [#1384](https://github.com/banodoco/astrid-dev/issues/1384) is prior R14 GPU exception, not current candidate case-C proof. ISS-01/02: #1206 mixed-version direction, #579/#584 engine survival, #1525 defaults, #818/#825 foreign service/autostart, #1611 identity binding, #1729 disk, #1230 Windows old fix, #816 readiness, #1413 timeout, #1848 built-in download skipped in exploratory report, #1952; original SC-09 IU-13/IU-15 migration lock and actual origin proof; SC-10 partial read: historical daemon stop hook failure swallowed, actual deployed native Stop/Quit and paired editor/runtime rollback not established. P09 owns shared transaction, P10 actual native custody witness, P29/30 routes/version, P35 state, P38 process, P93 CD-5/P94 ER-L environment and readiness. No duplicate updater or engine reinstall. Preserve unrelated labels/defaults/tombstones, credentials, receipts, user files and held media; prove no wrong-instance deletion, staged rollback, disk preflight, old/new/reversed direction and actual Stop/Quit. Historical tests and candidate manifest do not qualify installed support.

### A06 BLOCKING — exact workflow setup and trust, not reimplementation of R15 stage 1

ISS-02: #1861 remote clone staged/exact verification, #1928/#1910 typed recovery, #1731/#665 requirement schema, #733/#1380 timeout collapse, #722 existing progress/partial download, #721 reopened TLS/#823, #682 Windows Proactor hypothesis (proof obligation, not demonstrated bypass). P90 WS-2/9/3/TR1/UP1, P35 trust, preserve P56 stage 1; P93 CD-1, P94 consume readiness/transfer. Narrow exact identity/consent/typed refusal, retain real verified download and resume; no duplicated downloader or treating probe timeout as missing dependency. Test no unauthorized setup, revocation, corrupt/partial media, remote clone mismatch and bounded cancellation/unknown failures. This remains attributed to read issue originals/correction; current all-route source proof not complete.

### A07 BLOCKING / FOLLOW-UP — correct output, not blanket expansion of rendering work

Direct open [#771](https://github.com/banodoco/astrid-dev/issues/771) historical R14 range-filmstrip offset mismatch; [#851](https://github.com/banodoco/astrid-dev/issues/851) divergent source_offset meanings, prior P59 decision is nested sequence window origin; historical multi-clip trim incorrect preview/render. Current presence not established. Route P87 correctness/P59 previous owner to verify one canonical mapping and preview/export/filmstrip agreement; add narrowly only if actual supported route remains broken. Broader ripple/editing, nested sequence and performance refactors remain later absent a proven gate. [P88 mailbox comment](https://github.com/banodoco/astrid-dev/issues/1849#issuecomment-7142352430) directly confirms final standard and large-shots 616-clip and sweep delegated to Qualifier rather than verified by orchestrator; 2.6 MB parity unmet routed to P75 backlog; do not claim final pass from P88 COMPLETE. P85 exact comparable evidence and P87 rendering qualification; follow up with actual P88 handover and final R15 verdict. Preserve separation of artifact correctness, performance, and render lifecycle. #1855/#866 receipt mismatch cited by ISS-02; P82/P92 later, narrow actual correctness only.

### A08 FOLLOW-UP — credential readiness and fail-closed capability

Direct open [#1254](https://github.com/banodoco/astrid-dev/issues/1254) historical R13 FAL_KEY undeclared for generation audio; root/current reachability unverified. ISS-01 #1728 retained Runtime missing key. P35/P90 trust and P38 custody with capability owner. Confirm current declaration, truthful non-secret setup/refusal, no implicit fallback or charge; BLOCKING only if in-scope supported capability still cannot recover safely. No broad P36 pull-forward. Resolve severity seam with SC-35 F4 and ISS-02 F09 rather than silently classifying credential custody optional.

## 5. What must happen before an actual audit verdict

* Coordinator supply fresh served manifest bytes/digest and deployment bootstrap/version receipt, full read-only effective branch protections/rules/status and final R15 exact qualification (including delegated P88 sweep and installed route evidence). Preserve historical source labels and re-pin at actual candidate; no claim of outage.
* Finish semantic review of every not-fully-reviewed original in ledger plus complete source/proof reads required by packet; no substitution of summaries or receipts for originals. Finish per-issue canonical ID, state/reopen/duplicate, current source/owner and proof ledger and negative searches including broader horizon/no-assignee/GPU/unlinked, all relevant repos and state/date variants; reconcile actual task rows for every proposed task and issue. The scoped routing here is incomplete and is not a coverage denominator.
* Adjudicate P31 first-version ordering/actual protection and full-green conflict, P89 usable-latency obligation, mandatory paid custody vs future feature and exact trust boundary; ensure narrow owner/routing and no duplication.
* After gaps resolved, independently re-evaluate findings against exact proposal/implementation/served identities; preserve this original and use authorized linked correction or replacement evidence under coordinator direction. Never infer READY from a draft PR or from structural readback. No proposed scope, execution or release acceptance until authorized independent process.

**Final disposition for this original: BLOCKED.** The report is intentionally partial. No proposed scope or product changes, no CI or tests, no merge and no issue mutation beyond the authorized mailbox.
