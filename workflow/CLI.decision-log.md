# CLI Decision Log

## 2026-05-26 - Phase 01 Architecture Decision Baseline

- Accepted `workflow/docs/overview.spec.md` as the authoritative project overview for phase implementation.
- Accepted a documentation-only Phase 01 scope: ADRs, architecture overview, decision log, phase plan, and phase evidence only. Product source code, dependency configuration, CI configuration, and runtime implementation remain out of scope until later phases.
- Accepted local-first baseline assumptions for implementation sequencing: PySide6/Qt desktop UI, local FastAPI REST adapter, versioned JSON project files, local configured plugins, OpenAI structured-output prompt interpretation, and bounded local async execution.
- Deferred optional CLI product behavior because the overview marks CLI as optional and no phase currently accepts a user-facing CLI surface.
- Deferred advanced extensions until separately planned: GPU acceleration, ONNX, local inference, semantic image search, OCR, advanced EXIF analysis, AI-generated recipes beyond prompt-to-pipeline proposals, remote plugin registries, production deployment, and distributed workers.
- Phase 02 is responsible for executable architecture checks, Python packaging/tool configuration, CI, and CodeQL. Phase 01 intentionally records architecture decisions without adding enforcement code.

## 2026-05-26 - Phase 02 Project Scaffold Static Analysis

- Selected `mypy` as the baseline Python type checker because it is explicit, CI-friendly, and sufficient for the current package scaffold without adding a second static-analysis toolchain.
- Selected a small Ruff baseline covering `E`, `F`, `I`, `UP`, `B`, and `RUF` rules so early lint findings remain actionable without broad suppressions or style-heavy policy.
- Selected `python -m pip check` as the initial dependency hygiene command because Phase 02 has no runtime dependencies and should not introduce a vulnerability scanner before dependency policy is needed.
- Accepted plain pytest architecture-fitness checks for Phase 02 instead of a dedicated dependency-analysis tool, matching ADR-0001's preference for simple checks before heavier tooling.
- Accepted CodeQL code-scanning upload as the primary path and SARIF artifact upload as a fallback convention because repository code-scanning permissions may vary by visibility or GitHub settings.
