---
name: phase-creator
description: Create ordered implementation phase files from workflow/docs/overview.spec.md and review phase coverage against the overview, including final closure requirements for whole-project implementation coverage. Use when Codex / Copilot needs to convert a project overview into reviewable workflow phases under workflow/phases, validate per-phase and whole-plan consistency, preserve AGENTS.md governance, architecture boundaries, ADR follow-up, verification expectations, post-implementation operational validation, and final project closure/handover.
---

# Phase Creator

## Purpose

Create deterministic implementation phase files from the canonical overview:

```text
workflow/docs/overview.spec.md
```

Write phase files under:

```text
workflow/phases/
```

This skill plans implementation units only. It does not implement source code.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable planning model exposed by the current environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning planning model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

## Required Reading

Read:

- `AGENTS.md`
- `.github/instructions/phases.instructions.md`
- `.github/instructions/planningPersistence.instructions.md`
- `.github/instructions/adr.instructions.md`
- `workflow/docs/overview.spec.md`

When present, also inspect:

- `docs/adr/*.md`
- `workflow/*.decision-log.md`
- `workflow/plans/*.md`
- `workflow/investigations/*.md`
- existing `workflow/phases/*.md`

Use these artifacts as constraints. Do not invent missing decisions.

## Prerequisite Artifact Audit

Before designing phases, audit expected project artifacts against the overview, ADRs, decision log, existing phases, and repository contents.

Classify each expected artifact as:

- existing,
- to-create,
- to-modify,
- explicitly out of scope.

Use the matrix in:

```text
.github/skills/phase-creator/references/project-artifact-matrix.md
```

Do not assume referenced configuration, workflow, module, script, client workspace, documentation, or secrets-placeholder files already exist. If a phase mentions an artifact path, the phase must own it in `Generated / Modified Artifacts` or explicitly explain why it is out of scope.

## Overview Coverage And Consistency Review

After generating or modifying phase files, perform two review passes before validation is considered complete.

### Per-Phase Review

For each phase, verify:

- the phase has one coherent primary concern,
- all scope items are backed by concrete artifacts or tests,
- all referenced artifacts are owned in `Generated / Modified Artifacts`,
- acceptance criteria can fail objectively,
- out-of-scope items do not leak into implementation scope,
- architecture boundaries are preserved,
- ADR and decision-log follow-up is explicit,
- prerequisites from earlier phases are named rather than assumed.

### Whole-Plan Review

Create or update:

```text
workflow/phases/_overview-coverage-review.md
```

The review must include a traceability matrix with exactly these columns:

```md
| Overview Item ID | Overview Source / Summary | Phase(s) Covering It | Acceptance / Test Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- |
```

Allowed statuses:

- `Covered`
- `Partially covered`
- `Deferred`
- `Explicitly out of scope`
- `Needs clarification`
- `Missing`

The whole-plan review must check:

- every meaningful overview workflow, actor, domain concept, invariant, integration, UI/API expectation, security concern, persistence/runtime need, reporting/search need, and explicit exclusion is represented,
- no phase owns conflicting behavior,
- no overview requirement is implemented only implicitly,
- ordering respects dependencies,
- operational validation and handover phases cover the completed system,
- static-analysis and architecture-fitness gates appear before feature work depends on them.

If any item is `Missing`, `Partially covered`, or `Needs clarification`, report it in the final response and either revise phases or stop for user decision. `Missing` must fail helper-script validation unless explicitly allowed by the person requesting the review.

## Overview Resolution

1. If `workflow/docs/overview.spec.md` exists, use it.
2. If it does not exist and legacy `docs/overview.spec.md` exists, ask before copying or moving it to `workflow/docs/overview.spec.md`.
3. If neither canonical nor legacy overview exists, search for files named `overview.spec.md`.
4. If exactly one non-canonical overview exists, ask before copying it to `workflow/docs/overview.spec.md`.
5. If multiple non-canonical overviews exist, ask which one is authoritative.
6. If no overview exists, recommend `overview-creator` and stop.

Do not guess the authoritative overview.

## Phase Design Rules

