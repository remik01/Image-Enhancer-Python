# Mapping Instructions

Mappings are anti-corruption boundaries. They make transformation explicit, reviewable, and predictable.

## Must Do

- Map field by field.
- Preserve source context for failures.
- Validate technical shape before creating internal models.
- Delegate semantic validation to domain/application types.
- Keep mappings deterministic and side-effect free.
- Use names that identify source/target or format.

## Must Not Do

- Do not use reflection-based magic unless an ADR allows it.
- Do not silently default missing required values.
- Do not pass external DTOs into domain/application logic.
- Do not duplicate business rules in mappers.

## Tests

Test happy paths, missing fields, malformed values, duplicates/conflicts, ordering, and source-context diagnostics.

## Checklist

- Is the transformation explicit?
- Is source context preserved?
- Are external and internal models separated?
- Are edge cases tested?
