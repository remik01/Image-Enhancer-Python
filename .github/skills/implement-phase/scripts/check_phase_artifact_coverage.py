#!/usr/bin/env python3
"""Compare changed files with a phase's Generated / Modified Artifacts section."""

from __future__ import annotations

import argparse
import sys

from _phase_common import (
    PhaseToolError,
    coverage_result,
    find_repo_root,
    format_coverage,
    git_snapshot,
    resolve_phase,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, help="Workflow phase number, with or without leading zeroes.")
    parser.add_argument("--base", help="Optional git ref to compare changed files against.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero when missing expectations or unexpected files are found.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = find_repo_root()
        phase = resolve_phase(repo_root, args.phase)
        snapshot = git_snapshot(repo_root, args.base)
        result = coverage_result(repo_root, phase, snapshot.changed_files)
    except PhaseToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"# Phase {phase.prefix} Artifact Coverage")
    print()
    print(f"- Phase: {phase.title}")
    print(f"- Changed files considered: {len(result.changed_files)}")
    if snapshot.base:
        print(f"- Compared against: `{snapshot.base}`")
    print()
    print(format_coverage(result))
    print()
    print("Default mode is advisory. Use `--strict` only when the phase artifact contract is known to be precise.")

    if args.strict and (result.missing_labels or result.unexpected_files):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
