# Security Instructions

Security-sensitive work includes credentials, file paths, parsing external input, authentication, authorization, dependency changes, logging, persistence, network calls, and user-provided data.

## Must Do

- Keep secrets out of code, tests, logs, errors, screenshots, and committed config.
- Validate and normalize file paths before reading or writing user-selected locations.
- Avoid unsafe deserialization and reflection-based binding of untrusted input.
- Enforce authentication and authorization boundaries explicitly where relevant.
- Treat external input as untrusted until validated at the boundary.
- Redact sensitive fields in diagnostics.
- Set explicit network timeouts and limits.
- Review dependency additions for overlap, maintenance, licensing, and known risk.

## Must Not Do

- Do not log tokens, passwords, cookies, API keys, connection strings, or full sensitive payloads.
- Do not silently skip authorization checks.
- Do not build file paths through unchecked string concatenation with untrusted input.
- Do not parse untrusted XML with unsafe external entity behavior.
- Do not add cryptography, authentication, or authorization schemes casually.

## Tests

Test path traversal rejection, malformed input handling, redaction, unauthorized access behavior, and safe failure modes where relevant.

## ADR Triggers

Propose ADR discussion for authentication/authorization strategy, secret management, cryptography, security-relevant dependency changes, network trust boundaries, or persisted sensitive data.

## Checklist

- What input is untrusted?
- What data is sensitive?
- Where is access controlled?
- Are secrets protected in logs/errors/tests?
- Are failure modes safe?
