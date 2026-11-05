# Inputs: Pinokio qualification

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

These are historical observations from the source audit recorded 4 Nov 2026, not live execution bases. Re-resolve all identities at PIN-0.

| Repository | Recorded base / observations | Retained work / donor status | Candidate and destination |
|---|---|---|---|
| `banodoco/astrid-pinokio` (`https://github.com/banodoco/astrid-pinokio`) | Clean checkout `f8f1077eea22a729f7fe68b88acc1e4963495e18`, local `ci-smoke`, upstream `origin/codex/astrid-updater-only-20261028-pinokio`. Observed refs: `origin/main` `bbba620`; `origin/codex/astrid-updater-integration-20261028-pinokio` `34d6416`; `origin/codex/tst-pinokio-20261028` `1df7e67`; `origin/feat/pinokio` `5cea465`. | Checkout is evidence only; none of these branches is authorized as a donor. Compare chosen base with Task L environment work and retained donor heads; historical reports do not prove changes exist at `f8f1077`. | Candidate branch: **TBD**. Intended destination is user's `pre-main`; existence and current head were not established. Resolve repository/remote identity, target base, and ordinary create-or-fast-forward policy before mutation. Do not infer that `origin/main`, `ci-smoke`, or the updater branch is the destination. |

If composed into the Astrid product tuple, freeze then-current reviewed Agent, Runtime, and App pins. Completing Packs is not a dependency. Task L came from a separate `astrid-pinokio` checkout; its interface and validation documents are requirements/reference, not proof on this checkout.

## References and evidence

| Source | What it establishes | Identity or link | Limits |
|---|---|---|---|
| Task L interface and validation documents | Focused launcher/lifecycle contract and eventual 12 native checks | Separate historical `astrid-pinokio` checkout | Its tests/CI do not prove this checkout. At the recorded audit, `ci_journey.py` raised for non-direct modes and `journey_fully_local.py` was not wired into the workflow. Known render-smoke omission, manual-only fully-local journey, and upstream diagnostics hint are revisited only when a changed boundary or qualification owner selects them. |
| M4-4a Pinokio engine research | Internal request/event boundary | `pinokiocomputer/pterm@5be43718701c448b43daf0ce51d8935f170065bb`; `pinokiocomputer/pinokiod@add4a674ad1ba95bb62ec427fce519fe5bf0e9bf` | Queued acceptance is not settlement; disconnect or exit code zero is not success. No general terminal task readback is evidenced. Does not establish deployed version or supported action-engine invocation surface. |
| M4-6 historical Agent implementation | Source-backed, fail-closed provider report | Commit `98fc9af5752216ba298e34daa094435f8117a3b6`, on branch based on `64e18fb6b6812e04732f0bedd75e6e0f251ee6a9`; separate observer commit `4e60a4b249ddd4a4d2478ad3637127158a94aefc` | Not a reusable product release, authorization path, or proof current Q/Agent interfaces match. Reconcile with current owners/heads. Historical provider had no success-producing authorization path. |
| Plan 07 | Predecessor launcher and gate | [Plan 07](../07-pinokio/plan.md) | Start only after Plan 07 is done and from its verified launcher/gate. |

## Constraints

Native Stop/Quit refusal veto remains unproven. Adapter-side lifecycle ordering, fake kernel tests, POSIX child fixtures, and pinned historical engine source cannot establish deployed veto behavior. Historical local paths in copied material are sanitized; these references are not current evidence.
