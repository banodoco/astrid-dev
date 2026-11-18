# Alignment check: do Plans 64–66 set up Plan 67?

Read-only, 18 Nov 2026. Nothing run. Plans read at `aee9a968`. I read Plan 67 in full, the relevant Plan 66 cards, and `align-luna.md` and `nkd-speech.md`. I checked the Luna's main claims against NKD Basic Tools at `c157722a` (`nkd_event_curve.py`, `nkd_minimax_guides.py`), ComfyUI `6bfaacc` and `astrid-agent` `release/14/main`.

## 1. Verdict

**Largely aligned. Plan 67 can land on Plans 64–66 without reshaping them, provided four small reservations are made now. Plan 67 itself is consistent with the lever design in intent, with one sentence in Plan 66 that it contradicts and one lowering that would bring a mode back.**

- **No new mechanism:** holds. Timed prompts feed the text; guide `phase` schedules the timed rows; ControlNet and LoRA `phase` sit in the model chain; signals are a report.
- **Tools versus levers:** holds. The curve is made by a tool and used as an ordinary audio guide.
- **Two clocks:** holds in the request. It is broken in two places in the wording: Plan 66 says `phase` belongs to Process levers only, while Plan 67 puts it on guides, which are Context; and the Event Curve node has its own input called `phase` that means something else.
- **What 64–66 must reserve:** who may carry `phase`; one table column for the node pack a kind needs; the final prompt string in the dry-run view; and a worker node list that is not hard-coded.

### The Luna's claims, checked

| Claim | Verdict |
| --- | --- |
| Event Curve outputs 32 kHz, while CS-4 expects 48 kHz | **Confirmed.** `SAMPLE_RATE = 32000` in `nkd_event_curve.py`. |
| The Event Curve node has an input named `phase` that is a curve offset | **Confirmed** (`io.Float.Input("phase", …)`). |
| NKD MiniMax Guides only has `until`, so a phase must start at 0 | **Confirmed.** |
| The NKD node snaps positions to the 17-frame grid by default, merges same-frame guides and rejects two of one type on a frame | **Confirmed.** `snap_positions` defaults to true. Also: a merged frame takes the larger `until` of its image and audio, so they cannot have different phases. |
| The worker's custom-node list is hard-coded, so adding a pin is not enough | **Confirmed.** `astrid/packs/runpod/h3_release.py` `release_inputs` builds the list from two named packs. |
| CS-5's `during` on a control has no counterpart in the node | **Confirmed.** `MiniMaxH3FunControlNetApply` takes a whole control video and no clip-time span. |
| CC-3 and CC-2 need broad "compatibility language" for every Plan 67 field | **Overstated.** CC-2 already lists `phase`, `control`, `params` and status, and says later cards add their own rows. Only the four reservations below are missing. |

## 2. Inconsistencies, in priority order

1. **Guide `phase` through the NKD node is a hidden mode switch.** CS-3 says: when any guide has `phase`, lower all guides through `NKDMiniMaxGuides` instead of the stock chain. Adding `phase` to one guide would then change how every other guide in the job behaves: positions snap to the 17-frame grid unless switched off, same-frame guides merge and share one `until`, and a duplicate type on a frame becomes an error. Plan 66's invariant is that a lever never changes another lever's lowering.

   The NKD node does its scheduling with ordinary conditioning time ranges (`start_percent` and `end_percent` on copies of the conditioning). ComfyUI's own `ConditioningSetTimestepRange` and `ConditioningCombine` do the same thing. So guide `phase` can very likely be lowered with stock nodes around the CC-4 chain: one conditioning with the guide, limited to the phase, combined with one without it for the rest. That keeps one guide lowering, allows any `[from, to]`, and needs no NKD node in job graphs. NKD is then needed only where the curve tool runs. This is unverified with the H3 guider; NKD's node relies on the same behaviour, which is good evidence it works.

2. **Plan 66 says `phase` is for Process levers only.** Its "Two clocks" paragraph reads "says when during generation a Process lever acts". Plan 67 puts `phase` on guides. The clock is a property of the field, not of a family. One sentence to change.

3. **Jobs would require NKD even when they use no NKD lever.** Nothing in the table says which node pack a kind needs, and the worker list is hard-coded. Reserve one column now (pack, commit, node classes), and build each graph's node requirements from the kinds it uses. That is also what makes the next community pack a row and not a change to the release code.

4. **ControlNet may have nothing to load.** CS-5 assumes control types with weights files. No H3 Fun ControlNet weights are identified or pinned anywhere in the plans, and the node describes itself as applying "to a text-to-video model", so use with the Ref2VA weights is unverified. CS-5 needs the same "prove it or stay `unavailable`" shape as CS-7. Its `during` field also has no meaning the node can honour.

5. **Curve tool details contradict the node.** 48 kHz expected against 32 kHz produced; and the tool should not expose the node's `phase` input under that name.

