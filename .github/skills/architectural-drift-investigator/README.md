# Architectural Drift Investigator

## Reason

Architecture often decays while the system still compiles. This skill helps detect semantic drift from ADRs, decision logs, module boundaries, dependency rules, naming conventions, and historical intent.

## Functionality

- Reads architecture and governance artifacts.
- Compares declared intent against implementation evidence.
- Detects boundary erosion, semantic duplication, suspicious growth, and undocumented deviations.
- Produces severity, confidence, consequences, and correction recommendations.

## Proper Use Cases

Use before large refactors, during architecture reviews, after repeated boundary issues, or when implementation appears inconsistent with ADRs.

Do not use as a formatter, style checker, or replacement for architecture fitness checks/static analysis.

## Best Practices

- Anchor every finding to a concrete artifact or file.
- Classify weak signals separately from confirmed drift.
- Prefer focused remediation over broad redesign.
- Escalate ADR or decision-log updates when drift reflects a real architecture change.
