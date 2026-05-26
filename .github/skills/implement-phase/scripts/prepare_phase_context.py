#!/usr/bin/env python3
"""Prepare a deterministic context pack for workflow phase implementation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _phase_common import (
    PhaseToolError,
    existing_paths,
    existing_phase_logs,
    existing_plans,
    find_repo_root,
    git_snapshot,
    list_relative,
    markdown_bullets,
    markdown_plain_bullets,
    python_package_roots,
    relative_to_repo,
    resolve_phase,
    runtime_prerequisites,
    suggested_instruction_files,
    verification_items,
    write_markdown,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    parser.add_argument(
        "--output",
        help="Markdown output path. Defaults to target/phase-context/phase-NN-context.md.",
    )
    return parser.parse_args()


def render_context(repo_root: Path, phase_number: str) -> tuple[str, Path]:
    phase = resolve_phase(repo_root, phase_number)
    snapshot = git_snapshot(repo_root)
    output = repo_root / "target" / "phase-context" / f"phase-{phase.prefix}-context.md"
    instructions = suggested_instruction_files(repo_root, phase)
    plans = existing_plans(repo_root, phase)
    phase_logs = existing_phase_logs(repo_root, phase)
    adrs = list_relative(repo_root, "docs/adr/ADR-*.md", limit=30)
    investigations = list_relative(repo_root, "workflow/investigations/*.md", limit=30)
    modules = python_package_roots(repo_root)
    scripts = existing_paths(
        repo_root,
        [
            "scripts/run-operational-validation.ps1",
            "scripts/setup-local-database.ps1",
            "scripts/install-local-tomcat.ps1",
            "scripts/deploy-to-local-tomcat.ps1",
            "scripts/verify-phase-10-smoke.ps1",
            "scripts/audit-skills.py",
        ],
    )
    runtime = runtime_prerequisites(repo_root, phase)
    verification = verification_items(repo_root, phase, snapshot.changed_files)

    lines = [
        f"# Phase {phase.prefix} Implementation Context",
        "",
        "## Phase",
        "",
        f"- Phase file: `{relative_to_repo(repo_root, phase.path)}`",
        f"- Title: {phase.title}",
        f"- Tickets: {', '.join(phase.tickets) if phase.tickets else 'None parsed.'}",
        "",
        "## Worktree",
        "",
        f"- Branch: `{snapshot.branch}`",
        f"- Changed files: {len(snapshot.changed_files)}",
        markdown_bullets(snapshot.changed_files),
        "",
        "## Suggested Reading",
        "",
        markdown_bullets(instructions),
        "",
        "## Existing Phase Plans",
        "",
        markdown_bullets(plans),
        "",
        "## Existing Phase Logs",
        "",
        markdown_bullets(phase_logs),
        "",
        "## ADRs And Investigations",
        "",
        "### ADRs",
        markdown_bullets(adrs),
        "",
        "### Investigations",
        markdown_bullets(investigations),
        "",
        "## Parsed Phase Sections",
        "",
        "### Generated / Modified Artifacts",
        phase.sections.get("Generated / Modified Artifacts", "") or "Not found.",
        "",
        "### Acceptance Criteria",
        phase.sections.get("Acceptance Criteria", "") or "Not found.",
        "",
        "### ADR / Decision-Log Follow-Up",
        phase.sections.get("ADR / Decision-Log Follow-Up", "") or "Not found.",
        "",
        "## Repository Shape",
        "",
        "### Python Package Roots",
        markdown_bullets(modules),
        "",
        "### Relevant Scripts",
        markdown_bullets(scripts),
        "",
        "### Runtime Prerequisites Mentioned By Phase",
        markdown_plain_bullets([f"{label}: {value}" for label, value in runtime]),
        "",
        "## Initial Verification Suggestions",
        "",
        "These are heuristic suggestions. Add phase-specific checks after source inspection.",
        "",
        "\n".join(f"- `{item.command}`\n  Reason: {item.reason}" for item in verification)
        if verification
        else "- No verification commands suggested.",
    ]
    return "\n".join(lines), output


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        content, default_output = render_context(repo_root, args.phase)
        output = Path(args.output).resolve() if args.output else default_output
        write_markdown(output, content)
        print(f"Wrote phase context: {output}")
        return 0
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
