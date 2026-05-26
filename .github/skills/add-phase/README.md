# Add Phase

## Reason

Large initiatives in this repository are implemented through ordered workflow phases. This skill adds one new phase without rewriting the whole plan or duplicating previous scope.

## Functionality

- Resolves the next phase number.
- Checks existing overview, phases, plans, ADRs, decision logs, and source state.
- Drafts one reviewable phase using the standard phase contract.
- Narrows overlapping requests instead of creating duplicate phase ownership.
- Validates phase files with the phase validation helper.

## Proper Use Cases

Use this skill when a new implementation unit is needed after existing phases already exist.

Do not use it to regenerate all phases, implement code, or add vague placeholder work.

## Best Practices

- Run `python .github\skills\add-phase\scripts\next_phase_number.py --title "<title>"` before writing.
- Compare requested scope against `workflow/phases/` and `workflow/plans/`.
- Keep the phase to one primary architectural concern.
- Run the phase validator before reporting completion.
