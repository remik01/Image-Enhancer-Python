# Workflow Phase Instructions

Workflow phases split large initiatives into reviewable, incrementally executable units. A phase should reduce ambiguity and preserve architecture boundaries.

## Directory

Store phase files under:

```text
workflow/phases/
```

Use stable, ordered names such as:

```text
01_domain-model.md
02_application-ports.md
03_adapter-import.md
```

## Phase Rules

- One primary architectural concern per phase.
- Each phase must be independently reviewable.
- Each phase must leave the repository in a coherent state.
- Do not mix unrelated cleanup with feature work.
- Do not bypass domain/application/adapter/UI/CLI/bootstrap boundaries.
- Include verification for each phase.
- Identify ADR or decision-log needs.

## Required Phase Content

Each phase should include:

- goal,
- non-goals,
- dependencies,
- affected layers,
- implementation tasks,
- tests and verification,
- risks and rollback/rework notes,
- done criteria.

## Good Phase Boundaries

Prefer boundaries such as:

- domain model and invariants,
- application ports/use cases,
- adapter implementation,
- UI/CLI integration,
- bootstrap wiring,
- test/verification hardening,
- documentation and decision records.

Avoid phases such as "finish everything", "cleanup", or "integration" without precise scope.

## Agent Rules

- Create phases only for work large enough to need durable sequencing.
- Keep phase files concise and implementation-ready.
- Do not invent domain rules to fill a phase.
- Update phase status only when the repository state supports it.

## Phase Commit Message Convention

When committing work that implements a workflow phase, or fixes review findings directly related to a workflow phase, use this commit message format:

```text
YYYY.MM.DD <login-name> <ticket-1> <ticket-2> ... <phase-title>: <commit-description>
```

Rules:

- `YYYY.MM.DD` is the current local date at commit time.
- `<login-name>` is the current OS login name at commit time. In PowerShell/Windows contexts, read it from `$env:USERNAME`; in Python/runtime contexts, read it from `getpass.getuser()`.
- Tickets come from the phase file `## Tickets` section, in listed order, separated by spaces.
- `<phase-title>` is the phase file title, using the H1 text without the leading `#`.
- `<commit-description>` is a concise summary of the work done in this commit, ideally one line. For example, "Implement domain model and invariants" or "Add application ports and use cases".
- If a phase has no tickets, stop and ask for the phase file to be corrected before committing phase work.
- For review-remediation commits, use the tickets and title from the phase that the review finding belongs to.

## Checklist

- Can another engineer execute the phase without major decisions?
- Does the phase preserve boundaries?
- Are tests explicit?
- Are risks and dependencies named?
- Is completion objectively checkable?
