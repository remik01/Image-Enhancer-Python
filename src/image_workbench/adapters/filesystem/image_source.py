"""Filesystem-backed image discovery for batch import workflows."""

from __future__ import annotations

from pathlib import Path

from image_workbench.adapters.metadata.metadata_reader import (
    MetadataReadError,
    PillowMetadataReader,
)
from image_workbench.application.batch import (
    BatchImage,
    BatchImageMetadata,
    BatchImportCommand,
    BatchImportResult,
)
from image_workbench.application.results import ImageReference
from image_workbench.domain import ImageId

_SUPPORTED_IMAGE_EXTENSIONS = frozenset({".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff"})


class ImageSourceAdapterError(OSError):
    """Base failure for filesystem image source discovery."""


class InvalidImageSourceError(ImageSourceAdapterError):
    """Raised when a caller-selected image source path cannot be used safely."""


class FilesystemImageSource:
    """Discover local image files and map them into application batch models."""

    def __init__(self, *, metadata_reader: PillowMetadataReader | None = None) -> None:
        self._metadata_reader = metadata_reader or PillowMetadataReader()

    def import_images(self, command: BatchImportCommand) -> BatchImportResult:
        source_root = _normalize_existing_directory(command.source_location)
        paths = _discover_candidate_paths(source_root, recursive=command.recursive)
        images: list[BatchImage] = []
        for path in paths:
            metadata = self._metadata_reader.read_metadata(path)
            images.append(
                BatchImage(
                    image_reference=ImageReference(
                        image_id=metadata.image_id,
                        source_uri=str(path),
                    ),
                    metadata=metadata,
                    source_name=path.name,
                )
            )
        return BatchImportResult(images=tuple(images))


def _normalize_existing_directory(raw_location: str) -> Path:
    try:
        path = Path(raw_location).expanduser().resolve(strict=True)
    except OSError as exc:
        raise InvalidImageSourceError(
            f"Image source path does not exist: '{raw_location}'."
        ) from exc
    if not path.is_dir():
        raise InvalidImageSourceError(f"Image source path is not a directory: '{path}'.")
    return path


def _discover_candidate_paths(source_root: Path, *, recursive: bool) -> tuple[Path, ...]:
    iterator = source_root.rglob("*") if recursive else source_root.iterdir()
    paths = [
        path
        for path in iterator
        if path.is_file() and path.suffix.casefold() in _SUPPORTED_IMAGE_EXTENSIONS
    ]
    return tuple(sorted(paths, key=lambda path: (path.name.casefold(), str(path).casefold())))


def metadata_for_path(path: Path, metadata_reader: PillowMetadataReader) -> BatchImageMetadata:
    """Read metadata for tests and adapters that need the exact application model."""
    try:
        return metadata_reader.read_metadata(path)
    except MetadataReadError:
        raise


def image_id_for_path(path: Path) -> ImageId:
    """Create a stable image identifier from a discovered filesystem path."""
    return ImageId(path.stem)
