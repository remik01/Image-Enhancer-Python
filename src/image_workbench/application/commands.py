"""Immutable application commands for session, pipeline, and execution workflows."""

from __future__ import annotations

from dataclasses import dataclass

from image_workbench.domain import ImageId, PipelineStep, PipelineStepId

from .exceptions import InvalidCommandError


def _require_non_empty_text(value: str, *, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise InvalidCommandError(f"{label} must be a non-empty string.")
    return normalized


@dataclass(frozen=True)
class CreateSessionCommand:
    """Create an application session bound to one image identifier."""

    session_id: str
    image_id: ImageId

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class LoadImageReferenceCommand:
    """Request the image reference for an existing session."""

    session_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class AddPipelineStepCommand:
    """Add one validated domain pipeline step to an existing session pipeline."""

    session_id: str
    step: PipelineStep
    position: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class ReplacePipelineStepCommand:
    """Replace an existing pipeline step by its step identifier."""

    session_id: str
    step: PipelineStep

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class RemovePipelineStepCommand:
    """Remove one pipeline step from a session pipeline."""

    session_id: str
    step_id: PipelineStepId

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class MovePipelineStepCommand:
    """Move one existing pipeline step to a deterministic position."""

    session_id: str
    step_id: PipelineStepId
    position: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class UndoPipelineEditCommand:
    """Undo one pipeline-edit operation in a session history."""

    session_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class RedoPipelineEditCommand:
    """Redo one previously undone pipeline-edit operation in session history."""

    session_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )


@dataclass(frozen=True)
class ValidatePipelineProposalCommand:
    """Validate a proposed pipeline snapshot against domain invariants."""

    session_id: str
    steps: tuple[PipelineStep, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )
        object.__setattr__(self, "steps", tuple(self.steps))


@dataclass(frozen=True)
class RequestExecutionCommand:
    """Request local or queued pipeline execution for an existing session."""

    session_id: str
    export_target: str | None = None
    enqueue: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "session_id",
            _require_non_empty_text(self.session_id, label="Session identifier"),
        )
        if self.export_target is not None:
            object.__setattr__(
                self,
                "export_target",
                _require_non_empty_text(self.export_target, label="Export target"),
            )
