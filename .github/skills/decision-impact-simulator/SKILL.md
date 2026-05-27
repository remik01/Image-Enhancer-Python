---
name: decision-impact-simulator
description: "[Python] Simulate technical, operational, organizational, maintenance, testing, observability, AI-workflow, migration, and rollback consequences of proposed architectural or process decisions. Use during planning, ADR drafting, major refactoring, dependency adoption, runtime model changes, or governance tradeoff analysis."
---

# Decision Impact Simulator

## Overview

Use this skill to explore second-order consequences of proposed decisions. It is not a binary approval tool; it is an uncertainty-aware impact analysis workflow.

Primary source specification: `.github/skills/advanced_ai_skills_specification_pack.md`.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable analysis model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning analysis model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

Do not treat model availability as part of the decision evaluation. Impact conclusions must remain based on project evidence, realistic alternatives, constraints, uncertainty, governance obligations, and reversible implementation paths.

## Workflow

1. Define the proposed decision in one sentence.
2. Read relevant context:
   - `AGENTS.md`,
   - ADRs and decision logs,
   - project overview, plans, phases, and investigations,
   - current module/dependency structure,
   - tests, CI, deployment, security, and operational instructions affected by the decision.
3. Identify alternatives:
   - no change,
   - minimal change,
   - proposed change,
   - extended solution only when realistically in scope.
4. Analyze direct effects and ripple effects.
5. Estimate migration, testing, documentation, operational, onboarding, and rollback impact.
6. Identify hidden dependencies and likely future maintenance cost.
7. State confidence and uncertainty explicitly.
8. Recommend whether the decision needs an ADR, decision-log entry, investigation, or prototype.

## Impact Dimensions

Assess:
- architecture and dependency direction,
- module ownership,
- public contracts and compatibility,
- test strategy and fixture burden,
- static-analysis and CI impact,
- observability and incident response,
- deployment and runtime assumptions,
- security posture,
- team knowledge and onboarding,
- AI workflow reproducibility and rationale persistence,
- reversibility and rollback feasibility.

## Output

Write a durable decision impact report to `workflow/investigations/YYYY-MM-DD-decision-impact-<topic>.md` by default. Use chat-only output only when the user explicitly asks not to persist the report or the decision is narrow, reversible, and fully captured by an immediate answer.

The report must include:
- proposed decision,
- alternatives compared,
- direct effects,
- indirect effects,
- operational implications,
- testing and observability impact,
- organizational and onboarding impact,
- rollback feasibility,
- long-term maintenance implications,
- uncertainty indicators,
- recommended governance artifact.

## Persistence Strategy

Write the decision impact report incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title and proposed decision.
2. Use the `edit` tool to append each subsequent report section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

## Guardrails

- Do not advocate fashionable architecture without local evidence.
- Do not collapse tradeoffs into a single score.
- Do not ignore human or operational consequences.
- Do not treat ease of implementation as proof of long-term suitability.
