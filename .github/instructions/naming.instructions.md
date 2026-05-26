# Naming Instructions

Names should reduce cognitive load and preserve domain meaning.

## Must Do

- Use domain language from specifications, ADRs, and nearby code.
- Name classes by responsibility and layer role.
- Use consistent suffixes: `Command`, `Result`, `Port`, `Repository`, `Mapper`, `Client`, `Controller`, `Configuration`, `Exception`.
- Name methods by behavior and outcome.
- Prefer specific names over generic names.

## Must Not Do

- Do not use vague names such as `Manager`, `Helper`, `Util`, `Processor`, or `Data` without a precise local convention.
- Do not encode adapter technology into domain names.
- Do not rename broadly without explicit refactoring scope.
- Do not use abbreviations unless they are established project language.

## Package Guidance

Packages should reflect layer and responsibility. Avoid `common`, `misc`, and broad utility packages unless a specific convention exists.

## Checklist

- Does the name reveal the concept?
- Is it consistent with nearby code?
- Does it avoid leaking external technology inward?
