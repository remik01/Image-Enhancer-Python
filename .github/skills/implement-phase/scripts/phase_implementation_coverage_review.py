#!/usr/bin/env python3
"""Create or validate a per-phase implementation coverage review."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from _phase_common import (
    Phase,
    PhaseToolError,
    artifact_expectations,
    bullet_items,
    find_repo_root,
    git_snapshot,
    markdown_bullets,
    path_matches_expectation,
    relative_to_repo,
    resolve_phase,
    verification_items,
    write_markdown,
)


REQUIRED_COLUMNS = [
    "Phase Item ID",
    "Phase Section",
    "Phase Requirement / Summary",
    "Implementation Evidence",
    "Verification Evidence",
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
EMPTY_MARKERS = {
    "",
    "-",
    "- no matching changed files in compared scope.",
    "- none identified.",
    "n/a",
    "no matching changed files in compared scope.",
    "none",
    "none identified.",
    "tbd",
    "todo",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    parser.add_argument("--base", help="Optional git ref to compare changed files against.")
    parser.add_argument(
        "--output",
        help="Markdown output path. Defaults to workflow/phases/_phase-NN-implementation-coverage-review.md. Use '-' for stdout.",
    )
    parser.add_argument(
        "--coverage",
        help="Coverage review path to validate. Defaults to the phase's standard coverage review path.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing generated review file.")
    parser.add_argument("--validate", action="store_true", help="Validate an existing implementation coverage review.")
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


def default_review_path(repo_root: Path, phase: Phase) -> Path:
    return repo_root / "workflow" / "phases" / f"_phase-{phase.prefix}-implementation-coverage-review.md"


def collapse_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).strip()


def escape_cell(value: str) -> str:
    return collapse_text(value).replace("|", r"\|")


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


def is_empty(value: str) -> bool:
    return normalize_cell(value).lower() in EMPTY_MARKERS


def matrix_rows(text: str) -> tuple[int, list[dict[str, str]], list[str]]:
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


def section_items(phase: Phase, section: str) -> list[str]:
    body = phase.sections.get(section, "").strip()
    if not body or body == "None identified.":
        return []
    items = bullet_items(body)
    return items or [collapse_text(body)]


def add_section_rows(
    rows: list[dict[str, str]],
    phase: Phase,
    section: str,
    code: str,
    note: str,
) -> None:
    for index, item in enumerate(section_items(phase, section), start=1):
        rows.append(
            {
                "Phase Item ID": f"P{phase.prefix}-{code}-{index:03d}",
                "Phase Section": section,
                "Phase Requirement / Summary": item,
                "Implementation Evidence": "TBD",
                "Verification Evidence": "TBD",
                "Status": "Needs clarification",
                "Notes": note,
            }
        )


def build_artifact_rows(repo_root: Path, phase: Phase, changed_files: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    expectations = artifact_expectations(repo_root, phase)
    for index, expectation in enumerate(expectations, start=1):
        matching = [
            path
            for path in changed_files
            if path_matches_expectation(path, expectation)
        ]
        evidence = markdown_bullets(matching, empty="No matching changed files in compared scope.")
        patterns = ", ".join(f"`{pattern}`" for pattern in expectation.patterns)
        rows.append(
            {
                "Phase Item ID": f"P{phase.prefix}-ARTIFACT-{index:03d}",
                "Phase Section": "Generated / Modified Artifacts",
                "Phase Requirement / Summary": f"{expectation.label} ({patterns})",
                "Implementation Evidence": evidence,
                "Verification Evidence": "TBD",
                "Status": "Needs clarification",
                "Notes": "Confirm artifact exists and changed scope satisfies phase ownership.",
            }
        )
    if not expectations:
        rows.append(
            {
                "Phase Item ID": f"P{phase.prefix}-ARTIFACT-001",
                "Phase Section": "Generated / Modified Artifacts",
                "Phase Requirement / Summary": "No artifact expectations parsed from the phase.",
                "Implementation Evidence": "TBD",
                "Verification Evidence": "TBD",
                "Status": "Needs clarification",
                "Notes": "Confirm whether the phase truly owns no concrete artifact changes.",
            }
        )
    return rows


def build_rows(repo_root: Path, phase: Phase, changed_files: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    add_section_rows(
        rows,
        phase,
        "Goal",
        "GOAL",
        "Confirm the implemented behavior satisfies this phase goal.",
    )
    add_section_rows(
        rows,
        phase,
        "Features to implement",
        "FEATURE",
        "Replace with source and test evidence before marking covered.",
    )
    add_section_rows(
        rows,
        phase,
        "Constraints",
        "CONSTRAINT",
        "Confirm implementation does not violate this constraint.",
    )
    add_section_rows(
        rows,
        phase,
        "Scope",
        "SCOPE",
        "Confirm this in-scope item is represented by implementation and tests.",
    )
    add_section_rows(
        rows,
        phase,
        "Out of Scope",
        "OOS",
        "Confirm changed files do not implement this out-of-scope behavior.",
    )
    add_section_rows(
        rows,
        phase,
        "Architecture / Boundary Notes",
        "ARCH",
        "Confirm source dependencies and contracts preserve this boundary note.",
    )
    rows.extend(build_artifact_rows(repo_root, phase, changed_files))
    add_section_rows(
        rows,
        phase,
        "Testing Expectations",
        "TEST",
        "Replace with executed test or documented skipped-check evidence.",
    )
    add_section_rows(
        rows,
        phase,
        "Acceptance Criteria",
        "AC",
        "Do not mark covered without source and verification evidence.",
    )
    add_section_rows(
        rows,
        phase,
        "ADR / Decision-Log Follow-Up",
        "ADR",
        "Confirm required ADR or decision-log action was completed or explicitly deferred.",
    )
    return rows


def render_table(rows: list[dict[str, str]]) -> list[str]:
    lines = [
        "| " + " | ".join(REQUIRED_COLUMNS) + " |",
        "| " + " | ".join("---" for _ in REQUIRED_COLUMNS) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row[column]) for column in REQUIRED_COLUMNS) + " |")
    return lines


def render_review(repo_root: Path, phase: Phase, base: str | None) -> str:
    snapshot = git_snapshot(repo_root, base)
    verification = verification_items(repo_root, phase, snapshot.changed_files)
    rows = build_rows(repo_root, phase, snapshot.changed_files)
    source = relative_to_repo(repo_root, phase.path)
    compared = f"`{snapshot.base}`" if snapshot.base else "worktree status"
    lines = [
        f"# Phase {phase.prefix} Implementation Coverage Review",
        "",
        "## Context",
        "",
        f"Manual review date: {date.today().isoformat()}.",
        "",
        f"Scope: this review checks whether implementation evidence covers `{source}`. "
        "It does not replace source inspection, tests, ADR review, or human judgment.",
        "",
        "Generated rows start as `Needs clarification`. Before closeout, replace each status with an "
        "evidence-backed status and cite source files, tests, commands, logs, ADRs, or decision-log entries.",
        "",
        "Allowed statuses: `Covered`, `Partially covered`, `Deferred`, `Explicitly out of scope`, "
        "`Needs clarification`, `Missing`.",
        "",
        "## Phase",
        "",
        f"- Phase file: `{source}`",
        f"- Title: {phase.title}",
        f"- Tickets: {', '.join(phase.tickets) if phase.tickets else 'None parsed.'}",
        f"- Compared against: {compared}",
        f"- Changed files considered: {len(snapshot.changed_files)}",
        "",
        "## Changed Files",
        "",
        markdown_bullets(snapshot.changed_files),
        "",
        "## Suggested Verification",
        "",
    ]
    if verification:
        for item in verification:
            lines.append(f"- `{item.command}`")
            lines.append(f"  Reason: {item.reason}")
    else:
        lines.append("- No verification commands suggested by heuristics.")
    lines.extend(
        [
            "",
            "## Coverage Matrix",
            "",
            *render_table(rows),
            "",
            "## Review Findings",
            "",
            "- Replace this line with residual risks, skipped checks, or `None identified.` before closeout.",
        ]
    )
    return "\n".join(lines)


def validate_rows(
    rows: list[dict[str, str]],
    allow_missing: bool,
    strict_open_items: bool,
) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["coverage matrix must contain at least one phase item row"]

    item_ids = [normalize_cell(row["Phase Item ID"]) for row in rows]
    for item_id, count in Counter(item_ids).items():
        if not item_id:
            errors.append("coverage matrix contains a row with an empty Phase Item ID")
        elif count > 1:
            errors.append(f"coverage matrix contains duplicate Phase Item ID '{item_id}'")

    for row_number, row in enumerate(rows, start=1):
        item_id = normalize_cell(row["Phase Item ID"]) or f"row {row_number}"
        section = normalize_cell(row["Phase Section"])
        summary = normalize_cell(row["Phase Requirement / Summary"])
        implementation = normalize_cell(row["Implementation Evidence"])
        verification = normalize_cell(row["Verification Evidence"])
        status = normalize_status(row["Status"])
        notes = normalize_cell(row["Notes"])

        if not section:
            errors.append(f"{item_id}: Phase Section must not be empty")
        if not summary:
            errors.append(f"{item_id}: Phase Requirement / Summary must not be empty")
        if status not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            errors.append(f"{item_id}: invalid Status '{status}'; allowed values: {allowed}")
            continue

        if status in {"Covered", "Partially covered"}:
            if is_empty(implementation):
                errors.append(f"{item_id}: Status '{status}' requires implementation evidence")
            if is_empty(verification):
                errors.append(f"{item_id}: Status '{status}' requires verification evidence")

        if status in {"Deferred", "Explicitly out of scope", "Needs clarification", "Missing"} and is_empty(notes):
            errors.append(f"{item_id}: Status '{status}' requires an explanatory Notes value")

        if status == "Missing" and not allow_missing:
            errors.append(f"{item_id}: Status 'Missing' is not allowed without --allow-missing")

        if strict_open_items and status in OPEN_ITEM_STATUSES:
            errors.append(f"{item_id}: Status '{status}' is an open item and strict validation is enabled")

    return errors


def validate_review(path: Path, allow_missing: bool, strict_open_items: bool) -> int:
    if not path.exists():
        print(f"Coverage review not found: {path}")
        return 2

    matrix_line, rows, errors = matrix_rows(path.read_text(encoding="utf-8"))
    if not errors:
        errors.extend(
            validate_rows(
                rows=rows,
                allow_missing=allow_missing,
                strict_open_items=strict_open_items,
            )
        )

    if errors:
        print("Phase implementation coverage validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    statuses = Counter(normalize_status(row["Status"]) for row in rows)
    status_summary = ", ".join(f"{status}: {statuses[status]}" for status in sorted(statuses))
    print(
        f"Phase implementation coverage validation passed for {len(rows)} phase item(s) "
        f"from matrix line {matrix_line} ({status_summary})"
    )
    return 0


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        phase = resolve_phase(repo_root, args.phase)
        default_output = default_review_path(repo_root, phase)

        if args.validate:
            review_path = Path(args.coverage).resolve() if args.coverage else default_output
            return validate_review(review_path, args.allow_missing, args.strict_open_items)

        content = render_review(repo_root, phase, args.base)
        if args.output == "-":
            print(content)
            return 0

        output = Path(args.output).resolve() if args.output else default_output
        if output.exists() and not args.force:
            raise PhaseToolError(f"Coverage review already exists: {output}. Pass --force to overwrite.")
        write_markdown(output, content)
        print(f"Wrote phase implementation coverage review: {output}")
        return 0
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
