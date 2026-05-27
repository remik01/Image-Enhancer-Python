---
name: adapter-creation
description: "[Python] Workflow for creating or modifying infrastructure adapters that implement application ports, map external DTOs, preserve boundaries, and include tests."
---

# Adapter Creation Skill

Use this skill when Codex / Copilot needs to create, modify, or review an infrastructure adapter.

## Purpose

Create adapter implementations that:
- implement application ports,
- isolate external systems,
- map external DTOs explicitly,
- preserve domain/application boundaries,
- handle errors meaningfully,
- remain testable and replaceable.

Adapters are anti-corruption boundaries. They absorb external quirks so the core does not have to.

## When to Use

Use this skill for:
- HTTP/API clients,
- XML importers,
- JSON importers,
- Excel readers/writers,
- database repositories,
- file adapters,
- message consumers/producers,
- CLI/UI adapters when treated as boundaries.

Also use when the task mentions:
- DTO mapping,
- external system integration,
- implementing a port,
- adapter package,
- boundary translation,
- import/export logic.

## Workflow

1. Inspect existing architecture:
   - `AGENTS.md`,
   - `.github/instructions/adapters.instructions.md`,
   - `.github/instructions/mapping.instructions.md`,
   - `.github/instructions/exceptions.instructions.md`,
   - `.github/instructions/security.instructions.md` when untrusted input or credentials are involved,
   - application ports and domain model,
   - similar adapters,
   - existing tests and fixtures.

2. Identify the application port being implemented.
   - If no port exists, propose a semantic port before implementing adapter details.

3. Identify external contract shape:
   - DTOs,
   - files,
   - endpoints,
   - schemas,
   - rows/columns,
   - response status codes.

4. Define or update external DTOs in adapter package only.

5. Implement explicit mapper(s):
   - external DTO -> application/domain model,
   - application/domain output -> external request/output if needed.

6. Implement adapter logic:
   - timeouts,
   - error handling,
   - resource handling,
   - configuration,
   - diagnostics.

7. Add tests:
   - mapper tests,
   - malformed input tests,
   - missing field tests,
   - local fake server/file fixture tests where useful,
   - port contract tests where useful.

8. Run relevant verification.

## Boundary Rules

Adapters may depend on:
- application,
- domain,
- external libraries,
- framework/infrastructure APIs.

Domain and application must not depend on adapters.

External DTOs must not leak into domain/application contracts.

## Mapping Rules

Mappers must:
- be explicit,
- be deterministic,
- preserve useful source context,
- delegate semantic validation to domain factories,
- fail clearly on malformed input,
- avoid reflection magic.

Do not use `Map<String,Object>` for serious contracts.

## Error Handling Rules

Preserve context:
- external system,
- endpoint/action,
- file path,
- row number,
- column name,
- object id,
- status code,
- safe original value.

Do not log:
- passwords,
- tokens,
- secrets,
- unnecessary personal data,
- massive payloads by default.

## Configuration Rules

Use explicit configuration objects for:
- base URI,
- server/environment,
- timeout,
- retry limits,
- credentials reference,
- file paths where appropriate.

Validate configuration at startup or adapter creation.

## Testing Rules

Prefer:
- small realistic fixtures,
- local fake HTTP servers,
- temporary files/directories,
- focused mapper tests,
- deterministic assertions.

Avoid tests that require:
- production credentials,
- corporate VPN,
- live systems,
- machine-specific paths.

## Output Format

When finished, provide:

1. Port Implemented
2. External Contract
3. Mapping
4. Error Handling
5. Changed Files
6. Verification
7. Risks / Follow-Up

## Non-Goals

Do not:
- invent domain rules in adapters,
- orchestrate full workflows inside adapters,
- modify application ports to mirror awkward external APIs without justification,
- couple adapter to UI,
- introduce broad frameworks casually.

## ADR Escalation

Recommend ADR discussion when adapter creation affects:
- integration strategy,
- retry/caching policy,
- transport protocol,
- external contract ownership,
- security boundaries,
- runtime/deployment assumptions.

## Final Rule

Adapt the outside world to the application.
Do not bend the application around one external system's oddities unless the architecture explicitly accepts that cost.
