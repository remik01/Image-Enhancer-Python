from __future__ import annotations

from image_workbench.application import (
    AddPipelineStepCommand,
    CreateSessionCommand,
    ExecutionService,
    PipelineService,
    RequestExecutionCommand,
    SessionService,
)
from image_workbench.application.results import ExecutionArtifact, ImageMetadata, ImageReference
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
        return ImageMetadata(image_id=image_id, dimensions=ImageDimensions(width=1200, height=800))


class _FakeImageSourcePort:
    def fetch_image_reference(self, image_id: ImageId) -> ImageReference:
        return ImageReference(image_id=image_id, source_uri=f"memory://{image_id.value}")


class _FakeImageProcessingPort:
    def execute_pipeline(
        self,
        image_reference: ImageReference,
        pipeline: object,
        *,
        session_id: str,
    ) -> ExecutionArtifact:
        del image_reference
        del pipeline
        return ExecutionArtifact(
            session_id=session_id,
            output_image_id=ImageId("out-001"),
            applied_steps=(PipelineStepId("s1"),),
        )


class _FakeQueueExecutionPort:
    def enqueue_execution(
        self, *, session_id: str, image_reference: object, pipeline: object
    ) -> str:
        del session_id
        del image_reference
        del pipeline
        return "queue-123"


class _FakeExportWriterPort:
    def write_export(self, artifact: ExecutionArtifact, *, target: str) -> str:
        del artifact
        return f"{target}\\rendered.png"


def _step() -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId("s1"),
        operation_id=EnhancementOperationId("brightness"),
        parameters=OperationParameters({"delta": 0.2}),
    )


def test_execution_service_completes_local_execution_and_export() -> None:
    session_service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_FakeImageSourcePort(),
    )
    pipeline_service = PipelineService(session_service=session_service)
    execution_service = ExecutionService(
        session_service=session_service,
        image_processing_port=_FakeImageProcessingPort(),
        export_writer_port=_FakeExportWriterPort(),
    )

    session_service.create_session(
        CreateSessionCommand(session_id="s-1", image_id=ImageId("img-1"))
    )
    pipeline_service.add_step(AddPipelineStepCommand(session_id="s-1", step=_step()))

    result = execution_service.request_execution(
        RequestExecutionCommand(session_id="s-1", export_target="C:\\exports")
    )

    assert result.status == "completed"
    assert result.artifact is not None
    assert result.artifact.exported_uri == "C:\\exports\\rendered.png"
    assert result.queue_ticket_id is None


def test_execution_service_queues_execution_when_requested() -> None:
    session_service = SessionService(
        metadata_port=_FakeMetadataPort(),
        image_source_port=_FakeImageSourcePort(),
    )
    pipeline_service = PipelineService(session_service=session_service)
    execution_service = ExecutionService(
        session_service=session_service,
        image_processing_port=_FakeImageProcessingPort(),
        queue_execution_port=_FakeQueueExecutionPort(),
    )

    session_service.create_session(
        CreateSessionCommand(session_id="s-2", image_id=ImageId("img-2"))
    )
    pipeline_service.add_step(AddPipelineStepCommand(session_id="s-2", step=_step()))

    result = execution_service.request_execution(
        RequestExecutionCommand(session_id="s-2", enqueue=True)
    )

    assert result.status == "queued"
    assert result.artifact is None
    assert result.queue_ticket_id == "queue-123"
