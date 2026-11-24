# Living Planet — visual and motion specification

[Plan](plan.md) · [Milestones](tasks.md) · [Image references](assets/README.md)

## The intended first impression

Astrid's Vision page combines a clean editorial serif headline, spacious warm cream background, peach atmosphere, small orange accents and deliberately pixelated clouds. Into that world, place a **small complete 3D planet**, charming and physically credible enough to imagine picking it up or turning it over. The planet should look inhabitable beyond the visible hemisphere. It is a sculptural, quietly busy world—not an image of a village perched on a broad platform.

The emotion is curiosity and affection for a community of makers. A viewer sees the overall globe first, recognizes a couple of objects next, then notices the tiny private activities taking place around it. A recognizable detail should reward attention without dominating the hero.

## The physical form

- **True continuous sphere:** The horizon bends everywhere. Hills, a river/pond, rock outcrops and paths are attached to the globe; there is a real back, underside and local gravity.
- **Modest topography:** Small height differences make geography legible. Avoid sheer pasted-on vertical faces, overhanging tabletops and uniformly subdivided triangulated noise.
- **Material character:** soft matte soil and rock, gentle low-poly facets, stylized foliage and crisp water. A little micro-variation in surface roughness is enough; noisy photoreal textures or exposed Lego-like voxels are not the goal.
- **Illumination:** broad warm key from upper-left, cool/neutral soft fill and local occlusion beneath trees, minks, structures and rocks. The far side stays darker but not uniformly black.
- **Hierarchy:** two or three recognizable landmarks across the *globe*, clusters of medium trees/props, and much smaller inhabitants. Target a substantial amount of uncovered quiet ground. Tune counts by real-size readability, not a fixed quota.
- **Camera:** a three-quarter view with enough visible arc to show curvature. Give the right side breathing room, protect the left copy and allow the globe to intersect background cloud layers in intentional front/back order.

## The shared Astrid identity

The pixel mink remains the icon used in the interface. Its **3D counterpart** is a simplified sculpture of the *same creature*: elongated low body, slender neck, tapering muzzle, small ears, little short legs, cream throat/belly, plain eyes and a long tail with darker tip. Keep it legible from all sides and at tiny on-page sizes. Expression comes from pose, head angle and attention rather than detailed eyebrows, fur strands or oversized anime eyes.

Pixel-art belongs in selected **surface and information layers**: the mink's crisp authored markings, small signs, node connections, sparkles and website clouds. It should not make the planet a coarse low-resolution screenshot. Compare clean-shaded geometry with pixel accents on and off to ensure the art remains excellent without any post-processing trick.

## The scene portfolio

Eight scenes should be art-directed separately as detailed in [creative-units.md](creative-units.md), with each having its own emotional beat, graybox, on-page day/night stills and brief motion proof. The initial workshop collaboration scene locks the style; the other seven are tea, running game, solitary rose, mystery, astronomy, meditation and cozy creator. All use one sculptural palette and mascot identity while remaining distinct. Place them around the whole sphere with generous quiet land, not all in a dense front-facing village.

## Colour and light

Suggested starting relationships, tune to the real site rather than copying literal values blindly:

| Role | Starting tone |
| --- | --- |
| Website paper | warm ivory `#F7F3ED` |
| Subtle atmosphere | pale peach `#E8D7BF` |
| Earth and path | muted ochre `#C6A475` |
| Sunlit grass | olive `#818B59` |
| Shadowed foliage | deep sage `#53674C` |
| Water | softened blue `#6D9DA5` |
| Signature accent | Astrid orange `#F26B21` |

Don't make everything pastel: the globe needs dark values to feel dimensional. But more of the visible surface should be sunlit than in a heavily shaded game-engine scene. The website's clean graphics remain crisp at normal device resolution.

## Time-driven rotation and the site sky

The planet is **live Three.js**, not a flattened still. Its initial yaw is the authoritative effective hour from Astrid's existing local-time sky session. The default **does not spin automatically**. A rightward horizontal drag takes the visitor to later time; leftward takes them earlier. One full horizontal revolution represents one full 24-hour day and the wrap at midnight is seamless.

