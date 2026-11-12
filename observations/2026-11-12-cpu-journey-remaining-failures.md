Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (failure 14; task T13)
About: Plan 50
Outcome: open

After the Runtime fix the CPU journey is 21 passed, 3 failed, 2 errors: "host graph cleanup remains unresolved", "bounded pod operation deadline expired", "the cancelled machine was not released", and receipt `unavailable` versus `not_collected`. The synthesis reads two as stale tests and one as a first-claim deadline; not yet classified test by test. Plan 50 RB-1 needs the journey green before it can gate anything.
