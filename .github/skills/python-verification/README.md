# Python Verification

Python verification output is evidence for Python changes. This skill keeps validation scoped, reproducible, and honest across tests, linting, formatting, typing, packaging, and CI-like checks.

## Use Cases

- Validate a focused Python code change.
- Interpret pytest, ruff, type-checker, packaging, or CI failures.
- Decide which checks are enough before handoff.
- Report skipped checks without overstating confidence.

## Defaults

- Prefer repository-documented commands.
- Run focused pytest commands before broad suites.
- Use ruff and type checking where configured.
- Do not claim report-only scanner output as a passed gate without inspection.
