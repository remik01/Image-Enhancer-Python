from __future__ import annotations

import pytest

from image_workbench.domain import (
    EnhancementOperationId,
    OperationParameters,
    PipelineHistory,
    PipelineHistoryStateError,
    PipelineStep,
    PipelineStepId,
)


def _step(step_id: str, operation_id: str, parameters: dict[str, float]) -> PipelineStep:
    return PipelineStep(
        step_id=PipelineStepId(step_id),
        operation_id=EnhancementOperationId(operation_id),
        parameters=OperationParameters(parameters),
    )


def test_undo_rejects_empty_history_state() -> None:
    history = PipelineHistory.start()

    with pytest.raises(PipelineHistoryStateError, match="Undo is not available"):
        history.undo()


def test_single_edit_undo_redo_cycle_is_deterministic() -> None:
    history = PipelineHistory.start()
    edited = history.add_step(_step("s1", "brightness", {"delta": 0.2}))

    undone = edited.undo()
    assert len(undone.present.steps) == 0

    redone = undone.redo()
    assert tuple(step.step_id.value for step in redone.present.steps) == ("s1",)


def test_multi_step_undo_and_redo_behavior() -> None:
    history = PipelineHistory.start()
    first = history.add_step(_step("s1", "brightness", {"delta": 0.1}))
    second = first.add_step(_step("s2", "contrast", {"factor": 1.1}))
    third = second.add_step(_step("s3", "sharpen", {"amount": 0.4}))

    assert tuple(step.step_id.value for step in third.present.steps) == ("s1", "s2", "s3")

    undo_once = third.undo()
    assert tuple(step.step_id.value for step in undo_once.present.steps) == ("s1", "s2")

    undo_twice = undo_once.undo()
    assert tuple(step.step_id.value for step in undo_twice.present.steps) == ("s1",)

    redo_once = undo_twice.redo()
    assert tuple(step.step_id.value for step in redo_once.present.steps) == ("s1", "s2")


def test_redo_stack_is_cleared_after_new_edit() -> None:
    history = PipelineHistory.start()
    first = history.add_step(_step("s1", "brightness", {"delta": 0.2}))
    second = first.add_step(_step("s2", "contrast", {"factor": 1.4}))

    undone = second.undo()
    rewritten = undone.add_step(_step("s3", "saturation", {"factor": 0.8}))

    assert rewritten.can_redo is False
    with pytest.raises(PipelineHistoryStateError, match="Redo is not available"):
        rewritten.redo()
