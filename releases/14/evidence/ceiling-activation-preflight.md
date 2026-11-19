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
| Installed Windows tuple | Plan 39 AT4 owns the Windows task-host journey. The Lead must reconcile the installed App, Agent and Runtime identities against the reviewed expected pins in both shell cells. The existing run records sibling checkouts. [Journey workflow](https://github.com/banodoco/astrid-agent/blob/68e7aa85/.github/workflows/windows-journey.yml) |
| Trusted workflow and overall coverage | The Lead owns reconciliation against the full required-check manifests and the delegated checks. The owner supplies the Agent gate-owner variable. Activation still requires the trusted default-branch workflow and policy, followed by a verified rejected unapproved workflow edit. The global inventory remains unknown. [Activation prerequisites](https://github.com/banodoco/astrid-dev/issues/984) |
