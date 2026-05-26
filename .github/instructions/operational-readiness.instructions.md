# Operational Readiness Instructions

Operational readiness covers startup behavior, configuration, observability, runtime failures, deployment assumptions, and supportability.

## Must Do

- Validate configuration at startup.
- Fail fast for missing required runtime settings.
- Use explicit timeouts, limits, and bounded retries for integrations.
- Provide useful logs for startup, shutdown, external calls, import/export summaries, and failure conditions.
- Document runtime assumptions that affect operators or future maintainers.
- Consider rollback or rework notes for risky changes.
- Keep health, readiness, or status reporting aligned with actual dependencies when applicable.

## Must Not Do

- Do not rely on hidden defaults for critical runtime behavior.
- Do not leave integrations without timeout or failure handling.
- Do not make failures observable only through stack traces.
- Do not introduce background work without lifecycle and shutdown behavior.
- Do not log sensitive operational data.

## Tests

Test invalid configuration, timeout/failure handling, startup wiring, retry exhaustion, and summary diagnostics where relevant.

## ADR Triggers

Propose ADR discussion for deployment assumptions, observability strategy, background processing, retry/fallback policy, health checks, or operational ownership changes.
