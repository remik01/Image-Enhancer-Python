---
name: static-analysis-remediation
description: "[Python] Workflow for analyzing and fixing ruff, type-checker, Bandit, pip-audit, CodeQL, dependency, formatting, and Python quality-gate issues while preserving architecture and behavior."
---

# Static Analysis Remediation Skill

Use this skill when Codex / Copilot needs to investigate or fix static-analysis, build-quality, type-checking, formatting, dependency, or Python verification failures.

## Governing Instructions

This skill operationalizes `.github/instructions/static-analysis.instructions.md`.
When remediation involves severity classification, suppressions, baselines, rule configuration, or tracked exceptions, follow that instruction file as the policy source.

For non-trivial findings:

- classify severity as Critical/High, Medium/Important, or Low/Cosmetic,
- explain production impact,
- choose fix, justified suppression, or tracked future work before editing,
- avoid autonomous suppression, baseline growth, or rule weakening without explicit review.

## Purpose

Remediate static-analysis issues safely by:

- understanding the warning,
- identifying the real risk,
- applying the smallest correct fix,
- preserving behavior,
- preserving architecture,
- avoiding casual suppressions.

## Workflow

1. Inspect the exact failure output:
   - tool,
   - rule id,
   - file,
   - line,
   - message,
   - stack trace if present.

2. Inspect affected code and nearby context:
   - production code,
   - tests,
   - package/module conventions,
   - architecture layer,
   - related documentation.

3. Classify the warning:
   - severity: Critical/High, Medium/Important, or Low/Cosmetic,
   - nature: real defect, maintainability risk, security risk, false positive, generated-code issue, tool/configuration mismatch, or dependency/version problem,
   - production impact.

4. Prefer the smallest safe code fix.

5. Avoid broad refactoring unless the warning reveals structural risk.

6. Add or update tests if behavior is affected.

7. Run the narrowest useful verification command first.

8. Prefer the CI gate command from `.github/workflows/*`, `pyproject.toml`, tox/nox config, or project documentation. Do not treat report generation as a quality gate.

9. Report what changed and what remains unverified.

## Fixing Priorities

Prefer fixes that:

- make code safer,
- preserve behavior,
- improve explicitness,
- reduce ambiguity,
- satisfy the tool without weakening rules.

Avoid:

- suppressing warnings casually,
- changing static-analysis configuration to hide issues,
- deleting tests,
- weakening assertions,
- broad unrelated cleanup,
- turning meaningful failures into ignored logs.

## Common Python Static-Analysis Patterns

Check for:

- mutable internal state exposure,
- optional/`None` ambiguity,
- ignored return values,
- dead stores,
- unused variables,
- inconsistent equality/hash behavior,
- resource leaks,
- unsafe deserialization,
- questionable synchronization,
- inefficient repeated operations.

Preferred remedies:

- defensive copies,
- immutable collections or frozen dataclasses,
- constructor or factory validation,
- context managers,
- explicit optional handling,
- narrower scope,
- better ownership boundaries.

## Common Security Patterns

Check for:

- path traversal,
- hardcoded credentials,
- unsafe deserialization,
- SQL injection,
- command injection,
- weak cryptography,
- logging secrets,
- unsafe temporary files.

Preferred remedies:

- validate external input,
- normalize and constrain paths,
- remove secrets,
- parameterize queries,
- avoid shell execution,
- preserve security context in errors,
- avoid logging sensitive values.

## Suppression Rules

Suppress only when:

- the warning is understood,
- the risk is evaluated,
- no reasonable code fix exists,
- the suppression is narrow,
- the justification is documented.

Suppression comments must explain:

- why the warning is safe,
- why the suppression is necessary,
- what alternative was rejected.

Never suppress simply to pass CI.

## Verification Commands

Use the most relevant command first:

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy .
python -m pyright
python -m pip check
```

Use only commands configured or appropriate for the repository. Report-only scanner commands are not proof that a gate passed unless the report is inspected and confirmed clean or below the accepted threshold.

If verification cannot run:

- state why,
- do not claim success,
- provide the exact command the user should run.

## Output Format

When finished, provide:

1. Issue Classification
2. Root Cause
3. Fix Applied or Recommended
4. Changed Files
5. Verification
6. Remaining Risks

## Non-Goals

Do not:

- weaken static-analysis config without explicit instruction,
- introduce broad architecture changes,
- hide warnings,
- convert defects into suppressions,
- claim a clean build without running verification.

## Final Rule

Make the code correct first, quiet second.
A silent static-analysis report is worthless if the code became subtly worse to achieve it.
