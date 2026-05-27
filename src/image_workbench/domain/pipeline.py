"""Immutable pipeline model with deterministic step ordering semantics."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from .exceptions import (
    DuplicatePipelineStepIdError,
    PipelineOrderingError,
    PipelineStepNotFoundError,
)
from .models import EnhancementOperationId, OperationParameters, PipelineStepId
from .operations import validate_operation_parameters


@dataclass(frozen=True)
class PipelineStep:
    """One validated operation invocation inside an ordered pipeline."""

    step_id: PipelineStepId
    operation_id: EnhancementOperationId
    parameters: OperationParameters

    def __post_init__(self) -> None:
        validate_operation_parameters(self.operation_id, self.parameters)


@dataclass(frozen=True)
class EnhancementPipeline:
    """Immutable ordered collection of validated pipeline steps."""

    _steps: tuple[PipelineStep, ...]

    def __init__(self, steps: Iterable[PipelineStep] = ()) -> None:
        immutable_steps = tuple(steps)
        _validate_no_duplicate_step_ids(immutable_steps)
        object.__setattr__(self, "_steps", immutable_steps)

    @classmethod
    def empty(cls) -> EnhancementPipeline:
        """Create an empty pipeline with no steps."""
        return cls()

    @property
    def steps(self) -> tuple[PipelineStep, ...]:
        """Expose immutable step ordering for callers and tests."""
        return self._steps

    def __iter__(self) -> Iterator[PipelineStep]:
        return iter(self._steps)

    def __len__(self) -> int:
        return len(self._steps)

    def get_step(self, step_id: PipelineStepId) -> PipelineStep:
        """Return a step by identifier or fail if it does not exist."""
        for step in self._steps:
            if step.step_id == step_id:
                return step
        raise PipelineStepNotFoundError(f"Pipeline step '{step_id.value}' was not found.")

    def add_step(self, step: PipelineStep, *, position: int | None = None) -> EnhancementPipeline:
        """Insert a new step at a deterministic position."""
        if any(existing_step.step_id == step.step_id for existing_step in self._steps):
            raise DuplicatePipelineStepIdError(
                f"Pipeline step identifier '{step.step_id.value}' already exists."
            )

        insertion_index = len(self._steps) if position is None else position
        if insertion_index < 0 or insertion_index > len(self._steps):
            raise PipelineOrderingError(
                f"Insert position {insertion_index} is outside pipeline bounds."
            )

        updated_steps = list(self._steps)
        updated_steps.insert(insertion_index, step)
        return EnhancementPipeline(updated_steps)

    def replace_step(self, step: PipelineStep) -> EnhancementPipeline:
        """Replace an existing step while preserving step ordering."""
        index = _find_step_index(self._steps, step.step_id)
        updated_steps = list(self._steps)
        updated_steps[index] = step
        return EnhancementPipeline(updated_steps)

    def remove_step(self, step_id: PipelineStepId) -> EnhancementPipeline:
        """Remove one step by identifier."""
        index = _find_step_index(self._steps, step_id)
        updated_steps = self._steps[:index] + self._steps[index + 1 :]
        return EnhancementPipeline(updated_steps)

    def move_step(self, step_id: PipelineStepId, *, position: int) -> EnhancementPipeline:
        """Move an existing step to a new ordering index."""
        if position < 0 or position >= len(self._steps):
            raise PipelineOrderingError(f"Move position {position} is outside pipeline bounds.")

        current_index = _find_step_index(self._steps, step_id)
        if current_index == position:
            return self

        mutable_steps = list(self._steps)
        step = mutable_steps.pop(current_index)
        mutable_steps.insert(position, step)
        return EnhancementPipeline(mutable_steps)


def _validate_no_duplicate_step_ids(steps: tuple[PipelineStep, ...]) -> None:
    seen: set[PipelineStepId] = set()
    for step in steps:
        if step.step_id in seen:
            raise DuplicatePipelineStepIdError(
                f"Pipeline step identifier '{step.step_id.value}' appears more than once."
            )
        seen.add(step.step_id)


def _find_step_index(steps: tuple[PipelineStep, ...], step_id: PipelineStepId) -> int:
    for index, step in enumerate(steps):
        if step.step_id == step_id:
            return index
    raise PipelineStepNotFoundError(f"Pipeline step '{step_id.value}' was not found.")
