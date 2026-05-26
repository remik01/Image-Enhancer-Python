# Architecture Decision Baseline

## Goal

Establish the durable architecture decisions that must be accepted before implementation fixes long-lived direction in code.

## Tickets

* IEP-001

## Features to implement

* Create ADR candidates or accepted ADRs for layered package structure, dependency direction, UI strategy, REST exposure, project persistence, plugin model, AI integration, async execution, image adapter strategy, runtime configuration, and architecture fitness gates.
* Create an initial decision-log entry for accepted planning assumptions that are not ADR-sized.
* Create a concise architecture overview that future phase implementers can read before touching code.

## Constraints

* Do not implement product source code in this phase.
* Do not choose both PySide6/Qt and Tauri as active UI baselines.
* Do not mark unresolved decisions as accepted without explicit rationale.
* Do not introduce dependencies or package configuration beyond documentation artifacts.

## Scope

* Governance records needed before code implementation.
* ADRs or ADR candidates for the unresolved architecture choices identified by the overview.
* A decision-log baseline for local conventions and phase sequencing assumptions.

## Out of Scope

* Python package implementation.
* Static-analysis tooling setup.
* Domain, adapter, API, UI, plugin, or persistence code.
* Production deployment decisions.

## Architecture / Boundary Notes

The phase defines architecture intent only. Later phases must implement the accepted direction without putting persistence, HTTP, UI toolkit, OpenAI, Pillow, OpenCV, or plugin implementation concerns into domain code.

## Generated / Modified Artifacts

* docs/adr/0001-layered-architecture-and-boundaries.md
* docs/adr/0002-ui-runtime-and-api-strategy.md
* docs/adr/0003-project-persistence-and-plugin-contracts.md
* docs/adr/0004-ai-integration-and-async-execution.md
* docs/architecture/architecture-overview.md
* workflow/CLI.decision-log.md
* workflow/plans/01_architecture_decision_baseline_plan.md
* workflow/logs/phase-01-implementation-log.md

## Testing Expectations

* Documentation review against `AGENTS.md`, the overview, and `.github/instructions/adr.instructions.md`.
* Verify every unresolved overview architecture choice is either accepted, explicitly deferred, or identified as a blocker.
* No runtime tests are expected because this phase owns governance artifacts only.

## Acceptance Criteria

* Each ADR has status, context, decision or candidate decision, consequences, alternatives, risks, and follow-up.
* The decision log records phase sequencing assumptions and non-ADR conventions.
* docs/architecture/architecture-overview.md names the accepted layer responsibilities and forbidden dependency directions.
* No product source code or dependency configuration is added.

## ADR / Decision-Log Follow-Up

* ADR: Required for the architecture choices listed in this phase.
* Decision log: Required for accepted assumptions and local conventions that are not ADR-sized.

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
* Add or update tests with the implementation when behavior is introduced.
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

