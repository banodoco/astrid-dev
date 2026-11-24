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

## The little scenes

**A. A shared making place.** Two or three small orange minks cooperate at a workshop table, in a studio clearing or beside a little mechanical object. One holds something while another adjusts it. Use one short intentional cycle (or a composed pose in a still). The characters should look as though their work started before the visitor arrived.

**B. A place to pause.** A tiny elder/meditator sits on a rock or under a tree, with a still silhouette and perhaps a subtle breathing or leaf animation. This is a gentle cultural nod interpreted in Astrid's own geometry and palette.

**C. A cozy creative workstation.** A small figure sits at a lamplit desk with a monitor and a tiny node-chain or pixel sparkle. It alludes to the creative tool community, including ComfyUI, without reproducing any specific character, artwork, mascot or logo.

The globe can also have a bridge, a water feature, a windmill, workshop building or lone tree as a recognisable landmark **only if it improves composition**. These scenes need not be visible simultaneously. A visitor can intuit other places continue around the far side. Space between them is as important as the props.

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

## Motion and implementation

The **globe starts still**. Use a 3D scene that can be viewed from different directions, but no runtime spin, physics world or clickable resident is needed for the initial delivery. Tiny ambient moments—a windmill turn, a tail settling, a nod, a pixel spark or a monitor glow—can make the place alive if they remain very restrained. A single rendered loop may express that better and cheaper than a real-time simulation.

Create and keep editable 3D sources for the globe, minks and landmarks, with named locations, local orientation and a repeatable camera/lighting setup. The shippable media can be a poster, an ambient loop or a live 3D scene; choose from LP-0's evidence. Site text and controls remain browser-native. Provide a matching still for reduced motion, media failure and constrained devices.

## Review images and clips

LP-1: gray-material and shaded turntable; site hero at 1440 wide and 390 wide.
LP-2: front, side, rear, elevated mink views; three clear poses and a normal-size on-page comparison.
LP-3: one complete making place shown within the actual Vision hero; one 20–30-second ambient clip if animated.
LP-4: eight evenly spaced globe views; annotated map of three activity areas and open landscape.
LP-5/6: same camera and scene across five exact viewports; still fallback; normal and reduced-motion capture; baseline/candidate loading and performance numbers.

## Sign-off tests

A good result looks like an original Astrid world at the real display size, not just a good Blender beauty shot. It must be clearly spherical, use coherent perspective, scale, light and material, feature believable sculptural minks, contain the three discoverable scenes and preserve the page's editorial readability. **More props, more polygons and more texture are not substitutes for this.**
