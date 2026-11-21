# Agent #442, 08:37 UTC

**The four-shard comparison is complete.** Both 66c5ee27712d36c583eaf9c39fd62269fbc44f41 and f0283b919d5584fb2c6773d91a6b7090f98a4d8f ran the same 2,067 integration cases. All eight artifact digests match GitHub. Each pytest event stream finished, and each matching complete command recorded raw exit 1. The final current shard has 517 IDs, 1,488 phase reports and SHA-256 11429ae5ce89c5c65572769fe00a2c8108cece85bf59643b6c7ff5fc63cee8bd. [Current final shard](https://github.com/banodoco/astrid-agent/actions/runs/44675925731/artifacts/14613536164) · [Candidate final shard](https://github.com/banodoco/astrid-agent/actions/runs/44635028242/artifacts/14597461360)

| Native observation | Current 66c5 | Candidate f028 |
| --- | ---: | ---: |
| Distinct IDs | 2,067 | 2,067 |
| Recorded phases | 5,952 | 6,056 |
| Setup pass / fail / skip | 1,818 / 248 / 1 | 1,922 / 144 / 1 |
| Call pass / fail / absent | 1,520 / 298 / 249 | 1,572 / 350 / 145 |
| Teardown pass | 2,067 | 2,067 |

Every current ID and phase is retained. Exactly 104 additional candidate call phases are present. All 104 selected S01 setups fail on 66c5 at the provider-managed edge refusal, their calls remain unexecuted and their teardown passes. All 104 setups and teardowns pass on f028, with 53 passing and 51 failing calls. The final 26 contribute five passing and 21 failing candidate calls.

Outside S01, one current failing call passes on f028, the historical shared-redo source-archive acceptance case. Two current passing calls fail on f028, the Python child-host five-second discovery guard and image-True parent-media final store-integrity assertion at line 325. The separate exact Linux discovery trials all passed. Both exact macOS isolated parent-media controls returned clean deep integrity reports; the original hosted failure and its unobserved integrity entry remain open. [Current shard 1](https://github.com/banodoco/astrid-agent/actions/runs/44675925731/artifacts/14607895616) · [Current shard 2](https://github.com/banodoco/astrid-agent/actions/runs/44675925731/artifacts/14604213387)

Three original public-document cases remain red with a later first failure on f028: compound inverse, plus sequential swap/residual patch with False and True. They are outside S01. On b1 and 66c5, the shared fixture stops constructing its compound source when a provider-managed edge is rejected at _doc_patch.py:372. On f028 the fixture reaches _public_document_compound at test_authoring_media.py:690, then the test's SimpleNamespace lacks _capture_bundle at sync.py:461. Keep these downstream assertions unqualified. These failures were in shard 4. [Candidate](https://github.com/banodoco/astrid-agent/actions/runs/44635028242/artifacts/14591926983) · [Current](https://github.com/banodoco/astrid-agent/actions/runs/44675925731/artifacts/14607286078) · [Frozen reference](https://github.com/banodoco/astrid-agent/actions/runs/44635920236/artifacts/14596445927)

The [full per-case archive](442-current-four-shards-all.json.gz) and [104-case S01 subset](442-current-four-shards-s01.json.gz) include the native artifacts, digests, phase outcomes, first failures and source locations. The full archive encodes two absolute fixture parameter values with a reversible POSIX-root marker and includes hashes of the original IDs. SHA-256 digests for the compressed files follow.

| Archive | SHA-256 |
| --- | --- |
| Full | `d792425384318b371c7ae984b63f96c556ea32a7e7a5eb2da6f2d30766021c08` |
| S01 | `8fe1dece48d13d71011f921077cb7ff7e4e2cd7d14cb30a492e1f496e1911970` |

The Lead returned #442 to the existing writer for publication and qualification of the exact reviewed fixture commit. [Rework decision](https://github.com/banodoco/astrid-agent/pull/442#issuecomment-7034688483)
