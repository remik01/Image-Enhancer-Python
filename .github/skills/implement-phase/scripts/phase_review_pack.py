#!/usr/bin/env python3
"""Generate a review evidence pack for a workflow phase implementation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _phase_common import (
    PhaseToolError,
    coverage_result,
    existing_phase_logs,
    find_repo_root,
    format_coverage,
    format_verification_items,
    git_snapshot,
    group_changed_files,
    markdown_bullets,
    markdown_plain_bullets,
    relative_to_repo,
    resolve_phase,
    risk_scan,
    verification_items,
    write_markdown,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    parser.add_argument("--base", help="Optional git ref to compare changed files against.")
    parser.add_argument(
        "--output",
        help="Markdown output path. Defaults to target/phase-context/phase-NN-review-pack.md. Use '-' for stdout.",
    )
    return parser.parse_args()


def render_pack(repo_root: Path, phase_number: str, base: str | None) -> tuple[str, Path]:
    phase = resolve_phase(repo_root, phase_number)
    snapshot = git_snapshot(repo_root, base)
    coverage = coverage_result(repo_root, phase, snapshot.changed_files)
    verification = verification_items(repo_root, phase, snapshot.changed_files)
    phase_logs = existing_phase_logs(repo_root, phase)
    coverage_review = repo_root / "workflow" / "phases" / f"_phase-{phase.prefix}-implementation-coverage-review.md"
    risks = risk_scan(repo_root, snapshot.changed_files)
    grouped = group_changed_files(repo_root, snapshot.changed_files)
    output = repo_root / "target" / "phase-context" / f"phase-{phase.prefix}-review-pack.md"

    lines = [
        f"# Phase {phase.prefix} Review Pack",
        "",
        "## Phase",
        "",
        f"- Phase file: `{relative_to_repo(repo_root, phase.path)}`",
        f"- Title: {phase.title}",
        f"- Tickets: {', '.join(phase.tickets) if phase.tickets else 'None parsed.'}",
        "",
        "## Git Scope",
        "",
        f"- Branch: `{snapshot.branch}`",
        f"- Compared against: `{snapshot.base}`" if snapshot.base else "- Compared against: worktree status",
        f"- Changed files: {len(snapshot.changed_files)}",
        "",
        "### Diff Stat",
        "",
        "```text",
        snapshot.diff_stat or "No diff stat available.",
        "```",
        "",
        "### Changed Files By Area",
        "",
    ]
    if grouped:
        for group, paths in grouped.items():
            lines.append(f"#### {group}")
            lines.append(markdown_bullets(paths))
            lines.append("")
    else:
        lines.append("- No changed files detected.")
        lines.append("")

    lines.extend(
        [
            "## Artifact Coverage",
            "",
            format_coverage(coverage),
            "",
            "## Verification Suggestions",
            "",
            format_verification_items(verification),
            "",
            "## ADR / Decision-Log Checklist",
            "",
        phase.sections.get("ADR / Decision-Log Follow-Up", "") or "Not found.",
        "",
        "## Phase Logs",
        "",
        markdown_bullets(phase_logs),
        "",
        "## Implementation Coverage Review",
        "",
        (
            f"- `{relative_to_repo(repo_root, coverage_review)}`"
            if coverage_review.exists()
            else "- No phase implementation coverage review found."
        ),
        "",
        "## Risk Scan",
            "",
            markdown_plain_bullets(risks, empty="No TODO/FIXME, suppression, skipped-check, or secret-like assignments found in changed text files."),
            "",
            "## Review Notes",
            "",
            "- Confirm implementation stayed within phase scope.",
            "- Confirm skipped checks and environment prerequisites are documented.",
            "- Confirm helper output did not replace source, ADR, and test review.",
        ]
    )
    return "\n".join(lines), output


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        content, default_output = render_pack(repo_root, args.phase, args.base)
        if args.output == "-":
            print(content)
            return 0
        output = Path(args.output).resolve() if args.output else default_output
        write_markdown(output, content)
        print(f"Wrote phase review pack: {output}")
        return 0
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
