---
name: add-phase
description: Add one workflow phase file under workflow/phases from an inline plain-text description or a file containing the description. Use when Codex / Copilot needs to append a single numbered phase that is consistent with workflow/docs/overview.spec.md, existing phases, implemented plans, source code, AGENTS.md, and repository workflow governance.
---

# Add Phase

## Purpose

Add exactly one new implementation phase to:

```text
workflow/phases/
```

The Skill turns a user-provided phase idea into a numbered, reviewable phase file. It does **not** implement code, regenerate all phases, or rewrite existing phase files.

Use `.github/skills/phase-creator/SKILL.md` as the local style and content contract for phase file structure.

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable planning model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning planning model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

## Inputs

Accept one of:

- inline plain-text description of the new phase,
- path to a text or Markdown file containing the new phase description.

If the input appears to be a path:

1. Read the file when it exists.
2. Stop and report the missing file when it does not exist.
3. Do not guess from similarly named files.

If the input is too vague, ask for the missing product intent before creating the phase when the gap would materially change scope, boundaries, tests, or acceptance criteria. Otherwise create a conservative phase and mark assumptions explicitly.

## Required Context

Before creating the phase, read:

- `AGENTS.md`
- `.github/instructions/phases.instructions.md`
- `workflow/docs/overview.spec.md`
- `.github/skills/phase-creator/SKILL.md`
- existing `workflow/phases/*.md`
- existing `workflow/plans/*.md`

When present and relevant, inspect:

```text
docs/adr/*.md
workflow/*.decision-log.md
workflow/investigations/*.md
```

Inspect source code and tests enough to understand what has already been implemented. Use this evidence to avoid duplicate phase scope and to fit the new phase into the current project state.

## Phase Numbering

Use the helper script for deterministic numbering and collision checks:

```powershell
python .github\skills\add-phase\scripts\next_phase_number.py --title "<short phase title>"
```

If `python` is unavailable, use the interpreter discovered with `Get-Command python,py,python3`.

Create one new file under:

```text
workflow/phases/
```

Numbering rules:

- If no phase files exist, use `01`.
- Otherwise find existing phase files whose names begin with two digits followed by `_` or `-`.
- Use the highest existing numeric prefix plus one.
- Use a zero-padded two-digit number while the sequence is below 100.
- Do not fill gaps unless the user explicitly asks to repair numbering.
- Do not overwrite an existing phase file.

Filename format:

```text
NN_<ShortPhaseTitle>.md
```

Filename rules:

- Keep the title short and stable.
- Use PascalCase or the existing repository convention.
- Remove or replace spaces, ampersands, slashes, colons, question marks, and shell-awkward characters.
- Prefer a name that describes the phase ownership, not an implementation detail.

## Redundancy And Fit Checks

Before drafting, compare the requested phase against:

- `workflow/docs/overview.spec.md`,
- existing phase files,
- implemented plans in `workflow/plans/`,
- ADRs and decision logs,
- current source modules and tests.

Then choose one outcome:

- If the requested work is clearly already implemented and covered by an existing phase, stop and report the matching evidence.
- If the requested work overlaps an existing phase but has meaningful missing scope, create a narrowed follow-up phase for only the missing work.
- If the requested work conflicts with the overview, ADRs, or repository governance, stop or ask for clarification before creating the phase.
- If the requested work is new and compatible, create the next numbered phase.

Do not create a phase that duplicates ownership already assigned to an earlier phase. Constraints may repeat across phases when they protect architecture, security, testing, or governance.

## Required Phase Structure

Use the phase contract in:

```text
.github/skills/phase-creator/references/phase-file-contract.md
```

Do not omit sections. If no special content exists for a section, write `None identified.` rather than leaving it blank.

## Drafting Rules

- Keep the new phase independently reviewable.
- Assign one primary architectural concern to the phase.
- Preserve domain, application, adapter, UI, CLI, and bootstrap boundaries.
- Put contracts before clients and domain/application rules before infrastructure when the requested phase depends on them.
- Do not invent persistence, authentication, Docker, cloud deployment, messaging, AI services, databases, or new dependencies unless the overview, ADRs, existing code, or user input requires them.
- Make tests and acceptance criteria concrete enough to fail.
- Include verification commands appropriate to the affected layers.
- Explicitly evaluate ADR and decision-log follow-up.
- Keep implementation instructions compatible with the current project state, not only the original overview.

## Codex/Copilot Execution Notes Requirements

In the generated phase file, include advisory implementation-profile guidance in the `Codex / Copilot Execution Notes` section:

```text
Recommended implementation profile, if available:
- Model: gpt-5.3-codex
- Reasoning: extra high

If unavailable, use the strongest available coding model with high reasoning. Do not treat model availability as an acceptance criterion. Record the actual model/profile used when implementing the phase if the execution environment exposes that information.
```

Keep acceptance criteria model-independent. A phase is complete only when its artifacts, tests, architecture checks, documentation, and validation evidence satisfy the phase contract.

Every generated phase must tell implementers to:

- read `AGENTS.md`,
- read the phase file,
- check ADRs, decision logs, plans, and relevant source code,
- create or update a persisted plan when implementation touches multiple files or modules,
- avoid out-of-scope items,
- preserve architecture boundaries,
- add or update tests with the implementation,
- record meaningful decisions,
- propose ADR discussion for architectural impact,
- run relevant verification commands,
- report changed files, tests executed, and known weak points.

Include the phase commit message convention from `.github/instructions/phases.instructions.md`:

```text
YYYY.MM.DD <login-name> <ticket-1> <ticket-2> ... <phase-title>: <commit-description>
```

If the generated phase has no tickets, instruct implementers to stop before committing and correct the phase file.

## Persistence Strategy

Write phase file incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the first section (title block and Context).
2. Use the `edit` tool to append each subsequent section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

This approach provides intermediate checkpoints, reduces content loss on failure, and keeps the file reviewable at every step.

## Output Summary

After creating the phase file, respond with:

```md
## Result

Created `/workflow/phases/NN_<ShortPhaseTitle>.md`.

## Assumptions

<Confirmed facts and inferred assumptions.>

## Reasoning summary

<Why this phase number and scope were chosen.>

## Alternatives considered

<Notable alternatives and why they were not chosen.>

## Weak points / uncertainty

<Risks, unknowns, redundancy concerns, and checks not run.>

## Reusable artifact

<The new phase file path and any important usage note.>
```

## Failure Handling

- Missing input file: stop and report the missing path.
- Missing `workflow/docs/overview.spec.md`: recommend running `overview-creator` before adding phases.
- Missing phase directory: create `workflow/phases/` and use phase `01`.
- Existing phase filename collision: choose a shorter distinct title or stop and ask if the collision reflects duplicate scope.
- Conflicting governance: follow `AGENTS.md` priority rules and document the conflict.
- Redundant request: stop with evidence instead of creating noise.
- Validation failure: run `python .github\skills\phase-creator\scripts\validate_phase_files.py --phase-dir workflow\phases`, fix the new phase, and rerun before reporting completion.
