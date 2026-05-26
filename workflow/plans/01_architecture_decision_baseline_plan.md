# Phase 01 Architecture Decision Baseline Plan

## Status

In progress.

## Context

Phase 01 owns governance artifacts only. It must establish architectural direction before later phases add source code, dependencies, static-analysis configuration, image-processing adapters, AI integration, plugin loading, REST API surfaces, async execution, or desktop UI code.

## Goal

Create ADRs, an architecture overview, a decision-log baseline, and phase evidence that make the initial architecture decisions reviewable and actionable for later implementation phases.

## Non-Goals

- Do not implement Python package source code.
- Do not add runtime dependencies, tool configuration, or CI configuration.
- Do not implement static-analysis gates.
- Do not implement domain, application, adapter, API, UI, plugin, persistence, or async behavior.
- Do not decide production deployment ownership.

## Assumptions

- `workflow/docs/overview.spec.md` is the authoritative project overview.
- No prior ADRs, decision log, phase implementation plans, or investigations exist.
- The source code is still a PyCharm sample stub; this phase should not alter it.
- Phase 02 will implement package scaffolding, static-analysis configuration, architecture checks, CI, and CodeQL.
- Later phases may revise proposed decisions through ADR updates if implementation evidence invalidates an assumption.

## Rationale

The overview contains durable architecture questions that would otherwise be encoded implicitly by early source-code choices: layer structure, dependency direction, desktop runtime, REST exposure, persistence contract, plugin trust, AI provider boundary, async execution, image-processing adapter strategy, runtime configuration, and architecture-fitness gates. Capturing those choices before implementation keeps later phases reviewable and prevents accidental architecture drift.

The plan chooses documentation-first governance because Phase 01 is explicitly scoped to decision artifacts and excludes product code. A source-first approach would create architecture by implementation accident, especially around UI framework choice, REST contracts, plugin loading, and persistence format. A broad exploratory investigation was not chosen because the overview already identifies the decision areas; the useful artifact now is a set of proposed or accepted ADRs that can guide Phase 02 and later implementation.

Some decisions are accepted as initial direction where the repository governance and overview are clear, such as layered architecture and domain independence. Other choices are intentionally recorded as proposed or phase-gated, such as the final UI runtime and repository-specific static-analysis implementation, because later evidence may require adjustment.

## Trade-offs & Limitations

- ADRs created in this phase will guide implementation but cannot prove feasibility until later phases build and verify code.
- Choosing a conservative local-first baseline delays advanced extensions such as GPU acceleration, local inference, semantic search, and production deployment.
- Recording several decisions in one phase creates more review material up front, but it reduces the risk that later phases silently introduce incompatible architecture.
- The phase does not create executable architecture checks; that protection begins in Phase 02.
- The phase does not commit to final UI polish, packaging, or production operations.

## Implementation Approach

1. Create four ADRs under `docs/adr/` covering the architecture areas named by Phase 01.
2. Create `docs/architecture/architecture-overview.md` as a concise guide for implementers.
3. Append an initial `workflow/CLI.decision-log.md` entry for non-ADR assumptions and conventions.
4. Record context, decisions, actions, verification, and closeout status in `workflow/logs/phase-01-implementation-log.md`.
5. Generate phase verification suggestions, artifact coverage, implementation coverage review, and review pack evidence.

## Affected Layers

- Governance documentation.
- Architecture documentation.
- Workflow planning and phase evidence.

No product runtime layer is modified in this phase.

## Tests And Verification

- Run the implement-phase helper scripts for verification suggestions, artifact coverage, implementation coverage review, and review pack generation.
- Validate the phase implementation coverage review with strict open-item checks.
- Run `git diff --check`.
- Run `python .github\skills\phase-creator\scripts\validate_phase_files.py --phase-dir workflow\phases`.
- Run a secret-pattern scan across changed documentation and workflow areas.
- Skip runtime tests because this phase introduces no product code.

## Risks

- ADRs can become stale if later phases change direction without updating them.
- The UI, plugin, AI, and async choices may need revision after implementation proof.
- Documentation-only architecture can still drift until Phase 02 adds enforceable checks.
- The initial decision-log baseline may need expansion as implementation uncovers local conventions.

## ADR / Decision-Log Needs

- ADRs are required for the major architecture decisions listed in Phase 01.
- A decision-log entry is required for accepted phase sequencing assumptions, local-first baseline, deferred CLI behavior, and documentation-only nature of this phase.
