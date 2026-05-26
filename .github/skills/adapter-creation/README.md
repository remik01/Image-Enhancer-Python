# Adapter Creation

## Reason

Adapters are the boundary between external systems and the Image Manipulator core. This skill keeps HTTP, file, image-codec, persistence, UI, and other technical concerns out of domain and application code.

## Functionality

- Identifies the application port an adapter should implement.
- Defines external DTOs and explicit mapping responsibilities.
- Guides error handling, configuration, and diagnostics.
- Requires focused mapper, malformed-input, fixture, and port-contract tests.
- Flags ADR candidates for integration strategy, transport, retries, security, or runtime assumptions.

## Proper Use Cases

Use this skill for REST adapters, image-processing adapters, file import/export, HTTP clients, repositories, message consumers, and any boundary translation code.

Do not use it to invent domain rules, push adapter DTOs into application contracts, or hide workflow orchestration inside infrastructure.

## Best Practices

- Start from an application port; propose one if it does not exist.
- Keep external DTOs in adapter packages.
- Preserve safe source context in errors without logging secrets or image payloads.
- Add tests at the mapper and adapter boundary before wiring into bootstrap.
