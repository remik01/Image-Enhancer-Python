"""Domain operation catalog and parameter-range validation rules."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .exceptions import InvalidOperationParametersError, UnsupportedOperationError
from .models import EnhancementOperationId, OperationParameters


@dataclass(frozen=True)
class OperationParameterDefinition:
    """Describes an accepted numeric parameter range for an operation."""

    name: str
    minimum: float
    maximum: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise InvalidOperationParametersError(
                "Operation parameter definitions require a non-empty name."
            )
        if not isfinite(self.minimum) or not isfinite(self.maximum):
            raise InvalidOperationParametersError(
                f"Parameter range for '{self.name}' must use finite numeric limits."
            )
        if self.minimum > self.maximum:
            raise InvalidOperationParametersError(
                f"Parameter '{self.name}' has invalid range: minimum is greater than maximum."
            )


@dataclass(frozen=True)
class OperationDefinition:
    """Defines a supported operation and its required parameters."""

    operation_id: EnhancementOperationId
    parameters: tuple[OperationParameterDefinition, ...]

    def __post_init__(self) -> None:
        names = [parameter.name for parameter in self.parameters]
        unique_names = set(names)
        if len(names) != len(unique_names):
            raise InvalidOperationParametersError(
                f"Operation '{self.operation_id.value}' defines duplicate parameter names."
            )

    def parameter_names(self) -> tuple[str, ...]:
        """Return deterministic parameter-name ordering for validation and diagnostics."""
        return tuple(parameter.name for parameter in self.parameters)


_SUPPORTED_OPERATION_DEFINITIONS: tuple[OperationDefinition, ...] = (
    OperationDefinition(
        operation_id=EnhancementOperationId("blur"),
        parameters=(OperationParameterDefinition(name="radius", minimum=0.0, maximum=20.0),),
    ),
    OperationDefinition(
        operation_id=EnhancementOperationId("brightness"),
        parameters=(OperationParameterDefinition(name="delta", minimum=-1.0, maximum=1.0),),
    ),
    OperationDefinition(
        operation_id=EnhancementOperationId("contrast"),
        parameters=(OperationParameterDefinition(name="factor", minimum=0.1, maximum=3.0),),
    ),
    OperationDefinition(
        operation_id=EnhancementOperationId("saturation"),
        parameters=(OperationParameterDefinition(name="factor", minimum=0.0, maximum=3.0),),
    ),
    OperationDefinition(
        operation_id=EnhancementOperationId("sepia"),
        parameters=(OperationParameterDefinition(name="intensity", minimum=0.0, maximum=1.0),),
    ),
    OperationDefinition(
        operation_id=EnhancementOperationId("sharpen"),
        parameters=(OperationParameterDefinition(name="amount", minimum=0.0, maximum=5.0),),
    ),
)

_SUPPORTED_BY_OPERATION_ID: dict[str, OperationDefinition] = {
    definition.operation_id.value: definition for definition in _SUPPORTED_OPERATION_DEFINITIONS
}


def supported_operations() -> tuple[OperationDefinition, ...]:
    """Return all supported operation definitions in deterministic order."""
    return _SUPPORTED_OPERATION_DEFINITIONS


def resolve_operation_definition(operation_id: EnhancementOperationId) -> OperationDefinition:
    """Resolve an operation definition or fail with an unsupported-operation error."""
    try:
        return _SUPPORTED_BY_OPERATION_ID[operation_id.value]
    except KeyError as exc:
        raise UnsupportedOperationError(
            f"Unsupported operation identifier: '{operation_id.value}'."
        ) from exc


def validate_operation_parameters(
    operation_id: EnhancementOperationId,
    parameters: OperationParameters,
) -> None:
    """Validate provided parameter names and values against operation definition rules."""
    definition = resolve_operation_definition(operation_id)
    expected_names = definition.parameter_names()
    expected_name_set = set(expected_names)

    provided_names = tuple(parameters)
    provided_name_set = set(provided_names)

    missing_parameters = tuple(name for name in expected_names if name not in provided_name_set)
    unexpected_parameters = tuple(name for name in provided_names if name not in expected_name_set)

    if missing_parameters:
        raise InvalidOperationParametersError(
            f"Missing required parameters for '{operation_id.value}': {missing_parameters!r}."
        )
    if unexpected_parameters:
        raise InvalidOperationParametersError(
            f"Unexpected parameters for '{operation_id.value}': {unexpected_parameters!r}."
        )

    for parameter in definition.parameters:
        value = parameters[parameter.name]
        if not isfinite(value):
            raise InvalidOperationParametersError(
                f"Parameter '{parameter.name}' for '{operation_id.value}' "
                f"must be finite; got {value}."
            )
        if value < parameter.minimum or value > parameter.maximum:
            raise InvalidOperationParametersError(
                f"Parameter '{parameter.name}' for '{operation_id.value}' must be between "
                f"{parameter.minimum} and {parameter.maximum}; got {value}."
            )
