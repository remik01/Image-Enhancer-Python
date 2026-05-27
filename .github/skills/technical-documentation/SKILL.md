---
name: technical-documentation
description: "[Python] Generate senior-developer and AI-agent onboarding documentation for a software project. Use when Codex / Copilot needs to map a codebase, explain package/module/class/function structure, summarize data flow, identify use cases or endpoints, inventory dependencies, flag unusual implementation choices or smells, or create a Markdown technical context document before implementation, review, or exploration work."
---

# Technical Documentation

## Recommended Execution Profile

When this skill is used, prefer the strongest available reasoning-capable analysis and documentation model exposed by the current Codex / Copilot environment.

Preferred profile, if available:

- Model: `gpt-5.5`
- Reasoning: `extra high`

If that exact profile is unavailable, use the nearest available high-reasoning analysis and documentation model. Record the actual model and reasoning profile used in the final response when the execution environment exposes that information.

Do not add model or reasoning-level requirements to generated technical documentation unless the user explicitly asks for them. Documentation quality must remain based on repository evidence, governance alignment, accurate uncertainty, useful reading order, and reviewable technical judgment rather than model availability.

## Workflow

1. Read project governance first: `AGENTS.md`, relevant `.github/instructions/*.instructions.md`, ADRs, and existing overview/workflow docs when present.
2. Run the bundled generator from the repository root:

```powershell
python .github\skills\technical-documentation\scripts\generate_technical_documentation.py --root . --output workflow\docs\technical-documentation.md
```

If `python` is not on `PATH`, use the discovered interpreter path from `Get-Command python,py,python3`.

3. Read the generated Markdown before answering. Treat it as a structured evidence pack, not as final truth.
4. Add senior judgment where the script is intentionally heuristic:
   - architecture risks and boundary drift,
   - missing tests or unclear ownership,
   - untypical implementation choices,
   - smells that need human review,
   - gaps between docs, ADRs, and code.
5. If the output is too shallow for a developer or AI agent to start work, revise the script or the documentation manually and rerun.

6. When skill structure changed, run:

```powershell
python scripts\audit-skills.py --skills-root .github\skills
```

## Persistence Strategy

The bundled generator is an approved exception to the section-by-section write rule: it may rewrite `workflow/docs/technical-documentation.md` as one deterministic generated artifact.

Manual revisions, supplemental sections, or curated follow-up documentation must be persisted incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Match the last line of existing content and replace it with itself plus the new section text.

Do not use the generator exception for unrelated hand-written documentation.

## Output Standard

The finished Markdown should let a senior developer begin useful work without rediscovering the whole repository. It should also be compact enough for an AI agent to load as project context.

Include these sections when applicable:

- project identity, stack, and governance sources,
- repository, package, module, class, function, and test structure,
- internal module dependencies and external dependencies,
- rough request/data flow across UI, API, application, domain, and adapter layers,
- use cases, REST endpoints, UI entry points, CLI entry points, or scheduled jobs,
- notable domain invariants and application ports,
- distinction between derivable dependency structure and semantic dependency intent, including unclear workflow ownership, pass-through classes, hidden coupling, and boundary translations where evidence supports it,
- untypical code solutions, smells, TODOs, boundary risks, and missing tests,
- recommended reading order for a new contributor or AI agent.

## Generator Responsibilities

Use `scripts/generate_technical_documentation.py` for deterministic discovery. The script uses only the Python standard library and should stay dependency-free so it can run in constrained repositories.

The script should inspect:

- `pyproject.toml`, dependency files, and Python package metadata,
- Python packages, modules, classes, functions, imports, entry points, and tests,
- web framework route handlers, exception handlers, or CLI commands when detectable,
- frontend `package.json`, environment files, and API client files,
- ADRs, workflow plans/phases, README, overview docs, and decision logs,
- workflow phase logs under `workflow/logs/` as curated implementation evidence,
- review prompts such as framework imports in domain code, duplicate DTO names, broad exceptions, TODO/FIXME markers, large classes, and files without nearby tests.

## Review Discipline

Do not present generated documentation as authoritative until you have read it. If generated facts conflict with ADRs or project specifications, state the conflict and prefer the higher-priority source according to repository governance.

For non-trivial repositories, explicitly say what was not inspected or what remains uncertain. Prefer uncomfortable correctness over a polished but incomplete onboarding story.
