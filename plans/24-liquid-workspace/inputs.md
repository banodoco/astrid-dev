# Inputs — Agent-powered liquid workspace

[Plan](plan.md) · [Tasks](tasks.md)

## Product foundations (captured 2026-11-06; revalidate at execution start)

- [Liquid Software principle](../../visions/pillars/liquid-software.md), [portable components gap](../../visions/gaps/LS-001-portable-components.md), [component reference](components.md), [pinned source map](inputs.md).
- [Astrid App custom two-pane editor](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/examples/CustomTwoPaneVideoEditorExample.tsx) and [current editor shell](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/TimelineEditorShellCore.tsx): real existing views and layout coupling.
- [Editor SDK manifest](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/sdk/manifest.ts), [TimelineViewStore](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/sdk/video/timeline/viewState.ts), [RuntimeDataProvider](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/integrations/runtime/dataProvider.ts).
- [Agent Music pack](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/music/docs/SKILL.md), [Timeline pack](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/timeline/docs/SKILL.md), [pack authoring](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/docs/packs/creating-packs.md).
- [Astrid Runtime](https://github.com/banodoco/astrid-runtime/tree/9fc53b771134940aaac901e4cfc5d03c1db1a20a): one durable authority; do not invent competing state owner.

## Preconditions / unknowns

Exact active branch/SHAs and retained code to preserve, target integration branch, compatible Plan 04/06/18 outputs, approved trusted extension posture, source-specific gesture/size assertions, 2D layout library decision, and chosen second-domain component. No claim that arbitrary docking, agent workspace commands or native spatial desktop currently exist.
