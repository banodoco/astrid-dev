# Inputs — One manifest, one stack

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 17 November 2026 the owner asked whether the release-branch tool would make developing on top of it convoluted, and asked for the long-term path to be drafted as a follow-up plan to [Plan 61](../61-run-a-release-branch-locally/plan.md). This is that draft. Next: the owner decides D1 and D3 to D7.

**Prior art:** It is [Plan 61's](../61-run-a-release-branch-locally/inputs.md#planning-evidence), plus what two independent reviews of Plan 61 verified in code on 17 November 2026:
- *Moving back works in the code, not yet on these stacks.* In a real run on the isolated stack on 17 November, `--update` failed with "launchd service configuration is malformed". The cause is the installer's stop probe. Beside a live Astrid it finds the live job under the shared label, and it reports this stack's missing service file as malformed ([#825](https://github.com/banodoco/astrid-dev/issues/825), under [#818](https://github.com/banodoco/astrid-dev/issues/818)). The interim idea, removing `program/` and reinstalling over the kept data, is refused by the installer's retained-profile guard (`backend.py:1028-1044`, via `cli.py:962`), and it runs no migration. So `use` and `back` wait for V0 and V9, and there is no interim switch. The rest of this bullet is read from the code. `--update` installs whatever the manifest names, forward or back. A failed update rolls itself back inside the transaction. After a good update, `finish()` keeps the previous version directory and its `manifest.json` (Agent `astrid/installer/backend.py:2030-2040`). The installer's `--rollback` only switches back to the retained R0 service (`cli.py:531`, `:907-908`). So going back means `--update` with the kept manifest.
- *Local commits work today.* The installer takes a manifest `repo` path and archives its committed tree. `pin.mjs` cannot write such a manifest yet, because it reads raw GitHub.
- *Adopt cannot copy a realm into a fresh install.* `workspace adopt --from` refuses a destination that already has a workspace selection (`workspace_adopt.py:248-249`), and the installer always creates one (`core.py:862-864`). [#817](https://github.com/banodoco/astrid-dev/issues/817) is the fix.
- *RunPod.* The pack reads `Path(sys.prefix).parent / "manifest.json"`, so the interpreter decides which pins are used (`managed_sources.py:36-43`). The client, not the pod, fetches the sources, before the paid lease. Machine preferences and lease journals live under the data root. The stack is installed with `--command off`, so the `astrid` on PATH is the live install. No dry run prints the managed-source pins today.
- *Cost of the current naming.* A root per branch means each switch stages a full program, measured at about 3.8 GB, plus a new realm copy.
- *Prior art for live pins.* None in the code: no "snapshot" or "active snapshot" means a set of commits. The branch `p59/runpod-source-mode` was never pushed.

**Approach:** Keep the manifest as the only pin set, and make the stack the only place. Everything else is a verb or a row form on those two.

Alternatives set aside:
- A snapshot object: it would be a second way to say "these commits".
- A root per branch: a full program per switch.
- A new rollback command: the kept manifest plus `--update` does it.
- A replace-and-install switch before V0 and V9: the retained-profile guard refuses it, it runs no migration, and it would be a second path to delete later.
- A separate source-mode tool or environment: it would be a second stack to learn, where a row form is enough.
- Ranking source mode before local `repo` pins: those pins are cheaper and reuse more, so V4 comes before V6.
- A bare-commit form of `use`: a set of commits is a manifest file (D6).

Concept count: today, two ideas in about ten spellings. After Plan 61 alone: the manifest, a per-branch root and the realm copy. After this plan: the manifest, with three row forms, and the stack.

**Challenge:** Pending — an independent critique is required before greenlight. This plan changes the installer-tuple writer, the manifest's keys and a copy of user data, and it touches the Agent and Runtime source surfaces. Two reviews shaped this draft; neither has seen it written. Next: the advisor critiques the written plan and tasks against the code, briefed to remove and reuse.

**Proof and limits:** The list in [plan.md](plan.md#completion). macOS only. `use` and `back` need V0's fix in the Agent of every manifest they move between, and V9's fix on that release line. Until both land, Plan 61's rebuild steps are the only way to move a stack. Disk: about 14 GB, Plan 61's ~10 GB plus the previous program version that `--update` keeps. **Risk:** the same stop probe guards `astrid-runtime restart` and `up` over a stale owner (`runtime_lifecycle.py:87`, `:102`), and `--uninstall` (`core.py:692`). That is read from the code, not run. The tool keeps its own start and stop, including for V6's live rows, until V0 is in. The first-start retry and its cause are Plan 61's RB-9.

**Review rounds:** Recommend at most 5 at the end, stopping at the first round with no blockers. That is the owner's standing rule. It is warranted here because the plan reaches the installer tuple, the source surfaces and user data. Plan 61's tool has its own round before it lands (Plan 61's D3), so these rounds cover Plan 62's changes. Next: the owner confirms (D3).

**Run start:** Pending — no run is authorized. Next: when the owner starts a run, record the date, the phase or tasks it covers, the accountable session ([who that is](../../agent/shared/run-contract.md#who-answers-for-a-run)), what it may do without asking, what still needs the owner's go, and the advisor session if there is one.

## Owner decisions

The ids are shared with Plan 61: D1, D3 and D4 ask the same question in both plans, each for its own plan. D2 is Plan 61's only (where the tool lands; decided there: the release route). D5 to D7 are asked only here.

- **D1 Which release.** *Pending.* (a) Release 15. (b) Release 14, if it is still open when Plan 61 lands. Recommendation: (a). Plan 61 covers Release 14's need, this plan widens the manifest, and its two installer prerequisites must land first.
- **D3 Review rounds.** *Pending.* At most 5 at the end, stopping early (recommended), or a fixed smaller number.
- **D4 A real RunPod job.** *Pending.* (a) Not in this plan. V7's $0 check is enough here, and one job inside $1 goes with the Agent issue (recommended). (b) One owner-approved job of at most $1 from the stack after V7. It needs `machines setup` in the stack's data root first.
- **D5 Live Agent and Runtime rows as the source route.** *Pending.* Whether V6's live rows become the supported answer to [#758](https://github.com/banodoco/astrid-dev/issues/758) for an isolated stack. Recommendation: yes, agreed with #758's owner before V6 starts.
- **D6 A bare-commit form for `use`.** *Pending.* (a) No: a set of commits is a manifest file, and `pin.mjs` writes one in one line. (b) Yes: `use <40-hex>` for an App commit that carries a manifest. Recommendation: (a), one form fewer.
- **D7 Older routes.** *Pending.* Whether V8's section stops recommending Pinokio `ASTRID_APP_REF` reinstalls and hand-made staging scripts for trying a branch. Recommendation: yes. Tester builds stay.

## Source identities

The base is Plan 61's tool, as landed by its RB-7. Plan 61's astrid-app branch is `release/14/plan-61` (head `cf383fc0e2668fe25c4a24f77c1a0b438a3a9fca` on 17 November 2026); record the branch and SHA it has reached when this plan starts. Read-only references, 17 November 2026: astrid-agent `release/14/plan-59` at `4ca3ba324c29f6e3772bc9a08ea76024c009a377` (the code reading used `b9d0858`; `managed_sources.py`, `generation.py` and `launcher.py` are byte-identical between the two), and astrid-runtime `release/14/plan-59` at `e6106ac0799c84602e3fc19a3aede94e2ffe0aef`. Integration destination: `release/<NN>/plan-62` in astrid-app, astrid-dev and, for V0 and V9, astrid-agent (D1), cut from that repository's `release/<NN>/main`. If #825 or the retained-profile issue is fixed first on a fix branch of the release in progress, V0 or V9 consumes that fix instead. Re-check at dispatch.

## References

- [Plan 61](../61-run-a-release-branch-locally/plan.md), the first cut, and its [issues list](../61-run-a-release-branch-locally/tasks.md#issues-to-file): [#815](https://github.com/banodoco/astrid-dev/issues/815) to [#820](https://github.com/banodoco/astrid-dev/issues/820), and two comments on [#739](https://github.com/banodoco/astrid-dev/issues/739).
- Running from source: [#758](https://github.com/banodoco/astrid-dev/issues/758).
- Installer local sources: astrid-agent [`docs/setup/local-source-install.md`](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/local-source-install.md).
