# RA-0a: what is measured, what is not, and the recalculated estimate (24 November 2026)

By the Plan 82 orchestrator. Read-only on the product. Sources: the [floor experiment](../2026-11-24-thin-client-floor/README.md) (installed Release 15 build `a09ea669`, stand-in ComfyUI, 10 samples), the [startup baseline's import profile](../2026-11-24-startup-baseline/README.md#the-import-profile-of-a-real-generate-ra-0a-import-part) (dev checkout `514499de`, stand-in, loaded box), and [why each check](../2026-11-24-why-each-check/README.md).

## What the existing measurements already answer

The installed command to "task queued" has a median of **5.36 s** (run 1: 5.80, run 2: 5.20); Part 2b's 5.83 s is the same build. Stage medians over the ten samples, in seconds: pack discovery 2.19, workflow build 0.58, emission 0.43, other command work 0.41, pack-host attachment 0.40, approval compile 0.31, launcher connection 0.18, source identity 0.15, interpreter start 0.12. Imports are 0.87 s under `-X importtime` (1,284 modules) and are spread across those stages by the collector, not a stage of their own. With a warm resident host and today's code the same command is 4.33 s, so most of the cost is what is repeated, not the process.

## The estimate, recalculated so each second is counted once

The card estimates add to about 2.3 s *est.* (RA-0b 1.0, RA-1b 0.2, RA-2 1.1). Counted once against the stage table:

| Card | Stage it removes | Stage median | Saving counted | Overlap and caveat |
|---|---|---:|---:|---|
| RA-0b | pack discovery (live checks stay) | 2.19 | about 1.0 to 1.4 | The live checks (duplicate-name admission, pending transaction, managed inventory, own and project witness) still run; the floor experiment did not measure them. The import of the pack loader (0.13 s) sits inside this stage |
| RA-2a | workflow build, most of emission | 0.58 + 0.43 | about 0.6 to 0.8 | Emission keeps the per-request render (0.20 s in a warm host); only the value-independent part is reused |
| RA-2b | the second approval compile | 0.31 | about 0.2 | Values and projection are recomputed each request (0.025 s each in a warm host) |
| RA-1b | imports no `generate` needs | within several stages | about 0.1 to 0.2 | `generic_host` (0.45 to 0.6 s in my profile) is imported by pack-host attachment, which the command really does; some of it may not be avoidable. Overlaps the attachment stage |

**Recalculated: 5.36 − (1.0 to 1.4) − (0.6 to 0.8) − 0.2 − (0.1 to 0.2) ≈ 2.8 to 3.4 s, central about 3.1 s *est.***, on this box with the stand-in. The target "about 3 s" is plausible, with little margin; the floor experiment's earlier "near 2 s" assumed the disk caches also removed attachment, launcher connection and source identity (0.73 s together), which Plan 82 does not cache. **No timing in this note is a promise;** the installed baseline on the exact heads (R) decides.

## What is not measured, and why

- **A real ComfyUI's node list and model-root hashing (`validate_model_root_binding(verify_files=True)`) on a managed target.** They need a real ComfyUI with models, which this container does not have (no GPU, no models; the stand-in serves 13 classes). The floor experiment measured the node list at 0.005 s on the stand-in. These two are not taken; they decide Plan 92's GS-4 and do not gate Plan 82, because Plan 82 keeps both every command (the [check table](../2026-11-24-why-each-check/README.md)). If the Lead wants them for Plan 92 they need the owner's machine, which is hers to approve.
- The per-command witness for own and project packs; the rebuild cost on a miss (0.58 s, from the floor experiment); and any timing on a person's machine.

## The import profile

`python -X importtime` of a real `generate` is in the startup baseline folder with the script, the importer of each heavy module and both runs' summaries. In short, the three modules the floor experiment named are imported by the pack-host attachment (`generic_host`), the catalog workflow preparation (`comfy_schema`) and the approval compile (`vibecomfy.porting.emit.ui`, which also pulls `numpy` through `comfy_nodes`). P82-02 (RA-1b) starts from that table.
