# Domain Model Pipeline Invariants

## Goal

Implement the framework-free domain model for images, enhancement operations, operation parameters, ordered pipelines, validation, and undo/redo-capable pipeline state.

## Tickets

* IEP-003

## Features to implement

* Domain value objects for image identifiers, image dimensions, operation identifiers, parameters, and pipeline step identifiers.
* Immutable pipeline definitions with deterministic ordering.
* Domain validation for supported operations, parameter ranges, duplicate step identifiers, and invalid ordering.
* Undo/redo domain state transitions for pipeline edits without UI or persistence coupling.

## Constraints

* Domain code must not import OpenCV, Pillow, FastAPI, OpenAI, HTTP clients, UI frameworks, persistence adapters, file-system DTOs, or plugin implementation modules.
* Do not implement actual image processing.
* Keep domain behavior deterministic and side-effect free.
* Use explicit types and docstrings for non-trivial public APIs.

## Scope

* Domain package source and domain tests.
* Invariant and boundary-case tests for pipeline construction and mutation.
* Domain exceptions for invalid state.

## Out of Scope

* Application services and ports.
* Adapter mappings.
* File loading, project persistence, REST API, UI, AI, plugins, and async execution.
* Golden image tests.

## Architecture / Boundary Notes

The domain owns business meaning only. Technical shape validation for files, API payloads, and external DTOs belongs to adapters, while orchestration belongs to application services.

## Generated / Modified Artifacts

* src/image_workbench/domain/models.py
* src/image_workbench/domain/operations.py
* src/image_workbench/domain/pipeline.py
* src/image_workbench/domain/history.py
* src/image_workbench/domain/exceptions.py
* src/image_workbench/domain/__init__.py
* tests/domain/test_pipeline_model.py
* tests/domain/test_pipeline_history.py
* tests/domain/test_operation_validation.py
* workflow/plans/03_domain_model_pipeline_invariants_plan.md
* workflow/logs/phase-03-implementation-log.md

## Testing Expectations

* Focused domain pytest tests for valid construction, invalid input, boundary parameter values, duplicate/conflicting steps, ordering, equality, and undo/redo edge cases.
* Existing architecture tests from Phase 02 must pass.
* Static-analysis commands from Phase 02 should pass for changed code.

## Acceptance Criteria

* Domain pipeline state is immutable or protects collection ownership.
* Invalid domain states fail fast with specific exceptions.
* Undo and redo behavior is deterministic and tested for empty, single-step, multi-step, and redo-clearing scenarios.
* Domain package has no forbidden framework, adapter, UI, HTTP, persistence, OpenAI, Pillow, or OpenCV imports.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if implementation changes aggregate boundaries, operation taxonomy, or invariant ownership beyond accepted ADRs.
* Decision log: Add entry for any accepted local naming or value-object convention not already covered.

## Codex/Copilot Execution Notes

Recommended implementation profile, if available:

* Model: gpt-5.3-codex
* Reasoning: extra high

If unavailable, use the strongest available coding model with high reasoning. Do not treat model availability as an acceptance criterion. Record the actual model/profile used when implementing the phase if the execution environment exposes that information.

Before implementation:

* Read `AGENTS.md`.
* Read this phase file.
* Check existing `docs/adr/`, `workflow/*.decision-log.md`, `workflow/plans/`, and relevant source code.
* Create or update a persisted plan under `workflow/plans/` if implementation touches multiple files or modules.
* Include a `## Rationale` section in persisted plans as required by `.github/instructions/planningPersistence.instructions.md`.
* Include a `## Trade-offs & Limitations` section in persisted plans as required by `.github/instructions/planningPersistence.instructions.md`.
* Do not implement out-of-scope items.
* Do not bypass architecture boundaries.

During implementation:

* Keep changes focused on this phase.
* Create or modify only the artifacts listed in `Generated / Modified Artifacts`, unless a newly discovered prerequisite is first recorded in the persisted plan or decision log.
* Add or update tests with the implementation.
* Record meaningful decisions in the decision log.
* Propose ADR discussion for architectural impact.

After implementation:

* Read `.github/instructions/static-analysis.instructions.md`.
* Run relevant static-analysis and verification checks for the changed modules.
* Fix static-analysis findings by addressing root causes rather than weakening rules or adding broad suppressions.
* Report remaining static-analysis findings, suppressions, skipped checks, or required governance follow-up.

Before committing phase work or review-remediation work for this phase:

* Use commit message format: `YYYY.MM.DD <login-name> <ticket-1> <ticket-2> ... <phase-title>: <commit-description>`.
* Use the current OS login name for `<login-name>` at commit time.
* Read tickets from this phase file's `## Tickets` section.
* Use this phase file's H1 title as `<phase-title>`.
* If this phase has no tickets, stop and correct the phase file before committing.

Before completion:

* Run relevant verification commands.
* Report changed files.
* Confirm that every referenced config file, workflow, script, module, and documentation artifact exists or is explicitly documented as external/local-only.
* Report tests executed.
* Report known weak points.

