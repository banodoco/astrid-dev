Date: 2026-11-24
Kind: issue
Source: Plan 88 owned-stack and CI triage run
Resolved by: —

A delegated baseline comparison included a render-smoke selector even though the run prohibited visual tests. The manager stopped the process when inspecting its command; partial output does not establish how far that selector ran. The remaining nonvisual comparison exposed default integration-lane deselections, which needed an explicit separate pass. The runner should enforce the run's allowed test categories before launching pytest and show excluded lane IDs with the comparison, so neither a prohibited selector nor an incomplete green file run silently passes through.
