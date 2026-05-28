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

## 2026-05-27 - Phase 04 Application Service Grouping and Port Naming

- Accepted three focused application services (`SessionService`, `PipelineService`, `ExecutionService`) so each orchestrates one workflow concern and avoids a catch-all coordinator.
- Accepted application port names by capability (`ImageProcessingPort`, `ImageSourceAccessPort`, `MetadataAccessPort`, `ExportWriterPort`, `ProjectStoragePort`, `AIInterpretationPort`, `PluginDiscoveryPort`, `QueueExecutionPort`, `DiagnosticsPort`) to keep dependency intent explicit for later adapter phases.
- Recorded that the new command/result contracts remain internal to this repository and do not change dependency direction from ADR-0001; no new ADR is required for this phase.

## 2026-05-27 - Phase 05 Pillow Backend And Golden Fixtures

- Accepted Pillow as the canonical Phase 05 local image-processing backend; OpenCV behavior is deferred until a later phase or ADR identifies OpenCV-specific requirements.
- Accepted a golden-image comparison tolerance of maximum per-channel RGB delta `<= 1` to catch meaningful deterministic output drift while allowing tiny image-library encoding or rounding differences.
- Accepted fixture maintenance convention: update `tests/fixtures/golden/` only when an intentional operation behavior change or reviewed Pillow dependency update explains the changed pixels.
- Recorded that adding `blur` and `sepia` to the domain operation catalog is a Phase 05 prerequisite, because adapter execution receives already-validated domain `PipelineStep` instances.

## 2026-05-28 - Phase 06 Batch Metadata Export Workflows

- Accepted deterministic batch import ordering by casefolded source filename with resolved path as the tie-breaker, so repeated imports of the same folder produce stable application order.
- Accepted export conflict policies `fail`, `overwrite`, and `rename`; intra-batch duplicate output names are rejected unless `rename` is selected, and filesystem conflicts under `rename` receive deterministic numeric suffixes.
- Accepted explicit export metadata policy through `ExportPreset.strip_metadata`, defaulting to metadata stripping so image metadata is not silently carried into generated exports.
- Recorded that Phase 06 does not establish a public export compatibility contract or project persistence format; those remain candidates for later ADR review if external compatibility or persistence semantics become durable.

## 2026-05-28 - Phase 07 Project Persistence Contract

- Accepted project-file fixture convention: files under `tests/fixtures/projects/` are contract evidence and should change only for intentional schema or compatibility changes reviewed with ADR-0005.
- Accepted contract-test maintenance convention: every new project-file schema version, migration rule, required field, or secret-exclusion rule must have fixture or focused adapter test coverage before being considered supported.
