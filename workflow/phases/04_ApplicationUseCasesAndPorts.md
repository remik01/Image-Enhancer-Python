# Application Use Cases And Ports

## Goal

Implement application-layer commands, results, services, and ports that orchestrate image session and pipeline workflows without depending on adapter implementations.

## Tickets

* IEP-004

## Features to implement

* Commands and results for loading image references, editing pipelines, validating pipeline proposals, and requesting execution.
* Application services for session creation, pipeline editing, undo/redo orchestration, and local execution orchestration through ports.
* Ports for image processing, image source access, metadata access, export writing, project storage, AI interpretation, plugin discovery, queue execution, and diagnostics where needed by later phases.
* Application exceptions and failure-result contracts.

## Constraints

* Application code must not import adapters, FastAPI routes, UI classes, Pillow, OpenCV, OpenAI clients, persistence DTOs, or file-system implementation details.
* Do not implement external calls or image-processing behavior.
* Keep commands/results explicit and typed.
* Avoid catch-all services with unrelated reasons to change.

## Scope

* Application package source and tests with fake ports.
* Boundary contracts consumed by later adapter, API, UI, plugin, AI, and persistence phases.
* Deterministic ordering and failure translation at use-case boundaries.

## Out of Scope

* Adapter implementations.
* REST route handlers.
* Desktop UI.
* Async worker implementation.
* Project file serialization.

## Architecture / Boundary Notes

Ports belong in application only when they stabilize a real boundary. Port methods should use internal domain/application models, not external DTOs or framework request objects.

## Generated / Modified Artifacts

* src/image_workbench/application/commands.py
* src/image_workbench/application/results.py
* src/image_workbench/application/ports.py
* src/image_workbench/application/services.py
* src/image_workbench/application/exceptions.py
* src/image_workbench/application/__init__.py
* tests/application/test_pipeline_service.py
* tests/application/test_execution_service.py
* tests/application/test_application_failures.py
* workflow/plans/04_application_use_cases_and_ports_plan.md
* workflow/logs/phase-04-implementation-log.md

## Testing Expectations

* Application unit tests use fake ports rather than real adapters.
* Tests cover happy path, invalid command input, domain validation propagation, port failure handling, deterministic ordering, and undo/redo orchestration.
* Architecture tests verify application does not import adapters or frameworks.

## Acceptance Criteria

* Application services expose explicit commands/results and depend only on domain and application-owned contracts.
* Fake-port tests prove orchestration behavior without external systems.
* Known port failures translate into meaningful application failures with safe context.
* Static-analysis and architecture checks from Phase 02 remain passing.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if implementation introduces shared service conventions, public command/result contracts with compatibility implications, or changes dependency direction.
* Decision log: Add entry for accepted application service grouping and port naming conventions if not already covered.

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

