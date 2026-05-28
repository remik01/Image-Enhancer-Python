"""Pillow metadata reader that exposes only safe application metadata summaries."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from image_workbench.application.batch import BatchImageMetadata
from image_workbench.domain import ImageDimensions, ImageId


class MetadataReadError(OSError):
    """Raised when image metadata cannot be read from a local source."""


class PillowMetadataReader:
    """Read technical image metadata and map it into application-owned models."""

    def read_metadata(self, source_path: Path | str) -> BatchImageMetadata:
        path = Path(source_path)
        try:
            with Image.open(path) as image:
                format_name = image.format or "unknown"
                metadata_keys = tuple(str(key) for key in image.info)
                return BatchImageMetadata(
                    image_id=ImageId(path.stem),
                    dimensions=ImageDimensions(width=image.width, height=image.height),
                    format_name=format_name,
                    color_mode=image.mode,
                    metadata_keys=metadata_keys,
                )
        except FileNotFoundError as exc:
            raise MetadataReadError(f"Metadata source was not found: '{path}'.") from exc
        except PermissionError as exc:
            raise MetadataReadError(f"Metadata source is not readable: '{path}'.") from exc
        except UnidentifiedImageError as exc:
            raise MetadataReadError(f"Metadata source is not a supported image: '{path}'.") from exc
        except OSError as exc:
            raise MetadataReadError(f"Metadata could not be read from '{path}'.") from exc
