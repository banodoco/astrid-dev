# Using the Plan 59 work ("Into the Minkhole") from another machine

State as of 16 November 2026, 21:30 UTC. Everything below is on the branch
`release/14/plan-59` of each repository under `github.com/banodoco`. Nothing is
in any `release/14/main`, and nothing is published as a release.

## 1. The branches

| Repository | Branch | Head | What it carries |
| --- | --- | --- | --- |
| astrid-agent | `release/14/plan-59` | `cd058eb09` | Everything listed in section 2 |
| astrid-app | `release/14/plan-59` | `f3619a18a` | Clip placement in the editor (black bars) |
| astrid-runtime | `release/14/plan-59` | `e6106ac07` | Clip placement schema |
| timeline-composition | `release/14/plan-59` | `e628744bf` | The placement function; package 0.0.19 |
| VibeComfy | `release/14/plan-59` | `79143f24e` | Transcription workflow, output node, pinned Whisper node |
| runpod-lifecycle | `release/14/plan-59` | `93beec314` | Provider-side shut-off deadline on a rented machine |
| astrid-dev | `release/14/plan-59`, `release/14/plan-60` | `5b3ae2b7`, `471dfdc` | The plan records, current to 16 November |

The Agent branch pins the others: Runtime `e6106ac0`, VibeComfy `79143f24`,
runpod-lifecycle `9f88ef7` (same content as its plan branch), and composition
package 0.0.19 as a vendored archive (sha256 `536f8a91…ace7e5`) in both the
Agent and the App. Use the six plan branches together; do not mix one with a
different branch of another.

## 2. What is on the Agent branch, and how far each piece is proven

| Work | Proven by | Not proven |
| --- | --- | --- |
| Importing the rough cut; a clean composed frame; a short render | Tests; used daily in this work | An installed release build |
| Clip placement: one function decides where a clip sits; fit per clip; old projects converted once (`astrid timelines appearance`) | Four independent reviews; editor preview, composed frame and export compared pixel by pixel on the owner-approved cut | An installed build of all three parts together; old timelines with no canvas size are rendered as before with a warning, not converted (astrid-dev#770) |
| Reviewing a render of part of a timeline (`astrid timelines visualize --render-run … --at T`) | Two independent reviews; 173 focused tests; compared with a full render at seven moments | — |
| `astrid hivemind search` and `item` from a source install | Independent review; live searches | — |
| H3: real footage of any size and frame rate accepted; Pika speed-up LoRA as default; removed repeated checks | Independent reviews; tests without a GPU; **one real take on a rented RTX 5090 (16 November)**, composed and structurally verified by Astrid | The spoken words, voice and lip match of that take (with the owner); only plain continuation has run on a GPU; the take ran on commit `5ae4e172`, which is part of this branch, not on the branch head |
| Rented machines: shut-off deadline sent with the rental request; on-machine watchdog that can arm | Independent review; tests with the provider stubbed; one real machine accepted the deadline | Whether the provider enforces the deadline, and how fast |
| Timed words: `astrid timelines transcripts run / import / show`, transcription entry in `astrid generate`, skill page | Its own independent review; 52 focused tests; offline workflow compile | **Never run on a real machine**: model, node loading, transcription quality, storage |

## 3. Known failing tests on the Agent branch

- The four H3 tests that failed after integration were fixed with an independent
  review and are merged (`cd058eb09`).
- The failures that exist on untouched Release 14 are listed in astrid-dev#757.
  Do not "fix" them by editing the tests.

## 4. Setting up

- **To read, edit or test code, or to use the editor and timeline tools:** a
  source checkout of the six branches works. Bring-up from source has friction
  that is written up in astrid-dev#758 (prerequisites, the Node version the
  renderer needs, the browser-door port). A Runtime binds to the source it was
  started from: restart it after changing commits (astrid-dev#759).
- **To run generations on a rented GPU: a source checkout is not enough.** Astrid
  refuses RunPod generation without an installed copy whose release manifest
  names the exact commits the rented machine must fetch. The recipe that
  produced the first take is in `RUNPOD-PILOT-RUNBOOK.md` (with
  `RUNPOD-REHEARSAL.md` for the checks to pass before paying): install from
  pinned commits into an isolated home (astrid-agent
  `docs/setup/local-source-install.md` for commits that are not released), import
  the project archive, save the network volume in preferences, run the
  rehearsal that rents nothing, make one waiting claim, submit, read back,
  release. The installer downloads pinned tool sources from
  `codeload.github.com`; make sure that host is reachable.
- **Renting a machine:** use `astrid machines claim` and let it wait for capacity
  (`--capacity-timeout`), on a network volume; pass a spend cap and a deadline;
  release as soon as the work is verified. Single-shot claims
  (`--no-wait-for-capacity`) fail often and say only "capacity" (astrid-dev#782).

## 5. The film project itself

The owner-approved rough cut (the Matrix shots filling the frame) was exported
through Astrid as `approved-rough-cut.astrid` (231 MB, sha256 `54e14d8d…59bf`).
It currently exists only on the machine this work ran on; it has not been put
anywhere another machine can fetch it. The original archives are in the
handover repository's `timeline-v1` release and do not include the approved
crop. Decide where the approved archive should live before another agent
continues the edit.

## 6. Not on the plan branches yet

- `p59/h3-claim-preflight` (astrid-agent): `astrid machines claim` refuses to
  rent when the install cannot submit. Under review; not safe to use yet.
- `p59/h3-capacity-diagnostic` (astrid-agent): keeps the provider's own words in
  a refusal. Folded into later work.
- Fixes for the four failing H3 tests.
