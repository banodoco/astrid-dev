**BLOCK — W172, A′ `f709407cb10cc56bafebae51080832386bca3a44`.**

Three findings meet the card’s gate. The historical decision at `decisions.md:255,429` deliberately replaced the parked G3 redactor with unredacted declared logs. This verdict applies the current card’s explicit **secret leak in shared evidence** gate.

All source references below are at A′.

1. **BLOCK — Declared failure evidence preserves secrets, including credentials already known to the host.**

   [generic_host.py:6501](https://github.com/banodoco/astrid-agent/blob/f709407cb10cc56bafebae51080832386bca3a44/astrid/core/execution/generic_host.py#L6501) writes child output into the full log **before** redacting the separate diagnostic tail. The full logs become declared outputs at `generic_host.py:10809`. Thus tail scrubbing does not protect the files users attach.

   The common collector copies bytes without redaction at `astrid/core/_shared/run_logs.py:243,259`; receipt retention copies them again at `astrid/packs/runpod/failure_receipt.py:368`. These paths preserve printed provider keys, download tokens, authorization headers, credential-bearing URLs, private-key blocks, environment dumps and named home paths.

   Two additional exposure paths:

   - `failure_receipt.py:203,293,438` copies and renders the first issue message without another scrub.
   - `failure_receipt.py:369,454` stores and prints absolute local log paths. `astrid/core/generation/cli.py:808` prints the retained log contents verbatim.

   **Offline evidence:** eight synthetic member payloads covering job streams, doctor streams, preparation output, engine output, preparation JSON and generation JSON survived collection and receipt copying unchanged. A small oversized-log fixture retained secret-bearing head and tail text. This establishes the export-boundary failure; I did not find an actual credential in the supplied nine-file example.

2. **BLOCK — The doctor support-bundle redactor misses token-only URL userinfo.**

   [doctor_bundle.py:24](https://github.com/banodoco/astrid-agent/blob/f709407cb10cc56bafebae51080832386bca3a44/astrid/core/gateway/doctor_bundle.py#L24) requires `user:password@`. A plain-text Git error containing `https://<token>@github.com/org/repo.git` survives `redact_log()` and enters the support ZIP through `doctor_bundle.py:295`.

   **Offline evidence:** a synthetic, realistically shaped token in that URL form survived; the `user:password@` control was removed. This also affects the four supplemental engine-install artifacts using this redactor at `astrid/packs/runpod/remote_placement.py:686`.

   Tests cover password-bearing userinfo, bearer values, JSON credentials and PEM blocks, but not this URL form: `tests/core/gateway/test_doctor_bundle.py:19`; `tests/packs/runpod/test_remote_placement.py:360`.

3. **BLOCK — A log-only download failure turns completed generation into failure.**

   The success manifest covers **every file under `out`**, including collected logs: `astrid/packs/runpod/remote_placement.py:391`; `astrid/packs/runpod/machine.py:451,456`.

   Success then uses one shared fetch at [machine.py:1082](https://github.com/banodoco/astrid-agent/blob/f709407cb10cc56bafebae51080832386bca3a44/astrid/packs/runpod/machine.py#L1082). Its per-file download at `machine.py:1201` propagates log transfer errors exactly like generated-output errors. The failure-log fallback preserves that exception rather than returning the completed result.

   **User-hittable trigger:** generation succeeds, but downloading a large declared log times out or exhausts local storage. Logs permit up to 256 MiB each.

   **Offline evidence:** a filesystem fake downloaded a valid synthetic output, then raised a timeout only for `logs/engine.log`. The shipped fetch function raised; the shipped machine runner returned no successful result and invoked release with `success=False`. This proves outcome coupling, not a provider-release failure.

4. **NOTE — Aggregate collection bounds remain incomplete.**

   Ready-to-paste `deferred.md` row:

   | Item | Source |
   |---|---|
   | W172: Bound declared-log reads before allocation and apply one aggregate evidence deadline. Collection reads the whole selected slice before its 256 MiB truncation; local evidence and host uploads remain synchronous before cleanup/settlement. Extend the existing W2 evidence-budget item. No additional user-hittable billing/custody failure established by this review. | A′ `astrid/core/_shared/run_logs.py:243`; `astrid/packs/vibecomfy/local_job.py:188`; `astrid/core/execution/generic_host.py:12747,13574`; existing `releases/13/deferred.md:151` |

The producer trace is:

| Evidence | Producer and protection at A′ |
|---|---|
| Pod `job.stdout`, `job.stderr`, generation JSON | Declared by `machine.py:469`. Collection and retention have no common scrub. |
| Host job streams and tails | Full streams written raw at `generic_host.py:6504`; known-secret tail scrubbing follows at `:6506`, with secret values supplied at `:10836`. |
| Engine log/startup log | Raw pipe bytes appended at `engine_custody.py:923`; declarations at `:871,881` and `job_evidence.py:106`. |
| Doctor, pip, fetch and node/Git preparation output | Whole stdout/stderr saved at `managed_preparation.py:806`. Raw remote install streams also fetched at `remote_placement.py:659`. |
| Exception strings and tracebacks | Generation CLI applies credential-pattern scrubbing at `cli.py:886`, backed by `contracts/errors.py:36`. This is partial producer protection, not a bundle-wide boundary. Remote command tails are interpolated at `remote_placement.py:600,752`. |
| `h3.preparation.json`, plan and compilation | Declared at `h3_av/extensions/vibecomfy.workflows/hooks.py:122`; request values and asset paths serialized at `shared/prepare.py:471,512`, `shared/stages.py:132` and `shared/compile.py:863`. No export scrub. |
| `request.json` in the supplied attachment | Contains request input directly. It is not among the hook’s five declarations; I did not establish how that separate example file was assembled into the attachment. |
| `job-run.json` / collected `run.json` | `job_evidence.py:128,142` writes measurements, timestamps, booleans and diagnostic notes; no environment snapshot. |
| Timing records | `execution/phase_timing.py:66` emits stamps and phases; observed phase labels are copied at `:48`. No environment scrape. |
| Storage inventory | `model_storage.py:311,341,350` includes filesystem paths and mount information without identity redaction. |
| Supplemental install diagnostics / doctor ZIP | `remote_placement.py:686` applies `doctor_bundle.redact_log`; ZIP logs use it at `doctor_bundle.py:295`. This protection does not cover ordinary declared logs. |

**Unreadable/oversized members:** declared-log read failures become missing rows (`run_logs.py:261`), but oversized members export raw head/tail slices. There is no fail-closed redaction boundary. The doctor ZIP skips unreadable logs and redacts bounded tails (`doctor_bundle.py:214,287,295`); supplemental install diagnostics read the entire source before redacting (`remote_placement.py:690`). No dedicated full environment-snapshot member was found in the traced declarations or supplied example. Printed environment dumps can nevertheless pass through ordinary logs.

**Failure-domain result:** failed-job log collection catches ordinary errors and preserves the original failure (`machine.py:1167`). Host-refusal collection registers its observer before transport and bounds it by 120 seconds and remaining paid time (`machine.py:1102`). Reset/release follows collection; the machine runner invokes release in `finally` (`machine_run.py:132`), and receipt writing occurs afterward. Reset failure routes to exact release (`machine.py:1516,1571`). I established the successful-output failure in finding 3, but no additional collection-exception path bypassing release.

**Earlier manifest-refusal blocker: fixed.** `managed_sources.py:72` rejects userinfo and query strings; `:50` renders invalid repositories as `<invalid>`; mismatch messages use that projection at `:98`. `tests/packs/runpod/test_managed_source_root.py:13` explicitly checks both userinfo and `?token=` cases.

**Test assessment:** existing failure-log tests assert byte preservation, truncation and digest handling, not secret removal for each member type. The traceback test covers `token=` and `api_key=` (`test_failure_traceback.py:38`). Doctor tests cover several realistic syntactic forms, but do not establish protection for every G3 member.

I read the relevant decision entries, prior W87/W109 reviews, all nine supplied example files, and the producer/collector paths above. I did **not** audit every upstream dependency, third-party node, provider implementation or possible log message; the original report at `/home/user/wt/briefs/review-g3bundle-findings.md` was unavailable. No pytest suite or live flow was run. Two tiny stdlib probes used synthetic fixtures and shipped/AST-extracted functions.

No provider calls, credential-file reads, tracked edits or pushes. The worktree was verified clean and removed; temporary fixtures were removed, and no environment was created.