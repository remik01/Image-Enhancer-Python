# CLI Decision Log

## 2026-05-26 - Phase 01 Architecture Decision Baseline

- Accepted `workflow/docs/overview.spec.md` as the authoritative project overview for phase implementation.
- Accepted a documentation-only Phase 01 scope: ADRs, architecture overview, decision log, phase plan, and phase evidence only. Product source code, dependency configuration, CI configuration, and runtime implementation remain out of scope until later phases.
- Accepted local-first baseline assumptions for implementation sequencing: PySide6/Qt desktop UI, local FastAPI REST adapter, versioned JSON project files, local configured plugins, OpenAI structured-output prompt interpretation, and bounded local async execution.
- Deferred optional CLI product behavior because the overview marks CLI as optional and no phase currently accepts a user-facing CLI surface.
- Deferred advanced extensions until separately planned: GPU acceleration, ONNX, local inference, semantic image search, OCR, advanced EXIF analysis, AI-generated recipes beyond prompt-to-pipeline proposals, remote plugin registries, production deployment, and distributed workers.
- Phase 02 is responsible for executable architecture checks, Python packaging/tool configuration, CI, and CodeQL. Phase 01 intentionally records architecture decisions without adding enforcement code.
