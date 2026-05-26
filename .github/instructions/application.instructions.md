# Application Layer Instructions

The application layer coordinates use cases. It defines ports, commands, queries, and workflow boundaries without owning domain truth or infrastructure details.

## Must Do

- Put use-case orchestration in application services.
- Define ports for external dependencies needed by use cases.
- Accept input through explicit command/query models.
- Return explicit result models where useful.
- Delegate business invariants to domain types, policies, or domain services.
- Keep workflows deterministic and reviewable.
- Use transaction boundaries deliberately when persistence is involved.
- Translate domain outcomes into application-level results without exposing adapter details.

## Must Not Do

- Do not import adapter implementations, HTTP clients, persistence entities, UI classes, CLI parser internals, XML/JSON DTOs, or UI toolkit types.
- Do not duplicate domain rules in use cases.
- Do not hide infrastructure calls behind static helpers.
- Do not let one application service become a catch-all coordinator for unrelated workflows.
- Do not expose raw technical exceptions when a meaningful application exception or result is needed.

## Service Cohesion

Application services should group workflows that change for the same business reason.

Split a service when new behavior introduces a different reason to change, a different external capability, a different transaction boundary, or different failure or authorization rules.

Do not add behavior to an existing service merely because it already has access to a related identifier, aggregate, port, or dependency.

Avoid both extremes:

- catch-all services that coordinate unrelated workflows,
- tiny services whose boundaries are only technical or naming-driven and do not clarify ownership.

## Ports

- Put protocols, abstract base classes, or callable ports in the application layer when they stabilize a boundary.
- Name ports by business capability, not technology, for example `IssueRepository` or `ReportWriter`.
- Keep port methods expressed in internal models, not external DTOs.
- Model failure expectations explicitly through result objects, domain/application exceptions, or documented contracts.

## Commands And Results

- Use immutable command/result models for non-trivial inputs and outputs.
- Protect collection ownership in command/result models; do not pass mutable collection references across use-case or port boundaries as-is.
- Validate required command shape before workflow execution.
- Keep command validation technical; semantic validation belongs in domain/application policies.
- Avoid primitive obsession when meaningful value objects exist.

## Tests

Provide tests for:

- happy-path orchestration,
- invalid command input,
- domain validation propagation,
- port failure handling,
- duplicate/conflict behavior,
- ordering and deterministic output,
- transactional or partial-failure behavior when relevant.

Prefer fake ports over framework contexts for application unit tests. Use framework integration tests only when wiring or framework behavior is the subject.

## ADR Triggers

Propose ADR discussion for new application boundary patterns, new transaction strategy, changes to dependency direction, shared workflow conventions, or changes to public command/result contracts.

## Checklist

- Does the application layer depend only on domain and its own ports?
- Are external systems hidden behind ports?
- Are commands/results explicit?
- Are domain rules still owned by domain concepts?
- Are failure modes tested?
