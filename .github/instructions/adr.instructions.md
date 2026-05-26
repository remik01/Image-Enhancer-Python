# ADR And Architecture Governance Instructions

ADRs record decisions with long-term architectural consequences. They should be written when future maintainers need to know why a direction was chosen, not just what changed.

## ADR Required When Changing

- module boundaries or dependency direction,
- persistence strategy,
- integration architecture,
- serialization or public data contracts,
- concurrency or execution model,
- security architecture,
- observability strategy,
- deployment/runtime assumptions,
- dependency strategy,
- reusable conventions or cross-cutting patterns.

## ADR Usually Not Required For

- local bug fixes that preserve architecture,
- small refactors inside an existing boundary,
- tests that document existing behavior,
- implementation details already covered by an ADR,
- documentation updates that do not change direction.

Use the decision log for smaller durable decisions that are not ADR-sized. Append new decision-log entries to the bottom of `workflow/CLI.decision-log.md`; do not insert them at the top or reorder historical entries while adding a new decision.

## Decision Discipline

Default to no architectural change unless the change:

- fixes recurring defects or instability,
- removes a measurable bottleneck,
- reduces future maintenance, complexity, or onboarding cost,
- is required by an external business, regulatory, operational, or compatibility constraint.

For ADR-sized decisions, compare these options explicitly:

- no change,
- minimal change,
- target solution,
- extended solution only when clearly justified.

Evaluate alternatives by effort, risk, reversibility, blast radius, and long-term payoff. Include a rollback strategy and a review trigger when the decision may need later re-evaluation.

## ADR Content

An ADR should include:

- status,
- context,
- decision,
- consequences,
- alternatives considered,
- risks and mitigations,
- follow-up work if needed.

Keep ADRs specific. Do not use them as broad essays or implementation tickets.

## Persistence Strategy

Write ADR files incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple ADR sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the title, status, and context.
2. Use the `edit` tool to append each subsequent ADR section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

Decision-log entries are intentionally concise and may be appended to the bottom of `workflow/CLI.decision-log.md` as one complete dated entry.

## Agent Rules

- Before architectural changes, check existing ADRs and decision logs.
- If no ADR exists but the change has architectural impact, propose an ADR candidate before implementation.
- Do not silently introduce new architecture through code.
- If implementing an accepted ADR, keep code aligned with the decision and note deviations.
- Follow the Persistence Strategy section when creating or updating ADR files.

## Review Checklist

- Is the decision long-lived?
- Does it affect multiple modules or future work?
- Are alternatives and consequences documented?
- Are rejected options explained enough to prevent rediscovery?
- Is the decision consistent with existing ADRs?
