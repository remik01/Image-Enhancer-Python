# Local Image Processing Adapters

## Goal

Implement local image-processing adapters for baseline deterministic enhancement operations behind application ports.

## Tickets

* IEP-005

## Features to implement

* Pillow and/or OpenCV adapter implementation for baseline operations: blur, sharpen, contrast adjustment, and sepia.
* Explicit mapping between application pipeline steps and adapter operation parameters.
* Golden image fixtures and deterministic output comparison strategy.
* Adapter failure translation for unsupported formats, invalid parameters that reach the boundary, unreadable images, and processing failures.

## Constraints

* Do not import Pillow or OpenCV from domain or application.
* Do not add AI, plugin, UI, REST, persistence, or batch orchestration behavior.
* Golden image tolerances must be explicit and justified.
* Avoid avoidable duplicate full-size image buffers across boundaries.

## Scope

* Image-processing adapter source and tests.
* Golden image fixtures for baseline operations.
* Boundary diagnostics for image-processing failures.

## Out of Scope

* Batch folder traversal.
* Metadata stripping/reading.
* Project persistence.
* AI-generated pipelines.
* Desktop UI previews.

## Architecture / Boundary Notes

Adapters implement application ports and map internal pipeline operations to technical library calls. External image library types must not cross back into application or domain contracts.

## Generated / Modified Artifacts

* src/image_workbench/adapters/image_processing/__init__.py
* src/image_workbench/adapters/image_processing/pillow_processor.py
* src/image_workbench/adapters/image_processing/opencv_processor.py
* src/image_workbench/adapters/image_processing/mappers.py
* src/image_workbench/adapters/image_processing/exceptions.py
* tests/adapters/image_processing/test_baseline_operations.py
* tests/adapters/image_processing/test_processing_failures.py
* tests/fixtures/images/
* tests/fixtures/golden/
* workflow/plans/05_local_image_processing_adapters_plan.md
* workflow/logs/phase-05-implementation-log.md

## Testing Expectations

* Golden image tests for deterministic baseline operations.
* Adapter tests for unsupported format, unreadable image, invalid operation mapping, invalid parameter mapping, and processing failure translation.
* Static-analysis and architecture-fitness checks from earlier phases.

## Acceptance Criteria

* Baseline operations produce deterministic results for fixed fixtures within documented tolerances.
* Application and domain packages remain free of Pillow and OpenCV imports.
* Adapter exceptions preserve safe context and original causes where relevant.
* Image-processing adapters are replaceable behind application ports.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if implementation chooses a single canonical image library, changes adapter strategy, or defines long-term golden-image compatibility policy.
* Decision log: Required for chosen golden-image tolerance and fixture maintenance convention.

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

