#!/usr/bin/env python3
"""Validate workflow/docs/overview.spec.md for the repository overview contract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "Source Description",
    "Project Purpose",
    "Main Users Or Actors",
    "Core Features",
    "Functional/Nonfunctional Requirements",
    "Technology Stack",
    "Architecture Or Module Expectations",
    "Persistence / Runtime Assumptions",
    "UI / API Expectations",
    "Assumptions",
    "Weak Points / Uncertainty",
    "ADR / Decision-Log Considerations",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overview", default="workflow/docs/overview.spec.md")
    return parser.parse_args()


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def main() -> int:
    args = parse_args()
    overview = Path(args.overview)
    if not overview.exists():
        print(f"Overview not found: {overview}")
        return 2
    text = overview.read_text(encoding="utf-8")
    errors: list[str] = []
    if not re.search(r"^#\s+Project Overview Specification\s*$", text, re.MULTILINE):
        errors.append("overview H1 must be '# Project Overview Specification'")
    for section in REQUIRED_SECTIONS:
        if not section_text(text, section):
            errors.append(f"missing or empty section: {section}")
    placeholders = text.count("<TO BE FILLED !!!>")

    if errors:
        print("Overview validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Overview validation passed: {overview}")
    print(f"placeholders={placeholders}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
