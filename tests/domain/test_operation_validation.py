from __future__ import annotations

import math

import pytest

from image_workbench.domain import (
    EnhancementOperationId,
    InvalidOperationParametersError,
    OperationParameters,
    UnsupportedOperationError,
    validate_operation_parameters,
)


def test_validate_operation_parameters_accepts_supported_operation_ranges() -> None:
    validate_operation_parameters(
        EnhancementOperationId("brightness"),
        OperationParameters({"delta": 0.25}),
    )


def test_validate_operation_parameters_rejects_unknown_operation() -> None:
    with pytest.raises(UnsupportedOperationError):
        validate_operation_parameters(
            EnhancementOperationId("unknown"),
            OperationParameters({"delta": 0.0}),
        )


def test_validate_operation_parameters_rejects_missing_required_parameter() -> None:
    with pytest.raises(InvalidOperationParametersError, match="Missing required parameters"):
        validate_operation_parameters(
            EnhancementOperationId("contrast"),
            OperationParameters(),
        )


def test_validate_operation_parameters_rejects_unexpected_parameter() -> None:
    with pytest.raises(InvalidOperationParametersError, match="Unexpected parameters"):
        validate_operation_parameters(
            EnhancementOperationId("saturation"),
            OperationParameters({"factor": 1.2, "unused": 0.4}),
        )


def test_validate_operation_parameters_rejects_out_of_range_value() -> None:
    with pytest.raises(InvalidOperationParametersError, match="must be between"):
        validate_operation_parameters(
            EnhancementOperationId("sharpen"),
            OperationParameters({"amount": 9.0}),
        )


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_validate_operation_parameters_rejects_non_finite_values(value: float) -> None:
    with pytest.raises(InvalidOperationParametersError, match="must be finite"):
        validate_operation_parameters(
            EnhancementOperationId("brightness"),
            OperationParameters({"delta": value}),
        )
