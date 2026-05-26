---
name: implement-phase
description: Implement an existing workflow phase from workflow/phases and produce phase-scoped or final whole-project implementation coverage review evidence. Use when Codex / Copilot is asked to implement phase N, implement workflow phase NN, continue a phase implementation, verify implementation coverage against a phase file, verify final overview implementation coverage, or prepare review/closeout evidence while preserving repository governance, ADR discipline, artifact ownership, tests, and architectural boundaries.
---

# Implement Phase

Use this skill to execute an existing workflow phase without rediscovering the same governance, artifact, verification, and review steps in every session.

This skill orchestrates implementation. It does not generate product code from a phase file, and it does not replace source inspection, tests, ADR review, or human judgment.

## Workflow

1. Resolve the phase and prepare context:

```powershell
python .github\skills\implement-phase\scripts\prepare_phase_context.py --phase <phase-number>
```

Read the generated context pack. Treat it as evidence, not authority.

2. Initialize the phase implementation log:

```powershell
python .github\skills\implement-phase\scripts\phase_journal.py --phase <phase-number> --init
```

Use the log for concise, durable evidence. Record context read, assumptions, decisions, actions, verification, failures/remediation, review findings, and lessons learned. Do not persist raw chain-of-thought, chat transcripts, secrets, credentials, or long command output.

3. Read required governance and phase artifacts:

- `AGENTS.md`
- `.github/instructions/work-scope.instructions.md`
- `.github/instructions/planningPersistence.instructions.md`
- `.github/instructions/phases.instructions.md`
- `.github/instructions/review-checklist.instructions.md`
- the phase file under `workflow/phases/`
- the context pack's suggested instruction files, ADRs, plans, and investigations

Append log entries as work progresses. Examples:

```powershell
python .github\skills\implement-phase\scripts\phase_journal.py --phase <phase-number> --event context --summary "Read phase and governance context" --file AGENTS.md --file workflow\phases\<phase-file>.md
python .github\skills\implement-phase\scripts\phase_journal.py --phase <phase-number> --event decision --summary "Accepted ImageIO-only baseline" --details "Keeps native dependency risk out of this phase."
python .github\skills\implement-phase\scripts\phase_journal.py --phase <phase-number> --event verification --summary "Python test suite" --command "python -m pytest" --result "Passed"
```

4. Create or update a persisted implementation plan under `workflow/plans/` when the phase touches multiple files, layers, scripts, or documentation. Use `.github/instructions/planningPersistence.instructions.md` and write plan sections incrementally.

5. Implement the phase with the relevant layer guidance. Route focused work to existing skills when appropriate:

- `adapter-creation` for infrastructure adapters,
- `refactoring-safety` for behavior-preserving Python refactors,
- `static-analysis-remediation` for ruff, type-checker, security, dependency, or formatting findings,
- `python-verification` for Python validation strategy,
- `adr-writer` when a phase exposes an ADR or decision-log obligation,
- `technical-documentation` for generated onboarding documentation.

6. Before closeout, generate verification and review evidence:

```powershell
python .github\skills\implement-phase\scripts\suggest_phase_verification.py --phase <phase-number>
python .github\skills\implement-phase\scripts\check_phase_artifact_coverage.py --phase <phase-number>
python .github\skills\implement-phase\scripts\phase_implementation_coverage_review.py --phase <phase-number>
python .github\skills\implement-phase\scripts\phase_review_pack.py --phase <phase-number>
```

If reviewing against a branch or merge base, pass `--base <ref>` to the verification, artifact coverage, implementation coverage review, and review-pack scripts.

When implementing the final project closure and handover phase, also generate or update the whole-project overview implementation coverage review:

```powershell
python .github\skills\implement-phase\scripts\overview_implementation_coverage_review.py
```

Complete `workflow/phases/_overview-implementation-coverage-review.md` by mapping every overview item to implementation and verification evidence across phase implementation reviews, workflow logs, plans, decision logs, source/test files, runtime validation evidence, and handover documentation. Then validate it strictly:

```powershell
python .github\skills\implement-phase\scripts\overview_implementation_coverage_review.py --validate --strict-open-items
```

Use non-strict validation, adding `--allow-missing` when `Missing` rows are accepted, only when final project closure is intentionally incomplete and the final response plus decision log clearly record the accepted open items.

7. Run the relevant verification commands. Do not treat suggested commands as exhaustive; add phase-specific checks when source inspection or runtime risk requires them. Record meaningful verification outcomes in the phase log.

8. Complete the persisted implementation coverage review:

- update `workflow/phases/_phase-NN-implementation-coverage-review.md`,
- map every goal, feature, constraint, scope item, out-of-scope item, artifact expectation, testing expectation, acceptance criterion, and ADR / decision-log follow-up to implementation and verification evidence,
- do not mark a row `Covered` without source/test/command/log/ADR/decision-log evidence,
- report any `Partially covered`, `Deferred`, `Needs clarification`, or `Missing` row in the final response.

Validate the review before closeout:

```powershell
python .github\skills\implement-phase\scripts\phase_implementation_coverage_review.py --phase <phase-number> --validate --strict-open-items
```

Use non-strict validation only when the phase is intentionally incomplete and the final response clearly says so.

9. Mark the phase log status before commit handoff:

```powershell
python .github\skills\implement-phase\scripts\phase_journal.py --phase <phase-number> --status "Completed YYYY.MM.DD"
```

Use `commit-for-phase` only after the worktree scope is correct:

```powershell
.\.github\skills\commit-for-phase\scripts\Commit-ForPhase.ps1 <phase-number> -DryRun
```

If the dry run is correct, run the same command without `-DryRun`.

## Helper Scripts

- `prepare_phase_context.py`: writes a phase context pack under target/phase-context by default.
- `phase_journal.py`: creates or appends structured implementation evidence under `workflow/logs/phase-NN-implementation-log.md` by default.
- `phase_plan_skeleton.py`: prints a plan skeleton to stdout; it does not write the persisted plan.
- `suggest_phase_verification.py`: prints a dry-run verification matrix.
- `check_phase_artifact_coverage.py`: compares changed files with the phase's `Generated / Modified Artifacts` section.
- `phase_implementation_coverage_review.py`: creates or validates `workflow/phases/_phase-NN-implementation-coverage-review.md`, a phase-file-to-implementation traceability matrix.
- `overview_implementation_coverage_review.py`: creates or validates `workflow/phases/_overview-implementation-coverage-review.md`, a whole-project overview-to-implementation traceability matrix for final closure.
- `phase_review_pack.py`: writes a review pack under target/phase-context by default.

All helper output is review evidence. Do not use it as proof that implementation is correct.

## Guardrails

- Do not implement out-of-scope phase items.
- Do not broaden product behavior to make a phase feel complete.
- Do not weaken tests, architecture checks, or static-analysis rules to satisfy a phase.
- Do not claim phase completion while implementation coverage review rows remain `Missing`, `Partially covered`, or `Needs clarification`, unless the user explicitly accepts incomplete phase closure.
- Do not claim final project closure while overview implementation coverage rows remain `Missing`, `Partially covered`, or `Needs clarification`, unless the user explicitly accepts incomplete closure and the decision log records the open items.
- Do not use phase logs as raw thought dumps. Keep entries evidence-focused, concise, and safe to review.
- Do not print or rewrite local secrets, including repository-specific files under `%USERPROFILE%\<project-local-config-dir>\`.
- Do not automate commits or PR creation from this skill; delegate commits to `commit-for-phase` and PR work to the GitHub workflow.
- Stop and investigate when artifact coverage, verification suggestions, or review packs conflict with the phase file, ADRs, or source evidence.
