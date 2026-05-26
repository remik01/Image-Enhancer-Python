# Overview Coverage Review

## Artifact Audit Summary

Existing:

* AGENTS.md
* workflow/docs/overview.spec.md
* .github/instructions/
* .github/skills/
* docs/governance/future-phase-checklist.md
* main.py sample stub

To create or modify through phases:

* docs/adr/
* docs/architecture/
* docs/operations/
* docs/technical/
* pyproject.toml
* README.md
* USER_MANUAL.md
* src/image_workbench/
* tests/
* tests/fixtures/
* plugins/
* .github/workflows/ci.yml
* .github/workflows/codeql.yml
* .github/codeql/codeql-config.yml
* scripts/run-operational-validation.ps1
* scripts/check-local-runtime-prerequisites.ps1
* workflow/CLI.decision-log.md
* workflow/plans/
* workflow/logs/
* workflow/investigations/

Explicitly out of scope for this phase plan unless a later ADR or user request accepts them:

* Docker, cloud deployment, message brokers, remote workers, external monitoring stacks, production authentication, remote plugin registries, database provisioning, GPU acceleration, ONNX, local inference, semantic image search, OCR, advanced EXIF analysis, AI-generated recipes beyond prompt-to-pipeline proposals, and multi-agent runtime workflows.

## Traceability Matrix

