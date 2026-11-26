# One manifest, one stack

**Project:** One manifest, one stack

**Goal:** A developer switches one isolated local stack between a branch, a manifest file, committed local work and live checkouts with one verb, goes back with another, and everything that asks which commits run (status, RunPod, a reviewer) reads the same manifest.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.2

**Estimate:** About 6.5 engineering days; V6 (live Agent and Runtime) is about half of it, and V0 (the installer fix for [#825](https://github.com/banodoco/astrid-dev/issues/825)) about half a day.

**Waiting on:** it is queued and in no release brief. It is the follow-up to Plan 61; it needs Plan 61's RB-7, the two installer fixes V0 (#825) and V9 (the retained-profile guard), then D1: the owner decides its release (recommended: Release 15).

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — replaces about ten ways of running a non-release stack with one, so contributors try and develop branch work on a copy of their real work without wrangling installs.

## Status as of 17 November 2026, late evening

**This is the follow-up to [Plan 61](../61-run-a-release-branch-locally/plan.md), and nothing in it has started.** Its Status is `queued`.

**What works today is Plan 61's.** The `release/14/plan-59` stack runs isolated on a copy of the owner's realm, and a browser check passed at `http://127.0.0.1:2400/tools/video-editor?entry=editor`. The tool is on astrid-app `release/14/plan-61` (`cf383fc0e`), Plan 61 of Release 14; it reaches `main` when Release 14 publishes. See [Plan 61's status](../61-run-a-release-branch-locally/plan.md#status-as-of-17-november-2026-late-evening) and its [handover](../61-run-a-release-branch-locally/handover.md) and its [lessons](../61-run-a-release-branch-locally/plan.md#lessons), which apply here too.

**Written already:**
- a first contributor section for Plan 61's commands, in the release skill on astrid-dev `release/14/plan-61` ([#834](https://github.com/banodoco/astrid-dev/pull/834), merged there; it reaches `main` with Release 14). V8 rewrites it for this plan's verbs. The earlier [#832](https://github.com/banodoco/astrid-dev/pull/832) is closed.
- the tool, on astrid-app `release/14/plan-61`. [astrid-app #283](https://github.com/banodoco/astrid-app/pull/283), which proposed it against `main`, is closed.

**What it needs before it can start:**
1. Plan 61's RB-7: its plan branches merged into `release/14/main` (Plan 61's D2: the release route).
2. Two installer fixes in astrid-agent:
   - V0, for [#825](https://github.com/banodoco/astrid-dev/issues/825), the stop probe;
   - V9, for the retained-profile guard, an issue drafted and not yet filed.

   `use` and `back` cannot work without both.
3. D1, its release.

**Not proven:** anything in this plan. `--update` has never passed on a stack beside a live Astrid.

**Who decides.** The owner decides D1 and D3 to D7 ([decisions](inputs.md#owner-decisions)) and whether the drafted issues are filed. The plan manager, once named, runs the tasks.

## Outcome and scope

This is the long-term path after [Plan 61](../61-run-a-release-branch-locally/plan.md), which makes the current tool run once for one branch. Plan 62 makes it the one way.

**The design, in eight lines:**

1. **One noun: the manifest.** It names the exact commit of every component, the App included. A "snapshot" is a manifest, not a new object.
2. **One writer, one reader.** `pin.mjs` writes it; the installer reads it. RunPod reads the same file, from the stack's interpreter.
3. **One place.** A single stack at `~/astrid-release/stack`, not one root per branch. A switch changes what the stack runs; the realm copy and the ports stay.
4. **Four verbs:** `use <branch | manifest file>`, `back`, `status`, `stop`. `update` and `up` disappear: `use` with the same branch is the update.
5. **Switch and revert are the installer's update, and only that.** A switch is `--update --manifest <new>` over the installed program. `back` is the same with the manifest the installer kept in `versions/<previous>/`. Both have two hard prerequisites. First, V0's fix for [#825](https://github.com/banodoco/astrid-dev/issues/825) must be in the Agent of both manifests, because the installer that runs is the one fetched for the target. Second, V9's fix for the retained-profile guard ([to file](../61-run-a-release-branch-locally/tasks.md#issues-to-file)). Without it, an update whose own rollback fails leaves kept data that no reinstall accepts. Before either verb, the tool makes an APFS clone of `data/` (`data.pre-switch`) and runs a schema gate. There is no replace-and-install switch: the guard refuses it, and it runs no migration. To share a stack, send the manifest file.
6. **Three row forms, in the same file:**
   - `sha`: pushed work.
   - `sha` plus `repo`: committed local work. This is the installer field that already exists.
   - `live`: a working tree. The App first, then the Agent and Runtime through the Runtime's source profile.
7. **`status`, one row per component:** its form, its commit, and `up to date` or `moved`. For a live row it says "working tree, N uncommitted files". A stack with any live row says so on its first line. A RunPod line names the manifest the pins come from and any machine the stack holds.
8. **RunPod.** An installed stack already sends its own pins. A stack with `repo` rows needs those commits pushed. A stack with live rows refuses before any spend, until the Agent derives pins from clean, pushed checkouts (V7's issue).

Live rows are the only genuinely second idea: working trees instead of commits. They stay one idea for the developer because they are a row form in the same manifest and the same `use`, not a separate command or environment.

**Reuse versus new concept, judged piece by piece:**

| Piece | Reuse or new | Note |
| --- | --- | --- |
| The manifest as the pin set | reuse | Adds one key, `app`, in V3. It is a field, not a concept. No snapshot file. |
| `pin.mjs` as the one writer | reuse | Learns to read a local checkout (V4); today it reads raw GitHub only. |
| Switching | reuse `--update`; **needs V0 and the guard fix** | In the code, `--update` moves forward or back, compares no SHAs (Agent `astrid/installer/core.py:238-249`), migrates with a backup and rolls a failed update back (`core.py:577-606`). Beside a live Astrid its stop probe fails today ([#825](https://github.com/banodoco/astrid-dev/issues/825), under [#818](https://github.com/banodoco/astrid-dev/issues/818)). Removing `program/` and reinstalling is refused by the retained-profile guard (`backend.py:1028-1044`, via `cli.py:962`), so there is no interim switch. |
| `back` | reuse, new verb; **needs V0 and the guard fix** | `--update` with the kept `versions/<previous>/manifest.json`, after the same clone and schema gate. Data newer than the target's schema refuses. No rollback command exists outside the R0 switch-back (`cli.py:531`). |
| One stack root | new rule, one concept fewer | Replaces per-branch roots, which cost a full program and a realm copy per branch. |
| `use` | new verb, one verb fewer | Replaces `up` and `update`. |
| `sha` + `repo` rows | reuse | The installer archives the committed tree (`tools.py:268-290, 363-391`). |
| App `live` row | reuse | The App launcher already serves Vite from a checkout. |
| Agent and Runtime `live` rows | reuse, new glue | The Runtime source profile and the launcher's `--source-manifest` exist. The tool newly builds the source environment ([#758](https://github.com/banodoco/astrid-dev/issues/758)). |
| The realm copy | reuse Plan 61's | Plan 61 attaches it with the Runtime's `workspace attach`. Upstream [#817](https://github.com/banodoco/astrid-dev/issues/817) (`install --workspace-from`) would delete the step, the installer-record hand edit and the installer's empty realm. |
| Isolation by a fake HOME | reuse | Upstream [#818](https://github.com/banodoco/astrid-dev/issues/818) (a service label per root) would delete it. |
| RunPod pins | reuse | It reads the interpreter's manifest. Pins for live rows are Agent work ([tasks](tasks.md#issues-to-file)). |

**What a developer types:**

```sh
astrid-release use release/14/plan-59      # switch the one stack to a branch; the first use builds it and copies your realm
astrid-release status                      # each component: form, commit, up to date or moved; RunPod line
astrid-release back                        # return to what ran before the last use
astrid-release use ~/m.json                # run a manifest someone sent you, or one pin.mjs wrote with local or live rows
astrid-release stop                        # back to normal; the live install was never changed
```

Running your own work is a manifest: `node scripts/installer/pin.mjs --agent ~/src/astrid-agent --out ~/m.json` writes a `sha` plus `repo` row from that checkout's committed HEAD. `--live agent=~/src/astrid-agent` writes a live row instead. Then `use ~/m.json`. With live rows, `use` restarts only the live components, so a code edit is visible after one `use`.

**Out of scope:**
- Windows and Linux. The realm copy relies on APFS clones. Linux developers get RunPod without an install through V7's Agent issue, not through this tool.
- Copying the realm back to live.
- Switching timeline-composition: it follows the App and Agent commits that vendor it ([#820](https://github.com/banodoco/astrid-dev/issues/820)).
- An automatic follow of a branch.

## Existing work and decision

This plan builds on Plan 61's tool and changes how a stack is named and switched, not how it is installed or isolated. The upstream fixes that would delete tool code rather than add to it are issues, not tasks:
- [#817](https://github.com/banodoco/astrid-dev/issues/817): the hand-placed realm.
- [#818](https://github.com/banodoco/astrid-dev/issues/818): the fake HOME.
- [#815](https://github.com/banodoco/astrid-dev/issues/815): `--update` visible in `--help`.
- [#816](https://github.com/banodoco/astrid-dev/issues/816): one readiness command.
- [#819](https://github.com/banodoco/astrid-dev/issues/819): one data-root input.
- The two comments on [#739](https://github.com/banodoco/astrid-dev/issues/739): which commit has several owners, and the release repository list.
- A public "previous version" rollback would make `back` a pass-through.
- Two prerequisites, not just deletions: [#825](https://github.com/banodoco/astrid-dev/issues/825), the stop probe that mistakes another installation's launchd job for this one's (V0), and the retained-profile guard (V9; [to file](../61-run-a-release-branch-locally/tasks.md#issues-to-file)), which refuses a reinstall over kept data. `use` and `back` wait for both. The other asks only delete tool code.

The evidence and the alternatives are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

It starts after Plan 61's RB-7, once the tool has run once and sits on its own branch. The critical path is V0 → V1 → V3 → V4 → V6 → V8 → R → V10 ([tasks](tasks.md)). V0 and V9 land in astrid-agent first. V1's switching then needs V0's fix in the Agent of every manifest it moves between, and V9's fix on the release line. V2, V5 and V7 run beside the critical path. Nothing spends money: V7's RunPod check costs $0, and a real job is D4's choice. Recording this plan authorizes no implementation.

## Interfaces and handoff

**Consumes:** Plan 61's tool on its own branch; the installer's `--update` and kept versions, once V0 and the guard fix are in; the Runtime source profile; and the RunPod pack's manifest lookup (`managed_sources._installed_manifest_path`).

**Produces:** one stack at `~/astrid-release/stack`. Its `program/versions/<id>/manifest.json` is the whole truth of what runs, the App included. It also produces a manifest file that any developer can `use`, and one contributor section that replaces the older routes (V8).

**How to run it**, once V1 to V8 land (macOS, git, Node meeting the App's `engines`, a live Astrid install for the realm copy). It needs about 14 GB free: Plan 61's ~10 GB plus the previous program version, about 3.6 GB, that `--update` keeps.

```sh
git clone https://github.com/banodoco/astrid-app.git && cd astrid-app
scripts/astrid-release/astrid-release use release/<NN>/plan-<PP>
scripts/astrid-release/astrid-release status
scripts/astrid-release/astrid-release stop
```

The `astrid` on your PATH stays the live install. GPU jobs on the stack run through `~/astrid-release/stack/program/run-astrid`, with the stack's own RunPod setup and claims.

## Completion

On a Mac with a live install, from a fresh clone:
- [ ] `use` of a branch ends READY on a copy of the realm, attached by `workspace attach`.
- [ ] `use` of another branch, then `back`, each ends READY through `--update`, with no reinstall. Each keeps the same realm copy and an earlier edit, proven by the commit-history count. Each first makes `data.pre-switch` and prints the schema gate's result.
- [ ] `use` with nothing moved runs no installer.
- [ ] A manifest with a `repo` row runs an unpushed commit, and `status` marks it.
- [ ] A live App row hot-reloads.
- [ ] A live Agent row shows a code edit after one `use`, with no installer run.
- [ ] `status` shows every row's form and state, plus the RunPod line.
- [ ] V7's check prints the stack's pins, while the live interpreter prints the live ones.
- [ ] A RunPod job from a stack with live rows refuses before any spend.
- [ ] `stop` returns the machine to its live install untouched, by the hashes and database facts of [Plan 61's Completion](../61-run-a-release-branch-locally/plan.md#completion): every file under the live realm's `cas/`, the live `astrid.env`, the install record, the login service plist and the live manifest, by `shasum -a 256`; the live Runtime's pid, start time and launchd job state; and the live database's head publication ids, commit-history count and `runtime_epoch`, read with `mode=ro`.

Negative cases:
- `back` with no previous version says so.
- A target whose Agent lacks V0's fix is refused before anything changes, naming #825.
- `back` to an older schema than the data is refused, naming `data.pre-switch` as the way back.
- An update whose own rollback also fails stops, restores `data.pre-switch` and prints the state.
- A disk shortfall is refused before staging, naming the bytes needed.
- An old per-branch root is named, with the command that deletes it.
