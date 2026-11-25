# Plan 73 — MS-11 integrated negative-preflight preparation

**Disposition:** PASS for the listed bounded negative probes on Linux; **MS-11 NOT COMPLETE**. No D5 cutover, authored legacy deletion, project-to-main integration, independently credentialed reviewer, or change to canonical tasks is authorized or claimed.

## Source identity and evidence

- **Source under test:** `af21974b3b20c4be0784f935175e2d4941e39265` on isolated recovery branch `p73/recovery-ms8-validation-20261123-1`, stacked as draft [PR #1627](https://github.com/banodoco/astrid-dev/pull/1627) over unchanged [#1390](https://github.com/banodoco/astrid-dev/pull/1390).
- **Hosted proof:** [Documentation integrity run 45188940564](https://github.com/banodoco/astrid-dev/actions/runs/45188940564), job `137741821627`. Documentation, App vision-consumer, and review-intake checks passed on the exact commit. Generated publication and auto-merge were skipped.
- **Complete machine receipts:** `plan73-ms11-negative-preflight` workflow artifact **14824728384**, with `ms11-negative-matrix.json` and `ms11-negative-matrix.md`. Artifact is linked from run 45188940564.
- **Audited executable:** [scripts/ms11_negative_matrix.py](https://github.com/banodoco/astrid-dev/blob/af21974b3b20c4be0784f935175e2d4941e39265/scripts/ms11_negative_matrix.py) runs only on a temporary *detached* Git checkout fetched from the checked-out repository at the literal PR-head commit, with a disposable home and temporary installation targets. Original checked-out tracked state was compared before/after and remained unchanged.
- **Repro command from a checkout containing the exact commit:** `python3 scripts/ms11_negative_matrix.py --source-ref af21974b3b20c4be0784f935175e2d4941e39265 --output-dir /path/outside/checkout/ms11-negative`. Do **not** use a real installed skill destination.
- **Observed result:** artifact JSON `status: PASS`, **16 of 16 assertions true**, **20 command receipts** and `error: null`; eight *intentionally nonzero* CLI executions returned the required named refusal. Zero-exit commands established the baseline and restoration checks. No expected refusal was mistaken for a passing normal command.

## Negative matrix — exact expectations

| Probe, all in disposable checkout | Required refusal and observed disposition | Integrity observation |
| --- | --- | --- |
| Duplicate opted-in stem `agent/roles/gap.md` vs original gap workstream | `duplicate skill name astrid-dev-gap` — nonzero exit | Every existing generated `SKILL.md` hash unchanged |
| New workstream with missing Markdown target | `missing link target` — nonzero exit | Existing package hashes unchanged |
| Workstream with invalid `skill: yes` metadata | `literal boolean` — nonzero exit | Package hashes unchanged |
| Tampered generated manager `SKILL.md` | `astrid-dev-manager: generated SKILL.md is stale` — nonzero `skills check` | Check did not silently rewrite the tampered package; original bytes restored explicitly and rechecked |
| Foreign file with desired package name | `foreign installation entry` — nonzero dry-run and real install | No partial installation, both foreign files remained byte-identical |
| Foreign symlink with desired package name | `foreign symlink` — nonzero dry-run and real install | Symlink preserved; no other skill links installed |
| Rebuild/check after all probes | Zero-exit final `skills build` and `skills check` | All baseline skill names and hashes restored; original checkout tracked status unchanged |

## Other exact-head checks

The same hosted [run 45188940564](https://github.com/banodoco/astrid-dev/actions/runs/45188940564) independently passed: **563 Python unit tests**, **64 view tests after the generated-skill build**, one additional targeted golden fixture test, MS-10's scripted disposable authoring rehearsal, the reference-inventory upload, the repository checks and generated-view validation. These were hosted Linux tests, **not** local native macOS, Windows, or real-client executions.

## Preparation vs completion

The matrix proves only the bounded expected refusals and integrity checks above. It **does not** establish a project-wide cold start after deleting the authoritative `skills/` tree, any live Claude/Codex skill-picker discovery or credentials, macOS/Windows support, adversarial concurrent writer safety, durability after power loss, general orphan recovery, cross-repository releases or coherent multi-file snapshots. Existing standalone builder tests already cover narrower related behavior; this matrix additionally joins the *actual staged project sources* to the CLI and install refusal paths in one exact-source disposable environment.

No independent fresh AI-agent launcher was available in the manager's connected execution capabilities. The earlier [MS-10 scripted rehearsal](ms10-precutover-extension-20261123.md) remains useful pre-cutover evidence, but **fresh-agent authoring and actual client discovery are still NO-RESULT**; no independent AI agent or client was impersonated.

The original RS1 **technical BLOCK** persists. Supervisor adjudication of RS1.4–RS1.9 applies only to six named bounded repairs, not a retroactive formal ACCEPT; reviewer credential provenance and disputed historical round counters remain unresolved. MS-7 active-reference decisions, D5, MS-9 legacy removal, the genuine fresh-agent MS-10 exercise, MS-11 integrated cutover qualification, final independent R, and the separate max-two-round whole-project Astra High sense check still gate an owner-approved project-to-main integration.

**Next action when authorized:** integrate/qualify the staged candidates after exclusive management custody, adjudicate D5 and the MS-7 inventory, then exercise MS-9–MS-11 and client discovery on an integrated exact head. Do not mark this MS-11 task complete from the negative matrix alone.
