---
name: institutional-memory-curator
description: Reconstruct durable engineering rationale from ADRs, decision logs, plans, investigations, commits, pull requests, documentation, architecture diagrams, incident reports, and implementation evidence. Use for onboarding, historical reasoning, contradiction detection, obsolete assumptions, and AI continuity across sessions.
---

# Institutional Memory Curator

## Overview

Use this skill to turn fragmented project history into durable engineering knowledge. Preserve why decisions were made, not only what exists now.

Primary source specification: `.github/skills/advanced_ai_skills_specification_pack.md`.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable analysis model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning analysis model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

Do not treat model availability as a source of project memory. Reconstructions must remain based on durable artifacts, repository evidence, explicit inference, and clearly stated uncertainty.

## Workflow

1. Identify the memory question, such as:
   - why a module exists,
   - why an approach was rejected,
   - why a constraint is still enforced,
   - which decisions shaped a workflow.
2. Read authoritative history:
   - `AGENTS.md`,
   - `workflow/docs/overview.spec.md`,
   - `docs/adr/*.md`,
   - `workflow/*.decision-log.md`,
   - `workflow/plans/*.md`,
   - `workflow/logs/*.md`,
   - `workflow/investigations/*.md`,
   - `workflow/phases/*.md`,
   - relevant code, tests, commits, and PRs when available.
3. Reconstruct the timeline of intent, decision, implementation, and follow-up.
4. Detect contradictions, obsolete assumptions, and rationale gaps.
5. Link current implementation back to durable artifacts.
6. Recommend documentation, ADR, decision-log, or investigation updates when memory is missing or stale.

## Memory Signals

Look for:
- ADRs contradicted by implementation,
- decision-log entries not reflected in code,
- old assumptions still enforced after context changed,
- repeated rejected approaches reappearing,
- undocumented critical modules,
- plans or phases whose rationale did not survive implementation,
- phase logs whose actions, failures, or lessons were not reflected in plans, ADRs, or documentation,
- onboarding docs that no longer match code.

## Output

Write a durable knowledge reconstruction to `workflow/investigations/YYYY-MM-DD-institutional-memory-<topic>.md` by default. Use chat-only output only when the user explicitly asks not to persist the reconstruction or the answer is narrow and fully supported by already-durable artifacts.

The reconstruction must include:
- question answered,
- evidence sources,
- timeline,
- current interpretation,
- contradictions or obsolete assumptions,
- knowledge-decay risks,
- recommended durable artifact updates,
- confidence level.

## Persistence Strategy

Write the knowledge reconstruction incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title and question answered.
2. Use the `edit` tool to append each subsequent reconstruction section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

## Guardrails

- Do not invent project history.
- Separate facts, inference, and uncertainty.
- Prefer repository evidence over memory from chat.
- Do not replace ADRs or decision logs with a narrative report when durable governance artifacts are needed.
