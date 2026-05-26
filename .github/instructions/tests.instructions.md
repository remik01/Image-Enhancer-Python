# Test Instructions

Tests should prove behavior, protect invariants, and make regressions cheap to detect.

## Must Do

- Test meaningful behavior, not implementation trivia.
- Cover happy paths, invalid input, boundary cases, duplicates/conflicts, ordering, and regressions.
- Keep tests deterministic and independent from execution order.
- Prefer fast unit tests for domain/application behavior.
- Use fakes or local test doubles for external systems.
- Use framework integration tests only when wiring/framework behavior matters.
- Keep test names specific about scenario and expected outcome.

## Must Not Do

- Do not weaken assertions to make tests pass.
- Do not remove meaningful tests without justification.
- Do not introduce flaky tests.
- Do not depend on production systems, live credentials, VPN, or unstable networks.
- Do not hide failures behind retries.
- Do not treat coverage percentage as proof of quality.

## File / Contract Tests

For XML, JSON, Excel, imports, exports, and APIs, use realistic samples and verify malformed input, missing fields, ordering, and source-context diagnostics.

## Architecture Tests

Architecture tests and import-boundary checks are regression tests for structural decisions. They complement unit, integration, and contract tests; they do not prove behavior is correct.

When architecture tests fail, fix the boundary violation or revisit the governing ADR/spec. Do not weaken the rule just to make feature work easier.

## Checklist

- Does the test fail for the intended regression?
- Is the scenario name clear?
- Is setup minimal and readable?
- Are external dependencies isolated?
- Are edge cases covered?
