# Plan 95 run board — Otto

The live state of Plan 95's run, rewritten by the orchestrator at each check-in. The plan's [`tasks.md`](tasks.md) stays the record of progress; this board holds the authority, the rulings and the packet queue. Packets are in [packets/](packets/).

## Now (28 Nov 2026)

Read from the mailbox to 22:19 UTC on 27 Nov, Otto `main` at `2ad2550` and `project/95-otto`. An independent sense check on 28 Nov confirmed each fact below against commits.

**The Otto library is built; the Dev migration is stalled at OT-19 part d.** The acting Lead (`p95-acting-lead-codex-1`) has no running packet.

**Done.** On Otto `main`: OT-3 to OT-14, OT-16, OT-17 and OT-18, plus P95-06b, P95-PK and P95-SK. On `project/95-otto`: OT-1, OT-15 and OT-19 parts a, b and c. Otto has no tags and its `__version__` is `"0.0.0"`. [Tasks](tasks.md) holds the card-by-card record.

**Blocked: OT-19 part d** ([P95-19d](packets/P95-19d.md), astrid-dev PR #2054, unmerged). Its own proof is legacy parity (`list`, `check`, `sync`, the unit suite, golden output), and the Lead's run of it was clean. The Lead then also ran Otto's generic `otto check` on the real tree and found two things:

- **Skill configuration mismatch.** Fixed in Otto by P95-SK. Dev has not re-pinned or added its `[skills]` table, and no packet owns that step.
- **Link-anchor findings** (64 at the first strict run; 55 on the Lead's later strict base and candidate scans, SHA-256 `32c4e62c9941b274616d987cc419ebcd4e51d03fabe8656d56cef009b805a83e`). Nine of them are real `<a id=...>` targets in table cells of `plans/39-green-mains/evidence/release-14-record/tasks.md`, which Otto does not recognise.

**The anchor detour.** Packet P95-ANCHOR (Otto PR #20) tried to teach Otto to recognise explicit anchors with a hand-written, fail-closed scanner. Its heads were repeatedly rejected on 27 Nov (including `c8681932`, `7c53cb1` and `19674be`) after each differential run against GitHub's real GFM renderer found another false pass. On 27 Nov the Lead reported that ten expectations at Otto `tests/test_fragment_targets.py:385` disagree with GitHub's renderer, and that a disposable `cmarkgfm` proof rejected the false passes but was verified only on macOS ARM64 with Python 3.11 and breaks the stdlib-only rule ([mailbox 7229223038](https://github.com/banodoco/astrid-dev/issues/1886#issuecomment-7229223038)). Two corrections to how that was first recorded here: the ten expectations are in the packet's own unmerged Otto PR, not in astrid-dev, so they are not the owner-reserved kind of assertion; and the `cmarkgfm` route would need a stdlib-only exception.

**Scope finding.** The anchor target scope is Dev policy under the RS1-reviewed contract (`docs/contract.md`, check-registry table: "Dev mandatory source list, catalog gate and anchor target regex in Dev"; Otto's `target_pattern=None` means all relative Markdown targets), and Otto's `_link_anchors` already takes a `target_pattern`. Requiring Dev to pass a strict full-tree anchor audit comes from advice during the run, not from the plan. Even a perfect P95-ANCHOR leaves the remaining findings, which would need P95-ANCHOR-POLICY, a new ratchet feature outside Otto v0.

### Path (adopted 28 Nov 2026)

Adopted by the owner-delegated rulings in [Authority](#authority). The acting Lead sequences the technical steps. Serial chain 2, 4, 5, 6, 7, 8, 9; step 3 runs beside step 2, and OT-21's slices run beside OT-20.

1. **Rulings, done:** Otto is public (branch protection to be verified); the acting Lead cuts the tag; progress pull requests for Plan 95's records are authorised; Dev's `link-anchors` keeps its legacy target scope and no compiled parser is added.
2. **Lead:** finish 19d's own proof and merge PR #2054, completing OT-19.
3. **One small Otto packet, route N:** an opt-in `link-anchors` target pattern in `otto.toml`, strict by default. Park P95-ANCHOR (PR #20) and P95-ANCHOR-POLICY as post-v0.1 Otto issues.
4. **Dev consumer configuration**, folded into OT-20's first step: re-pin Otto, add `[skills]` and the anchor pattern, re-enable the check and view registrations.
5. **OT-20** (X) and **OT-21** slices a to f (X, at most three at once), the slices integrating once OT-20's pre-overlay skill manifest is captured.
6. **Merge `main` into `project/95-otto`** and re-baseline the parity oracles, with the owner accepting the OT-1 drift.
7. **OT-22.** Add one explicit install of the real `otto-*` and `astrid-dev-*` namespaces into a temporary destination, removing one (Completion 5).
8. **Bump Otto to `0.1.0`, then OT-23:** tag, pin by tag, tell Plan 96's board.
9. **R** (S), then **OT-24** on the owner's go, with a final progress pull request that ticks `tasks.md`.

### Risks the sense check raised

- The record trail has stalled because merges to `main` were treated as unauthorised publication, and live packets are briefed from draft commits that are not on `main`.
- One acting Lead runs every proof locally; proof attempts have already hit disk-space and `TMPDIR` problems.
- If nobody rules on literal OT-1 parity, R will flag it.
- If Otto is still internal, a consumer pinning a `git+https` tag will fail.

## Authority

On 27 November 2026, the owner appointed Codex session `p95-acting-lead-codex-1` acting Lead in place of the unavailable `p71-73-orchestrator` to carry out the existing Plan 95 Lead responsibilities. The owner directed the acting Lead to farm implementation out to ChatGPT packet sessions and seek guidance if work deviates from the agreed completion plan. The owner retains the final go for the merge into astrid-dev `main`; all existing packet-session boundaries remain in force. The handoff is recorded in [mailbox comment 7221454707](https://github.com/banodoco/astrid-dev/issues/1886#issuecomment-7221454707). References below to the orchestrator as Lead apply to the acting Lead during this handoff.

On 28 November 2026 the owner delegated five open rulings to a Claude Code session ("YOU DECIDE THAT"), recorded on the mailbox as [comment 7245203000](https://github.com/banodoco/astrid-dev/issues/1886#issuecomment-7245203000). Each stays within D2 and D3 in [inputs](inputs.md#owner-decisions); none widens the owner-authorized dev-tooling exception.

1. **The path under "Path" in [Now](#now-28-nov-2026) is adopted.** P95-ANCHOR (Otto PR #20) and P95-ANCHOR-POLICY are parked as post-v0.1 Otto issues; stdlib only stays and no compiled parser is added. The acting Lead may correct the ten expectations at Otto `tests/test_fragment_targets.py:385` in its own PR or close it.
2. **Tag authority:** as D3 says, the accountable agent cuts Otto `v0.x` tags after the integrated proof (OT-22) passes, after bumping `__version__` to `0.1.0`. Fixes after R ship as `v0.1.n`.
3. **Progress pull requests to astrid-dev `main` are authorised for Plan 95's own records only** (`plan.md`, `tasks.md`, `run.md`, `evidence/`), through a PR whose required checks pass. Nothing else reaches `main` without the owner's go, and the merge of `project/95-otto` (OT-24) still needs it.
4. **Parity drift:** re-baseline the oracles from like inputs at a recorded `main` SHA in `evidence/parity/`, keeping OT-1's summary as history. Every oracle that changed is recorded with its reason, and R reviews that difference. Other Completion 1 requirements are unchanged.
5. **Otto visibility:** `banodoco/otto` was anonymously readable (public) on 28 November. Its branch protection is unverified: the acting Lead checks and reports.

Not ruled: OT-18's before and after sign-off, and the final go at OT-24, both the owner's own.

On 25 November 2026, in orchestrator session `session_011EzfW1Urc5P4hpm2SvVy5d`, the owner approved Plan 95 to run once Plans 71–73 were on `main`, decided D2 to D5 ([inputs](inputs.md#owner-decisions)), and said the plan should simply run. The owner-authorized dev-tooling exception covers astrid-dev, the public `banodoco/otto` and the private `banodoco/astrid-marketing`, and nothing else: no product repository, no Astrid release, no publication or spend.

- **Orchestrator** (`p71-73-orchestrator`, Claude session `session_011EzfW1Urc5P4hpm2SvVy5d`): the accountable agent. It takes the Lead's part of the [packet workstream](../../agent/roles/leader/lane-orchestrators.md): it writes and orders packets, runs every proof, merges accepted PRs into Otto `main` (Otto cards) or `project/95-otto` (astrid-dev cards), keeps `tasks.md` true through progress PRs, commissions RS1 and R, and cuts Otto `v0.x` tags after the integrated proof passes. Merges into astrid-dev `main` need the owner's go, given when the plan is complete.
- **Manager** (`p95-manager-1`): a ChatGPT session in the owner's account, started by her launch message. It takes the Orchestrator's part of [multi-manager dispatch](../../agent/roles/orchestrator/multi-manager-dispatch.md), with this plan's orchestrator as "the Lead". It may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. It does not edit the repository, merge, approve or dispatch hosted CI.
- **Packet sessions** (`p95-<packet>-<n>`): may push to the `p95/<card id>` branch their packet names (in Otto or in astrid-dev, as the packet says), open pull requests, and comment on the mailbox. They never merge, never edit `tasks.md` or this board, never rebase a shared branch and never take a second packet. Their mode follows the packet's Route: N High, X Extra High, S Pro ([run contract](../../agent/shared/run-contract.md#chatgpt-session-modes)).
- **Stays in the orchestrator's lane:** OT-1, OT-2, OT-22, OT-23, RS1, R and every proof, build, tag and install.
- **Needs the owner:** the merge of `project/95-otto` into astrid-dev `main` (OT-24); installing generated skills on anyone's real machine or session; publishing; anything paid; changing an existing test's assertion in astrid-dev.

## Standing rulings

1. **Functions, not files, conflict.** Different functions or sections in one file are not a conflict between packets; the same function, section or new test table is.
2. **Proof runs where the network is.** Packet sessions write code and tests and end with `READY-PROOF <repo> <PR> <head> <selectors>`; the orchestrator runs the repository's checks and tests on the exact head and posts the result. Otto cards: `python3 -m unittest discover -s tests`. astrid-dev cards: `python3 scripts/astrid_dev.py check` and the full unit suite.
3. **Destinations.** Otto cards: `p95/<card id>` into Otto `main`. astrid-dev cards: `p95/<card id>` into `project/95-otto` (cut from `main`). Merge, never rebase; post BLOCKED if the board lists a different head for an existing draft.
4. **Dependants wait only for the cards they depend on.**
5. **Reviews.** The orchestrator reviews ordinary submissions itself. RS1 (the contract, after OT-4, one round) and R (the end, one round) are read-only **Pro** sessions in normal ChatGPT Chat on the orchestrator's REQUEST (packet [P95-RV](packets/P95-RV.md)); the manager starts a fresh session for each REQUEST. There is no sense check SC (owner, 25 November 2026).
6. **Cap:** at most three packets Running or Review at once (raised from two on 25 November 2026: the critical-path packets P95-04, P95-05 and P95-06 touch disjoint files and repositories). The first packet went alone and proved a session can push to Otto, open a draft PR and comment.
7. **Sessions:** packet sessions run in a normal ChatGPT Chat, not Work. One writer per branch: replace a stopped session only after its branch has been still for 30 minutes.
8. **Plan records:** `plans/95-composable-agentic-workspaces/*.md` change on `main` only through the orchestrator's progress PRs. A packet may add only the evidence file its packet names.
9. **Otto is public:** nothing private goes into it, and no secret is configured in its CI. Plan 96's Marketing data never goes into Otto.
10. **Cadence:** the manager checks in every 20 minutes while a packet is Running or in Review (relay submissions, resume stalled sessions, dispatch Ready packets) and hourly when idle.

## Mailbox

[astrid-dev #1886](https://github.com/banodoco/astrid-dev/issues/1886), run `p95-otto`, format in its first post.

| Role | Mailbox name | Session | Last processed comment |
|---|---|---|---|
| Orchestrator | `p71-73-orchestrator` | `session_011EzfW1Urc5P4hpm2SvVy5d` | — |
| Manager | `p95-manager-1` | named in its first STATUS | — |
| Packet session | `p95-<packet>-<n>` | from the manager's STATUS | — |

## When a session goes quiet

- **A packet session:** the manager resumes it after 3 hours with no commit or STATUS, and replaces it as the [dispatch workstream](../../agent/roles/orchestrator/multi-manager-dispatch.md) says.
- **The manager:** the orchestrator nudges it at 2 hours; at 3 hours it tells the owner, who starts `p95-manager-2` from the launch message below.
- **A READY-PROOF** unanswered for 45 minutes, or a Review for 4 hours: the manager sends the orchestrator a REQUEST and tells the owner.

## Manager startup checks

Post one STATUS with each as passed or failed; dispatch nothing until the orchestrator's DECISION answers it.

1. **Mailbox both ways:** read #1886, post one non-sensitive ACK, see the orchestrator's reply.
2. **Branches:** `banodoco/otto` exists (public, `main` has its first commit) and no `p95/*` branch exists that this board does not list.
3. **GitHub for packet sessions in Otto:** the ChatGPT GitHub connector can push a branch to, and open a draft pull request in, `banodoco/otto` as well as astrid-dev. If it cannot, that is a manual step for the owner, written in the STATUS.
4. **A fresh ChatGPT session** in each mode a Ready packet needs (High, Extra High, Pro) and the hourly reminder; then the 20-minute reminder while packets run.
5. **Capacity:** how many ChatGPT sessions the account can run at once, and whether Extra High and Pro are offered.

## Dispatch queue

Cap: three Running or Review at once (ruling 6). Nothing is running as of 28 Nov. Merged packets are listed once, not repeated per card.

| Packet | Source tasks | State | Route |
|---|---|---|---|
| P95-03 to P95-12, P95-13, P95-14, P95-16, P95-17, P95-18, [P95-06b](packets/P95-06b.md), [P95-PK](packets/P95-PK.md), P95-SK | OT-3 to OT-14, OT-16 to OT-18, and follow-ups | Merged into Otto `main` | N, X or T per [tasks](tasks.md) |
| [P95-15](packets/P95-15.md) | OT-15 | Merged into `project/95-otto` | S |
| [P95-19a](packets/P95-19a.md), [19b](packets/P95-19b.md), [19c](packets/P95-19c.md) | OT-19 | Merged into `project/95-otto` | X |
| [P95-19d](packets/P95-19d.md) | OT-19 | Open (PR #2054), blocked on the anchor decision above | X |
| `P95-ANCHOR` | Otto `link-anchors` fragment targets | Open draft (Otto PR #20), not accepted; parked (ruling 1) | X |
| `P95-ANCHOR-POLICY` | Historical-link ratchet | Draft, not started; parked (ruling 1) | X |
| `P95-20`, `P95-21`, `P95-21a` to `21f` | OT-20, OT-21 | Drafts on `p95/packets-20-21`, not on `main`, not ready | X |
| [P95-RV](packets/P95-RV.md) | RS1 (done), R | On REQUEST only | S |

## Manager launch message

The owner pastes this into the manager's own ChatGPT session.

```text
You are the Manager for the Plan 95 run (Otto, an importable framework for Markdown-first organisations), reporting to the orchestrator (mailbox name p71-73-orchestrator, Claude session session_011EzfW1Urc5P4hpm2SvVy5d).
Follow agent/roles/orchestrator/multi-manager-dispatch.md in banodoco/astrid-dev, taking its Orchestrator's part, with this plan's orchestrator as "the Lead".
Read plans/95-composable-agentic-workspaces/run.md on main, then again at every check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1886, format in its first post. Your mailbox name: p95-manager-1.
First do the Manager startup checks in run.md and post one STATUS with each result; dispatch nothing until the orchestrator's DECISION answers it. Then give each Ready packet a FRESH ChatGPT session (a normal Chat, not Work) in the mode its packet's Route sets (N High, X Extra High, S Pro), with the packet start message in run.md. Dispatch the first packet alone. Check in EVERY 20 MINUTES while any packet is Running or in Review, and hourly when idle: read the mailbox by cursor, check every open packet, start every Ready packet that has no unmet dependency and no conflict with a Running one (up to the cap), resume or replace stalled sessions, pass READY-PROOF submissions to the orchestrator, and post one STATUS an hour.
You may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. You may not merge, edit the repository, dispatch hosted CI or approve anything. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```

## Packet start message

The manager sends this, filled in, as the first message of each fresh packet session.

```text
You are the ChatGPT manager implementing ONE packet for the Plan 95 run (Otto).
Follow agent/roles/manager/chatgpt-packet.md in banodoco/astrid-dev.
Packet: plans/95-composable-agentic-workspaces/packets/<id>.md at <main SHA>; its PR destination names your repository and branches.
Authority: the Authority section of plans/95-composable-agentic-workspaces/run.md at <main SHA>, given by the owner.
Standing rulings: the same file's Standing rulings section; they bind you.
Board: https://github.com/banodoco/astrid-dev/issues/1886, run p95-otto, format in its first post. You are p95-<packet>-<n>;
the Manager is p95-manager-1; the orchestrator, in the Lead's place, is p71-73-orchestrator.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply orchestrator decisions <comment IDs> not yet done.]
Write this packet's code, tests and documents; do not clone, build or run tests. Post STATUS or BLOCKED as comments on the board,
the first as soon as your first branch is pushed and its draft pull request open.
End with READY-PROOF <repo> <PR> <head> <selectors>, then stop.
Do not merge, tick tasks.md or start another packet.
```
