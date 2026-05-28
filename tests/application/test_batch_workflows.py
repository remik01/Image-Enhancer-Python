from __future__ import annotations

import pytest

from image_workbench.application.batch import (
    BatchImage,
    BatchImageMetadata,
    BatchImportCommand,
    BatchImportResult,
    BatchWorkflowService,
)
from image_workbench.application.export import (
    BatchExportCommand,
    BatchExportResult,
    BatchExportService,
    ExportPreset,
    PlannedExport,
    plan_exports,
)
from image_workbench.application.results import ImageReference
from image_workbench.domain import ImageDimensions, ImageId


class _FakeBatchImageSourcePort:
    def import_images(self, command: BatchImportCommand) -> BatchImportResult:
        del command
        return BatchImportResult(images=(_batch_image("b"), _batch_image("a")))


class _FakeBatchExportWriterPort:
    def __init__(self) -> None:
        self.planned_exports: tuple[PlannedExport, ...] = ()

    def write_exports(
        self,
        planned_exports: tuple[PlannedExport, ...],
        *,
        preset: ExportPreset,
    ) -> BatchExportResult:
        del preset
        self.planned_exports = planned_exports
        return BatchExportResult(
            exported_uris=tuple(f"written://{export.output_name}" for export in planned_exports)
        )


def test_batch_workflow_service_delegates_to_image_source_port() -> None:
    service = BatchWorkflowService(image_source_port=_FakeBatchImageSourcePort())

    result = service.import_folder(BatchImportCommand(source_location="C:/images"))

    assert [image.image_reference.image_id.value for image in result.images] == ["b", "a"]


def test_plan_exports_uses_stable_order_and_output_names() -> None:
    command = BatchExportCommand(
        images=(_batch_image("first"), _batch_image("second")),
        preset=ExportPreset(
            destination="C:/exports",
            output_format="jpeg",
            filename_template="{index:03d}-{image_id}",
            conflict_policy="fail",
            strip_metadata=True,
        ),
    )

    planned = plan_exports(command)

    assert [export.output_name for export in planned] == ["001-first.jpg", "002-second.jpg"]
    assert [export.sequence_number for export in planned] == [1, 2]
    assert all(export.strip_metadata for export in planned)


def test_plan_exports_renames_duplicate_template_outputs_deterministically() -> None:
    command = BatchExportCommand(
        images=(_batch_image("a"), _batch_image("b"), _batch_image("c")),
        preset=ExportPreset(
            destination="C:/exports",
            filename_template="same-name",
            conflict_policy="rename",
        ),
    )

    planned = plan_exports(command)

    assert [export.output_name for export in planned] == [
        "same-name.png",
        "same-name-002.png",
        "same-name-003.png",
    ]


def test_plan_exports_preserves_dotted_stems_when_adding_extension() -> None:
    command = BatchExportCommand(
        images=(_batch_image("family.photo"),),
        preset=ExportPreset(
            destination="C:/exports",
            filename_template="{stem}",
            output_format="png",
        ),
    )

    planned = plan_exports(command)

    assert planned[0].output_name == "family.photo.png"


def test_plan_exports_replaces_known_image_extension_only() -> None:
    command = BatchExportCommand(
        images=(_batch_image("family.photo"),),
        preset=ExportPreset(
            destination="C:/exports",
            filename_template="{stem}.jpg",
            output_format="png",
        ),
    )

    planned = plan_exports(command)

    assert planned[0].output_name == "family.photo.png"


def test_plan_exports_rejects_duplicate_template_outputs_without_rename_policy() -> None:
    command = BatchExportCommand(
        images=(_batch_image("a"), _batch_image("b")),
        preset=ExportPreset(
            destination="C:/exports",
            filename_template="same-name",
            conflict_policy="fail",
        ),
    )

    with pytest.raises(ValueError, match="Duplicate output name"):
        plan_exports(command)


def test_batch_export_service_writes_planned_exports() -> None:
    writer = _FakeBatchExportWriterPort()
    service = BatchExportService(export_writer_port=writer)

    result = service.export_batch(
        BatchExportCommand(
            images=(_batch_image("image-1"),),
            preset=ExportPreset(destination="C:/exports"),
        )
    )

    assert result.exported_uris == ("written://001-image-1.png",)
    assert writer.planned_exports[0].output_name == "001-image-1.png"


def _batch_image(image_id: str) -> BatchImage:
    return BatchImage(
        image_reference=ImageReference(image_id=ImageId(image_id), source_uri=f"C:/{image_id}.png"),
        metadata=BatchImageMetadata(
            image_id=ImageId(image_id),
            dimensions=ImageDimensions(width=10, height=8),
            format_name="PNG",
            color_mode="RGB",
        ),
        source_name=f"{image_id}.png",
    )