6. **The dry-run view has no place for the final prompt.** CS-2 and CS-6 both need the final prompt string and per-tag bindings in the view. CC-3 has the bindings but not the string. Adding it now avoids changing the persisted view later.

7. **Signals do slightly too much.** `for` as a label shown beside each tag is useful and cheap. "A warning when a label appears in the prompt beside the wrong tag" means parsing prose, which will be wrong often enough to be ignored. Drop the warning.

8. **Sequencing inside Plan 67.** CS-5 and CS-7 are said to follow CS-2 (timed prompts). Neither uses it.

9. **NKD-node behaviours to pin if the NKD lowering is kept.** Positions must be passed as resolved positive frames with `snap_positions` off (the node counts negative positions on the sampled latent, the problem CC-4 already solved), and the table needs rows for same-frame merging.

Not a problem, checked: `settings.adapters[].phase` and `role: control` are already reserved as `unavailable` in CC-2; CC-9's time rules cover timed-prompt spans; Plan 64's reference rows carry what the binding report needs; Plan 65 needs no change.

## 3. Text edits (twelve)

**Plans 64–66: reserve now.**

1. **Plan 66 `plan.md`, "Two clocks".** Replace "says when during generation a Process lever acts" with "says when during generation a lever acts. Any kind may accept it; the table says which do."

2. **Plan 66 `tasks.md`, CC-2.** After "its limits and its conflicts" add: "and the node pack it needs (repository, commit and node classes; none for stock ComfyUI). A graph's node requirements are the union over the kinds it uses, so a job never requires a pack it doesn't use."

3. **Plan 66 `tasks.md`, CC-3.** Add to the list of what the view shows: "the final prompt string as sent to the text encoder".

4. **Plan 66 `tasks.md`, CC-4 detail.** Add: "Keep the guide lowering as one function that takes the ordered guides and returns conditioning, so a later schedule over denoising progress wraps it without changing it. Two guides of the same type on one frame are refused."

5. **Plan 64 `tasks.md`, SR-3 (or CC-1.2 if SR-3 is already dispatched).** Add: "Build the graph's custom-node requirements from the lowerings used. Replace the two-pack list in `astrid/packs/runpod/h3_release.py` `release_inputs` with one read from the pins, so a new pinned pack needs no code change there."

**Plan 67.**

6. **CS-3 scope.** Replace the first two sentences with: "First try stock nodes: wrap the CC-4 guide chain so that a conditioning with the phased guides is limited to their `phase` (`ConditioningSetTimestepRange`) and combined (`ConditioningCombine`) with one without them for the rest of denoising. If that compiles with the H3 guider on CPU, use it: any `[from, to]` is then allowed and no NKD node enters job graphs. Only if it does not, lower through `NKDMiniMaxGuides`, with `snap_positions` off, positions passed as resolved positive frames, `phase` required to start at 0, and unphased guides proven to produce the same rows as the stock chain. Either way, adding `phase` to one guide must not change how any other guide is lowered."

7. **CS-1 scope.** Add: "Declare NKD in the capability rows of the kinds that need it (Plan 66 CC-2), not as a requirement of every H3 job. If CS-3 uses stock nodes, NKD is needed only where the curve tool runs."

8. **CS-4 scope and proof.** Replace "has the requested duration at 48 kHz" with "has the requested duration at the node's 32 kHz, used like any other audio guide". Add: "The tool names the node's curve offset `--offset`, never `phase`."

9. **CS-5 scope.** Replace "`asset` (control video), `during`, `strength`, `phase`" with "`asset` (control video, covering the whole job after its `range` trim; a shorter one is refused), `strength`, `phase`". Add: "Start by identifying pinned Fun ControlNet weights for H3 and whether the patch loads on the Ref2VA model. If neither is established on CPU, the kind stays `unavailable` with its reason, as CS-7 does. The patch sits in the model chain after the adapters."

10. **CS-6 scope and proof.** Replace "and a warning when a label appears in the prompt beside the wrong tag" with "The report shows the label; it does not read the prompt." A video reference's `for` label applies to its soundtrack tag too.

11. **Plan 67 `plan.md`, order, and `tasks.md` critical path.** Replace "CS-5 (ControlNet) and CS-7 (LoRA phase) follow CS-2" with "CS-5 and CS-7 follow CS-1 and can run alongside CS-2, CS-3 and CS-6".

12. **Plan 67 `plan.md`, "Included", guide phase bullet.** Replace "It lowers through NKD's MiniMax Guides node, whose `until` is that phase." with "It lowers to a schedule over the timed rows: stock conditioning time ranges if they compile, otherwise NKD's MiniMax Guides node."

## Not established

- That stock conditioning time ranges work with the H3 guider. NKD's node depends on the same behaviour.
- That any Fun ControlNet weights for H3 exist in a form Astrid can pin.
- Anything about how well timed prompts, phased guides or curves are followed.
