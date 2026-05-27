# Phase 05 Implementation Plan: Local Image Processing Adapters

## Status

Completed 2026.05.27.

## Context

Phase 05 implements local deterministic image-processing adapters behind the
application-owned `ImageProcessingPort`. The application port already exists
from Phase 04, and the domain catalog currently validates operation identifiers
before adapter execution.

## Goal

Deliver a Pillow-backed local image-processing adapter for blur, sharpen,
contrast, and sepia with explicit step-to-library mapping, golden output tests,
safe failure translation, and phase governance evidence.

## Non-Goals

- Do not implement batch traversal, metadata extraction, persistence, AI,
  plugin loading, UI previews, REST endpoints, or export workflows.
- Do not introduce OpenCV as a runtime dependency in this phase.
- Do not expose Pillow or image-library types through domain or application
  contracts.

## Assumptions

- Pillow is the canonical local image-processing backend for Phase 05.
- `blur` and `sepia` must be added to the domain operation catalog because
  adapter execution receives already-validated `PipelineStep` objects.
- Adapter output may be written to a deterministic local filesystem path owned
  by the adapter without adding project persistence or export behavior.

## Rationale

The Pillow-only approach satisfies the baseline deterministic operations with
one small, well-supported dependency and avoids duplicating implementation and
test surface across two image libraries. Adding `blur` and `sepia` to the domain
catalog keeps semantic operation validation in the domain layer instead of
allowing adapters to accept operation identifiers that the application cannot
construct as valid pipeline steps.

Alternatives considered:

1. Implement Pillow and OpenCV together. Rejected for this phase because it
   adds dependency and compatibility risk without a current requirement for
   OpenCV-specific capabilities.
2. Keep the domain catalog unchanged and test only `contrast` and `sharpen`.
   Rejected because the phase explicitly requires `blur` and `sepia`, and those
   operations would remain unreachable through the application port.
3. Treat `blur` and `sepia` as adapter-local technical operations. Rejected
   because that would duplicate operation semantics outside the domain and
   weaken pipeline validation.

This decision should be revisited if future phases require OpenCV-only
algorithms, GPU/native acceleration, or long-term cross-library golden-image
compatibility.

## Trade-offs & Limitations

- Deferring OpenCV keeps Phase 05 smaller but means OpenCV parity is not proven.
- Golden-image output is tied to Pillow behavior and may need deliberate
  refresh if Pillow changes rendering details in a future dependency update.
- The adapter writes a concrete output image file because the Phase 04
  `ExecutionArtifact` contract carries metadata, not in-memory image bytes.
- The RGB pixel tolerance is intentionally narrow; it catches meaningful output
  drift but may require fixture review after dependency upgrades.

## Implementation Approach

1. Add Pillow to project dependencies and extend domain operation validation for
   `blur.radius` and `sepia.intensity`.
2. Add adapter exception types and deterministic mappers from pipeline steps to
   Pillow operation functions.
3. Implement a `PillowImageProcessor` that resolves local image references,
   opens supported images, applies each step in order, writes PNG output, and
   returns an `ExecutionArtifact`.
4. Add focused golden-output and failure-translation tests with local fixtures.
5. Record the Pillow-only backend decision, golden tolerance, and fixture
   maintenance convention in the decision log and phase log.
6. Generate and complete phase artifact and implementation coverage evidence.

## Affected Layers

- Domain: operation catalog only, to make Phase 05 operations valid pipeline
  steps.
- Adapters: local image-processing implementation and failure translation.
- Tests: domain operation coverage plus adapter golden and failure tests.
- Workflow artifacts: plan, phase log, decision log, coverage review, and review
  pack evidence.

## Tests And Verification

- `python -m pytest`
- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy .`
- `python -m pip check`
- `git diff --check`
- Phase helper scripts for verification suggestions, artifact coverage,
  implementation coverage review, review pack generation, and strict coverage
  validation.

## Risks

- Pillow may not be installed in an existing editable environment until
  dependencies are refreshed.
- Golden fixtures can become stale after intentional operation changes or
  dependency upgrades.
- Adding domain operations in an adapter phase is a controlled prerequisite but
  broadens Phase 05 beyond adapter-only source files.

## ADR / Decision-Log Needs

No ADR is required for Phase 05 because the dependency direction and application
port contract remain unchanged. The Pillow-only backend choice, golden tolerance,
and fixture maintenance convention are durable local decisions and must be
recorded in `workflow/CLI.decision-log.md`.
