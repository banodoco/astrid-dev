# Inputs — Workflow set-up

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner asked for this on 15 November 2026 in the advisor's session: "what I'd like is that we have a way to just download all the models for a workflow and if we can't find them we have a simple way to reconcile them, similar with custom nodes", and earlier the same day, "why have this blocker for stuff we can acquire instantly, automatically?" Recorded on the [strategy page](../../strategy.md#candidates-not-yet-in-a-version) as a candidate for version 0.2. D1 to D3 below were decided the same day.

**Prior art:** Four code readings on 15 November 2026 of astrid-agent `a91c35dfd` and VibeComfy `dba38f86`; summarised in [issue 665](https://github.com/banodoco/astrid-dev/issues/665) for the model half.

*Models.*
- A bundled model that is not downloaded works: a typed `missing_model` names the file, folder and roles (`astrid/core/generation/asset_gaps.py:65-84, 133-151`; `backends/comfy_target.py:621-651`), and `fetch-models` plans the address, size, fingerprint and destination, then applies that exact plan (`asset_gaps.py:244-371`). It takes a bundled entry and a mode, not a workflow file, and the skill walks only the image case (`astrid/packs/setup/docs/SKILL.md:169-188`).
- A model whose fingerprint or size is still missing after Astrid has filled what it can from its pinned locks is refused on a managed ComfyUI with a bare error (`astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py:167-174`; `managed_preparation.py:274-303`). A survey counted 132 incomplete authored records across 31 of the 52 bundled workflows; how many of those are actually refused after the locks are applied has not been counted. The look-up-and-record fix replaces the refusal.
- A person's own workflow naming a file nothing knows gets the file, node and field and nothing else; the skill ends at "tell the user the filename and folder" (`astrid/packs/vibecomfy/local_server_engine.py:154-205`; `astrid/packs/vibecomfy/docs/SKILL.md:183-186`).
- The same model under another name or subfolder is not noticed by Astrid's matching (`comfy_target.py:664-683`; `asset_gaps.py:193-214`). VibeComfy treats path-separator differences as equal and deliberately nothing looser (`model_assets.py:321-339`).
- There is no general identification of a file by content: no index by fingerprint or size, no reading of a file's header, no search of any site. One legacy file is special-cased by size and fingerprint (`registry/models_loader.py:180-192`), and download receipts record address, fingerprint and size without being an index (`fetch.py:316-348`). Verification records witness a known fingerprint at a known path; they are not an index (`model_verification.py:127-145`; VibeComfy `fetch.py:427-464`). VibeComfy's registry resolves by canonical name and alias only (`registry/models_loader.py:286-318, 533-550`).
- Downloads onto a person's own ComfyUI need the loader nodes present and the same machine (`asset_gaps.py:264-268, 323-333`). The plan step already writes a small probe file (`asset_gaps.py:334-338, 375-391`).
- Fully pinned records today: 36 in the RunPod pack's lock, 3 in the VibeComfy pack's lock.

*Node packs.*
- On a person's own ComfyUI a missing node gives a typed `missing_node_pack` with the class, pack and repository when the lock knows the class, and tells the person to install it and restart (`asset_gaps.py:105-122`).
- A class the lock does not know is reported as a ComfyUI core node with advice to update ComfyUI (`asset_gaps.py:96-98, 117-121`).
- Known packs are VibeComfy's static definitions merged with its lock, which holds 15 packs (`node_packs/_defs.py:474-478, 508-540`). A wider resolver exists and is not called by readiness. It is not a drop-in: its named look-up uses the Comfy Registry and refuses to work offline; the ComfyUI-Manager tier fetches two lists over the network on a cache miss, does not catch a transport error, is tested only against synthetic data whose shape may not match the real lists, and returns a repository without a commit (`registry/pack_resolver.py:592-744, 962-1031, 1300-1360, 1508-1538`; `tests/test_pack_resolver.py:660-689`).
- A managed ComfyUI installs missing locked packs with `astrid generate align --apply`, pinned to a full commit (`asset_alignment.py:353-475, 592-610`; VibeComfy `node_packs/_install.py:402-410`). Only the Python packages a pack's definition declares are installed, not an arbitrary `requirements.txt`; an unknown pack gets none. The protected-package check guards Torch and configured names, detects some changes only afterwards and cannot roll back (`node_packs/_install.py:943-1082`). Packs without a repository and full commit are listed and not installed.
- On a person's own ComfyUI Astrid installs nothing: the setup skill says setup never installs nodes, and the VibeComfy skill directs the person to ComfyUI-Manager or a separate install command (`astrid/packs/setup/docs/SKILL.md:196-200`; `astrid/packs/vibecomfy/docs/SKILL.md:167-202`).
- No command sets up models and node packs together for any workflow on any target. The nearest pieces: `generate align` (bundled and registered ready-template entries, on a managed ComfyUI; it downloads models first and only then reports a restart, `asset_alignment.py:344-366, 581-610`); `vibecomfy nodes reconcile` (a combined report of nodes, models and restart, `commands/nodes.py:396-460, 562-619`); `vibecomfy run --ensure-packs --ensure-models` (installs, reloads, then fetches, as part of a run, `runtime/session.py:1140-1224`); `vibecomfy fetch` (models only).

**Approach:** see [plan.md](plan.md#existing-work-and-decision). Alternatives: leave it to ComfyUI-Manager's own "install missing" (covers nodes on a person's ComfyUI, not models, not an agent, not a managed ComfyUI); fill in every bundled record by hand (fixes bundled workflows only and nothing a person brings); two separate commands for models and nodes (today's split, which is the complaint). Chosen: one requirements list and one plan-and-apply, extending the existing download plan and alignment.

**Challenge:** Reviewed — an independent Astra critique of the first draft against the code, recorded in [review.md](./review.md). Accepted: the corrections to the evidence above; one front door over existing pieces; the install, restart, continue flow in place of one all-or-nothing approval; stored approved actions with per-action progress; same machine only; refusing any change to an installed package on a person's ComfyUI; proving the ComfyUI-Manager path on real data first (WS-5); merging the two reconcile tasks and folding the skills into the proof. Deferred to issue 665 on its advice: identification from a file's contents and searching other sites. Rejected: none.

**Proof and limits:** Completion is in [plan.md](plan.md#completion). Not verified from the planning session: whether Hugging Face offers any search by fingerprint (believed not; only per-repository file details), and whether Civitai's look-up by fingerprint is usable; WS-5 checks both before building on them. Coverage of the ComfyUI-Manager list for the node classes bundled workflows use has not been counted.

**Review rounds:** Pending — recommended: one final round, because apply installs code into a person's ComfyUI and downloads from addresses a workflow names. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, and the advisor session.

## Owner decisions

- **D1 Installing node packs into a person's own ComfyUI.** Today Astrid never does. Approving a node pack means letting someone else's code run with the person's own access; a pinned commit does not make it safe, and its Python packages can break workflows that work today. Proposed: install only on approval of a plan that names each pack, repository, commit and every Python package to be added; refuse any item that would change a package already installed or an existing pack folder, and leave that item to the person. Alternative: keep all of it manual and have the plan print the exact steps. Recommendation: the proposal. **Decided 15 November 2026 (Hannah, "yes on all"): the recommendation.**
- **D2 Where Astrid may look.** In this plan: what Astrid and VibeComfy already know, and the ComfyUI-Manager node list once WS-5 has proven it. Later, under issue 665: Hugging Face and Civitai for models. Recommendation: as stated; a candidate is never applied without confirmation. **Decided 15 November 2026 (Hannah, "yes on all"): the recommendation.**
- **D3 Sources outside Hugging Face.** A workflow can name any address. Proposed: such a source is shown in the plan with its host, fingerprinted on download and recorded; it is never fetched without the plan being approved. This closes the deferred Release 13 item on addresses from unknown hosts. **Decided 15 November 2026 (Hannah, "yes on all"): the recommendation.**

## Source identities

Planning read: astrid-agent `a91c35dfd`, VibeComfy `dba38f86`. Base for code work: Release 13 as published plus the look-up-and-record fix (astrid-agent `r13/cells-model-lookup`), recorded at run start.

## References

- [Issue 665](https://github.com/banodoco/astrid-dev/issues/665): the model identification half
- [Strategy: version 0.2 candidates](../../strategy.md#candidates-not-yet-in-a-version)
- [Independent review](review.md)
