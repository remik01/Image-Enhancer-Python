# Desktop Workbench Ui

## Goal

Implement the accepted desktop workbench shell that collects user intent, renders application state, and keeps long-running work off the UI thread.

## Tickets

* IEP-013

## Features to implement

* Desktop shell using the UI technology accepted by ADR.
* Views or components for image loading, pipeline steps, operation parameters, AI proposals, export settings, job progress, failures, and undo/redo state.
* Presentation mapping from application results to UI state.
* UI tests for command creation, validation rendering, progress rendering, cancellation state, and failure rendering where practical.

## Constraints

* Do not duplicate domain validation in UI code.
* Do not call infrastructure adapters directly when application services exist.
* Do not block the UI thread with file, network, or image-processing work.
* Do not implement new backend features to satisfy UI shortcuts.

## Scope

* UI adapter code and presentation tests.
* Bootstrap wiring needed to start the selected desktop shell locally.
* README startup instructions for the desktop workbench.

## Out of Scope

* New image-processing operations.
* New REST API contracts.
* New persistence format changes.
* Production installers unless accepted by ADR.

## Architecture / Boundary Notes

The UI is an adapter. It should submit application commands and render application results. UI toolkit types must not enter domain or application code.

## Generated / Modified Artifacts

* src/image_workbench/ui/__init__.py
* src/image_workbench/ui/app.py
* src/image_workbench/ui/view_models.py
* src/image_workbench/ui/presenters.py
* src/image_workbench/bootstrap/desktop_runtime.py
* tests/ui/test_view_models.py
* tests/ui/test_presenters.py
* tests/ui/test_async_state_rendering.py
* README.md
* docs/architecture/desktop-ui.md
* workflow/plans/13_desktop_workbench_ui_plan.md
* workflow/logs/phase-13-implementation-log.md

## Testing Expectations

* Presentation tests for command creation, validation rendering, AI proposal display, progress rendering, cancellation state, and failure rendering.
* Manual smoke check for local desktop startup when automation is not practical.
* Architecture tests verify UI toolkit imports do not enter domain/application.

## Acceptance Criteria

* Users can load image references, inspect/edit pipeline steps, accept AI proposals, start jobs, observe progress, cancel work, see failures, and configure exports through application commands.
* UI thread is not used for long-running processing.
* UI behavior remains replaceable because core semantics live outside UI code.
* README.md documents the local desktop startup command and known UI limitations.

## ADR / Decision-Log Follow-Up

* ADR: Required if implementation changes accepted UI technology, packaging, local runtime, or API-bridge strategy.
* Decision log: Required for manual smoke-test convention and UI test boundaries.

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

