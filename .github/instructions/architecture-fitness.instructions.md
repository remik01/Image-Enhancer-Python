# Architecture Fitness Instructions

Architecture rules should be enforceable where practical. Prose guidance is useful, but tests and checks prevent drift.

## Must Do

- Look for existing boundary tests, dependency checks, build rules, and static-analysis configuration before proposing new enforcement.
- Prefer automated fitness checks for dependency direction, forbidden imports, package cycles, and public contract stability.
- Keep checks narrow enough to avoid blocking legitimate local changes.
- Document what a check protects and what it deliberately does not protect.
- Include verification commands when adding or changing fitness checks.

## Must Not Do

- Do not rely only on comments for important architecture boundaries when a simple check is practical.
- Do not add broad brittle checks that encode incidental package names unnecessarily.
- Do not weaken architecture checks to make a feature easier.
- Do not introduce new tooling without explaining maintenance cost.

## Examples Of Useful Checks

- forbidden imports from domain/application,
- adapter-only dependencies on external DTO packages,
- package cycle detection,
- module dependency constraints,
- static-analysis rules for security-sensitive code,
- contract/golden-file tests for stable exports.

## Python Architecture Fitness Guidance

Use Python architecture fitness checks when the project has meaningful package or module boundaries that should not drift silently.

Prefer simple, reviewable checks for:

- dependency direction between layers or modules,
- forbidden dependencies from domain/application into adapters, UI, bootstrap, frameworks, persistence, HTTP, or external DTOs,
- adapter separation rules,
- bootstrap/configuration isolation,
- package cycle detection,
- enforcement of accepted ADR boundary decisions.

Architecture fitness checks must:

- live in test scope only,
- run as part of the normal test or CI suite unless an ADR accepts a different gate,
- encode documented architecture, not aspirational architecture,
- include a short comment or assertion message explaining what the rule protects,
- stay narrow enough to avoid blocking legitimate local changes,
- exclude test code unless the rule is intentionally about tests,
- avoid generated code and incidental package details where possible.

Do not use architecture fitness checks to:

- replace behavior tests,
- enforce personal style preferences,
- freeze temporary package names,
- hide unclear architecture decisions behind failing tests,
- force refactors that are not backed by `AGENTS.md`, ADRs, phase files, or explicit specs.

Add or update ADR discussion before:

- adopting a new project-wide architecture-check tool,
- changing dependency direction,
- enforcing a new repository-wide architecture policy,
- wiring architecture checks into CI beyond the existing test lifecycle,
- adding broad rules that affect multiple teams or modules.

## ADR Triggers

Propose ADR discussion for new architecture-check tooling, repository-wide enforcement policy, module layout changes, or build pipeline changes.
