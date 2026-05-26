# Commit For Phase

## Reason

Phase commits must preserve traceability to workflow phase files and ticket placeholders. This skill wraps the repository commit-message convention in a deterministic script.

## Functionality

- Resolves a phase by number.
- Extracts tickets and H1 title from the phase file.
- Builds a commit message using local date, OS login, tickets, phase title, and a path-based description.
- Stages all repository changes and creates the commit.

## Proper Use Cases

Use this skill only when all current repository changes belong in the requested phase commit.

Do not use it when unrelated user edits are present or when a phase has no tickets.

## Best Practices

- Always run `.\.github\skills\commit-for-phase\scripts\Commit-ForPhase.ps1 <phase> -DryRun` first.
- Inspect the changed-path count and generated message.
- Stop if the phase, tickets, or staged scope look wrong.
