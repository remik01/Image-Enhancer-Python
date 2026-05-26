# Domain Instructions

The domain layer represents business concepts and protects invariants. It must remain independent from frameworks, adapters, UI, persistence, and external data contracts.

## Must Do

- Model business concepts with meaningful types.
- Enforce invariants at construction and mutation boundaries.
- Fail fast on invalid domain state.
- Prefer immutable values and deterministic behavior.
- Use domain services or policies for business rules that do not naturally belong to one entity/value object.
- Keep names aligned with the project language and specifications.
- Document non-obvious invariants and intentional limitations.

## Must Not Do

- Do not import web frameworks, UI toolkits, HTTP clients, XML/JSON/Excel adapters, persistence libraries, logging framework APIs, or adapter DTOs.
- Do not use domain objects as generic DTOs for convenience.
- Do not weaken invariants to fit an external system.
- Do not hide business rules in adapters, UI, CLI, or persistence entities.
- Do not introduce global mutable state.

## Modeling Guidance

- Prefer frozen dataclasses, typed value objects, tuples, or immutable collections for immutable value carriers with clear validation.
- Prefer classes when identity, behavior, or invariant-preserving methods matter.
- Use enums only for stable closed sets; avoid encoding unstable external statuses directly as domain truth.
- Use explicit class hierarchies or `typing.Literal` only when a closed model improves correctness.
- Use collections defensively: copy inputs and expose unmodifiable views or immutable values.
- Protect domain invariants from external mutation; never store caller-owned mutable collections or arrays as-is.
- Do not expose internal collections directly. Return immutable snapshots, or documented unmodifiable views only when later internal mutation is intentional.

## Validation

- Technical shape validation belongs at boundaries.
- Semantic validation belongs in domain/application.
- Error messages should explain the violated invariant without leaking sensitive data.
- Factories should make invalid states unrepresentable where practical.

## Tests

Provide tests for:

- valid construction,
- invalid input,
- boundary values,
- duplicate/conflict rules,
- ordering/comparison rules,
- equality semantics,
- regression cases from specifications or decisions.

Domain tests should be fast, deterministic, and independent from frameworks or external systems.

## ADR Triggers

Propose ADR discussion for new aggregate boundaries, major domain model restructuring, framework coupling in domain, shared domain patterns, or changes to invariant ownership.

## Checklist

- Is the type a real domain concept?
- Are invariants explicit and tested?
- Is the domain free from adapter/framework concerns?
- Is behavior deterministic?
- Are names aligned with project language?
