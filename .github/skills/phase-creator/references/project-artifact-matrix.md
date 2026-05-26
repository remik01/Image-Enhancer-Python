# Project Artifact Matrix

Use this matrix during the prerequisite artifact audit. Classify each relevant artifact as existing, to-create, to-modify, or explicitly out of scope before writing phase files.

## Python Package And Modules

Expected artifacts:

* Root `pyproject.toml` when package metadata or shared tool configuration is needed.
* Package directories under `src/` or the repository's established package layout.
* Test directories such as `tests/` or package-adjacent test modules.
* Module directories for domain, application, adapters, security, bootstrap, UI clients, or architecture tests.

Verification:

* `python -m pytest`
* Focused `python -m pytest <test-path>` commands when a phase is scoped.
* Import/package checks through the project command, `python -m pip check`, or packaging build commands when packaging is in scope.

Do not assume a package or module exists just because the overview names a layer.

## Static Analysis, Maintenance, And Architecture Fitness

Expected artifacts:

* `pyproject.toml` tool configuration for ruff, pytest, mypy, or other accepted tools.
* `.github/workflows/ci.yml` jobs for tests, static analysis, formatting, type checking, dependency hygiene, and architecture checks when CI is in scope.
* `.github/workflows/codeql.yml` or equivalent CodeQL workflow when GitHub security scanning is in scope.
* `.github/codeql/codeql-config.yml` when CodeQL uses repository-local advanced setup configuration.
* Type-checker configuration when not stored in `pyproject.toml`.
* Architecture-fitness tests or scripts when cross-package boundary checks are required.
* Narrow ignore or baseline files only when a reviewed non-actionable finding requires them.

Verification:

* `python -m pytest`
* `python -m ruff check .`
* `python -m ruff format --check .`
* `python -m mypy .` or `python -m pyright` when type checking is in scope.
* Dependency or security scanning commands when configured.
* GitHub Actions CodeQL workflow result when code scanning is introduced; local validation is limited to workflow/config review and available local commands.
* SARIF artifact publication when repository code scanning is not enabled; artifact paths must stay inside the workspace and must not use `..`.

Do not reference a config path in Python tooling or CI without assigning a phase to create or modify it.

## Runtime And Backend Bootstrap

Expected artifacts:

* Bootstrap or application factory modules.
* Runtime settings and validation modules.
* Local secrets placeholder documentation; never commit real secrets.
* Health/readiness endpoint or CLI command configuration where runtime validation needs it.
* Runtime-boundary metrics or lifecycle hooks when custom project metrics are introduced.
* README startup and troubleshooting commands.

Verification:

* Tests for runtime configuration.
* Tests that assert project metrics, health checks, or startup behavior through the selected runtime boundary.
* Local startup command documented with safe prerequisites.

Do not assume repository-specific local secrets files exist; document required external files under `%USERPROFILE%\<project-local-config-dir>\` with placeholder values only.
Do not introduce Prometheus clients, Grafana dashboards, scrape configuration, or alerting as part of a lightweight observability phase.

## Persistence

Expected artifacts:

* Persistence adapter source and tests.
* Migration directory and migration files when schema changes are in scope.
* Local integration-test profile or documented skip conditions.
* Database setup and migration verification documentation.

Verification:

* Persistence unit tests.
* Local database integration command only when prerequisites are available.

Do not commit credentials, production connection strings, or local database state.

## API And Security

Expected artifacts:

* API adapter DTOs, route handlers/controllers, mappers, exception handlers, and tests.
* OpenAPI configuration or generated contract test artifact when required.
* Security configuration, authentication endpoints, auth DTOs, redaction helpers, and tests.
* Security test fixtures that contain placeholders only.

Verification:

* API contract/handler tests.
* Security configuration and authorization tests.

Do not pass domain/application models directly as wire contracts unless an ADR explicitly accepts that boundary.

## Frontend And Desktop Clients

Expected artifacts:

* Client workspace/module directories.
* Client configuration files for API base URL, authentication, and local startup.
* UI tests and build/test scripts.
* Generated API client artifacts only when explicitly accepted.
* README startup commands for each implemented client.

Verification:

* Client build and test commands.
* Manual smoke checks where automation is not yet practical.

Do not duplicate backend domain rules in clients; clients submit intent and render outcomes.

## Operational Validation

Expected artifacts:

* Repository-local helper script such as `scripts/run-operational-validation.ps1`.
* Fixtures or sample payloads when needed.
* README or operations documentation explaining safe local execution.
* Output redaction checks for tokens, passwords, signing secrets, and database credentials.

Verification:

* Helper script safe failure paths.
* Runtime smoke scenarios through the real boundary where practical.

Do not add unbounded load tests, destructive operations, or production-like targets without explicit architecture review.

## Closure And Handover

Expected artifacts:

* `README.md` updates.
* `USER_MANUAL.md`.
* Technical documentation generated by the `technical-documentation` skill or a recorded skip rationale.
* Known limitations and future-work documentation.
* Optional setup/check helper scripts with safe/check-only behavior.

Verification:

* Documentation review for stale commands and secret leakage.
* Setup helper safe failure tests when helpers are added.

Do not present local-ready behavior as production-ready deployment capability.
