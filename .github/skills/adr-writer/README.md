# ADR Writer

## Reason

Architectural decisions need durable reasoning. This skill prevents module, dependency, security, persistence, integration, or runtime choices from becoming undocumented defaults.

## Functionality

- Classifies whether a change needs an ADR, decision-log entry, no artifact, or human decision.
- Drafts ADRs using the repository structure.
- Drafts concise decision-log entries for smaller durable choices.
- Validates ADR numbering and required sections with a helper script.

## Proper Use Cases

Use this skill for dependency direction, new dependencies, public contracts, storage, concurrency, security, deployment, observability, or reusable conventions.

Do not use it for trivial formatting, local bug fixes, or decorative process artifacts.

## Best Practices

- Read existing ADRs and `workflow/CLI.decision-log.md` before drafting.
- Compare no-change, minimal-change, target, and extended options when the decision is significant.
- Use `python .github\skills\adr-writer\scripts\adr_tools.py --adr-dir docs\adr --next` for numbering.
- Use `--validate` before finishing ADR edits.
