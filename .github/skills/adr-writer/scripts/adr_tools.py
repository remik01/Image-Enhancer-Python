#!/usr/bin/env python3
"""Small deterministic helpers for repository ADR files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "Status",
    "Context",
    "Decision",
    "Alternatives Considered",
    "Consequences",
    "Follow-Up Work",
]

ADR_RE = re.compile(r"^ADR-(?P<number>\d{4})-.+\.md$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adr-dir", default="docs/adr")
    parser.add_argument("--next", action="store_true", help="Print the next ADR number.")
    parser.add_argument("--validate", action="store_true", help="Validate existing ADR structure.")
    return parser.parse_args()


def next_adr_number(adr_dir: Path) -> str:
    numbers = []
    if adr_dir.exists():
        for path in adr_dir.iterdir():
            match = ADR_RE.match(path.name)
            if match:
                numbers.append(int(match.group("number")))
    return f"ADR-{max(numbers, default=0) + 1:04d}"


def validate_adr(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not re.search(r"^#\s+ADR-\d{4}:", text, re.MULTILINE):
        errors.append(f"{path}: H1 must start with '# ADR-XXXX:'")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"{path}: missing section '{section}'")
    return errors


def main() -> int:
    args = parse_args()
    adr_dir = Path(args.adr_dir)
    if args.next:
        print(next_adr_number(adr_dir))
    if args.validate:
        errors: list[str] = []
        for path in sorted(adr_dir.glob("ADR-*.md")):
            errors.extend(validate_adr(path))
        if errors:
            print("ADR validation failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"ADR validation passed for {adr_dir}")
    if not args.next and not args.validate:
        print("Specify --next and/or --validate")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
