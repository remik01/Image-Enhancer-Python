# AI Prompt To Pipeline

## Goal

Implement AI-assisted natural-language prompt interpretation as structured, reviewable pipeline proposals that remain separate from deterministic local execution.

## Tickets

* IEP-009

## Features to implement

* Structured-output schema for prompt-to-pipeline proposals.
* OpenAI adapter behind the application AI interpretation port.
* Mapper from AI DTOs to internal pipeline proposal commands.
* Validation that unsupported or unsafe proposed operations are rejected before execution.
* Tests with local fakes and recorded representative structured responses.

## Constraints

* Do not execute AI-generated operations automatically.
* Do not call the live OpenAI API from automated tests.
* Do not expose API keys in code, tests, logs, errors, or project files.
* Do not allow AI DTOs into domain models.

## Scope

* AI adapter source, DTOs, mappers, prompt constraints, timeout handling, and failure translation.
* Application service changes needed to request, validate, and return proposals.
* Tests for structured-output mapping and validation.

## Out of Scope

* Desktop UI proposal editor.
* REST endpoints for AI interpretation.
* Local inference, ONNX, semantic search, OCR, or generated recipes beyond prompt-to-pipeline proposals.
* Plugin-generated AI operations unless already supported by the accepted plugin contract.

## Architecture / Boundary Notes

AI is an interpretation boundary only. Application services must treat AI output as untrusted external input until mapped and validated into internal proposal models.

## Generated / Modified Artifacts

* src/image_workbench/adapters/ai/__init__.py
* src/image_workbench/adapters/ai/openai_interpreter.py
* src/image_workbench/adapters/ai/dtos.py
* src/image_workbench/adapters/ai/mappers.py
* src/image_workbench/adapters/ai/prompts.py
* src/image_workbench/application/ai_workflows.py
* tests/adapters/ai/test_openai_interpreter_mapping.py
* tests/adapters/ai/test_ai_failure_translation.py
* tests/application/test_ai_pipeline_proposals.py
* tests/fixtures/ai/
* docs/architecture/ai-prompt-contract.md
* workflow/plans/09_ai_prompt_to_pipeline_plan.md
* workflow/logs/phase-09-implementation-log.md

## Testing Expectations

* Tests for successful structured-output mapping, missing fields, unsupported operations, invalid parameters, timeout/failure translation, and secret redaction.
* Application tests verify proposals are not executed until accepted.
* Static-analysis and architecture-fitness checks from earlier phases.

## Acceptance Criteria

* A supported prompt can produce a structured internal pipeline proposal through a fake or recorded response.
* Invalid AI output is rejected with safe diagnostics.
* No automated test requires live credentials or network access.
* Domain and application layers do not import OpenAI client DTOs.

## ADR / Decision-Log Follow-Up

* ADR: Required for accepted AI provider boundary, structured-output contract, model-selection policy, timeout policy, and fallback behavior.
* Decision log: Required for prompt fixture maintenance and live-test skip convention.

## Codex/Copilot Execution Notes

Recommended implementation profile, if available:

* Model: gpt-5.3-codex
* Reasoning: extra high

If unavailable, use the strongest available coding model with high reasoning. Do not treat model availability as an acceptance criterion. Record the actual model/profile used when implementing the phase if the execution environment exposes that information.

Before implementation:

* Read `AGENTS.md`.
* Read this phase file.
* Check existing `docs/adr/`, `workflow/*.decision-log.md`, `workflow/plans/`, and relevant source code.
* Create or update a persisted plan under `workflow/plans/` if implementation touches multiple files or modules.
* Include a `## Rationale` section in persisted plans as required by `.github/instructions/planningPersistence.instructions.md`.
* Include a `## Trade-offs & Limitations` section in persisted plans as required by `.github/instructions/planningPersistence.instructions.md`.
* Do not implement out-of-scope items.
* Do not bypass architecture boundaries.

During implementation:

* Keep changes focused on this phase.
* Create or modify only the artifacts listed in `Generated / Modified Artifacts`, unless a newly discovered prerequisite is first recorded in the persisted plan or decision log.
* Add or update tests with the implementation.
* Record meaningful decisions in the decision log.
* Propose ADR discussion for architectural impact.

After implementation:

* Read `.github/instructions/static-analysis.instructions.md`.
* Run relevant static-analysis and verification checks for the changed modules.
* Fix static-analysis findings by addressing root causes rather than weakening rules or adding broad suppressions.
* Report remaining static-analysis findings, suppressions, skipped checks, or required governance follow-up.

Before committing phase work or review-remediation work for this phase:

* Use commit message format: `YYYY.MM.DD <login-name> <ticket-1> <ticket-2> ... <phase-title>: <commit-description>`.
* Use the current OS login name for `<login-name>` at commit time.
* Read tickets from this phase file's `## Tickets` section.
* Use this phase file's H1 title as `<phase-title>`.
* If this phase has no tickets, stop and correct the phase file before committing.

Before completion:

* Run relevant verification commands.
* Report changed files.
* Confirm that every referenced config file, workflow, script, module, and documentation artifact exists or is explicitly documented as external/local-only.
* Report tests executed.
* Report known weak points.

