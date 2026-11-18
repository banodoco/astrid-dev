# Stability first, or tied to extensibility? And what ships with Release 14

18 Nov 2026. Read-only; nothing was built or run. This follows `fable-save-category-design.md` (the five invariants, N1 to N12) and uses `sonnet-commit-profile-r14.md`, which has now landed.

**A correction first.** I had inferred that the commit itself was about 1–2 s and that most of the 12 s was elsewhere. The profile measured about 9 s in the commit, 67% of it in `_legacy_exemptions` → `_reference_basis` (deep copies per declaration), which is removable and is being fixed. It also measured an import waiting 5–7 s on `store._mutex` behind a commit. So a save in progress does delay an upload; the failure itself was still the cut connection, not the wait.

## Answer

**Separable, and stability goes first.** The dependency runs one way only: extensibility needs the stable base, and the stable base needs nothing from extensibility. Plan 18 already orders it that way (TL-1 waits for CC-3, CC-4 and CC-7). What I recommend changing is its standing: make Phase 0 a project with its own owner, its own release and its own "done", and do not start Phase 1 until it has held on the owner's timeline.

**A version of it does ship with Release 14:** the *behaviour* (no endless retry, one bar, Discard always works, no lost reply, a drop survives a save). The *structure* that makes those impossible to break again changes what is stored and what goes over the wire, and that belongs in Release 15.

---

## 1. Separable or tied?

### The three places they touch

| Touch point | Does it force interleaving? | Why |
|---|---|---|
| **TL-5** (the document is the head plus the queue replayed) | **No** | Stability needs only the Phase 0 form: one row per timeline, holding one display copy. CC-5 already replaces the before-and-after equality check with continuity by intent (`OutboxBasis {after: id}`), so a new edit can queue behind a waiting one without TL-5. TL-5's end form removes one stored copy and nothing the owner would notice. |
| **TL-10** (drops) | **Split it** | TL-10 is two things. "A dropped file is a record in the queue, sent again if cut" is stability. "A drop is a named command" is extensibility. The first moves into the stability project as a new task; the second stays. |
| **CC-3** (`register_rule`) | **No** | Phase 0 registers built-in rules only. Packs get the hook in TL-1, onto a gate that already exists and is already proven on old documents. That is the right order. |

Two smaller ones move for the same reason: TL-7's rule "a field commits when the edit ends" (already N7 today), and TL-4's "the badge is a function of one state" (already in the rewritten CC-5).

### Should the stability project own TL-5?

**No.** TL-5 is the heart of the command layer: one `sendIntent`, an operation per gesture, and with TL-6 to TL-11 about 60 days of conversions. Pulling it forward would make "stability" a 90-day project and delay the result the owner wants now. With TL-10's upload half moved in, the stability project completes all five invariants in the form a person can observe. What remains for Phase 1 is deletion of a copy.

### What extensibility first would cost

- **Every conversion is built against code that is then deleted.** TL-6 to TL-11 convert each gesture through the handoff (1,082 lines, 68 `refuse(` sites), the eight-status session and the nine-kind classifier. Each converted gesture is a new path through the space that produced today's sixteen incidents, and its tests would encode that behaviour.
- **Every pack rule can refuse an old document.** Without the delta gate, a pack's rule judges the whole head. That is I-11 again, once per pack, and the pack's author cannot fix it.
- **The generated gesture matrix (TL-15a) would be generated twice**, once with `retryable` and once with the four outcomes.
- **The owner cannot edit dependably for the length of Phase 1.** Sixty days of new commands on a save path that sticks.

### Recommendation

Keep it inside Plan 18, as Phase 0, because one cause should have one home and TL-1 already depends on it. Name it **"Phase 0: dependable saving"**, give it an owner and Release 15, and gate Phase 1 on its end-state checks **and** a week of the owner editing "Almost Ready" without a stuck state.

---

## 2. What the stability project contains

| Task | What | Route | Days | Change from today's plan |
|---|---|---|---|---|
| CC-7 | The corpus, plus two new shapes: a selection whose lifecycle advanced; a head with many audio sources | N | 3 | two shapes added |
| CC-1 | Counters and the one ratchet file, plus object GETs per gesture and the three scans | N | 3 | counts added |
| CC-2 | Close what CC-1 shows red. Starts from the r14 profile: `_reference_basis` if it has not landed, then the per-read deep copies, digests and the ancestry walk | X | 4 | named starting point |
| CC-3 | The rule registry and the one delta gate; input guards signed the same way | X | 4 | one sentence |
| CC-4 | **Four outcomes.** The reply carries `outcome`; one decoder; every mutating route; `send(): Outcome` is the only reader of status, held by a lint | X | 4 | rewritten |
| CC-5 | **One queue, one bar, a way out.** One row per timeline; owners and the draft database deleted; seven throws deleted; a refusal leaves the queue (D15); the model test | X | 6 | rewritten, +2 |
| CC-6 | Writers cannot store what readers refuse; names `shot-group-pack-commands.ts:189-190` | N | 2 | one name |
| CC-8 | The ratchet on the equality bridge | N | 1 | none |
| CC-9 | **Bounded transport.** One object reader and one URL builder in the App. Runtime: object and health reads do not wait on a commit's lock; the idempotent route table | N | 4 | new |
| CC-10 | **An upload is a queue record** (from TL-10). The dropped file is stored in the row and sent again if cut; the upload's private recovery and the "Failed to save asset" toast are deleted | X | 4 | new, moved in |
| R0 | One review round, with the new negatives | S | 2 | negatives added |

