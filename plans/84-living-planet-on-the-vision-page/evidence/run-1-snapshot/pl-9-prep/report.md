# PL-9 module seam preparation

Read-only, provisional outline from the merged PL-1 engine at `95a061b3ba24a0bdec598da449f04ee82c6acf5c`, in the dedicated `worktrees/pl-9-prep` worktree. The worktree was clean when checked. I did not read environment files or credentials and did not run tests, builds, or browser work. No product files were changed.

PL-9 is intentionally later than the visual and runtime decisions. PL-3, PL-10, PL-4 and PL-5 will change the camera/control, time-of-day, poster/fallback and quality/lifecycle APIs. The runtime split below is therefore a seam map, not a settled design; wait for the owner-authorized PL-8 sequence before refactoring.

## Current shape and hard preservation constraints

`src/pages/Home/planet/planetEngine.ts` is 9,146 lines. Almost everything from `LandmarkConfig` at line 77 to the returned API at 9145 is lexically inside `initPlanetEngine` (entry starts at line 42). Helpers that look global are currently per-engine closures. Moving one to module scope without explicit inputs can silently change instance lifetime, shared mutable state or creation order.

The module currently has only a runtime import of `three` (`:1`). The public `PlanetEngineAPI` and `initPlanetEngine` sit at `:27-50`; `PublicAstridPlanet.tsx` dynamically imports this engine. This one-way lazy boundary is valuable: lower-level files must not import the React component or re-import the engine to reach a helper.

Preserve these invariants through each extraction:

1. **One seeded RNG closure, same call order.** Fixed-pose seed and `random` are created once at `:6710-6715`. The 25 agents are built in explicit `AgentGroups` order (`:7103-7164`); foliage/rock placement consumes random values earlier (`:6911`, `:6933`, `:7046`), followed by agent constructors (e.g. `:2189-2192`), controller scene setup and later story setpieces. Extracted constructors must receive the same `random` function. Do not make module-level random calls, per-module random streams or reorder builder calls. Fixed-pose image evidence depends on deterministic construction.
2. **One clock source.** `engineNow` is created beside RNG (`:6715`), flows into agents/controllers (`:2632-2640`, called at `:7166`) and is used by the frame and visibility path (`:8440-8460`, `:8493-8946`). Inject that same function/frame timestamp. No per-module clocks or local frame loops; retain one `dt` and update order.
3. **One resource owner per engine.** The `own()` wrapper and live-resource counters are created inside `initPlanetEngine` (`:51-75`). Factories and scene modules must receive this exact owner. Do not give modules their own resource `Set` or wrap `dispose()` twice. Final disposal traverses both scene trees, explicitly handles detached/alternate resources and the render target, drains the owner registry and disposes the renderer (`:9083-9143`). The ten-mount PL-1 audit expects the current aggregate counts/zero live instances to remain unchanged.
4. **No accidental module-global mutable state.** `WORLD_CONFIG` contains `THREE.Vector3` instances (`:84-119`), terrain has a rendered-triangle cache and scratch vectors (`:288-300`), and the engine owns mutable materials/scene nodes. Keep per-instance vectors/caches/resources inside factories or clone them per engine; moving these closures to module singletons can make two mounts share mutation even if one mount works.
5. **Same scene and update order.** Initialization currently builds renderer/scene/lights, the planet/water and common props, procedural trees/rocks/grass, agents, `createSceneControllers`, the Up/Castle/Prince/Wright/Bullet setpieces and finally the pixel-filter/turnaround objects (`:6711-8215`). Keep the synchronous call order and each existing `scene.add`/`planetGroup.add` order. `createSceneControllers` appends controllers in source order and `animate` updates controllers, wanderers, pair/obstacle separation and all agents before the one final renderer pass (`:8493-8946`). Do not sort/parallelize builders, change controller order, or move draw submission earlier. Transparency and the visual references are sensitive to these changes.

## Candidate low-risk module map

The ranges below are the current source sections to move, not promised final line counts. The proposed modules keep each current body below 1,200 lines with headroom for contracts/exports. Use a leaf contract/context module for shared types rather than importing the orchestrator back into helpers.

