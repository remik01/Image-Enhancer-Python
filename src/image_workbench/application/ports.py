"""Application-owned protocol ports for external capability boundaries."""

from __future__ import annotations

from typing import Protocol

from image_workbench.domain import (
    EnhancementOperationId,
    EnhancementPipeline,
    ImageId,
    PipelineStep,
)

from .results import (
    DiagnosticsEvent,
    ExecutionArtifact,
    ImageMetadata,
    ImageReference,
    SessionSnapshot,
)


class ImageProcessingPort(Protocol):
    """Execute a validated enhancement pipeline against a source image reference."""

    def execute_pipeline(
        self,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
        *,
        session_id: str,
    ) -> ExecutionArtifact: ...


class ImageSourceAccessPort(Protocol):
    """Resolve an application image reference from a domain image identifier."""

    def fetch_image_reference(self, image_id: ImageId) -> ImageReference: ...


class MetadataAccessPort(Protocol):
    """Read immutable image metadata needed for session setup and validation."""

    def fetch_metadata(self, image_id: ImageId) -> ImageMetadata: ...


class ExportWriterPort(Protocol):
    """Persist execution output to a target selected by caller-facing adapters."""

    def write_export(self, artifact: ExecutionArtifact, *, target: str) -> str: ...


class ProjectStoragePort(Protocol):
    """Persist and restore application session snapshots across process restarts."""

    def save_session_snapshot(self, snapshot: SessionSnapshot) -> None: ...

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot | None: ...


class AIInterpretationPort(Protocol):
    """Translate prompt intent into operation suggestions using internal model types."""

    def suggest_pipeline(self, prompt: str) -> tuple[PipelineStep, ...]: ...


class PluginDiscoveryPort(Protocol):
    """List enhancement operations exposed by discovered runtime plugins."""

    def discover_operations(self) -> tuple[EnhancementOperationId, ...]: ...


class QueueExecutionPort(Protocol):
    """Queue a pipeline execution request for asynchronous processing."""

    def enqueue_execution(
        self,
        *,
        session_id: str,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
    ) -> str: ...


class DiagnosticsPort(Protocol):
    """Record safe diagnostics events for application operational observability."""

    def record_event(self, event: DiagnosticsEvent) -> None: ...
