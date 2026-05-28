"""Application services orchestrating session, pipeline, and execution workflows."""

from __future__ import annotations

from dataclasses import dataclass

from image_workbench.domain import (
    DomainValidationError,
    EnhancementPipeline,
    ImageDimensions,
    ImageId,
    PipelineHistory,
)

from .commands import (
    AddPipelineStepCommand,
    CreateSessionCommand,
    LoadImageReferenceCommand,
    MovePipelineStepCommand,
    RedoPipelineEditCommand,
    RemovePipelineStepCommand,
    ReplacePipelineStepCommand,
    RequestExecutionCommand,
    UndoPipelineEditCommand,
    ValidatePipelineProposalCommand,
)
from .exceptions import (
    ExecutionRequestError,
    ExternalDependencyError,
    InvalidCommandError,
    PipelineEditError,
    SessionNotFoundError,
)
from .ports import (
    DiagnosticsPort,
    ExportWriterPort,
    ImageProcessingPort,
    ImageSourceAccessPort,
    MetadataAccessPort,
    ProjectStoragePort,
    QueueExecutionPort,
)
from .results import (
    DiagnosticsEvent,
    ExecutionArtifact,
    ExecutionResult,
    ImageMetadata,
    ImageReference,
    PipelineValidationResult,
    SessionSnapshot,
)


@dataclass
class _SessionState:
    image_id: ImageId
    image_dimensions: ImageDimensions
    history: PipelineHistory
    image_reference: ImageReference | None = None


class SessionService:
    """Own application session lifecycle and immutable pipeline history state."""

    def __init__(
        self,
        *,
        metadata_port: MetadataAccessPort,
        image_source_port: ImageSourceAccessPort,
        project_storage_port: ProjectStoragePort | None = None,
        diagnostics_port: DiagnosticsPort | None = None,
    ) -> None:
        self._metadata_port = metadata_port
        self._image_source_port = image_source_port
        self._project_storage_port = project_storage_port
        self._diagnostics_port = diagnostics_port
        self._sessions: dict[str, _SessionState] = {}

    def create_session(self, command: CreateSessionCommand) -> SessionSnapshot:
        if command.session_id in self._sessions:
            raise InvalidCommandError(
                f"Session '{command.session_id}' already exists and cannot be recreated."
            )

        metadata = self._fetch_metadata(command.image_id)
        state = _SessionState(
            image_id=command.image_id,
            image_dimensions=metadata.dimensions,
            history=PipelineHistory.start(),
            image_reference=None,
        )
        self._sessions[command.session_id] = state
        snapshot = self.get_session_snapshot(command.session_id)
        try:
            self._persist_snapshot(snapshot)
        except ExternalDependencyError:
            del self._sessions[command.session_id]
            raise
        self._record_event("session.created", session_id=command.session_id)
        return snapshot

    def load_image_reference(self, command: LoadImageReferenceCommand) -> ImageReference:
        return self._get_or_load_image_reference(command.session_id)

    def get_session_snapshot(self, session_id: str) -> SessionSnapshot:
        state = self._require_session(session_id)
        history = state.history
        return SessionSnapshot(
            session_id=session_id,
            image_id=state.image_id,
            image_dimensions=state.image_dimensions,
            pipeline=history.present,
            can_undo=history.can_undo,
            can_redo=history.can_redo,
            source_uri=(
                state.image_reference.source_uri if state.image_reference is not None else None
            ),
        )

    def update_history(self, session_id: str, history: PipelineHistory) -> SessionSnapshot:
        state = self._require_session(session_id)
        previous_history = state.history
        state.history = history
        snapshot = self.get_session_snapshot(session_id)
        try:
            self._persist_snapshot(snapshot)
        except ExternalDependencyError:
            state.history = previous_history
            raise
        return snapshot

    def require_history(self, session_id: str) -> PipelineHistory:
        return self._require_session(session_id).history

    def require_image_reference(self, session_id: str) -> ImageReference:
        return self._get_or_load_image_reference(session_id)

    def _require_session(self, session_id: str) -> _SessionState:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise SessionNotFoundError(f"Session '{session_id}' was not found.") from exc

    def _fetch_metadata(self, image_id: ImageId) -> ImageMetadata:
        try:
            return self._metadata_port.fetch_metadata(image_id)
        except (ConnectionError, OSError, TimeoutError) as exc:
            raise ExternalDependencyError(
                f"Metadata lookup failed for image '{image_id.value}'."
            ) from exc

    def _get_or_load_image_reference(self, session_id: str) -> ImageReference:
        state = self._require_session(session_id)
        if state.image_reference is not None:
            return state.image_reference

        try:
            image_reference = self._image_source_port.fetch_image_reference(state.image_id)
        except (ConnectionError, OSError, TimeoutError) as exc:
            raise ExternalDependencyError(
                f"Image source lookup failed for image '{state.image_id.value}'."
            ) from exc
        state.image_reference = image_reference
        try:
            self._persist_snapshot(self.get_session_snapshot(session_id))
        except ExternalDependencyError:
            state.image_reference = None
            raise
        self._record_event("session.image-reference.loaded", session_id=session_id)
        return image_reference

    def _record_event(self, name: str, *, session_id: str) -> None:
        if self._diagnostics_port is None:
            return
        self._diagnostics_port.record_event(
            DiagnosticsEvent(name=name, details=(("session_id", session_id),))
        )

    def _persist_snapshot(self, snapshot: SessionSnapshot) -> None:
        if self._project_storage_port is None:
            return
        try:
            self._project_storage_port.save_session_snapshot(snapshot)
        except (ConnectionError, OSError, TimeoutError) as exc:
            raise ExternalDependencyError(
                f"Project storage save failed for session '{snapshot.session_id}'."
            ) from exc


