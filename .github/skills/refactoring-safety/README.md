# Refactoring Safety

## Reason

Refactoring should improve maintainability without changing behavior unexpectedly. This skill keeps Python refactors small, test-backed, typed where appropriate, and aligned with architecture ownership.

## Functionality

- Classifies refactoring risk.
- Identifies public APIs, callers, tests, and architecture constraints.
- Guides characterization tests for risky changes.
- Separates behavior changes from structural cleanup.
- Escalates ADR discussion for boundary or dependency direction changes.

## Proper Use Cases

Use this skill for package or module moves, class extraction, function or method extraction, naming cleanup, duplication reduction, dependency simplification, and preparation for later features.

Do not use it to smuggle in new behavior, weaken tests, or create speculative abstractions.

## Best Practices

- Define the refactoring goal before editing.
- Add characterization tests before medium/high-risk changes.
- Run focused tests first, then broader verification when needed.
- Report behavior-preservation evidence.
