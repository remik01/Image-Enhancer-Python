# ADR-0005: Project File Schema Versioning

## Status

Accepted

## Context

ADR-0003 accepts versioned JSON project files as the baseline persistence strategy. Phase 07 must define the first concrete contract for saving and loading project state containing pipeline definitions, image references, and settings while preserving layer boundaries.

The current application persistence port stores and loads `SessionSnapshot`, which represents one active session, image dimensions, source URI when the source reference has been loaded, and a pipeline. It does not carry export presets, runtime configuration, secrets, or undo/redo history. A schema decision is needed so Phase 07 does not silently invent a broader project aggregate or accidentally expose domain internals as the wire format.

## Decision

Use a versioned JSON v1 project-file contract owned by the persistence adapter.

The v1 contract stores one active session. Required top-level fields are `schema_version`, `project`, `images`, `pipelines`, and `settings`. Version `1` is the only accepted schema version in this phase. Unknown fields are rejected at every defined object level.

The `project` object stores `session_id` and `active_image_id`. The `images` array stores image identifiers, nullable source URIs, and dimensions. The `pipelines` array stores image-scoped ordered pipeline steps with operation identifiers and numeric parameters. The `settings` object is required but must be empty in v1.

Project-file DTOs remain inside `image_workbench.adapters.persistence`. Mapping into `SessionSnapshot`, `ImageId`, `ImageDimensions`, `EnhancementPipeline`, `PipelineStep`, and `OperationParameters` must be explicit and deterministic.

## Alternatives Considered

### Option 1: Single-Session V1 JSON Contract

Accepted. This matches the current application persistence port, keeps the first contract small, and still establishes explicit versioning, DTO validation, and deterministic mapping.

### Option 2: Multi-Image Project Aggregate

Rejected for Phase 07. It may become the right shape once UI, batch, and project-level orchestration are implemented, but adding it now would require new application contracts beyond current service behavior.

### Option 3: Adapter-Only SessionSnapshot Serialization

Rejected. Directly serializing current application/domain structures would make the wire format depend on implementation details and would not satisfy the phase requirement for explicit DTOs, schema documentation, and compatibility policy.

### Option 4: Free-Form Settings Map

Rejected. Free-form settings would make compatibility and secret-exclusion rules weak. V1 reserves a typed settings object but requires it to be empty until future phases define concrete non-secret settings.

### Option 5: Database Persistence

Rejected for this phase. ADR-0003 and Phase 07 require local versioned JSON project files, and database persistence would need a separate ADR.

## Consequences

### Positive

- The first project-file contract is small enough to review and contract-test.
- Persistence DTOs stay isolated inside the adapter layer.
- Future schema changes have a clear version gate and migration trigger.
- The contract reserves settings space while preserving loaded image source references without inventing runtime or UI state.

### Negative / Tradeoffs

- V1 does not represent multi-image project graphs, undo/redo history, execution artifacts, export presets, or plugin package state.
- Source URI values are nullable because a session may be saved before the image reference has been resolved.
- Future schema versions must add explicit migration behavior rather than being silently accepted.

### Operational Impact

- Invalid files fail during adapter validation with safe file and field context.
- Project files must not contain credentials, API keys, local secret-file contents, or runtime-only settings.

### Testing and Verification Impact

- Tests must cover round-trip behavior, deterministic serialization, missing and unknown fields, duplicate identifiers, incompatible versions, malformed values, and secret exclusion.
- Contract fixtures under `tests/fixtures/projects/` become review artifacts and must be updated only with intentional schema changes.

## Follow-Up Work

- Phase 07 implements the v1 adapter, mapper, schema documentation, and contract fixtures.
- Revisit this ADR before adding multi-image project aggregates, project-file migration support, persisted export presets, plugin package persistence, runtime settings, or database persistence.
- Later UI/API phases should call application-facing project persistence behavior rather than reading or writing project-file DTOs directly.
