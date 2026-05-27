"""Undo/redo domain state transitions for immutable pipeline edits."""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import PipelineHistoryStateError
from .models import PipelineStepId
from .pipeline import EnhancementPipeline, PipelineStep


@dataclass(frozen=True)
class PipelineHistory:
    """Tracks immutable pipeline snapshots for deterministic undo/redo behavior."""

    past: tuple[EnhancementPipeline, ...]
    present: EnhancementPipeline
    future: tuple[EnhancementPipeline, ...]

    @classmethod
    def start(cls, initial_pipeline: EnhancementPipeline | None = None) -> PipelineHistory:
        """Create a history state with optional initial pipeline snapshot."""
        present = initial_pipeline if initial_pipeline is not None else EnhancementPipeline.empty()
        return cls(past=(), present=present, future=())

    @property
    def can_undo(self) -> bool:
        """True when an earlier snapshot is available."""
        return bool(self.past)

    @property
    def can_redo(self) -> bool:
        """True when a reverted snapshot is available."""
        return bool(self.future)

    def apply(self, pipeline: EnhancementPipeline) -> PipelineHistory:
        """Record a new present state and clear redo history."""
        if pipeline == self.present:
            return self
        return PipelineHistory(
            past=(*self.past, self.present),
            present=pipeline,
            future=(),
        )

    def add_step(self, step: PipelineStep, *, position: int | None = None) -> PipelineHistory:
        """Apply an add-step edit and record history transition."""
        return self.apply(self.present.add_step(step, position=position))

    def replace_step(self, step: PipelineStep) -> PipelineHistory:
        """Apply a replace-step edit and record history transition."""
        return self.apply(self.present.replace_step(step))

    def remove_step(self, step_id: PipelineStepId) -> PipelineHistory:
        """Apply a remove-step edit and record history transition."""
        return self.apply(self.present.remove_step(step_id))

    def move_step(self, step_id: PipelineStepId, *, position: int) -> PipelineHistory:
        """Apply a move-step edit and record history transition."""
        return self.apply(self.present.move_step(step_id, position=position))

    def undo(self) -> PipelineHistory:
        """Revert to the latest past snapshot."""
        if not self.past:
            raise PipelineHistoryStateError("Undo is not available because no past state exists.")

        previous_present = self.past[-1]
        return PipelineHistory(
            past=self.past[:-1],
            present=previous_present,
            future=(self.present, *self.future),
        )

    def redo(self) -> PipelineHistory:
        """Re-apply the latest reverted snapshot."""
        if not self.future:
            raise PipelineHistoryStateError("Redo is not available because no future state exists.")

        next_present = self.future[0]
        return PipelineHistory(
            past=(*self.past, self.present),
            present=next_present,
            future=self.future[1:],
        )
