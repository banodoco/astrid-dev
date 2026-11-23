# Redacted retained installation receipts

## Installed generation and dependency witness

`program/current` is one generation ID. The corresponding `program/versions/<generation>/version.json` has the following shape. `env` is a dictionary of process settings. A single representative entry is shown and the rest of the values are omitted. Read the exact Runtime and Agent commits from the archived [profile tuple](../2026-11-23-save-profile/versions.json). The new diagnostic must generate an empty packaging/dependency diff from the installed Runtime SHA to its approved candidate and record SHA-256 inventory for `program/current` and the retained Python environment before and after the run.

```json
{
  "root": "/redacted/program/versions/<generation>",
  "python": "/redacted/program/versions/<generation>/py/bin/python",
  "profile": "/redacted/program/versions/<generation>/profile.json",
  "env": {"ASTRID_NODE_EXECUTABLE": "/redacted/pinned-node/bin/node"},
  "identity": {"release": 14, "managed_by": null}
}
```

## Direct-data source profile

The canonical `runtime/source-profiles/astrid.json` values are provenance and composition. An explicit diagnostic profile can use an independently verified source archive and the retained interpreter. The Runtime persists the supplied profile only after successful bootstrap. The SHA-bearing archive path and its tree proof are separate from installed identity fields.

```json
{
  "profile": "astrid",
  "runtime_checkout": "/redacted/exact-runtime-source",
  "source_checkout": "/redacted/program/versions/<generation>/py/lib/python3.11/site-packages",
  "runtime_environment": "/redacted/program/versions/<generation>/py",
  "worker_profile": null,
  "runtime_command": [],
  "protocol_version": "workspace.v1",
  "schema_version": "workspace-schema-v1",
  "capability_digest": "<redacted digest>",
  "source_digest": "<redacted digest>",
  "lock_digest": "<redacted digest>",
  "service_declaration": "/redacted/program/versions/<generation>/services.json"
}
```

## Direct-data catalog

The one selected realm and its exact root stay bound to the existing workspace. `source_profiles.astrid` is the same complete object as the source profile above. One compact representation is shown here.

```json
{
  "version": 1,
  "selected_realm_id": "<realm UUID>",
  "realms": [
    {
      "realm_id": "<same realm UUID>",
      "data_root": "/redacted/direct-data/runtime/realms/<realm UUID>",
      "display_name": "<synthetic realm name>",
      "selection_source": "<selection provenance>",
      "source_profile": "astrid"
    }
  ],
  "source_profiles": {"astrid": {"runtime_checkout": "/redacted/exact-runtime-source"}}
}
```
