from __future__ import annotations

import pytest

from image_workbench.domain import (
    DuplicatePipelineStepIdError,
    EnhancementOperationId,
    EnhancementPipeline,
    ImageDimensions,
    ImageId,
    InvalidImageDimensionsError,
    InvalidImageIdentifierError,
    InvalidOperationParametersError,
    InvalidParameterValueError,
    OperationParameters,
    PipelineOrderingError,
    PipelineStep,
    PipelineStepId,
    PipelineStepNotFoundError,
)


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )


def test_value_objects_validate_basic_construction_rules() -> None:
    assert ImageId(" image-1 ").value == "image-1"
    assert ImageDimensions(width=1920, height=1080) == ImageDimensions(width=1920, height=1080)

    with pytest.raises(InvalidImageIdentifierError):
        ImageId("  ")
    with pytest.raises(InvalidImageDimensionsError):
        ImageDimensions(width=0, height=100)
    with pytest.raises(InvalidParameterValueError):
        OperationParameters({"delta": True})


def test_pipeline_preserves_order_and_immutable_step_sequence() -> None:
    first = _step("s1", "brightness", {"delta": 0.3})
    second = _step("s2", "contrast", {"factor": 1.5})

    pipeline = EnhancementPipeline((first, second))

    assert tuple(step.step_id.value for step in pipeline.steps) == ("s1", "s2")
    assert isinstance(pipeline.steps, tuple)


def test_pipeline_rejects_duplicate_step_identifiers() -> None:
    duplicate_step_a = _step("dup", "brightness", {"delta": 0.2})
    duplicate_step_b = _step("dup", "contrast", {"factor": 1.3})

    with pytest.raises(DuplicatePipelineStepIdError):
        EnhancementPipeline((duplicate_step_a, duplicate_step_b))


def test_pipeline_rejects_invalid_insert_ordering_position() -> None:
    pipeline = EnhancementPipeline.empty()

    with pytest.raises(PipelineOrderingError):
        pipeline.add_step(_step("s1", "brightness", {"delta": 0.1}), position=2)


def test_pipeline_move_and_replace_operations_are_deterministic() -> None:
    first = _step("s1", "brightness", {"delta": 0.1})
    second = _step("s2", "contrast", {"factor": 1.2})
    third = _step("s3", "sharpen", {"amount": 0.5})

    pipeline = EnhancementPipeline((first, second, third))
    moved = pipeline.move_step(PipelineStepId("s3"), position=0)

    assert tuple(step.step_id.value for step in moved.steps) == ("s3", "s1", "s2")

    replaced = moved.replace_step(_step("s1", "saturation", {"factor": 2.0}))
    assert replaced.get_step(PipelineStepId("s1")).operation_id.value == "saturation"

    removed = replaced.remove_step(PipelineStepId("s2"))
    assert tuple(step.step_id.value for step in removed.steps) == ("s3", "s1")


def test_pipeline_reports_missing_step_for_replace_or_remove() -> None:
    pipeline = EnhancementPipeline.empty()

    with pytest.raises(PipelineStepNotFoundError):
        pipeline.remove_step(PipelineStepId("unknown"))
    with pytest.raises(PipelineStepNotFoundError):
        pipeline.replace_step(_step("unknown", "brightness", {"delta": 0.2}))


def test_pipeline_step_rejects_invalid_operation_parameters() -> None:
    with pytest.raises(InvalidOperationParametersError):
        _step("s1", "brightness", {"delta": 3.0})
