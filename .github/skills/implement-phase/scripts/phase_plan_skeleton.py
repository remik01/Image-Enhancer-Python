#!/usr/bin/env python3
"""Print a workflow phase implementation plan skeleton."""

from __future__ import annotations

import argparse
import sys

from _phase_common import PhaseToolError, find_repo_root, resolve_phase


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        phase = resolve_phase(repo_root, args.phase)
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    title_slug = phase.title.replace(" And ", " and ")
    print(f"# Phase {phase.number} {title_slug} Implementation Plan")
    print()
    print("## Status")
    print()
    print("Planned.")
    print()
    print("## Context")
    print()
    print(
        f"Phase `{phase.prefix}` implements `{phase.title}` from `{phase.path.relative_to(repo_root).as_posix()}`."
    )
    if phase.tickets:
        print(f"Tickets: {', '.join(phase.tickets)}.")
    print()
    print("## Goal")
    print()
    print(phase.sections.get("Goal", "").strip() or "[Summarize the phase goal.]")
    print()
    print("## Non-Goals")
    print()
    print(phase.sections.get("Out of Scope", "").strip() or "[Summarize out-of-scope items.]")
    print()
    print("## Assumptions")
    print()
    print("[State confirmed project facts and implementation assumptions.]")
    print()
    print("## Rationale")
    print()
    print("[Explain why this implementation path fits the phase, ADRs, boundaries, and tests.]")
    print()
    print("## Trade-offs & Limitations")
    print()
    print("[Record compromises, skipped checks, local-only behavior, or future follow-up.]")
    print()
    print("## Implementation Approach")
    print()
    print("[Describe concrete implementation steps and affected ownership boundaries.]")
    print()
    print("## Affected Layers")
    print()
    print("[List domain/application/adapters/UI/bootstrap/docs/scripts as applicable.]")
    print()
    print("## Tests and Verification")
    print()
    print(phase.sections.get("Testing Expectations", "").strip() or "[List verification commands.]")
    print()
    print("## Risks")
    print()
    print("[Describe risks and how implementation will avoid hiding them.]")
    print()
    print("## ADR / Decision-Log Needs")
    print()
    print(phase.sections.get("ADR / Decision-Log Follow-Up", "").strip() or "[Evaluate ADR and decision-log needs.]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
