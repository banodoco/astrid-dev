# Head-busy refusal after a clip-bearing commit (Release 15, 23 November 2026)

Found while running Plan 78's live proof on an isolated install (Agent `64cecdae9f679537f4a6dc82e5102e53b6943ef7` = `release/15/main` `b324d7c1` plus Plan 78; Runtime `737843e9cb92c565c266452dde540832ee2c745b`). Not caused by Plan 78 or the motion pack: a new project of plain titles reproduces it.

- `diag.md`: the diagnosis (mechanism, timings, runtime.log lines, controls, minimal repro in section 4).
- `generate.py` and `hist-detail.py`: the two small scripts of the repro (`LE4_PANELS=40` for the 40-title case). They need the isolated install's Python and data root (the paths are the ones of the proof stack: replace them); the read reports the SDK refusal details.

Status: the confirmation (pausing the pack host for 20 s during a read) is run separately; its result is added here when it exists.
