from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from image_workbench.adapters.image_processing import PillowImageProcessor
from image_workbench.application import ImageReference
from image_workbench.domain import (
    EnhancementOperationId,
    EnhancementPipeline,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)

MAX_CHANNEL_DELTA = 1

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures"
SOURCE_IMAGE = FIXTURE_ROOT / "images" / "baseline-source.png"
GOLDEN_ROOT = FIXTURE_ROOT / "golden"


@pytest.mark.parametrize(
    ("operation_id", "parameters", "golden_name"),
    [
        ("blur", {"radius": 1.0}, "blur-radius-1.png"),
        ("brightness", {"delta": 0.25}, "brightness-delta-0_25.png"),
        ("contrast", {"factor": 1.4}, "contrast-factor-1_4.png"),
        ("saturation", {"factor": 1.6}, "saturation-factor-1_6.png"),
        ("sepia", {"intensity": 0.75}, "sepia-intensity-0_75.png"),
        ("sharpen", {"amount": 1.5}, "sharpen-amount-1_5.png"),
    ],
)
def test_pillow_processor_matches_golden_baseline_operation(
    tmp_path: Path,
    operation_id: str,
    parameters: dict[str, float],
    golden_name: str,
) -> None:
    processor = PillowImageProcessor(output_directory=tmp_path)
    pipeline = EnhancementPipeline((_step("step-1", operation_id, parameters),))

    artifact = processor.execute_pipeline(
        ImageReference(image_id=ImageId("baseline-source"), source_uri=str(SOURCE_IMAGE)),
        pipeline,
        session_id="session-1",
    )

    assert artifact.applied_steps == (PipelineStepId("step-1"),)
    assert artifact.exported_uri is not None
    assert_images_match(Path(artifact.exported_uri), GOLDEN_ROOT / golden_name)


def test_pillow_processor_applies_pipeline_steps_in_order(tmp_path: Path) -> None:
    processor = PillowImageProcessor(output_directory=tmp_path)
    pipeline = EnhancementPipeline(
        (
            _step("step-1", "contrast", {"factor": 1.25}),
            _step("step-2", "blur", {"radius": 0.75}),
            _step("step-3", "sepia", {"intensity": 0.5}),
        )
    )

    artifact = processor.execute_pipeline(
        ImageReference(image_id=ImageId("baseline-source"), source_uri=str(SOURCE_IMAGE)),
        pipeline,
        session_id="session-2",
    )

    assert artifact.applied_steps == (
        PipelineStepId("step-1"),
        PipelineStepId("step-2"),
        PipelineStepId("step-3"),
    )
    assert artifact.exported_uri is not None
    assert_images_match(Path(artifact.exported_uri), GOLDEN_ROOT / "multi-step.png")


def assert_images_match(actual_path: Path, expected_path: Path) -> None:
    with Image.open(actual_path) as actual_image:
        actual_pixels = tuple(actual_image.convert("RGB").tobytes())
    with Image.open(expected_path) as expected_image:
        expected_pixels = tuple(expected_image.convert("RGB").tobytes())

    assert len(actual_pixels) == len(expected_pixels)
    for actual_channel, expected_channel in zip(actual_pixels, expected_pixels, strict=True):
        assert abs(actual_channel - expected_channel) <= MAX_CHANNEL_DELTA


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )
