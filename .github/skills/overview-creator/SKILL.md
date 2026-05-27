---
name: overview-creator
description: "[Python] Create workflow/docs/overview.spec.md from a short plain-text project description, a file containing the description, or a shared ChatGPT link containing the project brief, including functional/nonfunctional requirement tables when requirements are explicit or implied. Use when Codex / Copilot needs to analyze a project idea, brief, prompt, prior ChatGPT discussion, or early specification into a broad project overview that respects AGENTS.md, repository instructions, architecture boundaries, ADR expectations, and planning conventions before phase creation or implementation planning."
---

# Overview Creator

## Purpose

Create a broad project overview specification from a short project description.

The Skill reads one of:

```text
plain-text project description
```

a file path containing the project description, or a shared ChatGPT link containing the project brief, then writes the canonical overview:

```text
workflow/docs/overview.spec.md
```

This Skill does **not** implement source code, create phases, or make architectural decisions final. It converts early project intent into an analyzable overview that downstream planning skills, especially `phase-creator`, can consume.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable planning model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning planning model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

Do not add model or reasoning-level requirements to `workflow/docs/overview.spec.md` unless the user explicitly asks for them. The overview is a project specification, so its correctness must remain based on supported facts, explicit assumptions, architecture alignment, placeholders for unknowns, and governance follow-up rather than model availability.

## Required Context

Before analyzing the input, read:

- `AGENTS.md`
- `.github/instructions/work-scope.instructions.md`
- `.github/instructions/planningPersistence.instructions.md`
- `.github/instructions/adr.instructions.md`

Read additional instruction files only when relevant to the input:

- domain/application/module work: domain, application, module-boundaries, python, tests
- adapters, imports, exports, DTOs, APIs, or persistence: adapters, mapping, data-contracts, exceptions, logging, security, performance
- UI or frontend: ui, logging, security
- CLI: cli, exceptions, logging
- bootstrap/runtime/deployment/observability: bootstrap, operational-readiness, security
- static analysis or verification expectations: static-analysis, architecture-fitness, tests

When present, inspect these for constraints and project history:

```text
docs/adr/
docs/adrs/
workflow/*.decision-log.md
workflow/plans/
workflow/investigations/
workflow/phases/
```

Use existing artifacts as constraints. Do not invent missing decisions.

## Inputs

Accept one of:

- an inline plain-text project description,
- a path to a text or Markdown file containing the description,
- a shared ChatGPT link containing the project description or discussion.

If the input appears to be a file path and the file exists, read the description from the file. If the path does not exist, stop and report the missing input rather than guessing.

If the input is a ChatGPT share link:

- follow `.github/instructions/work-scope.instructions.md` for shared ChatGPT link access,
- try the normal browsing tool first,
- if it returns no readable content, try a local HTTP fetch,
- if local fetch cannot extract useful content, use browser automation when available,
- extract only the project-relevant description, requirements, constraints, and decisions needed for the overview,
- do not persist the raw shared-chat transcript unless explicitly requested and reviewed for sensitive content,
- cite the share link in `Source Description` without copying unnecessary transcript content.

If the input is too vague, still create `workflow/docs/overview.spec.md`, but preserve uncertainty with the placeholder:

```text
<TO BE FILLED !!!>
```

## Output File

Create or update:

```text
workflow/docs/overview.spec.md
```

Do not write the overview somewhere else unless the user explicitly requests a different path.

If a legacy `docs/overview.spec.md` exists and `workflow/docs/overview.spec.md` does not, inspect the legacy file and ask before moving or copying it into the canonical workflow location.

If `workflow/docs/overview.spec.md` already exists:

- do not overwrite silently;
- inspect it first;
- preserve useful human-authored details when regenerating;
- report assumptions and meaningful changes.

## Required Overview Structure

Use this structure exactly unless the user explicitly requests additional sections:

```md
# Project Overview Specification

## Source Description

<Summarize the provided description or cite the source file path or shared ChatGPT link.>

## Project Purpose

<What the project exists to accomplish.>

## Main Users Or Actors

<People, systems, administrators, operators, clients, or external actors.>

## Core Features

<Primary capabilities and workflows.>

## Functional/Nonfunctional Requirements

| ID | Type | Description | Rationale | Fit Criterion |
|---|---|---|---|---|
| FR-001 | Functional | <User-visible capability, system behavior, workflow, or contract.> | <Why this requirement matters.> | <Observable pass/fail condition.> |

## Technology Stack

<Languages, frameworks, build tools, UI technologies, storage, integration technologies, and test tools.>

## Architecture Or Module Expectations

<Expected boundaries between domain, application, adapters, UI, CLI, bootstrap, and shared modules.>

## Persistence / Runtime Assumptions

<Storage, file system, database, runtime packaging, deployment, configuration, local/cloud assumptions, concurrency, and operational assumptions.>

## UI / API Expectations

<Expected user interfaces, REST/CLI/desktop/API surfaces, contracts, and interaction style.>

## Assumptions

<Explicit assumptions inferred from the description and repository governance.>

## Weak Points / Uncertainty

<Missing information, ambiguous requirements, risks, or likely failure modes.>

## ADR / Decision-Log Considerations

<Whether ADR discussion, decision-log entries, or no durable governance artifact appears needed.>
```

For every required section, write concrete content only when it is supported by the input description, repository instructions, or existing project artifacts. If a section cannot be inferred, write exactly:

```text
<TO BE FILLED !!!>
```

If the input mentions requirements explicitly or implies requirements through actors, workflows, constraints, quality expectations, repository governance, or stakeholder wishes, include `Functional/Nonfunctional Requirements` as a Markdown table with exactly these columns:

