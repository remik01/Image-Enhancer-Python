from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

from image_workbench.adapters.persistence import (
    ProjectFileStorage,
    ProjectFileValidationError,
    ProjectFileVersionError,
)

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures" / "projects"


def test_project_file_rejects_missing_required_field(tmp_path: Path) -> None:
    document = _valid_document()
    del document["settings"]
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match=r"\$\.settings"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_unknown_top_level_field(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    project_file.write_text(
        (FIXTURE_ROOT / "invalid-unknown-field.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match=r"\$\.unexpected"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_unknown_nested_field(tmp_path: Path) -> None:
    document = _valid_document()
    project = _project(document)
    project["unexpected"] = "value"
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match=r"\$\.project\.unexpected"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_incompatible_version(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    project_file.write_text(
        (FIXTURE_ROOT / "invalid-version.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileVersionError, match="unsupported schema_version 2"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_duplicate_step_identifiers(tmp_path: Path) -> None:
    document = _valid_document()
    steps = _steps(document)
    steps.append(steps[0] | {"operation_id": "contrast", "parameters": {"factor": 1.2}})
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="duplicate step_id 'step-1'"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_duplicate_image_identifiers(tmp_path: Path) -> None:
    document = _valid_document()
    images = _images(document)
    images.append(images[0].copy())
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="duplicate image_id 'image-1'"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_duplicate_pipeline_image_identifiers(tmp_path: Path) -> None:
    document = _valid_document()
    pipelines = _pipelines(document)
    pipelines.append(pipelines[0].copy())
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="duplicate pipeline image_id 'image-1'"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_malformed_dimensions(tmp_path: Path) -> None:
    document = _valid_document()
    _dimensions(document)["width"] = 0
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="invalid dimensions"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_invalid_operation_parameters(tmp_path: Path) -> None:
    document = _valid_document()
    _steps(document)[0]["parameters"] = {"delta": 5.0}
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="invalid pipeline step"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_non_empty_settings(tmp_path: Path) -> None:
    document = _valid_document()
    document["settings"] = {"theme": "dark"}
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match=r"\$\.settings\.theme"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_secret_like_settings(tmp_path: Path) -> None:
    document = _valid_document()
    document["settings"] = {"api_key": "not-allowed"}
    project_file = _write_project(tmp_path, document)
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="secret-like settings field"):
        storage.load_session_snapshot("session-1")


def test_project_file_rejects_invalid_json_with_source_context(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    project_file.write_text("{", encoding="utf-8")
    storage = ProjectFileStorage(project_file)

    with pytest.raises(ProjectFileValidationError, match="line 1, column 2"):
        storage.load_session_snapshot("session-1")


def _write_project(tmp_path: Path, document: dict[str, object]) -> Path:
    project_file = tmp_path / "project.iwp.json"
    project_file.write_text(json.dumps(document), encoding="utf-8")
    return project_file


def _valid_document() -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": {
            "session_id": "session-1",
            "active_image_id": "image-1",
        },
        "images": [
            {
                "image_id": "image-1",
                "source_uri": None,
                "dimensions": {"width": 640, "height": 480},
            }
        ],
        "pipelines": [
            {
                "image_id": "image-1",
                "steps": [
                    {
                        "step_id": "step-1",
                        "operation_id": "brightness",
                        "parameters": {"delta": 0.25},
                    }
                ],
            }
        ],
        "settings": {},
    }


def _project(document: dict[str, object]) -> dict[str, object]:
    return cast("dict[str, object]", document["project"])


def _images(document: dict[str, object]) -> list[dict[str, object]]:
    return cast("list[dict[str, object]]", document["images"])


def _dimensions(document: dict[str, object]) -> dict[str, object]:
    return cast("dict[str, object]", _images(document)[0]["dimensions"])


def _pipelines(document: dict[str, object]) -> list[dict[str, object]]:
    return cast("list[dict[str, object]]", document["pipelines"])


def _steps(document: dict[str, object]) -> list[dict[str, Any]]:
    return cast("list[dict[str, Any]]", _pipelines(document)[0]["steps"])
