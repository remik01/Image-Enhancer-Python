from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from image_workbench.adapters.filesystem import FilesystemImageSource, InvalidImageSourceError
from image_workbench.adapters.metadata import MetadataReadError
from image_workbench.application.batch import BatchImportCommand


def test_filesystem_image_source_imports_images_in_deterministic_name_order(tmp_path: Path) -> None:
    _write_image(tmp_path / "b.PNG")
    _write_image(tmp_path / "A.png")
    (tmp_path / "ignored.txt").write_text("ignored", encoding="utf-8")
    source = FilesystemImageSource()

    result = source.import_images(BatchImportCommand(source_location=str(tmp_path)))

    assert [image.source_name for image in result.images] == ["A.png", "b.PNG"]
    assert [image.metadata.dimensions.width for image in result.images] == [3, 3]


def test_filesystem_image_source_rejects_invalid_source_path(tmp_path: Path) -> None:
    source = FilesystemImageSource()

    with pytest.raises(InvalidImageSourceError, match="does not exist"):
        source.import_images(BatchImportCommand(source_location=str(tmp_path / "missing")))


def test_filesystem_image_source_reports_malformed_candidate(tmp_path: Path) -> None:
    malformed = tmp_path / "bad.png"
    malformed.write_text("not image content", encoding="utf-8")
    source = FilesystemImageSource()

    with pytest.raises(MetadataReadError, match="not a supported image"):
        source.import_images(BatchImportCommand(source_location=str(tmp_path)))


def test_filesystem_image_source_recurses_when_requested(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    _write_image(nested / "child.png")
    source = FilesystemImageSource()

    result = source.import_images(BatchImportCommand(source_location=str(tmp_path), recursive=True))

    assert [image.source_name for image in result.images] == ["child.png"]


def test_filesystem_image_source_handles_representative_batch_size(tmp_path: Path) -> None:
    for index in range(25, 0, -1):
        _write_image(tmp_path / f"image-{index:03d}.png")
    source = FilesystemImageSource()

    result = source.import_images(BatchImportCommand(source_location=str(tmp_path)))

    assert len(result.images) == 25
    assert result.images[0].source_name == "image-001.png"
    assert result.images[-1].source_name == "image-025.png"


def _write_image(path: Path) -> None:
    Image.new("RGB", (3, 2), color=(10, 20, 30)).save(path)
