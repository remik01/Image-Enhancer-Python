# Post Implementation Operational Validation

## Goal

Validate the implemented tool end to end through real runtime boundaries and record bounded local operational evidence.

## Tickets

* IEP-014

## Features to implement

* Repository-local operational validation helper for local API, desktop-adjacent service, or application-service boundaries available after implementation.
* Repeatable scenarios for simultaneous operations, large valid inputs, large invalid inputs, duplicate/conflicting submissions, cancellation, timeout, deterministic repeated runs, and safe diagnostics.
* Operational evidence output that is useful for failure analysis and safe to keep in the repository or workflow logs.

## Constraints

* Do not introduce product features or architecture remediation in this phase.
* Do not add unbounded load tests or production-like targets.
* Do not print secrets, credentials, or sensitive image payloads.
* Keep performance claims local and non-binding unless separately validated.

## Scope

* Operational validation script and fixtures.
* Documentation for safe local execution.
* Evidence capture and redaction checks.

## Out of Scope

* Fixing issues found by validation.
* Changing async, persistence, API, UI, or adapter architecture.
* Production deployment validation.
* External load-test services.

## Architecture / Boundary Notes

This phase observes implemented behavior. If validation exposes architecture changes, record them as ADR candidates, decision-log follow-up, or later remediation work rather than folding them into validation.

## Generated / Modified Artifacts

* scripts/run-operational-validation.ps1
* tests/operational/test_validation_script_contract.py
* tests/fixtures/operational/
* docs/operations/local-operational-validation.md
* README.md
* workflow/logs/phase-14-implementation-log.md
* workflow/investigations/phase-14-operational-validation-findings.md

## Testing Expectations

* `scripts/run-operational-validation.ps1` safe failure path tests or contract tests.
* Operational helper exercises the real implemented boundary where practical.
* Evidence confirms deterministic repeated results and safe diagnostics.
* Static-analysis commands from Phase 02 remain passing.

## Acceptance Criteria

* The helper validates simultaneous operations, large valid inputs, large invalid inputs, duplicates/conflicts, timeout/cancellation behavior, deterministic repeated runs, and diagnostic output.
* Local-machine limits and assumptions are documented.
* Any discovered defects are recorded as follow-up and not silently remediated inside this phase.
* README.md and docs/operations/local-operational-validation.md describe safe execution.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if validation shows a need for new runtime topology, queue policy, persistence changes, caching, rate limiting, or observability ownership.
* Decision log: Required for accepted local operational validation limits and known residual risks.

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