```md
| ID | Type | Description | Rationale | Fit Criterion |
|---|---|---|---|---|
```

Use stable IDs:

- `FR-001`, `FR-002`, ... for functional requirements.
- `NFR-001`, `NFR-002`, ... for nonfunctional requirements.

Use `Functional` for capabilities, workflows, user-visible behaviors, system operations, and external contracts. Use `Nonfunctional` for quality attributes, constraints, performance, reliability, security, usability, maintainability, operability, architectural boundaries, and compatibility.

Fill obvious `Rationale` and `Fit Criterion` fields from the project context, repository governance, or common acceptance criteria. When either field is genuinely unclear, put exactly:

```text
<TO BE FILLED !!!>
```

Do not invent infrastructure-heavy, security-heavy, or workflow-heavy requirements unless the input or existing artifacts justify them. If the user explicitly asks for plausible stakeholder wishes, label them as inferred assumptions in the overview.

## Analysis Rules

### 1. Separate facts from inference

Treat the user's description and existing repository artifacts as facts. Treat technology choices, architecture structure, persistence model, UI shape, and runtime behavior as inferred only when the source supports them.

Do not present speculation as decided project scope.

### 2. Respect architecture boundaries

Align the overview with `AGENTS.md`:

- domain protects invariants and business meaning,
- application orchestrates use cases and defines ports,
- adapters implement ports and translate external systems,
- UI and CLI collect intent and render results,
- bootstrap wires runtime dependencies and validates configuration.

Do not suggest leaking persistence, HTTP, UI toolkit, external DTOs, JSON/XML/Excel, or framework details into the domain layer.

### 3. Prefer conservative defaults

When the description does not require infrastructure, do not invent it. Avoid adding Docker, cloud hosting, messaging, AI providers, full-text search, analytics platforms, external databases, or authentication mechanisms unless the input or existing project artifacts require them.

For this repository, Python 3.12+, `pyproject.toml`, pytest, ruff, and mypy or pyright are allowed defaults. Frameworks such as FastAPI, Typer, Flask, Django, PySide, PyQt, or Tkinter are optional and must be marked as assumptions unless the input explicitly requires them.

### 4. Preserve uncertainty

Use `<TO BE FILLED !!!>` for unknowns instead of filling gaps with attractive guesses. Include open questions under `Weak Points / Uncertainty` when the missing information would materially affect architecture, testing, persistence, security, or UX.

### 5. Extract requirements without overstating certainty

Treat direct requirement language such as "must", "shall", "needs to", "should", "users can", "support", "avoid", "limit", and "compatible with" as requirement candidates. Also extract implied requirements when they follow directly from stated users, workflows, architecture boundaries, runtime constraints, or non-negotiable repository instructions.

Keep requirement descriptions testable and implementation-neutral. Prefer fit criteria that can be checked through tests, contract review, static analysis, manual acceptance, or documented operational limits.

When stakeholder wishes are invented at the user's request, separate them from confirmed project facts by recording the assumption in `Assumptions`.

### 6. Evaluate governance impact

In `ADR / Decision-Log Considerations`, classify likely follow-up:

- `ADR: Not required` for early overview drafting with no final architecture decision.
- `ADR: Discuss before implementation` when the overview implies durable choices such as module boundaries, persistence strategy, public contracts, runtime packaging, security architecture, concurrency model, or new dependencies.
- `Decision log: Consider` for narrow durable conventions, accepted assumptions, phase sequencing, or local workflow choices.

Do not create an ADR from this Skill unless the user explicitly asks for one.

## Recommended Workflow

1. Read required context files.
2. Resolve the input as inline text, file content, or shared ChatGPT link content.
3. Inspect existing overview, ADRs, decision logs, plans, investigations, and phases when present.
4. Extract:
   - purpose,
   - actors,
   - workflows,
   - functional and nonfunctional requirements,
   - domain concepts,
   - integrations,
   - storage needs,
   - UI/API expectations,
   - security and operational concerns,
   - explicit exclusions.
5. Draft `workflow/docs/overview.spec.md` using the required structure.
6. Replace unsupported content with `<TO BE FILLED !!!>`.
7. Review the overview against `AGENTS.md` and relevant `.github/instructions`.
8. Validate the overview:
   ```powershell
   python .github\skills\overview-creator\scripts\validate_overview.py --overview workflow\docs\overview.spec.md
   ```
9. Report:
   - output file path,
   - assumptions,
   - sections containing placeholders,
   - requirement rows containing placeholders,
   - ADR or decision-log follow-up,
   - weak points.

## Persistence Strategy

Write the overview incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title and `Source Description` section.
2. Use the `edit` tool to append each subsequent required section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

This approach provides intermediate checkpoints, reduces content loss on failure, and keeps the overview reviewable at every step.

## Quality Bar

The overview must be:

- broad enough for phase planning,
- explicit about unknowns,
- aligned with repository governance,
- conservative about infrastructure,
- useful as input for `phase-creator`,
- readable by humans without needing chat history.

Avoid vague filler such as:

```text
Use best practices.
Add proper architecture.
Implement required features.
```

Prefer concrete wording such as:

```text
The domain layer should own image transformation concepts and validation rules. UI code should call application services rather than manipulate adapter DTOs directly.
```

## Final Response Format

After creating or updating `workflow/docs/overview.spec.md`, respond with:

```md
## Result

Created or updated `workflow/docs/overview.spec.md`.

## Assumptions

...

## Placeholders

Sections still containing `<TO BE FILLED !!!>`:
- ...

Requirement rows still containing `<TO BE FILLED !!!>`:
- ...

## ADR / Decision-Log Follow-Up

...

## Weak Points / Uncertainty

...
```
