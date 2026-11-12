Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (smell 5; usability 1; task T11)
About: Plan 20; Plan 37
Outcome: open

A fresh install cannot generate until someone creates a project: the first `generate` is refused with "project is required for generation", and neither the RunPod skill nor the generate examples mention creating one. Workaround: `astrid projects create setup --name Setup --select`. Wanted: a default project from install, or `generate` uses one and says so. Fits Plan 20 P3.1 (the skill's generation half) and Plan 37 G4 (destination resolution).
