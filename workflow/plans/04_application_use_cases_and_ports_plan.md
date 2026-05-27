# Phase 04 Implementation Plan: Application Use Cases And Ports

## Status

In progress.

## Context

Phase 04 requires implementing application-layer commands, results, exceptions, ports, and services that orchestrate domain workflows without adapter dependencies. The repository currently has only `src/image_workbench/application/__init__.py`, so this phase establishes the initial application boundary contracts and orchestration behavior for later adapter/UI/API phases.

## Goal

Deliver the phase-04 artifacts under `src/image_workbench/application/` and `tests/application/` with explicit command/result contracts, fake-port orchestration tests, meaningful application failure translation, and phase evidence required for strict coverage review closeout.

## Non-Goals

- Implementing adapter logic, file I/O, image-processing internals, REST handlers, desktop UI behavior, or async worker runtime.
- Defining persistence formats, project serialization details, or plugin runtime loading behavior.
- Expanding domain invariants beyond phase-03 behavior.

## Assumptions

- Application services are decomposed into three focused boundaries: `SessionService`, `PipelineService`, and `ExecutionService`.
- Commands and results are immutable dataclasses and carry explicit internal types.
- Port interfaces are defined as application-owned protocols for later adapter implementation, with no direct external client dependencies in this phase.

## Rationale

The selected approach balances phase-04 scope completeness with boundary safety from ADR-0001. Defining commands/results and ports first keeps adapter, API, and UI phases decoupled from orchestration details, while three focused services avoid a catch-all coordinator and preserve clear reasons to change.

Alternatives considered:

1. A single application service handling all workflows. Rejected because it would mix session state, pipeline editing, and execution concerns, reducing maintainability and reviewability.
2. Defining only services now and delaying typed commands/results until adapter phases. Rejected because explicit command/result contracts are an acceptance criterion and are needed to stabilize downstream boundaries.
3. Defining concrete in-memory adapter implementations inside application for convenience. Rejected because it would violate layer ownership and couple application to technical concerns.

This plan would change only if a new ADR accepted different application boundary ownership or if phase requirements explicitly narrowed scope away from shared command/result contracts.

## Trade-offs & Limitations

- Defining the full port surface early introduces interfaces that may evolve in later phases as real adapters reveal stricter needs.
- Explicit command/result models increase upfront code volume compared with direct service method arguments.
- Failure translation is intentionally application-centric and may need refinement when adapter error taxonomies are introduced.
- Session management remains in-memory for this phase; persistence behavior is deferred to later phases.

## Implementation Approach

1. Add application exceptions and typed command/result models for session lifecycle, pipeline editing, proposal validation, and execution requests.
2. Add application port protocols for image source access, metadata access, image processing, export writing, project storage, AI interpretation, plugin discovery, queue execution, and diagnostics.
3. Implement `SessionService`, `PipelineService`, and `ExecutionService` with deterministic orchestration and explicit failure translation.
4. Export the new application API from `src/image_workbench/application/__init__.py`.
5. Add fake-port tests for happy path and failure propagation/translation across pipeline and execution workflows.
6. Generate phase artifact coverage and implementation coverage review files, resolve matrix statuses with evidence, and validate strict-open-items.

## Affected Layers

- Application layer modules under `src/image_workbench/application/`.
- Application unit tests under `tests/application/`.
- Workflow artifacts under `workflow/plans/`, `workflow/logs/`, and `workflow/phases/`.

## Tests And Verification

- `python -m pytest`
- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy .`
- `python -m pip check`
- `python .github\skills\implement-phase\scripts\suggest_phase_verification.py --phase 4`
- `python .github\skills\implement-phase\scripts\check_phase_artifact_coverage.py --phase 4`
- `python .github\skills\implement-phase\scripts\phase_implementation_coverage_review.py --phase 4`
- `python .github\skills\implement-phase\scripts\phase_review_pack.py --phase 4`
- `python .github\skills\implement-phase\scripts\phase_implementation_coverage_review.py --phase 4 --validate --strict-open-items`

## Risks

- Overly broad port method signatures could leak technical details into application contracts.
- Service boundaries could drift into cross-cutting orchestration if command ownership is not kept strict.
- Failure contracts may be incomplete for some port capabilities until adapters are implemented and exercised.

## ADR / Decision-Log Needs

- ADR review is required if command/result compatibility policy, shared service conventions, or dependency direction changes beyond ADR-0001 boundaries.
- Append a decision-log entry only when a durable local service-grouping or port-naming convention is introduced beyond existing governance.
