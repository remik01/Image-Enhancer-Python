# Logging Instructions

Logging exists for operational diagnostics, incident analysis, and reviewable behavior. Logs must be useful, bounded, and safe.

## Must Do

- Log at system boundaries, important workflow milestones, and failure points.
- Include stable context such as operation, external system, identifier, file path, row, status, elapsed time, and counts when relevant.
- Use structured arguments where the logging framework supports them.
- Keep log messages deterministic and concise.
- Log retries, retry exhaustion, fallback activation, skipped records, and partial failures.
- Protect secrets, tokens, credentials, PII, and large payloads.

## Must Not Do

- Do not log secrets or full sensitive payloads.
- Do not log massive collections or file contents by default.
- Do not use logging as control flow.
- Do not log and rethrow repeatedly without adding new context.
- Do not use `System.out`/`System.err` in application code except deliberate CLI output.
- Do not hide failures behind debug-only logs.

## Levels

- `ERROR`: operation failed and requires attention or caller-visible failure.
- `WARN`: degraded behavior, fallback, skipped input, retry exhaustion, or recoverable external issue.
- `INFO`: lifecycle, completed high-value operations, summaries, and user-relevant milestones.
- `DEBUG`: diagnostic details useful during development or incident investigation.
- `TRACE`: rare, very detailed flow information; avoid in normal implementation.

## Layer Rules

- Domain should usually not depend on logging APIs.
- Application may log use-case start/end summaries and meaningful business workflow outcomes.
- Adapters should log external calls, import/export summaries, malformed technical input, retries, and integration failures.
- UI/CLI should separate user output from diagnostic logs.
- Bootstrap should log configuration source summaries without secrets and startup failures clearly.

## Tests

Add log-focused tests when logging is part of required behavior, such as security redaction, audit-like summaries, retry diagnostics, or no secret leakage.

## ADR Triggers

Propose ADR discussion for logging framework changes, structured logging strategy, correlation IDs, audit logging, telemetry conventions, or operational observability changes.

## Checklist

- Is the log at the right layer and level?
- Does it include useful safe context?
- Are secrets and large payloads protected?
- Does it avoid duplicate noise?
- Would it help diagnose a real failure?
