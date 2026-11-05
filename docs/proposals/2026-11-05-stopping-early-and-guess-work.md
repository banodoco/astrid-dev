# Why the overnight run stopped at 04:45 instead of 06:00, and what to change

For POM and the Banodoco team, from Dylan's overnight help-out (2026-11-04 22:00 to 2026-11-05 06:00 ET). The results are in Dylan's hand-off, and every judgment call is in his decisions ledger; both are shared separately, and the branches are on `github.com/matlowai/*` under `astrid-help/*`. This is a retrospective plus a proposal; it changes no rule by itself.

## What happened

- The last real work finished at **04:38 ET**: the PK-14 App fix b6619d9a6 was committed at 04:34, its final checks passed at 04:36, and the hand-off was written at 04:38.
- After that came only wrap-up: the push to Dylan's forks, a checkout inventory, and stopping the watcher. That finished at about 04:45.
- Dylan's window ran to 06:00, with quota left and Opus subagents allowed. **About 75 minutes of available capacity went unused.**
- **No rule forced the stop, and no permission prompt or classifier block happened near the end.** The classifier blocked three actions all night, all much earlier: the pin to POM's runpod-python fork and two edits to the settings file. Dylan approved all three.
- The stop was my call. By 04:38 every task that was *in the plans and ready to start* had stopped on an owner decision or a review budget. Nothing in the setup gave me a sanctioned way to take on "probably wanted, but a guess" work, so I defaulted to stopping.

## What was left, and what stopped each item

| Remaining work | What gated it | Source of the gate |
|---|---|---|
| Plan 06 PK-15, PK-15B, PK-16, PK-17 | PK-12 stopped on S25 (fixing the editorial→video_editing cycle changes public capability ids) and S26 (about 300 installed-import violations). PK-15 comes after PK-12 on the Agent line. | Plan 06 tasks.md order line; "a failure that also fails on pre-main is reported to the owner, not fixed here" |
| Plan 06 END review | Needs PK-17 first; at most 3 rounds (owner decision, 3 Nov) | tasks.md END |
| Plan 02 R1 round 2 | Round 1 failed on items only POM can decide, and fixing them depends on POM's answers. A second round would spend one of the five owner-budgeted rounds on a known FAIL. | tasks.md R1; run contract: "never add stages, reset counts" |
| Plan 02 C2-1 (cryptography) | Needs a commit on POM's runpod-python fork, and we can't push to peteromallet | Push scope: Dylan's forks only |
| RB1 rebase and promotion, both plans | "Only with the owner's explicit authority"; no banodoco pushes, no PRs | Plans 02 and 06; Dylan's push ruling |
| V2 on a RunPod CPU pod, real inference | No GPU, RunPod or provider calls | The run's hard rules |
| astrid-dev ledger note | Nothing. I never created a fork of astrid-dev; it is now pushed (see the end). | My omission |

## The rules that pushed toward stopping

1. **"Start only on the owner's go"** on every task in plans 02 and 06, and in the run contract: "do not start, resume, or broaden product work without its explicit authority." Dylan's ruling for the night ("use your best judgement … anything we move towards the final goal is welcome") overrode this for *plan tasks*. It said nothing about work outside the task list, so I read it narrowly.
2. **STOP hunks and owner items:** a conflict where both sides change the same statement, or a failure that also fails on `pre-main`, goes to the owner. That is correct for landing. Overnight it also froze every task downstream of the stop.
3. **Review-round budgets:** R1 has 5 rounds, LB-TXN 2 and END 3. These are owner budgets. Spending one on a review that is known to fail wastes it, so they block repeated tries.
4. **Focused checks only**, from this repository's AGENTS.md: never broad or whole-suite runs. This is fine; it ruled out "run everything and see" as filler work.
5. **Dylan's own agent instructions:**
   - #11: "do what was asked; bring clever ideas back as a list … don't dig into improving related things nobody asked for".
   - #1: state the goal before a long or costly action.

   Both lean hard toward stopping and reporting rather than guessing.
6. **Dylan's "don't get too burny" plus the 06:00 reset:** I turned this into a 05:30 cutoff for agents, to leave 30 minutes for wrap-up. With that cutoff, a task started at 04:40 had only 50 minutes, which felt too short for PK-15, a large deletion.
7. **How I scheduled work:** the heartbeat only started nodes the dependency graph marked *ready*. A node behind an owner decision was never "ready", so the graph ran out even though capacity didn't.

## Exact spec vs. a more flexible approach

