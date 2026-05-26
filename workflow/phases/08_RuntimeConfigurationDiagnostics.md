# Runtime Configuration Diagnostics

## Goal

Implement bootstrap-time runtime settings, local secrets documentation, safe diagnostics, and lightweight health/status behavior needed by adapters and runtime surfaces.

## Tickets

* IEP-008

## Features to implement

* Typed runtime settings for AI credentials, model selection, timeouts, limits, plugin paths, API host/port, and local file limits.
* Startup validation with clear safe errors for missing or invalid configuration.
* Safe diagnostic logging conventions for runtime boundaries.
* Lightweight health or status checks for local runtime readiness without external observability systems.
* Placeholder-only local secrets documentation.

## Constraints

* Do not commit real secrets, credentials, connection strings, or local machine-specific config.
* Do not introduce Prometheus, Grafana, tracing, alerting, cloud monitoring, or external dashboards.
* Do not put business logic in bootstrap.
* Do not implement API routes or UI behavior in this phase.

## Scope

* Bootstrap configuration modules.
* Redaction helpers and diagnostic policy.
* Tests for missing settings, invalid settings, redaction, and health/status behavior.
* Documentation of local runtime configuration.

## Out of Scope

* OpenAI adapter calls.
* Plugin loading behavior.
* REST route implementation.
* Desktop UI startup.
* Production deployment.

## Architecture / Boundary Notes

Bootstrap wires dependencies and validates configuration at the edge. Domain and application code should receive typed settings or configured ports, not environment variables or raw secrets.

## Generated / Modified Artifacts

* src/image_workbench/bootstrap/__init__.py
* src/image_workbench/bootstrap/settings.py
* src/image_workbench/bootstrap/logging_config.py
* src/image_workbench/bootstrap/health.py
* src/image_workbench/bootstrap/redaction.py
* tests/bootstrap/test_settings_validation.py
* tests/bootstrap/test_diagnostics_redaction.py
* tests/bootstrap/test_health_status.py
* docs/architecture/runtime-configuration.md
* README.md
* workflow/CLI.decision-log.md
* workflow/plans/08_runtime_configuration_diagnostics_plan.md
* workflow/logs/phase-08-implementation-log.md

## Testing Expectations

* Tests for valid configuration, missing required settings, invalid timeout/limit values, secret redaction, and health/status output.
* Static-analysis commands from Phase 02.
* Manual documentation review to confirm placeholder values only.

## Acceptance Criteria

* Missing required runtime settings fail fast with clear safe messages.
* Logs and errors redact OpenAI credentials and avoid raw image payloads or sensitive metadata dumps.
* Health/status behavior reports local readiness without claiming production observability.
* README.md documents local secrets placeholders and startup assumptions honestly.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if implementation changes secret-management architecture, observability strategy, or deployment assumptions.
* Decision log: Required for accepted local configuration source and lightweight diagnostic convention.

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

