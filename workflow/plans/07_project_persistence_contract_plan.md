# Phase 07 Project Persistence Contract Plan

## Status

In progress.

## Context

Phase 07 implements IEP-007: versioned JSON project-file persistence for pipelines, image references, and settings. ADR-0003 already accepts versioned JSON project files as the baseline persistence direction, and this phase must make the concrete schema, versioning, compatibility, fixture, and test conventions explicit.

## Goal

Implement a v1 project-file persistence adapter that saves and loads one workbench session snapshot with deterministic pipeline ordering, explicit DTO mapping, safe validation diagnostics, contract documentation, ADR coverage, and contract fixtures.

## Non-Goals

- Do not add database persistence.
- Do not add UI, REST, CLI, or bootstrap save/load flows.
- Do not persist runtime secrets, AI credentials, local secret-file paths, plugin packages, or undo/redo history.
- Do not broaden the existing application services beyond the current `ProjectStoragePort` use.

## Assumptions

- The v1 project file represents a single active session because the current application model has `SessionSnapshot`, not a multi-image project aggregate.
- The project file contains a required empty `settings` object in v1. Unknown setting keys are rejected so future settings additions require explicit compatibility decisions.
- `source_uri` is nullable before an image reference is loaded, but loaded source references must round-trip through `SessionSnapshot` and project-file persistence.
- Loaded snapshots set `can_undo` and `can_redo` to `False` because undo/redo stacks are runtime editing state, not v1 persistence state.

## Rationale

The repository already has `ProjectStoragePort` shaped around `SessionSnapshot`, and Phase 7 can satisfy the persistence contract without inventing a broader project aggregate ahead of UI, REST, and multi-image workflow phases. A single-session v1 format keeps the contract reviewable, gives future phases a stable versioned baseline, and avoids leaking adapter DTOs into application or domain code.

Keeping `settings` as a required empty object is intentionally conservative. It reserves schema space for future settings while preventing untyped free-form data, accidental secret serialization, or UI/runtime concerns from becoming part of the contract before those phases define them. Nullable `source_uri` is also explicit: unloaded sessions can be saved before a source reference exists, while loaded source references remain durable project-file state.

The persistence adapter will own JSON reading/writing, DTO validation, schema shape checks, and safe failure diagnostics. The mapper will construct application/domain models only after technical shape validation, preserving the anti-corruption boundary required by ADR-0001 and ADR-0003.

## Trade-offs & Limitations

- V1 restores one session snapshot, not a full multi-image project graph.
- V1 records no undo/redo history, generated execution artifacts, export presets, batch import state, plugin packages, or runtime configuration.
- `source_uri` is only as complete as the application snapshot: sessions saved before reference loading will still contain `null`.
- The compatibility policy accepts only schema version `1` and rejects future versions until a later migration phase adds explicit migration behavior.

## Implementation Approach

1. Create ADR-0005 for v1 project-file schema, versioning, compatibility, and migration policy.
2. Add `adapters/persistence` with DTO validation helpers, mapper functions, and `ProjectFileStorage` implementing `ProjectStoragePort`.
3. Document the v1 project-file contract under `docs/architecture/project-file-contract.md`.
4. Add valid and invalid project fixtures under `tests/fixtures/projects/`.
5. Add round-trip and validation tests for deterministic serialization, malformed fields, unknown fields, duplicates, incompatible versions, and no secret serialization.
6. Update the decision log, phase log, and implementation coverage review with evidence.

## Tests And Verification

- Run focused persistence adapter tests while implementing.
- Run `python -m pytest`, `python -m ruff check .`, `python -m ruff format --check .`, `python -m mypy .`, `python -m pip check`, and `git diff --check` before closeout.
- Run phase helper scripts for verification suggestions, artifact coverage, implementation coverage review, and review pack.

## ADR / Decision-Log Needs

ADR required: v1 project-file schema, versioning, compatibility, and migration policy.

Decision-log entry required: fixture and contract-test maintenance convention for project-file samples.
