# Advanced AI Skills Specification Pack

This document defines five advanced, project-independent AI Skills intended for usage with Codex / Copilot, ChatGPT, or future AI-assisted engineering workflows.

These Skills are not simple automation helpers. They are governance, reasoning, continuity, and architecture amplification systems.

The purpose is not merely generating code.
The purpose is reducing entropy in complex software organizations.

---

# 1. architectural-drift-investigator.skill.md

## Purpose

The Architectural Drift Investigator detects when a software system slowly diverges from:

- declared architecture,
- ADRs,
- dependency rules,
- naming conventions,
- modularity assumptions,
- organizational governance,
- design philosophy.

This Skill acts as a semantic architecture guardian.

It does not merely perform static analysis.
It interprets intent.

---

## Core Problem

Most systems decay gradually.

Typical symptoms:

- adapters begin containing business logic,
- domain rules leak into UI,
- utility classes become hidden frameworks,
- temporary exceptions become permanent,
- duplicate business concepts appear under different names,
- dependency directions reverse,
- naming consistency erodes,
- architectural boundaries become meaningless.

Traditional linters cannot detect this because the system still compiles.

Humans often stop noticing drift after several months.

---

## Skill Responsibilities

The Skill shall:

1. Read and interpret architecture documentation.
2. Read ADRs and decision logs.
3. Analyze package and module dependencies.
4. Detect violations of declared layering.
5. Detect semantic duplication.
6. Detect suspicious growth patterns.
7. Detect architectural inconsistency.
8. Compare current implementation against historical intent.
9. Explain why a detected drift matters.
10. Recommend corrective actions.

---

## Required Inputs

The Skill should consume:

- ADRs
- decision logs
- architecture diagrams
- package structures
- module descriptors
- Python packaging and dependency structures
- naming conventions
- coding standards
- dependency graphs
- Git history
- pull requests
- static-analysis contracts

Optional:

- incident reports
- onboarding documentation
- wiki pages
- runtime telemetry

---

## Expected Outputs

### Drift Report

The report should include:

- detected drift,
- severity,
- violated principle,
- affected modules,
- probable consequences,
- confidence level,
- historical references,
- suggested ADR updates or corrections.

---

## Example Findings

### Example 1

"The adapter module now contains domain validation logic introduced incrementally across six commits. This violates ADR-0007 establishing adapter passivity."

### Example 2

"Three separate naming variants exist for the same business concept: CustomerState, ClientStatus, ConsumerLifecycle. Semantic fragmentation risk detected."

### Example 3

"Temporary bypass introduced in March 2026 is now referenced by four production modules and should no longer be considered temporary."

---

## Advanced Analysis Capabilities

### Semantic Boundary Analysis

The Skill should infer:

- whether a module behaves differently than its declared responsibility,
- whether abstractions became infrastructural leakage points,
- whether package names no longer represent actual concerns.

---

### Architectural Entropy Trend

The Skill should estimate:

- whether architecture quality improves or degrades over time,
- whether drift accelerates,
- whether governance mechanisms remain effective.

---

## Non-Goals

The Skill is NOT:

- a formatter,
- a linter,
- a style checker,
- a simple dependency analyzer.

It is a semantic architecture reasoning engine.

---

## Suggested Technical Approaches

Possible implementation techniques:

- AST analysis,
- semantic embeddings,
- dependency graph analysis,
- Git history mining,
- ADR parsing,
- package clustering,
- naming similarity analysis,
- architectural rule DSLs.

---

## AI-Agent Integration

The Skill should:

- operate before large refactorings,
- participate in PR reviews,
- enrich ADR workflows,
- warn AI agents before generating architecture-breaking code.

---

## Success Criteria

The Skill is successful if:

- architectural violations are detected early,
- teams understand WHY drift matters,
- systems remain maintainable longer,
- organizational memory survives personnel changes.



---
---

# 2. decision-impact-simulator.skill.md

## Purpose

The Decision Impact Simulator estimates the technical, organizational, operational, and maintenance consequences of proposed architectural or process decisions.

It is not a binary recommendation engine.

It is a future-consequence exploration system.

---

## Core Problem

Engineering teams often evaluate decisions only locally.

Examples:

- "Can we implement this?"
- "Will this improve performance?"
- "Will this reduce boilerplate?"

But many failures emerge later:

- operational complexity,
- maintenance explosion,
- hidden coupling,
- organizational fragmentation,
- onboarding difficulty,
- testing burden,
- governance erosion.

The Skill exists to expose second-order consequences.

---

## Skill Responsibilities

The Skill shall:

