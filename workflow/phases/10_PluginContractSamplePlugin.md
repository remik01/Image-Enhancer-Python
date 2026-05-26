# Plugin Contract Sample Plugin

## Goal

Implement a controlled plugin contract and a sample plugin without allowing plugin implementation details to leak into domain models.

## Tickets

* IEP-010

## Features to implement

* Plugin registration contract for operation metadata, parameters, validation, and execution binding through application ports.
* Local plugin discovery using explicitly configured plugin paths.
* Version compatibility checks and duplicate operation handling.
* Sample plugin that contributes a deterministic enhancement operation.
* Tests for plugin discovery, validation, conflicts, failures, and boundary isolation.

## Constraints

* Do not load plugins from unvalidated paths.
* Do not execute arbitrary plugin behavior without a documented trust model.
* Do not import plugin implementation modules from domain code.
* Do not add remote plugin registries or package marketplaces.

## Scope

* Application plugin contracts.
* Local adapter for plugin discovery/loading.
* Sample plugin under the repository plugin directory.
* Plugin documentation and tests.

## Out of Scope

* Third-party plugin distribution.
* Plugin sandboxing beyond the accepted local trust model.
* AI-generated plugin creation.
* UI plugin manager.

## Architecture / Boundary Notes

Plugins are extension adapters. The stable contract should be application-facing, while domain code remains concerned only with operation identity, parameter validation, and pipeline invariants.

## Generated / Modified Artifacts

* src/image_workbench/application/plugins.py
* src/image_workbench/adapters/plugins/__init__.py
* src/image_workbench/adapters/plugins/loader.py
* src/image_workbench/adapters/plugins/manifest.py
* plugins/vintage_filter/__init__.py
* plugins/vintage_filter/plugin.py
* docs/architecture/plugin-contract.md
* tests/application/test_plugin_contract.py
* tests/adapters/plugins/test_plugin_loader.py
* tests/plugins/test_vintage_filter_plugin.py
* workflow/plans/10_plugin_contract_sample_plugin_plan.md
* workflow/logs/phase-10-implementation-log.md

## Testing Expectations

* Tests for successful plugin registration, duplicate operation identifiers, incompatible versions, invalid manifests, load failures, and execution through application contracts.
* Architecture tests verify domain does not import plugin implementations.
* Security-focused tests for plugin path normalization and rejected ambiguous paths.

## Acceptance Criteria

* A sample plugin registers and executes through the accepted application-facing contract.
* Invalid or conflicting plugins fail with safe diagnostics.
* Plugin implementation details do not cross into domain/application contracts except through accepted abstractions.
* docs/architecture/plugin-contract.md documents trust assumptions and compatibility rules.

## ADR / Decision-Log Follow-Up

* ADR: Required for accepted plugin discovery, trust model, compatibility policy, and extension contract.
* Decision log: Required for sample plugin naming and local plugin fixture convention.

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

