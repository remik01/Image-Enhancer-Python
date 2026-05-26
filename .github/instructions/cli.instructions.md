# CLI Instructions

CLI adapters collect command-line intent, call application use cases, and render results for humans or automation.

## Must Do

- Keep parsing separate from execution.
- Use deterministic output and stable exit codes.
- Make batch behavior non-interactive by default.
- Send user-facing output to stdout and diagnostics/errors to stderr or logs as appropriate.
- Translate CLI input into application commands.
- Report failures clearly without leaking secrets.

## Must Not Do

- Do not put domain rules in CLI parsing/rendering.
- Do not call infrastructure adapters directly when an application use case exists.
- Do not require interactive prompts unless explicitly requested.
- Do not use logs as the only user-visible error output.

## Tests

Test parsing, invalid arguments, exit codes, stdout/stderr behavior, and application failure rendering.

## Checklist

- Is output automation-friendly?
- Are exit codes meaningful?
- Is parsing separate from use-case execution?
- Are errors clear and safe?