Time and yaw are one bidirectional **pure mapping**, not two stateful clocks. Track a canonical unwrapped horizontal angle independently from pitch. Set the session's manual hours from *user* horizontal drag only, throttled to the render frame, and subscribe to the session to follow real time/manual preview/replay. An external update to the planet must not call the user's time-change callback. Preserve the existing sunrise/sunset/twilight palette and use its light/dark state for convincing planet lighting; do not invent new fixed-hour day/night colours.

**Vertical movement is not time input.** A vertical-only gesture leaves the sky/background unchanged and never sets manual time. Allow a modest pitch/vertical view if it enhances exploration without obscuring the globe, and preserve natural vertical touch scrolling. Provide a keyboard-accessible alternative for time scrubbing and a “Live”/“Now” control returning to the real hour.

## Animation and late-stage polish

Normal ambient activity is subtle: minks occasionally gesture, build, sit, or look toward their companions. The planet should feel occupied, not like a restless game scene. The scene is genuinely 3D and can be viewed around its circumference.

**Entrance:** After the site's Vision text appears, the camera flies toward the globe and arcs gently around into its chosen **current-hour orientation**, without moving the planet's time/yaw. Coordinate the movement with the existing Home→Vision page transition and sky reveal, avoiding two competing dramatic animations. Keep a matching still in place until a live frame is ready; no layout shift or empty/black frame.

**Exit:** Leaving Vision has a complementary camera pull-back/arc or thoughtful dissolve back toward Home. Keep navigation immediate; the animation must tolerate browser Back, a second click, interrupted loading, and re-entry. On re-entry the saved/shared sky hour remains authoritative; exiting must not reset the sky. For reduced motion, no fly-through is required: use a stable still or gentle instant/crossfade state.

**Flying objects:** four candidate aerial creative units—bird flock, tiny glider, balloon traveller, one original oddity—are described in [creative-units.md](creative-units.md). Each receives independent silhouette, choreography, lighting, occlusion and art review. The global airspace pass selects activity so the four do not crowd the scene. Their movement is **never** a time dial; no sky-hour writes or unwanted planet yaw.

The default visual strength comes from the sculpted form, lighting, coherent characters and narrative geography. Do not use a global pixelation filter, fur-heavy realism, oversized floating objects, or extra animations as a substitute for that.

## Review images and clips

- LP-0/LP-1: baseline Vision captures; 360° gray-material and shaded planet turntable; four initial views at 00:00/06:00/12:00/18:00; right and left drag videos showing the *actual page* change from morning through dusk and back; vertical drag recording with a fixed sky and palette.
- LP-2: front, side, rear and elevated sculptural mink views; three clear poses; natural-size on-page comparison against the pixel mascot.
- LP-3: complete collaboration scene within the real Vision hero and 20–30 seconds of believable independent activity; independent/manager art verdict and an owner-facing feedback request, not a blocking sign-off.
- LP-4: an eight-view tour of the globe showing eight individually directed story areas, quiet geographic regions, scale variation and lighting at day and night.
- LP-5: clock → planet (initial and replay), planet → clock (horizontal drag), vertical-only/no-time-change, “Live”/return to now, Home↔Vision, and reduced-motion/no-WebGL tests with five fixed viewports.
- **LP-6 polish:** short recording of Home→Vision camera fly-in/arc, Vision→Home exit and interrupted/re-entered flow; night and day variants; per-object clips plus a combined composition showing the small flying objects passing in front of and behind appropriate geometry. Record and assert no hour change from either camera movement or flying objects.
- LP-7: final production candidate at the same five viewports, loading/CLS, phone/laptop FPS, resource cleanup, focus/keyboard and touch-scroll proof; an owner-facing review prompt plus separate, explicit final release approval.

## Sign-off tests

A good result looks like an original Astrid world at the real display size, not just a good Blender beauty shot. It must be clearly spherical and fully rotatable in real time, follow the site's local-time sky on entry, scrub that same clock with horizontal dragging only, use coherent perspective, scale, light and material, feature believable sculptural minks, contain the eight individually reviewed scene concepts with quiet terrain, carry an authored entry/exit plus restrained flying accents, and preserve the page's editorial readability. **More props, more polygons and more texture are not substitutes for this.**
