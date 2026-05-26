#!/usr/bin/env python3
"""Append structured implementation evidence to a workflow phase log."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from _phase_common import PhaseToolError, find_repo_root, relative_to_repo, resolve_phase


STATUS_HEADING = "Status"
DEFAULT_STATUS = "In progress."
SECTION_BY_EVENT = {
    "context": "Context Read",
    "assumption": "Assumptions",
    "decision": "Decisions During Implementation",
    "action": "Actions Taken",
    "verification": "Verification",
    "failure": "Failures And Remediation",
    "review": "Review Findings Addressed",
    "lesson": "Lessons Learned",
    "note": "Notes",
}
SECTION_ORDER = [
    STATUS_HEADING,
    "Context Read",
    "Assumptions",
    "Decisions During Implementation",
    "Actions Taken",
    "Verification",
    "Failures And Remediation",
    "Review Findings Addressed",
    "Lessons Learned",
    "Notes",
]
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(password|secret|token|signing[-_. ]?key|api[-_. ]?key)(\s*[:=]\s*)([^\s#]+)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    parser.add_argument(
        "--event",
        choices=sorted(SECTION_BY_EVENT),
        help="Type of journal entry to append. Omit with --init or --status-only updates.",
    )
    parser.add_argument("--summary", help="Short human-readable entry summary.")
    parser.add_argument("--details", help="Additional concise evidence or rationale.")
    parser.add_argument("--command", help="Command associated with the entry, when relevant.")
    parser.add_argument("--result", help="Result associated with the entry, for example Passed, Failed, or Skipped.")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Repository-relative file touched or used by the entry. May be passed more than once.",
    )
    parser.add_argument("--status", help="Set the log ## Status section to this exact value.")
    parser.add_argument("--init", action="store_true", help="Create the phase log if it does not already exist.")
    parser.add_argument(
        "--output",
        help="Override log path. Defaults to workflow/logs/phase-NN-implementation-log.md.",
    )
    return parser.parse_args()


def redact(value: str) -> str:
    return SECRET_VALUE_RE.sub(r"\1\2<redacted>", value)


def default_log_path(repo_root: Path, phase_prefix: str) -> Path:
    return repo_root / "workflow" / "logs" / f"phase-{phase_prefix}-implementation-log.md"


def initial_log_content(phase_prefix: str, phase_title: str) -> str:
    lines = [
        f"# Phase {phase_prefix} Implementation Log: {phase_title}",
        "",
    ]
    for heading in SECTION_ORDER:
        lines.append(f"## {heading}")
        lines.append("")
        if heading == STATUS_HEADING:
            lines.append(DEFAULT_STATUS)
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def ensure_log(path: Path, phase_prefix: str, phase_title: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(initial_log_content(phase_prefix, phase_title), encoding="utf-8")


def find_section_bounds(lines: list[str], heading: str) -> tuple[int, int] | None:
    start = -1
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index
            break
    if start < 0:
        return None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def ensure_section(lines: list[str], heading: str) -> list[str]:
    if find_section_bounds(lines, heading) is not None:
        return lines
    if lines and lines[-1].strip():
        lines.append("")
    lines.extend([f"## {heading}", ""])
    return lines


def replace_status(path: Path, status: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = ensure_section(lines, STATUS_HEADING)
    bounds = find_section_bounds(lines, STATUS_HEADING)
    if bounds is None:
        raise PhaseToolError(f"Could not find or create ## {STATUS_HEADING} in {path}")
    start, end = bounds
    updated = lines[: start + 1] + ["", redact(status), ""] + lines[end:]
    path.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")


def format_files(files: list[str]) -> list[str]:
    if not files:
        return []
    lines = ["- Files:"]
    for value in files:
        normalized = value.replace("\\", "/").strip()
        if normalized:
            lines.append(f"  - `{redact(normalized)}`")
    return lines


def format_entry(args: argparse.Namespace) -> list[str]:
    if not args.summary:
        raise PhaseToolError("--summary is required when --event is provided.")

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    lines = [f"### {timestamp} - {redact(args.summary.strip())}", ""]
    lines.append(f"- Event: {args.event}")
    if args.command:
        lines.append(f"- Command: `{redact(args.command.strip())}`")
    if args.result:
        lines.append(f"- Result: {redact(args.result.strip())}")
    lines.extend(format_files(args.file))
    if args.details:
        lines.append(f"- Details: {redact(args.details.strip())}")
    lines.append("")
    return lines


def append_entry(path: Path, heading: str, entry: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = ensure_section(lines, heading)
    bounds = find_section_bounds(lines, heading)
    if bounds is None:
        raise PhaseToolError(f"Could not find or create ## {heading} in {path}")
    _, end = bounds

    insert_at = end
    while insert_at > 0 and not lines[insert_at - 1].strip():
        insert_at -= 1
    updated = lines[:insert_at] + [""] + entry + lines[end:]
    path.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        if not args.init and not args.event and not args.status:
            raise PhaseToolError("Provide --init, --event, or --status.")

        repo_root = find_repo_root()
        phase = resolve_phase(repo_root, args.phase)
        output = Path(args.output).resolve() if args.output else default_log_path(repo_root, phase.prefix)
        ensure_log(output, phase.prefix, phase.title)

        if args.status:
            replace_status(output, args.status)

        if args.event:
            heading = SECTION_BY_EVENT[args.event]
            append_entry(output, heading, format_entry(args))

        print(f"Phase log: {output}")
        if output.is_relative_to(repo_root):
            print(f"Repository path: {relative_to_repo(repo_root, output)}")
        return 0
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
