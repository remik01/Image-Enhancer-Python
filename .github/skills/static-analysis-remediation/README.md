# Static Analysis Remediation

## Reason

Static-analysis failures often point to real defects or architecture risks. This skill fixes the cause rather than muting the tool.

## Functionality

- Classifies ruff, mypy, pyright, Bandit, pip-audit, CodeQL, formatting, dependency, and Python quality-gate failures.
- Identifies root cause and related code ownership.
- Prefers small code fixes over broad suppressions.
- Defines suppression rules when no reasonable code fix exists.
- Requires verification after fixes.

## Proper Use Cases

Use this skill for local static-analysis failures, CI quality-gate failures, type-checker diagnostics, dependency issues, and formatting checks.

Do not use it to weaken rules, delete tests, hide warnings, or make broad unrelated cleanup.

## Best Practices

- Start from exact tool output and rule id.
- Treat security findings as high-priority until proven otherwise.
- Keep suppressions narrow and justified.
- Run the most relevant Python verification command after fixing.
