# UI Instructions

UI adapters collect user intent, call application use cases, and render results. They must not own business rules.

## Must Do

- Keep UI state separate from domain state.
- Convert user input into application commands.
- Render application results and validation errors clearly.
- Keep long-running work off the UI thread.
- Handle cancellation, progress, and failure states where relevant.
- Keep UI replaceable without changing core semantics.

## Must Not Do

- Do not import adapter infrastructure directly when an application use case exists.
- Do not duplicate domain validation in UI code.
- Do not leak UI toolkit or web framework types into domain/application.
- Do not block the UI thread with file, network, or heavy processing.

## Tests

Test presentation logic, command creation, validation rendering, and async state transitions where practical. Keep core behavior covered in domain/application tests.

## Checklist

- Does UI call application use cases?
- Is core logic outside UI code?
- Are long-running operations safe?
- Are errors user-visible and diagnostically useful?