| Proposed module | Current source seam | Estimated body | Contents and dependencies |
|---|---:|---:|---|
| `planet/types.ts` | `:3-50`, `:77-82`, `:288-300`, `:665-671`, `:751-760`, `:1481-1482`, `:2614-2630`, plus the small cross-module contracts | <250 | Public API and shared type-only contracts (`LandmarkId`, resource audit, mink/scene/context types). Keep it a leaf; use `import type` where practical. |
| `planet/resourceOwner.ts` | `:51-75` | <150 | A factory that creates one owner/registry/counters per `initPlanetEngine` call and returns the same `own` function plus final audit/disposal support. Keep owner creation inside initialization. |
| `planet/worldConfig.ts` | `:84-136` | <120 | A `createWorldConfig()` factory for landmark and bridge vectors, or immutable scalar config plus per-engine vector copies. No engine imports or dynamic random work; avoid a shared module-level vector singleton. |
| `planet/terrain.ts` | `:138-365` | <300 | Noise/mask/height/normal/walkable-surface math and rendered-triangle lookup helpers. Keep scratch vectors/cache private to one engine if mutation is required. |
| `planet/terrainMeshes.ts` | `:1247-1453` | <260 | `buildPlanetMesh`, rendered-triangle cache production and `buildWaterMesh`. Important coupling: `getRenderedTerrainHeight` (`:288-325`) consumes the cache populated by `buildPlanetMesh` (`:1247-1343`); keep them in one module or pass an explicit cache setter/result. Water shares `getTerrainHeight`, config and its own uniforms. |
| `planet/mink/visuals.ts` | `:367-775`, `:762-1225` | <900 | Pixel textures, geometry, rig, contact-shadow texture and pose application. Inject `own`; depend down on THREE/types/config as needed, never back on engine. |
| `planet/mink/MinkAgent.ts` | `:2139-2612` | <500 | Agent movement/state class. It uses mink visuals/rig (`:2177-2229`), terrain/walkability/config/bridge basis (`:2250-2340`, `:2460-2500`) and pose functions. Inject these dependencies and `random`, rather than importing the engine. |
| `planet/worldAssets.ts` | `:1454-2137` | <750 | Surface attachment and reusable prop factories/material helper. It depends on terrain queries, world materials and the injected resource owner. |
| `planet/scenes/tea-meadow-rose.ts` | `:2666-3479` | ~815 | Scene builders/controllers 1–3. Receive a narrow scene context and append returned controllers/interactions in the caller's sequence. |
| `planet/scenes/mystery-astro-ball.ts` | `:3480-4107` | ~630 | Scene builders/controllers 4–6. |
| `planet/scenes/derrick-monolith-thumper.ts` | `:4108-4790` | ~685 | Scene builders/controllers 7–9. |
| `planet/scenes/alpine-comfy-hand.ts` | `:4791-5414` | ~625 | Scene builders/controllers 10–13. |
| `planet/scenes/david-pillars.ts` | `:5415-6178` | ~770 | Scenes 14–18, including the four pillar-related constructions. |
| `planet/scenes/hobbit-thinker-giant.ts` | `:6179-6708` | ~535 | Remaining world scene/controller builders. The current comments repeat a “Scene 19” label; use stable descriptive module names, not that numbering. |
| `planet/world/vegetation.ts` | `:6825-7164` | ~340 | Obstacles, procedural trees/rocks/grass/cacti and ordered agent creation/assembly. Keep all random calls and order explicit. |
| `planet/world/story-setpieces.ts` | `:7168-8185` | ~1,020 | Up balloons, moving castle, Little Prince/birds, Wright Flyer and Bullet. If the context/export overhead pushes this above 1,200, split at the existing setpiece boundaries; each module returns only ordered scene additions/controllers/interactions. |
| `planet/runtime/interaction.ts` | `:8217-8386` | ~170 | Pointer/raycaster input and event handlers, after PL-3 settles its interaction API. |
| `planet/runtime/frameLoop.ts` | `:8428-8946` | ~520 | Visibility/context events, software-GL fence path and single animation loop. Keep as one frame owner until PL-5 settles its scheduler/quality controls. |
| `planet/runtime/timeOfDay.ts` | `:8948-9027` | ~100 | Light keyframes, time-to-angle mapping and landmark rotation control, after PL-10 settles session ownership. |
| `planet/runtime/dispose.ts` | `:9057-9143` | <200 | The single ordered cleanup path. Keep the owner registry, scene traversals and renderer disposal coordinated with runtime state. |
| `planetEngine.ts` | current `:42-75` plus the eventual assembly/API façade | <500 target | Orchestrate one init: construct context, build resources/agents/controllers/setpieces in the exact present sequence, install runtime, return one API. Do not keep the frame loop or scene definitions here after their extractions. |

