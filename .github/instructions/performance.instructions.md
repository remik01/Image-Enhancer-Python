# Performance Instructions

Assume data volume can grow. Prefer scalable, deterministic designs without premature micro-optimization.

## Must Do

- Prefer streaming parsers for large files or unbounded input.
- Avoid repeated parsing, repeated traversal, and avoidable N+1 access patterns.
- Use deterministic ordering for reproducible output.
- Bound memory use when processing large imports, exports, reports, or batches.
- Precompile regex patterns used repeatedly.
- Consider collection initial capacity when size is known and the code remains clear.
- Make concurrency assumptions explicit.

## Must Not Do

- Do not load entire large files into memory when streaming is practical.
- Do not introduce parallelism without clear ownership, ordering, error, and cancellation behavior.
- Do not optimize away readability without evidence.
- Do not cache globally without lifecycle and invalidation rules.

## Tests And Measurement

- Add boundary-size tests for parsers and batch workflows where practical.
- Use deterministic sample data for performance-sensitive behavior.
- Prefer simple measurements or profiling evidence before complex optimization.
- Verify cancellation, timeout, and partial-failure behavior for long-running work.

## ADR Triggers

Propose ADR discussion for concurrency model changes, caching strategy, large-data architecture, indexing strategy, background processing, or performance-related dependencies.
