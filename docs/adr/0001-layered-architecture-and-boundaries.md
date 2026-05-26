# ADR-0001: Layered Architecture And Boundary Enforcement

## Status

Accepted

## Context

The overview defines an AI-powered image enhancement workbench that must remain maintainable across many implementation phases. The repository governance requires explicit separation between domain, application, adapters, UI, CLI, and bootstrap concerns. The first implementation phases will otherwise make long-lived choices about package structure, dependency direction, image-processing library placement, and architecture checks by accident.

The highest-risk drift for this project is allowing framework, image library, API, persistence, or UI details to enter domain or application code. That would make later adapters, UI decisions, plugin support, and AI integration harder to replace or review.

## Decision

Use a layered Python package rooted at `src/image_workbench` once Phase 02 creates source structure.

Layer responsibilities:

- `domain`: image concepts, enhancement operation definitions, pipeline definitions, validation, immutable configuration values, and invariant-preserving behavior.
- `application`: commands, results, use-case orchestration, and ports for external capabilities.
- `adapters`: implementations for image libraries, files, metadata, project persistence, OpenAI, REST DTOs, plugin loading, and queue/runtime infrastructure.
- `ui`: desktop presentation adapter that creates application commands and renders application results.
- `cli`: optional automation adapter only when explicitly accepted by a later phase.
- `bootstrap`: runtime wiring, configuration validation, startup, shutdown, and lifecycle assembly.
- `plugins`: local extension packages that participate only through the accepted application-facing plugin contract.

Dependency direction must point inward:

- Domain depends on no project-specific layer outside domain.
- Application may depend on domain and application-owned contracts.
- Adapters may depend on application and domain.
- UI and CLI may depend on application-facing APIs and presentation helpers.
- Bootstrap may depend on all layers only to assemble runtime dependencies.

Image-processing libraries such as Pillow and OpenCV must live in adapters behind application ports. The domain and application layers must not import them.

Phase 02 must add simple architecture-fitness tests for dependency direction, forbidden imports, adapter separation, and package cycles where practical. Those checks should be narrow, live in test scope, and run with the normal verification suite.

## Alternatives Considered

### Option 1: Flat Script-Oriented Layout

This would be fast initially but would encourage utilities, hidden dependencies, and mixed responsibilities. It is rejected because the overview intentionally uses this project to test architectural persistence.

### Option 2: Framework-Centered Core

FastAPI, PySide6, Pillow, or OpenCV types could be used directly in central models and services. This is rejected because it would leak adapter concerns into core logic and make UI, API, and image-processing choices hard to replace.

### Option 3: Multi-Repository Or Multi-Package Split

Separate repositories or installable packages could enforce stronger boundaries. This is deferred because the project is still early and a single package with architecture tests is enough to start.

### Option 4: Prose-Only Boundary Guidance

Documentation without tests would be simpler in Phase 02. It is rejected because the project explicitly requires architecture drift resistance.

### Option 5: Heavy Architecture Tooling Immediately

Dedicated dependency-analysis tools could enforce richer rules. This is deferred until simple tests prove insufficient, because early tooling should remain understandable and cheap to maintain.

## Consequences

### Positive

- Future feature phases have a clear ownership model.
- Image, HTTP, persistence, AI, plugin, and UI technology choices remain replaceable.
- Architecture-fitness tests can detect common drift early.
- Domain and application tests can stay fast and deterministic.

### Negative / Tradeoffs

- Early implementation requires more files and explicit mapping than a script-style prototype.
- Some adapter boundaries may feel verbose until feature complexity justifies them.
- Architecture tests can become brittle if they encode incidental names rather than documented boundaries.

### Operational Impact

- Runtime wiring belongs at bootstrap boundaries.
- Configuration and lifecycle behavior must not be hidden in domain or application code.
- Local runtime support can evolve without changing core models.

### Testing and Verification Impact

- Phase 02 must add package import tests and architecture-fitness tests.
- Every later phase must keep the static-analysis and architecture checks passing.
- Any weakening of boundary checks requires ADR or decision-log review.

## Follow-Up Work

- Phase 02 creates `src/image_workbench`, baseline tooling, architecture tests, and CI gates.
- Phase 03 implements framework-free domain models and invariants.
- Phase 04 implements application services and ports.
- Later adapter phases must keep external DTOs and technical clients outside domain/application.
- Revisit this ADR if package boundaries, dependency direction, or architecture-check policy changes.

