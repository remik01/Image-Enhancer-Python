# Phase File Contract

Use this structure for every generated phase:

```md
# <Phase Title>

## Goal

<Concise intended outcome.>

## Tickets

* EXAMPLE-123
* EXAMPLE-456

## Features to implement

<Concrete capabilities included in this phase.>

## Constraints

<Rules, boundaries, and technical restrictions.>

## Scope

<What belongs in this phase.>

## Out of Scope

<What must not be implemented in this phase.>

## Architecture / Boundary Notes

<Layering, dependency, DTO, persistence, UI, security, adapter, or runtime notes.>

## Generated / Modified Artifacts

<Bulleted files, directories, workflow jobs, scripts, configuration, documentation, generated clients, or `None identified.`>

## Testing Expectations

<Unit, integration, UI, contract, manual, static-analysis, or verification expectations.>

## Acceptance Criteria

<Observable and testable completion criteria.>

## ADR / Decision-Log Follow-Up

* ADR: Required / Not required / Discuss if implementation chooses X.
* Decision log: Required / Not required / Add entry for Y.

## Codex/Copilot Execution Notes

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
```

Acceptance criteria must be concrete enough to fail. Examples:

- `python -m pytest` succeeds.
- Domain package has no web framework, UI toolkit, HTTP, persistence, or image-processing library dependencies.
- API adapter tests cover unsupported format, invalid operation, payload too large, and processing failure mappings.

Avoid criteria such as "code is clean" or "UI works well".

The `Generated / Modified Artifacts` section must contain one or more concrete bullets, or exactly `None identified.`. Use `None identified.` only when the phase owns no files, directories, workflow jobs, scripts, configuration, or documentation artifacts beyond ordinary source/test changes.
