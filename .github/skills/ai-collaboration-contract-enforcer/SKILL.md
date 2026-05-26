---
name: ai-collaboration-contract-enforcer
description: Validate AI-assisted engineering work against repository governance contracts, including ADR obligations, persisted plans, rationale persistence, prompt-to-artifact traceability, reproducibility, review evidence, context integrity, and architecture consistency. Use before major AI-generated changes, PR review, planning, or governance audits.
---

# AI Collaboration Contract Enforcer

## Overview

Use this skill to make AI-assisted development reproducible, reviewable, and aligned with repository governance. It enforces collaboration contracts between humans, AI agents, IDE assistants, CI/CD systems, architecture governance, and documentation.

Primary source specification: `.github/skills/advanced_ai_skills_specification_pack.md`.

## Workflow

1. Identify the AI-assisted work under review:
   - prompt, plan, branch, diff, PR, phase, or generated artifact.
2. Read governing contracts:
   - `AGENTS.md`,
   - relevant `.github/instructions/*.instructions.md`,
   - ADRs,
   - decision logs,
   - workflow plans, phase logs, investigations, and phases,
   - static-analysis and CI/CD policies,
   - PR templates or exception registers when present.
3. Check obligations:
   - persisted plan required,
   - ADR evaluation required,
   - decision-log entry required,
   - tests or verification required,
   - rationale summary required,
   - review evidence required.
4. Validate prompt-to-artifact traceability where evidence exists.
5. Check AI context integrity:
   - stale instructions,
   - conflicting governance files,
   - duplicated policies,
   - outdated workflow assumptions.
6. Detect governance drift and recommend reconciliation.

## Contract Signals

Look for:
- architecture-impacting changes without ADR evaluation,
- generated plans not persisted when required,
- large AI-generated artifacts without rationale,
- assumptions not linked to authoritative docs,
- unverified claims of test success,
- contradictory instructions left unresolved,
- exceptions that became normal workflow,
- missing review evidence for high-risk generated changes.
- missing or stale phase-log evidence when phase work was performed through `implement-phase`.

## Output

Write a durable AI governance report to `workflow/investigations/YYYY-MM-DD-ai-governance-<topic>.md` by default. Use chat-only output only when the user explicitly asks not to persist the report or the finding is trivial and fully captured by an immediate review response.

The report must include:
- violated workflow contracts,
- missing rationale,
- undocumented assumptions,
- ADR obligations,
- architectural inconsistencies,
- reproducibility risks,
- traceability gaps,
- governance bypass indicators,
- unresolved exceptions,
- missing review evidence,
- corrective actions.

## Persistence Strategy

Write the AI governance report incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title and context.
2. Use the `edit` tool to append each subsequent report section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

## Guardrails

- Do not treat traceability as surveillance.
- Do not require heavy process for trivial work.
- Do not invent governance rules beyond repository artifacts.
- Preserve engineering reviewability over code-generation speed.
