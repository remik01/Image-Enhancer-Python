# Implement Phase

## Reason

Phase implementation repeatedly requires the same setup: resolve the phase, read governance, create a durable plan, inspect artifact ownership, choose verification commands, and prepare review evidence. This skill makes that workflow explicit and repeatable.

## Functionality

- Resolves existing workflow phases by number.
- Generates phase context packs under `target/phase-context/`.
- Maintains structured implementation logs under `workflow/logs/`.
- Prints implementation plan skeletons for manual persisted-plan creation.
- Suggests verification commands from phase text and changed files.
- Checks changed files against phase artifact ownership.
- Creates and validates a final whole-project overview implementation coverage review.
- Generates phase review packs for closeout.

## Proper Use Cases

Use this skill for prompts such as `implement phase 8`, `implement workflow phase 12`, `continue phase 10`, or `prepare review evidence for phase 11`.

Do not use it to create new phase files, commit work, open PRs, or generate product code from the phase text.

## Best Practices

- Run `prepare_phase_context.py` before editing source files.
- Use `phase_journal.py` for concise context, decision, action, verification, failure, review, and lesson entries.
- Treat helper output as evidence that still requires source and governance review.
- Run artifact coverage and review-pack scripts before committing.
- For the final closure phase, run `overview_implementation_coverage_review.py --validate --strict-open-items` before claiming handover completion.
- Use `commit-for-phase` for the final phase-scoped commit.
