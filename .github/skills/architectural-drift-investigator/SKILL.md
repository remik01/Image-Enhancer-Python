---
name: architectural-drift-investigator
description: Detect semantic architecture drift against declared architecture, ADRs, decision logs, module boundaries, dependency rules, naming conventions, package structure, and historical intent. Use before large refactors, during architecture reviews, or when code appears to compile while architecture meaning may have eroded.
---

# Architectural Drift Investigator

## Overview

Use this skill to investigate whether implementation reality has drifted from declared architecture and historical intent. Treat static-analysis findings as evidence, not as the whole answer.

Primary source specification: `.github/skills/advanced_ai_skills_specification_pack.md`.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable analysis model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning analysis model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

Do not treat model availability as evidence for or against architectural drift. Findings must remain based on repository artifacts, implementation evidence, tests, ADRs, decision logs, and documented architecture rules.

## Workflow

1. Read governance and intent sources:
   - `AGENTS.md`
   - relevant `.github/instructions/*.instructions.md`
   - `docs/adr/*.md`
   - `workflow/*.decision-log.md`
   - `workflow/plans/*.md`
   - `workflow/phases/*.md`
   - architecture tests, dependency rules, and module descriptors.

2. Inspect implementation evidence:
   - package and module boundaries,
   - Python package and dependency direction,
   - naming patterns,
   - duplicate concepts,
   - large or rapidly growing classes/packages,
   - utility modules or exceptions that became hidden frameworks,
   - recent Git history when available and relevant.

3. Compare declared intent against implementation behavior.

4. Classify each drift candidate:
   - confirmed drift,
   - likely drift,
   - weak signal,
   - intentional deviation already documented,
   - unclear, needs human review.

5. Recommend corrective action:
   - local refactor,
   - test or architecture-rule hardening,
   - ADR update,
   - decision-log entry,
   - investigation artifact,
   - no action with rationale.

## Drift Signals

Look for:
- adapter modules containing business rules,
- UI/client code duplicating authoritative domain validation,
- domain/application imports from frameworks, adapters, UI, HTTP, persistence, or image-processing libraries,
- duplicate names for the same business concept,
- generic maps replacing explicit contracts,
- temporary bypasses referenced by production modules,
- architecture tests weakened without rationale,
- packages whose names no longer match their responsibilities.

## Output

Write a durable drift report to `workflow/investigations/YYYY-MM-DD-architectural-drift-<topic>.md` by default. Use chat-only output only when the user explicitly asks not to persist the report or the finding is trivial and fully captured by an immediate code review response.

The report must include:
- detected drift,
- severity,
- violated principle or artifact,
- affected files/modules,
- evidence and confidence level,
- probable consequences,
- suggested correction,
- ADR or decision-log follow-up.

## Persistence Strategy

Write the drift report incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title and context.
2. Use the `edit` tool to append each subsequent report section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

## Guardrails

- Do not treat every smell as a violation.
- Do not recommend broad rewrites when a focused correction is enough.
- Do not invent architecture rules not supported by repository governance.
- Prefer uncomfortable correctness over confirming the current structure.
