# A-2 W cache-witness caller evidence

This offline bundle records one instrumented W CLI trial and its warmup from `run/a2-witness-W`, plus the caller analysis from `run/witness-callers.md`. Source revisions were Agent `2ec9c24123a69916fe726023e2eede4c3386b1ce`, Runtime `182311f9d363712c0339254bd27e091d0e18318d`, and VibeComfy `799d90f619a6723d0b376b7e77aef09c244a0821`. The original manifest, target inventory, stdout/stderr, target receipts, teardown receipt, and observer/runner/test scripts are copied without edits. The two large raw event JSON files are stored as deterministic gzip streams; their decompressed SHA-256 values were checked against the source files. No event fields were redacted or rewritten.

## Files

- `manifest.json`, `target-inventory.json`: full run provenance and CPU fixture node inventory.
- `W-plain-warmup.*`, `W-plain-1.*`: stdout, stderr, target prompt receipts; witness event logs are `*.witness.json.gz`.
- `teardown.stderr`: teardown receipt.
- `witness-callers.md`: completed caller report.
- `witness_probe.py`, `witness_runner.py`, `run.sh`, `astrid`: observer and source runner/CLI launcher.
- `verify_probe.py`: probe parity test script, retained as evidence but not rerun during this staging task.

## Process and findings

The source runner starts a disposable, launcher-managed Runtime fixture and an attached CPU target stand-in, then invokes the W workflow CLI. The warmup and one measured task both succeeded; Runtime admission and target prompt receipts are matched in the manifest and per-trial target JSON. Teardown returned 0. The CLI probe eagerly imports instrumented VibeComfy modules, wraps `cache_file_witness`, records call stacks, elapsed call time, and before/after metadata tuples for allowlisted paths, and writes events at process exit. It does not retain file contents. Temporary fixture paths are anonymized by the probe; source checkout paths remain in the event stacks and manifest.

The measured capture contains 9,256 witness calls: 2,350 checks of absent `CURRENT` and 6,906 checks of present files. The nearest Astrid frames attribute 8,888 calls to `sdk/generation.py:2001` (`emit_bundle`), 360 to `_writable_node_bindings` during input description, and 8 to `bundle.compile`. These are call counts, not hash counts or time saved. Metadata before/after tuples matched, including the absent file; that does not prove file bytes stayed unchanged. The accompanying report describes the common VibeComfy `consume.py` stacks and code-inspection limits.

## Overhead and limits

This is an observer-instrumented run. Eager imports, stack collection, metadata stats, and JSON event capture add overhead. No matched uninstrumented W control was collected for this witness observer, so its overhead is unknown; captured call durations and wall time should not be treated as uninstrumented costs or savings. The separate SHA observer run cited in the caller report is not a paired measurement of this witness trial.

The evidence is one CPU fixture W trial, not a GPU or production run. It does not establish byte stability from metadata equality or prove that no safe optimization exists. Existing VibeComfy reader/provider caches re-witness files to detect mutation; a stat-only substitute is not validated. The caller report characterizes the observed route and code inspection, not every possible safe implementation.

## Sanitation and staging checks

The raw event paths may include local filesystem checkout paths, retained as requested. Neither source files nor staged files produced matches for targeted scans of bearer authorization headers, loopback host:port authorities, and quoted API-key/token/secret/password assignments; match values were not printed. The scan does not establish absence of arbitrary sensitive material. No local authority or credential contents were added. No probe, runner, test, timing run, `.env` read, or repository edit was performed for this staging task.

The two compressed event files decompress to byte-identical source JSON (SHA-256 comparison). Existing files elsewhere under `run/a4-evidence-staging` had the same combined path/content digest before and after staging: `fdf0da417ce52280438afa30cf10b288f84b676a3a5aaef770d0a53c1e534b96`.
