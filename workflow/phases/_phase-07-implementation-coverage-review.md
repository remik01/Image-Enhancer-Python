# Phase 07 Implementation Coverage Review

## Context

Manual review date: 2026-05-28.

Scope: this review checks whether implementation evidence covers `workflow/phases/07_ProjectPersistenceContract.md`. It does not replace source inspection, tests, ADR review, or human judgment.

Allowed statuses: `Covered`, `Partially covered`, `Deferred`, `Explicitly out of scope`, `Needs clarification`, `Missing`.

## Phase

- Phase file: `workflow/phases/07_ProjectPersistenceContract.md`
- Title: Project Persistence Contract
- Tickets: IEP-007
- Compared against: worktree status

## Changed Files

- `docs/adr/0005-project-file-schema-versioning.md`
- `docs/architecture/project-file-contract.md`
- `src/image_workbench/adapters/persistence/__init__.py`
- `src/image_workbench/adapters/persistence/project_file.py`
- `src/image_workbench/adapters/persistence/project_mapper.py`
- `src/image_workbench/adapters/persistence/schema.py`
- `src/image_workbench/application/results.py`
- `src/image_workbench/application/services.py`
- `tests/application/test_session_service.py`
- `tests/adapters/persistence/test_project_file_round_trip.py`
- `tests/adapters/persistence/test_project_file_validation.py`
- `tests/fixtures/projects/invalid-unknown-field.json`
- `tests/fixtures/projects/invalid-version.json`
- `tests/fixtures/projects/valid-v1-project.json`
- `workflow/CLI.decision-log.md`
- `workflow/logs/phase-07-implementation-log.md`
- `workflow/phases/_phase-07-implementation-coverage-review.md`
- `workflow/plans/07_project_persistence_contract_plan.md`

## Suggested Verification

- `python -m pytest`: Passed, 94 tests.
- `python -m ruff check .`: Passed.
- `python -m ruff format --check .`: Passed.
- `python -m mypy .`: Passed.
- `git diff --check`: Passed; Git reported line-ending warnings only.
- `python -m pip check`: Passed.
- `python -B .github\skills\implement-phase\scripts\check_phase_artifact_coverage.py --phase 7`: Expected artifacts matched; ADR and decision-log are intentional governance additions required by phase follow-up.

## Coverage Matrix

