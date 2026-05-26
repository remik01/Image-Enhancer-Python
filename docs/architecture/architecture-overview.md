# Architecture Overview

## Purpose

This document summarizes the accepted baseline architecture for the AI-powered image enhancement workbench. It is a concise implementation guide for future phases and should be read with `AGENTS.md`, `workflow/docs/overview.spec.md`, and the ADRs under `docs/adr/`.

## Accepted Baseline

- The project is a local-first Python 3.12+ desktop workbench.
- Source code will be rooted under `src/image_workbench` once Phase 02 creates the package scaffold.
- The primary desktop UI baseline is PySide6/Qt.
- REST support is a local adapter for automation and integration, not a public production service.
- Project persistence uses versioned JSON project files.
- Plugins are local configured extensions loaded through a controlled application-facing contract.
- AI is limited to prompt interpretation into structured pipeline proposals.
- Image execution is deterministic and local through image-processing adapters.
- Long-running work uses bounded local async execution.

## Layer Responsibilities

### Domain

Owns image concepts, operation definitions, pipeline definitions, validation, immutable configuration values, and invariant-preserving behavior.

Domain must not import:

- FastAPI or HTTP clients,
- PySide6/Qt or any UI toolkit,
- Pillow, OpenCV, NumPy image-processing implementations,
- OpenAI clients or DTOs,
- persistence DTOs or file-system adapter details,
- plugin implementation modules,
- logging framework APIs.

### Application

Owns commands, results, use-case orchestration, and ports for external capabilities. Application may depend on domain and application-owned contracts only.

Application must not import adapter implementations, HTTP DTOs, UI classes, CLI parser internals, persistence DTOs, OpenAI DTOs, Pillow, or OpenCV.

### Adapters

Implement application ports and translate external systems or technical formats into internal models. Adapter areas include image processing, file-system access, metadata, project persistence, OpenAI, REST DTOs, plugin loading, and local queue/runtime infrastructure.

Adapters own technical validation, explicit mapping, timeout handling, safe failure translation, and boundary diagnostics.

### UI

Collects user intent and renders application state. UI code submits application commands and displays results, progress, validation failures, and job state.

UI code must keep toolkit types out of domain and application.

### CLI

CLI behavior is optional and not part of the accepted baseline implementation sequence. If added later, it must be an adapter that parses command-line intent, calls application services, and renders deterministic output.

### Bootstrap

Assembles runtime dependencies, validates configuration, wires desktop and API runtimes, owns startup/shutdown, and protects credentials in diagnostics.

Bootstrap must not contain business rules or use-case orchestration.

## Data Contracts

- REST request and response DTOs are adapter contracts.
- Project files are adapter contracts.
- AI structured-output responses are adapter contracts.
- Plugin manifests are adapter contracts.

All data contracts require explicit mapping before crossing into application or domain models.

## Runtime And Configuration

Runtime settings include OpenAI credentials, model selection, timeouts, limits, plugin paths, API host/port, and local file limits. Settings are typed bootstrap concerns and must fail fast when required values are missing or invalid.

Credentials must not be committed, serialized into project files, or written to logs/errors.

## Verification Expectations

Phase 02 must introduce the first enforceable architecture checks. Those checks should protect:

- domain independence,
- application independence from adapters,
- adapter separation,
- forbidden framework imports in core layers,
- package cycles where practical.

Later phases must keep those checks passing and may only weaken them with ADR, decision-log, or specification updates.

## Deferred Scope

The following are not accepted baseline scope:

- Tauri as the primary desktop shell,
- public production REST deployment,
- production authentication and authorization,
- database persistence,
- remote plugin registries,
- plugin sandboxing,
- remote image execution,
- message brokers or distributed workers,
- GPU acceleration,
- ONNX models,
- local inference,
- semantic image search,
- OCR,
- advanced EXIF analysis,
- production observability stacks.

## Phase Ownership

- Phase 01: architecture decisions and this overview.
- Phase 02: package scaffold, static-analysis gates, CI, CodeQL, and architecture-fitness tests.
- Phase 03: framework-free domain model and invariants.
- Phase 04: application use cases and ports.
- Phase 05 and later: adapters, persistence, runtime configuration, AI, plugins, queueing, API, UI, operational validation, and closure.

