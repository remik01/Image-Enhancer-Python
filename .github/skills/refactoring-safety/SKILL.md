---
name: refactoring-safety
description: Workflow for safe Python refactoring that preserves behavior, public contracts, architecture boundaries, tests, typing, and static-analysis quality.
---

# Refactoring Safety Skill

Use this skill when Codex / Copilot needs to perform or review a refactoring.

## Purpose

Refactor safely by:
- preserving observable behavior,
- reducing complexity,
- improving structure,
- protecting architecture,
- minimizing regression risk,
- keeping changes reviewable.

Refactoring is not feature work. Keep behavior changes separate unless the user explicitly asks for both.

## When to Use

Use this skill for:
- package or module restructuring,
- class extraction,
- function or method extraction,
- naming cleanup,
- duplication reduction,
- dependency simplification,
- moving logic between layers,
- improving cohesion,
- reducing coupling,
- simplifying tests,
- preparing code for a later feature.

## Workflow

1. Identify refactoring goal:
   - readability,
   - duplication,
   - coupling,
   - package or module ownership,
   - testability,
   - static-analysis remediation,
   - architecture alignment.

2. Inspect current behavior:
   - public APIs,
   - tests,
   - callers,
   - module dependencies,
   - architecture docs,
   - ADRs.

3. Classify refactoring risk:
   - low: local rename/extract,
   - medium: class/package/module move,
   - high: boundary change/public contract change.

4. Identify safety net:
   - existing tests,
   - missing tests,
   - characterization tests,
   - static analysis,
   - Python verification.

5. Perform smallest coherent refactoring step.

6. Avoid mixing behavior changes with structural cleanup.

7. Run relevant tests.

8. Summarize behavior preservation evidence.

## Refactoring Rules

DO:
- preserve observable behavior,
- preserve public contracts unless explicitly requested,
- keep changes incremental,
- maintain deterministic behavior,
- preserve static-analysis compliance,
- keep commits/diffs reviewable,
- add characterization tests before risky changes.

DON'T:
- introduce new features,
- change semantics silently,
- introduce speculative abstractions,
- create generic frameworks,
- move business rules into adapters/UI,
- weaken tests,
- perform broad rewrites without explicit instruction.

## Architecture Boundary Checks

Before moving code, verify:
- Does the target package/layer own this responsibility?
- Does dependency direction remain correct?
- Are domain invariants still protected?
- Are adapter details kept outside core?
- Does the move require ADR discussion?

## Testing Strategy

For low-risk refactoring:
- run existing focused tests.

For medium/high-risk refactoring:
- add characterization tests first,
- run module tests,
- run static analysis if touched code is sensitive,
- consider broader Python verification.

## ADR Escalation

Recommend ADR discussion when refactoring:
- changes module boundaries,
- changes dependency direction,
- changes public contracts,
- creates reusable architectural patterns,
- redefines ownership of responsibilities,
- intentionally violates previous architecture guidance.

## Output Format

When finished, provide:

1. Refactoring Goal
2. Behavior Preservation
3. Changed Files
4. Verification
5. Risks
6. Follow-Up

## Non-Goals

Do not:
- implement unrelated features,
- redesign architecture broadly,
- introduce dependencies,
- hide behavior changes,
- claim safety without tests or inspection.

## Final Rule

A good refactoring should make the next change safer.
If it makes ownership or behavior less explicit, reassess the change.
