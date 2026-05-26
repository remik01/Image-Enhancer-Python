# Static Analysis Instructions

Static analysis detects defect patterns and architectural risks.
A clean report is not proof of correctness.
A silent report achieved through suppression abuse is considered a process failure.

## Primary Goal

The goal is not merely to obtain a green build.

The goal is to:
- reduce production risk,
- preserve maintainability,
- make findings understandable,
- keep warnings actionable and trusted by developers.

## Required Workflow

For non-trivial findings:

1. Understand the warning.
2. Classify severity:
    - Critical or High
    - Medium or Important
    - Low or Cosmetic
3. Explain production impact.
4. Decide:
    - fix,
    - suppress with justification,
    - leave visible as tracked future work.
5. Only then modify code or configuration.

Do not mechanically suppress warnings to satisfy the build.

## Must Do

- Treat ruff, type-checker diagnostics, security/dependency scanners, interpreter warnings, and configured checks as meaningful.
- Fix root causes instead of suppressing warnings whenever reasonable.
- Preserve architectural boundaries and ownership semantics while fixing findings.
- Re-run relevant checks after remediation.
- Summarize fixes and any behavioral impact.
- Keep static-analysis output actionable and trusted.

## Python Gate Verification

Do not treat report generation as proof that a static-analysis gate passed. A gate must fail when actionable findings are present, or the generated report must be inspected before claiming success.

When validating Python static-analysis remediation:

1. Prefer the exact command used by CI, discovered from `.github/workflows/*`, `pyproject.toml`, tox/nox config, or project documentation.
2. If the CI command is not available, run the configured ruff and type-checker commands.
3. If only a report command can be run, inspect the report before reporting success.

Never report a scanner or type checker as passed from report generation alone unless the report was inspected and confirmed empty or below the accepted threshold.

## Suppression Rules

Suppressions are exceptions, not cleanup tools.

Every suppression must:
- be narrow in scope,
- include a precise justification,
- explain why the risk is acceptable,
- avoid hiding unrelated findings.

Prefer:
- local suppression,
- narrow filters,
- documented exceptions.

Avoid:
- package-wide or project-wide suppression,
- global exclusions,
- disabling rules,
- weakening plugin configuration,
- baseline growth without review.

Do not allow autonomous suppression decisions without human review.

## Baseline And Severity Policy

- Do not grow baselines silently.
- Keep baseline and filter changes narrow and documented.
- Link analysis exceptions to:
    - ADRs,
    - decision log,
    - ticket,
    - exception register,
      where applicable.

Severity expectations:

- Critical or High findings:
    - treated as build-blocking unless explicitly accepted.
- Medium or Important findings:
    - normally fixed before merge or tracked with explicit rationale.
- Low or Cosmetic findings:
    - may remain visible if cleanup cost exceeds value.

## Must Not Do

- Do not hide failing checks.
- Do not optimize for "green build" over correctness.
- Do not weaken rules casually.
- Do not suppress warnings globally for local issues.
- Do not change behavior merely to silence analysis.
- Do not reduce readability for micro-optimizations without evidence.
- Do not treat static-analysis success as a substitute for tests or review.

## Common Focus Areas

Prioritize findings related to:
- null handling,
- resource management,
- path traversal,
- unsafe deserialization,
- ignored return values,
- concurrency hazards,
- collection sizing,
- repeated parsing,
- exception swallowing,
- secret exposure,
- external input validation at adapter boundaries,
- hardened XML parsing,
- normalized file paths,
- sensitive data in logs,
- missing HTTP timeouts,
- disabled TLS verification.

## Review Checklist

Before closing findings:

- Is the warning understood?
- Was severity classified?
- Was production risk explained?
- Is the fix behavior-preserving?
- Is suppression avoided or justified?
- Is the suppression narrow?
- Were architectural boundaries preserved?
- Were relevant checks executed?
- Would another developer still trust the report?

## AI Collaboration Rules

AI assistance is expected to support analysis and remediation.

AI must not:
- suppress findings autonomously,
- weaken analysis configuration,
- expand baselines silently,
- hide warnings without explicit justification.

AI should:
- explain findings,
- propose risk-based prioritization,
- suggest fixes with rationale,
- highlight behavioral or architectural consequences.
