#!/usr/bin/env python3
"""Validate structural hygiene for add-phase overview amendments.

The helper is intentionally read-only. It checks the overview requirements table
and optional before/after amendment safety; it does not decide whether new
overview content is semantically meaningful.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIREMENTS_HEADING = "Functional/Nonfunctional Requirements"
TRACKED_AMENDMENT_SECTIONS = [
    "Core Features",
    "Functional/Nonfunctional Requirements",
    "Architecture Or Module Expectations",
    "Persistence / Runtime Assumptions",
    "UI / API Expectations",
    "Assumptions",
    "Weak Points / Uncertainty",
    "ADR / Decision-Log Considerations",
]
REQUIRED_REQUIREMENT_COLUMNS = ["ID", "Type", "Description", "Rationale", "Fit Criterion"]
REQUIREMENT_ID_RE = re.compile(r"^(FR|NFR)-\d{3,}$")


@dataclass(frozen=True)
class RequirementRow:
    """One parsed requirement-table row from the canonical overview."""

    line_number: int
    requirement_id: str
    requirement_type: str
    description: str
    rationale: str
    fit_criterion: str

    @property
    def cells(self) -> tuple[str, str, str, str, str]:
        return (
            self.requirement_id,
            self.requirement_type,
            self.description,
            self.rationale,
            self.fit_criterion,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--overview",
        default="workflow/docs/overview.spec.md",
        help="Path to the amended overview specification.",
    )
    parser.add_argument(
        "--before",
        help="Optional path to the overview before the add-phase amendment.",
    )
    parser.add_argument(
        "--expect-changed",
        action="store_true",
        help="Fail when tracked overview sections did not change from --before.",
    )
    parser.add_argument(
        "--protect-existing-requirements",
        action="store_true",
        help="Fail when requirement rows present in --before are removed or changed.",
    )
    return parser.parse_args()


def split_markdown_row(line: str) -> list[str]:
    content = line.strip()
    if content.startswith("|"):
        content = content[1:]
    if content.endswith("|"):
        content = content[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in content:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    cells.append("".join(current).strip())
    return cells


def normalize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`")).strip()


def is_separator_row(line: str) -> bool:
    cells = split_markdown_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def section_lines(text: str, heading: str) -> tuple[int, list[str]]:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return 0, []
    start_line = text[: match.start("body")].count("\n") + 1
    return start_line, match.group("body").splitlines()


def parse_requirement_rows(text: str) -> tuple[list[RequirementRow], list[str]]:
    start_line, lines = section_lines(text, REQUIREMENTS_HEADING)
    if not lines:
        return [], [f"missing or empty section: {REQUIREMENTS_HEADING}"]

    errors: list[str] = []
    header_index = -1
    for index, line in enumerate(lines):
        cells = [normalize_cell(cell) for cell in split_markdown_row(line)]
        if cells == REQUIRED_REQUIREMENT_COLUMNS:
            header_index = index
            break

    if header_index < 0:
        return [], [
            f"{REQUIREMENTS_HEADING}: missing requirement table header with columns "
            f"{', '.join(REQUIRED_REQUIREMENT_COLUMNS)}"
        ]

    if header_index + 1 >= len(lines) or not is_separator_row(lines[header_index + 1]):
        return [], [f"{REQUIREMENTS_HEADING}: requirement table header must be followed by a separator row"]

    rows: list[RequirementRow] = []
    row_index = header_index + 2
    while row_index < len(lines):
        line = lines[row_index]
        if not line.strip().startswith("|"):
            break
        values = [normalize_cell(value) for value in split_markdown_row(line)]
        line_number = start_line + row_index
        if len(values) != len(REQUIRED_REQUIREMENT_COLUMNS):
            errors.append(
                f"{REQUIREMENTS_HEADING} line {line_number}: expected "
                f"{len(REQUIRED_REQUIREMENT_COLUMNS)} cells, found {len(values)}"
            )
            row_index += 1
            continue
        rows.append(
            RequirementRow(
                line_number=line_number,
                requirement_id=values[0],
                requirement_type=values[1],
                description=values[2],
                rationale=values[3],
                fit_criterion=values[4],
            )
        )
        row_index += 1

    if not rows:
        errors.append(f"{REQUIREMENTS_HEADING}: requirement table must contain at least one row")
    return rows, errors


def validate_requirement_rows(rows: list[RequirementRow]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, int] = {}

    for row in rows:
        if not all(row.cells):
            errors.append(f"line {row.line_number}: requirement cells must not be empty")

        match = REQUIREMENT_ID_RE.fullmatch(row.requirement_id)
        if not match:
            errors.append(
                f"line {row.line_number}: requirement ID '{row.requirement_id}' must match FR-### or NFR-###"
            )
        if row.requirement_type not in {"Functional", "Nonfunctional"}:
            errors.append(
                f"line {row.line_number}: requirement Type must be Functional or Nonfunctional"
            )
        if match and row.requirement_type == "Functional" and match.group(1) != "FR":
            errors.append(
                f"line {row.line_number}: Functional requirement '{row.requirement_id}' must use FR prefix"
            )
        if match and row.requirement_type == "Nonfunctional" and match.group(1) != "NFR":
            errors.append(
                f"line {row.line_number}: Nonfunctional requirement '{row.requirement_id}' must use NFR prefix"
            )

        previous_line = seen.get(row.requirement_id)
        if previous_line is not None:
            errors.append(
                f"line {row.line_number}: duplicate requirement ID '{row.requirement_id}' "
                f"also appears on line {previous_line}"
            )
        else:
            seen[row.requirement_id] = row.line_number

    return errors


def changed_sections(before_text: str, after_text: str) -> list[str]:
    return [
        section
        for section in TRACKED_AMENDMENT_SECTIONS
        if section_text(before_text, section) != section_text(after_text, section)
    ]


def rows_by_id(rows: list[RequirementRow]) -> dict[str, RequirementRow]:
    return {row.requirement_id: row for row in rows}


def compare_requirements(
    before_rows: list[RequirementRow],
    after_rows: list[RequirementRow],
    protect_existing_requirements: bool,
) -> tuple[list[str], list[str], list[str], list[str]]:
    errors: list[str] = []
    before_by_id = rows_by_id(before_rows)
    after_by_id = rows_by_id(after_rows)
    added = sorted(set(after_by_id) - set(before_by_id))
    removed = sorted(set(before_by_id) - set(after_by_id))
    changed = sorted(
        requirement_id
        for requirement_id in set(before_by_id) & set(after_by_id)
        if before_by_id[requirement_id].cells != after_by_id[requirement_id].cells
    )

    if protect_existing_requirements:
        for requirement_id in removed:
            errors.append(f"existing requirement '{requirement_id}' was removed")
        for requirement_id in changed:
            errors.append(f"existing requirement '{requirement_id}' was changed")

    return errors, added, removed, changed


def read_existing_file(path: Path, label: str) -> tuple[str, list[str]]:
    if not path.is_file():
        return "", [f"{label} not found: {path}"]
    return path.read_text(encoding="utf-8"), []


def main() -> int:
    args = parse_args()
    overview_path = Path(args.overview)
    overview_text, errors = read_existing_file(overview_path, "Overview")
    if errors:
        for error in errors:
            print(error)
        return 2

    rows, parse_errors = parse_requirement_rows(overview_text)
    errors.extend(parse_errors)
    errors.extend(validate_requirement_rows(rows))

    before_rows: list[RequirementRow] = []
    added: list[str] = []
    removed: list[str] = []
    changed: list[str] = []
    sections_changed: list[str] = []
    if args.before:
        before_path = Path(args.before)
        before_text, before_errors = read_existing_file(before_path, "Before overview")
        errors.extend(before_errors)
        if not before_errors:
            before_rows, before_parse_errors = parse_requirement_rows(before_text)
            errors.extend(before_parse_errors)
            errors.extend(validate_requirement_rows(before_rows))
            sections_changed = changed_sections(before_text, overview_text)
            if args.expect_changed and not sections_changed:
                errors.append("tracked overview sections did not change from --before")
            compare_errors, added, removed, changed = compare_requirements(
                before_rows,
                rows,
                args.protect_existing_requirements,
            )
            errors.extend(compare_errors)
    elif args.expect_changed:
        errors.append("--expect-changed requires --before")

    if errors:
        print("Overview amendment validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Overview amendment validation passed: {overview_path}")
    print(f"requirements={len(rows)}")
    if args.before:
        print(f"changed_sections={', '.join(sections_changed) if sections_changed else 'none'}")
        print(f"added_requirements={', '.join(added) if added else 'none'}")
        print(f"removed_requirements={', '.join(removed) if removed else 'none'}")
        print(f"changed_requirements={', '.join(changed) if changed else 'none'}")
        print(f"before_requirements={len(before_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