| Overview Item ID | Overview Source / Summary | Phase(s) Covering It | Acceptance / Test Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| SRC-001 | Shared ChatGPT brief converted into canonical overview | 01_ArchitectureDecisionBaseline.md; 15_ProjectClosureAndHandover.md | ADRs and final handover cite and reconcile the overview source. | Covered | The shared transcript itself is not persisted. |
| PUR-001 | Build a useful local image enhancement workbench | 03_DomainModelPipelineInvariants.md; 04_ApplicationUseCasesAndPorts.md; 05_LocalImageProcessingAdapters.md; 13_DesktopWorkbenchUi.md | Domain, application, adapter, and UI acceptance criteria cover usable local workbench behavior. | Covered | End-to-end usefulness is validated in Phase 14. |
| PUR-002 | Evaluate disciplined medium-sized Python engineering | 01_ArchitectureDecisionBaseline.md; 02_ProjectScaffoldStaticAnalysis.md; 14_PostImplementationOperationalValidation.md; 15_ProjectClosureAndHandover.md | ADRs, static gates, operational evidence, and strict coverage review prove governance discipline. | Covered | Static gates are intentionally before feature work. |
| ACT-001 | Desktop users enhancing local images | 05_LocalImageProcessingAdapters.md; 13_DesktopWorkbenchUi.md | UI acceptance covers loading image references, editing pipelines, execution, progress, and export controls. | Covered | UI technology remains decided by Phase 01 ADR. |
| ACT-002 | Power users needing batch, export, and repeatable projects | 06_BatchMetadataExportWorkflows.md; 07_ProjectPersistenceContract.md; 14_PostImplementationOperationalValidation.md | Batch/export tests and persistence round-trip tests cover repeatability. | Covered | Operational validation repeats deterministic scenarios. |
| ACT-003 | Users requesting AI style transformations | 09_AIPromptToPipeline.md; 13_DesktopWorkbenchUi.md | AI proposal tests and UI proposal rendering tests cover reviewable prompt workflows. | Covered | AI execution remains local only after acceptance. |
| ACT-004 | Plugin authors adding operations | 10_PluginContractSamplePlugin.md | Plugin registration, compatibility, conflict, and sample plugin tests cover this actor. | Covered | Third-party distribution is out of scope. |
| ACT-005 | REST API clients or hybrid shell | 12_RestApiContractsBackend.md; 13_DesktopWorkbenchUi.md | API contract tests and UI integration via accepted runtime cover this actor. | Covered | Public network exposure depends on ADR. |
| ACT-006 | Maintainers and reviewers | 01_ArchitectureDecisionBaseline.md; 02_ProjectScaffoldStaticAnalysis.md; 15_ProjectClosureAndHandover.md | ADRs, architecture tests, CI, CodeQL, README, and technical docs cover maintainability. | Covered | Review evidence is phase-scoped and final. |
| CF-001 | Load local images into a workbench session | 04_ApplicationUseCasesAndPorts.md; 06_BatchMetadataExportWorkflows.md; 13_DesktopWorkbenchUi.md | Application command tests, file adapter tests, and UI command tests. | Covered | File DTOs stay out of domain. |
| CF-002 | Build pipelines from explicit operations | 03_DomainModelPipelineInvariants.md; 04_ApplicationUseCasesAndPorts.md; 05_LocalImageProcessingAdapters.md | Pipeline invariant tests, application orchestration tests, and golden image tests. | Covered | Baseline operations precede advanced operations. |
| CF-003 | Convert natural language to structured proposals | 09_AIPromptToPipeline.md | Structured-output mapper tests and invalid AI output tests. | Covered | Live API calls are not required in automated tests. |
| CF-004 | Review and edit AI-generated pipelines before execution | 04_ApplicationUseCasesAndPorts.md; 09_AIPromptToPipeline.md; 13_DesktopWorkbenchUi.md | Application tests verify proposals are not executed until accepted; UI tests render editable proposal state. | Covered | User acceptance remains required. |
| CF-005 | Execute pipelines locally | 05_LocalImageProcessingAdapters.md; 11_AsyncQueueProgressCancellation.md | Golden image tests and queued execution tests. | Covered | Remote processing is not in scope. |
| CF-006 | Batch processing with deterministic order and export presets | 06_BatchMetadataExportWorkflows.md; 14_PostImplementationOperationalValidation.md | Batch ordering tests and operational repeated-run scenarios. | Covered | Large-data assumptions are local and bounded. |
| CF-007 | Undo/redo pipeline model | 03_DomainModelPipelineInvariants.md; 04_ApplicationUseCasesAndPorts.md; 13_DesktopWorkbenchUi.md | Domain history tests, application orchestration tests, and UI state tests. | Covered | Undo/redo applies to pipeline edits. |
| CF-008 | Controlled plugins | 10_PluginContractSamplePlugin.md | Plugin loader, contract, conflict, and sample plugin tests. | Covered | Remote plugin registries are explicitly out of scope. |
| CF-009 | Project persistence | 07_ProjectPersistenceContract.md; 15_ProjectClosureAndHandover.md | Round-trip, schema, compatibility, and documentation tests/reviews. | Covered | Database persistence is not assumed. |
| CF-010 | Async queue with progress, failure, and cancellation | 11_AsyncQueueProgressCancellation.md; 14_PostImplementationOperationalValidation.md | Queue tests and operational cancellation/timeout scenarios. | Covered | No external workers or message brokers. |
| CF-011 | REST API for local integration or hybrid shell | 12_RestApiContractsBackend.md | Route, DTO, contract, and error-handler tests. | Covered | Authentication and public exposure require ADR. |
| CF-012 | Reproducible workflows | 02_ProjectScaffoldStaticAnalysis.md; 14_PostImplementationOperationalValidation.md; 15_ProjectClosureAndHandover.md | CI/static commands, operational helper, and strict implementation coverage review. | Covered | Phase logs and plans preserve implementation evidence. |
| FR-001 | Load local image files into a session | 04_ApplicationUseCasesAndPorts.md; 06_BatchMetadataExportWorkflows.md; 13_DesktopWorkbenchUi.md | Command, adapter, and UI tests. | Covered | Supported formats are finalized during adapter implementation. |
| FR-002 | Baseline local operations: blur, sharpen, contrast, sepia | 05_LocalImageProcessingAdapters.md | Golden image tests for each baseline operation. | Covered | Advanced operations can be later phases. |
| FR-003 | Ordered pipelines of explicit operations and parameters | 03_DomainModelPipelineInvariants.md | Pipeline validation and ordering tests. | Covered | Serialization is covered in persistence phase. |
| FR-004 | Batch folder import, rename/export, presets, deterministic order | 06_BatchMetadataExportWorkflows.md | Batch ordering, conflict, and export preset tests. | Covered | Operational validation repeats representative batches. |
| FR-005 | AI prompt-to-pipeline proposals | 09_AIPromptToPipeline.md | Structured-output mapping and validation tests. | Covered | Live credentials are not required for test pass. |
| FR-006 | Review/edit AI proposals before execution | 09_AIPromptToPipeline.md; 13_DesktopWorkbenchUi.md | Proposal acceptance tests and UI presentation tests. | Covered | Automatic execution is forbidden. |
| FR-007 | Execute accepted pipelines locally | 05_LocalImageProcessingAdapters.md; 11_AsyncQueueProgressCancellation.md | Adapter golden tests and queued execution tests. | Covered | Local adapter selected by ADR. |
| FR-008 | Plugin mechanism for operations | 10_PluginContractSamplePlugin.md | Plugin registration and sample execution tests. | Covered | Trust model documented in plugin contract. |
| FR-009 | Undo/redo of pipeline edits | 03_DomainModelPipelineInvariants.md | Domain history tests cover add, edit, undo, redo, and boundary cases. | Covered | UI rendering comes later. |
| FR-010 | Persist project state | 07_ProjectPersistenceContract.md | Round-trip and schema validation tests. | Covered | Secrets must not serialize. |
| FR-011 | Async processing queue | 11_AsyncQueueProgressCancellation.md | Queue lifecycle, cancellation, timeout, duplicate, and failure tests. | Covered | External workers out of scope. |
| FR-012 | REST API capabilities | 12_RestApiContractsBackend.md | API contract and route tests. | Covered | Public exposure is ADR-controlled. |
| FR-013 | Metadata and histogram workflows | 06_BatchMetadataExportWorkflows.md | Metadata, stripping, malformed metadata, and histogram tests. | Covered | Advanced EXIF analysis remains future scope. |
| NFR-001 | Domain independent from frameworks and adapters | 02_ProjectScaffoldStaticAnalysis.md; 03_DomainModelPipelineInvariants.md | Architecture-fitness tests and domain import checks. | Covered | Boundary tests run before feature work. |
| NFR-002 | Application services and ports | 04_ApplicationUseCasesAndPorts.md | Fake-port application tests and architecture checks. | Covered | Ports are named by capability. |
| NFR-003 | Adapter mapping, validation, timeouts, retries, failure translation | 05_LocalImageProcessingAdapters.md; 06_BatchMetadataExportWorkflows.md; 07_ProjectPersistenceContract.md; 09_AIPromptToPipeline.md; 12_RestApiContractsBackend.md | Adapter contract tests and failure-translation tests. | Covered | Retry policy only where justified by ADR or boundary needs. |
| NFR-004 | AI interpretation separate from execution | 09_AIPromptToPipeline.md; 13_DesktopWorkbenchUi.md | Tests verify AI output remains a proposal until accepted. | Covered | Deterministic execution remains local. |
| NFR-005 | Meaningful pytest coverage including golden and architecture tests | 02_ProjectScaffoldStaticAnalysis.md; 05_LocalImageProcessingAdapters.md; 15_ProjectClosureAndHandover.md | pytest, golden fixtures, architecture tests, and final implementation coverage. | Covered | Property tests are added where valuable, not mechanically. |
| NFR-006 | Ruff, type checker, pytest, architecture checks, CodeQL | 02_ProjectScaffoldStaticAnalysis.md | Verification commands and workflow review. | Covered | Code scanning upload may need repository setting follow-up. |
| NFR-007 | Bounded deterministic batch/image handling | 05_LocalImageProcessingAdapters.md; 06_BatchMetadataExportWorkflows.md; 14_PostImplementationOperationalValidation.md | Boundary-size tests and operational large-input scenarios. | Covered | Performance claims remain bounded. |
| NFR-008 | Runtime configuration validation | 08_RuntimeConfigurationDiagnostics.md | Settings validation and startup tests. | Covered | Secrets documented with placeholders only. |
| NFR-009 | UI intent/rendering and non-blocking work | 13_DesktopWorkbenchUi.md; 11_AsyncQueueProgressCancellation.md | UI state tests and queue tests. | Covered | UI toolkit types stay out of core. |
| NFR-010 | Safe logs and errors | 08_RuntimeConfigurationDiagnostics.md; 09_AIPromptToPipeline.md; 14_PostImplementationOperationalValidation.md | Redaction tests and operational diagnostics review. | Covered | Raw image payload logging is forbidden. |
| NFR-011 | ADR/decision-log governance | 01_ArchitectureDecisionBaseline.md; all implementation phases | ADR/Decision-Log Follow-Up sections and phase logs. | Covered | Every phase includes governance follow-up. |
| TECH-001 | Python 3.12+, pyproject, pytest, Ruff, mypy | 02_ProjectScaffoldStaticAnalysis.md | Tool config and local/CI command acceptance criteria. | Covered | Type checker chosen in decision log. |
| TECH-002 | FastAPI, Pydantic, Pillow, OpenCV, NumPy, OpenAI | 01_ArchitectureDecisionBaseline.md; 05_LocalImageProcessingAdapters.md; 09_AIPromptToPipeline.md; 12_RestApiContractsBackend.md | ADRs and adapter/API tests prove dependency ownership. | Covered | Dependencies are not added before owning phases. |
| TECH-003 | PySide6/Qt versus Tauri choice | 01_ArchitectureDecisionBaseline.md; 13_DesktopWorkbenchUi.md | UI ADR and UI startup/test acceptance. | Covered | Only one baseline is implemented unless ADR changes. |
| ARCH-001 | Layered module expectations | 01_ArchitectureDecisionBaseline.md; 02_ProjectScaffoldStaticAnalysis.md | ADRs, architecture overview, package scaffold, architecture tests. | Covered | Dependency direction is enforceable. |
| RUNTIME-001 | Local desktop runtime and local image processing | 08_RuntimeConfigurationDiagnostics.md; 13_DesktopWorkbenchUi.md; 14_PostImplementationOperationalValidation.md | Startup/config tests, UI smoke checks, operational validation. | Covered | Production deployment is not implied. |
| RUNTIME-002 | Project file persistence with schema/versioning | 07_ProjectPersistenceContract.md | Contract documentation and round-trip/compatibility tests. | Covered | Database persistence is not assumed. |
| RUNTIME-003 | Local configured plugin discovery | 08_RuntimeConfigurationDiagnostics.md; 10_PluginContractSamplePlugin.md | Settings validation, path normalization, loader tests. | Covered | Remote plugin registry is out of scope. |
| UIAPI-001 | Desktop workbench views and state | 13_DesktopWorkbenchUi.md | Presentation and UI state tests plus manual smoke check. | Covered | Exact UI toolkit decided earlier. |
| UIAPI-002 | API DTO separation and mapping | 12_RestApiContractsBackend.md | API mapper and contract tests. | Covered | Domain internals not exposed as wire shape. |
| CLI-001 | Optional CLI automation surface | - | No phase owns CLI product behavior. | Explicitly out of scope | Overview marks CLI as optional; operational validation can use API or application-service boundaries. Add a later phase if CLI is explicitly accepted. |
| SEC-001 | Secrets, local files, plugin loading, API exposure, metadata security | 08_RuntimeConfigurationDiagnostics.md; 10_PluginContractSamplePlugin.md; 12_RestApiContractsBackend.md; 14_PostImplementationOperationalValidation.md | Settings/redaction tests, path validation tests, API error tests, operational diagnostics. | Covered | Authentication requires ADR if public exposure is accepted. |
| OPS-001 | Post-implementation operational validation | 14_PostImplementationOperationalValidation.md | Operational helper and evidence acceptance criteria. | Covered | Validation cannot implement remediation. |
| DOC-001 | Final handover and implementation coverage | 15_ProjectClosureAndHandover.md | Technical docs, README, USER_MANUAL, strict implementation coverage validation. | Covered | Incomplete closure requires explicit user acceptance. |
| FUT-001 | GPU, ONNX, local inference, semantic search, OCR, EXIF analysis, AI recipes, multi-agent workflows | - | No acceptance evidence in this phase sequence. | Deferred | These are explicitly advanced extensions from the overview, not baseline implementation scope. |
