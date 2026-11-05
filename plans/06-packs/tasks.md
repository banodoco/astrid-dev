# Tasks: Packs v1.3 working project

[Project explanation](plan.md) · [Inputs and provenance](inputs.md) · [Current project status](../../README.md)

The index links to the existing work rows below. These are preserved task rows, not new work or status claims. Pack count (19 named packs) is distinct from the number of task rows.

## Task index

| Group | Task | Outcome |
|---|---|---|
| Retained | [PK-2 + PK-3](#pk-2) | Reuse verified Hivemind and core/pack boundary work. |
| Early repair | [PK-4-REPAIR](#pk-4-repair) | Fix the demonstrated boundary and locking problem. |
| Integration bases | [PK-0](#pk-0) | Freeze current destinations and retained inputs. |
| Agent | [PK-4](#pk-4) | Combine the eight parked inputs and preserved fixes. |
| Agent | [PK-1](#pk-1) | Apply reviewed work and namespace/schema repairs to the final base. |
| Agent | [PK-5](#pk-5) | Verify installed CLI, startup, and core resources. |
| Agent | [PK-6](#pk-6) | Finish loading/discovery and include accepted health changes. |
| Agent | [PK-7](#pk-7) | Prove trust, secret scope, and validation. |
| Agent | [PK-8](#pk-8) | Check source identity and transaction preconditions. |
| Agent | [PK-9](#pk-9) | Prove install, update, rollback, and removal. |
| Agent | [PK-10](#pk-10) | Preserve rendering and composition behavior. |
| Agent | [PK-11](#pk-11) | Integrate registry and catalog selection. |
| Agent | [PK-12](#pk-12) | Finish pack management and public API behavior. |
| Runtime lane | [PK-13](#pk-13) | Integrate moved data and source locks after PK-0. |
| App lane | [PK-14](#pk-14) | Prove live loading, refresh, disposal, and passive opening. |
| Migration | [PK-15](#pk-15) | Remove the 19 designated packs from Agent core. |
| Migration | [PK-16](#pk-16) | Receive and install those packs in poms_packs. |
| Final proof | [PK-17](#pk-17) | Run the installed CPU journey and map required evidence. |
| Final proof | [END](#end) | Review all required outcomes and explicit deferrals. |
| Publication | [PK-BRANCH](#pk-branch) | Publish the immutable reviewed candidate. |
| Publication | [PK-PREMAIN](#pk-premain) | Promote the same reviewed commits to pre-main. |

## Existing task details

### PK-0

**Action and outcome:** PK-0 — freeze Agent/Runtime/App rolling pre-main candidate, poms base, eight park heads; adopt inventory

**Dependencies; owner / tier:** Latest promoted [Plan 05](../05-remaining-fixes/plan.md) increment, including the integrated [Generation](../02-consistent-generation/plan.md) and [Concurrent Editing](../04-concurrent-edits/plan.md) work; N/Luna

**Reuse, focused evidence, and done condition:** Reuse existing `PK-0` inputs. Freeze immutable `BASES.tsv`, `ADOPT.md`, `NOTED`/exclusions and park SHA inventory; verify the four repos and exact ancestry. Do not freeze old main or obsolete `lane/M-GPU/integrated` as if final.

### PK-2

**Action and outcome:** PK-2 — installed core Hivemind, `04e74695...`; PK-3 — core/pack boundary guard, `ed04114d...`

**Dependencies; owner / tier:** Existing verified rows; already done

**Reuse, focused evidence, and done condition:** Reuse exact heads/results and namespace `c08c38e...` and schema `c02386e...` preps. No rebuild unless later composition changes the tested tree; PK-4 and PK-1 carry the specified installed Hivemind, schema, namespace and boundary checks.

### PK-1

**Action and outcome:** PK-1 — resolve hidden-name/schema-origin defects on integrated Agent

**Dependencies; owner / tier:** PK-0, PK-4, PK-1-NAMESPACE, PK-1-SCHEMA; N/Luna

**Reuse, focused evidence, and done condition:** Merge the reviewed PK-4 head into the frozen PK-0 Agent base, reusing its already-contained namespace/schema preparations; do not rebuild or blindly fast-forward divergent prep branches. Run explicit discovery/render/schema/core-boundary/Hivemind selectors in `cards/PK-1.md`; done when codemod and version origin behavior pass on final Agent base.

### PK-4-REPAIR

**Action and outcome:** PK-4-REPAIR — repair the demonstrated core/pack boundary contract

**Dependencies; owner / tier:** Verified PK-3 and preserved PK-4-a5 work; X/Terra + native Luna helpers

**Reuse, focused evidence, and done condition:** Preserve the four staged compatibility repairs and first-failure evidence. Trace actual core CLI callers through `astrid/core/cli/domain_timelines.py`, `cli_find.py`, `cli_log.py`, `cli_pending.py`, `cli_working.py`, `astrid/core/pack/imports.py`, `astrid/core/execution/generic_host_worker.py` and the transaction lock at `astrid/core/pack/transaction.py`. Resolve which code belongs in core/pack, preserve admitted-source identity/custody and safe lock semantics; never hide imports or bypass locks. The orchestrator must amend PK-4 FILES and the narrow boundary tests to include the demonstrated necessary repair **before retry**, retaining the old contract/evidence. Do not repeat a run that is forbidden from fixing its known cause. A proven coupled transaction race may get a separate S/Sol owner; missing FILES alone is not extreme difficulty. Done: original boundary/lock failure has a focused passing reproduction and actual CLI behavior remains available.

### PK-4

**Action and outcome:** PK-4 — complete the eight-park-input merge on PK-3

**Dependencies; owner / tier:** PK-4-REPAIR; N/Luna for mechanical composition, Terra retains semantic repair ownership

**Reuse, focused evidence, and done condition:** Reuse retained work and immutable park inputs. Run the exact authored ancestry/exclusion, guard/shrink, namespace/schema/Hivemind, moved-data, rendering and transaction checks; select no surrounding suites. Done: reviewed combined head has all original required outcomes and feeds PK-1; no unfinished source is discarded.

### PK-5

**Action and outcome:** PK-5 — installed CLI, boot conformance and `_core` resources

**Dependencies; owner / tier:** PK-1; X/Terra + Luna

**Reuse, focused evidence, and done condition:** Exact TEST selectors in `cards/PK-5.md`: `test_installed_shots_references_cli.py`, `test_installed_boot_conformance.py`, named Skills/MCP parity and package-data nodes, plus boundary guard. Done: installed wheel behavior and boot paths pass, selected resources stay packaged.

### PK-6

**Action and outcome:** PK-6 — loading/discovery/provenance plus accepted Agent health fold `47d67d8d13bcbf4ab437bc41ae6ec5b6cf60598b`

**Dependencies; owner / tier:** PK-5; S/Sol + native Luna helpers; Astra review

**Reuse, focused evidence, and done condition:** Merge the whole SF-accepted fold once as an explicit PK-6 input (or prove exact final-tree equivalence); never merge its SUPERSEDED members. Reconcile its 46-file API/import/schema/executor baggage with PK-3 namespace and PK-4 final guard. Run exact PK-6 TEST selectors plus only fold-changed public API, installed child and generic-host action nodes. Done: fold SHA/equivalence, all public behavior once, passive discovery, strict failure and provenance contract all evidenced.

### PK-7

**Action and outcome:** PK-7 — trust, secrets and validation

**Dependencies; owner / tier:** PK-6; X/Terra + Luna

**Reuse, focused evidence, and done condition:** Exact `cards/PK-7.md` selectors: declared-action secrets/credential scope, installed receipt provenance, external public API, pack validation/import review and hello pilot. Done: fail-closed trust boundaries with selected tests.

### PK-8

**Action and outcome:** PK-8 — source/API/transaction preconditions

**Dependencies; owner / tier:** PK-7; X/Terra + Luna

**Reuse, focused evidence, and done condition:** Exact source composition, selected-root, namespace and API surface checks in `cards/PK-8.md`. Done: admitted sources and commands preserve identity and custody.

### PK-9

**Action and outcome:** PK-9 — install/update/rollback/remove transaction

**Dependencies; owner / tier:** PK-8; S/Sol + Luna; LB-TXN

**Reuse, focused evidence, and done condition:** Existing `LB-TXN` reviews PK-8 + PK-9 before proceeding. Run exact transaction, artifact, CLI manage, digest, install/update/rollback and source setup selectors in PK-9. Done: transaction preserves user data on success, refusal and interrupted recovery; Astra review `BLOCKING: 0`.

### PK-10

**Action and outcome:** PK-10 — rendering, composition and lifecycle features

**Dependencies; owner / tier:** PK-9, LB-TXN; X/Terra + Luna

**Reuse, focused evidence, and done condition:** Exact moved-data, Runtime fixture, core-only render and selected rendering composition nodes in `cards/PK-10.md`. Done: new format renders on CPU with preserved receipts.

### PK-11

**Action and outcome:** PK-11 — registry/catalog integration

**Dependencies; owner / tier:** PK-10; S/Sol + Luna

**Reuse, focused evidence, and done condition:** Exact registry, selection and catalog selectors in `cards/PK-11.md`; done when declared packs resolve without untrusted/disallowed discovery.

### PK-12

**Action and outcome:** PK-12 — remaining pack management/API behavior

**Dependencies; owner / tier:** PK-11; X/Terra + Luna

**Reuse, focused evidence, and done condition:** Exact API/import/validation/CLI selector set in `cards/PK-12.md`; done when public APIs, lifecycle and project selection contracts pass.

### PK-13

**Action and outcome:** PK-13 — Runtime-side moved-data composition

**Dependencies; owner / tier:** PK-0; S/Sol + Luna

**Reuse, focused evidence, and done condition:** Runtime candidate from PK-0 rolling base; run exact `cards/PK-13.md` selectors and card lock/producer checks. Done: relocated data contract and Runtime lock source agree.

### PK-14

**Action and outcome:** PK-14 — App live browser loading, refresh/dispose and passive open

**Dependencies; owner / tier:** PK-13, LB-TXN, PK-9; S/Sol + Luna

**Reuse, focused evidence, and done condition:** Exact Vitest and two direct Playwright journey greps in `cards/PK-14.md`; vendor-lock check against PK-13 Runtime. Done: live effect appears, refresh failure preserves old effect, disable disposes, project-open is passive.

### PK-15

**Action and outcome:** PK-15 — Agent removes 19 named packs from core and regenerates locks

**Dependencies; owner / tier:** PK-12, PK-13; N/Luna

**Reuse, focused evidence, and done condition:** Preserve H3/RunPod/training in core as card states. Run explicit absent-pack, runtime-lock, moved-pack absent/core-boundary and core-only render/Hivemind/transaction selectors in `cards/PK-15.md`.

### PK-16

**Action and outcome:** PK-16 — poms_packs receives 19 packs and test assets

**Dependencies; owner / tier:** PK-15; N/Luna

**Reuse, focused evidence, and done condition:** Reuse poms base from PK-0; exact `test_pack_install_boundary.py`, `test_relocation_integrity.py`, `test_music_resolves_chiptune`, `test_video_editing_resolves_editorial_and_iteration` only. Done: every listed pack has `pack.yaml`/tests, installs via `packs add`, and relocation integrity passes.

### PK-17

**Action and outcome:** PK-17 — installed CPU journey and evidence map

**Dependencies; owner / tier:** PK-15, PK-16, PK-14; X/Terra + Luna

**Reuse, focused evidence, and done condition:** Exact `tests/proof/test_packs_cpu_journey.py` and PK-14 Playwright journey. Done: all 30 CPU-provable statements mapped, all deferred rows explicit, no product changes, installed effect journey succeeds.

### END

**Action and outcome:** END — review all rows and deferred boundary

**Dependencies; owner / tier:** PK-0–17 + LB-TXN; existing Astra review, round cap 3

**Reuse, focused evidence, and done condition:** Compare each immutable head/diff, exact evidence, failure/deferred list and ancestry against END items 1–14. Done: `BLOCKING: 0`; anything GPU/H3/training/K-census remains explicitly deferred.

### PK-BRANCH

**Action and outcome:** PK-BRANCH — publish immutable create-only candidate

**Dependencies; owner / tier:** END; N/Luna

**Reuse, focused evidence, and done condition:** Preserve `lane/M-GPU/packs-integrated` as the immutable Packs candidate branch. The only publication-card amendment before execution is to record the frozen rolling pre-main bases and authorize promotion of these same reviewed candidate heads by the initiative manager; PK-BRANCH itself does not write pre-main, open a PR or touch main. Verify source SHA equals reviewed pack head and handoff names exact tuple.

### PK-PREMAIN

**Action and outcome:** PK-PREMAIN — promote the reviewed Packs candidate

**Dependencies; owner / tier:** PK-BRANCH; N/Luna; required final tuple review already in END

**Reuse, focused evidence, and done condition:** PK-0/PK-1 build on frozen rolling pre-main, so do not build a second aggregate by default. Verify those targets are unchanged and promote the exact END-reviewed candidate heads by ordinary fast-forward/create. Required final tuple proof before END includes Agent guard/shrink, PK-17 installed CPU journey, namespace/schema/Hivemind, PK-9 transaction, PK-16 install/relocation/two dependency checks, Runtime source locks and App PK-14 live/dispose/passive-open journeys. If targets moved, Terra with Luna reconciles only affected candidates/checks under the existing scoped review, uses a fresh immutable lane, and preserves the old candidate. Create missing pre-main only from its explicitly frozen base and reviewed descendant. No main/force/PR.

## Shared execution boundaries

Use the [inputs and provenance](inputs.md) for historical identities, original card sources, and recovery limits. Do not treat this document as authorization to start product work. The root README owns status and owner. Preserve the original scoped checks, review cap, and publication conditions in the task cards above.