- Keep each phase independently reviewable.
- Assign one primary architectural concern per phase.
- Put domain and application rules before adapters and clients when those layers depend on them.
- For Python projects, include pytest, ruff lint/format checks, mypy or pyright where type checking is in scope, dependency hygiene, optional security scanning, architecture-fitness checks, and CodeQL code scanning in the earliest applicable build-governance, CI-baseline, or static-analysis phase. If such a phase already exists, make all static-analysis, deterministic-maintenance, code-scanning, and architecture-fitness gates part of that phase instead of creating a duplicate. If no such phase exists, add a focused static-analysis, code-scanning, maintenance, and architecture-fitness gate phase before feature implementation depends on CI quality signals.
- Put server/API contracts before frontend or desktop client integration.
- Keep persistence, HTTP, UI toolkit, image-processing library, and storage details outside domain/application ownership.
- Do not introduce Docker, cloud deployment, messaging, AI services, storage, authentication, or new dependencies unless the overview, ADRs, decision log, or user explicitly requires them.
- When a phase introduces observability without an external metrics backend, prefer lightweight runtime-boundary metrics or health checks through existing project tooling, keep instrumentation out of domain types, and do not introduce Prometheus, Grafana, tracing, alerting, or dashboard ownership unless explicitly accepted.
- Make acceptance criteria observable and testable.
- Make every phase state generated or modified files, directories, workflow jobs, scripts, or configuration in `Generated / Modified Artifacts`. Use `None identified.` only when the phase truly owns no artifacts beyond source/test changes.
- Require verification commands to fail meaningfully when required config files, scripts, workflows, or local placeholders are absent. Do not rely on local IDE state, untracked files, or silently pre-existing repository-local configuration.
- Evaluate ADR and decision-log follow-up in every phase.
- End implementation sequences with a post-implementation operational validation phase unless the overview, ADRs, decision log, or user explicitly excludes runtime validation.
- End the overall phase sequence with a project closure and handover phase unless the overview, ADRs, decision log, or user explicitly excludes handover documentation.

## Static Analysis Gate Phase Content

When adding static analysis to a Python phase, require:

- `pyproject.toml` tool configuration for ruff linting and formatting where repository configuration is needed,
- mypy or pyright configuration when type checking is accepted for the project,
- dependency hygiene through `python -m pip check`, pip-audit, uv, poetry, or the repository's selected tool when configured,
- CodeQL advanced setup using `github/codeql-action/init@v4` and `github/codeql-action/analyze@v4`,
- repository-local CodeQL configuration under `.github/codeql/codeql-config.yml` unless the phase explicitly chooses default setup and records why no config file is owned,
- simple import-boundary or architecture-fitness tests for documented dependency direction, forbidden core-layer framework imports, adapter separation, and package cycles where meaningful,
- narrow suppressions or per-file ignores only when needed for non-actionable findings,
- `.github/workflows/ci.yml` static-analysis jobs or equivalent workflow entries for each local Python gate,
- `.github/workflows/codeql.yml` or an equivalent CodeQL workflow,
- if repository code scanning is enabled, CodeQL upload permissions including `actions: read`, `contents: read`, and `security-events: write`,
- if repository code scanning is not enabled, CodeQL analysis with SARIF upload and database upload disabled, SARIF written to a workspace-local directory, and SARIF published with `actions/upload-artifact` using a path that does not contain `..`,
- the verification command `python -m pytest`,
- the verification command `python -m ruff check .`,
- the verification command `python -m ruff format --check .`,
- the configured type-checking command, such as `python -m mypy .` or `python -m pyright`, when type checking is in scope,
- the configured dependency or security scanning command when that gate is in scope,
- CodeQL workflow validation through GitHub Actions, plus local YAML/path review when GitHub code scanning cannot be executed locally,
- explicit repository-setting follow-up when code scanning upload is deferred and SARIF artifact publication is used instead,
- remediation policy that fixes real findings and forbids broad suppressions, weakened thresholds, or subjective rule creep without review,
- formatter/linter policy that forbids mixing broad mechanical cleanup with feature implementation unless explicitly accepted,
- architecture-fitness policy that forbids weakening boundary checks without ADR, decision-log, or specification updates,
- CodeQL policy that forbids broad path exclusions, alert dismissal, custom query packs, or severity gate changes without documented triage and ADR or decision-log evaluation,
- documentation of all static-analysis commands in the phase acceptance criteria or testing expectations.

For deterministic snippets, read:

```text
.github/skills/phase-creator/references/static-analysis-templates.md
```

