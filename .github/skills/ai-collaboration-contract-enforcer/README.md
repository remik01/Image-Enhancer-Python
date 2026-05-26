# AI Collaboration Contract Enforcer

## Reason

AI-assisted work can become fast but non-reproducible. This skill checks whether generated plans, code, docs, and decisions remain traceable, reviewable, and aligned with repository governance.

## Functionality

- Validates AI-assisted work against repository instructions, ADRs, decision logs, workflow artifacts, and verification expectations.
- Checks ADR obligations, persisted-plan requirements, rationale persistence, prompt-to-artifact traceability, context integrity, and review evidence.
- Detects governance drift and unresolved exceptions.
- Produces AI governance reports with corrective actions.

## Proper Use Cases

Use before major AI-generated changes, during PR review, after multi-agent work, or when governance compliance is unclear.

Do not use to create heavy process for trivial changes or to surveil individuals.

## Best Practices

- Tie every contract finding to an authoritative rule.
- Distinguish missing evidence from confirmed violation.
- Preserve reviewability and reproducibility over generation speed.
- Escalate architecture-impacting gaps to ADR or decision-log workflows.
