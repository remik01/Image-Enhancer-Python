#!/usr/bin/env python3
"""Suggest verification commands for a workflow phase implementation."""

from __future__ import annotations

import argparse
import sys

from _phase_common import (
    PhaseToolError,
    find_repo_root,
    format_verification_items,
    git_snapshot,
    resolve_phase,
    verification_items,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    parser.add_argument("--base", help="Optional git ref to compare changed files against.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        phase = resolve_phase(repo_root, args.phase)
        snapshot = git_snapshot(repo_root, args.base)
        items = verification_items(repo_root, phase, snapshot.changed_files)
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"# Phase {phase.prefix} Verification Suggestions")
    print()
    print(f"- Phase: {phase.title}")
    print(f"- Branch: `{snapshot.branch}`")
    if snapshot.base:
        print(f"- Compared against: `{snapshot.base}`")
    print(f"- Changed files considered: {len(snapshot.changed_files)}")
    print()
    print(format_verification_items(items))
    print()
    print("Review these suggestions against the phase file, source changes, and skipped-check rationale.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
