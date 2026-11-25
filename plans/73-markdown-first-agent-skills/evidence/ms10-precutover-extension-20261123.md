# Plan 73 MS-10 — pre-cutover disposable extension rehearsal

**Status:** PASS for a scripted, disposable Linux CLI rehearsal. **Not MS-10 completion**, not an independent fresh-agent session, and not authority to cut over the current legacy skill tree.

## Exact source and custody

- **Rehearsed source:** `c184ff5d9a7773528a76d6a4e173a5a9a18e2852` on isolated `p73/recovery-ms8-validation-20261123-1`.
- **Rehearsal CI:** [Documentation integrity run 45179111579](https://github.com/banodoco/astrid-dev/actions/runs/45179111579), documentation job `137708111961`; vision-consumer and review-intake succeeded on the same exact source head.
- **Raw command and operator-task evidence:** GitHub Actions artifact `plan73-ms10-disposable-extension`, ID `14819644475` on that run: `task.txt`, `ms10-log.json` and `ms10-log.md`.
- **Owner and scope:** isolated recovery preparation stacked on draft [#1390](https://github.com/banodoco/astrid-dev/pull/1390) via [draft #1627](https://github.com/banodoco/astrid-dev/pull/1627). No changes to old manager branches, authoritative `skills/`, canonical task status, release instructions or main.
- **Source documentation:** `agent/README.md` at the rehearsed SHA, specifically “Author a document” and “Build and install.”
- **Environment:** GitHub-hosted `ubuntu-latest` runner. The exercise fetched the literal PR source SHA locally from the checked-out repository into a detached disposable Git checkout. It set a temporary HOME, created three disposable skill roots, used no live Claude/Codex login, and made no paid requests.

## Instructions and procedure

A hypothetical fresh author was asked, using the staged README as the only authoring guide: create one new independent Markdown workstream, include `skill: true`, run the published build/check/dry-run/install commands, find and load its installed `SKILL.md`, repeat to confirm idempotence, remove the opt-in, and verify safe retirement with foreign entries unchanged. The **script**, not a separate AI agent, executed that task.

The temporary source was `agent/shared/workstreams/extension-probe.md`, including a plain-text description, the five required workstream headings and a relative Markdown reference to the authoring guide. It was created **only in the disposable checkout**, not committed to this PR.

Command families run from the detached checkout:

```sh
python3 scripts/astrid_dev.py skills build
python3 scripts/astrid_dev.py skills check
python3 scripts/astrid_dev.py skills install --dry-run --destination <temporary-existing-skills-root>
python3 scripts/astrid_dev.py skills install --destination <temporary-existing-skills-root>
```

The install/dry-run operations were repeated independently for new `claude/skills`, `codex/skills` and `agents/skills` directories, all within the same temporary directory. The script read the generated `SKILL.md` **through the installed symlink**, resolved its Markdown link to the guide, and repeated build/install. It then removed the opt-in flag while leaving the source file, rebuilt, rechecked, retired the stale links and verified final idempotence.

## Exact outcomes

| Probe | Actual observation |
| --- | --- |
| Assertions and commands | **26/26 PASS**; **25/25 commands exit 0**; error field null |
| Starting packages | 14 generated packages present |
| After a single new opt-in workstream | 15 packages; all 14 original `SKILL.md` content hashes unchanged |
| Build/check/rebuild | First build created the new package; check passed; repeat build reported packages current |
| Dry-run | Three roots stayed unchanged before install |
| Install and load | 15 symlinks present per root; each successfully read the new skill and resolved the guide reference |
| Foreign preservation | One unrelated foreign file remained byte-identical in each root |
| Reinstall | Idempotent; already-linked receipts for existing skills |
| Remove opt-in flag | Generated package retired; plain Markdown source remained |
| Retirement and final check | Exactly 14 original links remained per root; new links retired; original content hashes preserved; final build/check passed |
| Source custody | Original checkout's tracked status identical before and after |

The same hosted exact-head workflow also passed its **563-test** full Python inventory, **64 post-build view tests**, targeted golden copy regression, repository checks, regenerated views and vision-consumer contract. These are hosted Linux results, **not native macOS or Windows executions**.

## Findings and limits

- One **rehearsal harness-only** issue arose during preparation: the nested disposable skill roots needed parent creation. This was fixed on the isolated recovery branch before the successful exact-head run. It is not evidence of a product installer failure.
- The shared-workstream navigation index lists the nine original shared procedures. Generated discovery is *not* limited by this index: the workstream added here packaged and loaded without a manual index entry. Staged authoring guidance was clarified to distinguish editorial navigation from generated discovery.
- No actual fresh AI-agent instance was given the instructions. Thus usability/confusion observations from an independent agent remain **NO-RESULT**, not PASS.
- The script read an installed package through symlinks; it did **not** exercise a real Claude or Codex skill picker, session startup, permissions, or registered skills UI. Those remain **NO-RESULT**.
- Windows and macOS installation and build→test sequences, crash/power-loss behavior, noncooperating concurrent writers, safe orphan recovery and multi-file snapshot guarantees remain unverified.
- MS-10's canonical dependencies (MS-7, MS-9 and D5-controlled active consumer migration/deletion) are outstanding. This is pre-cutover preparation, **not acceptance or task completion**.
- The independent original RS1 verdict remains **BLOCK**. Supervisor disposition of RS1.4–RS1.9 applies only to those six bounded remediations; reviewer credential/counter caveats and the separate final R and maximum two-round Astra High whole-project sense check remain open.

## Continuation

Keep draft #1627 on its isolated branch. Reconcile independent review and exclusive custody, obtain D5 decision and complete MS-7/MS-9, then commission an actual fresh-agent exercise and real client discovery where supported. Follow with MS-11 integrated proof and final review. No merge, cutover or legacy deletion is authorized by this report.
