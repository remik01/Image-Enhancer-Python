# Planning Persistence Instructions

Persist planning artifacts when reasoning needs to survive beyond the chat. The repository should explain important intent, evidence, alternatives, and remaining risk.

## Directories

Use:

```text
workflow/plans/
workflow/investigations/
workflow/phases/
workflow/logs/
workflow/CLI.decision-log.md
```

## Persist A Plan When

- the work spans multiple files or layers,
- the change has architectural risk,
- implementation order matters,
- the task will likely take multiple sessions,
- assumptions or tradeoffs need review,
- the user asks for a durable plan.

## Persist An Investigation When

Follow `.github/instructions/investigation.instructions.md` for investigation triggers, structure, and style.

## Use Phase Logs When

Use `workflow/logs/phase-<NN>-implementation-log.md` for concise implementation evidence during phase work:

- context read,
- assumptions,
- decisions and rationale,
- actions taken,
- verification commands and outcomes,
- failures and remediation,
- review findings addressed,
- lessons learned.

Do not persist raw chain-of-thought, chat transcripts, secrets, credentials, or long command output. Logs should help future review and continuation without replacing ADRs, decision logs, plans, tests, or review packs.

## Use The Decision Log When

- a decision is durable but not ADR-sized,
- a local convention is chosen,
- a tradeoff affects future implementation,
- an assumption is accepted with known risk.

Append new decision-log entries to the bottom of `workflow/CLI.decision-log.md`. Do not insert new entries at the top of the file or reorder historical entries while adding a new decision.

## Plan Content

Plans should include:

- status,
- context,
- goal,
- non-goals,
- assumptions,
- rationale,
- trade-offs and limitations,
- implementation approach,
- affected layers,
- tests and verification,
- risks,
- ADR/decision-log needs.

### Rationale Section

Every persisted implementation plan must include a `## Rationale` section before `## Implementation Approach`.

The rationale must explain why the agent chose the proposed implementation path, including:

- the project facts and constraints that drove the choice,
- the domain, architecture, testing, operational, and maintainability tradeoffs considered,
- realistic alternatives that were considered,
- why those alternatives were not chosen,
- what would need to change for a rejected alternative to become preferable.

Keep the rationale exhaustive enough for a future maintainer to understand the decision without reading the original chat. Do not use the rationale section to restate the implementation steps; use it to preserve the reasoning behind them.

### Trade-offs And Limitations Section

Every persisted implementation plan must include a `## Trade-offs & Limitations` section after `## Rationale` and before `## Implementation Approach`.

This section must describe:

- compromises accepted in the plan,
- additional limitations not already captured in the related phase file's `## Constraints` section,
- opportunity costs of the user's decisions and choices,
- opportunity costs of the agent's implementation decisions and choices.

Keep this section distinct from `## Rationale`: use `## Rationale` to explain why the plan chooses a path, and use `## Trade-offs & Limitations` to preserve what the chosen path gives up, defers, narrows, or makes harder.

## Persistence Strategy

Write plan files incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title, status, and context.
2. Use the `edit` tool to append each subsequent plan section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

This approach provides intermediate checkpoints, reduces content loss on failure, and keeps the plan reviewable at every step.

## Agent Rules

- Do not persist trivial plans.
- Do not let plans drift from implementation.
- Do not replace ADRs with plans when architecture changes are long-lived.
- Keep filenames stable and descriptive.
- Prefer concise durable records over long transcripts.
- Append decision-log entries only at the bottom of `workflow/CLI.decision-log.md`.
- Follow the Persistence Strategy section for file writing order and mechanism.

## Checklist

- Does this artifact help future maintainers?
- Is the decision or evidence durable?
- Are assumptions explicit?
- Is verification included?
- Is ADR escalation considered?
