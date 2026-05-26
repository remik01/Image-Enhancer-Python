# Exceptions Instructions

Exception handling must preserve diagnostics, protect invariants, and make failures actionable without hiding root causes or leaking sensitive data.

## Must Do

- Throw specific exception types for meaningful failure categories.
- Preserve the original cause when wrapping technical failures.
- Include safe diagnostic context: operation, identifier, file path, row, field, external system, or status code as relevant.
- Translate technical exceptions at boundaries into domain/application/adapter exceptions appropriate to the layer.
- Restore interrupt status when catching `InterruptedException`.
- Keep transactional and partial-failure behavior explicit.
- Prefer validation results only when callers are expected to recover from multiple user-correctable problems.

## Must Not Do

- Do not catch `Exception` broadly unless at an outer boundary with clear translation/logging.
- Do not swallow exceptions or return misleading defaults.
- Do not throw raw `RuntimeException` for known failure modes.
- Do not expose low-level technical exceptions through stable application contracts unless intentionally documented.
- Do not log and rethrow at multiple layers without adding value.
- Do not leak secrets, tokens, passwords, or sensitive payloads in messages.
- Do not suppress warnings or failures to make tests pass.

## Layer Rules

- Domain exceptions describe invariant or policy violations.
- Application exceptions describe use-case failure or failed dependency capabilities.
- Adapter exceptions describe technical integration failures and should be translated before crossing stable boundaries.
- UI/CLI should render useful messages and keep detailed diagnostics in logs when appropriate.
- Bootstrap exceptions should fail startup clearly when configuration or wiring is invalid.

## Naming

- Use names that describe the failure: `InvalidIssueIdException`, `ReportExportException`, `ExternalIssueProviderException`.
- Avoid vague names such as `ServiceException`, `ProcessingException`, or `CommonException` unless the repository has an established convention.

## Tests

Provide tests for:

- invalid input failures,
- wrapped causes,
- context in messages,
- boundary translation,
- interruption handling where relevant,
- no secret leakage,
- partial-failure behavior.

## ADR Triggers

Propose ADR discussion for changes to exception hierarchy, error-result strategy, retry/fallback behavior, transactional failure semantics, or public API error contracts.

## Checklist

- Is the failure category specific?
- Is the cause preserved?
- Is context useful and safe?
- Is translation done at the correct boundary?
- Are callers given a contract they can act on?
