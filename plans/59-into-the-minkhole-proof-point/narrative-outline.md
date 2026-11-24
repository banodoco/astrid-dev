# Into the Minkhole — narrative outline

[Plan](plan.md) · [Visual guide](visual-guide.md) · [Inputs](inputs.md)

Creative direction, 24 November 2026. Consolidates the owner's production-script v4 and magic-trick pacing discussion. Working script, not a claim of completed film production or additional engineering scope.

## Purpose and tone

A casual developer-led demonstration of Astrid, culminating in a short, playful remix of the red-pill/blue-pill scene from The Matrix. Aim for roughly 2–3 minutes. Let technically curious viewers discover the significance themselves rather than telling them how impressed they should be. The technical promise is that a creator retains creative direction and feedback while agents handle implementation. The result should be entertaining independently of Astrid.

## Structure: a magic trick

| Beat | Illustrative time | Pace | Audience experience |
| --- | --- | --- | --- |
| Hook / pledge | 0:00–0:22 | Immediate, conversational | Recognise the source; understand the ambitious challenge and the division of labour. |
| Establish difficulty | 0:22–0:36 | Accelerate | Understand that many interconnected problems must be solved. |
| Rough cut / first small payoff | 0:36–0:53 | Readable, then deadpan | See real progress, laugh at the terrible placeholder voice, anticipate the improvement. |
| Generation and iteration | 0:53–1:18 | Dense, fast | See the agent choose approaches and respond to feedback; build belief with evidence. |
| Assembly and pack | 1:18–1:33 | Decelerate | See the pieces come together; want to see the finished film. |
| Prestige | 1:33–2:15 | Cinematic, then explosive | Enjoy the film, the guilt-driven reversal and the unexpected change of medium. |
| Meaning / invitation | 2:15–2:40 | Relaxed | Understand what a shared foundation could enable beyond this example. |

Timing is an editorial target, not a measured voiceover. Adjust to the actual material. The middle has smaller payoffs; reserve the sad mink, pixel transformation, magical world and finished sound design for the film. The film itself contains a second magic trick: a familiar choice, an unexpected emotional dilemma, an entirely different world.

## 1. The demo

### The experiment — pledge

Show recognisable original footage immediately, alongside a short introduction. Avoid an extended product explanation.

**Narration**

> Hey, so I've been building an open-source creative tool called Astrid. The idea is to give people and agents a way to push what's creatively possible with open models.
>
> Rather than try to explain how it works, I thought I'd show you an example of how I use it. I'm going to remix the famous red pill, blue pill scene from The Matrix, changing the characters, environments, dialogue and more, while keeping everything consistent.

### Why it's difficult

Show the shot breakdown, references, workflows and timeline; make the interdependence of story, script, character design, video, audio and editing apparent.

> My role in this will be purely creative direction and feedback. I'm not going to be involved in how any of this is actually done. I'm going to leave the how to the agents.
>
> There are a lot of little interconnected problems to solve: mapping out the sequence, writing the script, designing the characters, generating the clips and sound, and editing it all into a coherent piece.

### Work out the scene first — first small payoff

Show the actual request, source footage, mock-up images and low-fidelity edit.

> I start by asking Astrid to find the original footage and describing what I want to happen. We work out the shots and put together a really low-fidelity version using the original clips, some basic mock-up images and a crappy voiceover, just to get the sequence right.

**Cutaway:** the serious original guide's mouth is unmoving. A flat, cheap system TTS voice says, “You have two options.” Hold a beat, then hard cut back without acknowledging the joke. Do not reveal the new dialogue. Let the roughness be funny and establish how far the work has to go.

### Generate, review, repeat — turn

Show real agent decisions, workflows and alternatives: inpainting (source/mask/result), continuation, voice/audio replacement, entirely new shots. Include one concrete before/feedback/after example, such as a request to make the protagonist more annoyed. Do not present simulated logs as real.