The renderer/context creation, stage resize/camera projection (`:6716-6769`, `:8391-8426`), shared materials, postprocess setup (`:8189-8215`) and lighting/API entry points are smaller cuts, but several are adjacent to PL-3/4/5 state. Leave them in the orchestrator until those APIs settle, then move them into `runtime/renderer.ts`/`runtime/camera.ts` only if each remains below the file ceiling. The 1,200-line limit is a hard maximum, so check actual final counts after every move rather than relying only on these approximate source-range sizes.

## Dependency direction and cycle risks

A safe dependency graph is one-way:

```text
planetEngine (orchestrator)
  -> runtime, scene builders, world assembly
scene builders/world assembly
  -> MinkAgent, worldAssets, terrainMeshes, terrain/config, shared context types
MinkAgent/worldAssets/terrainMeshes
  -> mink visuals, terrain/config, resource-owner contract
terrain/config, shared types
  -> THREE and leaf math only
```

Current closures hide this coupling. `MinkAgent` uses terrain and mink visuals; `MinkAgent` and `AgentGroups` reference one another's types. Put those contracts in a type-only leaf or use a narrow `MinkAgentLike` in the group type to avoid a runtime cycle. Scene modules need `own`, `random`, `engineNow`, materials, groups, terrain functions, obstacle/interaction/controller registries and shared scene nodes; pass a typed context downward. Do not have `terrain`, `worldAssets`, `MinkAgent` or individual scene modules import from `planetEngine.ts` to reach nested functions/types. Do not add side-effectful scene construction at module import time.

`buildPlanetMesh`/rendered-triangle cache is the main terrain split hazard; the shared `own` registry and shared generated materials are the main resource split hazard. The scene builders are the highest-coupling area because each closes over shared agents, directions, obstacle arrays, materials, random, callbacks and controller/interaction arrays. Split their bodies only after the lower-level context is explicit.

## Lowest-risk split order

1. Move public/internal type contracts to a leaf module and preserve the current public entrypoint/export. No runtime behavior changes.
2. Extract the per-instance resource-owner factory without changing when it is created or which factories call its `own` function.
3. Extract world config and terrain/math together, keeping the rendered-triangle cache and mesh builder relationship explicit. Keep numeric constants, helper evaluation order and mutable scratch vectors unchanged.
4. Extract mink visual assets/pose functions, then `MinkAgent` with injected terrain/config/resource dependencies. Verify its constructor still consumes the same RNG draws at the same point in the engine sequence.
5. Extract reusable static prop/world asset factories with the same injected owner and material instances.
6. Split `createSceneControllers` along existing scene boundaries into the six ordered modules above. Start with one block at a time; each module returns controller/interaction entries rather than importing shared arrays. Append returned entries and preserve its current call order.
7. Move the vegetation and story setpieces, preserving current invocation order relative to agents, controllers and later renderer setup. Keep random placement calls in their current sequence and preserve every `add()` order.
8. Only after PL-3/10/4/5 finish, split camera/input, time-of-day, quality and lifecycle APIs. Retain one `animate` owner, shared `engineNow`, same controller/agent update sequence, one final draw, and one ordered disposer.
9. After each move, check the diff for changed call order and module sizes; compare fixed-pose captures and the existing PL-1 resource/cleanup proof. The full file-size gate must include every `Home/planet` source file.

No implementation or test step was performed here. The extraction outline is provisional until the dependent PL-3, PL-10, PL-4 and PL-5 APIs and the owner-authorized PL-8 sequence are complete.