Use those snippets as templates, adapting only artifact versions, existing workflow structure, and repository path conventions.

## Lightweight Observability Phase Content

When adding runtime metrics or health checks without Prometheus or Grafana, require:

- metrics or health checks at bootstrap, adapter, CLI, or runtime boundaries,
- low-cardinality custom metric names that start with the project prefix, such as `<project-prefix>.runtime.startups`,
- tags limited to stable runtime facts and outcome/status values, never request ids, usernames, tokens, paths containing secrets, connection strings, or free-form messages,
- tests that assert metric registration, increments, or health-check behavior through the chosen runtime boundary,
- README or operations documentation that says metrics are local lightweight metrics and that Prometheus/Grafana are not part of the accepted baseline,
- decision-log follow-up for the local observability convention,
- ADR discussion only if the phase adds exporter registries, scrape endpoints, dashboards, alerting, tracing, or production observability ownership.

Do not add Prometheus clients, Grafana dashboards, Docker Compose, external scrape configuration, or cloud monitoring dependencies in a lightweight observability phase.

For deterministic snippets, read:

```text
.github/skills/phase-creator/references/observability-templates.md
```

Use those snippets when the overview or user asks for lightweight backend observability.

## Post-Implementation Operational Validation Phase

Create a final phase after the last feature-implementation phase with a stable name such as:

```text
NN_PostImplementationOperationalValidation.md
```

This phase validates actual tool behavior after the implemented workflow can run end to end. It must not introduce product features, silently change architecture, or implement remediation discovered by validation.

The phase must require a repeatable helper script that exercises the implemented tool through its real runtime boundary where practical, such as backend/API calls, CLI commands, or application service entry points. Prefer existing project tooling and repository-local scripts. Do not introduce external load-test dependencies unless the overview, ADRs, decision log, or user explicitly requires them.

The phase acceptance criteria must cover:

- simultaneous calls or operations against backend/application behavior,
- large valid inputs,
- large invalid or malformed inputs,
- duplicate, conflicting, or retried submissions,
- timeout, cancellation, and error behavior where applicable,
- deterministic result consistency across repeated runs,
- logging, diagnostics, or generated evidence useful for failure analysis,
- documented load assumptions and local-machine limits.

Keep performance claims bounded. Distinguish deterministic correctness checks from non-binding local performance observations.

If validation exposes a need for async processing, queues, rate limiting, caching, batching, persistence strategy changes, observability conventions, or runtime topology changes, record the item as an ADR candidate, decision-log follow-up, or later remediation phase. Do not fold those architectural changes into the operational validation phase.

## Project Closure And Handover Phase

Create the final phase after post-implementation operational validation with a stable name such as:

```text
NN_ProjectClosureAndHandover.md
```

This phase finalizes developer, operator, and non-technical user handover materials after implementation and runtime validation evidence exists. It must not introduce product features or present aspirational deployment capability as implemented reality.

The phase must require:

- running the `technical-documentation` skill or recording why it was skipped,
- generating or updating `workflow/phases/_overview-implementation-coverage-review.md` with `implement-phase/scripts/overview_implementation_coverage_review.py`,
- validating `workflow/phases/_overview-implementation-coverage-review.md` with `--validate --strict-open-items`,
- updating `README.md` with local prerequisites, build/test commands, runtime startup, verification commands, local secrets, database setup, troubleshooting, and known limitations,
- documenting required local secrets files with placeholder values only,
- documenting local database setup and verification for the implemented persistence strategy,
- creating `USER_MANUAL.md` for non-technical users,
- adding a bounded local setup/check helper script when it reduces setup risk,
- documenting deployment or handover status honestly, including what is local-ready versus production-ready,
- recording final known limitations and future work separately from completed behavior.

The closure phase must treat `workflow/phases/_overview-coverage-review.md` as planning coverage only. It must require implementation evidence for every overview item from completed phase implementation coverage reviews, workflow logs, workflow plans, decision logs, source/test files, operational validation evidence, and final handover documentation. The phase must not be accepted while overview implementation coverage rows remain `Missing`, `Partially covered`, or `Needs clarification`, unless the user explicitly accepts incomplete closure and the decision log records the open items.

The phase may recommend helper scripts such as `scripts/setup-local-database.ps1` or `scripts/check-local-runtime-prerequisites.ps1`, but these helpers must validate targets, support safe/check-only behavior where practical, avoid printing secrets, and refuse ambiguous production-like targets.