1. Analyze proposed technical changes.
2. Estimate ripple effects.
3. Estimate maintenance implications.
4. Detect organizational risks.
5. Evaluate migration complexity.
6. Estimate rollback difficulty.
7. Detect hidden dependencies.
8. Compare alternatives.
9. Explain trade-offs.
10. Produce uncertainty-aware assessments.

---

## Example Decision Types

- migration to a new Python baseline,
- introducing GraphQL,
- microservice decomposition,
- virtual threads adoption,
- event sourcing,
- framework replacement,
- AI integration,
- asynchronous processing,
- modularization,
- shared libraries,
- database replacement.

---

## Expected Outputs

### Decision Impact Report

The report should contain:

- direct effects,
- indirect effects,
- operational implications,
- staffing implications,
- testing impact,
- observability impact,
- deployment impact,
- AI workflow impact,
- rollback feasibility,
- long-term maintenance implications,
- uncertainty indicators.

---

## Example Analysis

### Example

Decision:
"Introduce asynchronous event-driven communication between modules."

Potential outputs:

- increased operational observability requirements,
- eventual consistency complexity,
- debugging difficulty increase,
- retry/idempotency obligations,
- expanded integration testing burden,
- reduced direct coupling,
- higher onboarding complexity,
- more difficult production incident reconstruction.

---

## Advanced Features

### Long-Term Entropy Estimation

The Skill should estimate whether a decision:

- increases architectural complexity,
- increases cognitive load,
- creates hidden operational dependencies,
- amplifies organizational fragmentation.

---

### Human-System Interaction Analysis

The Skill should analyze:

- required skill changes,
- onboarding impact,
- concentration of expertise,
- dependency on specific individuals.

---

## Non-Goals

The Skill is NOT:

- a simplistic recommendation engine,
- a "best practices" parroting system,
- a hype-driven modernization advocate.

It must reason contextually.

---

## Suggested Technical Approaches

Possible implementation methods:

- graph propagation analysis,
- dependency topology modeling,
- historical incident analysis,
- architectural heuristics,
- maintenance-cost estimation,
- semantic coupling analysis,
- ADR cross-referencing.

---

## AI-Agent Integration

The Skill should:

- participate during planning phases,
- enrich ADR creation,
- operate before large refactorings,
- help AI agents avoid local optimization traps.

---

## Success Criteria

The Skill is successful if:

- teams understand hidden trade-offs,
- fewer irreversible bad decisions are made,
- architecture decisions become explicit,
- organizational consequences are considered alongside technical ones.



---
---

# 3. institutional-memory-curator.skill.md

## Purpose

The Institutional Memory Curator transforms fragmented project history into durable, queryable engineering knowledge.

It preserves rationale.

Not only facts.

---

## Core Problem

Most organizations lose architectural knowledge continuously.

Consequences:

- repeated mistakes,
- reintroduced rejected approaches,
- contradictory implementations,
- cargo-cult architecture,
- dependency on long-term employees,
- forgotten constraints.

Most systems eventually become:

"Nobody remembers why this exists, but removing it breaks production."

The Skill exists to prevent that condition.

---

## Skill Responsibilities

The Skill shall:

1. Aggregate project knowledge.
2. Preserve rationale.
3. Link decisions to implementation.
4. Detect contradictions.
5. Detect obsolete assumptions.
6. Reconstruct historical reasoning.
7. Support onboarding.
8. Explain system evolution.
9. Detect knowledge decay.
10. Support AI continuity.

---

## Required Inputs

The Skill should process:

- ADRs,
- decision logs,
- pull requests,
- commit history,
- architecture diagrams,
- incident reports,
- wiki pages,
- onboarding notes,
- meeting summaries,
- technical RFCs,
- static-analysis contracts.

Optional:

- issue trackers,
- deployment histories,
- chat discussions,
- CI/CD reports.

---

## Expected Outputs

### Knowledge Reconstruction

Examples:

- "Why was a specific ORM rejected?"
- "Why is XML parsing streaming-based?"
- "Why is this module intentionally isolated?"
- "Which incidents influenced this ADR?"

---

### Contradiction Detection

The Skill should detect:

- ADRs contradicting implementation,
- obsolete assumptions still enforced,
- duplicated historical decisions,
- unresolved architectural debates.

---

## Example Output

"ADR-0012 rejected asynchronous processing due to operational observability limitations. However, three later modules introduced asynchronous workflows without updating the original rationale."

---

## Advanced Features

### Knowledge Decay Estimation

The Skill should estimate:

- undocumented critical areas,
- single-person knowledge concentration,
- outdated onboarding materials,
- historical rationale gaps.

---

### Evolution Narrative Generation

The Skill should explain:

- how the system evolved,
- which trade-offs shaped it,
- which constraints disappeared,
- which architectural scars remain.

