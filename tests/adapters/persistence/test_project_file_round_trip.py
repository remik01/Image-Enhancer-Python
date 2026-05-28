from __future__ import annotations

from pathlib import Path

from image_workbench.adapters.persistence import ProjectFileStorage
from image_workbench.application import SessionSnapshot
from image_workbench.domain import (
    EnhancementOperationId,
    EnhancementPipeline,
    ImageDimensions,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures" / "projects"


def test_project_file_storage_round_trips_session_snapshot(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    storage = ProjectFileStorage(project_file)
    snapshot = _snapshot()

    storage.save_session_snapshot(snapshot)
    loaded = storage.load_session_snapshot("session-1")

    assert loaded == SessionSnapshot(
        session_id="session-1",
        image_id=ImageId("image-1"),
        image_dimensions=ImageDimensions(width=640, height=480),
        pipeline=snapshot.pipeline,
        can_undo=False,
        can_redo=False,
        source_uri="file:///images/image-1.png",
    )


def test_project_file_storage_serialization_is_deterministic(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    storage = ProjectFileStorage(project_file)
    snapshot = _snapshot()

    storage.save_session_snapshot(snapshot)
    first_write = project_file.read_text(encoding="utf-8")
    storage.save_session_snapshot(snapshot)
    second_write = project_file.read_text(encoding="utf-8")

    assert first_write == second_write


def test_project_file_storage_loads_valid_v1_fixture(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    project_file.write_text(
        (FIXTURE_ROOT / "valid-v1-project.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    storage = ProjectFileStorage(project_file)

    loaded = storage.load_session_snapshot("session-1")

    assert loaded is not None
    assert loaded.session_id == "session-1"
    assert loaded.image_id == ImageId("image-1")
    assert loaded.source_uri == "file:///images/image-1.png"
    assert [step.step_id.value for step in loaded.pipeline] == ["step-1", "step-2"]


def test_project_file_storage_returns_none_for_different_session_id(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    storage = ProjectFileStorage(project_file)
    storage.save_session_snapshot(_snapshot())

    assert storage.load_session_snapshot("other-session") is None


def test_project_file_storage_does_not_serialize_secret_like_fields(tmp_path: Path) -> None:
    project_file = tmp_path / "project.iwp.json"
    storage = ProjectFileStorage(project_file)

    storage.save_session_snapshot(_snapshot())

    serialized = project_file.read_text(encoding="utf-8").casefold()
    assert "secret" not in serialized
    assert "token" not in serialized
    assert "password" not in serialized
    assert "api_key" not in serialized


def _snapshot() -> SessionSnapshot:
    return SessionSnapshot(
        session_id="session-1",
        image_id=ImageId("image-1"),
        image_dimensions=ImageDimensions(width=640, height=480),
        pipeline=EnhancementPipeline(
            (
                _step("step-1", "brightness", {"delta": 0.25}),
                _step("step-2", "contrast", {"factor": 1.4}),
            )
        ),
        can_undo=True,
        can_redo=True,
        source_uri="file:///images/image-1.png",
    )


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )
