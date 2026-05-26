# ADR-0003: Project Persistence And Local Plugin Contracts

## Status

Accepted

## Context

The overview requires repeatable projects containing pipeline definitions, image references, and settings. It also requires a plugin architecture for adding enhancement operations. Both features can easily leak external contracts or dynamic loading behavior into domain logic if they are not bounded early.

Persistence and plugins both need stable contracts, explicit mapping, validation, deterministic ordering, and compatibility rules. They must not introduce credentials, arbitrary unvalidated file access, or plugin implementation details into core models.

## Decision

Use a versioned JSON project-file contract for baseline project persistence.

Project files:

- Include a required schema/version field.
- Store pipeline definitions, image references, and settings in deterministic order.
- Do not store credentials or local credential-file contents.
- Are external data contracts owned by the persistence adapter.
- Are mapped explicitly into application/domain models.
- Validate missing fields, unknown fields, malformed values, duplicate identifiers, incompatible versions, and ordering-sensitive behavior with source context.

Use local configured plugin directories for the baseline plugin model.

Plugins:

- Provide a manifest with operation identifiers, operation metadata, parameter declarations, version compatibility, and entry point information.
- Register operations through an application-facing plugin contract.
- Are loaded only from normalized, configured local paths.
- Are treated as locally trusted extension code for the baseline.
- Must not be imported by domain code.
- Must fail safely on duplicate operation identifiers, incompatible versions, invalid manifests, or load failures.

Remote plugin registries, plugin marketplaces, package distribution, process isolation, and sandboxing are deferred.

## Alternatives Considered

### Option 1: Versioned JSON Project Files

This is accepted because it is readable, testable, deterministic, and sufficient for local project persistence.

### Option 2: Pickle Or Python Object Serialization

This is rejected because it is unsafe for untrusted input, poor as a stable contract, and too tightly coupled to implementation details.

### Option 3: Database Persistence

This is deferred because the overview only requires local project files and repeatable workflows, not query-heavy multi-user persistence.

### Option 4: Unversioned JSON

This is rejected because compatibility and migration behavior would become implicit.

### Option 5: Dynamic Plugin Imports Without Manifest

This is rejected because it would hide compatibility, operation metadata, and validation responsibilities.

### Option 6: Fully Sandboxed Plugin Runtime

This is deferred because it is a separate security and runtime architecture decision. The baseline documents local trust instead of pretending isolation exists.

## Consequences

### Positive

- Project files can be contract-tested with realistic fixtures.
- Persistence can evolve with explicit versioning and migration decisions.
- Plugin behavior becomes reviewable through manifests and application contracts.
- Domain models remain independent from project-file DTOs and plugin implementations.

### Negative / Tradeoffs

- JSON project files require explicit schema and mapper maintenance.
- Local trusted plugins are not safe for arbitrary untrusted code.
- Plugin compatibility rules must be maintained as operation contracts evolve.

### Operational Impact

- Users need clear documentation about where plugin paths are configured.
- Project files should be portable when image-reference policies allow it.
- Invalid project files and plugin manifests must fail with actionable local diagnostics.

### Testing and Verification Impact

- Persistence requires round-trip, malformed-file, unknown-field, missing-field, duplicate-id, and compatibility tests.
- Plugin loading requires path normalization, manifest validation, duplicate/conflict, incompatible-version, and safe failure tests.
- Architecture checks must prevent plugin implementation imports from domain.

## Follow-Up Work

- Phase 07 documents and implements the project-file contract.
- Phase 10 documents and implements the plugin contract and sample plugin.
- Revisit this ADR before adding database persistence, project-file migration complexity, remote plugin distribution, or plugin isolation.

