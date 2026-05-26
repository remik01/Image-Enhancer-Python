# Module Boundary Instructions

Module and package boundaries protect dependency direction and keep the system replaceable.

## Allowed Direction

- Domain depends on nothing project-specific outside domain.
- Application may depend on domain and application-owned contracts.
- Adapters may depend on application and domain.
- UI/CLI may depend on application-facing APIs and presentation helpers.
- Bootstrap may depend on all layers only to assemble runtime wiring.

## Must Do

- Check nearby package conventions before adding types.
- Put protocols, abstract base classes, or boundary callables in the layer that owns the abstraction.
- Keep external contracts outside domain/application.
- Keep framework annotations out of domain unless an ADR explicitly allows them.
- Prefer small boundary interfaces over passing technical clients inward.
- Make dependency direction visible in package names and imports.

## Must Not Do

- Do not import adapters from application or domain.
- Do not pass persistence entities, HTTP DTOs, XML/JSON DTOs, Excel rows, UI toolkit types, or CLI parser types into core logic.
- Do not create catch-all shared modules for unrelated convenience.
- Do not move code across boundaries without preserving behavior and tests.

## Boundary Review Checks

- Which layer owns this type?
- Which layer is allowed to depend on it?
- Does the dependency point inward or outward?
- Is a port, protocol, or abstract base class needed to stabilize the boundary?
- Is mapping explicit at the crossing point?

## ADR Triggers

Propose ADR discussion for new modules, changed dependency direction, shared kernel decisions, framework coupling in core, or reusable boundary conventions.
