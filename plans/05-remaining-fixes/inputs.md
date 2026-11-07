# Inputs: Release fixes integration

[Plan](plan.md) · [Tasks](tasks.md) · [Project status and owner](../index.md)

## Starting code

The accepted SF receipts and donors below are historical references, not a frozen Plan 05 base. The plan consumes the exact promoted Plan 02 integration and Plan 04 heads. No later Plan 05 destination base was frozen in the supplied audit; after predecessors promote, freeze then-current `pre-main` for each repository that the inventory selects for change.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Candidate branch | Intended destination |
|---|---|---|---|---|
| `astrid-agent` | TBD at start: exact promoted Plan 02 integration and Plan 04 tuple and current `pre-main` | Host-cancel `aff7686d0f6e6314dd5531600d173bbd265e437e`; generation extras `9c06b674dfe27d513eccc528e14fb423cf3a1881`, `7ab6aa10859b19bc3b13cf90966cc0da18026c68`, `9d6af90b1ae4bd4a7afd346942c07e57f75201c7`; RunPod owner `aee88cb87c4acd249023d16f096bce5f40c1b6f9`; Agent fold `47d67d8d13bcbf4ab437bc41ae6ec5b6cf60598b` is owned by Plan 06 PK-6. | TBD at start; isolated immutable candidate | `pre-main`, only after review |
| `astrid-runtime` | TBD at start: exact promoted Plan 02 integration and Plan 04 tuple and current `pre-main` | CAS `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373`; Runtime fold `287042b2426f7465a1fba77bba075766f18f26b1`. Do not substitute custody `103f97803f7f391e2c810ebdf086f798326cd75a`. | TBD at start; isolated immutable candidate | `pre-main`, only after review |
| `VibeComfy` | TBD at start: exact promoted Plan 02 integration and Plan 04 tuple and current target | Boundary test `1ac3b91fedf4a15842ff655442869569d4855396`; accepted test-only change, eligible only if absent. | TBD at start; isolated immutable candidate if changed | `pre-main`, only after review |

The RunPod-owner donor is in `astrid-agent`; do not infer a separate lifecycle repository change. No candidate branch name or later base SHA is supplied. Verify each actual target at setup, use isolated candidates, and promote only exact reviewed heads under the [shared run contract](../../skills/astrid-dev-shared/run-contract.md). The Agent fold is consumed once by Plan 06 PK-6, not merged here. Do not merge a fold together with its superseded members.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| Accepted SF receipts | Two accepted source receipts used for the ledger | `83f39c24e731fe199efa60bb2f5a262c9d4a871b` and `1c4cab15b614336c752f44976c8b283ca9b36667` | Historical evidence; neither receipt freezes this plan's later destination base. |
| SF host-cancel | Host-cancel fix donor | Agent `aff7686d0f6e6314dd5531600d173bbd265e437e` | Historical donor; compare changed behavior and preserve current receipts. |
| SF VibeComfy rank 9 | Independent boundary-test donor | VibeComfy `1ac3b91fedf4a15842ff655442869569d4855396` | Test-only change; no product rewrite or broad emitter sweep. |
| SF generation extras | Installed-boundary, generation ID/listing, and SDK fixture donors | Agent `9c06b674dfe27d513eccc528e14fb423cf3a1881`, `7ab6aa10859b19bc3b13cf90966cc0da18026c68`, `9d6af90b1ae4bd4a7afd346942c07e57f75201c7` | Reconcile once with Plan 02 integration. Freeze exact affected test nodes from immutable donor diffs at task setup. |
| Runtime CAS and fold | CAS donor and seven-file Runtime fold | Runtime `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373`; `287042b2426f7465a1fba77bba075766f18f26b1` | CAS is not automatically a generation dependency. Compose on post-CE Runtime; keep CE complete and do not reopen it. |
| RunPod owner | Owner/custody donor | Agent `aee88cb87c4acd249023d16f096bce5f40c1b6f9` | 23-file production delta. CPU behavior remains in scope; live-provider outcome is unproved and no provider/GPU run is authorized here. |
| Agent health fold | Fold assigned to Plan 06 | Agent `47d67d8d13bcbf4ab437bc41ae6ec5b6cf60598b` | 46-file production ancestry, not tests-only. Plan 06 PK-6/END must close this plan's outstanding record. |
| Parked H3 sources | Explicit parked production exclusions | Agent `d88a1c69e45fb5d2e729e449d4b2c1b8062b6956` and `ed985e81bbdf8e5b0535cf10ce28e1196ab56145` | Preserve source reasons; no GPU/model readiness claim. |
| Already-covered case-matrix | Source-published packet and original remote/evidence proof | `c7073ff98a2b456ee1aca065d2d473962271d94e` plus superseded-member records in donor manifest | Source publication is not proof of Plan 02 integration and Plan 04 pre-main inclusion. No product merge of the packet is required. |

## Constraints

- Every accepted ledger member receives one inclusion/equivalence/deferred record. Preserve exact source identities and replacement/fold mappings; do not merge superseded originals alongside their fold.
- The listed test paths are selectors, not authorization for broad suites. M-00 derives exact `FILES` and nodes from immutable diffs and named contracts; no wildcard selectors.
- Use only existing review/publication authority: scoped independent Astra review, fresh immutable candidates, exact reviewed heads, remote receipt, and no force. Do not publish empty changes for already-covered repositories.
- No provider or GPU work. Explicitly retain any live-provider result that cannot be proved. H3/GPU exclusions are not completed CPU features.
- Plan 05 completes at SF-PROMOTE and records the Agent fold as transferred to Plan 06 PK-6, which establishes inclusion or equivalence.
