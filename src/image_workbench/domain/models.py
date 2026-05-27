"""Domain value objects for image and pipeline identity plus operation parameters."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .exceptions import (
    InvalidImageDimensionsError,
    InvalidImageIdentifierError,
    InvalidOperationIdentifierError,
    InvalidParameterNameError,
    InvalidParameterValueError,
    InvalidPipelineStepIdentifierError,
)


def _require_non_empty_identifier(value: str, *, label: str, error_type: type[ValueError]) -> str:
    normalized = value.strip()
    if not normalized:
        raise error_type(f"{label} must be a non-empty string.")
    return normalized


@dataclass(frozen=True)
class ImageId:
    """Identifies an image inside a project domain workflow."""

    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty_identifier(
            self.value,
            label="Image identifier",
            error_type=InvalidImageIdentifierError,
        )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class ImageDimensions:
    """Represents immutable pixel dimensions for a logical image."""

    width: int
    height: int

    def __post_init__(self) -> None:
        if isinstance(self.width, bool) or self.width <= 0:
            raise InvalidImageDimensionsError("Image width must be a positive integer.")
        if isinstance(self.height, bool) or self.height <= 0:
            raise InvalidImageDimensionsError("Image height must be a positive integer.")


@dataclass(frozen=True)
class EnhancementOperationId:
    """Identifies an enhancement operation supported by the domain catalog."""

    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty_identifier(
            self.value,
            label="Operation identifier",
            error_type=InvalidOperationIdentifierError,
        )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class PipelineStepId:
    """Identifies a single ordered step in an enhancement pipeline."""

    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty_identifier(
            self.value,
            label="Pipeline step identifier",
            error_type=InvalidPipelineStepIdentifierError,
        )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class OperationParameters(Mapping[str, float]):
    """Immutable numeric parameter mapping used by operation validation."""

    _values: Mapping[str, float]

    def __init__(self, values: Mapping[str, float | int] | None = None) -> None:
        normalized_values: dict[str, float] = {}
        source = values if values is not None else {}

        for key, raw_value in source.items():
            if not key.strip():
                raise InvalidParameterNameError(
                    "Operation parameter names must be non-empty strings."
                )
            if isinstance(raw_value, bool):
                raise InvalidParameterValueError(
                    f"Parameter '{key}' must be numeric; bool values are not allowed."
                )

            try:
                numeric_value = float(raw_value)
            except (TypeError, ValueError) as exc:
                raise InvalidParameterValueError(
                    f"Parameter '{key}' must be a numeric value."
                ) from exc
            normalized_values[key] = numeric_value

        frozen_mapping = MappingProxyType(dict(sorted(normalized_values.items())))
        object.__setattr__(self, "_values", frozen_mapping)

    def __getitem__(self, key: str) -> float:
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def to_dict(self) -> dict[str, float]:
        """Return a detached mutable copy for callers that need mapping semantics."""
        return dict(self._values)