**Exact spec, as run that night.** Only plan tasks are done; anything that hits an owner decision waits.
- Pros:
  - Nothing is built on an assumption the owner rejects.
  - Review budgets aren't spent.
  - The owner reviews only work they asked for.
  - The branch history stays easy to read.
- Cons:
  - Spare capacity sits idle exactly when the owner is unavailable, which is when help is most valuable.
  - A single owner question can stall a whole line.
  - The owner wakes up to a list of questions instead of answers they can pick from.

**Flexible.** When the in-plan work runs out, keep going on work that is *likely wanted*, labelled as a guess.
- Pros:
  - Capacity gets used.
  - Owner decisions turn into "pick branch A or B" instead of "start the work".
  - Risk is found earlier, for example rebase conflicts or tests that can't pass.
  - Even rejected work leaves evidence behind.
- Cons:
  - Rework if the direction differs.
  - More branches to review or discard.
  - The risk of a guess leaking into what lands.
  - Some tokens spent on work that is thrown away.

**My view:** the flexible approach is better *for windows when the owner is unavailable*, as long as the guesses are fenced off by how branches are set up (next section). The overnight run already showed the ledger keeps guesses reviewable: 56 logged decisions (A*, G*, I*, K* rows), each with a way to undo it.

## How to keep guess work safe with branching

1. **Two lanes, named so they can't be confused.**
   - Spec work: `astrid-help/<task>`, for example `astrid-help/pk14-app`.
   - Guesses: `astrid-help/guess/<task>-<assumption>`, for example `astrid-help/guess/pk12-s25-keep-ids`.
   - Spec branches never contain guess commits. A guess branch starts from the spec head it depends on.
2. **Build both answers to a yes/no owner decision when it's cheap.** Example: `guess/pk12-s25-keep-ids` and `guess/pk12-s25-rename-ids`. The owner's answer picks one, and the other is deleted.
3. **Do work that is useful under any answer first:**
   - read-only probes (merge-tree against the current `pre-main`);
   - conflict lists;
   - tests that pin current behaviour;
   - analysis that turns a question into a one-line choice.

   These cost nothing if the direction changes.
4. **One ledger row per guess**, giving the assumption, the evidence, the branch, and how to discard it. That's the decisions-ledger pattern (`contrib/override-ledger`), extended with a "Guess" type.
5. **Never spend owner budgets on guesses.** Pre-review a guess with an informal reviewer pass labelled "not an R1/END round", so the official round counts stay untouched.
6. **Freeze the base and timebox:** start every guess from a recorded SHA, and stop it at a fixed time with a written state. A half-finished guess is fine if it says where it stopped.
7. **Same scope limits as that night:** only Dylan's forks, no PRs, no pushes to banodoco, no GPU or providers. Guesses change where work happens, not who is allowed to land it.

## What the 75 minutes could have gone to (ranked by value under any owner answer)

1. **RB1 dry run (read-only, no risk).** Agent `pre-main` moved overnight; six installer fixes overlap Plan 01's files. A `merge-tree` probe of each candidate against the current `pre-main` would have given the morning a conflict list.
2. **C2-1 option b1, shown working.** On a matlowai fork of POM's runpod-python fork, relax `cryptography` to `>= 48.0.1`, run the fork's tests on 48.0.1 (currently listed as "not verified"), and repin lifecycle on a guess branch. POM's decision then becomes "merge this commit". It needs a nod first, because that would be a fork of POM's personal fork rather than of a banodoco repo.
3. **PK-12 S25 both ways, plus the read-only PK-15B census** (step 1 of PK-15B is a `git grep` census).
4. **An informal Plan 02 pre-review** against the R1 items, not counted as a round, so round 2 is more likely to pass.
5. **The umask 0002 product fix** on a guess branch.
6. Pushing the ledger note, which took two minutes and is now done.

## Proposed rule (for Dylan and POM to accept or reject)

> When the owner is unavailable and an authorized operator has given a best-judgment window, an agent that runs out of ready plan tasks may continue on "guess" work. That work must:
>
> - go on `astrid-help/guess/*` branches in the operator's forks;
> - prefer work that is useful under any answer;
> - log one ledger row per guess, with how to discard it;
> - never spend owner review rounds;
> - stop at the window's end with a written state.
>
> Landing still needs the owner's go.

## Where things are

The decisions-ledger pattern this builds on is on the same branch (`skills/astrid-dev-shared/run-contract.md` section "Decisions ledger when the owner is unavailable" and `skills/astrid-dev-shared/templates/decisions-ledger.md`). Fork: `matlowai/astrid-dev`, branch `astrid-help/override-ledger`.
