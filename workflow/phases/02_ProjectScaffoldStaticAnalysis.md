# Project Scaffold Static Analysis

## Goal

Create the Python package scaffold and the earliest quality gates so later feature work depends on enforceable tooling rather than prose alone.

## Tickets

* IEP-002

## Features to implement

* Create the root Python package layout under `src/`.
* Configure pytest, Ruff linting, Ruff format checks, mypy type checking, dependency hygiene, and architecture-fitness tests.
* Add CI and CodeQL workflow definitions with repository-local CodeQL configuration.
* Replace or remove the PyCharm sample `main.py` only if the accepted package scaffold makes it obsolete.

## Constraints

* Keep the initial lint and type-checking rules small and reviewable.
* Do not add product features.
* Do not weaken static-analysis warnings or add broad suppressions.
* Do not add image-processing, AI, UI, API, or persistence dependencies unless the accepted ADRs require them in the scaffold.

## Scope

* Project metadata and package layout.
* Local and CI verification commands.
* Architecture-fitness tests for dependency direction and forbidden imports.
* Basic import/package smoke tests.

## Out of Scope

* Domain behavior.
* Image transformations.
* API endpoints.
* Desktop UI.
* OpenAI integration.
* Plugin loading.

## Architecture / Boundary Notes

Architecture checks should encode only documented boundaries from `AGENTS.md`, the overview, and accepted ADRs. Domain and application checks must forbid framework, UI, HTTP, persistence, OpenAI, Pillow, OpenCV, and adapter imports where those boundaries are not accepted.

## Generated / Modified Artifacts

* pyproject.toml
* src/image_workbench/__init__.py
* src/image_workbench/domain/__init__.py
* src/image_workbench/application/__init__.py
* src/image_workbench/adapters/__init__.py
* src/image_workbench/bootstrap/__init__.py
* tests/__init__.py
* tests/architecture/test_layer_boundaries.py
* tests/test_package_import.py
* .github/workflows/ci.yml
* .github/workflows/codeql.yml
* .github/codeql/codeql-config.yml
* README.md
* main.py
* workflow/CLI.decision-log.md
* workflow/plans/02_project_scaffold_static_analysis_plan.md
* workflow/logs/phase-02-implementation-log.md

## Testing Expectations

* `python -m pytest`
* `python -m ruff check .`
* `python -m ruff format --check .`
* `python -m mypy .`
* `python -m pip check`
* Local review of `.github/workflows/ci.yml`, `.github/workflows/codeql.yml`, and `.github/codeql/codeql-config.yml` when GitHub Actions cannot be executed locally.

## Acceptance Criteria

* The package imports successfully from `src/image_workbench`.
* Architecture tests fail on forbidden core-layer imports.
* Ruff lint, Ruff format, mypy, pytest, and dependency hygiene commands are documented and executable after dependencies are installed.
* CI references only configuration files created or owned by this phase.
* CodeQL uses explicit Python setup and records code-scanning upload assumptions or SARIF artifact fallback.

## ADR / Decision-Log Follow-Up

* ADR: Required if this phase changes accepted dependency direction, dependency strategy, or architecture-check policy.
* Decision log: Required for the selected type checker, baseline lint rule set, dependency hygiene command, and CodeQL upload/fallback convention.

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

