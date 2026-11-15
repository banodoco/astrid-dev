**BLOCK — W171, candidate `f709407cb10cc56bafebae51080832386bca3a44`.**

Two Windows failures meet the generate-path gate. Both prevent the controller from completing a paid-machine claim. These are source-established findings; I did not reproduce them on Windows.

The inventory covers all **216 first-parent merges and 19 direct commits**. The source inspection was focused; unread areas are explicitly listed below. This is not full-range clearance.

**Coverage table**

“NOT COVERED” means no applicable earlier source-review verdict was established from the located evidence. A review of a narrow fix does not approve its entire ancestry. Grouped hashes share the stated coverage classification.

| Merge/commit | Lane | Earlier read: verdict and reviewed head | Coverage boundary / changed since read |
|---|---|---|---|
| `f709407cb` | Preparation-stop | W166 APPROVE, `16dbe5b41` against `a91c35dfd` | Final preparation source identical to reviewed head. |
| `9a8a3b634` | First-frame revert | W164 faithful-revert test evidence, `8d88fc7ec` | No earlier independent source approval established; composition checked here. |
| `a91c35dfd` | Release false-success | W148 APPROVE, `1da0d1528` against `079f66883` | Final donor `dcc99a752` adds refusal guidance; that delta read here. |
| `247335369` | First-frame addition | W118 APPROVE, `e5fcaa87d` against `941fca2a4` | Donor `b9e999b64` had documentation changes; addition subsequently reverted. |
| `9acb55b60` | Local idle release | W88 BLOCK, `730ae8089`; W102 APPROVE, `2ca1a8de1` | Final `f4d124717` changes empty-response handling and bounded release polling; delta and merge seam read. |
| `22ffe8483` | Engine snapshots | W113/W116/W119 BLOCK; W122 APPROVE, `4da516b` | Relevant snapshot/preparation source matches final donor `c3014413e`; no release-time snapshot added. |
| `cb1a336ea` | Verification witnesses/settings | W83 BLOCK, `ae4d0a58e`; W86 BLOCK, `9d15e5502`; W91 APPROVE, `622ba89381` | Final `6a6ab6f4d` includes the authorized default change. Checked under the standing rulings. |
| `ee14644a4` | Polling/source-digest memo | No applicable earlier approval located | NOT COVERED. W109’s later timing review does not approve this predecessor delta. Read here. |
| `f26c8127f` | Host recovery/spool | W84 BLOCK, `1505a379c`; W95 APPROVE, `9efa11620`; W104 APPROVE, `7e01b773a` | Core spool changes covered; composition with job evidence inspected separately. |
| `5193a2331` | Job evidence/marker publication | W81 APPROVE WITH CONDITIONS, `8cebc4e2a`; W87 BLOCK, `ec264e87b` | Final donor `7e553baf7` includes changes after those reads. Marker delta is comments; evidence changes inspected. Existing deferred rulings retained. |
| `87bcc78a7` | Claim authorization/cancellation | W77 BLOCK, `daed72ed7`; W78 BLOCK, `9e0d4313d`; W80 BLOCK, `1c08bd3c4`; W93 BLOCK, `b60438061`; W96 APPROVE, `3f67b3553` | W96 approves round-five delta only, not every earlier machine change. |
| `175102ea1` | Low-disk release/control channel | No exact earlier source verdict located for donor `23ed942aa` | NOT COVERED for the Windows control-channel boundary. Finding 1. |
| `c1789e4ba` | Runtime authority/publication | W63 inspected test conversions at `525e14859` | Test review does not establish production approval. Production delta read here. |
| `aef8647aa` | Publication classifier | W45 MERGE, `b4923c09` | Covered for classifier-only scope; later authority changes in `c1789e4ba` handled separately. |
| `d5d659d46` | Durable provider gate | W39a REQUEST CHANGES, `b0d7ff4c`; W44 REQUEST CHANGES, `ece1436d` | Earlier cancellation/custody review exists. Native Windows persistence was not established by that evidence. Finding 2. |
| `857c39557` | Lint ratchet | W40 APPROVE, `1d1cb25f` | Covered for the ratchet change. |
| `56a758c07` | Boundary vocabulary | W35/W35b; final APPROVE, `2e47f694` | Covered for scanner/vocabulary scope. |
| `1e1f3b4fe` | Observation transaction | W30 BLOCK; W33 accepted `ce797451b` constructor fix | Covered for that narrow lock-release correction. |
| `42ea55bac`, `22e5a13e5` | Warm retention | W33 REQUEST CHANGES, `d072cf5d`, `9e7b2a48`; composed checks at `913c6b8ff` | Substantially changed afterward. Existing host-loss expiry ruling not raised again. |
| `922a19ebb` | Terminal reconciliation | W33 REQUEST CHANGES, `56284e6c` | Later classifier and authority changes have separate coverage above. |
| `c473f7dc4` | Original provider gate | W33 REQUEST CHANGES, `f0535fef` | Superseded by later gate work; not treated as approval. |
| `1d9b6d9e6` | Storage-folder binding | Ledger records NO BLOCKER recheck, `43b69032`, after `b1830b9e` | Original correction covered; later layout changes are separate. |
| `a6f389027` | R12 integration | R12 base `0e1543e0` | Base incorporation; no new approval inferred. |
| `48b143081`, `9630bb844` | Pins/installer | G4 REQUEST CHANGES at `821956162`; REJECTED at `54556c6f` | Final `0f584c92` manager-reviewed; no subsequent independent approval located. Changed source and conflict hunks inspected here. |
| `87f835e76`, `ae1c608a7`, `176e5ba1f`, `326245663`, `4cf9341a8`, `2f45835a4`, `7f3408f7c`, `ce9f0cd7b`, `6e1c34e28`, `384ee1ff3`, `b4c6c7b31` | Machines: admission, storage, policy, listings | Later narrow reads listed above | NOT COVERED as complete individual merge deltas. Focused cumulative machine-path inspection here. |
| `c57814c81`, `05826d633`, `930445147`, `90ca0fa11`, `be56a08cd`, `f420803f3`, `66d03d734`, `0106598bb`, `6021f4b55`, `8197390a0` | Machines: preparation, transport, cancellation | No exact earlier verdict located for each merge | NOT COVERED as complete merge deltas; relevant final custody/dispatch paths inspected. |
| `ec036e6a3`, `673227271`, `bb0ae49da`, `877508686`, `ad3cf8a98`, `cff670337`, `7bca9853c`, `dd6da9992`, `e8bf7aad0`, `14fa999a7` | Machines: portability, expiry, claim/recovery | W33 and later narrow machine reviews provide partial ancestry coverage | Remaining changes NOT COVERED by an exact earlier approval. |
| `941fca2a4`, `c92108812`, `359f04c53`, `4fe335203`, `d1671e0e0`, `207559073`, `c395a9d70`, `e24853a88` | Engine: selection, schema, placement, logs | No exact final source verdict located for each merge | NOT COVERED; focused final preparation/dispatch inspection. |
| `520803167`, `db363d734`, `5865d8435`, `b3fe464db`, `75ac0d0c5`, `28f4b7775`, `cc8bc0b8c`, `e42d22163` | Engine: bridge, stop, upgrade, diagnostics | Ledger mentions upgrade reviews, without a located final approval binding every listed merge | NOT COVERED as complete merge deltas; ownership/upgrade changes inspected. |
| `22563540c`, `5f90c51c9`, `e09423230`, `defbbfd88`, `df4836383`, `283a3aa48`, `913c6b8ff`, `e7f00181b` | Engine: preparation/layout/startup | Storage-folder and later preparation reviews cover narrower portions | Remaining changes NOT COVERED by an exact earlier approval. |
| `bb89b3f2b`, `9ae69bf89`, `71f76ad24`, `8a10a6cb0`, `785df62b2`, `9e4f2306c`, `9e13628b9`, `3c111cbed`, `5f31797fb` | Dependency pins | Earlier G4 reads concern earlier heads | Changed since those reads. Final declared bindings inspected; seven existing file references matched their digests. |
| `d753a87df`, `9fc2ebdd8`, `055a18ad0`, `11118f644`, `dfd433fd1` | Video request/build/documentation | W118 covers the separate first-frame addition | NOT COVERED as these individual deltas; final request/build changes and revert consistency inspected. |
| `9c7db3f4a`, `08dad5f5f`, `e9778a599`, `3c3c4cc7a`, `5d9aced0e`, `19e7236be`, `e9f161892`, `58089bf07` | Audio defaults, recipes, source patches | Ledger records earlier patch review and BLOCK at `def11775` | Later heads changed; no blanket final approval established. Patch implementation exclusions below. |
| `060a7555e`, `64d76bfa5`, `fc4b36d43`, `d5bb25741`, `a76626175`, `12e0add6c`, `a77f58525`, `ddfefa609`, `0c44a6054` | Catalog and declared logs | G3 BLOCK reads: `49516887d`, `a648a1df` | Those parked bundle branches do not approve the replacement declared-log path. NOT COVERED; final collection/publication boundaries inspected. |
| `35ba632aa`, `ec5b1de91`, `357dc3b51`, `0a553819c`, `4696668d5`, `c474563da`, `ae0f284d2`, `bf3b6ba77`, `246cad0fd` | Structural receipts/diagnostics | No exact final approval located | NOT COVERED; receipt handling and combined conflict hunks inspected. |
| `8c0d7f03f`, `0bee45e5d`, `7ba479a73`, `8cf3ada99` | Installer/setup/update | Earlier G4 reviews only partially overlap | Changed/NOT COVERED; installer and update deltas inspected. |
| `46e40eb0a`, `017651122`, `11cf5544b`, `257cda90c`, `a00e5fe8a`, `8895139e9`, `fbdd8a5b5` | Declarations, collection, visibility, diagnostics | No exact final approval located | NOT COVERED as complete merge deltas. |
| `6ea94e00f`, `274b18e9d`, `542f545d0`, `6107b7b46`, `4be74fe94`, `890b1e1bd` | Initial generation/routing/catalog/launchers | Ledger acceptance is not an independently located source-review approval | NOT COVERED as complete merge deltas; focused generate-path reading only. |
| `10ae3e1df` | Failure-release correction | W52 REQUEST CHANGES, `728550590` | Final donor `4b0f55c0f` changed afterward; relevant release code inspected. |
| `f56376877`, `fd5ff0d90`, `d5ed51620`, `5cca0bcae` | Test-labelled merges containing product changes | W140 provides test/gate evidence for `acef27e45` | Not independent source approval. Product changes distinguished from test-only changes. |
| `079f66883`, `c6a631510`, `fdd535270`, `542bc5c0d`, `2e5dc8d28`, `a921b7dce`, `a045b00ee`, `980d4888b`, `dea1bd1be`, `ac3dc93a6`, `c61db4a82` | Tests/harness | No product-source approval inferred | No first-parent delta under `astrid/`; test internals not reread. |
| `a371431db`, `dd8ea822f`, `e51723152`, `95cbb0e19`, `14ad09684`, `475c2dade`, `540ac409d`, `3ff2cc648`, `7762a0111`, `70b052fc8`, `a4d893c8f` | Tests/harness | Same | No `astrid/` delta. |
| `d8c116f18`, `f6e32cf82`, `31f19f1f1`, `78d01b137`, `c8436b544`, `b91a21842`, `4b17ae7ee`, `88c88c114`, `a53d11d19`, `21dacd488`, `65b1d45c6` | Tests/harness | Same | No `astrid/` delta. |
| `c9636ed41`, `c79f3ce07`, `05c8ab767`, `9b3c6022b`, `1e94061c8`, `95d9e8768`, `a66574c8a`, `65cd88659`, `27a58fac5`, `05346e9fd` | Tests/harness | Same | No `astrid/` delta. |
| `58442e7a0`, `e51cfee34`, `bd59f32e2`, `1feb10a6b`, `f4ec941dc`, `2b6c49639`, `79d0cd3f4`, `016d46e6b`, `1706f4ce8`, `994cd75d9` | Tests/harness/generated artifacts | Same | No `astrid/` delta. |
| `4dec04bbd`, `1f69f754e`, `48d868dac`, `6f304c485`, `75c11a007`, `67b96b54d`, `f2cc94b5f`, `e489a207f`, `30a644bce`, `65630ff96` | Tests/harness/preflight | Same; narrower ratchet/vocabulary reviews noted above | No `astrid/` delta. |
| `efc3b44cf`, `5dae0cfe1`, `013f01e6a`, `9f9db742e`, `a94c1902d`, `df60b917b`, `a9851cc82`, `e329efd16`, `a935c968b`, `501d7a9ee` | Tests/harness/install inputs | No product-source approval inferred | No `astrid/` delta; not a claim that build inputs are irrelevant. |

