# Decision Impact Simulator

## Reason

Architecture and process decisions often fail through second-order effects: testing burden, operational complexity, onboarding difficulty, hidden coupling, or governance erosion. This skill makes those consequences explicit before the decision hardens.

## Functionality

- Compares no-change, minimal-change, proposed, and extended options.
- Estimates direct and indirect effects.
- Assesses testing, operations, observability, migration, rollback, maintenance, and organizational impact.
- Produces uncertainty-aware decision impact reports.

## Proper Use Cases

Use during ADR drafting, phase planning, dependency adoption, runtime model changes, major refactoring, or process changes.

Do not use as a hype filter that rubber-stamps fashionable architecture.

## Best Practices

- State the proposed decision in one sentence first.
- Keep uncertainty visible.
- Include rollback feasibility and future maintenance cost.
- Recommend ADR, decision-log, or investigation follow-up when appropriate.