class PipelineService:
    """Orchestrate immutable pipeline edits and undo/redo transitions per session."""

    def __init__(
        self,
        *,
        session_service: SessionService,
        diagnostics_port: DiagnosticsPort | None = None,
    ) -> None:
        self._session_service = session_service
        self._diagnostics_port = diagnostics_port

    def add_step(self, command: AddPipelineStepCommand) -> SessionSnapshot:
        history = self._session_service.require_history(command.session_id)
        try:
            updated = history.add_step(command.step, position=command.position)
        except DomainValidationError as exc:
            raise PipelineEditError(
                f"Add-step edit failed for session '{command.session_id}'."
            ) from exc
        snapshot = self._session_service.update_history(command.session_id, updated)
        self._record_event("pipeline.step-added", session_id=command.session_id)
        return snapshot

    def replace_step(self, command: ReplacePipelineStepCommand) -> SessionSnapshot:
        history = self._session_service.require_history(command.session_id)
        try:
            updated = history.replace_step(command.step)
        except DomainValidationError as exc:
            raise PipelineEditError(
                f"Replace-step edit failed for session '{command.session_id}'."
            ) from exc
        return self._session_service.update_history(command.session_id, updated)

    def remove_step(self, command: RemovePipelineStepCommand) -> SessionSnapshot:
        history = self._session_service.require_history(command.session_id)
        try:
            updated = history.remove_step(command.step_id)
        except DomainValidationError as exc:
            raise PipelineEditError(
                f"Remove-step edit failed for session '{command.session_id}'."
            ) from exc
        return self._session_service.update_history(command.session_id, updated)

    def move_step(self, command: MovePipelineStepCommand) -> SessionSnapshot:
        history = self._session_service.require_history(command.session_id)
        try:
            updated = history.move_step(command.step_id, position=command.position)
        except DomainValidationError as exc:
            raise PipelineEditError(
                f"Move-step edit failed for session '{command.session_id}'."
            ) from exc
        return self._session_service.update_history(command.session_id, updated)

    def undo(self, command: UndoPipelineEditCommand) -> SessionSnapshot:
        history = self._session_service.require_history(command.session_id)
        try:
            updated = history.undo()
        except DomainValidationError as exc:
            raise PipelineEditError(f"Undo failed for session '{command.session_id}'.") from exc
        return self._session_service.update_history(command.session_id, updated)

    def redo(self, command: RedoPipelineEditCommand) -> SessionSnapshot:
        history = self._session_service.require_history(command.session_id)
        try:
            updated = history.redo()
        except DomainValidationError as exc:
            raise PipelineEditError(f"Redo failed for session '{command.session_id}'.") from exc
        return self._session_service.update_history(command.session_id, updated)

    def validate_pipeline_proposal(
        self, command: ValidatePipelineProposalCommand
    ) -> PipelineValidationResult:
        try:
            normalized_pipeline = EnhancementPipeline(command.steps)
        except DomainValidationError as exc:
            return PipelineValidationResult(
                is_valid=False,
                errors=(str(exc),),
                normalized_pipeline=None,
            )
        return PipelineValidationResult(
            is_valid=True,
            errors=(),
            normalized_pipeline=normalized_pipeline,
        )

    def _record_event(self, name: str, *, session_id: str) -> None:
        if self._diagnostics_port is None:
            return
        self._diagnostics_port.record_event(
            DiagnosticsEvent(name=name, details=(("session_id", session_id),))
        )


