# Project File Contract

## Purpose

Project files are versioned JSON adapter contracts for saving local workbench project state. They are not domain objects and must be mapped explicitly before application or domain models are constructed.

## Versioning

Phase 07 defines schema version `1`. Files with any other `schema_version` are rejected until a later ADR or migration phase accepts explicit migration behavior.

## V1 Schema

Required top-level fields:

- `schema_version`: integer, exactly `1`.
- `project`: object with `session_id` and `active_image_id`.
- `images`: array with exactly one image entry in v1.
- `pipelines`: array with exactly one pipeline entry in v1.
- `settings`: required empty object in v1.

Image entry fields:

- `image_id`: non-empty string.
- `source_uri`: string or `null`. Phase 07 writes the loaded `SessionSnapshot.source_uri` when the image reference has been resolved, and writes `null` before a source reference is available.
- `dimensions`: object with positive integer `width` and `height`.

Pipeline entry fields:

- `image_id`: non-empty string matching `project.active_image_id`.
- `steps`: ordered array of pipeline steps.

Step fields:

- `step_id`: non-empty string unique within the pipeline.
- `operation_id`: non-empty operation identifier validated by the domain operation catalog.
- `parameters`: object of numeric parameter values validated by the domain operation catalog.

## Validation Rules

Unknown fields are rejected at every defined object level. Missing required fields, duplicate identifiers, malformed values, unsupported schema versions, invalid operation parameters, and non-empty `settings` all fail with safe source-context diagnostics.

Secret-like fields such as API keys, passwords, tokens, credentials, and signing secrets are not supported in project files. Runtime secrets belong to runtime configuration, not persisted project state.

## Compatibility

V1 readers accept only version `1`. Future versions must add explicit migration or compatibility behavior and contract tests before being treated as supported.

## Known Limitations

- V1 stores one active session, not a multi-image project graph.
- V1 does not store undo/redo history, generated execution artifacts, export presets, plugin packages, runtime settings, AI credentials, or local secret-file paths.
- Loaded snapshots restore `can_undo` and `can_redo` as `False`.
- `source_uri` round-trips through `SessionSnapshot` when present, but may be `null` for sessions saved before the source image reference is loaded.
