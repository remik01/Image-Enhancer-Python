from __future__ import annotations

import pytest

from image_workbench.application import (
    AddPipelineStepCommand,
    CreateSessionCommand,
    ExecutionRequestError,
    ExecutionService,
    ExternalDependencyError,
    InvalidCommandError,
    PipelineEditError,
    PipelineService,
    RequestExecutionCommand,
    SessionService,
)
from image_workbench.application.results import ExecutionArtifact, ImageMetadata, ImageReference
from image_workbench.domain import (
    EnhancementOperationId,
    EnhancementPipeline,
    ImageDimensions,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)


class _FailingMetadataPort:
    def fetch_metadata(self, image_id: ImageId) -> ImageMetadata:
        del image_id
        raise TimeoutError("metadata timeout")


class _FakeMetadataPort:
    def fetch_metadata(self, image_id: ImageId) -> ImageMetadata:
        return ImageMetadata(image_id=image_id, dimensions=ImageDimensions(width=1000, height=600))


class _FailingImageSourcePort:
    def fetch_image_reference(self, image_id: ImageId) -> ImageReference:
        del image_id
        raise OSError("source unavailable")


class _FailingImageProcessingPort:
    def execute_pipeline(
        self,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
        *,
        session_id: str,
    ) -> ExecutionArtifact:
        del image_reference
        del pipeline
        del session_id
        raise ConnectionError("processing offline")


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )


def test_create_session_translates_metadata_failures() -> None:
    service = SessionService(
        metadata_port=_FailingMetadataPort(),
        image_source_port=_FailingImageSourcePort(),
    )

    with pytest.raises(ExternalDependencyError, match="Metadata lookup failed"):
        service.create_session(CreateSessionCommand(session_id="s-fail", image_id=ImageId("img-3")))


def test_pipeline_edit_translates_domain_failures() -> None:
    session_service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_FailingImageSourcePort(),
    )
    pipeline_service = PipelineService(session_service=session_service)
    session_service.create_session(
        CreateSessionCommand(session_id="s-4", image_id=ImageId("img-4"))
    )

    pipeline_service.add_step(
        AddPipelineStepCommand(
            session_id="s-4",
            step=_step("dup", "brightness", {"delta": 0.1}),
        )
    )

    with pytest.raises(PipelineEditError, match="Add-step edit failed"):
        pipeline_service.add_step(
            AddPipelineStepCommand(
                session_id="s-4",
                step=_step("dup", "contrast", {"factor": 1.1}),
            )
        )


def test_execution_service_rejects_empty_pipeline_and_translates_processing_failure() -> None:
    session_service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_FailingImageSourcePort(),
    )
    execution_service = ExecutionService(
        session_service=session_service,
        image_processing_port=_FailingImageProcessingPort(),
    )
    session_service.create_session(
        CreateSessionCommand(session_id="s-5", image_id=ImageId("img-5"))
    )

    with pytest.raises(ExecutionRequestError, match="has no pipeline steps"):
        execution_service.request_execution(RequestExecutionCommand(session_id="s-5"))

    pipeline_service = PipelineService(session_service=session_service)
    pipeline_service.add_step(
        AddPipelineStepCommand(
            session_id="s-5",
            step=_step("s1", "brightness", {"delta": 0.2}),
        )
    )

    with pytest.raises(ExternalDependencyError, match="Image source lookup failed"):
        execution_service.request_execution(RequestExecutionCommand(session_id="s-5"))


def test_command_validation_rejects_blank_session_identifier() -> None:
    with pytest.raises(InvalidCommandError, match="Session identifier"):
        CreateSessionCommand(session_id="   ", image_id=ImageId("img-6"))
