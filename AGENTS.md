# AGENTS.md

# AI Engineering Constitution

This repository uses AI-assisted development with explicit architectural governance. AI is an assistant, not an authority. Non-trivial output must be validated against project specifications, ADRs, workflow artifacts, domain invariants, tests, and architectural boundaries.

## Primary Technology

- Python 3.12+
- `pyproject.toml` for project metadata and tool configuration where practical
- pytest for tests where a Python test framework is needed
- ruff plus mypy or pyright for linting, formatting, and type-checking where configured or introduced deliberately
- Frameworks such as FastAPI, Typer, Flask, Django, PySide, PyQt, or Tkinter only when the project explicitly needs them

## Instruction Priority

When instructions conflict, apply this order:

1. ADRs and explicit project specifications
2. Domain invariants and architectural boundaries
3. Security and static-analysis requirements
4. Tests and reproducibility
5. Layer-specific instructions
6. Local implementation conventions

Prefer correctness, maintainability, deterministic behavior, and reviewability over generation speed.

## Architecture Principles

Keep these concerns separated:

- domain
- application
- adapters
- UI
- CLI
- bootstrap/configuration

Do not leak HTTP, persistence, XML/JSON, Excel, UI toolkit, external DTO, or framework concerns into the domain layer.

Layer ownership:

- Domain protects invariants and expresses business meaning.
- Application orchestrates use cases and defines ports.
- Adapters implement ports and translate external systems.
- UI and CLI collect user intent and render application results.
- Bootstrap wires runtime dependencies and validates configuration.

## Work Scope

Read `.github/instructions/work-scope.instructions.md` before non-trivial work. Use it to decide when plans, investigations, decision logs, ADR checks, and verification are required.

For non-trivial work:

- persist implementation plans under `workflow/plans/` when the task spans multiple steps or has architectural risk,
- persist investigations under `workflow/investigations/` according to `.github/instructions/investigation.instructions.md`,
- append durable local decisions to `workflow/CLI.decision-log.md`,
- evaluate ADR necessity explicitly.

## Required Reading Strategy

Read only the instruction files relevant to the task, plus nearby code, tests, ADRs, specs, and workflow artifacts that affect the change.

### Always Consider

- `.github/instructions/work-scope.instructions.md`
- `.github/instructions/investigation.instructions.md` when investigation findings are requested or evidence-dependent
- `.github/instructions/review-checklist.instructions.md`
- relevant ADRs and workflow artifacts
- nearby code and tests

### Domain Logic

- `.github/instructions/domain.instructions.md`
- `.github/instructions/python.instructions.md`
- `.github/instructions/tests.instructions.md`
- `.github/instructions/module-boundaries.instructions.md`

### Application Layer

- `.github/instructions/application.instructions.md`
- `.github/instructions/python.instructions.md`
- `.github/instructions/tests.instructions.md`
- `.github/instructions/module-boundaries.instructions.md`

### Adapters / Infrastructure

- `.github/instructions/adapters.instructions.md`
- `.github/instructions/mapping.instructions.md`
- `.github/instructions/exceptions.instructions.md`
- `.github/instructions/logging.instructions.md`
- `.github/instructions/data-contracts.instructions.md`
- `.github/instructions/security.instructions.md`

### UI / Frontend

- `.github/instructions/ui.instructions.md`
- `.github/instructions/logging.instructions.md`
- `.github/instructions/security.instructions.md`

### CLI

- `.github/instructions/cli.instructions.md`
- `.github/instructions/exceptions.instructions.md`
- `.github/instructions/logging.instructions.md`

### Bootstrap / Configuration

- `.github/instructions/bootstrap.instructions.md`
- `.github/instructions/operational-readiness.instructions.md`
- `.github/instructions/security.instructions.md`

### Exceptions, Logging, Naming, Mapping

- `.github/instructions/exceptions.instructions.md`
- `.github/instructions/logging.instructions.md`
- `.github/instructions/naming.instructions.md`
- `.github/instructions/mapping.instructions.md`

### Static Analysis / Verification

- `.github/instructions/static-analysis.instructions.md`
- `.github/instructions/tests.instructions.md`
- `.github/instructions/architecture-fitness.instructions.md`

### Planning / Phases

- `.github/instructions/phases.instructions.md`
- `.github/instructions/planningPersistence.instructions.md`
- `.github/instructions/investigation.instructions.md`
- `.github/instructions/adr.instructions.md`

### Maturity Concerns

- Boundary or module changes: `.github/instructions/module-boundaries.instructions.md`
- Enforceable architecture checks: `.github/instructions/architecture-fitness.instructions.md`
- Security-sensitive work: `.github/instructions/security.instructions.md`
- APIs, DTOs, schemas, imports, or exports: `.github/instructions/data-contracts.instructions.md`
- Large data, batch work, parsing, reporting, or concurrency: `.github/instructions/performance.instructions.md`
- Runtime configuration, startup, deployment, observability, or integration reliability: `.github/instructions/operational-readiness.instructions.md`

## ADR Awareness

Evaluate ADR necessity when a change affects:

- module boundaries or dependency direction
- persistence strategy
- runtime assumptions
- integration architecture
- concurrency model
- observability strategy
- security architecture
- reusable conventions
- public contracts or data compatibility

Do not silently introduce architectural direction.

## Non-Negotiable Rules

Do not:

- bypass architectural boundaries,
- duplicate domain logic across layers,
- silently weaken typing,
- suppress static-analysis warnings casually,
- introduce hidden global state,
- silently swallow failures,
- replace explicit contracts with generic maps,
- invent undocumented architecture.

## Final Rule

The repository must remain understandable, reviewable, reproducible, and incrementally evolvable. Optimize for long-term maintainability over short-term generation convenience.
