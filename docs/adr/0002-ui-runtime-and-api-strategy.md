# ADR-0002: Desktop UI Runtime And Local REST API Strategy

## Status

Accepted

## Context

The overview names a modern desktop workbench as the primary user experience and presents two UI options: PySide6/Qt or Tauri with a Python backend. It also requires REST API support for local integration, automation, or a hybrid desktop shell. Choosing both desktop strategies as active baselines would split early implementation effort and force premature API-bridge complexity.

The project should stay local-first while preserving a reviewable REST adapter boundary for automation and possible future client integration.

## Decision

Use PySide6/Qt as the primary desktop UI baseline for the first implementation sequence.

Use FastAPI as a local REST API adapter when API behavior is implemented. The REST API is application-adjacent and local by default. It is not accepted as a public production service in this baseline.

Runtime surface ownership:

- The PySide6 UI calls application use cases or presentation adapters and must not call infrastructure adapters directly.
- The FastAPI adapter maps HTTP DTOs to application commands and maps application results or failures back to HTTP responses.
- API DTOs stay inside adapter code and must not become domain or application models by accident.
- Bootstrap owns separate local runtime assembly for desktop and API surfaces.
- API host, port, timeout, payload limits, and local exposure settings are configuration concerns handled at bootstrap.

Tauri is deferred. It can be reconsidered only through ADR review after the PySide6 baseline proves insufficient or a web-shell requirement becomes more important than native desktop integration.

If the REST API is exposed beyond local loopback or requires multi-user access, authentication and authorization must be decided in a new ADR before implementation.

## Alternatives Considered

### Option 1: PySide6/Qt Desktop Baseline

This is accepted because it is mature, native-feeling, and well suited to a local desktop workbench with long-running image workflows.

### Option 2: Tauri Plus Python Backend

This remains a plausible future direction for a web-style desktop shell. It is deferred because it would make REST communication a prerequisite for the primary UI before core behavior exists.

### Option 3: REST API Only

This would simplify UI work early but would not deliver the desktop workbench described by the overview. It is rejected as the primary baseline.

### Option 4: Public API Service

This would require authentication, authorization, deployment, and operational decisions outside current scope. It is rejected for the baseline.

### Option 5: UI Directly Coupled To Adapters

This would be fast but would bypass application services and duplicate domain or adapter rules in UI code. It is rejected.

## Consequences

### Positive

- The project has one primary desktop direction for Phase 13.
- REST support remains available for automation and possible local integration.
- UI and API can both remain replaceable adapters around application use cases.
- Public-service security concerns are not silently introduced.

### Negative / Tradeoffs

- A future Tauri shell would require additional work and possibly a revised UI ADR.
- PySide6 adds desktop runtime and packaging considerations.
- API behavior still needs DTO and contract tests even when local-only.

### Operational Impact

- Desktop startup and API startup are local runtime concerns.
- Bootstrap must validate UI/API runtime settings at startup.
- API exposure beyond loopback is not part of the accepted baseline.

### Testing and Verification Impact

- UI tests should focus on presentation state, command creation, async state, and error rendering.
- API tests must cover DTO mapping, route behavior, malformed payloads, and safe error responses.
- Architecture checks must prevent UI toolkit and FastAPI imports from entering domain/application.

## Follow-Up Work

- Phase 08 defines runtime configuration and diagnostics.
- Phase 12 implements local REST API contracts.
- Phase 13 implements the PySide6 desktop workbench.
- Revisit this ADR before adopting Tauri, public API exposure, authentication, or production deployment assumptions.

