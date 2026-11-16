# Release 12 Track B — shared-session handoff

This is a work-in-progress handoff for the next Track B manager, not a release
gate or permission to rent a GPU. The active instructions are
[`releases/12.md`](../../releases/12.md),
[`releases/12/generation.md`](../../releases/12/generation.md),
`skills/astrid-dev-manage/SKILL.md` and the linked P20/P32/P34/P40 task cards.
Read them and recheck live refs. Direct collaboration was used for this shared
session; a new session needs the orchestrator's verified communication path.
The owner asked managers to keep working, check off accepted work, escalate
blockers promptly and give check-ins. Do not treat a waiting role as stopping
other ready work.

## Exact durable state

- **P20 Agent:** `plan20/staging-agent` at
  `e28a509b6bd8c352514d4b4cc14c95628a8302e7` is `P20-AGENT`. R3 round 2/2
  found no blocking integration issue. Receipt and exact-base comparisons
  are on main via [PR #373](https://github.com/banodoco/astrid-dev/pull/373).
  P20 focused proof had 57 passes, one package-data failure reproduced on its
  exact base; two review entry-contract failures also reproduced on base.
  A reviewer machine deadline failure passed both base and candidate reruns;
  the incomplete review run is not a green suite claim. Mirror, README and
  candidate installer quotation checks passed. Verify published quotations
  again after publication, then do P3.5/P3.6.
- **P20 App:** `plan20/staging-app` at
  `ee9e0b9a6995a08c63040e031d049a7a320f7ef1` merges preliminary App candidate
  `bd06aeef5b891616a3174ce17ba8083b2c5eea82` and passed 237 tests in 14
  focused files. This is not `P20-APP`. Merge the exact orchestrator-issued
  `A-FROZEN` App SHA and re-prove P2.3/P2.4/R2 before the final handoff.
- **VibeComfy:** `release12/vibecomfy` is
  `8d065a8fef3dd602d5462e27d8eca088cf4e8262`, ordered no-ff merges of #165
  and #166, 119 focused tests and index check passed. Its two CI workflows
  failed at the same first errors as `main`; downstream checks did not run.
  See merged [PR #371](https://github.com/banodoco/astrid-dev/pull/371).
  VibeComfy CI ownership is not assumed by that record.
- **P40 intermediate:** `plan40/staging-int40` is
  `1b93d2799364612374810b5b38f7ad1ee3eb61a0`, including R1.1–R1.4, Plan 32
  `d28cac190` and fix N `e0d95d7b8`, plus failed-setup persistence proof.
  R1.1 SDK proof: 24 passed; R1.4 CLI/SDK: 80 passed. The full machine file
  on this head had 90 passes and two deadline failures, each passing on base
  and candidate rerun; another warm-reuse selector failed on both base and
  candidate under load but passed in the full candidate run. This is not an
  uninterrupted green proof. Status is on main via PR #374. T9 is incomplete.
- **P32:** `plan32/staging-int32` is
  `d28cac1902328836acce35230517a19c137ecd55`. The isolated preparation clone
  `/workspace/r12-track-b/p32-compose` is unchanged at that SHA. Runtime lock
  donor Agent `ec48555d8298d155390ffbb37d1950c3e80b43a4` has full lock at
  Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`; its lock passed
  `scripts/vendor_lock.py check` against that producer and the staged
  vendored files. Recheck after composition. Existing worker environment uses
  older Runtime `4f5477cb` and VibeComfy `e65f4941` and is not tuple proof.
  Wait for accepted P40-T9, merge P40 first and exact P20-AGENT second, then
  apply B4 pins, run each plan's focused proof, and post B-CANDIDATE. Use
  Runtime donor's entire lock; Vibe `8d065a8f` and ComfyUI `ee71d5c4` apply
  to both relevant Agent pin files. Rebuild/check the matching test environment.
- **P34:** read-only evidence branch `plan34/gpu-validation-2026-11-10` was
  checked at `1874afa21f7ad9b9a5777c55daa0224b797831e4`. Synthetic inputs
  in `validation/gpu/fixtures/plan34-synthetic` match their manifest byte sizes
  and SHA-256 hashes; they are not Matrix footage or GPU proof. H3 excludes
  h3_av, attached and local-managed cells for this release.

## P40 T9: open blockers and review

The first T9 commit `80bbf6904a7d9ed2204ac4f1635091aa964e8895` was reviewed
in the separately authorized focused round and is **not accepted**. A local
provisional merge `95038ea681cc52da428eab2395ab621fe93984d7` is also not
accepted, not pushed, and must not be used as P40-T9 or B5 input. Independent
review reported four blockers: observed changed custody could incorrectly idle;
real slow-drip could exceed the transport deadline and block release drain;
regex-safe synthetic secrets could enter summaries; stored summary round trip
lost node/field facts. Prior bounded advice also identified stale-acquire
replacement identity, wrong/missing cancel ID, and cleanup under outer lock.
Fix verification is follow-up within the consumed focused round, not another
unrelated review round.

The worker committed unfinished correction `4a21520aad8b62d2db35e079647533ce5981e5ab`,
pushed to Agent `handoff/2026-11-10/track-b-t9-wip-4a21520`; its parent is
`80bbf6904a7d9ed2204ac4f1635091aa964e8895`. The isolated checkout
`/workspace/r12-track-b/p40-t9` was clean at transfer. This WIP is not reviewed
or accepted. It needs the remaining repair, exact-head named proof and
independent verification. Check for residual processes before restarting tests.

Critical design advice: preserve original consent, paid expiry and caps.
Failure verification/reset RPCs may use a short-lived child with private IPC,
parent-enforced absolute deadline, kill/reap and fixed errors; the owner and
journal remain in the parent. A killed local caller does not stop a remote reset:
the exact journaled ID must be cancelled/reconciled and unknown state stays
`cleanup_pending`, blocking reuse/replacement. No child metadata or logs may
expose the token. A partial IPC frame can block `recv_bytes` after `poll`, so
watchdog, EOF, oversized and late-success tests are required. HTTPX phase
timeouts and scheduling do not prove exact wall-clock provider deletion.
Trusted diagnostic node IDs must be bounded, canonical and validated against
submitted graph structure; class/field/constraint facts require trusted local
schema/registry allowlists. Never preserve arbitrary message text or secrets.

The worker reported changed-custody tests 2/2, exact lost-reset-ACK cleanup 1/1,
owner journal/listing 1/1, diagnostics 31/31 before later additions, metadata
1/1, malformed IPC 4/4 and failed-owner/settlement 7/7. Earlier
claimed real slow-drip proof was corrected twice due to fixture protocol errors;
the corrected test hit real `/download-chunk` POST, and adviser requested
exact path, entered-request, multiple writes/retries, timeout reason and child
cleanup checks. A combined fake-owner + real localhost dripper/drain test
**failed**: the verifier thread remained alive at the post-timer 3-second join
(`tests/packs/runpod/test_machine.py:410`). Tightened entered-HTTPS assertions
were committed but not rerun. Astra's subsequent cleanup advice is to use a
separate finite cleanup budget, never the expired verification deadline;
unresolved cancellation or unreaped children retain pending custody and block
replacement. The concrete budget and exact implementation remain open. The earlier named
suite on `80bb` was interrupted after 12 passes and a known deadline failure;
it does not qualify a replacement. Keep user-visible behavior and review budgets.

## Sequence and safety

No RunPod API call, census or rental was made in this resumed session. The
historical ledger shows $3.13 spent, not a current balance or account census.
P34 must not rent until reviewed `P40-T9`, the orchestrator's exact diagnostic
candidate/manifest/pins, current account census and budget verification, and
the orchestrator's explicit go. Observe the $25 shared cap, $1 margin and all
cell caps, no unowned pod actions, census before rental/after release, and never
leave paid resources running across pauses. CPU fakes cannot prove GPU output.

B7 waits for frozen A, accepted B5, B4 and resolved TTS diagnosis. B8, B9 and
B10 use exact `FINAL-B7`/`FINAL-TUPLE` inputs; later changes require the
orchestrator's re-freeze protocol and explicit rerun authority. B11 remains
open through publication and plan-specific hosted/completion work. No product
`main` or `int/**` pushes or publication are authorized from this handoff.

## Transfer update

At handoff the T9 worker stopped tests, committed WIP and finished. A process
check found no T9 pytest or spawned observer process. Track A's independent
comparison was subsequently stopped for the move. No Track B test remains in
flight. Local P32/P34 clones, P40 provisional merge and
environments are convenience copies only; pushed branches above are the
transferable source of truth. Diagnose the failing paid-timer/drain test and
apply the finite-budget cleanup advice with the orchestrator, then fix and prove on a new commit.
Merge accepted T9 work with `plan40/staging-int40` by merge commit, repeat
appropriate exact-head proof and review-fix verification, then post `P40-T9`.
Do not reset the focused-review budget.

## Clean-transfer audit

The final read-only remote-ref check confirmed all full SHAs above on GitHub:
Agent `plan20/staging-agent` `e28a509b6bd8c352514d4b4cc14c95628a8302e7`,
`plan32/staging-int32` `d28cac1902328836acce35230517a19c137ecd55`,
`plan40/staging-int40` `1b93d2799364612374810b5b38f7ad1ee3eb61a0`, P40
handoff `cc4ed06f78ae7dac3a90bc402cecdd4fe6841033`, and T9 WIP handoff
`4a21520aad8b62d2db35e079647533ce5981e5ab`; App `plan20/staging-app`
`ee9e0b9a6995a08c63040e031d049a7a320f7ef1`; VibeComfy
`release12/vibecomfy` `8d065a8fef3dd602d5462e27d8eca088cf4e8262`; and
astrid-dev P34 evidence branch `1874afa21f7ad9b9a5777c55daa0224b797831e4`.
The T9 WIP branch contains `80bbf6904a7d9ed2204ac4f1635091aa964e8895` and
`cc4ed06f78ae7dac3a90bc402cecdd4fe6841033` as ancestors. Runtime lock donor
Agent handoff `ec48555d8298d155390ffbb37d1950c3e80b43a4` also exists remotely.

Records PRs [#371](https://github.com/banodoco/astrid-dev/pull/371),
[#373](https://github.com/banodoco/astrid-dev/pull/373) and
[#374](https://github.com/banodoco/astrid-dev/pull/374) are merged at
`71196eb0d1f9c07c44d1755536f8c4da64cde732`,
`fdfe9081fdc960d94b16e8dfb12c5ce00238cb09` and
`f51f4bc62311a4002214370711c1526aa6301f59`, respectively. The final WIP and
failed drain proof are recorded in merged
[PR #378](https://github.com/banodoco/astrid-dev/pull/378), head
`092f08464b83adcea0716f55d9000335f8fa896c`, merged as `d140dac34efca32bcaf3c2f942b834413e3bf674`. Its task row stays unchecked. No relevant product work is
uncommitted or unpushed. The local provisional P40 merge `95038ea681cc52da428eab2395ab621fe93984d7`
is intentionally unpushed and superseded; reconstruct the final merge from
the remote staging and corrected WIP branches. Earlier local Git remote-tracking
refs may be stale, so compare with `git ls-remote` rather than their ahead counts.

Detailed T9 logs such as `/tmp/p40-t9/drain-real.log`, `http-entered*.log`,
`diagnostics-final.log` and `final-named.log` are local-only and will not travel
to another machine. The recorded results above are a handoff transcription;
rerun the exact checks on the replacement candidate and keep fresh logs. No
Track B test, observer process or worker is active. The combined handoffs are published through astrid-dev PR #377; fetch its branch if it has not yet merged.

## Ready-to-send kickoff

> Resume Release 12 Track B from this handoff and the binding release brief.
> Verify current remote refs and review the T9 progress record. Diagnose
> the failed paid-timer/drain test on the pushed T9 WIP, apply Astra's finite
> exact-cleanup guidance, run exact-head CPU proof, and obtain verification of
> the four existing review findings. Continue independent B5/B6 preparation and
> record progress without resetting review budgets. Send blockers and exact
> handoffs to the orchestrator. Coordinate the read-only census and budget check
> with the orchestrator; do not rent until reviewed T9, exact diagnostic inputs,
> current census/budget and explicit orchestrator go are all available. No paid
> resource may be left running on a pause.