If closure work requires deployment architecture, packaging conventions, database provisioning policy, production support ownership, secret-management architecture, or new operational tooling dependencies, record the item as an ADR candidate, decision-log follow-up, or later implementation phase. Do not hide those decisions inside documentation cleanup.

## Standard Structure

Use the complete phase contract in:

```text
.github/skills/phase-creator/references/phase-file-contract.md
```

Do not omit required sections. If a section has no special content, write `None identified.` rather than leaving it blank.

## Codex / Copilot Execution Notes For Generated Phases

In each generated phase file, include advisory implementation-profile guidance in the `Codex / Copilot Execution Notes` section:

```text
Recommended implementation profile, if available:
- Model: gpt-5.3-codex
- Reasoning: extra high

If unavailable, use the strongest available coding model with high reasoning. Do not treat model availability as an acceptance criterion. Record the actual model/profile used when implementing the phase if the execution environment exposes that information.
```

Keep acceptance criteria model-independent. A phase is complete only when its artifacts, tests, architecture checks, documentation, and validation evidence satisfy the phase contract.

## Helper Script

After creating or modifying phase files, run the structural validator:

```powershell
python .github\skills\phase-creator\scripts\validate_phase_files.py --phase-dir workflow\phases
```

Then run the coverage validator:

```powershell
python .github\skills\phase-creator\scripts\validate_phase_coverage.py --coverage workflow\phases\_overview-coverage-review.md --phase-dir workflow\phases
```

When generating or updating the final project closure and handover phase, include these implementation-time commands in that phase:

```powershell
python .github\skills\implement-phase\scripts\overview_implementation_coverage_review.py
python .github\skills\implement-phase\scripts\overview_implementation_coverage_review.py --validate --strict-open-items
```

If `python` is unavailable, use the interpreter discovered with `Get-Command python,py,python3`.

## Workflow

1. Read required context and resolve the canonical overview.
2. Extract purpose, actors, workflows, domain concepts, integrations, storage/runtime needs, UI/API expectations, security concerns, reporting/search needs, and explicit exclusions.
3. Perform the prerequisite artifact audit using `project-artifact-matrix.md`.
4. Compare extracted scope with existing phases, plans, ADRs, and implementation state.
5. Determine a phase sequence that preserves architecture boundaries.
6. Place pytest, ruff lint/format checks, type checking where accepted, dependency hygiene, optional security scanning, architecture-fitness checks, and CodeQL code scanning in the earliest applicable build-governance, CI-baseline, or static-analysis phase for Python projects.
7. Add a final post-implementation operational validation phase unless runtime validation is explicitly excluded.
8. Add the final project closure and handover phase unless handover documentation is explicitly excluded; include the whole-project overview implementation coverage review commands in that phase.
9. Write one Markdown file per phase using stable names such as `NN_PhaseTitle.md`.
10. Perform the per-phase review and revise any weak or conflicting phase before the whole-plan review.
11. Write or update `workflow/phases/_overview-coverage-review.md` with the coverage matrix.
12. Validate generated files with both helper scripts.
13. Report generated files, ordering, artifact classifications, coverage status, assumptions, ADR candidates, verification expectations, and weak points.

## Regeneration Rules

- Do not overwrite existing phase files unless the user explicitly requests replacement.
- Preserve human edits when revising existing phases.
- For substantial regeneration, prefer `workflow/phases/_regeneration-notes.md` to record added, removed, renamed, or materially changed phases.


## Persistence Strategy

Write phase files incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the first section (title block and Context).
2. Use the `edit` tool to append each subsequent section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

This approach provides intermediate checkpoints, reduces content loss on failure, and keeps the file reviewable at every step.

## Failure Handling

- Missing overview: stop and recommend `overview-creator`.
- Conflicting overview, ADR, or governance guidance: stop or ask before generating phases.
- Existing phase ownership overlap: narrow the new phase or report the duplicate evidence.
- Validation failure: fix the generated phase files before reporting completion.

## Final Response

Use the repository serious-work format and include:

- generated or updated phase files,
- coverage review file and unresolved coverage statuses,
- assumptions,
- ADR candidates,
- validation command and result,
- weak points and unresolved inputs.
