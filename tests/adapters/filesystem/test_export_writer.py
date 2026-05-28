from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image, PngImagePlugin

from image_workbench.adapters.filesystem import ExportConflictError, FilesystemExportWriter
from image_workbench.adapters.filesystem.export_writer import ExportWriterError
from image_workbench.application.batch import BatchImage, BatchImageMetadata
from image_workbench.application.export import BatchExportCommand, ExportPreset, plan_exports
from image_workbench.application.results import ImageReference
from image_workbench.domain import ImageDimensions, ImageId


def test_filesystem_export_writer_writes_in_planned_order_and_strips_metadata(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.png"
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Description", "should be stripped")
    Image.new("RGB", (2, 2), color=(12, 34, 56)).save(source, pnginfo=metadata)
    destination = tmp_path / "exports"
    command = BatchExportCommand(
        images=(_batch_image("img-1", source),),
        preset=ExportPreset(destination=str(destination), strip_metadata=True),
    )
    writer = FilesystemExportWriter()

    result = writer.write_exports(plan_exports(command), preset=command.preset)

    assert len(result.exported_uris) == 1
    output_path = Path(result.exported_uris[0])
    assert output_path.name == "001-img-1.png"
    with Image.open(output_path) as exported:
        assert exported.size == (2, 2)
        assert exported.info == {}


def test_filesystem_export_writer_preserves_png_text_metadata_when_requested(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.png"
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Description", "should be preserved")
    Image.new("RGB", (2, 2), color=(12, 34, 56)).save(source, pnginfo=metadata)
    command = BatchExportCommand(
        images=(_batch_image("img-1", source),),
        preset=ExportPreset(destination=str(tmp_path / "exports"), strip_metadata=False),
    )
    writer = FilesystemExportWriter()

    result = writer.write_exports(plan_exports(command), preset=command.preset)

    with Image.open(Path(result.exported_uris[0])) as exported:
        assert exported.info["Description"] == "should be preserved"


def test_filesystem_export_writer_fails_on_existing_output_when_policy_is_fail(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.png"
    _write_image(source)
    destination = tmp_path / "exports"
    destination.mkdir()
    (destination / "001-img-1.png").write_bytes(b"existing")
    command = BatchExportCommand(
        images=(_batch_image("img-1", source),),
        preset=ExportPreset(destination=str(destination), conflict_policy="fail"),
    )
    writer = FilesystemExportWriter()

    with pytest.raises(ExportConflictError, match="already exists"):
        writer.write_exports(plan_exports(command), preset=command.preset)


def test_filesystem_export_writer_renames_existing_output_deterministically(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.png"
    _write_image(source)
    destination = tmp_path / "exports"
    destination.mkdir()
    (destination / "001-img-1.png").write_bytes(b"existing")
    command = BatchExportCommand(
        images=(_batch_image("img-1", source),),
        preset=ExportPreset(destination=str(destination), conflict_policy="rename"),
    )
    writer = FilesystemExportWriter()

    result = writer.write_exports(plan_exports(command), preset=command.preset)

    assert Path(result.exported_uris[0]).name == "001-img-1-002.png"


def test_filesystem_export_writer_overwrites_existing_output_when_policy_allows(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.png"
    _write_image(source)
    destination = tmp_path / "exports"
    destination.mkdir()
    output_path = destination / "001-img-1.png"
    output_path.write_bytes(b"existing")
    command = BatchExportCommand(
        images=(_batch_image("img-1", source),),
        preset=ExportPreset(destination=str(destination), conflict_policy="overwrite"),
    )
    writer = FilesystemExportWriter()

    result = writer.write_exports(plan_exports(command), preset=command.preset)

    assert Path(result.exported_uris[0]) == output_path
    with Image.open(output_path) as exported:
        assert exported.size == (2, 2)


def test_filesystem_export_writer_translates_malformed_source(tmp_path: Path) -> None:
    source = tmp_path / "bad.png"
    source.write_text("not image content", encoding="utf-8")
    command = BatchExportCommand(
        images=(_batch_image("img-1", source),),
        preset=ExportPreset(destination=str(tmp_path / "exports")),
    )
    writer = FilesystemExportWriter()

    with pytest.raises(ExportWriterError, match="not a supported image"):
        writer.write_exports(plan_exports(command), preset=command.preset)


def test_filesystem_export_writer_translates_missing_source(tmp_path: Path) -> None:
    command = BatchExportCommand(
        images=(_batch_image("img-1", tmp_path / "missing.png"),),
        preset=ExportPreset(destination=str(tmp_path / "exports")),
    )
    writer = FilesystemExportWriter()

    with pytest.raises(ExportWriterError, match="not found"):
        writer.write_exports(plan_exports(command), preset=command.preset)


def _batch_image(image_id: str, source_path: Path) -> BatchImage:
    return BatchImage(
        image_reference=ImageReference(image_id=ImageId(image_id), source_uri=str(source_path)),
        metadata=BatchImageMetadata(
            image_id=ImageId(image_id),
            dimensions=ImageDimensions(width=2, height=2),
            format_name="PNG",
            color_mode="RGB",
        ),
        source_name=source_path.name,
    )


def _write_image(path: Path) -> None:
    Image.new("RGB", (2, 2), color=(12, 34, 56)).save(path)