class ExecutionService:
    """Orchestrate local or queued execution through application-owned ports."""

    def __init__(
        self,
        *,
        session_service: SessionService,
        image_processing_port: ImageProcessingPort,
        queue_execution_port: QueueExecutionPort | None = None,
        export_writer_port: ExportWriterPort | None = None,
        diagnostics_port: DiagnosticsPort | None = None,
    ) -> None:
        self._session_service = session_service
        self._image_processing_port = image_processing_port
        self._queue_execution_port = queue_execution_port
        self._export_writer_port = export_writer_port
        self._diagnostics_port = diagnostics_port

    def request_execution(self, command: RequestExecutionCommand) -> ExecutionResult:
        snapshot = self._session_service.get_session_snapshot(command.session_id)
        if len(snapshot.pipeline) == 0:
            raise ExecutionRequestError(
                f"Session '{command.session_id}' has no pipeline steps to execute."
            )
        image_reference = self._session_service.require_image_reference(command.session_id)

        if command.enqueue:
            queue_execution_port = self._queue_execution_port
            if queue_execution_port is None:
                raise ExecutionRequestError("Queue execution port is not configured.")
            ticket_id = self._enqueue_execution(
                session_id=command.session_id,
                image_reference=image_reference,
                pipeline=snapshot.pipeline,
                queue_execution_port=queue_execution_port,
            )
            self._record_event("execution.queued", session_id=command.session_id)
            return ExecutionResult(
                session_id=command.session_id,
                status="queued",
                artifact=None,
                queue_ticket_id=ticket_id,
            )

        artifact = self._run_execution(
            session_id=command.session_id,
            image_reference=image_reference,
            pipeline=snapshot.pipeline,
        )
        if command.export_target is not None:
            if self._export_writer_port is None:
                raise ExecutionRequestError("Export writer port is not configured.")
            exported_uri = self._write_export(artifact=artifact, target=command.export_target)
            artifact = ExecutionArtifact(
                session_id=artifact.session_id,
                output_image_id=artifact.output_image_id,
                applied_steps=artifact.applied_steps,
                exported_uri=exported_uri,
            )

        self._record_event("execution.completed", session_id=command.session_id)
        return ExecutionResult(
            session_id=command.session_id,
            status="completed",
            artifact=artifact,
            queue_ticket_id=None,
        )

    def _run_execution(
        self,
        *,
        session_id: str,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
    ) -> ExecutionArtifact:
        try:
            return self._image_processing_port.execute_pipeline(
                image_reference,
                pipeline,
                session_id=session_id,
            )
        except (ConnectionError, OSError, TimeoutError) as exc:
            raise ExternalDependencyError(
                f"Image processing failed for session '{session_id}'."
            ) from exc

    def _enqueue_execution(
        self,
        *,
        session_id: str,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
        queue_execution_port: QueueExecutionPort,
    ) -> str:
        try:
            return queue_execution_port.enqueue_execution(
                session_id=session_id,
                image_reference=image_reference,
                pipeline=pipeline,
            )
        except (ConnectionError, OSError, TimeoutError) as exc:
            raise ExternalDependencyError(
                f"Queue submission failed for session '{session_id}'."
            ) from exc

    def _write_export(self, *, artifact: ExecutionArtifact, target: str) -> str:
        export_writer_port = self._export_writer_port
        if export_writer_port is None:
            raise ExecutionRequestError("Export writer port is not configured.")
        try:
            return export_writer_port.write_export(artifact, target=target)
        except (ConnectionError, OSError, TimeoutError) as exc:
            raise ExternalDependencyError(
                f"Export write failed for session '{artifact.session_id}'."
            ) from exc

    def _record_event(self, name: str, *, session_id: str) -> None:
        if self._diagnostics_port is None:
            return
        self._diagnostics_port.record_event(
            DiagnosticsEvent(name=name, details=(("session_id", session_id),))
        )
