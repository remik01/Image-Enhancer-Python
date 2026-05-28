from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image, PngImagePlugin

from image_workbench.adapters.metadata import (
    HistogramAnalysisError,
    MetadataReadError,
    PillowHistogramAnalyzer,
    PillowMetadataReader,
)


def test_metadata_reader_maps_safe_metadata_summary(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Description", "fixture")
    Image.new("RGB", (4, 3), color=(1, 2, 3)).save(image_path, pnginfo=metadata)
    reader = PillowMetadataReader()

    result = reader.read_metadata(image_path)

    assert result.image_id.value == "sample"
    assert result.dimensions.width == 4
    assert result.dimensions.height == 3
    assert result.format_name == "PNG"
    assert result.color_mode == "RGB"
    assert result.metadata_keys == ("Description",)


def test_metadata_reader_rejects_malformed_image_with_source_context(tmp_path: Path) -> None:
    image_path = tmp_path / "broken.png"
    image_path.write_text("not image content", encoding="utf-8")
    reader = PillowMetadataReader()

    with pytest.raises(MetadataReadError, match="not a supported image"):
        reader.read_metadata(image_path)


def test_histogram_analyzer_returns_fixed_rgb_channels(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (2, 1), color=(10, 20, 30)).save(image_path)
    analyzer = PillowHistogramAnalyzer()

    histogram = analyzer.analyze_histogram(image_path)

    assert histogram.image_id.value == "sample"
    assert len(histogram.red) == 256
    assert len(histogram.green) == 256
    assert len(histogram.blue) == 256
    assert histogram.red[10] == 2
    assert histogram.green[20] == 2
    assert histogram.blue[30] == 2


def test_histogram_analyzer_rejects_missing_source(tmp_path: Path) -> None:
    analyzer = PillowHistogramAnalyzer()

    with pytest.raises(HistogramAnalysisError, match="not found"):
        analyzer.analyze_histogram(tmp_path / "missing.png")
