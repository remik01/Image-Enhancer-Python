from __future__ import annotations

import ast
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = PROJECT_ROOT / "src" / "image_workbench"

FORBIDDEN_CORE_IMPORT_PREFIXES = (
    "PIL",
    "PyQt6",
    "PySide6",
    "cv2",
    "fastapi",
    "httpx",
    "openai",
    "pydantic",
    "requests",
    "sqlalchemy",
)

LAYER_FORBIDDEN_PREFIXES = {
    "domain": (
        "image_workbench.adapters",
        "image_workbench.application",
        "image_workbench.bootstrap",
        "image_workbench.cli",
        "image_workbench.plugins",
        "image_workbench.ui",
        *FORBIDDEN_CORE_IMPORT_PREFIXES,
    ),
    "application": (
        "image_workbench.adapters",
        "image_workbench.bootstrap",
        "image_workbench.cli",
        "image_workbench.plugins",
        "image_workbench.ui",
        *FORBIDDEN_CORE_IMPORT_PREFIXES,
    ),
    "adapters": (
        "image_workbench.bootstrap",
        "image_workbench.cli",
        "image_workbench.plugins",
        "image_workbench.ui",
    ),
}


@dataclass(frozen=True)
class ImportViolation:
    module_path: Path
    imported_name: str
    reason: str

    def describe(self) -> str:
        relative_path = self.module_path.relative_to(PROJECT_ROOT)
        return f"{relative_path}: imports {self.imported_name!r}: {self.reason}"


def test_core_layers_do_not_import_forbidden_technical_dependencies() -> None:
    violations = find_import_violations(PACKAGE_ROOT)

    assert violations == [], "\n".join(violation.describe() for violation in violations)


def test_architecture_scanner_flags_forbidden_core_layer_imports(tmp_path: Path) -> None:
    package_root = tmp_path / "image_workbench"
    domain_root = package_root / "domain"
    domain_root.mkdir(parents=True)
    (package_root / "__init__.py").write_text("", encoding="utf-8")
    (domain_root / "__init__.py").write_text("", encoding="utf-8")
    forbidden_module = domain_root / "invalid_import.py"
    forbidden_module.write_text("import image_workbench.adapters\n", encoding="utf-8")

    violations = find_import_violations(package_root)

    assert violations
    assert violations[0].imported_name == "image_workbench.adapters"


def find_import_violations(package_root: Path) -> list[ImportViolation]:
    violations: list[ImportViolation] = []
    for module_path in sorted(package_root.rglob("*.py")):
        layer_name = resolve_layer_name(package_root, module_path)
        if layer_name is None:
            continue
        forbidden_prefixes = LAYER_FORBIDDEN_PREFIXES.get(layer_name, ())
        for imported_name in iter_imported_names(module_path):
            matched_prefix = find_matching_prefix(imported_name, forbidden_prefixes)
            if matched_prefix is None:
                continue
            violations.append(
                ImportViolation(
                    module_path=module_path,
                    imported_name=imported_name,
                    reason=f"{layer_name} layer must not depend on {matched_prefix}",
                )
            )
    return violations


def resolve_layer_name(package_root: Path, module_path: Path) -> str | None:
    relative_parts = module_path.relative_to(package_root).parts
    if not relative_parts:
        return None
    layer_name = relative_parts[0]
    if layer_name == "__init__.py":
        return None
    return layer_name


def iter_imported_names(module_path: Path) -> Iterable[str]:
    syntax_tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=str(module_path))
    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                yield node.module


def find_matching_prefix(imported_name: str, forbidden_prefixes: Iterable[str]) -> str | None:
    for forbidden_prefix in forbidden_prefixes:
        if imported_name == forbidden_prefix or imported_name.startswith(f"{forbidden_prefix}."):
            return forbidden_prefix
    return None