| Phase Item ID | Phase Section | Phase Requirement / Summary | Implementation Evidence | Verification Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| P07-GOAL-001 | Goal | Implement versioned project save/load support for pipelines, image references, and settings. | `ProjectFileStorage`, `SessionSnapshot.source_uri`, `snapshot_to_project_document`, `project_document_to_snapshot`, v1 schema docs. | Round-trip tests; `python -m pytest`. | Covered | V1 persists one session, image id, nullable source URI, pipeline, and empty settings object. |
| P07-FEATURE-001 | Features | Define a JSON-like project file contract with required and optional fields. | `schema.py`; `project-file-contract.md`; ADR-0005. | Fixture tests and validation tests. | Covered | Required fields are explicit; unknown fields rejected. |
| P07-FEATURE-002 | Features | Serialize and deserialize project state through a persistence adapter. | `ProjectFileStorage.save_session_snapshot`; `ProjectFileStorage.load_session_snapshot`. | Round-trip and valid fixture tests. | Covered | Implements existing `ProjectStoragePort` shape. |
| P07-FEATURE-003 | Features | Validate malformed, missing, unknown, duplicate, and incompatible fields with source context. | `validate_project_document`; mapper validation; adapter exceptions. | Validation tests for missing, unknown, duplicate image/pipeline/step ids, malformed values, invalid JSON, incompatible version. | Covered | Errors include safe project-file and field context. |
| P07-FEATURE-004 | Features | Add compatibility and round-trip tests. | Fixture files and persistence tests. | `test_project_file_round_trip.py`; `test_project_file_validation.py`. | Covered | Version 1 accepted; version 2 rejected. |
| P07-CONSTRAINT-001 | Constraints | Do not expose domain internals as the wire format by accident. | Adapter DTO/schema/mapping code is separate from domain/application models. | Architecture tests in full pytest; source review. | Covered | Wire shape uses explicit JSON contract, not dataclass serialization. |
| P07-CONSTRAINT-002 | Constraints | Do not add database persistence unless an ADR explicitly changes the accepted strategy. | No database dependency or persistence backend added. | Source review; `pyproject.toml` unchanged. | Covered | JSON file adapter only. |
| P07-CONSTRAINT-003 | Constraints | Do not store secrets or AI credentials in project files. | `settings` must be empty; secret-like unknown fields rejected; serialization has no secret fields. | Secret serialization and secret-like settings tests. | Covered | Runtime secrets remain out of scope. |
| P07-CONSTRAINT-004 | Constraints | Do not add UI save/load flows in this phase. | No UI, CLI, REST, or bootstrap files changed. | Source review; changed file list. | Covered | Adapter only. |
| P07-SCOPE-001 | Scope | Persistence DTOs and explicit mappers. | `schema.py`; `project_mapper.py`. | Mypy; validation tests. | Covered | Mapper constructs domain/application types only after shape validation. |
| P07-SCOPE-002 | Scope | Project file schema documentation. | `docs/architecture/project-file-contract.md`. | Source review; coverage review. | Covered | Documents schema, versioning, compatibility, limitations. |
| P07-SCOPE-003 | Scope | Application project storage port implementation. | `ProjectFileStorage` implements `save_session_snapshot` and `load_session_snapshot`. | Round-trip tests; mypy. | Covered | Uses configured project-file path. |
| P07-SCOPE-004 | Scope | Contract tests and fixture files. | `tests/adapters/persistence/*`; `tests/fixtures/projects/*`. | `python -m pytest`. | Covered | Valid and invalid fixtures included. |
| P07-OOS-001 | Out of Scope | Desktop UI integration. | No UI files changed. | Source review. | Explicitly out of scope | Not implemented. |
| P07-OOS-002 | Out of Scope | REST endpoints for project files. | No REST/API files changed. | Source review. | Explicitly out of scope | Not implemented. |
| P07-OOS-003 | Out of Scope | Plugin package persistence beyond storing accepted operation identifiers and parameters. | No plugin modules or package persistence added. | Source review. | Explicitly out of scope | Pipeline operation ids/parameters are persisted; plugin packages are not. |
| P07-OOS-004 | Out of Scope | Runtime secrets storage. | Settings object must be empty and secret-like keys rejected. | Secret-related tests. | Explicitly out of scope | Not implemented. |
| P07-ARCH-001 | Architecture Notes | Project files are external data contracts; persistence DTOs belong in adapters; mapping must be explicit before constructing application/domain models. | `adapters/persistence` package; no domain/application persistence DTO additions. | Architecture tests; mypy; source review. | Covered | Dependency direction preserved. |
| P07-ARTIFACT-001 | Artifacts | `src/image_workbench/adapters/persistence/__init__.py` | File added. | Import tests; package import. | Covered | Exports adapter API. |
| P07-ARTIFACT-002 | Artifacts | `src/image_workbench/adapters/persistence/project_file.py` | File added. | Round-trip tests. | Covered | Filesystem JSON storage adapter. |
| P07-ARTIFACT-003 | Artifacts | `src/image_workbench/adapters/persistence/project_mapper.py` | File added. | Round-trip and validation tests. | Covered | Explicit DTO-to-model mapper. |
| P07-ARTIFACT-004 | Artifacts | `src/image_workbench/adapters/persistence/schema.py` | File added. | Validation tests. | Covered | Schema constants, exceptions, shape validation. |
| P07-ARTIFACT-005 | Artifacts | `docs/architecture/project-file-contract.md` | File added. | Source review. | Covered | Contract documentation. |
| P07-ARTIFACT-006 | Artifacts | `tests/adapters/persistence/test_project_file_round_trip.py` | File added. | `python -m pytest`. | Covered | Save/load and deterministic serialization tests. |
| P07-ARTIFACT-007 | Artifacts | `tests/adapters/persistence/test_project_file_validation.py` | File added. | `python -m pytest`. | Covered | Contract validation tests. |
| P07-ARTIFACT-008 | Artifacts | `tests/fixtures/projects/` | Fixtures added. | Fixture load/invalid tests. | Covered | Valid v1 and invalid samples. |
| P07-ARTIFACT-009 | Artifacts | `workflow/plans/07_project_persistence_contract_plan.md` | Plan added. | Source review. | Covered | Includes rationale and trade-offs. |
| P07-ARTIFACT-010 | Artifacts | `workflow/logs/phase-07-implementation-log.md` | Log added and updated. | Log entries for context, decisions, actions, verification. | Covered | Status updated before closeout. |
| P07-TEST-001 | Testing | Round-trip tests for saving and loading representative project files. | `test_project_file_storage_round_trips_session_snapshot`; valid fixture test; source URI session-service regression tests. | `python -m pytest`: 94 passed. | Covered | Restores equivalent snapshot with runtime undo/redo flags reset and source URI preserved when present. |
| P07-TEST-002 | Testing | Contract tests for missing required fields, unknown fields, duplicate identifiers, malformed values, ordering, and version handling. | Validation test module. | `python -m pytest`: 94 passed. | Covered | Includes duplicate image, pipeline, and step ids. |
| P07-TEST-003 | Testing | Tests verify secrets are not serialized. | Secret serialization and secret-like settings tests. | `python -m pytest`: 94 passed. | Covered | Settings keys are rejected in v1. |
| P07-AC-001 | Acceptance Criteria | Saving and loading a project restores equivalent pipeline, image references, and settings with deterministic ordering. | Adapter persists image id, loaded source URI, dimensions, pipeline, and empty settings; deterministic JSON ordering. | Round-trip, source URI regression, and deterministic serialization tests. | Covered | `source_uri` remains nullable only when no source reference has been loaded yet. |
| P07-AC-002 | Acceptance Criteria | Invalid project files fail with safe source-context diagnostics. | `ProjectFileValidationError`; JSON decode and field validation messages. | Invalid JSON/missing/unknown/version/duplicate/malformed tests. | Covered | Diagnostics cite file and field path; no payload dumps. |
| P07-AC-003 | Acceptance Criteria | Project-file DTOs remain inside adapter code. | DTO/schema/mapping files are under `adapters/persistence`; core layers unchanged. | Architecture tests and source review. | Covered | No adapter imports from application/domain. |
| P07-AC-004 | Acceptance Criteria | `docs/architecture/project-file-contract.md` documents schema, versioning, compatibility, and known limitations. | Contract documentation file. | Source review. | Covered | Includes V1 schema, validation rules, compatibility, limitations. |
| P07-ADR-001 | ADR Follow-Up | ADR required for accepted project persistence schema, versioning, compatibility, and migration policy. | `docs/adr/0005-project-file-schema-versioning.md`. | ADR/source review. | Covered | ADR accepted. ADR helper validation could not be executed due repeated shell spawn errors. |
| P07-ADR-002 | Decision Log | Decision log required for fixture and contract-test maintenance convention. | `workflow/CLI.decision-log.md` entry dated 2026-05-28. | Source review. | Covered | Fixture and test maintenance convention recorded. |

## Review Findings

- Review remediation 2026-05-28: source image references were previously serialized as `null`; fixed by adding `SessionSnapshot.source_uri`, persisting loaded references, and restoring `source_uri` from v1 project files.
