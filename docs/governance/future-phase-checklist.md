# Future Phase Governance Checklist

Use this checklist before implementing a workflow phase.

- Read `AGENTS.md`, the target phase file, relevant ADRs, the decision log, and nearby code.
- Confirm the phase ticket exists before committing phase work.
- Keep changes inside the affected layers named by the phase.
- Do not add domain behavior to adapters, UI, CLI, or bootstrap.
- Do not add adapter, UI, REST, SQL, persistence, frontend, desktop UI, or framework concerns to domain.
- Add or update tests for meaningful behavior.
- Evaluate ADR need when changing module boundaries, dependency direction, runtime strategy, public contracts, persistence, security, concurrency, or reusable conventions.
- Record durable local decisions in `workflow/CLI.decision-log.md`.
- Run relevant Python verification and report skipped checks.
- For verification phases, separate completed baseline behavior from future-scope ideas and record environment-dependent checks as manual or skipped with a reason.
