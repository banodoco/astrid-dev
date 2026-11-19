# App plan-39 Direct Journey census for #316

Each side selected the same 59 native identities. The compressed receipt reconciles the Playwright IDs, original attempt indices/statuses and ceiling-reporter identities with the job checkout logs and command journals. Rows identical across both executions are stored once. The archive is 6,030 bytes, SHA-256 `813f43864d10f59bae6e8ae71eb1d31ad1e07f87dce914a955042146cfebe2da`. [Receipt](direct-journey-by-id.json.gz)

| Job | Native outcome on each side | Playwright exit | Outcome-check exit |
| --- | --- | ---: | ---: |
| Direct Journey | All 45 passed at retry 0 | 0 | 0 |
| Three products | Two passed at retries 0 and 1. Concurrent edit failed at retry 0 at `three-products.spec.ts:571:26`. Eleven serial IDs had a skipped retry-0 placeholder, no assigned worker and `finished=false`. | 1 | 5 |

The three-products finish record says 14 selected and 11 pending. Both sides have 48 distinct executed cases across the jobs. Identity and attempt coverage are available for the census. The eleven missing executions, PT5 failure and trusted-verdict hold remain open. [Tracker](https://github.com/banodoco/astrid-dev/issues/984)

| Source | App checkout and verified tree | Playwright reports | Native ceiling streams and controller receipts |
| --- | --- | --- | --- |
| Plan-39 destination `0700e981` | `9191f610`, tree `27492a7b`, exact destination tree from the prior PR run | [Direct](https://github.com/banodoco/astrid-app/actions/runs/44458988949/artifacts/14499657393) · [Three products](https://github.com/banodoco/astrid-app/actions/runs/44458988949/artifacts/14499813121) | [Direct](https://github.com/banodoco/astrid-app/actions/runs/44458988949/artifacts/14499996603) · [Three products](https://github.com/banodoco/astrid-app/actions/runs/44458988949/artifacts/14499209039) |
| Candidate `cb5193ea` | `b72438eb`, tree `cd6d80a6`, exact candidate tree from #316's PR run | [Direct](https://github.com/banodoco/astrid-app/actions/runs/44563320327/artifacts/14557295719) · [Three products](https://github.com/banodoco/astrid-app/actions/runs/44563320327/artifacts/14557307158) | [Direct](https://github.com/banodoco/astrid-app/actions/runs/44563320327/artifacts/14555034544) · [Three products](https://github.com/banodoco/astrid-app/actions/runs/44563320327/artifacts/14557511574) |

Both jobs on both sides checked out Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c` and Agent `9814193a73f606719e81883a8be197d27dd361d4`. The workflow blob was `532317d1ff6dd0b663ac8027a23e71b9d5b2b98b`; both Playwright configs, the capture and reporter code, skip guard, outcome checker and declared-failure file were also byte-identical. Each source was workflow attempt 1. [Destination workflow](https://github.com/banodoco/astrid-app/blob/0700e981be5dfbfc229784b8ade69869f62716dd/.github/workflows/direct-journey.yml)