> Once we've got that right, the agent figures out which approach to take for each shot. Some need inpainting, some need video continuation, some just need new dialogue or sound, and some are completely new shots. It sends the results back to me for feedback, and we iterate until they work.
>
> Then it edits everything together, and we go through two rounds of feedback on the edit.

### The pack — heighten anticipation

Slow down. Show the assembled timeline and the actual pack. Keep the explanation short; the broader vision follows the film.

> This all uses an Astrid pack I've been working on. This one's focused on remixing existing scenes, but you can build your own packs on top of ComfyUI workflows, code or other tools.
>
> And here's the final product.

Pause. Hard cut to black.

## 2. The finished short — prestige

Play uninterrupted. Keep the guide completely serious and replace the original protagonist with a new character who is confused and slightly irritated. The mink is a tiny excitable pixel-art creature, not a second pill. Maintain visual and character continuity across the shots.

| Beat | Action / dialogue |
| --- | --- |
| 00 — Entrance | On black, the Astrid wordmark appears. The mink jumps on top, then leaps forward. Match cut to the guide's glasses: the mink flies out of a lens towards us, revealing the scene. Keep this ident to 2–3 seconds. |
| 01 — Setup | The guide sits opposite the protagonist and offers a green pill with complete seriousness. **Guide:** “You take the green pill, you keep running workflows by hand, tuning parameters, trying to get everything to work together.” |
| 02 — Alternative | The guide opens his other hand. The tiny pixel mink bounces around, desperate for attention. **Guide:** “Or you take this cute little pixely creature, and you see just how deep the mink hole goes.” |
| 03 — Obvious choice | The protagonist looks confused and unimpressed, then reaches for the green pill. |
| 04 — Interruption | Just before he takes it, the guide adds, almost as an afterthought: **“Oh, by the way, I don't really know what happens to him if you don't pick him.”** |
| 05 — Guilt | The mink abruptly stops jumping. Its ears droop. A tiny disappointed squeak, then uncomfortable silence. The protagonist looks from pill to mink. |
| 06 — Reversal | The protagonist sighs, withdraws his hand from the pill and reaches for the mink instead. **Protagonist:** “Oh, what the hell.” |
| 07 — Transformation and adventure | At contact, pixelation spreads from the protagonist's hand across his body. Both spring upwards into a colourful, magical pixel-art world, flying through strange landscapes and into the sky. The mink is delighted; the protagonist remains a little annoyed and bewildered. |
| 08 — End card | The mink flies towards the camera and transforms into the Astrid logo. Let the film finish on the logo before returning to the presenter. |

**Direction:** The humour is deadpan, slightly absurd and tender rather than a forced punchline. The guide's gravitas contrasts with the mink's behaviour. Hold the sad moment just long enough to feel awkward. Use serious ambience, a small squeak, silence, then a disproportionate euphoric burst of sound and colour. The protagonist doesn't suddenly become enthusiastic. Don't explain what the mink represents.

## 3. The closing — meaning

Return to the presenter or the editor after the film has landed. Show the website as a simple invitation.

> So that's Astrid. The idea is to create a shared foundation for agents that people can build higher-level tools and guidance on top of, so we can combine all these different pieces of the open-source ecosystem to do extraordinary things. Ultimately, the goal is just to help you do more and create more.
>
> All of this happens inside a creative editor as well, and I'll be sharing more of the app very soon. If you'd like to try it out, head to astrid.haus. Any feedback is hugely appreciated.

## Production integrity

Use actual prompts, agent actions, shot decisions, feedback and intermediate results. Adjust narration to what actually happened, including the stated human/agent division of work and two rounds of editing feedback; do not claim unshown capabilities or conceal manual implementation. Check permissions for any source footage, voices and audio used in a public version. The creative choices remain with the owner; the agents work through Astrid's tools in accordance with the existing plan. This brief is separate from engineering acceptance evidence and release qualification.
