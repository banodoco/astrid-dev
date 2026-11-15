# Moving a Version 0 installation out of Pinokio

This describes a fresh-workspace transfer tested on macOS, not an in-place
database conversion or a universal one-command migration. A Pinokio-managed
installation is still managed by
Pinokio: the [current setup guide](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/SKILL.md)
says not to run the standalone installer against it or offer a second install.
There is not yet a released, supported tool that converts every Version 0
installation to standalone. The [conversion plan](https://github.com/banodoco/astrid-dev/pull/625)
is still under review.

1. **Inventory the source.** Find the actual Pinokio installation, its active
   Runtime, selected workspace and data root. Record the projects, timelines,
   media, world-library documents and their objects, external timing files,
   custom effects, credentials, preferences and agent instructions to retain.
   A browser connection failure does not mean the installation or data is absent.
2. **Back up before changing anything.** Create and independently verify a
   complete Runtime backup, including media and its backup authentication key;
   keep a separate copy. Export the saved timelines you need as an additional
   safeguard, and verify ZIP integrity and referenced media hashes. Preserve
   world-library documents and objects, external files and custom effects
   separately. Timeline exports alone are not a complete workspace backup.
3. **Check the ownership result.** Read the current setup guide and installer.
   If the installation is Pinokio-managed, follow its Pinokio route. If the
   installer reports an ownership conflict or a missing legacy marker, keep
   the source and the printed log, and stop for a reviewed recovery. Do not
   overwrite a directory, invent ownership markers or delete the workspace to
   make the installer proceed.
4. **For an exceptional recovery, get an expert to review the specific
   machine.** The successful one-time recovery used a machine-specific tool to
   verify the backup against the live source, lock and identify the Runtime,
   stop its exact owner, and archive the active selection while retaining the
   original data. It then installed to a new standalone location and imported
   selected content into a fresh workspace. The restore used a reviewed Agent
   patched with [astrid-agent #346](https://github.com/banodoco/astrid-agent/pull/346)
   against the stock Runtime; stock archive import may fail or imported timelines
   may not edit correctly until that fix is merged and released. The retirement
   tool is not a published or portable migration command; reproducing it
   requires an independently reviewed procedure and explicit approval for that
   machine. See the conversion plan above.
5. **Restore and verify.** Map old project IDs to new ones when restoring
   world-library documents and objects, and restore preferences, credentials,
   instructions and custom effects separately as needed. Inspect the result of
   an interrupted import before retrying: a retry can create duplicates. Check
   Runtime health and that astrid.haus says Connected. Open each retained
   timeline, check its media and playback, save an edit and reopen it; check
   documents, credentials and instructions separately. Keep the original data
   and verified backup until the user confirms everything they need works.

For a separately supported standalone installation, use the installer and
connection checks in the current setup guide. Never run workspace or schema
migrations by hand.