**Estimate: about 37 engineering days, about 15 elapsed with parallel workers.** Today's plan says 23 and 11. Release 14's N-items remove a few days from CC-4, CC-5 and CC-9, so expect about 33.

**Stays in extensibility:** TL-1 to TL-3, TL-4's headlines, TL-5 and TL-5b, TL-6 to TL-9, TL-10's command half, TL-11 to TL-15, and Phase 2.

**Critical path:** CC-4 → CC-5 → CC-10 → R0, about 16 days on the App. Three lines run beside it: CC-7 → CC-1 → CC-2 (Agent and Runtime); CC-7 → CC-3 → CC-6; CC-9 alone.

**Done when:**
- **The model test passes.** A scripted `send` plays every outcome at every queue position, a lost reply, a cut upload, a reload between any two steps and a second tab. After each step: adding an edit never throws; the screen equals the function of the row; every record is accepted, listed as not saved, or waiting; Discard and Dismiss leave a saved state.
- **The counts hold at 3 and 30 history entries:** identical computation counters; adding one object causes object GETs for that object only; the three scans are at zero.
- **Phase 0's six end-state checks** (P0-1 to P0-6) are true, plus the route table and the `ENOBUFS` writer test.
- **As evidence, not a gate:** the commit timing line on "Almost Ready", and a week of the owner's editing with no stuck state.

**Owner decisions it needs:** D9 (Release 15), D14 (cold start), and D15 (a refused change is removed and listed with Restore). D15 is needed before CC-5 starts.

---

## 3. What could ship with Release 14, beyond N1 to N12

Release 14's own description is "fixes at their cause and adds no capability". The test for each part: does it change what is stored in the browser, what goes over the wire, or what the owner sees happen to their work? If so, it needs the corpus and the model test under it first, and those are the stability project's first tasks.

| Part | Size | Risk this week | Depends on | Call |
|---|---|---|---|---|
| **The model test, as a seed** | M, 2 days, tests only | None to the product | N3, N4 | **Release 14.** It is the proof N3 and N4 need anyway. Build the scripted `send` now, with the cases that are true today (Discard, reload, two retained owners, the next edit saves). Release 15 grows it; nothing is thrown away |
| **The `_reference_basis` fix** | S to M, in flight | Low if the old probe stays as the test oracle | #394's tests | **Release 14.** It is the measured 67% |
| **Four-outcome decoder, client half** | S, 1 day | Low | #299 | **Release 15.** After #299 it changes no behaviour. Its value is the lint and the single boundary, which arrive with the server's `outcome` field |
| **The typed `send()` boundary and its lint** | M, 3 days | Medium: touches every caller that reads a status, in `dataProvider.ts` too | the decoder | **Release 15** |
| **One row per timeline, owners deleted** | L, 4 to 5 days | **High.** It changes the stored shape in IndexedDB, where testers and the owner hold retained work today, and it changes how two tabs share a lock | the model test's two-tab case | **Release 15.** N3's `discardScope` gives the visible benefit now |
| **The draft database deleted** | M, 2 days | **High.** The draft slot is what keeps an edit when the queue declines it. It is the safety net until the throws are gone | the seven throws deleted | **Release 15**, after CC-5's deletions, in the same change |
| **Refusals leave the queue (D15)** | M, 3 days with Restore | Medium, and it changes what happens to the owner's work | the owner's answer; the "not saved" list in the row | **Release 15.** Without Restore it discards work, and Restore needs the row change. Ask D15 now |
| **CC-9's one object reader** | M, 3 days | Medium: playback warm-up and waveforms run through it | — | **Release 15.** N6 removes the re-download now. CC-9's Runtime half is already N5, N10 and N11 |

### The cut-line

**Release 14 carries the behaviour; Release 15 carries the structure.**

- **Release 14:** N1 to N12, the `_reference_basis` fix, and the seed of the model test. Nothing that changes the shape of stored data or the wire.
- **Release 15:** the stability project above.

What that means for the owner on Release 14: saves in a few seconds, not minutes (inferred from the profile: about 3 s once the 67% is gone, unmeasured); a drop during a save works; nothing retries for ever; one bar with Try again and Discard, the same after a reload; Discard always clears.

What Release 14 does **not** give: a guarantee that the category cannot come back. Until Release 15, a new status or a new surface can still be added without a test failing, an import still waits behind a commit's lock for as long as the commit runs, and a cut upload is still lost if its one replay fails.

**One thing to do this week regardless:** put D15 to the owner. It is the only decision on the stability project's critical path.

## Not checked

- The 37-day estimate is task arithmetic on Plan 18's own figures, not a bottom-up estimate.
- "About 3 s after the fix" is 33% of the measured 9 s. Nobody has measured it.
- Whether a `File` stored in the queue row survives a reload in every supported browser. CC-10 starts by confirming it.
