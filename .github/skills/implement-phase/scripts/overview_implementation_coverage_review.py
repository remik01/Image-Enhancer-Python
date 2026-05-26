#!/usr/bin/env python3
"""Create or validate whole-project overview implementation coverage review."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path


PLANNING_COLUMNS = [
    "Overview Item ID",
    "Overview Source / Summary",
    "Phase(s) Covering It",
    "Acceptance / Test Evidence",
    "Status",
    "Notes",
]

REQUIRED_COLUMNS = [
    "Overview Item ID",
    "Overview Requirement / Summary",
    "Planning Coverage Evidence",
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
    "- none identified.",
    "n/a",
    "none",
    "none identified.",
    "tbd",
    "todo",
}
PHASE_REF_RE = re.compile(r"\b(?P<number>\d{2,})[_-][A-Za-z0-9_.-]+\.md\b")
IMPLEMENTATION_REVIEW_RE = re.compile(r"_phase-(?P<number>\d{2,})-implementation-coverage-review\.md$")


class CoverageToolError(RuntimeError):
    """Raised when the coverage helper cannot safely continue."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--overview",
        default="workflow/docs/overview.spec.md",
        help="Canonical overview path used for context in the rendered review.",
    )
    parser.add_argument(
        "--overview-coverage",
        default="workflow/phases/_overview-coverage-review.md",
        help="Planning coverage review matrix created by phase-creator.",
    )
    parser.add_argument(
        "--output",
        help="Markdown output path. Defaults to workflow/phases/_overview-implementation-coverage-review.md. Use '-' for stdout.",
    )
    parser.add_argument(
        "--coverage",
        help="Implementation coverage review path to validate. Defaults to the standard output path.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing generated review file.")
    parser.add_argument("--validate", action="store_true", help="Validate an existing overview implementation coverage review.")
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


def find_repo_root(start: Path | None = None) -> Path:
    cwd = start or Path.cwd()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()

    current = cwd.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise CoverageToolError("Could not find repository root.")


def repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def relative_to_repo(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def collapse_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).strip()


def escape_cell(value: str) -> str:
    return collapse_text(value).replace("|", r"\|")


