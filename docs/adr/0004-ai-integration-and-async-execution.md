# ADR-0004: AI Integration And Async Execution

## Status

Accepted

## Context

The overview requires AI-assisted prompt-to-pipeline conversion, deterministic local image execution, and non-blocking long-running workflows. These concerns are coupled by user experience but must remain architecturally separate: AI interprets intent, application validates proposals, local adapters execute accepted pipelines, and queued runtime infrastructure handles long-running work.

The project also needs safe runtime configuration for OpenAI credentials, timeouts, model selection, plugin paths, API limits, and local file limits.

## Decision

Use the OpenAI Responses API behind an AI adapter for prompt interpretation.

AI integration rules:

- AI output is a structured pipeline proposal, not executable authority.
- AI DTOs stay inside the AI adapter.
- AI proposals must be mapped and validated before becoming application pipeline proposals.
- Users or callers must accept proposals before execution.
- Automated tests must not require live OpenAI credentials or network access.
- The adapter must enforce configured model, timeout, retry, payload, and structured-output limits.
- Diagnostics must avoid credentials and large prompt or image payload dumps.

Use bounded local in-process async execution for baseline long-running work.

Async execution rules:

- Application owns job-state contracts and observable progress semantics.
- Bootstrap owns worker lifecycle and shutdown.
- The local executor must support progress, cancellation, timeout handling, failure reporting, and deterministic partial-result policy.
- External workers, message brokers, distributed queues, and remote execution are out of scope for the baseline.

Use typed bootstrap configuration for runtime settings and fail fast when required configuration is missing or invalid. Use lightweight local status or health behavior only; production observability ownership is not accepted in this baseline.

## Alternatives Considered

### Option 1: AI Generates And Executes Operations Directly

This is rejected because it would hide behavior, bypass user review, and weaken deterministic execution.

### Option 2: No AI Integration

This would reduce integration risk but would miss a core purpose of the project. It is rejected for the baseline.

### Option 3: Remote AI Image Processing

This is rejected because the project is a local image enhancement workbench and should not make image execution opaque or remote by default.

### Option 4: Unbounded Parallel Execution

This is rejected because image processing and batch work can be resource-intensive and require cancellation and partial-failure semantics.

### Option 5: External Queue Or Message Broker

This is deferred because the overview does not require distributed execution, and adding infrastructure would increase operational scope prematurely.

### Option 6: Production Observability Stack

This is deferred because the baseline needs local diagnostics and status behavior, not dashboards, tracing, alerting, or external monitoring ownership.

## Consequences

### Positive

- AI remains reviewable and deterministic execution remains local.
- Runtime failures can be handled through explicit adapter and queue boundaries.
- Tests can use fakes and recorded structured responses without live credentials.
- Async behavior can protect UI and API callers from blocking work.

### Negative / Tradeoffs

- The AI adapter needs explicit schema and mapper maintenance.
- In-process queues are not suitable for distributed production workloads.
- Progress and partial-failure semantics must be defined carefully to avoid misleading users.

### Operational Impact

- OpenAI credentials and model settings are runtime configuration concerns.
- Missing required configuration must fail clearly at startup or command boundary.
- Long-running jobs need lifecycle and shutdown behavior owned by bootstrap.

### Testing and Verification Impact

- AI tests must cover structured-output mapping, missing fields, unsupported operations, timeout/failure translation, and redaction.
- Queue tests must cover simultaneous submissions, cancellation, timeout, duplicate/conflicting jobs, failure propagation, deterministic result state, and shutdown.
- Operational validation must exercise large valid inputs, large malformed inputs, repeated runs, cancellation, and diagnostic output.

## Follow-Up Work

- Phase 08 implements typed runtime configuration and diagnostics.
- Phase 09 implements AI prompt-to-pipeline mapping.
- Phase 11 implements bounded local async execution.
- Phase 14 validates runtime behavior through operational scenarios.
- Revisit this ADR before adding local inference, ONNX, remote image execution, message brokers, distributed workers, caching, or production observability tooling.

