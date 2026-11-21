# Inputs — Live custom-element editing

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked for this plan on 21 November 2026 ("Can you spec out those issues specifically as a plan according to /astrid-dev-plan please") and set its direction in the same conversation, quoted under [Owner decisions](#owner-decisions); the specific scope below is not yet greenlit. Next: the owner reads the ten statements, strikes any that are wrong and answers D2 and D4.

**Prior art:** Checked on 21 November against the plan-69 heads in [Source identities](#source-identities).

- **The batch exists.** `astrid/sdk/timeline/commit_session.py:603` `Timeline.commit` takes a function or a fixed command list and submits one request; `astrid/sdk/timeline/commands.py:75-115` registers `clip.set-element`, `clip.set-params`, `clip.add` and `doc.patch`. `astrid/sdk/timeline_elements.py:419` `place_element` is that same commit with one `clip.set-element`, after fetching the pack pin with `_admitted_element_inputs`. Nothing in `model.py` or `edits.py` stages a placement, which is the gap.
- **Limits found.** `clip.add` refuses anything but the parent (`_clip_commands.py:16-18`), so clips added inside a shot go through the `doc.patch` that `_capture_free_edits` emits (`commit_session.py:485`). A formula can be removed with `doc.patch` (`_doc_patch.py:379-417`), not `clip.set`.
- **The skill teaches the slow way.** `astrid/packs/rendering/docs/references/generated-elements-authoring.md:65` gives `place-element` with one `--target`; the timeline skill teaches one commit for many edits but never mentions placements.
- **Live refresh exists.** App `src/tools/video-editor/contexts/VideoEditorProvider.tsx:273-283` re-reads admitted elements whenever the element refs the preview renders change, so a commit that points clips at a new revision refreshes the open editor. `admitted-elements.ts:72` loads only exact refs, and `admittedElementLoader.ts:104-117` checks each bundle's SHA-256 before import. Not covered: re-admitting different bytes under an unchanged ref, which admission never does because the revision is the digest.
- **The restart.** The Runtime runs the Agent's commit code in-process (`runtime_protocol/timeline_commit_provider.py:70-99`); the element registry is cached (`astrid/core/element/registry.py:197`), and `astrid/sdk/timeline_address.py:471-492` clears it only when a known provider changes, not after a miss. The pack host already acknowledges installs while idle (`GenericPackHost.acknowledge_pack_refresh`), so the CLI's "next start" line (`cli_manage.py:354-356`) is wrong. That the cache caused the reported restart is inferred from code, not reproduced.
- **The motion pack.** `astrid/resources/moved-elements.json` says `astrid_motion` moved to `poms_packs` and suggests a floating `--revision main` install. `astrid/core/pack/defaults.py:36` installs defaults from a release manifest passed in by the installer; no manifest in the three repositories pins the motion pack.
- **Checks on pack code.** `astrid/core/element/project_packs.py:327` `_check_imports` (comment: "Pack code is trusted build source, but its dependency closure is explicit"), `:478` `admit_project_pack` (snapshot, compile, digest revision); Runtime `runtime_protocol/service.py:5987`, `:6013` serve only currently admitted bytes and verify them.
- **Whole-timeline cost.** Agent `astrid/sdk/timeline/commit.py:1201` `RuntimeCommitService.commit` and Runtime `runtime_protocol/timeline_commit_store.py:1528` `_validate` hash and validate the full closure on every commit; there is no diff-scoped path. [Plan 75](../75-fast-saving/plan.md) and [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) own that cost; [Plan 18](../18-timeline-editing/plan.md) owns broader command unification; plans [61](../61-run-a-release-branch-locally/plan.md) and [62](../62-one-manifest-one-stack/plan.md) own the local stack. Issues [#842](https://github.com/banodoco/astrid-dev/issues/842), [#846](https://github.com/banodoco/astrid-dev/issues/846), [#852](https://github.com/banodoco/astrid-dev/issues/852) and [#966](https://github.com/banodoco/astrid-dev/issues/966) overlap validation, replay, commands and saving; do not duplicate them.
- **What the run did instead.** The runbook used seven serial placements, direct SQLite reads and a detached publish. It worked on a fresh stack once the motion pack was installed and the Runtime restarted (reported by the run, not reproduced here).

**Approach:** Extend the one commit path with a staged placement, clear one cache on a miss, fix the skills, prove it live. Compared and rejected: doing nothing (the owner cannot use the flow they asked for); a new batch command or endpoint (duplicates `Timeline.commit`, its outbox and its conflict rules); a combined admit-and-apply command (two transactions behind one name, and unnecessary once the commit is one call); an App change for live refresh (already there); a trust-tier design for local packs (nothing to distinguish it from yet, see D1). No new pack and no core change outside the Agent.

**Challenge:** Reviewed — by Claude Fable on 21 November against the draft at `fb16986db` and the code, with three read-only Luna verifiers (outputs `V1.txt`–`V3.txt`, machine-local). Fable also wrote the source report the draft was built from, so this is independent of the draft but not of the evidence; one finding corrects that report. Findings and rulings:

- **Live refresh is already built** (`VideoEditorProvider.tsx:273-283`). Accepted: removed the App half of LE-3.
- **The admit-and-apply wrapper adds a surface and hides which step failed.** Accepted: removed; the skills teach two calls. LE-3 is gone and its doc work moved into LE-1.
- **RS1 guarded a contract that no longer exists.** Accepted: removed. One final review stays.
- **Phase 2 (LE-5) designed a local-versus-shared trust boundary for packs that have no shared path.** Accepted: removed. The owner's words decide the direction (D1); hosted and shared trust stays a proposed issue.
- **The restart fix was scoped across the pack transaction, the CLI and the Runtime daemon.** Accepted: narrowed to the miss path in `timeline_address.py` plus the wrong message; route N.
- **Wrong names in the draft:** `commit.py:_CommitProvider` is `RuntimeCommitService`; the test that pins the restart message is `tests/core/pack/test_cli_manage.py`, missing from the inventory. Corrected.
- **Missed limit:** `clip.add` refuses occurrences, so the six added text clips depend on `doc.patch` mixing with `clip.set-element`. Accepted as LE-1's main risk and written into its card.
- **Correction to Fable's own report:** it described a DEV-only editor gate and no integrity check, read from the App's `release/14/plan-59` checkout. On plan-69 (`5c5899a61`) every editor loads admitted elements from the Runtime and checks the digest. The draft had this right.
- **Rejected:** dropping the final review as well. The change alters what one commit may contain and what a long-lived process caches; one review is cheap against that.
- **Rejected:** a seconds target as a completion gate. The commit cost belongs to plans 75 and 77; this plan records times and does not promise them.
- **Left to the owner:** D2 and D4.

**Proof and limits:** Unit proofs for the mixed commit and the miss-then-install lookup; a live proof through the editor's chat agent for the whole flow, with negative cases, as [Completion](plan.md#completion) describes. Limits: the restart cause is inferred until LE-2 reproduces it; mixing native and patch commands in one request is unproven until LE-1; the live proof is one project on one machine and says nothing about hosted use.

**Review rounds:** Recommended: no review stop, and one final review of at most 2 rounds, because the change is small but touches what a commit may contain. Next: the owner confirms the cap (D4).

**Run start:** Pending — no run is authorized. Next: when the owner starts one, record the date, the accountable session, the actual base and dependency revisions and what it may do without asking.

Ten statements for the owner to strike or keep:

1. Now, a custom-element edit is eight commits driven by a script outside the editor. After, the editor's own agent does it in one commit.
2. Seven placements, their parameter changes and six new text clips are one receipt and one undo.
3. We add no new batch system: `place-element` already rides the batch path one clip at a time, and we let it carry many.
4. Installing a pack never needs a restart, and Astrid stops saying it does.
5. Pack code a creator wrote on their own machine is trusted as theirs: no sandbox, no provenance check, no trust tiers.
6. The digest pin and exact revision stay, because they are why last month's timeline still renders last month's code.
7. Custom elements may still import only React, Remotion and files in the pack; arbitrary packages stay out.
8. Admitting an element and committing the timeline stay two calls, and a failure says which one failed.
9. This plan does not make a save faster; it makes one save do the work of eight.
10. Hosted and shared packs get no isolation from this plan, and none exists today.

Owner reactions: pending. Record any struck statement under [Owner decisions](#owner-decisions) and revise the plan before greenlight.

Proposed issues (do not create them as part of planning):

- **Review once-per-process CAS verification integrity** — Independently review Runtime `b2ea261` cache identity, same-size mutation, replaced inode and force-verify semantics against adversarial file changes; keep or repair based on focused evidence. Related existing history-state tests; this optimization is not automatically approved by the live-flow proof.
- **Recover from admitted-element list and proxy timeouts** — App `admitted-elements.ts` shares the bridge's 30 s deadline for list and module import; `scripts/runtime-discovery-proxy.mjs` has a 60 s idle timeout. Reproduce slow/late responses and add bounded retry with cancellation and scope fencing; avoid replaying mutation under a new idempotency key. Verified constants; whether it blocks the target remains a measured question.
- **Make release stack updates safe and repeatable** — Extend plans 61/62's `scripts/astrid-release/astrid-release` to repin while retaining realm data, report readiness and backup/restore behavior, and test failed start and retry. Treat cloning/inode-trust, backup deletion and stop reports as leads until independently reproduced. This is test infrastructure, not the editor workflow.
- **Isolate Agent test pack roots from the user's home** — Reproduce the reported `~/Astrid/packs/astrid_motion` collision with the named tests; make fixtures use temporary HOME/XDG and explicit Runtime/Node configuration. Inspection found many temp-rooted tests, so the broad collision claim is unverified.
- **Bind words on newly added shot clips** — Reproduce the runbook's reported `missing exact word binding` using a minimal shot and registered transcript; resolve at the timing/authority owner and test old and new bindings. This plan's proof must disclose numeric timing if word binding remains unavailable.
- **Inspect repeated media hashing during publish** — Verify with a profile whether media bytes are read or hashed twice across CAS and `runtime_protocol/service.py:_validate_media_dependencies`; line 3613 alone checks one computed digest and does not establish double hashing. Optimize only with integrity coverage.
- **Qualify hosted custom-element trust and delivery** — Plan-69 tests the Runtime loader, but production deployment, malicious/shared pack isolation and multi-user authorization are not proved. Define a strict execution boundary and verify hosted delivery, including stale or cross-project artifacts; no claim that allowlists alone are a sandbox.

## Owner decisions

Owner's words, 21 November 2026, from the planning conversation (machine-local record `evidence.md`):

- "we should just be able to look at the timeline editing skill associated with Astrid and do this live very easily without changing any code in the core."
- "we have built a path for batch edits, so why aren't we just using that? And why are we scripting outside the editor?" and "we 100% should be able to batch these."
- "the custom elements are just stuff that we vibe code… there should be only the loose necessary kind of security stuff."
- "Wut, why on earth would loading a pack require restart?"

- **D1 — Decided by the owner's words: only loose, necessary security for local custom elements.** The plan reads that as: trust local pack code, add no gates, keep the integrity checks (compile, digest pin, exact revision) and the import rule. Statements 5–7 are that reading; the owner can strike any of them.
- **D2 — Owner decision needed:** should a fresh install include the motion pack, pinned to an exact commit in the release manifest? Recommended: yes. The timeline skill teaches `am-type` and `am-footage`, and a fresh install without them refuses the first edit. The cost is a larger install and one more pin to move each release. Without it, LE-2 still removes the restart, and the first edit installs the pack on demand.
- **D3 — Decided by the planner, reported:** one phase; if word-bound timing on new shot clips cannot be committed, the proof uses numeric timing and says so, and the binding defect is an issue.
- **D4 — Owner decision needed:** confirm one final review of at most 2 rounds, and name the release this work joins.

## Source identities

Numbering: fetched `origin/main` at `7d851684deb5dfbbcab0b2e803768b8b227777e2` contains plans through 77; plan 70 is already used. Remote branch names and all open PR heads/titles showed no claim on 78. `gh pr list` was attempted but `gh` is not installed; the authenticated GitHub pulls API supplied the open-PR inventory instead, without exposing the token. Recheck before any later publication.

Observed donor heads: Agent `release/14/plan-69` `83d5f8fe382e2573deee39ffb6036cf2c834b1f7`, Runtime `release/14/plan-69` `b2ea261f36f5f39c5f9964b02c8012c420e0b359`, App `release/14/plan-69` `e0c6f7cdbb943074e1c2d4a7f483d352471f1770`. Observed `origin/release/14/main` respectively `9f614dff7707a493f29a548583f86c4791b957d2`, `2537fed24385ec1c24f48a812e09af4bb63fb794`, `a55ff290ed4f291420f21d340a5117c0f8b5a38a`. These are observations, not future bases. The App path supplied was actually checked out at `release/14/plan-59` `36c3c6f6a`; the plan-69 App was inspected in its separate worktree. Plan-69 App reverts release/14/main PR #297 (`ef9df969c`); review retained/replaced behavior explicitly rather than silently importing the reversal. At run start select exact retained feature commits and prove composition on current release bases; regenerate locks rather than trusting old pins. If assigned to release N, cut each product `release/N/plan-78` from its current `release/N/main`; no release N is chosen now.

## References

Owner evidence, Fable reviews, Luna L1–L5 and V1–V3, stack logs and fresh runbook supplied in the planning request are private machine-local inputs, not portable project dependencies. Their specific checked findings and uncertainty are recorded above. The live proof must use a distributable fixture or an explicitly authorized private test copy; never include private media or credentials in the plan.
