"""Application models and service for deterministic batch image import."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from image_workbench.domain import ImageDimensions, ImageId

from .exceptions import InvalidCommandError
from .results import ImageReference


def _require_text(value: str, *, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise InvalidCommandError(f"{label} must be a non-empty string.")
    return normalized


@dataclass(frozen=True)
class BatchImportCommand:
    """Request image discovery from one caller-selected external location."""

    source_location: str
    recursive: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_location",
            _require_text(self.source_location, label="Batch source location"),
        )


@dataclass(frozen=True)
class BatchImageMetadata:
    """Safe metadata summary allowed to cross from metadata adapters into the app."""

    image_id: ImageId
    dimensions: ImageDimensions
    format_name: str
    color_mode: str
    metadata_keys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "format_name",
            _require_text(self.format_name, label="Image format"),
        )
        object.__setattr__(
            self,
            "color_mode",
            _require_text(self.color_mode, label="Image color mode"),
        )
        object.__setattr__(self, "metadata_keys", tuple(sorted(set(self.metadata_keys))))


@dataclass(frozen=True)
class BatchImage:
    """One deterministically ordered imported image and its safe metadata."""

    image_reference: ImageReference
    metadata: BatchImageMetadata
    source_name: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "source_name", _require_text(self.source_name, label="Source name")
        )


@dataclass(frozen=True)
class BatchImportResult:
    """Deterministic snapshot of imported images for downstream workflows."""

    images: tuple[BatchImage, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "images", tuple(self.images))


class BatchImageSourcePort(Protocol):
    """Discover images from an external batch source without leaking adapter DTOs."""

    def import_images(self, command: BatchImportCommand) -> BatchImportResult: ...


class BatchWorkflowService:
    """Coordinate batch import through an application-owned image source port."""

    def __init__(self, *, image_source_port: BatchImageSourcePort) -> None:
        self._image_source_port = image_source_port

    def import_folder(self, command: BatchImportCommand) -> BatchImportResult:
        """Import images while preserving the adapter's deterministic ordering contract."""
        return self._image_source_port.import_images(command)
