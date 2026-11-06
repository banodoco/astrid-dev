# Tasks — Continuous agent learning integration

[Plan](plan.md) · [Inputs](inputs.md). **Proposed work only; routes, owners and focused proof selectors TBD at authorized implementation start.**

| ID | Bounded output | Dependency | Focused evidence |
| --- | --- | --- | --- |
| AL-1 | Select one creative workflow and baseline no-knowledge/raw-search task results; map existing Agent skill and tool hooks | None | Recorded task/environment/repo identity and grounded evaluation fixtures |
| AL-2 | Agent read adapter and contextual `find/inspect`-equivalent with explicit source/capability boundary | AL-1; existing Hivemind read API or verified Plan 22 contract | Matching and mismatching environments, evidence/citation, stale/contradicted result and access-denial cases |
| AL-3 | Private knowledge candidate from exact observed Runtime/action receipts, independent of live project state | AL-1, AL-2 | End-to-end actual outcome, version pins, local persistence, no private upload |
| AL-4 | Opt-in sanitized proposal with separate user authorization and dataset editorial acceptance | AL-3; verified contribution API | Approve, reject, retry, redaction and no-leak tests |
| AL-5 | Agent reuses the earlier lesson in a new session; UI surfaces provenance and feedback if warranted | AL-2, AL-3, AL-4 | Compare quality/time-to-useful-action with baselines; present negative/uncertain evidence honestly |

Keep this separate from protocol migrations (Plan 22) and from pack distribution changes (Plan 06). A routine retrieval hook should be context-triggered rather than a mandatory broad search before every trivial operation.
