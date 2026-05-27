from __future__ import annotations

from image_workbench.application import (
    AddPipelineStepCommand,
    CreateSessionCommand,
    MovePipelineStepCommand,
    PipelineService,
    RedoPipelineEditCommand,
    SessionService,
    UndoPipelineEditCommand,
    ValidatePipelineProposalCommand,
)
from image_workbench.application.results import ImageMetadata, ImageReference
from image_workbench.domain import (
    EnhancementOperationId,
    ImageDimensions,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)


class _FakeMetadataPort:
    def fetch_metadata(self, image_id: ImageId) -> ImageMetadata:
        return ImageMetadata(image_id=image_id, dimensions=ImageDimensions(width=1600, height=900))


class _FakeImageSourcePort:
    def fetch_image_reference(self, image_id: ImageId) -> ImageReference:
        return ImageReference(image_id=image_id, source_uri=f"memory://{image_id.value}")


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )


def _build_pipeline_service() -> PipelineService:
    session_service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_FakeImageSourcePort(),
    )
    return PipelineService(session_service=session_service)


def test_pipeline_service_orchestrates_edit_order_and_undo_redo() -> None:
    session_service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_FakeImageSourcePort(),
    )
    pipeline_service = PipelineService(session_service=session_service)

    session_service.create_session(
        CreateSessionCommand(session_id="session-1", image_id=ImageId("img-001"))
    )
    added_once = pipeline_service.add_step(
        AddPipelineStepCommand(
            session_id="session-1",
            step=_step("s1", "brightness", {"delta": 0.2}),
        )
    )
    added_twice = pipeline_service.add_step(
        AddPipelineStepCommand(
            session_id="session-1",
            step=_step("s2", "contrast", {"factor": 1.2}),
        )
    )

    moved = pipeline_service.move_step(
        MovePipelineStepCommand(
            session_id="session-1",
            step_id=PipelineStepId("s2"),
            position=0,
        )
    )
    assert tuple(step.step_id.value for step in moved.pipeline.steps) == ("s2", "s1")

    undone = pipeline_service.undo(UndoPipelineEditCommand(session_id="session-1"))
    assert tuple(step.step_id.value for step in undone.pipeline.steps) == ("s1", "s2")

    redone = pipeline_service.redo(RedoPipelineEditCommand(session_id="session-1"))
    assert tuple(step.step_id.value for step in redone.pipeline.steps) == ("s2", "s1")
    assert added_once.can_undo is True
    assert added_twice.can_undo is True


def test_pipeline_service_validates_pipeline_proposals_without_mutating_session() -> None:
    pipeline_service = _build_pipeline_service()
    result = pipeline_service.validate_pipeline_proposal(
        ValidatePipelineProposalCommand(
            session_id="session-x",
            steps=(
                _step("dup", "brightness", {"delta": 0.1}),
                _step("dup", "contrast", {"factor": 1.1}),
            ),
        )
    )

    assert result.is_valid is False
    assert result.normalized_pipeline is None
    assert result.errors
