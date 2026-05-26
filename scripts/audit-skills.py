#!/usr/bin/env python3
"""Audit repository-local Codex skill folders.

The audit is intentionally conservative. It checks deterministic structure and
local references; it does not try to judge whether a skill is semantically good.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9-]+$")
LOCAL_PATH_RE = re.compile(r"`([^`]+)`")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        default=".github/skills",
        help="Directory containing repository-local skill folders.",
    )
    return parser.parse_args()


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def looks_like_local_path(value: str) -> bool:
    if value.startswith(("http://", "https://", "$", "<")):
        return False
    if any(marker in value for marker in (" ", "\n", "*", "...", "<", ">")):
        return False
    if value.startswith(("NN_", "ADR-XXXX")):
        return False
    return (
        value.endswith((".md", ".py", ".ps1", ".yaml", ".yml", ".json", ".xml"))
        or "/" in value
        or "\\" in value
    )


def local_reference_exists(skill_dir: Path, repo_root: Path, reference: str) -> bool:
    normalized = reference.replace("\\", "/").lstrip("/")
    optional_references = {
        "docs/adr",
        "docs/adrs",
        "workflow/CLI.decision-log.md",
        "workflow/docs/overview.spec.md",
    }
    if normalized in optional_references:
        return True
    candidates = [skill_dir / normalized, repo_root / normalized]
    return any(candidate.exists() for candidate in candidates)


def audit_skill(skill_dir: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    readme_file = skill_dir / "README.md"
    if not skill_file.exists():
        return errors

    frontmatter = parse_frontmatter(skill_file)
    expected_name = skill_dir.name
    actual_name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if actual_name != expected_name:
        errors.append(f"{skill_dir}: frontmatter name is '{actual_name}', expected '{expected_name}'")
    if not NAME_RE.match(actual_name):
        errors.append(f"{skill_dir}: skill name must use lowercase letters, digits, and hyphens")
    if len(description) < 40:
        errors.append(f"{skill_dir}: description is missing or too short to trigger reliably")
    if not readme_file.exists():
        errors.append(f"{skill_dir}: missing README.md")

    text = skill_file.read_text(encoding="utf-8")
    for reference in LOCAL_PATH_RE.findall(text):
        if looks_like_local_path(reference) and not local_reference_exists(skill_dir, repo_root, reference):
            errors.append(f"{skill_dir}: local reference does not exist: {reference}")

    return errors


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    skills_root = (repo_root / args.skills_root).resolve()
    if not skills_root.exists():
        print(f"Skill root not found: {skills_root}")
        return 2

    errors: list[str] = []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        errors.extend(audit_skill(skill_dir, repo_root))

    if errors:
        print("Skill audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill audit passed for {skills_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
