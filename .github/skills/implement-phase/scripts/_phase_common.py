#!/usr/bin/env python3
"""Shared helpers for implement-phase scripts."""

from __future__ import annotations

import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


PHASE_FILE_RE = re.compile(r"^(?P<number>\d{2,})[_-].+\.md$")
SECTION_RE_TEMPLATE = r"^##\s+{heading}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)"
BASE_REPO_PATH_ROOTS = (
    ".github",
    "workflow",
    "docs",
    "scripts",
    "config",
    "src",
    "tests",
    "target",
    "build",
    "tools",
)
PATH_SEGMENT_RE = r"(?:[/\\][A-Za-z0-9_.\-\[\]]+)+"
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(password|secret|token|signing[-_. ]?key|api[-_. ]?key)(\s*[:=]\s*)([^\s#]+)"
)

TEXT_SUFFIXES = {
    ".ts",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".xml",
    ".toml",
    ".yml",
    ".yaml",
    ".md",
    ".ps1",
    ".py",
    ".properties",
}


class PhaseToolError(RuntimeError):
    """Raised when a phase helper cannot safely continue."""


@dataclass(frozen=True)
class Phase:
    number: int
    prefix: str
    path: Path
    title: str
    text: str
    sections: dict[str, str]
    tickets: list[str]


@dataclass(frozen=True)
class GitSnapshot:
    branch: str
    status_lines: list[str]
    changed_files: list[str]
    diff_stat: str
    base: str | None


@dataclass(frozen=True)
class ArtifactExpectation:
    label: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class CoverageResult:
    expectations: list[ArtifactExpectation]
    matched_labels: set[str]
    missing_labels: list[str]
    unexpected_files: list[str]
    changed_files: list[str]


@dataclass(frozen=True)
class VerificationItem:
    command: str
    reason: str


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
    raise PhaseToolError("Could not find repository root.")


def git_output(repo_root: Path, args: list[str], allow_failure: bool = False) -> str:
    command = ["git", "-c", f"safe.directory={repo_root.as_posix()}", *args]
    result = subprocess.run(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 and not allow_failure:
        detail = (result.stderr or result.stdout).strip()
        raise PhaseToolError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def normalize_path(value: str) -> str:
    normalized = value.strip().strip("`'\"").rstrip(",;:")
    normalized = normalized.replace("\\", "/")
    if " -> " in normalized:
        normalized = normalized.split(" -> ", 1)[1].strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.lstrip("/")


def expand_changed_path(repo_root: Path, value: str) -> list[str]:
    normalized = normalize_path(value)
    absolute = repo_root / normalized
    if absolute.is_dir():
        return [
            path.relative_to(repo_root).as_posix()
            for path in sorted(absolute.rglob("*"))
            if path.is_file()
        ]
    return [normalized]


def parse_phase_number(value: str) -> tuple[int, str]:
    if not re.fullmatch(r"0*[1-9][0-9]*", value.strip()):
        raise PhaseToolError(f"Phase number must be a positive integer; received '{value}'.")
    number = int(value)
    return number, f"{number:02d}"


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        SECTION_RE_TEMPLATE.format(heading=re.escape(heading)),
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def bullet_items(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        match = re.match(r"^\s*[*-]\s+(.+?)\s*$", line)
        if match:
            items.append(match.group(1).strip())
    return items


def resolve_phase(repo_root: Path, phase_number: str) -> Phase:
    number, prefix = parse_phase_number(phase_number)
    phase_dir = repo_root / "workflow" / "phases"
    if not phase_dir.exists():
        raise PhaseToolError(f"Phase directory not found: {phase_dir}")

    matches: list[Path] = []
    for path in sorted(phase_dir.glob("*.md")):
        match = PHASE_FILE_RE.match(path.name)
        if match and int(match.group("number")) == number:
            matches.append(path)

    if not matches:
        raise PhaseToolError(f"No phase file found for phase {phase_number}.")
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise PhaseToolError(f"Multiple phase files found for phase {phase_number}: {names}")

    path = matches[0]
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not title_match:
        raise PhaseToolError(f"Phase file has no H1 title: {path}")

    headings = [
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
    sections = {heading: section_text(text, heading) for heading in headings}
    tickets = bullet_items(sections.get("Tickets", ""))
    return Phase(
        number=number,
        prefix=prefix,
        path=path,
        title=title_match.group(1).strip(),
        text=text,
        sections=sections,
        tickets=tickets,
    )


def git_snapshot(repo_root: Path, base: str | None = None) -> GitSnapshot:
    branch = git_output(repo_root, ["branch", "--show-current"], allow_failure=True) or "<detached>"
    status_lines = git_output(repo_root, ["status", "--short"], allow_failure=True).splitlines()
    if base:
        changed = git_output(repo_root, ["diff", "--name-only", base], allow_failure=True).splitlines()
        diff_stat = git_output(repo_root, ["diff", "--stat", base], allow_failure=True)
    else:
        changed = []
        for line in status_lines:
            if len(line) >= 4:
                changed.extend(expand_changed_path(repo_root, line[3:]))
        diff_stat = git_output(repo_root, ["diff", "--stat", "HEAD"], allow_failure=True)
    return GitSnapshot(
        branch=branch,
        status_lines=status_lines,
        changed_files=sorted({normalize_path(path) for path in changed if path.strip()}),
        diff_stat=diff_stat,
        base=base,
    )


def path_token_re(repo_root: Path | None = None) -> re.Pattern[str]:
    roots = set(BASE_REPO_PATH_ROOTS)
    if repo_root is not None:
        roots.update(project_path_roots(repo_root))
    root_pattern = "|".join(re.escape(root) for root in sorted(roots, key=lambda item: (-len(item), item)))
    return re.compile(
        r"`(?P<quoted>[^`\n]+)`|"
        rf"(?P<path>(?:{root_pattern}){PATH_SEGMENT_RE}|"
        r"(?:README|USER_MANUAL)\.md|pyproject\.toml)"
    )


def extract_path_tokens(text: str, repo_root: Path | None = None) -> list[str]:
    tokens: list[str] = []
    for match in path_token_re(repo_root).finditer(text):
        token = match.group("quoted") or match.group("path") or ""
        token = normalize_path(token)
        if looks_like_repo_path(token):
            tokens.append(token)
    return sorted(set(tokens))


def looks_like_repo_path(value: str) -> bool:
    if not value or value.startswith(("%", "$", "http://", "https://")):
        return False
    if value in {"build/test"}:
        return False
    if " " in value and "/" not in value and "\\" not in value:
        return False
    return (
        "/" in value
        or value in {"README.md", "USER_MANUAL.md", "pyproject.toml"}
        or value.endswith((".md", ".xml", ".toml", ".yml", ".yaml", ".ps1", ".py", ".properties"))
    )


def artifact_expectations(repo_root: Path, phase: Phase) -> list[ArtifactExpectation]:
    artifacts = phase.sections.get("Generated / Modified Artifacts", "")
    if artifacts.strip() == "None identified.":
        return []

    expectations: dict[str, set[str]] = {}

    def add(label: str, *patterns: str) -> None:
        values = expectations.setdefault(label, set())
        for pattern in patterns:
            values.add(normalize_path(pattern))

    for token in extract_path_tokens(artifacts, repo_root):
        add(token, token)

    lower = artifacts.lower()
    role_patterns = project_role_patterns(repo_root)
    broad_patterns = [
        ("domain artifacts", ("domain",), role_patterns.get("domain", ())),
        ("application artifacts", ("application", "use case", "port"), role_patterns.get("application", ())),
        ("persistence artifacts", ("persistence", "sql", "migration"), role_patterns.get("persistence", ())),
        ("api adapter artifacts", ("api", "http", "route"), role_patterns.get("api", ())),
        ("security artifacts", ("security", "auth", "jwt"), role_patterns.get("security", ())),
        ("bootstrap artifacts", ("bootstrap", "runtime", "settings"), role_patterns.get("bootstrap", ())),
        ("architecture test artifacts", ("architecture", "import boundary"), role_patterns.get("architecture-test", ())),
        ("frontend artifacts", ("frontend", "browser", "client"), role_patterns.get("frontend", ())),
        ("desktop ui artifacts", ("desktop", "ui client"), role_patterns.get("desktop", ())),
        ("script artifacts", ("script", "helper"), ("scripts/",)),
        ("workflow documentation artifacts", ("workflow", "plan", "phase"), ("workflow/",)),
        ("technical documentation artifacts", ("technical documentation",), ("workflow/docs/",)),
        ("decision log artifacts", ("decision-log", "decision log"), ("workflow/CLI.decision-log.md",)),
        ("readme artifacts", ("readme",), ("README.md",)),
        ("user manual artifacts", ("user manual",), ("USER_MANUAL.md",)),
        ("github workflow artifacts", ("github actions", "workflow job", "ci"), (".github/workflows/",)),
        ("skill artifacts", ("skill",), (".github/skills/",)),
    ]
    for label, keywords, patterns in broad_patterns:
        if patterns and any(contains_keyword(lower, keyword) for keyword in keywords):
            add(label, *patterns)

    return [
        ArtifactExpectation(label=label, patterns=tuple(sorted(patterns)))
        for label, patterns in sorted(expectations.items())
    ]


def contains_keyword(text: str, keyword: str) -> bool:
    pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
    return re.search(pattern, text) is not None


def path_matches_expectation(path: str, expectation: ArtifactExpectation) -> bool:
    normalized = normalize_path(path)
    for pattern in expectation.patterns:
        token = normalize_path(pattern)
        if not token:
            continue
        if token.endswith("/"):
            if normalized.startswith(token):
                return True
        elif normalized == token or normalized.startswith(f"{token}/"):
            return True
        elif "/" not in token and Path(normalized).name == token:
            return True
    return False


def coverage_result(repo_root: Path, phase: Phase, changed_files: list[str]) -> CoverageResult:
    expectations = artifact_expectations(repo_root, phase)
    normalized_changed = [normalize_path(path) for path in changed_files if path.strip()]
    matched_labels: set[str] = set()
    unexpected_files: list[str] = []

    for path in normalized_changed:
        matching = [item for item in expectations if path_matches_expectation(path, item)]
        if matching:
            matched_labels.update(item.label for item in matching)
        else:
            unexpected_files.append(path)

    missing_labels = [
        item.label
        for item in expectations
        if item.label not in matched_labels
        and not any(path_matches_expectation(path, item) for path in normalized_changed)
    ]
    return CoverageResult(
        expectations=expectations,
        matched_labels=matched_labels,
        missing_labels=missing_labels,
        unexpected_files=unexpected_files,
        changed_files=normalized_changed,
    )


def python_package_roots(repo_root: Path) -> list[str]:
    roots: set[str] = set()
    src_dir = repo_root / "src"
    if src_dir.exists():
        for path in src_dir.iterdir():
            if path.is_dir() and (path / "__init__.py").exists():
                roots.add(f"src/{path.name}")
    for path in repo_root.iterdir():
        if not path.is_dir() or path.name.startswith("."):
            continue
        if path.name in {"tests", "docs", "scripts", "tools", "workflow", "target", "build"}:
            continue
        if (path / "__init__.py").exists():
            roots.add(path.name)
    if (repo_root / "tests").exists():
        roots.add("tests")
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


def role_roots(repo_root: Path, role: str) -> tuple[str, ...]:
    roots = project_path_roots(repo_root)

    def has(root: str, *tokens: str) -> bool:
        root_tokens = name_tokens(root)
        return any(token in root_tokens for token in tokens)

    matches: list[str] = []
    for root in roots:
        tokens = name_tokens(root)
        if role == "domain" and has(root, "domain"):
            matches.append(root)
        elif role == "application" and has(root, "application"):
            matches.append(root)
        elif role == "persistence" and has(root, "persistence"):
            matches.append(root)
        elif role == "api" and has(root, "api", "rest", "http"):
            matches.append(root)
        elif role == "security" and has(root, "security"):
            matches.append(root)
        elif role == "bootstrap" and has(root, "bootstrap"):
            matches.append(root)
        elif role == "architecture-test" and "architecture" in tokens and ("test" in tokens or "tests" in tokens):
            matches.append(root)
        elif role == "frontend" and has(root, "frontend", "web", "client"):
            matches.append(root)
        elif role == "desktop" and has(root, "desktop", "ui", "client"):
            matches.append(root)
    return tuple(f"{root}/" for root in sorted(set(matches)))


def project_role_patterns(repo_root: Path) -> dict[str, tuple[str, ...]]:
    roles = (
        "domain",
        "application",
        "persistence",
        "api",
        "security",
        "bootstrap",
        "architecture-test",
        "frontend",
        "desktop",
    )
    return {role: role_roots(repo_root, role) for role in roles}


def existing_paths(repo_root: Path, relative_paths: list[str]) -> list[str]:
    return [path for path in relative_paths if (repo_root / path).exists()]


def existing_plans(repo_root: Path, phase: Phase) -> list[str]:
    plan_dir = repo_root / "workflow" / "plans"
    if not plan_dir.exists():
        return []
    phase_patterns = [
        re.compile(rf"phase[-_ ]0*{phase.number}\b", re.IGNORECASE),
        re.compile(re.escape(phase.title).replace(r"\ ", r".*"), re.IGNORECASE),
    ]
    matches: list[str] = []
    for path in sorted(plan_dir.glob("*.md")):
        haystack = path.name.replace("_", "-")
        if any(pattern.search(haystack) for pattern in phase_patterns):
            matches.append(path.relative_to(repo_root).as_posix())
    return matches


def existing_phase_logs(repo_root: Path, phase: Phase) -> list[str]:
    log_dir = repo_root / "workflow" / "logs"
    if not log_dir.exists():
        return []
    patterns = [
        re.compile(rf"phase[-_ ]0*{phase.number}\b", re.IGNORECASE),
        re.compile(re.escape(phase.title).replace(r"\ ", r".*"), re.IGNORECASE),
    ]
    matches: list[str] = []
    for path in sorted(log_dir.glob("*.md")):
        haystack = path.name.replace("_", "-")
        if any(pattern.search(haystack) for pattern in patterns):
            matches.append(path.relative_to(repo_root).as_posix())
    return matches


def list_relative(repo_root: Path, pattern: str, limit: int = 20) -> list[str]:
    return [path.relative_to(repo_root).as_posix() for path in sorted(repo_root.glob(pattern))[:limit]]


def suggested_instruction_files(repo_root: Path, phase: Phase) -> list[str]:
    lower = phase.text.lower()
    suggestions = [
        "AGENTS.md",
        ".github/instructions/work-scope.instructions.md",
        ".github/instructions/planningPersistence.instructions.md",
        ".github/instructions/phases.instructions.md",
        ".github/instructions/review-checklist.instructions.md",
    ]
    keyword_files = [
        (("domain", "invariant", "aggregate"), ".github/instructions/domain.instructions.md"),
        (("python", "pytest", "ruff", "mypy", "pyright"), ".github/instructions/python.instructions.md"),
        (("test", "verification", "regression"), ".github/instructions/tests.instructions.md"),
        (("module", "boundary", "dependency direction"), ".github/instructions/module-boundaries.instructions.md"),
        (("application", "use case", "port"), ".github/instructions/application.instructions.md"),
        (("adapter", "persistence", "sql", "api", "http"), ".github/instructions/adapters.instructions.md"),
        (("mapping", "dto"), ".github/instructions/mapping.instructions.md"),
        (("exception", "problem response", "failure"), ".github/instructions/exceptions.instructions.md"),
        (("log", "logging"), ".github/instructions/logging.instructions.md"),
        (("contract", "schema", "dto", "api"), ".github/instructions/data-contracts.instructions.md"),
        (("security", "auth", "jwt", "secret", "password"), ".github/instructions/security.instructions.md"),
        (("ui", "frontend", "desktop"), ".github/instructions/ui.instructions.md"),
        (("cli", "command-line"), ".github/instructions/cli.instructions.md"),
        (("bootstrap", "runtime", "configuration", "settings"), ".github/instructions/bootstrap.instructions.md"),
        (("operational", "health", "runtime", "deployment"), ".github/instructions/operational-readiness.instructions.md"),
        (("static-analysis", "ruff", "mypy", "pyright", "bandit", "pip-audit", "codeql"), ".github/instructions/static-analysis.instructions.md"),
        (("architecture", "fitness", "import boundary"), ".github/instructions/architecture-fitness.instructions.md"),
        (("adr", "decision log", "decision-log"), ".github/instructions/adr.instructions.md"),
        (("performance", "concurrency", "large input", "benchmark"), ".github/instructions/performance.instructions.md"),
    ]
    for keywords, path in keyword_files:
        if any(keyword in lower for keyword in keywords):
            suggestions.append(path)
    return [path for path in dict.fromkeys(suggestions) if (repo_root / path).exists()]


def runtime_prerequisites(repo_root: Path, phase: Phase) -> list[tuple[str, str]]:
    lower = phase.text.lower()
    candidates: list[tuple[str, str]] = []

    def add(label: str, path: str) -> None:
        status = "present" if (repo_root / path).exists() else "missing"
        candidates.append((label, f"{path} ({status})"))

    def add_role_file(label: str, role: str, file_name: str) -> None:
        for root in role_roots(repo_root, role):
            add(label, f"{root}{file_name}")

    if any(word in lower for word in ("backend", "runtime", "settings", "health")):
        add("Python project metadata", "pyproject.toml")
    if any(word in lower for word in ("database", "migration", "sql")):
        add("Database helper", "scripts/setup-local-database.ps1")
        candidates.append(("Local secrets", "%USERPROFILE%\\<project-local-config-dir>\\prod.properties (not read by this script)"))
    if any(word in lower for word in ("operational validation", "smoke", "runtime validation")):
        add("Operational validation helper", "scripts/run-operational-validation.ps1")
    if "frontend" in lower:
        add_role_file("Frontend client", "frontend", "package.json")
    if "desktop" in lower:
        add_role_file("Desktop client", "desktop", "pyproject.toml")
    return candidates


def changed_packages(repo_root: Path, changed_files: list[str]) -> list[str]:
    modules = set(python_package_roots(repo_root))
    touched = set()
    for path in changed_files:
        normalized = normalize_path(path)
        for module in modules:
            if normalized == module or normalized.startswith(f"{module}/"):
                touched.add(module)
    return sorted(touched)


def verification_items(repo_root: Path, phase: Phase, changed_files: list[str]) -> list[VerificationItem]:
    lower = phase.text.lower()
    changed = [normalize_path(path) for path in changed_files]
    joined = "\n".join(changed).lower()
    items: list[VerificationItem] = []

    def add(command: str, reason: str) -> None:
        if command not in {item.command for item in items}:
            items.append(VerificationItem(command, reason))

    add("git diff --check", "Detect whitespace and conflict-marker issues before review.")

    if any(path.startswith("workflow/phases/") for path in changed):
        add(
            "python .github\\skills\\phase-creator\\scripts\\validate_phase_files.py --phase-dir workflow\\phases",
            "Validate phase-file structure after workflow phase edits.",
        )

    packages = changed_packages(repo_root, changed)
    python_related = (
        any(path.endswith(".py") or path.endswith("pyproject.toml") for path in changed)
        or any(word in lower for word in ("python", "pytest", "ruff", "backend", "api", "desktop"))
    )
    if packages:
        add(
            "python -m pytest",
            "Run tests after touched Python packages or modules.",
        )
    if python_related:
        add("python -m pytest", "Run the Python test suite for Python changes.")

    static_related = python_related or any(
        word in lower or word in joined
        for word in ("ruff", "mypy", "pyright", "bandit", "pip-audit", "static-analysis", "codeql")
    )
    if static_related:
        add("python -m ruff check .", "Run Python lint/static-analysis checks.")
        add("python -m ruff format --check .", "Confirm Python formatting remains clean.")
        add("python -m mypy .", "Run mypy when type-checking contracts may be affected and mypy is configured.")

    frontend_roots = role_roots(repo_root, "frontend")
    frontend_related = "frontend" in lower or any(
        path.startswith(root) for path in changed for root in frontend_roots
    )
    if frontend_related:
        add("npm test", "Run frontend tests when a frontend client exists.")
        add("npm run build", "Run frontend build when a frontend client exists.")

    if any(path.startswith(".github/skills/") for path in changed):
        for skill in sorted({path.split("/")[2] for path in changed if path.startswith(".github/skills/") and len(path.split("/")) > 2}):
            add(
                f"python \"$env:USERPROFILE\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py\" .github\\skills\\{skill}",
                f"Validate the {skill} skill metadata and structure.",
            )
        add(
            "python scripts\\audit-skills.py --skills-root .github\\skills",
            "Run repository-local skill structure audit.",
        )

    operational_related = any(
        word in lower for word in ("operational validation", "runtime", "backend", "smoke")
    ) or any(path.startswith("scripts/") for path in changed)
    if operational_related and (repo_root / "scripts" / "run-operational-validation.ps1").exists():
        add(
            ".\\scripts\\run-operational-validation.ps1 -ValidateOnly",
            "Validate operational helper self-checks without contacting the backend.",
        )

    documentation_related = any(path.endswith(".md") for path in changed) or "documentation" in lower
    if documentation_related:
        add(
            'rg -n "password=|signing-secret=|SQLCMDPASSWORD|BEGIN (RSA|OPENSSH)|sk-[A-Za-z0-9]|AKIA|secret" README.md USER_MANUAL.md workflow docs scripts .github -g "*.md" -g "*.ps1" -g "*.properties"',
            "Scan changed documentation/script areas for obvious secret leakage before closeout.",
        )

    overview_closure_related = (
        "overview implementation coverage" in lower
        or "_overview-implementation-coverage-review" in lower
        or any(path.endswith("_overview-implementation-coverage-review.md") for path in changed)
    )
    if overview_closure_related:
        add(
            "python .github\\skills\\implement-phase\\scripts\\overview_implementation_coverage_review.py --validate --strict-open-items",
            "Validate whole-project overview implementation coverage before final closure.",
        )

    return items


def group_changed_files(repo_root: Path, changed_files: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    project_roots = set(project_path_roots(repo_root))
    for path in changed_files:
        normalized = normalize_path(path)
        first_segment = normalized.split("/", 1)[0]
        if normalized.startswith(".github/skills/"):
            group = ".github/skills"
        elif normalized.startswith(".github/workflows/"):
            group = ".github/workflows"
        elif normalized.startswith("workflow/"):
            group = "workflow"
        elif normalized.startswith("docs/"):
            group = "docs"
        elif normalized.startswith("scripts/"):
            group = "scripts"
        elif any(normalized == root or normalized.startswith(f"{root}/") for root in project_roots):
            group = next(root for root in sorted(project_roots) if normalized == root or normalized.startswith(f"{root}/"))
        else:
            group = first_segment
        groups.setdefault(group, []).append(normalized)
    return {group: sorted(paths) for group, paths in sorted(groups.items())}


def risk_scan(repo_root: Path, changed_files: list[str], limit: int = 80) -> list[str]:
    findings: list[str] = []
    patterns = [
        ("TODO/FIXME", re.compile(r"\b(TODO|FIXME)\b", re.IGNORECASE)),
        ("suppression or skipped check", re.compile(r"#\s*noqa|type:\s*ignore|pyright:\s*ignore|xskip|skip", re.IGNORECASE)),
        ("secret-like assignment", SECRET_VALUE_RE),
    ]
    for relative in changed_files:
        path = repo_root / normalize_path(relative)
        if not path.exists() or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.stat().st_size > 1_000_000:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for label, pattern in patterns:
                if pattern.search(line):
                    redacted = SECRET_VALUE_RE.sub(r"\1\2<redacted>", line.strip())
                    display = f"{normalize_path(relative)}:{line_number}: {label}: {redacted}"
                    findings.append(display)
                    if len(findings) >= limit:
                        return findings
    return findings


def markdown_bullets(values: list[str], empty: str = "None identified.") -> str:
    if not values:
        return f"- {empty}"
    return "\n".join(f"- `{value}`" for value in values)


def markdown_plain_bullets(values: list[str], empty: str = "None identified.") -> str:
    if not values:
        return f"- {empty}"
    return "\n".join(f"- {value}" for value in values)


def format_verification_items(items: list[VerificationItem]) -> str:
    if not items:
        return "- No verification commands suggested by heuristics."
    lines: list[str] = []
    for item in items:
        lines.append(f"- `{item.command}`")
        lines.append(f"  Reason: {item.reason}")
    return "\n".join(lines)


def format_coverage(result: CoverageResult) -> str:
    lines: list[str] = []
    lines.append("### Expected Artifact Ownership")
    if result.expectations:
        for item in result.expectations:
            status = "matched" if item.label in result.matched_labels else "not matched"
            patterns = ", ".join(f"`{pattern}`" for pattern in item.patterns)
            lines.append(f"- {item.label}: {status} ({patterns})")
    else:
        lines.append("- No artifact expectations parsed from the phase section.")

    lines.append("\n### Missing Expected Artifacts")
    lines.append(markdown_plain_bullets(result.missing_labels))
    lines.append("\n### Changed Files Outside Parsed Expectations")
    lines.append(markdown_bullets(result.unexpected_files))
    return "\n".join(lines)


def write_markdown(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path


def relative_to_repo(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()
