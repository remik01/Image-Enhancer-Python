# Phase 03 Implementation Plan: Domain Model Pipeline Invariants

## Status

Completed 2026.05.27.

## Context

Phase 03 (`workflow/phases/03_DomainModelPipelineInvariants.md`) requires a framework-free domain model for ordered enhancement pipelines, operation and parameter validation, and undo/redo-capable pipeline state transitions. The repository currently has only a domain package scaffold, so the phase must establish the initial domain model and tests while preserving ADR-0001 layered boundaries.

## Goal

Deliver the phase-03 domain artifacts (`models.py`, `operations.py`, `pipeline.py`, `history.py`, `exceptions.py`, domain exports, and domain tests) with deterministic behavior, invariant enforcement, and coverage evidence required for phase closeout.

## Non-Goals

- Implementing image processing algorithms or adapter integrations.
- Implementing application services, ports, REST contracts, UI behavior, persistence, plugins, or async execution.
- Changing architecture-test policy introduced in phase 02 except as needed to keep phase-03 artifacts compliant.

## Assumptions

- Pipeline ordering is a domain concern represented by deterministic step sequence and explicit index-based edit operations.
- Operation parameters are numeric for this phase and validated against operation definitions and ranges in the domain layer.
- Existing phase-02 quality gates (`pytest`, `ruff`, `mypy`, `pip check`) remain the verification baseline for this phase.

## Rationale

The chosen implementation path centers domain invariants in immutable value objects and deterministic pipeline/history models because the phase acceptance criteria emphasize fast failure, explicit ownership, and deterministic undo/redo behavior. Using frozen dataclasses and tuple-backed collections keeps mutation authority local to domain methods, aligns with `.github/instructions/domain.instructions.md`, and reduces accidental aliasing risks that would otherwise violate review-checklist ownership requirements.

A second design choice is to separate operation catalogs/parameter-range rules (`operations.py`) from pipeline orchestration (`pipeline.py`) and history transitions (`history.py`). This keeps each module responsible for one domain concept and avoids a monolithic type that would mix validation taxonomy, sequence rules, and state-transition rules.

Alternatives considered:

1. A single "pipeline aggregate" module with nested classes and mixed validation logic. Rejected because it obscures boundaries between operation taxonomy and edit-state transitions, making tests less targeted.
2. Mutable list-backed pipeline and history classes. Rejected because mutable exposure complicates ownership guarantees and makes undo/redo determinism easier to break.
3. Deferring operation parameter validation to a later application phase. Rejected because this phase explicitly requires domain-level supported-operation and parameter-range validation.

The rejected alternatives become preferable only if later ADRs explicitly move invariant ownership out of domain (which would conflict with current ADR-0001), or if runtime-driven operation schemas require adapter-owned validation contracts beyond phase-03 scope.

## Trade-offs & Limitations

- Restricting parameter values to numeric ranges simplifies invariant handling in this phase but postpones support for non-numeric parameter types that some operations may need later.
- Explicit value objects and deterministic tuple transformations increase file count and boilerplate versus a lightweight script-style model.
- Index-based ordering APIs are strict and predictable, but they require callers to manage insertion/move positions explicitly instead of relying on implicit reordering heuristics.
- The phase intentionally avoids extensibility hooks for plugins/adapters, so future phases may need mapper or contract adjustments when integrating external operation definitions.

## Implementation Approach

1. Define domain exception taxonomy for invalid identifiers, parameter violations, duplicate step identifiers, ordering errors, and undo/redo boundary errors.
2. Implement value objects and immutable parameter carriers in `models.py` for image identifiers, dimensions, operation identifiers, and pipeline step identifiers.
3. Implement operation definitions and parameter-range validation in `operations.py` with explicit supported-operation catalog and deterministic lookups.
4. Implement immutable pipeline model and edit methods in `pipeline.py`, including duplicate-step checks, ordering validation, and operation/parameter invariant enforcement.
5. Implement undo/redo state transitions in `history.py` with deterministic past/present/future tuple semantics and redo clearing on new edits.
6. Update `src/image_workbench/domain/__init__.py` to expose phase-03 domain API intentionally.
7. Add focused tests under `tests/domain/` for construction invariants, ordering conflicts, parameter range enforcement, and undo/redo edge cases.
8. Generate phase closeout evidence using phase helper scripts and strict implementation coverage validation.

## Affected Layers

- Domain layer: new domain model modules and exports.
- Test layer: focused domain tests and existing architecture checks.
- Workflow artifacts: phase plan, phase log updates, implementation coverage review, and review pack.

## Tests And Verification

- `python -m pytest`
- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy .`
- `python -m pip check`
- `python .github\skills\implement-phase\scripts\suggest_phase_verification.py --phase 3`
- `python .github\skills\implement-phase\scripts\check_phase_artifact_coverage.py --phase 3`
- `python .github\skills\implement-phase\scripts\phase_implementation_coverage_review.py --phase 3`
- `python .github\skills\implement-phase\scripts\phase_review_pack.py --phase 3`
- `python .github\skills\implement-phase\scripts\phase_implementation_coverage_review.py --phase 3 --validate --strict-open-items`

## Risks

- Overly strict ordering semantics could conflict with later application workflows; mitigate by keeping ordering rules explicit and tested.
- Parameter catalog choices in this phase may not match later adapter/plugin capabilities; mitigate by documenting operation taxonomy and constraining to phase scope.
- Missing phase-artifact evidence can block closeout even when code is correct; mitigate with helper scripts and strict coverage validation before handoff.

## ADR / Decision-Log Needs

- ADR: not expected if implementation stays within ADR-0001 boundaries and does not redefine aggregate ownership or dependency direction.
- Decision log: append a concise entry only if a durable local naming/value-object convention is introduced beyond existing ADR and instruction guidance.