---

## Non-Goals

The Skill is NOT:

- a document search engine,
- a wiki replacement,
- a vector-database demo.

Its purpose is reconstructing engineering meaning.

---

## Suggested Technical Approaches

Potential implementation techniques:

- semantic document indexing,
- graph-based relationship models,
- commit clustering,
- rationale extraction,
- timeline reconstruction,
- semantic contradiction detection,
- embeddings + symbolic references.

---

## AI-Agent Integration

The Skill should:

- provide historical context to AI agents,
- prevent repeated mistakes,
- support onboarding of future agents,
- improve continuity across sessions.

---

## Success Criteria

The Skill is successful if:

- rationale survives personnel changes,
- onboarding accelerates,
- architectural decisions remain understandable,
- repeated mistakes decrease.



---
---

# 4. socio-technical-risk-analyzer.skill.md

## Purpose

The Socio-Technical Risk Analyzer detects organizational and human coordination risks hidden inside technical systems.

The Skill recognizes that many software failures are organizational failures expressed through code.

---

## Core Problem

Most engineering tools analyze only code.

But real risks often emerge from:

- knowledge silos,
- invisible ownership,
- governance bypass,
- hero-developer dependency,
- communication breakdown,
- undocumented critical knowledge,
- opaque workflows,
- architectural authority concentration.

The Skill exists to expose these hidden systemic risks.

---

## Skill Responsibilities

The Skill shall:

1. Analyze collaboration patterns.
2. Detect hidden ownership concentration.
3. Detect low bus-factor areas.
4. Detect suspicious development isolation.
5. Detect governance bypass patterns.
6. Detect architectural opacity.
7. Detect risky communication structures.
8. Detect AI misuse patterns.
9. Estimate organizational fragility.
10. Explain why detected risks matter.

---

## Example Risk Signals

### Knowledge Silo

"One developer authored 92% of a critical module while documentation coverage remained low."

---

### Governance Bypass

"Multiple direct commits bypassed ADR review workflow for architecture-impacting changes."

---

### Invisible Criticality

"A utility package with no declared ownership became transitively required by 78% of production modules."

---

### AI Dependency Risk

"Large code sections were generated without rationale persistence or architectural traceability."

---

## Required Inputs

The Skill should analyze:

- Git history,
- PR discussions,
- review participation,
- ADR workflows,
- commit frequencies,
- ownership patterns,
- documentation density,
- CI/CD activity,
- deployment histories,
- issue tracker interactions.

Optional:

- organizational charts,
- onboarding metrics,
- incident timelines.

---

## Advanced Features

### Transparency Health Estimation

The Skill should estimate:

- how observable development actually is,
- whether critical decisions happen publicly,
- whether key rationale remains reviewable.

---

### Governance Stability Analysis

The Skill should estimate:

- whether architecture governance is weakening,
- whether standards are selectively ignored,
- whether process exceptions become normalized.

---

### AI Workflow Safety

The Skill should detect:

- unreviewed AI-generated code concentration,
- prompt-to-production anti-patterns,
- absence of rationale persistence.

---

## Non-Goals

The Skill is NOT:

- employee surveillance,
- productivity scoring,
- simplistic developer ranking.

The purpose is systemic resilience.

---

## Suggested Technical Approaches

Possible techniques:

- graph analysis,
- commit topology analysis,
- collaboration heatmaps,
- semantic workflow analysis,
- governance event tracking,
- ownership concentration metrics.

---

## AI-Agent Integration

The Skill should:

- help AI agents understand organizational constraints,
- identify fragile areas before major changes,
- encourage transparent workflows.

---

## Success Criteria

The Skill is successful if:

- organizational fragility decreases,
- knowledge silos shrink,
- transparency improves,
- governance becomes sustainable.



---
---

# 5. ai-collaboration-contract-enforcer.skill.md

## Purpose

The AI Collaboration Contract Enforcer establishes durable governance rules for cooperation between:

- humans,
- AI agents,
- IDE assistants,
- CI/CD systems,
- architectural governance,
- documentation systems.

It transforms AI usage from ad-hoc prompting into reproducible engineering collaboration.

---

## Core Problem

Most AI-assisted development is currently:

- session-based,
- weakly governed,
- poorly documented,
- non-reproducible,
- architecturally inconsistent,
- rationale-poor.

The result:

- hidden assumptions,
- inconsistent patterns,
- unstable quality,
- architecture erosion,
- context loss.

The Skill exists to formalize AI collaboration.

---

## Skill Responsibilities

The Skill shall:

