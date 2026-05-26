# Technical Documentation

## Reason

Senior developers and AI agents need compact, evidence-backed onboarding context before making non-trivial changes. This skill generates a documentation evidence pack and requires human review.

## Functionality

- Runs a deterministic repository inspection script.
- Summarizes modules, dependencies, packages, endpoints, UI/API entry points, workflow evidence, data flow, and review prompts.
- Flags likely smells and missing tests as review leads.
- Requires reading the generated documentation before reporting it as useful.

## Proper Use Cases

Use this skill before major implementation work, review, onboarding, architecture investigation, or when codebase context has drifted.

Do not use it as a substitute for source inspection, ADR review, or tests.

## Best Practices

- Generate to `workflow/docs/technical-documentation.md`.
- Read and correct the generated output before summarizing it.
- Check `workflow/logs/` when phase implementation history affects onboarding or review context.
- Treat script findings as evidence prompts, not automatic defects.
- Update the generator when recurring discovery gaps appear.
