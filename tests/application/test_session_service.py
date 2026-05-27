from __future__ import annotations

import pytest

from image_workbench.application import (
    CreateSessionCommand,
    ExternalDependencyError,
    InvalidCommandError,
    LoadImageReferenceCommand,
    SessionNotFoundError,
    SessionService,
)
from image_workbench.application.results import ImageMetadata, ImageReference, SessionSnapshot
from image_workbench.domain import (
    EnhancementOperationId,
    ImageDimensions,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)


class _CountingImageSourcePort:
    def __init__(self) -> None:
        self.calls = 0

    def fetch_image_reference(self, image_id: ImageId) -> ImageReference:
        self.calls += 1
        return ImageReference(image_id=image_id, source_uri=f"memory://{image_id.value}")


class _FakeMetadataPort:
    def fetch_metadata(self, image_id: ImageId) -> ImageMetadata:
        return ImageMetadata(image_id=image_id, dimensions=ImageDimensions(width=640, height=480))


class _FailingStoragePort:
    def save_session_snapshot(self, snapshot: SessionSnapshot) -> None:
        del snapshot
        raise TimeoutError("storage unavailable")

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot | None:
        del session_id
        return None


class _FailOnSecondSaveStoragePort:
    def __init__(self) -> None:
        self.saves = 0

    def save_session_snapshot(self, snapshot: SessionSnapshot) -> None:
        del snapshot
        self.saves += 1
        if self.saves >= 2:
            raise OSError("save failed")

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot | None:
        del session_id
        return None


def _step() -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId("s1"),
        operation_id=EnhancementOperationId("brightness"),
        parameters=OperationParameters({"delta": 0.1}),
    )


def test_load_image_reference_uses_cached_reference_after_first_fetch() -> None:
    image_source_port = _CountingImageSourcePort()
    service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=image_source_port,
    )
    service.create_session(CreateSessionCommand(session_id="session-1", image_id=ImageId("img-1")))

    first = service.load_image_reference(LoadImageReferenceCommand(session_id="session-1"))
    second = service.load_image_reference(LoadImageReferenceCommand(session_id="session-1"))

    assert first == second
    assert image_source_port.calls == 1


def test_create_session_rejects_duplicate_identifier() -> None:
    service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_CountingImageSourcePort(),
    )
    command = CreateSessionCommand(session_id="session-2", image_id=ImageId("img-2"))
    service.create_session(command)

    with pytest.raises(InvalidCommandError, match="already exists"):
        service.create_session(command)


def test_snapshot_flags_follow_history_state_transitions() -> None:
    service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_CountingImageSourcePort(),
    )
    service.create_session(CreateSessionCommand(session_id="session-3", image_id=ImageId("img-3")))

    initial = service.get_session_snapshot("session-3")
    updated_history = service.require_history("session-3").add_step(_step())
    updated = service.update_history("session-3", updated_history)

    assert initial.can_undo is False
    assert initial.can_redo is False
    assert updated.can_undo is True
    assert updated.can_redo is False


def test_create_session_rolls_back_when_storage_save_fails() -> None:
    service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_CountingImageSourcePort(),
        project_storage_port=_FailingStoragePort(),
    )

    with pytest.raises(ExternalDependencyError, match="Project storage save failed"):
        service.create_session(
            CreateSessionCommand(session_id="session-4", image_id=ImageId("img-4"))
        )

    with pytest.raises(SessionNotFoundError):
        service.get_session_snapshot("session-4")


def test_update_history_rolls_back_when_storage_save_fails() -> None:
    storage_port = _FailOnSecondSaveStoragePort()
    service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_CountingImageSourcePort(),
        project_storage_port=storage_port,
    )
    service.create_session(CreateSessionCommand(session_id="session-5", image_id=ImageId("img-5")))
    previous_snapshot = service.get_session_snapshot("session-5")

    with pytest.raises(ExternalDependencyError, match="Project storage save failed"):
        service.update_history("session-5", service.require_history("session-5").add_step(_step()))

    current_snapshot = service.get_session_snapshot("session-5")
    assert current_snapshot == previous_snapshot
