# Overview Creator

## Reason

The project overview is the durable bridge between an early product idea and implementation phases. This skill turns rough intent into `workflow/docs/overview.spec.md` without pretending unknowns are decided.

## Functionality

- Reads an inline description, source file, or shared ChatGPT link.
- Produces the canonical overview structure.
- Separates confirmed facts from inferred assumptions.
- Preserves missing information with `<TO BE FILLED !!!>`.
- Validates the overview structure with a helper script.

## Proper Use Cases

Use this skill before phase generation or when the product description changes enough to affect scope, architecture, runtime, UI/API, or governance assumptions.

Do not use it to implement code, create phases, or finalize ADR-sized choices silently.

## Best Practices

- Keep infrastructure assumptions conservative.
- Mark unresolved storage, security, limits, deployment, and compatibility topics explicitly.
- Run `python .github\skills\overview-creator\scripts\validate_overview.py --overview workflow\docs\overview.spec.md`.
