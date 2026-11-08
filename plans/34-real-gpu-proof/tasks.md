# Tasks — Real-GPU proof of generation

[Plan](plan.md) · [Inputs](inputs.md)

A draft outline. Exact commands and the candidate SHAs are set when Plan 32 lands (owner, 8 Nov: no pass on Plan 33's route). Every task spends money: it needs the owner's go and a budget, and a pod census before and after.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| G1 Wipe and fill the storage volume; VibeComfy smoke per slot | N | Plan 32 review passed; $25 approved (owner, 8 Nov); account balance checked | One pod in the volume's datacenter, running VibeComfy's own commands (`prepare`, `fetch`, `run`) per slot workflow | Each workflow produces an output or a recorded real-hardware failure; the volume holds the models | [ ] |
| G2 Astrid route on the Plan 32 candidate | N | G1 | `astrid generate --placement runpod` for image, edit, voice, music and sfx, then h3_av on the Matrix clip | Each output is recorded and sent to the owner; models are not re-downloaded; a warm pod is reused; the census ends empty | [ ] |
| G3 Route failures | N | G2 | The plans' tasks files | Each failure becomes a row in its owning plan (a repair task on Plan 32's line, fixed and re-run live) | [ ] |
| G4 Second pass after Plan 32 | N | Plan 32 complete | The same matrix on the one path, locally where hardware exists and on RunPod | As G2, plus local outputs | [ ] |
