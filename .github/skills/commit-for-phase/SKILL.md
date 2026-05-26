---
name: commit-for-phase
description: Commit repository changes for a workflow phase. Use when the user invokes `$commit-for-phase <phase-number>` or asks Codex / Copilot to stage all changes and commit them using the repository Phase Commit Message Convention from `.github/instructions/phases.instructions.md`.
---

# Commit For Phase

Use this skill to create a phase-scoped Git commit with the repository's phase commit message convention.

## Workflow

1. Read `.github/instructions/phases.instructions.md`.
2. Run the bundled script in dry-run mode first:

```powershell
.\.github\skills\commit-for-phase\scripts\Commit-ForPhase.ps1 <phase-number> -DryRun
```

3. If the dry run resolves the intended phase and commit message, run the bundled script from the repository root:

```powershell
.\.github\skills\commit-for-phase\scripts\Commit-ForPhase.ps1 <phase-number>
```

4. Report the created commit hash and commit message.

## Behavior

The script:

- accepts a phase number with or without leading zeros, such as `7`, `07`, or `007`,
- resolves exactly one matching `workflow/phases/<NN>_*.md` file,
- extracts tickets from the phase file `## Tickets` section,
- extracts the phase title from the phase file H1,
- resolves `workflow/plans/phase-<NN>-*.md` when a matching persisted plan exists,
- sets the matching phase plan `## Status` section to `Completed YYYY.MM.DD` before staging files,
- reads the current OS login name from `USERNAME`, then `USER`, then .NET identity,
- auto-generates a concise commit description from changed paths,
- runs `git add .`,
- runs `git commit -m "YYYY.MM.DD <login-name> <tickets...> <phase-title>: <commit-description>"`.

## Guardrails

Stop and report the failure if:

- the phase argument is missing or not a positive integer,
- no matching phase file exists,
- multiple matching phase files exist,
- the phase file has no H1 title,
- the phase file has no tickets,
- multiple matching phase plan files exist,
- a matching phase plan exists but has no `## Status` section,
- there are no repository changes to commit,
- Git staging or commit fails.

Use dry-run mode for validation:

```powershell
.\.github\skills\commit-for-phase\scripts\Commit-ForPhase.ps1 7 -DryRun
```

Do not use this skill when unrelated user changes should remain unstaged. The script intentionally stages all repository changes.
