# Data Contract Instructions

Data contracts include APIs, DTOs, schemas, imports, exports, reports, files, and persisted wire formats.

## Must Do

- Keep external DTOs separate from domain/application models.
- Map contracts explicitly at boundaries.
- Preserve backward compatibility unless a breaking change is explicitly accepted.
- Define required vs optional fields clearly.
- Keep ordering deterministic for exports and reports.
- Preserve source context for import errors.
- Use contract tests, sample files, or golden outputs for stable external formats.

## Must Not Do

- Do not silently change wire shape, column names, field names, status values, or ordering.
- Do not default missing required fields without explicit policy.
- Do not expose internal domain structure as an external contract by accident.
- Do not mix version migration with unrelated feature work.

## Versioning And Migration

- Identify whether a contract is public, internal, generated, or temporary.
- Document compatibility expectations.
- Add migration or fallback behavior only when required by a real compatibility need.
- Keep old and new contract handling explicit and tested.

## Tests

Test happy paths, missing fields, unknown fields, malformed values, duplicate identifiers, ordering, round-trip behavior where relevant, and regression samples.

## ADR Triggers

Propose ADR discussion for public contract changes, schema versioning policy, new serialization formats, migration strategy, or compatibility-breaking changes.
