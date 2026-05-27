---
name: socio-technical-risk-analyzer
description: "[Python] Analyze organizational and human coordination risks expressed through technical systems, including ownership concentration, low bus-factor areas, governance bypass, opaque workflows, documentation gaps, AI misuse patterns, and architectural authority concentration. Use before major changes, reviews, onboarding, or governance health checks."
---

# Socio-Technical Risk Analyzer

## Overview

Use this skill to identify systemic coordination risks hidden inside technical artifacts. The goal is resilience, not individual productivity scoring.

Primary source specification: `.github/skills/advanced_ai_skills_specification_pack.md`.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable analysis model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning analysis model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

Do not treat model availability as a risk signal or mitigation. Findings must remain non-punitive and evidence-based, grounded in repository artifacts, workflow evidence, governance expectations, and explicitly stated uncertainty.

## Workflow

1. Define the risk lens:
   - module ownership,
   - governance compliance,
   - AI-assisted work,
   - documentation and onboarding,
   - review participation,
   - critical workflow transparency.
2. Inspect available evidence:
   - Git history,
   - PRs and review discussions when available,
   - ADRs and decision logs,
   - plans, phases, and investigations,
   - CI/CD history,
   - documentation density,
   - module and dependency centrality.
3. Identify systemic risk signals, not personal blame.
4. Estimate severity, confidence, and likely consequences.
5. Recommend process, documentation, review, ownership, or governance improvements.

## Risk Signals

Look for:
- one person or one agent producing most changes in a critical area,
- critical code with weak documentation or no durable rationale,
- direct commits bypassing expected review or ADR workflow,
- utility packages becoming transitively central without declared ownership,
- architecture-impacting changes without governance artifacts,
- large AI-generated changes without reviewable reasoning,
- opaque workflows that future maintainers cannot reproduce.

## Output

Write a durable socio-technical risk report to `workflow/investigations/YYYY-MM-DD-socio-technical-risk-<topic>.md` by default. Use chat-only output only when the user explicitly asks not to persist the report or the risk check is narrow and fully captured by an immediate review response.

The report must include:
- risk finding,
- evidence,
- affected systems or workflows,
- systemic consequence,
- confidence level,
- non-punitive mitigation,
- governance or documentation follow-up.

## Persistence Strategy

Write the socio-technical risk report incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title and risk lens.
2. Use the `edit` tool to append each subsequent report section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

## Guardrails

- Do not rank developers.
- Do not infer intent from sparse evidence.
- Do not use this skill for surveillance or productivity scoring.
- Frame findings as system resilience risks and governance gaps.
