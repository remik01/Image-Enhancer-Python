#!/usr/bin/env python3
"""Resolve the next workflow phase number and candidate filename."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PHASE_RE = re.compile(r"^(?P<number>\d{2,})[_-].+\.md$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", default="workflow/phases")
    parser.add_argument("--title", required=True, help="Short phase title to normalize into a filename.")
    return parser.parse_args()


def normalize_title(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "".join(word[:1].upper() + word[1:] for word in words) or "NewPhase"


def main() -> int:
    args = parse_args()
    phase_dir = Path(args.phase_dir)
    numbers: list[int] = []
    if phase_dir.exists():
        for path in phase_dir.iterdir():
            match = PHASE_RE.match(path.name)
            if match:
                numbers.append(int(match.group("number")))

    next_number = max(numbers, default=0) + 1
    prefix = f"{next_number:02d}"
    candidate = phase_dir / f"{prefix}_{normalize_title(args.title)}.md"

    print(f"next_number={prefix}")
    print(f"candidate={candidate.as_posix()}")
    if candidate.exists():
        print("status=collision")
        return 1
    print("status=available")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
