"""Immutable application results shared across orchestration boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from image_workbench.domain import (
    EnhancementOperationId,
    EnhancementPipeline,
    ImageDimensions,
    ImageId,
    PipelineStepId,
)


@dataclass(frozen=True)
class ImageReference:
    """Reference to source image content resolved by application-owned ports."""

    image_id: ImageId
    source_uri: str


@dataclass(frozen=True)
class ImageMetadata:
    """Metadata snapshot for one logical image managed by application workflows."""

    image_id: ImageId
    dimensions: ImageDimensions


@dataclass(frozen=True)
class SessionSnapshot:
    """Session state projection for deterministic UI/CLI/API rendering."""

    session_id: str
    image_id: ImageId
    image_dimensions: ImageDimensions
    pipeline: EnhancementPipeline
    can_undo: bool
    can_redo: bool
    source_uri: str | None = None


@dataclass(frozen=True)
class PipelineValidationResult:
    """Validation response for proposed pipeline edits before persistence/apply."""

    is_valid: bool
    errors: tuple[str, ...]
    normalized_pipeline: EnhancementPipeline | None


@dataclass(frozen=True)
class ExecutionArtifact:
    """Result metadata returned by an image-processing adapter execution."""

    session_id: str
    output_image_id: ImageId
    applied_steps: tuple[PipelineStepId, ...]
    exported_uri: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "applied_steps", tuple(self.applied_steps))


@dataclass(frozen=True)
class ExecutionResult:
    """Execution orchestration result for immediate or queued workflows."""

    session_id: str
    status: Literal["completed", "queued"]
    artifact: ExecutionArtifact | None
    queue_ticket_id: str | None = None


@dataclass(frozen=True)
class DiagnosticsEvent:
    """Safe, structured diagnostics event emitted from application services."""

    name: str
    details: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", tuple(self.details))


@dataclass(frozen=True)
class PipelineSuggestion:
    """AI-assisted proposal result represented in internal domain types."""

    operations: tuple[EnhancementOperationId, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "operations", tuple(self.operations))
        object.__setattr__(self, "notes", tuple(self.notes))