def normalize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`")).strip()


def normalize_status(value: str) -> str:
    normalized = normalize_cell(value)
    return normalized[:1].upper() + normalized[1:] if normalized else normalized


def is_empty(value: str) -> bool:
    return normalize_cell(value).lower() in EMPTY_MARKERS


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


def is_separator_row(line: str) -> bool:
    cells = split_markdown_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def matrix_rows(text: str, columns: list[str]) -> tuple[int, list[dict[str, str]], list[str]]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        cells = [normalize_cell(cell) for cell in split_markdown_row(line)]
        if cells != columns:
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
            if len(values) != len(columns):
                return index + 1, rows, [
                    f"coverage matrix row {row_index + 1} has {len(values)} cells; expected {len(columns)}"
                ]
            rows.append(dict(zip(columns, (value.strip() for value in values), strict=True)))
            row_index += 1
        return index + 1, rows, []
    return 0, [], ["coverage matrix with the required columns was not found"]


def parse_planning_rows(path: Path) -> tuple[int, list[dict[str, str]]]:
    if not path.exists():
        raise CoverageToolError(f"Overview planning coverage review not found: {path}")
    matrix_line, rows, errors = matrix_rows(path.read_text(encoding="utf-8"), PLANNING_COLUMNS)
    if errors:
        detail = "\n".join(f"- {error}" for error in errors)
        raise CoverageToolError(f"Could not read overview planning coverage matrix:\n{detail}")
    return matrix_line, rows


def phase_numbers(value: str) -> list[str]:
    return sorted({match.group("number") for match in PHASE_REF_RE.finditer(value)})


def phase_review_statuses(path: Path) -> Counter[str]:
    if not path.exists():
        return Counter()
    _, rows, errors = matrix_rows(path.read_text(encoding="utf-8"), [
        "Phase Item ID",
        "Phase Section",
        "Phase Requirement / Summary",
        "Implementation Evidence",
        "Verification Evidence",
        "Status",
        "Notes",
    ])
    if errors:
        return Counter({"unreadable": 1})
    return Counter(normalize_status(row["Status"]) for row in rows)


def format_status_counts(counts: Counter[str]) -> str:
    if not counts:
        return "no rows parsed"
    return ", ".join(f"{status}: {counts[status]}" for status in sorted(counts))


def existing_evidence_paths(repo_root: Path, overview_id: str, phases: list[str]) -> list[str]:
    candidates: list[Path] = []
    phase_dir = repo_root / "workflow" / "phases"
    for phase in phases:
        candidates.append(phase_dir / f"_phase-{phase}-implementation-coverage-review.md")

    workflow_patterns = [
        "workflow/logs/phase-*-implementation-log.md",
        "workflow/plans/phase-*.md",
        "workflow/CLI.decision-log.md",
    ]
    for pattern in workflow_patterns:
        candidates.extend(repo_root.glob(pattern))

    token = overview_id.lower()
    matched: list[str] = []
    for path in sorted({candidate for candidate in candidates if candidate.exists()}):
        include = path.name.startswith("_phase-")
        if not include and phases:
            include = any(phase in path.name for phase in phases)
        if not include and token:
            include = token in path.read_text(encoding="utf-8", errors="ignore").lower()
        if include:
            matched.append(relative_to_repo(repo_root, path))
    return matched


def implementation_evidence(repo_root: Path, overview_id: str, phases: list[str]) -> str:
    paths = existing_evidence_paths(repo_root, overview_id, phases)
    if not paths:
        return "TBD"

    lines: list[str] = []
    for path in paths:
        review_match = IMPLEMENTATION_REVIEW_RE.match(Path(path).name)
        if review_match:
            counts = phase_review_statuses(repo_root / path)
            lines.append(f"- `{path}` ({format_status_counts(counts)})")
        else:
            lines.append(f"- `{path}`")
    return "\n".join(lines)


def initial_status(planning_status: str, implementation: str) -> str:
    status = normalize_status(planning_status)
    if status in {"Deferred", "Explicitly out of scope", "Missing"}:
        return status
    if implementation != "TBD":
        return "Needs clarification"
    return "Missing"


def planning_evidence(row: dict[str, str]) -> str:
    phases = normalize_cell(row["Phase(s) Covering It"])
    evidence = normalize_cell(row["Acceptance / Test Evidence"])
    status = normalize_status(row["Status"])
    values = [
        f"Planning status: {status or 'Unspecified'}",
        f"Planning phase coverage: {phases or 'None identified.'}",
        f"Planning acceptance/test evidence: {evidence or 'None identified.'}",
    ]
    return "; ".join(values)


def build_rows(repo_root: Path, planning_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in planning_rows:
        overview_id = normalize_cell(row["Overview Item ID"])
        phases = phase_numbers(row["Phase(s) Covering It"])
        implementation = implementation_evidence(repo_root, overview_id, phases)
        status = initial_status(row["Status"], implementation)
        notes = normalize_cell(row["Notes"])
        if status in {"Covered", "Partially covered"}:
            notes = notes or "Confirm implementation and verification evidence before closure."
        elif status == "Needs clarification":
            notes = "Replace seeded evidence with concrete implementation and verification citations before closure."
        elif status == "Missing":
            notes = notes or "No implementation evidence was discovered for this overview item."

        rows.append(
            {
                "Overview Item ID": overview_id,
                "Overview Requirement / Summary": row["Overview Source / Summary"],
                "Planning Coverage Evidence": planning_evidence(row),
                "Implementation Evidence": implementation,
                "Verification Evidence": "TBD",
                "Status": status,
                "Notes": notes,
            }
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


def render_review(
    repo_root: Path,
    overview_path: Path,
    planning_path: Path,
    planning_matrix_line: int,
    rows: list[dict[str, str]],
) -> str:
    return "\n".join(
        [
            "# Overview Implementation Coverage Review",
            "",
            "## Context",
            "",
            f"Manual review date: {date.today().isoformat()}.",
            "",
            f"Scope: this review checks whether implementation evidence covers `{relative_to_repo(repo_root, overview_path)}`.",
            "",
            f"Planning coverage source: `{relative_to_repo(repo_root, planning_path)}` matrix line {planning_matrix_line}.",
            "",
            "Generated rows are intentionally conservative. Replace `TBD` and open statuses with source, test, command, log, ADR, decision-log, or documentation evidence before final closure.",
            "",
            "Allowed statuses: `Covered`, `Partially covered`, `Deferred`, `Explicitly out of scope`, `Needs clarification`, `Missing`.",
            "",
            "Strict closure validation must use `--strict-open-items` and must fail while any `Missing`, `Partially covered`, or `Needs clarification` rows remain.",
            "",
            "## Coverage Matrix",
            "",
            *render_table(rows),
            "",
            "## Review Findings",
            "",
            "- Replace this line with final residual risks, skipped checks, deferred items, or `None identified.` before closure.",
        ]
    )


def validate_rows(
    rows: list[dict[str, str]],
    allow_missing: bool,
    strict_open_items: bool,
) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["coverage matrix must contain at least one overview item row"]

    item_ids = [normalize_cell(row["Overview Item ID"]) for row in rows]
    for item_id, count in Counter(item_ids).items():
        if not item_id:
            errors.append("coverage matrix contains a row with an empty Overview Item ID")
        elif count > 1:
            errors.append(f"coverage matrix contains duplicate Overview Item ID '{item_id}'")

    for row_number, row in enumerate(rows, start=1):
        item_id = normalize_cell(row["Overview Item ID"]) or f"row {row_number}"
        summary = normalize_cell(row["Overview Requirement / Summary"])
        planning = normalize_cell(row["Planning Coverage Evidence"])
        implementation = normalize_cell(row["Implementation Evidence"])
        verification = normalize_cell(row["Verification Evidence"])
        status = normalize_status(row["Status"])
        notes = normalize_cell(row["Notes"])

        if not summary:
            errors.append(f"{item_id}: Overview Requirement / Summary must not be empty")
        if is_empty(planning):
            errors.append(f"{item_id}: Planning Coverage Evidence must not be empty")
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
        print(f"Overview implementation coverage review not found: {path}")
        return 2

    matrix_line, rows, errors = matrix_rows(path.read_text(encoding="utf-8"), REQUIRED_COLUMNS)
    if not errors:
        errors.extend(
            validate_rows(
                rows=rows,
                allow_missing=allow_missing,
                strict_open_items=strict_open_items,
            )
        )

    if errors:
        print("Overview implementation coverage validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    statuses = Counter(normalize_status(row["Status"]) for row in rows)
    status_summary = ", ".join(f"{status}: {statuses[status]}" for status in sorted(statuses))
    print(
        f"Overview implementation coverage validation passed for {len(rows)} overview item(s) "
        f"from matrix line {matrix_line} ({status_summary})"
    )
    return 0


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        default_output = repo_root / "workflow" / "phases" / "_overview-implementation-coverage-review.md"

        if args.validate:
            review_path = repo_path(repo_root, args.coverage).resolve() if args.coverage else default_output
            return validate_review(review_path, args.allow_missing, args.strict_open_items)

        overview_path = repo_path(repo_root, args.overview).resolve()
        planning_path = repo_path(repo_root, args.overview_coverage).resolve()
        planning_matrix_line, planning_rows = parse_planning_rows(planning_path)
        rows = build_rows(repo_root, planning_rows)
        content = render_review(repo_root, overview_path, planning_path, planning_matrix_line, rows)

        if args.output == "-":
            print(content)
            return 0

        output = repo_path(repo_root, args.output).resolve() if args.output else default_output
        if output.exists() and not args.force:
            raise CoverageToolError(f"Coverage review already exists: {output}. Pass --force to overwrite.")
        write_markdown(output, content)
        print(f"Wrote overview implementation coverage review: {output}")
        return 0
    except CoverageToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
