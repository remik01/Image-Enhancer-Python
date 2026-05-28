# Add Phase

## Reason

Large initiatives in this repository are implemented through ordered workflow phases. This skill adds one new phase without rewriting the whole plan or duplicating previous scope, and keeps the canonical overview aligned when the new phase introduces meaningful scope amendments.

## Functionality

- Resolves the next phase number.
- Checks existing overview, phases, plans, ADRs, decision logs, and source state.
- Updates `workflow/docs/overview.spec.md` when the new phase introduces non-trivial project-scope changes.
- Drafts one reviewable phase using the standard phase contract.
- Narrows overlapping requests instead of creating duplicate phase ownership.
- Validates phase files and overview amendment structure with repository helper scripts.

## Proper Use Cases

Use this skill when a new implementation unit is needed after existing phases already exist, especially when the new phase also needs durable traceability in the canonical overview.

Do not use it to regenerate all phases, implement code, regenerate the whole overview, or add vague placeholder work.

## Best Practices

- Run `python .github\skills\add-phase\scripts\next_phase_number.py --title "<title>"` before writing.
- Compare requested scope against `workflow/phases/` and `workflow/plans/`.
- Amend only meaningful overview sections; prefer `Core Features` and `Functional/Nonfunctional Requirements` only when the phase changes project scope.
- Do not add overview entries for routine phase mechanics, helper-script names, model preferences, or repeated boilerplate.
- Use `python .github\skills\add-phase\scripts\validate_overview_amendment.py --overview workflow\docs\overview.spec.md` after overview edits.
- Keep the phase to one primary architectural concern.
- Run the overview and phase validators before reporting completion.
