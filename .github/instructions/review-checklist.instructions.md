# Review Checklist Instructions

Use this checklist for reviews and as a final self-check before completing non-trivial work.

## Architecture

- Boundaries are preserved.
- Dependency direction points inward.
- Domain remains framework- and adapter-free.
- Ports and mappings are explicit where boundaries need stability.
- ADR or decision-log needs are evaluated.

## Correctness

- Requirements and assumptions are explicit.
- Invariants are enforced in the right layer.
- Collection ownership is explicit; mutable internal state is not exposed, aliased, or passed across boundaries as-is.
- Edge cases, duplicates, conflicts, ordering, and invalid input are handled.
- Failure modes are intentional and observable.

## Tests

- Meaningful behavior has tests.
- Tests are deterministic and isolated.
- Boundary samples cover malformed and missing data.
- Assertions were not weakened.
- Relevant verification commands were run or reported as not run.
- Phase logs capture meaningful implementation evidence when phase work used them.

## Security And Operations

- Secrets and sensitive data are protected.
- External input is validated.
- Timeouts, limits, and retries are explicit where needed.
- Logs are useful, safe, and not noisy.
- Configuration failures are clear.

## Maintainability

- Names follow project language.
- Abstractions remove real complexity.
- Dependencies are justified.
- Unrelated cleanup is avoided.
- Documentation explains non-obvious intent.
- Non-obvious dependencies and data flow are documented at the owning type, package, plan, ADR, or technical-documentation level.
- Docstrings explain collaborator intent for architectural APIs without duplicating import or call graphs.
- Services have a clear reason to change.
- New behavior belongs to the same workflow, not merely near the same data.
- Billing, export, notification, authentication, audit, and similar capability changes remain reviewable without risking unrelated workflows.
- Decomposition is justified by cohesion, not by maximizing class count.
