#!/usr/bin/env python3
"""Validate the overview-to-phase coverage review matrix."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = [
    "Overview Item ID",
    "Overview Source / Summary",
    "Phase(s) Covering It",
    "Acceptance / Test Evidence",
    "Status",
    "Notes",
]

ALLOWED_STATUSES = {
    "Covered",
    "Partially covered",
    "Deferred",
    "Explicitly out of scope",
    "Needs clarification",
    "Missing",
}

OPEN_ITEM_STATUSES = {"Partially covered", "Needs clarification", "Missing"}
EMPTY_MARKERS = {"", "-", "n/a", "none", "none identified.", "tbd", "todo"}
PHASE_NAME_RE = re.compile(r"\b\d{2,}[_-][A-Za-z0-9_.-]+\.md\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage",
        default="workflow/phases/_overview-coverage-review.md",
        help="Path to the persisted coverage review Markdown file.",
    )
    parser.add_argument(
        "--phase-dir",
        default="workflow/phases",
        help="Directory containing phase files referenced by the coverage matrix.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Allow rows with Status 'Missing' without failing validation.",
    )
    parser.add_argument(
        "--strict-open-items",
        action="store_true",
        help="Fail rows with Status 'Partially covered' or 'Needs clarification' as well as 'Missing'.",
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


def normalize_status(value: str) -> str:
    normalized = normalize_cell(value)
    return normalized[:1].upper() + normalized[1:] if normalized else normalized


def is_separator_row(line: str) -> bool:
    cells = split_markdown_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def extract_matrix(text: str) -> tuple[int, list[dict[str, str]], list[str]]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        cells = [normalize_cell(cell) for cell in split_markdown_row(line)]
        if cells != REQUIRED_COLUMNS:
            continue
        if index + 1 >= len(lines) or not is_separator_row(lines[index + 1]):
            return index + 1, [], ["coverage matrix header is not followed by a Markdown separator row"]

        rows: list[dict[str, str]] = []
        row_index = index + 2
        while row_index < len(lines):
            candidate = lines[row_index]
            if not candidate.strip().startswith("|"):
                break
            values = split_markdown_row(candidate)
            if len(values) != len(REQUIRED_COLUMNS):
                return index + 1, rows, [
                    f"coverage matrix row {row_index + 1} has {len(values)} cells; "
                    f"expected {len(REQUIRED_COLUMNS)}"
                ]
            rows.append(dict(zip(REQUIRED_COLUMNS, (value.strip() for value in values), strict=True)))
            row_index += 1
        return index + 1, rows, []
    return 0, [], ["coverage matrix with the required columns was not found"]


def known_phase_files(phase_dir: Path) -> set[str]:
    if not phase_dir.exists():
        return set()
    return {
        path.name
        for path in phase_dir.glob("*.md")
        if PHASE_NAME_RE.fullmatch(path.name)
    }


def is_empty(value: str) -> bool:
    return normalize_cell(value).lower() in EMPTY_MARKERS


def phase_references(value: str) -> list[str]:
    return PHASE_NAME_RE.findall(value)


def validate_rows(
    rows: list[dict[str, str]],
    phase_files: set[str],
    allow_missing: bool,
    strict_open_items: bool,
) -> list[str]:
    errors: list[str] = []
    if not rows:
        errors.append("coverage matrix must contain at least one overview item row")
        return errors

    item_ids = [normalize_cell(row["Overview Item ID"]) for row in rows]
    for item_id, count in Counter(item_ids).items():
        if not item_id:
            errors.append("coverage matrix contains a row with an empty Overview Item ID")
        elif count > 1:
            errors.append(f"coverage matrix contains duplicate Overview Item ID '{item_id}'")

    for row_number, row in enumerate(rows, start=1):
        item_id = normalize_cell(row["Overview Item ID"]) or f"row {row_number}"
        source = normalize_cell(row["Overview Source / Summary"])
        phases = normalize_cell(row["Phase(s) Covering It"])
        evidence = normalize_cell(row["Acceptance / Test Evidence"])
        status = normalize_status(row["Status"])
        notes = normalize_cell(row["Notes"])

        if not source:
            errors.append(f"{item_id}: Overview Source / Summary must not be empty")

        if status not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            errors.append(f"{item_id}: invalid Status '{status}'; allowed values: {allowed}")
            continue

        refs = phase_references(phases)
        for ref in refs:
            if ref not in phase_files:
                errors.append(f"{item_id}: references phase '{ref}', but it is not present in the phase directory")

        if status in {"Covered", "Partially covered"}:
            if not refs:
                errors.append(f"{item_id}: Status '{status}' must reference at least one phase filename")
            if is_empty(evidence):
                errors.append(f"{item_id}: Status '{status}' requires acceptance or test evidence")

        if status in {"Deferred", "Explicitly out of scope", "Needs clarification", "Missing"} and is_empty(notes):
            errors.append(f"{item_id}: Status '{status}' requires an explanatory Notes value")

        if status == "Missing" and not allow_missing:
            errors.append(f"{item_id}: Status 'Missing' is not allowed without --allow-missing")

        if strict_open_items and status in OPEN_ITEM_STATUSES:
            errors.append(f"{item_id}: Status '{status}' is an open item and strict validation is enabled")

    return errors


def main() -> int:
    args = parse_args()
    coverage_path = Path(args.coverage)
    phase_dir = Path(args.phase_dir)

    if not coverage_path.exists():
        print(f"Coverage review not found: {coverage_path}")
        return 2

    matrix_line, rows, errors = extract_matrix(coverage_path.read_text(encoding="utf-8"))
    if not errors:
        errors.extend(
            validate_rows(
                rows=rows,
                phase_files=known_phase_files(phase_dir),
                allow_missing=args.allow_missing,
                strict_open_items=args.strict_open_items,
            )
        )

    if errors:
        print("Phase coverage validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    statuses = Counter(normalize_status(row["Status"]) for row in rows)
    status_summary = ", ".join(f"{status}: {statuses[status]}" for status in sorted(statuses))
    print(
        f"Phase coverage validation passed for {len(rows)} overview item(s) "
        f"from matrix line {matrix_line} ({status_summary})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
