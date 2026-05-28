"""Schema constants and validation helpers for v1 project files."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
TOP_LEVEL_FIELDS = frozenset({"schema_version", "project", "images", "pipelines", "settings"})
PROJECT_FIELDS = frozenset({"session_id", "active_image_id"})
IMAGE_FIELDS = frozenset({"image_id", "source_uri", "dimensions"})
DIMENSIONS_FIELDS = frozenset({"width", "height"})
PIPELINE_FIELDS = frozenset({"image_id", "steps"})
STEP_FIELDS = frozenset({"step_id", "operation_id", "parameters"})
SECRET_FIELD_FRAGMENTS = (
    "api_key",
    "credential",
    "password",
    "secret",
    "signing_secret",
    "token",
)


class ProjectFileError(OSError):
    """Base failure for local project-file persistence."""


class ProjectFileValidationError(ProjectFileError):
    """Raised when a project file violates the v1 schema contract."""


class ProjectFileVersionError(ProjectFileValidationError):
    """Raised when a project file uses an unsupported schema version."""


def validate_project_document(document: object, *, source: Path) -> dict[str, object]:
    """Validate the outer project-file shape and return the typed mapping."""
    root = require_object(document, field_path="$", source=source)
    require_exact_fields(root, expected_fields=TOP_LEVEL_FIELDS, field_path="$", source=source)
    schema_version = require_int(
        root["schema_version"], field_path="$.schema_version", source=source
    )
    if schema_version != SCHEMA_VERSION:
        raise ProjectFileVersionError(
            f"Project file '{source}' uses unsupported schema_version {schema_version}; "
            f"expected {SCHEMA_VERSION}."
        )
    require_object(root["project"], field_path="$.project", source=source)
    require_array(root["images"], field_path="$.images", source=source)
    require_array(root["pipelines"], field_path="$.pipelines", source=source)
    settings = require_object(root["settings"], field_path="$.settings", source=source)
    if settings:
        first_key = next(iter(settings))
        if contains_secret_field(str(first_key)):
            raise ProjectFileValidationError(
                f"Project file '{source}' contains unsupported secret-like settings field "
                f"'$.settings.{first_key}'."
            )
        raise ProjectFileValidationError(
            f"Project file '{source}' contains unsupported v1 settings field "
            f"'$.settings.{first_key}'."
        )
    return root


def require_exact_fields(
    value: Mapping[str, object],
    *,
    expected_fields: frozenset[str],
    field_path: str,
    source: Path,
) -> None:
    """Reject missing or unknown fields before adapter DTO mapping proceeds."""
    actual_fields = set(value)
    missing_fields = sorted(expected_fields - actual_fields)
    if missing_fields:
        raise ProjectFileValidationError(
            f"Project file '{source}' is missing required field '{field_path}.{missing_fields[0]}'."
        )
    unknown_fields = sorted(actual_fields - expected_fields)
    if unknown_fields:
        unknown_field = unknown_fields[0]
        if contains_secret_field(unknown_field):
            raise ProjectFileValidationError(
                f"Project file '{source}' contains unsupported secret-like field "
                f"'{field_path}.{unknown_field}'."
            )
        raise ProjectFileValidationError(
            f"Project file '{source}' contains unknown field '{field_path}.{unknown_field}'."
        )


def require_object(value: object, *, field_path: str, source: Path) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' must be an object."
        )
    if not all(isinstance(key, str) for key in value):
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' object keys must be strings."
        )
    return value


def require_array(value: object, *, field_path: str, source: Path) -> list[object]:
    if not isinstance(value, list):
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' must be an array."
        )
    return value


def require_string(value: object, *, field_path: str, source: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' must be a non-empty string."
        )
    return value


def require_nullable_string(value: object, *, field_path: str, source: Path) -> str | None:
    if value is None:
        return None
    return require_string(value, field_path=field_path, source=source)


def require_int(value: object, *, field_path: str, source: Path) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' must be an integer."
        )
    return value


def require_number(value: object, *, field_path: str, source: Path) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' must be numeric."
        )
    return float(value)


def contains_secret_field(field_name: str) -> bool:
    normalized = field_name.casefold().replace("-", "_")
    return any(fragment in normalized for fragment in SECRET_FIELD_FRAGMENTS)


def ensure_json_object(value: Any) -> object:
    """Return loaded JSON while keeping callers from depending on raw decoder types."""
    return value
