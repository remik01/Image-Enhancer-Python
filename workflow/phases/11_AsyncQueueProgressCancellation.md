# Async Queue Progress Cancellation

## Goal

Implement bounded asynchronous execution for long-running image and batch work with progress, cancellation, failure, and partial-result semantics.

## Tickets

* IEP-011

## Features to implement

* Application-owned queue contracts and job state models.
* Runtime adapter for local queued execution.
* Progress reporting, cancellation requests, failure reporting, and deterministic partial-result behavior.
* Tests for simultaneous jobs, cancellation, timeout, duplicate submissions, and failure states.

## Constraints

* Do not block UI or API callers during long-running work.
* Do not introduce unbounded concurrency.
* Do not swallow cancellation or broad failures.
* Do not add remote queues, messaging systems, or external worker infrastructure.

## Scope

* Application queue contracts.
* Local in-process execution adapter.
* Tests for queue lifecycle and edge cases.
* Documentation of local-machine limits.

## Out of Scope

* REST API job endpoints.
* Desktop UI progress widgets.
* Cloud workers, message brokers, or distributed execution.
* Performance optimization beyond bounded local behavior.

## Architecture / Boundary Notes

Application contracts should define observable job state without depending on a concrete concurrency library. Bootstrap owns lifecycle wiring and shutdown behavior.

## Generated / Modified Artifacts

* src/image_workbench/application/jobs.py
* src/image_workbench/application/queue_service.py
* src/image_workbench/adapters/queue/__init__.py
* src/image_workbench/adapters/queue/local_executor.py
* src/image_workbench/bootstrap/runtime.py
* docs/architecture/async-execution.md
* tests/application/test_queue_service.py
* tests/adapters/queue/test_local_executor.py
* tests/bootstrap/test_runtime_lifecycle.py
* workflow/plans/11_async_queue_progress_cancellation_plan.md
* workflow/logs/phase-11-implementation-log.md

## Testing Expectations

* Tests for simultaneous submissions, cancellation, timeout handling, duplicate/conflicting jobs, failure propagation, deterministic result state, and shutdown.
* Static-analysis and architecture checks from earlier phases.
* No external services or unstable timing assumptions in tests.

## Acceptance Criteria

* Long-running work can be queued and observed through job state.
* Cancellation and timeout behavior are documented and tested.
* Partial failures produce deterministic, safe diagnostics.
* Queue lifecycle is controlled by bootstrap and does not introduce hidden global mutable state.

## ADR / Decision-Log Follow-Up

* ADR: Required for accepted concurrency model, cancellation semantics, partial-failure policy, and queue lifecycle.
* Decision log: Required for local test timing limits and job-state naming convention.

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

