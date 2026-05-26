# Phase 02 Project Scaffold Static Analysis Plan

## Status

Completed 2026.05.26.

## Context

Phase 02 creates the first executable Python package scaffold and quality gates for the image workbench. The governing source is `workflow/phases/02_ProjectScaffoldStaticAnalysis.md`, with accepted architecture direction from ADR-0001 through ADR-0004 and repository governance in `AGENTS.md`.

## Goal

Add a minimal `src/image_workbench` package, Python verification configuration, architecture-fitness tests, CI/CodeQL workflows, and documentation needed for later phases to rely on enforceable boundaries.

## Non-Goals

Do not add image processing, AI, UI, REST API, persistence, plugin loading, or domain behavior in this phase. Do not add runtime dependencies for future capabilities before the phase that owns them.

## Assumptions

The scaffold targets Python 3.12 or newer. `mypy` is the selected baseline type checker because the phase explicitly allows a Python type checker and mypy is simple to run in local and CI contexts. Dependency hygiene is initially `python -m pip check`, which validates installed package metadata without introducing an additional scanner dependency during scaffold setup.

## Rationale

The repository currently has architecture documentation and ADRs but no importable product package or executable quality gates. A minimal package scaffold is the lowest-risk way to give later phases stable module ownership without prematurely designing domain models or adapters.

Ruff, mypy, pytest, and `pip check` are enough for this baseline because they cover formatting/linting, typing, behavior/architecture tests, and dependency metadata integrity without adding product dependencies. Architecture tests are implemented as plain pytest checks over repository files rather than a dedicated dependency-analysis library because ADR-0001 explicitly defers heavier architecture tooling until simple checks prove insufficient.

The CI workflow should mirror documented local commands so failures are reproducible. CodeQL should configure Python explicitly and include a SARIF artifact fallback because code-scanning upload permissions can vary by repository visibility and GitHub settings.

## Trade-offs & Limitations

Plain pytest architecture checks are intentionally narrower than a full dependency graph tool. They will catch direct forbidden imports and simple layer cycles, but they will not prove all runtime dependency behavior.

`python -m pip check` is dependency hygiene, not a vulnerability scanner. A security scanner can be added later if the project accepts the maintenance cost and failure policy.

The scaffold keeps runtime dependencies empty. This defers useful libraries such as Pillow, OpenCV, FastAPI, PySide6, and OpenAI until the phases that own their adapter contracts.

## Implementation Approach

Create `pyproject.toml` with package metadata, editable-install support, pytest configuration, Ruff lint/format configuration, and strict but small mypy configuration. Replace the PyCharm sample `main.py` with a thin import smoke entry point.

Create package directories for `domain`, `application`, `adapters`, and `bootstrap` only, matching the phase artifact list. Add import smoke tests and architecture tests that scan production modules under `src/image_workbench`.

Add GitHub Actions workflows for CI and CodeQL using only repository-local config created in this phase. Update `README.md` with setup and verification commands.

## Affected Layers

This phase creates package placeholders for domain, application, adapters, and bootstrap without implementing product behavior. Test scope gains architecture-fitness checks. Workflow scope gains implementation plan, phase log, and decision-log evidence. CI scope gains local-command parity checks.

## Tests and Verification

Run `python -m pytest`, `python -m ruff check .`, `python -m ruff format --check .`, `python -m mypy .`, `python -m pip check`, `git diff --check`, and a documentation/config secret scan before closeout. Locally inspect CI and CodeQL workflow references because GitHub Actions cannot be executed in this workspace.

## Risks

The main risk is over-encoding future architecture before feature phases clarify actual contracts. Keep tests tied to accepted ADRs and the phase file only. A secondary risk is local tool availability; if Ruff or mypy are not installed, install project development dependencies or report the blocked verification clearly.

## ADR / Decision-Log Needs

No new ADR is required if this phase implements ADR-0001's accepted boundary policy without changing dependency direction or adopting new architecture-check tooling. Append decision-log entries for mypy, baseline Ruff rules, `pip check`, and CodeQL upload/fallback convention.
