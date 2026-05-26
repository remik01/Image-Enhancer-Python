# Investigation Instructions

Use persisted investigations when evidence, hypotheses, and conclusions need to survive beyond the chat.

## Directory And Naming

Store investigation files under:

```text
workflow/investigations/
```

Use stable, dated filenames:

```text
YYYY-MM-DD-short-topic.md
```

## Create An Investigation When

- the user explicitly asks for an investigation or investigation record,
- conclusions depend on repository evidence, logs, runtime behavior, HTTP responses, database state, CI output, or external system behavior,
- debugging requires hypotheses, observations, and discarded alternatives,
- a failure spans multiple layers, tools, services, adapters, or runtime assumptions,
- future implementation, operations, security, persistence, or architecture work may depend on the findings,
- repeated work would otherwise rediscover the same evidence.

Do not create an investigation for trivial local fixes, obvious compile errors, or conclusions fully captured by a small code change and test.

## Recommended Sections

### Context

State the user request, symptom, failure, or question being investigated.

### Scope

Define what was investigated and what was deliberately left out.

### Evidence

Record relevant commands, files, logs, responses, observations, and dates.
Summarize noisy output instead of pasting long transcripts.

### Findings

List what the evidence shows.
Separate confirmed facts from plausible inferences.

### Root Cause Or Current Explanation

Describe the best-supported explanation.
If root cause is not proven, say so explicitly.

### Options Considered

Document realistic next actions or interpretations and why they were accepted or rejected.

### Decision Or Recommendation

State the recommended next step, if any.
Link to an ADR candidate or decision-log entry when the implication is durable.

### Verification

Record checks performed and their results.
Mention checks not run and why.

### Follow-Up

List remaining risks, unknowns, or future work.

## Persistence Strategy

Write investigation files incrementally, one section at a time, appending each section at the bottom of the file before starting the next. Do not batch multiple sections into a single write operation.

Mechanism:

1. Use the `create` tool to produce the file with the first section (title block and Context).
2. Use the `edit` tool to append each subsequent section at the bottom of the file. Match the last line of existing content and replace it with itself plus the new section text.
3. Persist each section individually before beginning work on the next section.
4. Do not combine sections, even when a section is short.

This approach provides intermediate checkpoints, reduces content loss on failure, and keeps the file reviewable at every step.

## Agent Rules

- Prefer concise evidence over exhaustive transcripts.
- Do not include secrets, tokens, credentials, or unnecessary personal data.
- Do not present speculation as fact.
- Do not replace ADRs or decision-log entries with investigations when a durable decision is being made.
- Link related plans, ADRs, decision-log entries, issues, tests, or source files where useful.
- Follow the Persistence Strategy section for file writing order and mechanism.
