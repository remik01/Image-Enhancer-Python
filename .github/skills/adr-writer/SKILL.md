---
name: adr-writer
description: Repository-local workflow for deciding whether an architectural change needs an ADR or decision-log entry, and for drafting high-quality ADRs aligned with project governance.
---

# ADR Writer Skill

Use this skill when Codex / Copilot needs to evaluate, create, update, or review Architecture Decision Records or decision-log entries.

## Purpose

Support explicit architecture governance by:
- identifying ADR candidates,
- distinguishing ADRs from decision-log entries,
- drafting ADRs,
- updating existing ADRs,
- preserving architectural reasoning,
- preventing silent architectural drift.

## When to Use

Use this skill when a task affects or may affect:
- module boundaries,
- dependency direction,
- new dependencies,
- persistence strategy,
- integration strategy,
- external contracts,
- serialization formats,
- concurrency model,
- caching strategy,
- runtime/deployment assumptions,
- observability strategy,
- security posture,
- reusable architectural patterns,
- long-term maintainability tradeoffs.

Also use it when the user explicitly asks for:
- an ADR,
- architecture decision,
- decision-log entry,
- governance review,
- architectural impact assessment.

## Workflow

1. Inspect repository guidance:
   - `AGENTS.md`
   - relevant `.github/instructions/*.instructions.md`
   - existing ADRs under `docs/adr`, `docs/adrs`, or similar locations
   - decision logs, if present
   - relevant project specifications

2. Inspect the change or proposal:
   - touched modules/packages,
   - new dependencies,
   - changed contracts,
   - changed runtime behavior,
   - changed boundary ownership,
   - changed verification strategy.

3. Classify the decision:
   - ADR required
   - decision-log entry sufficient
   - no documentation needed
   - unclear, human decision required

4. If ADR is required, draft or update an ADR.

5. If decision-log entry is sufficient, draft a concise entry and append it to the bottom of `workflow/CLI.decision-log.md`.

6. State assumptions and unresolved questions explicitly.

7. Recommend follow-up verification:
   - tests,
   - static analysis,
   - architecture review,
   - migration tasks,
   - documentation updates.

Use the helper for mechanical ADR numbering and section checks:

```powershell
python .github\skills\adr-writer\scripts\adr_tools.py --adr-dir docs\adr --next
python .github\skills\adr-writer\scripts\adr_tools.py --adr-dir docs\adr --validate
```

## ADR Required Criteria

Recommend an ADR when the decision affects:
- module boundaries,
- dependency direction,
- technology/framework adoption,
- public application/domain contracts,
- external integration contracts,
- persistence model,
- transaction model,
- concurrency or scheduling model,
- runtime packaging,
- deployment assumptions,
- security boundaries,
- observability architecture,
- significant performance strategy,
- long-term architectural policy.

## Decision-Log Sufficient Criteria

Recommend a decision-log entry when the decision is:
- local,
- narrow,
- implementation-specific,
- reversible,
- limited to naming or package convention,
- a parser/mapping interpretation,
- a static-analysis suppression rationale,
- a temporary compromise,
- a small test strategy clarification.

## ADR Draft Structure

Use this structure unless the repository already has a stronger template:

```md
# ADR-XXXX: <Decision Title>

## Status

Proposed

## Context

<Problem, constraints, forces, current state, risks.>

## Decision

<Clear statement of the selected decision.>

## Alternatives Considered

### Option 1: <Name>

<Benefits, drawbacks, reason accepted/rejected.>

### Option 2: <Name>

<Benefits, drawbacks, reason accepted/rejected.>

## Consequences

### Positive

- ...

### Negative / Tradeoffs

- ...

### Operational Impact

- ...

### Testing and Verification Impact

- ...

## Follow-Up Work

- ...
```

## Persistence Strategy

When creating or updating an ADR file under `docs/adr/`, write the ADR incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple ADR sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title, status, and context.
2. Use the `edit` tool to append each subsequent ADR section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

Decision-log entries are intentionally concise and may be appended to the bottom of `workflow/CLI.decision-log.md` as one complete dated entry. Do not insert new decision-log entries at the top of the file or reorder historical entries while adding a new decision.

## Quality Rules

DO:
- explain why the decision exists,
- document tradeoffs honestly,
- mention alternatives,
- preserve uncertainty,
- connect decision to project constraints,
- identify verification implications.

DON'T:
- write decorative ADRs,
- hide risks,
- invent project history,
- decide major architecture silently,
- use ADRs to bypass code review,
- create ADRs for trivial code formatting choices.

## Output Format

When finished, provide:

1. Classification
2. Reasoning
3. Reusable Artifact
4. Follow-Up Work
5. Risks / Open Questions

## Non-Goals

Do not:
- implement large architectural changes,
- rewrite code unless explicitly asked,
- approve architecture without review,
- create bureaucracy for trivial choices.

## Final Rule

Important architecture should be documented while the reasoning is still available.
Future maintainers should be able to recover the decision without reconstructing chat history.
