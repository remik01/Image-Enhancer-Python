---
name: python-verification
description: Workflow for running, interpreting, and reporting Python validation commands including pytest, ruff, formatting checks, type checking, packaging/import checks, and CI-like checks in Python projects.
---

# Python Verification Skill

Use this skill when Codex / Copilot needs to validate a Python project, interpret Python test or quality-gate failures, or prepare a reliable verification summary.

## Purpose

Provide reproducible Python verification by:

- selecting the right commands,
- running checks in sensible order,
- interpreting failures,
- avoiding false confidence,
- reporting verification status clearly.

## Workflow

1. Inspect project structure:
   - `pyproject.toml`,
   - package layout under a src directory or repository root,
   - pytest, ruff, mypy, pyright, tox, nox, uv, poetry, or hatch configuration,
   - existing CI workflow,
   - README build/test instructions if present.

2. Determine appropriate command scope:
   - whole project,
   - selected package/module,
   - selected test file or test node,
   - static analysis only,
   - type checking only,
   - packaging/import checks only.

3. Run the narrowest meaningful command first.

4. If it fails:
   - read the first meaningful failure,
   - distinguish root cause from cascading failures,
   - inspect relevant files,
   - fix only related problems if asked to fix,
   - rerun the relevant command.

5. Escalate to broader verification only after narrow checks pass.

6. Summarize verification honestly.

## Recommended Command Order

Prefer repository-documented commands. If no project command exists, use the narrowest applicable command from this set:

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy .
python -m pyright
python -m pip check
python -m build --sdist --wheel
```

For a single test file or test node:

```bash
python -m pytest tests/test_example.py
python -m pytest tests/test_example.py::test_behavior
```

For projects using tox, nox, uv, poetry, hatch, or a repository script, prefer the configured command after confirming it exists.

Do not report a report-only scanner as passed unless the generated report was inspected and confirmed clean or below the accepted threshold.

## Failure Classification

Classify failures as:

- import/package discovery failure,
- unit test failure,
- integration test failure,
- lint failure,
- formatting failure,
- type-checking failure,
- dependency resolution failure,
- packaging/build failure,
- environment/configuration issue,
- CI-only problem,
- unrelated existing failure.

## Reporting Rules

Always state:

- command run,
- whether each command was a gate that fails on findings or a report that may only generate output,
- working directory,
- result,
- relevant failure summary,
- whether failures appear related to the change,
- what remains unverified.

Never claim:

- "build passed",
- "tests passed",
- "verified",

unless the command was actually run and passed.

## Fixing Rules

When fixing failures:

- fix the root cause, not symptoms,
- avoid broad unrelated cleanup,
- preserve behavior,
- do not weaken tests,
- do not delete checks,
- do not change tool configuration without justification.

## Output Format

Provide:

1. Verification Scope
2. Commands Run
3. Failure Analysis
4. Fixes Applied
5. Remaining Work
6. Confidence Level

## Non-Goals

Do not:

- change project architecture,
- update dependency versions casually,
- alter CI configuration unless explicitly asked,
- hide failing tests,
- claim results from commands not run.

## Final Rule

Verification is evidence.
No command run means no verified claim.
