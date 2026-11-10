# Release 12 P20 Agent R3 receipt

On 10 November 2026 the remaining independent R3 round (round 2 of 2) reviewed
Agent `e28a509b6bd8c352514d4b4cc14c95628a8302e7`. The integration merges
P20 `d2a84370fa620c6649f765b486285b14d699c86a` and Plan 32
`d28cac1902328836acce35230517a19c137ecd55`. The prior round and follow-up
coverage are recorded in [the handoff](handoff.md#task-and-review-state). The reviewer
found no blocking integration issue: the five files changed by the merge match
the Plan 32 parent, and the previously reviewed P20 guide, pack and selection
implementation is preserved. The reviewer inspected TTS prompt normalization,
receipt checkpoint custody and the generic-host callback. Four changed
receipt/callback cases passed. The mirror and README checks passed.

The manager's exact-candidate guide, setup-pack, setup-branch, selection,
opt-out and package-data checks produced **57 passed, 1 failed**. The failure,
`test_retained_integrations_flow_through_existing_sync_selection`, lacks the
`media` and `understanding` descriptors and failed identically on the exact
P20 base `d2a84370f`. The setup mirror and README rendering checks passed, and
the guide's quoted installer success and failure prefixes were checked against
the candidate's `astrid/installer/outcome.py`. Phase-1 `6fb1d5861` is an
ancestor. Published-revision quotation proof remains required after release.

The reviewer's broader invocation was incomplete (46 passed, 3 failed). Two
entry-contract tests expected `target` rather than `placement`; both reproduced
on `d2a84370f`. The third, the fake RunPod claim with idle values 15/60,
exhausted its fixed deadline in the reviewer run, but passed on both the base
and an exact-candidate rerun. This is an intermittent test limitation, not a
claim of a fully green run. No timeout was changed. No GPU or hosted journey
was run; those remain separate release and post-publication requirements.
