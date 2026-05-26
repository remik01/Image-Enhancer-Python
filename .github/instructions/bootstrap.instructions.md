# Bootstrap And Configuration Instructions

Bootstrap assembles runtime dependencies and validates startup configuration. It should not contain business logic.

## Must Do

- Keep dependency wiring explicit.
- Validate required configuration at startup.
- Keep configuration objects typed and meaningful.
- Separate environment concerns from domain/application logic.
- Fail fast with clear startup errors when configuration is invalid.
- Avoid logging secrets while still reporting useful configuration source context.

## Must Not Do

- Do not put use-case orchestration in bootstrap.
- Do not hide dependencies behind global static state.
- Do not perform business validation in configuration classes.
- Do not silently apply risky defaults for required runtime settings.

## Tests

Test invalid configuration, missing required values, and expected wiring where configuration behavior is meaningful.

## ADR Triggers

Propose ADR discussion for new runtime assembly patterns, dependency injection framework changes, configuration source strategy, profile strategy, or startup lifecycle changes.

## Checklist

- Are dependencies wired at the edge?
- Are required settings validated?
- Are secrets protected?
- Is bootstrap free from business logic?
