# Inputs and provenance

## How to use these identities

The SHAs below are exact historical observations or retained source identities recorded in the historical source audit. They are provenance, not presumed current refs, accepted publication donors, current running status, or authorization to start work. Re-freeze current heads and destination refs when product work starts; use the actual reviewed retained worktree or immutable refs. If a repository has no current `pre-main`, record that absence and use frozen `main` as merge base.

## Historical base observations

- Agent: `01eceda02e58a1940ada4a261f4789539d6f0a56` — pre-main observation.
- App: `878c28df7a6c80fa9aaa6540c5fccad95473e7c1` — pre-main observation.
- Runtime: `9fc53b771134940aaac901e4cfc5d03c1db1a20a` — pre-main observation.
- VibeComfy: `e2905d068d5851b9c32856d32b8251852a01d6dd` — main; no pre-main observed.
- Lifecycle: `db79345536985c701b7aff2eb5eec36667aae204` — main; no pre-main observed.

These audit-time bases are historical only. Integration consumes exact promoted Plan 01 Agent/App heads and accepted completion outcomes, then freezes the actual rolling `pre-main` at execution. When VibeComfy/lifecycle still lack `pre-main`, explicitly record that and use their frozen `main` as merge base.

## Retained and conditional inputs

- **Agent PINS candidate:** `1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`. Retain its implementation; the task is candidate-only proof and acceptance, not rebuilding broad selectors.
- **Agent DEFAULTS donor:** `9d3bb24831676cbfc2a0d3dd1c7769f1937569c3`, merged with PINS at unpublished checkpoint `3fe46b90e4081b20bfb5e6face00520eddafbebd`. The checkpoint is incomplete and unaccepted; `astrid/sdk/generation.py` and `tests/core/generation/test_cli_gold_075b.py` remain unfinished/uncommitted per audit.
- **VibeComfy donor:** `1b2e242ce7396442c85395d3220a2481216b57c1`; audit composition base `e2905d068d5851b9c32856d32b8251852a01d6dd` (observed main).
- **Lifecycle donor:** `c47fa76be6e7c0aa661d044a0de5b3b73f6fdbac`; audit composition base `db79345536985c701b7aff2eb5eec36667aae204` (observed main).
- **Possible Runtime stop/ownership donor:** `b005394b06602c84e2abd4ba7eec8fa2f1dd8e94`. Include only if source comparison proves the retained included Agent behavior depends on it; otherwise preserve the current Runtime source. Historical composition base `9fc53b771134940aaac901e4cfc5d03c1db1a20a` (observed pre-main).
- **Older verified Agent comparison:** `620a3fd5146fed9f623a2f7101c40c4279f03516`, pins VibeComfy `1b2e242...`, Runtime `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373`, lifecycle `db79345536985c701b7aff2eb5eec36667aae204`. It is not a shortcut or automatic input: it predates retained PINS closure/asset/receipt repairs and selects older dependencies.
- **App:** no generation feature donor. Retain the Installer Consent candidate and refresh canonical Agent/Runtime manifest and lock against the final reviewed heads.

## Existing decisions and provenance limits

- PINS cancellation exit `143` had no final pytest summary, so it is neither acceptance nor a product failure. The audit reported 231 generation checks, 28 asset/installed-child checks, and pin/recipe/ancestry/source-policy investigation as reusable local evidence; fresh native Linux x86_64 closure and the specified candidate-only proof remain required.
- Two supplemental bootstrap checks failed before assertions because distribution metadata was absent. If this recurs, repair that specific test setup rather than unrelated product behavior.
- DEFAULTS is an unpublished local merge, not passed work. A prior static contract required real managed Qwen readiness without model bytes, while readiness requires a receipt and three locked model files. No installed execution occurred. Replace that contradiction with the narrower honest proof described in the task details; do not weaken readiness.
- The original candidate tuple used Runtime `b005394...` in the PINS lock, but final Agent/App locks must be regenerated against the actual final reviewed producer heads. Do not ship stale historical locks.
- Audit-time pairwise merge probes recorded 20 conflicting paths for Agent `620a3fd...`, 22 for PINS `1608db...`, and one for VibeComfy; Runtime stop merged cleanly in its then-current-base probe. These are historical pairwise observations, not bug counts or a tested sequential aggregate.
- Keep separate Runtime CAS `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373`, lease `33e9195a8ac57c4ba61f372ef6f25139c37eaa97`, healthfold `2870…`, and custody `103f97803f7f391e2c810ebdf086f798326cd75a` deferred unless a separately named included dependency is proven. Do not substitute custody-chain `103f978...` for Runtime stop.
- The historical inclusion rationale remains at [INCLUDING-GENERATION.md](../../references/INCLUDING-GENERATION.md). It is supporting audit evidence, not another plan or active task list.

## Composition and publication boundaries

Use a unique immutable create-only candidate lane per touched repository, for example `lane/M-GPU/increment-02-generation-<run-id>`; do not overwrite or depend on fixed historical `lane/M-GPU/integrated`. Compose producers first (VibeComfy, lifecycle, any required Runtime stop), then Agent, then App pin/lock refresh. Preserve valid ancestry and Installer Consent protections; resolve conflicts only in already changed files with focused behavior checks. Do not salvage by extraction/cherry-pick. Promote only exact reviewed immutable candidate heads to current `pre-main` using the existing release procedure, and recapture/reconcile if a frozen base moves. No new approval stage is introduced.

No broad suite, unrelated baseline repair, ARM project, general hardening, concurrent editing, Packs, or unproven full model execution enters this increment. Installer 01 is the required predecessor for final composition/publication, not for all preparation. The full managed-generation journey remains deferred. At normal task setup, recover the exact retained card/check identities and evidence from the referenced source evidence and retained run materials: the complete card corpus and logs are not bundled in this documentation set. This setup is part of the existing tasks, not a new approval gate. A named test file does not authorize running its whole suite; use only selectors already designated by the retained cards, and do not invent missing node IDs.