The 19 direct first-parent commits also belong to the range:

| Commits | Lane | Earlier coverage / boundary |
|---|---|---|
| `f9214240c`, `dd5bc8223`, `b306b2be7`, `6eacb0776`, `4ca9cdbf8` | Pins, patch declarations, installer pin resolution | Changed since earlier G4/patch reads; final bindings and relevant resolution code inspected. |
| `64e00c285`, `fc063698b`, `878d13f46`, `eeeee9ef5`, `c627edbab` | Diagnostics, receipts, installed-state checks | No exact earlier approval established; focused cumulative inspection. |
| `72fbdf65c`, `cffffe056` | Command output and task logs | No exact earlier approval established; final log path inspected. |
| `f1a487c99`, `e6d857667` | Capacity waiting/provider observations | Earlier machine reviews provide partial coverage; no independent approval of each whole commit inferred. |
| `5f531504a` | Capability registration | Manager-approved ledger correction; no independent source verdict located. |
| `77632da90`, `6c9efd1ae`, `cdc1774ae`, `0560e34d0` | Test, lint and naming maintenance | No separate product approval inferred; no tests run here. |

W109, W124, W126–W152 and W160 do not collectively approve A′. Several concern subsequent timing/optimization work or another candidate. W167 and W169 are design reviews, not implementation approvals.

