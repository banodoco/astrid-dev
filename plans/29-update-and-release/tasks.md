# Tasks — One update path and release

[Plan](plan.md) · [Inputs](inputs.md)

| Task / outcome | Route | Depends on | Focused proof | Progress |
| --- | --- | --- | --- | --- |
| UR-1 One decision table for every update surface | N | — | Table test over install type × situation, including the negative cases in the plan | [ ] |
| UR-2 Releases 9 and earlier never show an enabled Update now | N | UR-1 | Table rows for release ≤ 9 and for no identity | [ ] |
| UR-3 Show the real refusal reason | N | UR-1 | Each Runtime reason renders its line; an unknown reason renders as needs repair | [ ] |
| UR-4 Remove setup block from update surfaces and the status section | N | UR-1 | Surfaces render the command, not SetupBlock; the status section has no actions | [ ] |
| UR-5 Fully-local and Pinokio memory | N | UR-1 | A dev:local page shows its own command; the Pinokio memory comes from `identity.managed_by` | [ ] |
| UR-6 `release-guard` and protected App `main` | N | — | A PR changing pins or `public/install*` without +1 fails; any other change to `release` fails | [ ] |
| UR-7 Make Update now work | X | — | Agent test runs the Runtime's real update request through the real `update_job.main()` | [ ] |
| UR-8 Runtime always gives a reason | N | — | Status sets `reason` whenever `available` is false; anything unclassified is `needs-repair` | [ ] |
| UR-9 Hosted update through the button path | X | UR-7 | The per-OS update leg is a door POST from the installed candidate to a stand-in next release | [ ] |
| UR-10 One pin tool; release only by bump PR | N | UR-6 | `pin.mjs` leaves `release` unchanged; `update-manifest.mjs` and stale baseline files removed | [ ] |
| UR-END Publish release 10 | N | all | Completion evidence in [plan.md](plan.md#completion) | [ ] |

## Task details

### UR-1 One decision table for every update surface

- **Outcome:** each update surface calls the existing `resolveUpdate`. That covers Settings → Updates, the update notice, the connection panel and pill update cards, the recovery banner and the chat update cards. Settings → Updates is the one place to act; other surfaces show the same primary or "See updates". Install type comes from `identity.managed_by`, plus the `dev:local` page flag. The `originless ⇒ source` guess is removed.
- **Table:**

| Situation | Primary | Secondary |
|---|---|---|
| Normal install, release ≥ 10, available | **Update now** | command / copy for agent (collapsed) |
| Normal install, busy or updating | Update now, disabled, "try again shortly" | none |
| Normal install, release ≤ 9, no identity, `autostart-off` or `unsupported-service-manager` | Update now, disabled, with the reason | command / copy for agent, **expanded** |
| Normal install, unfinished update (release ≥ 10) | **Update now** | command |
| Normal install, `needs-repair` | none | repair command (plain install line), expanded |
| Pinokio (either mode) | **Update in Pinokio** | none |
| Fully local (normal install) | text: `npm run update` in the Astrid folder | none |
| Source checkout | text: update your checkouts | none |
| Installed newer than astrid.haus | none | none |

### UR-7 Make Update now work

The Runtime sends helper action `reconcile` first (astrid-runtime `astrid_runtime/update.py` around :261-265, in every pinned Runtime since `c0e5c4a`). The installed Agent's `update_job.main()` rejects it as unknown (astrid-agent `astrid/installer/update_job.py` around :2065-2067). So every in-app update refuses. A handler exists unmerged: Agent `b97c43db8`, on `lane/M-R1FIX/R-15-R29`. Merge it, and add the contract test named in the table. The button can't be repaired for installs on releases 9 and earlier, because the helper runs the installed release's own code; UR-2 covers those.
