"""Pillow-backed histogram analysis behind a metadata adapter boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from image_workbench.domain import ImageId


class HistogramAnalysisError(OSError):
    """Raised when histogram analysis cannot be completed for a local image."""


@dataclass(frozen=True)
class ImageHistogram:
    """RGB histogram summary with fixed 256-bin channels."""

    image_id: ImageId
    red: tuple[int, ...]
    green: tuple[int, ...]
    blue: tuple[int, ...]

    def __post_init__(self) -> None:
        _require_channel(self.red, label="red")
        _require_channel(self.green, label="green")
        _require_channel(self.blue, label="blue")


class PillowHistogramAnalyzer:
    """Analyze local image histograms without exposing Pillow DTOs to core layers."""

    def analyze_histogram(self, source_path: Path | str) -> ImageHistogram:
        path = Path(source_path)
        try:
            with Image.open(path) as image:
                histogram = image.convert("RGB").histogram()
        except FileNotFoundError as exc:
            raise HistogramAnalysisError(f"Histogram source was not found: '{path}'.") from exc
        except PermissionError as exc:
            raise HistogramAnalysisError(f"Histogram source is not readable: '{path}'.") from exc
        except UnidentifiedImageError as exc:
            raise HistogramAnalysisError(
                f"Histogram source is not a supported image: '{path}'."
            ) from exc
        except OSError as exc:
            raise HistogramAnalysisError(f"Histogram could not be read from '{path}'.") from exc

        return ImageHistogram(
            image_id=ImageId(path.stem),
            red=tuple(histogram[0:256]),
            green=tuple(histogram[256:512]),
            blue=tuple(histogram[512:768]),
        )


def _require_channel(values: tuple[int, ...], *, label: str) -> None:
    if len(values) != 256:
        raise ValueError(f"Histogram {label} channel must contain 256 bins.")
    if any(value < 0 for value in values):
        raise ValueError(f"Histogram {label} channel counts must be non-negative.")
