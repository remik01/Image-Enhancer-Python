#!/usr/bin/env python3
"""Validate workflow phase files for the repository phase contract."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


REQUIRED_SECTIONS = [
    "Goal",
    "Tickets",
    "Features to implement",
    "Constraints",
    "Scope",
    "Out of Scope",
    "Architecture / Boundary Notes",
    "Generated / Modified Artifacts",
    "Testing Expectations",
    "Acceptance Criteria",
    "ADR / Decision-Log Follow-Up",
    "Codex/Copilot Execution Notes",
]

PHASE_NAME_RE = re.compile(r"^\d{2,}[_-].+\.md$")

BASE_KNOWN_ARTIFACT_PATTERNS = [
    (re.compile(r"\.github/workflows/[A-Za-z0-9_.\-/]+"), ".github/workflows/"),
    (re.compile(r"\bpyproject\.toml\b"), "pyproject.toml"),
    (re.compile(r"\bREADME\.md\b"), "README.md"),
    (re.compile(r"\bUSER_MANUAL\.md\b"), "USER_MANUAL.md"),
    (re.compile(r"scripts/[A-Za-z0-9_.\-/]+"), "scripts/"),
    (re.compile(r"workflow/docs/[A-Za-z0-9_.\-/]+"), "workflow/docs/"),
    (re.compile(r"docs/architecture/[A-Za-z0-9_.\-/]+"), "docs/architecture/"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", default="workflow/phases")
    return parser.parse_args()


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return Path.cwd()


def python_package_roots(repo_root: Path) -> list[str]:
    roots: set[str] = set()
    src_dir = repo_root / "src"
    if src_dir.exists():
        for path in src_dir.iterdir():
            if path.is_dir() and (path / "__init__.py").exists():
                roots.add(f"src/{path.name}")
    for path in repo_root.iterdir():
        if path.is_dir() and (path / "__init__.py").exists():
            roots.add(path.name)
    return sorted(roots)


def common_module_prefix(modules: list[str]) -> str | None:
    prefixes = Counter(module.split("-", 1)[0] for module in modules if "-" in module)
    if not prefixes:
        return None
    prefix, count = prefixes.most_common(1)[0]
    return prefix if count >= 2 else None


def project_path_roots(repo_root: Path) -> list[str]:
    modules = set(python_package_roots(repo_root))
    prefix = common_module_prefix(sorted(modules))
    if prefix:
        prefix_marker = f"{prefix}-"
        modules.update(
            path.name
            for path in repo_root.iterdir()
            if path.is_dir() and path.name.startswith(prefix_marker)
        )
    return sorted(modules)


def name_tokens(value: str) -> set[str]:
    return {token for token in re.split(r"[/\\\-_.]+", value.lower()) if token}


def known_artifact_patterns(repo_root: Path) -> list[tuple[re.Pattern[str], str]]:
    patterns = list(BASE_KNOWN_ARTIFACT_PATTERNS)
    for root in project_path_roots(repo_root):
        tokens = name_tokens(root)
        if "architecture" in tokens and ("test" in tokens or "tests" in tokens):
            patterns.append((re.compile(rf"\b{re.escape(root)}\b"), "architecture test module"))
    return patterns


def validate_phase(path: Path, repo_root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not PHASE_NAME_RE.match(path.name):
        errors.append(f"{path}: filename must start with NN_ or NN-")
    if not re.search(r"^#\s+\S", text, re.MULTILINE):
        errors.append(f"{path}: missing H1 title")
    for section in REQUIRED_SECTIONS:
        body = section_text(text, section)
        if not body:
            errors.append(f"{path}: missing or empty section '{section}'")
    artifacts = section_text(text, "Generated / Modified Artifacts")
    if artifacts:
        has_bullet = re.search(r"^\s*[*-]\s+\S", artifacts, re.MULTILINE)
        if artifacts != "None identified." and not has_bullet:
            errors.append(
                f"{path}: Generated / Modified Artifacts must contain bullets or exactly 'None identified.'"
            )
        if artifacts == "None identified." and re.search(r"^\s*[*-]\s+\S", artifacts, re.MULTILINE):
            errors.append(
                f"{path}: Generated / Modified Artifacts cannot mix 'None identified.' with bullets"
            )
        for pattern, required_text in known_artifact_patterns(repo_root):
            text_without_artifacts = text.replace(artifacts, "")
            if pattern.search(text_without_artifacts) and required_text not in artifacts:
                errors.append(
                    f"{path}: references '{required_text}' outside Generated / Modified Artifacts "
                    "but does not classify it there"
                )
    tickets = section_text(text, "Tickets")
    if not re.search(r"^\s*[*-]\s+\S", tickets, re.MULTILINE):
        errors.append(f"{path}: Tickets must contain at least one bullet")
    acceptance = section_text(text, "Acceptance Criteria")
    if not re.search(r"^\s*[*-]\s+\S", acceptance, re.MULTILINE):
        errors.append(f"{path}: Acceptance Criteria must contain at least one bullet")
    follow_up = section_text(text, "ADR / Decision-Log Follow-Up")
    if "ADR:" not in follow_up or "Decision log:" not in follow_up:
        errors.append(f"{path}: ADR / Decision-Log Follow-Up must mention ADR and Decision log")
    notes = section_text(text, "Codex/Copilot Execution Notes")
    verification_markers = ("verification", "python", "pytest", "ruff", "npm", "test", "verify")
    if "AGENTS.md" not in notes or not any(marker in notes.lower() for marker in verification_markers):
        errors.append(f"{path}: execution notes must mention AGENTS.md and a verification command or test")
    return errors


def main() -> int:
    args = parse_args()
    phase_dir = Path(args.phase_dir)
    if not phase_dir.exists():
        print(f"Phase directory not found: {phase_dir}")
        return 2
    repo_root = find_repo_root(phase_dir)

    phase_files = sorted(path for path in phase_dir.glob("*.md") if PHASE_NAME_RE.match(path.name))
    errors: list[str] = []
    for path in phase_files:
        errors.extend(validate_phase(path, repo_root))

    if errors:
        print("Phase validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Phase validation passed for {len(phase_files)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
