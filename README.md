# Image Workbench

Image Workbench is a local image enhancement workbench built as a deliberately layered Python project. The current implementation is a Phase 02 scaffold: it creates the package layout, quality gates, CI configuration, and architecture-fitness tests without adding product behavior.

## Architecture Baseline

The package root is `src/image_workbench`.

- `domain` owns future image concepts and invariants.
- `application` owns future use cases, commands, results, and ports.
- `adapters` will implement technical integrations and external contract mapping.
- `bootstrap` will own runtime wiring, configuration validation, and lifecycle concerns.

Architecture tests enforce the initial boundary policy from `AGENTS.md` and ADR-0001. Domain and application code must not import UI, HTTP, persistence, AI, plugin, image-processing, or adapter implementation dependencies.

## Local Setup

Use Python 3.12 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Verification

Run the scaffold quality gates locally after installing development dependencies:

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy .
python -m pip check
```

These commands are mirrored by `.github/workflows/ci.yml`. CodeQL analysis is configured by `.github/workflows/codeql.yml` and `.github/codeql/codeql-config.yml`.

## Current Scope

This scaffold intentionally does not implement image transformations, AI prompt interpretation, REST endpoints, desktop UI, persistence, plugin loading, or domain behavior. Those belong to later workflow phases and must preserve the dependency direction established here.
