#!/usr/bin/env python3
"""Generate senior-developer technical documentation for a Python repository.

The script intentionally uses lightweight static inspection. It is meant to
produce a deterministic onboarding evidence pack that an engineer or agent
reviews, not to replace source-level judgment.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import tomllib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


IGNORED_DIRS = {
    ".git",
    ".idea",
    ".venv",
    "venv",
    "env",
    "target",
    "build",
    "dist",
    "out",
    "tools",
    "node_modules",
    ".angular",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}

TODO_RE = re.compile(
    r"(?://|#|<!--|/\*)\s*(TODO|FIXME|HACK|XXX)\b|"
    r"\b(TODO|FIXME|HACK|XXX)\s*[:(]",
    re.IGNORECASE,
)
SECRET_RE = re.compile(
    r"(?i)\b(password|secret|token|api[-_]?key|signing[-_]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_.:/+=-]{8,}"
)
WEB_ROUTE_METHODS = {"get", "post", "put", "patch", "delete", "route", "websocket"}
CLI_DECORATORS = {"command", "callback"}


@dataclass(frozen=True)
class PythonProject:
    path: Path
    name: str
    version: str
    dependencies: list[str] = field(default_factory=list)
    optional_dependencies: dict[str, list[str]] = field(default_factory=dict)
    scripts: dict[str, str] = field(default_factory=dict)
    tools: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PythonModule:
    relative_path: str
    package: str
    imports: list[str]
    line_count: int
    is_test: bool
    has_main_guard: bool


@dataclass(frozen=True)
class PythonSymbol:
    relative_path: str
    package: str
    kind: str
    name: str
    decorators: list[str]
    line_number: int
    is_test: bool


@dataclass(frozen=True)
class Endpoint:
    module: str
    handler: str
    method: str
    path: str
    source: str


@dataclass(frozen=True)
class TypeScriptSymbol:
    project: str
    relative_path: str
    kind: str
    name: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--output",
        default="workflow/docs/technical-documentation.md",
        help="Markdown file to write.",
    )
    parser.add_argument(
        "--max-source-lines",
        type=int,
        default=450,
        help="Line-count threshold used for large-file smell prompts.",
    )
    return parser.parse_args()


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_pyproject(root: Path) -> PythonProject | None:
    path = root / "pyproject.toml"
    if not path.exists():
        return None
    try:
        data = tomllib.loads(read_text(path))
    except tomllib.TOMLDecodeError:
        return None

    project = data.get("project", {})
    tools = sorted(data.get("tool", {}).keys())
    optional_dependencies = {
        str(name): [str(item) for item in values]
        for name, values in project.get("optional-dependencies", {}).items()
        if isinstance(values, list)
    }
    return PythonProject(
        path=path,
        name=str(project.get("name") or root.name),
        version=str(project.get("version") or ""),
        dependencies=[str(item) for item in project.get("dependencies", [])],
        optional_dependencies=optional_dependencies,
        scripts={str(name): str(value) for name, value in project.get("scripts", {}).items()},
        tools=tools,
    )


def package_name(root: Path, path: Path) -> str:
    relative = path.relative_to(root)
    if relative.parts and relative.parts[0] == "src" and len(relative.parts) > 1:
        parts = relative.parts[1:-1]
    else:
        parts = relative.parts[:-1]
    module = path.stem
    if module != "__init__":
        parts = (*parts, module)
    return ".".join(part for part in parts if part)


def decorator_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = decorator_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return decorator_name(node.func)
    return ""


def literal_string_arg(node: ast.AST) -> str:
    if isinstance(node, ast.Call) and node.args:
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            return first.value
    return ""


def import_names(tree: ast.AST) -> list[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return sorted(names)


def has_main_guard(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        comparison = node.test
        if not isinstance(comparison, ast.Compare):
            continue
        left = comparison.left
        comparators = comparison.comparators
        if (
            isinstance(left, ast.Name)
            and left.id == "__name__"
            and comparators
            and isinstance(comparators[0], ast.Constant)
            and comparators[0].value == "__main__"
        ):
            return True
    return False


def parse_python(root: Path) -> tuple[list[PythonModule], list[PythonSymbol], list[Endpoint]]:
    modules: list[PythonModule] = []
    symbols: list[PythonSymbol] = []
    endpoints: list[Endpoint] = []

    for path in sorted(iter_files(root)):
        if path.suffix != ".py":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        try:
            tree = ast.parse(text, filename=relative)
        except SyntaxError:
            modules.append(
                PythonModule(
                    relative_path=relative,
                    package=package_name(root, path),
                    imports=[],
                    line_count=text.count("\n") + 1,
                    is_test=is_test_path(relative),
                    has_main_guard=False,
                )
            )
            continue

        module_name = package_name(root, path)
        module_imports = import_names(tree)
        module = PythonModule(
            relative_path=relative,
            package=module_name,
            imports=module_imports,
            line_count=text.count("\n") + 1,
            is_test=is_test_path(relative),
            has_main_guard=has_main_guard(tree),
        )
        modules.append(module)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                decorators = sorted({decorator_name(item) for item in node.decorator_list if decorator_name(item)})
                symbols.append(
                    PythonSymbol(
                        relative_path=relative,
                        package=module_name,
                        kind="class",
                        name=node.name,
                        decorators=decorators,
                        line_number=node.lineno,
                        is_test=module.is_test,
                    )
                )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                decorators = sorted({decorator_name(item) for item in node.decorator_list if decorator_name(item)})
                kind = "async function" if isinstance(node, ast.AsyncFunctionDef) else "function"
                symbols.append(
                    PythonSymbol(
                        relative_path=relative,
                        package=module_name,
                        kind=kind,
                        name=node.name,
                        decorators=decorators,
                        line_number=node.lineno,
                        is_test=module.is_test,
                    )
                )
                for decorator in node.decorator_list:
                    name = decorator_name(decorator)
                    method = name.rsplit(".", 1)[-1].upper()
                    if method.lower() in WEB_ROUTE_METHODS:
                        endpoints.append(
                            Endpoint(
                                module=module_name,
                                handler=node.name,
                                method=method,
                                path=literal_string_arg(decorator) or "(dynamic)",
                                source=relative,
                            )
                        )
                    elif name.rsplit(".", 1)[-1] in CLI_DECORATORS:
                        endpoints.append(
                            Endpoint(
                                module=module_name,
                                handler=node.name,
                                method="CLI",
                                path=name,
                                source=relative,
                            )
                        )

    return modules, symbols, endpoints


def is_test_path(relative: str) -> bool:
    parts = relative.split("/")
    return (
        "tests" in parts
        or Path(relative).name.startswith("test_")
        or Path(relative).name.endswith("_test.py")
    )


def parse_ts_symbols(root: Path) -> list[TypeScriptSymbol]:
    symbol_re = re.compile(
        r"^\s*export\s+(?:abstract\s+)?(?P<kind>class|interface|type|enum)\s+"
        r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)",
        re.MULTILINE,
    )
    symbols: list[TypeScriptSymbol] = []
    for path in sorted(iter_files(root)):
        if path.suffix != ".ts":
            continue
        relative = path.relative_to(root)
        project = relative.parts[0] if len(relative.parts) > 1 else "."
        text = read_text(path)
        for match in symbol_re.finditer(text):
            symbols.append(
                TypeScriptSymbol(
                    project=project,
                    relative_path=relative.as_posix(),
                    kind=match.group("kind"),
                    name=match.group("name"),
                )
            )
    return symbols


def parse_package_json(root: Path) -> dict[str, dict[str, str]]:
    package_files = sorted(iter_files(root), key=lambda path: path.as_posix())
    results: dict[str, dict[str, str]] = {}
    for path in package_files:
        if path.name != "package.json":
            continue
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        deps: dict[str, str] = {}
        for section in ("dependencies", "devDependencies"):
            for name, version in data.get(section, {}).items():
                deps[f"{name} ({section})"] = str(version)
        results[path.parent.relative_to(root).as_posix()] = deps
    return results


def detect_smells(
    root: Path,
    modules: list[PythonModule],
    symbols: list[PythonSymbol],
    max_source_lines: int,
) -> list[str]:
    smells: list[str] = []
    duplicate_names = [
        name
        for name, count in Counter(symbol.name for symbol in symbols if symbol.kind == "class").items()
        if count > 1
    ]
    for name in sorted(duplicate_names):
        sources = sorted(symbol.relative_path for symbol in symbols if symbol.name == name)
        smells.append(f"Duplicate Python class name `{name}` appears in: {', '.join(sources)}")

    test_stems = {Path(module.relative_path).stem.removeprefix("test_") for module in modules if module.is_test}
    for module in sorted((item for item in modules if not item.is_test), key=lambda item: item.relative_path):
        if module.line_count > max_source_lines:
            smells.append(f"Large Python module `{module.relative_path}` has {module.line_count} lines.")
        stem = Path(module.relative_path).stem
        if stem not in {"__init__", "__main__"} and stem not in test_stems:
            if not module.relative_path.startswith((".github/", "scripts/", "tools/")):
                smells.append(f"No nearby test module detected for `{module.relative_path}`.")
        if ".domain" in f".{module.package}.":
            forbidden = [
                name
                for name in module.imports
                if name.split(".", 1)[0]
                in {"fastapi", "flask", "django", "sqlalchemy", "requests", "httpx", "tkinter", "PySide6", "PyQt6"}
            ]
            if forbidden:
                smells.append(
                    f"Domain module `{module.relative_path}` imports framework/adapter APIs: {', '.join(forbidden)}"
                )

    for path in sorted(iter_files(root)):
        if path.suffix not in {".py", ".ts", ".html", ".css", ".md", ".toml", ".yml", ".yaml"}:
            continue
        text = read_text(path)
        relative = path.relative_to(root).as_posix()
        if TODO_RE.search(text):
            smells.append(f"TODO/FIXME-style marker found in `{relative}`.")
        if path.suffix == ".py" and has_broad_exception_handler(path, text):
            smells.append(f"Broad exception handler found in `{relative}`.")
        if path.suffix == ".py" and has_module_mutable_global(text):
            smells.append(f"Module-level mutable global candidate found in `{relative}`.")
        if SECRET_RE.search(text):
            smells.append(f"Secret-like assignment candidate found in `{relative}`.")

    return sorted(set(smells))


def has_broad_exception_handler(path: Path, text: str) -> bool:
    try:
        tree = ast.parse(text, filename=path.as_posix())
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                return True
            if isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
                return True
    return False


def has_module_mutable_global(text: str) -> bool:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            return True
        if isinstance(node, ast.AnnAssign) and isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            return True
    return False


def collect_docs(root: Path) -> dict[str, list[str]]:
    patterns = {
        "ADRs": ["docs/adr/*.md"],
        "Workflow plans": ["workflow/plans/*.md"],
        "Workflow phases": ["workflow/phases/*.md"],
        "Workflow logs": ["workflow/logs/*.md"],
        "Investigations": ["workflow/investigations/*.md"],
        "Project docs": ["README.md", "docs/*.md", "docs/api/*.md", "workflow/CLI.decision-log.md"],
    }
    docs: dict[str, list[str]] = {}
    for label, globs in patterns.items():
        paths: list[str] = []
        for pattern in globs:
            paths.extend(path.relative_to(root).as_posix() for path in root.glob(pattern) if path.is_file())
        docs[label] = sorted(set(paths))
    return docs


def first_heading(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.exists():
        return ""
    for line in read_text(path).splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def render_list(items: Iterable[str], empty: str = "None detected.") -> list[str]:
    rendered = [f"- {item}" for item in items]
    return rendered or [f"- {empty}"]


def render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["None detected."]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("\n", " ") for cell in row) + " |")
    return lines


def summarize_data_flow(
    modules: list[PythonModule],
    endpoints: list[Endpoint],
    has_frontend_project: bool,
) -> list[str]:
    package_names = {module.package for module in modules}
    flow: list[str] = []
    if has_frontend_project:
        flow.append("Frontend files provide browser workflow and call API/client boundaries from TypeScript or JS.")
    if endpoints:
        endpoint_summary = ", ".join(f"{endpoint.method} {endpoint.path}" for endpoint in endpoints[:12])
        flow.append(f"Detected route or command handlers: {endpoint_summary}.")
    if any(".application" in f".{name}." for name in package_names):
        flow.append("Application modules receive commands, validate orchestration input, and call ports.")
    if any(".domain" in f".{name}." for name in package_names):
        flow.append("Domain modules represent business concepts and protect invariants.")
    if any(".adapter" in f".{name}." or ".adapters" in f".{name}." for name in package_names):
        flow.append("Adapters translate external or technical concerns into application ports and results.")
    if any(".bootstrap" in f".{name}." for name in package_names):
        flow.append("Bootstrap modules assemble runtime dependencies and validate configuration.")
    return flow


def write_markdown(
    root: Path,
    output: Path,
    project: PythonProject | None,
    modules: list[PythonModule],
    symbols: list[PythonSymbol],
    endpoints: list[Endpoint],
    ts_symbols: list[TypeScriptSymbol],
    npm_dependencies: dict[str, dict[str, str]],
    docs: dict[str, list[str]],
    smells: list[str],
) -> None:
    lines: list[str] = []
    lines.extend(
        [
            "# Technical Documentation",
            "",
            "> Generated by `.github/skills/technical-documentation/scripts/generate_technical_documentation.py`.",
            "> Review this document against ADRs, source code, and tests before treating it as authoritative.",
            "",
            "## Project Identity",
            "",
            f"- Repository: `{root.name}`",
            f"- Python project: `{project.name if project else 'not detected'}`",
            f"- Version: `{project.version if project and project.version else 'not detected'}`",
            f"- Tool configuration: {', '.join(f'`{tool}`' for tool in project.tools) if project and project.tools else '`not detected`'}",
        ]
    )
    if project and project.scripts:
        lines.append(
            "- Console scripts: "
            + ", ".join(f"`{name}` -> `{target}`" for name, target in sorted(project.scripts.items()))
        )
    if npm_dependencies:
        lines.append(f"- npm workspaces/projects detected: {', '.join(f'`{name}`' for name in npm_dependencies)}")

    lines.extend(["", "## Governance And Existing Docs", ""])
    for label, paths in docs.items():
        if not paths:
            continue
        lines.append(f"### {label}")
        for relative in paths:
            heading = first_heading(root, relative)
            suffix = f" - {heading}" if heading else ""
            lines.append(f"- `{relative}`{suffix}")
        lines.append("")

    lines.extend(["## Python Dependencies", ""])
    dependencies = project.dependencies if project else []
    lines.extend(render_list(f"`{item}`" for item in dependencies))
    if project and project.optional_dependencies:
        lines.append("")
        lines.append("### Optional Dependency Groups")
        for group, values in sorted(project.optional_dependencies.items()):
            lines.append(f"- `{group}`: {', '.join(f'`{value}`' for value in values) or 'empty'}")
    lines.append("")

    if npm_dependencies:
        lines.extend(["## Frontend / npm Dependencies", ""])
        for project_name, deps in sorted(npm_dependencies.items()):
            lines.append(f"### `{project_name}`")
            lines.extend(render_list(f"`{name}` {version}" for name, version in sorted(deps.items())))
            lines.append("")

    lines.extend(["## Package, Module, And Symbol Structure", ""])
    package_counts = Counter(module.package.rsplit(".", 1)[0] or "(root)" for module in modules)
    lines.extend(render_list(f"`{package}`: {count} module(s)" for package, count in sorted(package_counts.items())))
    lines.append("")
    rows = [
        [
            f"`{module.relative_path}`",
            module.package or "(root)",
            "test" if module.is_test else "main",
            str(module.line_count),
            ", ".join(f"`{name}`" for name in module.imports[:8]) or "-",
        ]
        for module in sorted(modules, key=lambda item: item.relative_path)
    ]
    lines.extend(render_table(["Source", "Module", "Set", "Lines", "Imports"], rows))
    lines.append("")

    lines.append("### Classes And Functions")
    symbol_rows = [
        [
            symbol.kind,
            f"`{symbol.name}`",
            symbol.package or "(root)",
            f"`{symbol.relative_path}:{symbol.line_number}`",
            ", ".join(f"`@{decorator}`" for decorator in symbol.decorators[:6]) or "-",
        ]
        for symbol in sorted(symbols, key=lambda item: (item.relative_path, item.line_number))
    ]
    lines.extend(render_table(["Kind", "Name", "Module", "Source", "Decorators"], symbol_rows))
    lines.append("")

    if ts_symbols:
        lines.extend(["## TypeScript Structure", ""])
        by_project: dict[str, list[TypeScriptSymbol]] = defaultdict(list)
        for symbol in ts_symbols:
            by_project[symbol.project].append(symbol)
        for project_name, project_symbols in sorted(by_project.items()):
            lines.append(f"### `{project_name}`")
            rows = [
                [symbol.kind, f"`{symbol.name}`", f"`{symbol.relative_path}`"]
                for symbol in sorted(project_symbols, key=lambda item: (item.relative_path, item.name))
            ]
            lines.extend(render_table(["Kind", "Symbol", "Source"], rows))
            lines.append("")

    lines.extend(["## Use Cases, Routes, Commands, And Entry Points", ""])
    endpoint_rows = [
        [
            endpoint.method,
            f"`{endpoint.path}`",
            endpoint.handler,
            f"`{endpoint.module}`",
            f"`{endpoint.source}`",
        ]
        for endpoint in endpoints
    ]
    lines.extend(render_table(["Kind", "Path/Decorator", "Handler", "Module", "Source"], endpoint_rows))
    lines.append("")

    lines.append("### Entry Point Candidates")
    entry_points = []
    if project:
        entry_points.extend(f"`{name}` -> `{target}` from `pyproject.toml`" for name, target in sorted(project.scripts.items()))
    entry_points.extend(f"`{module.relative_path}` has `if __name__ == \"__main__\"`" for module in modules if module.has_main_guard)
    lines.extend(render_list(sorted(set(entry_points))))
    lines.append("")

    lines.extend(["## Rough Data Flow", ""])
    lines.extend(render_list(summarize_data_flow(modules, endpoints, bool(npm_dependencies))))
    lines.append("")

    lines.extend(["## Untypical Solutions, Smells, And Review Prompts", ""])
    lines.extend(render_list(smells))
    lines.append("")

    lines.extend(
        [
            "## Recommended Reading Order",
            "",
            "1. `README.md` for local run and verification commands.",
            "2. `workflow/docs/overview.spec.md` for product intent and unresolved assumptions.",
            "3. `docs/adr/` for accepted architectural direction.",
            "4. `workflow/plans/`, `workflow/phases/`, and `workflow/logs/` for implementation sequencing, scope, and curated phase evidence.",
            "5. Domain and application packages before adapters, UI, and bootstrap.",
            "6. Architecture fitness and package tests before changing dependency direction.",
            "",
            "## Generator Limits",
            "",
            "- Static AST/TOML inspection cannot prove runtime behavior or architecture correctness.",
            "- Route and command detection is best-effort and may miss dynamically composed registrations.",
            "- Smell prompts are review leads; they are not automatic defects.",
            "- Generated data flow is inferred from package names and detected decorators.",
            "",
        ]
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output

    project = parse_pyproject(root)
    modules, symbols, endpoints = parse_python(root)
    ts_symbols = parse_ts_symbols(root)
    npm_dependencies = parse_package_json(root)
    docs = collect_docs(root)
    smells = detect_smells(root, modules, symbols, args.max_source_lines)

    write_markdown(
        root=root,
        output=output,
        project=project,
        modules=modules,
        symbols=symbols,
        endpoints=endpoints,
        ts_symbols=ts_symbols,
        npm_dependencies=npm_dependencies,
        docs=docs,
        smells=smells,
    )
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