1. Enforce AI workflow contracts.
2. Require rationale persistence.
3. Validate ADR obligations.
4. Validate documentation requirements.
5. Validate architectural consistency.
6. Enforce reviewability.
7. Preserve AI reasoning artifacts.
8. Validate reproducibility.
9. Detect governance bypass.
10. Improve continuity across AI sessions.

---

## Example Rules

### Rule Example 1

"Any architecture-impacting change requires ADR evaluation."

---

### Rule Example 2

"AI-generated code exceeding 150 lines requires rationale persistence."

---

### Rule Example 3

"Generated plans must be persisted in workflow/plans/."

---

### Rule Example 4

"Architectural assumptions must be linked to authoritative documents."

---

### Rule Example 5

"Any exception to static-analysis contracts must be documented in an exception register."

---

### Rule Example 6

"AI-generated changes affecting multiple modules require dependency impact analysis."

---

## Required Inputs

The Skill should consume:

- project instructions,
- ADRs,
- workflow rules,
- decision logs,
- coding standards,
- static-analysis contracts,
- CI/CD policies,
- repository structures,
- governance documentation,
- architectural diagrams,
- PR templates,
- exception registers.

Optional:

- incident reports,
- onboarding documents,
- deployment policies,
- security standards.

---

## Expected Outputs

### AI Governance Report

The report should contain:

- violated workflow contracts,
- missing rationale,
- undocumented assumptions,
- ADR obligations,
- architectural inconsistencies,
- reproducibility risks,
- traceability gaps,
- governance bypass indicators,
- unresolved exceptions,
- missing review evidence.

---

## Advanced Features

### Prompt-to-Artifact Traceability

The Skill should maintain:

- which prompts produced major artifacts,
- which decisions emerged from AI planning,
- which assumptions were machine-generated,
- which generated artifacts influenced production systems.

The purpose is not surveillance.
The purpose is engineering traceability.

---

### Reproducibility Validation

The Skill should estimate whether another engineer or AI agent could:

- reproduce the same outcome,
- understand why decisions were made,
- continue the work safely,
- audit architectural reasoning.

---

### AI Context Integrity

The Skill should detect:

- stale instructions,
- contradictory governance files,
- duplicated policies,
- inconsistent architecture guidance,
- outdated workflow assumptions.

---

### Governance Drift Detection

The Skill should detect when:

- teams silently stop following workflows,
- ADR discipline weakens,
- review rigor declines,
- rationale persistence disappears,
- AI usage becomes increasingly opaque.

---

## Example Scenarios

### Scenario 1

An AI agent introduces a new infrastructure dependency.

The Skill should:

- require ADR evaluation,
- verify dependency governance,
- ensure rationale persistence,
- request operational impact analysis.

---

### Scenario 2

A developer merges large AI-generated changes without documentation.

The Skill should:

- flag traceability violations,
- require rationale summaries,
- request architecture consistency validation,
- recommend review escalation.

---

### Scenario 3

Workflow instructions contradict newer ADRs.

The Skill should:

- identify conflicting guidance,
- estimate affected workflows,
- recommend governance reconciliation.

---

## Suggested Repository Structure

Example:

```text
/workflow
    /plans
    /investigations
    ai-decision-log.md
    ai-governance-rules.md

/adr
    ADR-0001-example.md

/architecture
    dependency-rules.md
    layering-rules.md

/.github
    copilot-instructions.md
    /instructions
```

---

## Suggested Technical Approaches

Possible implementation techniques:

- semantic policy validation,
- workflow graph analysis,
- repository rule engines,
- prompt-to-artifact linking,
- architecture consistency validation,
- Git metadata analysis,
- reasoning persistence models,
- AI workflow DSLs.

---

## AI-Agent Integration

The Skill should:

- operate before major code generation,
- participate in planning phases,
- enrich pull-request reviews,
- validate governance compliance,
- persist important reasoning artifacts,
- support multi-agent collaboration.

The Skill should function as a governance layer above individual AI sessions.

---

## Long-Term Vision

The long-term purpose is establishing:

- durable AI-assisted engineering systems,
- reproducible organizational reasoning,
- architecture continuity across years,
- transparent AI-human cooperation,
- institutional resilience.

The ultimate goal is not maximizing code generation speed.

The ultimate goal is preserving engineering sanity while AI capability increases.

Because without governance, advanced AI-assisted development eventually degenerates into high-speed architectural entropy.

Which, to be fair, is already how many organizations operate even without AI. They simply perform the collapse manually and call it agility.

---

## Success Criteria

The Skill is successful if:

- architectural rationale remains traceable,
- AI collaboration becomes reproducible,
- governance survives personnel changes,
- AI-generated systems remain understandable,
- engineering transparency improves,
- organizational memory persists.
