# Batch Metadata Export Workflows

## Goal

Implement deterministic batch import, metadata, rename, and export workflows through application services and file-system adapters.

## Tickets

* IEP-006

## Features to implement

* Folder import with deterministic image ordering.
* Export presets for output format, destination, naming, and overwrite/conflict policy.
* Batch rename/export behavior.
* Metadata reading and metadata stripping workflows.
* Histogram analysis through an adapter boundary.

## Constraints

* Domain must not depend on file-system, metadata, or image library DTOs.
* Do not add project persistence format in this phase.
* Do not add UI or REST endpoints.
* Validate and normalize user-selected paths at the adapter boundary.

## Scope

* Application commands/results for batch and export use cases.
* File-system, metadata, and export adapters.
* Tests for deterministic ordering, malformed inputs, duplicate names, conflicts, and metadata edge cases.

## Out of Scope

* Project save/load files.
* AI prompt interpretation.
* Plugin operations.
* Async queue execution.
* Desktop UI integration.

## Architecture / Boundary Notes

File paths, metadata records, and export DTOs are external concerns. Adapters must map them into internal command/result models and preserve safe source context for failures.

## Generated / Modified Artifacts

* src/image_workbench/application/batch.py
* src/image_workbench/application/export.py
* src/image_workbench/adapters/filesystem/__init__.py
* src/image_workbench/adapters/filesystem/image_source.py
* src/image_workbench/adapters/filesystem/export_writer.py
* src/image_workbench/adapters/metadata/__init__.py
* src/image_workbench/adapters/metadata/metadata_reader.py
* src/image_workbench/adapters/metadata/histogram_analyzer.py
* tests/application/test_batch_workflows.py
* tests/adapters/filesystem/test_image_source.py
* tests/adapters/filesystem/test_export_writer.py
* tests/adapters/metadata/test_metadata_workflows.py
* workflow/plans/06_batch_metadata_export_workflows_plan.md
* workflow/logs/phase-06-implementation-log.md

## Testing Expectations

* Unit tests for deterministic import and export ordering.
* Adapter tests for path normalization, missing files, unsupported files, duplicate output names, overwrite conflicts, malformed metadata, and safe failure messages.
* Boundary-size tests with representative batch fixtures.

## Acceptance Criteria

* Given the same folder contents and preset, output order and names are stable across repeated runs.
* Invalid paths and malformed files fail with actionable safe diagnostics.
* Metadata stripping behavior is explicit and tested for no silent data loss.
* Domain and application layers remain independent of file-system and metadata adapter DTOs.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if implementation establishes durable export contract compatibility, metadata policy, or large-data processing policy.
* Decision log: Required for accepted conflict/overwrite behavior and deterministic ordering convention.

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

