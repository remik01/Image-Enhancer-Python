from __future__ import annotations

from pathlib import Path

import pytest

import image_workbench.adapters.image_processing.pillow_processor as pillow_processor
from image_workbench.adapters.image_processing import (
    ImageProcessingFailureError,
    ImageReadError,
    ImageWriteError,
    OperationMappingError,
    PillowImageProcessor,
    UnsupportedImageReferenceError,
)
from image_workbench.application import ImageReference
from image_workbench.domain import (
    EnhancementOperationId,
    EnhancementPipeline,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures"
SOURCE_IMAGE = FIXTURE_ROOT / "images" / "baseline-source.png"


def test_pillow_processor_rejects_unsupported_reference_scheme(tmp_path: Path) -> None:
    processor = PillowImageProcessor(output_directory=tmp_path)

    with pytest.raises(UnsupportedImageReferenceError, match="Unsupported image reference scheme"):
        processor.execute_pipeline(
            ImageReference(image_id=ImageId("image-1"), source_uri="memory://image-1"),
            EnhancementPipeline((_step("step-1", "contrast", {"factor": 1.0}),)),
            session_id="session-1",
        )


def test_pillow_processor_translates_missing_source_image(tmp_path: Path) -> None:
    processor = PillowImageProcessor(output_directory=tmp_path)

    with pytest.raises(ImageReadError, match="was not found") as exc_info:
        processor.execute_pipeline(
            ImageReference(
                image_id=ImageId("missing-image"),
                source_uri=str(tmp_path / "missing.png"),
            ),
            EnhancementPipeline((_step("step-1", "contrast", {"factor": 1.0}),)),
            session_id="session-1",
        )

    assert isinstance(exc_info.value.__cause__, FileNotFoundError)


def test_pillow_processor_translates_unsupported_image_format(tmp_path: Path) -> None:
    invalid_image = tmp_path / "not-an-image.txt"
    invalid_image.write_text("not image content", encoding="utf-8")
    processor = PillowImageProcessor(output_directory=tmp_path / "out")

    with pytest.raises(ImageReadError, match="unsupported format") as exc_info:
        processor.execute_pipeline(
            ImageReference(image_id=ImageId("invalid-image"), source_uri=str(invalid_image)),
            EnhancementPipeline((_step("step-1", "contrast", {"factor": 1.0}),)),
            session_id="session-1",
        )

    assert exc_info.value.__cause__ is not None


def test_pillow_processor_reports_invalid_operation_mapping(tmp_path: Path) -> None:
    processor = PillowImageProcessor(output_directory=tmp_path)

    with pytest.raises(OperationMappingError, match="Unsupported image-processing operation"):
        processor.execute_pipeline(
            ImageReference(image_id=ImageId("baseline-source"), source_uri=str(SOURCE_IMAGE)),
            EnhancementPipeline((_forged_step("step-1", "unknown", {}),)),
            session_id="session-1",
        )


def test_pillow_processor_reports_invalid_parameter_mapping(tmp_path: Path) -> None:
    processor = PillowImageProcessor(output_directory=tmp_path)

    with pytest.raises(OperationMappingError, match="Missing adapter parameter"):
        processor.execute_pipeline(
            ImageReference(image_id=ImageId("baseline-source"), source_uri=str(SOURCE_IMAGE)),
            EnhancementPipeline((_forged_step("step-1", "contrast", {}),)),
            session_id="session-1",
        )


def test_pillow_processor_translates_processing_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_operation(image: object) -> object:
        del image
        raise OSError("library failure")

    monkeypatch.setattr(
        pillow_processor,
        "map_step_to_pillow_operation",
        lambda step: fail_operation,
    )
    processor = PillowImageProcessor(output_directory=tmp_path)

    with pytest.raises(ImageProcessingFailureError, match="Image processing failed") as exc_info:
        processor.execute_pipeline(
            ImageReference(image_id=ImageId("baseline-source"), source_uri=str(SOURCE_IMAGE)),
            EnhancementPipeline((_step("step-1", "contrast", {"factor": 1.0}),)),
            session_id="session-1",
        )

    assert isinstance(exc_info.value.__cause__, OSError)


def test_pillow_processor_translates_output_write_failures(tmp_path: Path) -> None:
    output_file = tmp_path / "output-file"
    output_file.write_text("blocks directory creation", encoding="utf-8")
    processor = PillowImageProcessor(output_directory=output_file)

    with pytest.raises(ImageWriteError, match="could not be written") as exc_info:
        processor.execute_pipeline(
            ImageReference(image_id=ImageId("baseline-source"), source_uri=str(SOURCE_IMAGE)),
            EnhancementPipeline((_step("step-1", "contrast", {"factor": 1.0}),)),
            session_id="session-1",
        )

    assert isinstance(exc_info.value.__cause__, OSError)


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )


def _forged_step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    step = object.__new__(PipelineStep)
    object.__setattr__(step, "step_id", PipelineStepId(step_id))
    object.__setattr__(step, "operation_id", EnhancementOperationId(operation_id))
    object.__setattr__(step, "parameters", OperationParameters(parameters))
    return step
