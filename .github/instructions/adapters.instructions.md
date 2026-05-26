# Adapter / Infrastructure Instructions

Adapters connect the application to external systems and technical formats. They implement application ports and translate between outside contracts and internal models.

## Must Do

- Implement ports defined by the application layer.
- Keep external DTOs, generated clients, database entities, XML/JSON/Excel records, and HTTP details inside adapter packages.
- Map external data to application/domain types before crossing into the core.
- Validate technical shape at the boundary: readable files, required columns, well-formed XML/JSON, response status, encoding, schema, and required fields.
- Translate technical failures into meaningful application-level exceptions while preserving causes.
- Include diagnostic context in failures: system, action, file path, row, column, element, external id, or HTTP status as relevant.
- Configure timeouts, limits, retry counts, and backoff explicitly.
- Keep adapters observable with useful boundary logs that avoid secrets and excessive payloads.

## Must Not Do

- Do not put business rules in adapters.
- Do not orchestrate use cases inside adapters.
- Do not expose external DTOs through application ports.
- Do not couple infrastructure adapters to UI controls or CLI formatting.
- Do not silently repair malformed external data.
- Do not swallow external failures and return empty/default results.
- Do not use reflection mappers when explicit mapping is reasonable.
- Do not mix unrelated external systems in one adapter class.

## Mapping Rules

- Use explicit field-by-field mapping.
- Preserve source context for mapping errors.
- Delegate semantic validation to domain/application factories or policies.
- Keep mapper methods deterministic and side-effect free.
- Name mappers by source or target, for example `IssueJsonMapper`, `ExcelRowMapper`, or `CustomerEntityMapper`.

## Adapter Types

- File adapters read/write files, validate paths and structure, and report row/element-level failures.
- HTTP/API adapters build requests, apply authentication, enforce timeouts, handle status codes, parse responses, and map payloads.
- Database adapters implement repository ports and translate persistence entities without adding persistence annotations to domain objects unless an ADR allows it.
- Messaging adapters deserialize, validate, call application use cases, and handle idempotency and retry implications explicitly.
- UI/CLI adapters collect user intent, call application use cases, and render application results.

## Tests

Provide focused tests for:

- successful mapping,
- malformed input,
- missing required fields,
- duplicate/conflict handling,
- external error translation,
- deterministic output,
- timeout/retry behavior where practical,
- no silent data loss,
- no secret leakage in errors or logs.

Use realistic boundary samples and local fakes. Automated tests must not depend on production systems, live credentials, VPN, or unstable networks.

## ADR Triggers

Propose ADR discussion for new external systems, new persistence technologies, new retry strategy, new serialization format, shared adapter conventions, or changes to port contracts.

## Checklist

- Which application port is implemented?
- Which external system or format is integrated?
- Where are external DTOs kept?
- Where does mapping happen?
- How are technical errors translated?
- How are timeouts, limits, credentials, and logs handled?
- Which tests prove boundary behavior?
