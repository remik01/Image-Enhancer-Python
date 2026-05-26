# Project Closure And Handover

## Goal

Finalize developer, operator, and non-technical user handover materials after implementation and operational validation evidence exists.

## Tickets

* IEP-015

## Features to implement

* Run the technical-documentation skill or record why it was skipped.
* Generate and strictly validate whole-project implementation coverage.
* Update developer setup, runtime, verification, troubleshooting, secrets, and known-limits documentation.
* Create a non-technical user manual.
* Add a safe local prerequisite check helper if it reduces setup risk.

## Constraints

* Do not introduce product features.
* Do not claim production readiness unless deployment architecture and support ownership were actually implemented and validated.
* Do not include real secrets or local machine-specific paths.
* Do not close with missing, partially covered, or unclear implementation coverage unless the user explicitly accepts incomplete closure and the decision log records open items.

## Scope

* Final documentation, handover, setup checks, and implementation coverage review.
* Honest known limitations and future work.
* Verification that documented commands match implemented reality.

## Out of Scope

* Feature remediation discovered during closure.
* New deployment architecture.
* New database provisioning policy.
* New operational tooling dependencies.

## Architecture / Boundary Notes

Closure documentation must distinguish local-ready behavior from production-ready deployment. Any remaining architecture gap belongs in ADR, decision-log, or future work rather than being hidden in prose.

## Generated / Modified Artifacts

* README.md
* USER_MANUAL.md
* docs/technical/project-technical-context.md
* workflow/phases/_overview-implementation-coverage-review.md
* workflow/docs/known-limitations.md
* scripts/check-local-runtime-prerequisites.ps1
* workflow/CLI.decision-log.md
* workflow/plans/15_project_closure_and_handover_plan.md
* workflow/logs/phase-15-implementation-log.md

## Testing Expectations

* Run `python .github\skills\implement-phase\scripts\overview_implementation_coverage_review.py`.
* Run `python .github\skills\implement-phase\scripts\overview_implementation_coverage_review.py --validate --strict-open-items`.
* Review README.md, USER_MANUAL.md, and technical documentation for stale commands, false readiness claims, and secret leakage.
* Test setup helper safe failure behavior if the helper is added.

## Acceptance Criteria

* Whole-project implementation coverage validates with strict open-item checks.
* README.md documents local prerequisites, build/test commands, runtime startup, verification commands, local secrets placeholders, persistence setup, troubleshooting, and known limitations.
* USER_MANUAL.md explains implemented workflows for non-technical users.
* Documentation separates completed behavior from future scope and production-readiness gaps.
* Any accepted incomplete closure is recorded in workflow/CLI.decision-log.md with explicit open items.

## ADR / Decision-Log Follow-Up

* ADR: Discuss if closure requires new deployment architecture, packaging conventions, production support ownership, secret-management architecture, or operational tooling dependencies.
* Decision log: Required for final known limitations, accepted incomplete items, and handover status.

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

