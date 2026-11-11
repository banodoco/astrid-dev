# Inputs — Releases defined and published from astrid-dev

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 8 Nov 2026 the owner asked for releases to be defined and published from astrid-dev, with CI and protection, as a new project that starts after Plan 29 ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)). On 10 Nov 2026 she asked that each release be planned in advance as one living brief that becomes the record. On 11 Nov 2026 she asked for this plan to be brought up to date and made ready to execute, with Codex doing most of the work ([re-planning session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)); that is an instruction to prepare, not acceptance of the scope and not a go to run. Next: the owner answers D1 to D7 below and confirms the scope as the [ten statements](#ten-statements-for-the-owner) describe it.

**Prior art:** the 8 Nov read-only maps of the release number in the App, Agent, Runtime and Pinokio at App `915bfa84d87268038f396dc999dc2095683e5d8a`, and a re-read on 11 Nov 2026 of every file the cards name at astrid-dev `12a54b6d8baa220fbe3d3a48e3a04f48b0511c07`, App `6545f130f559b66d0924fb46fd5c05a64a536de7` and Agent `a105de3a4852cb61b9647dfe2c920118bd29f272`. What exists and is reused is under [What exists today](#what-exists-today); what the code settled is under [Ambiguity pass](#ambiguity-pass).

**Approach:** a release is one file in astrid-dev, `releases/<N>.md`, which turns Final in a pull request the owner approves. The App carries a byte-exact copy of what that record renders, written by one command and accepted only by a required check that re-derives it and verifies the approval. The code that reads, renders and verifies lives in the App, where the last write happens; astrid-dev holds the records and a job that runs the App's checker on a proposed record, as it already does for the vision feed. Nothing in the Agent, Runtime or Pinokio changes. This keeps the 8 Nov source-of-truth decision and replaces its transport (a generated branch and a scheduled job with write access to App `main`), which the re-read showed could be written by anyone with push access ([D2](#owner-decisions), [alternatives](#alternatives)). It takes over Plan 29's UR-8b, UR-8c and UR-8d and replaces UR-8's tuple guard.

**Challenge:** Pending — three independent high-judgment reviews on 8 Nov 2026 shaped the earlier design ([planning session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9); [summary](#earlier-reviews)). The plan skill requires a fresh critique of this re-plan, because it touches a cross-repository contract, release, security and astrid-dev's own workflows. Next: see [Critique](#critique).

**Proof and limits:** see [plan.md](plan.md#completion). The approval can be verified only if the owner approves from an account no agent can act as (D1). The plan does not defend against someone who can change the hosted App's serving code or its deployment.

**Review rounds:** Pending — recommend one review stop of one round after the trust root's contracts (RS1) and at most two rounds on the integrated pipeline (R); none for phase 2 beyond pull-request review. [Why](#review-rounds). Next: the owner confirms the numbers (D7).

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record here the date; the phase covered (recommend phase 1, RL-0 to RL-G); the accountable session, which is the Claude session that hosts Codex and manages the run on route S ([dispatch notes](tasks.md#dispatch-notes)); what it may do without asking (create `int/31-releases-from-astrid-dev` in astrid-dev and the App, open and merge task and progress pull requests into those branches, open and close the throwaway pull requests the hosted proofs name); what still needs the owner's go (anything reaching either `main`, every step of RL-G, O-1 and O-2, and RL-14t's wording); and the advisor session if there is one.

## Owner decisions

Already decided (8 Nov 2026, recorded in [Plan 29's inputs](../29-update-and-release/inputs.md#owner-decisions), decisions 7 and 8):
- **Versions:** `major.minor.patch`, patch by default, minor or major only when the owner declares it. Release 10 is `0.0.10`.
- **Wire ordering:** the integer `release` stays the ordering key.
- **Required:** its own per-release decision with a reason, never implied by kind. Kind changes no behaviour for now.
- **History:** it starts at a legacy record for the release actually live when the work starts.
- **Hosted App deploys** are not releases.
- **Source:** astrid-dev defines each release. This replaced Plan 29 decision 9's "App manifest stays the source".

Decided or settled since:
- **Order** (owner, 11 Nov 2026, recorded as [Plan 48's D6](../48-one-record-model/inputs.md#owner-decisions)): this plan is queued after Plan 48's Phase 2.
- **Protection timing** (8 Nov open decision 3): astrid-dev `main` has required a pull request and the `documentation` and `vision-consumer-contract` checks since 11 Nov 2026, with no approval and no code-owner review (ruleset 27040267, read through the API on 11 Nov). What this plan still needs is owner rows O-1 and O-2, at go-live.

Open, each with a recommendation:

- **D1. Which GitHub account approves a release?** Every pull request in astrid-dev, including #521, is opened and merged by one account, `AstridPseudon`, which agent sessions act as. GitHub does not let an account approve its own pull request, so with one account there is no approval to verify.
  - a. The owner approves from an account that no agent session can act as, and that account is the code owner of the App's installer code. *Recommended.*
  - b. Keep one account. The plan then delivers records, checks and a byte-exact copy, and does not control who publishes.
- **D2. How does a decided release reach the App?**
  - a. One generated pull request per release: `install-copy.mjs write` produces it, the required `install-copy-guard` check proves its bytes equal the approved record, any session merges it. No new credential, no generated branch, no scheduled job. *Recommended.* It gives up "no App pull request per release".
  - b. The 8 Nov design: astrid-dev writes a `release-published` branch and a scheduled App job pushes the copy to `main`. Today anyone with push access can write that branch directly, and a workflow token can be used by any branch's workflow, so this needs a branch ruleset, a write credential for App `main` held as an environment secret that only `main` can use, and a ruleset bypass for it. Two to three more days, and a new credential for the owner to create and keep.
- **D3. How far does protection of App `main` go?**
  - a. Require the guard, and require code-owner review for `/.github/` and `/scripts/installer/` in the App. The owner then approves App changes to workflows and installer code from the approving account. *Recommended:* without it an agent can change the guard, or the list of approvers, in an ordinary pull request.
  - b. Require the guard only. That stops mistakes, races and hand edits, not a deliberate change to the guard.
- **D4. Who may approve a release** (8 Nov open decision 2): only the owner, or any maintainer she lists as a code owner of the App's installer code. *Recommend* only the owner.
- **D5. Versions for past releases** (8 Nov open decision 4): the live record maps releases 1 to N as `0.0.<n>`, so every install that exists has a version to show. *Recommend* yes.
- **D6. Phasing** (8 Nov open decision 5): phase 1 is the record and the checked copy; phase 2 is versions on screen and the clean-up, about a day and a quarter. *Recommend* these phases. RL-14 could join phase 1 at the cost of a longer final review.
- **D7. Review rounds:** one round at RS1 and at most two at R. *Recommend* these; the 8 Nov recommendation was at most three at the end, with no stop.

The 8 Nov open decision 1 (sync trigger and push identity) is replaced by D2: under D2 a there is no sync job and no push identity.

## Ten statements for the owner

Each is true of the plan as written, under the recommended answers.

1. **Now, a release is whatever the App's manifest says after someone's pull request merges. After, a release is a file in astrid-dev, and the App may only carry a byte-exact copy of it.**
2. **Your go stops being a sentence in a session and becomes one approval on one pull request,** from an account no agent can use. Without that account the plan cannot verify anything (D1).
3. **A Final record nobody approved can sit on `main` and still publish nothing:** the App's check refuses its bytes.
4. **astrid-dev stays as free as today.** No code-owner review arrives there; managers keep editing draft briefs and merging their own progress. Once a record is Final, changing it un-approves it.
5. **You approve more in the App instead:** every change to its workflows and installer code waits for you (D3).
6. **Nobody edits `public/install*` by hand again.** `pin.mjs` stops writing the manifest and `release-guard` is deleted.
7. **There is still one App pull request per release,** written by one command and proven by CI. The generated branch, the scheduled job and the new credential are cut, because anyone who can push to astrid-dev could write that branch, and no robot gets write access to App `main` (D2).
8. **This does not stop someone who can change what astrid.haus serves.** App `main` deploys the page that hands out the installer; the plan protects the installer files and their workflows, not the whole App.
9. **Users see "Astrid 0.0.13", never "Release 13".** The integer stays on the wire and on disk, and no Agent, Runtime or Pinokio code changes.
10. **The first thing published this way changes nothing users install.** The live release is re-published as a record first, as the rehearsal; the first real release through the path is the plan's completion.

Also true, and about the run, not the product: Codex writes about seven tenths of it; the hosting Claude session commits, reviews, does the wording and runs go-live with the owner.

Her reaction to any contested statement is recorded above as a decision before greenlight.

## What exists today

Read at the revisions in **Prior art**.

**astrid-dev, reused as it stands:**
- `releases/TEMPLATE.md` (with the optional `## Included pull requests` section) and `releases/12.md`, a Draft; its row in `strategy.md`.
- The checks `release-documents` and `strategy-consistency`, registered in `scripts/checks.py` and implemented by `check_docs.py:release_errors` and `strategy_errors`. They already enforce every Draft rule the 8 Nov card listed, and one Final rule (the payload's eight keys).
- `docs.yml`'s `vision-consumer-contract` job, the precedent for checking astrid-dev content with the App's own code.
- The Release skill's "Take stock of open pull requests" step.
- `plans/releases.md`, a hand-written log with rows for Releases 9 and 10. Release 11 was published without a row. It is closed, not extended.

**App, reused:** `pin.mjs:checkManifest` (Agent lock, schema digest, and since Release 11 the `vibecomfy` and `lifecycle` blocks) and the functions that derive those pins from an Agent commit; `manifest.test.mjs`'s bootstrap-pin and asset-digest cases; `served-manifest.mjs` and its canary workflow; the `Windows installer` workflow. **Deleted:** `release-guard.mjs` and `pin.mjs`'s write mode.

**Agent, read only:** `astrid.installer.tools.validate_manifest`.

**Not built anywhere:** a reader of a Final record's payload, a render, any approval check, `CODEOWNERS` in either repository, an App worker setup script.

## Ambiguity pass

Done on 11 Nov 2026 by reading the code at the revisions above; it replaces the pass the 8 Nov plan deferred to the start. Each line is a choice the cards would otherwise have left to a worker, and what the code or the record settles. The decisions that are really the owner's are D1 to D7.

| Question | Settled by | Answer |
| --- | --- | --- |
| Where does the code that decides what ships live? | Plan 48's D3 gives a bot a bypass on astrid-dev `main`; managers merge there with no approval; the last write is in the App; `vision-consumer-contract` already runs the App's code on astrid-dev content | In the App, under `scripts/installer/`; astrid-dev runs it in a job |
| Does astrid-dev need `CODEOWNERS` or code-owner review? | `releases/12.md` took 24 commits in two days from managers | No; the gate checks the one finalizing pull request instead |
| Do new checks register in `scripts/checks.py`? | The reader is in the App | No new check and no Python; the landed draft checks are untouched |
| Does a Final record need more than the 8 Nov payload? | `pin.mjs:checkManifest` at App `6545f13` refuses a manifest without `vibecomfy` and `lifecycle` | Yes, both blocks |
| Do the added manifest keys break an installed Agent's update? | `tools.py:validate_manifest` at Agent `a105de3`, `6e9c4f9c`, `709492fa` has no closed key set; the update job hashes its own downloaded copy, not the served file | No |
| Do they break the deployed App? | `updateStatus.ts:readManifest`, `localUpdateStatus.ts`, `appBuild.ts` read `release` and `required` and ignore the rest | No, so the shared typed schema is not needed |
| Who are the approvers? | Nothing names them today | The code owners of the App's `/scripts/installer/`, read before the change |
| Does `release-published` carry trust? | astrid-dev's ruleset covers only `main`; every agent session can push other branches | No; whatever reads it must re-derive from `main`, so the branch is cut (D2) |
| Can the workflow token be the App's writer? | A push to any branch runs that branch's workflow with the same token | No (D2 b needs a credential scoped to `main`) |
| Is `source` needed in the manifest? | The guard can find record N on astrid-dev `main` from `release` alone | No; without it a candidate's bytes equal the published bytes |
| How is a candidate qualified once `pin.mjs` stops writing? | The Agent's `journey.yml` reads `public/install*` from the App checkout | `install-copy.mjs write --candidate` writes the same bytes on the candidate branch |
| Where do `runtime`, the digest and the pack pins come from? | `pin.mjs` already computes them from an Agent commit | `pin.mjs --print` |
| Does a required floor persist? | `release-guard.mjs` leaves an unchanged floor in place today | Yes: the render carries the highest floor at or below N |
| How does astrid-dev CI import the Agent's validator? | `tools.py` imports `runtime_protocol`; Agent `ci.yml` installs with `pip install -e '.[dev]'` and `scripts/ci_install_runtime.py` | Those two steps, after ancestry |
| Which Node? | App `.nvmrc` 20.19.4; `validate_manifest` requires Node 20.19.4 in the manifest | 20.19.x for the worker |
| Which App tests assert "Release n"? | `git grep` at App `6545f13` | The seven files in the test inventory |
| What does a release with no version show? | No versions exist in today's manifest | No name at all; wording is RL-14t's |
| Is "pins disagree with included plans" checkable? | No plan file names a commit | No; dropped |
| Do the golden fixtures survive the live record turning Final? | Each overlays a whole `releases/12.md` or `strategy.md` | Only if RL-11 refreshes them; `golden.txt` must not change |
| Can a Codex sub-agent commit? | [Plan 48 run note](../../docs/ledger/2026-11-11-plan48-phase1-run.md) | Assume not; the run's first step tests it |

**Could not be verified from the planning session:** the App's branch rules and the state of App pull request #208 (the session had no API access to the App repository); whether `AstridPseudon` is the owner's own account or a shared one, and which account the owner would approve from; whether `raw.githubusercontent.com` answers inside a Codex sandbox (it answered from the planning session); whether a workflow token from the App can read astrid-dev's pull-request reviews at the rate the guard needs; whether the GitHub Actions app can be listed as a ruleset bypass actor (it no longer matters under D2 a).

## Alternatives

- **Do nothing.** Release 11 was published by two projects racing for one number ([ledger](../../docs/ledger/2026-11-09-two-projects-published-release-11.md)); the release log already misses it; and any session can change what users install by merging to App `main`.
- **Do less: records and the contract check only.** Keep `pin.mjs` and `release-guard`, and add Final records with `release-contract`. About four days. The record and the manifest are then two hand-kept copies with nothing forcing them to agree; rejected for that.
- **Do less: no approval gate (D1 b).** About three days less. Stops races and hand edits; anyone who can merge can still publish.
- **Recommended: record, gate, and a checked copy by pull request (D2 a), with the trusted code in the App.**
- **The same, with the reader and gate as Python in astrid-dev** (this re-plan's first draft). Rejected: astrid-dev would need code-owner review on `main` just as it gains a bypassing bot, the App would run astrid-dev code in its guard, and the checks would have to be registered and kept in step with Plan 48's Phase 2.
- **The 8 Nov design: generated branch and scheduled push (D2 b).** More to build and a new credential; see D2.
- **astrid.haus serves the manifest from astrid-dev at request time.** Rejected on 8 Nov: server code on the install path, installs depend on GitHub, five consumers change.
- **A shared Zod schema for every App reader** (accepted on 8 Nov, cut here): the readers already ignore unknown keys, the trusted scripts must run without installed dependencies, and RL-14 touches the two readers anyway for two fields.
- **Still not built:** signatures, a separate go-check bot, version arithmetic in the App, a second release log.

## Estimates

Per task in [tasks.md](tasks.md#size). Phase 1 is 11 days of agent work (range 9 to 14), phase 2 is 1.25; elapsed time for phase 1 is about six working days on the critical path if the owner's steps are prompt. The total is about what the 8 Nov plan estimated (12.5): the transport got smaller, and the tests-first tasks, the wording tasks and the review stop were added. Owner time: the decisions; creating the approving account; two settings changes; her go in the publishing session for the two `main` merges; one approval, of the live record; and RL-14t's wording.

## Review rounds

- **RS1, one round, after RL-3 and RL-4.** Those two are tests that define what a record is, when it counts as approved, and when the App accepts a copy. RL-5, RL-6 and RL-7 are built to pass them. A hole found at the end would mean rewriting them; a hole found after go-live would have been open to every user. Reviewing the contracts costs half a day before any implementation exists.
- **R, at most two rounds,** on both integrated heads before anything reaches `main`. The run contract's guide gives two or three for release and security work across repositories; two is enough with RS1 in front.
- **Phase 2, none.** RL-14 changes three lines of text behind tests, and RL-14t's wording goes to the owner.

## Critique

Pending — see **Challenge**. Findings, and what was accepted or rejected, are recorded here.

### Earlier reviews

Two reviews on 8 Nov 2026 chose between the App manifest and astrid-dev as the source, and between a generated copy and serving at request time; they cut signatures, a go-check bot, version arithmetic and the markdown log. A third, after Plan 29's lessons, split four tasks into twelve and resized the plan to about 12.5 days. Its findings that still stand: work lands on `int/31` with a go-live task; the fail-closed gate is its own S task; each commit must be an ancestor of its repository's `main`, because GitHub serves fork and pull-request commits through the parent; `CODEOWNERS` covers the publishing code; `release-contract` checks against the App branch the pull request targets; deleting `release-guard` needs an owner row; a worker setup script for the App; phasing. Its findings this re-plan changes: the publishing code and its `CODEOWNERS` are in the App, not astrid-dev; `releases/` is not code-owned; the typed shared schema is cut; the sync job is replaced (D2).

## Source identities

Planning read astrid-dev `12a54b6d8baa220fbe3d3a48e3a04f48b0511c07`, App `6545f130f559b66d0924fb46fd5c05a64a536de7` and Agent `a105de3a4852cb61b9647dfe2c920118bd29f272`, each its `main` on 11 Nov 2026; the served manifest was Release 11 with that Agent commit. These are not the run's bases. When the run starts, cut `int/31-releases-from-astrid-dev` from each `main`, record the two SHAs here, save the served manifest, and record each task's base SHA when it starts. Only the Release skill moves either branch to `main` (RL-G).

## References

- [Plan 48's run note](../../docs/ledger/2026-11-11-plan48-phase1-run.md) and [worker recovery](../../docs/ledger/2026-11-11-plan48-worker-recovery.md): the lessons behind the scopes, test lists and dispatch notes.
- [Release 11's publication race](../../docs/ledger/2026-11-09-two-projects-published-release-11.md).
- [Plan 29's inputs](../29-update-and-release/inputs.md#owner-decisions): decisions 7 to 9 and 14.
