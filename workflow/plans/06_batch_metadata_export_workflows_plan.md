# Phase 06 Batch Metadata Export Workflows Plan

## Status

In progress.

## Context

Phase 06 implements deterministic folder import, metadata, rename, and export workflows for IEP-006. The work spans application use-case models, filesystem adapters, metadata adapters, tests, decision-log evidence, and phase coverage review.

## Goal

Add batch import and export capabilities that remain deterministic, preserve domain/application boundaries, translate filesystem and image-library failures into safe diagnostics, and make metadata stripping explicit.

## Non-Goals

- Do not introduce project save/load persistence.
- Do not add UI, REST, AI prompt interpretation, plugins, or async queue execution.
- Do not add a new image processing dependency beyond the existing Pillow dependency.
- Do not define a public export compatibility contract beyond the local adapter behavior needed for this phase.

## Assumptions

- Folder import treats common Pillow-readable image extensions as candidate images and rejects malformed candidates when metadata is read.
- Batch ordering is casefolded filename order with resolved path as the tie-breaker for reproducibility across repeated runs.
- Export conflict behavior is caller-selected through a preset and supports `fail`, `overwrite`, and deterministic `rename`.
- Metadata stripping is explicit in the export preset and defaults to stripping metadata to avoid silent carry-over.

## Rationale

Phase 04 already established application-owned ports and focused services, while ADR-0001 requires technical libraries and filesystem details to stay in adapters. Adding batch/export models in new application modules preserves that direction without bloating existing session and execution services. The filesystem and metadata adapters own path normalization, image discovery, Pillow metadata parsing, histogram calculation, and concrete writes because those are external concerns.

The chosen approach keeps ordering, naming, and conflict policy reviewable in application-facing models while leaving path safety and image-library failure translation at adapter boundaries. A heavier project-level export contract or persistence format would be premature because Phase 07 owns project persistence and this phase only needs deterministic local export behavior.

## Trade-offs & Limitations

- The export format support is intentionally limited to PNG and JPEG because those are enough to prove the workflow with the existing Pillow dependency.
- The histogram adapter returns fixed 256-bin RGB channel tuples instead of a richer analysis model; richer analytics can be added when a later phase needs them.
- Metadata reading captures dimensions, format, mode, and safe tag names rather than exposing raw EXIF values through application models.
- The deterministic rename policy uses numeric suffixes and does not attempt cross-process locking; callers that need concurrent export guarantees need a later runtime policy.

## Implementation Approach

1. Add `application.batch` models and service for deterministic batch import through a batch image source port.
2. Add `application.export` models, preset validation, filename planning, and service orchestration through an export writer port.
3. Add filesystem adapters for folder discovery and export writing with path normalization and conflict handling.
4. Add metadata adapters for Pillow metadata reading and RGB histogram analysis.
5. Add focused application and adapter tests for ordering, malformed inputs, duplicate names, conflicts, metadata stripping, and boundary behavior.
6. Update the decision log, phase log, and implementation coverage review with evidence.

## Tests And Verification

- Run focused tests for application batch/export workflows and new adapters while implementing.
- Run `python -m pytest`, `python -m ruff check .`, `python -m ruff format --check .`, `python -m mypy .`, and `git diff --check` before closeout.
- Run the phase helper scripts for verification suggestions, artifact coverage, implementation coverage review, and review pack.

## ADR / Decision-Log Needs

No ADR is expected unless implementation changes dependency direction, adds a new public file contract, or establishes a reusable metadata compatibility policy. A decision-log entry is required for deterministic ordering and export conflict behavior.
