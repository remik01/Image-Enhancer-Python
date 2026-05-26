# Rest Api Contracts Backend

## Goal

Implement REST API contracts and backend route adapters for application use cases without exposing domain internals as wire contracts.

## Tickets

* IEP-012

## Features to implement

* FastAPI route adapter for session, pipeline, execution, project, AI proposal, and job-status use cases accepted by prior phases.
* Request/response DTOs and explicit mappers.
* Exception handlers that translate application failures to safe HTTP responses.
* OpenAPI contract review or generated contract artifact if accepted by the ADR baseline.

## Constraints

* API DTOs must not be domain/application models by accident.
* Do not add public network exposure or authentication unless accepted by ADR.
* Do not add desktop UI code.
* Do not bypass application services from route handlers.

## Scope

* API adapter modules and tests.
* Bootstrap wiring for local API startup.
* Contract and error-handling tests.

## Out of Scope

* Desktop UI shell.
* Production deployment.
* External authentication/authorization.
* Remote storage or cloud hosting.

## Architecture / Boundary Notes

The API layer is an adapter. It maps HTTP DTOs to application commands/results and renders application failures without leaking technical internals or secrets.

## Generated / Modified Artifacts

* src/image_workbench/adapters/api/__init__.py
* src/image_workbench/adapters/api/app.py
* src/image_workbench/adapters/api/routes.py
* src/image_workbench/adapters/api/dtos.py
* src/image_workbench/adapters/api/mappers.py
* src/image_workbench/adapters/api/error_handlers.py
* src/image_workbench/bootstrap/api_runtime.py
* docs/architecture/rest-api-contract.md
* tests/adapters/api/test_routes.py
* tests/adapters/api/test_api_contracts.py
* tests/adapters/api/test_error_handlers.py
* workflow/plans/12_rest_api_contracts_backend_plan.md
* workflow/logs/phase-12-implementation-log.md

## Testing Expectations

* API route tests for valid requests, invalid payloads, unsupported operations, too-large payloads where limits exist, application failures, job-state responses, and safe diagnostics.
* Contract tests verify DTO shape and deterministic ordering.
* Architecture tests verify API code does not leak into domain/application.

## Acceptance Criteria

* Routes call application use cases through explicit commands/results.
* API DTOs are mapped explicitly and stay in adapter code.
* Error handlers return safe, deterministic responses for known failures.
* Local API startup is documented and configuration validation is enforced.

## ADR / Decision-Log Follow-Up

* ADR: Required if REST exposure model, authentication, public contract stability, or route compatibility policy changes from accepted decisions.
* Decision log: Required for local API startup command and contract fixture convention.

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

