# Phase Creator

## Reason

Phase files convert the project overview into implementation units that are small enough to review, verify, and commit safely.

## Functionality

- Reads `workflow/docs/overview.spec.md` and governance artifacts.
- Generates ordered `workflow/phases/NN_PhaseTitle.md` files.
- Applies the standard phase contract from `references/phase-file-contract.md`.
- Preserves layer boundaries and ADR/decision-log follow-up.
- Validates generated phase files and overview coverage with helper scripts.
- Requires final closure phases to validate whole-project overview implementation coverage before handover completion.

## Proper Use Cases

Use this skill when a broad overview needs an initial implementation sequence or when explicit regeneration is requested.

Do not use it to implement source code, overwrite existing phase files silently, or introduce infrastructure not supported by the overview or ADRs.

## Best Practices

- Resolve the canonical overview before drafting.
- Put domain/application concerns before adapter and UI work.
- Keep server/API contracts ahead of frontend or desktop client phases.
- Run `python .github\skills\phase-creator\scripts\validate_phase_files.py --phase-dir workflow\phases`.
- Run `python .github\skills\phase-creator\scripts\validate_phase_coverage.py --coverage workflow\phases\_overview-coverage-review.md --phase-dir workflow\phases`.
