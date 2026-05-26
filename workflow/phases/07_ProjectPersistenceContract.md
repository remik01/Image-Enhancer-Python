# Project Persistence Contract

## Goal

Implement versioned project save/load support for pipelines, image references, and settings.

## Tickets

* IEP-007

## Features to implement

* Define a JSON-like project file contract with required and optional fields.
* Serialize and deserialize project state through a persistence adapter.
* Validate malformed, missing, unknown, duplicate, and incompatible fields with source context.
* Add compatibility and round-trip tests.

## Constraints

* Do not expose domain internals as the wire format by accident.
* Do not add database persistence unless an ADR explicitly changes the accepted strategy.
* Do not store secrets or AI credentials in project files.
* Do not add UI save/load flows in this phase.

## Scope

* Persistence DTOs and explicit mappers.
* Project file schema documentation.
* Application project storage port implementation.
* Contract tests and fixture files.

## Out of Scope

* Desktop UI integration.
* REST endpoints for project files.
* Plugin package persistence beyond storing accepted operation identifiers and parameters.
* Runtime secrets storage.

## Architecture / Boundary Notes

Project files are external data contracts. Persistence DTOs belong in adapters, and mapping must be explicit before constructing application/domain models.

## Generated / Modified Artifacts

* src/image_workbench/adapters/persistence/__init__.py
* src/image_workbench/adapters/persistence/project_file.py
* src/image_workbench/adapters/persistence/project_mapper.py
* src/image_workbench/adapters/persistence/schema.py
* docs/architecture/project-file-contract.md
* tests/adapters/persistence/test_project_file_round_trip.py
* tests/adapters/persistence/test_project_file_validation.py
* tests/fixtures/projects/
* workflow/plans/07_project_persistence_contract_plan.md
* workflow/logs/phase-07-implementation-log.md

## Testing Expectations

* Round-trip tests for saving and loading representative project files.
* Contract tests for missing required fields, unknown fields, duplicate identifiers, malformed values, ordering, and version handling.
* Tests verify secrets are not serialized.

## Acceptance Criteria

* Saving and loading a project restores equivalent pipeline, image references, and settings with deterministic ordering.
* Invalid project files fail with safe source-context diagnostics.
* Project-file DTOs remain inside adapter code.
* docs/architecture/project-file-contract.md documents schema, versioning, compatibility, and known limitations.

## ADR / Decision-Log Follow-Up

* ADR: Required for accepted project persistence schema, versioning, compatibility, and migration policy.
* Decision log: Required for fixture and contract-test maintenance convention.

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

