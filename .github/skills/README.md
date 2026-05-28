# Repository Skills

This directory contains repository-local Codex / Copilot skills for this Python project template.

Each skill folder contains:

- `SKILL.md` for Codex / Copilot trigger metadata and execution instructions,
- `README.md` for human-facing reason, use cases, and best practices,
- optional `scripts/`, `references/`, or `agents/openai.yaml` resources.

The per-skill `README.md` files are a repository-local convention. They are intentionally kept out of the trigger path and are meant for maintainers who want to understand when a skill should be used or changed.

## Catalog

| Skill | Purpose |
| --- | --- |
| `adapter-creation` | Create or modify infrastructure adapters while protecting application/domain boundaries. |
| `add-phase` | Append exactly one numbered workflow phase and keep the canonical overview aligned. |
| `adr-writer` | Classify and draft ADRs or decision-log entries. |
| `ai-collaboration-contract-enforcer` | Validate AI-assisted work against governance, traceability, and reproducibility contracts. |
| `architectural-drift-investigator` | Detect semantic architecture drift against ADRs, decisions, boundaries, and implementation evidence. |
| `commit-for-phase` | Commit phase-scoped work using the repository commit-message convention. |
| `decision-impact-simulator` | Explore second-order consequences of proposed architecture or process decisions. |
| `implement-phase` | Prepare, implement, verify, and review existing workflow phases. |
| `institutional-memory-curator` | Reconstruct durable engineering rationale and detect knowledge decay. |
| `python-verification` | Run and interpret pytest, ruff, type-checking, packaging, verification, and static-analysis checks. |
| `overview-creator` | Convert early project descriptions into `workflow/docs/overview.spec.md`. |
| `phase-creator` | Generate ordered implementation phase files from the canonical overview. |
| `refactoring-safety` | Refactor Python code while preserving behavior and architecture boundaries. |
| `socio-technical-risk-analyzer` | Identify systemic coordination, ownership, governance, and AI workflow risks. |
| `static-analysis-remediation` | Fix ruff, type-checking, security, dependency, formatting, and Python quality-gate failures. |
| `technical-documentation` | Generate and review senior-developer onboarding documentation. |

See `FUTURE_SKILLS.md` for recommended complex skill candidates that have not been scaffolded yet.

## Maintenance

After adding, renaming, or deleting a skill directory, run:

```powershell
.\scripts\link-skills-to-codex.ps1
```

Then restart or reload the Codex / Copilot session so the available skill list is refreshed.

Run the repository skill audit after structural changes when the audit script is present:

```powershell
python scripts\audit-skills.py --skills-root .github\skills
```

If `python` is unavailable, use the interpreter discovered with `Get-Command python,py,python3`.
