# Release 14 ceiling activation evidence, 19 November

Two independent readers matched the Runtime native reports to their selected test identities at `97321788`. These receipts resolve the observed counts for the two jobs below. [Activation issue #984](https://github.com/banodoco/astrid-dev/issues/984)

| Runtime job | Agent checkout | Selected and reported | Native outcomes | Pytest exit |
| --- | --- | ---: | --- | ---: |
| [Nightly integration](https://github.com/banodoco/astrid-runtime/actions/runs/44462380084/artifacts/14504397024) | `0e1543e0da2215db9cb3320cfd1083174c3c62a9` | 667 | 498 call passes, 121 call failures, 28 setup errors, 20 setup skips | 1 |
| [Darwin native](https://github.com/banodoco/astrid-runtime/actions/runs/44462380054/artifacts/14505142580) | `4866090edcce7df31d1f0e03cf2354b878e94105` | 21 | 20 call passes and one declared strict XFAIL for `installed-pair-source-closure` | 0 |

Each selected ID had one primary outcome and a teardown report. Nightly's collection-only list matched its execution inventory in order and matched the 667 seeded identities. The Darwin seed contains zero entries for this lane. The Darwin XFAIL appears as a skipped call with `wasxfail`. The two jobs used different Agent revisions. Their combined count does not establish release-tuple qualification. [Runtime seed](https://github.com/banodoco/astrid-runtime/blob/97321788/ci/evidence/p39-k2-k3/seed-summary.json)

| Remaining work | Owner and evidence |
| --- | --- |
| Agent integrations and Darwin | P39-13 reconciles all four integration shards on its exact submission. The Lead compares the results against the sealed inventory and reviews Darwin separately. Destination Darwin collected 55 IDs and executed none. Candidate Darwin reported all 55, with 42 passes and 13 failures. [Integration run](https://github.com/banodoco/astrid-agent/actions/runs/44535552341) · [Darwin artifact](https://github.com/banodoco/astrid-agent/actions/runs/44535765805/artifacts/14537431686) |
| App Direct Journey | The Lead owns #316. Retain IDs, failures, retries and checkout identities from both Direct Journey and three-products when the queued jobs finish. [Plan-39 sync run](https://github.com/banodoco/astrid-app/actions/runs/44563320327) |
| Installed Windows tuple | Plan 39 AT4 owns the Windows task-host journey. The Lead must reconcile the installed App, Agent and Runtime identities against the reviewed expected pins in both shell cells. The two shell artifacts also prove the source pins selected by the installer, as detailed below. [Journey workflow](https://github.com/banodoco/astrid-agent/blob/68e7aa85/.github/workflows/windows-journey.yml) |
| Trusted workflow and overall coverage | The Lead owns reconciliation against the full required-check manifests and the delegated checks. The owner supplies the Agent gate-owner variable. Activation still requires the trusted default-branch workflow and policy, followed by a verified rejected unapproved workflow edit. The global inventory remains unknown. [Activation prerequisites](https://github.com/banodoco/astrid-dev/issues/984) |

## Installed Windows evidence, 19 November at 19:37 UTC

Both shell cells of [run 44462370880](https://github.com/banodoco/astrid-agent/actions/runs/44462370880) executed the real installer from App `de7dd1e6`. Each install step succeeded after comparing the installed-root Agent and Runtime records against the complete corresponding records in the served manifest. In both artifacts all four installed-profile binding checks passed. App plan-39 at `0700e981` declares the same two pins as the installer used in this run. [Installed-root comparison](https://github.com/banodoco/astrid-agent/blob/68e7aa85/scripts/ci_windows_journey.py#L403-L427) · [Plan manifest](https://github.com/banodoco/astrid-app/blob/0700e981/public/install-manifest.json)

| Shell | Installer App checkout | Selected and verified installed Agent | Selected and verified installed Runtime |
| --- | --- | --- | --- |
| [Windows PowerShell](https://github.com/banodoco/astrid-agent/actions/runs/44462370880/artifacts/14502544860) | `de7dd1e6` | `9814193a` | `6855dfa8` |
| [PowerShell 7](https://github.com/banodoco/astrid-agent/actions/runs/44462370880/artifacts/14506254222) | `de7dd1e6` | `9814193a` | `6855dfa8` |

The harness ran from Agent `68e7aa85` and checked out sibling Runtime `2537fed2`. The App SHA identifies the installer script. Health and pack-host readiness passed in both jobs. The installed CLI rejected the top-level packs command, so discovery and SDK settlement still block AT4. P39-27 owns the qualifying two-shell journey. [Activation finding](https://github.com/banodoco/astrid-dev/issues/984#issuecomment-7020193721)

## App journey inventory

The #316 comparison accounts for all 59 selected native identities and their Playwright attempts on both exact trees. Each side executed 48 distinct cases. The same concurrent edit failed on both, and eleven later serial cases were never assigned a worker. Those eleven have no execution result. The trusted Node recorder and the original PT5 failure remain open. [Native receipt, source commits and job links](app-journey-census/README.md)

## Trusted default-branch preparation

The three product defaults lack both reviewed files. For each repository the Lead prepared a local two-file patch for `.github/workflows/gate-integrity.yml` and `scripts/ci/protect_gate_paths.py`. Each applied cleanly to its default, passed workflow lint, accepted an unchanged tree and returned exit 1 for the unapproved protected-file change. [Exact file blobs, candidate trees and patch digests](gate-bootstrap-preflight.json)

| Product | Current default | Reviewed plan-39 source |
| --- | --- | --- |
| App | `de7dd1e6` | [0700e981](https://github.com/banodoco/astrid-app/tree/0700e981) |
| Agent | `959da732` | [68e7aa85](https://github.com/banodoco/astrid-agent/tree/68e7aa85) |
| Runtime | `6855dfa8` | [97321788](https://github.com/banodoco/astrid-runtime/tree/97321788) |

The current default and plan-39 branches report no effective protection on all three products. The trusted workflow fetches its checker from the current default branch. Production activation requires protecting that policy source or reviewing and qualifying an immutable binding, then confirming the hosted verdict covers the exact PR head. The accessible variable inventories contain no gate-owner roster. The owner's existing instructions reserve the Agent roster and product-default changes before release qualification. An authorized organization administrator must verify organization-level workflow enforcement. Release-branch required checks remain within the Lead's delegation after their prerequisites are met.

## Outcomes through 22:37 UTC

- The restored Agent wrapper executed 2,067 integration IDs, including all 2,064 sealed G1 IDs. The complete per-phase ledger retains the failures, setup errors and original exits. The landed `b1e53baf` reference has its own CI and Lanes in flight. The S01 writer owns the combined 104-case fixture qualification against that reference. [Census](agent-integration-collection/README.md) · [Landing](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7023657159)
- App #316 recovered all 59 expected journey outcomes on `75daac1c`. The trusted collector normalized all three jobs. Its 855 error entries matched the prior #319 verdict, with four missing IDs, 850 unregistered observations and the first binding mismatch. P39-28 owns the protected census of all fifteen differing bindings, the 824 observed passes and 26 Linux skips. [Disposition](https://github.com/banodoco/astrid-app/pull/316#issuecomment-7024224908) · [Source-bound census](app-native-inventory/README.md)
- The corrected Windows driver ran on the original installed App `de7dd1e6`, Agent `9814193a` and Runtime `6855dfa8`. Both shells passed discovery, settled one chiptune task through the SDK, verified both outputs and found zero remaining Astrid processes after shutdown. The newer-tuple run explicitly requests the separate App installer `f915d469`, which selects Agent `b1e53baf` and Runtime `2537fed2`. Its native results are pending. [Windows PowerShell receipt](https://github.com/banodoco/astrid-agent/actions/runs/44622336995/artifacts/14580595589) · [PowerShell 7 receipt](https://github.com/banodoco/astrid-agent/actions/runs/44622336995/artifacts/14580021483) · [Newer tuple](https://github.com/banodoco/astrid-agent/actions/runs/44627849962)
