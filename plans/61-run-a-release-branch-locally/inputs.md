# Inputs — Run a release branch locally

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Partly decided. On 17 November 2026 the owner asked, in the accountable session, for this plan to be set up in astrid-dev and pushed to a plan branch, not run. Later that day she put it into Release 14 and on `main` and asked for it to be taken over and driven to completion ([D1 and D2](#owner-decisions)); she has not signed off the task list as such, and D3 and D4 stay open. The owner then asked whether the tool follows its branch by itself, whether the Agent and Runtime can run from source, and whether the approach makes development convoluted. Two independent reviews followed. Their answers cut this plan to the shortest safe path and moved the rest to [Plan 62](../62-one-manifest-one-stack/plan.md). Next: the owner decides D3 and D4 when the manager asks.

**Prior art:** Traced on 17 November 2026 at the source identities below, and re-read by both reviews.
- *The pin set already exists.* It is the install manifest. `pin.mjs` writes it, the installer reads it (`public/install --manifest`), and the RunPod pack reads an install's copy beside the interpreter (`managed_sources.py:36-43`). No "snapshot" concept means a set of commits in the Agent or Runtime. The branch `p59/runpod-source-mode`, mentioned as prior art, was never pushed.
- *The installer.* `--update` is hidden from `--help` (Agent `astrid/installer/cli.py:528`). With `--update` it installs whatever the manifest names, forward or back, and compares no SHAs (`core.py:238-249`). A failed update rolls back inside the transaction (`core.py:577-606`). After a good update the previous version and its `manifest.json` are kept (`backend.py:2030-2040`). There is no rollback command for this case: `--rollback` only switches back to the retained R0 service (`cli.py:531`). **All of that is read from the code.** In a real run on the isolated stack on 17 November, `--update` failed with "launchd service configuration is malformed", and so did its recovery. A follow-up review traced the cause in Agent `b9d0858f`. It is not autostart off as such: it is the global launchd label ([#818](https://github.com/banodoco/astrid-dev/issues/818)) meeting a fake HOME, filed as [#825](https://github.com/banodoco/astrid-dev/issues/825).
  - Every stop first runs `validate_stop_target` (`backend.py:1203`), which probes the per-user label `haus.astrid.runtime` (`service.py:37`, `:831-833`).
  - On a developer Mac that label is loaded, by the live install.
  - The probe then reads the stack's plist under the fake HOME (`service.py:737-740`). Autostart off never writes one (`service.py:1364-1365`), so the missing file is reported as "malformed" (`service.py:749-750`).
  - On a Mac with no live Astrid loaded, the same update would pass.
  
  The installer's "program gone, workspace present" route (`core.py:768-771`, `backend.py:738-746`) was the next idea for keeping data across a switch. A later review showed it is unreachable. Every installer run except doctor calls `source_checkout_ownership` first (`cli.py:962`). With no `program/current`, that call requires the retained managed source profile's paths to be Git checkout roots, which a managed profile never is (`backend.py:1028-1044`). So `update` across changed pins refuses and prints the rebuild steps (RB-8). The kept-data update waits for [#825](https://github.com/banodoco/astrid-dev/issues/825) and the guard's fix (an issue to file).
- *The first start on a copy.* It fails once with "accepted commit inputs changed during verification", and the second start succeeds. A read-only review found that it is not the data. A pristine snapshot of the live realm reached READY on its first start in scratch, as did 10 of 10 starts there, through a different launch path. A tracer on a later, non-first start of the stack saw one Runtime, 185 "tracer armed" lines, no version change and no raise. The cause is open (RB-9).
- *`workspace attach`.* It attaches a copied realm once the installer's empty selection is removed, and refuses a wrong realm id. That was run on scratch clones of the real copy, and each one started READY afterwards. It is committed in astrid-app `36c3c6f6a` and has not run on the real stack.
- *Adopt.* `workspace adopt --from` refuses a destination that already has a workspace selection (`workspace_adopt.py:248-249`), and the installer always creates one (`core.py:862-864`). Adopt therefore cannot copy a realm into a fresh install ([#817](https://github.com/banodoco/astrid-dev/issues/817)).
- *RunPod notes.* The 17 November handover notes ("RunPod needs an install" and the "snapshot" note) are addressed to this plan's manager, and their "snapshot" is this plan's manifest. Two of their claims are inexact:
  - the client, not the pod, fetches the sources, before the paid lease (`remote_placement.py:782-797`; `generation.py:78-81` runs before `:103`);
  - `--managed-by pinokio` refuses `--update` only without `--root` (`cli.py:148-149`).
  
  Machine preferences and lease journals live per data root (`target_selection.py:301-305`). That is why the realm copy must never include the live `runpod/`.
- *The PATH.* The stack is installed with `--command off`, so the `astrid` on PATH stays the live install. `<root>/program/run-astrid` carries the stack's data root and door (`launcher.py:174-181`, `backend.py:1554-1558`).
- *Routes today.* We counted about ten ways to run a non-release stack, expressing two ideas: *these commits* and *these working trees*. Plan 62 reduces them to one.
- *The tool.* See [the state table](plan.md#sequence-and-readiness).

**Approach:** The shortest safe path. It adds no new command, flag, file format or concept, and only touches files that are already open. One script; the door port from the install; the realm as a snapshot copy (one path); a README that tells the truth; `pin.mjs` never overwriting its input; `update` refusing across changed pins, with the rebuild steps, while the installer cannot move a stack and keep its data; one real run; then the code on its own branch. The realm decision:
- *Disk.* Clones plus a 6.8 MB database cost about 14 MB. The Runtime's own backup of a 2.1 GB realm, followed by adopt's disk gate (copy size plus 4 GiB), would not fit on the development Mac we measured.
- *Two paths.* Adopt refuses a fresh install by construction, so "adopt, else snapshot" would be two paths where the first never wins.
- *Safety.* It is the same either way: the live tree is only read.

Adopt alone would migrate and check the copy. So we add `PRAGMA integrity_check`, and "the Runtime opens the copy and a timeline loads" becomes the acceptance check.

Set aside, with reasons, in Plan 62:
- a root per branch (each switch would stage a full program);
- `behind N` and `rewritten` states, with their fixtures;
- switching by commit or manifest file, and going back;
- local and live work;
- a RunPod check;
- the contributor text;
- review rounds.

**Challenge:** Pending — two independent reviews of the earlier draft ran on 17 November 2026. One looked at the RunPod path. The other weighed the shortest safe path against the long-term path. Their findings are applied here and in Plan 62, and the 18 contradictions they listed are resolved in this text. Two more read-only reviews traced the failed `update` to the stop probe ([#825](https://github.com/banodoco/astrid-dev/issues/825)) and to the retained-profile guard. No advisor has critiqued this rewritten version against the code. Next: one advisor critique before greenlight, because the plan copies user data and changes the installer-tuple writer. The findings that changed the design are listed below.

**Review findings that changed the design**, from the Opus and Fable reviews and the first run:
- Adopt was rejected. It refuses a destination with a workspace, so the realm is a snapshot copy, one path.
- The live `runpod/` is never copied: a copied `claim.json` makes two owners of one pod.
- The stale `instance.lock` and `discovery.json` from the installer's first Runtime blocked the start on the copy. They are cleared while the stack is stopped.
- `ASTRID_ENV_FILE` is no longer passed to the stack, so it gets no live keys.
- The live-untouched proof is by hash and database facts, not size and mtime.
- The remove-`program/` switch is refuted by the retained-profile guard, so `update` refuses across changed pins.
- The realm is attached with `workspace attach`, not a hand edit of the catalog.

**Proof and limits:** One real run against the list in [plan.md](plan.md#completion), with evidence in the [run record](tasks.md#run-record).

Limits:
- macOS only. Linux developers are served by Plan 62's RunPod issue, not by this tool.
- The copy is point-in-time and one-way.
- The Runtime and VibeComfy follow the Agent's pins, not their branch tips.
- timeline-composition is not switched.
- The force-push behaviour is read from the code and not exercised: the tool fetches by branch name and checks out detached, with no pull, merge or ancestry assumption.
- A built stack does not move to new Agent or Runtime commits with its data. `update` refuses and prints the rebuild steps. The installer's `--update` fails beside a live Astrid ([#825](https://github.com/banodoco/astrid-dev/issues/825); Plan 62's V0), and its reinstall over kept data is refused by the retained-profile guard.
- The first start on a copy needs a guarded retry, cause open (RB-9).
- About 10 GB of free disk in practice.
- **Risk:** the same probe guards `astrid-runtime restart` and `up` over a stale owner (`runtime_lifecycle.py:87`, `:102`), and `--uninstall` (`core.py:692`). This is read from the code and has not been run. The tool may have to start and stop the stack's Runtime itself, and it never calls `astrid-runtime restart`, `up` or `down` on the stack until the fix for [#825](https://github.com/banodoco/astrid-dev/issues/825) lands.

**Review rounds:** One round, R, before RB-7 merges the plan branch into `release/14/main` (D3). Landing first and reviewing in Plan 62 would put unreviewed code in the release candidate. Plan 62's rounds then cover Plan 62's changes only. Next: the manager asks the owner (D3) when RB-6 has run, before it starts R.

**Run start:** Pending — the owner has directed that a manager take this plan over and drive it to completion (her words are under D1 and D2), but has not recorded what that manager may do without asking. The stop window for RB-6 and the filing of the drafted issues are hers. Next: when the owner starts a run, record the date, the phase or tasks it covers, the accountable session ([who that is](../../skills/shared/run-contract.md#who-answers-for-a-run)), what it may do without asking, what still needs the owner's go, and the advisor session if there is one.

## Owner decisions

The ids are shared with Plan 62: D1, D3 and D4 ask the same question there, for that plan, and D2 is asked only here. The owner's words are quoted from her messages in the accountable session on 17 November 2026.

- **D1 Which release, and which branch the code lands on.** *Decided, 17 November 2026: Release 14.* Plan 61 joins Release 14: a line in `releases/14.md`, and `release/14/plan-61` cut from `release/14/main` in astrid-app and astrid-dev. Her words: "it should go into its own branch, which will then be merged into the release branch … We should make sure that the kind of project is a good representation of where we're at now in the actual project, so someone can take it over easily, and then just drive it through its completion … make sure it's on main." Options not taken: Release 15, and a fix branch with no plan.
- **D2 Where the tool lands.** *Decided, 17 November 2026: the release route.* The code goes on `release/14/plan-61` in astrid-app and astrid-dev; the plan manager merges each into `release/14/main` after the RB-6 proofs and the review; and it reaches `main` when Release 14 publishes. [astrid-app #283](https://github.com/banodoco/astrid-app/pull/283) is closed and its branch deleted. Plan 59's branch returns the tool's paths in one commit (`4eb6fb350`), so Plan 59 does not land them twice. This replaced her earlier ask for the tool on `main` through #283; the same words as D1 are the decision.
- **D3 Review rounds.** *Pending.* (a) One round before RB-7 merges the plan branch into the release branch (recommended): the tool is then reviewed before it enters the release branch. (b) None here, and Plan 62's final review covers the tool. That review comes after the tool has already landed. The manager asks when RB-6 has run, and before it starts R.
- **D4 A real RunPod proof.** *Pending.* (a) Not in Plan 61 (recommended). Its README states how GPU jobs run from the stack, and the $0 check and one job inside $1 go with Plan 62's V7 and its Agent issue. (b) One owner-approved job of at most $1 from the stack after RB-6. It needs `machines setup` in the stack's data root first. The manager asks after RB-6 has passed, and before this plan is closed. No money is spent until the owner says (b).

## Source identities

Read on 17 November 2026; re-check at dispatch.

| Repository | Ref | SHA | Use |
| --- | --- | --- | --- |
| astrid-dev | `main` | `0670863108f802b0bf6c20d6f09bda071be34533` | base of the planning pull request that brought Plans 61 and 62 to `main` |
| astrid-dev | `release/14/main` | `abafc66e539cb64f679c9083f134e5a288bfd205` | cut point of astrid-dev `release/14/plan-61` |
| astrid-dev | `release/14/plan-61` | cut at `abafc66e539cb64f679c9083f134e5a288bfd205` | the plan branch; [#834](https://github.com/banodoco/astrid-dev/pull/834) merged the contributor section into it. Its head moves; read it with `git ls-remote` |
| astrid-app | `release/14/main` | `0b6ef16152dc3fa11246ccc2007da630c66d1a1a` | base of `release/14/plan-61` |
| astrid-app | `release/14/plan-61` | `cf383fc0e2668fe25c4a24f77c1a0b438a3a9fca` | the tool: cherry-picks `aceeb7d00` (from `1412e9ffc`) and `cf383fc0e` (from `36c3c6f6a`), pushed 17 November; the head moves with later task work |
| astrid-app | `release/14/plan-59` | `4eb6fb350ddced8547dabca69ee825514b4367e2` | head after the one commit that returns the tool's paths to their `release/14/main` state; `158186d85de8397cf1cd37bd0afaeb71c41b49aa`, the preview banner fix, stays on it and is Plan 59's. The old tool commits `1412e9ffc` and `36c3c6f6a` remain in its history |
| astrid-agent | `release/14/plan-59` | `4ca3ba324c29f6e3772bc9a08ea76024c009a377` | branch head; the code reading used `b9d0858` on the same branch, and the RunPod files are byte-identical between the two |
| astrid-runtime | `release/14/plan-59` | `e6106ac0799c84602e3fc19a3aede94e2ffe0aef` | read-only reference |

Integration destination: `release/14/plan-61` in astrid-app and astrid-dev, merged into each `release/14/main` by RB-7. The tool reaches `main` when Release 14 publishes.

## References

- Follow-up: [Plan 62, one manifest, one stack](../62-one-manifest-one-stack/plan.md).
- Installer local sources: astrid-agent [`docs/setup/local-source-install.md`](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/local-source-install.md).
- Release branches and steps: [release skill](../../skills/capabilities/astrid-dev-release/SKILL.md), [ledger entry](../../docs/ledger/2026-11-16-release-branches-per-repository.md), and the [contributor section for this tool](https://github.com/banodoco/astrid-dev/blob/release/14/plan-61/skills/astrid-dev-release/SKILL.md#try-a-release-or-plan-branch-live) on the plan branch, until Release 14 publishes.
- Issues from this work: [#815](https://github.com/banodoco/astrid-dev/issues/815) to [#820](https://github.com/banodoco/astrid-dev/issues/820), [#825](https://github.com/banodoco/astrid-dev/issues/825), two comments on [#739](https://github.com/banodoco/astrid-dev/issues/739), and [#758](https://github.com/banodoco/astrid-dev/issues/758) for running from source.
