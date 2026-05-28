"""Filesystem JSON project-file storage for the application project port."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from image_workbench.application import SessionSnapshot

from .project_mapper import project_document_to_snapshot, snapshot_to_project_document
from .schema import ProjectFileError, ProjectFileValidationError, ensure_json_object


class ProjectFileStorage:
    """Persist one application session snapshot to a configured local project file."""

    def __init__(self, project_file: Path | str) -> None:
        self._project_file = Path(project_file)

    def save_session_snapshot(self, snapshot: SessionSnapshot) -> None:
        document = snapshot_to_project_document(snapshot)
        try:
            self._project_file.parent.mkdir(parents=True, exist_ok=True)
            self._project_file.write_text(
                _dumps_project_document(document),
                encoding="utf-8",
            )
        except OSError as exc:
            raise ProjectFileError(
                f"Project file '{self._project_file}' could not be written."
            ) from exc

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot | None:
        if not session_id.strip():
            raise ProjectFileValidationError("Session identifier must be a non-empty string.")
        if not self._project_file.exists():
            return None
        document = _load_project_document(self._project_file)
        snapshot = project_document_to_snapshot(document, source=self._project_file)
        if snapshot.session_id != session_id:
            return None
        return snapshot


def _load_project_document(project_file: Path) -> object:
    try:
        raw_text = project_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProjectFileError(f"Project file '{project_file}' could not be read.") from exc
    try:
        return ensure_json_object(json.loads(raw_text))
    except json.JSONDecodeError as exc:
        raise ProjectFileValidationError(
            f"Project file '{project_file}' is not valid JSON at line {exc.lineno}, "
            f"column {exc.colno}."
        ) from exc


def _dumps_project_document(document: dict[str, object]) -> str:
    return json.dumps(_ordered_for_json(document), indent=2, ensure_ascii=False) + "\n"


def _ordered_for_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _ordered_for_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_ordered_for_json(item) for item in value]
    return value
