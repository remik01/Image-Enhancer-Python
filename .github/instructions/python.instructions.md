# Python Instructions

Use Python 3.12+ features where they improve clarity, correctness, or maintainability.

## Must Do

- Prefer clear names, explicit invariants, and meaningful types.
- Use type hints for public, architectural, and non-trivial functions.
- Use frozen dataclasses, typed value objects, tuples, or immutable collections for immutable data carriers.
- Use `Protocol` or `abc.ABC` only when an interface stabilizes a real boundary.
- Keep comprehensions and generator expressions simple and side-effect free.
- Move non-trivial logic into named functions, methods, or classes.
- Make collection ownership explicit at boundaries; copy mutable inputs when callers should not retain mutation authority.
- Return empty collections instead of `None` when absence is a normal query result.
- Precompile regex patterns used repeatedly.
- Use docstrings for non-trivial public or architectural modules, classes, functions, and methods.

## Must Not Do

- Do not use modern Python features only for style.
- Do not hide side effects inside comprehensions, generator expressions, or property accessors.
- Do not introduce speculative abstractions.
- Do not weaken typing for convenience.
- Do not perform unrelated cleanup.
- Do not introduce runtime code generation, metaclass tricks, monkeypatching, or dynamic imports unless the project already relies on that pattern and the tradeoff is documented.

## Exceptions And Logging

- Use specific exceptions and preserve original causes with `raise ... from ...` when translating failures.
- Keep domain code free from logging framework dependencies unless an ADR allows otherwise.
- Do not swallow `CancelledError`, `KeyboardInterrupt`, or broad `BaseException`.
- Avoid broad `except Exception` unless the boundary owns failure translation and the handler preserves safe diagnostic context.

## Verification

Before considering a Python change complete:

- relevant tests pass,
- import/package checks pass where available,
- linting and formatting expectations remain satisfied,
- type-checking expectations remain satisfied where configured,
- unrelated code remains untouched.

## Docstrings For Architectural APIs

For non-trivial public or architectural APIs, docstrings should explain dependency intent, not restate imports.

Document:

- why the module, class, function, or method exists in its layer,
- which conceptual collaborators it depends on and why,
- what data enters and leaves the boundary,
- which invariants, ownership rules, or boundary translations it protects,
- what it deliberately does not own.

Do not maintain exhaustive caller/callee lists in docstrings. Prefer generated documentation, package structure, architecture tests, static analysis, and IDE analysis for derivable dependencies.

## Functions, Callables, And Protocols

- Use lambdas only for short local callbacks or transformations.
- Extract named functions when behavior needs branching, validation, exception translation, logging, or multiple statements.
- Use standard callables for local seams; use named protocols or abstract base classes for architectural dependencies.
- Do not hide mutation, I/O, logging, or failure handling inside comprehensions. If order, mutation, or failure handling matters, use explicit control flow.

## Failure Translation

- Translate technical failures at the boundary that owns the dependency: adapters translate external APIs, application services translate port failures, domain code protects invariants.
- Preserve the original cause and include safe context such as operation, format, path, field, or capability.
- Do not wrap exceptions in generic `Exception` or `RuntimeError` just to satisfy a callback.
- Avoid exception handling inside comprehensions and generator expressions. Extract a named function when exception handling is part of the operation.

## Performance

- Treat image bytes, decoded pixels, uploads, and batch operations as potentially large.
- Prefer streaming or bounded processing when reading external data; avoid loading duplicate full-size buffers unless ownership or immutability requires it.
- At module, layer, port, command/result, and DTO mapping boundaries, make mutability explicit with tuples, frozen dataclasses, mapping proxies, or deliberate copies.
- Immutable containers are shallow; protect or copy mutable elements when they can affect invariants.
- Use straightforward loops where performance, exception handling, or mutation order is important.
- Pre-size collections only when the expected size is known and the code remains readable.
- Precompile regex and reusable parsers used repeatedly or inside loops.
- Avoid repeatedly copying large byte arrays across layers. Copy at ownership boundaries, then keep later handoffs explicit.
- Benchmark only code that is plausibly hot; keep optimizations explainable in code or tests.