**Findings**

1. **BLOCK — Windows cannot construct the paid-machine owner.**

   `astrid/packs/runpod/release_control.py:99` unconditionally calls standard-library `os.fchmod`. Python 3.11 exposes that function on Unix, not Windows. The release’s Windows CI explicitly selects Python 3.11 at `.github/workflows/ci.yml:34`. [Python 3.11 documentation](https://docs.python.org/3.11/library/os.html#os.fchmod).

   `RunPodLeaseOwner` unconditionally constructs this server at `astrid/packs/runpod/worker_owner.py:168`, before claim/recovery proceeds. A Windows user with otherwise valid configuration therefore gets an exception during owner construction and cannot claim the machine needed for generation.

   Introduced by `4b61f1272`, integrated through `175102ea1`; unchanged in A′. Use the supported native permission implementation for this descriptor and its reader.

2. **BLOCK — Provider-gate persistence independently fails on Windows.**

   `astrid/packs/runpod/provider.py:196` opens the parent directory with ordinary `os.open`; on Windows, the missing `O_DIRECTORY` becomes zero. The Windows CRT rejects opening a directory this way with `EACCES`. The exception escapes `_replace_state`. [Microsoft CRT documentation](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/open-wopen).

   New or changed gate state reaches that write at `astrid/packs/runpod/provider.py:288`. Claim binds the account gate before discovery/create at `astrid/packs/runpod/target_selection.py:800`. Thus, after fixing finding 1, a fresh Windows claim still fails at gate initialization; subsequent pacing-state writes have the same defect.

   Introduced by `0a212484cd`, integrated through `d5d659d46`; unchanged in A′. Directory durability needs the platform-aware implementation.

No additional new NOTE findings are proposed. Existing deferred rulings were not promoted back into blockers.

**Composition checks**

- Inspected combined production conflict hunks in `247335369`, `9acb55b60`, `913c6b8ff`, `19e7236be`, `e9f161892`, `48b143081`, `4696668d5`, `c474563da`, `fbdd8a5b5` and `246cad0fd`. `a91c35dfd` itself has no combined production hunk.
- Final `astrid/packs/h3_av` matches the pre-first-frame tree at `9acb55b60`. Searches of Markdown/YAML documentation and guides found no remaining instruction to pass `first_frame` or an image-only keyframe.
- Final `managed_preparation.py` matches `16dbe5b41`, the W166-reviewed preparation-stop head.
- No additional blocker established in these seams.

**What I did not read or prove**

- I did not read every uncovered production hunk line by line. In particular, the complete `generic_host.py`, `remote_placement.py`, `worker_preparation.py`, CLI/catalog/default-selection and asset-alignment diffs were not exhaustively covered. Their relevant custody, admission, dispatch, collection, recovery and preparation boundaries received focused inspection.
- I did not independently audit the complete bundled speech implementation patches, every generated workflow/lock/catalog asset, or all implementation changes inside pinned dependencies.
- I did not reread already-covered snapshot, spool and other implementations in full where the relevant source matched the reviewed head.
- I did not read every test body, historical test log, superseded implementation or unchanged R12 file. The referenced original G3 findings file was unavailable; its ledger summary was available.
- No native Windows execution, installation/uninstallation, live upgrade, GPU generation or provider behavior was tested. No test suite or individual test was run.
- No credential files, `.env` files or `~/.codex` were read.

Fetched origin, inspected the detached candidate, made no tracked edits or pushes, and removed `/home/user/wt/w171-a` after confirming it was clean.